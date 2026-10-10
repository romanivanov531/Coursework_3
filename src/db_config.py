import psycopg2


class DBConfig:
    """Класс для создания БД и таблиц planes и countries"""
    def __init__(self, db_name):
        self.db_name = db_name

    def create_db(self) -> None:
        """Метод для создания локальной БД"""
        try:
            conn = psycopg2.connect(
                dbname='postgres',
                user='postgres',
                password='i630842121',
                host='localhost',
                port='5432'
            )

            conn.autocommit = True
            cur = conn.cursor()
            create_db_query = f"CREATE DATABASE {self.db_name}"
            cur.execute(create_db_query)
            print(f"База данных '{self.db_name}' успешно создана")
        except Exception as e:
            print(e)
        finally:
            cur.close()
            conn.close()

    def db_connection(self):
        """Метод для соединения с БД"""
        conn = psycopg2.connect(
            host='localhost',
            database=self.db_name,
            user='postgres',
            password='i630842121'
        )
        if conn:
            print(f'Поключено к {self.db_name}')
        return conn

    def create_db_tables(self) -> None:
        """Метод для создания таблиц country и planes"""
        # создаем таблицу country
        try:
            with DBConfig.db_connection(self) as conn:
                with conn.cursor() as cur:
                    cur.execute('CREATE TABLE countries('
                                'country_id serial PRIMARY KEY,'
                                'country varchar(100) UNIQUE NOT NULL)'
                                )
                    conn.commit()
        except Exception as exc:
            print(f'Bad connection: {exc}')


        # создаем таблицу planes
        try:
            with DBConfig.db_connection(self) as conn:
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

    def insert_into_countries(self, countries: list) -> None:
        """Метод для добавления уникальных стран в БД, таблица country"""
        try:
            with DBConfig.db_connection(self) as conn:
                with conn.cursor() as cur:
                    i = 1
                    cur.execute(f"TRUNCATE TABLE countries RESTART IDENTITY CASCADE")
                    conn.commit()
                    for country in countries:
                        try:
                            cur.execute(f"INSERT INTO countries VALUES ({i}, '{country}') ON CONFLICT (country) DO NOTHING")
                            conn.commit()
                            i += 1
                        except Exception as exc:
                            print(exc)
            print('Данные внесены. Таблица "country"')
        except Exception as exc:
            print(exc)

    def insert_into_planes(self, planes_data: list) -> None:
        """Метод для добавления самолетов в БД, в таблицу planes"""
        try:
            with DBConfig.db_connection(self) as conn:
                with conn.cursor() as cur:
                    cur.execute(f"TRUNCATE TABLE planes RESTART IDENTITY CASCADE")
                    for plane in planes_data:
                        cur.execute(
                            f"INSERT INTO planes(plane_id, callsign, country, velocity, altitude)\n"
                            f"VALUES ('{plane['unique_id']}', '{plane['callsign']}', '{plane['registration']}','{plane['velocity']}', '{plane['geo_altitude']}')")
                        conn.commit()
            print('Данные внесены в таблицу "planes"')
        except Exception as exc:
            print(exc)
