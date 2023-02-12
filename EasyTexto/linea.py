from io import UnsupportedOperation


class Linea:
    def __init__(self, texto:str, num_linea:int):
        self.texto: str = texto
        self.__num_linea:int = num_linea
    
    @property
    def num_linea(self):
        return self.__num_linea
    
    def editar(self, texto:str):
        self.texto = texto

    def eqf(self, other) -> bool:
        if type(other) == Linea: return other.texto == self.texto and other.num_linea == self.num_linea
        return other == self.texto

    def nef(self, other) -> bool:
        if type(other) == Linea: return other.texto != self.texto and other.num_linea != self.num_linea
        return other != self.texto

    def __len__(self) -> int:
        return len(self.texto)
    
    def __bool__(self) -> bool:
        return not not self.texto.strip('\r\n')

    def __lt__(self, __o) -> bool:
        if type(__o) == Linea: self.num_linea < __o.num_linea
        raise UnsupportedOperation(f'No se puede operar Linea con {type(__o)}')

    def __le__(self, __o) -> bool:
        if type(__o) == Linea: self.num_linea <= __o.num_linea
        raise UnsupportedOperation(f'No se puede operar Linea con {type(__o)}')

    def __gt__(self, __o) -> bool:
        if type(__o) == Linea: self.num_linea > __o.num_linea
        raise UnsupportedOperation(f'No se puede operar Linea con {type(__o)}')

    def __ge__(self, __o) -> bool:
        if type(__o) == Linea: self.num_linea >= __o.num_linea
        raise UnsupportedOperation(f'No se puede operar Linea con {type(__o)}')

    def __eq__(self, __o) -> bool:
        if type(__o) == Linea: return __o.texto.strip('\r\n') == self.texto.strip('\r\n')
        return  __o == self.texto.strip('\r\n')
    
    def __ne__(self, __o: object) -> bool:
        if type(__o) == Linea: return __o.texto.strip('\r\n') != self.texto.strip('\r\n')
        return  __o != self.texto.strip('\r\n')

    def __str__(self) -> str:
        return self.texto

    def __repr__(self) -> str:
        return f'{self.num_linea}| {self.texto}'