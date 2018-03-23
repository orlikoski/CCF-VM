#!/usr/bin/python
from concurrent import futures
import time

import grpc

import rc_pb2
import rc_pb2_grpc
import subprocess


import os 
#dir_path = os.path.dirname(os.path.realpath(__file__))
rcpy = "/var/lib/automation/rc.py"

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class RC(rc_pb2_grpc.RCServicer):

    def ExecuteRC(self, request, context):
        args = ' '.join(request.arg)
        #command = "python3 " + rcpy + " " + request.service + " --" + request.flag + " " + args
        command = "python3 " + rcpy + " " + request.service
        runout, errorout = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).wait()
        return rc_pb2.RCReply(message=runout + " " + errorout)      


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    rc_pb2_grpc.add_RCServicer_to_server(RC(), server)
    server.add_insecure_port('[::]:10101')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()

