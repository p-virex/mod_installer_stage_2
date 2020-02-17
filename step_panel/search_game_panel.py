import os
import xml.etree.cElementTree as et

import wx

from common.constants import SIZE_PANEL, VERSION_CLIENT
from common.path import MAIN_LOGO_600x100_PATH, NEXT_BUTTON_PATH, BACK_BUTTON_PATH, WGC_DEFAULT_PATH
from core.panel_template import TemplatePanel


class SearchGamePanelUi(TemplatePanel):
    def __init__(self, parent, panel_name):
        super(SearchGamePanelUi, self).__init__(parent, panel_name)
        self.SetSizeHints(minSize=SIZE_PANEL, maxSize=SIZE_PANEL)
        self.logo_image = wx.Bitmap(MAIN_LOGO_600x100_PATH)
        # bmp_back = wx.Image(BACK_BUTTON_PATH, wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        # bmp_next = wx.Image(NEXT_BUTTON_PATH, wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        # self.button_back = wx.BitmapButton(self, wx.ID_ANY, bmp_back)
        # self.button_next = wx.BitmapButton(self, wx.ID_ANY, bmp_next)
        self.game_path = wx.Choice(self, wx.ID_ANY, choices=[])
        self.button_manual = wx.Button(self, wx.ID_ANY, 'Обзор')
        self.button_back = wx.Button(self, wx.ID_ANY, 'Назад')
        self.button_next = wx.Button(self, wx.ID_ANY, 'Далее')

        static_text = wx.StaticText(self, wx.ID_ANY,
                                    'Для продолжения установки выберите путь до папки с игрой или нажмите Далее')

        self.main_vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.path_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.text_sizer = wx.StaticBoxSizer(wx.StaticBox(self, -1, ''), wx.VERTICAL)
        self.button_sizer.Add(self.button_back, 1, wx.ALL | wx.EXPAND, 5)
        self.button_sizer.Add(self.button_next, 1, wx.ALL | wx.EXPAND, 5)
        self.path_sizer.Add(self.game_path, 1, wx.ALL | wx.EXPAND, 5)
        self.path_sizer.Add(self.button_manual, 0, wx.ALL | wx.EXPAND, 5)
        self.text_sizer.Add(static_text, 1, wx.CENTRE, 5)
        self.main_vertical_sizer.Add(wx.StaticBitmap(self, wx.ID_ANY, self.logo_image), 0, wx.ALL | wx.EXPAND, 0)
        self.main_vertical_sizer.Add(self.text_sizer, 0, wx.ALL | wx.EXPAND, 5)
        self.main_vertical_sizer.Add(self.path_sizer, 0, wx.ALL | wx.EXPAND | wx.CENTRE, 5)
        self.main_vertical_sizer.Add((0, 0), 1, wx.ALL | wx.EXPAND | wx.CENTRE, 5)
        self.main_vertical_sizer.Add(self.button_sizer, 0, wx.ALL | wx.CENTRE | wx.DOWN, 5)
        self.SetSizer(self.main_vertical_sizer)
        self.Fit()
        self.Hide()
        self.button_next.Disable()
        self.button_next.Bind(wx.EVT_BUTTON, self.event_next_step)
        self.button_back.Bind(wx.EVT_BUTTON, self.event_prev_step)
        self.button_manual.Bind(wx.EVT_BUTTON, self.event_select_dir)
        self.search_path_game()

    def event_select_dir(self, event):
        """
        Show the DirDialog and print the user's choice to stdout
        """
        dlg = wx.DirDialog(self, "Choose a directory:", style=wx.DD_DEFAULT_STYLE |
                                                              wx.DD_DIR_MUST_EXIST |
                                                              wx.DD_CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            if self.checkModsDirVersion(dlg.GetPath()):
                self.game_path.Append(dlg.GetPath())
                self.game_path.SetSelection(int(self.game_path.GetCount()) - 1)
            else:
                wx.MessageBox('По указанному пути игровой клиент не найден')
        dlg.Destroy()

    def search_path_game(self):
        if not os.path.isfile(WGC_DEFAULT_PATH):
            return
        root = et.parse(WGC_DEFAULT_PATH).getroot()
        for subtags in root.findall('./application/games_manager/selectedGames/WOT'):
            if self.checkModsDirVersion(subtags.text):
                self.game_path.Append(subtags.text)
                self.button_next.Enable()
                self.checkModsDirVersion(subtags.text)
        for subtags in root.findall('./application/games_manager/games/game/working_dir'):
            if self.checkModsDirVersion(subtags.text):
                self.game_path.Append(subtags.text)
                self.button_next.Enable()
                self.checkModsDirVersion(subtags.text)
        self.game_path.SetSelection(0)

    @staticmethod
    def checkModsDirVersion(path):
        version_xml = os.path.join(path, 'version.xml')
        if not os.path.isfile(version_xml):
            return
        root = et.parse(version_xml).getroot()
        for subtags in root.findall('version'):
            if subtags.text.split()[0] == VERSION_CLIENT:
                return True
            else:
                return
