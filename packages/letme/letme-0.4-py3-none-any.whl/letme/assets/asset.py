import math
from tqdm import tqdm

from .load import *
from ..expect.basics import *
from ..helpers import metastore_save_object, get_absolute_path

class asset:
    def __init__(self, source ,query):
        self.query = query
        self.source = source
        self.__load_data()
        self.location = None
    
    def __load_data(self):
        if self.source.source_type == 'mssql':
            self.data = load_mssql_query(source=self.source, query=self.query)


    def write_to_delta_table(self, table_fullname: str, location: str, chunk_size: int = 10000):
        if not self.data:
            return 'No data.'

        self.location = location

        # create delta table
        script = f'create table if not exists {table_fullname} ( '
        for row in self.data.dtypes:
            script += f'{row[0]} {row[1]},'
        script = script[0: len(script)-1]
        script += f''') using delta location '{get_absolute_path(location)}' '''
        self.source.app.spark.sql(script)

        # save script to the metastore
        metastore_save_object(script, self.source.app.username)

        # write data into delta table
        self.data.createOrReplaceTempView('tmp_tbl')
        if chunk_size == 0:
            self.source.app.spark.sql(f'''
                insert into {table_fullname}
                select * from tmp_tbl
            ''')
        else:
            iter = 0
            cnt = self.data.count()
            total = math.ceil(cnt / chunk_size)
    
            with tqdm(total = total) as pbar:
                while iter < total:
                    self.source.app.spark.sql(f'''
                                insert into {table_fullname}
                                select * from tmp_tbl limit {chunk_size} offset {iter*chunk_size}
                            ''')
                    iter += 1
                    pbar.update(1)
        self.source.app.spark.sql('drop table tmp_tbl')

    def __str__(self):
        pass

    # expectations
    def expect_column_value_to_not_be_null(self, column_name: str):
        return expect_column_value_to_not_be_null(self, column_name)
    
    def expect_columns_have_conditions(self, conditions: str):
        return expect_columns_have_conditions(self, conditions)

    def expect_column_max_to_be_between(self, column_name: str, lower_bound, upper_bound):
        return expect_column_max_to_be_between(self, column_name, lower_bound, upper_bound)