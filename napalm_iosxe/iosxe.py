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

class IOSXEDriver(NetworkDriver):
    """Napalm driver for IOS-XE."""

    def __init__(self, hostname, username, password, timeout=60, optional_args=None):
        """Constructor."""
        self.hostname = hostname
        self.username = username
        self.password = password
        self.timeout = timeout

        self.port = optional_args.get("port", "443")
        self.verify_ssl = optional_args.get("verify_ssl", True)
        self.url_format = "https://"

        self.profile = ["iosxe"]
        self.url_format = self.url_format + "{host}:{port}/restconf/{path}"

    def open(self):
        pass

    def close(self):
        pass

    def _build_request_args(self, path):
        args = {
            'url': self.url_format.format(host=self.hostname, port=self.port, path=path),
            'headers': {'accept': 'application/yang-data+json'},
            'auth': (self.username, self.password),
            'verify': self.verify_ssl
        }
        return args

    def _rpc(self, get):
        result = requests.get(**self._build_request_args(get))
        return result.text


