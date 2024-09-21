from .mssql import mssql

class source:
    def __init__(self, app, source_name: str):
        self.source_name = source_name
        self.app = app
        self.source_type = None
    
    def mssql(self ,server: str, database: str, username: str, password: str, port: int = 1433):
        self.source_type = 'mssql'
        return mssql(self.app ,self.source_name, server, database, username, password, port)