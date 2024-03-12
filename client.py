# client.py
# Implementation of the client-side behavior of the chat app.

import socket, sys, argparse

def main():
    """
    Handles the initialization, running behavior, and termination of the client.
    """
    def INITIALIZE():
        global clientSocket
        """
        Initializes client-server connection.
        """
            # attempt client-server connection
        try:
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientSocket.connect((serverIP, int(serverPort)))
            print("{} running on {}".format(clientName, clientIP))
            #clientSocket.send("READY_FOR_CHAT".encode())
        except KeyboardInterrupt:
            print("Error: Client interrupt caught. Ending program.\n", file=sys.stderr)
            sys.exit(0)
        except:
            print("Error: Connection not established. Ending program.\n", file=sys.stderr)
            sys.exit(1)
        # end try-except

        # get client input for next action
        print("*** STATE: INITIALIZE ***")
        try:
            while True:
                userInput = input(">")
                # id
                if userInput == "/id":
                    print("User ID:", clientName)
                # register
                elif userInput == "/register":
                    registerRequest = "REGISTER\r\nclientID: {}\r\nIP: {}\r\nPort: {}\r\n\r\n".format(clientName, clientIP, clientPort)
                    clientSocket.send(registerRequest.encode())
                    clientData = (clientSocket.recv(4096)).decode()
                    try:
                        assert clientData == ("REGACK\r\nclientID: {}\r\nIP: {}\r\nPort: {}\r\n\r\n".format(clientName, clientIP, clientPort))
                    except:
                        print("Error: Invalid REGACK.\n", file=sys.stderr)
                        TERMINATE()
                    clientSocket.close()  # close the socket after registration
                    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # reopen socket
                    clientSocket.connect((serverIP, int(serverPort))) 
                # bridge
                elif userInput == "/bridge":
                    bridgeRequest = "BRIDGE\r\nclientID: {}\r\n\r\n".format(clientName)
                    clientSocket.send(bridgeRequest.encode())
                    bridgeData = (clientSocket.recv(4096)).decode()
                    print("Response from server:",bridgeData)
                    if "clientID: \r\nIP: \r\nPort: \r\n" in bridgeData:
                        WAIT()
                    #end if
                #chat      
                elif userInput == "/chat":
                    # TODO: somehow parse bridgeData string to get peer's info
                    clientSocket.close()
                    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # reopen socket
                    clientSocket.connect((serverIP, int(serverPort)))
                    CHAT()
                # quit
                elif userInput == "/quit":
                    TERMINATE()
                # unknown command
                else:
                    print("Error: Unknown command.\n")  
                # end if
            # end while
        except KeyboardInterrupt:
            print("Error: Client interrupt caught. Closing connection.\n", file=sys.stderr)
            TERMINATE()
        except:
            print("Error: Connection failed.\n", file=sys.stderr)
            TERMINATE()
        # end try-except
    # end INITIALIZE()
            
    def WAIT():
        global clientSocket
        """
        Pauses client input while awaiting second client connection.
        """
        print("*** STATE: WAIT ***")
        try:
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientSocket.bind((clientIP, int(clientPort)))
            clientSocket.listen()   # stop-and-wait function, returns when connection received
            clientSocket.accept()
            #print("Connection established with", address)
            #clientSocket.close()
            CHAT()
        except KeyboardInterrupt:
            print("Error: Client interrupt caught. Closing connection.\n", file=sys.stderr)
            TERMINATE()
        except Exception as e:
            print("Error:", e, file=sys.stderr)
            TERMINATE()
    # end WAIT()!
    
    def CHAT():
        global clientSocket
        """
        Operates chat activity between both clients. 
        """
        print("*** STATE: CHAT ***")
        try:
            while True:
                message = input("Enter message: ")
                if message == "/quit":
                    clientSocket.send(message.encode())
                    break  
                else:
                    clientSocket.send(message.encode())
        except KeyboardInterrupt:
            print("Error: Client interrupt caught. Closing connection.\n", file=sys.stderr)
            TERMINATE()
        except:
            print("Error: Connection failed.\n", file=sys.stderr)
            TERMINATE()

    def TERMINATE():
        global clientSocket
        """
        Terminates the client program.
        """
        print("*** STATE: TERMINATE ***")
        clientSocket.close()
        sys.exit(0)
    # end TERMINATE()

    # read client options
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", action='store') 
    parser.add_argument("--port", action='store') 
    parser.add_argument("--server", action='store') 
    args = parser.parse_args()

    # save client and server details
    clientName = args.id
    clientPort = args.port
    serverIP, serverPort = (args.server).split(":")
    clientIP = '127.0.0.1'

    INITIALIZE()


# end main()

if __name__ == "__main__":
    main()
# end if