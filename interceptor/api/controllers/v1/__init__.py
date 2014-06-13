# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import pecan
from pecan.core import request
import wsmeext.pecan
from oslo import messaging
from oslo.config import cfg

from interceptor.model import health
from interceptor.engine.v1 import client as rpc_client
from interceptor.openstack.common import log as logging


logger = logging.getLogger(__name__)


class ApplicationController(object):
    """Root of version 1 API controller."""

    @pecan.expose(generic=True, template='index.html')
    def index(self):
        return dict()

    @wsmeext.pecan.wsexpose(health.PingResponse)
    def ping(self):
        transport = messaging.get_transport(cfg.CONF)
        client = rpc_client.EngineClient(transport)
        echo = client.ping(request.context)
        response = health.PingResponse(**echo)
        return response
