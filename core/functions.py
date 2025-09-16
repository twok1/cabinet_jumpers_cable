from collections import defaultdict


def sorting_key(item: set):
    """
    Кастомный ключ сортировки для элементов вида XT...
    Возвращает кортеж: (приоритет группы, число, исходная строка)
    """
    item = ''.join(item)
    # Определяем приоритет группы
    if item.startswith('XTK'):
        group_priority = 0  # Первая группа: XTK
    elif item.startswith('XT') and not item.startswith('XTN'):
        group_priority = 1  # Вторая группа: XT (но не XTN)
    elif item.startswith('XTN'):
        group_priority = 2  # Третья группа: XTN
    else:
        group_priority = 3  # Все остальное
    
    # Извлекаем число из строки
    import re
    numbers = re.findall(r'\d+', item)
    number_one = int(numbers[0]) if numbers and len(numbers) >= 1 else 0
    number_two = int(numbers[1]) if numbers and len(numbers) >= 2 else 0
    
    return (group_priority, number_one, number_two, item)
