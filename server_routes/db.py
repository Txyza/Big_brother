import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.contrib.cache import SimpleCache
from server_routes import recogniser
from server_routes import server
from base64 import b64encode


def sql_execute(sql_give):
    conn = psycopg2.connect(dbname='postgres', user='postgres', password='postgres', host='localhost')
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    answer = None

    print(sql_give)
    cursor.execute(sql_give)
    conn.commit()
    try:
        answer = cursor.fetchall()
    except:
        pass
    finally:
        conn.close()
        cursor.close()
        return answer


# https://khashtamov.com/ru/postgresql-python-psycopg2/
cache_user = SimpleCache()


def get_users():

    return sql_execute("SELECT * FROM users2")

def cleaning(user):
    id = server.findFace(user.get("photo"), "@cleaning")
    while id is not None:
        sql = """DELETE FROM postgres WHERE id = '{id}'""".format(id)
        id = server.findFace(user.get("photo"),"@cleaning")
    

def add_user(user):
    encode = recogniser.encode_image(user.get('photo'))
    user.get('photo').seek(0)
    user['photo'] = b64encode(user.get('photo').read()).decode()
    user.update({"encoding": encode})
    if user.get("name") != "Unknown":
        cleaning(user)
        sql = """
           INSERT INTO users2(name,surname,photo,status,encoding) 
           VALUES ('{name}','{surname}','{photo}','unknown','{encoding}')""".format(**user)
    else:
        sql = """
        INSERT INTO users2(name,surname,photo,status,encoding) 
        VALUES ('{name}','{surname}','{photo}','{status}','{encoding}')""".format(**user)
    sql_execute(sql)
    print(sql)


def update(id, status):
    sql = "UPDATE users2 SET status  = '{status}' WHERE id = {id} ;".format(status=status, id=id)
    sql_execute(sql)
