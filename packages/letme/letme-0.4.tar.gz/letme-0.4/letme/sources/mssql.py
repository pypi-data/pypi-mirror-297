from ..assets.asset import asset
from ..helpers import metastore_select, get_metastore_con
import json
from sqlalchemy import text
from datetime import datetime

class mssql:
    def __init__(self, app ,source_name: str ,server: str, database: str, username: str, password: str, port: int = 1433):
        self.app = app
        self.source_name = source_name
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.port = port
        self.source_type = 'mssql'
    
    def asset(self, query: str):
        return asset(self, query)

    def __str__(self):
        return {
            'source_name': self.source_name,
            'source_type': self.source_type,
            'server': self.server,
            'database': self.database,
            'username': self.username,
            'password': self.password,
            'port': self.port
        }

    def save(self):
        user_id = metastore_select(f'''select id from delta_users where username = '{self.app.username}' ''')[0][0]
        result = json.dumps(self.__str__())

        engine = get_metastore_con()
        sql = text('insert into delta_sources (user_id, source_type, source_name, source_object, created_date) values (:user_id, :source_type, :source_name, :source_object, :created_date)')
        parameters = {"user_id": user_id, "source_type": self.source_type, "source_name": self.source_name, "source_object": result, "created_date": datetime.now()}
        with engine.connect() as conn:
            conn.execute(sql, parameters)
        