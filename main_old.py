from collections import defaultdict
import time

RUS_LETTERS = (
    'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 
    'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 
    'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я',
    'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й',
    'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф',
    'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я'
)

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

def main():
    # Инициализируем словарь для хранения данных
    result = {}
    original_file = {}
    num_line = 0
    num_file = 0
    
    # Открываем файл для чтения с правильной кодировкой
    with open('./data/data.txt', encoding='utf-8') as f:
        # Читаем все строки файла
        for line in f.readlines():
            if 'Откуда' in line:
                num_line = 0
                num_file += 1
            num_line += 1
            line = line.strip()
            # Пропускаем строки с заголовком 'Откуда'
            if 'Откуда' not in line and line:
                # Разбиваем строку на две части (предполагается формат "откуда куда")
                cabinet, signal, fr, to = line.split('\t')
                original_file[cabinet] = original_file.get(cabinet, {})
                for klemm in (fr, to):
                    original_file[cabinet][klemm] = original_file[cabinet].get(klemm, []) + [f'{num_file}_{num_line}']
                # Добавляем множество {откуда, куда} в data
                result[cabinet] = result.get(cabinet, []) + [{fr, to}]
    
    # Объединяем связанные множества (нахождение компонент связности графа)
    for cabinet in result:
        data = result[cabinet]
        a = 0 # Индекс текущего множества
        while a < len(data):
            b = a + 1  # Индекс следующего множества для сравнения
            
            while b < len(data):
                # Проверяем есть ли общие элементы между множествами data[a] и data[b]
                if data[a] & data[b]:
                    # Если есть общие элементы - объединяем множества
                    data[a] |= data.pop(b)  # Объединяем и удаляем второе множество
                    a -= 1  # Возвращаемся к предыдущему индексу для повторной проверки
                    break   # Прерываем внутренний цикл, т.к. массив изменился
                else:
                    b += 1  # Переходим к следующему множеству
            
            a += 1  # Переходим к следующему множеству
    
    
    for cabinet in result:
        data = result[cabinet]
        i = 0
        while i < len(data):
            data[i] = sorted(data[i], key=sorting_key)
            i += 1
        result[cabinet] = sorted(data, key=sorting_key)
    
    # for cabinet in result:
    #     data = result[cabinet]
    #     # Преобразуем множества в отсортированные списки
    #     result = [list(i) for i in data]
    
    # Выводим результат: сначала сортируем списки, затем каждый список выводим через табуляцию
    with open('./output/result.txt', 'w', encoding='utf-8') as f:
        max_count_xt = 0
        for cabinet in result:
            this_cab_xt_count = 0
            print(cabinet)
            f.write(f'{cabinet}\n')
            for i in result[cabinet]:
                this_cab_xt_count += len(i)
                write_line = "\t".join(i)
                jumpers_line = "\t".join(tuple(', '.join((s for s in k)) for k in tuple(original_file[cabinet][klemm] for klemm in i)))
                for letter in RUS_LETTERS:
                    if letter in write_line:
                        print(f'нашел русскую букву "{letter}"')
                        time.sleep(3)
                print(*i, sep='\t')
                print(jumpers_line)
                f.write(f'\t{write_line}\n')
                f.write(f'\t{jumpers_line}\n')
            max_count_xt = max(max_count_xt, this_cab_xt_count)
    print(max_count_xt)


# Стандартная конструкция для запуска main() при непосредственном выполнении файла
if __name__ == '__main__':
    main()