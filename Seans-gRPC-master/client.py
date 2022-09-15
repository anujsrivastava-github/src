import grpc
import messageProtocol_pb2
import messageProtocol_pb2_grpc
import getpass

def run():
    counter = 0
    #with grpc.insecure_channel("localhost:9999") as channel:
    with grpc.insecure_channel('localhost:8888', options=(('grpc.enable_http_proxy', 0),)) as channel:
        stub = messageProtocol_pb2_grpc.PingPongServiceStub(channel)
        #userName = input("\nUser Name : ")
        #password = getpass.getpass("\nPassword : ")
        #response = stub.ping(messageProtocol_pb2.Ping(command=userName, query=password))
        #print( "Server Response : ", response.command)

        while True:
            try:
                print("\n----- Trigger Docker commands using gRPC -----")
                print("1. Docker version")
                print("2. Run container")
                print("3. Stop container")
                print("4. Start container")
                print("5. Remove container")
                print("6. Show all containers")
                print("7. Show all images")
                print("8. See container logs")
                print("9. Commit container")
                print("10. Exit")

                choice = int(input("\nEnter the Choice : ")) 

                if choice == 1:
                    clientCommand = "DOCKER_VERSION"
                    response = stub.ping(messageProtocol_pb2.Ping(command=clientCommand, query=""))
                    print( "Server Response : ", response.command)

                elif choice == 2:
                     clientQuery = input("\nEnter image name : ")
                     clientCommand = "DOCKER_RUN"
                     response = stub.ping(messageProtocol_pb2.Ping(command=clientCommand, query=clientQuery))
                     print( "Server Response : ", response.command)

                elif choice == 3:
                     clientQuery = input("\nEnter container id : ")
                     clientCommand = "DOCKER_STOP"
                     response = stub.ping(messageProtocol_pb2.Ping(command=clientCommand, query=clientQuery))
                     print( "Server Response : ", response.command)

                elif choice == 4:
                     clientQuery = input("\nEnter container id : ")
                     clientCommand = "DOCKER_START"
                     response = stub.ping(messageProtocol_pb2.Ping(command=clientCommand, query=clientQuery))
                     print( "Server Response : ", response.command)

                elif choice == 5:
                     clientQuery = input("\nEnter container id : ")
                     clientCommand = "DOCKER_REMOVE"
                     response = stub.ping(messageProtocol_pb2.Ping(command=clientCommand, query=clientQuery))
                     print( "Server Response : ", response.command)
                    
                elif choice == 6:
                     clientCommand = "DOCKER_SHOWALL_CONTAINERS"
                     response = stub.ping(messageProtocol_pb2.Ping(command=clientCommand, query=""))
                     print( "Server Response : ", response.command)
                    
                elif choice == 7:
                     clientCommand = "DOCKER_SHOWALL_IMAGES"
                     response = stub.ping(messageProtocol_pb2.Ping(command=clientCommand, query=""))
                     print( "Server Response : ", response.command)

                elif choice == 8:
                     clientQuery = input("\nEnter container id : ")
                     clientCommand = "DOCKER_LOGS"
                     response = stub.ping(messageProtocol_pb2.Ping(command=clientCommand, query=clientQuery))
                     print( "Server Response : ", response.command)

                elif choice == 9:
                     clientQuery = input("\nEnter container id : ")
                     clientCommand = "DOCKER_COMMIT"
                     response = stub.ping(messageProtocol_pb2.Ping(command=clientCommand, query=clientQuery))
                     print( "Server Response : ", response.command)

                elif choice == 10:    
                    exit()
                     
            except KeyboardInterrupt:
                print("KeyboardInterrupt")
                channel.unsubscribe(close)
                exit()

def close(channel):
    "Close the channel"
    channel.close()

if __name__ == "__main__":
    run()
