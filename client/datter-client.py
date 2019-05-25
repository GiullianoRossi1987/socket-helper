# coding = utf-8
# using namespace std
from typing import Type, AnyStr


class DatFile(object):
    data_client = list()
    file_dat = AnyStr

    def __init__(self, fl_nm="database/logs-client.dat"):
        self.file_dat = fl_nm
        with open(fl_nm, "r") as fl: self.data_client = fl.readlines()

    @classmethod
    def update_reg(cls):
        n = ""
        for i in cls.data_client:
            n += i + "\n"
        with open(cls.file_dat, "w") as fl: fl.write(n)
        del n

    @classmethod
    def add_reg(cls, data: list):
        cls.data_client.append(data)
        cls.update_reg()

    @classmethod
    def show_regs(cls):
        return "\n".join(cls.data_client)



