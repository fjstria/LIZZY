# Chat App
## Dependencies
* `python-statemachine`

## Testing
Before running the server the file must have execute permissions – enter `chmod +x server.out`.

`./server.out --port=<server port> [--debug]` runs the server.

To start the client program, enter `python3 client.py --id=<name> --port=<client port> --server=<server ip:port>`.