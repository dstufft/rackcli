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
import os
import ConfigParser

APP_NAME = 'rackcli'


def validate_path(ctx, value):
    if not value:
        return False
    elif not os.path.isfile(value):
        ctx.die('configuration file option invalid, %s is not a file.' % value)
    return value


def load_config(ctx, override):
    """ Pulls the rackcli configuration file and reads it if it exists
    otherwise, warn the user. Try a set of default paths, overridden if the
    user passes in one on the command line.
    """
    ctx.vlog('Loading raxcli config.ini file.')
    if override:
        validate_path(ctx, override)
    # todo: handle windows %user stuff
    config_home = os.environ.get('RX_CONFIG_HOME') or \
        os.path.expanduser('~/.config')
    if not override:
        possible_configs = [os.path.join(config_home, "rackcli", "config.ini"),
                            os.path.join(os.path.expanduser("~/.rackcli"),
                            "config.ini"),
                            os.path.join(".rackcli", "config.ini")]
    else:
        possible_configs = [override]
    for cfg in possible_configs:
        if os.path.isfile(cfg):
            ctx.vlog('%s is not a file', cfg)
            found = cfg
    parser = ConfigParser.RawConfigParser()
    parser.read([found])
    rv = {}
    for section in parser.sections():
        sect = {}
        for key, value in parser.items(section):
            sect[key] = value
        rv[section] = sect
    if not rv:
        ctx.vlog("Warning: could not parse %s." % found)
    ctx.vlog('Loaded %s', found)
    return rv, cfg
