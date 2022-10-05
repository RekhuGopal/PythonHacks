import psycopg2

conn = psycopg2.connect(database="db_name",
                        host="db_host",
                        user="db_user",
                        password="db_pass",
                        port="db_port")

cursor = conn.cursor()

cursor.execute("SELECT * FROM example_table")

print(cursor.fetchone())

print(cursor.fetchall())

print(cursor.fetchmany(size=5))