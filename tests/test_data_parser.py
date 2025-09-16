import pytest
import tempfile
import os
from unittest.mock import mock_open, patch, MagicMock
from collections import defaultdict

from core.data_parser import DataParser
from core.connection import Connection

class TestDataParser:
    
    def test_initialization(self):
        parser = DataParser('test.txt')
        assert parser.source == 'test.txt'
        assert parser.num_file == 0
        assert parser.num_line == 0
        assert parser.cabinets_connections == defaultdict(list)
        assert parser.jumpers_to_lines == defaultdict(lambda: defaultdict(list))
        
    @patch('builtins.open', mock_open(read_data="Откуда\tКуда\tСигнал\n"))
    def test_only_header(self):
        parser = DataParser('header_only.txt')
        parser.parse_data()
        
        assert parser.num_file == 1
        assert parser.num_line == 0
        assert parser.cabinets_connections == defaultdict(list)
        
    @patch('builtins.open', mock_open(read_data="Откуда\tКуда\tСигнал\ncab1\t1\tTX1-a1\tXT1-b1\n"))
    def test_valid_data_line(self):
        parser = DataParser('valid.txt')
        parser.parse_data()
        
        assert parser.num_file == 1
        assert parser.num_line == 1
        assert len(parser.cabinets_connections['cab1']) == 1
        assert len(parser.jumpers_to_lines['cab1']) == 2
        assert parser.cabinets_connections['cab1'] == [Connection(*'cab1\t1\tTX1-a1\tXT1-b1'.split('\t'))]
        
    @patch('builtins.open', mock_open(read_data="Cab1\tSignal1\tXT1-b1\tXT2-b2\nCab2\tSignal2\tXT3-b3\tXT4-b4\n"))
    def test_data_without_header(self):
        """Тест данных без заголовка"""
        parser = DataParser("no_header.txt")
        parser.parse_data()
        
        assert parser.num_file == 0  # Не было заголовков
        assert parser.num_line == 2  # Но строки обработаны
        assert len(parser.cabinets_connections["Cab1"]) == 1
        assert len(parser.cabinets_connections["Cab2"]) == 1
        
    @patch('builtins.open', mock_open(read_data="Откуда\tКуда\tСигнал\nCab1\tSignal1\tXT1-b1\tXT2-b2\n\nCab2\tSignal2\tXT3-b3\tXT4-b4\n"))
    def test_with_empty_lines(self):
        """Тест с пустыми строками"""
        parser = DataParser("with_empty.txt")
        parser.parse_data()
        
        assert parser.num_file == 1
        assert parser.num_line == 2  # Пустая строка пропущена
        assert len(parser.cabinets_connections["Cab1"]) == 1
        assert len(parser.cabinets_connections["Cab2"]) == 1
        
    @patch('builtins.open', mock_open(read_data="Откуда\tКуда\tСигнал\nCab1\tSignal1\tXT1-b1\tXT2-b2\nОткуда\tКуда\tСигнал\nCab2\tSignal2\tXT3-b3\tXT4-b4\n"))
    def test_multiple_headers(self):
        """Тест нескольких заголовков"""
        parser = DataParser("multiple_headers.txt")
        parser.parse_data()
        
        assert parser.num_file == 2  # Два заголовка
        assert parser.num_line == 1  # Одна строка в послед файле данных
        assert len(parser.cabinets_connections["Cab1"]) == 1
        assert len(parser.cabinets_connections["Cab2"]) == 1
        # проверяем заполнение номеров клемм:
        assert parser.jumpers_to_lines['Cab1']['XT1-b1'] == ['1_1']
        assert parser.jumpers_to_lines['Cab1']['XT2-b2'] == ['1_1']
        assert parser.jumpers_to_lines['Cab2']['XT3-b3'] == ['2_1']
        assert parser.jumpers_to_lines['Cab2']['XT4-b4'] == ['2_1']
        
    @patch('builtins.open', mock_open(read_data="Откуда\tКуда\tСигнал\nCab1\tSignal1\tXT1-b1\tXT2-b2\nCab1\tSignal1\tXT1-b1\tXT4-b4\n"))
    def test_multiple_links(self):
        parser = DataParser('multiple_links.txt')
        parser.parse_data()
        
        assert parser.jumpers_to_lines['Cab1']['XT1-b1'] == ['1_1', '1_2']
        
    @patch('builtins.open', mock_open(read_data="Cab1\t\tXT1-b1\tXT2-b2\n"))
    @patch('builtins.print')
    def test_empty_signal(self, mock_print):
        """Тест пустого сигнала"""
        parser = DataParser("empty_signal.txt")
        parser.parse_data()
        
        # Должен обработать без ошибок
        assert len(parser.cabinets_connections["Cab1"]) == 1
        connection = parser.cabinets_connections["Cab1"][0]
        assert connection.signal == ""  # Пустой сигнал
        
def test_connection_objects_creation():
    """Тест что создаются правильные объекты Connection"""
    test_content = "Cab1\tSignal1\tXT1-b1\tXT2-b2\n"
    
    with patch('builtins.open', mock_open(read_data=test_content)):
        parser = DataParser("test.txt")
        parser.parse_data()
        
        connection = parser.cabinets_connections["Cab1"][0]
        assert isinstance(connection, Connection)
        assert connection.cabinet == "Cab1"
        assert connection.signal == "Signal1"
        assert connection.terms == {"XT1-b1", "XT2-b2"}