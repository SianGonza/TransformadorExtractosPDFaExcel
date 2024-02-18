import os
from utils.helper_functions import extract_text_from_pdf_meridian
from utils.helper_functions import extract_text_from_pdf, convert_to_float, asignar_tipo_movimiento, eliminar_comas
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


def convertir_extractos_macro(path):

    files_list = []

    for file in os.listdir(path):
        if file.endswith('.pdf'):
            files_list.append(file)

    for file in files_list:

        data = []

        print(f'Transformando archivo: {file}')
        complete_file_path = os.path.join(path, file)
        texts = extract_text_from_pdf_meridian(complete_file_path, 'Lascano6548')

        all_lines = []

        for text in texts:
            lines = text.split('\n')
            all_lines.extend(lines)

        next_line = None
        next_lines = []

        for i, line in enumerate(all_lines):
            # print(line)
            if 'SALDO ULTIMO EXTRACTO' in line:
                pattern = r"SALDO ULTIMO EXTRACTO AL (\d{2}\/\d{2}\/\d{4}) ([\d\.]+,\d{2})"
                match = re.search(pattern, line)
                if match:
                    groups = match.groups()
                    saldo = groups[1]

                    if line.endswith('-'):
                        saldo = '-' + saldo

                    data.append({
                        'Fecha': None,
                        'Descripcion': f'SALDO ANTERIOR AL {groups[0]}',
                        'Importe': None,
                        'Saldo': saldo
                    })

            else:
                pattern = r"(\d{2}\/\d{2}\/\d{2}) (.+?) ([\d\.]+,\d{2}) ([\d\.]+,\d{2})"
                match = re.search(pattern, line)

                if match:
                    groups = match.groups()

                    fecha = groups[0]
                    descripcion = groups[1]
                    importe = groups[2]
                    saldo = groups[3]

                    data.append({
                        'Fecha': fecha,
                        'Descripcion': descripcion,
                        'Importe': importe,
                        'Saldo': saldo

                    })

        df = pd.DataFrame(data)

        # df = eliminar_comas(df, ['Importe', 'Saldo'])
        df['Importe'] = df['Importe'].str.replace('.', '').str.replace(',', '.')
        df['Importe'] = df['Importe'].astype(float)

        df['Saldo'] = df['Saldo'].str.replace('.', '').str.replace(',', '.')
        df['Saldo'] = df['Saldo'].astype(float)

        print(df.head(20))

        df[['Importe', 'Saldo']] = df[['Importe', 'Saldo']].astype(float)
        df['Diferencia'] = df['Saldo'].diff()
        df['Tipo Movimiento'] = df['Diferencia'].apply(asignar_tipo_movimiento)

        complete_file_path_sin_extension = complete_file_path.replace('.pdf', '')
        df.to_excel(f'{complete_file_path_sin_extension}.xlsx')


# path = r'\\192.168.0.3\wns\Asesoramiento Contable\WNS\ALMATEX SA\Contabilidad\2023\INFORMACION DEL CLIENTE\EXTRACTOS BANCARIOS\MACRO\macro cc\a convertir'
# convertir_extractos_macro(path)
