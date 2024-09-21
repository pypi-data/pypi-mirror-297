from .helpers import metastore_select

class auth:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def login(self):
        sql = f'''
                select
                    * 
                from delta_users 
                where username = '{self.username}' and password = '{self.password}' 
        '''
        rows = metastore_select(sql)
        if not rows:
            return False
        return True


    def get_access_level(self):
        sql = f'''
                select
                     dlo.script as script, 
                     dlo."name" as name,
                     case when dlo."type" = 'database' then 'rwc' else dlou.access_level end as access_level
                from delta_objects_users dlou
                inner join delta_objects dlo on dlou.object_id = dlo.id
                inner join delta_users du on du.id = dlou.user_id
                where du.username = '{self.username}'
                order by dlo.last_modified_date asc
            '''
        return metastore_select(sql)