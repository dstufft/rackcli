# -*- coding: utf-8 -*-
import click
from rackcli.rackcli import pass_ctx


@click.group(help='Cloud Files related commands.')
@pass_ctx
def cli(ctx):
    pass


@cli.command(name='dog')
@pass_ctx
def migrate_label(ctx):
    ctx.log('got here')
