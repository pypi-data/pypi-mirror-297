def load_mssql_query(source, query):
    sqlsUrl = f'jdbc:sqlserver://{source.server}:{source.port};database={source.database};trustServerCertificate=true'
    jdbc_options = {
                "url": sqlsUrl,
                "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver",
                "user": source.username,
                "password": source.password
    }
    qryStr = f'({query}) t'
    return source.app.spark.read.format('jdbc').option('dbtable', qryStr ).options(**jdbc_options).load()