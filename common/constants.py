import json
import os

import wx

VERSION = '2.0'

TITLE = 'My installer {}'.format(VERSION)

VERSION_CLIENT = 'v.1.7.1.2'

SIZE_FRAME = (600, 660)
SIZE_PANEL = (585, 625)

FRAME_STYLE = wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL | wx.BORDER

g_MODS_CONFIG = json.load(open(os.path.join(os.getcwd(), 'common', 'mods_config.json'), encoding='utf-8'))

g_PRESET_SETTINGS = json.load(open(os.path.join(os.getcwd(), 'common', 'stream_settings.json'), encoding='utf-8'))

STREAM_NAMES = list(g_PRESET_SETTINGS.keys())


DROP_GAME_FOLDER = ['battle_results', 'clan_cache', 'custom_data', 'veh_cmp_cache', 'dossier_cache', 'web_cache']

DROP_XVM_FOLDER = ['xvm\\Hitlog', 'xvm\\cache', 'xvm\\custom_data', 'xvm\\statistics']
