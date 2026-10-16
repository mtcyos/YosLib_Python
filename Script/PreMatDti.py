# -*- coding: utf-8 -*-

from dbfread import DBF
from datetime import datetime
import os

def PreMatDti_DtiReg():
    Mem_Svr = "DtiReg"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Tip"] = "MsSQL"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Dir"] = "172.16.10.1"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Usr"] = "pfc_consulta"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Pas"] = "pfc.upnfm2025"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Bdt"] = "registro"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Obs"] = ""
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_ObsSis"] = ""

def PreMatDti_Env():
    PreMatDti_DtiReg()

    Mem_Cont=0
    # 1. Parámetros de Control mtcyos
    Yos.Yos_Cls_Txt()
    Yos.FrmCab("Rot")
    print("    PARA EL ENVÍO DE LA PRE MATRICULA.")
    print("    ES NECESARIO QUE LA EMISIÓN DE LA PROPUESTA ACADEMIA")
    print("    ESTE REALIZADA (AluPrtAca.dbf)")
    print()

    print("    **************************************")
    print("    *    ENVIO DE PRE MATRICULA A DTI    *")
    print("    *                                    *")
    print("    * ENVIO POR CENTRO                   *")
    print("    **************************************")
    #print("\n")
    #print("     ORIGEN : "+Mem_Dbf_AluPrt)
    print("     DESTINO : "+YosAplCfg["Apl"]["Bdt_DtiReg_Dir"])
    #print("\n")
    print("    **************************************")
#    print("\n")
    Mem_Per = input("    Periodo (aaaaIII) : ").upper().strip()
    Mem_Cen = input("    Centro (nn)    : ").strip()
    if not Mem_Cen or str(Mem_Cen).strip() == "":
        print("    ERROR: Centro es OBlIGATORIO.")
        input("    Pulse INTRO.")
        Yos.Yos_Cls_Txt()
        return

    print(f"\n    CONFIRMAR :\n    Periodo : {Mem_Per}\n    Centro : {Mem_Cen}")
    if input("\n    ¿CORRECTO? (Si/): ").strip().capitalize() != "Si":
        print("    PROPUESTA NO ENVIADA")
        input("    Pulse INTRO.")
        Yos.Yos_Cls_Txt()
        return

    Mem_PerAnio = Mem_Per[:4]
#    Mem_PerSolo = Mem_Per[4:]
#    input(Mem_PerSolo)

    match Mem_Per[4:]:
        case "I":
            Mem_PerSolo = "1"
        case "II":
            Mem_PerSolo = "2"
        case "III":
            Mem_PerSolo = "3"

    ruta_base = fr"n:\DfpGesItg\GesDfp\Dat\Emp_{Mem_Cen}"
    Mem_Dbf_AluPrt = os.path.join(ruta_base, 'AluPrtAca.dbf')

    if not os.path.exists(Mem_Dbf_AluPrt):
        print(f"    ERROR: No se encontró {Mem_Dbf_AluPrt} en la ruta actual.")
        input("    Pulse INTRO.")
        return

    Yos.Yos_Cls_Txt()
    Yos.FrmCab("Rot")
    print("    **************************************")
    print("    *    ENVIO DE PRE MATRICULA A DTI    *")
    print("    **************************************")
    print(f"     PERIODO : {Mem_PerAnio} {Mem_PerSolo}")
    #print("\n")
    print("     ORIGEN  : "+Mem_Dbf_AluPrt)
    print("     DESTINO : "+YosAplCfg["Apl"]["Bdt_DtiReg_Dir"])
    #print("\n")
    print("    **************************************")

    try:
        Mem_Cnx_Dti = Yos.Idd_BdtSvr_Cnx("DtiReg")
        Mem_Cur_Dti = Mem_Cnx_Dti.cursor()

        # 3. Lectura de Datos DBF
        tabla = DBF(Mem_Dbf_AluPrt, load=True, encoding='cp1252', char_decode_errors='replace')

        # Filtro mtcyos: Periodo, Empresa, Estado 9 y sin Errores
        registros = [r for r in tabla if (r.get('CPER') or '').strip() == Mem_Per
#            and (r.get('CCODEMP') or '').strip() == Mem_Cen
#            and (r.get('CEST') or '').strip() == "9"
#            and (r.get('CORIPREALU') or '').strip() != "S"
#            and not (r.get('CERR') or '').strip()
            ]

        if not registros:
            print("    AVISO: No hay registros pendientes para estos criterios.")
            input("    Pulse INTRO.")
            return

        print(f"    SISTEMA: Insertando {len(registros)} registros...")

        # SQL Parametrizado para evitar inyecciones y errores de formato
        Mem_Sql = """
            INSERT INTO carga_datos_matricula (
                carnet, carrera, centro, sede, subsede, anio, periodo, asignatura, seccion,
                fecha, usuario
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        for r in registros:
            # Unificación cTimModReg
            f_str = f"{r.get('DFECMODREG')} {r.get('CHORMODREG')}"
            try:
                fecha_dt = datetime.strptime(f_str, '%Y-%m-%d %H:%M:%S')
            except:
                fecha_dt = datetime.now()

            params = (
                r.get('CCODALU', '')[:13],      # carnet
                r.get('CCODCAR', '')[:4],       # carrera
                Mem_Cen[:2],                    # centro
                r.get('CCODSEDUPN', '')[:2],    # sede
                r.get('CCODSUBSED', '')[:2],    # subsede
                Mem_PerAnio,          # anio
                Mem_PerSolo,                    # periodo
                r.get('CCODASG', '')[:10],      # asignatura
                r.get('CSEC', '')[:2],          # seccion
                fecha_dt,                       # fecha
                "IptIni",                       # usuario
            )
            Mem_Cur_Dti.execute(Mem_Sql, params)
            Mem_Cont += 1
        Mem_Cur_Dti.commit()
        print(f"    SISTEMA: Carga finalizada exitosamente.")

    except Exception as e:
        print(f"    ERROR CRITICO: {e}")
    finally:
        if 'Mem_Cnx_Dti' in locals(): Yos.Cie(Mem_Cnx_Dti)

        from Yos.YosLib import EmlEnv
        Mem_Txt=f"DFP - PRE MATRICULA A DTI\n\n"
        Mem_Txt=Mem_Txt +f"PERIODO : {Mem_Per}\n"
        Mem_Txt=Mem_Txt +f"CENTRO : {Mem_Cen}\n"
        Mem_Txt=Mem_Txt +f"REGISTROS : {Mem_Cont}\n"
        Mem_Txt=Mem_Txt +f"\nENVIO FINALIZADO CORRECTAMENTE"

        if not Mem_Cont==0:
            pass
#            Yos.EmlEnv(["ricardo.lopez@upnfm.edu.hn", "mtcyos@upnfm.edu.hn", "belinaguilar@upnfm.edu.hn"], "DFP - ENVIO DE PRE MATRICULA", Mem_Txt)

    input("    Pulse INTRO.")
    Yos.Yos_Cls_Txt()


def PreMatDti_Ver():
    PreMatDti_DtiReg()

    Yos.Yos_Cls_Txt()
    Yos.FrmCab("Rot")
    # 1. Conexión al Motor de Datos DTI
    Mem_Cnx_Dti = Yos.Idd_BdtSvr_Cnx("DtiReg")
    Mem_Cur_Dti = Mem_Cnx_Dti.cursor()

    # 2. SQL Agrupado por Procesado y Error [cite: 2026-02-05]
    # reg[0]: procesado | reg[1]: errorMsg | reg[2]: total
    # Mem_Sql = "SELECT procesado, errorMsg, COUNT(*) as total FROM carga_datos_matricula GROUP BY procesado, errorMsg"
    Mem_Sql = '''SELECT centro, carrera, sede, subsede, procesado, errorMsg, COUNT(*) as total
                FROM carga_datos_matricula
                GROUP BY centro, carrera,sede, subsede, procesado, errorMsg
                ORDER BY centro, carrera,sede, subsede;
              '''
    Mem_Cur_Dti.execute(Mem_Sql)
    lista_errores = Mem_Cur_Dti.fetchall()

    print("    ***************************************")
    print("    *    RESULTADO PRE MATRICULA A DTI    *")
    print("    ***************************************")
    print("               REPORTE DE ESTADOS")
    print("    -----------------------------------------------------------------")
    print("    CANTIDAD | CENTRO | CARRERA | SEDE/SUB | ESTADO / ERROR")
    print("    -----------------------------------------------------------------")

    nTot = 0  # Acumulador para el Gran Total

    for reg in lista_errores:
        # Ahora el orden es: centro, sede, subsede, procesado, errorMsg, total
        cCentro  = reg[0]
        cCarrera = reg[1]
        cSede    = reg[2]
        cSubSede = reg[3]
        nPro     = reg[4]

        # Limpieza de Honor
        cErr = str(reg[5]).strip() if reg[5] else "" # Antes era reg[1]

        nCan = reg[6] # Antes era reg[2], ahora es el campo 6 (índice 5)
        nTot += nCan

        # --- LÓGICA DE TEXTO SOLICITADA ---
        if nPro == 1 and (cErr == "" or cErr == "0"):
            cMsg = "CORRECTOS"
        elif nPro == 0 and cErr == "":
            cMsg = "PENDIENTES DE PROCESAR"
        else:
            cMsg = cErr if cErr else "ERROR INDETERMINADO"

        # 3. Impresión incluyendo la ubicación para que el reporte sea útil
        print(f"    {nCan:8d} |   {cCentro}   |  {cCarrera}   |  {cSede}-{cSubSede}   | {cMsg}")

    print("    -----------------------------------------------------------------")
    print(f"    {nTot:8d} | TOTAL REGISTROS EVALUADOS")
    print("    ***************************************")
    print("\n")

    Yos.Cie(Mem_Cnx_Dti)
    input("    PULSE INTRO PARA CONTINUAR")
    Yos.Yos_Cls_Txt()

def PreMatDti_Eli():
    PreMatDti_DtiReg()

    Yos.Yos_Cls_Txt()
    Yos.FrmCab("Rot")

    print("   ***************************************")
    print("   *     VACIAR PRE MATRICULA A DTI      *")
    print("   ***************************************")
    print()
    print("   ESTE PROCESO SOLO SE DEBE HACER AL COMIENZO DE UNA IMPORTACIÓN")
    print("   Y CUANDO PRE MATRICULA IMPORTADAS ESTÁN FINALIZADAS.")

    if input("\n   ¿CORRECTO? (Si/): ").strip().capitalize() != "Si":
         return

    # 2. Conexión Directa a SQL Server
    Mem_Cnx_Dti = Yos.Idd_BdtSvr_Cnx("DtiReg")
    Mem_Cur_Dti = Mem_Cnx_Dti.cursor()

    Yos.Yos_Cls_Txt()
    Yos.FrmCab("Rot")

    print("   ***************************************")
    print("   *     VACIAR PRE MATRICULA A DTI      *")
    print("   ***************************************")

    Mem_Sql = "delete from carga_datos_matricula"

    try:
        # 2. Ejecutamos y confirmamos [cite: 2026-01-20]
        Mem_Cur_Dti.execute(Mem_Sql)
        Mem_Cnx_Dti.commit()
        print("1. SISTEMA: Tabla vaciada correctamente (TRUNCATE).")

    except Exception as e:
        print(f"Error al vaciar tabla: {e}")

    Yos.Cie(Mem_Cnx_Dti)

    input("PULSE INTRO PARA CONTINUAR")
    Yos.Yos_Cls_Txt()

