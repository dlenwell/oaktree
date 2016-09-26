import grpc

from oaktree.rpc import oaktree_pb2

channel = grpc.insecure_channel('localhost:50051')
stub = oaktree_pb2.OaktreeStub(channel)

cloud = oaktree_pb2.CloudRegion()
cloud.cloud = 'vexxhost'

flavors = stub.ListFlavors(oaktree_pb2.ListFlavorsRequest(cloud_region=cloud))
