def planes_filter(planes_data: list) -> list[dict]:
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
