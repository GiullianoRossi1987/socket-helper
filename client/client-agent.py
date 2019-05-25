# coding = utf-8
# using namespace std
import socket
from typing import Optional, AnyStr, Any, List
import json
import ftplib
from datetime import date, datetime

dt_hj = "{}/{}/{}".format(date.today().day, date.today().month, date.today().year)
hour_now = "{}:{}".format(datetime.now().hour, datetime.now().minute)


class SocketData(object):
    # file system data
    file_name = AnyStr
    dataSocketClient = dict()

    def __init__(self, filenm="../database/client-data.json"):
        self.file_name = filenm
        with open(filenm, "r") as f: self.dataSocketClient = json.loads(f.read())

    @classmethod
    def update_file(cls):
        n = json.dumps(cls.dataSocketClient)
        with open(cls.file_name, "w") as lsf: lsf.write(n)

    @classmethod
    def alter_data(cls, camp: str, val):
        cls.dataSocketClient[camp] = val
        cls.update_file()

    @classmethod
    def show_data(cls, type_to_show: Optional[Any] = str) -> Any:
        if type_to_show is str:
            return json.dumps(cls.dataSocketClient)
        elif type_to_show is list or type_to_show is iter:
            s = []
            for i , l in cls.dataSocketClient:
                s.append(l)
            return s
        elif type_to_show is tuple:
            return tuple(cls.show_data(list))
        elif type_to_show is dict:
            return cls.dataSocketClient
        else: TypeError("This type can not be used in this query")


class SocketSystem(object):
    # main tool
    agent = socket.socket()

    # connection vars
    connected = bool
    connected_with_data = list()

    # user system vars
    user_connected_data = list()
    user_connected = bool()
    user_anonymous = bool()

    #system data
    client_all_data = dict()  # imported from client-data.json

    # exceptions here

    class NotConnectedError(Exception):
        args = "There's no such connection with any address to do this action"

    class NotEnoughtUserPermissions(Exception):
        args = "You don't have permission to do this"

    class NoSuchLoginUser(Exception):
        args = "You need to be a user to do this action!"

    def __init__(self, addr: tuple, tp_connection: int = 2):
        self.agent.connect(addr)
        self.connected_with_data = [x for x in addr]
        self.connected_with_data.append(tp_connection)
        self.connected = True
        self.agent.sendto(data=b"Now you are connected with "+bytes(self.client_all_data["Name"]), address=addr)


    @classmethod
    def send_connected_message(cls, addr: tuple):
        cls.agent.sendto(data=b"Now you are connected with "+bytes(cls.client_all_data["Name"]), address=addr)

    @classmethod
    def close_connection(cls, addr: tuple):
        cls.agent.sendto(data=b"Now you are unconnected with " + bytes(cls.client_all_data["Name"]),
                         address=addr)
        cls.connected_with_data = list()
        cls.connected = False

    @classmethod
    def export_connection_reg(cls) -> list:
        return [cls.connected_with_data + cls.user_connected_data]


class FtpAgent(object):
    agent_FTP = ftplib.FTP()

    # ftp client data
    ftp_data = dict()
    connected = bool()
    connected_with_data = list()

    # regs data
    last_downloads = List[dict]
    last_uploads = List[dict]
    last_login = List[dict]

    # user data
    user_connected_now = list()
    user_connected = bool()

    def __init__(self, addr: tuple, message_sended: Optional[bool] = False, user_data: list = list):
        self.agent_FTP.connect(addr[0], addr[1])
        if len(user_data) != 2:
            self.agent_FTP.login()
        else:
            self.agent_FTP.login(user_data[0], user_data[1])
            s = {"UserName": user_data[0], "UserPassword": user_data[1], "Date": dt_hj, "Time": hour_now}
            self.last_login.append(s)
            del s
            self.user_connected = True
            self.user_connected_now = addr
        if not message_sended:
            SocketSystem.send_connected_message(addr)
        self.connected_with_data = [x for x in addr]

    @classmethod
    def download(cls, file_local_path: AnyStr):
        with open(file_local_path, "bw") as download:
            cls.agent_FTP.storbinary("RETR", file_local_path, download.write, 1024)
        n = {
            "Date": dt_hj,
            "Hour": hour_now,
            "FilePath": file_local_path,
            "Addr": cls.connected_with_data,
            "Success": "true",
            "User": cls.user_connected_now[0]
        }
        if not cls.user_connected: n["User"] = "anonymous"
        cls.last_downloads.append(n)
        del n

    @classmethod
    def change_dir_remote(cls, path: AnyStr):
        cls.agent_FTP.cwd(path)
        n = cls.agent_FTP.dir()
        return n

    @classmethod
    def loggoff(cls):
        cls.agent_FTP.login()

    @classmethod
    def upload_file_to(cls, file_local_path: AnyStr):
        with open(file_local_path, "rb") as upload:
            cls.agent_FTP.storbinary("STOR", upload)
        a = {
            "Date": dt_hj,
            "Time": hour_now,
            "FileLocal": file_local_path,
            "Addr": cls.connected_with_data,
            "Success": "True",
            "User": cls.user_connected_now[0]
        }
        if not cls.user_connected: a["User"] = "anonymous"
        cls.last_uploads.append(a)
        del a

    @classmethod
    def show_dir(cls):
        cls.agent_FTP.dir()





















