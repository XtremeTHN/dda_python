from pystyle import Colorate, Colors
from pathlib import Path
from zipfile import ZipFile
from platform import freedesktop_os_release as distro
import requests, json
import os
apps_fold = os.path.join(Path.home(),'.local','share','apps')
def main(sprint, package, dat):
    #Revisando si ya esta instalado el paquete, solo toma los datos del archivo de configuracion
    dirx = os.path.join(Path.home(), '.cache', 'dda')
    app_folder = open(os.path.join(dirx,package,'info.json'),'r')
    pack = json.load(open('modules/configs.json','r'))
    for x in pack['apps']:
        if x == package:
            sprint('WARN','Paquete ya instalado, se reinstalará',Colors.red_to_purple)
    sprint('INFO', 'Paquete encontrado...', Colors.blue_to_purple)
    sprint('INFO','Obteniendo el tamaño del archivo...',Colors.blue_to_purple,endx='')
    down = requests.get(dat['utilities'][package])
    size = float(down.headers['content-length'])/1048576
    print(' Tamaño= '+str(size)[0:5]+' MB')
    sprint('DOWN','Descargando...',Colors.blue_to_purple,endx='\r')
    with open('{}'.format(os.path.join(dirx, package + '_pkg_cache.dda')), 'wb') as file:
        file.write(down.content)
    sprint('SUCCESS', 'Descargado!', Colors.blue_to_purple)
    sprint('INFO', 'Revisando dependencias...', Colors.blue_to_purple)
    if not os.path.exists(dirx):
        os.mkdir(dirx)
    try:
        with ZipFile(os.path.join(dirx, package + '_pkg_cache.dda'), 'r') as zip:
            zip.extract(os.path.join(package, 'info.json'), dirx)
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
                                    os.system(f'pip install {b}')
                            if v == 'system':
                                for b in dependency['dependency'][v]:
                                    if b != 'null':
                                        if distro()['NAME'] == 'Arch Linux':
                                            os.system(f'sudo pacman -S {b}')
                                        elif distro()['NAME'] == 'Debian GNU/Linux':
                                            os.system(f'sudo apt-get install {b}')
                sprint('INFO', 'Descomprimiendo...', Colors.blue_to_purple)
                package_name = json.load(app_folder)['name']
                zip.extractall(os.path.join(apps_fold,'com.' + package_name))
            elif choice == 'N' or 'n':
                package_name = json.load(app_folder)['name']
                sprint('WARN', 'No instalar dependencias puede resultar a un error, obtendras las dependencias que necesitas si vuelves a ejecutar dda con "-pi" y especificando el paquete', Colors.red_to_blue)
                sprint('INFO', 'Descomprimiendo...', Colors.blue_to_purple)
                #zip.extractall(json.load(open(os.path.join(dirx,package,'info.json'), 'r'))['dest_linux'].replace('~', str(Path.home())))
                zip.extractall(os.path.join(apps_fold,'com.' + package_name))
                with open('modules/configs.json','r+') as file:
                    conf_dict = json.load(file)
                    conf_dict['apps'][package] = os.path.join(apps_fold,'com.' + package_name,package,'info.json')
                with open('modules/configs.json','w') as file:
                    conf = json.dump(conf_dict,file,indent=4)
                app_folder.close()
    except:
        raise IOError('Error en la creación del archivo')
    finally:
        os.remove(os.path.join(dirx, package + '_pkg_cache.dda'))

def start(pkg,sprint):
    confs = json.load(open(os.path.join('modules','configs.json')))
    ##temp_path = json.load(open(os.path.join(confs['apps'][])))
    if confs != {}:
        path_to_pkg = os.path
        for x in confs['apps']:
            if x == pkg:
                os.system(f"./{confs['apps'][x]}")
    else:
        sprint('ERR','No has instalado ningun paquete',Colors.blue_to_purple)

