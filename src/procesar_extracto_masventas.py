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


def convert_to_float_masventas(importe):
    if isinstance(importe, str) and importe.endswith('-'):
        importe = '-' + importe[:-1]

    return float(importe.replace('.', '').replace(',', '.'))



def convertir_extractos_masventas(path):

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

        saldo_inicial_encontrado = False
        for i, line in enumerate(all_lines):
            # print(line)

            if not saldo_inicial_encontrado:
                pattern = r"Saldo Inicial: ([\d\.]+,\d+)"
                match = re.search(pattern, line)
                if match:
                    groups = match.groups()
                    saldo = groups[0]

                    if line.endswith('-'):
                        saldo = '-' + saldo

                    data.append({
                        'Fecha': None,
                        'Descripcion': 'Saldo Inicial',
                        'Saldo': saldo
                    })

                    saldo_inicial_encontrado = True

            else:
                pattern = r"(\d{1,2}/\d{2}/\d{4})\s+([^']+)"
                match = re.search(pattern, line)

                if match:
                    groups = match.groups()

                    data.append({
                        'Fecha': groups[0],
                        'Descripcion': groups[1],

                    })

        df = pd.DataFrame(data)

        df['Descripcion_split'] = df['Descripcion'].str.split()
        df['Descripcion'] = df['Descripcion_split'].apply(lambda x: ' '.join(x[:-3]) if len(x) >= 3 else ' '.join(x))

        def asignar_valores(x):
            if len(x) >= 3:
                return x[-3], x[-2], x[-1]
            elif x[0] == 'Saldo Inicial':
                return None, None, x[1]
            else:
                return None, None, None

        df['Debito'], df['Credito'], df['Saldo_temp'] = zip(*df['Descripcion_split'].apply(asignar_valores))

        # Reemplazamos los valores en 'Saldo' solo cuando 'Saldo_temp' no es None
        df.loc[df['Saldo_temp'].notna(), 'Saldo'] = df['Saldo_temp']

        df = df.drop(columns=['Descripcion_split', 'Saldo_temp'])
        df = df.dropna(subset=['Saldo'])
        df = df.reindex(columns=['Fecha', 'Descripcion', 'Debito', 'Credito', 'Saldo'])

        df['Saldo'] = df['Saldo'].apply(convert_to_float_masventas)

        print(df)
        complete_file_path_sin_extension = complete_file_path.replace('.pdf', '')
        df.to_excel(f'{complete_file_path_sin_extension}.xlsx')


