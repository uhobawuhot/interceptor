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

from wsme.rest import json

from oslo import messaging

from interceptor.engine import v1
from interceptor.model import health
from interceptor.openstack.common import log as logging


logger = logging.getLogger(__name__)


class EngineServer(object):

    target = messaging.Target(version=v1.VERSION)

    def ping(self, cntx):
        """
        Returns status object if service is healthy and responding
        """
        return json.tojson(health.PingResponse, health.PingResponse())
