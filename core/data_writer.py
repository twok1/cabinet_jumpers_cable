from typing import Dict, List, Set

from core.functions import sorting_key

class DataWriter:
    def __init__(self, target, cabinet_jumpers: Dict[str, List[Set[str]]], jumpers_to_lines: Dict[str, Dict[str, List[str]]]):
        self.target = target
        self.cabinet_jumpers: Dict[str, List[Set[str]]] = cabinet_jumpers
        self.jumpers_to_lines: Dict[str, Dict[str, List[str]]] = jumpers_to_lines
        
    def process(self):
        for cabinet, jumpers in sorted(self.cabinet_jumpers.items(), key=lambda x: int(''.join(i for i in x[0] if i.isdigit()))):
            print(cabinet)
            for jumper in sorted(jumpers, key=sorting_key):
                lines = []
                for wire in sorted(jumper, key=sorting_key):
                    print('\t', wire, end='\t')
                    lines.append(', '.join(self.jumpers_to_lines[cabinet][wire]))
                print()
                print('\t', '\t'.join(lines))