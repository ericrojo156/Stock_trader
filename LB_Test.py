from websock import WebSocketServer


def on_data_receive(client, data):
    """Called by the WebSocketServer when data is received."""

    if data == "disconnect":
        ws.close_client(client)
    else:
        data += '!'
        print(data)
        ws.send(client, data)


def on_connection_open(client):
    """Called by the WebSocketServer when a new connection is opened.
    """
    ws.send(client, "Welcome to the echo server!")


def on_error(exception):
    """Called when the server returns an error
    """
    raise exception


def on_connection_close(client):
    """Called by the WebSocketServer when a connection is closed."""
    ws.send(client, "Closing socket")


def on_server_destruct():
    """Called immediately prior to the WebSocketServer shutting down."""
    pass


ws = WebSocketServer("127.0.0.1", 44421,
                     on_data_receive=on_data_receive,
                     on_connection_open=on_connection_open,
                     on_error=on_error,
                     on_connection_close=on_connection_close)
ws.serve_forever()
