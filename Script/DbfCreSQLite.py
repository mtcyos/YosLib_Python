#!/usr/bin/env python3
# -*- coding: utf-8 -*
"""
   Dbf_Cre_Sqt.py
   IMPORTA DE .dbf a SQLite

   Copyright (c) 2026 Miguel Tortosa

   Licenciado bajo la Licencia MIT.

   Consulte el archivo LICENCIA en la raíz del proyecto para más información.
"""

import sqlite3
import datetime
import os
import sys
import glob
from dbfread import DBF
import platform
from datetime import datetime

_Mem = {}   # Definimos la gaveta privada del script
"""
try:
    # Listamos todo el contenido
    Dir_Sub = os.listdir(Ini_Dbf_Dir)
    for Sub in Dir_Sub:
        SQLite_Clave ="SQLITE_" +Sub
        SQLite_path = Ini_SQL_Dir +"Yos" +Sub +".Bdt" #os.path.join(Ini_SQL_Dir, f"Yos{nombre_final}.Bdt")

        Dbf_Clave ="Dbf_" +Sub
        Dbf_path = Ini_Dbf_Dir +Sub #+"/"
        # 5. Guardamos en el diccionario
        _privado[SQLite_Clave] = SQLite_path
        _privado[Dbf_Clave] = Dbf_path

    # 1. Buscamos archivos directamente en Dbf (según tu última prueba)
    for filename in os.listdir(Ini_Dbf_Dir):
        if filename.lower().endswith(".dbf"):
            # Obtenemos el nombre sin extensión (ej: "Yoscli")
            nombre_raw = os.path.splitext(filename)[0]

            # 2. LIMPIEZA: Si el nombre empieza por 'Yos' (ignorando mayúsculas), lo quitamos
            if nombre_raw.lower().startswith("yos"):
                nombre_limpio = nombre_raw[3:] # Quita los primeros 3 caracteres
            else:
                nombre_limpio = nombre_raw

            # 3. Capitalizamos para que quede "Cli", "Sis", "Msi"
            nombre_final = nombre_limpio.capitalize()

            # 4. Construimos las rutas finales
            # Clave: SQLITE_Cli, Ruta: .../YosCli.Bdt
            SQLite_path = os.path.join(Ini_SQL_Dir, f"Yos{nombre_final}.Bdt")
            dbf_path = os.path.join(Ini_Dbf_Dir, filename)

            # 5. Guardamos en el diccionario
            _privado[f"SQLITE_{nombre_final}"] = SQLite_path
            _privado[f"Dbf_{nombre_final}"] = dbf_path

except Exception as e:
    print(f"Error: {e}")
#  input(_privado)
"""

def DbfCreSQLite_Ipt(Titular,ruta_db, carpeta_dbf):
    Yos.Yos_Cls_Txt()
    # Asegurarnos de que la carpeta de destino de la BD existe
    os.makedirs(os.path.dirname(ruta_db), exist_ok=True)

    conexion = sqlite3.connect(ruta_db)
    conexion.execute("PRAGMA journal_mode=WAL;")
    cursor = conexion.cursor()

    # Buscamos todos los archivos .dbf en la ruta especificada
    patron = os.path.join(carpeta_dbf, "*.dbf")
    archivos = glob.glob(patron)

    if not archivos:
        print(f"ATENCION : No se encontraron archivos .dbf. {patron}")
        print(f"Ejecute la opcion Desencriptar Systema es Hmg-Python")
        Yos.FrmWit()
        return "Err"

    for ruta_completa in archivos:
        nombre_tabla = os.path.splitext(os.path.basename(ruta_completa))[0]
        if nombre_tabla == "Not":
            nombre_tabla = "Ntc" # se cambia porqque Not es reservada
        if nombre_tabla[:3]== "Py_":    # quito el Py_ porque solo lo uso en YsCtr Hmg
            nombre_tabla =nombre_tabla.removeprefix("Py_")

        # -- Cambiar el nombre de la tabla de forma segura
        # ALTER TABLE "Not" RENAME TO "Ntc";

        try:
            # char_decode_errors='ignore' salta el error del byte 0x81
            tabla_fox = DBF(ruta_completa, encoding='cp1252', char_decode_errors='ignore')

            print(f"Importando: {nombre_tabla}...", end="\r")

 #           # Crear tabla
 #           columnas = tabla_fox.field_names
 #           input(tabla_fox.fields)
 #           definicion = ", ".join([f"[{col}] TEXT" for col in columnas])

##########################33
# --- SUSTITUIR DESDE AQUÍ (Aprox. Línea 112) ---
            definiciones_campos = []
            for campo in tabla_fox.fields:
                nom_col = campo.name
                tipo_fox = campo.type.upper()
                L = campo.length
                D = campo.decimal_count

                # Mapeo con Longitud y Decimales Bin >
                if tipo_fox == 'C':
                    tipo_sql = f"VARCHAR({L})"
                elif tipo_fox == 'N':
                    if D > 0:
                        tipo_sql = f"DECIMAL({L},{D})"
                    else:
                        tipo_sql = f"INTEGER({L})"
                elif tipo_fox == 'D':
                    tipo_sql = "TEXT(10)" # Las fechas Fox no tienen longitud variable útil en SQL
                elif tipo_fox == 'L':
                    tipo_sql = "INTEGER(1)"
                elif tipo_fox == 'M':
                    tipo_sql = "TEXT" # Memo es ilimitado
                else:
                    tipo_sql = "TEXT"

                definiciones_campos.append(f"[{nom_col}] {tipo_sql}")

            definicion = ", ".join(definiciones_campos)
#########################
            cursor.execute(f"DROP TABLE IF EXISTS [{nombre_tabla}]")
            cursor.execute(f"CREATE TABLE [{nombre_tabla}] ({definicion})")
            # Insertar datos
            for registro in tabla_fox:
                valores = list(registro.values())
                huecos = ", ".join(["?" for _ in valores])
                cursor.execute(f"INSERT INTO [{nombre_tabla}] VALUES ({huecos})", valores)

            print(f"✅ Tabla [{nombre_tabla}] importada con éxito.      ")

        except Exception as e:
            print(f"❌ Error en {nombre_tabla}: {e}")

    conexion.commit()
    conexion.close()
    print(f"\n{Titular}\n--- Proceso de importación finalizado ---")
    input("Presiona Enter para continuar...")

# Arreglo nombre la esctruturas
#Ini_SQL_Dir = Ini_SQL_Dir #YosAplCfg["Apl"]["Dir_Bdt"]
#input(Ini_SQL_Dir)

def DbfCreSQLite_ModClm_Nom(old_name):
    """
    Regla Bin >: prefijo(1) + Bloques de 3 (Mayúscula + minúsculas)
    """
    name = old_name.upper()

    # Mapeo específico para auditoría
    if name == "CNIKMODREG": return "cModRegNik"
    if name in ["DFECMODREG", "CHORMODREG"]: return "cModRegTim"

    prefix = name[0].lower()
    resto = name[1:].lower()
    chunks = [resto[i:i+3].capitalize() for i in range(0, len(resto), 3)]
    Salida = f"{prefix}{''.join(chunks)}"
    # Abreviciones Reservada de SQLite
    if "Not" in Salida:
        Salida = Salida.replace("Not", "Ntc")
    return Salida

def DbfCreSQLite_ModClm_ModReg(cursor, tabla):
    """
    Restaura cModRegTim y mantiene cModRegNik - Versión corregida Bin >
    """
    # Usamos corchetes [tabla] para evitar el error con "Not" o "Ntc"
    for col in ["cModRegNik", "cModRegTim"]:
        try:
            cursor.execute(f"ALTER TABLE [{tabla}] ADD COLUMN {col} VARCHAR(20)")
        except sqlite3.OperationalError:
            pass

    cursor.execute(f"PRAGMA table_info([{tabla}])")
    cols = {c[1].upper(): c[1] for c in cursor.fetchall()}

    # Unificar Fecha y Hora en cModRegTim (Corrección de sintaxis)
    if "DFECMODREG" in cols and "CHORMODREG" in cols:
        # Usamos corchetes también para los nombres de las columnas viejas
        cursor.execute(f"""
            UPDATE [{tabla}]
            SET cModRegTim = [{cols['DFECMODREG']}] || ' ' || [{cols['CHORMODREG']}]
            WHERE cModRegTim IS NULL OR cModRegTim = ''
        """)
        # Borrar columnas antiguas
        try:
            cursor.execute(f"ALTER TABLE [{tabla}] DROP COLUMN [{cols['DFECMODREG']}]")
            cursor.execute(f"ALTER TABLE [{tabla}] DROP COLUMN [{cols['CHORMODREG']}]")
        except sqlite3.OperationalError:
            pass

    # Mover Nik si existe la vieja
    if "CNIKMODREG" in cols:
        cursor.execute(f"UPDATE [{tabla}] SET cModRegNik = [{cols['CNIKMODREG']}] WHERE cModRegNik IS NULL")
        try:
            cursor.execute(f"ALTER TABLE [{tabla}] DROP COLUMN [{cols['CNIKMODREG']}]")
        except sqlite3.OperationalError:
            pass

def DbfCreSQLite_ModClm():
    Ini_SQL_Dir = _Mem.get('Ini_SQL_Dir')
    print(f"--- SISTEMA YOS: NORMALIZACIÓN TOTAL (Nik + Tim) ---")
    print(f"Tim - {datetime.now().strftime('%Y%m%d %H:%M:%S')} | Bin >\n")

    if not os.path.exists(Ini_SQL_Dir):
        print(f"[ERROR] No se encuentra la carpeta {Ini_SQL_Dir}")
        return

    unidades = [f for f in os.listdir(Ini_SQL_Dir) if f.endswith('.Bdt')]

    for unidad in unidades:
        ruta = os.path.join(Ini_SQL_Dir, unidad)

        print(f"Patrullando: {unidad}")
        conn = sqlite3.connect(ruta)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tablas = [t[0] for t in cursor.fetchall()]

        for tabla in tablas:
            # Unificar auditoría primero
            DbfCreSQLite_ModClm_ModReg(cursor, tabla)

            # Renombrar el resto
            cursor.execute(f"PRAGMA table_info({tabla})")
            for col in cursor.fetchall():
                nom_old = col[1]
                nom_new = DbfCreSQLite_ModClm_Nom(nom_old)
                if nom_old != nom_new:
                    try:
                        cursor.execute(f"ALTER TABLE {tabla} RENAME COLUMN {nom_old} TO {nom_new}")
                        print(f"  [OK] {tabla}: {nom_old} -> {nom_new}")
                    except sqlite3.OperationalError:
                        pass

        conn.commit()
        conn.close()
    print(f"\n--- OPERACIÓN FINALIZADA CON ÉXITO ---")
# FIN - Arreglo nombre la esctruturas

def DbfCreSQLite_IptAll():
    print("CONVERTIDOR DE Dbf A SQLite en BLOQUE")

    Mem_Sql = os.path.join(_Mem.get('Ini_SQL_Dir'), "YosSis.Bdt")
    Mem_Dbf = os.path.join(_Mem.get('Ini_Dbf_Dir'), "Sis") + os.sep
    if DbfCreSQLite_Ipt('IMPORTAR Dbf.Sis A YosSis',Mem_Sql, Mem_Dbf) == "Err":
        return

    Mem_Sql = os.path.join(_Mem.get('Ini_SQL_Dir'), "YosMsi.Bdt")
    Mem_Dbf = os.path.join(_Mem.get('Ini_Dbf_Dir'), "Msi") + os.sep
    DbfCreSQLite_Ipt('IMPORTAR Dbf.Msi A YosMsi',Mem_Sql, Mem_Dbf)

    Mem_Sql = os.path.join(_Mem.get('Ini_SQL_Dir'), "YosMrp.Bdt")
    Mem_Dbf = os.path.join(_Mem.get('Ini_Dbf_Dir'), "Mrp") + os.sep
    DbfCreSQLite_Ipt('IMPORTAR Dbf.Mrp A YosMrp',Mem_Sql, Mem_Dbf)

    Mem_Sql = os.path.join(_Mem.get('Ini_SQL_Dir'), "YosMae.Bdt")
    Mem_Dbf = os.path.join(_Mem.get('Ini_Dbf_Dir'), "Mae") + os.sep
    DbfCreSQLite_Ipt('IMPORTAR Dbf.Mae A YosMae',Mem_Sql, Mem_Dbf)

    Mem_Sql = os.path.join(_Mem.get('Ini_SQL_Dir'), "YosDat.Bdt")
    Mem_Dbf = os.path.join(_Mem.get('Ini_Dbf_Dir'), "Dat") + os.sep
    DbfCreSQLite_Ipt('IMPORTAR Dbf.Dat A YosDat',Mem_Sql, Mem_Dbf)

    Mem_Sql = os.path.join(_Mem.get('Ini_SQL_Dir'), "YosCfg.Bdt")
    Mem_Dbf = os.path.join(_Mem.get('Ini_Dbf_Dir'), "Cfg") + os.sep
    DbfCreSQLite_Ipt('IMPORTAR Dbf.Cfg A YCfg',Mem_Sql, Mem_Dbf)

def DbfCreSQLite():
    # pongo valores en la Gaveta
    _Mem['Ini_SQL_Dir'] = os.path.join(YosAplCfg["Apl"]["Dir_Bdt"]) + "Dbf" + os.sep
    _Mem['Ini_Dbf_Dir'] = os.path.join(YosAplCfg["Apl"]["Dir_Bdt"]) + "Dbf" + os.sep

    # DEFINO EL MENU A USAR
    MenuDef = {
        '0010': {
            'Txt': 'ENTORNO',
            'Sub': {
                '0090': {'Txt': 'SALIR',               'Fnc': '«AppSld»',                'Cod': 'MnuIte'}
            }
        },

        '0100': {
            'Txt': 'CONVERTIR DE .Dbf A SQLite',
            'Sub': {
                '0110': {'Txt': 'IMPORTAR Dbf.Sis A YosSis',    'Fnc': 'Dbf.Sis',   'Cod': 'MnuIte'},
                '0120': {'Txt': 'IMPORTAR Dbf.Msi A YosMsi',    'Fnc': 'Dbf.Msi',   'Cod': 'MnuIte'},
                '0130': {'Txt': 'IMPORTAR Dbf.Mrp A YosMrp',    'Fnc': 'Dbf.Mrp',   'Cod': 'MnuIte'},
                '0140': {'Txt': 'IMPORTAR Dbf.Mae A YosMae',    'Fnc': 'Dbf.Mae',   'Cod': 'MnuIte'},
                '0150': {'Txt': 'IMPORTAR Dbf.Dat A YosDat',    'Fnc': 'Dbf.Dat',   'Cod': 'MnuIte'},
                '0160': {'Txt': 'IMPORTAR Dbf.Cfg A YosCfg',    'Fnc': 'Dbf.Cfg',   'Cod': 'MnuIte'},
                '0170': {'Txt': '--------------------------',   'Fnc': '',          'Cod': 'Sep'},
                '0180': {'Txt': 'IMPORTAR TODOS',               'Fnc': 'Todos',     'Cod': 'MnuIte'},
            }
        },

        '0200': {
            'Txt': 'HERRAMIENTAS',
            'Sub': {
                '0210': {'Txt': 'Normalizar Clm',   'Fnc': 'Normalizar',    'Cod': 'MnuIte'},
            }
        },
    }

    # INICIO - Proceso del menu
    while True:
        MnuFnc = Yos.Yos_Mnu(Mnu=MenuDef, MnuNom="__local__")   # "__local__" el menu esta dentro del .py

        match MnuFnc:
            case "«AppSld»": # Salir al Menú Anterior
                os.system('cls')
                break
            case "Dbf.Sis":
                Mem_Sql = os.path.join(_Mem.get('Ini_SQL_Dir'), "YosSis.Bdt")
                Mem_Dbf = os.path.join(_Mem.get('Ini_Dbf_Dir'), "Sis") + os.sep
                DbfCreSQLite_Ipt('IMPORTAR Dbf.Sis A YosSis',Mem_Sql, Mem_Dbf)

            case "Dbf.Msi":
                Mem_Sql = os.path.join(_Mem.get('Ini_SQL_Dir'), "YosMsi.Bdt")
                Mem_Dbf = os.path.join(_Mem.get('Ini_Dbf_Dir'), "Msi") + os.sep
                DbfCreSQLite_Ipt('IMPORTAR Dbf.Msi A YosMsi',Mem_Sql, Mem_Dbf)

            case "Dbf.Mrp":
                Mem_Sql = os.path.join(_Mem.get('Ini_SQL_Dir'), "YosMrp.Bdt")
                Mem_Dbf = os.path.join(_Mem.get('Ini_Dbf_Dir'), "Mrp") + os.sep
                DbfCreSQLite_Ipt('IMPORTAR Dbf.Mrp A YosMrp',Mem_Sql, Mem_Dbf)

            case "Dbf.Mae":
                Mem_Sql = os.path.join(_Mem.get('Ini_SQL_Dir'), "YosMae.Bdt")
                Mem_Dbf = os.path.join(_Mem.get('Ini_Dbf_Dir'), "Mae") + os.sep
                DbfCreSQLite_Ipt('IMPORTAR Dbf.Mae A YosMae',Mem_Sql, Mem_Dbf)

            case "Dbf.Dat":
                Mem_Sql = os.path.join(_Mem.get('Ini_SQL_Dir'), "YosDat.Bdt")
                Mem_Dbf = os.path.join(_Mem.get('Ini_Dbf_Dir'), "Dat") + os.sep
                DbfCreSQLite_Ipt('IMPORTAR Dbf.Dat A YosDat',Mem_Sql, Mem_Dbf)

            case "Dbf.Cfg":
                Mem_Sql = os.path.join(_Mem.get('Ini_SQL_Dir'), "YosCfg.Bdt")
                Mem_Dbf = os.path.join(_Mem.get('Ini_Dbf_Dir'), "Cfg") + os.sep
                DbfCreSQLite_Ipt('IMPORTAR Dbf.Cfg A YCfg',Mem_Sql, Mem_Dbf)

            case "Todos":
                DbfCreSQLite_IptAll()
#                Yos.Yos_RunFunFlo("DbfCreSQLite_IptAll")

            case "Normalizar":
                DbfCreSQLite_ModClm()
                #Yos.Yos_RunFunFlo("DbfCreSQLite_ModClm")    # Como se puede poner en varios programas se llama así, no importa al nombre de la aplicación


    # FIN - Proceso del menu

"""
{
'SQLITE_Tmp': 'D:\\_YosPrg\\YosMnu\\Bdt\\Dbf\\YosTmp.Bdt',
'Dbf_Tmp': 'D:\\_YosPrg\\YosMnu\\Bdt\\Dbf\\Tmp',

'SQLITE_Ycl': 'D:\\_YosPrg\\YosMnu\\Bdt\\Dbf\\YosYcl.Bdt',
'Dbf_Ycl': 'D:\\_YosPrg\\YosMnu\\Bdt\\Dbf\\Ycl',
    }
"""
