# EasyTexto
EasyTexto es un paquete que permite el manejo de archivos de texto de forma sencilla. Esta herramienta provee funciones para leer archivos así como para acceder, modificar y eliminar líneas específicas.

### ejemplo

#### Accediendo a  líneas
```python
from EasyTexto import EasyTexto

texto = EasyTexto('ruta_al_archivo.txt', encode="utf-8") #el encode por defecto es utf-8
print(texto[1]) #los índices comienzan en 1, es lo mismo que el número de línea
texto[1] = 'Soy el reemplazo de la línea #1'
print(texto[1])
```

Al acceder a las líneas del archivo se devuelve un objeto de tipo `Linea`, puede hacer la conversión a `str` usando la clase. Esta clase posee los atributos `num_línea` y `texto`, puede usar esto según su contexto.

- ejemplo

```python
print(type(texto[1]))

línea_1 = texto[1]  # la variable será de tipo Linea

#convirtiendo a str
línea_1_str = str(texto[1]) # el tipo será str

#accediendo al contenido de la línea
contenido_línea_1 = texto[1].texto
```

#### Modificando líneas
Tambien se permite el uso de slicing ya sea para obtener o modificar líneas

```python
print(texto[:3])
texto[::2] = 'holas'
print(texto) #mostrará una vista previa del archivo
```

#### Eliminando líneas
Para eliminar líneas se provee el método `eliminar` de la clase `EasyTexto`, este método recibe un entero indicando el número de línea a eliminar o una tupla con los números de líneas a eliminar.

```python
texto.eliminar(1)
texto.eliminar((1, 2))
print(texto)
```

#### Añadiendo líneas
Así como se puede eliminar líneas también se puede añadir líneas **al final** del archivo, esto gracias al método `append`. El argumento recibido puede ser de tipo `str`, `bytes`, `list` o `tuple`.

```python
texto.append('Soy una nueva línea')
texto.append(b'Soy una línea de bytes')
texto.append(('soy otra línea', 'y yo sigo despues'))
texto.append(['soy lo mismo de arriba', 'pero en forma de lista'])
```

En caso una línea no puedo decodificarse se mostrará como bytes y se guardará como tal. De todas formas se recomienda validar los datos y que la codificación sea correcta