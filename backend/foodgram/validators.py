import re
from django.core.exceptions import ValidationError


def hex_color_validator(value):
    if not re.match(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$', value):
        raise ValidationError('Enter the correct HEX color code')
