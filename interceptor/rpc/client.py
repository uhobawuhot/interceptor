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

from interceptor.openstack.common.rpc.proxy import RpcProxy


class EngineClient(RpcProxy):
    """
    Client side of the engine rpc API.
    """

    ENGINE_TOPIC = 'engine'
    BASE_RPC_API_VERSION = '1.0'

    def __init__(self):
        super(EngineClient, self).__init__(
            topic=self.ENGINE_TOPIC,
            default_version=self.BASE_RPC_API_VERSION)

    def ping(self, cntx):
        """
        Returns status object if service is healthy
        :param context: RPC context
        """
        return self.call(cntx, self.make_msg('ping'))
