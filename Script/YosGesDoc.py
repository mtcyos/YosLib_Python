#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   YosGesDoc
   GESTION DE DOCUMENTOS

   Copyright (c) 2026 Miguel Tortosa

   Licenciado bajo la Licencia MIT.
   Consulte el archivo LICENCIA en la raíz del proyecto para más información.
"""
import os
from nicegui import ui
import asyncio
import sqlite3
import copy

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Flowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_RIGHT, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Flowable, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import copy

# --- CLASES ---
class GeneradorIndice:
    def __init__(self):
        self.entradas = []
    def registrar(self, titulo, pagina_manual, es_sub):
        if not self.entradas or self.entradas[-1][0] != titulo:
            self.entradas.append((titulo, pagina_manual, es_sub))

# --- INSTANCIACIÓN ---
recolector_indice = GeneradorIndice()

class MarcadorCapitulo(Flowable):
    def __init__(self, titulo, es_arranque_indice=False, es_sub=False):
        Flowable.__init__(self)
        self.titulo = titulo
        self.es_arranque_indice = es_arranque_indice
        self.es_sub = es_sub
        self.width = 1
        self.height = 1
    def draw(self):
        global PAGINA_CORTE_INDICE
        pagina_absolute = self.canv.getPageNumber()
        if self.es_arranque_indice:
            PAGINA_CORTE_INDICE = pagina_absolute
        else:
            recolector_indice.registrar(self.titulo, pagina_absolute - 2, self.es_sub)

Mem_Tit = "YosGesDoc - Gestión de Documentos" # Titulo de la Aplicacion

Mem_DocNom = "" # Nombre del Documento
Mem_DocNomSin = "" # Nombre del Documento sin YosDoc_ inicial
Mem_DocTit = "" # Titulo del Documento
Mem_DocTip = "" # Tipo del Documento
Mem_DocTipDes = "" # Descripcion de Tipo del Documento

Mem_Svr = ""    # Nombre del Docuemnto

Mem_IniCap = ""
Mem_IniSub = ""
Mem_IniPrf = ""

# --- VARIABLES GLOBALES DE CONTROL ---
TITULO_GLOBAL_HEADER = "Manual"
PAGINA_CORTE_INDICE = 999999

Mem_PagAct = 0

# DEFINO EL MENU A USAR
#Yos_Cfg_Jsn(**Fnc_Dic):
Mem_Mnu = {
    '0100': {
        'Txt': 'GESTIÓN DE DOCUMENTOS',
        'Sub': {
            '0110': {'Txt': 'CARGAR DOCUMENTO',         'Fnc': 'YosGesDoc_CagDoc()',    'Cod': 'MnuIte'},
            '0120': {'Txt': '',                         'Fnc': '',                      'Cod': 'Sep'},
            '0130': {'Txt': 'MODIFICAR CONTENIDO',      'Fnc': '/YosGesDoc_Cap',        'Cod': 'MnuIte'}, # Es una pagina Web de aqui
            '0140': {'Txt': '',                         'Fnc': '',                      'Cod': 'Sep'},
            '0150': {'Txt': 'RENUMERAR CAPÍTULOS',      'Fnc': 'YosGesDoc_Num()',       'Cod': 'MnuIte'},
            '0160': {'Txt': '',                         'Fnc': '',                      'Cod': 'Sep'},
            '0170': {'Txt': 'IMPRIMIR DOCUMENTO',       'Fnc': '/YosGesDoc_Ipr',        'Cod': 'MnuIte'},
            '0180': {'Txt': '',                         'Fnc': '',                      'Cod': 'Sep'},
            '0190': {'Txt': 'CERRAR DOCUMENTO',         'Fnc': 'YosGesDoc_Cie()',  'Cod': 'MnuIte'}
#            '0180': {'Txt': '',                         'Fnc': '',                      'Cod': 'Sep'},
#            '0190': {'Txt': 'PANTALLA ANTERIOR',        'Fnc': '/',                     'Cod': 'MnuIte'}
        }
    },
}
def YosGesDoc_Cie():
    global Mem_DocNom, Mem_DocNomSin
    Mem_DocNom = ""
    ui.navigate.to('/YosGesDoc')

def YosGesDoc_Svr(Fnc_Svr):
    # Defini el Servidor para el Documentos Bdt
    import sys
    f = sys._getframe(1)
    print(f"Llamado desde la función: '{f.f_code.co_name}' en la línea: {f.f_lineno}")

    global Mem_Svr

    # Creo su propia direccion
    if Mem_Svr and Mem_Svr != Fnc_Svr:
        del YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Tip"]
        del YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Dir"]
        del YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Usr"]
        del YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Pas"]
        del YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Bdt"]
        del YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Obs"]
        del YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_ObsSis"]

    Mem_Svr = Fnc_Svr
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Tip"] = "SQLite"
    YosAplCfg["Apl"]["Dir"] = YosAplCfg["Apl"]["Dir"]
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Dir"] = os.path.abspath(os.path.join(YosAplCfg["Apl"]["Dir"], "Doc")) # Esta en la propia aplicacion
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Usr"] = ""
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Pas"] = ""
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Bdt"] = ""
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Obs"] = "Esta en DirAplicacion\\Doc\\"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_ObsSis"] = "YosDoc = Son los manuales que crea YosGesDc"

    '''
#    if YosAplCfg["Apl"]["Dbg"]=="S":
    print("--------------------------------------------------")
    print(f'Mem_Svr = {Mem_Svr}')
    print("--------------------------------------------------")
    print(f'YosAplCfg[Apl][Bdt_{Mem_Svr}_Tip] = {YosAplCfg["Apl"]["Bdt_{Mem_Svr}_Tip"]}')
    print(f'YosAplCfg[Apl][Bdt_{Mem_Svr}_Dir] = {YosAplCfg["Apl"]["Bdt_{Mem_Svr}_Dir"]}')
    print(f'YosAplCfg[Apl][Bdt_{Mem_Svr}_Usr] = {YosAplCfg["Apl"]["Bdt_{Mem_Svr}_Usr"]}')
    print(f'YosAplCfg[Apl][Bdt_{Mem_Svr}_Pas] = {YosAplCfg["Apl"]["Bdt_{Mem_Svr}_Pas"]}')
    print(f'YosAplCfg[Apl][Bdt_{Mem_Svr}_Bdt] = {YosAplCfg["Apl"]["Bdt_{Mem_Svr}_Bdt"]}')
    print(f'YosAplCfg[Apl][Bdt_{Mem_Svr}_Obs] = {YosAplCfg["Apl"]["Bdt_{Mem_Svr}_Obs"]}')
    print(f'YosAplCfg[Apl][Bdt_{Mem_Svr}_ObsSis] = {YosAplCfg["Apl"]["Bdt_{Mem_Svr}_ObsSis"]}')
    print("--------------------------------------------------")
    '''

#    print(f' 107 -Nuevo Servidor de Docuemnto {Mem_Svr}')
#################################################################################################################

def detectar_paginas_y_marcar(canvas, doc):
    """Función que gestiona el diseño estético de la cabecera y el pie de página."""
    global PAGINA_CORTE_INDICE, Mem_PagAct
    pagina_absoluta = canvas.getPageNumber()
    Mem_PagAct = canvas.getPageNumber()

    # REGLA DE ORO: Ni la portada (Pág 1) ni la ficha técnica (Pág 2) llevan nada
    if pagina_absoluta <= 2:
        return

    canvas.saveState()

    # MATEMÁTICA REAL: Las dos primeras hojas no cuentan para el lector
    pagina_manual = pagina_absoluta - 2

    # 1. CONFIGURACIÓN DE LA CABECERA (Centrada arriba)
    canvas.setFont('Helvetica', 9)
    canvas.setFillColor('#555555')
    canvas.drawCentredString(306, 750, TITULO_GLOBAL_HEADER)

    # Línea sutil de separación tipográfica debajo de la cabecera
    canvas.setStrokeColor('#DDDDDD')
    canvas.setLineWidth(0.5)
    canvas.line(54, 742, 558, 742)

    # 2. CONFIGURACIÓN DEL PIE DE PÁGINA
    if pagina_absoluta >= PAGINA_CORTE_INDICE:
        numero_hoja_indice = (pagina_absoluta - PAGINA_CORTE_INDICE) + 1
        texto_pie = f"- I : {numero_hoja_indice} -"
    else:
        texto_pie = f"- {pagina_manual} -"

    canvas.setFont('Helvetica', 9)
    canvas.setFillColor('#555555')
    canvas.drawCentredString(306, 36, texto_pie)

    canvas.restoreState()

###################################################################################################################
def YosGesDoc_Acd():
        # Que es YosGesDoc
#    with ui.card().classes('w-full max-w-4xl mx-auto p-8 shadow-lg rounded-2xl'):
    with ui.element('div').classes('w-full pl-30 pr-4 py-4'): # pl-20 es el secreto
        with ui.card().classes('w-full p-8 shadow-lg rounded-2xl'):
            # Título con estilo comercial
            ui.label('YosGesDoc (Yos Gestión de Documentos)') \
                .classes('text-3xl font-bold text-primary mb-4')

            # Subtítulo descriptivo
            ui.label('Gestión de Documentos Minimalista') \
                .classes('text-xl font-semibold text-gray-700 mb-6')

            ui.label(
                'La gestión de documentos es una aplicación que permite crear de manera rápida y sencilla los documentos que necesite.'
            ).classes('text-justify text-gray-600 mb-4')


            ui.label(
                'Solo se permite texto, el cual se puede clasificar por capítulo, subcapítulo y párrafo, permitiendo la reordenación de ellos.'
            ).classes('text-justify text-gray-600 mb-4')

            ui.label(
                'En la opción de guardar, la aplicación genera un .pdf en la subcarpeta Doc e incluye un índice.'
            ).classes('text-justify text-gray-600 mb-4')

            # Elemento visual opcional para dar toque corporativo
            with ui.row().classes('w-full justify-center mt-8'):
                ui.image('/yos_img/Log_Yos_100.png').props('width=48px height=48px')
                ui.label('mtcyos') \
                    .classes('text-sm font-light text-gray-400 self-center')

def YosGesDoc_Inf():
    # Que es YosGesDoc
    global Mem_DocTit, Mem_DocNom, Mem_DocNomSin, Mem_DocTit, Mem_DocTip, Mem_DocTipDes, Mem_Svr

    Mem_Svr = os.path.splitext(Mem_DocNom)[0]
    YosGesDoc_Svr(Mem_Svr)

    # Inicializamos las variables en None para evitar errores si el try falla antes
    Mem_Cnx_YosDoc = None
    Mem_Cur_YosDoc = None

    try:
        Mem_Cnx_YosDoc = Yos.Idd_BdtSvr_Cnx(Mem_Svr, Fnc_Mod="ro")
        Mem_Cur_YosDoc = Mem_Cnx_YosDoc.cursor()

        # Lectura del único registro de la tabla SifInf
        Mem_Cur_YosDoc.execute("SELECT cTip FROM SisInf WHERE NumReg = 1")
        reg = Mem_Cur_YosDoc.fetchone()

        if reg:
            Mem_DocTip = reg[0]
            if Mem_DocTip == "Doc":
                Mem_DocTipDes = "DOCUMENTO : "
            elif Mem_DocTip == "Fnc":
                Mem_DocTipDes = "FUNCIONES : "
            else:
                Mem_DocTipDes = "DESCONOCIDO : "
        else:
            Mem_DocTip = "ERROR TABLA SisInf VACÍA"
            ui.notify(Mem_DocTip, color='negative')

        # Lectura del único registro de la tabla Inf
        Mem_Cur_YosDoc.execute("SELECT cTit, cSub, cAtr, cLug, cYea, cEdi, cIsb, cCpy, cDup FROM Inf LIMIT 1")
        reg = Mem_Cur_YosDoc.fetchone()
        if reg:
            cTit, cSub, cAtr, cLug, cYea, cEdi, cIsb, cCpy, cDup = reg
        else:
            cTit, cSub, cAtr, cLug, cYea, cEdi, cIsb, cCpy, cDup = "", "", "", "", "", "", "", "", "N"
    except Exception as e:
        print(f"Error en acceso a BD: {e}")
        ui.notify("Error de acceso a datos", color='negative')
    finally:
        # ESTO SE EJECUTA SIEMPRE, PASE LO QUE PASE
        if Mem_Cur_YosDoc:
            Mem_Cur_YosDoc.close()
        if Mem_Cnx_YosDoc:
            Yos.Cie(Mem_Cnx_YosDoc)

    with ui.element('div').classes('w-full pl-30 pr-4'):
        with ui.card().classes('w-full p-4 shadow-lg rounded-2xl'):  # p-8 → p-4

            # Título con estilo comercial
            ui.label(f'{Mem_DocTipDes}{os.path.splitext(Mem_DocNomSin)[0]}').classes('text-2xl font-bold text-primary mb-2')  # text-3xl → text-2xl, mb-4 → mb-2

            # Creamos entradas de texto cargando los valores por defecto de la BD
            txt_tit = ui.input(label='Título', value=cTit).classes('w-full mb-1')  # mb-2 → mb-1
            txt_sub = ui.input(label='Subtítulo', value=cSub).classes('w-full mb-2')  # mb-4 → mb-2

            # Contenedor para el resto de los metadatos del libro
            with ui.row().classes('w-full gap-2'):  # gap-4 → gap-2
                txt_atr = ui.input(label='Autor', value=cAtr).classes('flex-1')
                txt_edi = ui.input(label='Edición', value=cEdi).classes('flex-1')

            with ui.row().classes('w-full gap-2 mt-1'):  # gap-4 → gap-2, mt-2 → mt-1
                txt_lug = ui.input(label='Lugar', value=cLug).classes('flex-1')
                txt_yea = ui.input(label='Año', value=cYea).classes('flex-1')
                txt_isb = ui.input(label='ISBN', value=cIsb).classes('flex-1')
                txt_dup = ui.select(label='IMPRIMIR A DOS CARAS', options={'S': 'Sí', 'N': 'No'}, value=cDup if cDup in ['S', 'N'] else 'N').classes('flex-1')

            # El Copyright como área de texto larga por si tiene la licencia MIT completa
            txt_cpy = ui.textarea(label='Copyright / Licencia', value=cCpy).classes('w-full mt-2 flex-grow').props('rows=3')  # mt-4 → mt-2, rows=3 añadido

            # 4. FUNCIÓN INTERNA PARA GRABAR LOS CAMBIOS EN LA BASE DE DATOS
            def Grabar_Datos_Inf():
                try:
                    # Abrimos conexión en modo escritura
                    Cnx_W = Yos.Idd_BdtSvr_Cnx(Mem_Svr, Fnc_Mod="rw")
                    Cur_W = Cnx_W.cursor()

                    # Actualizamos el registro (asumiendo que NumReg es 1 o actualizando toda la tabla Inf)
                    Sql = """
                        UPDATE Inf
                        SET cTit=?, cSub=?, cAtr=?, cLug=?, cYea=?, cEdi=?, cIsb=?, cCpy=?, cDup=?
                        WHERE NumReg = 1
                    """
                    Cur_W.execute(Sql, (txt_tit.value, txt_sub.value, txt_atr.value, txt_lug.value,txt_yea.value, txt_edi.value, txt_isb.value, txt_cpy.value, txt_dup.value))
                    Cnx_W.commit()
                    Cur_W.close()
                    Cnx_W.close()

                    ui.notify("Cambios guardados con éxito", color='positive')
                    # Recargamos la página para asentar visualmente los datos actualizados
                    ui.run_javascript('window.location.reload()')

                except Exception as ex:
                    ui.notify(f"Error al grabar: {ex}", color='negative')

            # 5. BOTÓN DE GRABAR AL FINAL DEL FORMULARIO
            with ui.row().classes('w-full justify-end mt-4'):  # mt-8 → mt-4
                ui.button('GRABAR', on_click=Grabar_Datos_Inf)\
                    .props('icon=save').classes('bg-primary text-white px-6 py-2 rounded-lg font-bold')

def YosGesDoc_Num():
    # Renumero los Capitulos

    # VERIFICACIÓN DE SEGURIDAD
    if not Mem_DocNom:
        ui.notify("No se ha seleccionado ningún documento.", type='warning', position='center')
        ui.run_javascript('setTimeout(() => { window.location.href = "/YosGesDoc"; }, 2000);')  # 2000 = 2 Segundos
        return

    Mem_Svr = os.path.splitext(Mem_DocNom)[0]

    # Inicializamos las variables en None para evitar errores si el try falla antes
    Mem_Cnx_YosDoc = None
    Mem_Cur_YosDoc = None

    try:
        ui.notify("RENUMERANDO CAPÍTULOS–SUBCAPÍTULOS-PÁRRAFOS.", type='info', position='center')
        Mem_Cnx_YosDoc = Yos.Idd_BdtSvr_Cnx(Mem_Svr, Fnc_Mod="rw")
        Mem_Cur_YosDoc = Mem_Cnx_YosDoc.cursor()

        Mem_Cnx_YosDoc.execute("BEGIN TRANSACTION")

        # 1. Leemos con tu ordenación natural (Tu orden es la ley)
        Mem_Cur_YosDoc.execute("""
            SELECT NumReg, cNul, cCap, cSubCap, cPrf, cTit, cTxt, cObs, cModRegNik, cModRegTim
            FROM Txt
            ORDER BY cCap, cSubCap, cPrf
        """)
        filas = Mem_Cur_YosDoc.fetchall()

        if not filas:
            print("La tabla está vacía.")
            Mem_Cnx_YosDoc.close()
            return

        nuevos_registros = []

        # Variables de control para detectar los cambios reales de tu rejilla
        ultimo_cCap_origen = None
        ultimo_cSub_origen = None

        # Contadores matemáticos que se irán autogenerando
        contador_cap = 0
        contador_sub = 0
        contador_prf = 0

        # 2. Bucle de control por niveles en cascada
        for fila in filas:
            num_reg, c_nul, c_cap, c_sub, c_prf, c_tit, c_txt, c_obs, c_mod_nik, c_mod_tim = fila

            # REGLA 1: DETECTAMOS CAMBIO DE CAPÍTULO EN TU REJILLA
            if c_cap != ultimo_cCap_origen:
                ultimo_cCap_origen = c_cap
                ultimo_cSub_origen = c_sub  # Sincronizamos también el subcapítulo

                contador_cap += 10   # Avanza el capítulo (0010, 0020...)
                contador_sub = 10    # REGLA ORO 1: subCap vuelve a 0010
                contador_prf = 10    # REGLA ORO 1: Parrafo vuelve a 0010

            # REGLA 2: MISMO CAPÍTULO, PERO DETECTAMOS CAMBIO DE SUBCAPÍTULO
            elif c_sub != ultimo_cSub_origen:
                ultimo_cSub_origen = c_sub

                # El contador_cap NO SE TOCA (se queda en el actual)
                contador_sub += 10   # Avanza el subcapítulo (0020, 0030...)
                contador_prf = 10    # REGLA ORO 2: Parrafo vuelve a 0010 alterno

            # REGLA 3: CONTINUIDAD ABSOLUTA (Mismo capítulo y mismo subcapítulo)
            else:
                # Los bloques mayores se quedan congelados
                contador_prf += 10   # Solo avanza el párrafo de 10 en 10 (0020, 0030...)

            # Formateamos matemáticamente las tres variables a 4 dígitos con ceros a la izquierda
            nuevo_c_cap = f"{contador_cap:04d}"
            nuevo_c_sub = f"{contador_sub:04d}"
            nuevo_c_prf = f"{contador_prf:04d}"

            # Añadimos el registro transformado a la cola
            nuevos_registros.append((num_reg, c_nul, nuevo_c_cap, nuevo_c_sub, nuevo_c_prf, c_tit, c_txt, c_obs, c_mod_nik, c_mod_tim))

            # 3. Limpieza absoluta de la tabla para evitar choques de índices
            Mem_Cur_YosDoc.execute("DELETE FROM Txt")

            # 4. Inserción limpia de la nueva matriz normalizada
            query_insert = """
                INSERT INTO Txt (NumReg, cNul, cCap, cSubCap, cPrf, cTit, cTxt, cObs, cModRegNik, cModRegTim)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            Mem_Cur_YosDoc.executemany(query_insert, nuevos_registros)
            Mem_Cnx_YosDoc.commit()
    except Exception as e:
        print(f"Error en acceso a BD: {e}")
        Mem_Cnx_YosDoc.rollback()
        ui.notify("Error de acceso a datos", color='negative')
    finally:
        # ESTO SE EJECUTA SIEMPRE, PASE LO QUE PASE
        if Mem_Cur_YosDoc:
            Mem_Cur_YosDoc.close()
        if Mem_Cnx_YosDoc:
            Yos.Cie(Mem_Cnx_YosDoc)

    ui.notify("REMUNERACIÓN TERMINADA CORRECTAMENTE.", type='info', position='center')
    ui.navigate.reload()


#######################################################################
def YosGesDoc_CagDoc():

    ruta_directorio = os.path.join(YosAplCfg["Apl"]["Dir"], "Doc")
    os.makedirs(ruta_directorio, exist_ok=True)

    with ui.dialog() as dialog:
        with ui.card().classes('w-full max-w-md p-4 shadow-lg rounded-xl bg-white'):
            ui.label('SELECCIONE O CREE UN DOCUMENTO').classes('font-bold text-xs text-neutral-500 mb-2')

            # --- NUEVA OPCIÓN: BOTÓN DE "NUEVO DOCUMENTO" ---
            with ui.row().classes('w-full mb-2'):
                nuevo_nombre = ui.input(placeholder='Nombre del nuevo archivo...').classes('flex-grow')
                ui.button(icon='add', on_click=lambda: YosGesDoc_CagDoc_Nue(nuevo_nombre.value, dialog))\
                    .props('flat dense').classes('text-primary')

            # Área con scroll
            with ui.scroll_area().classes('w-full h-48 border border-neutral-200 rounded p-1 bg-neutral-50'):
                # (Aquí mantienes el código de listar archivos que ya tenías)
                archivos = [f for f in os.listdir(ruta_directorio)
                            if f.startswith('YosDoc_') and f.endswith('.Bdt')]
                for archivo in archivos:
                    nombre_base = os.path.splitext(archivo)[0]
                    if nombre_base.startswith('YosDoc_'):
                        nombre_limpio = nombre_base[7:] # 7 es la longitud de 'YosDoc_'
                    else:
                        nombre_limpio = nombre_base
#                    ui.button(nombre_limpio, on_click=lambda a=archivo: [YosGesDoc_SelDoc(a), dialog.close()]).props('flat dense').classes('w-full text-left justify-start')
                    ui.button(nombre_limpio,
                    on_click=lambda a=archivo: [YosGesDoc_SelDoc(a), dialog.close()])\
                    .props('flat dense no-caps')\
                    .classes('w-full text-left justify-start')

    dialog.open()

    # --- FUNCIÓN PARA CREAR EL ARCHIVO ---
    import sqlite3

    def YosGesDoc_CagDoc_Nue(nombre, dialog):
        if not nombre:
            ui.notify("Escribe un nombre", color='warning')
            return

        nombre = 'YosDoc_' + nombre
#        if not nombre.endswith('.Bdt'):
#            nombre += '.Bdt'

        ruta = os.path.join(YosAplCfg["Apl"]["Dir"], "Doc", f"{nombre}.Bdt")
        input(ruta)
        if not os.path.exists(ruta):
            # 1. Intentamos conectar. SQLite creará el archivo automáticamente si no existe.
            conn = sqlite3.connect(ruta)
            cur = conn.cursor()
            conn.close()

        YosGesDoc_Svr(nombre)

        try:
            # Al conectar, si no existe, SQLite crea el archivo correctamente
            Mem_Cnx_YosDoc = Yos.Idd_BdtSvr_Cnx(Mem_Svr, Fnc_Mod="rw")
            Mem_Cur_YosDoc = Mem_Cnx_YosDoc.cursor()

            # --- ACTIVAMOS EL MODO WAL ---
            Mem_Cur_YosDoc.execute('PRAGMA journal_mode = WAL')

            # Creamos la estructura básica que tu aplicación necesita
            Mem_Cur_YosDoc.execute('''
                CREATE TABLE "SisInf" (
                    "NumReg" INTEGER PRIMARY KEY CHECK (NumReg = 1),
                    "cTip" TEXT,
                    "cModRegNik" TEXT,
                    "cModRegTim" TEXT
                )
            ''')
            # Insertamos Los Datos Iniciales
            Mem_Cur_YosDoc.execute('INSERT INTO SisInf (NumReg, cTip) VALUES (1, ?)', ("Doc",))

            Mem_Cur_YosDoc.execute('''
                CREATE TABLE "Inf" (
                    "NumReg" INTEGER PRIMARY KEY CHECK (NumReg = 1),
                    "cTit"  TEXT,
                    "cSub"  TEXT,
                    "cAtr"  TEXT,
                    "cLug"  TEXT,
                    "cYea"  TEXT,
                    "cEdi"  TEXT,
                    "cIsb"  TEXT,
                    "cCpy"  TEXT,
                    "cDup"  TEXT,
                    "cModRegNik"    TEXT,
                    "cModRegTim"    TEXT
                )
            ''')

            # Insertamos un registro vacío por defecto para que funcione el SELECT LIMIT 1
            Mem_Cur_YosDoc.execute('INSERT INTO Inf (NumReg, cTit) VALUES (1, ?)', (nombre,))

            Mem_Cur_YosDoc.execute('''
                CREATE TABLE "Txt" (
                    "NumReg"    INTEGER,
                    "cNul"  VARCHAR(1),
                    "cCap"  VARCHAR(4),
                    "cSubCap"   VARCHAR(4),
                    "cPrf"  VARCHAR(4),
                    "cTit"  VARCHAR(255),
                    "cTxt"  TEXT,
                    "cObs"  TEXT,
                    "cModRegNik"    VARCHAR(20),
                    "cModRegTim"    VARCHAR(20),
                    PRIMARY KEY("NumReg" AUTOINCREMENT),
                    UNIQUE("cCap","cSubCap","cPrf")
                )
            ''')


            Mem_Cnx_YosDoc.commit()
            Mem_Cnx_YosDoc.close()

            ui.notify(f"Base de datos creada: {nombre}", color='positive')
            dialog.close()
            YosGesDoc_SelDoc(nombre)

        except Exception as e:
            ui.notify(f"Error al crear BD: {e}", color='negative')
#########################################################################################################################
def YosGesDoc_SelDoc(nombre_seleccionado):
    global Mem_DocNom, Mem_DocNomSin
    Mem_DocNom = nombre_seleccionado  # <--- AQUÍ SE GUARDA EL NOMBRE
    if Mem_DocNom.startswith('YosDoc_'):
        Mem_DocNomSin = Mem_DocNom[7:] # 7 es la longitud de 'YosDoc_'
    else:
        Mem_DocNomSin = Mem_DocNom
    print(f'Mem_DocNom={Mem_DocNom} Mem_DocNomSin={Mem_DocNomSin}')

    # Notificación visual de que ya quedó registrado
    ui.notify(f"Seleccionado: {Mem_DocNom}", color='positive')
    ui.navigate.to('/YosGesDoc')

def Yos_MnuVrt_Fnc(Mem_Fnc):    # De momento Simpre debe estas y no se puede cambiar en Nombre
#    print(f'Yos_MnuVrt_Fnc Mem_Fun={Mem_Fnc}')  # <--- ¡Aquí sí se imprimirá cuando hagas clic!
    try:
        eval(Mem_Fnc)
    except Exception as e:
        print(f"Error al ejecutar: {e}")

################################################################################################################################################################################
# PÁGINA YosGesDoc
@ui.page('/YosGesDoc')
async def Pgn_YosGesDoc():

    from nicegui import context
    client = context.client

    if YosAplCfg["Apl"]["Usr_Acc"] == "S":
        if not app.storage.user.get('autenticado', False):
            ui.run_javascript('window.location.href = "/login"')
            return

    if YosAplCfg["Apl"]["Etn"] == "Loc" and YosAplCfg["Apl"]["Usr_Acc"] != "S" and not YosSes['Usr_Nik']:
        Yos.Apl_UsrAcc_UsrEliDat("SinUsr")

    # CABECERA con TITULO DE LA PAGINA
    Yos.Yos_Cab_Gui(Tit=Mem_Tit)

    # MENU
    Yos.Yos_Mnu(Mnu = Mem_Mnu, MnuNom = "GesDoc")

    # --- ESTILOS VISUALES GENERALES ---
    ui.query('body').style('background-color: #ffffff; color: #000000; font-family: sans-serif;')

    if not Mem_DocNom:
        YosGesDoc_Acd()
    else:
        YosGesDoc_Inf()

    # --- 4. PIE DE PÁGINA Y NOTAS DE DESCARGO ---
    Yos.Yos_PieAvs_Gui(Avs="Yos Gestión de Documentos")

################################################################################################################################################################################
# PÁGINA PARA GESTIÓN DE CAPÍTULOS
@ui.page('/YosGesDoc_Cap')
async def Pgn_YosGesDoc_Cap():
    Yos.Yos_Cab_Gui(Tit=Mem_Tit)
    # VERIFICACIÓN DE SEGURIDAD
    if not Mem_DocNom:
        ui.notify("No se ha seleccionado ningún documento.", type='warning', position='center')
        ui.run_javascript('setTimeout(() => { window.location.href = "/YosGesDoc"; }, 2000);')  # 2000 = 2 Segundos
        return

    Yos.Yos_Mnu(Mnu = Mem_Mnu, MnuNom = "GesDoc")

    global Mem_IniCap, Mem_IniSub, Mem_IniPrf

    # Definimos la ruta de la base de datos basada en el nombre del documento
    Mem_Svr = os.path.splitext(Mem_DocNom)[0]

    with ui.element('div').classes('w-full pl-30 pr-4'):
        with ui.card().classes('w-full p-0 shadow-lg rounded-2xl'):
            # Título sin padding inferior
            ui.label(f'Capítulos de : {os.path.splitext(Mem_DocNomSin)[0]}').classes('text-xl font-bold text-primary px-4 pt-2').style('margin: 0; padding-bottom: 0;')

            # Botón NUEVO sin margen superior, solo inferior pequeño
            ui.button('NUEVO', icon='add', on_click=lambda: ui.navigate.to('/YosGesDoc_CapEdi')).props('flat dense').classes('text-primary ml-4').style('margin-top: 0; margin-bottom: 4px;')

            # --- LISTA DE CAPÍTULOS CARGADA DESDE LA BDT ---
            with ui.scroll_area().classes('w-full h-[60vh] border rounded').style('margin-top: 0;'):
                try:
                    Mem_Cnx_YosDoc = Yos.Idd_BdtSvr_Cnx(Mem_Svr, Fnc_Mod="ro")
                    Mem_Cur_YosDoc = Mem_Cnx_YosDoc.cursor()
                    Mem_Cur_YosDoc.execute("SELECT cCap, cSubCap, cPrf, cTit, cTxt, cNul FROM Txt ORDER BY CAST(cCap AS INTEGER), CAST(cSubCap AS INTEGER), CAST(cPrf AS INTEGER)")
                    capitulos = Mem_Cur_YosDoc.fetchall()
                    Mem_Cnx_YosDoc.close()

                    if not capitulos:
                        ui.label('No hay capítulos creados.').classes('text-gray-400 p-2')
                        Mem_IniCap, Mem_IniSub, Mem_IniPrf = "0010", "0010", "0010"
                    else:
                        ultimo_registro = capitulos[-1]

                        # Extraemos los valores (según tu select: cCap=0, cSubCap=1, cPrf=2)
                        Mem_IniCap = ultimo_registro[0]
                        Mem_IniSub = ultimo_registro[1]
                        Mem_IniPrf = ultimo_registro[2]
                        Mem_IniPrf = f"{int(Mem_IniPrf) + 10:04d}"

                        # UNA SOLA TABLA HTML CON TODO
                        filas_html = []
                        for cap, SubCap, Prf, titulo, Txt, Nulo in capitulos:
                            ncap = int(cap)
                            nSubCap = int(SubCap)
                            nPrf = int(Prf)

                            if Txt.strip():
                                Txt = Txt.splitlines()[0]

                            # Texto a mostrar: solo si es "S" (oculto)
                            NulTxt = "OCULTO" if Nulo == "S" else ""

                            filas_html.append(f'''
                                <tr style="border-bottom: 1px solid #e5e7eb;">
                                    <td style="font-size: 0.75rem; font-weight: bold; color: #dc2626; padding: 2px 4px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; width: 60px;">{NulTxt}</td>
                                    <td style="font-family: monospace; font-size: 0.75rem; padding: 2px 8px; white-space: nowrap; width: 150px;">CAPITULO {ncap:>4}.{nSubCap:>4}.{nPrf:>4} :</td>
                                    <td style="font-size: 0.75rem; font-weight: bold; padding: 2px 8px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 200px;">{titulo or ''}</td>
                                    <td style="font-size: 0.75rem; color: #6b7280; padding: 2px 8px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{Txt or ''}</td>
                                    <td style="padding: 2px 8px; text-align: right; width: 110px;">
                                        <a href="/YosGesDoc_CapEdi?cap={cap}&sub={SubCap}&prf={Prf}" class="text-primary text-xs" style="text-decoration: none;">✎ SELECCIONAR</a>
                                    </td>
                                </tr>
                            ''')

                        tabla_completa = f'''
                            <table style="width: 100%; border-collapse: collapse; table-layout: fixed; margin: 0;">
                                <colgroup>
                                    <col style="width: 60px;">
                                    <col style="width: 150px;">
                                    <col style="width: 25%;">
                                    <col style="width: auto;">
                                    <col style="width: 110px;">
                                </colgroup>
                                {''.join(filas_html)}
                            </table>
                        '''

                        ui.html(tabla_completa).style('margin: 0; padding: 0; display: block;')

                except Exception as e:
                    ui.label(f'Error al leer capítulos: {e}').classes('text-red-500 p-2')

    Yos.Yos_PieAvs_Gui(Avs="Yos Gestión de Capítulos")
################################################################################################################################################################################
@ui.page('/YosGesDoc_CapEdi')
async def Pgn_YosGesDoc_CapEdi(cap: str = '', sub: str = '', prf: str = ''):

    global Mem_IniCap, Mem_IniSub, Mem_IniPrf

    Msg_HlpTxt = '''
    ATENCIÓN

    Use estos comandos con sumo cuidado; si no los transcribe correctamente, la aplicación puede que no dé los resultados previstos al generar el PDF.

    Etiqueta,Función,Ejemplo
    &lt;b&gt;Texto en negrita&lt;/b&gt; -> <b>Texto en negrita</b>
    &lt;i&gt;Texto en cursiva&lt;/i&gt; -> <i>Texto en cursiva</i>
    &lt;u&gt;Texto subrayado&lt;/u&gt; -> <u>Texto subrayado</u>
    H&lt;sub&gt;2&lt;/sub&gt;O Subíndice -> H<sub>2</sub>O
    E=mc&lt;sup&gt;2&lt;/sup&gt; Superíndice-> E=mc<sup>2</sup>
    E=mc&lt;super&gt;2&lt;/super&gt; Superíndice -> E=mc<super>2</super>

    &lt;font color="red"&gt;Texto rojo&lt;/font&gt; -> <font color="red">Texto rojo</font>
    &lt;font size="14"&gt;Otro tamaño&lt;/font&gt; -> <font size="14">Otro tamaño</font>
    &lt;br /&gt; -> Salto de linea

    Hipervínculo -> &lt;link href="https://www.google.com/"&gt;Enlace&lt;/link&gt;
    '''
#    Yos.Yos_Cab_Gui(Mem_Tit, Msg_HlpTxt)
    Yos.Yos_Cab_Gui(Tit=Mem_Tit, Hlp=Msg_HlpTxt, HlpTit ="Ayuda Edición del Capítulo")

    Mem_Svr = os.path.splitext(Mem_DocNom)[0]
    Mem_Ach = ""
    Nul_orig = ""  # Valor por defecto de cNul

    if cap:
        Mem_Cnx_YosDoc = Yos.Idd_BdtSvr_Cnx(Mem_Svr, Fnc_Mod="rw")
        Mem_Cur_YosDoc = Mem_Cnx_YosDoc.cursor()

        # Añadimos cNul a la consulta
        Mem_Cur_YosDoc.execute("SELECT cTit, cTxt, cNul FROM Txt WHERE cCap=? AND cSubCap=? AND cPrf=?", (cap, sub, prf))
        registro = Mem_Cur_YosDoc.fetchone()
        Mem_Cnx_YosDoc.close()

        if not registro:
            ui.notify("No se encontró el capítulo.", type='negative')
            return

        titulo_orig, txt_orig, Nul_orig = registro
        Mem_Ach = "Mod"
    else:
        titulo_orig = ""
        txt_orig    = ""
        Nul_orig = ""  # Por defecto visible (no oculto)
        Mem_Ach = "Cre"
        cap = Mem_IniCap
        sub = Mem_IniSub
        prf = Mem_IniPrf

    # 2.Mem_IniPrf Formulario de Edición
    with ui.element('div').classes('w-full pl-30 pr-4 py-4'):
        with ui.card().classes('w-full p-8 shadow-lg rounded-2xl'):

            ui.label('Detalle del Capítulo').classes('text-lg font-bold mb-4')

            # Fila de identificadores separados (Solo lectura)
            with ui.row().classes('w-full items-center gap-2 mb-4'):
                inp_cap = ui.input(label='Capítulo',    value=cap).classes('w-24').props('mask="####" inputmode="numeric"')
                inp_sub = ui.input(label='Subcapítulo', value=sub).classes('w-24').props('mask="####" inputmode="numeric"')
                inp_prf = ui.input(label='Párrafo',     value=prf).classes('w-24').props('mask="####" inputmode="numeric"')
                inp_nul = ui.select(label='Oculto', options={'': 'Visible', 'S': 'Oculto'}, value=Nul_orig if Nul_orig in ['', 'S'] else '').classes('w-24')

            inp_tit = ui.input(label='Título', value=titulo_orig).classes('w-full')

            # Texto
            inp_txt = ui.textarea(label='Texto', value=txt_orig).classes('w-full mt-4 flex-grow').props('rows=10')

            def Pgn_YosGesDoc_CapEdi_Mod():
                # Validación: Capitulo no puede esta vacio
                Mem_Num = int(inp_cap.value) if str(inp_cap.value).strip() else 0
                Mem_NumTxt ="Capítulo"
                if not Mem_Num:
                    ui.notify(f"El {Mem_NumTxt} no pueden ser cero.", type='warning')
                    return

                Mem_Num = int(inp_sub.value) if str(inp_sub.value).strip() else 0
                Mem_NumTxt ="Subcapítulo"
                if not Mem_Num:
                    ui.notify(f"El {Mem_NumTxt} no pueden ser cero.", type='warning')
                    return

                Mem_Num = int(inp_prf.value) if str(inp_prf.value).strip() else 0
                Mem_NumTxt ="Párrafo"
                if not Mem_Num:
                    ui.notify(f"El {Mem_NumTxt} no pueden ser cero.", type='warning')
                    return

                # Validación: Txt no puede estar vacío
                titulo_val = (inp_tit.value or "").strip()
                texto_val = (inp_txt.value or "").strip()
                if not titulo_val and not texto_val:
                    ui.notify("El Título y el Texto no pueden estar vacíos a la vez.", type='warning')
                    return

                v_cap = str(inp_cap.value).zfill(4)
                v_sub = str(inp_sub.value).zfill(4)
                v_prf = str(inp_prf.value).zfill(4)

                # Guardar en BDT
                Mem_Cnx_YosDoc = Yos.Idd_BdtSvr_Cnx(Mem_Svr, Fnc_Mod="rw")
                try:
                    if Mem_Ach == "Mod":
                        # Añadimos cNul al UPDATE
                        Mem_Cnx_YosDoc.execute(
                            "UPDATE Txt SET cCap=?, cSubCap=?, cPrf=?, cTit=?, cTxt=?, cNul=? WHERE cCap=? AND cSubCap=? AND cPrf=?",
                            (v_cap, v_sub, v_prf, inp_tit.value, inp_txt.value, inp_nul.value, cap, sub, prf)
                        )
                    else:
                        # Añadimos cNul al INSERT
                        Mem_Cnx_YosDoc.execute(
                            "INSERT INTO Txt (cCap, cSubCap, cPrf, cTit, cTxt, cNul) VALUES (?, ?, ?, ?, ?, ?)",
                            (v_cap, v_sub, v_prf, inp_tit.value, inp_txt.value, inp_nul.value)
                        )

                    Mem_Cnx_YosDoc.commit()
                    Mem_Cnx_YosDoc.close()
                    ui.notify("Cambios guardados correctamente.")
                    ui.navigate.to('/YosGesDoc_Cap')
                except Exception as e:
                    error_msg = str(e)
                    if "UNIQUE" in error_msg.upper():
                        ui.notify("Error: Capítulo/Subcapítulo/Párrafo ya existe.", type='negative')
                    else:
                        ui.notify(f"Error al guardar: {error_msg}", type='negative')
                finally:
                    Mem_Cnx_YosDoc.close()

            async def Pgn_YosGesDoc_CapEdi_Eli(cap, sub, prf):
                respuesta = await Yos.Yos_MsgPgt_Frm(Fnc_Tit="ATENCIÓN", Fnc_Msg = "¿ Eliminar Párrafo ?")
                if not respuesta:
                    return

                Mem_Svr = os.path.splitext(Mem_DocNom)[0]
                Mem_Cnx_YosDoc = Yos.Idd_BdtSvr_Cnx(Mem_Svr, Fnc_Mod="rw")
                try:
                    Mem_Cnx_YosDoc.execute("DELETE FROM Txt WHERE cCap=? AND cSubCap=? AND cPrf=?",
                                (str(cap).zfill(4), str(sub).zfill(4), str(prf).zfill(4)))
                    Mem_Cnx_YosDoc.commit()
                    ui.notify("Registro eliminado.", type='positive')
                    ui.navigate.to('/YosGesDoc_Cap')
                except Exception as e:
                    ui.notify(f"Error al eliminar: {e}", type='negative')
                finally:
                    Mem_Cnx_YosDoc.close()

            with ui.row().classes('w-full justify-end gap-2 mt-4'):
                ui.button('GUARDAR', on_click=Pgn_YosGesDoc_CapEdi_Mod).props('unelevated')
                ui.button('ELIMINAR', icon='delete', on_click=lambda: Pgn_YosGesDoc_CapEdi_Eli(cap, sub, prf)).props('flat dense color=red').classes('text-red-500')
                ui.button('CANCELAR', on_click=lambda: ui.navigate.to('/YosGesDoc_Cap')).props('flat color=red')

        Yos.Yos_PieAvs_Gui(Avs="Edición del Capítulo")

#######################################################################
@ui.page('/YosGesDoc_Ipr')
async def Pgn_YosGesDoc_Ipr():
    Yos.Yos_Cab_Gui(Tit=Mem_Tit)
#def YosGesDoc_Ipr():
    # VERIFICACIÓN DE SEGURIDAD
    if not Mem_DocNom:
        ui.notify("No se ha seleccionado ningún documento.", type='warning', position='center')
        ui.run_javascript('setTimeout(() => { window.location.href = "/YosGesDoc"; }, 2000);')  # 2000 = 2 Segundos
        return

    global TITULO_GLOBAL_HEADER, PAGINA_CORTE_INDICE, Mem_PagAct
    recolector_indice.entradas = []

    with ui.column().classes('w-full items-center justify-center p-10'):
        msg_label = ui.label('GENERANDO DOCUMENTO, ...').classes('text-2xl font-bold text-blue-600')

    nombre_bdt = os.path.splitext(Mem_DocNom)[0]

    conn = Yos.Idd_BdtSvr_Cnx(nombre_bdt, Fnc_Mod="ro")
    cur = conn.cursor()
    info = cur.execute("SELECT cTit, cSub, cAtr, cYea, cEdi, cLug, cIsb, cCpy, cDup FROM Inf LIMIT 1").fetchone()
    registros = cur.execute("SELECT cCap, cSubCap, cPrf, cTit, cTxt FROM Txt WHERE cNul IS NOT 'S' ORDER BY cCap, cSubCap, cPrf").fetchall()
    conn.close()

    c_tit, c_sub, c_atr, c_yea, c_edi, c_lug, c_isb, c_cpy, c_dup = info if info else ("MANUAL", "", "", "", "", "", "", "", "")

    tit_formateado = c_tit.strip() if c_tit else "Manual"
    sub_formateado = f" - {c_sub.strip()}" if c_sub and c_sub.strip() else ""
    archivo_tit = tit_formateado.replace(" ", "_")
    archivo_sub = f"_-_{c_sub.strip().replace(' ', '_')}" if c_sub and c_sub.strip() else ""
    Mem_Rut = os.path.join(YosAplCfg["Apl"]["Dir"], "Doc", f"{archivo_tit}{archivo_sub}.pdf")

    Mem_Dup = c_dup   # DUPLEX

    TITULO_GLOBAL_HEADER = f"{c_tit.strip()} {'- ' + c_sub.strip() if c_sub.strip() else ''}"

    doc = SimpleDocTemplate(
        Mem_Rut,
        pagesize=letter,
        rightMargin=54,
        leftMargin=54,
        topMargin=72,
        bottomMargin=54
    )

    # --- TUS ESTILOS PROFESIONALES ---
    estilos = getSampleStyleSheet()

    # Estilos de Portada y Ficha
    estilo_portada_tit = ParagraphStyle('PortadaTitulo', parent=estilos['Normal'], fontName='Helvetica-Bold', fontSize=34, leading=40, alignment=TA_CENTER, spaceAfter=20)
    estilo_portada_sub = ParagraphStyle('PortadaSubTitulo', parent=estilos['Normal'], fontName='Helvetica', fontSize=20, leading=26, alignment=TA_CENTER, textColor='#444444')
    estilo_ficha_tit = ParagraphStyle('FichaEtiqueta', parent=estilos['Normal'], fontName='Helvetica-Bold', fontSize=11, leading=16, alignment=TA_LEFT, spaceAfter=4)
    estilo_ficha_txt = ParagraphStyle('FichaTexto', parent=estilos['Normal'], fontName='Helvetica', fontSize=11, leading=16, alignment=TA_LEFT, spaceAfter=14)

    estilo_ficha_cpy = ParagraphStyle('FichaCopyright', parent=estilos['Normal'], fontName='Helvetica', fontSize=10, leading=15, alignment=TA_JUSTIFY, spaceBefore=20, textColor='#333333')

    # Estilos de Contenido
    estilo_seccion = ParagraphStyle('SeccionTitulo', parent=estilos['Normal'], fontName='Helvetica-Bold', fontSize=20, leading=26, alignment=TA_CENTER, spaceBefore=10, spaceAfter=20, keepWithNext=True)
    estilo_parrafo_tit = ParagraphStyle('ParrafoInternoTitulo', parent=estilos['Normal'], fontName='Helvetica-Bold', fontSize=13, leading=17, alignment=TA_LEFT, spaceBefore=12, spaceAfter=6, keepWithNext=True)
    estilo_cuerpo = ParagraphStyle('CuerpoParrafo', parent=estilos['Normal'], fontName='Helvetica', fontSize=11, leading=16, alignment=TA_JUSTIFY, spaceAfter=12)

    # Estilos Especiales para la Tabla del Índice
    estilo_idx_base = ParagraphStyle('IdxBase', parent=estilos['Normal'], fontName='Helvetica', fontSize=11, leading=16)
    estilo_idx_num = ParagraphStyle('IdxNum', parent=estilos['Normal'], fontName='Helvetica-Bold', fontSize=11, leading=16, alignment=TA_RIGHT)

    # 1. PORTADA
    historia = []
    historia.append(Spacer(1, 180))
    historia.append(Paragraph(c_tit.strip() if c_tit else "MANUAL", estilo_portada_tit))
    if c_sub:
        historia.append(Spacer(1, 10))
        historia.append(Paragraph(c_sub.strip(), estilo_portada_sub))
    historia.append(PageBreak())

    # 2. COLOFÓN (TU LÓGICA TEXTUAL EXACTA)
    historia.append(Spacer(1, 40))
    if c_tit:
        historia.append(Paragraph("<b>Título de la obra:</b>", estilo_ficha_tit))
        historia.append(Paragraph(c_tit.strip(), estilo_ficha_txt))
    if c_sub:
        historia.append(Paragraph("<b>Subtítulo:</b>", estilo_ficha_tit))
        historia.append(Paragraph(c_sub.strip(), estilo_ficha_txt))
    if c_atr:
        historia.append(Paragraph("<b>Autor:</b>", estilo_ficha_tit))
        historia.append(Paragraph(c_atr.strip(), estilo_ficha_txt))
    if c_edi:
        historia.append(Paragraph("<b>Edición:</b>", estilo_ficha_tit))
        historia.append(Paragraph(c_edi.strip(), estilo_ficha_txt))
    if c_lug or c_yea:
        historia.append(Paragraph("<b>Publicación:</b>", estilo_ficha_tit))
        lugar_ano = f"{c_lug.strip() if c_lug else ''} {c_yea.strip() if c_yea else ''}".strip()
        historia.append(Paragraph(lugar_ano, estilo_ficha_txt))
    if c_isb:
        historia.append(Paragraph("<b>ISBN:</b>", estilo_ficha_tit))
        historia.append(Paragraph(c_isb.strip(), estilo_ficha_txt))
    if c_cpy:
        historia.append(Paragraph(c_cpy.strip().replace("\n", "<br/>"), estilo_ficha_cpy))
    historia.append(PageBreak())

    # 3. CUERPO
    '''
    for cCap, cSubCap, cPrf, cTit, cTxt in registros:
        if cTit:
            historia.append(MarcadorCapitulo(cTit, es_sub=False))
            historia.append(Paragraph(cTit, estilo_seccion))
        if cTxt:
            historia.append(Paragraph(cTxt, estilo_cuerpo))
    '''
    # PAGINA 3 EN ADELANTE: CONTENIDO FLUYENTE
    primer_contenido = True

    for cCap, cSubCap, cPrf, cTit, cTxt in registros:
        titulo = cTit.strip() if cTit else ""
        texto_parrafo = cTxt.strip() if cTxt else ""

        if titulo and not texto_parrafo:
            if not primer_contenido:
                historia.append(PageBreak())

            historia.append(Paragraph(titulo, estilo_seccion))
            # Inyectamos el marcador para títulos principales de capítulos
            historia.append(MarcadorCapitulo(titulo, es_sub=False))
            primer_contenido = False

        elif texto_parrafo:
            if titulo:
                # Inyectamos el marcador justo antes del párrafo para capturar su página exacta
                historia.append(MarcadorCapitulo(titulo, es_sub=True))
                historia.append(Paragraph(titulo, estilo_parrafo_tit))
            historia.append(Paragraph(texto_parrafo, estilo_cuerpo))
            primer_contenido = False

    # =========================================================================
    # CONSTRUCCIÓN DINÁMICA DEL ÍNDICE AL FINAL DEL LIBRO
    # =========================================================================
    historia.append(PageBreak())

    # Inyectamos el marcador que indica el inicio del Índice
    historia.append(MarcadorCapitulo("", es_arranque_indice=True))
    historia.append(Paragraph("ÍNDICE GENERAL", estilo_seccion))
    historia.append(Spacer(1, 15))

    from reportlab.platypus import Table, TableStyle
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

    pdfmetrics.registerFont(TTFont('CourierPS', 'cpsr45w.ttf'))
    estilo_idx_base.fontName = 'CourierPS'
    estilo_idx_base.fontSize = 11
    estilo_idx_base.leading = 16

    # --- SIMULACIÓN Y DUPLEX TRATADO (PAGINAS EN BLANCO) ---

    # Pass 1: Simulación para recolectar páginas originales
    recolector_indice.entradas = []
    PAGINA_CORTE_INDICE = 999999

    historia_copia = copy.deepcopy(historia)
    doc.build(
        historia_copia,
        onFirstPage=detectar_paginas_y_marcar,
        onLaterPages=detectar_paginas_y_marcar
    )

    if Mem_Dup == "S":
        # 1. Recolectar marcadores principales en historia
        chapter_markers = []
        for j, flowable in enumerate(historia):
            if isinstance(flowable, MarcadorCapitulo):
                if not flowable.es_sub:
                    chapter_markers.append({
                        'story_index': j,
                        'title': flowable.titulo,
                        'es_index': flowable.es_arranque_indice
                    })

        # 2. Recolectar páginas de inicio reales de cada capítulo
        main_chapters_pages = [pag for title, pag, es_sub in recolector_indice.entradas if not es_sub]
        chapter_start_pages = main_chapters_pages + [PAGINA_CORTE_INDICE - 2]

        # 3. Determinar qué capítulos necesitan página en blanco
        chapters_needing_blank = set()
        if len(chapter_markers) == len(chapter_start_pages):
            for i in range(len(chapter_markers) - 1):
                start = chapter_start_pages[i]
                end = chapter_start_pages[i+1]
                length = end - start
                if length % 2 != 0:
                    chapters_needing_blank.add(i + 1)

        # 4. Encontrar los índices de PageBreak a los que insertar antes
        pb_indices_to_insert_before = {}
        for k in chapters_needing_blank:
            marker = chapter_markers[k]
            pb_idx = -1
            for idx in range(marker['story_index'] - 1, -1, -1):
                if isinstance(historia[idx], PageBreak):
                    pb_idx = idx
                    break
            if pb_idx != -1:
                pb_indices_to_insert_before[pb_idx] = k

        # 5. Reconstruir historia con las páginas en blanco insertadas
        nueva_historia = []
        for idx, flowable in enumerate(historia):
            if idx in pb_indices_to_insert_before:
                nueva_historia.append(PageBreak())
                estilo_blanco = ParagraphStyle('Blanco', parent=estilos['Normal'], alignment=TA_CENTER, fontSize=12, fontName='Helvetica-Oblique')
                nueva_historia.append(Spacer(1, 300))
                nueva_historia.append(Paragraph("Página EN BLANCO", estilo_blanco))

            nueva_historia.append(flowable)

        historia = nueva_historia

        # Pass 2: Segunda simulación (con páginas en blanco) para actualizar recolector_indice.entradas y PAGINA_CORTE_INDICE
        recolector_indice.entradas = []
        PAGINA_CORTE_INDICE = 999999
        historia_copia2 = copy.deepcopy(historia)
        doc.build(
            historia_copia2,
            onFirstPage=detectar_paginas_y_marcar,
            onLaterPages=detectar_paginas_y_marcar
        )

    # Montamos la tabla visual del Índice recorriendo todas las entradas guardadas
    datos_tabla_indice = []
    for titulo_idx, pag_idx, es_sub in recolector_indice.entradas:
        Mem_Tot = 68
        puntos_relleno = " . " * Mem_Tot

        if es_sub:
#            pag_idx =1250
            Mem_Num = f"{pag_idx:>5,}".replace(" ", "&nbsp;")
            # Párrafos internos: agregamos sangría y formato normal
            Mem_Txt = f"&nbsp;&nbsp;&nbsp;&nbsp;{titulo_idx} "
            Mem_Lnf = len(Mem_Txt.replace("&nbsp;", " "))
            Mem_Lnf = Mem_Tot - Mem_Lnf
            puntos_relleno = "." * Mem_Lnf
            col_izquierda = Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;{titulo_idx} {puntos_relleno} {Mem_Num}", estilo_idx_base)
        else:
#            pag_idx =180
            Mem_Num = f"{pag_idx:>5,}".replace(" ", "&nbsp;")
            # Capítulos principales: texto destacado en negrita
            Mem_Txt = f"{titulo_idx} "
            Mem_Lnf = len(Mem_Txt.replace("&nbsp;", " "))
            Mem_Lnf = Mem_Tot - Mem_Lnf
            puntos_relleno = "." * Mem_Lnf
            col_izquierda = Paragraph(f"<b>{titulo_idx}</b> {puntos_relleno} {Mem_Num}", estilo_idx_base)

        col_derecha = Paragraph(str(pag_idx), estilo_idx_num)
#        datos_tabla_indice.append([col_izquierda, col_derecha])
        datos_tabla_indice.append([col_izquierda])

    if datos_tabla_indice:
        tabla_idx = Table(datos_tabla_indice, colWidths=[504])
        tabla_idx.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'BOTTOM')]))
#        tabla_idx = Table(datos_tabla_indice, colWidths=[450, 54])
#        tabla_idx.setStyle(TableStyle([
#            ('VALIGN', (0,0), (-1,-1), 'BOTTOM'),
#            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
#            ('TOPPADDING', (0,0), (-1,-1), 0),
#        ]))
        historia.append(tabla_idx)

    # =========================================================================
    # Si existe la Base de Datos Nombre_Def
    # =========================================================================

    # CONSTRUCCIÓN FÍSICA FINAL (Segunda pasada real)
    doc.pageMode = 'UseNone'
    doc.pageLayout = 'SinglePage'

    doc.build(
        historia,
        onFirstPage=detectar_paginas_y_marcar,
        onLaterPages=detectar_paginas_y_marcar
    )

    Mem_Txt = f'RUTA : {Mem_Rut}'

    with ui.column().classes('w-full items-center justify-center p-10'):
        ui.label('DOCUMENTO GENERADO').classes('text-2xl font-bold text-green-600')
        ui.label(Mem_Txt).classes('text-sm text-gray-500')

    await asyncio.sleep(0.1)

    async def lanzar_dialogo():
        respuesta = await Yos.Yos_Msg_Gui(Fnc_Tit="GENERADO PDF", Fnc_Msg=Mem_Txt, Fnc_Tip="Inf", Ancho="40")
        #Yos.Yos_MsgPgt_Frm(Fnc_Tit="ATENCIÓN", Fnc_Bot="SÍ/NO", Fnc_Msg="¿ Desea Salir ?", Ancho="400px", Alto="auto") #moco()
        if respuesta:
            ui.navigate.to('/YosGesDoc')

    ui.timer(0.1, lanzar_dialogo, once=True)
    # 5. Redirección limpia (sin Javascript manual)
    #ui.navigate.to('/YosGesDoc')

#    ui.run_javascript('setTimeout(() => { window.location.href = "/YosGesDoc"; }, 8000);')  # 2000 = 2 Segundos
