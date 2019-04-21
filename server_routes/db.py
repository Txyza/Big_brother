import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.contrib.cache import SimpleCache
from server_routes import recogniser
from server_routes import server
from base64 import b64encode
from datetime import datetime

def sql_execute(sql_give):
    conn = psycopg2.connect(dbname='postgres', user='postgres', password='postgres', host='localhost')
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    answer = None

    # print(sql_give)
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


def get_info(status):
    return sql_execute("""
    select name, surname, status
    from users2
    where status = '{status}'
    """.format(status=status))


def get_users():

    return sql_execute("""
    SELECT * 
      , (select date from history h where h.id = u.id order by date desc limit 1) as date
    FROM users2 u
    order by id
    """)


def get_user(id):

    return sql_execute("""
with hist as (
  select id, array_agg(array[date::text, status::text]) dates
  from (
    select id, date, status
    from history
    where id = {id}
    order by date
    limit 5
  ) n
  group by id
)
    SELECT id, name, photo, surname, name, status
      , (select dates from hist) as date
    FROM users2 u
    where id={id}
    order by id
    """.format(id=id))


def get_find_users(name, surname):

    return sql_execute("""
    SELECT distinct * 
      , (select date from history h where h.id = u.id order by date desc limit 1) as date
    FROM users2 u
    where
      name like '{name}' || '%'
      or name like '{surname}' || '%'
      or surname like '{name}' || '%'
      or surname like '{surname}' || '%'
      or status like '{name}' || '%'
      or status like '{surname}' || '%'
    order by id
    """.format(name=name, surname=surname))

def add_user(user):
    encode = recogniser.encode_image(user.get('photo'))
    user.get('photo').seek(0)
    user['photo'] = b64encode(user.get('photo').read()).decode()
    user.update({"encoding": encode})

    sql = """
    INSERT INTO users2(name,surname,photo,status,encoding) 
    VALUES ('{name}','{surname}','{photo}','Unknown','{encoding}')""".format(**user)
    sql_execute(sql)
    print(sql)



def add_history(id,status):
    sql = '''
        select status
        from history t
        where id = '{id}'
        order by date desc
        limit 1
    '''.format(id=id)
    # print(sql_execute(sql))
    status_old = sql_execute(sql)
    print(id, status, status_old)
    if status != 'None':
        if not status_old or (status and status != status_old[0].get('status')):
            sql = """INSERT INTO history(id,status,date)
                     VALUES ('{id}','{status}','{date}')""".format(id = id,status = status,date = str(datetime.now()))
            # print(sql)
            sql_execute(sql)


def update(id, status):
    add_history(id,status)
    sql = "UPDATE users2 SET status  = '{status}' WHERE id = {id} ;".format(status=status, id=id)
    sql_execute(sql)
