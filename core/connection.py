from core.functions import sorting_key

class Connection:
    """представления одного соединения /перемычка, шлейф в рамках шкафа и в рамках нескольких шкафов/"""
    def __init__(self, cabinet: str, signal: str, *terms):
        self.cabinet = cabinet
        self.signal = signal
        self.terms = set(terms)
        
    def __str__(self):
        line = " -> ".join(sorted(self.terms, key=sorting_key))
        return f'{self.cabinet} ({line}) ({self.signal})'
    
    def __iter__(self):
        return iter(sorted(self.terms, key=sorting_key))
    
    def __repr__(self):
        return f'Connection({self.cabinet}, {self.signal}, {", ".join(self.terms)})'
    
    def __and__(self, other):
        if isinstance(other, Connection):
            if self.cabinet == other.cabinet and self.signal == other.signal:
                return Connection(self.cabinet, self.signal, *(self.terms & other.terms))
            elif self.cabinet == other.cabinet and self.signal != other.signal:
                return Connection(self.cabinet, self.signal)
        return NotImplemented
    
    def __or__(self, other):
        if isinstance(other, Connection):
            if self.cabinet == other.cabinet and self.signal == other.signal:
                return Connection(self.cabinet, self.signal, *(self.terms | other.terms))
            elif self.cabinet == other.cabinet and self.signal != other.signal:
                return Connection(self.cabinet, self.signal)
        return NotImplemented
    
    def __bool__(self):
        return bool(len(self.terms))
    
    def __add__(self, other):
        if isinstance(other, Connection):
            if self.cabinet == other.cabinet and self.signal == other.signal:
                return Connection(self.cabinet, self.signal, *(self.terms | other.terms))
        return NotImplemented
    
    def tabulated_term(self):
        return '\t'.join(iter(self))
    
    
if __name__ == '__main__':
    print(*{'1', '2'})
    first_conn = Connection(*'1HV19	0501	XT11-b9	XT10-b9'.split('\t'))
    second_conn = Connection(*'1HV19	0501	XT11-b9	XT12-b9'.split('\t'))
    third_conn = first_conn + second_conn
    print(third_conn)