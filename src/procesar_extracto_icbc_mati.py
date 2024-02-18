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


def convertir_extractos_icbc_mati(path):
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

            pattern = r"(\d{2}-\w{3}-\d{4})\s+(.*\s\$\s)(-?\d{1,},\d{2})\s\$\s(-?\d{1,},\d{2})"

            match = re.search(pattern, line)

            if match:
                fecha = match.group(1)
                descripcion = match.group(2).strip()
                importe_str = match.group(3).strip()
                saldo = match.group(4).strip()

                # Agregar los datos que coinciden con el patron a la lista.
                data.append({
                    'Fecha': fecha,
                    'Descripcion': descripcion,
                    'Importe': importe_str,
                    'Saldo': saldo
                })

        df = pd.DataFrame(data)
        df['Importe'] = df['Importe'].str.replace(',', '.')
        df['Importe'] = df['Importe'].astype(float)

        df['Saldo'] = df['Saldo'].str.replace(',', '.')
        df['Saldo'] = df['Saldo'].astype(float)

        print(df)

        complete_file_path_sin_extension = complete_file_path.replace('.pdf', '')
        df.to_excel(f'{complete_file_path_sin_extension}.xlsx')


# path = '../data/test/icbc/mati'
# convertir_extractos_icbc(path)
