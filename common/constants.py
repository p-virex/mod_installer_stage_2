import os

import wx


g_PYTHON_START = True if os.path.isfile(os.path.join(os.getcwd(), 'start_python')) else False

g_DEBUG = True if os.path.isfile(os.path.join(os.getcwd(), 'debug')) else False

VERSION = '2.0'

TITLE = 'Sharewax installer {}'.format(VERSION)

VERSION_CLIENT = 'v.1.8.0.1'

SIZE_FRAME = (600, 660)
SIZE_PANEL = (585, 625)

FRAME_STYLE = wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL | wx.BORDER

DROP_GAME_FOLDER = ['battle_results', 'clan_cache', 'custom_data', 'veh_cmp_cache', 'dossier_cache', 'web_cache']

DROP_XVM_FOLDER = ['xvm\\Hitlog', 'xvm\\cache', 'xvm\\custom_data', 'xvm\\statistics']

DEFAULT_LANG = 'RU'
