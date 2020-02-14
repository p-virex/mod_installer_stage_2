import json
import os

import wx

VERSION = '2.0'

TITLE = 'My installer {}'.format(VERSION)

VERSION_CLIENT = 'v.1.7.1.2'

SIZE_FRAME = (600, 620)
SIZE_PANEL = (585, 585)

FRAME_STYLE = wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL | wx.BORDER

g_MODS_CONFIG = json.load(open(os.path.join(os.getcwd(), 'common', 'mods_config.json'), encoding='utf-8'))

STREAM_NAMES = ['Левша', 'Кортавый']

g_STREAM_SETTINGS = json.load(open(os.path.join(os.getcwd(), 'common', 'stream_settings.json'), encoding='utf-8'))


