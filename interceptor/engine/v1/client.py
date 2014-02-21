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

from oslo import messaging
from oslo.config import cfg

from interceptor.engine import v1
from interceptor.openstack.common import log as logging


logger = logging.getLogger(__name__)


class EngineClient(object):
    """
    Client side of the engine rpc API.
    """

    def __init__(self, transport):
        target = messaging.Target(topic=cfg.CONF.engine.topic,
                                  version=v1.VERSION)
        self._client = messaging.RPCClient(transport, target)

    def ping(self, cntx):
        """
        Returns status object if service is healthy
        :param context: RPC context
        """
        return self._client.call(cntx, 'ping')
