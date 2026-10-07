from abc import ABC, abstractmethod

import requests


class Api(ABC):
    """Абстрактный класс для основного класса для работы с API"""
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_coordinates(self, country: str):
        pass

    @abstractmethod
    def get_aeroplanes(self, coordinates: list):
        pass


class BasicAPI(Api):
    """Базовый класс для работы с API"""
    def __init__(self):
        self.opensky_url = 'https://opensky-network.org/api/states/all?'
        self.openstreetmap_url = 'https://nominatim.openstreetmap.org/search'

    def get_coordinates(self, country: str):
        """Метод для получения крайних координат выбранной страны.
        Возвращает список координат в формате:[Южная широта, Северная широта, Западная долгота, Восточная долгота]"""
        headers = {
            'User-Agent' : 'test_app'
        }
        params = {
            'country' : country,
            'format' : 'json',
            'limit' : 1
        }
        response = requests.get(self.openstreetmap_url, headers=headers, params=params)
        data = response.json()
        coordinates = data[0]['boundingbox']
        return coordinates

    def get_aeroplanes(self, coordinates: list):
        """Метод для получения информации о полетах в заданных координатах.
        Возвращает словарь в формате json"""
        params = {
            'lamin': coordinates[0],
            'lomin': coordinates[1],
            'lamax': coordinates[2],
            'lomax': coordinates[3]
        }

        response = requests.get(url=self.opensky_url, params=params)
        data = response.json()
        planes_list = []
        for plan in data['states']:
            plane_dict = ({
                'unique_id' : plan[0],
                'registration' : plan[2],
                'callsign' : plan[1],
                'velocity' : plan[9],
                'geo_altitude' : plan[13],
                'on_ground' : plan[8]
            })
            planes_list.append(plane_dict)
        return planes_list
