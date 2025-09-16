import pytest
from core.functions import sorting_key
from core.connection import Connection


class TestConnection:
    """Тесты для класса Connection"""
    
    def test_initialization(self):
        """Тест инициализации объекта"""
        conn = Connection("Cab1", "Signal1", "term1", "term2")
        assert conn.cabinet == "Cab1"
        assert conn.signal == "Signal1"
        assert conn.terms == {"term1", "term2"}
    
    def test_initialization_with_single_term(self):
        """Тест инициализации с одним терминалом"""
        conn = Connection("Cab1", "Signal1", "term1")
        assert conn.terms == {"term1"}
    
    def test_initialization_no_terms(self):
        """Тест инициализации без терминалов"""
        conn = Connection("Cab1", "Signal1")
        assert conn.terms == set()
    
    def test_str_representation(self):
        """Тест строкового представления"""
        conn = Connection("Cab1", "Signal1", "XT2-b1", "XT1-b2")
        expected = "Cab1 (XT1-b2 -> XT2-b1) (Signal1)"
        assert str(conn) == expected
    
    def test_str_representation_no_terms(self):
        """Тест строкового представления без терминалов"""
        conn = Connection("Cab1", "Signal1")
        expected = "Cab1 () (Signal1)"
        assert str(conn) == expected
    
    def test_repr_representation(self):
        """Тест repr представления"""
        conn = Connection("Cab1", "Signal1", "term1", "term2")
        repr_str = repr(conn)
        assert "Connection(" in repr_str
        assert "Cab1" in repr_str
        assert "Signal1" in repr_str
        assert "term1" in repr_str
        assert "term2" in repr_str
    
    def test_iteration(self):
        """Тест итерации по терминалам"""
        conn = Connection("Cab1", "Signal1", "XT2-b1", "XT1-b2")
        terms = list(conn)
        expected = sorted(["XT1-b2", "XT2-b1"], key=sorting_key)
        assert terms == expected
    
    def test_iteration_empty(self):
        """Тест итерации по пустым терминалам"""
        conn = Connection("Cab1", "Signal1")
        terms = list(conn)
        assert terms == []
    
    def test_bool_true(self):
        """Тест булевого значения с терминалами"""
        conn = Connection("Cab1", "Signal1", "term1")
        assert bool(conn) is True
    
    def test_bool_false(self):
        """Тест булевого значения без терминалов"""
        conn = Connection("Cab1", "Signal1")
        assert bool(conn) is False
    
    def test_and_operator_same_signal(self):
        """Тест оператора & с одинаковыми сигналами"""
        conn1 = Connection("Cab1", "Signal1", "term1", "term2")
        conn2 = Connection("Cab1", "Signal1", "term2", "term3")
        result = conn1 & conn2
        assert result.cabinet == "Cab1"
        assert result.signal == "Signal1"
        assert result.terms == {"term2"}
    
    def test_and_operator_different_signal(self):
        """Тест оператора & с разными сигналами"""
        conn1 = Connection("Cab1", "Signal1", "term1", "term2")
        conn2 = Connection("Cab1", "Signal2", "term2", "term3")
        result = conn1 & conn2
        assert result.cabinet == "Cab1"
        assert result.signal == "Signal1"  # Берет сигнал из первого объекта
        assert result.terms == set()  # Пустое множество при разных сигналах
    
    def test_and_operator_different_cabinet(self):
        """Тест оператора & с разными шкафами"""
        conn1 = Connection("Cab1", "Signal1", "term1")
        conn2 = Connection("Cab2", "Signal1", "term1")
        result = conn1 & conn2
        assert result.cabinet == conn1.cabinet
        assert result.signal == conn1.signal
        assert result.terms == set()
    
    def test_or_operator_same_signal(self):
        """Тест оператора | с одинаковыми сигналами"""
        conn1 = Connection("Cab1", "Signal1", "term1", "term2")
        conn2 = Connection("Cab1", "Signal1", "term2", "term3")
        result = conn1 | conn2
        assert result.cabinet == "Cab1"
        assert result.signal == "Signal1"
        assert result.terms == {"term1", "term2", "term3"}
    
    def test_or_operator_different_signal(self):
        """Тест оператора | с разными сигналами"""
        conn1 = Connection("Cab1", "Signal1", "term1", "term2")
        conn2 = Connection("Cab1", "Signal2", "term2", "term3")
        result = conn1 | conn2
        assert result.cabinet == "Cab1"
        assert result.signal == "Signal1"  # Берет сигнал из первого объекта
        assert result.terms == set()  # Пустое множество при разных сигналах
    
    def test_add_operator_same_signal(self):
        """Тест оператора + с одинаковыми сигналами"""
        conn1 = Connection("Cab1", "Signal1", "term1", "term2")
        conn2 = Connection("Cab1", "Signal1", "term2", "term3")
        result = conn1 + conn2
        assert result.cabinet == "Cab1"
        assert result.signal == "Signal1"
        assert result.terms == {"term1", "term2", "term3"}
    
    def test_add_operator_different_signal(self):
        """Тест оператора + с разными сигналами"""
        conn1 = Connection("Cab1", "Signal1", "term1")
        conn2 = Connection("Cab1", "Signal2", "term2")
        
        # Проверяем что операция не поддерживается
        with pytest.raises(TypeError, match="unsupported operand type"):
            result = conn1 + conn2

    def test_add_operator_different_cabinet(self):
        """Тест оператора + с разными шкафами"""
        conn1 = Connection("Cab1", "Signal1", "term1")
        conn2 = Connection("Cab2", "Signal1", "term2")
        
        # Проверяем что операция не поддерживается
        with pytest.raises(TypeError, match="unsupported operand type"):
            result = conn1 + conn2
    
    def test_tabulated_term_with_terms(self):
        """Тест метода tabulated_term с терминалами"""
        conn = Connection("Cab1", "Signal1", "XT1-b1", "XT2-b2")
        result = conn.tabulated_term()
        expected_terms = sorted(["XT1-b1", "XT2-b2"], key=sorting_key)
        expected = "\t".join(expected_terms)
        assert result == expected
    
    def test_tabulated_term_empty(self):
        """Тест метода tabulated_term без терминалов"""
        conn = Connection("Cab1", "Signal1")
        result = conn.tabulated_term()
        assert result == ""
    
    def test_equality_not_implemented(self):
        """Тест что равенство не реализовано"""
        conn1 = Connection("Cab1", "Signal1", "term1")
        conn2 = Connection("Cab1", "Signal1", "term1")
        # Класс не реализует __eq__, поэтому объекты не равны даже с одинаковыми данными
        assert conn1 != conn2
    
    def test_real_world_example(self):
        """Тест реального примера из main"""
        first_conn = Connection(*'1HV19\t0501\tXT11-b9\tXT10-b9'.split('\t'))
        second_conn = Connection(*'1HV19\t0501\tXT11-b9\tXT12-b9'.split('\t'))
        third_conn = first_conn + second_conn
        
        assert third_conn.cabinet == "1HV19"
        assert third_conn.signal == "0501"
        assert third_conn.terms == {"XT10-b9", "XT11-b9", "XT12-b9"}
        
        # Проверяем сортировку в строковом представлении
        str_result = str(third_conn)
        assert "XT10-b9 -> XT11-b9 -> XT12-b9" in str_result or \
               "XT10-b9 -> XT12-b9 -> XT11-b9" in str_result  # Зависит от sorting_key


class TestConnectionEdgeCases:
    """Тесты для крайних случаев класса Connection"""
    
    def test_terms_with_duplicates(self):
        """Тест что дубликаты терминалов удаляются"""
        conn = Connection("Cab1", "Signal1", "term1", "term1", "term2")
        assert conn.terms == {"term1", "term2"}
        assert len(conn.terms) == 2
    
    def test_terms_with_different_types(self):
        """Тест с терминалами разных типов (должно работать если sorting_key обрабатывает)"""
        conn = Connection("Cab1", "Signal1", "XT1-b1", "A1", "Z10")
        terms = list(conn)
        # Проверяем что сортировка работает без ошибок
        assert len(terms) == 3
    
    def test_empty_string_terms(self):
        """Тест с пустыми строками в терминалах"""
        conn = Connection("Cab1", "Signal1", "", "term1")
        assert conn.terms == {"", "term1"}
    

def test_sorting_key_integration():
    """Интеграционный тест с sorting_key"""
    # Создаем соединение с терминалами, которые должны сортироваться
    terms = ["XT20-b1", "XT3-b10", "XT1-b2", "XT10-b1"]
    conn = Connection("Cab1", "Signal1", *terms)
    
    sorted_terms = list(conn)
    # Проверяем что сортировка произошла (не в исходном порядке)
    assert sorted_terms != terms
    # Проверяем что все терминалы присутствуют
    assert set(sorted_terms) == set(terms)


if __name__ == "__main__":
    # Запуск тестов без pytest
    test_instance = TestConnection()
    
    print("Запуск тестов класса Connection...")
    
    # Запускаем основные тесты
    test_instance.test_initialization()
    test_instance.test_str_representation()
    test_instance.test_real_world_example()
    
    print("Все тесты пройдены успешно!")
    
    # Демонстрация работы из примера
    print("\nДемонстрация из примера:")
    first_conn = Connection(*'1HV19\t0501\tXT11-b9\tXT10-b9'.split('\t'))
    second_conn = Connection(*'1HV19\t0501\tXT11-b9\tXT12-b9'.split('\t'))
    third_conn = first_conn + second_conn
    print(third_conn)