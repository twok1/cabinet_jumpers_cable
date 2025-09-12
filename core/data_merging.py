from typing import Dict, Set, List
from core.functions import union_find

class DataMerging:
    def __init__(self, cabinet_jumpers: Dict[str, List[Set[str]]]):
        self.cabinet_jumpers = cabinet_jumpers
        
    def process(self):
        for cabinet, jumpers in self.cabinet_jumpers.items():
            a = 0
            while a < len(jumpers):
                b = a + 1
                while b < len(jumpers):
                    if jumpers[a] & jumpers[b]:
                        jumpers[a] |= jumpers.pop(b)
                    else:
                        b += 1
                a += 1