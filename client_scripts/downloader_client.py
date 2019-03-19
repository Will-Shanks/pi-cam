import socket
import time

from protobufp.processor import Processor

import request_pb2
from options import ops

req = request_pb2.ServerRequest()
req.op = ops['D_REQ']
req.args.extend([1, 2, 3, 4, 5])

a = req.SerializeToString()
print(a)
print(request_pb2.ServerRequest().FromString(a))
