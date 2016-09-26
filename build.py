import os
try:
    os.unlink('oaktree/rpc/oaktree_pb2.py')
except:
    pass
try:
    os.unlink('oaktree/rpc/oaktree_pb2.pyc')
except:
    pass
import oaktree
