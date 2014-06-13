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

import eventlet
eventlet.monkey_patch()

import time

import testtools
from oslo import messaging
from oslo.config import cfg

from interceptor.openstack.common import context
from interceptor.engine.v1 import service as engine
from interceptor.engine.v1 import client as rpc_client


class RpcClientTestCase(testtools.TestCase):

    def get_transport(self):
        # get transport manually, oslo.messaging get_transport is broken
        from stevedore import driver
        from oslo.messaging import transport
        messaging.get_transport(cfg.CONF)
        cfg.CONF.set_default('verbose', True)
        cfg.CONF.set_default('rpc_backend', 'fake')
        url = transport.TransportURL.parse(cfg.CONF, None, None)
        kwargs = dict(default_exchange=cfg.CONF.control_exchange,
                      allowed_remote_exmods=[])
        mgr = driver.DriverManager('oslo.messaging.drivers',
                                   url.transport,
                                   invoke_on_load=True,
                                   invoke_args=[cfg.CONF, url],
                                   invoke_kwds=kwargs)
        return transport.Transport(mgr.driver)

    def setUp(self):
        # init configuration
        cfg_grp = cfg.OptGroup(name='engine', title='Engine options')
        opts = [cfg.StrOpt('host', default='localhost'),
                cfg.StrOpt('topic', default='engine')]
        cfg.CONF.register_group(cfg_grp)
        cfg.CONF.register_opts(opts, group=cfg_grp)

        # start server
        transport = self.get_transport()
        target = messaging.Target(topic='engine', server='localhost')
        endpoints = [engine.EngineServer()]
        self.server = messaging.get_rpc_server(transport, target,
                                               endpoints, executor='eventlet')
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
        transport = self.server.transport
        client = rpc_client.EngineClient(transport)
        start_time = time.time()
        echo = client.ping(context.RequestContext())
        end_time = time.time()
        self.assertIn('epoch', echo)
        self.assertIsInstance(echo['epoch'], float)
        self.assertTrue(echo['epoch'] > start_time)
        self.assertTrue(echo['epoch'] < end_time)
