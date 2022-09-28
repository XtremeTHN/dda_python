from pystyle import Colorate, Colors
from modules.updatelib import *
import argparse
def sprint(text, color):
    print(Colorate.Horizontal(color, text))

parser = argparse.ArgumentParser(description="Administrador de paquetes thn22yt.blogspot.com")
parser.add_argument('-u', '--update', action='store_true', dest='upd_opt',
                    help="Chequea si hay actualizaciones y si lo hay, actualiza el script")
parser.add_argument('-i', '--install', action='store_true', dest='inst_opt',
                    help="Instala paquetes descargados desde mi pagina web")
parser.add_argument('-r', '--remove', action='store_true', dest='rm_opt',
                    help='Desinstala un paquete instalado')
parser.add_argument('-b', '--browse', action='store_true', dest='brow_opt',
                    help='Busca paquetes por su nombre')

if __name__ == "__main__":
    