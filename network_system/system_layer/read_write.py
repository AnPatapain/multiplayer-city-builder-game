import json
import os
import socket
import sys
import re
import struct
import subprocess
from typing import TypedDict

from class_types.buildind_types import BuildingTypes
from class_types.network_commands_types import NetworkCommandsTypes


# from class_types.buildind_types import BuildingTypes



class BuildingMsg(TypedDict):
    start: list[int, int]
    end: list[int, int]
    building_type: BuildingTypes



class SystemInterface:
    instance = None

    def __init__(self):
        self.message_read = None
        self.message_write = None
        self.connection = None
        self.sock = None

        self.is_online = False

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

    def send_message(self, id_player, command, id_object, data, encode=True):
        if encode:
            data = data.encode()

        object_size = len(data)

        format_send_types = f"=H H L L {object_size}s"
        sending_message = struct.pack(format_send_types,
                                      id_player, command,
                                      object_size,
                                      id_object,
                                      data)

        return self.connection.sendall(sending_message)

    def read_message(self):
        header_size = 16
        binary_received_header = self.connection.recv(header_size)
        header = self.unpack_header(binary_received_header)

        binary_received_data = self.connection.recv(header["object_size"])
        data = self.unpack_data(binary_received_data, header["object_size"])

        class Message(TypedDict):
            header: any
            data: any

        self.message_read: Message = {
            "header": header,
            "data": data
        }

        print(self.message_read)

    def unpack_data(self, binary_received_data, data_len):
        format = f"={data_len}s"
        print(format, binary_received_data)
        data = struct.unpack(format, binary_received_data)
        return data
    def unpack_header(self, binary_received_header):
        header = struct.unpack("=H H L L H H", binary_received_header)
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
        c_file = ["./network_system/network_layer/test"]
        self.pid = subprocess.Popen(c_file)
        # output, error = self.pid.communicate()

        self.init_server()

        self.set_is_online(True)

        # return output.decode("utf-8")

    #methode pour stoper le process

    def stop_subprocess(self):

        self.pid.terminate()

        self.set_is_online(False)
#..............................................................................#
    def send_disconnect(self):
        pass

    def recieve_disconnect(self, datas):
        pass



    def send_connect(self, ip):
        pass

    def recieve_connect(self, datas):
        pass



    def send_game_save(self):
        pass

    def recieve_game_save(self, datas):
        pass



    def send_delete_buildings(self, start, end):
        pass

    def recieve_delete_buildings(self, datas):
        pass



    """
    Build message format:
    {
        "start": [x, y],
        "end": [x, y],
        "building_type": building_type from the enum,
    } """
    def send_build(self, start: list[int, int], end: list[int, int], building_type: BuildingTypes):
        from game.game_controller import GameController

        msg: BuildingMsg = {
            "start": start,
            "end": end,
            "building_type": building_type
        }

        self.send_message(
            id_player=GameController.get_instance().total_day,
            command=NetworkCommandsTypes.BUILD,
            id_object=None,
            data=json.dumps(msg)
        )

    def recieve_build(self, datas):
        pass



    # def send_risk_update(self, risk_type, building_id):
    #     pass
    #
    # def recieve_risk_update(self, datas):
    #     pass
    #
    #
    #
    # def send_walker_direction_update(self, new_direction, walker_id):
    #     pass
    #
    # def recieve_walker_direction_update(self, datas):
    #     pass
    #
    #
    #
    # def send_spawn_walker(self, pos, walker_type, walker_id):
    #     pass
    #
    # def recieve_spawn_walker(self, datas):
    #     pass
    #
    #
    #
    # def send_delete_walker(self, walker_id):
    #     pass
    #
    # def recieve_delete_walker(self, datas):
    #     pass


# def main():
#     system_agent = SystemInterface.get_instance()
#     system_agent.send_message(id_player=1, command=2, id_object=3, data="Bonjour C je suis Python")
#     # system_agent.read_message()
#
#
# main()
