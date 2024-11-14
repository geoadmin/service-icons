import os


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


def fetch_and_clean_unlisted_sets():
    unlisted_icon_sets = os.environ.get('UNLISTED_ICON_SETS', '').split(',')
    cleaned_unlisted_icon_sets = [icon_set for icon_set in unlisted_icon_sets if icon_set]
    return cleaned_unlisted_icon_sets
