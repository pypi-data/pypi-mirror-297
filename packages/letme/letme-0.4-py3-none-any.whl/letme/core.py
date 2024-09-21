from pyspark.sql import SparkSession
from delta import *
import getpass
import pandas as pd
import shutil

from .helpers import *
from .config import *
from .auth import *

from .sources.source import source

class spark(SparkSession):
    def __init__(self, spark_memory: str, spark_cpu_cores: str):
        self.spark_cpu_cores = spark_cpu_cores
        self.spark_memory = spark_memory
        self.spark_session = self.__create_spark_session()


    def __create_spark_session(self):
        builder = super().builder.master(f'local[{self.spark_cpu_cores}]') \
            .config('spark.driver.extraClassPath', jar_files) \
            .config('spark.executor.extraClassPath', jar_files) \
            .config('spark.sql.extensions', 'io.delta.sql.DeltaSparkSessionExtension') \
            .config('spark.sql.catalog.spark_catalog', 'org.apache.spark.sql.delta.catalog.DeltaCatalog') \
            .config('spark.sql.warehouse.dir', spark_warehouse) \
            .config('spark.driver.memory', self.spark_memory) \
            .config('spark.driver.maxResultSize', self.spark_memory) \
            .config('spark.sql.repl.eagerEval.enabled', True) \
            .config('spark.databricks.delta.schema.autoMerge.enabled', True) \
            .config('spark.databricks.delta.autoCompact.enabled', True)
        return builder.getOrCreate()

class app:
    def __init__(self, username: str, password: str = None, spark_memory: int = 2, spark_cpu_cores: int = 1):
        if spark_memory > spark_max_memory:
            self.spark_memory = spark_max_memory
        else:
            self.spark_memory = spark_memory

        if spark_cpu_cores > spark_max_cpu_cores:
            self.spark_cpu_cores = spark_max_cpu_cores
        else:
            self.spark_cpu_cores = spark_cpu_cores
        
        self.username = username
        if not password:
            self.password = getpass.getpass('Please enter your password: ')
        else:
            self.password = password

        self.auth = auth(self.username, self.password)
        if not self.auth.login():
            print('The username and/or password is incorrect. Please try again.')
            return None
        
        self.spark = spark(f'{self.spark_memory}g', f'{self.spark_cpu_cores}').spark_session


    def load(self):
        rows = self.auth.get_access_level()
        for row in rows:
            self.spark.sql(row[0])


    def add_source(self, source_name: str):
        return source(app=self ,source_name=source_name)
    

    def find_source(self, source_name: str):
        sql = f'''
            select source_name, source_type, source_object, created_date 
            from delta_sources ds
            inner join delta_users du on ds.user_id = du.id 
            where du.username = '{self.username}' and source_name like '%{source_name}%'
        '''
        df = pd.DataFrame(metastore_select(sql))
        if df.empty:
            return None
        return df

    
    def load_source(self, source_name: str):
        sql = f'''
            select source_name, source_type, source_object 
            from delta_sources ds
            inner join delta_users du on ds.user_id = du.id 
            where du.username = '{self.username}' and source_name = '{source_name}'
        '''
        try:
            row = metastore_select(sql)[0]
        except:
            print('Source not found!')
            return
        source_name = row[0]
        source_type = row[1]
        source_params = row[2]

        src = source(app=self, source_name=source_name)
        if source_type == 'mssql':
            return src.mssql(server=source_params.get('server'), database=source_params.get('database'), username=source_params.get('username'), password=source_params.get('password'), port=source_params.get('port'))


    def checks_report(self):
        sql = '''
            select
                runtime as run_date,
                "result" -> 'source_name' as source_name,
                "result" -> 'source_type' as source_type,
                "result" -> 'asset' as asset_query,
                "result" -> 'check_name' as check_name,
                "result" -> 'check_parameters' as check_parameters,
                "result" -> 'success_percentage' as success_percentage,
                "result" -> 'user' as username
            from delta_checks dc
        '''
        rows = metastore_select(sql)
        filtered = [row for row in rows if row[-1] == self.username]
        if len(filtered) > 0:
            return pd.DataFrame(filtered).drop('username', axis=1)
        return None


    def terminate(self):
        self.spark.stop()


    def list_access_level(self):
        sql = f'''select 
            name, 
            "type", 
            "location",
            case 
            	when dou.access_level = 'r' then 'Read'
            	when dou.access_level = 'w' then 'Write'
            	when dou.access_level = 'c' then 'Change'
            	when dou.access_level = 'rw' then 'Read - Write'
            	when dou.access_level = 'rc' then 'Read - Change'
            	when dou.access_level = 'wc' then 'Write - Change'
            	when dou.access_level = 'rwc' then 'Read - Write - Change'
                else 'No Permission'
            end as access_level
        from delta_objects dlo inner join delta_objects_users dou on dou.object_id = dlo.id
        inner join delta_users du on du.id = dou.user_id
        where du.username = '{self.username}'
        '''
        return pd.read_sql(sql, get_metastore_con())
    

    def set_access_level(self, username: str, object_name: str, access_level: str):
        current_user = self.username
        
        current_user_id = metastore_select(f''' select id from delta_users du where username = '{current_user}' ''')[0][0]
        object_id = metastore_select(f''' select id from delta_objects where name = '{object_name}' ''')[0][0]
        current_access_level = metastore_select(f''' select access_level from delta_objects_users where user_id = {current_user_id} and object_id = {object_id}''')[0][0]
    
        if 'c' not in current_access_level:
            print('''You don't have enough permission to give access of this object to the user.''')
            return
        
        user_id = metastore_select(f''' select id from delta_users du where username = '{username}' ''')[0][0]

        row = metastore_select(f''' select id from delta_objects_users where user_id = {user_id} and object_id = {object_id} ''')
        
        if not row:
            metastore_ciud(f''' insert into delta_objects_users (user_id, object_id, access_level) values ({user_id}, {object_id}, '{access_level}') ''')
        else:
            metastore_ciud(f''' update delta_objects_users set access_level = '{access_level}' where user_id = {user_id} and object_id = {object_id} ''')


    def create_db(self, db_name):
        sql = f'create database {db_name}'
        self.spark.sql(sql)
        metastore_save_object(sql, self.username)
    

    def create_view(self, view_script: str):
        self.spark.sql(view_script)
        metastore_save_object(view_script, self.username)
    

    def create_table(self, table_script: str, location: str):
        table_script = f'{table_script} using delta location {location}'
        self.spark.sql(table_script)
        metastore_save_object(table_script, self.username)