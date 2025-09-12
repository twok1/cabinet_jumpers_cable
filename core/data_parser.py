from typing import Dict, Set, List
from collections import defaultdict

from core.connection import Connection

class DataParser:
    def __init__(self, source):
        self.source = source
        self.num_file = 0
        self.num_line = 0
        self.cabinets_jumpers: Dict[str, List[Set[str]]] = defaultdict(list)
        self.jumpers_to_lines: Dict[str, Dict[str, List[str]]] = defaultdict(lambda: defaultdict(list))
        
    def parse_data(self):
        with open(self.source, encoding='utf-8') as rf:
            for line in rf.readlines():
                self._process_line(line=line)
            
    def _process_line(self, line: str):
        line = line.strip()
        
        if not line.strip():
            return
        
        if 'Откуда' in line:
            self.num_line = 0
            self.num_file += 1
            return
        
        self.num_line += 1
        
        try:
            cabinet, signal, fr, to = line.split('\t')
            source_info = f'{self.num_file}_{self.num_line}'
            self.cabinets_jumpers[cabinet].append(Connection(
                cabinet,
                signal,
                fr,
                to
            ))
            for term in (fr, to):
                self.jumpers_to_lines[cabinet][term].append(source_info)
            
        except:
            print('Ошибка парсинга страницы')
            
            