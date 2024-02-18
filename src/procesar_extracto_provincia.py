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


def convertir_extractos_provincia(path):

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

            pattern = r"(\d{2}/\d{2}/\d{4})\s+([^']+)"
            match = re.search(pattern, line)

            if match:
                groups = match.groups()

                data.append({
                    'Fecha': groups[0],
                    'Descripcion': groups[1],

                })

        df = pd.DataFrame(data)

        print(df)
        df['Descripcion'] = df['Descripcion'].astype(str)
        df['Descripcion_split'] = df['Descripcion'].str.split()

        df['Importe'] = df['Descripcion_split'].apply(lambda x: x[-3] if len(x) >= 3 else None)

        df['Fecha_ref'] = df['Descripcion_split'].apply(lambda x: x[-2] if len(x) >= 3 else None)
        df['Saldo'] = df['Descripcion_split'].apply(lambda x: x[-1] if len(x) >= 3 else None)

        # Elimina la columna auxiliar 'Descripcion_split'
        df = df.drop(columns=['Descripcion_split'])
        df_copy = df.copy()
        df_copy = df_copy.dropna(subset=['Saldo'])

        print(df_copy)

        df_copy['Importe'] = df_copy['Importe'].replace(['SALDO', 'SIN'], 0)
        df_copy['Fecha_ref'] = df_copy['Fecha_ref'].replace('ANTERIOR', 0)
        df_copy['Importe'] = df_copy['Importe'].astype(float)
        df_copy['Tipo Movimiento'] = df_copy['Importe'].apply(asignar_tipo_movimiento)

        complete_file_path_sin_extension = complete_file_path.replace('.pdf', '')
        df_copy.to_excel(f'{complete_file_path_sin_extension}.xlsx')


