import os

from common.common_utils import resource_path

ICON_PATH = resource_path('main.ico')
MAIN_LOGO_PATH = resource_path('temp_logo.png')
MAIN_LOGO_600x100_PATH = resource_path('logo_600_100.png')
MAIN_LOGO_600x500_PATH = resource_path('logo_600x500.png')
NEXT_BUTTON_PATH = resource_path('next_button.bmp')
BACK_BUTTON_PATH = resource_path('back_button.bmp')
WGC_DEFAULT_PATH = os.path.join(os.environ['PROGRAMDATA'], 'Wargaming.net', 'GameCenter', 'preferences.xml')

NOT_PATH_DEFAULT = resource_path('not_found.jpg')
