import random as rd

class   ID_GEN:
    def __init__(self):
        self.id_list = set()

    def id_gen(self):
        while True:
            id = rd.getrandbits(64)
            if id not in self.id_list:
                self.id_list.add(id)
                return id
                

#id_create=ID_GEN()
#for i in range(10):
 #   unique_id = id_create.id_gen()
  #  print(unique_id)




