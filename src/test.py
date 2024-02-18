from utils.helper_functions import extract_text_from_pdf
import re
import pandas as pd


def extraer_info(file):
    texts = extract_text_from_pdf(file)
    all_lines = []
    for text in texts:
        lines = text.split('\n')
        for line in lines:
            parts = line.split('cuenta contable', 1)  # divide la línea en dos partes
            if len(parts) > 1:  # si la línea contiene 'cuenta contable'
                info = parts[1].strip()
                info = re.sub(r'^.*?(?=[A-Z])', '', info)
                all_lines.append(info)
    return all_lines


file = (r'C:\Users\WNS\Documents\recibos\extraer_info\2024-01-11 Asientos de Mov de Fondos - Error por falta de '
        r'imputaciones contables.pdf')

info = extraer_info(file)

# Crear un DataFrame con los datos
df = pd.DataFrame(info, columns=['Información'])

# Guardar el DataFrame en un archivo Excel
df.to_excel('informacion.xlsx', index=False)
