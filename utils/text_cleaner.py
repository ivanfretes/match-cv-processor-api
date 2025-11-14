"""
Utilidades para limpiar y normalizar texto extraído de PDFs.
"""
import re
from typing import Optional


def clean_pdf_text(text: str) -> str:
    """
    Limpia y normaliza el texto extraído de un PDF.
    
    Esta función:
    - Elimina caracteres no imprimibles y control
    - Normaliza espacios en blanco múltiples
    - Convierte saltos de línea entre palabras en espacios
    - Identifica y preserva párrafos reales
    - Mantiene la estructura legible del texto
    
    Args:
        text: Texto crudo extraído del PDF
        
    Returns:
        Texto limpio y normalizado
    """
    if not text:
        return ""
    
    # Eliminar caracteres de control y no imprimibles
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
    
    # Reemplazar tabs por espacios
    text = text.replace('\t', ' ')
    
    # Dividir en líneas primero
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    if not lines:
        return ""
    
    # Procesar líneas: unir líneas cortas (palabras sueltas) y preservar estructura
    cleaned_lines = []
    prev_was_short = False
    
    for i, line in enumerate(lines):
        is_short = len(line) < 60  # Línea corta (probablemente palabra suelta)
        is_very_short = len(line) < 30
        ends_sentence = bool(re.search(r'[.!?]\s*$', line))
        is_title_caps = bool(re.match(r'^[A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ\s]{3,}$', line) and len(line) < 50)
        
        # Si es una línea muy corta, probablemente es una palabra suelta - unir con la anterior
        if is_very_short and cleaned_lines and not ends_sentence:
            # Unir con la línea anterior
            if cleaned_lines:
                cleaned_lines[-1] = cleaned_lines[-1] + ' ' + line
            else:
                cleaned_lines.append(line)
        # Si es corta pero la anterior también era corta y no termina en oración, unir
        elif is_short and cleaned_lines and prev_was_short and not ends_sentence:
            cleaned_lines[-1] = cleaned_lines[-1] + ' ' + line
        # Si es un título en mayúsculas, mantenerlo como nueva línea
        elif is_title_caps:
            if cleaned_lines:
                cleaned_lines.append('')  # Línea vacía antes del título
            cleaned_lines.append(line)
        # Si la línea anterior terminaba en oración y esta empieza con mayúscula, nueva línea
        elif cleaned_lines and re.search(r'[.!?]\s*$', cleaned_lines[-1]) and re.match(r'^[A-ZÁÉÍÓÚÑ]', line):
            cleaned_lines.append(line)
        # Si la línea es muy larga (párrafo completo), mantenerla separada
        elif len(line) > 120:
            if cleaned_lines:
                cleaned_lines.append('')
            cleaned_lines.append(line)
        # Por defecto, unir con la anterior si ambas son cortas
        elif is_short and cleaned_lines and len(cleaned_lines[-1]) < 100:
            cleaned_lines[-1] = cleaned_lines[-1] + ' ' + line
        else:
            # Nueva línea
            cleaned_lines.append(line)
        
        prev_was_short = is_short or is_very_short
    
    # Unir todas las líneas
    text = '\n'.join(cleaned_lines)
    
    # Limpiar espacios múltiples dentro de cada línea
    lines = text.split('\n')
    lines = [re.sub(r' +', ' ', line.strip()) for line in lines]
    text = '\n'.join(lines)
    
    # Normalizar espacios alrededor de puntuación
    # Eliminar espacios antes de puntuación
    text = re.sub(r' +([.,:;!?])', r'\1', text)
    # Añadir espacio después de puntuación si no hay
    text = re.sub(r'([.,:;!?])([^\s\n])', r'\1 \2', text)
    
    # Eliminar líneas vacías al inicio y final
    lines = [line for line in text.split('\n')]
    # Eliminar líneas vacías al inicio
    while lines and not lines[0].strip():
        lines.pop(0)
    # Eliminar líneas vacías al final
    while lines and not lines[-1].strip():
        lines.pop()
    
    text = '\n'.join(lines)
    
    # Reducir múltiples saltos de línea consecutivos a máximo 2
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Limpiar espacios al inicio y final del texto completo
    text = text.strip()
    
    return text


def clean_text_preserve_structure(text: str) -> str:
    """
    Limpia el texto preservando mejor la estructura original.
    Versión más conservadora que mantiene más la estructura del documento.
    
    Args:
        text: Texto crudo extraído del PDF
        
    Returns:
        Texto limpio pero con estructura preservada
    """
    if not text:
        return ""
    
    # Eliminar caracteres de control y no imprimibles
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
    
    # Reemplazar espacios en blanco múltiples dentro de una línea por uno solo
    # Pero preservar saltos de línea
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        # Limpiar espacios múltiples en cada línea
        cleaned_line = re.sub(r' +', ' ', line.strip())
        cleaned_lines.append(cleaned_line)
    
    # Unir líneas, eliminando líneas vacías múltiples
    text = '\n'.join(cleaned_lines)
    
    # Reducir múltiples saltos de línea consecutivos a máximo 2
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Limpiar espacios al inicio y final
    text = text.strip()
    
    return text

