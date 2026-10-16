#!/usr/bin/env python3
# -*- coding: utf-8 -*

import sys
import os

from Yos import FrmWit

"""
   Idd_BdtSvr.py
   ACCESO AL SERVIDOR

   Copyright (c) 2026 Miguel Tortosa

   Licenciado bajo la Licencia MIT.

   Consulte el archivo LICENCIA en la raíz del proyecto para más información.
"""
"""
    | Motor de BD   | Librería Python   | Tipo          | Portabilidad
    | MariaDB/MySQL | pymysql           | Python Puro   | Excelente (Win, Linux, Mac)
    | PostgreSQL    | pg8000            | Python Puro   | Excelente (Win, Linux, Mac)
    | MsSQL         | pypyodbc          | Python Puro   | Buena (Requiere Driver ODBC)
    | Dbf           | dbfread           | Python Puro   | Excelente (Win, Linux, Mac)

    para SQLite, Solo cuando Creamos la Base de Datos
    -- 1. Activamos el modo WAL en la sesión actual de la base de datos abierta
    PRAGMA journal_mode = WAL;
    -- 2. Ajustamos la sincronización a NORMAL para optimizar la velocidad en disco junto con WAL
    PRAGMA synchronous = NORMAL;

    # Servidores
    | Sis | SISTEMA              | MODIFICA YosCtr
    | Msi | MAESTROS DEL SISTEMA | MODIFICA ADMINISTRADORES
    | Mrp | MAESTROS DEL GRUPO   | MODIFICA USUARIOS
    | Mae | MAESTROS             | MODIFICA USUARIOS
    | Dat | DATOS EMPRESA        | MODIFICA USUARIOS
    | Ach | ARCHIVOS             | MODIFICA AUTORIZADOS EN EL SERVIDOR
    | Tmp | TEMPORAL             | DIRECTORIO TEMPORAL %Tmp% del sistema
    | Ext | EXTERNO DEL SISTEMA  | MODIFICA USUARIOS

    | YosAplCfg["Bdt_Xxx_Tip"] | YosAplCfg["Bdt_Xxx_Dir"] | YosAplCfg["Bdt_Xxx_Usr"] | YosAplCfg["Bdt_Xxx_Pas"] | YosAplCfg["Bdt_Xxx_Dbt"]
    | SQLite                   | Direccion Local o Red    |                          |                          |
    | PostgreSQL               | Ip:Puerto                | Usuario                  | Contraseña               |
    | MariaDB                  | Ip:Puerto                | Usuario                  | Contraseña               |
    | MSSQL                    | Ip:Puerto                | Usuario                  | Contraseña               | Registro
    | Ach                      | Direccion Local o Red    |                          |                          |

    | Xxx |
    | Sis | YosAplCfg["Bdt_Sis_Dbt"] | YosAplCfg["Bdt_Sis_Dir"] | YosAplCfg["Bdt_Sis_Usr"] | YosAplCfg["Bdt_Sis_Pas"] |
    | Msi | YosAplCfg["Bdt_Msi_Dbt"] | YosAplCfg["Bdt_Msi_Dir"] | YosAplCfg["Bdt_Msi_Usr"] | YosAplCfg["Bdt_Msi_Pas"] |
    | Mrp | YosAplCfg["Bdt_Mrp_Dbt"] | YosAplCfg["Bdt_Mrp_Dir"] | YosAplCfg["Bdt_Mrp_Usr"] | YosAplCfg["Bdt_Mrp_Pas"] |
    | Mae | YosAplCfg["Bdt_Mae_Dbt"] | YosAplCfg["Bdt_Mae_Dir"] | YosAplCfg["Bdt_Mae_Usr"] | YosAplCfg["Bdt_Mae_Pas"] |
    | Dat | YosAplCfg["Bdt_Dat_Dbt"] | YosAplCfg["Bdt_Dat_Dir"] | YosAplCfg["Bdt_Dat_Usr"] | YosAplCfg["Bdt_Dat_Pas"] |
    | Ach | YosAplCfg["Bdt_Ach_Dbt"] | YosAplCfg["Bdt_Ach_Dir"] | Direccion donde estan guardaddos varios archivos que usa la aplicacion
    | Tmp |                          | YosAplCfg["Apl"]["Tmp"]  | En el directorio Temporal de la Computadora
    | Ext | Pendiete de revision o ponerlo en la aplicación


    Base de Datos de Configuracion
    YosCfg esta en el directorio Bdt de la aplicacion y tiene dos tablas
        Apl - (1 solo Registro, se copiarande la YosSis.AplCfg ) Los Datos que definen a la Aplicacion
        Dat - Valores necesarios para la aplicacion que se definen durante la programacion

Ahora empezaremos con el script Idd_BdtSvr.py y tendrá las siguientes def
- Cnx - conexión a la base de datos
- Sel - Select único
- SelMul - Select de Transacción
- Cie - Cerrar la conexión

"""

def Idd_BdtSvr_Cnx(Fnc_Svr, Fnc_Mod="ro"):
    # Conexion
    if YosAplCfg["Apl"]["Dbg"] == "S":
        print(f'Dbg -> Idd_BdtSvr_Cnx("{Fnc_Svr}", {Fnc_Mod})')

    match Fnc_Mod:
        case "ro": # YosCfg SIEMPRE es SQLite y esta en YosAplCfg["Apl"]["Dir_Bdt"]
            pass
        case "rw":
            pass
        case _:
            Fnc_Mod="ro"

    if not YosAplCfg["Apl"][f"Bdt_{Fnc_Svr}_Dir"]:
        Yos.Yos_MsgSis(Txt=f"LA DIRECCIÓN DE SERVIDOR {Fnc_Svr} ESTA VACÍA.", Tip="Err")
        Yos.FrmWit()
        sys.exit(1)
        return None

    match YosAplCfg["Apl"][f"Bdt_{Fnc_Svr}_Tip"]:
        case "SQLite":
            Mem_Dir = YosAplCfg["Apl"][f"Bdt_{Fnc_Svr}_Dir"]
            Mem_Dir = os.path.join(Mem_Dir, Fnc_Svr + ".Bdt")
        case _:
            Mem_Dir = YosAplCfg["Apl"][f"Bdt_{Fnc_Svr}_Dir"]

    if YosAplCfg["Apl"]["Dbg"] == "S":
        print(f'Dbg -> Mem_Dir={Mem_Dir}')

    Mem_Cnx = {
        "Svr": Fnc_Svr,
        "Tip": YosAplCfg["Apl"][f"Bdt_{Fnc_Svr}_Tip"],
        "Dir": Mem_Dir,
        "Usr": YosAplCfg["Apl"][f"Bdt_{Fnc_Svr}_Usr"],
        "Pas": YosAplCfg["Apl"][f"Bdt_{Fnc_Svr}_Pas"],
        "Bdt": YosAplCfg["Apl"][f"Bdt_{Fnc_Svr}_Bdt"],
        "Obs": YosAplCfg["Apl"][f"Bdt_{Fnc_Svr}_Obs"]
    }

    if YosAplCfg["Apl"]["Dbg"] == "S":
        print("Dbg ->")
        print("--------------------------------------------------")
        print("Mem_Cnx")
        print("--------------------------------------------------")
        print("\n".join([f"{k}: {v}" for k, v in Mem_Cnx.items()]))
        print("--------------------------------------------------")
        Yos.FrmWit()

    try:
        match Mem_Cnx['Tip']:
            case "SQLite":
                # Validamos existencia física
                if not os.path.exists(Mem_Cnx['Dir']):
                    Mem_Txt = f"ATENCION: NO EXISTE LA BASE DE DATOS : {Mem_Cnx['Dir']}"
                    Yos.Yos_MsgSis(Txt=Mem_Txt, Tip="Avs")
                    Idd_BdtSvr_Cre(Mem_Cnx)

                    Mem_Txt = f"SE HA CREADO LA BASE DE DATOS : {Fnc_Svr}"
                    Yos.Yos_MsgSis(Txt=Mem_Txt, Tip="Avs")

                    Mem_Txt = "REVISE LOS DATOS DE LA APLICACION"
                    Yos.Yos_MsgSis(Txt=Mem_Txt, Tip="Avs")
                    FrmWit()
                    #sys.exit(1)
                    #return None

                uri_path = f"file:{Mem_Cnx['Dir']}?mode={Fnc_Mod}"
#                print(uri_path)

                import sqlite3
                conn = sqlite3.connect(uri_path, uri=True, timeout=5000)
                conn.row_factory = sqlite3.Row

                # 2. INYECTAMOS EL MODO WAL EN LA CONEXIÓN ACTIVADA
                conn.execute("PRAGMA journal_mode = WAL;")
                conn.execute("PRAGMA synchronous = NORMAL;")

                return conn

                try:
                    # uri=True es obligatorio para que SQLite interprete el modo
                    conn = sqlite3.connect(uri_path, uri=True)
                    conn.row_factory = sqlite3.Row
                    return conn

                except sqlite3.Error as e:
                    print(f"Error al conectar en modo {'Lectura' if pSoloLectura else 'Escritura'}: {e}")
                    FrmWit()
                    sys.exit(1)
                    return None

            case "PostgreSQL":
                print("PostgreSQL")

            case "MsSQL":
                import pypyodbc as pyodbc
                SvrDir = (
                    "DRIVER={ODBC Driver 18 for SQL Server};"
                    f"SERVER={Mem_Cnx['Dir']};"
                    f"DATABASE={Mem_Cnx['Bdt']};"
                    f"UID={Mem_Cnx['Usr']};"
                    f"PWD={Mem_Cnx['Pas']};"
                    "Encrypt=yes;"
                    "TrustServerCertificate=yes;"
                )

                try:
                    conn = pyodbc.connect(SvrDir)
                except pyodbc.Error as e:
                    # Extraemos el código de error y el mensaje
                    sqlstate = e.args[0]
                    # Imprimimos con honor: Bin >
                    print(f"001. ERROR DE SQL (Estado {sqlstate}):")
                    print(f"     Detalle: {e.args[1]}")
                    conn = None  # Aseguramos que la variable no quede con basura

                return conn

            case "MariaDB":
                print("MariaDB")

            case _:
                print(f"SERVIDOR {Fnc_Svr} TIPO {Mem_Cnx['Tip']} NO IMPLEMENTADO")
                FrmWit()
                sys.exit(1)
                return None

    except Exception as Err:
        print(f"Error de CONEXION A {Fnc_Svr} TIPO {Mem_Cnx['Tip']} : {Err}")
        FrmWit()
        sys.exit(1)
        return None

#def Sel(Fnc_Cur, Fnc_Sel):
#    # Fnc_Sel ahora es el SQL que mandas desde afuera
#    # Cuando Sql solo devuelve un registro o mensaje
#    try:
#        Fnc_Cur.execute(Fnc_Sel)
#        return Fnc_Cur.fetchone()

#    except Exception as Err:
#        print(f"Error en Sel: {Err}")
#        return None

def Sel(Fnc_Cur, Fnc_Sql, pParams=()):
    # 1. Convertimos a mayúsculas para buscar palabras clave
    sql_upper = Fnc_Sql.strip().upper()

    try:
        Fnc_Cur.execute(Fnc_Sql, pParams)

        # 2. Verificamos si es un comando de acción
        es_accion = any(sql_upper.startswith(word) for word in ["INSERT", "UPDATE", "DELETE", "CREATE", "DROP"])

        if es_accion:
            # Si tu conexión no tiene autocommit, lo forzamos aquí
            # Nota: Necesitarías acceso al objeto conexión o ejecutar COMMIT directamente
            Fnc_Cur.execute("COMMIT;")
            print(f"1. [SQL] Acción ejecutada y confirmada (COMMIT).")
            return True
        else:
            # Si es un SELECT, devolvemos el registro único
            return Fnc_Cur.fetchone()

    except Exception as Err:
        print(f"2. [Error en Sel]: {Err}")
        return None

def SelTot(Fnc_Cur, Fnc_Sql, pParams=()):
    # Cuando Sql solo devuelve VARIOS registros
    """
    Lee TODOS los registros de una consulta.
    Fnc_Cur: El cursor activo.
    Fnc_Sql: La sentencia SQL (ej. "SELECT * FROM MiTabla").
    """
    try:
        Fnc_Cur.execute(Fnc_Sql, pParams)
        # fetchall() devuelve una lista con todas las filas
        return Fnc_Cur.fetchall()

    except Exception as e:
        print(f"Error en SelTodo: {e}")
        return []

def SelMul():
    # Transaccion
    pass

def Cie(Fnc_Cnx):
    """
    Cierra la conexión de forma segura.
    Fnc_Cnx: El objeto de conexión que recibiste de Idd_BdtSvr_Cnx().
    """
    if Fnc_Cnx:
        try:
            # Cerramos la conexión
            Fnc_Cnx.close()
        except Exception as e:
            print(f"Error al cerrar la conexión: {e}")

def IptSql(Fnc_Ach, Fnc_Cnx, Fnc_Dat=None):
    """
    Lee un archivo .sql desde el directorio Yos/Sql
    """
    Mem_Dat = os.path.join(YosAplCfg["Yos"]["Dir"], "Sql", Fnc_Ach + ".sql")
    Mem_Sql = os.path.abspath(Mem_Dat)

    try:
        with open(Mem_Sql, 'r', encoding='utf-8') as archivo:
            Mem_Contenido = archivo.read()

            # Si enviamos un diccionario de datos, aplicamos el formato (la "f")
            if Fnc_Dat:
                return Mem_Contenido.format(**Fnc_Dat)

            return Mem_Contenido

    except FileNotFoundError:
        input(f"ERROR: No se encontró el archivo SQL en: {Mem_Sql}")
        Cie(Fnc_Cnx)
        Mem_Sql = os.path.join(YosAplCfg["Apl"]["Dir_Bdt"], "YosCfg.Bdt")
        os.remove(Mem_Sql)
        import sys
        sys.exit(0)
        return "Err"

def Idd_BdtSvr_Cre(Fnc_Cnx):
    # Crea las tablas NECESARIOS de el servidor y sus datos iniciales
    # Servidor, Tabla (Vacio=todas)
    """
                Mem_Cnx = {
                "Svr": Fnc_Svr,
                "Tip": "SQLite",
                "Dir": os.path.join(YosAplCfg["Yos"]["Dir"], "_Bdt", Fnc_Svr + ".Bdt"),
                "Usr": "",
                "Pas": "",
                "Bdt": "",
                "Obs": ""
            }
    """
    # De momento Solo YosCfg, YosLib
    match Fnc_Cnx['Svr']:
        case "YosCfg":
            pass
        case "YosLib":
            pass
        case _:
            return "Err"

    print("Fnc_Cnx")
    print("--------------------------------------------------")
    print("\n".join([f"{k}: {v}" for k, v in Fnc_Cnx.items()]))
    print("--------------------------------------------------")
    FrmWit()

    # FrmWit(Fnc_Txt="",Fnc_Wit=0):
    import sqlite3
    Mem_Cnx_YosCfg = sqlite3.connect(Fnc_Cnx['Dir'])
    Mem_Cnx_YosCfg.row_factory = sqlite3.Row

    Mem_Cur_YosCfg = Mem_Cnx_YosCfg.cursor()

    # Verifico que las tablas de Yos.cfg SQLite

    # De momento Solo YosCfg, YosLib
    match Fnc_Cnx['Svr']:
        case "YosCfg":
            Idd_BdtSvr_Cre_Tab("Apl", Mem_Cnx_YosCfg, Mem_Cur_YosCfg)
            Idd_BdtSvr_Cre_Reg("Apl", "YosCfg", Mem_Cnx_YosCfg, Mem_Cur_YosCfg)

            Idd_BdtSvr_Cre_Tab("Bdt", Mem_Cnx_YosCfg, Mem_Cur_YosCfg)
#            Idd_BdtSvr_Cre_Reg("Bdt", "YosCfg", Mem_Cnx_YosCfg, Mem_Cur_YosCfg)

            Idd_BdtSvr_Cre_Tab("Dat", Mem_Cnx_YosCfg, Mem_Cur_YosCfg)
            Idd_BdtSvr_Cre_Reg("Dat", "YosCfg", Mem_Cnx_YosCfg, Mem_Cur_YosCfg)

            Idd_BdtSvr_Cre_Tab("Mnu", Mem_Cnx_YosCfg, Mem_Cur_YosCfg)
            Idd_BdtSvr_Cre_Reg("Mnu", "YosCfg", Mem_Cnx_YosCfg, Mem_Cur_YosCfg)

            Idd_BdtSvr_Cre_Tab("Ord", Mem_Cnx_YosCfg, Mem_Cur_YosCfg)
            Idd_BdtSvr_Cre_Reg("Ord", "YosCfg", Mem_Cnx_YosCfg, Mem_Cur_YosCfg)

            Idd_BdtSvr_Cre_Tab("Brw", Mem_Cnx_YosCfg, Mem_Cur_YosCfg)
            Idd_BdtSvr_Cre_Reg("Brw", "YosCfg", Mem_Cnx_YosCfg, Mem_Cur_YosCfg)

            Idd_BdtSvr_Cre_Tab("ClmMod", Mem_Cnx_YosCfg, Mem_Cur_YosCfg)
            Idd_BdtSvr_Cre_Reg("ClmMod", "YosCfg", Mem_Cnx_YosCfg, Mem_Cur_YosCfg)
            print("CONTRASEÑA DEL ADMINISTRADOR = Admin1967")

        case "YosLib":
            Idd_BdtSvr_Cre_Tab("Bdt", Mem_Cnx_YosCfg, Mem_Cur_YosCfg)
            Idd_BdtSvr_Cre_Reg("Bdt", "YosLib", Mem_Cnx_YosCfg, Mem_Cur_YosCfg)

            Idd_BdtSvr_Cre_Tab("Dat", Mem_Cnx_YosCfg, Mem_Cur_YosCfg)
#            Idd_BdtSvr_Cre_Reg("Dat", "YosLib", Mem_Cnx_YosCfg, Mem_Cur_YosCfg)

            Idd_BdtSvr_Cre_Tab("Ord", Mem_Cnx_YosCfg, Mem_Cur_YosCfg)
            Idd_BdtSvr_Cre_Reg("Ord", "YosCfg", Mem_Cnx_YosCfg, Mem_Cur_YosCfg)


            Idd_BdtSvr_Cre_Tab("Brw", Mem_Cnx_YosCfg, Mem_Cur_YosCfg)
            Idd_BdtSvr_Cre_Reg("Brw", "YosCfg", Mem_Cnx_YosCfg, Mem_Cur_YosCfg)

            Idd_BdtSvr_Cre_Tab("ClmMod", Mem_Cnx_YosCfg, Mem_Cur_YosCfg)
            Idd_BdtSvr_Cre_Reg("ClmMod", "YosCfg", Mem_Cnx_YosCfg, Mem_Cur_YosCfg)


def Idd_BdtSvr_Cre_Tab(Mem_Tab, Mem_Cnx_YosCfg, Mem_Cur_YosCfg):
    print(f"Creando {Mem_Tab}")
    Mem_Sql = IptSql(f"{Mem_Tab}_Cre", Mem_Cnx_YosCfg)
    Mem_Dat = SelTot(Mem_Cur_YosCfg, Mem_Sql)
    Mem_Cnx_YosCfg.commit()

def Idd_BdtSvr_Cre_Reg(Mem_Tab, Mem_Svr, Mem_Cnx_YosCfg, Mem_Cur_YosCfg):
    from datetime import datetime
    # Creo un diccionario para las sustituciones del .sql
    input(YosAplCfg["Apl"]["Apl"])
    Mem_Dic = {
        "Mem_Ini_AplNom": Mem_Ini_AplNom,
        "Mem_Vsn": datetime.now().strftime("%Y.%m"),
        "Mem_Cpy": datetime.now().strftime("%Y")+" © Miguel Tortosa",
        "Usr": "YosCfg",
        "DateTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "«Apl_Apl»": YosAplCfg["Apl"]["Apl"],
        "«Apl_Etn»": Mem_Ini_AplEtn,
    }
    Mem_Sql = IptSql(f"{Mem_Tab}_{Mem_Svr}", Mem_Cnx_YosCfg, Mem_Dic)
    print(Mem_Sql)
    Mem_Dat = SelTot(Mem_Cur_YosCfg, Mem_Sql)
    Mem_Cnx_YosCfg.commit()
