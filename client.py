# client.py
# Implementation of the client-side behavior of the chat app.

import socket, sys, argparse

# CLIENT FINITE STATE MACHINE ---------------------------------------
def INITIALIZE(name, port):
  serverName = name
  serverPort = port
  clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  clientSocket.connect(serverName, serverPort)
# end INITIALIZE()

def WAIT():
  pass
# end WAIT()

def CHAT():
  pass
# end CHAT()
  
def TERMINATE():
  pass
# end TERMINATE()
# -------------------------------------------------------------------

def main():
  try:
    # get options from command line input
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", action='store') 
    parser.add_argument("--port", action='store') 
    parser.add_argument("--server", action='store') 
    args = parser.parse_args()
    clientName = args.id
    serverPort = args.port
    serverName = args.server
    INITIALIZE()
  except:
    pass
# end main()

if __name__ == "__main__":
  main()
# end if
