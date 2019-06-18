from photobooth.settings import config
from .stripvertical import StripVertical


# Retrieve the correct type of photostrip
if config.get('Photostrip', 'type') == 'vertical':
    photostrip = StripVertical()

else:
    photostrip = StripVertical()
