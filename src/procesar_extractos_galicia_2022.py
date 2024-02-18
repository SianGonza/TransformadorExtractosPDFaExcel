import os
from utils.helper_functions import extract_text_from_pdf, convert_to_float, asignar_tipo_movimiento
import re
import pandas as pd
import numpy as np


# configuracion
pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 500)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', 800)
pd.options.display.float_format = '{:,.2f}'.format


def split_descripcion(row):
    if pd.isna(row['Saldo']):
        return pd.Series(row['Descripcion'].rsplit(' ', 2))
    else:
        return pd.Series([row['Descripcion'], np.nan, row['Saldo']])


def convert_to_float_galicia(importe):
    if isinstance(importe, str) and importe.endswith('-'):
        importe = '-' + importe[:-1]

    return float(importe.replace('.', '').replace(',', '.'))


def convertir_extractos_galicia_2022(path):

    # imputaciones_df = pd.read_excel(r'../data/bind/clasificacion_bind.xlsx')

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
            # print(i, line)
            if 'SALDO INICIAL' in line:
                # print(line)
                pattern = r"(\d{2}-\d{2}) SALDO INICIAL ([\d.]+,\d{2})"
                match = re.search(pattern, line)
                if match:
                    groups = match.groups()
                    fecha = groups[0]
                    saldo = groups[1]

                    if line.endswith('-'):
                        saldo = '-' + saldo

                    data.append({
                        'Fecha': fecha,
                        'Descripcion': 'Saldo Inicial',
                        'Saldo': saldo,
                        'Detalle': None
                    })

            else:
                pattern = r"(\d{2}-\d{2})\s+([^']+)"

                match = re.search(pattern, line)

                if match:
                    groups = match.groups()

                    fecha = groups[0]
                    descripcion = groups[1]

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
                        'Detalle': next_lines_str
                    })

                    next_lines = []

        df = pd.DataFrame(data)

        df['Saldo'] = df['Saldo'].replace({'': np.nan})  # Convierto los Nan en espacios vacios.
        df[['Descripcion', 'Importe', 'Saldo']] = df.apply(split_descripcion, axis=1)
        df = df.reindex(columns=['Fecha', 'Descripcion', 'Detalle', 'Importe', 'Saldo'])
        df['Importe'] = df['Importe'].str.replace('.', '').str.replace(',', '.')
        df['Importe'] = df['Importe'].astype(float)
        df['Saldo'] = df['Saldo'].apply(convert_to_float_galicia)

        df['Diferencia'] = df['Saldo'].diff()
        df['Tipo Movimiento'] = df['Diferencia'].apply(asignar_tipo_movimiento)

        print(df.head(20))

        complete_file_path_sin_extension = complete_file_path.replace('.pdf', '')
        df.to_excel(f'{complete_file_path_sin_extension}.xlsx')


# path = (r'\\192.168.0.3\wns\Asesoramiento Contable\WNS\OBRAS ACUSTICAS SRL\Contabilidad\2023\Extractos '
#         r'bancarios\Galicia\formato viejo')
# convertir_extractos_galicia_2022(path)
