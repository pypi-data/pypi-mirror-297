from datetime import datetime
from ..helpers import save_checks

# expect column value to not be null
def expect_column_value_to_not_be_null(asset, column_name):
    data = asset.data
    data.createOrReplaceTempView('tmp')
    total = asset.source.app.spark.sql('select * from tmp')
    failed = asset.source.app.spark.sql(f'''select * from tmp where {column_name} is null ''')
    total_count = total.count()
    failed_count = failed.count()
    asset.source.app.spark.sql('drop table tmp')
    output = {
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'source_name': asset.source.source_name,
            'source_type': asset.source.source_type,
            'user':  asset.source.app.username,
            'asset': asset.query,
            'check_name': 'expect_column_value_to_be_not_null',
            'check_parameters': {'column_name':f'{column_name}'},
            'total_count': total_count,
            'failed_count': failed_count,
            'success_percentage': ( (total_count-failed_count) / total_count) * 100
            }
    save_checks(output)
    return output

# expect the data asset has specific conditions. usually will be used for complex conditions.
def expect_columns_have_conditions(asset, conditions: str):
    data = asset.data
    data.createOrReplaceTempView('tmp')
    total = asset.source.app.spark.sql('select * from tmp')
    failed = asset.source.app.spark.sql(f'''select * from tmp where not ({conditions}) ''')
    total_count = total.count()
    failed_count = failed.count()
    asset.source.app.spark.sql('drop table tmp')
    output = {
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'source_name': asset.source.source_name,
            'source_type': asset.source.source_type,
            'user':  asset.source.app.username,
            'asset': asset.query,
            'check_name': 'expect_columns_have_conditions',
            'check_parameters': {'conditions': f'{conditions}'},
            'total_count': total_count,
            'failed_count': failed_count,
            'success_percentage': ( (total_count-failed_count) / total_count) * 100
            }
    save_checks(output)
    return output

# expect max column to be between a lower bound and upper bound
def expect_column_max_to_be_between(asset, column_name: str, lower_bound, upper_bound):
    data = asset.data
    data.createOrReplaceTempView('tmp')
    max_column = asset.source.app.spark.sql(f'select max({column_name}) from tmp').collect()[0][0]
    asset.source.app.spark.sql('drop table tmp')
    success_percentage = 100 if lower_bound < max_column < upper_bound else 0
    output = {
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'source_name': asset.source.source_name,
            'source_type': asset.source.source_type,
            'user':  asset.source.app.username,
            'asset': asset.query,
            'check_name': 'expect_column_max_to_be_between',
            'check_parameters': {'column_name': f'{column_name}', 'lower_bound': lower_bound, 'upper_bound': upper_bound},
            'success_percentage': success_percentage
            }
    save_checks(output)
    return output
