def planes_filter(planes_data: list) -> list[dict]:
    """Функция для фильтрации самолетов.
    Оставляем только те, где все значения заполнены.
    Удаляем пустые вложенные списки."""

    i = 0
    while i < len(planes_data):
        if len(planes_data[i]) < 1:
            del planes_data[i]
        else: i += 1

    for data in planes_data:
        i = 0
        while i < len(data):
            if None in data[i].values():
                del data[i]  # элемент удалён, индекс не увеличиваем
            elif '' in data[i]:
                del data[i]
            else:
                i += 1
    if len(planes_data) > 1:
        extended_list = []
        for item in planes_data:
            extended_list.extend(item)
        return extended_list
    else:
        return planes_data