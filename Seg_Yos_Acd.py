#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
   Yos_Acd.py
   INFORMACION DE LA APLICACION Y MOTOR DE Mem_MsgS

   Copyright (c) 2026 Miguel Tortosa
   Licenciado bajo la Licencia MIT.
"""

def Acd():
    from Yos import FrmMsg

    Mem_Tab = "&nbsp;&nbsp;&nbsp;&nbsp;"

    Mem_Dat = f'<b>ENTORNO</b><br>{Mem_Tab}S.O. : {YosAplCfg["Apl"]["Sis_Etn"]} - {YosAplCfg["Apl"]["Sis_Etn_Des"]}<br><br>'
    Mem_Dat = Mem_Dat + f'<b>APLICACION</b><br>{Mem_Tab}{YosAplCfg["Apl"]["Apl"]}<br>{Mem_Tab}{Mem_Tab}{YosAplCfg["Apl"]["Nom"]}<br>{Mem_Tab}{Mem_Tab}Ver. {YosAplCfg["Apl"]["Vsn"]}<br>{Mem_Tab}{Mem_Tab}{YosAplCfg["Apl"]["Cpy"]}<br>{Mem_Tab}{Mem_Tab}email : {YosAplCfg["Apl"]["CpyEml"]}<br><br>'
    Mem_Dat = Mem_Dat + f'<b>LIBRERIAS</b><br>{Mem_Tab}{YosAplCfg["Yos"]["Apl"]} - {YosAplCfg["Yos"]["Nom"]} - Ver. {YosAplCfg["Yos"]["Vsn"]}<br>{Mem_Tab}{Mem_Tab}{YosAplCfg["Yos"]["Cpy"]}'

    FrmMsg(Fnc_Tit="ACERCA DE ...", Fnc_Msg=Mem_Dat, Fnc_Tip="Inf")

def AcdRes():
    from Yos import FrmMsg

    Mem_Dat = f'{YosAplCfg["Apl"]["Apl"]}<br>{YosAplCfg["Apl"]["Nom"]}<br><br>Licenciado bajo la Licencia MIT.<br><br>Consulte el archivo LICENCIA en la raíz del proyecto para más información'

    FrmMsg(Fnc_Tit="AVISO DE DESCARGO DE RESPONSABILIDAD", Fnc_Msg=Mem_Dat, Fnc_Tip="Inf", Ancho="500px")

