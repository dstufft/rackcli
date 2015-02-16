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

from openstack import connection as osconn
from rackspace import user_preference


def determine_creds(ctx):
    """ because we could be looking at one profile, many profiles or an
    ovveride from the cli, look at the context object and pick which thing
    to use """

    region, user, passw = None, None, None
    profile = ctx.config.get(ctx.profile, None)
    if not profile:
        ctx.die('Profile supplied: %s, does not exist in %s',
                ctx.profile, ctx.cfgfile)
    region = profile.get('region').upper()
    user = profile.get('username')
    passw = profile.get('password')
    if ctx.region:
        region = ctx.region.upper()
    return region, user, passw


def conn(ctx):
    """ Return an *unvalidated* connection object """
    region, user, passw = determine_creds(ctx)
    pref = user_preference.UserPreference()
    pref.set_region(pref.ALL, region)
    conn = osconn.Connection(preference=pref,
                             auth_plugin="rackspace",
                             user_name=user,
                             api_key=passw)
    return conn
