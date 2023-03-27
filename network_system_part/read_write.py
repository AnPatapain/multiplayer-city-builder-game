import sysv_ipc
import sys
import re

# Constants
KEY = 192002
COOR_MESSAGE_TYPE = 1

FROM_PY_TO_C = 2
FROM_C_TO_PY = 3

class NetworkInterface:

    instance = None

    def __init__(self):
        self.message_queue = sysv_ipc.MessageQueue(KEY, sysv_ipc.IPC_CREAT)
        self.message = None
        print(self.message_queue)
        self.is_online = False

    def send_message(self, message):
        self.message_queue.send(message.encode(), type=FROM_PY_TO_C)

    def read_message(self):
        try:
            # print(self.message_queue)
            self.message = self.message_queue.receive(type=FROM_C_TO_PY, block=False)
        except sysv_ipc.BusyError:
            return False
        else:
            self.message = self.decode_and_clean_message()
            return True

    def decode_and_clean_message(self):
        temp_list = list(self.message)
        temp_list[0] = self.message[0].decode(sys.getdefaultencoding(), errors='ignore')
        temp_list[0] = temp_list[0].split('\n')[0]
        temp_list[0] = temp_list[0].rstrip('\0')
        # print(temp_list[0])
        temp_list[1] = self.message[1]
        return tuple(temp_list)
    
    def get_message(self): return self.message[0]

    def get_coordinates(self):
        numbers = []
        pattern = r'\d+'
        for word in self.message[0].split():
            matches = re.findall(pattern, word)
            # if word.isdigit():
            if matches:   
                numbers.append(int(float(word)))
        return numbers

    @staticmethod
    def get_instance():
        if NetworkInterface.instance is None:
            NetworkInterface.instance = NetworkInterface()
        return NetworkInterface.instance


#..............................................................................#

    # def __init__(self, is_online=False):
    #     self.is_online = is_online

    def get_is_online(self):
        return self.is_online

    def set_is_online(self, status: bool):
        self.is_online = status
        
#..............................................................................#
 