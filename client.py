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
        # get client input for next action
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
                        print("Error: Invalid REGACK.", file=sys.stderr)
                        TERMINATE()
                    clientSocket.close()  # close the socket after registration
                    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # reopen socket
                    clientSocket.connect((serverIP, int(serverPort))) 
                # bridge
                elif userInput == "/bridge":
                    bridgeRequest = "BRIDGE\r\nclientID: {}\r\n\r\n".format(clientName)
                    clientSocket.send(bridgeRequest.encode())
                    bridgeData = (clientSocket.recv(4096)).decode()
                    print("Response from server:\n", bridgeData)
                    if bridgeData == " BRIDGEACK\r\nclientID: \r\nIP: \r\n Port: \r\n\r\n":
                        WAIT()
                        return
                    else:
                        print("Entered CHAT State.")
                        CHAT(clientSocket)
                        return
                    # end if
                # quit
                elif userInput == "/quit":
                    TERMINATE()
                # unknown command
                else:
                    pass  
                # end if
            # end while
        except KeyboardInterrupt:
            print("Error: Client interrupt caught. Closing connection.", file=sys.stderr)
            TERMINATE()
        except:
            print("Error: Connection failed.", file=sys.stderr)
            TERMINATE()
        # end try-except
    # end INITIALIZE()
            
    def WAIT():
        global clientSocket
        """
        Pauses client input while awaiting second client connection.
        """
        print("Entered WAIT State.")
        try:
            while True:
                # TODO TODO TODO TODO TODO
                pass
        except KeyboardInterrupt:
            print("Error: Client interrupt caught. Closing connection.", file=sys.stderr)
            TERMINATE()
        except:
            print("Error: Connection failed.", file=sys.stderr)
            TERMINATE()
    # end WAIT()
    
    def CHAT():
        global clientSocket
        """
        Operates chat activity between both clients. 
        """
        print("Entered CHAT State.")
        try:
            while True:
                message = input("Enter message: ")
                if message == "/quit":
                    clientSocket.send(message.encode())
                    break  
                else:
                    clientSocket.send(message.encode())
        except KeyboardInterrupt:
            print("Error: Client interrupt caught. Closing connection.", file=sys.stderr)
            TERMINATE()
        except:
            print("Error: Connection failed.", file=sys.stderr)
            TERMINATE()

    def TERMINATE():
        global clientSocket
        """
        Terminates the client program.
        """
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

    # attempt client-server connection
    try:
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((serverIP, int(serverPort)))
        print("{} running on {}".format(clientName, clientIP))
        INITIALIZE()
    except KeyboardInterrupt:
        print("Error: Client interrupt caught. Ending program.", file=sys.stderr)
        sys.exit(0)
    except:
        print("Error: Connection not established. Ending program.", file=sys.stderr)
        sys.exit(1)
    # end try-except
# end main()

if __name__ == "__main__":
    main()
# end if