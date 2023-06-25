import psycopg2
conn = psycopg2.connect(
    user = 'postgres',
    password='In12ter!',
    host='127.0.0.1',
    port='53354',
    database='vkbot'
)
c = conn.cursor()

def init_db():
    c.execute()
