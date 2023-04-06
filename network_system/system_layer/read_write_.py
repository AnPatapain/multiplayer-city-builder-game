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

# Receive data from the client
data = connection.recv(1024)
print(f"Received data: {data.decode()}")

# Send a response to the client
message = "Hello, C!".encode()
connection.sendall(message)

# Close the connection and socket
connection.close()
sock.close()

