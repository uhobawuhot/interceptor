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

from oslo.config import cfg

from interceptor.openstack.common import log as logging
from interceptor import version


logger = logging.getLogger(__name__)


engine_opts = [
    cfg.StrOpt('host',
               default='0.0.0.0',
               help='Name of the engine node. This can be an opaque '
                    'identifier. It is not necessarily a hostname, '
                    'FQDN, or IP address.'),
    cfg.StrOpt('topic',
               default='engine',
               help='The message topic that the engine listens on.'),
    cfg.StrOpt('version',
               default='1.0',
               help='The version of the engine.')
]

api_opts = [
    cfg.StrOpt('host',
               default='0.0.0.0',
               help='API server host.'),
    cfg.IntOpt('port',
               default=8080,
               help='API server port.')
]

cfg.CONF.register_opts(api_opts, group='api')
cfg.CONF.register_opts(engine_opts, group='engine')


def parse_args(args=None, usage=None, default_config_files=None):
    cfg.CONF(args=args,
             project='interceptor',
             version=version,
             usage=usage,
             default_config_files=default_config_files)


def get_config(option, group=None):
    """Get configuration option."""

    cfg_grp = (getattr(cfg.CONF, group)
               if group and hasattr(cfg.CONF, group)
               else cfg.CONF)

    return (getattr(cfg_grp, option)
            if cfg_grp and hasattr(cfg_grp, option)
            else None)
