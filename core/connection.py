from functions import sorting_key

class Connection:
    """представления одного соединения /перемычка, шлейф в рамках шкафа и в рамках нескольких шкафов/"""
    def __init__(self, num_file, num_line, cabinet, signal, *terms):
        self.lines = {cabinet: {i: f'{num_file}_{num_line}' for i in terms}}
        self.cabinet = cabinet
        self.signal = signal
        self.terms = set(terms)
        
    def __str__(self):
        line = " -> ".join(sorted(self.terms, key=sorting_key))
        return f'{self.cabinet} ({line}) ({self.signal})'
    
    def __repr__(self):
        return f'Connection({self.cabinet}, {self.signal}, {", ".join(self.terms)})'
    
    def __add__(self, other):
        if isinstance(other, Connection):
            if self.cabinet == other.cabinet and self.signal == other.signal:
                return Connection(self.cabinet, self.signal, *(self.terms | other.terms))
        return NotImplemented
    
    
    
if __name__ == '__main__':
    print(*{'1', '2'})
    first_conn = Connection(1, 1, *'1HV19	0501	XT11-b9	XT10-b9'.split('\t'))
    second_conn = Connection(2, 1, *'1HV19	0501	XT11-b9	XT12-b9'.split('\t'))
    third_conn = first_conn + second_conn
    print(third_conn)