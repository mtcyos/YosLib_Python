#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   YosMnu.py

   Yos Menú en entrono Txto

   Copyright (c) 2026 Miguel Tortosa

   Licenciado bajo la Licencia MIT.

   Consulte el archivo LICENCIA en la raíz del proyecto para más información.
"""

import platform
import sys
import os
import subprocess
import builtins

#import importlib
#import importlib.util

# Añado Directorio de YosLib
match platform.system():
    case "Windows":
        sys.path.append(os.path.abspath("..")+"\\Lib\\")
    case "Linux":
        sys.path.append(os.path.abspath("..")+os.path.abspath("/Lib/"))
#   case "Darwin": # macOS
#       sys.path.append(os.path.abspath("..")+os.path.abspath("/Lib/"))
    case _:
        print("YosCtr.36")
        print(f"Sistema Operativo {platform.system()} no implementado.")
        sys.exit(0)

# Nombre de la Aplicacion
builtins.Mem_Ini_AplCod = "YosMnu"                # ES el nombre REAL de la Aplicacion, NO LO CAMBIE, use cNom="Apl_Apl" en YosCfg.Dat
builtins.Mem_Ini_AplNom = "MENU DE APLICACIONES"  # ES el nombre REAL de la Aplicacion, NO LO CAMBIE, use cNom="Apl_Nom" en YosCfg.Dat
builtins.Mem_Ini_AplEtn = "Txt"                   # ES el entorno REAL de la Aplicacion, NO LO CAMBIE, Txt = prompt_toolkit

import inspect

import Yos

Yos.Yos_Cfg()
Yos.Yos_YosIni()

# --- 1. DEFINICIÓN DE YOSSES PARA YOSCTR (Sin NiceGUI) ---
# Creamos un contenedor simple para que YosSes cuelgue de aquí
class UserStorageProxy(dict):
    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)

# Inyectamos en builtins para que sea global en todo el árbol
builtins.YosSes = UserStorageProxy()

YosCfg["Dbg"]="" # MODO DEPURACION S="Completo" X=Para NiceGUI en local

#Idd_TabMst("YosCfg", "Mnu")

def main():
    # DEFINO EL MENU A USAR
#   Yos.FrmCab("Rot")
#    print(YosCfg["Apl_Mnu"])
#    print(f" def main() - {inspect.currentframe().f_lineno}")
    while True:
        MnuFnc = Yos.Mnu(YosCfg["Apl_Mnu"])
#        print(f"MnuFnc - {inspect.currentframe().f_lineno}")
#        input(f'MnuFnc={MnuFnc}')
        # CASOS ESPECIALES *********************************************************************************************
        if MnuFnc == "«AppSld»":  # CERRAR SESIÓN
            Yos.Apl_Fin_Txt(Fnc_Pgt="Si" )
            continue

        if MnuFnc == "«MnuCag»":  # Recargo El menu
            Yos.Yos_MnuRec(YosCfg["Apl_Apl"], "MnuGen")  # Menu General ("Nombre_de_la_Aplciacion" ,"MnuGen" lo guarda en YosCfg["Apl_Mnu"] , si no lo debuelve en return
            continue

        if MnuFnc[:7] == "«Cmd»":  # «Cmd» se pone ANTES del comando que queramos ejecutar
            MnuFnc = MnuFnc.replace("«Cmd»", "").strip()

            if not os.path.exists(MnuFnc):
                '''
                if builtins.Mem_Ini_AplEtn == "Txt":    # Entorno Txt
                    Yos.Yos_Msg_Tui(Fnc_Tit="ATENCION", Fnc_Msg=f'Aplicacion no encontrada : {MnuFnc}', Fnc_Tip="Ant")
                else:
                    Yos.Yos_Msg_Frm(Fnc_Tit=Mem_Tit, Fnc_Msg=f'Aplicacion no encontrada : {MnuFnc}', Fnc_Tip="Ant")
                '''
                ui.notify(f'Aplicacion no encontrada : {MnuFnc}', type='negative')
                print(f'Aplicacion no encontrada : {MnuFnc}')
                return

            print(f'{Yos.Yos_TimeStamp()} -> {YosSes["Usr_Ipd"]} - {YosSes["Usr_Nik"]} : EJECUTA {MnuFnc}')
            print(f'La aplicación {MnuFnc} se ejecutará en breve.')
            ui.notify(f'La aplicación {MnuFnc} se ejecutará en breve.', type='info')

            try:
                if platform.system() == "Windows":
                    os.startfile(MnuFnc)
                elif platform.system() == "Darwin":
                    subprocess.Popen(['open', MnuFnc])  # MacOs
                else:
                    subprocess.Popen(['xdg-open', MnuFnc])  # Linux

            except Exception as e:
                # Si el comando falla (ej: no existe word.exe), avisamos por consola
                print(f"Error al ejecutar comando externo: {e}")

            return  # Salimos para que no intente ejecutar el texto como función de Python

        if MnuFnc[:10] == "«CmdWit»":  # «CmdWit» se pone ANTES del comando que queramos ejecutar
            MnuFnc = MnuFnc.replace("«CmdWit»", "").strip()

            if not os.path.exists(MnuFnc):
#                ui.notify(f'Aplicacion no encontrada : {MnuFnc}', type='negative')
                print(f'Aplicacion no encontrada : {MnuFnc}')
                return

            print(f'{Yos.Yos_TimeStamp()} -> {YosSes["Usr_Ipd"]} - {YosSes["Usr_Nik"]} : EJECUTA {MnuFnc}')
            print(f'La aplicación {MnuFnc} se ejecutará en breve.')
#            ui.notify(f'La aplicación {MnuFnc} se ejecutará en breve.', type='info')#

#            await asyncio.sleep(0.1)

            try:
                if platform.system() == "Windows":
                    proceso = subprocess.Popen(MnuFnc, shell=True)
                    proceso.wait()
                elif platform.system() == "Darwin":
                    subprocess.run(['open', '-W', MnuFnc])
                else:  # Linux
                    subprocess.run([MnuFnc], shell=True)

                print('Su aplicación terminó')
                ui.notify('Proceso finalizado.', type='positive')

            except Exception as e:
                # Si el comando falla (ej: no existe word.exe), avisamos por consola
                print(f"Error al ejecutar comando externo: {e}")

            return  # Salimos para que no intente ejecutar el texto como función de Python
        # FIN CASOS ESPECIALES *********************************************************************************************

        # USO  de Yos_DefLib(), para def en Sql
        # Extraemos el nombre base para limpiar la memoria y buscar la función
        Mem_Fnc_Base = MnuFnc.split('(')[0].strip().split('.')[-1] # << MODIFICADO

        print(f'Mem_Yos_DefLib = {Mem_Fnc_Base} 171')

        # 1. FORZAR RECARGA: Borramos de la memoria builtins antes de cargar
        if hasattr(builtins, Mem_Fnc_Base):
            delattr(builtins, Mem_Fnc_Base)

        # 2. CARGA DINÁMICA: Llamamos a tu nueva función síncrona
        # Esta función ya inyecta en builtins y globals
        Yos.Yos_DefLib_Txt(MnuFnc) # << MODIFICADO

        # 3. RECUPERACIÓN: Buscamos la función recién inyectada
        func = getattr(builtins, Mem_Fnc_Base, None) or globals().get(Mem_Fnc_Base)

        YosSes["Apl_Def"] = Mem_Fnc_Base
        print(f'{Yos.Yos_TimeStamp()} -> {YosSes["Usr_Ipd"]} - {YosSes["Usr_Nik"]} : EJECUTA {YosSes["Apl_Def"]}')

        # 4. EJECUCIÓN ÚNICA (Síncrona por defecto para Txt)
        if callable(func):
            # Como es para Txt, asumimos ejecución normal sin await
            func()
        else:
            try:
                # Intento de ejecución directa si es una asignación o comando simple
                if "=" in MnuFnc:
                    exec(MnuFnc, globals())
                else:
                    eval(MnuFnc, globals())
            except Exception:
                # Si falla lo anterior, usamos el método tradicional
                exec(MnuFnc, globals())

        YosSes["Apl_Def"] = YosCfg["Apl_Apl"]

# FIN - Proceso del menu

if __name__ == '__main__':
    main()

