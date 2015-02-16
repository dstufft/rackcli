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
import glob
import os
import click
from rackcli.rackcli import pass_ctx
from rackcli import auth
from openstack.object_store.v1 import obj


@click.group(help='Cloud Files related commands.')
@pass_ctx
def cli(ctx):
    pass


"""
Cloudfile Level Account things
"""


@cli.command(name='metadata-account')
@pass_ctx
def metatadata_account(ctx):
    """ Retrieve Account-Level Cloud Files Metadata """
    conn = auth.conn(ctx)
    res = conn.object_store.get_account_metadata()
    for e in res.items():
        click.echo('%s: %s' % (e[0], e[-1]))

"""
Container level operations
"""


@cli.command(name='containers')
@pass_ctx
def list_containers(ctx):
    """List all Cloud Files containers for your specified region. If not in
    interactive mode, these are printed to stdout; interactive mode will
    paginate the output for you. """
    conn = auth.conn(ctx)
    if ctx.interactive:
        click.echo_via_pager('\n'.join('Container: %s' % c.name
                                       for c in conn.object_store.containers()
                                       ))
    else:
        for container in conn.object_store.containers():
            click.echo(container.name)


@cli.command(name='create-container')
@click.argument('containername')
@pass_ctx
def create_container(ctx, containername):
    """ Create a Cloud Files container """
    conn = auth.conn(ctx)
    conn.object_store.create_container(containername)


@cli.command(name='delete-container')
@click.argument('containername')
@pass_ctx
def delete_container(ctx, containername):
    """ Delete the specified container - note, if the container is not empty
    this operation will fail. See also bulkdelete-container for recursive
    with container removal. """
    conn = auth.conn(ctx)
    conn.object_store.delete_container(containername)


@cli.command(name='metadata-container')
@click.argument('containername')
@pass_ctx
def metatadata_container(ctx, containername):
    """Get the metadata about a container."""
    conn = auth.conn(ctx)
    res = conn.object_store.get_container_metadata(containername)
    for e in res.items():
        click.echo('%s: %s' % (e[0], e[-1]))


@cli.command(name='bulkdelete-container')
@click.argument('containername')
@pass_ctx
def bulkddelete_container(ctx, containername):
    """ Recursively deletes a container with the bulk delete command, all
    objects in the target container will be deleted as well as the container
    itself. """
    conn = auth.conn(ctx)
    conn.object_store.bulk_delete(containername)
    conn.object_store.delete_container(containername)

"""
Object level operations
"""


@cli.command(name='objects')
@click.argument('containername', required=True)
@pass_ctx
def list_objects(ctx, containername):
    """List all Cloud Files objects in the specified container. If not in
    interactive mode, these are printed to stdout; interactive mode will
    paginate the output for you. """
    conn = auth.conn(ctx)
    if ctx.interactive:
        click.echo_via_pager('\n'.join('Container: %s' % c.name
                                       for c in
                                       conn.object_store.objects(containername)
                                       ))
    else:
        for object in conn.object_store.objects(containername):
            click.echo(object.name)


@cli.command(name='metadata-object')
@click.argument('containername', required=True)
@click.argument('objectname', required=True)
@pass_ctx
def metatadata_object(ctx, containername, objectname):
    """Get the metadata about a specific object in the container, note that
    objects are stored container/<virtual path> - for example container/my/file
    the object identifier is my/file."""
    # Hack around SDK interface
    oobj = obj.Object({"container": containername, "name": objectname})
    conn = auth.conn(ctx)
    res = conn.object_store.get_object_metadata(oobj)
    for e in res.items():
        click.echo('%s: %s' % (e[0], e[-1]))


@cli.command(name='delete-object')
@click.argument('containername', required=True)
@click.argument('objectname', required=True)
@pass_ctx
def delete_object(ctx, containername, objectname):
    """Delete target object from the specified container"""
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


@cli.command(name='save-object')
@click.argument('containername', required=True)
@click.argument('objectname', required=True)
@click.argument('filepath', required=True)
@pass_ctx
def save_object(ctx, containername, objectname, filepath):
    """ Save the specified object to a local file (filepath) """
    # Hack around SDK interface
    oobj = obj.Object({"container": containername, "name": objectname})
    conn = auth.conn(ctx)
    # TODO: Add a progress bar, based on size? Num Chunks?
    conn.object_store.save_object(oobj, filepath)


@cli.command(name='create-object')
@click.argument('containername', required=True)
@click.argument('objectname', required=True)
@click.argument('inputfile', required=True, type=click.File('rb', lazy=False))
@pass_ctx
def create_object(ctx, containername, objectname, inputfile):
    """Upload a local file to the remote container with the specified
    objectname """
    # Hack around SDK interface
    oobj = obj.Object({"container": containername, "name": objectname})
    conn = auth.conn(ctx)
    # TODO: Add a progress bar, based on size? Num Chunks?
    conn.object_store.create_object(inputfile, oobj)


@cli.command(name='data-object')
@click.argument('containername', required=True)
@click.argument('objectname', required=True)
@pass_ctx
def data_object(ctx, containername, objectname):
    """Advanced: Get raw data from object from a container this data
    prints to stdout. This means if it's binary data you're going to have a
    bad time."""
    # Hack around SDK interface
    oobj = obj.Object({"container": containername, "name": objectname})
    conn = auth.conn(ctx)
    # TODO: Add a progress bar, based on size? Num Chunks?
    # TODO: This is insane.
    click.echo(conn.object_store.get_object_data(oobj))


@cli.command(name='upload-dir')
@click.argument('directory', required=True)
@click.argument('pattern', required=True)
@pass_ctx
def upload_directory(ctx, directory, pattern):
    """Upload a directory to a container named after the specified directory to
    Cloud Files. The pattern is a valid "glob" pattern - e.g *.* or *.mp3. The
    directory name will be the container, and sub directories will become paths
    within the parent container (not new containers).
    """
    container_name = os.path.basename(os.path.realpath(directory))
    conn = auth.conn(ctx)
    conn.object_store.create_container(container_name.decode("utf8"))

    for root, dirs, files in os.walk(directory):
        for file in glob.iglob(os.path.join(root, pattern)):
            with open(file, "rb") as f:
                conn.object_store.create_object(data=f.read(),
                                                obj=file.decode("utf8"),
                                                container=container_name)
                click.echo('Uploaded: %s' % file)


"""
TBD:
conn.object_store.set_container_metadata
conn.object_store.set_object_metadata
conn.object_store.set_account_metadata


from openstack.object_store.v1 import container, obj

cn = obj.Container({"name": "my container"})
cn.read_ACL = "asdfasdfas"
conn.set_container_metadata(cn)

ob = obj.Object({"container": "my container", "object": "my object"})
ob.content_type = "asdfasdfasdf"
conn.set_object_metadata(ob)
"""
