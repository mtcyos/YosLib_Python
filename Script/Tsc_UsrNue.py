# -*- coding: utf-8 -*-
import os
import shutil
import subprocess
from pathlib import Path

def Tsc_UsrNue(usr=None, pas=None):
    Yos.Yos_Cls_Txt()
    Yos.FrmCab("Rot")

    if not usr:
        usr=input("Usuario    : ")

    if not usr :
        Yos.FrmWit("    Err : Usuario es obligatorio.")
        Yos.Yos_Cls_Txt()
        return

    if not pas:
        pas=input("contraseña : ")

    if not pas:
        Mem_Dat = Yos.Yos_MsgPgt_Txt(Fnc_Tit="ATENCION - USUARIO VACIO", Fnc_Msg="La Contraseña está vacía.\n\n ¿ Desea que generemos una?", Fnc_Bot="SÍ/NO")
        if Mem_Dat == "NO":
            Yos.Yos_Cls_Txt()
            return
        else:
            import random
            Mem_Dat = random.randint(1000, 9999)
            pas = f"{usr}{Mem_Dat:04d}"

    Yos.Yos_Cls_Txt()
    Yos.FrmCab("Rot")
    print()
    print("    *****************************************************")
    print("    *          CREANDO USUARIO DE ACCESO REMOTO         *")
    print("    *****************************************************")
    print(f"    * USUARIO    : {usr}")
    print(f"    * CONTRASEÑA : {pas}")

    try:
        print("    * CREANDO USUARIO.")
        subprocess.run(["net", "user", usr, pas, "/add"], check=True)

        print("    * CONFIGURANDO RESTRICCIONES DE CONTRASEÑA.")
        subprocess.run(["net", "user", usr, "/passwordchg:no"], check=True)
        subprocess.run(["powershell", "-Command", f"Set-LocalUser -Name '{usr}' -PasswordNeverExpires $true"], check=True)

        print("    * AÑADIENDOLO A GRUPO : Usuarios de escritorio remoto.")
        subprocess.run(["net", "localgroup", "Usuarios de escritorio remoto", usr, "/add"], check=True)

        print("    * AÑADIENDOLO A GRUPO : Administradores.")
        subprocess.run(["net", "localgroup", "Administradores", usr, "/add"], check=True)

        print(f"    * Usuario creado y asignado a grupos.")
    except subprocess.CalledProcessError as e:
        Yos.FrmWit(f"    Err : No se pudo crear el usuario {usr}.")
        Yos.Yos_Cls_Txt()
        return

    print()
    print("    *****************************************************")
    print("    *          CREANDO USUARIO DE ACCESO REMOTO         *")
    print("    *****************************************************")
    print()
    print("    * ACCEDA A ESTE USUARIO POR ACCESO REMOTO.")
    print("    * CUANDO ESTE EN EL ESCRITORIO REGRESE A AQUI.")

    print()
    input("PULSE INTRO PARA SEGUIR")
    print()
    print("    *****************************************************")
    print("    *          CREANDO USUARIO DE ACCESO REMOTO         *")
    print("    *****************************************************")
    print()
    print("    * ACCESO DESDE EL EXPLORADOR DE ARCHIVOS")
    print(rf"    * ACCEDA AL DIRECTORIO DEL USUARIO c:\Users\{usr}\ ")
    print("    * PARA QUE EL SISTEMA LE DE ACCESO")
    print()
    subprocess.Popen(['explorer', rf"C:\Users\{usr}"])
    input("PULSE INTRO PARA SEGUIR")
#    print("    * COPIANDO /Startup y /Desktop")

#    # 2. Definir rutas (usando tu estructura)
    path_usr_desktop = Path(f"C:/Users/{usr}/Desktop")
    path_startup = Path(f"C:/Users/{usr}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup")

    # 3. Esperar a que el perfil exista (bucle de espera)
    while not path_usr_desktop.exists():
        pass # Aquí podrías añadir un pequeño time.sleep(1)

    # 4. Copia de archivos (usando tu estructura de Dat)
    # Asumiendo que el script reside en YosCtr/_Script, subimos para llegar a Dat
#    source_startup = Path(__file__).resolve().parents[0] / "Tsc_UsrNue_Dat/Startup"
    source_desktop = Path(__file__).resolve().parents[0] / "Tsc_UsrNue_Dat/Desktop"
#    print(f'source_startup={source_startup}')
    print(f'source_desktop={source_desktop}')

    # Copiar Startup
#    if source_startup.exists():
#        for item in source_startup.iterdir():
#            if item.is_file():
#                # Definimos el destino exacto: carpeta destino + nombre del archivo
#                shutil.copy2(item, path_startup / item.name)
#                print(f"Copiado a Startup: {item.name}")

    # Copiar Desktop
    if source_desktop.exists():
        for item in source_desktop.iterdir():
            if item.is_file():
                shutil.copy2(item, path_usr_desktop / item.name)
                print(f"Copiado a Desktop: {item.name}")

    # eliminamos Boton derecho del mouse en el Boton de windows
    winx_path = os.path.expandvars(r"%LocalAppData%\Microsoft\Windows\WinX")

    # Creamos una carpeta de respaldo para no perder los enlaces
    backup_path = os.path.join(winx_path, "Backup")
    if not os.path.exists(backup_path):
        os.makedirs(backup_path)

    # Movemos los grupos de enlaces al backup
    for group in ["Group1", "Group2", "Group3"]:
        source = os.path.join(winx_path, group)
        if os.path.exists(source):
            shutil.move(source, os.path.join(backup_path, group))
            print(f"Deshabilitado: {group}")


    print()
    print("    *****************************************************")
    print("    *          CREANDO USUARIO DE ACCESO REMOTO         *")
    print("    *****************************************************")
    print()
    print("    * REALICE DESDE ACCESO REMOTO LAS SIGUIENTES TAREAS.")
    print()
    print("    1 - Ejecute Acceso_Red.bat del escritorio, para acceder a los servidores")
    print()
    print(f"    2 - crear la impresora PDF_{usr} EN PDF24")
    print("         MARCAR - Guardar los documentos automáticamente después de imprimirlos")
    print(r"         Directorio de destino : \\tsclient\C\_GesItg")
    print("         Nombre del archivo : $fileName")
    print("         TODO LO DEMAS DESACTIVADO")
    print("     3 - PONERLA COMO IMPRESORA PREDETERINADA")
    print("         Y QUITARLE EL ACCESO A TODOS LOS DEMAS")
    print()
    print("    5 - Quitar los iconos que sobran")
    print("    6 - Quitar del Menú de Inicio Todo lo que Sobra")
    print("    8 - Ocultar la Barra de Tareas")
    print()
    print("    * RECUERDE CERRAR LA SESION DEL ACCESO REMOTO")
    print()
    input("PULSE INTRO PARA SEGUIR")

    # 5. Limpieza final de privilegios
    print()
    print("    * QUITANDOLO A GRUPO : Administradores.")
    subprocess.run(["net", "localgroup", "Administradores", usr, "/delete"], check=True)

    print()
    print("Proceso finalizado con éxito.")
    input("PULSE INTRO PARA TERMINAR")

# Ejemplo de uso
# crear_usuario("alumno01", "Password123")
