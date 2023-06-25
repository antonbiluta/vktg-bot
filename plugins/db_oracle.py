import cx_Oracle
cx_Oracledsn = cx_Oracle.makedsn(
    'localhost',
    '1521',
    service_name = 'orcl'
)

conn = cx_Oracle.connect(
    user = 'hr',
    password ='hr',
    dsn=dsn
)c = conn.cursor()