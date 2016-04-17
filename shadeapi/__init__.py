from flask import Flask
from flask_restplus import Resource, Api

import shade

app = Flask(__name__)
api = Api(app)
all_clouds = {}


class Config(Resource):
    def get(self):
        return cloud.cloud_config.config

def make_resource(name):
    class RestResource(Resource):
        def get(self, cloud='vexxhost', region=None, **kwargs):
            if cloud not in all_clouds:
                all_clouds[cloud] = shade.openstack_cloud(
                    cloud=cloud, debug=True)
            return getattr(all_clouds[cloud], name)()
    return RestResource

for f in shade.OpenStackCloud.__dict__.keys():
    if not f.startswith('list_'):
        continue
    name = f[5:]
    res_class = make_resource(f)

    api.add_resource(
        res_class, '/{res}'.format(res=name),
        '/cloud/<string:cloud>/{res}'.format(res=name),
        '/cloud/<string:cloud>/region/<string:region>/{res}'.format(res=name),
        endpoint=f)

api.add_resource(Config, '/config')
if __name__ == '__main__':
    app.run(debug=True)
