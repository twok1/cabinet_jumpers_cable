from collections import defaultdict
import time
import re
from typing import Dict, List, Set, Tuple

class RussianLettersValidator:
    """Класс для валидации русских букв"""
    RUS_LETTERS = (
        'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 
        'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 
        'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я',
        'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й',
        'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф',
        'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я'
    )
    
    @classmethod
    def contains_russian_letters(cls, text: str) -> bool:
        """Проверяет, содержит ли текст русские буквы"""
        return any(letter in text for letter in cls.RUS_LETTERS)
    
    @classmethod
    def find_russian_letters(cls, text: str) -> List[str]:
        """Находит все русские буквы в тексте"""
        return [letter for letter in cls.RUS_LETTERS if letter in text]


class SortingStrategy:
    """Стратегия сортировки для элементов вида XT..."""
    
    @staticmethod
    def get_key(item: str) -> Tuple[int, int, int, str]:
        """
        Кастомный ключ сортировки для элементов вида XT...
        Возвращает кортеж: (приоритет группы, число, исходная строка)
        """
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
        numbers = re.findall(r'\d+', item)
        number_one = int(numbers[0]) if numbers and len(numbers) >= 1 else 0
        number_two = int(numbers[1]) if numbers and len(numbers) >= 2 else 0
        
        return (group_priority, number_one, number_two, item)


class Connection:
    """Сущность, представляющая соединение между точками"""
    
    def __init__(self, fr: str, to: str, source_info: str):
        self.fr = fr
        self.to = to
        self.source_info = source_info
        self.points = {fr, to}
    
    def __eq__(self, other):
        if not isinstance(other, Connection):
            return False
        return self.points == other.points
    
    def __hash__(self):
        return hash(frozenset(self.points))
    
    def merge(self, other: 'Connection') -> 'Connection':
        """Объединяет два соединения"""
        if not isinstance(other, Connection):
            raise ValueError("Can only merge with another Connection")
        
        merged_points = self.points | other.points
        merged_source = f"{self.source_info}, {other.source_info}"
        
        # Создаем новое соединение с объединенными точками
        # Для простоты берем первую точку как fr, последнюю как to
        sorted_points = sorted(merged_points)
        return Connection(sorted_points[0], sorted_points[-1], merged_source)
    
    def get_sorted_points(self, sorting_key_func) -> List[str]:
        """Возвращает отсортированные точки соединения"""
        return sorted(self.points, key=sorting_key_func)
    
    def __repr__(self):
        return f"Connection({self.fr} -> {self.to}, source: {self.source_info})"


class Cabinet:
    """Сущность, представляющая шкаф с соединениями"""
    
    def __init__(self, name: str):
        self.name = name
        self.connections: List[Connection] = []
        self.original_data: Dict[str, List[str]] = defaultdict(list)
    
    def add_connection(self, connection: Connection):
        """Добавляет соединение к шкафу"""
        self.connections.append(connection)
        
        # Добавляем информацию в original_data
        for point in connection.points:
            self.original_data[point].append(connection.source_info)
    
    def merge_connections(self):
        """Объединяет связанные соединения (компоненты связности графа)"""
        merged = True
        while merged:
            merged = False
            i = 0
            while i < len(self.connections):
                j = i + 1
                while j < len(self.connections):
                    if self.connections[i].points & self.connections[j].points:
                        # Объединяем соединения
                        merged_conn = self.connections[i].merge(self.connections[j])
                        self.connections[i] = merged_conn
                        self.connections.pop(j)
                        merged = True
                    else:
                        j += 1
                i += 1
    
    def sort_connections(self):
        """Сортирует соединения и их точки"""
        # Сортируем точки внутри каждого соединения
        for i in range(len(self.connections)):
            sorted_points = self.connections[i].get_sorted_points(SortingStrategy.get_key)
            # Создаем временное соединение с отсортированными точками
            self.connections[i] = Connection(
                sorted_points[0], 
                sorted_points[-1] if len(sorted_points) > 1 else sorted_points[0],
                self.connections[i].source_info
            )
        
        # Сортируем сами соединения
        self.connections.sort(key=lambda conn: SortingStrategy.get_key(conn.fr))


class DataParser:
    """Класс для парсинга данных из файла"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.cabinets: Dict[str, Cabinet] = {}
        self.num_line = 0
        self.num_file = 0
    
    def parse_file(self):
        """Парсит файл и создает объекты Cabinet и Connection"""
        with open(self.file_path, encoding='utf-8') as f:
            for line in f.readlines():
                self._process_line(line.strip())
    
    def _process_line(self, line: str):
        """Обрабатывает одну строку файла"""
        if 'Откуда' in line:
            self.num_line = 0
            self.num_file += 1
            return
        
        self.num_line += 1
        
        if not line or 'Откуда' in line:
            return
        
        try:
            cabinet, signal, fr, to = line.split('\t')
            source_info = f'{self.num_file}_{self.num_line}'
            
            # Создаем или получаем шкаф
            if cabinet not in self.cabinets:
                self.cabinets[cabinet] = Cabinet(cabinet)
            
            # Создаем и добавляем соединение
            connection = Connection(fr, to, source_info)
            self.cabinets[cabinet].add_connection(connection)
            
        except ValueError:
            print(f"Ошибка парсинга строки: {line}")


class ResultWriter:
    """Класс для записи результатов"""
    
    def __init__(self, output_path: str):
        self.output_path = output_path
        self.max_count_xt = 0
    
    def write_results(self, cabinets: Dict[str, Cabinet]):
        """Записывает результаты в файл"""
        with open(self.output_path, 'w', encoding='utf-8') as f:
            for cabinet_name, cabinet in cabinets.items():
                self._write_cabinet(f, cabinet_name, cabinet)
        
        print(f"Максимальное количество XT: {self.max_count_xt}")
    
    def _write_cabinet(self, f, cabinet_name: str, cabinet: Cabinet):
        """Записывает данные одного шкафа"""
        print(cabinet_name)
        f.write(f'{cabinet_name}\n')
        
        this_cab_xt_count = 0
        
        for connection in cabinet.connections:
            points = connection.get_sorted_points(SortingStrategy.get_key)
            this_cab_xt_count += len(points)
            
            # Формируем строки для записи
            write_line = "\t".join(points)
            jumpers_line = "\t".join(
                ', '.join(cabinet.original_data[klemm]) 
                for klemm in points
            )
            
            # Проверяем на русские буквы
            self._check_russian_letters(write_line)
            
            # Выводим в консоль и файл
            print(*points, sep='\t')
            print(jumpers_line)
            f.write(f'\t{write_line}\n')
            f.write(f'\t{jumpers_line}\n')
        
        self.max_count_xt = max(self.max_count_xt, this_cab_xt_count)
    
    def _check_russian_letters(self, text: str):
        """Проверяет текст на наличие русских букв"""
        if RussianLettersValidator.contains_russian_letters(text):
            found_letters = RussianLettersValidator.find_russian_letters(text)
            print(f'Найдены русские буквы: {found_letters}')
            time.sleep(3)


class Application:
    """Основной класс приложения"""
    
    def __init__(self, input_path: str, output_path: str):
        self.input_path = input_path
        self.output_path = output_path
        self.parser = DataParser(input_path)
        self.writer = ResultWriter(output_path)
    
    def run(self):
        """Запускает приложение"""
        # Парсим данные
        self.parser.parse_file()
        
        # Обрабатываем каждый шкаф
        for cabinet in self.parser.cabinets.values():
            cabinet.merge_connections()
            cabinet.sort_connections()
        
        # Записываем результаты
        self.writer.write_results(self.parser.cabinets)


def main():
    """Точка входа в приложение"""
    app = Application('./data/data.txt', './output/result.txt')
    app.run()


if __name__ == '__main__':
    main()