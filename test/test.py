from pathlib import Path
import pytest
import sys

sys.path.append('../EasyTexto')
from EasyTexto.linea import Linea
from EasyTexto import EasyTexto

path_txt = Path(__file__).parent
filename = 'test.txt'
texto = EasyTexto(path_txt / filename)

#test de archivo normal
def test_get_first_line():
    assert texto[1] == 'Uno:Primera línea'

def test_get_last_line():
    print(texto[-1])
    assert texto[-1] == 'Uno:   Ya dije que depende, pero diré que si ya que es lo que aveces más consumo'

def test_replace_line():
    nueva_linea = '1:Soy el reemplazo de la línea #1'
    vieja_linea:Linea = texto[1]
    
    texto[1] = nueva_linea
    cambio = texto[1]
    texto[1] = vieja_linea.texto.strip()
    assert cambio == nueva_linea

texto = EasyTexto(path_txt / filename, tipo="dialogo")

# test de archivo tipo dialogo
def test_forma_dialogo():
    msgs = texto.get_msg_by('Uno')
    assert len(msgs) == 7

def test_get_msg_by():
    msgs = texto.get_msg_by('Uno')
    assert msgs[0] == 'Primera línea\n'

def test_get_all_msg():
    msgs = texto.get_msgs()
    assert sorted(list(msgs.keys())) == ['Dos', 'Uno']

def test_count_all_msg():
    msgs = texto.get_msgs()
    assert len(msgs['Uno']) == 7
    assert len(msgs['Dos']) == 6
