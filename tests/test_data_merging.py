import pytest
from typing import Dict, Set, List

from core.data_merger import DataMerging
from core.connection import Connection

class TestDataMerging:
    
    def test_basic_merging(self):
        """Тест базового объединения пересекающихся множеств"""
        cabinet_jumpers = {
            'cab1': [
                Connection('cab1', '1', 'a', 'b'),
                Connection('cab1', '1', 'b', 'c')
            ]
        }
        merger = DataMerging(cabinet_jumpers)
        merger.process()
        
        expected = {
            'cab1': [Connection('cab1', '1', 'a', 'b', 'c')]
        }
        assert cabinet_jumpers == expected
        
    def test_no_intersection(self):
        cabinet_jumpers = {
            'cab1': [
                Connection('cab1', '1', 'a', 'b'),
                Connection('cab1', '1', 'c', 'd'),
                Connection('cab1', '1', 'e', 'f')
            ]
        }
        merger = DataMerging(cabinet_jumpers)
        merger.process()
        
        expected = {
            'cab1': [
                Connection('cab1', '1', 'a', 'b'),
                Connection('cab1', '1', 'c', 'd'),
                Connection('cab1', '1', 'e', 'f')
            ]
        }
        assert cabinet_jumpers == expected
        
    def test_multiple_cabinets(self):
        cabinets_jumpers = {
            'cab1': [Connection('cab1', '1', 'A', 'B'), Connection('cab1', '1', 'B', 'C')],
            'cab2': [Connection('cab2', '1', 'X', 'Y'), Connection('cab2', '1', 'Y', 'Z')]
        }
        
        merger = DataMerging(cabinets_jumpers)
        merger.process()
        
        expected = {
            'cab1': [Connection('cab1', '1', 'A', 'B', 'C')],
            'cab2': [Connection('cab2', '1', 'X', 'Y', 'Z')]
        }
        
        assert cabinets_jumpers == expected
        
    def test_complex_merging(self):
        cabinet_jumpers = {
            'cab1': [
                Connection('cab1', '1', 'a', 'b'),
                Connection('cab1', '1', 'b', 'c', 'd'),
                Connection('cab1', '1', 'e', 'f'),
                Connection('cab1', '1', 'd', 'e'),
                Connection('cab1', '1', 'g', 'h')
            ]
        }
        
        merger = DataMerging(cabinet_jumpers)
        merger.process()
        
        expected = {
            'cab1': [
                Connection('cab1', '1', 'a', 'b', 'c', 'd', 'e', 'f'),
                Connection('cab1', '1', 'g', 'h')
            ]
        }
        
        assert cabinet_jumpers == expected
        
    def test_single_set(self):
        cabinet_jumpers = {
            'cab1': [
                Connection('cab1', '1', 'a', 'b', 'c')
            ]
        }
        merger = DataMerging(cabinet_jumpers)
        merger.process()
        
        expected = {
            'cab1': [
                Connection('cab1', '1', 'a', 'b', 'c')
            ]
        }
        
        assert cabinet_jumpers == expected
        
    def test_empty_cabinet(self):
        cabinet_humpers = {
            'cab1': [Connection('cab1')]
        }
        merger = DataMerging(cabinet_humpers)
        merger.process()
        
        expected = {
            'cab1': [Connection('cab1')]
        }
        assert cabinet_humpers == expected