import os

from common.common_utils import resource_path

ICON_PATH = resource_path('res_image\\main.ico')
MAIN_LOGO_PATH = resource_path('res_image\\temp_logo.png')
MAIN_LOGO_600x100_PATH = resource_path('res_image\\logo_600_100.png')
MAIN_LOGO_600x500_PATH = resource_path('res_image\\logo_600x500.png')
NEXT_BUTTON_PATH = resource_path('res_image\\next_button.bmp')
BACK_BUTTON_PATH = resource_path('res_image\\back_button.bmp')
WGC_DEFAULT_PATH = os.path.join(os.environ['PROGRAMDATA'], 'Wargaming.net', 'GameCenter', 'preferences.xml')

NOT_PATH_DEFAULT = resource_path('res_image\\not_found.jpg')
