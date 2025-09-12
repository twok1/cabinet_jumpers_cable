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


from collections import defaultdict

def union_find(sets):
    parent = {}
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        parent[find(x)] = find(y)
    
    # Инициализация
    for s in sets:
        for item in s:
            if item not in parent:
                parent[item] = item
    
    # Объединение
    for s in sets:
        if len(s) > 0:
            first = next(iter(s))
            for item in s:
                union(first, item)
    
    # Группировка результатов
    groups = defaultdict(set)
    for item in parent:
        groups[find(item)].add(item)
    
    return list(groups.values())