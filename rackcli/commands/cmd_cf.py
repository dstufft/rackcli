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
from openstack.object_store.v1 import obj


@click.group(help='Cloud Files related commands.')
@pass_ctx
def cli(ctx):
    pass

"""
Container level operations
"""


@cli.command(name='containers', help='List all Cloud Files containers')
@pass_ctx
def list_containers(ctx):
    conn = auth.conn(ctx)
    if ctx.interactive:
        click.echo_via_pager('\n'.join('Container: %s' % c.name
                                       for c in conn.object_store.containers()
                                       ))
    else:
        for container in conn.object_store.containers():
            click.echo(container.name)


@cli.command(name='create-container', help='Create a container')
@click.argument('containername')
@pass_ctx
def create_container(ctx, containername):
    conn = auth.conn(ctx)
    conn.object_store.create_container(containername)


@cli.command(name='delete-container', help='Delete a container')
@click.argument('containername')
@pass_ctx
def delete_container(ctx, containername):
    conn = auth.conn(ctx)
    conn.object_store.delete_container(containername)


@cli.command(name='metadata-container', help='Get metadata about a container')
@click.argument('containername')
@pass_ctx
def metatadat_container(ctx, containername):
    conn = auth.conn(ctx)
    res = conn.object_store.get_container_metadata(containername)
    for e in res.items():
        click.echo('%s: %s' % (e[0], e[-1]))


@cli.command(name='bulkdelete-container',
             help='Recursively delete a container with the bulk delete command'
             )
@click.argument('containername')
@pass_ctx
def bulkddelete_container(ctx, containername):
    conn = auth.conn(ctx)
    conn.object_store.bulk_delete(containername)
    conn.object_store.delete_container(containername)

"""
Object level operations
"""


@cli.command(name='objects',
             help='List all objects in a Cloud Files container')
@click.argument('containername', required=True)
@pass_ctx
def list_objects(ctx, containername):
    conn = auth.conn(ctx)
    if ctx.interactive:
        click.echo_via_pager('\n'.join('Container: %s' % c.name
                                       for c in
                                       conn.object_store.objects(containername)
                                       ))
    else:
        for object in conn.object_store.objects(containername):
            click.echo(object.name)


@cli.command(name='metadata-object', help='Get metadata about an object')
@click.argument('containername', required=True)
@click.argument('objectname', required=True)
@pass_ctx
def metatadat_object(ctx, containername, objectname):

    # Hack around SDK interface
    oobj = obj.Object({"container": containername, "name": objectname})
    conn = auth.conn(ctx)
    res = conn.object_store.get_object_metadata(oobj)
    for e in res.items():
        click.echo('%s: %s' % (e[0], e[-1]))


@cli.command(name='delete-object', help='Delete an object from a container')
@click.argument('containername', required=True)
@click.argument('objectname', required=True)
@pass_ctx
def delete_object(ctx, containername, objectname):
    # Hack around SDK interface
    oobj = obj.Object({"container": containername, "name": objectname})
    conn = auth.conn(ctx)
    conn.object_store.delete_object(oobj)

"""
Not Implemented in SDK
@cli.command(name='copy-object', help='Copy an object from a container')
@click.argument('containername', required=True)
@click.argument('objectname', required=True)
@pass_ctx
def copy_object(ctx, containername, objectname):
    # Hack around SDK interface
    oobj = obj.Object({"container": containername, "name": objectname})
    conn = auth.conn(ctx)
    conn.object_store.copy_object(oobj)
"""


@cli.command(name='save-object', help='Save an object from a container')
@click.argument('containername', required=True)
@click.argument('objectname', required=True)
@click.argument('filepath', required=True)
@pass_ctx
def save_object(ctx, containername, objectname, filepath):
    # Hack around SDK interface
    oobj = obj.Object({"container": containername, "name": objectname})
    conn = auth.conn(ctx)
    # TODO: Add a progress bar, based on size? Num Chunks?
    conn.object_store.save_object(oobj, filepath)


@cli.command(name='create-object',
             help='Save a local file to the remote container & name/path')
@click.argument('containername', required=True)
@click.argument('objectname', required=True)
@click.argument('inputfile', required=True, type=click.File('rb', lazy=False))
@pass_ctx
def create_object(ctx, containername, objectname, inputfile):
    # Hack around SDK interface
    oobj = obj.Object({"container": containername, "name": objectname})
    conn = auth.conn(ctx)
    # TODO: Add a progress bar, based on size? Num Chunks?
    conn.object_store.create_object(inputfile, oobj)


@cli.command(name='data-object',
             help='Advanced: Get raw data from object from a container, \
prints to stdout')
@click.argument('containername', required=True)
@click.argument('objectname', required=True)
@pass_ctx
def data_object(ctx, containername, objectname, ):
    # Hack around SDK interface
    oobj = obj.Object({"container": containername, "name": objectname})
    conn = auth.conn(ctx)
    # TODO: Add a progress bar, based on size? Num Chunks?
    # TODO: This is insane.
    click.echo(conn.object_store.get_object_data(oobj))


"""
TBD:
conn.object_store.set_container_metadata
conn.object_store.set_object_metadata
conn.object_store.set_account_metadata
conn.object_store.get_account_metadata
"""
