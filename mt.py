# flake8: noqa
import grpc

from oaktree.rpc import model
from oaktree.rpc import oaktree_pb2

channel = grpc.insecure_channel('localhost:50051')
stub = oaktree_pb2.OaktreeStub(channel)

cloud = common_pb2.Location()
cloud.cloud = 'vexxhost'

flavors = stub.SearchFlavors(common_pb2.Filter(location=cloud))
flavor = stub.GetFlavor(
    common_pb2.Filter(
        location=cloud,
        name_or_id='e82d0a5b-8031-4526-9a5d-a15f7b4d48ff'))
images = stub.SearchImages(common_pb2.Filter(location=cloud))
