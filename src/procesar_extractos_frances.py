import os
from utils.helper_functions import extract_text_from_pdf, asignar_tipo_movimiento
import re
import pandas as pd

# configuracion
pd.set_option('display.max_rows', 2000)
pd.set_option('display.max_columns', 500)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', 800)
pd.options.display.float_format = '{:,.2f}'.format


def convertir_extractos_frances(path):

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
            # print(lines)

        for i, line in enumerate(all_lines):
            # print(line)
            pattern = r'(\d{2}/\d{2})\s(.+?)\s(-?[\d.,]+)\s(-?[\d.,]+)$'
            match = re.search(pattern, line)

            if match:
                groups = match.groups()
                data.append({
                    'Fecha': groups[0],
                    'Descripcion': groups[1],
                    'Importe': groups[2],
                    'Saldo': groups[3]
                })

        # Convertir la lista de diccionarios en un DataFrame
        df = pd.DataFrame(data)

        df['Importe'] = df['Importe'].str.replace('.', '').str.replace(',', '.')
        df['Importe'] = df['Importe'].astype(float)

        df['Saldo'] = df['Saldo'].str.replace('.', '').str.replace(',', '.')
        df['Saldo'] = df['Saldo'].astype(float)

        # Calcular la diferencia
        df['Diferencia'] = df['Saldo'].diff()
        df['Tipo Movimiento'] = df['Diferencia'].apply(asignar_tipo_movimiento)

        print(df)
        complete_file_path_sin_extension = complete_file_path.replace('.pdf', '')
        df.to_excel(f'{complete_file_path_sin_extension}.xlsx')


# test
# convertir_extractos_frances(r'../data/test/frances/domestic')
