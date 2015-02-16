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


@cli.command(name='containers', help='List all Cloud Files containers')
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


@cli.command(name='container_create', help='Create a container')
@click.argument('containername')
@pass_ctx
def container_create(ctx, containername):
    conn = auth.conn(ctx)
    conn.object_store.create_container(containername)


@cli.command(name='container_delete', help='Delete a container')
@click.argument('containername')
@pass_ctx
def container_delete(ctx, containername):
    conn = auth.conn(ctx)
    conn.object_store.create_container(containername)


@cli.command(name='container_metadata', help='Get metadata about a container')
@click.argument('containername')
@pass_ctx
def container_metadata(ctx, containername):
    conn = auth.conn(ctx)
    res = conn.object_store.get_container_metadata(containername)
    for e in res.items():
        click.echo('%s: %s' % (e[0], e[-1]))



"""
conn.object_store.bulk_delete             conn.object_store.get_object_data
conn.object_store.get_object_metadata
conn.object_store.copy_object             conn.object_store.objects
conn.object_store.save_object
conn.object_store.create_object           conn.object_store.session
conn.object_store.delete_container        conn.object_store.set_account_metadata
conn.object_store.delete_object
conn.object_store.get_account_metadata    conn.object_store.set_object_metadata
"""
