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


def convert_to_float_icbc(importe):
    if isinstance(importe, str) and importe.endswith('-'):
        importe = '-' + importe[:-1]

    return float(importe.replace('.', '').replace(',', '.'))



def convertir_extractos_icbc(path):

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
            if 'SALDO ULTIMO EXTRACTO' in line:
                pattern = r"(SALDO ULTIMO EXTRACTO AL \d{2}/\d{2}/\d{4}) ([\d.,]+)"
                match = re.search(pattern, line)
                if match:
                    groups = match.groups()
                    saldo = groups[1]

                    if line.endswith('-'):
                        saldo = '-' + saldo

                    data.append({
                        'Fecha': None,
                        'Descripcion': groups[0],
                        'Importe': saldo
                    })

            else:
                pattern = r"(\b\d{2}-\d{2}\b)\s+([^']+)"
                match = re.search(pattern, line)

                if match:
                    groups = match.groups()

                    data.append({
                        'Fecha': groups[0],
                        'Descripcion': groups[1],

                    })

        df = pd.DataFrame(data)
        df['Descripcion'] = df['Descripcion'].astype(str)
        df['Importe'] = df['Descripcion'].str.extract(r'([\d\.]+,\d+-?)').fillna(df['Importe'])
        df['Descripcion'] = df['Descripcion'].str.extract(r'(.*?)(?:[\d\.]+,\d+-?)')

        df['Importe'] = df['Importe'].apply(convert_to_float_icbc)

        df['Saldo'] = df['Importe'].cumsum()
        df['Tipo Movimiento'] = df['Importe'].apply(asignar_tipo_movimiento)

        print(df)

        complete_file_path_sin_extension = complete_file_path.replace('.pdf', '')
        df.to_excel(f'{complete_file_path_sin_extension}.xlsx')

