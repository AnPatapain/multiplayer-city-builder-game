import sysv_ipc
import sys
import re
import struct
import subprocess


# Constants
KEY = 192002
COOR_MESSAGE_TYPE = 1

FROM_PY_TO_C = 2
FROM_C_TO_PY = 3

class SystemInterface:

    instance = None

    def __init__(self):
        self.message_queue = sysv_ipc.MessageQueue(KEY, sysv_ipc.IPC_CREAT)
        self.message = None
        print(self.message_queue)
        self.is_online = False
        self.pid = None

    def send_message(self, type_object, meta_data, object_size, id_object, id_player, data, encode=True):
        
        if encode:
            data = data.encode()
            print(data)

        sending_message = struct.pack('=H H L L H 1024s', 
                                      type_object, meta_data, 
                                      object_size, 
                                      id_object, 
                                      id_player, 
                                      data)
        
        self.message_queue.send(sending_message, type=FROM_PY_TO_C)

    def read_message(self):
        try:
            self.message = self.message_queue.receive(type=FROM_C_TO_PY, block=False)
        except sysv_ipc.BusyError:
            return False
        else:
            self.message = list(self.message)
            self.message[0] = self.message[0][0:1037]
            print(self.message)
            # unpacked_data = struct.unpack("=BHLLH1024s", self.message[0])
            # print(unpacked_data[5].decode(sys.getdefaultencoding(), errors='ignore'))
            self.message[0] = self.decode_and_clean_message()
            return True

    def decode_and_clean_message(self):
        # Unpack the message from bytes to Python objects
        unpacked_data = struct.unpack("=HHLLH1023s", self.message[0])
    
        temp_dict = {}
        temp_dict["object_type"] = {
            "typeObject": unpacked_data[0],
            "metaData": unpacked_data[1]
        }
        temp_dict["object_size"] = unpacked_data[2]
        temp_dict["id_object"] = unpacked_data[3]
        temp_dict["id_player"] = unpacked_data[4]
        temp_dict["data"] = unpacked_data[5].decode(sys.getdefaultencoding(), errors='ignore')
        temp_dict["data"] = temp_dict["data"].split('\n')[0]
        temp_dict["data"] = temp_dict["data"].rstrip('\0')

        print(temp_dict["object_type"])
        print(temp_dict["object_size"])
        print(temp_dict["id_object"])
        print(temp_dict["id_player"])
        print(temp_dict["data"])

        return temp_dict
    
    def get_message(self): return self.message[0]['data']

    def get_coordinates(self):
        numbers = []
        pattern = r'\d+'
        for word in self.message[0]['data'].split():
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

    # def __init__(self, is_online=False):
    #     self.is_online = is_online

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



    def send_build(self, start, end, building, building_id):
        pass

    def recieve_build(self, datas):
        pass



    def send_risk_update(self, risk_type, building_id):
        pass

    def recieve_risk_update(self, datas):
        pass



    def send_walker_direction_update(self, new_direction, walker_id):
        pass

    def recieve_walker_direction_update(self, datas):
        pass



    def send_spawn_walker(self, pos, walker_type, walker_id):
        pass

    def recieve_spawn_walker(self, datas):
        pass



    def send_delete_walker(self, walker_id):
        pass

    def recieve_delete_walker(self, datas):
        pass
