import pdfplumber


def extract_text_from_pdf(file_path):
    """
    This function opens the PDF and stores all the text from each page in a list.
    ----------------------
    Args:
        file_path: A string representing the path where the PDF file is located.
    Returns:
        A list containing the text from each page.
    """
    texts = []

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            lines = page_text.splitlines()
            texts.extend(lines)

    return texts


def extract_text_from_pdf_meridian(file_path, password=None):
    """
    This function opens the PDF and stores all the text from each page in a list.
    ----------------------
    Args:
        file_path: A string representing the path where the PDF file is located.
    Returns:
        A list containing the text from each page.
    """
    texts = []

    with pdfplumber.open(file_path, password=password) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            lines = page_text.splitlines()
            texts.extend(lines)

    return texts


def asignar_tipo_movimiento(diferencia):
    if diferencia < 0:
        return 'Debito'
    else:
        return 'Credito'


def convert_to_float(val):
    if val[-1] == '-':
        return -float(val[:-1].replace(',', ''))
    else:
        return float(val.replace(',', ''))


def eliminar_comas(df, columns):
    for col in columns:
        df[col] = df[col].str.replace(',', '')
    return df


def eliminar_puntos(df, columns):
    for col in columns:
        df[col] = df[col].str.replace('.', '')
    return df


def eliminar_signo_negativo_al_final(val):
    if val[-1] == '-':
        val = val.replace('-', '')
        val = float(val) * -1
    else:
        val = float(val)

    return val


def detallar_pagos_entes_recaudacion(row):
    if 'afip' in row['Detalle'].lower():
        return row['Descripcion'] + ' (Pago AFIP: ' + row['Detalle'] + ')'

    elif 'arba' in row['Detalle'].lower():
        return row['Descripcion'] + ' (Pago ARBA: ' + row['Detalle'] + ')'

    else:
        return row['Descripcion']
