#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Bin > Sistema Yos - Inicialización y Verificación de Módulos
# Tim - 20260409 14:15:00

import sys
import importlib
import subprocess

from .Yos_Ges import Yos_MsgSis, Yos_RegApl

Yos_RegApl(Tip= "«LogIni»")
Yos_MsgSis(Txt= "VERIFICANDO DEPENDENCIAS.")

# Mdl_Map: Mapeo de (Nombre_Instalación_Con_Version : Nombre_De_Importacion)
Mdl_Map = {
    "pip": "pip",                               # Gestor de paquetes (Instalador oficial)

    "bcrypt": "bcrypt",                         # Seguridad de alto nivel (HASH Bcr)
    "pyperclip": "pyperclip",                   # Portapapeles (Copiar y Pegar) *** Solo Windows

                                                # ACCESO ARCHIVOS
    "pypyodbc": "pypyodbc",                     # Conector universal de Base de Datos (ODBC)
    "dbfread": "dbfread",                       # Conector para LECTURA de .dbf
    "openpyxl": "openpyxl",                     # LECTURA y ESCRITURA de archivos Excel (.xlsx)
    "reportlab": "reportlab",                   # Generador de reportes y documentos en PDF
    "pillow": "PIL",                            # Gui: Manejo de imágenes (ReportLab)

                                                # ENTORNO GRAFICO
    "colorama": "colorama",                     # Tui Básica : Gestión de color en consola
    "pyfiglet": "pyfiglet",                     # Tui Básica : Arte ASCII
    "pytimedinput": "pytimedinput",             # Tui Básica : Entradas de teclado con timeout
    "textual": "textual",                       # Tui Avanzada : Interfaz de Terminal

    "PyMySQL": "pymysql",                       # Acceso a MySql y MariaDB
    "dbf": "dbf",                               # Gestión completa de archivos base de datos DBF

    "prompt_toolkit": "prompt_toolkit",         # Tui: Interfaz de Terminal Avanzada **** a Quitar, cambia por Textual y colorama

    "nicegui==3.12.1": "nicegui",               # Gui: Interfaz Web moderna                 *** BORRAR
    "pydantic==2.10.6": "pydantic",             # Gui: Base de datos (Core para NiceGUI)    *** BORRAR
    "pydantic-core==2.27.2": "pydantic_core",   # Gui: Motor de validación                  *** BORRAR
    "asyncio": "asyncio",                       # Gui: Manejo de tareas asíncronas          *** BORRAR

}

"""

    "fastapi>=0.110.0": "fastapi",              # Gui Backend: Framework de API de alto rendimiento
    "uvicorn>=0.28.0": "uvicorn",               # Gui Backend: Servidor ASGI ultrarrápido
    "fpdf2": "fpdf",                            # Generador de archivos PDF (Quitar en un futuro)
    "waitress": "waitress",                     # Servidor WSGI robusto para Windows (Quitar en un futuro)
    "django": "django",                         # Framework Web (Quitar en un futuro)

"""

# pip uninstall fpdf

# 2. Verificación de existencia de los módulos
for install_pkg, import_name in Mdl_Map.items():
    try:
        importlib.import_module(import_name)
    except ImportError:
        print(f"\nEl módulo '{import_name}' no está instalado.")
        # Usamos el nombre del paquete para la pregunta
        pkg_display = install_pkg.split('==')[0]

        if input(f"Instalar {pkg_display} (S=Instalar) : ").upper() == "S":
            print(f"Instalando {install_pkg}...")
            try:
                # Instalación usando el nombre exacto con versión
                subprocess.check_call([sys.executable, "-m", "pip", "install", install_pkg, "--break-system-packages"])
                print(f"Módulo {pkg_display} instalado correctamente.")
            except Exception as e:
                print(f"Error al instalar {pkg_display}: {e}")
    except Exception as e:
        print(f"Ocurrió otro error al importar {import_name}: {e}")

# Importaciones de la YosLib
from .YosLib import * # Aqui se guardan todas las Def Yos_xxxx que no tienen salida a pantalla
from .YosIdd import * # Aqui se guardan todas las Def Idd_xxxx que no tienen salida a pantalla
from .YosApl import * # Aqui se guardan todas las Def Apl_xxxx que no tienen salida a pantalla

# ENTORNO GRAFICO Tui (Text User Interface)
from .Yos_Ges import *  # Gestion de todas las Def Yos_xxx_Tui
from .Idd_Ges import *  # Gestion de todas las Def Idd_xxx_Tui
from .Apl_Ges import *  # Gestion de todas las Def Apl_xxx_Tui

# ENTORNO GRAFICO Gui (Graphical User Interface)
from .Yos_Ges_Gui import *  # Gestion de todas las Def Yos_xxx_Frm     *** BORRAR
from .Idd_Ges_Gui import *  # Gestion de todas las Def Idd_xxx_Frm     *** BORRAR
from .Apl_Ges_Gui import *  # Gestion de todas las Def Apl_xxx_Frm     *** BORRAR

from .Yos_Cfg import *
# from .Yos_Acd import *
from .Yos_YosIni import *
from .Yos_Ent import *

from .Yos_Mnu_Tui import *

# Sistema de Menu Unificado
from .Yos_Mnu import *

from .Idd_BdtSvr import *
from .Idd_TabMod import *
from .Idd_TabMst import *
