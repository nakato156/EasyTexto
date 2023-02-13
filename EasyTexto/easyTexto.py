from io import FileIO, StringIO
from colorama import Fore, init
from os.path import getsize as os_getsize
from os import remove as os_remove, rename as os_rename
from typing import Type, Union, Literal, Any, Callable
from .linea import Linea

init()

class EasyTexto:
    def __init__(self, filename:str, encoding:str='utf-8', tipo:Literal['simple', 'dialogo'] = 'simple', rule: Callable = None):
        self.encoding = encoding
        self.filename = filename
        # self.__file = FileIO(filename)
        self.tipo = tipo
        self.__preview = ''
        self.update_preview()
        self.lineas_totales = self._contar_lineas()
        if tipo == 'dialogo':
            if rule != None: self.validator = rule
            else: self.validator = lambda x: x.split(':', maxsplit=1) if ':' in x else False

    def _contar_lineas(self) -> int:
        with open(self.filename) as f:
            return sum( 1 for _ in f)
    
    def _decode_line(self, line, line_number) -> Linea:
        try: 
            line = line.decode(self.encoding)
        except: 
            line = str(line)

        return Linea(line, line_number)

    def update_preview(self):
        with FileIO(self.filename) as f:
            size_file = os_getsize(self.filename)
            total_bytes = 800
            if size_file > total_bytes:
                preview = b''.join(f.readline() for _ in range(5)) + b'.' * 10 + b'\n'
                lineas = []
                linea = f.readline()
                while linea:
                    lineas.append(linea)
                    if len(lineas) > 3: lineas[:] = lineas[1:]
                    linea = f.readline()
                preview += b''.join(lineas)
            else: preview = f.read()
        self.__preview = preview
    
    def get_msg_by(self, name:str) -> list[str]:
        res = []
        with open(self.filename, encoding=self.encoding) as f:
            for linea in f:
                r = self.validator(linea)
                if not r:
                    raise SyntaxError(f'El archivo no concide con el formato selecionado ({self.tipo})')
                if r[0].strip() == name: res.append(r[1])

        return res

    def get_msgs(self) -> dict:
        res:dict[list] = {}
        with open(self.filename) as f:
            for linea in f:
                r = self.validator(linea)
                if not r:
                    raise SyntaxError(f'El archivo no concide con el formato selecionado ({self.tipo})')
                if r[0] in res:
                    res[r[0]].append(r[1])
                else:
                    res[r[0]] = [r[1]]
        return res

    def __getitem__(self, num_linea:Type[int]) -> Union[Linea, list]:
        if not isinstance(num_linea, (int, slice)):
            raise TypeError('El índice debe ser un valor entero o slice')
        
        is_slice = False
        if type(num_linea) == int:
            num_linea = num_linea if num_linea > 0 else self.lineas_totales + num_linea + 1
            start, stop, step = num_linea, num_linea, 1
        else:
            is_slice = True
            start = num_linea.start or 0
            stop = num_linea.stop or self.lineas_totales
            step = num_linea.step or 1
        
        if start > self.lineas_totales: raise IndexError()

        result = []
        with FileIO(self.filename) as f:
            for i in range(stop - 1):
                linea = f.readline()
                if start < i+1 and not i % step: result.append(self._decode_line(linea, i + 1))
            
            result.append(self._decode_line(f.readline(), stop))
        return result if is_slice else result[0]
    
    def __setitem__(self, pos:Type[int], val:Union[Linea, str, Any]):
        if not isinstance(pos, (int, slice)): 
            raise TypeError('El índice debe ser un valor entero o slice')
        if not isinstance(val, (str, Linea)):
            raise TypeError('El valor debe ser de tipo str, Linea o una instancia de esta')
        texto = val if type(val) == str else val.texto

        if type(pos) == slice:
            start = pos.start or 1
            stop = pos.stop or self.lineas_totales + 1
            step = pos.step or 1
            rango = range(start, stop, step)
        else: rango = (pos, )
        
        for pos_ in rango:
            bytes_leidos = 0
            resto_texto = self[pos_:]
            with FileIO(self.filename, 'r+') as f:
                for _ in range(pos_ - 1):
                    bytes_leidos += len(f.readline())
                f.write(texto.encode(self.encoding) + b'\n')
                f.truncate()
                if pos_ < self.lineas_totales:
                    f.write(b''.join(str(linea).encode(self.encoding) for linea in resto_texto))
        
    def append(self, texto:Union[str, bytes, list, tuple]):
        convert = lambda txt: txt.encode(self.encoding) if type(txt) == str else txt
        with FileIO(self.filename, 'a+b') as f:
            if isinstance(texto, (list, tuple)): texto = b'\n'.join(convert(text) for text in texto)
            else: texto = convert(texto)
            f.write(texto)
        self.lineas_totales += 1

    def eliminar(self, indices:Union[int, tuple]):
        if not isinstance(indices, (int, tuple)):
            raise TypeError('El  índice debe ser int o tuple')
                
        if type(indices) == int: indices = (indices, )
                
        with open(self.filename) as file, open(f"{self.filename}.tmp", "w") as new_file:
            for i, line in enumerate(file):
                if not (i + 1) in indices:
                    new_file.write(line)
            
        os_remove(self.filename)
        os_rename(f"{self.filename}.tmp", self.filename)

    def leer(self) -> str:
        with FileIO(self.filename) as f:
            return f.read().decode(self.encoding)

    def diff(self, other, encodig:str=None, show:bool = True) -> list[tuple]:
        if not isinstance(other, (str, EasyTexto, StringIO, FileIO)):
            raise TypeError("El argumento debe ser un string, EasyTexto object, StringIO object o FileIO object.")
        
        diferencias = []
        if isinstance(other, (str, EasyTexto)):
            filename = other.filename if type(other) == EasyTexto else other
            other_stream = open(filename, encoding=encodig)
        else: other_stream = other

        with open(self.filename, encoding=self.encoding) as this_file, other_stream as other_file:
            for i, (f1, f2) in enumerate(zip(this_file, other_file)):
                if f1 != f2:
                    diferencias.append((i + 1, f1, f2))
        
        if show: print(''.join(f'{Fore.GREEN}{lineas[0]}| {lineas[1]}{Fore.RED}{lineas[0]}| {lineas[2]}{Fore.RESET}' for lineas in diferencias))
        return diferencias

    def __repr__(self) -> str:
        self.update_preview()
        try:
            return self.__preview.decode(self.encoding)
        except:
            return str(self.__preview)
