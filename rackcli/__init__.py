# -*- coding: utf-8 -*-
from pkg_resources import get_distribution
# Temporarily monkey-patch until Identity gets the cert deployed right.
from requests.packages import urllib3
urllib3.disable_warnings()

__author__ = 'Jesse Noller'
__email__ = 'jesse.noller@rackspace.com'
__version__ = get_distribution('rackcli').version
