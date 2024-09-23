# Copyright (c) Huawei Technologies Co., Ltd. 2024, All rights reserved.
# Copyright 2022 The HuggingFace Team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import accelerate
from accelerate.utils import send_to_device
from accelerate.utils.megatron_lm import prepare_scheduler
from megatron import get_args, get_num_microbatches
from megatron.arguments import (
    core_transformer_config_from_args,
    parse_args,
    validate_args,
)
from megatron.checkpointing import (
    load_args_from_checkpoint,
    load_checkpoint,
    save_checkpoint,
)
from megatron.core import mpu, tensor_parallel
from megatron.core.distributed import (
    DistributedDataParallel as LocalDDP,
)
from megatron.core.distributed import (
    finalize_model_grads,
)
from megatron.core.enums import ModelType
from megatron.core.parallel_state import get_tensor_model_parallel_group, get_tensor_model_parallel_src_rank
from megatron.core.pipeline_parallel import get_forward_backward_func
from megatron.core.utils import get_model_config
from megatron.global_vars import set_global_variables
from megatron.initialize import (
    _compile_dependencies,
    _init_autoresume,
    _initialize_distributed,
    _set_random_seed,
    set_jit_fusion_options,
)
from megatron.model import BertModel, GPTModel, T5Model
from megatron.model.classification import Classification
from megatron.optimizer import get_megatron_optimizer
from megatron.tokenizer.tokenizer import _vocab_size_with_padding
from megatron.training import (
    build_train_valid_test_data_iterators,
    num_floating_point_operations,
    setup_model_and_optimizer,
    train_step,
    training_log,
)
from megatron.utils import (
    average_losses_across_data_parallel_group,
    calc_params_l2_norm,
    get_ltor_masks_and_position_ids,
)
import torch


def model_provider_func(pre_process=True, post_process=True, add_encoder=True, add_decoder=True):
    """Build the model."""
    args = get_args()
    if args.rank == 0:
        print(
            "The Megatron LM model weights are initialized at random in `accelerator.prepare`. "
            "Please use `accelerator.load_checkpoint` to load a pre-trained checkpoint matching the distributed setup."
        )
    config = core_transformer_config_from_args(args)
    if args.model_type_name == "bert":
        if args.pretraining_flag:
            num_tokentypes = 2 if args.bert_binary_head else 0
            model = BertModel(
                config=config,
                num_tokentypes=num_tokentypes,
                add_binary_head=args.bert_binary_head,
                parallel_output=True,
                pre_process=pre_process,
                post_process=post_process,
            )
        else:
            model = Classification(
                config=config,
                num_classes=args.num_labels,
                num_tokentypes=2,
                pre_process=pre_process,
                post_process=post_process,
            )
    elif args.model_type_name == "gpt":
        model = GPTModel(
            config=config,
            num_tokentypes=0,
            parallel_output=True,
            pre_process=pre_process,
            post_process=post_process,
        )
    elif args.model_type_name == "t5":
        model = T5Model(
            config=config,
            num_tokentypes=0,
            parallel_output=True,
            pre_process=pre_process,
            post_process=post_process,
            add_encoder=add_encoder,
            add_decoder=add_decoder,
        )
    else:
        raise ValueError(f"Unsupported model type: {args.model_type_name}")
    return model


def prepare_model_optimizer_scheduler(accelerator):
    accelerator.print("Preparing model optimizer scheduler")
    args = get_args()
    if accelerator.state.megatron_lm_plugin.custom_prepare_model_function is not None:
        if accelerator.state.megatron_lm_plugin.custom_model_provider_function is None:
            raise ValueError(
                "You must provide a `custom_model_provider_function` when using a `custom_prepare_model_function`."
            )
        custom_model_provider_func = accelerator.state.megatron_lm_plugin.custom_model_provider_function
        model = accelerator.state.megatron_lm_plugin.custom_prepare_model_function(custom_model_provider_func)
        optimizer = prepare_optimizer(accelerator, model)
        scheduler = prepare_scheduler(accelerator, optimizer, scheduler=None)
    else:
        model_type = ModelType.encoder_or_decoder
        if args.model_type_name == "t5":
            model_type = ModelType.encoder_and_decoder
        model_provider_func_ = model_provider_func
        if accelerator.state.megatron_lm_plugin.custom_model_provider_function is not None:
            model_provider_func_ = accelerator.state.megatron_lm_plugin.custom_model_provider_function
        (model, optimizer, scheduler) = setup_model_and_optimizer(
            model_provider_func_,
            model_type,
            no_wd_decay_cond=args.no_wd_decay_cond,
            scale_lr_cond=args.scale_lr_cond,
            lr_mult=args.lr_mult,
        )
    args.model_len = len(model)
    return model, optimizer, scheduler


class MegatronLMDummyDataLoader(accelerate.utils.MegatronLMDummyDataLoader):
    def set_megatron_data_args(self):
        args = get_args()
        for key, value in self.dataset_args.items():
            setattr(args, key, value)

    def get_train_valid_test_datasets_provider(self, accelerator):
        if accelerator.state.megatron_lm_plugin.custom_megatron_datasets_provider_function is not None:
            return accelerator.state.megatron_lm_plugin.custom_megatron_datasets_provider_function
        args = get_args()
        # Use '--no-use-pep517' to pip install nvidia's megatron from source
        if args.model_type_name == "bert":
            from pretrain_bert import train_valid_test_datasets_provider

            train_valid_test_datasets_provider.is_distributed = True
            return train_valid_test_datasets_provider
        elif args.model_type_name == "gpt":
            from pretrain_gpt import train_valid_test_datasets_provider

            train_valid_test_datasets_provider.is_distributed = True
            return train_valid_test_datasets_provider
        elif args.model_type_name == "t5":
            from pretrain_t5 import train_valid_test_datasets_provider

            train_valid_test_datasets_provider.is_distributed = True
            return train_valid_test_datasets_provider
        raise ValueError(f"Unsupported model type: {args.model_type_name}")

    def build_train_valid_test_data_iterators(self, accelerator):
        args = get_args()

        train_valid_test_dataset_provider = self.get_train_valid_test_datasets_provider(accelerator)
        if args.virtual_pipeline_model_parallel_size is not None:
            train_data_iterator = []
            valid_data_iterator = []
            test_data_iterator = []
            for i in range(getattr(args, "model_len", 0)):
                mpu.set_virtual_pipeline_model_parallel_rank(i)
                iterators = build_train_valid_test_data_iterators(train_valid_test_dataset_provider)
                train_data_iterator.append(iterators[0])
                valid_data_iterator.append(iterators[1])
                test_data_iterator.append(iterators[2])
        else:
            train_data_iterator, valid_data_iterator, test_data_iterator = build_train_valid_test_data_iterators(
                train_valid_test_dataset_provider
            )

        return train_data_iterator, valid_data_iterator, test_data_iterator


def _handle_megatron_data_iterator(accelerator, data_iterator):
    class DummyMegatronDataloader:
        def __iter__(self):
            return self

        def __next__(self):
            return {}

    is_data_iterator_empty = data_iterator is None
    is_src_data_iterator_empty = torch.tensor(is_data_iterator_empty, dtype=torch.bool, device=accelerator.device)
    torch.distributed.broadcast(
        is_src_data_iterator_empty, get_tensor_model_parallel_src_rank(), group=get_tensor_model_parallel_group()
    )
    if not is_src_data_iterator_empty and is_data_iterator_empty:
        return DummyMegatronDataloader()
    return data_iterator


def prepare_data_loader(accelerator, dataloader):
    accelerator.print("Preparing dataloader")
    args = get_args()
    if not args.megatron_dataset_flag:
        from accelerate.data_loader import _PYTORCH_DATALOADER_KWARGS, prepare_data_loader

        micro_batch_size = args.micro_batch_size * args.num_micro_batches
        kwargs = {k: getattr(dataloader, k, _PYTORCH_DATALOADER_KWARGS[k]) for k in _PYTORCH_DATALOADER_KWARGS}
        if kwargs["batch_size"] is None:
            if isinstance(kwargs["sampler"], torch.utils.data.BatchSampler):
                kwargs["sampler"].batch_size = micro_batch_size
            else:
                del kwargs["sampler"]
                del kwargs["shuffle"]
                del kwargs["batch_size"]
                kwargs["batch_sampler"].batch_size = micro_batch_size
        else:
            del kwargs["batch_sampler"]
            kwargs["batch_size"] = micro_batch_size

        dataloader = torch.utils.data.DataLoader(dataloader.dataset, **kwargs)
        # split_batches:
        # Megatron only needs to fetch different data between different dp groups,
        # and does not need to split the data within the dp group.
        return prepare_data_loader(
            dataloader,
            accelerator.device,
            num_processes=mpu.get_data_parallel_world_size(),
            process_index=mpu.get_data_parallel_rank(),
            split_batches=False,
            put_on_device=True,
            rng_types=accelerator.rng_types.copy(),
            dispatch_batches=accelerator.dispatch_batches,
        )
    else:
        if args.consumed_samples is not None:
            (
                args.consumed_train_samples,
                args.consumed_valid_samples,
                args.consumed_test_samples,
            ) = args.consumed_samples
        else:
            args.consumed_train_samples, args.consumed_valid_samples, args.consumed_test_samples = 0, 0, 0
        args.micro_batch_size = args.micro_batch_size * args.num_micro_batches
        # In order to be compatible with data in transform format,
        # it needs to increase the size of mbs first,
        # and then split the large batch data into some mbs.
        (
            train_data_iterator,
            valid_data_iterator,
            test_data_iterator,
        ) = dataloader.build_train_valid_test_data_iterators(accelerator)
        args.micro_batch_size = args.micro_batch_size // args.num_micro_batches

        train_data_iterator = _handle_megatron_data_iterator(accelerator=accelerator, data_iterator=train_data_iterator)
        valid_data_iterator = _handle_megatron_data_iterator(accelerator=accelerator, data_iterator=valid_data_iterator)
        test_data_iterator = _handle_megatron_data_iterator(accelerator=accelerator, data_iterator=test_data_iterator)

        return train_data_iterator, valid_data_iterator, test_data_iterator


def prepare_optimizer(accelerator, model):
    accelerator.print("Preparing optimizer")
    args = get_args()
    return get_megatron_optimizer(model, args.no_wd_decay_cond, args.scale_lr_cond, args.lr_mult)


class GPTTrainStep(accelerate.utils.megatron_lm.GPTTrainStep):
    def __init__(self, accelerator, args):
        super().__init__(args)
        self.get_batch = self.new_get_batch_func(accelerator, args.megatron_dataset_flag)
        self.loss_func = self.new_get_loss_func(accelerator)

    def new_get_batch_func(self, accelerator, megatron_dataset_flag):
        def get_batch_megatron(data_iterator):
            """Generate a batch"""
            # Items and their type.
            keys = ["text"]
            datatype = torch.int64

            # Broadcast data.
            if data_iterator is not None:
                data = next(data_iterator)
            else:
                data = None
            data_b = tensor_parallel.broadcast_data(keys, data, datatype)

            # Unpack.
            tokens_ = data_b["text"].long()
            labels = tokens_[:, 1:].contiguous()
            tokens = tokens_[:, :-1].contiguous()

            # Get the masks and postition ids.
            attention_mask, loss_mask, position_ids = get_ltor_masks_and_position_ids(
                tokens, self.eod_token, self.reset_position_ids, self.reset_attention_mask, self.eod_mask_loss
            )

            return tokens, labels, loss_mask, attention_mask, position_ids

        def get_batch_transformer(data_iterator):
            data = next(data_iterator)
            data = {"input_ids": data["input_ids"]}
            data = send_to_device(data, torch.cuda.current_device())

            tokens_ = data["input_ids"].long()
            padding = torch.zeros((tokens_.shape[0], 1), dtype=tokens_.dtype, device=tokens_.device) + self.eod_token
            tokens_ = torch.concat([tokens_, padding], dim=1)
            labels = tokens_[:, 1:].contiguous()
            tokens = tokens_[:, :-1].contiguous()
            # Get the masks and postition ids.
            attention_mask, loss_mask, position_ids = get_ltor_masks_and_position_ids(
                tokens, self.eod_token, self.reset_position_ids, self.reset_attention_mask, True
            )
            return tokens, labels, loss_mask, attention_mask, position_ids

        if accelerator.state.megatron_lm_plugin.custom_get_batch_function is not None:
            return accelerator.state.megatron_lm_plugin.custom_get_batch_function
        if megatron_dataset_flag:
            args = get_args()
            # Use '--no-use-pep517' to pip install nvidia's megatron from source
            if args.model_type_name == "bert":
                from pretrain_bert import get_batch

                return get_batch
            elif args.model_type_name == "gpt":
                from pretrain_gpt import get_batch

                return get_batch
            elif args.model_type_name == "t5":
                from pretrain_t5 import get_batch

                return get_batch
            return get_batch_megatron
        else:
            return get_batch_transformer

    def new_get_loss_func(self, accelerator):
        args = get_args()

        def loss_func(loss_mask, output_tensor):
            if args.return_logits:
                losses, logits = output_tensor
            else:
                losses = output_tensor
            losses = losses.float()
            loss_mask = loss_mask.view(-1).float()
            if args.context_parallel_size > 1:
                loss = torch.cat([torch.sum(losses.view(-1) * loss_mask).view(1), loss_mask.sum().view(1)])
                torch.distributed.all_reduce(loss, group=mpu.get_context_parallel_group())
                loss = loss[0] / loss[1]
            else:
                loss = torch.sum(losses.view(-1) * loss_mask) / loss_mask.sum()

            # Check individual rank losses are not NaN prior to DP all-reduce.
            if args.check_for_nan_in_loss_and_grad:
                global_rank = torch.distributed.get_rank()
                if loss.isnan():
                    raise ValueError(
                        f"Rank {global_rank}: found NaN in local forward loss calculation. "
                        f"Device: {torch.cuda.current_device()}, node: {os.uname()[1]}"
                    )

            # Reduce loss for logging.
            averaged_loss = average_losses_across_data_parallel_group([loss])

            output_dict = {"lm loss": averaged_loss[0]}
            if args.return_logits:
                output_dict.update({"logits": logits})
            return loss, output_dict

        if accelerator.state.megatron_lm_plugin.custom_loss_function is not None:
            return accelerator.state.megatron_lm_plugin.custom_loss_function
        return loss_func


def finish_mpu_init():
    # torch.distributed initialization
    args = get_args()
    # Pytorch distributed.
    _initialize_distributed()

    # Random seeds for reproducibility.
    _set_random_seed(args.seed, args.data_parallel_random_init)


def initialize(accelerator, extra_args_provider=None, args_defaults=None):
    if args_defaults is None:
        args_defaults = {}
    accelerator.print("Initializing Megatron-LM")
    if not torch.cuda.is_available():
        raise Exception("Megatron requires CUDA.")

    # Parse arguments
    args = parse_args(extra_args_provider, ignore_unknown_args=True)

    # Set defaults
    for key, value in args_defaults.items():
        setattr(args, key, value)

    if args.use_checkpoint_args or args_defaults.get("use_checkpoint_args", False):
        if args.load is None:
            raise ValueError("--use-checkpoints-args requires --load argument")
        load_args_from_checkpoint(args)

    validate_args(args)

    # set global args, build tokenizer, and set adlr-autoresume,
    # tensorboard-writer, and timers.
    set_global_variables(args)

    # Megatron's MPU is the master. Complete initialization right away.
    finish_mpu_init()

    # Autoresume.
    _init_autoresume()

    # Compile dependencies.
    _compile_dependencies()

    # Set pytorch JIT layer fusion options and warmup JIT functions.
    set_jit_fusion_options()
    args = get_args()
    if getattr(args, "padded_vocab_size", None) is None:
        args.padded_vocab_size = _vocab_size_with_padding(args.orig_vocab_size, args)
    if args.model_type_name == "bert" and args.pretraining_flag and args.num_labels == 2:
        args.bert_binary_head = True
    else:
        args.bert_binary_head = False
    args.iteration = 0


class MegatronEngine(accelerate.utils.megatron_lm.MegatronEngine):
    def __init__(self, accelerator, model, optimizer, scheduler):
        super().__init__(accelerator, model, optimizer, scheduler)
        args = get_args()
        if args.model_type_name == "gpt":
            self.train_step_handler = GPTTrainStep(accelerator, args)
        self.num_floating_point_operations_so_far = 0
        self.module_config = None

    def train(self):
        for model_module in self.module:
            model_module.train()

        if self.module_config is None:
            self.module_config = self.get_module_config()

        self.log_eval_results()

    def get_module_config(self):
        args = get_args()
        config = get_model_config(self.module[0])
        # Setup some training config params
        config.grad_scale_func = self.optimizer.scale_loss
        if isinstance(self.module[0], LocalDDP) and args.overlap_grad_reduce:
            if config.no_sync_func is not None:
                raise ValueError(
                    "When overlap_grad_reduce is True, config.no_sync_func must be None; "
                    "a custom no_sync_func is not supported when overlapping grad-reduce"
                )
            config.no_sync_func = [model_chunk.no_sync for model_chunk in self.module]
            if len(self.module) == 1:
                config.no_sync_func = config.no_sync_func[0]
            if args.delay_grad_reduce:
                config.grad_sync_func = [model_chunk.start_grad_sync for model_chunk in self.module]
                if len(self.module) == 1:
                    config.grad_sync_func = config.grad_sync_func[0]
        if args.overlap_param_gather and args.delay_param_gather:
            config.param_sync_func = [
                lambda x: self.optimizer.finish_param_sync(model_index, x) for model_index in range(len(self.module))
            ]
            if len(self.module) == 1:
                config.param_sync_func = config.param_sync_func[0]
        config.finalize_model_grads_func = finalize_model_grads
        return config

    def train_step(self, **batch_data):
        """
        Training step for Megatron-LM

        Args:
            batch_data (:obj:`dict`): The batch data to train on.
        """

        batch_data_iterator = self.get_batch_data_iterator(batch_data)

        loss_reduced, skipped_iter, grad_norm, num_zeros_in_grad = train_step(
            forward_step_func=self.train_step_handler.forward_step,
            data_iterator=batch_data_iterator,
            model=self.module,
            optimizer=self.optimizer,
            opt_param_scheduler=self.scheduler,
            config=self.module_config,
        )

        self.optimizer.skipped_iter = skipped_iter == 1

        return loss_reduced, skipped_iter, grad_norm, num_zeros_in_grad

    def eval(self):
        for model_module in self.module:
            model_module.eval()

        if self.module_config is None:
            self.module_config = self.get_module_config()

    def eval_step(self, **batch_data):
        """
        Evaluation step for Megatron-LM

        Args:
            batch_data (:obj:`dict`): The batch data to evaluate on.
        """

        args = get_args()
        batch_data_iterator = self.get_batch_data_iterator(batch_data)
        forward_backward_func = get_forward_backward_func()
        loss_dicts = forward_backward_func(
            forward_step_func=self.train_step_handler.forward_step,
            data_iterator=batch_data_iterator,
            model=self.module,
            num_microbatches=get_num_microbatches(),
            seq_length=args.seq_length,
            micro_batch_size=args.micro_batch_size,
            forward_only=True,
        )
        # Empty unused memory
        if args.empty_unused_memory_level >= 1:
            torch.cuda.empty_cache()

        args.consumed_valid_samples += (
            mpu.get_data_parallel_world_size() * args.micro_batch_size * get_num_microbatches()
        )

        if mpu.is_pipeline_last_stage(ignore_virtual=True):
            # Average loss across microbatches.
            loss_reduced = {}
            for key in loss_dicts[0]:
                losses_reduced_for_key = [x[key] for x in loss_dicts]
                if len(losses_reduced_for_key[0].shape) == 0:
                    loss_reduced[key] = sum(losses_reduced_for_key) / len(losses_reduced_for_key)
                else:
                    loss_reduced[key] = torch.concat(losses_reduced_for_key)
            return loss_reduced
        return {}

    def get_batch_data_iterator(self, batch_data):
        args = get_args()
        data_chunks = []
        if len(batch_data) > 0:
            if args.num_micro_batches > 1:
                for i in range(0, args.num_micro_batches):
                    data_chunks.append(
                        {
                            k: v[i * args.micro_batch_size : (i + 1) * args.micro_batch_size]
                            for k, v in batch_data.items()
                        }
                    )
            else:
                data_chunks = [batch_data]
        if len(self.module) > 1:
            batch_data_iterator = (
                [iter(data_chunks) for _ in range(len(self.module))]
                if len(batch_data) > 0
                else [None] * len(self.module)
            )
        else:
            batch_data_iterator = iter(data_chunks) if len(batch_data) > 0 else None
        return batch_data_iterator

    def forward(self, **batch_data):
        """
        During training, we use train_step()
        model(**batch_data) performs following operations by delegating it to `self.train_step`:
        1. Prepare **batch_data for Tendor, Pipeline and Model Parallelism
        2. Set grad to zero.
        3. forward pass and backward pass using Pipeline Parallelism
        4. Empty unused memory.
        5. Reduce gradients.
        6. Update parameters.
        7. Gather params when using Distributed Optimizer (Data Parallelism).
        8. Update learning rate if scheduler is specified.
        9. Empty unused memory.
        10. Average loss across microbatches and across DP ranks.

        During evaluation, we use eval_step()
        """
        args = get_args()
        if self.module[0].training:
            loss_dict, skipped_iter, grad_norm, num_zeros_in_grad = self.train_step(**batch_data)
            self.iteration += 1
            batch_size = mpu.get_data_parallel_world_size() * args.micro_batch_size * get_num_microbatches()
            args.consumed_train_samples += batch_size
            self.num_floating_point_operations_so_far += num_floating_point_operations(args, batch_size)
            if args.tensorboard_dir is not None:
                # Logging.
                loss_scale = self.optimizer.get_loss_scale().item()
                params_norm = None
                if args.log_params_norm:
                    params_norm = calc_params_l2_norm(self.model)
                self.report_memory_flag = training_log(
                    loss_dict,
                    self.total_loss_dict,
                    self.optimizer.param_groups[0]["lr"],
                    self.iteration,
                    loss_scale,
                    self.report_memory_flag,
                    skipped_iter,
                    grad_norm,
                    params_norm,
                    num_zeros_in_grad,
                )
        else:
            loss_dict = self.eval_step(**batch_data)
            if args.tensorboard_dir is not None:
                for key in loss_dict:
                    self.eval_total_loss_dict[key] = (
                        self.eval_total_loss_dict.get(key, torch.cuda.FloatTensor([0.0])) + loss_dict[key]
                    )
                    self.eval_total_loss_dict[key + "_num_iters"] = self.eval_total_loss_dict.get(
                        key + "_num_iters", torch.cuda.FloatTensor([0.0])
                    ) + torch.cuda.FloatTensor([1.0])

        loss = torch.tensor(0.0, device=torch.cuda.current_device())
        for key in loss_dict:
            if len(loss_dict[key].shape) == 0:
                loss += loss_dict[key]

        logits = None
        if "logits" in loss_dict:
            logits = loss_dict["logits"]
        if self.train_step_handler.model_output_class is not None:
            return self.train_step_handler.model_output_class(loss=loss, logits=logits)
        return loss

    def save_checkpoint(self, output_dir):
        self.log_eval_results()
        args = get_args()
        args.save = output_dir
        torch.distributed.barrier()
        save_checkpoint(
            self.iteration,
            self.module,
            self.optimizer,
            self.scheduler,
        )
        torch.distributed.barrier()

    def load_checkpoint(self, input_dir):
        args = get_args()
        args.load = input_dir
        args.consumed_train_samples = 0
        args.consumed_valid_samples = 0
        torch.distributed.barrier()
        iteration, num_floating_point_operations_so_far = load_checkpoint(self.module, self.optimizer, self.scheduler)
        torch.distributed.barrier()
        self.iteration = iteration
        self.num_floating_point_operations_so_far = num_floating_point_operations_so_far
        if args.fp16 and self.iteration == 0:
            self.optimizer.reload_model_params()


def apply_accelerate_megatron_lm_plugin():
    print("*" * 15 + f"PID:{os.getpid()} Applying the accelerate megatron-lm plugin." + "*" * 15)
    accelerate.utils.megatron_lm_prepare_model_optimizer_scheduler = prepare_model_optimizer_scheduler
    accelerate.accelerator.megatron_lm_prepare_model_optimizer_scheduler = prepare_model_optimizer_scheduler
    accelerate.utils.megatron_lm.prepare_model_optimizer_scheduler = prepare_model_optimizer_scheduler

    accelerate.utils.megatron_lm.MegatronLMDummyDataLoader = MegatronLMDummyDataLoader
    accelerate.utils.MegatronLMDummyDataLoader = MegatronLMDummyDataLoader
    accelerate.accelerator.MegatronLMDummyDataLoader = MegatronLMDummyDataLoader

    accelerate.utils.megatron_lm_prepare_data_loader = prepare_data_loader
    accelerate.accelerator.megatron_lm_prepare_data_loader = prepare_data_loader
    accelerate.utils.megatron_lm.prepare_data_loader = prepare_data_loader

    accelerate.utils.megatron_lm_initialize = initialize
    accelerate.accelerator.megatron_lm_initialize = initialize
    accelerate.utils.megatron_lm.initialize = initialize

    accelerate.utils.megatron_lm.MegatronEngine = MegatronEngine
    accelerate.utils.MegatronEngine = MegatronEngine
    accelerate.accelerator.MegatronEngine = MegatronEngine
