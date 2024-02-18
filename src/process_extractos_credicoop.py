import pandas as pd
import os
from utils.helper_functions import extract_text_from_pdf
import re
from fuzzywuzzy import fuzz, process

# configuracion
pd.set_option('display.max_rows', 2000)
pd.set_option('display.max_columns', 500)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', 800)
pd.options.display.float_format = '{:,.2f}'.format


def convertir_extracto_credicoop(path):

    files_list = []

    for file in os.listdir(path):
        if file.endswith('.pdf'):
            files_list.append(file)

    for file in files_list:
        print(f'Transformando archivo: {file}')
        complete_file_path = os.path.join(path, file)
        texts = extract_text_from_pdf(complete_file_path)

        data = []

        imputaciones_df = pd.read_excel(r'./data/clasificacion/credicoop/clasificacion_credicoop.xlsx')
        previous_line = None


        ### ORIGINAL
        # for text in texts:
        #     # print(text)
        #     pattern = r'(\d{2}/\d{2}/\d{2})\s(.+?)\s([\d.,]+)(?:\s(−?[\d.,]+))?$'
        #     matches = re.findall(pattern, text, re.MULTILINE)
        #     for match in matches:
        #         fecha = match[0]
        #         descripcion = match[1].strip()
        #         importe_str = match[2].strip()
        #
        #         saldo = None
        #
        #         if match[3]:
        #             saldo_str = match[3].strip()
        #
        #         # Obtener la posición final del patrón coincidente
        #         start, end = match.start(), match.end()
        #
        #         # Capturar líneas siguientes hasta encontrar una nueva línea que coincida con el patrón
        #         additional_text = text[end:text.find('\n', end)].strip()
        #         print(additional_text)
        #
        #         # Agregar los datos que coinciden con el patron a la lista.
        #         data.append((fecha, descripcion, importe_str, additional_text, saldo))

        # TEST
        # print(texts)
        all_lines = []

        for text in texts:
            lines = text.split('\n')
            all_lines.extend(lines)

        next_line = None

        for i, line in enumerate(all_lines):
            # print(i, line)
            pattern = r'(\d{2}/\d{2}/\d{2})\s(.+?)\s([\d.,]+)(?:\s(−?[\d.,]+))?$'
            match = re.search(pattern, line)

            if match:
                fecha = match.group(1)
                descripcion = match.group(2).strip()
                importe_str = match.group(3).strip()
                saldo = None

                # procesar la línea siguiente
                next_line_index = i + 1
                if next_line_index < len(all_lines):
                    next_line = all_lines[next_line_index]
                    next_match = re.search(pattern, next_line)

                    if next_match:
                        # si la línea siguiente coincide con el patrón, establecer next_line como None
                        next_line = None
                    # print(next_line)

                # Agregar los datos que coinciden con el patron a la lista.
                data.append((fecha, descripcion, importe_str, next_line, saldo))

        extracto_df = pd.DataFrame(data, columns=['Fecha', 'Descripcion', 'Importe', 'Texto Adicional', 'Saldo'])


        extracto_df['Tipo de Movimiento'] = None
        umbral_similitud = 85

        # Clasificar los movimientos basados en las descripciones
        for index, row in extracto_df.iterrows():
            descripcion = row['Descripcion']

            # Buscar la descripción más cercana en el DataFrame de imputaciones
            mejores_coincidencias = process.extract(descripcion, imputaciones_df['Descripcion'],
                                                    scorer=fuzz.token_sort_ratio)

            # Filtrar las coincidencias con similitud por encima del umbral
            coincidencias_filtradas = [match for match in mejores_coincidencias if match[1] >= umbral_similitud]

            if coincidencias_filtradas:
                # Obtener la descripción más cercana y su tipo de movimiento
                descripcion_cercana = coincidencias_filtradas[0][0]
                tipo_movimiento = imputaciones_df[imputaciones_df['Descripcion'] == descripcion_cercana].iloc[0][
                    'Tipo de Movimiento']
                extracto_df.at[index, 'Tipo de Movimiento'] = tipo_movimiento
            else:
                tipo_movimiento = 'Sin Tipo de Movimiento'
                extracto_df.at[index, 'Tipo de Movimiento'] = tipo_movimiento

        extracto_df['Importe'] = extracto_df['Importe'].str.replace('.', '').str.replace(',', '.').astype(float)
        total_debitos = extracto_df.loc[extracto_df['Tipo de Movimiento'] == 'Debitos', 'Importe'].sum()
        total_creditos = extracto_df.loc[extracto_df['Tipo de Movimiento'] == 'Creditos', 'Importe'].sum()

        file_name = file.replace('.pdf', '')
        ubicacion_guardado_excels = os.path.join(path, file_name)
        extracto_df.to_excel(f'{ubicacion_guardado_excels}.xlsx')
