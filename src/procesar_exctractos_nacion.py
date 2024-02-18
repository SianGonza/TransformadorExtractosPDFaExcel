import os
from utils.helper_functions import extract_text_from_pdf, asignar_tipo_movimiento
import re
import pandas as pd

# configuracion
pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 500)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', 250)
pd.options.display.float_format = '{:,.2f}'.format


def convert_to_float(df, column):
    df[column] = df[column].str.replace('.', '').str.replace(',', '.').astype(float)


def convertir_extractos_nacion(path):

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

        for i, line in enumerate(all_lines):
            # print(line)
            if 'SALDO ANTERIOR' in line:
                pattern = r"(SALDO ANTERIOR)\s+([\d.,]+)-?"
                match = re.search(pattern, line)
                if match:
                    groups = match.groups()
                    saldo = groups[1]
                    if line.endswith('-'):
                        saldo = '-' + saldo
                    data.append({
                        'Fecha': None,
                        'Descripcion': groups[0],
                        'Importe': None,
                        'Saldo': saldo
                    })
            else:
                pattern = r"(\d{2}/\d{2}/\d{2})\s+([^$]+) ([\d\.]+,\d+)\s+([\d.,]+)-?"
                match = re.search(pattern, line)

                if match:
                    groups = match.groups()
                    saldo = groups[3]
                    if line.endswith('-'):
                        saldo = '-' + saldo

                    data.append({
                        'Fecha': groups[0],
                        'Descripcion': groups[1],
                        'Importe': groups[2],
                        'Saldo': saldo
                    })

        df = pd.DataFrame(data)

        # Convertimos a float las columnas de saldos e importe
        convert_to_float(df, 'Saldo')
        convert_to_float(df, 'Importe')

        # Calculamos la diferencia entre saldos para saber si el importe es negativo o positivos
        df['Diferencia'] = df['Saldo'].diff()
        df['Diferencia'].fillna(df['Importe'], inplace=False)

        # Creamos una columna Tipo Movimiento y dependiendo si es negativo o positivo la diferencia le asignamos un tipo
        # de movimiento (debito o credito)
        df['Tipo Movimiento'] = df['Diferencia'].apply(asignar_tipo_movimiento)

        complete_file_path_sin_extension = complete_file_path.replace('.pdf', '')
        df.to_excel(f'{complete_file_path_sin_extension}.xlsx')


# path = r'\\192.168.0.3\wns\Asesoramiento Contable\WNS\CASA BERGMAN SOCIEDAD ANONIMA\Subdiarios\2024\01-2024\repedidodeinformacioncasabergmans_a_012024\BANCOS\nacion'
# convertir_extractos_nacion(path)
