# coding = utf-8
# using namespace std
import sqlite3
from json import loads, dumps
import typing


class DatabaseConnection(object):
    connection = sqlite3.connect("../database/database-client.db")
    cursor = connection.cursor()
    initialized = False

    class WrongDatabaseSystem(Exception):
        args = "This database cannot be used as the system database!"

    def __init__(self, file_name="/database/database-client.db"):
        self.connection = sqlite3.connect(file_name)
        self.cursor = self.connection.cursor()
    

    @classmethod
    def check_database_useful(cls) -> list: 
        try:
            s = cls.cursor.execute("select * from tb_ips_servers;")
            n = cls.cursor.execute("select * from tb_users;")
        except Exception as error:
            return [False, error.args]
        del s, n 
        return [True, "usefull database"]


class Users(DatabaseConnection):

    user_logged_data = list
    user_logged = bool
    user_annonymous = bool


    class UserNotFound(Exception):
        args = "There's no user as this!"
    
    class UserExistsError(Exception):
        args = "This user already exists in database!"
    
    class NotLoggedUser(Exception):
        args = "To do this action you have to be logged as user and not annonymous!"
    
    @classmethod
    def user_exists(cls, user: str) -> bool:
        n = cls.cursor.execute("select nm_user from tb_users;")
        for i in n.fetchall():
            if i[0] == user: return True
        del n 
        return False
    
    @classmethod
    def usr_enoght_permissions(cls) -> bool:
        if not cls.user_logged: raise cls.NotLoggedUser()
        return cls.user_logged_data[2] and not cls.user_annonymous
    
    @classmethod
    def add_user(cls, user_data: list, duplicate_trade=False):
        if cls.user_exists(user_data[0]) and not duplicate_trade: raise cls.UserExistsError()
        if not cls.user_logged_data[2] or cls.user_annonymous or (user_data[2] and not cls.user_logged_data[2]): 
            raise PermissionError("Yor user don't have enought permissions to do this action")
        n = cls.cursor.execute("insert into tb_users (nm_user, password, is_root)")
        cls.connection.commit()
        del n 

    @classmethod
    def del_user(cls, user_nm: str):
        if not cls.user_exists(user_nm): raise cls.UserNotFound()
        if not cls.user_logged_data[2]: 
            raise PermissionError("You don't have enought")
        n = cls.cursor.execute(f"delete from tb_users where nm_user = '{user_nm}';")
        cls.connection.commit()
        del n
    
    @classmethod
    def alt_user(cls, usr_name: str, camp: str, vl_cmp):
        if not cls.user_exists: raise cls.UserNotFound()
        if not cls.usr_enoght_permissions: raise PermissionError()
        a = cls.cursor.execute(f"update tb_users set {camp} = '{vl_cmp}' where nm_user = '{usr_name}';")
        cls.connection.commit()
        del a 

    @classmethod
    def set_logged_data(cls, user_name: str) -> bool:
        if not cls.user_exists(user_name): raise cls.UserNotFound()
        n = cls.cursor.execute(f"select nm_user, password, is_root from tb_users where nm_user = '{user_name}';")
        cls.user_logged_data = n.fetchall()[0]
        cls.user_logged = True
    
    @classmethod
    def unset_user_data(cls, continue_using: typing.Optional[bool] = False):
        cls.user_logged = False
        cls.user_logged_data = typing.Type[list]
        if continue_using: cls.user_annonymous = True
    
    @classmethod
    def query_user_all_camp(cls, camp: str):
        n = cls.cursor.execute(f"select {camp} from tb_users;")
        return n.fetchall()
    
    @classmethod
    def query_user_param(cls, param: str, vl):
        if vl is str:
            return cls.cursor.execute(f"select * from tb_users where {param} = '{vl}';").fetchall()
        elif vl is bool:
            a = vl
            vl = int(a)
            del a 
            return cls.cursor.execute(f"select * from tb_users where {param} = '{vl}';").fetchall()
        else:
            return cls.cursor.execute(f"select * from tb_users where {param} = {vl};").fetchall()
        

class ServerDatabase(DatabaseConnection):

    class ServerDataNotFound(Exception):
        args = "There's no data such as in the database"
    
    class ServerDataExists(Exception):
        args = "This server already exists with this data!"
    
    class PortConfigurationError(Exception):
        args = "This port is not useful"

    
    @classmethod
    def selesctConfigId(cls, server_data: list) -> int:
        if not cls.server_config_exists(server_data): raise cls.ServerDataNotFound()
        s = cls.cursor.execute("select cd_server from tb_ips_servers where host_name = '?' and ip_con = '?' and ports = '?';", server_data)
        return int(s.fetchall()[0])
    
    @classmethod
    def convert_ports(cls, ports: str) -> typing.List[int]:
        if "/" in ports:
            n = ports.split("/")
            n.remove("/")
            return [int(x) for x in n]
        elif len(ports) <= 4 and len(ports) > 0:
            return [int(ports)]
        else:
            raise cls.PortConfigurationError()
    
    @classmethod
    def server_config_exists(cls, server_data: list) -> bool:
        s = cls.cursor.execute("select ip_con, host_name, ports from tb_ips_servers;")
        for i in s.fetchall():
            if i == server_data: return True
        del s 
        return False
    
    @classmethod
    def add_server_config(cls, server_config_data: list):
        if cls.server_config_exists(server_config_data): raise cls.ServerDataExists()
        n = cls.cursor.execute("insert into tb_ips_servers (ip_con, host_name, ports) values (?,?,?);", server_config_data)
        del n
        cls.connection.commit()
    
    @classmethod
    def del_server_config(cls, server_config:list):
        if not cls.server_config_exists(server_config): raise cls.ServerDataNotFound()
        id_conf = cls.selesctConfigId(server_config)
        n = cls.cursor.execute("delete from tb_ips_servers where cd_server = ?;", [id_conf])
        del n, id_conf
        cls.connection.commit()
    
    @classmethod
    def alt_server_config(cls, server_config: list, camp_to_alter:str, vl: str):
        if not cls.server_config_exists(server_config): raise cls.ServerDataNotFound()
        n = cls.cursor.execute("update tb_ips_servers set ? = '?' where cd_server = ?;", [camp_to_alter, vl, server_config])
        del n 
        cls.connection.commit()
    
    @classmethod
    def query_all_servers(cls, camp: str):
        return cls.cursor.execute(f"select {camp} from tb_ips_servers;").fetchall()
    
    @classmethod
    def query_server_all_param(cls, param: str, vl):
        if vl is str:
            return cls.cursor.execute(f"select * from tb_ips_servers where {param} = '{vl}';").fetchall()
        elif vl is bool:
            a = vl
            vl = int(a)
            del a 
            return cls.cursor.execute(f"select * from tb_ips_servers where {param} = '{vl}';").fetchall()
        else:
            return cls.cursor.execute(f"select * from tb_ips_servers where {param} = {vl};").fetchall()
    
        

        
            
            


    

        




        
        















