# coding = utf-8
# using namespace std
import sqlite3
from typing import Type


class Database(object):
    con = sqlite3.Connection()
    cursor = con.cursor()

    def __init__(self):
        self.con = sqlite3.connect("database/database-server.db", timeout=10)
        self.cursor = self.con.cursor()
    

class Connections(Database):
    """
    This class works with the connections database system
    there's 
    """

    class ConnectionNotFound(Exception): args = "This connection wasn't found in the database"
    
    @classmethod
    def connection_exists(cls, addr: tuple):
        a = cls.cursor.execute("select Host_Bind, At_Port from tb_connections;")
        for i in a.fetchall():
            if i[0] == addr[0] and i[1] == addr[1]: return True
        del a
        return False 
    
    @classmethod
    def add_connection(cls, data: list):
        n = cls.cursor.execute("insert into tb_connections(Host_Bind, At_Port) values (?,?);", data)
        del n 
        cls.con.commit()
    
    @classmethod
    def del_connection(cls, address: tuple):
        if not cls.connection_exists(address): raise cls.ConnectionNotFound()
        b = cls.cursor.execute(f"delete from tb_connections where Host_Bind = '{address[0]}' and At_Port = {address[1]};")
        cls.con.commit()
        del b 
    


class IpsStandarts(Database):

    class IpNotFound(Exception): args = "This IP is not in the database"
    
    class IpExistsError(Exception): args = "This IP already exists in the database"
    
    @classmethod
    def ip_exists(cls, addr: list):
        b = cls.cursor.execute("select Host_Ip, port from tb_ips_std;")
        for i in b.fetchall():
            if i[0] == addr[0] and i[1] == addr[1]: return True
        del b
        return False
    
    @classmethod
    def add_addr(cls, data: list):
        if cls.ip_exists(data[:1]): 
            raise cls.IpExistsError()
        a = cls.cursor.execute("insert into tb_ips_std (Host_Ip, port, Action_To_Server) values (?,?,?);", data)
        cls.con.commit()
        del a 

    @classmethod
    def del_addr(cls, addr: list):
        if not cls.ip_exists(addr): raise cls.IpNotFound()
        a = cls.cursor.execute(f"delete from tb_ips_std where Host_Ip = '{addr[0]}' and port = {addr[1]};")
        del a 
        cls.con.commit()
    
    @classmethod
    def alt_addr(cls, addr: list, camp_alt: str, vl):
        if not cls.ip_exists(addr): raise cls.IpNotFound()
        if vl is str:
            a = cls.cursor.execute(f"update tb_ips_std set {camp_alt} = '{vl}' where Host_Ip = '{addr[0]}' and port = {addr[1]};")
        else: a = cls.cursor.execute(f"update tb_ips_std set {camp_alt} = {vl} where Host_Ip = '{addr[0]}' and port = {addr[1]};")
        del a 
        cls.con.commit()


class AddrsServer(Database):

    class AddrExistsError(Exception): 
        args = "This address already exists in database"
    
    class AddrNotFound(Exception):
        args = "This address not exists in database"
    






    



















