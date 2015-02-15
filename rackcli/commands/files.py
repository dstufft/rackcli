# -*- coding: utf-8 -*-
import click


@click.group(help='Handle Cloud Files commands.')
def cli():
    pass


@cli.command()
def pr():
    click.echo('got here')
