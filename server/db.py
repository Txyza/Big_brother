import psycopg2
conn = psycopg2.connect(dbname='bigbrother', user='test_user', 
                        password='qwerty', host='localhost')
cursor = conn.cursor(cursor_factory=RealDictCursor)

# https://khashtamov.com/ru/postgresql-python-psycopg2/

cursor.execute("SELECT * FROM user2")
for line in cursor:
	print(line)
cursor.close()
conn.close()