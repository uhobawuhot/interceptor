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

import socket
from oslo.config import cfg
from interceptor.openstack.common import log as logging


logger = logging.getLogger(__name__)


def get_config(option, group=None):
    """Get configuration option."""

    cfg_grp = (getattr(cfg.CONF, group)
               if group and hasattr(cfg.CONF, group)
               else cfg.CONF)

    return (getattr(cfg_grp, option)
            if cfg_grp and hasattr(cfg_grp, option)
            else None)


def register_opts_for_engine():
    """Register configuration options for the engine service."""

    # define group name
    cfg_grp_name = 'engine'

    # define group
    cfg_grp = cfg.OptGroup(name=cfg_grp_name, title='Engine options')

    # define options
    opts = [cfg.IntOpt('periodic_interval', default=60,
                       help='seconds between running periodic tasks'),
            cfg.StrOpt('host', default=socket.gethostname(),
                       help='Name of the engine node. '
                            'This can be an opaque identifier. '
                            'It is not necessarily a hostname, '
                            'FQDN, or IP address.'),
            cfg.StrOpt('topic', default='engine',
                       help='The message topic that the engine listens on.')]

    # register the group and options
    cfg.CONF.register_group(cfg_grp)
    cfg.CONF.register_opts(opts, group=cfg_grp)


def register_opts_for_api():
    """Register configuration options for the API group."""

    # define group name
    cfg_grp_name = 'api'

    # define group
    cfg_grp = cfg.OptGroup(name=cfg_grp_name, title='API server options')

    # define options
    opts = [cfg.StrOpt('host', default='0.0.0.0'),
            cfg.IntOpt('port', default=8080)]

    # register the group and options
    cfg.CONF.register_group(cfg_grp)
    cfg.CONF.register_opts(opts, group=cfg_grp)


def register_opts_for_data():
    """Register configuration options for the data group."""

    # define group name
    cfg_grp_name = 'data'

    # define group
    cfg_grp = cfg.OptGroup(name=cfg_grp_name, title='Data backend options')

    # define options
    opts = [cfg.ListOpt('providers', default=[]),
            cfg.StrOpt('default', default=None)]

    # register the group and options
    cfg.CONF.register_group(cfg_grp)
    cfg.CONF.register_opts(opts, group=cfg_grp)

    # validate provider options
    if (cfg.CONF.data.default and
            cfg.CONF.data.default not in cfg.CONF.data.providers):
        raise Exception('Default provider is not recognized.')

    # register each available providers
    for provider in cfg.CONF.data.providers:
        cfg_provider = cfg.OptGroup(name=provider)
        opts = [cfg.StrOpt('plugin', required=True),
                cfg.StrOpt('username', default=None),
                cfg.StrOpt('password', secret=True, default=None),
                cfg.DictOpt('attributes', default={})]
        cfg.CONF.register_group(cfg_provider)
        cfg.CONF.register_opts(opts, group=cfg_provider)
