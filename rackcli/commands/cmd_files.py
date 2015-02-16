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


# Try compiling things into a container command
@cli.command(name='container', help='Container Operations')
@click.option('--list', is_flag=True, required=False,
              help='List all Cloud Files containers')
@click.option('--create', is_flag=True, required=False,
              help='Create a Container')
@click.option('--delete', is_flag=True, required=False,
              help='Delete a Container')
@click.option('--metadata', is_flag=True, required=False,
              help='Get container metadata')
@click.argument('containername', required=False)
@pass_ctx
def container(ctx, list, containername, create, delete, metadata):
    conn = auth.conn(ctx)
    if list:
        if ctx.interactive:
            click.echo_via_pager('\n'.join('Container: %s' % c.name
                                           for c in
                                           conn.object_store.containers()))
        else:
            for container in conn.object_store.containers():
                click.echo(container.name)
    if create and containername:
        conn.object_store.create_container(containername)
    elif delete and containername:
        conn.object_store.delete_container(containername)
    elif metadata and containername:
        res = conn.object_store.get_container_metadata(containername)
        for e in res.items():
            click.echo('%s: %s' % (e[0], e[-1]))


@cli.command(name='object', help='Object Operations')
@click.option('--list', is_flag=True, required=False,
              help='List all objects in a container.')
@click.argument('containername', required=False)
@click.argument('objectname', required=False)
@pass_ctx
def objects(ctx, list, containername, objectname):
    conn = auth.conn(ctx)
    if list:
        if ctx.interactive:
            click.echo_via_pager('\n'.join('Container: %s' % c.name
                                           for c in
                                           conn.object_store.objects(containername)))
        else:
            for object in conn.object_store.objects(containername):
                click.echo(object.name)


"""
conn.object_store.bulk_delete             conn.object_store.get_object_data
conn.object_store.get_object_metadata
conn.object_store.copy_object             conn.object_store.objects
conn.object_store.save_object
conn.object_store.create_object           conn.object_store.session
        conn.object_store.set_account_metadata
conn.object_store.delete_object
conn.object_store.get_account_metadata    conn.object_store.set_object_metadata
"""
