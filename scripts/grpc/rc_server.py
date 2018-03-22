 
from concurrent import futures
import time

import grpc

import rc_pb2
import rc_pb2_grpc
import subprocess


import os 
dir_path = os.path.dirname(os.path.realpath(__file__))


_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class RC(rc_pb2_grpc.RCServicer):

    def ExecuteRC(self, request, context):
        args = ' '.join(request.arg)
        command = "python " + dir_path + "/..rc.py " + request.service + " --" + request.flag + " " + args
        cmd = subprocess.Popen(command, shell=True).wait()
        return rc_pb2.RCReply(message="SUCCESS")      


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    rc_pb2_grpc.add_RCServicer_to_server(RC(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()

