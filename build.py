import os
for proto in os.listdir('oaktree/_protos'):
    if proto.endswith('.proto'):
        proto = proto[:-6]
        try:
            os.unlink('oaktree/rpc/{proto}.py'.format(proto=proto))
            os.unlink('oaktree/rpc/{proto}.pyc'.format(proto=proto))
        except:
            pass
import oaktree
