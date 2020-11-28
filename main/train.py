import os
from argparse import ArgumentParser
import torch
import pytorch_lightning as pl

from data import DataModule
from model import Model, get_model
from utils.preprocessing import tfms

def main():
    pl.seed_everything(1234)

    # ------------
    # args
    # ------------
    parser = ArgumentParser()
    parser = pl.Trainer.add_argparse_args(parser)
    parser = Model.add_model_specific_args(parser)
    args = parser.parse_args()

    # ------------
    # data
    # ------------
    dm = DataModule(tfms)

    # ------------
    # model
    # ------------
    model = Model(args.lr)

    # ------------
    # training
    # ------------
    trainer = pl.Trainer.from_argparse_args(
        # training settings
        args,
        distributed_backend='ddp',
        logger=wandb_logger,
        gpus=[2,3,4],
        # profiler=True,
        max_epochs=cfg.end_epoch

        # debug
        # fast_dev_run=True,
        limit_train_batches=10,
        limit_val_batches=1.0,

        # training tricks
        accumulate_grad_batches=10,
        early_stop_callback=early_stop_callback,
        precision=16, 
        benchmark=True
    )
    trainer.fit(model, dm)

    # ------------
    # testing
    # ------------
    trainer.test(model, datamodule=dm)


if __name__ == '__main__':
    main()