#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Yos_Mnu.py
    Genero el Menu de la Aplicacion

    Copyright (c) 2026 Miguel Tortosa
"""
from Yos import Yos_Cls_Txt, FrmWit, FrmCab, FrmLin
import os

from textual.app import App, ComposeResult
from textual.containers import Grid, Vertical, Horizontal
from textual.widgets import Button, Label, Input
from textual.screen import Screen

class YosMenuScreen(Screen):
    def __init__(self, fnc_mnu, yos_cfg, columnas, cab_text, titulo, subtitulo, copy_app, ancho_total, salir_num):
        super().__init__()
        self.fnc_mnu = fnc_mnu
        self.yos_cfg = yos_cfg
        self.columnas = columnas
        self.cab_text = cab_text
        self.titulo = titulo
        self.subtitulo = subtitulo
        self.copy_app = copy_app
        self.ancho_total = ancho_total
        self.salir_num = salir_num

    def compose(self) -> ComposeResult:
        # Header banner
        if self.cab_text:
            yield Label(self.cab_text, id="ascii-banner")
        if self.titulo:
            yield Label(self.titulo, id="titulo-app")
        if self.subtitulo:
            yield Label(self.subtitulo, id="subtitulo-app")

        # Grid containing headers
        yield Grid(id="headers-grid")

        # Horizontal Separator
        yield Label("═" * self.ancho_total, id="sep-header")

        # Grid containing columns
        yield Grid(id="menu-grid")

        # Horizontal Separator
        yield Label("═" * self.ancho_total, id="sep-footer")

        # Copyright
        if self.copy_app:
            yield Label(self.copy_app, id="copy-app")

        # Input Prompt
        with Horizontal(id="input-container"):
            yield Label("  Seleccione Opción : ", id="input-label")
            yield Input(id="opcion-input", placeholder="")

    def on_mount(self) -> None:
        headers_grid = self.query_one("#headers-grid", Grid)
        grid = self.query_one("#menu-grid", Grid)
        num_cols = len(self.columnas)
        headers_grid.styles.grid_size_columns = num_cols
        grid.styles.grid_size_columns = num_cols

        for i, col in enumerate(self.columnas):
            # Col has [header_item, sub_item1, sub_item2, ...]
            col_title = col[0]["txt"]#.upper()

            # Determine if it's the last column to not draw a vertical border line
            is_last = (i == num_cols - 1)

            # Header Column Title
            header_col = Vertical(classes="header-col-last" if is_last else "header-col")
            headers_grid.mount(header_col)
            header_col.mount(Label(col_title, classes="titulo-col"))

            # Column Body (options)
            col_container = Vertical(classes="columna-last" if is_last else "columna")
            grid.mount(col_container)

            for item in col[1:]:
                id_ver = "   S" if item["fnc"] == "«AppSld»" else item["id"]
                btn_text = f" {id_ver}  - {item['txt']} "

                if item["fnc"]:
                    col_container.mount(Button(btn_text, id=f"btn_{item['id'].strip()}"))
                else:
                    col_container.mount(Label(" "+btn_text, classes="label-opcion"))

        # Auto-focus the option input field
        self.query_one("#opcion-input", Input).focus()

class YosApp(App):
    CSS_PATH = []
    CSS = """
    Screen {
        background: black;
        color: white;
    }
    #ascii-banner {
        color: orange;
        text-align: left;
        width: 100%;
        margin-top: 0;
    }
    #titulo-app {
        color: yellow;
        text-style: bold;
        text-align: center;
        width: 100%;
    }
    #subtitulo-app {
        color: cyan;
        text-align: center;
        width: 100%;
    }
    #sep-header, #sep-footer {
        color: blue;
        text-align: center;
        width: 100%;
    }
    #headers-grid {
        height: auto;
        width: 100%;
        margin-top: 1;
        margin-bottom: 0;
    }
    .header-col {
        height: auto;
        border-right: solid black;
        padding: 0 2;
    }
    .header-col-last {
        height: auto;
        padding: 0 2;
    }
    #menu-grid {
        height: auto;
        width: 100%;
        margin-top: 0;
        margin-bottom: 0;
    }
    .columna {
        height: 100%;
        border-right: solid blue;
        padding: 0 2;
    }
    .columna-last {
        height: 100%;
        padding: 0 2;
    }
    .titulo-col {
        color: magenta;
        text-align: center;
        width: 100%;
    }
    .separador {
        color: white;
        width: 100%;
        text-align: left;
    }
    .label-opcion {
        border: none;
        background: transparent;
        color: silver;
        content-align: left middle !important;
        text-align: left !important;
        width: 100%;
        height: 1;
        margin: 0;
        padding: 0;
        min-width: 0;
        min-height: 0;
    }
    #menu-grid Button {
        border: none;
        background: transparent;
        color: silver;
        padding: 0 !important;
        content-align: left middle !important;
        text-align: left !important;
        width: 100%;
        height: 1;
        margin: 0;
        min-width: 0;
        min-height: 0;
        margin-left: 0;
    }
    #menu-grid Button:focus {
        background: blue;
        color: white;
        text-style: bold;
    }
    #copy-app {
        color: yellow;
        text-align: center;
        width: 100%;
    }
    #input-container {
        height: auto;
        margin-top: 1;
        padding-left: 2;
        align: left middle;
    }
    #input-label {
        color: orange;
        text-style: bold;
    }
    #opcion-input {
        width: 15;
        height: 1;
        border: none;
        background: transparent;
        color: orange;
        padding: 0;
    }
    #opcion-input:focus {
        border: none;
        background: transparent;
    }
    """

    BINDINGS = [
        ("q", "custom_exit", "Salir"),
        ("escape", "custom_exit", "Salir"),
    ]

    def __init__(self, fnc_mnu, yos_cfg, columnas, cab_text, titulo, subtitulo, copy_app, ancho_total, salir_num):
        super().__init__()
        self.fnc_mnu = fnc_mnu
        self.yos_cfg = yos_cfg
        self.columnas = columnas
        self.cab_text = cab_text
        self.titulo = titulo
        self.subtitulo = subtitulo
        self.copy_app = copy_app
        self.ancho_total = ancho_total
        self.salir_num = salir_num

    def on_mount(self) -> None:
        self.push_screen(YosMenuScreen(
            self.fnc_mnu, self.yos_cfg, self.columnas, self.cab_text,
            self.titulo, self.subtitulo, self.copy_app, self.ancho_total, self.salir_num
        ))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id and button_id.startswith("btn_"):
            btn_id_val = button_id[4:]
            self.process_selection(btn_id_val)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        val = event.value.strip()
        if val:
            self.process_selection(val)

    def process_selection(self, val: str) -> None:
        val_upper = val.upper()
        if val_upper == "S":
            target_id = self.salir_num
        else:
            target_id = val.zfill(4)

        for col in self.columnas:
            for item in col[1:]:
                if item["id"] == target_id or (item["fnc"] == "«AppSld»" and val_upper == "S"):
                    cFunc = item.get("fnc", "")
                    if cFunc:
                        self.exit(cFunc)
                        return

    def action_custom_exit(self) -> None:
        self.exit("«AppSld»")

def Yos_Mnu_Tui(Fnc_Mnu):
    # Menu Grafico con soporte de Raton en Textual
    if not Fnc_Mnu:
        Fnc_Mnu = YosAplCfg["Apl"]["Mnu"]

    ancho_total = YosAplCfg["Apl"].get("Etn_Lon", 80) - 1
    titulo_app = f"{YosAplCfg["Apl"].get('Nom', '')}"
    subtitulo_app = YosAplCfg["Apl"].get('TitSub', '')
    copy_app = YosAplCfg["Apl"].get('Cpy', '')

    Salir_Num = ""

    # 1. Preparar Columnas basadas en 'Sub'
    columnas = []
    claves_columnas = sorted(Fnc_Mnu.keys())

    for cNumCol in claves_columnas:
        columna_data = Fnc_Mnu[cNumCol]
        items_columna = []

        # Título de columna
        items_columna.append({
            "id": cNumCol,
            "txt": columna_data.get("Txt", "MENU"),
            "fnc": ""
        })

        # Sub-ítems
        dic_items = columna_data.get("Sub", {})
        for cNumOrd in sorted(dic_items.keys()):
            val = dic_items[cNumOrd]
            ent = val.get("Ent", "")
            if ent == "" or ent in YosAplCfg["Apl"]["Sis_Etn"]:
                if val["Cod"].strip() == "Sep":
                    items_columna.append({
                        "id": " " * len(cNumOrd),
                        "txt": val["Txt"] if val.get("Txt") and val["Txt"].strip() else "--------------------",
                        "fnc": val.get("Fnc", "")
                    })
                elif val["Txt"].strip() != "":
                    items_columna.append({
                        "id": cNumOrd,
                        "txt": val["Txt"],
                        "fnc": val.get("Fnc", "")
                    })

        if len(items_columna) > 1:
            columnas.append(items_columna)

    # Buscar el Salir_Num de la misma manera que en prompt_toolkit
    for col in columnas:
        for item in col[1:]:
            if item['fnc'] == "«AppSld»":
                Salir_Num = item['id']

    # --- TRATAMIENTO DE CABECERA (Evitando AttributeError) ---
    lineas_cab = YosAplCfg["Apl"].get("Cab", "")
    if isinstance(lineas_cab, str):
        lineas_cab_lista = lineas_cab.split('\n')
    else:
        lineas_cab_lista = list(lineas_cab)

    # Limpiar y preparar visual de cabecera
    lineas_cab_lista.insert(0, " " * ancho_total)
    Mem_Cab_Final = '\n'.join(lineas_cab_lista)

    app = YosApp(Fnc_Mnu, YosAplCfg, columnas, Mem_Cab_Final, titulo_app, subtitulo_app, copy_app, ancho_total, Salir_Num)
    return app.run()


