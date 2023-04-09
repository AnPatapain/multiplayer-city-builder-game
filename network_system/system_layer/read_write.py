from typing import TYPE_CHECKING

import errno
import json
import os
import socket
import re
import struct
import subprocess
from typing import TypedDict, Optional

from class_types.buildind_types import BuildingTypes
from class_types.network_commands_types import NetworkCommandsTypes
from class_types.road_types import RoadTypes


from game.game_controller import GameController


# from class_types.buildind_types import BuildingTypes

class Header(TypedDict):
    player_id: int
    command: int
    object_size: int
    id_object: int

class Message(TypedDict):
    header: Header
    data: any

class BuildingMsg(TypedDict):
    start: list[int, int]
    end: list[int, int]
    building_type: BuildingTypes | RoadTypes



class SystemInterface:
    instance = None

    def __init__(self):
        self.message_read = None
        self.message_write = None
        self.connection = None
        self.sock = None
        self.player_id = 0
        self.ip = None

        self.is_online = False

    def init_listen(self):

        client_path = "./network_system/client_c"
        if not os.path.exists(client_path):
            print("Error C client not found, please run `make` before play online")
            return

        socket_address = "/tmp/socket"
        if os.path.exists(socket_address):
            os.remove(socket_address)

        # Create a Unix domain socket
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

        # Bind the socket
        self.sock.bind(socket_address)

        # Listen for incoming connections
        self.sock.listen(1)

        # Wait for a connection
        print(f"Waiting for a connection on {socket_address}")

        # Run subprocess here to wait connection before lauch it

        if self.ip:
            c_file = [client_path,self.ip]
        else:
            c_file = [client_path]

        self.pid = subprocess.Popen(c_file)

        connection, client_address = self.sock.accept()
        self.connection = connection

        message = self.read_message(block=True)
        if not message:
            print("error receive C connection")
            return

        if message["header"]["command"] != 400:
            print("bad receive packet")
            return

        self.player_id = message["header"]["player_id"]

        print(f"Found C connection, player id : {self.player_id}")
        gc = GameController.get_instance()
        gc.set_all_player_id(self.player_id)
        self.set_is_online(True)

    def send_message(self, command, id_object, data, encode=True):
        if not self.connection:
            return

        if encode:
            data = data.encode()

        if data:
            object_size = len(data)

            format_send_types = f"=H H L L {object_size}s"
            sending_message = struct.pack(format_send_types,
                                          self.player_id, command,
                                          object_size,
                                          id_object,
                                          data)

        else:
            format_send_types = f"=H H L L"
            sending_message = struct.pack(format_send_types,
                                          self.player_id, command,
                                          0,
                                          id_object)

        return self.connection.sendall(sending_message)

    def read_message(self,block: bool = False) -> Optional[Message]:
        if self.connection is None:
            return None

        header_size = 12
        if not block:
            self.connection.setblocking(0)

        try:
            binary_received_header = self.connection.recv(header_size)
            if binary_received_header == b'':
                return None
        except socket.error as e:
            if e.errno != errno.EAGAIN:
                raise e
            self.connection.setblocking(1)
            return None

        self.connection.setblocking(1)


        header = self.unpack_header(binary_received_header)

        if header["object_size"]:
            binary_received_data = self.connection.recv(header["object_size"], socket.MSG_WAITALL)
            data = self.unpack_data(binary_received_data, header["object_size"])
        else:
            data = None


        self.message_read: Message = {
            "header": header,
            "data": data
        }

        print(self.message_read)
        return self.message_read


    def unpack_data(self, binary_received_data, data_len):
        format = f"={data_len}s"
        #print(format, binary_received_data)
        data = struct.unpack(format, binary_received_data)
        return data
    def unpack_header(self, binary_received_header) -> Header:
        header = struct.unpack("=H H L L", binary_received_header)
        temp_dict = {
            "player_id": header[0],
            "command": header[1],
            "object_size": header[2],
            "id_object": header[3]
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
        self.init_listen()

        # return output.decode("utf-8")

    #methode pour stoper le process

    def stop_subprocess(self):

        self.pid.terminate()
        self.set_is_online(False)
        self.player_id = 0
        GameController.get_instance().set_all_player_id(0)
        self.connection = None
#..............................................................................#
    def send_disconnect(self):
        pass

    def recieve_disconnect(self, datas):
        pass


    def recieve_connect(self, datas):
        pass



    def send_game_save(self):
        import pickle
        read_write_py_c = SystemInterface.get_instance()
        serialize_data = pickle.dumps(GameController.get_instance().__dict__)
        read_write_py_c.send_message(command=NetworkCommandsTypes.GAME_SAVE, id_object=1, data=serialize_data, encode=False)

    def recieve_game_save(self):
        import pickle

        message = self.read_message(block=True)

        if message["header"]["command"] != NetworkCommandsTypes.GAME_SAVE:
            return

        GameController.get_instance().__dict__ = pickle.loads(message["data"][0])
        GameController.get_instance().save_load()

    def send_delete_buildings(self, start, end):
        pass

    def recieve_delete_buildings(self, datas):
        pass

    def get_ip(self):
        return self.ip

    def set_ip(self,ip: str):
        self.ip = ip

    """
    Build message format:
    {
        "start": [x, y],
        "end": [x, y],
        "building_type": building_type from the enum,
    } """
    def send_build(self, start: list[int, int], end: list[int, int], building_type: BuildingTypes | RoadTypes):

        msg: BuildingMsg = {
            "start": start,
            "end": end,
            "building_type": building_type
        }

        self.send_message(command=NetworkCommandsTypes.BUILD, id_object=12, data=json.dumps(msg))
    def recieve_build(self, datas):
        pass

    def get_player_id(self) -> int:
        return self.player_id

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