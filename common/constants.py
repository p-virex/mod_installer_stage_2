import json
import os

import wx

VERSION = '2.0'

TITLE = 'My installer {}'.format(VERSION)

SIZE_FRAME = (600, 620)
SIZE_PANEL = (585, 585)

FRAME_STYLE = wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL | wx.BORDER

ICON_PATH = os.path.join(os.getcwd(), 'res', 'main.ico')
MAIN_LOGO_PATH = os.path.join(os.getcwd(), 'res', 'temp_logo.png')
MAIN_LOGO_600x100_PATH = os.path.join(os.getcwd(), 'res', 'temp_logo_600x100.png')
MAIN_LOGO_600x500_PATH = os.path.join(os.getcwd(), 'res', 'temp_logo_600x500.png')
NEXT_BUTTON_PATH = os.path.join(os.getcwd(), 'res', 'next_button.bmp')
BACK_BUTTON_PATH = os.path.join(os.getcwd(), 'res', 'back_button.bmp')
WGC_DEFAULT_PATH = os.path.join(os.environ['PROGRAMDATA'], 'Wargaming.net', 'GameCenter', 'preferences.xml')

MODS_CONFIG = json.load(open(os.path.join(os.getcwd(), 'common', 'mods_config.json'), encoding='utf-8'))
