# -*- coding: utf-8 -*
def PrtAcaXlsDile_Gen():

    import os
    from dbfread import DBF
    from datetime import datetime
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment, Border, Side

    #  Directorio donde esta la Tabla AsnCagAca.dbf
    ruta_base = r"n:\DfpGesItg\GesDfp\Dat\Emp_04"
    Mem_Dbf_Prt = os.path.join(ruta_base, 'AsnCagAca.dbf')

    Mem_Sal = "\\\\tsclient\\c\\_GesItg\\"
    Yos.Yos_Cls_Txt()
    Yos.FrmCab("Rot")
    print("    *******************************************")
    print("    * DFP - GENERAR EXCEL DE  PrtAca - DILE   *")
    print("    *******************************************")
    print(f"     ORIGEN  : {ruta_base}")
    print(f"     DESTINO : {Mem_Sal}")
    print("    *******************************************")


    Mem_Per = input("    Periodo (aaaaIII)         : ").upper().strip()
    Mem_FecEnv = input("    Fecha Envío (Enter para HOY): ").strip()
    if not Mem_FecEnv:
        Mem_FecEnv = datetime.now().strftime('%d/%m/%Y')

    try:
        # 1. Carga de Datos con Encoding de Windows para Tildes
        print(f"    SISTEMA: Procesando...")
        #tabla = DBF(Mem_Dbf_Prt, load=True, encoding='cp1252', char_decode_errors='replace')
        tabla = DBF(Mem_Dbf_Prt, load=True, encoding='cp850', char_decode_errors='replace')

        registros = [r for r in tabla if
                     (r.get('CPER') or '').strip() == Mem_Per and
                     (r.get('CCODEPL') or '').strip() != "" and
                     (r.get('CSEC') or '').strip() != "T" and
                     not (r.get('CERR') or '').strip()]

        if not registros:
            Yos.FrmWit("    ATENCION : No hay registros para exportar.")
            Yos.Yos_Cls_Txt()
            return

        # --- CAMBIO DE HONOR: ORDENADO POR IDENTIDAD ---
        registros.sort(key=lambda x: (x.get('CCODEPL') or '').strip())

        # 2. Configuración de Excel
        wb = Workbook()
        ws = wb.active
        ws.title = "Planilla"

        bold = Font(bold=True, name='Segoe UI', size=10)
        border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
        center = Alignment(horizontal='center', vertical='center', wrap_text=True)

        # 3. Cabeceras UPNFM
        ws.merge_cells('A1:Z1'); ws['A1'] = "UNIVERSIDAD PEDAGOGICA NACIONAL FRANCISCO MORAZAN"; ws['A1'].font = Font(bold=True, size=12)
        ws.merge_cells('A2:Z2'); ws['A2'] = "DIRECCIÓN DE FORMACIÓN PERMANENTE - DILE"; ws['A2'].font = Font(bold=True)
        ws.merge_cells('A3:Z3'); ws['A3'] = "PLANILLA DE DOCENTES POR HORA"
        ws.merge_cells('A4:Z4'); ws['A4'] = f"PERIODO: {Mem_Per}"

        for r_tit in range(1, 5): ws.cell(row=r_tit, column=1).alignment = center

        # 4. Encabezados (26 Columnas)
        headers = [
            "No.", "IDENTIDAD", "NOMBRE DEL DOCENTE", "GENERO", "TIPO DE CONTRATACIÓN",
            "CENTRO", "CÓDIGO", "NOMBRE DE LA CLASE", "MODALIDAD", "N° DE ALUMNOS",
            "SECCIÓN", "IMPARTIDA EN LA SEDE", "CARRERA A LA QUE PERTENECE", "FACULTAD",
            "BLOQUE", "VIERNES", "SABADO", "DOMINGO", "N° HORAS", "CATEGORIA",
            "TOTAL CLASE", "TOTAL DOCENTE", "FECHA ENVÍO", "FIRMA", "CUENTA", "OBS"
        ]

        for col, text in enumerate(headers, 1):
            c = ws.cell(row=6, column=col, value=text)
            c.font = bold; c.alignment = center; c.border = border
            ws.column_dimensions[c.column_letter].width = 14

        # 5. Cuerpo de Datos con Acumulador y Formato Contable
        row_idx = 8
        Mem_Cnt = 0
        Mem_EplAnt = None
        Mem_SumaDocente = 0
        formato_num = '#,##0.00'

        for r in (registros + [None]):
            if r is None:
                if Mem_EplAnt:
                    c_tot = ws.cell(row=row_idx-1, column=22, value=Mem_SumaDocente)
                    c_tot.font = bold; c_tot.number_format = formato_num
                break

            actual_epl = (r.get('CCODEPL') or '').strip()

            if Mem_EplAnt is not None and actual_epl != Mem_EplAnt:
                c_tot = ws.cell(row=row_idx-1, column=22, value=Mem_SumaDocente)
                c_tot.font = bold; c_tot.number_format = formato_num
                Mem_SumaDocente = 0

            if actual_epl != Mem_EplAnt:
                Mem_Cnt += 1; t_cnt = Mem_Cnt
            else:
                t_cnt = ""

            # --- LÓGICA DE CÁLCULO DE HORAS (V, S, D) ---
            val_horas = 0
            for ini_k, fin_k in [('CVIEHORINI','CVIEHORFIN'), ('CSABHORINI','CSABHORFIN'), ('CDOMHORINI','CDOMHORFIN')]:
                h1, h2 = (r.get(ini_k) or '').strip(), (r.get(fin_k) or '').strip()
                if h1 and h2 and ':' in h1 and ':' in h2:
                    try:
                        diff = datetime.strptime(h2, '%H:%M') - datetime.strptime(h1, '%H:%M')
                        val_horas += diff.seconds / 3600
                    except: pass

            val_clase = r.get('NSLAACA', 0)
            Mem_SumaDocente += val_clase

            val_sexo = {"M": "Masculino", "F": "Femenino"}.get((r.get('CSEX') or '').strip().upper(), "")

            nombre_sucio = (r.get('CNOMEPL') or '')
            nombre_limpio = nombre_sucio.replace('+', 'É').replace('═', 'Í').replace('-', 'Í').replace('Ë', 'Ó').replace('Ð', 'Ñ').replace('±', 'Ñ').strip().upper()

            Asg_sucio = (r.get('CDES') or '')
            Asg_limpio = Asg_sucio.replace('+', 'É').replace('═', 'Í').replace('-', 'Í').replace('Ë', 'Ó').replace('Ð', 'Ñ').replace('±', 'Ñ').strip().upper()

            fila_datos = [
                t_cnt, actual_epl, #r.get('CNOMEPL'),
                nombre_limpio,
                val_sexo,
                "", "DFP-04", r.get('CCODASG'), Asg_limpio,
                "PRESENCIAL", r.get('NALUMAT'), r.get('CSEC'), r.get('CNOMSEDABV'),
                "DILE - DIPLOMADO DE INGLES COMO LENGUA EXTRANJERA", "FACE", r.get('CBLQ'),
                f"{r.get('CVIEHORINI','')}-{r.get('CVIEHORFIN','')}" if r.get('CVIEHORINI') else "",
                f"{r.get('CSABHORINI','')}-{r.get('CSABHORFIN','')}" if r.get('CSABHORINI') else "",
                f"{r.get('CDOMHORINI','')}-{r.get('CDOMHORFIN','')}" if r.get('CDOMHORINI') else "",
                val_horas, r.get('CGRAACA'), val_clase, "", Mem_FecEnv, "", "", ""
            ]

            for col_idx, valor in enumerate(fila_datos, 1):
                c = ws.cell(row=row_idx, column=col_idx, value=valor)
                c.border = border
                if col_idx == 2: c.number_format = '@'
                if col_idx in [21, 22]:
                    c.number_format = formato_num

            Mem_EplAnt = actual_epl
            row_idx += 1

        # 6. Pie de Firmas
        row_idx += 2
        ws.merge_cells(start_row=row_idx, start_column=2, end_row=row_idx, end_column=3)
        ws.cell(row=row_idx, column=2, value="___________________________________").alignment = center
        ws.merge_cells(start_row=row_idx+1, start_column=2, end_row=row_idx+1, end_column=3)
        ws.cell(row=row_idx+1, column=2, value="Director Formación Permanente").font = bold
        ws.cell(row=row_idx+1, column=2, value="Director Formación Permanente").alignment = center

        ws.merge_cells(start_row=row_idx, start_column=8, end_row=row_idx, end_column=9)
        ws.cell(row=row_idx, column=8, value="___________________________________").alignment = center
        ws.merge_cells(start_row=row_idx+1, start_column=8, end_row=row_idx+1, end_column=9)
        ws.cell(row=row_idx+1, column=8, value="Tesorería General").font = bold
        ws.cell(row=row_idx+1, column=8, value="Tesorería General").alignment = center

        row_idx += 5
        ws.merge_cells(start_row=row_idx, start_column=2, end_row=row_idx, end_column=3)
        ws.cell(row=row_idx, column=2, value="___________________________________").alignment = center
        ws.merge_cells(start_row=row_idx+1, start_column=2, end_row=row_idx+1, end_column=3)
        ws.cell(row=row_idx+1, column=2, value="Jefe Gestión Talento Humano").font = bold
        ws.cell(row=row_idx+1, column=2, value="Jefe Gestión Talento Humano").alignment = center

        # Guardado final mtcyos
        nombre_final = f"{Mem_Sal}DFP_{Mem_Per}_DILE_PrtAca.xlsx"
        wb.save(nombre_final)
        print(f"\n    SISTEMA: ¡Éxito! Archivo generado : {nombre_final}")

    except Exception as e:
        print(f"    ERROR: {e}")
    Yos.FrmWit()
    Yos.Yos_Cls_Txt()

if __name__ == "__main__":
    PrtAca_DILE_a_Excel()
