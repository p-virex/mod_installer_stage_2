import json
import os

from common.common_utils import resource_path

ICON_PATH = resource_path('res_image\\main.ico')
MAIN_LOGO_600x100_PATH = resource_path('res_image\\logo_600_100.png')
MAIN_LOGO_600x500_PATH = resource_path('res_image\\logo_600x500.png')
CACHE_PATH = os.path.join(os.environ['appdata'], 'TEMP_INSTALLER_LOGS', 'cache.json')

WGC_DEFAULT_PATH = os.path.join(os.environ['PROGRAMDATA'], 'Wargaming.net', 'GameCenter', 'preferences.xml')

NOT_PATH_DEFAULT = resource_path('res_image\\not_found.jpg')
# путь до кеша игры
PATH_TO_CACHE_WOT = os.path.join(os.environ['appdata'], 'Wargaming.net', 'WorldOfTanks')

LOG_FOLDER = os.path.join(os.environ['appdata'], 'TEMP_INSTALLER', 'INSTALLER_LOGS')

g_MODS_CONFIG = json.load(open(resource_path('mods_config.json'), encoding='utf-8'))

g_PRESET_SETTINGS = json.load(open(resource_path('preset.json'), encoding='utf-8'))

PRESET_NAMES = list(g_PRESET_SETTINGS.keys())
