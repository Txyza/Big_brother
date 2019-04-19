import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.contrib.cache import SimpleCache
from server_routes import recogniser

def sql_execute(sql_give):
    conn = psycopg2.connect(dbname='bigbrother', user='test_user', password='qwerty', host='localhost')
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
    global cache_user
    if cache_user.get_dict() == {}:
        cache_user = sql_execute("SELECT * FROM users2")
    return cache_user


def add_user(user):
    # user.update({model: model.get_model(user.get(["photo"]))})
    encode = recogniser.make_string_of_encoding(recogniser.encode_image(user.get("photo")))
    user.update({"encoding":encode})
    sql = "INSERT INTO users2(name,surname,photo,status,encoding) VALUES ('{name}','{surname}','{photo}','unknown','{encoding}')".format(**user)
    sql_execute(sql)
    print(sql)


def update(id, status):
    sql = "UPDATE users2 SET status  = '{status}' WHERE id = {id} ;".format(status = status,id = id)


#add_user({'photo': 'urlll', 'name': "qwe", "surname": "rty"})
