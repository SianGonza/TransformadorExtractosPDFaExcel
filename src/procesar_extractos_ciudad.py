import os
from utils.helper_functions import extract_text_from_pdf, eliminar_puntos, asignar_tipo_movimiento, eliminar_comas
from utils.helper_functions import eliminar_signo_negativo_al_final
import re
import pandas as pd
import numpy as np


# configuracion
pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 500)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', 800)
pd.options.display.float_format = '{:,.2f}'.format


def convertir_extractos_ciudad(path):

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

            pattern = r"(\d{2}-[A-Z]{3}-\d{4})\s+(.+?)\s+([\d\.]+,\d{2})\s*([\d\.]+,\d{2}-?)"
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
        df = eliminar_puntos(df, ['Importe', 'Saldo'])
        df['Importe'] = df['Importe'].str.replace(',', '.')
        df['Saldo'] = df['Saldo'].str.replace(',', '.')
        df['Saldo'] = df['Saldo'].apply(eliminar_signo_negativo_al_final)
        df['Importe'] = df['Importe'].astype(float)
        df['Diferencia'] = df['Saldo'].diff()
        df['Tipo Movimiento'] = df['Diferencia'].apply(asignar_tipo_movimiento)
        print(df)

        complete_file_path_sin_extension = complete_file_path.replace('.pdf', '')
        df.to_excel(f'{complete_file_path_sin_extension}.xlsx')


# path = r'../data/test/ciudad'
# convertir_extractos_ciudad(path)
