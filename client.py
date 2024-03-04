# client.py
# Implementation of the client-side behavior of the chat app.

import socket, sys, argparse

# CLIENT FINITE STATE MACHINE ---------------------------------------
def INITIALIZE(sName, sPort):
  serverName = sName
  serverPort = sPort
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
    clientPort = args.port
    serverName, serverPort = (args.server).split(":")
    INITIALIZE(serverName, serverPort)
  except:
    print("Error: Argument parsing failed. Client was not initialized.")
# end main()

if __name__ == "__main__":
  main()
# end if
