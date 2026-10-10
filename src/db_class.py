import psycopg2

class DBManager:
    """Клвчч для работы с информацией из БД"""
    def __init__(self,db_name):
        self.connection = {
            'host': 'localhost',
            'database': db_name,
            'user': 'postgres',
            'password': 'i630842121'
        }

    # (
    #     host='localhost',
    # database=db_name,
    # user='postgres',
    # password='i630842121'
    # )

    def get_countries_and_aeroplanes_count(self):
        """Метод для получения списка всех стран с указанием кол-ва самолетов в низ"""
        try:
            with psycopg2.connect(**self.connection) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT countries.country, COUNT(planes.plane_id) AS planes FROM countries\n"
                                "JOIN planes ON countries.country = planes.country\n"
                                "GROUP BY countries.country")
                    for row in cur.fetchall():
                        print(row)
        except Exception as exc:
            print(exc)
        finally:
            #на всякий случай
            cur.close()
            conn.close()

    def get_all_aeroplanes(self):
        """Метод для получения списка со всеми самолетами из БД"""
        try:
            with psycopg2.connect(**self.connection) as conn:
                with conn.cursor() as cur:
                    cur.execute('SELECT * FROM planes')
                    return cur.fetchall()
        except Exception as exc:
            print(exc)
        finally:
            #на всякий случай
            cur.close()
            conn.close()

    def get_avg_speed(self):
        """Метод для получения средней скорости самолетов"""
        try:
            with psycopg2.connect(**self.connection) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT AVG(velocity) as AvgSpeed FROM planes")
                    return cur.fetchall()
        except Exception as exc:
            print(exc)
        finally:
            #на всякий случай
            cur.close()
            conn.close()

    def get_aeroplanes_with_higher_speed(self):
        """Метод для получения списка самолетов со скоростью выше средней"""
        try:
            with psycopg2.connect(**self.connection) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM planes\n"
                                "WHERE velocity > (SELECT AVG(velocity) FROM planes)")
                    return cur.fetchall()
        except Exception as exc:
            print(exc)
        finally:
            #на всякий случай
            cur.close()
            conn.close()
    def get_aeroplanes_with_keyword(self, string):
        """Метод для получения списка самолетов по ключевому слову в позывном"""
        try:
            with psycopg2.connect(**self.connection) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM planes\n"
                                f"WHERE callsign LIKE '%{string}%'")
                    print(cur.fetchall())
                    return cur.fetchall()
        except Exception as exc:
            print(exc)
        finally:
            #на всякий случай
            cur.close()
            conn.close()
