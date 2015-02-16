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
import click
from rackcli.rackcli import pass_ctx
from rackcli import auth


@click.group(help='Cloud Files related commands.')
@pass_ctx
def cli(ctx):
    pass


@cli.command(name='containers')
@pass_ctx
def containers_list(ctx):

    conn = auth.conn(ctx)
    if ctx.interactive:
        click.echo_via_pager('\n'.join('Container: %s' % c.name
                                       for c in conn.object_store.containers()
                                       ))
    else:
        for container in conn.object_store.containers():
            click.echo(container.name)
