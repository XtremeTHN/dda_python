import requests, sys, argparse, json, os
from pystyle import Colorate, Colors
from modules.updatelib import updatelib
def sprint(category,text, color, endx='\n'):
    print(Colorate.Horizontal(color, f'[{category}]'), end='')
    print(f' {text}', end=endx)

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
parser.add_argument('-i', '--install', choices=('locally', 'web'), dest='inst_opt',
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
    print(Colorate.Horizontal(Colors.cyan_to_green, "Gestor de paquetes dda"))
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
                from linux.functions import main
            elif sys.platform == 'win32':
                from windows.functions import main
            main(sprint,package,dat)
    if objects.start_opt:
        if sys.platform == 'linux':
            from linux.functions import start
        elif sys.platform == 'win32':
            from windows.functions import start
        start(objects.pkg, sprint)
