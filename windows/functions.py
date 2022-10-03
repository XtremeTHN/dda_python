from pystyle import Colorate, Colors
from pathlib import Path
from zipfile import ZipFile
import requests, json
import os
def main(sprint, package, dat):
    sprint('INFO', 'Paquete encontrado...', Colors.blue_to_purple)
    sprint('DOWN', 'Obteniendo el tamaño del archivo...', Colors.blue_to_green)
    resp = requests.get(dat['utilities'][package])
    size = float(resp.headers['content-length'])/1048576
    sprint('DOWN', 'Tamaño= '+str(size)[0:5]+' MB', Colors.blue_to_green)
    sprint('DOWN', 'Descargando...', Colors.blue_to_green)
    down = requests.get(dat['utilities'][package])
    sprint('SUCCESS', 'Descargado!', Colors.blue_to_purple)
    dirx = os.path.join(Path.home(), '.cache', 'dda')
    sprint('INFO', 'Revisando dependencias...', Colors.blue_to_purple)
    if not os.path.exists(dirx):
        os.mkdir(dirx)
    try:
        with open('{}'.format(os.path.join(dirx, package + '_pkg_cache.dda')), 'wb') as file:
            file.write(down.content)
        with ZipFile(os.path.join(dirx, package + '_pkg_cache.dda'), 'r') as zip:
            zip.extract('mrw10/info.json', dirx)
            sprint('INFO', 'Deseas instalar las dependencias? (Y/N): ', Colors.blue_to_purple, endx='')
            choice = input()
            if choice == 'Y':
                sprint('WARN', 'Si se muestra un error al intentar descargar las dependencias, deberias instalarlas manualmente', Colors.blue_to_red)
                with open(os.path.join(dirx,package,'info.json'), 'r') as file:
                    dependency = json.load(file)
                    if dependency['dependency'] == 'null':
                        sprint('INFO', 'No hay dependencias', Colors.blue_to_purple)  
                    else:
                        for v in dependency['dependency']:
                            if v == 'pip':
                                for b in dependency['dependency'][v]:
                                    print(f'pip install {b}')
                            if v == 'system':
                                for b in dependency['dependency'][v]:
                                    print(f'sudo dnf install {b}')           
            elif choice == 'N' or 'n':
                sprint('WARN', 'No instalar dependencias puede resultar a un error, obtendras las dependencias que necesitas si vuelves a ejecutar dda con "-pi" y especificando el paquete', Colors.red_to_blue)
                sprint('INFO', 'Descomprimiendo...', Colors.blue_to_purple)
                zip.extractall(json.load(open(os.path.join(dirx,package,'info.json'), 'r'))['dest_linux'].replace('~', str(Path.home())))
    except:
        raise IOError('Error en la creación del archivo')
    finally:
        os.remove(os.path.join(dirx, package + '_pkg_cache.dda'))
