from pathlib import Path
from sqlalchemy import create_engine, text
import json
from datetime import datetime

from .config import *

def get_metastore_con():
    connection_string = f'postgresql://{pg_username}:{pg_password}@{pg_server}:{pg_port}/{pg_database}'
    return create_engine(connection_string, isolation_level='autocommit')


def metastore_ciud(script: str):
    engine = get_metastore_con()
    with engine.connect() as conn:
        conn.execute(text(script))


def metastore_select(script: str):
    engine = get_metastore_con()
    with engine.connect() as conn:
        return conn.execute(text(script)).fetchall()


def normalize_script(script: str):
    script = script.replace('\n', ' ').strip().replace(';', '').replace('"', "'")
    new_words = [word.strip() for word in script.split(' ') if len(word.strip()) != 0]
    script = ' '.join(new_words)
    return f'{script} ;'


def get_absolute_path(system_path: str):
    return Path(system_path).resolve().__str__()



def initdb():
    metastore_ciud('''
        create table if not exists delta_objects 
            ( 
                id serial primary key, 
                script text, 
                type text, 
                name text, 
                location text, 
                username text, 
                last_modified_date timestamp 
            )
    ''')
    metastore_ciud('create unique index if not exists delta_objects_unique_name on delta_objects (name)')
    metastore_ciud('create unique index if not exists delta_objects_unique_location on delta_objects (location) where length(location) > 0')
    metastore_ciud('''
        create table if not exists delta_users 
            (
                id serial primary key, 
                username varchar(500), 
                password varchar(500) 
            )
    ''')
    metastore_ciud('create unique index if not exists delta_users_unique_username on delta_users (username)')
    metastore_ciud('''insert into delta_users (username, "password") values ('admin', 'admin1234')''')
    metastore_ciud('''insert into delta_users (username, "password") values ('test', 'test1234')''')
    metastore_ciud('''
        create table if not exists delta_objects_users 
            ( 
                id serial primary key, 
                user_id int, 
                object_id int, 
                access_level varchar(3) 
            )
    ''')
    metastore_ciud('''
        create table if not exists delta_sources 
            ( 
                id serial4 NOT NULL, 
                user_id int,
                source_type varchar(128),
                source_name varchar(128),
                source_object json, 
                created_date timestamp
            )
    ''')
    metastore_ciud('create unique index if not exists delta_source_unique on delta_sources (source_name)')
    metastore_ciud('''
        create table if not exists delta_checks 
            (
                id serial4 not null, 
                result json, 
                runtime timestamp
            )
    ''')


def extract_info_from_ddl_script(script: str):
    script = normalize_script(script)
    if ' using delta location ' in script.lower():
        start = script.lower().find(' using delta location ') + 21
        end = len(script.lower())
        table_location = script[start:end].replace(';', '').strip().replace("'", "")
        table_location = get_absolute_path(table_location)
        if ' if not exists ' in script.lower():
            start = script.lower().find(' if not exists ') + 14
        else:
            start = script.lower().find(' table ') + 6
        end = script.find('(')
        table_name = script[start:end].strip()
        return ['table' ,table_name, table_location]
        
    elif ' view ' in script.lower():
        if ' if not exists ' in script.lower():
            start = script.lower().find(' if not exists ') + 14
        else:
            start = script.lower().find(' view ') + 5
        end = script.lower().find('as')    
        view_name = script[start:end].strip()
        return ['view', view_name, '']
    
    elif ' database ' in script.lower():
        db_name = script.replace(';', '').strip().split(' ')[-1]
        return ['database', db_name, '']


def metastore_save_object(script, username: str):
    script = normalize_script(script)
    info = extract_info_from_ddl_script(script)
    object_type = info[0]
    object_name = info[1]
    object_location = info[2]
    last_modified_date = datetime.now()

    engine = get_metastore_con()
    with engine.connect() as conn:
        data = [{'script': str(script), 'type': str(object_type), 'name': object_name, 'loc': object_location, 'username': username, 'dt': str(last_modified_date)}]
        sql = '''
            insert into public.delta_objects (script, type, name, location, username, last_modified_date)
            values (:script, :type, :name, :loc, :username, :dt) returning id
            '''
        result = conn.execute(text(sql), data)
    object_id = result.fetchone()[0]

    result = metastore_select(f''' select id from delta_users where username = '{username}' ''')
    user_id = result[0][0]
    access_level = 'rwc'

    sql = f''' insert into delta_objects_users (user_id, object_id, access_level) values ({user_id}, {object_id}, '{access_level}') '''
    metastore_ciud(sql)


def save_checks(summary):
    engine = get_metastore_con()
    result = json.dumps(summary)
    sql = text('insert into delta_checks (result, runtime) values (:result, :runtime)')
    params = {"result": result, "runtime": datetime.now()}
    with engine.connect() as conn:
        conn.execute(sql, params)