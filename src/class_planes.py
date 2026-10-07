import json


class Planes:
    """Класс для работы с самолетами"""
    registration: str   # Страна регистрации ВС
    unique_id: str   # уникальный идентификатор борта
    callsign: str   # позывной рейса
    velocity: str  # горизонтальная скорость (м/с)
    geo_altitude: str  # геометрическая высота (м)
    on_grond: str  # находится ли самолёт на земле
    planes_list11 = []

    def __init__(self, data: dict):
        if isinstance(data, dict):
            self.unique_id = data['unique_id']
            self.registration = data['registration']
            self.callsign = data['callsign']
            self.velocity = data['velocity']
            self.geo_altitude = data['geo_altitude'] if data['geo_altitude'] else 0
            self.on_ground = data['on_ground']
            Planes.planes_list11.append(self)
        else:
            raise TypeError('Неверный тип данных. Ожидается тип данных Dict\n')

    def __str__(self):
        return (f'{"=" * 10}\n'
                f'Уникальный ID: {self.unique_id}\n'
                f'Страна регистрации: {self.registration}\n'
                f'Позывной рейса: {self.callsign}\n'
                f'Скорость: {self.velocity}\n'
                f'Высота: {self.geo_altitude}')

    @classmethod
    def compare_planes_by_velocity(cls, user_range: int):
        if user_range > len(cls.planes_list11):
            print(f'Недостаточно самолетов для вашего топ {user_range}\n'
                  f'Вот топ {len(cls.planes_list11)}')
        rating = sorted(cls.planes_list11, key=lambda x: x.velocity, reverse=True)
        return rating

    @classmethod
    def compare_planes_by_geo_altitude(cls, user_range, country=None) -> list:
        if country:
            filtered_planes = []
            for plane in Planes.planes_list11:
                if country.lower() == plane.registration.lower():
                    filtered_planes.append(plane)
            if user_range > len(cls.planes_list11):
                print(f'Недостаточно самолетов для вашего топ {user_range}\n'
                      f'Вот топ {len(cls.planes_list11)}')
            rating = sorted(filtered_planes, key=lambda x: x.geo_altitude, reverse=True)
            return rating[0: user_range]
        else:
            if user_range > len(cls.planes_list11):
                print(f'Недостаточно самолетов для вашего топ {user_range}\n'
                      f'Вот топ {len(cls.planes_list11)}')
            rating = sorted(cls.planes_list11, key=lambda x: x.geo_altitude, reverse=True)
            return rating[0: user_range]

    def make_json_dict(self):
        json_dict = {
            "Уникальный ID": str(self.unique_id),
            "Страна регистрации": str(self.registration),
            "Позывной рейса": str(self.callsign),
            "Скорость": str(self.velocity),
            "Высота": str(self.geo_altitude)
        }
        json_string = json.dumps(json_dict)
        return json_string
