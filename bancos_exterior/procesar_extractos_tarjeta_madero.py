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


def convertir_extractos_madero(path):

    files_list = []

    for file in os.listdir(path):
        if file.endswith('.pdf'):
            files_list.append(file)

        # Lista para almacenar los resultados
        resultados = []

        for file in files_list:
            print(f'Transformando archivo: {file}')
            complete_file_path = os.path.join(path, file)
            texts = extract_text_from_pdf(complete_file_path)

            transaccion_actual = {}
            detalles_transaccion = []

            for text in texts:
                # Expresiones regulares para extraer la información
                venta_pattern = re.compile(r"\+ VENTAS (C/DESCUENTO CONTADO|C/DTO CUOTAS FINANC. OTORG\.) \$ ([\d,.]+)")
                arancel_pattern = re.compile(r"- ARANCEL \$ ([\d,.]+)")
                iva_pattern = re.compile(r"- IVA CRED\.FISC\.COMERCIO S/ARANC [\d,]+% \$ ([\d,.]+)")
                retencion_pattern = re.compile(r"- RETENCION ING\.BRUTOS SIRTAC \$ ([\d,.]+)")
                importe_neto_pattern = re.compile(r"IMPORTE NETO DE PAGOS \$ ([\d,.]+)")

                # Buscar coincidencias en el extracto
                venta_match = venta_pattern.search(text)
                arancel_match = arancel_pattern.search(text)
                iva_match = iva_pattern.search(text)
                retencion_match = retencion_pattern.search(text)
                importe_neto_match = importe_neto_pattern.search(text)

                # Extraer los valores encontrados
                if venta_match:
                    concepto = venta_match.group(1)
                    monto = venta_match.group(2)
                    transaccion_actual.setdefault(concepto, []).append(monto)
                elif arancel_match:
                    transaccion_actual['Arancel'] = float(arancel_match.group(1).replace(',', ''))
                elif iva_match:
                    transaccion_actual['IVA'] = float(iva_match.group(1).replace(',', ''))
                elif retencion_match:
                    transaccion_actual['Retencion'] = float(retencion_match.group(1).replace(',', ''))
                elif importe_neto_match:
                    transaccion_actual['Importe_Neto'] = float(importe_neto_match.group(1).replace(',', ''))

                # Si se encuentra una línea que indica una nueva transacción, guardar la actual en la lista de resultados
                if "Transacción" in text:
                    if transaccion_actual:  # Asegurar que hay información en la transacción actual antes de agregarla
                        transaccion_actual['Detalles'] = detalles_transaccion
                        resultados.append(transaccion_actual)

                    # Reiniciar la información para la nueva transacción
                    transaccion_actual = {}
                    detalles_transaccion = []

                # Verificar si la línea tiene detalles de transacción y agregarlos a la lista
                if "Operación" in text or "F.de Pago" in text or "Fecha Tarj/ Plan" in text:
                    detalles_transaccion.append(text)

            # Agregar la última transacción a la lista de resultados
            if transaccion_actual:
                transaccion_actual['Detalles'] = detalles_transaccion
                resultados.append(transaccion_actual)

            # Convertir la lista de resultados en un DataFrame
        df = pd.DataFrame(resultados)
        print(df)



path = r'../data/test/madero'
convertir_extractos_madero(path)
