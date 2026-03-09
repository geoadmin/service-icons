import re


def normalize_umlauts(text):
    """Maps German umlauts to their ASCII equivalents."""
    mapping = {'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'Ä': 'Ae', 'Ö': 'Oe', 'Ü': 'Ue', 'ß': 'ss'}
    for char, replacement in mapping.items():
        text = text.replace(char, replacement)
    return text


def sanitize_name(text):
    """
    Standardizes names by removing umlauts and replacing
    non-alphanumeric characters with hyphens.
    """
    # Normalize Umlauts
    clean_name = normalize_umlauts(text)
    # Replace non-allowed chars with hyphens
    clean_name = re.sub(r'[^a-zA-Z0-9-]+', '-', clean_name)
    # Strip leading/trailing hyphens and spaces
    return clean_name.strip('-')
