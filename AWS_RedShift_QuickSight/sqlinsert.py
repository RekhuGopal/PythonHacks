import psycopg2

# Connect to the database
conn = psycopg2.connect("dbname=test user=postgres password=secret")
cursor = conn.cursor()

# Insert values dynamically
cursor.execute('''
    INSERT INTO demo (faceId, email, name, phone, title, amount)
    VALUES (%s, %s, %s, %s, %s, %s)
''', ('face123', 'example@example.com', 'John Doe', '1234567890', 'Manager', 1000))

# Commit and close
conn.commit()
conn.close()
