# -*- coding: utf-8 -*-

# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
"""
rackcli.py

"""
import os
import sys
import click
import config


class Context(object):
    """ Configuration context """
    def __init__(self):
        self.verbose = False
        self.interactive = False
        self.no_verify_ssl = False
        self.config = None
        self.cfgfile = None
        self.output = 'text'
        self.profile = None
        self.region = None

    def log(self, msg, *args):
        """Logs a message to stderr."""
        if args:
            msg %= args
        click.echo(msg, file=sys.stderr)

    def die(self, msg, *args):
        if args:
            msg %= args
        click.echo(msg, file=sys.stderr)
        sys.exit(1)

    def vlog(self, msg, *args):
        """Logs a message to stderr only if debug is enabled."""
        if self.verbose:
            self.log(msg, *args)


pass_ctx = click.make_pass_decorator(Context, ensure=True)
cmd_folder = os.path.join(os.path.dirname(__file__), 'commands')


class ComplexCLI(click.MultiCommand):

    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith('.py') and \
               filename.startswith('cmd_'):
                rv.append(filename[4:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            if sys.version_info[0] == 2:
                name = name.encode('ascii', 'replace')
            mod = __import__('rackcli.commands.cmd_' + name,
                             None, None, ['cli'])
        except ImportError:
            raise
        return mod.cli


@click.command(cls=ComplexCLI)
@click.version_option()
@click.option('--verbose', '-v', is_flag=True, default=False)
@click.option('--interactive', '-i', is_flag=True, default=False,
              help='If enabled, turn on pagination and prompts as needed')
@click.option('--no-verify-ssl', is_flag=True, default=False,
              help='Disable SSL - not recommended, considered harmful')
@click.option('--config-file', '-c', required=False,
              help='Optional Configuration file to use')
@click.option('--output', '-o', required=False, default='table',
              type=click.Choice(['json', 'text', 'table']),
              help='The formatting style for command output.')
@click.option('--profile', '-p', required=False, default='global',
              help='Use a specific profile from your credential file.')
@click.option('--region', '-r', required=False,
              help='The region to use. Overrides config/env settings.')
@pass_ctx
def cli(ctx, verbose, interactive, no_verify_ssl, config_file, output, profile,
        region):
    """ rackcli [options] <command> <subcommand> [parameters] """
    overrides = False
    ctx.verbose = verbose
    ctx.interactive = interactive
    ctx.no_verify_ssl = no_verify_ssl
    ctx.output = output
    ctx.profile = profile
    ctx.region = region
    if config_file:
        overrides = config.validate_path(config_file)
    ctx.config, ctx.cfgfile = config.load_config(ctx, overrides)
