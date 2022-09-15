from concurrent import futures
import string
import time
from tracemalloc import stop
import grpc
import messageProtocol_pb2
import messageProtocol_pb2_grpc
import docker

class Listener(messageProtocol_pb2_grpc.PingPongServiceServicer):

    def __init__(self):
        self.nameData = "ubuntu"
        
    def __str__(self):
        return self.__class__.__name__

    def ping(self, request, context):
        client = docker.from_env()

        if  request.command == "DOCKER_VERSION":
            resData = client.version()
            print("----- Client request execeuted -----")
            return messageProtocol_pb2.Pong(command=resData["Platform"]["Name"])
        
        elif  request.command == "DOCKER_RUN":
              resData = client.containers.run(request.query, detach=True)
              print("----- Client request execeuted -----")
              return messageProtocol_pb2.Pong(command=resData.id)
        
        elif  request.command == "DOCKER_STOP":
              container = client.containers.get(request.query)
              container.stop()
              print("----- Client request execeuted -----")
              return messageProtocol_pb2.Pong(command=request.query+ " stopped.")

        elif  request.command == "DOCKER_START":
              container = client.containers.get(request.query)
              container.start()
              print("----- Client request execeuted -----")
              return messageProtocol_pb2.Pong(command=request.query+ " started.")

        elif  request.command == "DOCKER_REMOVE":
              container = client.containers.get(request.query)
              container.remove()
              print("----- Client request execeuted -----")
              return messageProtocol_pb2.Pong(command=request.query+ " removed.")

        elif  request.command == "DOCKER_SHOWALL_CONTAINERS":
              containerNames = ""
              containers = client.containers.list(all=True)
              for container in containers:
                containerNames += container.id
                if container.id != containers[-1]:
                    containerNames += ","     
              print("----- Client request execeuted -----")
              return messageProtocol_pb2.Pong(command=containerNames)

        elif  request.command == "DOCKER_SHOWALL_IMAGES":
              imageNames = ""
              images = client.images.list(all=True)
              for image in images:
                imageNames += image.id
                if image.id != images[-1]:
                    imageNames += ","
              print("----- Client request execeuted -----")
              return messageProtocol_pb2.Pong(command=imageNames)

        elif  request.command == "DOCKER_LOGS":
              container = client.containers.get(request.query)
              data = container.logs()
              print("----- Client request execeuted -----")
              return messageProtocol_pb2.Pong(command=data)

        elif  request.command == "DOCKER_COMMIT":
              container = client.containers.get(request.query)
              container.commit()
              print("----- Client request execeuted -----")
              return messageProtocol_pb2.Pong(command=request.query+ " commited.")

        else:
            client.login(username=request.command, password=request.query)
            print("----- Client request execeuted -----")
            return messageProtocol_pb2.Pong(command=request.command + " authenticated.")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    messageProtocol_pb2_grpc.add_PingPongServiceServicer_to_server(Listener(), server)
    server.add_insecure_port("[::]:8888")
    server.start()
    try:
        while True:
            print("Server status : Running..")
            time.sleep(12)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        server.stop(0)

if __name__ == "__main__":
    serve()
