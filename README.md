# Chat App
## Testing
Before running the server the file must have execute permissions – enter `chmod +x server.out`.

`./server.out --port=<server_port> [--debug]` runs the server.

To start the client program, enter `python3 client.py --id=<client_name> --port=<client_port> --server=<server_ip:server_port>`.

## References
Command Line Argument Parsing:
* https://docs.python.org/3.11/library/argparse.html

Exception Handling:
* https://www.programiz.com/python-programming/exception-handling

Socket Programming:
* https://pythontic.com/modules/socket/send
* https://www.geeksforgeeks.org/socket-programming-python/
* https://www.youtube.com/watch?v=_iHMMo7SDfQ