# client.py
# Implementation of the client-side behavior of the chat app.

import socket, sys, argparse

# CLIENT FINITE STATE MACHINE ---------------------------------------
def INITIALIZE():
    """
    Initializes the client program.
    """
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

    # attempt server connection
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientIP = '127.0.0.1'
    try:
        clientSocket.connect((serverIP, int(serverPort)))
        print("{} running on {}".format(clientName, clientIP))
    except:
        print("Error: Connection failed.", file=sys.stderr)
        TERMINATE(1)  # exit code for error

    # get client input for next action!
    try:
        while True:
            userInput = input(">")
            if userInput == "/id":
                print("User ID:", clientName)
            elif userInput == "/register":
                registerRequest = "REGISTER\r\nclientID: {}\r\nIP: {}\r\nPort: {}\r\n\r\n".format(clientName, clientIP, clientPort)
                clientSocket.send(registerRequest.encode())
                clientData = (clientSocket.recv(1024)).decode()
                try:
                    assert clientData == ("REGACK\r\nclientID: {}\r\nIP: {}\r\nPort: {}\r\n\r\n".format(clientName, clientIP, clientPort))
                except:
                    print("Error: Invalid REGACK.", file=sys.stderr)
                    TERMINATE(1)
            elif userInput == "/bridge":
                bridgeRequest = "BRIDGE\r\nclientID: {}\r\n\r\n".format(clientName)
                clientSocket.send(bridgeRequest.encode())
                bridgeData = (clientSocket.recv(1024)).decode()
                print("Response from server:", bridgeData)  # end point for part 1
                if (bridgeData == ""):
                    WAIT()
                else:
                    CHAT()
    except KeyboardInterrupt:
        TERMINATE(130)  # exit code for ctrl+c
    except Exception as e:
        print("Error:", e, file=sys.stderr)
        TERMINATE(1)
    # end while
# end INITIALIZE()

def WAIT():
    print("Entered WAIT State.")
    TERMINATE(0)  # exit code for success

def CHAT():
    print("Entered CHAT State.")
    TERMINATE(0)

def TERMINATE(exitCode):
    """
    Terminates the client program.
    """
    clientSocket.close()
    sys.exit(exitCode)
# end TERMINATE()
# -------------------------------------------------------------------

def main():
    INITIALIZE()

if __name__ == "__main__":
    main()
