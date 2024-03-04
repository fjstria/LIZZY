# client.py
# Implementation of the client-side behavior of the chat app.

import socket, sys, argparse

# CLIENT FINITE STATE MACHINE ---------------------------------------
def INITIALIZE():
  """
  Initializes the client program.
  """
  # get command line options
  initializeParser = argparse.ArgumentParser()
  initializeParser.add_argument("--id", action='store') 
  initializeParser.add_argument("--port", action='store') 
  initializeParser.add_argument("--server", action='store') 
  args = initializeParser.parse_args()

  # assign options to variables
  clientName = args.id
  clientPort = args.port
  serverIP, serverPort = (args.server).split(":")

  # attempt server connection
  clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  try:
    clientSocket.connect(serverIP, serverPort)
  except:
    print("Error: Connection to server failed.")
    TERMINATE(1)
# end INITIALIZE()

def WAIT():
  pass
# end WAIT()

def CHAT():
  pass
# end CHAT()
  
def TERMINATE(exitCode):
  """
  Terminates the client program.
  """
  clientSocket.close()
  sys.exit(exitCode)
# end TERMINATE()
# -------------------------------------------------------------------

def main():
  global clientSocket
  INITIALIZE()
# end main()

if __name__ == "__main__":
  main()
# end if
