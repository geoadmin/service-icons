def get_icon_set_template_url(base_url=''):
    """
    Generate and return a template URL to access icon_sets' metadata
    """
    return f"{base_url}/sets/{{icon_set_name}}"


def get_icon_template_url(base_url='', with_color=True):
    """
    Generate and returns a URL template for icons
    """
    color_part = ""
    if with_color:
        color_part = "-{r},{g},{b}"
    return f"{get_icon_set_template_url(base_url)}/icons/{{icon_name}}" \
           f"@{{icon_scale}}{color_part}.png"


def split_and_clean_string(input_string):
    split_string = input_string.split(',')
    cleaned_split_string = [string_item for string_item in split_string if string_item]
    return cleaned_split_string
