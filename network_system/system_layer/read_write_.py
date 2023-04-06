import os
import socket
import sys
import re
import struct
import subprocess


class SystemInterface:
    instance = None
    def __init__(self):
        self.message_read = None
        self.message_write = None
        self.connection = None
        self.sock = None
        self.init_server()

    def init_server(self):
        server_address = "/tmp/socket"
        if os.path.exists(server_address):
            os.remove(server_address)

        # Create a Unix domain socket
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

        # Bind the socket to the server address
        self.sock.bind(server_address)

        # Listen for incoming connections
        self.sock.listen(1)

        # Wait for a connection
        print(f"Waiting for a connection on {server_address}")
        connection, client_address = self.sock.accept()
        self.connection = connection

        print(f"Accepted a connection from {client_address}")

    def send_message(self, type_object, meta_data, id_object, id_player, data, encode=True):
        if encode:
            data = data.encode()

        object_size = len(data)

        format_send_types = f"=H H L L H H {object_size}s"
        sending_message = struct.pack(format_send_types,
                                      type_object, meta_data,
                                      object_size,
                                      id_object,
                                      id_player,
                                      65535,
                                      data)

        return self.connection.sendall(sending_message)

    def read_message(self):
        header_size = 16
        binary_received_message = self.connection.recv(header_size)
        print(binary_received_message)
        self.message_read = self.unpack_message(binary_received_message)
        print(self.message_read)

    def unpack_message(self, binary_received_message):
        header = struct.unpack("=H H L L H H", binary_received_message)
        temp_dict = {
            "object_type": {
                "typeObject": header[0],
                "metaData": header[1]
            },
            "object_size": header[2],
            "id_object": header[3],
            "id_player": header[4]
        }
        return temp_dict

    def close_socket(self):
        self.connection.close()
        self.sock.close()

    def get_coordinates(self):
        numbers = []
        pattern = r'\d+'
        for word in self.message_read['data'].split():
            matches = re.findall(pattern, word)
            # if word.isdigit():
            if matches:
                numbers.append(int(float(word)))
        return numbers

    @staticmethod
    def get_instance():
        if SystemInterface.instance is None:
            SystemInterface.instance = SystemInterface()
        return SystemInterface.instance

    #..............................................................................#

    def get_is_online(self):
        return self.is_online

    def set_is_online(self, status: bool):
        self.is_online = status

    #..............................................................................#
    def run_subprocess(self) :

        # RUN PROCESS
        c_file = ["./network_system/system_layer/peer"]
        self.pid = subprocess.Popen(c_file)
        # output, error = self.pid.communicate()

        self.set_is_online(True)

        # return output.decode("utf-8")

    #methode pour stoper le process

    def stop_subprocess(self):

        self.pid.terminate()

        self.set_is_online(False)
#..............................................................................#


def main():
    sysemAgent = SystemInterface.get_instance()
    sysemAgent.send_message(type_object=1, meta_data=2, id_object=3, id_player=4, data="Bonjour C je suis Python")
    sysemAgent.read_message()
main()
