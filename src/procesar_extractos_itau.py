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


def limpiar_descripcion_impuesto_ley(row):
    if 'impuesto - ley' in row['Descripcion'].lower():
        return 'Impuesto Ley - 25413'
    else:
        return row['Descripcion']




def convertir_extractos_itau(path):
    files_list = []

    for file in os.listdir(path):
        if file.endswith('.pdf'):
            files_list.append(file)

    for file in files_list:

        data_saldo_inicial = []
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

        n = 0

        for i, line in enumerate(all_lines):
            # print(line)
            pattern = r'SALDO AL (\d{2}/\d{2}/\d{2}) (-?\d+\.\d{3},\d{2})'
            match = re.search(pattern, line)

            if match:

                n += 1

                # si encuentro el patron dos veces rompo el bucle para no seguir tomando mas movimientos
                if n == 2:
                    break

                groups = match.groups()

                fecha = groups[0]
                saldo = groups[1]

                data_saldo_inicial.append({
                    'Fecha': fecha,
                    'Descripcion': 'SALDO INICIAL',
                    'Importe': None,
                    'Saldo': saldo
                })

            else:
                pattern = r"(\d{2}/\d{2}/\d{2})\s+(.*)"
                match = re.search(pattern, line)

                if match:
                    groups = match.groups()

                    fecha = groups[0]
                    descripcion = groups[1]
                    # importe = groups[2]
                    # saldo = groups[3]

                    data.append({
                        'Fecha': fecha,
                        'Descripcion': descripcion,
                        # 'Importe': importe,
                        # 'Saldo': saldo

                    })

        df = pd.DataFrame(data)
        df_saldo_inicial = pd.DataFrame(data_saldo_inicial)
        df[['Descripcion', 'Importe', 'Saldo']] = df['Descripcion'].str.rsplit(' ', n=2, expand=True)

        df_final = pd.concat([df_saldo_inicial, df])

        df_final = eliminar_puntos(df_final, ['Importe', 'Saldo'])
        df_final['Importe'] = df_final['Importe'].str.replace(',', '.')
        df_final['Saldo'] = df_final['Saldo'].str.replace(',', '.')
        df_final = df_final.fillna(0)
        df_final['Importe'] = df_final['Importe'].astype(float)
        df_final['Saldo'] = df_final['Saldo'].astype(float)

        df_final['Diferencia'] = df_final['Saldo'].diff()
        df_final['Tipo Movimiento'] = df_final['Diferencia'].apply(asignar_tipo_movimiento)

        df_final['Descripcion'] = df_final.apply(limpiar_descripcion_impuesto_ley, axis=1)

        print(df_final)

        complete_file_path_sin_extension = complete_file_path.replace('.pdf', '')
        df_final.to_excel(f'{complete_file_path_sin_extension}.xlsx')


# path = (r'\\192.168.0.3\wns\Asesoramiento Contable\WNS\PNC SRL\Contabilidad\2023\INFORMACION DEL CLIENTE\EXTRACTOS BANCARIOS\ITAU')
# convertir_extractos_itau(path)
