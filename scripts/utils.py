import re


def normalize_special_characters(text):
    """Maps special characters and common European accents to their ASCII equivalents."""
    mapping = {
        'ä': 'ae',
        'ö': 'oe',
        'ü': 'ue',
        'Ä': 'Ae',
        'Ö': 'Oe',
        'Ü': 'Ue',
        'ß': 'ss',
        'é': 'e',
        'è': 'e',
        'ê': 'e',
        'ë': 'e',
        'à': 'a',
        'â': 'a',
        'á': 'a',
        'ã': 'a',
        'ò': 'o',
        'ô': 'o',
        'ó': 'o',
        'õ': 'o',
        'ù': 'u',
        'û': 'u',
        'ú': 'u',
        'ì': 'i',
        'î': 'i',
        'í': 'i',
        'ï': 'i',
        'ç': 'c',
        'ñ': 'n',
        'É': 'E',
        'È': 'E',
        'Ê': 'E',
        'Ë': 'E',
        'À': 'A',
        'Â': 'A',
        'Á': 'A',
        'Ã': 'A',
        'Ò': 'O',
        'Ô': 'O',
        'Ó': 'O',
        'Õ': 'O',
        'Ù': 'U',
        'Û': 'U',
        'Ú': 'U',
        'Ì': 'I',
        'Î': 'I',
        'Í': 'I',
        'Ï': 'I',
        'Ç': 'C',
        'Ñ': 'N'
    }
    for char, replacement in mapping.items():
        text = text.replace(char, replacement)
    return text


def sanitize_name(text):
    """
    Standardizes names by removing umlauts and replacing
    non-alphanumeric characters with hyphens.
    """
    # Normalize Umlauts
    clean_name = normalize_special_characters(text)
    # Replace non-allowed chars with hyphens
    clean_name = re.sub(r'[^a-zA-Z0-9-]+', '-', clean_name)
    # Strip leading/trailing hyphens and spaces
    return clean_name.strip('-')
