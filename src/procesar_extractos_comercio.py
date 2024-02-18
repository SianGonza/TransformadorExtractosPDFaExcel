import os
from utils.helper_functions import extract_text_from_pdf, convert_to_float, asignar_tipo_movimiento, eliminar_puntos
import re
import pandas as pd
import numpy as np


# configuracion
pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 500)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', 800)
pd.options.display.float_format = '{:,.2f}'.format


def convert_to_float_galicia(importe):
    if isinstance(importe, str) and importe.endswith('-'):
        importe = '-' + importe[:-1]

    return float(importe.replace('.', '').replace(',', '.'))


def convertir_extractos_comercio(path):

    files_list = []

    for file in os.listdir(path):
        if file.endswith('.pdf'):
            files_list.append(file)

    for file in files_list:

        data = []

        print(f'Transformando archivo: {file}')
        complete_file_path = os.path.join(path, file)
        texts = extract_text_from_pdf(complete_file_path)

        all_lines = []

        for text in texts:
            lines = text.split('\n')
            all_lines.extend(lines)

        next_line = None
        next_lines = []

        for i, line in enumerate(all_lines):
            print(line)
            if 'SALDO ANTERIOR' in line:
                pattern = r"SALDO ANTERIOR\.+ (\d{1,3}(?:\.\d{3})*,\d{2})"
                match = re.search(pattern, line)
                if match:
                    groups = match.groups()
                    saldo = groups[0]

                    if line.endswith('-'):
                        saldo = '-' + saldo

                    data.append({
                        'Fecha': None,
                        'Codigo': None,
                        'Descripcion': 'SALDO ANTERIOR',
                        'Cuenta': None,
                        'Detalle': None,
                        'Importe': None,
                        'Saldo': saldo
                    })

            else:
                pattern = r"(\d{2}/\d{2}/\d{4})\s+(\d{5})-(.+?)\s+(\d{1,3}(?:\.\d{3})*,\d{2})\s+(\d{1,3}(?:\.\d{3})*,\d{2})\s+(\d{3}/\d{5})-(.+)"
                match = re.search(pattern, line)

                if match:
                    groups = match.groups()

                    fecha = groups[0]
                    codigo = groups[1]
                    descripcion = groups[2]
                    monto = groups[3]
                    saldo = groups[4]
                    cuenta = groups[5]
                    detalle = groups[6]

                    data.append({
                        'Fecha': fecha,
                        'Codigo': codigo,
                        'Descripcion': descripcion,
                        'Cuenta': cuenta,
                        'Detalle': detalle,
                        'Importe': monto,
                        'Saldo': saldo

                    })

        df = pd.DataFrame(data)
        print(df.head(20))
        df = eliminar_puntos(df, ['Importe', 'Saldo'])
        df['Importe'] = df['Importe'].str.replace(',', '.')
        df['Saldo'] = df['Saldo'].str.replace(',', '.')
        df[['Importe', 'Saldo']] = df[['Importe', 'Saldo']].astype(float)
        df['Diferencia'] = df['Saldo'].diff()
        df['Tipo Movimiento'] = df['Diferencia'].apply(asignar_tipo_movimiento)

        complete_file_path_sin_extension = complete_file_path.replace('.pdf', '')
        df.to_excel(f'{complete_file_path_sin_extension}.xlsx')


# path = r'\\192.168.0.3\wns\Asesoramiento Contable\WNS\566 SRL\Contabilidad\2023\INFORMACION DEL CLIENTE\EXTRACTOS BANCARIOS\Comercio'
# convertir_extractos_comercio(path)
