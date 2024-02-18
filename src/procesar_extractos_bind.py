import os
from utils.helper_functions import extract_text_from_pdf, convert_to_float, asignar_tipo_movimiento
import re
import pandas as pd

# configuracion
pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 500)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', 800)
pd.options.display.float_format = '{:,.2f}'.format


def convertir_extractos_bind(path):

    # imputaciones_df = pd.read_excel(r'../data/clasificacion/bind/clasificacion_bind.xlsx')

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
            # print(i, line)
            pattern = r"(\d{1,2}/\d{2}/\d{2})\s+([^']+)\s+([\d,]+\.\d{2}-?)\s+([\d,]+\.\d{2}-?) (\d+)$"

            match = re.search(pattern, line)
            if match:
                groups = match.groups()
                data.append({
                    'Fecha': groups[0],
                    'Descripcion': groups[1],
                    'Importe': groups[2],
                    'Saldo': groups[3],
                    # 'Numero': groups[4],
                })

        # Convertir la lista de diccionarios en un DataFrame
        df = pd.DataFrame(data)

        df['Importe'] = df['Importe'].str.replace(',', '')
        df['Importe'] = df['Importe'].astype(float)

        df['Saldo'] = df['Saldo'].apply(convert_to_float)

        # Calcular la diferencia
        df['Diferencia'] = df['Saldo'].diff()

        # Si quieres rellenar la primera fila (que será NaN después de aplicar diff()) con el primer valor de 'Saldo'
        df['Diferencia'].fillna(df['Saldo'], inplace=False)

        # Crear la nueva columna 'Tipo Movimiento'
        df['Tipo Movimiento'] = df['Diferencia'].apply(asignar_tipo_movimiento)

        print(df.head(25))

        df.to_excel(f'{complete_file_path}.xlsx')


# path = r'\\192.168.0.3\wns\Asesoramiento Contable\WNS\CREDI LOW S.A\Contabilidad\2023\Informacion del cliente\Extractos bancarios\Extractos\BIND\12'
# convertir_extractos_bind(path)
