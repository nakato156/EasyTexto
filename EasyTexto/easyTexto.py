from io import FileIO
from os.path import getsize as os_getsize
from os import remove as os_remove, rename as os_rename
from typing import Type, Union, Any
from .linea import Linea

class EasyTexto:
    def __init__(self, filename:str, encode:str='utf-8', tipo:str = 'normal'):
        self.encode = encode
        self.filename = filename
        self.__file = FileIO(filename)
        self.__preview = ''
        self.update_preview()
        self.lineas_totales = self._contar_lineas()

    def _contar_lineas(self) -> int:
        with open(self.filename) as f:
            return sum( 1 for _ in f)

    def update_preview(self):
        with FileIO(self.filename) as f:
            size_file = os_getsize(self.filename)
            total_bytes = 800
            preview = ''
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
    
    def _decode_line(self, line, line_number):
        try: 
            line = line.decode(self.encode)
        except: 
            line = str(line)

        return Linea(line, line_number)
    
    def __getitem__(self, num_linea:Type[int]):
        if not isinstance(num_linea, (int, slice)):
            raise TypeError('El índice debe ser un valor entero o slice')
        
        is_slice = False
        if type(num_linea) == int:
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
        if type(val) != str:
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
                f.write(texto.encode(self.encode) + b'\n')
                f.truncate()
                if pos_ < self.lineas_totales:
                    f.write(b''.join(str(linea).encode(self.encode) for linea in resto_texto))
        
    def append(self, texto:Union[str, bytes, list, tuple]):
        convert = lambda txt: txt.encode(self.encode) if type(txt) == str else txt
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

    def __repr__(self) -> str:
        self.update_preview()
        try:
            return self.__preview.decode(self.encode)
        except:
            return str(self.__preview)
