import re
import unicodedata

# Define the German-specific mapping once
GERMAN_UMLAUTS_MAPPING = str.maketrans({
    'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'Ä': 'Ae', 'Ö': 'Oe', 'Ü': 'Ue', 'ß': 'ss'
})


def normalize_special_characters(text):
    # Step 1: handle the german umlauts specifically (make sure, ö will be oe and so on.)
    text = text.translate(GERMAN_UMLAUTS_MAPPING)

    # Step 2: Decompose remaining accents (é -> e + ´)
    # NFKD separates the base character from the "combining" accent mark
    text = unicodedata.normalize('NFKD', text)

    # Filter out the combining marks (the accents) and rejoin
    return "".join(c for c in text if not unicodedata.combining(c))


def sanitize_name(text):
    """
    Standardizes names by removing umlauts and replacing
    non-alphanumeric characters with hyphens.
    """
    # Normalize Umlauts
    clean_name = normalize_special_characters(text)
    # Replace non-allowed chars with hyphens
    clean_name = re.sub(r'[^a-zA-Z0-9-]+', '-', clean_name)
    # prevent multiple subsequent hyphens, such as -- for example. Replace with a single -
    clean_name = re.sub(r'-+', '-', clean_name)
    # Strip leading/trailing hyphens and spaces
    return clean_name.strip('-')
