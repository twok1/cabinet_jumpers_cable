import pytest
import tempfile
import os
from unittest.mock import mock_open, patch, MagicMock
from typing import Dict, List, Set
from collections import defaultdict

from core.functions import sorting_key
from core.data_writer import DataWriter
from core.connection import Connection

class TestDataWriter:
    @pytest.fixture
    def sample_data(self):
        return {
            'cabinet_jumpers': {
                'cab2': [Connection('cab2', '1', 'XT1-b1', 'XT2-b2')],
                'cab1': [Connection('cab1', '2', 'XT3-b3', 'XT4-b4'), Connection('cab1', '3', 'XT5-b5', 'XT6-b6')]
            }
        }