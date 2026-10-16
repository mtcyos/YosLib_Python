#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Procesos de inicio de la Aplicacion

@author: Miguel Tortosa
"""

import os
import sys
import platform
import importlib.util
import builtins

def Yos_YosIni(**Fnc_Dic):
    # cTit : Inicio de YosLib
    # cDes : Inicio de YosLib
    # cPmt : Apl    -> Bombre del Archivo.
    #        Tip    -> Direccion del Archivo.

    import Yos
    Yos.Yos_MsgSis(Txt= "INICIALIZANDO Yos")

    ########################################################## Verificamos Mem_Apl+Mem_Tip en /cfg/YosApl.json (Aplicaciones del YosLib)

    Mem_Apl    = Fnc_Dic.get("Apl", "") # Aplicacion Inicial.
    Mem_Tip    = Fnc_Dic.get("Tip", "") # Tipo.

    if not Mem_Apl:
        Yos.Yos_MsgSis(Txt='Yos_YosIni(Apl="No puede estar Vacio", Tip="") AMBOS parametros con obligatorios.', Tip= "Err")
        sys.exit(0)

    if not Mem_Tip:
        Yos.Yos_MsgSis(Txt='Yos_YosIni(Apl="", Tip="No puede estar Vacio") AMBOS parametros con obligatorios.', Tip= "Err")
        sys.exit(0)

    # Recuperamos /cfg/YosApl.json
    Mem_YosApl = Yos.Yos_Cfg_Jsn(Ach="YosApl.json", Dir="Yos")
    # Verificamos si es un diccionario (éxito) o un string (error)
    if isinstance(Mem_YosApl, dict):
        pass
    else:
        Yos.Yos_MsgSis(Txt=f"(/cfg/YosApl.json) {Mem_YosApl}", Tip= "Err")
        sys.exit(0)

    Mem_Apl_2 = Mem_Apl +"_" +Mem_Tip
    # Acceso directo al diccionario de la aplicación
    if Mem_Apl_2 not in Mem_YosApl:
        Yos.Yos_MsgSis(Txt=f"Err: La aplicación {Mem_Apl_2} no existe en /cfg/YosApl.json.", Tip= "Err")
        sys.exit(0)
    ########################################################## FIN - Verificamos Mem_Apl+Mem_Tip en /cfg/YosApl.json (Aplicaciones del YosLib)

    Mem_AplDat = Mem_YosApl[Mem_Apl_2] # Recupero los datos

    builtins.Yos = Yos  # Mando la librería Yos al entorno de Python, NO TOCAR
    # Mando YosAplCfg y YosAplCfg_Def al entorno de Python, NO TOCAR
    builtins.YosAplCfg = {
        "Yos": {}, # Datos de la Libreria
        "Apl": {}  # Datos de la Aplicacion
    }
    builtins.YosAplCfg_Def = {
        "Yos": {},  # Datos de la Librería
        "Apl": {}   # Datos de la Aplicación
    }

    # DATOS DE LA APLICACION ORIGINAL, NO CAMBIAR
    YosAplCfg["Apl"]["Ori_Cod"] = Mem_Apl
    YosAplCfg["Apl"]["Ori_Nom"] = Mem_AplDat['cNom']
    YosAplCfg["Apl"]["Ori_Etn"] = Mem_AplDat['cTip']
    # FIN - DATOS DE LA APLICACION ORIGINAL, NO CAMBIAR

    Yos.Yos_Cfg()   # INICIALIZANDO Yos_Cfg

    # Definimos la ruta base de los scripts (donde cuelga el Main)
    script_path = os.path.join(os.getcwd(), 'Script')

    # Configurar sys.path según el sistema
    Mem_Tit = f'{YosAplCfg["Apl"]["Apl"]} - {YosAplCfg["Apl"]["Nom"]} - {YosAplCfg["Apl"]["Vsn"]}'
    match YosAplCfg["Apl"]["Sis_Etn"]:
        case "Windows":
            sys.path.append(script_path + "\\")
            # Obtener el handle de la ventana actual (CMD)
            import ctypes
            import time

            hwnd = ctypes.windll.kernel32.GetConsoleWindow()
            if hwnd:
                # Rotulo en el Cmd
                ctypes.windll.kernel32.SetConsoleTitleW(Mem_Tit)
                # 1. Intentar el método normal
                ctypes.windll.user32.ShowWindow(hwnd, 3)# Maximizar la pantalla

                # 2. Refuerzo: Simular Windows + Flecha Arriba
                time.sleep(0.1) # Pausa mínima para que el sistema reaccione
                ctypes.windll.user32.keybd_event(0x5B, 0, 0, 0) # Presiona Windows
                ctypes.windll.user32.keybd_event(0x26, 0, 2, 0) # Suelta Flecha Arriba
                ctypes.windll.user32.keybd_event(0x26, 0, 0, 0) # Presiona Flecha Arriba
                ctypes.windll.user32.keybd_event(0x5B, 0, 2, 0) # Suelta Windows

                # Bloquear el botón de cierre (X)
                # Primero obtenemos el menú del sistema de esa ventana
                hMenu = ctypes.windll.user32.GetSystemMenu(hwnd, False)
                if hMenu:
                    SC_MINIMIZE = 0xF020 # Boton Minimizar
                    SC_MAXIMIZE = 0xF030 # Bloquear Maximizar
                    SC_RESTORE  = 0xF120 # <--- Esta es la clave para que no se pueda achicar
                    SC_CLOSE = 0xF060 # Botón de cierre (X)
                    ctypes.windll.user32.DeleteMenu(hMenu, SC_MINIMIZE, 0x00000000) # Bloquear Minimizar
                    ctypes.windll.user32.DeleteMenu(hMenu, SC_MAXIMIZE, 0x00000000) # Bloquear Maximizar
                    ctypes.windll.user32.DeleteMenu(hMenu, SC_RESTORE, 0x0) # Bloquea el "volver a tamaño normal"
                    ctypes.windll.user32.DeleteMenu(hMenu, SC_CLOSE, 0x00000000)  # Bloquear el botón de cierre (X)

        case "Linux":
            sys.path.append(script_path + "/")
            os.system("echo -ne '\033]0;YosCtr - Linux\007'") # Cambiar título en Linux

        case "Darwin":  # MAC
            sys.path.append(script_path + "/")
            # En Mac se usa AppleScript o secuencias de escape para el título
            os.system("echo -n -e '\033]0;YosCtr - macOS\007'")

            try:
                # Intentamos maximizar, pero si falla, no rompemos el programa
                sys.stdout.write("\x1b[9;1t")
                sys.stdout.flush()
            except Exception:
                # Si falla, simplemente limpiamos pantalla y seguimos
                os.system("clear")

#       case "Darwin": # macOS
#           pass
#       case "iOS": # iOS or iPadOS
#           pass
        case _:
            print("Yos_Ini.Yos_YosIni()")
            print(f"Sistema Operativo {platform.system()} no implementado.")
            sys.exit(0)

    # Intentamos obtener el ancho de la terminal, por defecto 80
    if YosAplCfg["Apl"]["Sis_Etn"] == "Windows":
        # En Windows 11, la ventana se maximiza de forma asíncrona.
        # Esperamos a que la ventana termine de maximizarse y el buffer se actualice.
        import shutil
        last_width = 80
        last_height = 25

        # Esperamos hasta 10 iteraciones (0.5s en total) a que se estabilice el tamaño
        for _ in range(10):
            try:
                size = shutil.get_terminal_size()
                width, height = size.columns, size.lines
            except Exception:
                try:
                    size = os.get_terminal_size()
                    width, height = size.columns, size.lines
                except Exception:
                    width, height = 80, 25

            # Si el tamaño es mayor a 80 y coincide con el anterior, se ha maximizado y estabilizado correctamente
            if width > 80 and width == last_width and height == last_height:
                break

            # Si el tamaño sigue siendo 80 pero ya se estabilizó tras los primeros intentos, rompemos para no demorar
            if width == 80 and width == last_width and height == last_height:
                break

            last_width = width
            last_height = height
            time.sleep(0.05)

        YosAplCfg["Apl"]["Etn_Lon"] = last_width
        YosAplCfg["Apl"]["Etn_Alt"] = last_height
    else:
        # En Linux/macOS, la obtención del tamaño de terminal es directa
        try:
            import shutil
            size = shutil.get_terminal_size()
            YosAplCfg["Apl"]["Etn_Lon"] = size.columns
            YosAplCfg["Apl"]["Etn_Alt"] = size.lines
        except Exception:
            try:
                size = os.get_terminal_size()
                YosAplCfg["Apl"]["Etn_Lon"] = size.columns
                YosAplCfg["Apl"]["Etn_Alt"] = size.lines
            except Exception:
                YosAplCfg["Apl"]["Etn_Lon"] = 80
                YosAplCfg["Apl"]["Etn_Alt"] = 25

    # Definimos el Rotulo y la CABECERA
    Yos.Yos_Txt_Cab_CreRot()

    # Importo TODOS los .py de ./Script
    # 1. VALIDACIÓN INICIAL: ¿Existe la carpeta?
    if not os.path.exists(script_path):
        print(f"Error: No se encuentra la carpeta {script_path}")
        input("Pulse INTRO para salir...")
        sys.exit(0)

    # Bucle de carga inteligente
    Yos.Yos_MsgSis(Txt= "CARGADO Script.")
    app_name = os.path.basename(YosAplCfg["Apl"]["Dir"].rstrip("\\"))
#    Yos.Yos_MsgSis(Txt=f"{app_name}")
    for filename in os.listdir(script_path):

        if filename.endswith('.py'): #and '_' in filename:
            module_name = filename[:-3]
            spec = importlib.util.spec_from_file_location(module_name, os.path.join(script_path, filename))
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # 3. Creación/Recuperación del contenedor (YosCtr, YosGes, etc.)
                if not hasattr(builtins, app_name):
                    class AppContainer: pass
                    setattr(builtins, app_name, AppContainer())

                target_app = getattr(builtins, app_name)

                # 4. Registro de funciones (Solo las propias del archivo)
                for atributo in dir(module):
                    if not atributo.startswith("__"):
                        obj = getattr(module, atributo)
                        # Verificamos que sea ejecutable y que se haya definido EN ESTE archivo
                        if callable(obj) and getattr(obj, '__module__', None) == module_name:
                            setattr(target_app, atributo, obj)

                            Yos.Yos_MsgSis(Txt=f"   {app_name}.{atributo}()")

                            #YosAplCfg["Apl"]["Fnc"] += f"{app_name}.{atributo}()\n"
                            YosAplCfg["Apl"]["Fnc"].append(f"{app_name}.{atributo}()")
                # Le quito el ultimo \n
                #YosAplCfg["Apl"]["Fnc"] = YosAplCfg["Apl"]["Fnc"].rstrip("\n")

    # Nuevo formato para llamar los def
    # Archivo físico /Script | Función dentro del .py | Llamada desde Main.py
    # Directorio del programa :  YosCtr
    # Abv.py           | def Abv_VfyDat():      | YosCtr.Abv_VfyDat()
    # Abv.py           | def Abv_Save():        | YosCtr.Abv_Save()
    # Clm.py           | def Clm_Calculo():     | YosDfp.Clm_Calculo()

    # FIN Importo TODOS los .py de ./Script

    # ATENCION ESTO NO PUEDE EXISTIR YosCtr_Abv.py def Ipt(): y YosCtr_Clm.py def Ipt(): los del tienen que tener el prefijo de la aplicacion Abv_Ipt() y Clm_Ipt()
    Yos.Yos_DefLib_Full()

    # Recupero la Ip del Equipo Si es Tui
#    if Mem_Ini_AplEtn == "Tui":
#        YosSes["Usr_Ipd"] = "LocalHost"

    Yos.Yos_MsgSis(Txt= "IMPORTANDO LAS UTILIDADES YOS")
    Yos.Yos_IptAplUtl()
    Yos.Yos_MsgSis(Txt= "IMPORTADAS UTILIDADES YOS")
    Yos.Yos_MsgSis(Txt= "INICIALIZADA Yos")

    Yos.FrmWit(Fnc_Wit=3)

def Yos_MnuRec(Fnc_Mnu, Fnc_Tipo= ""):
    import Yos
    # Recupero el Menu desde YosAplCfg["Apl"]["Mnu"]
    if not Fnc_Mnu:
        Fnc_Mnu = "MnuGen"

    if Fnc_Mnu == "YosMnuEtn":
        Mem_Cnx = Yos.Idd_BdtSvr_Cnx("YosLib")  # YosMnuEtn esta en YosLib.mnu
    else:
        Mem_Cnx = Yos.Idd_BdtSvr_Cnx("YosCfg")

    Mem_Cur = Mem_Cnx.cursor()

    Mem_Sql = """
        SELECT * FROM Mnu
        WHERE cMnu = ?
            AND (cNul IS NULL OR cNul <> 'S')               -- 1. Salta los anulados
            AND (cEtn = ? OR cEtn = '' OR cEtn IS NULL)     -- 2. Filtra por Win, Linux o Mac
        ORDER BY cMnu, cNumOrd ASC;
    """
#    print(Mem_Sql)
#    print(Fnc_Mnu)
#    print(YosAplCfg["Apl"]["Sis_Etn"])
    Mem_Dat = Yos.SelTot(Mem_Cur, Mem_Sql, pParams=(Fnc_Mnu, YosAplCfg["Apl"]["Ori_Etn"]))
    if not Mem_Dat:

        import traceback
        # Obtiene la pila de llamadas actual
        stack = traceback.extract_stack()

        # El penúltimo elemento de la pila corresponde al contexto anterior (el llamante)
        # (el último elemento es la propia línea actual)
        if len(stack) > 1:
            caller_frame = stack[-2]
            print(f"Llamado desde el archivo: {caller_frame.filename}, línea: {caller_frame.lineno}, función/bloque: {caller_frame.name}")


        Yos.Yos_MsgSis(Txt=f"NO EXISTEN DATOS DE Mnu.{Fnc_Mnu} en ./Bdt/YosCfg.Bdt.", Tip= "Err")
        if Fnc_Mnu == "MnuGen":
            Yos.Yos_MsgSis(Txt= "Asegúrese que el menú principal se llama MnuGen en ./Bdt/YosCfg.Bdt.", Tip= "Err")
        input("PULSE INTRO PARA CONTINUAR")
        sys.exit(1)

    # Construimos el diccionario con cNum como clave para mantener orden
    Mem_Dic_Tmp = {}

    # 2. La 'Pila' nos indica en qué nivel estamos trabajando
    # Empezamos en la raíz [Mem_Dic_Tmp]
    Pila = [Mem_Dic_Tmp]

    for row in Mem_Dat:
        # Ignorar si está anulado (aunque ya venga filtrado por SQL)
        if row["cNul"] == "S":
            continue

        # Extraemos datos básicos
        cOrd = str(row["cNumOrd"])
        cCod = row["cMnuCod"]
        cDes = row["cDes"] if row["cDes"] else ""
        cFnc = row["cFnc"] if row["cFnc"] else ""

        # A. INICIO DE NIVEL (Submenú)
        if cCod == "IniPop":
            # Creamos el nodo con su propio diccionario 'Sub'
            Nuevo_Sub = {"Txt": cDes, "Sub": {}}
            # Lo colgamos en el nivel actual de la pila
            Pila[-1][cOrd] = Nuevo_Sub
            # 'Entramos' en este nuevo diccionario para los siguientes registros
            Pila.append(Nuevo_Sub["Sub"])

        # B. FIN DE NIVEL (Cierre de submenú)
        elif cCod == "EndPop":
            if len(Pila) > 1:
                Pila.pop() # Volvemos al nivel anterior

        # C. SEPARADOR
        elif cCod == "Sep":
            Pila[-1][cOrd] = {"Txt": cDes, "Fnc": "", "Cod": cCod}

        # D. ITEM NORMAL O INYECCIÓN DE OTRO MENÚ
        else:
            if cCod == "MnuSub":
                # RECURSIVIDAD: Buscamos el submenú (ej: 'YosMnuEtn')
                Sub_Dic_Inyectado = Yos_MnuRec(Fnc_Mnu=cFnc, Fnc_Tipo= "SubApp")

                # REGLA DE ORO: Si hay Texto en la celda 'TEXTO MENU'
                # lo convertimos en un grupo desplegable (PopUp)
                if cDes:
                    # Creamos el nivel "Padre" y le colgamos lo inyectado
                    Nuevo_Sub = {"Txt": cDes, "Sub": Sub_Dic_Inyectado}
                    Pila[-1][cOrd] = Nuevo_Sub
                elif cCod == "Sep":
                    Pila[-1][cOrd] = {"Txt": "", "Fnc": "", "Cod": cCod}
                else:
                    # Si no hay texto (como lo tienes ahora), se mezcla con la raíz
                    Pila[-1].update(Sub_Dic_Inyectado)
            else:
                # Item normal
                Pila[-1][cOrd] = {
                    "Txt": cDes,
                    "Fnc": cFnc,
                    "Cod": cCod
                }

    # Al finalizar el bucle, Mem_Dic_Tmp contiene todo el árbol jerárquico.

    Yos.Cie(Mem_Cnx)
    if Fnc_Tipo == "MnuGen":
        YosAplCfg["Apl"]["Mnu"] = Mem_Dic_Tmp
    else:
        return Mem_Dic_Tmp
