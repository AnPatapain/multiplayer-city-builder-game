# import sysv_ipc
# import sys
# import re
# import struct
# import subprocess


# # Constants
# KEY = 192002
# COOR_MESSAGE_TYPE = 1

# FROM_PY_TO_C = 2
# FROM_C_TO_PY = 3

# class SystemInterface:

#     instance = None

#     def __init__(self):
#         self.message_queue = sysv_ipc.MessageQueue(KEY, sysv_ipc.IPC_CREAT)
#         self.message = None
#         print(self.message_queue)
#         self.is_online = False
#         self.pid = None

#     def send_message(self, type_object, meta_data, object_size, id_object, id_player, data, encode=True):
        
#         if encode:
#             data = data.encode()
#             print(data)

#         sending_message = struct.pack('=H H L L H 1024s', 
#                                       type_object, meta_data, 
#                                       object_size, 
#                                       id_object, 
#                                       id_player, 
#                                       data)
        
#         self.message_queue.send(sending_message, type=FROM_PY_TO_C)

#     def read_message(self):
#         try:
#             self.message = self.message_queue.receive(type=FROM_C_TO_PY, block=False)
#         except sysv_ipc.BusyError:
#             return False
#         else:
#             self.message = list(self.message)
#             self.message[0] = self.message[0][0:1037]
#             print(self.message)
#             # unpacked_data = struct.unpack("=BHLLH1024s", self.message[0])
#             # print(unpacked_data[5].decode(sys.getdefaultencoding(), errors='ignore'))
#             self.message[0] = self.decode_and_clean_message()
#             return True

#     def decode_and_clean_message(self):
#         # Unpack the message from bytes to Python objects
#         unpacked_data = struct.unpack("=HHLLH1023s", self.message[0])
    
#         temp_dict = {}
#         temp_dict["object_type"] = {
#             "typeObject": unpacked_data[0],
#             "metaData": unpacked_data[1]
#         }
#         temp_dict["object_size"] = unpacked_data[2]
#         temp_dict["id_object"] = unpacked_data[3]
#         temp_dict["id_player"] = unpacked_data[4]
#         temp_dict["data"] = unpacked_data[5].decode(sys.getdefaultencoding(), errors='ignore')
#         temp_dict["data"] = temp_dict["data"].split('\n')[0]
#         temp_dict["data"] = temp_dict["data"].rstrip('\0')

#         print(temp_dict["object_type"])
#         print(temp_dict["object_size"])
#         print(temp_dict["id_object"])
#         print(temp_dict["id_player"])
#         print(temp_dict["data"])

#         return temp_dict
    
#     def get_message(self): return self.message[0]['data']

#     def get_coordinates(self):
#         numbers = []
#         pattern = r'\d+'
#         for word in self.message[0]['data'].split():
#             matches = re.findall(pattern, word)
#             # if word.isdigit():
#             if matches:   
#                 numbers.append(int(float(word)))
#         return numbers

#     @staticmethod
#     def get_instance():
#         if SystemInterface.instance is None:
#             SystemInterface.instance = SystemInterface()
#         return SystemInterface.instance


import os
import struct
import ctypes

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

def main():
    # Generate a unique key for the message queue
    key = os.ftok('msgq.txt', 'A')

    # Get the message queue ID
    msgid = os.msgget(key, 0)

    # Create a message to send to C
    msg = Message()
    msg.message_type = FROM_PY_TO_C
    msg.msg_body.object_type.typeObject = COOR_MESSAGE_TYPE
    msg.msg_body.object_type.metaData = 0
    msg.msg_body.object_size = 12
    msg.msg_body.id_object = 42
    msg.msg_body.id_player = 1
