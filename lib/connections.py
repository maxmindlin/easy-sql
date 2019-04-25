from __future__ import annotations
import mysql.connector as connector
import platform
import os
import subprocess
import pandas as pd
from typing import Optional
from dotenv import load_dotenv
from typing import Union

class MySQLBase:

    def __init__(self, user: str, passwd: str, host: str, port: Union[str, int], db_name: str, tunnel: Optional[str] = None) -> MySQLBase:
        
        self._host = host
        self._user = user
        self._passwd = passwd
        self._dbname = db_name
        self._con = None

        if type(port) == str:
            port = int(port)
        self._port = port
        
        if tunnel:
            self._open_tunnel(tunnel)

    @staticmethod
    def _open_tunnel(tunnel_cmd) -> None:
        """Open an ssh tunnel connection.
        
        Should only open if one is not already open."""

        # The following doesnt appear to work on ubuntu
        if not 'ubuntu' in platform.platform().lower():
            FNULL = open(os.devnull, 'w')
            s = subprocess.call('lsof -ti:3306',shell=True,stdout=FNULL,stderr=subprocess.STDOUT)
            # Only if the tunnel isnt already open, attempt to open a new one.
            if s == 1:
                os.system(tunnel_cmd)
    
    def _connect(self) -> None:
        
        # Handle case where theres already a connection established
        if self._con != None:
            # Probably not the best thing to do
            return
        
        try:
            self._con = connector.connect(
                host = self._host,
                port = self._port,
                user = self._user,
                passwd = self._passwd,
                db = self._dbname
            )
        except:
            self._con = None
    
    def _disconnect(self) -> None:

        self._con.close()

    def new(self) -> MySQLBase:
        # This is allowed to exist to create a new connection client,
        # but class extensions should ensure that connection is always closed.
        # This does not do that.

        self._connect()
        return self
    
    def data_frame_query(self, query: str) -> pd.DataFrame:

        return pd.read_sql(query, self._con)

    @property
    def client(self):
        return self._con
    

class EasySQLConnector(MySQLBase):

    def __init__(self, env_path: str, tunnel: bool = False) -> EasySQLConnector:
        creds = list(self.extract_env_creds(env_path, tunnel).values())
        super().__init__(*creds)

    def extract_env_creds(self, env_path: str, needs_tunnel: bool = False) -> dict:
        """Reads in a .env file and converts it to a dict of creds."""

        load_dotenv(env_path)
        keys = ["DB_USER", "DB_PASS", "DB_HOST", "DB_PORT", "DB_NAME"]

        if needs_tunnel:
            keys.append("DB_TUNNEL")

        return {k:os.getenv(k) for k in keys}

