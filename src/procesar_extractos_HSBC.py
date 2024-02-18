import os
from utils.helper_functions import extract_text_from_pdf, eliminar_comas, asignar_tipo_movimiento
import re
import pandas as pd
import numpy as np


# configuracion
pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 500)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', 800)
pd.options.display.float_format = '{:,.2f}'.format


def convertir_extractos_hsbc(path):

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
            # print(line)
            if 'SALDO ANTERIOR' in line:
                # print(line)
                pattern = r"- SALDO ANTERIOR (\d{1,3}(?:,\d{3})*\.\d{2})"
                match = re.search(pattern, line)
                if match:
                    groups = match.groups()
                    saldo = groups[0]

                    if line.endswith('-'):
                        saldo = '-' + saldo

                    data.append({
                        'Fecha': None,
                        'Descripcion': 'SALDO ANTERIOR',
                        'Detalle': None,
                        'Codigo': None,
                        'Importe': None,
                        'Saldo': saldo
                    })

            else:
                pattern = r"(?:(\d{2}-\w{3}) - )?(.+?) (\d{5}) ((?:\d{1,3}(?:,\d{3})*|)\.\d{2}) (\d{1,3}(?:,\d{3})*\.\d{2})"

                match = re.search(pattern, line)

                if match:
                    groups = match.groups()

                    fecha = groups[0] if groups[0] else None
                    descripcion = groups[1]
                    codigo = groups[2]

                    if groups[3].startswith('.'):
                        monto = '0' + groups[3]
                    else:
                        monto = groups[3]

                    saldo = groups[4]

                    # procesar la línea siguiente
                    next_line_index = i + 1
                    while next_line_index < len(all_lines):
                        next_line = all_lines[next_line_index]  # busco la linea siguiente
                        next_match = re.search(pattern, next_line)  # si la linea siguiente coincide con el patron

                        if next_match:
                            break  # rompo el bucle

                        # si la línea siguiente no coincide con el patrón, añadirla a next_lines
                        next_lines.append(next_line)
                        next_line_index += 1

                    next_lines_str = '\n'.join(next_lines)
                    data.append({
                        'Fecha': fecha,
                        'Descripcion': descripcion,
                        'Detalle': next_lines_str,
                        'Codigo': codigo,
                        'Importe': monto,
                        'Saldo': saldo
                    })

                    next_lines = []

        df = pd.DataFrame(data)
        df = eliminar_comas(df, ['Importe', 'Saldo'])
        df[['Importe', 'Saldo']] = df[['Importe', 'Saldo']].astype(float)
        df['Diferencia'] = df['Saldo'].diff()
        df['Tipo Movimiento'] = df['Diferencia'].apply(asignar_tipo_movimiento)
        print(df.head(30))

        complete_file_path_sin_extension = complete_file_path.replace('.pdf', '')
        df.to_excel(f'{complete_file_path_sin_extension}.xlsx')


# path = r'../data/test/hsbc'
# convertir_extractos_hsbc(path)
