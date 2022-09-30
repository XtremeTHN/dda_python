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
parser.add_argument('-i', '--install', choices=('locally', 'web'), dest='inst_opt',
                    help="Instala paquetes descargados desde mi pagina web o localmente")
parser.add_argument('-a', '--append', action='store', dest='pkg', default='nil',
                    help="No utilizar a menos que se use con --install, Ejemplo: 'dda --install web -a mw10'")
parser.add_argument('-r', '--remove', action='store_true', dest='rm_opt',
                    help='Desinstala un paquete instalado')
parser.add_argument('-b', '--browse', action='store_true', dest='brow_opt',
                    help='Busca paquetes por su nombre')
parser.add_argument('-tb','--trouble-shoting', action='store_true',dest='tb',
                    help='Intenta varios metodos para solucionar errores')

if __name__ == "__main__":
    objects = parser.parse_args()
    print(Colorate.Horizontal(Colors.cyan_to_green, "Gestor de paquetes dda"))
    if objects.upd_opt:
        sprint("INFO", "Checando actualizaciones...", Colors.blue_to_red)
        new_ver = json.loads(updatelib.get_dict_of_files('https://raw.githubusercontent.com/XtremeTHN/dda_python/main/modules/repo-stable.json', quiet=True).decode("utf-8"))['version']
        if float(new_ver) >= 1:
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
    from pathlib import Path
    from zipfile import ZipFile
    import os
    if objects.inst_opt == 'web':
        with open('modules/repo.json','r') as file:
            dat = json.load(file)
        sprint('DEBUG', dat['utilities'], Colors.blue_to_red)
        for x in dat['utilities']:
            if x != objects.pkg:
                sprint('ERROR', 'El paquete que usted solicitó no se encontró, revise si lo ha escrito correctamente')
            else:
                sprint('INFO', 'Paquete encontrado...', Colors.blue_to_purple)
                sprint('DOWN', 'Obteniendo el tamaño del archivo...', Colors.blue_to_green)
                resp = requests.get(dat['utilities'][x])
                size = float(resp.headers['content-length'])/1048576
                sprint('DOWN', 'Tamaño= '+str(size)[0:5]+' MB', Colors.blue_to_green)
                sprint('DOWN', 'Descargando...', Colors.blue_to_green)
                down = requests.get(dat['utilities'][x])
                sprint('SUCCESS', 'Descargado!', Colors.blue_to_purple)
                dirx = os.path.join(Path.home(), '.cache', 'dda')
                if not os.path.exists(dirx):
                    os.mkdir(dirx)
                try:
                    with open('{}'.format(os.path.join(dirx, x + '_pkg_cache.dda')), 'wb') as file:
                        file.write(down.content)
                    with ZipFile(os.path.join(dirx, x + '_pkg_cache.dda'), 'r') as zip:
                        sprint('INFO', 'Descomprimiendo...', Colors.blue_to_purple)
                        zip.extract('info.json', dirx)
                        zip.extractall(json.load(open(os.path.join(dirx,'info.json'), 'r'))['dest_linux'].replace('~', Path.home()))
                except:
                    raise IOError('Error en la creación del archivo')
                finally:
                    os.remove(os.path.join(dirx, x + '_pkg_cache.dda'))
                sprint('INFO', 'Revisando dependencias...', Colors.blue_to_purple)


