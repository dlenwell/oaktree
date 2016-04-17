# Copyright (c) 2016 Monty Taylor
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import flask
import flask_restplus
from flask.ext import login
import shade

from shadeapi.auth import authentication

app = flask.Flask(__name__)
api = flask_restplus.Api(app)
all_clouds = {}
CLOUD_API = shade.OpenStackCloud.__dict__.keys()
C_PREFIX = '/cloud/<string:cloud>'
CR_PREFIX = '/cloud/<string:cloud>/region/<string:region>'

authentication.login_manager.init_app(app)

def _make_cloud_key(cloud, region):
    return "{cloud}:{region}".format(cloud=cloud, region=region)


def _get_cloud(cloud, region):
    key = _make_cloud_key(cloud, region)
    if key not in all_clouds:
        all_clouds[key] = shade.openstack_cloud(
            cloud=cloud, region_name=region, debug=True)
    return all_clouds[key]


class Config(flask_restplus.Resource):
    @login.login_required
    def get(self, cloud='vexxhost', region=None):
        return cloud.cloud_config.config
api.add_resource(
    Config, '/config',
    '/cloud/<string:cloud>/config',
    '/cloud/<string:cloud>/region/<string:region>/config',
    endpoint='config')


def make_list_resource(name):
    class RestResource(flask_restplus.Resource):
        @login.login_required
        def get(self, cloud='vexxhost', region=None, **kwargs):
            cloud_obj = _get_cloud(cloud, region)
            filters = flask.request.args
            if filters:
                search_key = name.replace('list', 'search')
                return getattr(cloud_obj, search_key)(
                    filters=filters.to_dict())
            else:
                return getattr(cloud_obj, name)()
    return RestResource


def make_get_resource(name):
    class RestResource(flask_restplus.Resource):
        @login.login_required
        def get(self, name_or_id, cloud='vexxhost', region=None, **kwargs):
            cloud_obj = _get_cloud(cloud, region)
            filters = flask.request.args
            get_method = getattr(cloud_obj, name)
            if filters:
                return get_method(name_or_id, filters=filters.to_dict())
            return get_method(name_or_id)
    return RestResource


for list_key in CLOUD_API:
    if not list_key.startswith('list_'):
        continue
    name = list_key[5:]
    single_name = name[:-1]
    res_class = make_list_resource(list_key)

    api.add_resource(
        res_class, '/{res}'.format(res=name),
        '/cloud/<string:cloud>/{res}'.format(res=name),
        '/cloud/<string:cloud>/region/<string:region>/{res}'.format(res=name),
        endpoint=list_key)

    get_key = 'get_{name}'.format(name=single_name)

    if get_key in CLOUD_API:
        get_class = make_get_resource(get_key)
        api.add_resource(
            get_class,
            '/{res}/<string:name_or_id>'.format(res=single_name),
            '{prefix}/{res}/<string:name_or_id>'.format(
                prefix=C_PREFIX, res=single_name),
            '{prefix}/{res}/<string:name_or_id>'.format(
                prefix=CR_PREFIX, res=single_name),
            endpoint=get_key)

if __name__ == '__main__':
    app.run(debug=True)
