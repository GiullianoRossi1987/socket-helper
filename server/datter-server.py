# coding  = utf-8
# using namespace std


class DatFile(object):
    rgs_data = list()
    init = False  

    class NonInitalizedError(Exception):
        args = "The system needs to be initialized to do this action"

    def __init__(self):
        with open("database/logs-server.dat", "r") as file:
            self.rgs_data = file.readlines() # or file.read().split(("\b"*4))
        self.init = True
    
    @classmethod
    def update_commit_file(cls):
        if not cls.init: raise cls.NonInitalizedError()
        s = "\n".join(cls.rgs_data)
        with open("database/logs-server.dat", "w") as dat_file: 
            dat_file.write(s)
        del s
    
    @classmethod
    def add_reg(cls, data: list):
        if not cls.init: 
            raise cls.NonInitalizedError()
        cls.rgs_data.append(data)
        cls.update_commit_file()




