import requests
from pystyle import Colorate, Colors
from modules.updatelib import updatelib
import argparse, json
def sprint(category,text, color):
    print(Colorate.Horizontal(color, f'[{category}]'), end='')
    print(f' {text}')

parser = argparse.ArgumentParser(description="Administrador de paquetes thn22yt.blogspot.com")
parser.add_argument('-u', '--update', action='store_true', dest='upd_opt',
                    help="Chequea si hay actualizaciones y si lo hay, actualiza el script")
parser.add_argument('-i', '--install', action='store_true', dest='inst_opt',
                    help="Instala paquetes descargados desde mi pagina web")
parser.add_argument('-r', '--remove', action='store_true', dest='rm_opt',
                    help='Desinstala un paquete instalado')
parser.add_argument('-b', '--browse', action='store_true', dest='brow_opt',
                    help='Busca paquetes por su nombre')
parser.add_argument('-tb','--trouble-shoting', action='store_true',dest='tb',
                    help='Intenta varios metodos para solucionar errores')

if __name__ == "__main__":
    objects = parser.parse_args()
    if objects.upd_opt:
        sprint("INFO", "Checando actualizaciones...", Colors.blue_to_red)
        new_ver = json.loads(updatelib.get_dict_of_files('https://raw.githubusercontent.com/XtremeTHN/dda_python/main/modules/repo-stable.json', quiet=True).decode("utf-8"))['version']
        if float(new_ver) >= 0:
            sprint("INFO", "Actualizacion disponible", Colors.blue_to_red)
            sprint("UPDATE", "Descargando...", Colors.blue_to_green)
            with open('modules/repo-stable.json','r') as file:
                data = json.load(file)
            for x in data:
                file_data = requests.get(data[x])
                if x != 'dda.py':
                    with open(x, 'wb') as f:
                        f.write(file_data.content)
            sprint("SUCCESS", "Actualización hecha", Colors.blue_to_purple)