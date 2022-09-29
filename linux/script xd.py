from pystyle import Colorate, Colors
from modules.updatelib import updatelib
import sys
if sys.platform == "win32":
    import colorama
    colorama.init()
from colorama import Style, Fore
import argparse
def sprint(category, text, color):
    print(Colorate.Horizontal(color, "[{}] ".format(category)), end='')
    print(text)

parser = argparse.ArgumentParser(description="Administrador de paquetes thn22yt.blogspot.com")
parser.add_argument('-u', '--update', action='store_true', dest='upd_opt',
                    help="Chequea si hay actualizaciones y si lo hay, actualiza el script")
parser.add_argument('-i', '--install', action='store_true', dest='inst_opt',
                    help="Instala paquetes descargados desde mi pagina web")
parser.add_argument('-r', '--remove', action='store_true', dest='rm_opt',
                    help='Desinstala un paquete instalado')
parser.add_argument('-b', '--browse', action='store_true', dest='brow_opt',
                    help='Busca paquetes por su nombre')
objects = parser.parse_args()

if __name__ == "__main__":
    if objects.upd_opt:
        sprint("INFO", "Checando actualizaciones...", Colors.blue_to_red)
        updatelib
