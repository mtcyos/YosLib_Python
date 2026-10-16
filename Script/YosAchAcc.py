#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   YosAchAcc
   Muestra Directorio para Descargar los Archivos

   Copyright (c) 2026 Miguel Tortosa

   Licenciado bajo la Licencia MIT.
   Consulte el archivo LICENCIA en la raíz del proyecto para más información.
"""
from nicegui import ui

################################################################################################################################################################################
# PÁGINA YosAchAcc
@ui.page('/YosAchAcc')
async def Pgn_YosAchAcc(Dir: str = 'NoDir', Tit: str = 'Archivo'):

    if YosAplCfg["Apl"]["Usr_Acc"] == "S":
        if not app.storage.user.get('autenticado', False):
            ui.run_javascript('window.location.href = "/login"')
            return

    if YosAplCfg["Apl"]["Etn"] == "Loc" and YosAplCfg["Apl"]["Usr_Acc"] != "S" and not YosSes['Usr_Nik']:
        Yos.Apl_UsrAcc_UsrEliDat("SinUsr")

    # CABECERA con TITULO DE LA PAGINA
    Yos.Yos_Cab_Gui(Tit="YosAchAcc")

    # llamada desdes Menu /YosAchAcc?Dir=c:\&Tit=Ana
    if Dir == "NoDir":
        ui.notify("No se ha definido ningún Directorio.", type='warning', position='center')
        ui.run_javascript('setTimeout(() => { window.history.back(); }, 2000);')
        return
#    print(f'Dir={Dir}')
#    print(f'YosAplCfg["Apl"]["DirAch"]={YosAplCfg["Apl"]["DirAch"]}')
    if YosAplCfg["Apl"]["DirAch"] and Dir.startswith('/Apl_DirAch'): # Verifico si creo un directorio para Aplicaciones, Si ha puesto /Apl_DirAch en el Dir lo sustituyo por YosAplCfg["Apl"]["DirAch"]
            Dir = Dir.replace('/Apl_DirAch', YosAplCfg["Apl"]["DirAch"], 1)
            import os
            Dir = os.path.normpath(Dir)

    Mem_Dir = Dir
    Mem_DirNom = Tit

    print(f'Mem_Dir={Mem_Dir} Mem_DirNom={Mem_DirNom}')

    from nicegui import context
    client = context.client

    # MENU
    Yos.Yos_Mnu_Vrt()

    # --- ESTILOS VISUALES GENERALES ---
    ui.query('body').style('background-color: #ffffff; color: #000000; font-family: sans-serif;')

    container_multiteka = ui.column().classes('w-full items-center py-4')

#    Yos.Yos_MstDir_Frm(Mem_Dir, container_multiteka, Mem_DirNom)
    Yos.Yos_MstDir_Frm(
        ruta_base=Mem_Dir,
        container=container_multiteka,
        Fnc_Tit=Mem_DirNom
    )

    # PIE DE PÁGINA Y AVISO
    Yos.Yos_PieAvs_Gui()
################################################################################################################################################################################

