import os
from utils.helper_functions import extract_text_from_pdf_meridian, asignar_tipo_movimiento
import re
import pandas as pd

# configuracion
pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 500)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', 250)
pd.options.display.float_format = '{:,.2f}'.format


def convertir_extractos_fiserv(path):
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
            print(line)
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
        print(df)


path = r'C:\Users\WNS\PycharmProjects\TransformadorExtractos\data\test\fiserv'
convertir_extractos_fiserv(path)

