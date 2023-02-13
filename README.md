# EasyTexto

![PyPI](https://img.shields.io/pypi/v/EasyTexto)
![PyPI - Downloads](https://img.shields.io/pypi/dm/EasyTexto)
![GitHub branch checks state](https://img.shields.io/github/checks-status/nakato156/EasyTexto/720e10ce3054f4e7ae3036c4412f332328851e1d)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/nakato156/EasyTexto)
![PyPI - License](https://img.shields.io/pypi/l/EasyTexto)

EasyTexto es un paquete que permite el manejo de archivos de texto de forma sencilla. Esta herramienta provee funciones para leer archivos así como para acceder, modificar y eliminar líneas específicas.

## instalacion

```
pip install EasyTexto
```

## Uso

### Accediendo a  líneas
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

### Modificando líneas
Tambien se permite el uso de slicing ya sea para obtener o modificar líneas

```python
print(texto[:3])
texto[::2] = 'holas'
print(texto) #mostrará una vista previa del archivo
```

### Eliminando líneas
Para eliminar líneas se provee el método `eliminar` de la clase `EasyTexto`, este método recibe un entero indicando el número de línea a eliminar o una tupla con los números de líneas a eliminar.

```python
texto.eliminar(1)
texto.eliminar((1, 2))
print(texto)
```

### Añadiendo líneas
Así como se puede eliminar líneas también se puede añadir líneas **al final** del archivo, esto gracias al método `append`. El argumento recibido puede ser de tipo `str`, `bytes`, `list` o `tuple`.

```python
texto.append('Soy una nueva línea')
texto.append(b'Soy una línea de bytes')
texto.append(('soy otra línea', 'y yo sigo despues'))
texto.append(['soy lo mismo de arriba', 'pero en forma de lista'])
```

En caso una línea no puedo decodificarse se mostrará como bytes y se guardará como tal. De todas formas se recomienda validar los datos y que la codificación sea correcta

## Archivo con formato de dialogo
Esta herramienta provee una forma de poder manejar archivos de texto que tenga una estructura de dialogo, por ejemplo:

**test.txt**
```txt
Uno:Primera línea
Uno: Otra linea
Uno: Pregunta
Dos: Cual es mejor, mayonesa de pollería o la normal?
Dos: Si-si-no
Uno:En cualquier caso depende de la preparación
```

Al tener un archivo de este y querer realizar más operaciones, puede indicar el parámetro `tipo='dialogo'`
Esto funciona para archivos con la estructura `<participante>: <dialogo>`

```python
from EasyTexto import EasyTexto
diialogo = EasyTexto('ruta_al_archivo.txt', tipo='dialogo')
```

Si intenta acceder o modificar líneas parecerá que no hay ningún cambio y es así. la diferencia radica en el uso de métodos `get_msg_by` y `get_msgs`. A continuación se explica el caso de uso de cada una


- `get_msg_by` se usa para recopilar todas las líeas que tengan cómo autor o participate al nombre que se le pasa a la función. Ejemplo:

```python
msgs = dialogo.get_msg_by('Uno') # retorna una lista con todas las líneas
print(msgs[0])
```

- `get_msgs` se usa para clasificar a cada participante del díalogo, esta función retorna un diccionario cuya llave corresponde al nombre del participante y como valor una lista con todas las intervenciones del participante. Ejemplo:

```python
msgs = dialogo.get_msgs()
print(msgs.keys())
```
## Archivos de dialogo con estructura diferente
Si su archivo posee una estructura diferente, es decir no tiene la estructura `<participante>: <dialogo>` puede proveer una función para la detección de las líneas.

Por ejemplo, si su archivo tiene la estructura `<participante> - <dialogo>` puede crear la siguiente función:

```python
def mi_funcion(linea: str) -> list:
    if '-' in linea:
        return linea.split('-', maxsplit=1)
    return False
```
La función debe retornar una lista con 2 elementos, el primero debe hacer referencia al participante y el segundo al diálogo, en caso contrario debe retornar `False`. 

Una vez implementada su función deberá pasarla al constructor de la clase en el parámetro `rule=su_funcion`.

```python
from EasyTexto import EasyTexto

def mi_funcion(linea: str) -> list:
    if '-' in linea:
        return linea.split('-', maxsplit=1)
    return False

diialogo = EasyTexto('ruta_al_archivo.txt', tipo='dialogo', rule=mi_funcion)
# hacer las operaciones que desee
```