#!/usr/bin/env python3
# -*- coding: utf-8 -*
"""
Datos de Configuraacion de la Aplicacion

@author: Miguel Tortosa
"""
import sys
import os
import string
import random
import shelve
import builtins # Lo usamos para poder usar una VARIABLES GLOBAL
import platform
from datetime import datetime
import tempfile
import json

import Yos

def GenNomAch(longitud=10, Prefijo= "YosCfg_"):
    """Genera un nombre de archivo aleatorio con letras y números."""
    caracteres = string.ascii_letters + string.digits # Letras (mayús/minús) y números
    nombre_base = ''.join(random.choice(caracteres) for i in range(longitud))
    return f"{Prefijo}{nombre_base}"

def Yos_Cfg():
    global YosCfg
    YosCfg = {}   # Datos Libreria Yos

    Yos.Yos_MsgSis(Txt= "INICIALIZANDO Yos_Cfg().")

    # Recupero datos YosLib YosAplCfg.Yos
    Yos_Cfg_YosLib()

    # DATOS DE LA APLICACION ORIGINAL
    YosAplCfg_Def["Apl"]["Ori_Cod"] = "(Ro) Codigo  REAL de la Aplicacion"
    YosAplCfg_Def["Apl"]["Ori_Nom"] = "(Ro) Nombre  REAL de la Aplicacion"
    YosAplCfg_Def["Apl"]["Ori_Etn"] = "(Ro) Entorno REAL de la Aplicacion"
    if YosAplCfg["Apl"]["Ori_Etn"] == "Gui":
        YosAplCfg["Apl"]["Ori_EtnNom"]  = "NiceGui"
    elif YosAplCfg["Apl"]["Ori_Etn"] == "Tui":
        YosAplCfg["Apl"]["Ori_EtnNom"]  = "Textual"
    else:
        Yos.Yos_MsgSis(Txt=F'(Ro) EL ENTORNO DE LA APLICACIÓN ({YosAplCfg["Apl"]["Ori_Etn"]}) ES INCORRECTO. (YosAplCfg.Apl.Ori_Etn)', Tip= "Err")
        Yos.FrmWit(Fnc_Wit=8)
        import sys
        sys.exit(0)
    YosAplCfg_Def["Apl"]["Ori_EtnNom"]  = "(Ro) Nombre del Entorno"


    # DATOS DE LA APLICACION
    #### Ro SOLO LECTURA
    YosAplCfg["Apl"]["Sis_Etn"]        = platform.system() # "Windows", "Linux", "Darwin"
    YosAplCfg_Def["Apl"]["Sis_Etn"]    = "(Ro) Sistema Operativo"
    YosAplCfg["Apl"]["Sis_EtnDes"]     = platform.platform()
    YosAplCfg_Def["Apl"]["Sis_EtnDes"] = "(Ro) Sistema Operativo Descripcion"
    YosAplCfg["Apl"]["Sis_Cpd"]        = platform.node()
    YosAplCfg_Def["Apl"]["Sis_Cpd"]    = "(Ro) Nombre de la computadora"

    YosAplCfg["Apl"]["Tmp"]     = tempfile.gettempdir()
    YosAplCfg_Def["Apl"]["Tmp"] = "(Ro) Directorio Temporal"

    YosAplCfg["Apl"]["Atv"]     = os.path.basename(os.getcwd())
    YosAplCfg_Def["Apl"]["Atv"] = "(Ro) Programa actual en Curso"

    YosAplCfg["Apl"]["Etn_Lon"]     = 0
    YosAplCfg_Def["Apl"]["Etn_Lon"] = "(Ro) Entorno Tui, Ancho de la pantalla (WX) (Width)(Longitud)"
    YosAplCfg["Apl"]["Etn_Alt"]     = 0
    YosAplCfg_Def["Apl"]["Etn_Alt"] = "(Ro) Entorno Tui, Alto de la pantalla (HY) (Height)"

    YosAplCfg["Apl"]["Rot"]     = ""
    YosAplCfg_Def["Apl"]["Rot"] = "(Ro) Entorno Txt, Rotulo del nombre de la Aplicacion"
    YosAplCfg["Apl"]["Cab"]     = ""
    YosAplCfg_Def["Apl"]["Cab"] = "(Ro) Entorno Txt, Cabecera, Rotulo + Datos de la aplicacion"

    YosAplCfg["Apl"]["Dir"]      = os.getcwd()  +"\\"
    YosAplCfg_Def["Apl"]["Dir"]  = "(Ro) Directorio de la Aplicacion"
    YosAplCfg["Apl"]["DirNom"]    = os.path.basename(YosAplCfg["Apl"]["Dir"].rstrip("\\")) # Solo el Nombre del Directorio
    YosAplCfg_Def["Apl"]["DirNom"]  = "(Ro) Directorio de la Aplicacion solo"
    YosAplCfg["Apl"]["Dir_Bdt"]   = YosAplCfg["Apl"]["Dir"] +"Bdt\\"
    YosAplCfg_Def["Apl"]["Dir_Bdt"]   = "(Ro) Directorio Bdt bases de datos"

    YosAplCfg["Apl"]["Mnu"]        = ""
    YosAplCfg_Def["Apl"]["Mnu"]    = "(Ro) Menu de la Aplicacion"
    YosAplCfg["Apl"]["MnuNom"]     = ""
    YosAplCfg_Def["Apl"]["MnuNom"] = "(Ro) Nombre del menu en uso"
    YosAplCfg["Apl"]["TitSub"]     = ""
    YosAplCfg_Def["Apl"]["TitSub"] = "(Ro) Muestra TITUTLO DEL SCRIPT , nombre del Script, Es para el menu"

    YosAplCfg["Apl"]["Fnc"]     = []
    YosAplCfg_Def["Apl"]["Fnc"] = "(Ro) Lista de las Funciones de ./Script/*.py de la Aplicacion"

    # Usuario
    YosAplCfg["Apl"]["Usr_Nik"]     = ""
    YosAplCfg_Def["Apl"]["Usr_Nik"] = "(Ro) Nick del Usuario"
    YosAplCfg["Apl"]["Usr_Nom"]     = ""
    YosAplCfg_Def["Apl"]["Usr_Nom"] = "(Ro) Nombre del Usuario"
    YosAplCfg["Apl"]["Usr_Pas"]     = ""
    YosAplCfg_Def["Apl"]["Usr_Pas"] = "(Ro) Contraseña del Usuario"
    YosAplCfg["Apl"]["Usr_Niv"]     = ""
    YosAplCfg_Def["Apl"]["Usr_Niv"] = "(Ro) Nivel del Usuario"
    YosAplCfg["Apl"]["Usr_Ipd"]     = ""
    YosAplCfg_Def["Apl"]["Usr_Ipd"] = "(Ro) Direccion Ip del Usuario"

    #### Rw - Modificar en YosCfg.AplDef.Xxx - YosAplCfg["Apl"]["Xxx"]
    YosAplCfg["Apl"]["Dbg"] = ""
    YosAplCfg_Def["Apl"]["Dbg"] = "MODO DEPURACION (S/)"

    YosAplCfg["Apl"]["Apl"]     = os.path.basename(os.getcwd())
    YosAplCfg_Def["Apl"]["Apl"] = "Codigo de la Aplicacion, Por omision el directorio"

    YosAplCfg["Apl"]["Nom"]     = YosAplCfg["Apl"]["Apl"]
    YosAplCfg_Def["Apl"]["Nom"] = "Nombre de la Aplicacion"

    # YosAplCfg["Apl"]["Tit"]       = "" # TITULO de la Aplicacion ****  Se usa YosAplCfg["Apl"]["Apl_Nom"]       = "" # Nombre EXTENDIDO de la aplicacion

    if YosAplCfg["Apl"]["Ori_Etn"] == "Tui":
        YosAplCfg["Apl"]["Etn"]     = "Txt"
    else:
        YosAplCfg["Apl"]["Etn"]     = "Loc"
    YosAplCfg_Def["Apl"]["Etn"] = "Entorno Tui(Txt=Texto), Gui(Loc=Web Local, Www=Web), MAdre YosAplCfg.Apl.Ori_Etn"

    YosAplCfg["Apl"]["Etn_Let"]     = "dos_rebel" #"dos_rebel","banner3"#
    YosAplCfg_Def["Apl"]["Etn_Let"]  = "Entorno Txt, Tipo de letra para el Rotulo, Modulo pyfiglet"

    YosAplCfg["Apl"]["Vsn"]        = ""
    YosAplCfg_Def["Apl"]["Vsn"]    = "Version de la Aplicacion"
    YosAplCfg["Apl"]["Cpy"]        = "" # Copyright de la aplicacion
    YosAplCfg_Def["Apl"]["Cpy"]    = "Copyright de la aplicacion"
    YosAplCfg["Apl"]["CpyEml"]     = ""
    YosAplCfg_Def["Apl"]["CpyEml"] = "Email del Autor de la Aplicacion"
    YosAplCfg["Apl"]["Res"]        = ""
    YosAplCfg_Def["Apl"]["Res"]    = "Documento de DE RESPONSABILIDAD"

    # COLUMAS encriptadas
    YosAplCfg["Apl"]["Enc_nCos"]     = 12
    YosAplCfg_Def["Apl"]["Enc_nCos"] = "Factor de Costo de bcrypt.10 <= Enc_nCos <= 15 "
    # Omision Yos_81321 (Tamaño Md5=32 , Bcrypt=60 Contraseña Max=72)
    YosAplCfg["Apl"]["Enc_AdmPas"]     = "$2a$12$kXQ4P3waPzyKX9a3X4gOMu9VtqNV1ZQBHo8JH.r.vv4L6Wv0N4KaK"
    YosAplCfg_Def["Apl"]["Enc_AdmPas"] = "Contraseña del Administrador"

    YosAplCfg["Apl"]["DirAch"]     = ""
    YosAplCfg_Def["Apl"]["DirAch"] = "Directorio de Almacenaje donde se guardan los Archivos"

    # Datos de Usuario
    YosAplCfg["Apl"]["Usr_Acc"]     = "N"
    YosAplCfg_Def["Apl"]["Usr_Acc"] = "Control de Acceso por Usuario (S/N)"

    YosAplCfg["Apl"]["Usr_NumMaxAcc"] = 3
    YosAplCfg_Def["Apl"]["Usr_NumMaxAcc"] = "(n) Numero de intentos de Acceso del Usuario"

    # Datos Email
    YosAplCfg["Apl"]["Eml_Svr"]        = ""
    YosAplCfg_Def["Apl"]["Eml_Svr"]    = "Servidor SMTP"
    YosAplCfg["Apl"]["Eml_Puo"]        = 0
    YosAplCfg_Def["Apl"]["Eml_Puo"]    = "(n) PUERTO"
    YosAplCfg["Apl"]["Eml_Usr"]        = ""
    YosAplCfg_Def["Apl"]["Eml_Usr"]    = "CORREO USUARIO EMISOR"
    YosAplCfg["Apl"]["Eml_Pas"]        = ""
    YosAplCfg_Def["Apl"]["Eml_Pas"]    = "CONTRASEÑA USUARIO EMISOR"
    YosAplCfg["Apl"]["Eml_EmlEnv"]     = ""
    YosAplCfg_Def["Apl"]["Eml_EmlEnv"] = "EMAIL DE ENVIO"
    YosAplCfg["Apl"]["Eml_MsgCab"]     = ""
    YosAplCfg_Def["Apl"]["Eml_MsgCab"] = "CABECERA DEL MENSAJE"
    YosAplCfg["Apl"]["Eml_MsgPie"]     = ""
    YosAplCfg_Def["Apl"]["Eml_MsgPie"] = "PIE DEL MENSAJE"
    YosAplCfg["Apl"]["Eml_EmlDst"]     = ""
    YosAplCfg_Def["Apl"]["Eml_EmlDst"] = "EMAIL DESTINATARIO DE LA APLICACION"

    # DATOS WEB Www
    YosAplCfg["Apl"]["Www_Avs"]           = ""
    YosAplCfg_Def["Apl"]["Www_Avs"]       = "AVISO A PIE DE PAGINA"
    YosAplCfg["Apl"]["Www_Des"]           = ""
    YosAplCfg_Def["Apl"]["Www_Des"]       = "TITULO PRINCIPAL"
    YosAplCfg["Apl"]["Www_Des002"]        = ""
    YosAplCfg_Def["Apl"]["Www_Des002"]    = "SUBTÍTULO"
    YosAplCfg["Apl"]["Www_ImgDch"]        = ""
    YosAplCfg_Def["Apl"]["Www_ImgDch"]    = "IMAGEN DERECHA"
    YosAplCfg["Apl"]["Www_ImgDchWww"]     = ""
    YosAplCfg_Def["Apl"]["Www_ImgDchWww"] = "IMAGEN DERECHA ENLACE"
    YosAplCfg["Apl"]["Www_ImgIzq"]        = ""
    YosAplCfg_Def["Apl"]["Www_ImgIzq"]    = "IMAGEN IZQUIERDA"
    YosAplCfg["Apl"]["Www_ImgIzqWww"]     = ""
    YosAplCfg_Def["Apl"]["Www_ImgIzqWww"] = "IMAGEN IZQUIERDA ENLACE"
    YosAplCfg["Apl"]["Www_Puo"] = 8080
    YosAplCfg_Def["Apl"]["Www_Puo"]       = "(n) PUERTO DE WEB"
    YosAplCfg["Apl"]["Www_Not"]           = ""
    YosAplCfg_Def["Apl"]["Www_Not"]       = "GESTION DE NOTICIAS (S/)"

    # Imagenes "Img/"
    if YosAplCfg["Apl"]["Ori_Etn"] == "Gui":
        # Asigno los Directorios de Imaqenes, Tanto de Yos como de la Apl
        # Así, en tu código puedes llamar a /yos_img/... o /apl_img/...
        ruta_yos = os.path.normpath(os.path.join(YosAplCfg["Yos"]["Dir"], "Img"))
        ruta_apl = os.path.normpath(os.path.join(YosAplCfg["Apl"]["Dir"], "Img"))
        from nicegui import app
        app.add_static_files('/yos_img', ruta_yos)
        app.add_static_files('/apl_img', ruta_apl)

    # Bases de Datos "Bdt"
    # Sql "Sql"

    # Verificacion de los Bdt del sistema, Para modificar, definala en YosCfg.Bdt de su aplicacion.
    # YosLib
    Mem_Svr = "YosLib"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Tip"]        = "SQLite"
    YosAplCfg_Def["Apl"][f"Bdt_{Mem_Svr}_Tip"]    = "(Ro) Tipo de Servidor"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Dir"]        = os.path.abspath(os.path.join(YosAplCfg["Yos"]["Dir"], "Bdt")) # Esta en Yos
    YosAplCfg_Def["Apl"][f"Bdt_{Mem_Svr}_Dir"]    = "(Ro) Direccion del Servidor"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Usr"]        = ""
    YosAplCfg_Def["Apl"][f"Bdt_{Mem_Svr}_Usr"]    = "(Ro) Usuario"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Pas"]        = ""
    YosAplCfg_Def["Apl"][f"Bdt_{Mem_Svr}_Pas"]    = "(Ro) Contraseña"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Bdt"]        = ""
    YosAplCfg_Def["Apl"][f"Bdt_{Mem_Svr}_Bdt"]    = "(Ro) Base de Datos"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Obs"]        = "Esta en ./Yos/Bdt/, NO MODIFICAR NI CAMBIAR DE DIRECTORIO"
    YosAplCfg_Def["Apl"][f"Bdt_{Mem_Svr}_Obs"]    = "(Ro) Obsevaciones del Administrador"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_ObsSis"]     = "YosSis = TABLAS DE LA LIBRERIA Yos, NO MODIFICAR"
    YosAplCfg_Def["Apl"][f"Bdt_{Mem_Svr}_ObsSis"] = "(Ro) Obsevaciones del Sitema YosLib"

    # YosCfg
    Mem_Svr = "YosCfg"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Tip"]        = "SQLite"
    YosAplCfg_Def["Apl"][f"Bdt_{Mem_Svr}_Tip"]    = "Tipo de Servidor"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Dir"]        = os.path.abspath(os.path.join(YosAplCfg["Apl"]["Dir"], "Bdt")) # Esta en la propia aplicacion
    YosAplCfg_Def["Apl"][f"Bdt_{Mem_Svr}_Dir"]    = "Direccion del Servidor"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Usr"]        = ""
    YosAplCfg_Def["Apl"][f"Bdt_{Mem_Svr}_Usr"]    = "Usuario"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Pas"]        = ""
    YosAplCfg_Def["Apl"][f"Bdt_{Mem_Svr}_Pas"]    = "Contraseña"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Bdt"]        = ""
    YosAplCfg_Def["Apl"][f"Bdt_{Mem_Svr}_Bdt"]    = "Base de Datos"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Obs"]        = "Esta en DirAplicacion/Bdt/"
    YosAplCfg_Def["Apl"][f"Bdt_{Mem_Svr}_Obs"]    = "Obsevaciones del Administrador"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_ObsSis"]     = "(Ro) YosCfg = CONFIGURACION APLICACION (NO MOVER) , MODIFICA ADMINISTRADORES"
    YosAplCfg_Def["Apl"][f"Bdt_{Mem_Svr}_ObsSis"] = "(Ro) Obsevaciones del Sitema YosLib"

    # YosSis
    Mem_Svr = "YosSis"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Tip"]        = "SQLite"
    YosAplCfg_Def["Apl"][f"Bdt_{Mem_Svr}_Tip"]    = "Tipo de Servidor"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Dir"]        = os.path.abspath(os.path.join(YosAplCfg["Yos"]["Dir"], "Bdt")) # Esta en Yos
    YosAplCfg_Def["Apl"][f"Bdt_{Mem_Svr}_Dir"]    = "Direccion del Servidor"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Usr"]        = ""
    YosAplCfg_Def["Apl"][f"Bdt_{Mem_Svr}_Usr"]    = "Usuario"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Pas"]        = ""
    YosAplCfg_Def["Apl"][f"Bdt_{Mem_Svr}_Pas"]    = "Contraseña"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Bdt"]        = ""
    YosAplCfg_Def["Apl"][f"Bdt_{Mem_Svr}_Bdt"]    = "Base de Datos"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Obs"]        = "Esta en .\\Yos\\Bdt\\, para cambiar use la opcion de Migracion"
    YosAplCfg_Def["Apl"][f"Bdt_{Mem_Svr}_Obs"]    = "Obsevaciones del Administrador"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_ObsSis"]     = "YosSis = TABLAS DE LA LIBRERIA Yos, NO MODIFICAR"
    YosAplCfg_Def["Apl"][f"Bdt_{Mem_Svr}_ObsSis"] = "(Ro) Obsevaciones del Sitema YosLib"
    # YosMsi
    Mem_Svr = "YosMsi"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Tip"]        = "SQLite"
    YosAplCfg_Def["Apl"][f"Bdt_{Mem_Svr}_Tip"]    = "Tipo de Servidor"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Dir"]        = os.path.abspath(os.path.join(YosAplCfg["Yos"]["Dir"], "Bdt")) # Esta en Yos
    YosAplCfg_Def["Apl"][f"Bdt_{Mem_Svr}_Dir"]    = "Direccion del Servidor"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Usr"]        = ""
    YosAplCfg_Def["Apl"][f"Bdt_{Mem_Svr}_Usr"]    = "Usuario"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Pas"]        = ""
    YosAplCfg_Def["Apl"][f"Bdt_{Mem_Svr}_Pas"]    = "Contraseña"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Bdt"]        = ""
    YosAplCfg_Def["Apl"][f"Bdt_{Mem_Svr}_Bdt"]    = "Base de Datos"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Obs"]        = "Esta en .\\Yos\\Bdt\\, para cambiar use la opcion de Migracion"
    YosAplCfg_Def["Apl"][f"Bdt_{Mem_Svr}_Obs"]    = "Obsevaciones del Administrador"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_ObsSis"]     = "YosMsi = MAESTROS DEL SISTEMA Yos, MODIFICA ADMINISTRADORES"
    YosAplCfg_Def["Apl"][f"Bdt_{Mem_Svr}_ObsSis"] = "(Ro) Obsevaciones del Sitema YosLib"

    # YosMrp
    Mem_Svr = "YosMrp"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Tip"]        = "SQLite"
    YosAplCfg_Def["Apl"][f"Bdt_{Mem_Svr}_Tip"]    = "Tipo de Servidor"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Dir"]        = YosAplCfg["Apl"]["Dir_Bdt"]
    YosAplCfg_Def["Apl"][f"Bdt_{Mem_Svr}_Dir"]    = "Direccion del Servidor"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Usr"]        = ""
    YosAplCfg_Def["Apl"][f"Bdt_{Mem_Svr}_Usr"]    = "Usuario"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Pas"]        = ""
    YosAplCfg_Def["Apl"][f"Bdt_{Mem_Svr}_Pas"]    = "Contraseña"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Bdt"]        = ""
    YosAplCfg_Def["Apl"][f"Bdt_{Mem_Svr}_Bdt"]    = "Base de Datos"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Obs"]        = "Esta en DirAplicacion\\Bdt\\, para cambiar use la opcion de Migracion"
    YosAplCfg_Def["Apl"][f"Bdt_{Mem_Svr}_Obs"]    = "Obsevaciones del Administrador"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_ObsSis"]     = "YosMrp = MAESTROS DEL GRUPO (Son la tablas comunes a Varias Aplicaciones), MODIFICA USUARIOS"
    YosAplCfg_Def["Apl"][f"Bdt_{Mem_Svr}_ObsSis"] = "(Ro) Obsevaciones del Sitema YosLib"

    # YosMae
    Mem_Svr = "YosMae"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Tip"]        = "SQLite"
    YosAplCfg_Def["Apl"][f"Bdt_{Mem_Svr}_Tip"]    = "Tipo de Servidor"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Dir"]        = YosAplCfg["Apl"]["Dir_Bdt"]
    YosAplCfg_Def["Apl"][f"Bdt_{Mem_Svr}_Dir"]    = "Direccion del Servidor"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Usr"]        = ""
    YosAplCfg_Def["Apl"][f"Bdt_{Mem_Svr}_Usr"]    = "Usuario"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Pas"]        = ""
    YosAplCfg_Def["Apl"][f"Bdt_{Mem_Svr}_Pas"]    = "Contraseña"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Bdt"]        = ""
    YosAplCfg_Def["Apl"][f"Bdt_{Mem_Svr}_Bdt"]    = "Base de Datos"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Obs"]        = "Esta en DirAplicacion\\Bdt\\, para cambiar use la opcion de Migracion"
    YosAplCfg_Def["Apl"][f"Bdt_{Mem_Svr}_Obs"]    = "Obsevaciones del Administrador"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_ObsSis"]     = "YosMae = MAESTROS (Son la tablas comunes a Varias YosDat), MODIFICA USUARIOS"
    YosAplCfg_Def["Apl"][f"Bdt_{Mem_Svr}_ObsSis"] = "(Ro) Obsevaciones del Sitema YosLib"

    # YosDat
    Mem_Svr = "YosDatNnn"   # Nnn se sustituira por el nombre de la empresa
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Tip"]        = "SQLite"
    YosAplCfg_Def["Apl"][f"Bdt_{Mem_Svr}_Tip"]    = "Tipo de Servidor"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Dir"]        = YosAplCfg["Apl"]["Dir_Bdt"]
    YosAplCfg_Def["Apl"][f"Bdt_{Mem_Svr}_Dir"]    = "Direccion del Servidor"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Usr"]        = ""
    YosAplCfg_Def["Apl"][f"Bdt_{Mem_Svr}_Usr"]    = "Usuario"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Pas"]        = ""
    YosAplCfg_Def["Apl"][f"Bdt_{Mem_Svr}_Pas"]    = "Contraseña"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Bdt"]        = ""
    YosAplCfg_Def["Apl"][f"Bdt_{Mem_Svr}_Bdt"]    = "Base de Datos"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Obs"]        = "Esta en DirAplicacion\\Bdt\\, para cambiar use la opcion de Migracion"
    YosAplCfg_Def["Apl"][f"Bdt_{Mem_Svr}_Obs"]    = "Obsevaciones del Administrador"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_ObsSis"]     = "YosDatNnn = DATOS EMPRESA (Modulo Multiempresa Activo) , MODIFICA USUARIOS"
    YosAplCfg_Def["Apl"][f"Bdt_{Mem_Svr}_ObsSis"] = "(Ro) Obsevaciones del Sitema YosLib"

    # FIN - Verificacion de los Bdt del sistema, Para modificar, definala en YosCfg.Bdt de su aplicacion.

    ####################################################################################################### Recuperamos los datos de la Bases de datos YosCfg.Bdt
    Mem_Cnx_YosCfg = Yos.Idd_BdtSvr_Cnx("YosCfg")
    Mem_Cur_YosCfg = Mem_Cnx_YosCfg.cursor()

    ############################## Recuperamos los datos de la Tabla Bdt
    Mem_Sql = "SELECT * FROM Bdt"
    Mem_Dat = Yos.SelTot(Mem_Cur_YosCfg, Mem_Sql, pParams=())

    if Mem_Dat is None:
        Yos.Yos_MsgSis(Txt="La tabla YosCfg.Bdt está vacía.", Tip= "Avs")

    for Mem_Uni in Mem_Dat:
        # Acceso por nombre de columna
        Mem_Svr=Mem_Uni["cSvr"] #Mem_Uni["cSvr"][3:]
        YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Tip"]= Mem_Uni["cSvrTip"]
        YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Dir"]= Mem_Uni["cDir"]
        YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Usr"]= Mem_Uni["cUsr"]
        YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Pas"]= Mem_Uni["cPas"]
        YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Bdt"]= Mem_Uni["cBdt"]
        YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Obs"]= Mem_Uni["cObs"]

    ############################## Recuperamos los datos de las bases de datos YosCfg.Dat
    Mem_Sql = "SELECT * FROM YosAplCfg"
    Mem_Dat = Yos.SelTot(Mem_Cur_YosCfg, Mem_Sql, pParams=())

    if Mem_Dat is None:
        Yos.Yos_MsgSis(Txt="La tabla YosCfg.YosAplCfg está vacía.", Tip= "Avs")

    for Mem_Uni in Mem_Dat:
        # Acceso por nombre de columna

        """
        "cClm"  VARCHAR(60),
        "cDes"  VARCHAR(100),
        "cVal"  VARCHAR(253),
        "cObs"  VARCHAR(100),
        """

        Mem_Clm = Mem_Uni["cClm"]
        if "Apl" not in YosAplCfg or Mem_Clm not in YosAplCfg["Apl"]:
            Yos.Yos_MsgSis(Txt=f'YosCfg.YosAplCfg. NO EXISTE LA COLUMNA DE CONFIGURACION YosAplCfg["Apl"]["{Mem_Clm}"], SE IGNORA.', Tip= "Avs")
        elif YosAplCfg_Def["Apl"][Mem_Clm].startswith("(Ro)"):
            Yos.Yos_MsgSis(Txt=f'YosCfg.YosAplCfg. LA COLUMNA DE CONFIGURACION YosAplCfg["Apl"]["{Mem_Clm}"] ES DE SOLO LECTURA, SE IGNORA.', Tip= "Avs")
        else:
            if YosAplCfg_Def["Apl"][Mem_Clm].startswith("(n)"): # El valor de la columna es Numerico
                try:
                    YosAplCfg["Apl"][Mem_Clm] = int(Mem_Uni["cVal"])
                except ValueError:
                    Yos.Yos_MsgSis(Txt=f'YosCfg.YosAplCfg. EL VALOR PARA YosAplCfg["Apl"]["{Mem_Clm}"] DEBE SER NUMERICO, SE IGNORA.', Tip="Avs")
            else:
                YosAplCfg["Apl"][Mem_Clm] = Mem_Uni["cVal"]

    Yos.Cie(Mem_Cnx_YosCfg)

    if YosAplCfg["Apl"]["DirAch"]:    # Verifico si creo un directorio para Aplicaciones
        if len(YosAplCfg["Apl"]["DirAch"]) >= 2 and YosAplCfg["Apl"]["DirAch"][1] == ':':   # Pongo la letra en minuscula d: -> d:
            YosAplCfg["Apl"]["DirAch"]=YosAplCfg["Apl"]["DirAch"][0].lower() + YosAplCfg["Apl"]["DirAch"][1:]

        ruta_apl = os.path.normpath(os.path.join(YosAplCfg["Apl"]["DirAch"]))

        if os.path.exists(ruta_apl): # Verificación crucial
            from nicegui import app
            app.add_static_files('/Apl_DirAch', ruta_apl)
        else:
            Yos.Yos_MsgSis(Txt=f"EL DIRECTORIO DE APLICACIONES (YosCfg.Dat.DirAch) {ruta_apl} NO EXISTE.", Tip= "Err")

    ############################## Recuperamos el menu YosCfg.Mnu
    YosAplCfg["Apl"]["MnuNom"]= "MnuGen"
    Yos.Yos_MnuRec(YosAplCfg["Apl"]["MnuNom"], "MnuGen")  # Menu General ("Nombre_de_la_Aplciacion" ,"MnuGen" lo guarda en YosAplCfg["Apl"]["Apl_Mnu"] , si no lo debuelve en return

    ################# VERIFICACIONES IMPORTANTES - SALEN DEL SISTEMA
    Mem_Err = ""
    if not (10 <= YosAplCfg["Apl"]["Enc_nCos"] <= 15):
        YosAplCfg["Apl"]["Enc_nCos"] = 12 # Valor por defecto seguro si se sale del rango permitido
#        Mem_Err = f'{Mem_Err}\n YosAplCfg["Apl"]["Enc"]={YosAplCfg["Apl"]["Enc"]} no está bien definida.\n   Corrija o elimínela en la configuración de la aplicación.'


    if Mem_Err:
        Mem_Tit = f'{YosAplCfg["Apl"]["Apl"]} - {YosAplCfg["Apl"]["Nom"]}'
        Mem_Err = f" **** SE HAN DETECTADO ERRORES – SE SALDRÁ DE LA APLICACIÓN ****\n{Mem_Err}"
        Yos.Yos_Msg_Tui(Fnc_Tit=Mem_Tit, Fnc_Msg=Mem_Err, Fnc_Tip= "Err")
        Yos.Apl_Fin_Txt(Pgt= "No", SisMsg= "No")

    # Yos_Cfg_Mst() # Muestra todos los datos de YosAplCfg, Yos_Cfg_Mst("Seccion")

def  Yos_Cfg_YosLib():
    ################################################# LIBRERIA Yos
    # Recupero datos YosLib YosAplCfg.Yos
        # recupero Yos

    YosAplCfg["Yos"]["Apl"]        = "YosLib"
    YosAplCfg_Def["Yos"]["Apl"]    = "Codigo de la Libreria Yos"
    YosAplCfg["Yos"]["Nom"]        = "LIBRERIA DE PROPOSITO GENERAL"
    YosAplCfg_Def["Yos"]["Nom"]    = "Nombre de la libreria"
    YosAplCfg["Yos"]["Vsn"]        = "2026.7"
    YosAplCfg_Def["Yos"]["Vsn"]    = "Version"
    YosAplCfg["Yos"]["Atr"]        = "Miguel Tortosa"
    YosAplCfg_Def["Yos"]["Atr"]    = "Autor"
    YosAplCfg["Yos"]["AtrEml"]     = "mtcyos@yahoo.es"
    YosAplCfg_Def["Yos"]["AtrEml"] = "Email Autor"
    YosAplCfg["Yos"]["Enc_Mtd"]    = "Bcr"
    YosAplCfg_Def["Yos"]["Enc_Mtd"]= "METODO DE ENCRIPTACION Bcr = Bcrypt"
    YosAplCfg["Yos"]["Cpy"]        = ""
    YosAplCfg_Def["Yos"]["Cpy"]    = "Copyright"
    YosAplCfg["Yos"]["Dir"]        = ""
    YosAplCfg_Def["Yos"]["Dir"]    = "Directorio"
    YosAplCfg["Yos"]["SctDir"]     = ""
    YosAplCfg_Def["Yos"]["SctDir"] = "Directorio Sct (Scripts)"

    YosAplCfg["Yos"]["PrgCpd"]     = "Yos_Prg"
    YosAplCfg_Def["Yos"]["PrgCpd"] = "Computadora de Programación"

    # Dfino valores Calculados
    Mem_Dat = YosAplCfg["Yos"]["Vsn"]
    Mem_Json = YosAplCfg["Yos"]["Atr"]
    YosAplCfg["Yos"]["Cpy"] = f"{Mem_Dat[:4]} © {Mem_Json}"
    # Definimos el directorio base usando la ubicación real del archivo fuente
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    # Directorio principal Yos
    YosAplCfg["Yos"]["Dir"] = os.path.join(BASE_DIR, "Yos")
    # Directorio Sct (Scripts)
    YosAplCfg["Yos"]["SctDir"] = os.path.join(BASE_DIR, "Yos", "Script")

# ******************************************************************************************************************************************* Yos_Cfg_Jsn()
def Yos_Cfg_Jsn(**Fnc_Dic):
    # cTit : Gestion de archivos JSON
    # cDes : Gestion de archivos JSON
    # cPmt : Ach    -> Bombre del Archivo.
    #        Dir    -> Direccion del Archivo.

    Mem_Ach    = Fnc_Dic.get("Ach", "") # Direccion del Archivo .
    Mem_Dir    = Fnc_Dic.get("Dir", "") # Seccion.

    if Mem_Dir =="Yos":
        Mem_Dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        Mem_Dir = os.path.join(Mem_Dir, "Yos", "Cfg")

    Mem_Json = os.path.join(Mem_Dir, Mem_Ach)
    #print(f'Mem_Ach={Mem_Ach} Mem_Dir = {Mem_Dir} Mem_Json={Mem_Json}')
    #input("INTRO continuar")

    try:
        with open(Mem_Json, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Retorna solo el diccionario de las aplicaciones
            return data.get("YosApl", {})
    except FileNotFoundError:
        return f"Err: El archivo {Mem_Json} no se encontró."
    except json.JSONDecodeError:
        return f"Err: El archivo {Mem_Json} tiene un formato JSON inválido."

# FIN ******************************************************************************************************************************************* Yos_Cfg_Jsn()

def Yos_Cfg_Mst(Fnc_Sub= "", Fnc_Dat= "", Fnc_Def= ""):
    # Si se pide una sección específica de YosAplCfg
    if Fnc_Sub == "Mst": # Muestro las Clm, para programacion
        print("******************************************************")
        print("* YosAplCfg - Definición de las Columnas del sistema *")
        print("******************************************************")

        # 1. Recopilar primero todas las líneas para calcular el ancho máximo de la clave
        lineas_proyectadas = []
        max_ancho_clave = 0

        for seccion, datos in sorted(YosAplCfg.items()):
            Mem_Sec = f'YosAplCfg["{seccion}"]'
            if isinstance(datos, dict):
                for k, v in sorted(datos.items()):
                    clave_completa = f'{Mem_Sec}["{k}"]'
                    if len(clave_completa) > max_ancho_clave:
                        max_ancho_clave = len(clave_completa)

                    def_texto = YosAplCfg_Def.get(seccion, {}).get(k, "")
                    if not def_texto:
                        def_texto = "******** ATENCION : VARIABLE SIN DEFINICION, PUEDE SER QUE NO ESTE DEFINIDA EN Yos_Cfg  *******"

                    lineas_proyectadas.append((clave_completa, def_texto))
            else:
                lineas_proyectadas.append((seccion, f"{datos}"))

        # 2. Imprimir con alineación exacta usando el ancho máximo calculado
        for clave_completa, def_texto in lineas_proyectadas:
            print(f"{clave_completa:<{max_ancho_clave}} : {def_texto}")

        print("******************************************************")
        input("PULSE INTRO PARA CONTINUAR ")
        return

    from colorama import Fore, Style

    print("**************************************************")
    print('* YosAplCfg["Seccion"]["Dato"]                    *')
    print(f'* YosAplCfg["{Fnc_Sub}"]["{Fnc_Dat}"] Def = {Fnc_Def}')
    print("**************************************************")

    items_a_imprimir = []

    if Fnc_Sub:
        if Fnc_Sub in YosAplCfg:
            datos_sec = YosAplCfg[Fnc_Sub]
            if Fnc_Dat:
                if Fnc_Dat.endswith("*"):
                    prefijo = Fnc_Dat[:-1]
                    elementos = {
                        k: v for k, v in datos_sec.items() if k.startswith(prefijo)
                    }
                else:
                    elementos = (
                        {Fnc_Dat: datos_sec.get(Fnc_Dat)}
                        if Fnc_Dat in datos_sec
                        else {}
                    )
            else:
                elementos = datos_sec

            for k, v in elementos.items():
                def_texto = YosAplCfg_Def.get(Fnc_Sub, {}).get(k, "")
                items_a_imprimir.append((Fnc_Sub, k, v, def_texto))
        else:
            print(f'Sección ["{Fnc_Sub}"] no encontrada en YosAplCfg.')
    else:
        for seccion, datos in YosAplCfg.items():
            if isinstance(datos, dict):
                for k, v in datos.items():
                    def_texto = YosAplCfg_Def.get(seccion, {}).get(k, "")
                    items_a_imprimir.append((seccion, k, v, def_texto))
            else:
                items_a_imprimir.append((seccion, "", datos, ""))

    items_a_imprimir.sort()

    if items_a_imprimir:
        # Calcular ancho máximo para la clave formateada
        max_ancho_clave = 0
        for seccion, k, v, def_texto in items_a_imprimir:
            if k:
                ancho = len(f'YosAplCfg["{seccion}"]["{k}"]')
            else:
                ancho = len(f'YosAplCfg["{seccion}"]')
            if ancho > max_ancho_clave:
                max_ancho_clave = ancho

        current_sec = ""
        for seccion, k, v, def_texto in items_a_imprimir:
            if seccion != current_sec:
                current_sec = seccion
                print(f'Sección : ["{current_sec}"]')

            if k:
                clave_str = f'YosAplCfg["{seccion}"]["{k}"]'
                # Imprimimos la clave tabulada y su valor
                print(f"  {clave_str:<{max_ancho_clave}} : {v}")
            else:
                print(f"  {seccion} : {v}")

            # Mostrar definición tabulada alineada debajo o en bloque limpio
            mostrar_def = True
            if Fnc_Sub and Fnc_Def == "N":
                mostrar_def = False

            if mostrar_def and k:
                # Usamos un espaciado proporcional para que las flechas y textos inicien alineados
                if def_texto:
                    print(
                        f"  {'':<{max_ancho_clave}}    -> {def_texto}"
                    )
                else:
                    print(
                        f"  {'':<{max_ancho_clave}}    "
                        f"{Fore.RED}-> ATENCION : VARIABLE SIN DEFINICION, PUEDE"
                        f" SER QUE NO ESTE DEFINIDA EN Yos_Cfg{Style.RESET_ALL}"
                    )

    print("**************************************************")
    input("PULSE INTRO PARA CONTINUAR ")
