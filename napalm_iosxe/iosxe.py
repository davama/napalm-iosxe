# Copyright 2017 Jive Communications Inc. All rights reserved.
#
# The contents of this file are licensed under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with the
# License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

"""
Napalm driver for IOS-XE using NETCONF.

Read https://napalm.readthedocs.io for more information.
"""

from napalm.base import NetworkDriver
from napalm.base.exceptions import (
    ConnectionException,
    SessionLockedException,
    MergeConfigException,
    ReplaceConfigException,
    CommandErrorException,
    )

import requests
import json
from distutils.util import strtobool

class IOSXEDriver(NetworkDriver):
    """Napalm driver for IOS-XE."""

    def __init__(self, hostname, username, password, timeout=60, optional_args=None):
        """Constructor."""
        self.hostname = hostname
        self.username = username
        self.password = password
        self.timeout = timeout

        self.port = optional_args.get('port', '443')
        self.verify_ssl = optional_args.get('verify_ssl', True)
        self.url_format = 'https://'

        self.profile = ['iosxe']
        self.url_format = self.url_format + '{host}:{port}/restconf/{path}'

    def open(self):
        #pass
        self.device.open()

    def close(self):
        #pass
        self.device.close()

    def _build_request_args(self, path):
        args = {
            'url': self.url_format.format(host=self.hostname, port=self.port, path=path),
            'headers': {'Accept': 'application/yang-data+json'},
            'auth': (self.username, self.password),
            #'verify': self.verify_ssl # NOT SURE WHY IT DOES NOT WORK WITH type str
            'verify': strtobool(self.verify_ssl)
        }
        return args

    def _rpc(self, get):
        result = requests.get(**self._build_request_args(get))
        return result.text

    def get_config(self, retrieve="all", full=False, sanitized=False):
        yang_module = 'Cisco-IOS-XE-native'
        container = 'native'
        y_c = yang_module + ':' + container
        path = 'data/' + y_c
        configs = {
            "startup": "",
            "running": "",
            "candidate": "",
        }

        if retrieve in ("all", "startup"):
            result = requests.get(**self._build_request_args(path))
            startup = json.dumps(result.json())
            configs["startup"] = startup

        if retrieve in ("all", "running"):
            result = requests.get(**self._build_request_args(path))
            running = json.dumps(result.json())
            configs["running"] = running

        #if sanitized:
        #    configs = self._get_config_sanitized(configs)
        
        return configs

    def get_cdp_neighbors_detail(self):
        yang_module = 'Cisco-IOS-XE-cdp-oper'
        container = 'cdp-neighbor-details'
        y_c = yang_module + ':' + container
        path = 'data/' + y_c
        result = requests.get(**self._build_request_args(path))
        json_parsed = json.dumps(result.json())
        return json_parsed

    def get_interfaces(self):
        yang_module = 'ietf-interfaces'
        container = 'interfaces'
        list = 'interface'
        y_c = yang_module + ':' + container
        path = 'data/' + y_c
        result = requests.get(**self._build_request_args(path))
        json_parsed = json.loads(json.dumps(result.json()))
        inter_list = []
        for key in json_parsed[y_c][list]:
            inter_list.append(key['name'])

        print(inter_list)
        return json_parsed

    def is_alive(self):
        path = ''
        result = requests.get(**self._build_request_args(path))
        if result.status_code == 200:
            status = {"is_alive": True}
        else:
            status = {"is_alive": False}

        return status
