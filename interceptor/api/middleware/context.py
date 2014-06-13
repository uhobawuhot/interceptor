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

from pecan.core import request

from interceptor.openstack.common import context
from interceptor.openstack.common import importutils
from interceptor.openstack.common import log as logging


logger = logging.getLogger(__name__)


class ContextMiddleware(object):
    def __init__(self, app, options=None):
        self.app = app
        if options:
            self.options = options

    def __call__(self, environ, start_response):
        """Process the request.

        Extract any authentication information in the request and
        construct an appropriate context from it.
        """
        # Use the default empty context, with admin turned on for
        # backwards compatibility
        request.context = self.make_context(is_admin=True)

        return self.app(environ, start_response)

    def make_context(self, *args, **kwargs):
        """Create a context with the given arguments."""

        # Determine the context class to use
        ctxcls = context.RequestContext
        if self.options and 'context_class' in self.options:
            ctxcls = importutils.import_class(self.options['context_class'])

        return ctxcls(*args, **kwargs)
