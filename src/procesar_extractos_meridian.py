import os
from utils.helper_functions import extract_text_from_pdf_meridian, asignar_tipo_movimiento
import re
import pandas as pd
import numpy as np

# configuracion
pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 500)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', 250)
pd.options.display.float_format = '{:,.2f}'.format


def dividir_importe_y_saldo(x):
    if ' '.join(x) == 'Saldo Inicial':
        return None, None

    if len(x) >= 2:
        return x[-2], x[-1]

    else:
        return None, None, None


def convert_to_float_masventas(importe):
    if isinstance(importe, str) and importe.endswith('-'):
        importe = '-' + importe[:-1]

    return float(importe.replace(',', ''))


def convertir_extractos_meridian(path):
    files_list = []

    for file in os.listdir(path):
        if file.endswith('.pdf'):
            files_list.append(file)

    for file in files_list:

        data = []

        print(f'Transformando archivo: {file}')
        complete_file_path = os.path.join(path, file)
        texts = extract_text_from_pdf_meridian(complete_file_path, '232647')

        all_lines = []

        for text in texts:
            lines = text.split('\n')
            all_lines.extend(lines)

        for i, line in enumerate(all_lines):
            # print(line)
            if 'SALDO FINAL' in line:
                pattern = r"SALDO FINAL (-?[\d,]+.\d+)"
                match = re.search(pattern, line)
                if match:
                    print("Hasta aca hay que leer del extracto")
                    break

            if 'SALDO INCIAL' in line:
                # print(line)
                pattern = r"SALDO INCIAL (-?[\d,]+.\d+)"
                match = re.search(pattern, line)
                if match:
                    groups = match.groups()
                    saldo = groups[0]

                    if line.endswith('-'):
                        saldo = '-' + saldo

                    data.append({
                        'Fecha': None,
                        'Descripcion': 'Saldo Inicial',
                        'Importe': None,
                        'Saldo': saldo
                    })

            else:
                pattern = r"(\d{1,2}/\d{2})\s+([^']+)"
                match = re.search(pattern, line)

                if match:
                    groups = match.groups()

                    data.append({
                        'Fecha': groups[0],
                        'Descripcion': groups[1],

                    })

        df = pd.DataFrame(data)

        df['Descripcion_split'] = df['Descripcion'].str.split()
        df['Descripcion'] = df['Descripcion_split'].apply(lambda x: ' '.join(x[:-2]) if len(x) >= 2 else ' '.join(x))
        df['Importe'], df['Saldo_temp'] = zip(*df['Descripcion_split'].apply(dividir_importe_y_saldo))

        # Reemplazamos los valores en 'Saldo' con los de saldo_temp solo cuando saldo es NaN
        mask = df['Saldo'].isna()
        df.loc[mask, 'Saldo'] = df['Saldo_temp']
        df = df.drop(columns=['Descripcion_split', 'Saldo_temp'])

        # Eliminar de la columna saldo los valores con formato de fecha
        fecha_regex = r"\d{1,2}/\d{2}/\d{2}"
        mask_fecha = df['Saldo'].str.contains(fecha_regex, na=False)
        df.loc[mask_fecha, 'Saldo'] = np.nan
        df = df.dropna(subset=['Saldo']).reset_index(drop=True)
        df['Saldo'] = df['Saldo'].apply(convert_to_float_masventas)
        df['Importe'] = df['Importe'].fillna('0.00')
        df['Importe'] = df['Importe'].apply(convert_to_float_masventas)

        df['Diferencia'] = df['Saldo'].diff()
        df['Tipo Movimiento'] = df['Diferencia'].apply(asignar_tipo_movimiento)

        complete_file_path_sin_extension = complete_file_path.replace('.pdf', '')
        df.to_excel(f'{complete_file_path_sin_extension}.xlsx')

        print(df)
        print(df.dtypes)


