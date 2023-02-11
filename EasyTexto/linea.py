class Linea:
    def __init__(self, texto:str, num_linea:int):
        self.texto: str = texto
        self.__num_linea:int = num_linea
    
    @property
    def num_linea(self):
        return self.__num_linea
    
    def editar(self, texto:str):
        self.texto = texto
        
    def __len__(self) -> int:
        return len(self.texto)

    def __str__(self) -> str:
        return self.texto

    def __repr__(self) -> str:
        return f'{self.num_linea}| {self.texto}'