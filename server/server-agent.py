# coding = utf-8
# using namespace std
import socket
import ftplib
from typing import Type, Optional, List, AnyStr
import json
from base64 import b64decode, b64encode
from datetime import date, datetime

__doc__ = """"""


class ServerData(object):
    # the socket agent will be the connection main tool
    # Main tool:
    agent = socket.socket()

    # connection data
    last_connections_today = Type[list, tuple]
    connected = bool()
    connected_with_ip = str 
    connected_with_port = int
    connected_type_connection = Type[int, str, None]

    # server data
    server_data = dict()
    initialized_data = bool 
    accepted_ports = Type[list, tuple]

    # [user_name, password, is_root]
    user_server_command_data = Type[list, tuple]

    class DatabasePermissionError(Exception):
        args = "This host can't be accepted by the system.\nIt's not acceptable!"
    
    class ConnectionNotFound(Exception):
        args = "There's no ip such it connected!"
    
    class PortPermissionError(Exception):
        args = "You don't have enoght permissions to use this port"
    

    def __init__(self, addr: tuple, tp_ip="host", action="--accept", tp_connection: Type[int, str] = "--message-tiping"):
        self.import_server_data_from_file()  # import all data from the std file, like a BIOS
        if tp_ip == "host": # to get the real ip from the hostname
            self.agent.bind((socket.gethostbyname(addr[0]), addr[1]))
        else:
            self.agent.bind(addr)
        if action == "--accept":  # if the system will accept the connection or refuse it
            self.agent.accept()
            self.agent.sendto(b"To connect as sucessful please type: Y", address=addr)
            n = repr(self.agent.recv(1024))
            if n == "Y":
                self.connected = True
                self.agent.sendto(b"You are now connected to "+self.server_data["ServerName"], address=addr)
            else:
                self.agent.close()
                self.connected = False
                print("Was unable to connect with {addr[0]}.\nIt was interrupted by user action.")
        elif action == "--deny":
            self.agent.sendto(b"You were refused by '"+self.server_data["ServerName"]+"'\n Have a nice day!", address=addr)
            self.last_connections_today = [addr, tp_connection, "--refused"]
            self.agent.close()
            

    
    
    def import_server_data_from_file(self, file_config="database/server-data.json"):
        with open(file_config, "r", encoding="utf-8") as file_data:
            self.server_data = json.loads(file_data.read())
            self.initialized_data = True
            
    
    def close_connection(self, forced: Optional[bool] = False):
        if not self.connected: raise self.ConnectionNotFound()
        if forced:
            self.agent.sendto(address=(self.connected_with_ip, self.connected_with_port), data=b"--force-down-connection")
            self.agent.close()
            self.connected_with_ip = str()
            self.connected = False
        else:
            self.agent.sendto(b"Closing connection here!" ,address=(self.connected_with_ip, self.connected_with_port))
            self.agent.close()
            self.connected_with_ip = str()
            self.connected_with_port = int()
            self.connected = False

    def permited_port(self, port: int) -> bool:
        if bool(self.user_server_command_data[2]):
            return True 
        else:
            for i in self.accepted_ports:
                if int(i[0]) == port: return True
            return False 
    
    def get_database_data(self, ports_lists: Type[list, tuple], user_data: Type[list, tuple], 
                                                        annonimous_user: Optional[bool] = False):
        self.accepted_ports = ports_lists
        if not annonimous_user:
            self.user_server_command_data = user_data
        else:
            from random import randint
            port_to_use = randint(1, 1000)
            while True:
                if port_to_use in self.accepted_ports: break
                port_to_use = randint(1, 1000)
            self.user_server_command_data = ["Annonymous", "None", port_to_use]
    
    def export_regist_data(self) -> Type[str, bytes]:
        all_data_connection = ("Std-Socket-System",self.connected_with_ip, self.connected_with_port, self.connected_type_connection)
        return ("\b"*4).join(all_data_connection)
    
    def send_connection_message_to(self, addr=tuple, server_name: Optional[str] = [server_data["Name"]]):
        self.agent.connect(addr)
        self.agent.sendto(b"You're now connected with '"+server_name+"' !", address=addr)
        self.agent.close()
    
    def get_data_from(self, addr=tuple, tp_addr: Optional[bytes, str] = bytes):
        self.agent.connect(addr)
        n = self.agent.recvfrom(1024, addr)
        if tp_addr is bytes: return n 
        else: return repr(n)
        

class FtpAgentSystem(object):

    ftp_agent = ftplib.FTP()  # the main tool, like the ServerData.agent
    addr_data = Type[list, tuple]  # probably exported from ServerData
    lasts_downloads = [
        {"Download_File_From": str, "At_Port": int, "File_Downloaded": str}  # the path to downloaded file
    ]
    lasts_uploads = [
        {"Uploaded_File_To": str, "At_Port": int, "Uploaded": str} # the path to the uploaded file
        # obvisly will have a copy from the file that be uploaded
    ]
    ft_connection_ = bool

    # ports to the connection
    __const_port = 21
    accepted_ports: list = List[int]

    # ftp system data
    ftp_system_data = Type[dict]
    imported_system_data = bool

    class UnablePort(Exception):
        args = "This port to use in the connection is not accepted by the system"
    
    class ConnectionNotSelected(Exception):
        args = "The system is not connected at all\nThis action is impossible"


    def __init__(self, addr=Type[list, tuple], timeout_connection: Optional[int] = 10):
        if addr[1] not in self.accepted_ports: raise self.UnablePort()
        self.ftp_agent.connect(addr[0], int(addr[1]), timeout=timeout_connection)
        ServerData.send_connection_message_to(addr, self.ftp_system_data["ServerName"])
        self.ft_connection_ = True

    

    def import_ftp_data(self, file_config="/database/ftp-all-data.json"):
        with open(file_config, "r", encoding="utf-8") as dl:
            self.ftp_system_data = json.loads(dl.read())["Server-Data"]
        self.imported_system_data = True
    
    def export_regist_downloads(self) -> str:
        s = ""
        for download in self.lasts_downloads:
            n = ["Ftp-System"]
            for key, item in download: n.append(item)
            s += ("\b"*4).join(n)
        return s 
    
    def export_regist_uploads(self) -> str:
        s = ""
        for download in self.lasts_uploads:
            n = ["Ftp-System"]
            for key, item in download: n.append(item)
            s += ("\b"*4).join(n)
        return s 
    
    def change_action_download(self, file_path: str):
        dt_today = "{}/{}/{}".format(date.today().day, date.today().month, date.today().year)
        hour_now = "{}:{}".format(datetime.now().hour, datetime.now().minute)
        self.lasts_downloads.append({
            "Download_File_From": self.addr_data[0], "At_Port": self.addr_data[1], "File_Downloaded": file_path, "Date": dt_today, "Time": hour_now
        })
    
    def change_action_uploads(self, file_path: str):
        dt_today = "{}/{}/{}".format(date.today().day, date.today().month, date.today().year)
        hour_now = "{}:{}".format(datetime.now().hour, datetime.now().minute)
        self.lasts_uploads.append({
            "Download_File_From": self.addr_data[0], "At_Port": self.addr_data[1], "File_Downloaded": file_path, "Date": dt_today, "Time": hour_now
        })


    def upload_file(self, file_path: Type[str, bytes]):
        with open(file_path, "rb") as upload:
            self.ftp_agent.storbinary("STOR", upload.read())
        print("File Uploaded!")
        self.change_action_uploads(file_path)
    
    def download_file(self, file_path: Type[str,bytes], file_name: Type[str, bytes]):
        with open(file_path+"/"+file_name, "wb") as local:
            self.ftp_agent.storbinary("RETR", file_name,local.write(), 2000)
        print("File Downloaded")
        self.change_action_download(file_path+"/"+file_name)
    
    def close_connection(self): 
        self.addr_data = Type[list, tuple, iter]
        self.ftp_agent.quit()
        self.ft_connection_ = False
    

        



        





            
        

    

        



    
    
