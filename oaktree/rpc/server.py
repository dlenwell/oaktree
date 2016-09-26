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

import shade
shade.simple_logging(debug=True)

from concurrent import futures
import logging
logging.getLogger().setLevel(logging.INFO)
import time

from google.protobuf.descriptor import FieldDescriptor
import grpc
from grpc.framework.foundation import logging_pool

from oaktree import _clouds
from oaktree.rpc import oaktree_pb2

_BOOL_TYPES = (FieldDescriptor.TYPE_BOOL,)
_STR_TYPES = (FieldDescriptor.TYPE_STRING, )
_INT_TYPES = (
    FieldDescriptor.TYPE_FIXED32, FieldDescriptor.TYPE_FIXED64,
    FieldDescriptor.TYPE_SFIXED32, FieldDescriptor.TYPE_SFIXED64,
    FieldDescriptor.TYPE_INT32, FieldDescriptor.TYPE_INT64,
    FieldDescriptor.TYPE_SINT32, FieldDescriptor.TYPE_SINT64,
    FieldDescriptor.TYPE_UINT32, FieldDescriptor.TYPE_UINT64,
)
_FLOAT_TYPES = (
    FieldDescriptor.TYPE_DOUBLE, FieldDescriptor.TYPE_FLOAT,
)

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

# Skipping bytes and enum for now


def convert_for_field(value, field):
    if value is None:
        return value
    if field.type in _BOOL_TYPES:
        return bool(value)
    elif field.type in _STR_TYPES:
        return str(value)
    elif field.type in _INT_TYPES:
        if value == '':
            return 0
        return int(value)
    elif field.type in _FLOAT_TYPES:
        return float(value)


def convert_flavor(flavor):
    flavor_pb = oaktree_pb2.Flavor()
    for key, field in flavor_pb.DESCRIPTOR.fields_by_name.items():
        value = convert_for_field(flavor.pop(key, None), field)
        if value:
            setattr(flavor_pb, key, value)
    for key, value in flavor.items():
        if key == 'request_ids':
            continue
        flavor_pb.extra_specs[key] = str(value)
    return flavor_pb


def convert_flavors(flavors):
    flavor_list = oaktree_pb2.FlavorList()
    for flavor in flavors:
        # Why does this require a list extend? That seems silly enough that
        # I feel like I'm doing something wrong
        flavor_list.flavors.extend([convert_flavor(flavor)])
    return flavor_list


class OaktreeServicer(oaktree_pb2.OaktreeServicer):

    def ListFlavors(self, request, context):
        logging.info('listing flavors')
        cloud = _clouds._get_cloud(
            cloud=request.cloud_region.cloud,
            region=request.cloud_region.region,
            project=request.cloud_region.project)
        return convert_flavors(cloud.list_flavors())


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    oaktree_pb2.add_OaktreeServicer_to_server(OaktreeServicer(), server)
    server.add_insecure_port('[::]:50051')
    logging.info("Starting server")
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
