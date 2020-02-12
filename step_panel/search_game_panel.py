import os
import xml.etree.cElementTree as et

import wx

from common.constants import MAIN_LOGO_600x100_PATH, SIZE_PANEL, BACK_BUTTON_PATH, NEXT_BUTTON_PATH, WGC_DEFAULT_PATH
from core.panel_template import TemplatePanel


class SearchGamePanelUi(TemplatePanel):
    def __init__(self, parent, panel_name):
        super(SearchGamePanelUi, self).__init__(parent, panel_name)
        self.SetSizeHints(minSize=SIZE_PANEL, maxSize=SIZE_PANEL)
        self.logo_image = wx.Bitmap(MAIN_LOGO_600x100_PATH)
        bmp_back = wx.Image(BACK_BUTTON_PATH, wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        bmp_next = wx.Image(NEXT_BUTTON_PATH, wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        self.button_back = wx.BitmapButton(self, wx.ID_ANY, bmp_back)
        self.button_next = wx.BitmapButton(self, wx.ID_ANY, bmp_next)
        self.game_path = wx.DirPickerCtrl(self, wx.ID_ANY, '')

        self.main_vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.button_sizer.Add(self.button_back, 1, wx.ALL | wx.EXPAND | wx.RIGHT, 5)
        self.button_sizer.Add(self.button_next, 1, wx.ALL | wx.EXPAND | wx.RIGHT, 5)

        self.main_vertical_sizer.Add(wx.StaticBitmap(self, wx.ID_ANY, self.logo_image), 0, wx.ALL | wx.EXPAND, 0)
        self.main_vertical_sizer.Add(self.game_path, 0, wx.ALL | wx.EXPAND | wx.CENTRE, 5)
        self.main_vertical_sizer.Add(self.button_sizer, 0, wx.ALL | wx.CENTRE, 5)
        self.SetSizer(self.main_vertical_sizer)
        self.Fit()
        self.Hide()
        self.button_next.Disable()
        self.button_next.Bind(wx.EVT_BUTTON, self.event_next_step)
        self.button_back.Bind(wx.EVT_BUTTON, self.event_prev_step)
        self.search_path_game()

    def search_path_game(self):
        if not os.path.isfile(WGC_DEFAULT_PATH):
            return
        root = et.parse(WGC_DEFAULT_PATH).getroot()
        for subtags in root.find('application').find('games_manager').find('selectedGames'):
            if subtags.tag in ('WOT',):
                self.game_path.SetPath(subtags.text)
                self.button_next.Enable()
                self.set_tooltip(self.button_next, 'Далее')

