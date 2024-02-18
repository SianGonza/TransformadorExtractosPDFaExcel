import os
from utils.helper_functions import extract_text_from_pdf, asignar_tipo_movimiento, detallar_pagos_entes_recaudacion
import re
import pandas as pd

# configuracion
pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 500)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', 250)
pd.options.display.float_format = '{:,.2f}'.format


def convertir_extractos_stonex(path):

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

        next_line = None
        next_lines = []

        for i, line in enumerate(all_lines):
            print(line)
            pattern = r"(\d{1,2}/\d{2}/\d{2})?\s+([^$]+)\$ ([\d\.]+,\d+) (-?\$ [\d\.]+,\d+)"
            match = re.search(pattern, line)

            if match:

                groups = match.groups()

                # procesar la línea siguiente
                next_line_index = i + 1
                while next_line_index < len(all_lines):
                    next_line = all_lines[next_line_index]  # busco la linea siguiente
                    next_match = re.search(pattern, next_line)  # si la linea siguiente coincide con el patron

                    if next_match:
                        break  # rompo el bucle

                    # si la línea siguiente no coincide con el patrón, añadirla a next_lines
                    next_lines.append(next_line)
                    next_line_index += 1

                next_lines_str = '\n'.join(next_lines)

                data.append({
                    'Fecha': groups[0],
                    'Descripcion': groups[1],
                    'Detalle': next_lines_str,
                    'Importe': groups[2],
                    'Saldo': groups[3]
                })

                next_lines = []

        df = pd.DataFrame(data)
        print(df)


path = r'../data/test/stonex'
convertir_extractos_stonex(path)
