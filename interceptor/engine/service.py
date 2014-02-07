# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012-2013 Red Hat, Inc.
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
from oslo.config import cfg
from interceptor.openstack.common import log as logging
from interceptor.openstack.common.rpc import service
from interceptor.model import health


logger = logging.getLogger(__name__)


class EngineService(service.Service):

    def _service_task(self):
        """
        This is a dummy task which gets queued on the service.Service
        threadgroup.  Without this service.Service sees nothing running
        i.e has nothing to wait() on, so the process exits..
        This could also be used to trigger periodic housekeeping tasks
        """
        pass

    def start(self):
        """
        Starts the service
        """
        super(EngineService, self).start()

        # create dummy task, when there is nothing in queue, the process exits
        # tg -> thread group defined in the openstack.commmon.service module
        self.tg.add_timer(cfg.CONF.engine.periodic_interval,
                          self._service_task)

    def ping(self, cntx):
        """
        Returns status object if service is healthy and responding
        """
        return json.tojson(health.PingResponse, health.PingResponse())
