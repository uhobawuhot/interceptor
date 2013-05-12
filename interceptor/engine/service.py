#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright © 2012 eNovance <licensing@enovance.com>
#
# Author: Julien Danjou <julien@danjou.info>
#
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
import socket

from oslo.config import cfg

from interceptor.openstack.common import context
from interceptor.openstack.common import log as logging
from interceptor.openstack.common import rpc
from interceptor.openstack.common.rpc import service


logger = logging.getLogger(__name__)


cfg.CONF.register_opts([
    cfg.IntOpt('periodic_interval',
               default=60,
               help='seconds between running periodic tasks')])


class EngineService(service.Service):

    def start(self):
        super(EngineService, self).start()

        # create dummy task, when there is nothing queue, the process exits
        self.tg.add_timer(cfg.CONF.periodic_interval,
                          self._service_keep_alive_task)

    def _service_keep_alive_task(self):
        """
        This is a dummy task which gets queued on the service.Service
        threadgroup.  Without this, service.Service sees nothing running
        i.e has nothing to wait() on, so the process exits.
        """
        pass
