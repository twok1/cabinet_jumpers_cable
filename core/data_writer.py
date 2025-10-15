from typing import Dict, List, Set

from core.functions import sorting_key
from core.connection import Connection

class DataWriter:
    def __init__(self, target, cabinet_jumpers: Dict[str, List[Connection]], jumpers_to_lines: Dict[str, Dict[str, List[str]]]):
        self.target = target
        self.cabinet_jumpers: Dict[str, List[Set[str]]] = cabinet_jumpers
        self.jumpers_to_lines: Dict[str, Dict[str, List[str]]] = jumpers_to_lines
        with open(self.target, 'w', encoding='utf-8') as f:
            f.write('')
        
    def process(self):
        for cabinet, jumpers in sorted(self.cabinet_jumpers.items(), key=lambda x: int(''.join(i for i in x[0] if i.isdigit()))):
            self.print(cabinet)
            for jumper in sorted(jumpers, key=sorting_key):
                lines = []
                for wire in jumper:
                    lines.append(', '.join(self.jumpers_to_lines[cabinet][wire]))
                ending = ''
                for k in lines:
                    if k.count(',') > 1:
                        ending = '\tЗамечание 3 на 2' 
                self.print(f'\t{jumper.tabulated_term()}')
                self.print(f'\t{"\t".join(lines)}{ending}')
                
    def print(self, *line):
        with open(self.target, 'a', encoding='utf-8') as f:
            f.write(f'{line[0]}\n')
            # print(*line)