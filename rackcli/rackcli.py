# -*- coding: utf-8 -*-

"""
rackcli.py

Apache License 2.0

Stuff
"""
import os
import sys
import click
import config


class Context(object):
    """ Configuration context """
    def __init__(self):
        self.verbose = False
        self.config = None

    def log(self, msg, *args):
        """Logs a message to stderr."""
        if args:
            msg %= args
        click.echo(msg, file=sys.stderr)

    def vlog(self, msg, *args):
        """Logs a message to stderr only if verbose is enabled."""
        if self.verbose:
            self.log(msg, *args)


pass_ctx = click.make_pass_decorator(Context, ensure=True)
cmd_folder = os.path.join(os.path.dirname(__file__), 'commands')


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    # how do I get this from __init__.py fml
    click.echo('0.1.1')
    ctx.exit()


class ComplexCLI(click.MultiCommand):

    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith('.py'):
                rv.append(filename[4:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            if sys.version_info[0] == 2:
                name = name.encode('ascii', 'replace')
            mod = __import__('complex.commands.cmd_' + name,
                             None, None, ['cli'])
        except ImportError:
            return
        return mod.cli


@click.command(cls=ComplexCLI)
@click.option('--debug', '-d', is_flag=True, default=False)
@click.option('--no-verify-ssl', is_flag=True, default=False,
              help='Disable SSL - not recommended, considered harmful')
@click.option('--config-file', '-c', required=False,
              help='Optional Configuration file to use')
@click.option('--output', '-o', required=False, default='table',
              type=click.Choice(['json', 'text', 'table']),
              help='The formatting style for command output.')
@click.option('--profile', '-p', required=False,
              help='Use a specific profile from your credential file.')
@click.option('--region', '-r', required=False,
              help='The region to use. Overrides config/env settings.')
@click.option('--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True)
@pass_ctx
def cli(ctx, debug, no_verify_ssl, config_file, output, profile, region):
    """ rackcli [options] <command> <subcommand> [parameters] """
    overrides = False
    if config_file:
        overrides = config.validate_path(config_file)
    # dump the loaded config - throwaway
    click.echo(config.load_config(debug, overrides))
    click.echo('Hello World')
