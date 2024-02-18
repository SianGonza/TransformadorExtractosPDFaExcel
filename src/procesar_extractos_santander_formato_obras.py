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


def convertir_extractos_santander(path):

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
            # print(lines)
            all_lines.extend(lines)

        for i, line in enumerate(all_lines):

            pattern = r"(\d{1,2}/\d{2}/\d{2})\s+(.*)"
            match = re.search(pattern, line)

            if match:
                groups = match.groups()
                data.append({
                    'Fecha': groups[0],
                    'Descripcion': groups[1]
                })

        df = pd.DataFrame(data)
        df['Importe'] = df['Descripcion'].str.split().str[-1]
        df['Descripcion'] = df['Descripcion'].str.split().str[:-1].str.join(' ')
        df['Importe'] = pd.to_numeric(df['Importe'].str.replace('.', '').str.replace(',', '.'), errors='coerce')
        df['Descripcion'] = df['Descripcion'].str.replace('$', '')
        print(df)

        complete_file_path_sin_extension = complete_file_path.replace('.pdf', '')
        df.to_excel(f'{complete_file_path_sin_extension}.xlsx')


path = r'../data/test/santander'
convertir_extractos_santander(path)
