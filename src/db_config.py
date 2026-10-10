from csv import excel

import psycopg2

from src.class_api import BasicAPI
from src.db_class import DBManager

class DBSettings:
    """Класс для создания ДБ"""

def create_db(db_name: str) -> None:
    """Функция для создания локальной БД"""
    try:
        conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='i630842121',
            host='localhost',
            port='5432'
        )
    except Exception as exc:
        print(f'Bad connection: {exc}')
    try:
        conn.autocommit = True
        cursor = conn.cursor()
        create_db_query = f"CREATE DATABASE {db_name}"
        cursor.execute(create_db_query)
        print(f"База данных {db_name} успешно создана")
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


def db_connection(db_name: str):
    """Функция для соединения с БД"""
    conn = psycopg2.connect(
            host='localhost',
            database=db_name,
            user='postgres',
            password='i630842121'
        )
    return conn

def create_db_tables(db_name: str) -> None:
    """Функция для создания таблиц country и planes"""
    #создаем таблицу country
    try:
        with db_connection(db_name) as conn:
            with conn.cursor() as cur:
                cur.execute('CREATE TABLE countries('
                            'country_id serial PRIMARY KEY,'
                            'country varchar(100) UNIQUE NOT NULL)'
                            )
                conn.commit()
    except Exception as exc:
        print(f'Bad connection: {exc}')
    finally:
        conn.close()

    #создаем таблицу planes
    try:
        with db_connection(db_name) as conn:
            with conn.cursor() as cur:
                cur.execute('CREATE TABLE planes('
                            'plane_id varchar(25) PRIMARY KEY,'
                            'callsign varchar(25) UNIQUE NOT NULL,'
                            'country varchar(50) NOT NULL,'
                            'velocity FLOAT NOT NULL,'
                            'altitude FLOAT NOT NULL)'
                            )
                conn.commit()
    except Exception as exc:
        print(f'Bad connection: {exc}')
    finally:
        conn.close()


def insert_into_countries(planes_info: list, db_name: str) -> None:
    """ Функция для добавления уникальных стран в БД, таблица country"""
    try:
        conn = db_connection(db_name)
        with conn.cursor() as cur:
            i = 1
            cur.execute(f"TRUNCATE TABLE countries RESTART IDENTITY CASCADE")
            for plane in planes_info:
                try:
                    cur.execute(f"INSERT INTO countries VALUES ({i}, '{plane}') ON CONFLICT (country) DO NOTHING")
                    conn.commit()
                    i += 1
                    print(type(plane))
                except Exception as exc:
                    print(exc)
    except Exception as exc:
        print(exc)
    finally:
        #на всякий случай
        cur.close()
        conn.close()


def insert_into_planes(planes_data: list, db_name: str) -> None:
    """Функция для добавления самолетов в БД, в таблицу planes"""
    try:
        with db_connection(db_name) as conn:
            with conn.cursor() as cur:
                for plane in planes_data:
                    cur.execute(f"TRUNCATE TABLE planes RESTART IDENTITY CASCADE")
                    cur.execute(
                                f"INSERT INTO planes(plane_id, callsign, country, velocity, altitude)\n"
                                f"VALUES ('{plane['unique_id']}', '{plane['callsign']}', '{plane['registration']}','{plane['velocity']}', '{plane['geo_altitude']}')")
                    conn.commit()
    except Exception as exc:
        print(exc)
    finally:
        #на всякий случай
        cur.close()
        conn.close()


def planes_filter(planes_data):
    """Функция для фильтрации самолетов.
    Оставляем только те, где все значения заполнены."""
    i = 0
    while i < len(planes_data):
        if None in planes_data[i].values():
            del planes_data[i]  # элемент удалён, индекс не увеличиваем
        else:
            i += 1
    i = 0
    while i < len(planes_data):
        if '' in planes_data[i].values():
            del planes_data[i]  # элемент удалён, индекс не увеличиваем
        else:
            i += 1
    return planes_data

if __name__ == '__main__':
    # api = BasicAPI()
    # coor = api.get_coordinates('japan')
    # planes = api.get_aeroplanes(coor)
    #
    # #Список стран с повторами
    # planes_list = []
    # for plane in planes:
    #     planes_list.append(plane['registration'])
    # #оставляем только те салеты, где нет незаполненных значений в ключах
    # filter = planes_filter(planes)
    # #выделяем список уникальных стран
    # unique_countries = sorted(list(set(planes_list)))
    # print(unique_countries)
    #
    # create_db('kaka')
    # create_db_tables('kaka')
    #
    # insert_into_planes(filter, 'kaka')
    #
    # insert_into_countries(unique_countries, 'kaka')
    # manager = DBManager('kaka')
    # manager.get_countries_and_aeroplanes_count()
    # manager.get_all_aeroplanes()
    # manager.get_aeroplanes_with_higher_speed()
    # manager.get_aeroplanes_with_keyword('NA')
