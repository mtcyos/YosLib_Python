#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Yos_Mnu.py
Sistema de Menú Unificado para Yos Framework
TUI (Textual) / GUI-Vrt (NiceGUI Vertical) / GUI-Hrt (NiceGUI Horizontal)

Copyright (c) 2026 Miguel Tortosa
"""

import os
import sys
import gc
import builtins
import asyncio
import subprocess
import platform
import inspect

#import Yos

# ===========================================================================
# DISPATCHER PRINCIPAL
# ===========================================================================
def Yos_Mnu(**Fnc_Dic):
    # cTit : Gestion de Menus
    # cDes : Gestion de Menusm unifica las 3 versiones Tui, Gui Vertical y Horizontal
    #        Usa YosAplCfg["Apl"]["Ori_Etn"] para saber Tui/Gui
    # cPmt : Tip    -> Tipo "Vrt" (Vertical), "Hrt" (Horizontal) solo en Gui
    #        Mnu    -> Menu a Mostrar , si esta vacio YosAplCfg["Apl"]["Mnu"]
    #        Nom    -> Nombre del menu, "__local__" el menu esta dentro del .py

    nombre_funcion = inspect.currentframe().f_code.co_name
#    input(f"Ejecutando: {nombre_funcion}()")

    # Validar: si hay Mnu debe haber MnuNom
    if Fnc_Dic.get("Mnu") and not Fnc_Dic.get("MnuNom"):
        caller = inspect.stack()[1]
        Mem_Txt = "la sintaxis de Yos.Yos_Mnu(Mnu, MnuNom) es incorrecta.\nTodo menú necesita su Nombre\n\n"
        Mem_Txt = Mem_Txt + 'PÓNGASE EN CONTACTO CON EL ADMINISTRADOR\n'
        Mem_Txt = Mem_Txt + f'Y facilítele este dato :  {inspect.currentframe().f_back.f_code.co_name}({caller.lineno})'
        Yos.Yos_MsgSis(Txt=Mem_Txt, Tip= "Err")
        return "«AppSld»"
#        Fnc_Dic = {}  # Ignora el Mnu inválido, carga menú raíz

    if not hasattr(builtins, "Yos_Mnu_Dat"):    # Creo builtins.Yos_Mnu_Dat
        builtins.Yos_Mnu_Dat = {}

    if "MnuPil" not in builtins.Yos_Mnu_Dat:    # Creo builtins.Yos_Mnu_Dat["MnuPil"] = []
        builtins.Yos_Mnu_Dat["MnuPil"] = []
    builtins.Yos_Mnu_Dat["_MnuSal"] = False           # Flag deteccion salida recursiva

    # Guardar menú actual en la pila ANTES de sobrescribirlo
    if Fnc_Dic.get("Mnu") and "Mnu" in builtins.Yos_Mnu_Dat and builtins.Yos_Mnu_Dat["Mnu"]:
        MnuNom_old = builtins.Yos_Mnu_Dat.get("MnuNom", "")
        if MnuNom_old != "__local__":
            builtins.Yos_Mnu_Dat["MnuPil"].append((MnuNom_old, builtins.Yos_Mnu_Dat["Mnu"]))

    # Recupero los Parametros
    builtins.Yos_Mnu_Dat["Tip"] = Fnc_Dic.get("Tip", "")
    builtins.Yos_Mnu_Dat["MnuNom"] = Fnc_Dic.get("MnuNom", "")
    builtins.Yos_Mnu_Dat["Mnu"] = Fnc_Dic.get("Mnu", "")

    if not builtins.Yos_Mnu_Dat["Tip"]:
        builtins.Yos_Mnu_Dat["Tip"] = "Vrt"

    if not builtins.Yos_Mnu_Dat["Mnu"]:
        builtins.Yos_Mnu_Dat["Mnu"] = YosAplCfg["Apl"]["Mnu"]
        builtins.Yos_Mnu_Dat["MnuNom"] = YosAplCfg["Apl"]["MnuNom"] if YosAplCfg["Apl"].get("MnuNom") else "MnuGen"

    if YosAplCfg["Apl"]["Ori_Etn"] == "Tui":
        while True:
            result = Yos_Mnu_Tui()
            if result == "«AppSld»":
                Mem_Dat = Yos.Yos_MsgPgt_Tui(Fnc_Tit= "FINALIZAR", Fnc_Msg= "¿ DESEA SALIR ?", Fnc_Bot= "SÍ/NO")
                if Mem_Dat == "SÍ":
                    if builtins.Yos_Mnu_Dat["MnuPil"]:
                        MnuNom_old, Mnu_old = builtins.Yos_Mnu_Dat["MnuPil"].pop()
                        builtins.Yos_Mnu_Dat["MnuNom"] = MnuNom_old
                        builtins.Yos_Mnu_Dat["Mnu"] = Mnu_old
                        continue
                    builtins.Yos_Mnu_Dat["_MnuSal"] = True
                    Yos.Yos_MsgSis(Txt=f"FINALIZANDO APLICACION - {YosAplCfg["Apl"]["Apl"]}")
                    return result
                else:
                    result = ""
            if result:
                sel_result = Yos_Mnu_Sel(result)

                if builtins.Yos_Mnu_Dat["MnuNom"] =="__local__":
#                    input(f'sel_result={sel_result} __local__')
                    return sel_result

                if sel_result == "«AppSld»" or builtins.Yos_Mnu_Dat.get("_MnuSal", False):
                    return "«AppSld»"

    elif YosAplCfg["Apl"]["Ori_Etn"] == "Gui":
        if builtins.Yos_Mnu_Dat["Tip"] == "Hrt":
            Yos_Mnu_Hrt()
        else:
            Yos_Mnu_Vrt()

# ===========================================================================
# MENU TUI (Textual)
# ===========================================================================
def Yos_Mnu_Tui():
    # cTit : Menú TUI (Textual)
    # cDes : Menu en modo texto usando Textual
    #

    Fnc_Mnu = builtins.Yos_Mnu_Dat["Mnu"]
    from textual.app import App, ComposeResult
    from textual.containers import Grid, Vertical, Horizontal
    from textual.widgets import Button, Label, Input
    from textual.screen import Screen

    class YosMenuScreen(Screen):
        def __init__(self, columnas, cab_text, titulo, subtitulo, copy_app, ancho_total, salir_num):
            super().__init__()
            self.columnas = columnas
            self.cab_text = cab_text
            self.titulo = titulo
            self.subtitulo = subtitulo
            self.copy_app = copy_app
            self.ancho_total = ancho_total
            self.salir_num = salir_num

        def compose(self) -> ComposeResult:
            if self.cab_text:
                yield Label(self.cab_text, id= "ascii-banner")
            if self.titulo:
                yield Label(self.titulo, id= "titulo-app")
            if self.subtitulo:
                yield Label(self.subtitulo, id= "subtitulo-app")
            yield Grid(id= "headers-grid")
            yield Label("═" * self.ancho_total, id= "sep-header")
            yield Grid(id= "menu-grid")
            yield Label("═" * self.ancho_total, id= "sep-footer")
            if self.copy_app:
                yield Label(self.copy_app, id= "copy-app")
            with Horizontal(id= "input-container"):
                yield Label("  Seleccione Opción : ", id= "input-label")
                yield Input(id= "opcion-input", placeholder= "")

        def on_mount(self) -> None:
            headers_grid = self.query_one("#headers-grid", Grid)
            grid = self.query_one("#menu-grid", Grid)
            num_cols = len(self.columnas)
            headers_grid.styles.grid_size_columns = num_cols
            grid.styles.grid_size_columns = num_cols

            for i, col in enumerate(self.columnas):
                col_title = col[0]["txt"]
                is_last = (i == num_cols - 1)
                header_col = Vertical(classes= "header-col-last" if is_last else "header-col")
                headers_grid.mount(header_col)
                header_col.mount(Label(col_title, classes= "titulo-col"))

                col_container = Vertical(classes= "columna-last" if is_last else "columna")
                grid.mount(col_container)

                for item in col[1:]:
                    id_ver = "   S" if item["fnc"] == "«AppSld»" else item["id"]
                    btn_text = f"{id_ver} - {item['txt']}"
                    if item["fnc"]:
                        col_container.mount(Button(btn_text, id=f"btn_{item['id'].strip()}"))
                    else:
                        col_container.mount(Label(" "+btn_text, classes= "label-opcion"))

            self.query_one("#opcion-input", Input).focus()

    class YosApp(App):
        CSS = """
        Screen { background: black; color: white; }
        #ascii-banner { color: orange; text-align: left; width: 100%; margin-top: 0; }
        #titulo-app { color: yellow; text-style: bold; text-align: center; width: 100%; }
        #subtitulo-app { color: cyan; text-align: center; width: 100%; }
        #sep-header, #sep-footer { color: blue; text-align: center; width: 100%; }
        #headers-grid { height: auto; width: 100%; margin-top: 1; margin-bottom: 0; }
        .header-col { height: auto; border-right: solid black; padding: 0 2; }
        .header-col-last { height: auto; padding: 0 2; }
        #menu-grid { height: auto; width: 100%; margin-top: 0; margin-bottom: 0; }
        .columna { height: 100%; border-right: solid blue; padding: 0 0; }
        .columna-last { height: 100%; padding: 0 0; }
        .titulo-col { color: magenta; text-align: center; width: 100%; }
        .label-opcion { border: none; background: transparent; color: silver; content-align: left middle !important; text-align: left !important; width: 100%; height: 1; margin: 0; padding: 0; min-width: 0; min-height: 0; }
        #menu-grid Button { border: none; background: transparent; color: silver; padding: 0 !important; content-align: left middle !important; text-align: left !important; width: 100%; height: 1; margin: 0; min-width: 0; min-height: 0; margin-left: 0; }
        #menu-grid Button:focus { background: blue; color: white; text-style: bold; }
        #copy-app { color: yellow; text-align: center; width: 100%; }
        #input-container { height: auto; margin-top: 1; padding-left: 2; align: left middle; }
        #input-label { color: orange; text-style: bold; }
        #opcion-input { width: 15; height: 1; border: none; background: transparent; color: orange; padding: 0; }
        #opcion-input:focus { border: none; background: transparent; }
        """
        BINDINGS = [("q", "custom_exit", "Salir"), ("escape", "custom_exit", "Salir")]

        def __init__(self, columnas, cab_text, titulo, subtitulo, copy_app, ancho_total, salir_num):
            super().__init__()
            self.columnas = columnas
            self.cab_text = cab_text
            self.titulo = titulo
            self.subtitulo = subtitulo
            self.copy_app = copy_app
            self.ancho_total = ancho_total
            self.salir_num = salir_num

        def on_mount(self) -> None:
            self.push_screen(YosMenuScreen(
                self.columnas, self.cab_text,
                self.titulo, self.subtitulo, self.copy_app, self.ancho_total, self.salir_num
            ))

        def on_button_pressed(self, event: Button.Pressed) -> None:
            button_id = event.button.id
            if button_id and button_id.startswith("btn_"):
                self.process_selection(button_id[4:])

        def on_input_submitted(self, event: Input.Submitted) -> None:
            val = event.value.strip()
            if val:
                self.process_selection(val)

        def process_selection(self, val: str) -> None:
            val_upper = val.upper()
            target_id = self.salir_num if val_upper == "S" else val.zfill(4)
            for col in self.columnas:
                for item in col[1:]:
                    if item["id"] == target_id or (item["fnc"] == "«AppSld»" and val_upper == "S"):
                        cFunc = item.get("fnc", "")
                        if cFunc:
                            self.exit(cFunc)
                            return

        def action_custom_exit(self) -> None:
            self.exit("«AppSld»")

    # Preparar datos del menu
    ancho_total = YosAplCfg["Apl"].get("Etn_Lon", 80) - 1
    titulo_app = f"{YosAplCfg["Apl"].get('Nom', '')}"
    subtitulo_app = YosAplCfg["Apl"].get('TitSub', '')
    copy_app = YosAplCfg["Apl"].get('Cpy', '')
    Salir_Num = ""

    columnas = []
    claves_columnas = sorted(Fnc_Mnu.keys())

    for cNumCol in claves_columnas:
        columna_data = Fnc_Mnu[cNumCol]
        items_columna = []
        items_columna.append({"id": cNumCol, "txt": columna_data.get("Txt", "MENU"), "fnc": ""})
        dic_items = columna_data.get("Sub", {})
        for cNumOrd in sorted(dic_items.keys()):
            val = dic_items[cNumOrd]
            ent = val.get("Ent", "")
            if ent == "" or ent in YosAplCfg["Apl"]["Sis_Etn"]:
                if val["Cod"].strip() == "Sep":
                    items_columna.append({"id": "-" * len(cNumOrd), "txt": val["Txt"] if val.get("Txt") and val["Txt"].strip() else "--------------------", "fnc": val.get("Fnc", "")})
                elif val["Txt"].strip() != "":
                    items_columna.append({"id": cNumOrd, "txt": val["Txt"], "fnc": val.get("Fnc", "")})
        if len(items_columna) > 1:
            columnas.append(items_columna)

    for col in columnas:
        for item in col[1:]:
            if item['fnc'] == "«AppSld»":
                Salir_Num = item['id']

    lineas_cab = YosAplCfg["Apl"].get("Cab", "")
    lineas_cab_lista = lineas_cab.split('\n') if isinstance(lineas_cab, str) else list(lineas_cab)
    lineas_cab_lista.insert(0, " " * ancho_total)
    Mem_Cab_Final = '\n'.join(lineas_cab_lista)

    app = YosApp(columnas, Mem_Cab_Final, titulo_app, subtitulo_app, copy_app, ancho_total, Salir_Num)
    return app.run()


# ===========================================================================
# MENU GUI VERTICAL (NiceGUI)
# ===========================================================================
def Yos_Mnu_Vrt():
    # cTit : Menú GUI Vertical (NiceGUI)
    # cDes : Menu Vertical en entorno NiceGUI con submenús desplegables
    #
    from nicegui import ui

    async def Yos_Mnu_Vrt_MnuSel(MnuFnc):
        """Procesa la seleccion del menu vertical"""
        if not MnuFnc:
            return
        # «MnuCag» - Recargar menu
        if MnuFnc == "«MnuCag»":
            MnuNom = builtins.Yos_Mnu_Dat.get("MnuNom", "")
            if MnuNom and MnuNom != "__local__":
                builtins.Yos_Mnu_Dat["Mnu"] = Yos.Yos_MnuRec(MnuNom)
                Yos.Yos_DefLib_Full()
                ui.notify("Menu recargado", color='positive')
                Mnu_Nue()
            return

        if MnuFnc.startswith('http') or MnuFnc.startswith('www.'):
            url = MnuFnc if MnuFnc.startswith('http') else 'https://' + MnuFnc
            ui.run_javascript(f"window.open('{url}', '_blank');")
            return

        if MnuFnc.startswith('«WwwPgnNue»/'):
            ruta = MnuFnc.replace('«WwwPgnNue»', '')
            ui.run_javascript(f"window.open('{ruta}', '_blank');")
            return

        if '()' in MnuFnc: # aqui ejecuta funciones
            await Yos_Mnu_Sel_Async(MnuFnc)
            return

        ruta_local = MnuFnc if MnuFnc.startswith('/') else '/' + MnuFnc
        builtins.Mem_Pag = ruta_local.lstrip('/')
        ui.navigate.to(ruta_local)

    with ui.row().classes('w-full p-2 pl-4 -mb-20'):
        with ui.button('≡ MENU').classes(
            'bg-neutral-200 hover:bg-neutral-300 text-neutral-900 border border-neutral-400 rounded-none shadow-sm text-sm font-bold px-3 py-1 relative'
        ) as btn_menu:
            menu_ancla = ui.element('div').classes('absolute left-0 bottom-0')

        def Mnu_Nue():
            menu_ancla.clear()
            with menu_ancla:
                with ui.menu().props('anchor= "bottom left" self= "top left"').classes('bg-neutral-200 border border-neutral-400 rounded-none shadow-md py-2') as menu_obj:
                    for cNumCol in sorted(builtins.Yos_Mnu_Dat["Mnu"].keys()):
                        col_data = builtins.Yos_Mnu_Dat["Mnu"][cNumCol]
                        ui.label(col_data.get("Txt", "MENU").upper()).classes('font-bold text-xs text-neutral-500 bg-neutral-100 py-1 px-2')
                        dic_items = col_data.get("Sub", {})
                        for cNumOrd in sorted(dic_items.keys()):
                            val = dic_items[cNumOrd]
                            ent = val.get("Ent", "")
                            if ent == "" or ent in YosAplCfg["Apl"]["Etn"] :
                                if val["Txt"].strip() != "":
                                    cFunc = val.get("Fnc", "")

                                    async def _on_click(f=cFunc):
                                        await Yos_Mnu_Vrt_MnuSel(f)

                                    item_click = ui.menu_item(val["Txt"]).classes('text-sm text-neutral-900 py-1 px-4').props('dense')
                                    item_click.on('click', _on_click)
                                elif val.get("Cod", "").strip() == "Sep":
                                    ui.separator()
                    btn_menu.on('click', menu_obj.open)

        Mnu_Nue()
    builtins.Yos_Mnu_Dat["_MnuNue"] = Mnu_Nue


# ===========================================================================
# MENU GUI HORIZONTAL (NiceGUI) - Barra de menu
# ===========================================================================
def Yos_Mnu_Hrt():
    # cTit : Menú GUI Horizontal (NiceGUI)
    # cDes : Barra de Menu Horizontal en entorno NiceGUI con submenús desplegables
    #
    from nicegui import ui
    import os

    Fnc_Mnu = builtins.Yos_Mnu_Dat["Mnu"]

    ui.add_head_html('''
        <style>
            main { margin-top: 0 !important; padding-top: 0 !important; }
            .nicegui-content { padding: 0 !important; }
            body { margin: 0 !important; background-color: #f0f2f5; font-family: "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
            .q-btn { font-size: 0.75rem !important; }
            .q-item { font-size: 0.75rem !important; min-height: 24px !important; }
            .hmg-separator { margin: 4px auto !important; width: 90% !important; background-color: #d1d5db !important; min-height: 1px !important; }
        </style>
    ''')

    def generar_items(diccionario):
        for clave in sorted(diccionario.keys()):
            valor = diccionario[clave]
            texto = valor.get("Txt", "")
            comando = valor.get("Fnc", "")
            codigo = valor.get("Cod", "")

            if comando == "«AppSld»":
                if YosAplCfg["Apl"]["Etn"] == "Loc":
                    texto = "SALIR DE LA APLICACION"
                elif YosAplCfg["Apl"]["Etn"] == "Www":
                    if YosAplCfg["Apl"]["Usr_Acc"] == "S":
                        texto = "CERRAR SESION"
                    else:
                        continue

            if codigo == "Sep" or (not texto and not comando):
                ui.separator().classes('hmg-separator')
                continue

            clase_item = 'text-xs min-h-[24px] py-0 px-3'

            if "Sub" in valor and isinstance(valor["Sub"], dict):
                with ui.item().props('clickable').classes(clase_item + ' items-center').style('min-height: 25px; height: 25px;'):
                    ui.label(f"{texto}").classes('flex-grow')
                    ui.icon('chevron_right', size='xs').classes('ml-2')
                    with ui.menu().props('anchor= "top right" self= "top left"').classes('bg-white border border-gray-400'):
                        generar_items(valor["Sub"])
            else:
                async def _on_item_click(f=comando):
                    await _ejecutar(f)
                ui.menu_item(texto, on_click=_on_item_click).classes(clase_item)

    async def _ejecutar(comando):
        await Yos_Mnu_Sel_Async(comando)

    barra_menu = ui.row().classes('w-full bg-slate-200 p-0 gap-0 border-b border-gray-400 items-center')

    def dibujar_botones(datos_menu):
        with barra_menu:
            for clave in sorted(datos_menu.keys()):
                valor = datos_menu[clave]
                texto = valor.get("Txt", "Sin nombre")
                with ui.button(texto).props('flat color=black').classes('text-xs font-bold min-h-[24px] py-0 px-3 rounded-none hover:bg-slate-300'):
                    if "Sub" in valor:
                        with ui.menu().classes('bg-white border border-gray-400'):
                            generar_items(valor["Sub"])

    def _Mnu_Nue_Hrt():
        barra_menu.clear()
        with barra_menu:
            for clave in sorted(builtins.Yos_Mnu_Dat["Mnu"].keys()):
                valor = builtins.Yos_Mnu_Dat["Mnu"][clave]
                texto = valor.get("Txt", "Sin nombre")
                with ui.button(texto).props('flat color=black').classes('text-xs font-bold min-h-[24px] py-0 px-3 rounded-none hover:bg-slate-300'):
                    if "Sub" in valor:
                        with ui.menu().classes('bg-white border border-gray-400'):
                            generar_items(valor["Sub"])
    builtins.Yos_Mnu_Dat["_MnuNue"] = _Mnu_Nue_Hrt

    dibujar_botones(Fnc_Mnu)
    barra_menu.refrescar = dibujar_botones
    return barra_menu


# ===========================================================================
# PROCESADOR UNIFICADO DE SELECCION (Sinclono - para TUI)
# ===========================================================================
def Yos_Mnu_Sel(MnuFnc):
    # cTit : Procesador de selección síncrono
    # cDes : Procesa la seleccion del menu en modo TUI (sincrono)
    # cPmt : MnuFnc -> Código de la función a ejecutar
    #
#    print(f'MnuFnc={MnuFnc} 416')

    if not MnuFnc:
        return False

    import Yos
    MnuFnc = Yos.Yos_SutTxt(Txt=MnuFnc)

    # «MnuCag» - Recargar menu
    if MnuFnc == "«MnuCag»":
        MnuNom = builtins.Yos_Mnu_Dat.get("MnuNom", "")
        if MnuNom and MnuNom != "__local__":
            builtins.Yos_Mnu_Dat["Mnu"] = Yos.Yos_MnuRec(MnuNom)
            Yos.Yos_DefLib_Full()
        return False

    if builtins.Yos_Mnu_Dat["MnuNom"] =="__local__":
#        input(MnuFnc)
#        input(builtins.Yos_Mnu_Dat["MnuNom"])
        return MnuFnc

    # «Cmd» - Ejecutar comando externo (sin esperar)
    if MnuFnc[:5] == "«Cmd»":
        MnuFnc = MnuFnc.replace("«Cmd»", "").strip()
        if not os.path.exists(MnuFnc):
            Yos.Yos_Msg_Tui(Fnc_Tit= "ATENCION", Fnc_Msg=f'APLICACION NO ENCONTRADA: {MnuFnc}', Fnc_Tip= "Err")
            return False

        try:
            if platform.system() == "Windows":
                os.startfile(MnuFnc)
            elif platform.system() == "Darwin":
                subprocess.Popen(['open', MnuFnc])
            else:
                subprocess.Popen(['xdg-open', MnuFnc])

            print()
            Mem_Txt = "LA APLICACIÓN SE EJECUTARÁ EN BREVE."
            Yos.Yos_Msg_Tui(Fnc_Tit= "ATENCION", Fnc_Msg=Mem_Txt, Fnc_Tip= "Inf")

            Mem_Txt = f'EJECUTA {MnuFnc}'
            Yos.Yos_RegApl(Txt=Mem_Txt, Tip= "Inf")

        except Exception as e:
            Yos.Yos_Msg_Tui(Fnc_Tit= "ATENCION", Fnc_Msg=f"Error: {e}", Fnc_Tip= "Err")
        return False

    # «CmdWit» - Ejecutar comando externo (esperando)
    if MnuFnc[:8] == "«CmdWit»":
        MnuFnc = MnuFnc.replace("«CmdWit»", "").strip()
        if not os.path.exists(MnuFnc):
            Mem_Txt = f"Error al ejecutar comando externo: {e}"
            Yos.Yos_Msg_Tui(Fnc_Tit= "ATENCION", Fnc_Msg=Mem_Txt, Fnc_Tip= "Err")
            Yos.Yos_RegApl(Txt=Mem_Txt, Tip= "Err")
            return False

        print()
        Mem_Txt = "LA APLICACIÓN SE EJECUTARÁ EN BREVE. ESPERANDO A QUE TERMINE LA APLICACIÓN EXTERNA."
        Yos.Yos_MsgSis(Txt=Mem_Txt, Fnc_Tip= "Inf")

        Mem_Txt = f'EJECUTA {MnuFnc}'
        Yos.Yos_RegApl(Txt=Mem_Txt, Tip= "Inf")

        try:
            if platform.system() == "Windows":
                proceso = subprocess.Popen(MnuFnc, shell=True)
                proceso.wait()
            elif platform.system() == "Darwin":
                subprocess.run(['open', '-W', MnuFnc])
            else:
                subprocess.run([MnuFnc], shell=True)

        except Exception as e:
                Mem_Txt = f"Error al ejecutar comando externo: {e}"
                Yos.Yos_Msg_Tui(Fnc_Tit= "ATENCION", Fnc_Msg=Mem_Txt, Fnc_Tip= "Err")
                Yos.Yos_RegApl(Txt=Mem_Txt, Tip= "Err")
        return False

    # Ejecucion directa de funcion
    Mem_Fnc_Base = MnuFnc.replace("()", "").strip()
    func = getattr(builtins, Mem_Fnc_Base, None)

    if callable(func):
        YosAplCfg["Apl"]["AtlCur"] = Mem_Fnc_Base
        rv = func()
        if rv == "«AppSld»":
            YosAplCfg["Apl"]["AtlCur"] = YosAplCfg["Apl"]["Apl"]
            return "«AppSld»"
        YosAplCfg["Apl"]["AtlCur"] = YosAplCfg["Apl"]["Apl"]
    else:
        try:
            if "= " in MnuFnc:
                exec(MnuFnc, globals())
            else:
                rv = eval(MnuFnc, globals())
                if rv == "«AppSld»":
                    return "«AppSld»"

            Mem_Txt = f'EJECUTA {MnuFnc}'
            Yos.Yos_RegApl(Txt=Mem_Txt, Tip= "Inf")

        except Exception as e:
            Mem_Txt = f"Error al ejecutar comando externo: {e}"
            Yos.Yos_Msg_Tui(Fnc_Tit= "ATENCION", Fnc_Msg=Mem_Txt, Fnc_Tip= "Err")
            Yos.Yos_RegApl(Txt=Mem_Txt, Tip= "Err")


    return False


# ===========================================================================
# PROCESADOR UNIFICADO DE SELECCION (Asincrono - para GUI)
# ===========================================================================
async def Yos_Mnu_Sel_Async(MnuFnc):
    # cTit : Procesador de selección asíncrono
    # cDes : Procesa la seleccion del menu en modo GUI (asincrono)
    # cPmt : MnuFnc -> Código de la función a ejecutar
    #
    if not MnuFnc:
        return

    import Yos
    from nicegui import ui

    MnuFnc = Yos.Yos_SutTxt(Txt=MnuFnc)
    print(f'MnuFnc={MnuFnc}')
    try:
        # «AppSld» - Salir / Cerrar sesion
        if MnuFnc == "«AppSld»":
            await Yos.Yos_AplFin_Frm(Fnc_Pgt= "Si")
            return

        # «MnuCag» - Recargar menu
        if MnuFnc == "«MnuCag»":
            MnuNom = builtins.Yos_Mnu_Dat.get("MnuNom", "")
            if MnuNom and MnuNom != "__local__":
                builtins.Yos_Mnu_Dat["Mnu"] = Yos.Yos_MnuRec(MnuNom)
                Yos.Yos_DefLib_Full()
                ui.notify("Menu recargado", color='positive')
                _MnuNue = builtins.Yos_Mnu_Dat.get("_MnuNue")
                if _MnuNue:
                    ui.timer(0.001, _MnuNue, once=True)
            return

        # URLs externas
        if MnuFnc.startswith('http') or MnuFnc.startswith('www.'):
            url = MnuFnc if MnuFnc.startswith('http') else 'https://' + MnuFnc
            ui.run_javascript(f"window.open('{url}', '_blank');")
            return

        # Pagina interna en la Misma pantalla
        if MnuFnc.startswith('/'):
            YosAplCfg["Apl"]["Atv"] = MnuFnc
            ui.run_javascript("location.reload();")
            return

        # Pagina interna por funcion  en la Misma pantalla
        if MnuFnc.startswith('Pgn_'):
            YosAplCfg["Apl"]["Atv"] = MnuFnc
            ui.run_javascript("location.reload();")
            return

        # Pagina interna en nueva pestana
        if MnuFnc.startswith('«WwwPgnNue»/'):
            ruta = MnuFnc.replace('«WwwPgnNue»', '')
            ui.run_javascript(f"window.open('{ruta}', '_blank');")
            return

        # «Cmd» - Ejecutar comando externo (sin esperar)
        if MnuFnc[:5] == "«Cmd»":
            MnuFnc = MnuFnc.replace("«Cmd»", "").strip()
            if not os.path.exists(MnuFnc):
                ui.notify(f'Aplicacion no encontrada: {MnuFnc}', type='negative')
                return
            ui.notify(f'La aplicacion {MnuFnc} se ejecutara en breve.', type='info')
            try:
                if platform.system() == "Windows":
                    os.startfile(MnuFnc)
                elif platform.system() == "Darwin":
                    subprocess.Popen(['open', MnuFnc])
                else:
                    subprocess.Popen(['xdg-open', MnuFnc])
            except Exception as e:
                ui.notify(f"Error: {e}", color='negative')
            return

        # «CmdWit» - Ejecutar comando externo (esperando)
        if MnuFnc[:8] == "«CmdWit»":
            MnuFnc = MnuFnc.replace("«CmdWit»", "").strip()
            if not os.path.exists(MnuFnc):
                Yos.Yos_Msg_Frm(Fnc_Tit= "APLICACION", Fnc_Msg=f'Aplicacion no encontrada: {MnuFnc}', Fnc_Tip= "Ant")
                return
            ui.notify(f'La aplicacion {MnuFnc} se ejecutara en breve.', type='info')
            Yos.Yos_Msg_Frm(Fnc_Tit= "APLICACION", Fnc_Msg=f'La aplicacion {MnuFnc} se ejecutara en breve.', Fnc_Tip= "Inf")
            await asyncio.sleep(0.1)
            try:
                if platform.system() == "Windows":
                    proceso = subprocess.Popen(MnuFnc, shell=True)
                    proceso.wait()
                elif platform.system() == "Darwin":
                    subprocess.run(['open', '-W', MnuFnc])
                else:
                    subprocess.run([MnuFnc], shell=True)
                ui.notify('Proceso finalizado.', type='positive')
            except Exception as e:
                ui.notify(f"Error: {e}", color='negative')
            return

        # Ejecucion directa de funcion
        Mem_Yos_DefLib = MnuFnc.replace("()", "").strip()
        print(Mem_Yos_DefLib)
        func = getattr(builtins, Mem_Yos_DefLib, None)

        if callable(func):
            YosAplCfg["Apl"]["Atv"] = Mem_Yos_DefLib
            try:
                resultado = func()
                if asyncio.iscoroutine(resultado):
                    await resultado
            except Exception as e:
                ui.notify(f"Error: {e}", color='negative')
        else:
            try:
                if "= " in MnuFnc:
                    exec(MnuFnc, globals())
                else:
                    resultado = eval(MnuFnc, globals())
            except Exception:
                exec(MnuFnc, globals())

        YosAplCfg["Apl"]["AtlCur"] = YosAplCfg["Apl"]["Apl"]

    except Exception as e:
        ui.notify(f"Error: {e}", color='negative')
