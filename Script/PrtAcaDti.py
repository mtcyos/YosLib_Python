# -*- coding: utf-8 -*-

from dbfread import DBF
from datetime import datetime
import os

def PrtAcaDti_DtiReg():
    Mem_Svr = "DtiReg"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Tip"] = "MsSQL"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Dir"] = "172.16.10.1"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Usr"] = "pfc_consulta"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Pas"] = "pfc.upnfm2025"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Bdt"] = "registro"
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_Obs"] = ""
    YosAplCfg["Apl"][f"Bdt_{Mem_Svr}_ObsSis"] = ""

def PrtAcaDti_Env():
    #  Directorio donde esta la Tabla PrtAca.dbf
    ruta_base = r"n:\DfpGesItg\GesDfp\Mae"
    Mem_Dbf_Prt = os.path.join(ruta_base, 'PrtAca.dbf')

    if not os.path.exists(Mem_Dbf_Prt):
        print("ERROR: No se encontró PrtAca.dbf en la ruta actual.")
        return

    PrtAcaDti_DtiReg()

    # 1. Parámetros de Control mtcyos
    Yos.Yos_Cls_Txt()
    Yos.FrmCab("Rot")
    print("    PARA EL ENVÍO DE LA PROPUESTA ACADÉMICA.")
    print("    ES NECESARIO QUE LA PROPUESTA A ENVIAR ESTE FINALIZADA = 9")
    print("")
    print("    **************************************")
    print("    * ENVIO DE PROPUESTA ACADEMICA A DTI *")
    print("    *                                    *")
    print("    * ENVIO POR CENTRO                   *")
    print("    **************************************")
    #print("\n")
    print("     ORIGEN  : "+Mem_Dbf_Prt)
    print("     DESTINO : "+YosAplCfg["Apl"]["Bdt_DtiReg_Dir"])
    #print("\n")
    print("    **************************************")
    print("\n")
    Mem_Per = input("    Periodo (aaaaIII) : ").upper().strip()
    Mem_Emp = input("    Centro (nn)    : ").strip()
    if not Mem_Emp or str(Mem_Emp).strip() == "":
        print("    ERROR: Centro es OBlIGATORIO.")
        input("    Pulse INTRO.")
        Yos.Yos_Cls_Txt()
        return

    Mem_PreAlu = input("    PreAlumnos (S/ )    : ").upper().strip()

    print(f"\n    CONFIRMAR :\n    Periodo : {Mem_Per}\n    Centro : {Mem_Emp}\n    PreAlumnos : {Mem_PreAlu}")
    if input("\n    ¿CORRECTO? (Si/): ").strip().capitalize() != "Si":
        input("    PROPUESTA NO ENVIADA")
        Yos.Yos_Cls_Txt()
        return

    try:
        Mem_Cnx_Dti = Yos.Idd_BdtSvr_Cnx("DtiReg")
        Mem_Cur_Dti = Mem_Cnx_Dti.cursor()

        # 3. Lectura de Datos DBF
        tabla = DBF(Mem_Dbf_Prt, load=True, encoding='cp1252', char_decode_errors='replace')

        # Filtro mtcyos: Periodo, Empresa, Estado 9 y sin Errores
        if Mem_PreAlu=="S":
            registros = [r for r in tabla if (r.get('CPER') or '').strip() == Mem_Per
                and (r.get('CCODEMP') or '').strip() == Mem_Emp
                and (r.get('CEST') or '').strip() == "9"
                and (r.get('CORIPREALU') or '').strip() == "S"
                and not (r.get('CERR') or '').strip()]
        else:
            registros = [r for r in tabla if (r.get('CPER') or '').strip() == Mem_Per
                and (r.get('CCODEMP') or '').strip() == Mem_Emp
                and (r.get('CEST') or '').strip() == "9"
                and (r.get('CORIPREALU') or '').strip() != "S"
                and not (r.get('CERR') or '').strip()]

        if not registros:
            print("AVISO: No hay registros pendientes para estos criterios.")
            return

        print(f"SISTEMA: Insertando {len(registros)} registros...")

        # SQL Parametrizado para evitar inyecciones y errores de formato
        Mem_Sql = """
            INSERT INTO carga_datos_propuesta (
                centro, sede, subsede, anio, periodo, asignatura, seccion, identidad_prof, cupomax,
                lhi, lhf, laula, mhi, mhf, maula, mihi, mihf, miaula,
                jhi, jhf, jaula, vhi, vhf, vaula, shi, shf, saula, dhi, dhf, daula,
                fecha, usuario, virtual, error
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """
        Mem_Cont = 0
        for r in registros:
            # Unificación cTimModReg
            f_str = f"{r.get('DFECMODREG')} {r.get('CHORMODREG')}"
            try:
                fecha_dt = datetime.strptime(f_str, '%Y-%m-%d %H:%M:%S')
            except:
                fecha_dt = datetime.now()

            params = (
                r.get('CCODEMP', '')[:2],      # centro
                r.get('CCODSEDUPN', '')[:2],      # sede
                r.get('CCODSUBSED', '')[:2],   # subsede
                r.get('CYEA', ''),             # anio
                r.get('CPERINI', '')[-1:],     # periodo
                r.get('CCODASG', '')[:10],     # asignatura
                r.get('CSEC', '')[:4],         # seccion
                r.get('CCODEPL', '')[:13],     # identidad_prof
                int(r.get('NALUMAX', 0)),      # cupomax
                r.get('CLUNHORINI', ''),       # lhi
                r.get('CLUNHORFIN', ''),       # lhf
                r.get('CLUNAUL', ''),          # laula
                r.get('CMRTHORINI', ''),       # mhi
                r.get('CMRTHORFIN', ''),       # mhf
                r.get('CMRTAUL', ''),          # maula
                r.get('CMIEHORINI', ''),       # mihi
                r.get('CMIEHORFIN', ''),       # mihf
                r.get('CMIEAUL', ''),          # miaula
                r.get('CJUEHORINI', ''),       # jhi
                r.get('CJUEHORFIN', ''),       # jhf
                r.get('CJUEAUL', ''),          # jaula
                r.get('CVIEHORINI', ''),       # vhi
                r.get('CVIEHORFIN', ''),       # vhf
                r.get('CVIEAUL', ''),          # vaula
                r.get('CSABHORINI', ''),       # shi
                r.get('CSABHORFIN', ''),       # shf
                r.get('CSABAUL', ''),          # saula
                r.get('CDOMHORINI', ''),       # dhi
                r.get('CDOMHORFIN', ''),       # dhf
                r.get('CDOMAUL', ''),          # daula
                fecha_dt,                      # fecha
                r.get('CNOM', ''),             # usuario
#                1 if r.get('CTRACSSVIR') == '1' else 0, # virtual
                r.get('CTRACSSVIR'),           # virtual
                (r.get('CERR') or '')[:160]    # error
            )
            Mem_Cur_Dti.execute(Mem_Sql, params)
            Mem_Cont += 1
        Mem_Cur_Dti.commit()

        print(f"SISTEMA: Carga finalizada exitosamente.")

    except Exception as e:
        print(f"ERROR CRITICO: {e}")
    finally:
        if 'Mem_Cnx_Dti' in locals(): Yos.Cie(Mem_Cnx_Dti)

        Mem_Txt=f"DFP - PROPUESTA ACADEMICA A DTI\n\n"
        Mem_Txt=Mem_Txt +f"PERIODO : {Mem_Per}\n"
        Mem_Txt=Mem_Txt +f"CENTRO : {Mem_Emp}\n"
        Mem_Txt=Mem_Txt +f"PreAlumnos : {Mem_PreAlu}\n"
        Mem_Txt=Mem_Txt +f"REGISTROS : {Mem_Cont}\n"
        Mem_Txt=Mem_Txt +f"\nENVIO FINALIZADO CORRECTAMENTE"

        if not Mem_Cont==0:
            pass
            Yos.EmlEnv(["mtcyos@upnfm.edu.hn"], "DFP - ENVIO DE PROPUESTA ACADEMICA", Mem_Txt)

            input("PULSE INTRO PARA CONTINUAR")
            Yos.Yos_Cls_Txt()

def PrtAcaDti_Ver():

    PrtAcaDti_DtiReg()

    Yos.Yos_Cls_Txt()
    Yos.FrmCab("Rot")

    # 1. Conexión al Motor de Datos DTI
    Mem_Cnx_Dti = Yos.Idd_BdtSvr_Cnx("DtiReg")
    Mem_Cur_Dti = Mem_Cnx_Dti.cursor()

    # 2. SQL Agrupado por Procesado y Error [cite: 2026-02-05]
    # reg[0]: procesado | reg[1]: errorMsg | reg[2]: total
    #Mem_Sql = "SELECT procesado, errorMsg, COUNT(*) as total FROM carga_datos_propuesta GROUP BY procesado, errorMsg"
    Mem_Sql = "SELECT usuario, procesado, ISNULL(errorMsg, '') as errorMsg, COUNT(*) as total FROM carga_datos_propuesta GROUP BY usuario, procesado, ISNULL(errorMsg, '')"

    Mem_Cur_Dti.execute(Mem_Sql)
    lista_errores = Mem_Cur_Dti.fetchall()

    print("    " + "*" * 73)
    print("     RESULTADO PROPUESTA ACADEMICA - DTI")
    print("    " + "*" * 73)
    print("               REPORTE DE ESTADOS")
    print("    " + "-" * 73)
    print("                  USUARIO             | CANTIDAD | ESTADO / ERROR")
    print("    " + "*" * 73)

    nTot = 0  # Acumulador para el Gran Total

    for reg in lista_errores:
        Usr = reg[0]
        nPro = reg[1] # Según tu SQL: usuario=0, procesado=1, errorMsg=2, total=3

        # Limpieza de Honor: manejamos NULL y espacios en blanco
        cErr = str(reg[2]).strip() if reg[2] else ""

        # --- CORRECCIÓN CRÍTICA ---
        # Forzamos nCan a entero para evitar el error de operandos
        try:
            nCan = int(reg[3])
        except (ValueError, TypeError):
            nCan = 0

        nTot += nCan # Ahora la suma de int + int es segura

        # --- LÓGICA DE TEXTO SOLICITADA ---
        if nPro == 1 and (cErr == "" or cErr == "0"):
            cMsg = "CORRECTOS"
        elif nPro == 0 and (cErr == "" or cErr == "NULL"):
            cMsg = "PENDIENTES DE PROCESAR"
        else:
            cMsg = cErr if cErr else "ERROR INDETERMINADO"

        # 3. Impresión con formato de 8 dígitos para la cantidad
        print(f"     {Usr:<32} | {nCan:8d} | {cMsg}")

    print("    " + "-" * 73)
    print(f"     {" " * 32} | {nTot:8d} | TOTAL REGISTROS EVALUADOS")
    print("    " + "*" * 73)
    print("\n")

    Yos.Cie(Mem_Cnx_Dti)
    input("PULSE INTRO PARA CONTINUAR")
    Yos.Yos_Cls_Txt()

def PrtAcaDti_Eli():

    PrtAcaDti_DtiReg()

    Yos.Yos_Cls_Txt()
    Yos.FrmCab("Rot")

    print("   ***************************************")
    print("   * VACIAR LA PROPUESTA ACADEMICA - DTI *")
    print("   ***************************************")
    print()
    print("   ESTE PROCESO SOLO SE DEBE HACER AL COMIENZO DE UNA IMPORTACIÓN")
    print("   Y CUANDO LAS PROPUESTAS IMPORTADAS ESTÁN FINALIZADAS.")

    if input("\n   ¿CORRECTO? (Si/): ").strip().capitalize() != "Si":
         return

    # 2. Conexión Directa a SQL Server
    Mem_Cnx_Dti = Yos.Idd_BdtSvr_Cnx("DtiReg")
    Mem_Cur_Dti = Mem_Cnx_Dti.cursor()

    Yos.Yos_Cls_Txt()
    Yos.FrmCab("Rot")

    print("   ***************************************")
    print("   * VACIAR LA PROPUESTA ACADEMICA - DTI *")
    print("   ***************************************")

    Mem_Sql = "delete from carga_datos_propuesta"

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

