from src.class_api import BasicAPI
from src.db_class import DBManager
from src.db_config import DBConfig
from utils.planes_filter import planes_filter

if __name__ == '__main__':
    countries = input('Введите страны для отслеживания\n'
                      'Например: Canada, Japan, India, Italy\n')
    db_name = input('Назовите базу данных\n')

    county_list = countries.split(', ')
    api = BasicAPI()
    planes_list = []
    coordinates = []
    countries = []
    #уникальные страны для добавления в БД countries
    unique_countries = sorted(list(set(countries)))

    for country in county_list:
        coordinates.append(api.get_coordinates(country))
    for coor in coordinates:
        planes_list.append(api.get_aeroplanes(coor))
    for country in planes_list:
        if len(country) < 1:
            continue
        else:
            for item in country:
                countries.append(item['registration'])
    filtered_planes = planes_filter(planes_list)
    # print(len(filtered_planes))

    db = DBConfig(db_name)
    db.create_db()
    db.create_db_tables()
    db.insert_into_countries(countries)
    db.insert_into_planes(filtered_planes)
    db_manager = DBManager(db_name)
    db_manager.get_countries_and_aeroplanes_count()
    db_manager.get_aeroplanes_with_higher_speed()
    db_manager.get_all_aeroplanes()
    db_manager.get_avg_speed()
    db_manager.get_aeroplanes_with_keyword('SM')