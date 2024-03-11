# client.py
# Implementation of the client-side behavior of the chat app.

import socket, sys, argparse

def main():
    def INITIALIZE():
        # attempt server connection
        try:
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientSocket.connect((serverIP, int(serverPort)))
            print("{} running on {}".format(clientName, clientIP))
        except:
            print("Error: Connection failed.", file=sys.stderr)
            TERMINATE()  # exit code for error
        # end try-except

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
                    if bridgeData == "BRIDGEACK\r\nclientID: \r\nIP: \r\n Port: \r\n\r\n":
                        WAIT()
                        return
                    else:
                        print("Entered CHAT State.")
                        CHAT(clientSocket)
                        return
                    # end if
                # chat
                elif userInput == "/chat":
                    print("Entered CHAT State.")
                    try:
                      while True:
                          message = input("Enter message: ")
                          if message == "/quit":
                              break
                          clientSocket.send(message.encode())
                    except KeyboardInterrupt:
                        pass
                    finally:
                      pass
                # quit
                elif userInput == "/quit":
                    TERMINATE()
                # unknown command
                else:
                    pass  
                # end if
            # end while
        except:
            print("Error: Connection failed.", file=sys.stderr)
            TERMINATE()
        # end try-except
    # end INITIALIZE()

    def TERMINATE():
        """
        Terminates the client program.
        """
        clientSocket.close()
        sys.exit()
    # end TERMINATE()
    
    # get command line options
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", action='store') 
    parser.add_argument("--port", action='store') 
    parser.add_argument("--server", action='store') 
    args = parser.parse_args()

    # assign options to variables
    clientName = args.id
    clientPort = args.port
    serverIP, serverPort = (args.server).split(":")
    clientIP = '127.0.0.1'
    global clientSocket

    INITIALIZE()
 # end main()

if __name__ == "__main__":
    main()
# end if