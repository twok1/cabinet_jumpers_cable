from typing import Dict, Set, List

from core.connection import Connection

class DataMerging:
    def __init__(self, cabinet_jumpers: Dict[str, List[Connection]]):
        self.cabinet_jumpers = cabinet_jumpers
        
    def process(self):
        for cabinet, jumpers in self.cabinet_jumpers.items():
            a = 0
            while a < len(jumpers):
                b = a + 1
                while b < len(jumpers):
                    if jumpers[a] & jumpers[b]:
                        jumpers[a] |= jumpers.pop(b)
                        b = a + 1
                    else:
                        b += 1
                a += 1
                if a % 100 == 0:
                    print(f"{cabinet}={a}/{len(jumpers)}")