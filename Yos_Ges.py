#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Miguel Tortosa

Yos_Ges_Txt.py  .Py donde estan todas las Def _Txt

Gestión Definiciones Txt, para el entorno Texto con base en prompt_toolkit

Estructura nombre Def

PREFIJO DESCRIPCION
Yos_    Def de uso General

SUFIJO
_Txt -> Modo Texto -> Terminal / Consola

"""

import os
import datetime
import shutil

from colorama import Fore, Style, init
init(autoreset=True)

###################################################################################  Inicio Def ###################################################################################
# ******************************************************************************************************************************************* Yos_MsgSis_Tui
def Yos_MsgSis(**Fnc_Dic):
    # Memsajes del Sistema en Tui
    # Yos_SutTxt(Txt=MnuFnc)    # Sis
    # Yos.Yos_MsgSis(Txt= "Mensaje", Tip= "Err")

    ''' Valores
        Txt = Texto
        Tip = Tipo del Mensaje, por Omision Sis
    '''

    # Sacamos la lista de campos. Si no viene, usamos uno por defecto.
    Mem_Txt = Fnc_Dic.get("Txt","")
    Mem_Tip = Fnc_Dic.get("Tip","Sis")
    if not Mem_Tip:
        Mem_Tip = "Sis"

    Mem_Col = Yos_RegApl_VfyTip(Tip=Mem_Tip)
    if Mem_Col == "Err":
        Mem_Col =Yos_RegApl_VfyTip(Tip= "Err")
        Mem_Txt = f'ERROR : TIPO {Mem_Tip} INEXISTENTE EN Yos_RegApl_VfyTip(){Yos_RegApl_VfyTip(Tip= "Sis")} -> '+ Mem_Txt
        Mem_Tip = "Sis"

    Mem_Tim = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"  {Mem_Col}{Mem_Tip} -> {str(Mem_Txt)}{Style.RESET_ALL}", flush=True)

    Yos_RegApl(Txt=Mem_Txt, Tip=Mem_Tip)

# ******************************************************************************************************************************************* FIN - Yos_MsgSis_Tui
# ******************************************************************************************************************************************* Yos_RegApl
def Yos_RegApl(**Fnc_Dic):
    # Crea un Registro en /Reg
    # Yos_RegApl(Txt=MnuFnc)    # Sis
    # Yos.Yos_RegApl(Txt= "Mensaje", Tip= "Err")

    ''' Valores
        Txt = Texto
        Tip = Tipo del Mensaje, por Omision Sis
    '''

    # Sacamos la lista de campos. Si no viene, usamos uno por defecto.
    Mem_Txt = Fnc_Dic.get("Txt","")
    Mem_Tip = Fnc_Dic.get("Tip","Sis")
    if not Mem_Tip:
        Mem_Tip = "Sis"

    Mem_DirApl = os.path.join(os.getcwd()  +"\\" )  # Directorio de la Aplicacion
    Mem_Dir = os.path.join(Mem_DirApl  +"\\" , "Reg")  # Directorio de la Aplicacion
    Mem_DirAnt = os.path.join(Mem_Dir, "Vie")
    Mem_Ext = "YosReg" # Extension de los Archivos
    Mem_AplNom = os.path.basename(os.getcwd())

    Mem_Tim = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    Mem_Ach = os.path.join(Mem_Dir, f"{Mem_Tip}.{Mem_Ext}")

    if Mem_Tip == "«LogIni»":
        Mem_Tip = "Sis"
        Mem_Ach = os.path.join(Mem_Dir, f"{Mem_Tip}.{Mem_Ext}")

        if not os.path.exists(Mem_DirAnt):
            os.makedirs(Mem_DirAnt)

        # Mover todos los .log existentes a /Vie
        for archivo in os.listdir(Mem_Dir):
            if archivo.endswith(f".{Mem_Ext}"):
                shutil.move(os.path.join(Mem_Dir, archivo), os.path.join(Mem_DirAnt, archivo))

        with open(Mem_Ach, 'w', encoding='utf-8') as f:
            f.write("CONTROL DE INCIDENCIAS SISTEMA Yos\n")
            f.write("----------------------------------\n")
            f.write(f"{Mem_Tim} -> INICIANDO APLICACION - {Mem_AplNom}\n")
            f.write(f"{Mem_Tim} -> DIRECTORIO - {Mem_DirApl}\n")

        return

    Mem_Col = Yos_RegApl_VfyTip(Tip=Mem_Tip)
    if Mem_Col == "Err":
        Mem_Col = Yos_RegApl_VfyTip(Tip= "Sis")

    Mem_TxtIp = ""

    import builtins
    if hasattr(builtins, "YosAplCfg"):
        if YosAplCfg.get("Apl", {}).get("Usr_Ipd"):
            Mem_TxtIp += f'{YosAplCfg["Apl"]["Usr_Ipd"]} - '

        if YosAplCfg.get("Apl", {}).get("Usr_Nik"):
            Mem_TxtIp += f'{YosAplCfg["Apl"]["Usr_Nik"]} - '

    if Mem_TxtIp:
        Mem_Txt = Mem_TxtIp + Mem_Txt

    with open(Mem_Ach, 'a', encoding='utf-8') as f:
        f.write(f"{Mem_Tim} -> {Mem_Txt}\n")
#    print(f'{Yos.Yos_TimeStamp()} -> {YosSes["Usr_Ipd"]} - {YosSes["Usr_Nik"]} : EJECUTA {YosSes["Apl_Def"]}')

# ******************************************************************************************************************************************* FIN - Yos_RegApl
# ******************************************************************************************************************************************* Yos_RegApl_VfyTip
def Yos_RegApl_VfyTip(**Fnc_Dic):
    # Verifico si el tipo de Registros existe
    # Yos.Yos_RegApl_VfyTip(Tip= "Err")

    ''' Valores
        Tip = Tipo del Mensaje
    '''
    # Sacamos la lista de campos. Si no viene, usamos uno por defecto.
    Mem_Tip = Fnc_Dic.get("Tip","")

    # Diccionario de estilos por tipo de mensaje
    Mem_Dic_Col = {
        "Sis": Fore.CYAN,           # Información del Sistema
        "Err": Fore.RED,            # Errores graves
        "Inf": Fore.GREEN,          # Informacion
        "Avs": Fore.YELLOW,         # Avisos
        "Msg": Fore.WHITE           # Mensajes estándar
    }

    # Devuelve el Color
    Mem_Col = Mem_Dic_Col.get(Mem_Tip, "Err")

    return Mem_Col

# ******************************************************************************************************************************************* FIN - Yos_RegApl

###################################################################################  A REVISAR ###################################################################################
# *******************************************************************************************************************************************
# ******************************************************************************************************************************************* FIN -
# ******************************************************************************************************************************************* Yos_MstDir_Tui
def Yos_MstDir_Tui(ruta_base):
    """
    Modo Texto: Llama al motor y hace un print estructurado.
    """
    datos = Yos.Yos_MstDir(ruta_base)
    print(f"\n--- Contenido de: {ruta_base} ---")
    for item in datos:
        tipo = "[DIR]" if item['es_dir'] else "[FILE]"
        print(f"{tipo} {item['nombre']}")
# ******************************************************************************************************************************************* FIN - Yos_MstDir_Tui


# ******************************************************************************************************************************************* Yos_Msg_Tui
from textual.app import App
from textual.widgets import Static, Button, Label
from textual.containers import Vertical, Container, Horizontal

class Yos_Msg_Tui_Css(App):
    CSS = """
    Screen {
        layout: vertical;
        background: black;
        align: center top;
    }

    #rotulo_box {
        width: 100%;
        text-align: center;
        color: $accent;
        dock: top;
        margin-top: 0;
        padding-top: 1;
    }

    #dialog_container {
        width: 100%;
        height: auto; /* IMPORTANTE: Deja que el contenedor sea tan alto como su contenido */
        align: center middle;
    }

    #dialog {
        /* Usamos width con una unidad relativa o el valor dinámico calculado */
        width: 60;        /* Un ancho base cómodo para lectura */
        max-width: 90;    /* Límite máximo para pantallas grandes */
        height: auto;
        padding: 0 1;
        background: black;
        border: heavy $accent;
    }

    #title {
        text-style: bold;
        text-align: center;
        width: 100%;
        margin-bottom: 1;
    }

    #body {
        text-align: left;
        width: 100%;      /* El texto debe ocupar el 100% de la caja */
        height: auto;
    }

    Button {
        width: 100%;      /* El botón SI debe ocupar el 100% de la caja */
        height: 3;
        margin-top: 1;    /* Separación clara */
        background: black;
        border: heavy $accent;
    }

    /* Clases dinámicas para el hover según el color de la caja */
    .hover-blue:hover { background: blue; color: black; }
    .hover-red:hover { background: red; color: black; }
    .hover-yellow:hover { background: yellow; color: black; }
    .hover-green:hover { background: green; color: black; }
    """

    def __init__(self, rotulo, titulo, mensaje, tipo):
        super().__init__()
        self.rotulo = rotulo
        self.titulo = titulo
        self.mensaje = mensaje
        self.tipo = tipo

    def compose(self):
        yield Static(self.rotulo, id= "rotulo_box", markup=False)
        with Container(id= "dialog_container"):
            with Vertical(id= "dialog"):
                yield Label(self.titulo, id= "title")
                yield Static(self.mensaje, id= "body")
                yield Button("CERRAR", id= "btn_close")

    def on_mount(self):
        # 1. Definimos los mapeos
        color_map = {"Inf": "blue", "Err": "red", "Atn": "yellow", "Std": "green"}
        class_map = {"Inf": "hover-blue", "Err": "hover-red", "Atn": "hover-yellow", "Std": "hover-green"}

        border_color = color_map.get(self.tipo, "blue")
        hover_class = class_map.get(self.tipo, "hover-blue")

        # 2. Aplicamos estilos y la clase específica para el hover
        btn = self.query_one("Button")
        btn.add_class(hover_class)
        btn = self.query_one("#btn_close", Button)
        btn.focus()

        # --- AQUI PONEMOS EL AJUSTE DE ANCHO ---
        ancho_total = int(YosAplCfg["Apl"]["Etn_Lon"] if YosAplCfg["Apl"]["Etn_Lon"] else 80)
        ancho_final = max(40, ancho_total - 4)
        dialog = self.query_one("#dialog")
        dialog.styles.width = ancho_final
        dialog.styles.border = ("heavy", border_color)
        # ---------------------------------------

        self.query_one("#dialog").styles.border = ("heavy", border_color)
        self.query_one("#title").styles.color = border_color
        btn.styles.border = ("heavy", border_color)



    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "btn_close":
            self.exit()

    def on_key(self, event):
        if event.key == "space":
            btn = self.query_one("#btn_close", Button)
            if btn.has_focus:
                btn.press()

def Yos_Msg_Tui(Fnc_Tit= "ATENCION", Fnc_Msg= "Mem_Dat", Fnc_Tip= "Inf", Fnc_Hx=None):
    datos = YosAplCfg["Apl"]["Rot"]
    rotulo_ascii = "\n".join(datos) if isinstance(datos, list) else str(datos)
    Fnc_Msg = Fnc_Msg.replace("«Esp»", " ")

    app = Yos_Msg_Tui_Css(rotulo=rotulo_ascii, titulo=Fnc_Tit, mensaje=Fnc_Msg, tipo=Fnc_Tip)
    app.run()

# ******************************************************************************************************************************************* FIN - Yos_Msg_Tui

# ******************************************************************************************************************************************* Yos_MsgPgt_Tui
class Yos_MsgPgt_Tui_Css(App):
    CSS = """
    Screen {
        layout: vertical;
        background: black;
        align: center top;
    }

    #rotulo_box {
        width: 100%;
        text-align: center;
        color: $accent;
        dock: top;
        margin-top: 0;
        padding-top: 1;
    }

    #dialog_container {
        width: 100%;
        height: auto;
        align: center middle;
    }

    #dialog {
        width: 60;
        max-width: 90;
        height: auto;
        padding: 0 1;              /* padding horizontal, vertical mínimo */
        background: black;
        border: heavy $accent;
    }

    #title {
        text-style: bold;
        text-align: center;
        width: 100%;
        margin: 0;                 /* ← Sin márgenes */
        padding: 0;                /* ← Sin padding */
        height: auto;
    }

    #body {
        text-align: left;
        width: 100%;
        height: auto;
        margin: 0;                 /* ← Sin márgenes */
        padding: 0;                /* ← Sin padding */
    }

    .button_container {
        layout: horizontal;
        width: 100%;
        height: auto;
        align: center middle;
        margin-top: 1;             /* Solo espacio antes de botones */
    }

    Button {
        width: 1fr;
        height: 3;
        margin: 0 1;
        background: black;
        border: heavy $accent;
        text-style: bold;
    }

    /* Foco */
    Button:focus {
        background: blue;
        color: black;
    }
    Button.hover-blue:focus   { background: blue;   color: black; }
    Button.hover-red:focus    { background: red;    color: black; }
    Button.hover-yellow:focus { background: yellow; color: black; }
    Button.hover-green:focus  { background: green;  color: black; }

    /* Hover */
    .hover-blue:hover   { background: blue;   color: black; }
    .hover-red:hover    { background: red;    color: black; }
    .hover-yellow:hover { background: yellow; color: black; }
    .hover-green:hover  { background: green;  color: black; }
    """

    def __init__(self, rotulo, titulo, mensaje, botones=None):
        super().__init__()
        self.rotulo = rotulo
        self.titulo = titulo
        self.mensaje = mensaje
        self.botones = botones if botones else ["SÍ", "NO"]
        self.resultado = None

    def compose(self):
        yield Static(self.rotulo, id= "rotulo_box", markup=False)
        with Container(id= "dialog_container"):
            with Vertical(id= "dialog"):
                yield Label(self.titulo, id= "title")
                yield Static(self.mensaje, id= "body")
                with Horizontal(classes= "button_container"):
                    yield Button(self.botones[0], id= "btn_a", variant= "primary")
                    yield Button(self.botones[1], id= "btn_b", variant= "default")

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "btn_a":
            self.resultado = self.botones[0]
        else:
            self.resultado = self.botones[1]
        self.exit()

    def on_key(self, event):
        btn_a = self.query_one("#btn_a", Button)
        btn_b = self.query_one("#btn_b", Button)

        if event.key == "space":
            if btn_a.has_focus:
                btn_a.press()
            elif btn_b.has_focus:
                btn_b.press()

        elif event.key in ("left", "right", "tab"):
            if btn_a.has_focus:
                btn_b.focus()
            else:
                btn_a.focus()

    def on_mount(self):
        color_map = {"Inf": "blue", "Err": "red", "Atn": "yellow", "Std": "green"}
        class_map = {"Inf": "hover-blue", "Err": "hover-red", "Atn": "hover-yellow", "Std": "hover-green"}

        border_color = "blue"
        hover_class = "hover-blue"

        ancho_total = int(YosAplCfg["Apl"].get("Etn_Lon", 80))
        ancho_final = max(40, ancho_total - 4)
        dialog = self.query_one("#dialog")
        dialog.styles.width = ancho_final
        dialog.styles.border = ("heavy", border_color)

        self.query_one("#title").styles.color = border_color

        for btn in self.query("Button"):
            btn.add_class(hover_class)
            btn.styles.border = ("heavy", border_color)

        self.query_one("#btn_b", Button).focus()


def Yos_MsgPgt_Tui(Fnc_Tit= "ATENCION", Fnc_Msg= "Mem_Dat", Fnc_Bot= "SÍ/NO"):
    datos = YosAplCfg["Apl"].get("Rot", [])
    rotulo_ascii = "\n".join(datos) if isinstance(datos, list) else str(datos)
    Fnc_Msg = Fnc_Msg.replace("«Esp»", " ")

    lista_botones = Fnc_Bot.split("/") if "/" in Fnc_Bot else ["SÍ", "NO"]

    app = Yos_MsgPgt_Tui_Css(rotulo=rotulo_ascii, titulo=Fnc_Tit, mensaje=Fnc_Msg, botones=lista_botones)
    app.run()

    return app.resultado

##########################################
def Yos_MsgPgt_Txt(Fnc_Tit= "ATENCION", Fnc_Msg= "Mem_Dat", Fnc_Bot= "SÍ/NO", Fnc_Hx=None):
    Yos_Cls_Txt()
    FrmCab(Fnc_Dat= "Cab")
    print("\n\n")

    from prompt_toolkit.shortcuts import clear
    from prompt_toolkit.widgets import Button, Frame
    from prompt_toolkit.layout.containers import HSplit, VSplit, Window
    from prompt_toolkit.layout.controls import FormattedTextControl
    from prompt_toolkit.application import Application
    from prompt_toolkit.layout.layout import Layout
    from prompt_toolkit.key_binding import KeyBindings
    from prompt_toolkit.styles import Style
    from prompt_toolkit.formatted_text import HTML
    from prompt_toolkit.layout.dimension import D

    # --- 1. CONFIGURACIÓN DE RESPUESTA ---
    Mem_Res = [None]
    Bot_Txt = Fnc_Bot.split("/")
    Bot_A = Bot_Txt[0].strip() if len(Bot_Txt) > 0 else "SÍ"
    Bot_B = Bot_Txt[1].strip() if len(Bot_Txt) > 1 else "NO"

    # --- 2. COLORES ---
    Mem_Col = "#1976d2"  # Azul Corporativo

    # --- 3. FORMATEADOR ---
    Mem_Msg = str(Fnc_Msg).replace("<br>", "\n").replace("<br/>", "\n").replace("&nbsp;", " ")
    Mem_Msg = Mem_Msg.replace("<b>", "<negrita>").replace("</b>", "</negrita>")

    if not Fnc_Hx:
        lineas = Mem_Msg.splitlines() or [Mem_Msg]
        linea_mas_larga = max(len(l) for l in lineas)

        # +6: márgenes internos + bordes del frame (ajústalo a gusto)
        Fnc_Hx = linea_mas_larga + 6
        # límites de seguridad para que no se rompa en terminales pequeñas/grandes
        Fnc_Hx = max(30, min(Fnc_Hx, 100))

    # --- 4. ESTILO ---
    Yos_Estilo = Style.from_dict({
        'frame': f'bg:#000000 fg:{Mem_Col}',
        'frame.border': f'fg:{Mem_Col}',
        'frame.label': 'fg:#ffffff bold',

        'body': 'bg:#000000 fg:#ffffff',
        'negrita': 'fg:#ffffff bold',

        # Barra azul
        'btnbar': f'bg:{Mem_Col} fg:#ffffff',

        # Botones más visibles
        'button': 'bg:#0d47a1 fg:#ffffff bold',
        'button.focused': 'bg:#ffffff fg:#0d47a1 bold',
    })

    # --- 5. CONSTRUCCIÓN ---
    def Sal_Bot_A():
        Mem_Res[0] = Bot_A
        app.exit()

    def Sal_Bot_B():
        Mem_Res[0] = Bot_B
        app.exit()

    # Más grandes (padding en texto)
    btn_a = Button(text=f"   {Bot_A}   ", handler=Sal_Bot_A, left_symbol= "", right_symbol= "")
    btn_b = Button(text=f"   {Bot_B}   ", handler=Sal_Bot_B, left_symbol= "", right_symbol= "")

    # Barra: relleno flexible izquierda/derecha para centrar grupo de botones
    barra_botones = VSplit(
        [
            Window(style='class:btnbar'),                # flexible izquierda
            btn_a,
            Window(width=5, style='class:btnbar'),       # espacio fijo entre botones
            btn_b,
            Window(style='class:btnbar'),                # flexible derecha
        ],
        height=1,
        style='class:btnbar'
    )

    cuerpo_fijo = HSplit(
        [
            Window(content=FormattedTextControl(HTML(f" {Mem_Msg}")), dont_extend_height=True, style='class:body'),
            Window(height=1, style='class:body'),
            barra_botones
        ],
        width=Fnc_Hx - 2,   # interior del frame
        style='class:body',
        padding=0
    )

    ventana_frame = Frame(
        title=f"{Fnc_Tit}",
        body=cuerpo_fijo,
        width=Fnc_Hx
    )

    # CENTRADO REAL EN PÁGINA (horizontal y vertical)
    layout_final = HSplit(
        [
            Window(height=0),  # ajusta: 0, 1 o 2 según cuánto ocupe tu rótulo real
            VSplit(
                [
                    Window(),          # relleno izq
                    ventana_frame,     # tu frame
                    Window(),          # relleno der
                ]
            ),
            Window(),  # relleno abajo
        ]
    )

    # --- 6. EJECUCIÓN ---
    kb = KeyBindings()

    @kb.add('escape')
    def _(event):
        Mem_Res[0] = False
        app.exit()

    @kb.add('left')
    def _(event):
        event.app.layout.focus_previous()

    @kb.add('right')
    def _(event):
        event.app.layout.focus_next()

    app = Application(
        layout=Layout(layout_final, focused_element=btn_a),
        key_bindings=kb,
        style=Yos_Estilo,
        mouse_support=True,
        full_screen=False
    )

    app.run()
    clear()
    Yos_Cls_Txt()

    return Mem_Res[0]
# ******************************************************************************************************************************************* FIN - Yos_MsgPgt_Tui

# ******************************************************************************************************************************************* Apl_Fin_Txt
def Apl_Fin_Txt(**Fnc_Dic):
    # Finaliza la Aplicacion
    ''' Valores
        Pgt = {Si/No} Omi : Si
        SisMsg = {Si/No} Omi : Si

        Yos.Apl_Fin_Txt(Pgt= "No", SisMsg= "No")
    '''
    # Recupero los parametros
    if "SisMsg" not in Fnc_Dic:
        Fnc_Dic["SisMsg"] = "Si"

    if "Pgt" not in Fnc_Dic:
        Fnc_Dic["Pgt"] = "Si"

    import Yos

    if Fnc_Dic["Pgt"] == "Si":
        from prompt_toolkit import prompt, HTML
#        Mem_Pgt = Yos_MsgPgt_Txt(Fnc_Tit= "FINALIZAR", Fnc_Msg= "\n ¿ Desea salir de la aplicación ?", Fnc_Bot= "SÍ/NO")
        Mem_Pgt = Yos_MsgPgt_Tui(Fnc_Tit= "FINALIZAR", Fnc_Msg= "\n ¿ Desea salir de la aplicación ?", Fnc_Bot= "SÍ/NO")
        if Mem_Pgt.strip() == 'NO':
            return

    if Fnc_Dic["SisMsg"] == "Si":
        print(f'{Yos.Yos_TimeStamp()} -> {YosSes["Usr_Ipd"]} - {YosSes["Usr_Nik"]} : FINALIZA APLICACION')

    import sys
    sys.exit(0)
    return
# ******************************************************************************************************************************************* FIN - Apl_Fin_Txt

def Yos_EntDat_Txt(**Fnc_Dic):
    # Extraemos los valores del diccionario
    Mem_Dat = Fnc_Dic.get("Dat", "")
    Fnc_Vfy = Fnc_Dic.get("Vfy", "")
    Fnc_Rot = Fnc_Dic.get("Rot", "Dato")
    Fnc_Tip = Fnc_Dic.get("Tip", "C")
    Fnc_Lon = Fnc_Dic.get("Lon", 0)

    while True:
        # 1. Pedimos el dato (Si es Pas, ocultamos, si no, normal)
        if "Pas" in Fnc_Vfy:
            from Yos import Yos_Pas
            print(f"{Fnc_Rot}: ", end= "", flush=True)
            Mem_Val = Yos_Pas()
        else:
            Mem_Val = input(f"{Fnc_Rot} [{Mem_Dat}]: ") or Mem_Dat

        # 2. Llamamos al verificador (El cerebro que ya hicimos)
        # Importante: El verificador nos devuelve el dato ya modificado (Myu, Cap, etc.)
        Mem_Val, Mem_Err = Yos_EntDat_Vfy(Mem_Val, Fnc_Vfy, Fnc_Rot, Fnc_Tip, Fnc_Lon)

        if not Mem_Err:
            return Mem_Val # Dato correcto, salimos
        else:
            print(f" >> {Mem_Err}") # Error, el bucle sigue


def Yos_Cls_Txt():

    os.system('cls' if os.name == 'nt' else 'clear')

def FrmWit(Fnc_Txt= "",Fnc_Wit=0):
    from prompt_toolkit import print_formatted_text, HTML
    from pytimedinput import timedInput

    if Fnc_Txt:
        print_formatted_text(HTML(f"\n<ansigreen>{Fnc_Txt}</ansigreen>"))

    # Espera a que pulses Intro o que pase el Tiempo asignado
    Fnc_Txt = "<orange>\n  Pulse INTRO para continuar </orange>"
    # f"{Fore.YELLOW}\n Pulse INTRO para continuar"
    if Fnc_Wit==0:
        print_formatted_text(HTML(Fnc_Txt), end= "")
        input("")
    else:
        Fnc_Txt = Fnc_Txt + f" <orange>({Fnc_Wit} Seg)</orange> " #f" ({Fnc_Wit} Seg) "
        print_formatted_text(HTML(Fnc_Txt), end= "")
        timedInput(prompt= "", timeout=Fnc_Wit)


def FrmLin(Fnc_Txt, Fnc_Pos= ""): # Formatea un linea
#    print(f"{Fore.RED}{FrmLin('ACCESO RESTRINGIDO - POR FAVOR IDENTIFÍQUESE', '')}{Style.RESET_ALL}") # A la Izquierda
#    print(f"{Fore.RED}{FrmLin('ACCESO RESTRINGIDO - POR FAVOR IDENTIFÍQUESE', 'C')}{Style.RESET_ALL}") # Al Centro
#    print(f"{Fore.RED}{FrmLin('ACCESO RESTRINGIDO - POR FAVOR IDENTIFÍQUESE', 'D')}{Style.RESET_ALL}") # a la Derecha
#    print(f"{Fore.RED}{FrmLin('ACCESO RESTRINGIDO - POR FAVOR IDENTIFÍQUESE', 88)}{Style.RESET_ALL}") # a 88 espacion de la Derecha
#    input(f"\n{Fore.YELLOW}{FrmLin('Pulse INTRO para continuar', 8)}{Style.RESET_ALL}")
    match Fnc_Pos:
        case "C": # centro
                Fnc_Pos = YosAplCfg["Apl"]["Etn_Lon"]
                Fnc_Pos = int((Fnc_Pos -len(Fnc_Txt)) /2)
                return (" " * int(Fnc_Pos)) + Fnc_Txt
#                Mem_Txt=f"{Fnc_Txt:^{Mem_Cen}}"
#                return Mem_Txt
        case "D": # Derecha
#                Mem_Cen=YosAplCfg["Apl"]["Etn_Lon"]
#                Mem_Txt=f"{Fnc_Txt:>{int(Mem_Cen)}}"
#                return Mem_Txt
                Fnc_Pos = YosAplCfg["Apl"]["Etn_Lon"]
                Fnc_Pos = Fnc_Pos -len(Fnc_Txt)
                return (" " * int(Fnc_Pos)) + Fnc_Txt


        case n if str(Fnc_Pos).isdigit(): # Es numerico
            return (" " * int(Fnc_Pos)) + Fnc_Txt

        case _:
            return Fnc_Txt

def Yos_Txt_Cab_CreRot():
    # Creamos en Rotulo y la Cabacera de la aplicacion

#    from Yos import MstFncLin
#    input(MstFncLin(FncNiv= "All"))

    Mem_Cab = ""
    # Genero el Rotulo del nombre de la aplicacion
    import pyfiglet
    import shutil
    # 1. Generamos el banner y aplicamos el strip (tu parámetro -s)
    Rotulo = pyfiglet.figlet_format(YosAplCfg["Apl"]["Apl"], font=YosAplCfg["Apl"]["Etn_Let"], width=1000).rstrip()

    lineas = Rotulo.splitlines()

    ancho_dibujo = max(len(linea) for linea in lineas)

    # Añadimos un margen interno de seguridad (ej: 6 espacios)
    ancho_total = ancho_dibujo + 0

    borde_S = "╔" + "═" * (ancho_total + 2) + "╗"
    borde_I = "╚" + "═" * (ancho_total + 2) + "╝"
    contenido = [f"║ {linea.ljust(ancho_total)} ║" for linea in lineas]
    dibujo_ascii = [borde_S] + contenido + [borde_I]

    YosAplCfg["Apl"]["Rot"] = dibujo_ascii # Rotulo del nombre de la Aplicacion

#    return lineas
    #print_formatted_text(HTML(f"<ansiyellow>{FrmLin('CONFIGURACIÓN DEL ENTORNO DE LA APLICACION', 'C')}</ansiyellow>"))
    # 3. Centramos cada línea individualmente

#    print("\n".join(lineas))
    Mem_MaxLon = (max(len(l) for l in lineas) if lineas else 0)
#    print(f"Mem_MaxLon {Mem_MaxLon}")
    # ajustos a todos al mismo ancho
    lineas_v = dibujo_ascii
    lineas = []
    for l in lineas_v:
        espacios_izq = int(Mem_MaxLon - len(l))
#        print(f"Mem_MaxLon={Mem_MaxLon} espacios_izq={espacios_izq}")
        nueva_linea = ( l + " " * espacios_izq)
        lineas.append(nueva_linea)

    Mem_MaxFrm = YosAplCfg["Apl"]["Etn_Lon"]
#    print(f"Mem_MaxFrm={Mem_MaxFrm} Mem_MaxLon={Mem_MaxLon}")
#    print(len(lineas))
    lineas_v = lineas
    lineas = []
    for l in lineas_v:
#        print(f"Mem_MaxFrm = {Mem_MaxFrm} Len =  {(len(l) // 2)}")
        espacios_izq = int((Mem_MaxFrm - len(l)) // 2)
        nueva_linea = (" " * espacios_izq) + l
        lineas.append(nueva_linea)
    Rotulo_Final = "\n".join(lineas)
#    print("\n".join(lineas))
#    print()
#    print(lineas[1])

    # pongo en Usuario
    if YosAplCfg["Apl"]["Usr_Acc"] == "S":
        if 'YosSes' in globals() or 'YosSes' in dir(__builtins__):
            Mem_Txt = f"Usuario : {YosSes['Usr_Nik']}"
        else:
            Mem_Txt = "Usuario : Invitado" # O dejarlo vacío

        Mem_Ini = 5
        Mem_Fin = len(Mem_Txt)
        lineas[0] = lineas[0][:Mem_Ini] + Mem_Txt + lineas[0][Mem_Ini + Mem_Fin:]

#·    from prompt_toolkit import print_formatted_text, HTML
#    for linea in lineas:
#        print_formatted_text(HTML(f"<orange>{linea}</orange>"))
    YosAplCfg["Apl"]["Cab"] = lineas # Cabecera  Rotula + Datos de la apliccion

def FrmCab(Fnc_Dat=None):
    # Imprimimos la cabecero o el rotulo

    # Fnc_Dat = Rot -> Rotulo
    #         = Cab -> Cabecera

    match Fnc_Dat:
        case "Rot":
            lineas_cab_lista = YosAplCfg["Apl"]["Rot"]
        case "Cab":
            lineas_cab_lista = YosAplCfg["Apl"]["Cab"]
        case _:
            input("Entorno de la Aplicacion inexisente")

    Mem_Cab_Final = '\n'.join(lineas_cab_lista)         # Convertimos la lista en un solo string para el control visual


    from prompt_toolkit import print_formatted_text, HTML
    for linea in lineas_cab_lista:
        print_formatted_text(HTML(f"<orange>{linea}</orange>"))

####################################################################################################


