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

import inspect

import flask
import flask_restplus
from flask.ext import login
import os_client_config
import shade

from shadeapi.auth import authentication


app = flask.Flask(__name__)
api = flask_restplus.Api(app, authorizations=authentication.authorizations)
all_clouds = {}
CLOUD_API = shade.OpenStackCloud.__dict__.keys()
C_PREFIX = '/cloud/<string:cloud>'
CR_PREFIX = '/cloud/<string:cloud>/region/<string:region>'
openstack_config = os_client_config.OpenStackConfig()

authentication.LOGIN_MANAGER.init_app(app)


def _make_cloud_key(cloud, region):
    return "{cloud}:{region}".format(cloud=cloud, region=region)


def _get_cloud(cloud, region):
    key = _make_cloud_key(cloud, region)
    if key not in all_clouds:
        all_clouds[key] = shade.openstack_cloud(
            cloud=cloud, region_name=region, debug=True)
    return all_clouds[key]


@api.header(authentication.API_KEY_HEADER, authentication.API_KEY_HEADER_DESC,
            required=True)
class CloudConfig(flask_restplus.Resource):
    @login.login_required
    def get(self, cloud=None, region=None):
        if not cloud and not region:
            return [
                config.config for config in openstack_config.get_all_clouds()]
        if not region:
            return [
                config.config for config in openstack_config.get_all_clouds()
                if config.name == cloud]
        return openstack_config.get_one_cloud(
            cloud=cloud, region_name=region).config
api.add_resource(
    CloudConfig, '/clouds',
    '/cloud/<string:cloud>',
    '/cloud/<string:cloud>/region/<string:region>',
    endpoint='config')


def make_list_resource(name):
    @api.header(authentication.API_KEY_HEADER,
                authentication.API_KEY_HEADER_DESC,
                required=True)
    class RestResource(flask_restplus.Resource):
        @login.login_required
        def get(self, cloud='vexxhost', region=None, **kwargs):
            cloud_obj = _get_cloud(cloud, region)
            filters = flask.request.args
            if filters:
                search_key = name.replace('list', 'search')
                return getattr(cloud_obj, search_key)(
                    filters=filters.to_dict(), **kwargs)
            else:
                return getattr(cloud_obj, name)(**kwargs)
    return RestResource


def make_get_resource(name):
    @api.header(authentication.API_KEY_HEADER,
                authentication.API_KEY_HEADER_DESC,
                required=True)
    class RestResource(flask_restplus.Resource):
        @login.login_required
        def get(self, name_or_id, cloud='vexxhost', region=None):
            cloud_obj = _get_cloud(cloud, region)
            filters = flask.request.args
            get_method = getattr(cloud_obj, name)
            if filters:
                return get_method(name_or_id, filters=filters.to_dict())
            return get_method(name_or_id)
    return RestResource


def get_required_args(list_key):
    list_obj = getattr(shade.OpenStackCloud, list_key)
    argspec = inspect.getargspec(list_obj)
    default_len = len(argspec.defaults) if argspec.defaults else 0
    return argspec.args[1:len(argspec.args) - default_len]


def get_rest_args(name, req_args):
    args = []
    for arg in req_args:
        args.append(arg)
        args.append("<string:{arg}>".format(arg=arg))
    args.append(name)
    res = "/".join(args)

    return [
        '/{res}'.format(res=res),
        '/cloud/<string:cloud>/{res}'.format(res=res),
        '/cloud/<string:cloud>/region/<string:region>/{res}'.format(res=res),
    ]


for list_key in CLOUD_API:
    if not list_key.startswith('list_'):
        continue
    name = list_key[5:]
    single_name = name[:-1]
    res_class = make_list_resource(list_key)

    req_args = get_required_args(list_key)
    rest_args = get_rest_args(name, req_args)
    api.add_resource(res_class, endpoint=list_key, *rest_args)

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
