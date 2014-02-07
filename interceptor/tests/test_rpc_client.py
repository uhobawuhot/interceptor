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

import time
import testtools
from oslo.config import cfg
from interceptor.openstack.common import context
from interceptor.rpc import client as rpc_client


class RpcClientTestCase(testtools.TestCase):

    def setUp(self):
        # init config
        cfg.CONF.set_default('verbose', True)
        cfg.CONF.set_default('rpc_backend',
                             'interceptor.openstack.common.rpc.impl_fake')
        cfg_grp = cfg.OptGroup(name='engine', title='Engine options')
        opts = [cfg.IntOpt('periodic_interval', default=60),
                cfg.StrOpt('host', default='localhost'),
                cfg.StrOpt('topic', default='engine')]
        cfg.CONF.register_group(cfg_grp)
        cfg.CONF.register_opts(opts, group=cfg_grp)

        # start server
        from interceptor.engine import service as engine
        engine_conf = cfg.CONF.engine
        self.server = engine.EngineService(engine_conf.host, engine_conf.topic)
        self.server.start()

        # upcall
        super(RpcClientTestCase, self).setUp()

    def tearDown(self):
        # stop server
        if self.server:
            self.server.stop()

        # upcall
        super(RpcClientTestCase, self).tearDown()

    def test_ping(self):
        client = rpc_client.EngineClient()
        start_time = time.time()
        echo = client.ping(context.RequestContext())
        end_time = time.time()
        self.assertIn('epoch', echo)
        self.assertIsInstance(echo['epoch'], float)
        self.assertTrue(echo['epoch'] > start_time)
        self.assertTrue(echo['epoch'] < end_time)
