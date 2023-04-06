import os
import struct
import ctypes
import socket

BUFFER_SIZE = 1024
COOR_MESSAGE_TYPE = 1
FROM_PY_TO_C = 2
FROM_C_TO_PY = 3

class Object_type(ctypes.Structure):
    _fields_ = [
        ('typeObject', ctypes.c_uint16),
        ('metaData', ctypes.c_uint16),
    ]

class Msg_body(ctypes.Structure):
    _fields_ = [
        ('object_type', Object_type),
        ('object_size', ctypes.c_uint32),
        ('id_object', ctypes.c_uint32),
        ('id_player', ctypes.c_uint16),
        ('data', ctypes.c_char * BUFFER_SIZE),
    ]

class Message(ctypes.Structure):
    _fields_ = [
        ('message_type', ctypes.c_long),
        ('msg_body', Msg_body),
    ]


def message_to_send(type_object, meta_data, id_object, id_player, data, encode=True):
    if encode:
        data = data.encode()
        print(data)

    object_size = len(data)

    format_send_types = f"=H H L L H H {object_size}s"
    sending_message = struct.pack(format_send_types,
                                  type_object, meta_data,
                                  object_size,
                                  id_object,
                                  id_player,
                                  65535,
                                  data)

    return sending_message

server_address = "/tmp/socket"
if os.path.exists(server_address):
    os.remove(server_address)


# Create a Unix domain socket
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# Bind the socket to the server address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

# Wait for a connection
print(f"Waiting for a connection on {server_address}")
connection, client_address = sock.accept()
print(f"Accepted a connection from {client_address}")

# Send a response to the client
# message = "hello c".encode()
message_ = message_to_send(type_object=1, meta_data=2, id_object=3, id_player=4, data="Hello C")
print(message_)
connection.sendall(message_)

# Close the connection and socket
connection.close()
sock.close()

