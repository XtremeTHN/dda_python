import requests, sys, argparse, json, os
from modules.updatelib import updatelib
try:
    from pystyle import Colorate, Colors
    def sprint(category,text, color, endx='\n'):
        print(Colorate.Horizontal(color, f'[{category}]'), end='')
        print(f' {text}', end=endx)
except ImportError:
    print('Pystyle no instalado, se deshabilitaron los colores')
    def sprint(category,text,color,endx='\n'):
        print(f'[{category}] {text}', end=endx)
    class colors():
        def __init__(self):
            self.blue_to_red = 'R'
            self.blue_to_green = 'G'
            self.blue_to_purple = 'P'
            self.red_to_blue = 'B'
    Colors = colors()
if not os.path.exists('modules/configs.json'):
    with open('modules/configs.json','w') as file:
        json.dump({
            'autoupdate_repo':False,
            'work_dir':os.getcwd(),
            'apps':{}
            },file,indent=4)

parser = argparse.ArgumentParser(description="Algunos de los comandos aun no estan completos",epilog='Administrador de paquetes DDA (Descompresor de archivos) DDA Copyright (C) 2022 Axel')
parser.add_argument('-u', '--update', action='store_true', dest='upd_opt',
                    help="Chequea si hay actualizaciones y si lo hay, actualiza el script")
parser.add_argument('-i', '--install', choices=('local', 'web'), dest='inst_opt',
                    help="Instala paquetes descargados desde mi pagina web o localmente")
parser.add_argument('-s','--start',action='store_true', dest='start_opt',
                    help='Iniciar aplicaciones instaladas')
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
    sprint('Gestor de paquetes DDA','',Colors.blue_to_green)
    if objects.upd_opt:
        sprint("INFO", "Checando actualizaciones...", Colors.blue_to_red)
        new_ver = json.loads(updatelib.get_dict_of_files('https://raw.githubusercontent.com/XtremeTHN/dda_python/main/modules/repo-stable.json', quiet=True).decode("utf-8"))['version']
        if float(new_ver) >= 2:
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
    
    if objects.inst_opt == 'web':
        with open('modules/repo.json','r') as file:
            dat = json.load(file)
        sprint('DEBUG', dat['utilities'], Colors.blue_to_red)
        finded_package = False
        for x in dat['utilities']:
            if x != objects.pkg:
                next
            else:
                finded_package = True
                package = x
        if finded_package:
            if sys.platform == 'linux':
                from linux.functions import install_pkgweb
                from linux.functions import extractpkg
            elif sys.platform == 'win32':
                from windows.functions import install_pkgweb
                from windows.functions import extractpkg
            dirx, package2, pack, app_folder,zip_obj = install_pkgweb(sprint,objects.pkg,dat)
            extractpkg(dirx,package2,pack,app_folder,zip_obj,sprint)
    if objects.inst_opt == 'local':
        if os.path.exists(objects.pkg):
            from pathlib import Path
            sprint('INFO',f'Instalando {os.path.split(objects.pkg)[1]}...',Colors.blue_to_red)
            if sys.platform == 'linux':
                from linux.functions import extractpkg
                from linux.functions import install_pkglocal
            elif sys.platform == 'win32':
                from linux.functions import extractpkg
                from linux.functions import install_pkglocal
            dirx = os.path.join(Path.home(), '.cache', 'dda')
            zip_obj,pkg_name = install_pkglocal(objects.pkg,dirx)
            app_folder = open(os.path.join(dirx, pkg_name,'info.json'),'r')
            pack = json.load(open('modules/configs.json','r'))
            extractpkg(dirx,pkg_name,pack,app_folder,zip_obj,sprint)
        else:
            sprint('FATAL','Paquete no encontrado',Colors.red_to_blue)
            sys.exit(1)
    if objects.start_opt:
        if sys.platform == 'linux':
            from linux.functions import start
        elif sys.platform == 'win32':
            from windows.functions import start
        start(objects.pkg, sprint)
