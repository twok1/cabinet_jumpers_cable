from typing import Dict, Set, List
from core.functions import union_find

class DataMerging:
    def __init__(self, cabinet_jumpers: Dict[str, List[Set[str]]]):
        self.cabinet_jumpers = cabinet_jumpers
        
    def process(self):
        for cabinet, jumpers in self.cabinet_jumpers.items():
            self.cabinet_jumpers[cabinet] = union_find(jumpers)