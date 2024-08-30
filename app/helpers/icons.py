from app.settings import DEFAULT_ICON_SIZE


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


def calculate_icon_size(size, scale=1):
    """
    Calculate icon size so that the size of the smaller dimension is equal to the standard icon size
    multiplied by the scaling
    """
    width, height = size
    min_size = min(width, height)
    return (
        int(scale * DEFAULT_ICON_SIZE * width / min_size),
        int(scale * DEFAULT_ICON_SIZE * height / min_size)
    )
