#!/usr/bin/env python3
# -*- coding: utf-8 -*
"""
   YosLib.py

   LIBRERIA DE PROPOSITO GENERAL>

   Copyright (c) 2026 Miguel Tortosa

   Licenciado bajo la Licencia MIT.

   Consulte el archivo LICENCIA en la raíz del proyecto para más información.
"""

import os
import sys
import inspect
import shutil
import builtins
import asyncio

#import Yos

###################################################################################  Inicio Def ###################################################################################
# ******************************************************************************************************************************************* Yos_AplEntVfy()
def Yos_AplEntVfy():
    # Verifico en Entorno de la Aplicacion

    Mem_Err = ""

    if YosAplCfg["Apl"]["Ori_Etn"] == "Gui" and YosAplCfg["Apl"]["Etn"] not in ("Loc", "Www"):
        Mem_Err = "Err"

    if YosAplCfg["Apl"]["Ori_Etn"] == "Tui" and YosAplCfg["Apl"]["Etn"] in ("Loc", "Www"):
        Mem_Err = "Err"

    if Mem_Err:
        Yos.Apl_UsrAcc_UsrEliDat(Fnc_Cmd= "SinUsr")
        YosSes['Usr_Ipd'] = "127.0.0.1".ljust(15)

        print()
        ruta_completa = os.path.basename(YosAplCfg["Apl"]["Dir"].rstrip("\\"))
        nombre_app = os.path.basename(ruta_completa)

        Yos.Yos_MsgSis(Txt= "******** ATENCION ********", Tip= "Err")
        Yos.Yos_MsgSis(Txt=f"APLICACION : {nombre_app} es de entorno {YosAplCfg["Apl"]["Ori_Etn"]}.", Tip= "Err")
        Yos.Yos_MsgSis(Txt=f"Entorno [{YosAplCfg['Apl'].get('Etn')}] no soportado.", Tip= "Err")
        print()
        Yos.FrmWit(Fnc_Wit=8)
        print()
        Yos.Apl_Fin_Txt(Pgt= "No", SisMsg= "No")

#        return
# ******************************************************************************************************************************************* FIN - Yos_AplEntVfy()
# ******************************************************************************************************************************************* Yos_DefLib_Full
def Yos_DefLib_Full():
    # Carga TODA la tabla de definiciones de la SQLite a la memoria (builtins)
    import builtins
#    import Yos

    Yos.Yos_MsgSis(Txt= "INICIALIZANDO Librería Dinámica de Funciones.")

    # 1. Conexión usando tus funciones estándar
    Mem_Cnx = Yos.Idd_BdtSvr_Cnx("YosLib")
    Mem_Cur = Mem_Cnx.cursor()

    # 2. Seleccionamos el nombre de la función (cFnc) y su código (cCmd)
    # He añadido un filtro para evitar cargar cosas vacías
    Mem_Sql = "SELECT cFnc, cCmd FROM FncDef WHERE cCmd IS NOT NULL"
    Mem_Dat_Lista = Yos.SelTot(Mem_Cur, Mem_Sql, pParams=())
    Yos.Cie(Mem_Cnx)

    if not Mem_Dat_Lista:
        print("    [ATENCION] No se encontraron definiciones para cargar.")
        return False

    # 3. Bucle de Inyección
    for Fnc_Nom, Fnc_Cod in Mem_Dat_Lista:
        try:
            # Limpieza de caracteres (tu lógica de limpieza)
            Mem_Cmd = str(Fnc_Cod).replace('\r\n', '\n').replace('\r', '\n').replace('\xa0', ' ')

            # Inyectamos en el espacio global
            exec(Mem_Cmd, globals())

            # Buscamos la función recién inyectada
            func_inyectada = globals().get(Fnc_Nom)

            if callable(func_inyectada):
                # La subimos a builtins para que sea universal
                setattr(builtins, Fnc_Nom, func_inyectada)
                # print(f"    [OK] Inyectada: {Fnc_Nom}") # Opcional para debug

        except Exception as e:
            print(f"    [ERROR] Fallo al inyectar {Fnc_Nom}: {e}")

    Yos.Yos_MsgSis(Txt= "INICIALIZADA Librería Dinámica de Funciones.")
    return True
# ******************************************************************************************************************************************* FIN - Yos_DefLib_Full
# ******************************************************************************************************************************************* Yos_DefFncHlp
import os
import sqlite3
import re
import Yos  # Tu biblioteca central
import asyncio

async def Yos_DefFncHlp(**Fnc_Dic):
    # cTit : Define y actualiza el manual digital de las Funciones
    # cDes : Lee cada .py que exista en el Directorio dado y documenta todas sus def.
    #        El directorio a inspeccionar, bebe estar dentro del entorno Yos.
    #        Las subdef las marca como cNul= "S" para luego no imprimirlas, pero quedan como documentación.
    #        Yos_DefFncHlp(Dir= "Directorio")   # Guarda en ./Doc/«Apl_Apl»_Def.Bdt
    #        Yos.Yos_DefFncHlp(Dir= "Yos")   # La libreria Yos, lo guarda en .Yos/Doc/YosDoc_YosMnlPth_Def.Bdt
    # cPmt : Dir -> Directorio a inspeccionar.

    Mem_Tit = "Yos_DefFncHlp() - Generacion del Manual Digital"
    Mem_Txt = ""

    Mem_Dir = Fnc_Dic.get("Dir", "Yos").strip()

    # Encontramos la raíz del proyecto Python para movernos con seguridad por el árbol
    Mem_DirIni = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
#   Mem_DirIni = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
#   Mem_DirIni = YosAplCfg["Apl"]["Dir"]

    print(f'Mem_DirIni={Mem_DirIni}')

    # 1. BIFURCACIÓN ESTRICTA SEGÚN TU REGLA DE NEGOCIO
    if Mem_Dir == "Yos":
        dir_inspeccionar = YosAplCfg["Yos"]["Dir"]
        ruta_bdt         = os.path.join(dir_inspeccionar, "Doc", "YosDoc_YosMnlPth_Def.Bdt")
        Men_Txtfin = "Bdt Actualizada : ./Yos/Doc/YosDoc_YosMnlPth_Def.Bdt"

    else:
        dir_inspeccionar = os.path.join(Mem_DirIni, Mem_Dir, "Script")
        ruta_bdt         = os.path.join(Mem_DirIni, Mem_Dir, "Doc", YosAplCfg["Apl"]["Apl"]+"_Def.Bdt")
        Men_Txtfin = "Bdt Actualizada : ./Doc/"+YosAplCfg["Apl"]["Apl"]+"_Def.Bdt"

    print(f'dir_inspeccionar={dir_inspeccionar} ruta_bdt={ruta_bdt}')

    if not os.path.exists(dir_inspeccionar):
        print(f"[-] Error: No existe el directorio de scripts en: {dir_inspeccionar}")
        return

    Mem_Txt += f'Iniciando análisis de : {dir_inspeccionar}\n'

    os.makedirs(os.path.dirname(ruta_bdt), exist_ok=True)

    timestamp = Yos.Yos_TimeStamp()
    nick_sistema = "Yos"

    # 2. CONEXIÓN Y CREACIÓN DE TABLA EN LA RUTA CALCULADA
    conn = sqlite3.connect(ruta_bdt)
    conn.execute("PRAGMA journal_mode=WAL;")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Fnc (
            NumReg INTEGER PRIMARY KEY AUTOINCREMENT,
            cNul VARCHAR(1),
            cFun VARCHAR(100),
            cTit VARCHAR(255),
            cDes TEXT,
            cPmt TEXT,
            cObs TEXT,
            cOri VARCHAR(100),
            cEst VARCHAR(3),
            cModRegNik VARCHAR(20),
            cModRegTim VARCHAR(20),
            UNIQUE (cOri, cFun)
        );
    ''')

    conn.commit()

    # 3. EL DEVORADOR FÍSICO (Solo primer nivel de carpeta)
    for raiz, directorios, archivos in os.walk(dir_inspeccionar):
        directorios.clear() # Corta la recursividad para respetar tu estructura estricta

        for archivo in archivos:
            if archivo.endswith(".py") and not archivo.startswith("__"):
                ruta_completa = os.path.join(raiz, archivo)

                # Marcado preventivo por archivo físico local usando LIKE
                cursor.execute("UPDATE Fnc SET cEst = 'Eli' WHERE cOri LIKE ?", (f"{archivo}%",))

                try:
                    with open(ruta_completa, "r", encoding= "utf-8") as f:
                        lineas = f.readlines()
                except Exception:
                    continue

                i = 0
                total_lineas = len(lineas)

                # ESCANEO INTELIGENTE DE LÍNEAS (Filtrado por marcas fijas '# cXXX :')
                while i < total_lineas:
                    linea_real = lineas[i]
                    linea_limpia = linea_real.strip()

                    # --- PROCESAMIENTO DE DETECCIÓN "DEF" ---
                    if linea_limpia.startswith("def "):
                        match = re.match(r"def\s+(\w+)\s*\((.*)\)\s*:", linea_limpia)

                        if match:
                            cFun = match.group(1)
                            cPmt_Firma = match.group(2).strip()
                            cOri_ConLinea = f"{archivo} ({i + 1:05d})" # Tus 5 ceros blindados para el manual

                            # Listas contenedoras para acumular texto multilínea de forma dinámica
                            ext_cTit = ""
                            ext_cDes = []
                            ext_cPmt = []

                            # Puntero explorador para revisar las líneas de comentario debajo del 'def'
                            j = i + 1
                            tag_actual = None # Registra qué campo está activo para recibir líneas continuas

                            while j < total_lineas:
                                linea_original = lineas[j]
                                sub_linea_limpia = linea_original.strip()

                                # Si la línea no empieza con '#', el bloque de documentación terminó por completo
                                if not sub_linea_limpia.startswith("#"):
                                    break

                                # Extraemos el contenido quitando el primer carácter '#' de la línea original
                                # Buscamos la posición del '#' para cortar justo después de él y no perder el formato
                                pos_hash = linea_original.find("#")
                                contenido_bloque = linea_original[pos_hash + 1:]
                                contenido_limpio = contenido_bloque.strip()

                                # REGLA DE DETECCIÓN: Evaluamos las etiquetas fijas de inicio usando la cadena limpia
                                if contenido_limpio.startswith("cTit :"):
                                    ext_cTit = contenido_limpio[6:].strip()
                                    tag_actual = "cTit"

                                elif contenido_limpio.startswith("cDes :"):
                                    # Para la primera línea, quitamos la etiqueta y limpiamos los extremos
                                    ext_cDes.append(contenido_limpio[6:].strip())
                                    tag_actual = "cDes"

                                elif contenido_limpio.startswith("cPmt :"):
                                    ext_cPmt.append(contenido_limpio[6:].strip())
                                    tag_actual = "cPmt"

                                else:
                                    # MULTILÍNEA PURA: Si es una línea de continuación, limpiamos solo el exceso de la izquierda
                                    # Pero OJO: le quitamos el '\n' final temporalmente para que no se dupliquen los saltos al consolidar
                                    linea_sin_salto = contenido_bloque.rstrip("\r\n")
                                    texto_final = linea_sin_salto.strip()

                                    if texto_final:
                                        if tag_actual == "cDes":
                                            ext_cDes.append(texto_final)
                                        elif tag_actual == "cPmt":
                                            ext_cPmt.append(texto_final)

                                j += 1

                            # Consolidamos uniendo estrictamente por salto de línea real (\n)
                            final_cTit = ext_cTit if ext_cTit else f"Función {cFun}"
                            final_cDes = "\n".join(ext_cDes) if ext_cDes else "Pendiente de ampliar documentación..."
                            final_cPmt = "\n\n".join(ext_cPmt) if ext_cPmt else cPmt_Firma

                            # Regla automática de visibilidad y subfunciones
                            cNul_Inicial = ""
                            if not linea_real.startswith("def "):  # Subfunción (identada)
                                cNul_Inicial = "S"
                            elif cFun.startswith("_"):           # Función interna/privada
                                cNul_Inicial = "S"

                            # Inyección o actualización en SQLite
                            cursor.execute("SELECT NumReg FROM Fnc WHERE cOri LIKE ? AND cFun = ?", (f"{archivo}%", cFun))
                            reg_previo = cursor.fetchone()

                            if reg_previo:
                                cursor.execute('''
                                    UPDATE Fnc
                                    SET cTit = ?, cDes = ?, cPmt = ?, cEst = '', cOri = ?, cModRegTim = ?, cModRegNik = ?
                                    WHERE NumReg = ?
                                ''', (final_cTit, final_cDes, final_cPmt, cOri_ConLinea, timestamp, nick_sistema, reg_previo[0]))
                            else:
                                cursor.execute('''
                                    INSERT INTO Fnc (cNul, cFun, cTit, cDes, cPmt, cObs, cOri, cEst, cModRegNik, cModRegTim)
                                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                ''', (cNul_Inicial, cFun, final_cTit, final_cDes, final_cPmt, "", cOri_ConLinea, "Nue", nick_sistema, timestamp))

                            # Avanzamos el índice del bucle principal hasta donde llegó el puntero explorador
                            i = j - 1

                    i += 1

    # 4. FASE VIRTUAL: INYECCIÓN DIRECTA DESDE TU TABLA REAL FncDef
    if Mem_Dir == "Yos":
        Mem_Txt += f'Iniciando análisis de : Yoslib.Bdt -> FncDef\n'

        try:
            ruta_bdt_yos = os.path.join(YosAplCfg["Yos"]["Dir"], "Bdt", "YosLib.Bdt")
            conn_fuente = sqlite3.connect(ruta_bdt_yos)

            cursor_lectura = conn_fuente.cursor()
            cursor_lectura.execute("SELECT cFnc, cCmd, cTit FROM FncDef")
            funciones_virtuales = cursor_lectura.fetchall()

            cOri_Virtual = "YosLib.FncDef"
            cursor.execute("UPDATE Fnc SET cEst = 'Eli' WHERE cOri = ?", (cOri_Virtual,))

            for reg_v in funciones_virtuales:
                v_cFnc = reg_v[0].strip() if reg_v[0] else ""
                v_cCmd = reg_v[1].strip() if reg_v[1] else ""

                if not v_cFnc:
                    continue

                cursor.execute("SELECT NumReg FROM Fnc WHERE cOri = ? AND cFun = ?", (cOri_Virtual, v_cFnc))
                reg_previo = cursor.fetchone()

                cNul_Virt = "S" if v_cFnc.startswith("_") else ""

                if reg_previo:
                    v_cPmt_Update = "[Virtual / Macro]"
                    cursor.execute('''
                        UPDATE Fnc
                        SET cPmt = ?, cEst = '', cModRegTim = ?, cModRegNik = ?
                        WHERE NumReg = ?
                    ''', (v_cPmt_Update, timestamp, nick_sistema, reg_previo[0]))
                else:
                    v_cTit_Ini = reg_v[2].strip() if reg_v[2] else "Función Virtual de Sistema"
                    v_cDes_Ini = f"Macro Comando Dinámico: {v_cCmd}"
                    v_cPmt_Ini = "PONGA LOS PARAMETROS"

                    cursor.execute('''
                        INSERT INTO Fnc (cNul, cFun, cTit, cDes, cPmt, cObs, cOri, cEst, cModRegNik, cModRegTim)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (cNul_Virt, v_cFnc, v_cTit_Ini, v_cDes_Ini, v_cPmt_Ini, "", cOri_Virtual, "Nue", nick_sistema, timestamp))

            cursor_lectura.close()

        except Exception as e:
            print(f"[-] No se pudo procesar la lectura de tu tabla FncDef: {e}")

    conn.commit()
    cursor.close()
    conn.close()

    Mem_Txt += f'{Men_Txtfin}\n'
    Mem_Txt += f'Proceso finalizado'

    import builtins
    if builtins.YosAplCfg["Apl"]["Ori_Etn"] == "Txt":
        Yos.Yos_Msg_Tui(Fnc_Tit=Mem_Tit, Fnc_Msg=Mem_Txt, Fnc_Tip= "Inf", Fnc_Hx=None)
    else:
       await Yos.Yos_Msg_Gui(Fnc_Tit=Mem_Tit, Fnc_Msg=Mem_Txt, Fnc_Tip= "Inf", Ancho= "450px", Alto= "auto")
    print(f"[+] Sincronización TOTAL finalizada con éxito para '{Mem_Dir}'.")

# ******************************************************************************************************************************************* FIN - Yos_DefFncHlp
# ******************************************************************************************************************************************* Yos_SutTxt
def Yos_SutTxt(**Fnc_Dic):
    # cTit : Sustituye los comando «Xxx» por sus valores definidos.
    # cDes : En esta función se han definido ciertos comandos y su texto real.
    #        Se puede usar para reducir texto o por si luego ese comando cambiar, un directorio, por ejemplo.
    #        Yos.Yos_SutTxt(Txt= "Texto a sustituir")
    # cPmt : Txt -> Texto en donde buscar los comandos «Xxx» y sustituir.
    #

    if "Txt" not in Fnc_Dic:
        return ""

    if Fnc_Dic["Txt"] is None:
        return ""

    Mem_Txt = Fnc_Dic["Txt"]

#    print(f'>>> ENTRANDO EN Yos_SutTxt: {Fnc_Txt}', flush=True)
#    print(YosAplCfg["Apl"]["Apl"])

    import builtins

    # --- DICCIONARIO DE SUSTITUCIÓN ---
    Mem_Sus = {
        "«Apl_Etn»" : builtins.YosAplCfg["Apl"]["Ori_Etn"],  # Entorno REAL de la Aplicacion, definido en Main.
        "«Apl_Apl»" : YosAplCfg["Apl"]["Apl"], # Nombre de la Aplicacion, el corto YosCtr

        "«YosLib_Dir»" : YosAplCfg["Yos"]["Dir"], # Direccion de la Libreria Yos

        "«DateTime»": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), # Fecha y hora Formato Bdt

        "«Apl_DirNom»" : YosAplCfg["Apl"]["DirNom"], # Solo el Nombre del Directorio

        #####################################################################

        #        "«Nick»"  : getattr(builtins, 'mtcyos', 'mtcyos'),
        #        "Mem_Ini_AplNom": Mem_Ini_AplNom,
        #        "Mem_Vsn": datetime.now().strftime("%Y.%m"),
        #        "Mem_Cpy": datetime.now().strftime("%Y")+" © Miguel Tortosa",
        #        "Usr": "YosAplCfg",
        # "«Otro»" : "Valor",
    }

    # --- PROCESO DE CAMBIO ---
    for k, v in Mem_Sus.items():
        if k in Mem_Txt:
#            print(f'Antes Cambio {k} - {Fnc_Txt}')
            Mem_Txt = Mem_Txt.replace(k, str(v))
#            print(f'Despues Cambio {k} - {Fnc_Txt}')

    return Mem_Txt
# ******************************************************************************************************************************************* FIN - Yos_SutTxt
# ******************************************************************************************************************************************* Yos_MstDir
def Yos_MstDir(ruta_base):
    # Escanea el Directorio indicado
    """
    Motor operativo: Escanea el directorio y retorna una lista de diccionarios.
    Sin dependencias externas.
    """
    estructura = []
    try:
        for elemento in os.listdir(ruta_base):
            ruta_completa = os.path.join(ruta_base, elemento)
            es_dir = os.path.isdir(ruta_completa)
            estructura.append({
                'nombre': elemento,
                'es_dir': es_dir,
                'path': ruta_completa,
                'img': 'folder.png' if es_dir else 'file.png'
            })
    except Exception as e:
        return []
    return estructura

# ******************************************************************************************************************************************* FIN - Yos_MstDir
# ******************************************************************************************************************************************* Yos_ZipDir
import shutil
import tempfile

def Yos_ZipDir(ruta_dir):
    # Comprime un directorio en un zip temporal y retorna la ruta del archivo.

    print(ruta_dir)
    nombre_base = os.path.basename(ruta_dir)

    from pathlib import Path
    Mem_NomZip = Path(ruta_dir).name
    print(f'Mem_NomZip={Mem_NomZip}')

    ruta_destino = os.path.join(tempfile.gettempdir(), Mem_NomZip)
    # 3. Comprimimos una sola vez
    # shutil.make_archive(base_name, format, root_dir)
    archivo_zip = shutil.make_archive(ruta_destino, 'zip', ruta_dir)

    print(f"ZIP creado exitosamente en: {archivo_zip}")

    return archivo_zip
# ******************************************************************************************************************************************* FIN - Yos_ZipDir
# ******************************************************************************************************************************************* Yos_RunFunFlo
def Yos_RunFunFlo(Fnc_Nom: str) -> bool:
    """
    Ejecuta una Función Flotante de manera dinámica basándose en la aplicación
    activa configurada en YosAplCfg["Apl"]["Apl"].

    Parámetros:
        Fnc_Nom (str): Nombre de la función a ejecutar (ej: "DbfCreSQLite_ModClm")

    Devuelve:
        bool: True si la ejecución fue exitosa, False en caso contrario.
    """
    # 1. Recuperamos el nombre de la aplicación activa desde la configuración global
    Nombre_App = YosAplCfg["Apl"].get("Apl")
    if not Nombre_App:
        print("Yos_RunFunFlo -> Error: YosAplCfg['Apl'] no está definido.")
        return False

    # 2. Armamos el nombre completo calificado del bloque flotante
    Funcion_Completa = f"{Nombre_App}.{Fnc_Nom.replace('()', '').strip()}"
    Nombre_App_Base, Nombre_Fnc_Base = Funcion_Completa.split(".")

    # 3. BÚSQUEDA EN CASCADA: Localizamos el objeto contenedor flotante en memoria
    App_Activa = (
        globals().get(Nombre_App_Base) or
        (isinstance(__builtins__, dict) and __builtins__.get(Nombre_App_Base)) or
        getattr(__builtins__, Nombre_App_Base, None) or
        sys.modules.get(Nombre_App_Base)
    )

    # 4. Extracción y ejecución segura de la función flotante
    if App_Activa and hasattr(App_Activa, Nombre_Fnc_Base):
        try:
            Func_Ejecutar = getattr(App_Activa, Nombre_Fnc_Base)
            Func_Ejecutar()
            return True
        except Exception as e:
            print(f"Yos_RunFunFlo -> Error al ejecutar {Funcion_Completa}: {e}")
            return False
    else:
        print(f"Yos_RunFunFlo -> Error: No se pudo localizar el contenedor flotante para {Funcion_Completa}")
        return False
# ******************************************************************************************************************************************* FIN - Yos_RunFunFlo
# ******************************************************************************************************************************************* Yos_IptAplUtl
def Yos_IptAplUtl():
    import sys
    import os
    import json
    import builtins
    import importlib.util

    Mem_Json_YosDir = os.path.join(YosAplCfg["Yos"]["SctDir"], "YosAplUtl.json")
    if not os.path.exists(Mem_Json_YosDir):
        Yos.Yos_MsgSis(Txt= "YosLib.Script.YosAplUtl.json no encontrado.", Tip= "Err")
        return
#    print(f'Mem_Json_YosDir={Mem_Json_YosDir}')

    with open(Mem_Json_YosDir, "r", encoding= "utf-8") as f:
        Mem_Json_YosAplUtl = json.load(f)
        Mem_Json_YosAplUtl_Ori = Mem_Json_YosAplUtl
#    print(f'Mem_Json_YosAplUtl={Mem_Json_YosAplUtl}')
#    print(f'Mem_Json_YosAplUtl_Ori={Mem_Json_YosAplUtl_Ori}')

# Verifico si ./YosAplUtl.json , el de la aplicacion existe
    Mem_Json_AplDir = os.path.join(YosAplCfg["Apl"]["Dir"], "YosAplUtl.json")   # Directorio de YosAplUtl.json
    Mem_Ori_Etn = YosAplCfg["Apl"]["Ori_Etn"]   # Entorno de la aplicacion
    Mem_Json_YosAplUtl = Mem_Json_YosAplUtl.get("YosAplUtl", {})    # Extraigo las Utilidades
    Mem_Json_YosAplUtl_Etn = {} # Solo las utilidades del entorno
    for nombre_serv, datos_serv in Mem_Json_YosAplUtl.items():
        etn_serv = datos_serv.get("Etn", "")
        # Comprobamos si coincide con el entorno de la aplicación
        if etn_serv == "" or etn_serv == Mem_Ori_Etn:
            Mem_Json_YosAplUtl_Etn[nombre_serv] = {
                "Des": datos_serv.get("Des", ""),
                "Atv": ""
            }

#    print(f'Mem_Json_AplDir={Mem_Json_AplDir}')
#    print(f'Mem_Ori_Etn={Mem_Ori_Etn}')
#    print(f'Mem_Json_YosAplUtl={Mem_Json_YosAplUtl}')
#    print(f'Mem_Json_YosAplUtl_Etn={Mem_Json_YosAplUtl_Etn}')

    if not os.path.exists(Mem_Json_AplDir):
        Mem_Json_YosAplUtl_Etn = {"YosAplUtl": Mem_Json_YosAplUtl_Etn}
        with open(Mem_Json_AplDir, "w", encoding="utf-8") as f_local:
            json.dump(Mem_Json_YosAplUtl_Etn, f_local, indent=4, ensure_ascii=False)

        Yos.Yos_MsgSis(Txt=f'YosAplUtl.json local creado con las aplicaciones compatibles del entorno {Mem_Ori_Etn}. Use "Atv": "S" para activarla', Tip="Inf")
    else:
        # Si existe, leemos el archivo local actual
        with open(Mem_Json_AplDir, "r", encoding="utf-8") as f_local:
            Mem_Json_Local_Data = json.load(f_local)

        local_servicios = Mem_Json_Local_Data.get("YosAplUtl", {})
        if "YosAplUtl" in local_servicios:
            local_servicios = local_servicios["YosAplUtl"]
#        print(f'local_servicios={local_servicios}')
        modificado = False

        # 1. Añado los que están en Yos (compatibles) pero no están en local
        for nombre_serv, datos_serv in Mem_Json_YosAplUtl_Etn.items():
            if nombre_serv not in local_servicios:
                local_servicios[nombre_serv] = datos_serv
                modificado = True
                Yos.Yos_MsgSis(Txt=f'YosAplUtl.json local modificado: Se añadió "{nombre_serv}".', Tip="Inf")

        # 2. Elimino los que están en local pero ya no están en Yos (o dejaron de ser compatibles)
        servicios_a_eliminar = []
        for nombre_serv in list(local_servicios.keys()):
            if nombre_serv not in Mem_Json_YosAplUtl_Etn:
                servicios_a_eliminar.append(nombre_serv)
        for nombre_serv in servicios_a_eliminar:
            del local_servicios[nombre_serv]
            modificado = True
            Yos.Yos_MsgSis(Txt=f'YosAplUtl.json local modificado: Se eliminó "{nombre_serv}".', Tip="Inf")

        # 3. Si está modificado, guardamos el resultado actualizado
        if modificado:
            contenido_local = {"YosAplUtl": local_servicios}
            with open(Mem_Json_AplDir, "w", encoding="utf-8") as f_local:
                json.dump(contenido_local, f_local, indent=4, ensure_ascii=False)

    # Leemos y Cergamos los Atv="S"
    with open(Mem_Json_AplDir, "r", encoding="utf-8") as f_local:
        Mem_Json_Local_Data = json.load(f_local)
    Mem_Json_Local_Data = Mem_Json_Local_Data.get("YosAplUtl", {})    # Extraigo las Utilidades
#    print(f'Mem_Json_Local_Data={Mem_Json_Local_Data}')
    for Mem_AplSer, datos_serv in Mem_Json_Local_Data.items():
        atv_val = datos_serv.get("Atv", "")
        if atv_val != "" and atv_val != "S":
            Yos.Yos_MsgSis(Txt=f'Yos_IptAplUtl() Valor de Atv no válido ("{atv_val}") en la aplicación {nombre_serv}. Use "S" o déjelo en blanco.', Tip="Err")
        elif atv_val == "S":
#            Yos_IptAplUtl_Cre(Mem_AplSer, Mem_Json_YosAplUtl_Ori)

#def Yos_IptAplUtl_Cre(Mem_AplSer, Mem_SuApl_Json):

            Mem_SuApl_Json = Mem_Json_YosAplUtl_Ori.get("YosAplUtl", {}).get(Mem_AplSer)

            ruta = os.path.join(YosAplCfg["Yos"]["SctDir"], f"{Mem_AplSer}.py")

            # Carga del módulo
            spec = importlib.util.spec_from_file_location(Mem_AplSer, ruta)
            modulo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(modulo)

            # 1. Recuperación del contenedor (mismo criterio que tu carga inteligente)
            app_name = os.path.basename(YosAplCfg["Apl"]["Dir"].rstrip("\\"))
            if not hasattr(builtins, app_name):
                class AppContainer: pass
                setattr(builtins, app_name, AppContainer())

            target_app = getattr(builtins, app_name)

            # 2. Registro de funciones (Inyectamos en el contenedor)
            for atributo in dir(modulo):
                if not atributo.startswith("__"):
                    obj = getattr(modulo, atributo)
                    if callable(obj) and getattr(obj, '__module__', None) == Mem_AplSer:
#                        setattr(target_app, atributo, obj)
                        setattr(builtins, atributo, obj)

        #                Yos.Yos_MsgSis(Txt=f"   {app_name}.{atributo}()")

            # 3. MANTENEMOS TU MENSAJE EXACTO (Sin tocar nada, tal como pediste)
            Yos.Yos_MsgSis(Txt=f'Yos Utilidad {Mem_AplSer} cargada, para ejecutarla, use {Mem_SuApl_Json["Run"]}')

#            return modulo

# ******************************************************************************************************************************************* FIN - Yos_IptAplUtl

###################################################################################  A REVISAR ###################################################################################

async def Yos_EntDat(**Fnc_Dic):
    # Solicita informacion directa

    if not Fnc_Dic:
        return

    """
    Tit -> Titulo
    Des -> Descripcion de los datoa a introducir
    Acn -> Cre, Ver, Mod, Eli , mision Ver
    Columnas a pedir
        {
            "Clm": "AplNue",
            "Rot": "Nombre aplicación",
            "ClmTip": "C",
            # Aplicamos: No_Nul (Obligatorio) y No_Pto (Sin puntos/signos para carpetas)
            "Vfy": "No_Nul, No_Pto",
            "Lon": 20, # Añadimos longitud para que Vfy Lon funcione Si es ClmTip=N 3.1  3 espacios 2 decimales 1.2  ( minimo 1 entero + . + decimales)
            "Opc": ""
        },
    Tipo    Funcion VERIFICACIONES DE DATOS
    Mod     Cap     .capitalize()   "Hola mundo" (Solo la primera letra de la frase)
    Mod     Min     .lower()        "hola mundo"
    Mod     Myu     .upper()        "HOLA MUNDO"
    Mod     Tit     .title()        "Hola Mundo" (La primera de cada palabra)
    Mod     NoEsp   Quita espacio de izquierda y derecha
    Mod     NoEsp_D Quita espacio de derecha
    Mod     NoEsp_I Quita espacio de izquierda

    Ver     Pas     contraseña (se mostrara *) y pondrá otro campo para verificacion
    Vfy     Lon     Longitud
    Vfy     No_Nul  (/NoNul) en campo cNul (S/N)    Tiene que estar lleno
    Vfy     No_Pto  No permite signos de puntuación (ideal para nombres de archivos).
    Vfy     Opc     Opciones (a,b,c,d,e)
    Vfy     Ran     Ran:Ini-Fin
    Vfy     UncLet  Solo permite A-Z y espacios.
    Vfy     UncNum  Solo permite 0-9.

    Rel     OpcTab  Opc:Tab:Clm:Des (Browse de selección)
    Rel     Unc     Unico Unc:Tab:Clm:Des

    DEVUELVE
    {
        "Clm": "AplNue",    # Columna
        "Dato": ""   # Dato devuelto
    },
    SI HAY ERRORES -> return


    EJEMPLO


    """


    # **Fnc_Dic es un diccionario con todo lo que envíes por nombre
    Mem_Tit = Fnc_Dic.get("Tit", "INTRODUCCIÓN DE DATOS") # Titulo
    Mem_Des = Fnc_Dic.get("Des", "INTRODUZCA LA INFORMACIÓN REQUERIDA.")    # Descripcion de los datoa a introducir
    Fnc_Dic["Tit"] = Mem_Tit
    Fnc_Dic["Des"] = Mem_Des

    import builtins
    if builtins.YosAplCfg["Apl"]["Ori_Etn"] == "Txt":    # Entorno Txt
        return yos.Yos_EntDat_Txt(**Fnc_Dic)
    else:
        return await Yos.Yos_EntDat_Frm(**Fnc_Dic)

from datetime import datetime
import string

def Yos_EntDat_Vfy(Fnc_Dat, Fnc_Vfy, Fnc_Rot, Fnc_Tip, Fnc_Lon):
    Mem_Err = ""
    Mem_Dat = Fnc_Dat
    reglas = [r.strip() for r in Fnc_Vfy.split(",") if r.strip()]

    for regla in reglas:
        # Mod - MODIFICADORES (Cambian el dato) ---
        if regla == "Cap":  # capitalize() : Convierte solo el primer carácter de toda la cadena a mayúscula y cambia todos los demás caracteres a minúscula
            Mem_Dat = Mem_Dat.capitalize()

        if regla == "Min":  # lower() : Convierte una cadena a minúsculas
            Mem_Dat = Mem_Dat.lower()

        if regla == "Myu":  # upper() : Convierte una cadena a mayúsculas
            Mem_Dat = Mem_Dat.upper()

        if regla == "NoEsp":  # strip() : Elimina caracteres de ambos extremos, izquierdo y derecho.
            Mem_Dat = Mem_Dat.strip()

        if regla == "NoEsp_D":  # rstrip() : Elimina caracteres solo desde la derecha (extremo).
            Mem_Dat = Mem_Dat.rstrip()

        if regla == "NoEsp_I":  # lstrip() : Elimina los caracteres solo desde la izquierda (inicio).
            Mem_Dat = Mem_Dat.lstrip()

        if regla == "Tit":  # title() : Convierte una cadena donde el primer carácter de cada palabra está en mayúscula y el resto en minúscula.
            Mem_Dat = Mem_Dat.title()

        # Vfy - VERIFICADORES (Lanzan errores) ---

        # Lon - Longitud
        if Fnc_Tip == "N":
            Nun_Limpio = str(Mem_Dat).replace(',', '') if Mem_Dat is not None else ""
            if Fnc_Lon > 0 and len(Nun_Limpio) > Fnc_Lon:
                Mem_Err = f"Error : {Fnc_Rot} excede al maximo definido {len(Nun_Limpio)}/{Fnc_Lon}."
                break
        else:
            # Aqui trunca por la derecha
            if Fnc_Lon > 0 and len(Mem_Dat) > Fnc_Lon:
                Mem_Dat = Mem_Dat[:Fnc_Lon]


        # No_Nul - Tiene que estar lleno
        if regla == "No_Nul":
            if Fnc_Tip == "D" and Fnc_Dat==None:    # para fechas
                Mem_Err = f"Error : Campo '{Fnc_Rot}' no puede estar vacío."
                break

            elif not Mem_Dat.strip():
                Mem_Err = f"Error : Campo '{Fnc_Rot}' no puede estar vacío."
                break

        # Opc - Opciones (a,b,c,d,e)
        if regla.startswith("Opc:") and not regla.startswith("OpcTab:"):
            lista_opc = [o.strip() for o in regla.split(":")[1].split(",")]
            if Mem_Dat not in lista_opc:
                opciones_str = ", ".join(lista_opc)
                Mem_Err = f"Error en '{Fnc_Rot}': Debe elegir entre ({opciones_str})."
                break

        # Ran - Ran:Ini-Fin
        if regla.startswith("Ran:"):
            try:
                val_ini, val_fin = regla.split(":")[1].split("-")
                val_ini, val_fin = val_ini.strip(), val_fin.strip()

                # --- Caso N (Números) ---
                if Fnc_Tip == "N":
                    if not (float(val_ini) <= float(Mem_Dat) <= float(val_fin)):
                        Mem_Err = f"Error : {Fnc_Rot} fuera de rango ({val_ini}-{val_fin})"
                        break

                # --- Caso D (Fechas) ---
                elif Fnc_Tip == "D":
                    f = Mem_Dat.strip()
                    dt_obj = None
                    try:
                        if "/" in f: dt_obj = datetime.strptime(f, "%d/%m/%Y")
                        elif "-" in f: dt_obj = datetime.strptime(f, "%Y-%m-%d")
                        elif len(f) == 8: dt_obj = datetime.strptime(f, "%Y%m%d")
                    except: pass

                    if not dt_obj:
                        Mem_Err = f"Error : Fecha '{Fnc_Rot}' no reconocida."
                        break
                    else:
                        if not (val_ini <= dt_obj.strftime("%Y%m%d") <= val_fin):
                            Mem_Err = f"Error : {Fnc_Rot} fuera de fecha ({val_ini}-{val_fin})."
                            break

                # --- Caso C (Texto) ---
                elif Fnc_Tip == "C":
                    if not (val_ini.upper() <= Mem_Dat.upper() <= val_fin.upper()):
                        Mem_Err = f"Error : {Fnc_Rot} fuera de secuencia alfabética."
                        break
            except:
                Mem_Err = f"Error de sintaxis en Rango para {Fnc_Rot}."
                break

        # Validaciones de caracteres
        # No_Pto - No permite signos de puntuación (Ideal para archivos)
        if regla == "No_Pto" and Mem_Dat:
            import string
            # !"#$%&'()*+,-./:;<=>?@[\]^_{|}~`
            signos_prohibidos = string.punctuation.replace("_", "") # le digo qiue el _ es permitido

            if any(char in signos_prohibidos for char in Mem_Dat):
                Mem_Err = f"Error : {Fnc_Rot} contiene signos no permitidos."
                break

        # UncLet - Solo permite A-Z y espacios.
        if regla == "UncLet" and Mem_Dat:
            if not all(x.isalpha() or x.isspace() for x in Mem_Dat):
                Mem_Err = f"Error : {Fnc_Rot} solo admite letras."
                break

        # UncNum - Solo permite 0-9.
        if regla == "UncNum" and Mem_Dat:
            if not Mem_Dat.isdigit():
                Mem_Err = f"Error : {Fnc_Rot} solo admite números."
                break

    return Mem_Dat, Mem_Err

async def Yos_AplCre(**Fnc_Dic):
    # Crea la estructura básica necesaria de una nueva aplicación Yos.
    import builtins
    import Yos

    # Aplicaciones
    Mem_Apl_Dir = {
        "YosMnu_Txt": ["Bat", "Bdt", "Script", "Sql"],
        "YosMnu_Frm": ["Bat", "Bdt", "Cfg", "Img", "Script", "Sql"]
    }


    # Definimos los campos que necesitamos
    if not Fnc_Dic:
        # Si entra aquí, es porque Fnc_Dic está VACÍO {}
        Mem_Campos = [
            {
                "Clm": "AplNue",
                "Rot": "Nombre aplicación",
                "Tip": "C",
                "Lon": 20,
                "Dat" : "Yos_KK",   # Dato por Omision
                "Mod" : "Cre",   # En que momento se puede Modificar Cre=Creacion , Mod=Modificacion
                "Vfy": "No_Nul, No_Pto",    # Aplicamos: No_Nul (Obligatorio) y No_Pto (Sin puntos/signos para carpetas)
                "Opc": ""
            },

            {
                "Clm": "AplOri",
                "Rot": "Origen (Plantilla)",
                "Tip": "C",
                "Lon": 0, # Añadimos longitud para que Vfy Lon funcione
                "Dat" : "YosMnu_Frm",
                "Mod" : "Cre",   # En que momento se puede Modificar Cre=Creacion , Mod=Modificacion
                "Vfy": "Opc",
                "Opc": list(Mem_Apl_Dir.keys()) # Aplicamos: Opc (Valida contra la lista de opciones)
            }
        ]
        '''
        Tip - Tipo Columna C=Caracteres, N = Numerico, D = Fecha
        TIPO = C -> NiceGui ui.input
            Clm - Nombre Columna a Devolver
            Rot - Rotulo
                NiceGui -> label : Etiqueta mostrada para la entrada de texto
            Tip = "C"
            Mod - En que momento se puede Modificar Cre=Creacion , Mod=Modificacion
            Lon - Longitud, MAXIMA ??
            Dat - Dato por Omision
                NiceGui -> value : El valor actual de la entrada de texto
            Vfy - Verificaciones
            Vfy_Opc - Opciones a Seleccionar {Dat, Dat, Dat, Dat}

            placeholder:            -> : marcador de posición, Texto que se mostrará si no se ha introducido ningún valor.
            password:               -> : contraseña, o si se debe ocultar la entrada (predeterminado: Falso)
            password_toggle_button: -> : botón_alternador_de_contraseña, Indica si se debe mostrar un botón para alternar la visibilidad de la contraseña (predeterminado: Falso).
            prefix:                 -> : prefijo,    un prefijo para anteponer al valor mostrado ( añadido en la versión 3.5.0 )
            suffix:                 -> : sufijo, un sufijo para agregar al valor mostrado ( añadido en la versión 3.5.0 )
            on_change:              -> : on_change;  Función de devolución de llamada que se ejecutará cuando cambie el valor.
            autocomplete:           -> : autocompletar,  Lista opcional de cadenas para autocompletar
            validation:             -> : validación, Diccionario de reglas de validación o una función que devuelve un mensaje de error opcional (predeterminado: None para ninguna validación).


        TIPO = N (C) -> NiceGui ui.input
            Clm - Nombre Columna a Devolver
            Rot - Rotulo
                NiceGui -> label : Etiqueta mostrada para la entrada de texto
            Tip = "C" - Auque es Numerico se trata conmo C , cuando se devuelve se hace float()
            Mod = {Cre/Mod} - En que momento se puede Modificar Cre=Creacion , Mod=Modificacion

            Lon - Longitud, Maxima en N=15
            Dec - Decimales, Maximo Lon -2

            Dat - Dato por Omision
                NiceGui -> value : El valor actual de la entrada de texto

            Vfy - Verificaciones
            Vfy_Opc - Opciones a Seleccionar ["1", "2","3","4"]

            placeholder:            -> : marcador de posición, Texto que se mostrará si no se ha introducido ningún valor.
            password:               -> : contraseña, o si se debe ocultar la entrada (predeterminado: Falso)
            password_toggle_button: -> : botón_alternador_de_contraseña, Indica si se debe mostrar un botón para alternar la visibilidad de la contraseña (predeterminado: Falso).
            prefix:                 -> : prefijo,    un prefijo para anteponer al valor mostrado ( añadido en la versión 3.5.0 )
            suffix:                 -> : sufijo, un sufijo para agregar al valor mostrado ( añadido en la versión 3.5.0 )
            on_change:              -> : on_change;  Función de devolución de llamada que se ejecutará cuando cambie el valor.
            autocomplete:           -> : autocompletar,  Lista opcional de cadenas para autocompletar
            validation:             -> : validación, Diccionario de reglas de validación o una función que devuelve un mensaje de error opcional (predeterminado: None para ninguna validación).

        TIPO = D -> NiceGui ui.date_input
            Rot (Rotulo) -> label : Etiqueta, Etiqueta mostrada para la entrada de texto
            range_input: -> : rango_entrada, Si es True, permite seleccionar un rango de fechas (el valor será un diccionario con las claves "desde" y "hasta").
            placeholder: -> : marcador de posición, Texto que se mostrará si no se selecciona ninguna fecha.
            Dat  (Dato) -> value: valor, el valor de la fecha actual
            on_change:   -> : on_change, Función de devolución de llamada que se ejecutará cuando cambie el valor.
        '''
        Mem_Campos = [
#            {   "Clm": "SaltoDeLinea"},
            {
                "Clm": "TIPO_C",            # Nombre de la Columna
                "Rot": "TIPO_C",            # Rotulo
                "Tip": "C",                 # Tipo de la Columna C=Caracteres, N = Numerico, D = Fecha
                "Mod" : "Cre",              # En que momento se puede Modificar Cre=Creacion , Mod=Modificacion
                "Lon": 20,                  # Longitud MAXIMA
                "Dat" : "Valor_Inicial",           # Dato por Omision
                "Vfy": "No_Nul, No_Pto",    # Aplicamos: No_Nul (Obligatorio) y No_Pto (Sin puntos/signos para carpetas)
                "Vfy_Opc": ""
            },
            {   "Clm": "SaltoDeLinea"},
            {
                "Clm": "AplOri",
                "Rot": "Origen (Plantilla)",
                "Tip": "C",
                "Mod" : "Cre",   # En que momento se puede Modificar Cre=Creacion , Mod=Modificacion
                "Lon": 0, # Añadimos longitud para que Vfy Lon funcione
                "Dat" : "YosMnu_Frm",
                "Vfy": "Opc",
                "Vfy_Opc": list(Mem_Apl_Dir.keys()) # Aplicamos: Opc (Valida contra la lista de opciones)
            },
            {   "Clm": "SaltoDeLinea"},
            {
                "Clm": "TIPO_Cz",            # Nombre de la Columna
                "Rot": "TIPO_Cz",            # Rotulo
                "Tip": "C",                 # Tipo de la Columna C=Caracteres, N = Numerico, D = Fecha
                "Mod" : "Cre",              # En que momento se puede Modificar Cre=Creacion , Mod=Modificacion
                "Lon": 20,                  # Longitud MAXIMA
                "Dat" : "Volor_Inicial",           # Dato por Omision
                "Vfy": "No_Nul, No_Pto",    # Aplicamos: No_Nul (Obligatorio) y No_Pto (Sin puntos/signos para carpetas)
                "Vfy_Opc": ""
            },
            {
                "Clm": "nSla",
                "Rot": "Sueldo",
                "Tip": "N",
                "Mod" : "Cre",   # En que momento se puede Modificar Cre=Creacion , Mod=Modificacion
                "Lon": 15, # longitud Maxima en N=15
                "Dec": 2, # Decimales (Maximo Lon -2)
                "Dat" : 12345678.45,   # Dato por Omision
                "Vfy": "No_Nul",    # Aplicamos: No_Nul (Obligatorio)
                "Vfy_Opc": ""
            },
            {
                "Clm": "Mes",
                "Rot": "Mes",
                "Tip": "N",
                "Mod" : "Cre",   # En que momento se puede Modificar Cre=Creacion , Mod=Modificacion
                "Lon": 2, # longitud Maxima en N=15
                "Dec": 0, # Decimales (Maximo Lon -2)
                "Dat" : "",   # Dato por Omision
                "Vfy": "Opc",
                "Vfy_Opc": ["1", "2","3","4"]
            },
            {   "Clm": "SaltoDeLinea"},
            {
                "Clm": "FecIni",            # Nombre de la Columna
                "Rot": "Fecha Inicial",            # Rotulo
                "Tip": "D",                 # Tipo de la Columna C=Caracteres, N = Numerico, D = Fecha
                "Mod" : "Cre",              # En que momento se puede Modificar Cre=Creacion , Mod=Modificacion
                "Dat" : "21/01/1967",           # Dato por Omision

                "Lon": 0,                  # Longitud MAXIMA


                "Vfy": "No_Nul",    # Aplicamos: No_Nul (Obligatorio) y No_Pto (Sin puntos/signos para carpetas)
                "Vfy_Opc": ""
            },
        ]

        Fnc_Dic = {
            "Tit": "CREAR UNA NUEVA APLICACIÓN",
            "Des": 'Va a crear el entorno de una nueva aplicación. Por favor ponga los datos necesarios.', # <br>
            "Acn": 'Cre',
            "Frm": 'Max', # Max=Pantalla al maximo
            "Campos": Mem_Campos
        }

    # 2. Llamamos al "Cerebro" de entrada de datos
    # Él se encargará de llamar a Yos_EntDat_Txt o Yos_EntDat_Frm
    Mem_Dat = await Yos_EntDat(**Fnc_Dic)
    # 3. Si el usuario cancela o hay error, salimos
    if not Mem_Dat:
        print(f'{Yos.Yos_TimeStamp()} -> {YosSes["Usr_Ipd"]} - {YosSes["Usr_Nik"]} : SE CANCELA Yos.Yos_AplCre()')
        return

    # **Fnc_Dic es un diccionario con todo lo que envíes por nombre
    print(f"NUESTO DATOS  - {inspect.currentframe().f_lineno}")
    print(Mem_Dat)
    Mem_AplNue  = Mem_Dat.get("AplNue", "") # Nombre de la Nueva Aplicacion
    Mem_AplOri  = Mem_Dat.get("AplOri", "")    # Nombre de la Aplicacion de Origen, esta en Mem_Apl_Dir


    """
    Crea la estructura de una nueva aplicación Yos.
    Ubicación de plantillas: Lib/Yos/AplCre/
    """
    if not Mem_AplNue:
        print("Aviso: No se ha especificado nombre de aplicación.")
        return

    if not Mem_AplOri:
        print("Aviso: No se ha especificado Mem_AplOri de aplicación.")
        return

    print(f'GENERANDO aplicacion {Mem_AplNue} aplicacion maestra {Mem_AplOri}')
    Mem_Sal = ""

    # VALIDACIÓN SOLICITADA [cite: 2026-04-20]
    if Mem_AplOri not in Mem_Apl_Dir:
        Mem_Sal = f"\n  ATENCIÓN : La Aplicación '{Mem_AplOri}' no esta definida."
        Mem_Sal += f"      Aplicaciones definidas : {list(Mem_Apl_Dir.keys())}"

        if builtins.YosAplCfg["Apl"]["Ori_Etn"] == "Txt":    # Entorno Txt
            print(Mem_Sal)
            Yos.FrmWit()
        else:
            Yos.Yos_Msg_Frm(Fnc_Tit= "ATENCIÓN", Fnc_Msg=Mem_Sal, Mem_AplOri= "Err", Ancho= "500px")
        return False

    Mem_Inf = []
    Mem_SubPla = "Frm" if "Frm" in Mem_AplOri else "Txt"

    # 1. RUTAS
    ruta_raiz = os.path.abspath(os.path.join(os.getcwd(), ".."))
    ruta_apl = os.path.join(ruta_raiz, Mem_AplNue)
    ruta_yos_lib = os.path.join(ruta_raiz, "Yos")
    ruta_apl_cre = os.path.join(ruta_yos_lib, "AplCre") # Nueva base

    es_nueva = not os.path.exists(ruta_apl)

    # 2. DIRECTORIOS
    if es_nueva:
        os.makedirs(ruta_apl, exist_ok=True)
        Mem_Inf.append(f"Carpeta Raíz Creada : {Mem_AplNue}")

    for sub in Mem_Apl_Dir[Mem_AplOri]:
        camino = os.path.join(ruta_apl, sub)
        os.makedirs(camino, exist_ok=True)
        Mem_Inf.append(f"  Subdirectorio creado : {sub}")

    # 3. COPIA DE LICENCIA (Lib/Yos/AplCre/LICENCIA)
    orig_lic = os.path.join(ruta_apl_cre, "LICENCIA")
    dest_lic = os.path.join(ruta_apl, "LICENCIA")
    if os.path.exists(orig_lic) and not os.path.exists(dest_lic):
        shutil.copy2(orig_lic, dest_lic)
        Mem_Inf.append("LICENCIA : Archivo copiado")

    # 4. COPIA DE MAIN (Lib/Yos/AplCre/Frm o Txt/Main.py)
    orig_main = os.path.join(ruta_apl_cre, Mem_SubPla, "Main.py")
    dest_main = os.path.join(ruta_apl, "main.py")
    if os.path.exists(orig_main) and not os.path.exists(dest_main):
        shutil.copy2(orig_main, dest_main)
        Mem_Inf.append(f"main.py : Generado desde entorno {Mem_SubPla}")

    # 5. COPIA DE GRÁFICOS (Solo si existe carpeta Img y es modo Frm)
    if Mem_SubPla == "Frm":
        ruta_orig_img = os.path.join(ruta_apl_cre, "Frm", "Img")
        ruta_dest_img = os.path.join(ruta_apl, "Img")
        if os.path.exists(ruta_orig_img):
            recursos = ["favicon", "Log_01", "Log_02"]
            for rec in recursos:
                for f in os.listdir(ruta_orig_img):
                    if f.startswith(rec):
                        orig_f = os.path.join(ruta_orig_img, f)
                        dest_f = os.path.join(ruta_dest_img, f)
                        if not os.path.exists(dest_f):
                            shutil.copy2(orig_f, dest_f)
                            Mem_Inf.append(f"  Gráfico : {f} copiado")

    # 6. GENERACIÓN DEL .BAT
    Mem_YosMnu_Txt_Bat = (
        "@echo off\n"
        "\n"
        f"Set AplNom={Mem_AplNue}\n"
        ":: AplNom es el nombre de la Aplicacion y del Directorio que la contiene\n"
        "Set AplDir=%~dp0\n"
        "\n"
        ":: Pongo os Path temporales\n"
        "call %AplDir%Lib\\Yos\\YosAccDirPth.bat %AplDir%\n"
        "\n"
        ":: Accedo a disco/directorio\n"
        f"cd /d %AplDir%%AplNom%\\\n"
        "\n"
        ":: Ejecuto Python\n"
        "echo Python - %AplNom%\n"
        "python main.py\n"
        "\n"
        "echo.\n"
        "echo Python - %AplNom%.py - Script Finalizado\n"
        "timeout /t 8\n"
        "exit"
    )

    bat_ruta = os.path.join(ruta_raiz, f"{Mem_AplNue}.bat")
    with open(bat_ruta, "w", encoding= "utf-8") as f:
        f.write(Mem_YosMnu_Txt_Bat)
    Mem_Inf.append(f"Lanzador : {Mem_AplNue}.bat generado")


    if builtins.YosAplCfg["Apl"]["Ori_Etn"] == "Txt":    # Entorno Txt
        # INFORME FINAL
        print("\n  " + "═"*55)
        print(f"  GENERANDO APLICACION : {Mem_AplNue}")
        for linea in Mem_Inf: print(f"    {linea}")
        print("  "+"═"*55 + "\n")
    else:
        Mem_Inf_Str = "\n".join(Mem_Inf)
        Mem_Inf_Str = Mem_Inf_Str.replace("\n", "<br>")
        Mem_Inf_Str = Mem_Inf_Str.replace(" ", "&nbsp;")

        return Yos.Yos_Msg_Frm(
            Fnc_Tit=f'GENERANDO APLICACION : {Mem_AplNue}',
            Fnc_Msg=Mem_Inf_Str,
            Fnc_Tip= "Inf",
            Ancho= "450px",
            Alto= "auto"
        )

    return True

#############################################################################################################
def MstFncLin(FncNiv= "Act"):
    # Mustra la Funcion que llamo a la Funcion ACTUAL (Act/Ant)
    #    from Yos import MstFncLin
    #    input(MstFncLin(FncNiv= "All"))

    if YosAplCfg["Apl"]["Dbg"]== "S": print("******** Yos.MstFncLin() ********")
    if YosAplCfg["Apl"]["Dbg"]== "S": print(f"FncNiv={FncNiv}")

    match FncNiv:
        case "Ant": # Anterior
            marco_llamador = sys._getframe(2)
        case "All":
            lineas = []
            actual = sys._getframe(1)
            nivel = 0
            while actual:
                nombre = actual.f_code.co_filename
                fnc = actual.f_code.co_name
                lin = actual.f_lineno
                lineas.append(f"[{nivel:02d}] {nombre} -> {fnc} (L{lin})")
                actual = actual.f_back
                nivel += 1
            return "\n".join(lineas)
        case _:
            print("Actual")
            marco_llamador = sys._getframe(1)

    nombre_archivo = marco_llamador.f_code.co_filename
    numero_linea = marco_llamador.f_lineno
    return f"- {nombre_archivo} - {numero_linea}"

def YosCfg_Rcu(**FncDic):
    # Busca dentro de YosAplCfg las Clm del prefijo indicado Yos.YosCfg_Rcu(CodBus='_Prefijo_')
    if YosAplCfg["Apl"]["Dbg"]== "S": print("******** Yos.YosCfg_Rcu() ********")
    if YosAplCfg["Apl"]["Dbg"]== "S": print(f"FncDic={FncDic}")
    Fnc_Txt= "Yos.YosCfg_Rcu(CodBus='_Prefijo_')"

    if not 'CodBus' in FncDic:
       FrmWit(Fnc_Wit=8, Fnc_Txt=f"{Fnc_Txt} La clave 'CodBus' no existe."+ MstFncLin("Ant"))
       return {}

    SalDat={k: v for k, v in YosCfg.items() if k.startswith(FncDic["CodBus"])}
    print(SalDat)
    #for key in YosCfg: # O for key in shelf.keys():
    #    print(f"Clave: {key} -> Valor: {YosCfg[key]}")

def EmlEnv(Destinatario=None, Asunto= "", Cuerpo= ""):
    # Envia un Email
    #Yos.EmlEnv("mmedina@upnfm.edu.hn", "Contacto desde YosCtr", "Desde Python con amor.")
    # Caso A (Un solo amigo): EmlEnv("mtcyos@yahoo.es", "Aviso", "Hola Bin")
    # Caso B (Varios socios): EmlEnv(["mtcyos@yahoo.es", "socio@gmail.com"], "Reporte", "Adjunto datos")

    from prompt_toolkit.application import Application
    from prompt_toolkit.layout import Layout, HSplit, VSplit, Window
    from prompt_toolkit.widgets import TextArea, Button, Label, Frame
    from prompt_toolkit.key_binding import KeyBindings
    from prompt_toolkit.styles import Style as PtStyle
    from prompt_toolkit.formatted_text import HTML
    from prompt_toolkit.layout.containers import FloatContainer, Float, ConditionalContainer
    from prompt_toolkit.filters import Condition
    from prompt_toolkit.shortcuts import message_dialog
    from prompt_toolkit.clipboard.pyperclip import PyperclipClipboard

    import smtplib
    from email.message import EmailMessage

    if not YosAplCfg["Apl"].get("Eml_Svr", "").strip():
        FrmWit(f'\n{Fore.RED} [ ERROR ] El servidor de (YosAplCfg.Apl."Eml_Svr") correo no está configurado la tabla Dat.' ,8)
        return False

    Mem_EmlDst = "N"
    if Destinatario == "Eml_EmlDst":
        if "Eml_EmlDst" in YosAplCfg:
            Destinatario = YosAplCfg["Apl"]["Eml_EmlDst"]
            Mem_EmlDst = "S"
        else:
            Mem_MsgErr = '[ ERROR ] No se ha definido el destinatario Eml_EmlDst en la tabla Dat.'
            FrmWit(Mem_MsgErr, 8)
            return False

    Yos.Yos_Cls_Txt()
    Yos.FrmCab("Rot")
#    print()
#    print(f"{Fore.YELLOW}{FrmLin('ENVÍO DE EMAIL', 'C')}{Style.RESET_ALL}")
    print()

    # 2. Configuración de Medidas
    Mem_Tit = "*** ENVÍO DE EMAIL *** (F2 - Ayuda)"
    Mem_F2 = """Destinatario :
    Un solo email : nombre@yahoo.es
    Varios emails : uno@yahoo.es, dos@gmail.com

Su Nombre    :
Su Email     :
    Son campos optativos

Asunto       : Asunto del email
Mensaje      : mensaje del email, puede añadir líneas pulsando INTRO al final de la línea"""
    Mem_F2_WX = 95
    Mem_F2_HY = 10

    Mem_WX = 95
    Mem_HY = 20

    if not Destinatario or not Asunto or not Cuerpo:
        if Mem_EmlDst == "S":
            txt_dest = TextArea(
                text=Destinatario if Destinatario else "",
                multiline=False,
                read_only=True  # 🔒 Esto bloquea la edición del usuario
            )
        else:
            txt_dest = TextArea(text=Destinatario if Destinatario else "", multiline=False)

        txt_nom = TextArea(multiline=False)
        txt_eml = TextArea(multiline=False)
        txt_asun = TextArea(text=Asunto if Asunto else "", multiline=False)
        txt_cuerpo = TextArea(text=Cuerpo if Cuerpo else "")
        lbl_error = Label("", style= "fg:ansired bold")

        def aceptar_handler():
            if not txt_dest.text.strip():
                lbl_error.text = "✖ Error : DEBE INDICAR EL DESTINATARIO"
                app.layout.focus(txt_dest)
                return
            if not txt_asun.text.strip():
                lbl_error.text = "✖ Error : DEBE INDICAR EL ASUNTO"
                app.layout.focus(txt_asun)
                return
            if not txt_cuerpo.text.strip():
                lbl_error.text = "✖ Error : DEBE ESCRIBIR UN MENSAJE"
                app.layout.focus(txt_cuerpo)
                return
            app.exit(result=True)

        def cancelar_handler():
            app.exit(result=False)

        btn_enviar = Button(" ENVIAR ", handler=aceptar_handler)
        btn_enviar.left_symbol = ""; btn_enviar.right_symbol = ""
        btn_cancelar = Button(" CANCELAR ", handler=cancelar_handler)
        btn_cancelar.left_symbol = ""; btn_cancelar.right_symbol = ""

        kb = KeyBindings()

        # ---------------- VARIABLES Y LÓGICA DEL POPUP DE AYUDA F2 ----------------
        estado_ayuda = {"visible": False}

        @Condition
        def is_help_visible():
            return estado_ayuda["visible"]

        def ocultar_ayuda():
            estado_ayuda["visible"] = False
            # Recuperamos foco al cuerpo o al botón
            app.layout.focus(txt_cuerpo)

        txt_cuerpo_ayuda = TextArea(
            text=Mem_F2,
            multiline=True,
            read_only=True,   # Solo lectura
            scrollbar=True,   # Activa la barra lateral
            focusable=True,   # Importante para que las flechas funcionen
            width=Mem_F2_WX,         # Ancho estándar para el cuadro de ayuda
            height=Mem_F2_HY,        # Alto estándar (ajusta según necesites)
            style= "fg:ansiwhite bg:black"
        )

        btn_cerrar_ayuda = Button(" CERRAR ", handler=ocultar_ayuda)
        btn_cerrar_ayuda.left_symbol = ""; btn_cerrar_ayuda.right_symbol = ""

        marco_ayuda = Frame(
            body=HSplit([
                Window(height=1),
                txt_cuerpo_ayuda, # Reemplazamos el Label por el TextArea
                Window(height=1),
                VSplit([Window(), btn_cerrar_ayuda, Window()])
            ]),
            title=HTML("<b><ansiyellow>*** AYUDA ***</ansiyellow></b>"),
            style= "fg:ansicyan bg:black"
        )

        ayuda_float = Float(
            content=ConditionalContainer(content=marco_ayuda, filter=is_help_visible),
            transparent=False
        )

        @kb.add('f2')   # Ayuda Flotante
        def _(event):
            estado_ayuda["visible"] = True
            event.app.layout.focus(txt_cuerpo_ayuda) #btn_cerrar_ayuda)

        @kb.add('escape')
        def _(event):
            if estado_ayuda["visible"]:
                ocultar_ayuda()
            else:
                event.app.exit(result=False)

        @kb.add('c-v', eager=True)    # Ctrl + V Pegar del portapapeles
        def _(event):
            """Fuerza el pegado limpio desde el portapapeles de Windows"""
            data = event.app.clipboard.get_data()
            event.current_buffer.insert_text(data.text)

        @kb.add('c-c')    # CTRL + C (Copiar o Salida de emergencia)
        def _(event):
            buffer = event.current_buffer
            if buffer.selection_state:
                data = buffer.copy_selection()
                event.app.clipboard.set_data(data)
            else:
                if AccReg == "Ver":
                    do_copy_clipboard()
                else:
                    event.app.exit(result=False)

#        @kb.add('c-c')
#        def _(event):
#            event.app.exit(result=False)

        @kb.add('tab', filter=is_help_visible)
        def _(event):
            # Ciclo cerrado dentro de la ayuda
            if event.app.layout.has_focus(txt_cuerpo_ayuda):
                event.app.layout.focus(btn_cerrar_ayuda)
            else:
                event.app.layout.focus(txt_cuerpo_ayuda)

        # --- TAB: Para cuando la ayuda está CERRADA (Email normal) ---
        @kb.add('tab', filter=~is_help_visible) # El símbolo ~ significa "NO"
        def _(event):
            event.app.layout.focus_next()

        @kb.add('s-tab', filter=is_help_visible)
        def _(event):
            if event.app.layout.has_focus(btn_cerrar_ayuda):
                event.app.layout.focus(txt_cuerpo_ayuda)
            else:
                event.app.layout.focus(btn_cerrar_ayuda)

        # --- SHIFT-TAB: Para cuando la ayuda está CERRADA (Email normal) ---
        @kb.add('s-tab', filter=~is_help_visible)
        def _(event):
            event.app.layout.focus_previous()

        @kb.add('pageup', filter=is_help_visible)
        def _(event):
            # Desplaza el cursor 10 líneas hacia arriba
            for _ in range(10):
                txt_cuerpo_ayuda.buffer.cursor_up()

        @kb.add('pagedown', filter=is_help_visible)
        def _(event):
            # Desplaza el cursor 10 líneas hacia abajo
            for _ in range(10):
                txt_cuerpo_ayuda.buffer.cursor_down()


        cuerpo_frame = HSplit([
            Label(""),
            VSplit([Label(HTML("  <ansiyellow>Destinatario : </ansiyellow>"), width=18), txt_dest]),
            Label(""),
            VSplit([Label(HTML("  <ansiyellow>Su Nombre    : </ansiyellow>"), width=18), txt_nom]),
            Label(""),
            VSplit([Label(HTML("  <ansiyellow>Su Email     : </ansiyellow>"), width=18), txt_eml]),
            Label(""),
            VSplit([Label(HTML("  <ansiyellow>Asunto       : </ansiyellow>"), width=18), txt_asun]),
            Label(""),
            VSplit([Label(HTML("  <ansiyellow>Mensaje      : </ansiyellow>"), width=18), txt_cuerpo]),
            Label(""),
            lbl_error,
            Label(""),
            VSplit([Window(), btn_enviar, Label("    "), btn_cancelar, Window()])
        ])

        marco = Frame(
            body=cuerpo_frame,
            title=HTML(f"<b><ansigreen>{Mem_Tit}</ansigreen></b>"),
            width=Mem_WX,
            height=Mem_HY
        )

#        layout_formulario = HSplit([
#            VSplit([Window(), marco, Window()]),
#            Window()
#        ])
        layout_base = HSplit([
            VSplit([Window(), marco, Window()]), # El marco ahora está al tope
            Window()                             # Este empuja todo desde abajo hacia arriba
        ])

        layout_formulario = FloatContainer(
            content=layout_base,
            floats=[ayuda_float]
        )

        estilo_eml = PtStyle([
            ("button", "fg:white bg:#0000aa"),
            ("button.focused", "fg:white bg:#00aa00 bold"),
            ("text-area", "bg:#333333 fg:white"),
            ("frame.border", "fg:ansigreen"),
            ("frame.label", "fg:ansigreen"),
        ])

        app = Application(
            layout=Layout(layout_formulario),
            key_bindings=kb,
            style=estilo_eml,
            clipboard=PyperclipClipboard(),
            mouse_support=True,
            full_screen=False,
            erase_when_done=True
        )

        # Foco inicial inteligente
        if not Destinatario: app.layout.focus(txt_dest)
        elif not Asunto: app.layout.focus(txt_asun)
        else: app.layout.focus(txt_cuerpo)

        if not app.run():
            FrmWit(f"\n [ ATENCION ] Envío de email cancelado por el usuario." ,8)
            return False

        Destinatario = txt_dest.text.strip()
        Asunto = txt_asun.text.strip()
        Cuerpo_Final = txt_cuerpo.text.strip()
        Mem_Nom = txt_nom.text.strip()
        Mem_Eml = txt_eml.text.strip()

        MemCab = ""
        if Mem_Nom:
            MemCab += f"{Mem_Nom}\n"
        if Mem_Eml:
            MemCab += f"Correo Electrónico : {Mem_Eml}\n"
        if MemCab:
            MemCab += "*****************************************\n"
        Cuerpo = MemCab + Cuerpo_Final

    Cuerpo = YosAplCfg["Apl"]["Eml_MsgCab"].replace("\\n", "\n") +Cuerpo + YosAplCfg["Apl"]["Eml_MsgPie"].replace("\\n", "\n")

    # 1. Normalización: Si es un string, lo convertimos en lista de un elemento
    if isinstance(Destinatario, str):
        Lista_Dest = [Destinatario]
    else:
        Lista_Dest = Destinatario

    # 3. Construcción del mensaje
    Msg = EmailMessage()
    Msg['Subject'] = Asunto
    Msg['From'] = f'{YosAplCfg["Apl"]["Eml_EmlEnv"]} <{YosAplCfg["Apl"]["Eml_EmlEnv"]}>'
    Msg['To'] = ", ".join(Lista_Dest)
    Msg.set_content(Cuerpo)

    try:
        with smtplib.SMTP(YosAplCfg["Apl"]["Eml_Svr"], YosAplCfg["Apl"]["Eml_Puo"]) as server:
            server.starttls()
            server.login(YosAplCfg["Apl"]["Eml_Usr"], YosAplCfg["Apl"]["Eml_Pas"])
            # Enviamos a la lista completa
            server.send_message(Msg)
        Yos.FrmWit(f' [ OK ] SISTEMA: Correo enviado a {len(Lista_Dest)} destinatario(s).' ,8)
        return True
    except Exception as e:
        error_seguro = str(e).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        Yos.FrmWit(f' [ ERROR ] {error_seguro}.' ,8)
        print(f"ERROR EmlEnv: {e}")
        return False

def Yos_TxtMulLin(Fnc_Esp=0):
    # Introduce los datos en un Texto Multilinea
    from colorama import Fore, Back, Style

    try:
        # Convertimos a entero. Si es "8", se vuelve 8.
        Fnc_Esp = int(Fnc_Esp)
    except (ValueError, TypeError):
        # Si mandan algo que no es número (ej: "hola"), volvemos a 0
        Fnc_Esp = 0

    print(f"{Style.BRIGHT}{Fore.BLUE}{FrmLin('Ingrese el texto (Deje una línea en blanco y presione Enter para finalizar.', Fnc_Esp)}")
    lineas = []

    # Iniciamos el conteo según tu regla de numeración [cite: 2026-01-20]
    while True:
#       linea = input(f"{len(lineas) + 1}-> ")
        linea = input(f"{Fore.YELLOW}{FrmLin(f'{len(lineas) + 1}-> ', 8)}{Style.RESET_ALL}")
        if linea == "": # Si la línea está vacía, terminamos
            break
        lineas.append(linea)

    texto_final = "\n".join(lineas)
    return texto_final

def Yos_ClipCopy(texto):
    # Manda el texto a PortaPapeles
    import pyperclip
    """
    Copia cualquier cadena al portapapeles del sistema operativo actual.
    """
    try:
        # 1. Limpiamos espacios laterales para evitar errores de pegado
        cadena = str(texto).strip()

        # 2. Comando universal
        pyperclip.copy(cadena)

        return True
    except Exception as e:
        input(f"Error Portapapeles: {e}")
        return False

def Yos_Pas(prompt= ""):
    # Entrada de datos tipo Password
    import msvcrt
    import sys

    print(prompt, end='', flush=True)
    pw = ""
    while True:
        # Capturamos una tecla sin que se vea en pantalla
        char = msvcrt.getch()

        # Si es Enter (CR o LF)
        if char in (b'\r', b'\n'):
            print() # Salto de línea al terminar
            break

        # Si es Backspace (Borrar)
        elif char == b'\x08':
            if len(pw) > 0:
                pw = pw[:-1]
                # Truco para borrar el asterisco en la consola:
                # Retroceder (\b), Espacio (borra), Retroceder (\b)
                sys.stdout.write('\b \b')
                sys.stdout.flush()

        # Si es cualquier otro carácter (evitamos teclas de función)
        elif len(char) == 1 and char >= b' ':
            try:
                pw += char.decode('utf-8')
                sys.stdout.write('*')
                sys.stdout.flush()
            except:
                pass # Ignorar caracteres extraños

    return pw

def Yos_TimeStamp(Fnc_Nue= ""):
    # Devuelve el formato TimeStamp , Fnc_Nue == "Cre" añado la marca de registro nuevo +"*"
    from datetime import datetime

    Mem_TimeStamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if Fnc_Nue == "Cre":
        Mem_TimeStamp = Mem_TimeStamp +"*"
    else:
        Mem_TimeStamp = Mem_TimeStamp +" "

    return Mem_TimeStamp

# PARA REVISION *********************************************************************
def Dic_Rcu(Fnc_Pre, Fnc_Dic= "gcAplDat"):
    # Devuelve un Dicccionario Segun el Prefijo de los datos "Yos_"
    if YosAplCfg["Apl"]["Dbg"]== "S": print("******** Yos.Dic_Rcu() ********")

    if isinstance(Fnc_Dic, dict):
        if gcAplDat["Dbg"]== "S": print("Es un diccionario Reg."+str(len(Fnc_Dic))+" Fnc_Pre= "+Fnc_Pre)
        if gcAplDat["Dbg"]== "S": print(Fnc_Dic)
        SalDat={k: v for k, v in Fnc_Dic.items() if k.startswith(Fnc_Pre)}
    else:
        if gcAplDat["Dbg"]== "S": print("No es un diccionario")
        SalDat={}

    return SalDat

def Yos_Enc(Fnc_Txt):

    Mem_Txt = Fnc_Txt.encode('utf-8')

    print(f'Yos_Enc(Mem_Txt) YosAplCfg["Apl"][Enc]={YosAplCfg["Apl"]["Enc_Mtd"]}')
    print(f'Entrada={Mem_Txt}')
    if YosAplCfg["Apl"]["Enc_Mtd"]== "Md5":  # Convierte Texto a Md5
        import hashlib
        md5_hash = hashlib.md5()
        md5_hash.update(Mem_Txt)
        Fnc_Txt = md5_hash.hexdigest()

    elif YosAplCfg["Apl"]["Enc_Mtd"]== "Bcr":  # Convierte Texto a Bcr
        import bcrypt
        # Generamos el hash con una "sal" automática
        # Esto genera los 60 caracteres que guardaremos en cPasBcr
        Bcr_Hash = bcrypt.hashpw(Mem_Txt, bcrypt.gensalt())
        # Lo convertimos a texto para guardarlo en la SQLite
        Fnc_Txt = Bcr_Hash.decode('utf-8')
    print(f'Salida={Fnc_Txt}')
    return Fnc_Txt

def Yos_Otp(Fnc_Txt):
    #def GenOtp()

    # Generate a secure random secret key (store this securely!)
    # It should be base32 encoded for compatibility with pyotp
    secret = base64.b32encode(pyotp.random_base32().encode()).decode()

    # Create a TOTP object
    totp = pyotp.TOTP(secret)

    # Generate a current OTP
    current_otp = totp.now()
    print(f"CODIGO TOTP: {current_otp}")

    # Verify an OTP (e.g., entered by the user)B
    user_entered_otp = input("Enter the OTP: ")
    if totp.verify(user_entered_otp):
        print("OTP verified successfully!")
    else:
            print("Invalid OTP.")

    # To generate a provisioning URI for QR code generation (e.g., for Google Authenticator)
    # Replace 'YourAppName' and 'user@example.com' with your actual values
    provisioning_uri = totp.provisioning_uri(name='user@example.com', issuer_name='YourAppName')
    print(f"Provisioning URI: {provisioning_uri}")

######################################################################
