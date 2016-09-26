# Copyright (c) 2016 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# This is totes cheating - but at the moment I don't particularly care
def _try_import():
    try:
        import oaktree.rpc.oaktree_pb2
    except ImportError:
        _build_proto()


def _build_proto():
    import os
    from grpc.tools import protoc

    base_path = os.path.abspath(os.path.dirname(__file__))
    proto_path = os.path.join(base_path, '_protos')
    rpc_path = os.path.join(base_path, 'rpc')
    protoc.main(
        (
            '',
            '-I{proto_path}'.format(proto_path=proto_path),
            '--python_out={rpc_path}'.format(rpc_path=rpc_path),
            '--grpc_python_out={rpc_path}'.format(rpc_path=rpc_path),
            '{proto_path}/oaktree.proto'.format(proto_path=proto_path),
        )
    )


_try_import()
