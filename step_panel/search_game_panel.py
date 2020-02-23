import os
import xml.etree.cElementTree as et

import wx

from common.constants import SIZE_PANEL, VERSION_CLIENT
from common.path import MAIN_LOGO_600x100_PATH, WGC_DEFAULT_PATH
from core.logger import logger
from core.panel_template import TemplatePanel


class SearchGamePanelUi(TemplatePanel):
    def __init__(self, parent, panel_name):
        super(SearchGamePanelUi, self).__init__(parent, panel_name)
        self.path_client_set = set()
        self.SetSizeHints(minSize=SIZE_PANEL, maxSize=SIZE_PANEL)
        self.logo_image = wx.Bitmap(MAIN_LOGO_600x100_PATH)
        self.game_path = wx.Choice(self, wx.ID_ANY, choices=[])
        self.button_manual = wx.Button(self, wx.ID_ANY, self.get_text('overview_button'))
        self.button_back = wx.Button(self, wx.ID_ANY, self.get_text('back_button'))
        self.button_next = wx.Button(self, wx.ID_ANY, self.get_text('next_button'))

        static_text = wx.StaticText(self, wx.ID_ANY, self.get_text('select_path_game'))

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
        self.main_vertical_sizer.Add((0, 0), 1, wx.ALL | wx.EXPAND, 5)
        self.main_vertical_sizer.Add(self.button_sizer, 0, wx.CENTRE, 5)
        self.SetSizer(self.main_vertical_sizer)
        self.Fit()
        self.Hide()
        self.button_next.Disable()
        self.button_next.Bind(wx.EVT_BUTTON, self.event_next_step)
        self.button_back.Bind(wx.EVT_BUTTON, self.event_prev_step)
        self.button_manual.Bind(wx.EVT_BUTTON, self.event_select_dir)
        self.search_path_game()

    def event_select_dir(self, event):
        dlg = wx.DirDialog(self, self.get_text('select_dir'), style=wx.DD_DEFAULT_STYLE |
                                                                    wx.DD_DIR_MUST_EXIST |
                                                                    wx.DD_CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            if self.check_mods_dir_version(dlg.GetPath()):
                self.path_client_set.update([dlg.GetPath()])
                self.append_path_in_selector()
                self.game_path.SetSelection(int(self.game_path.GetCount()) - 1)
        dlg.Destroy()
        event.Skip()

    def search_path_game(self):
        if not os.path.isfile(WGC_DEFAULT_PATH):
            return
        root = et.parse(WGC_DEFAULT_PATH).getroot()
        for subtags in root.findall('./application/games_manager/selectedGames/WOT'):
            if self.check_mods_dir_version(subtags.text) and self.check_mods_dir_version(subtags.text):
                self.path_client_set.update([subtags.text])
                self.button_next.Enable()
                logger.info('Game found: {}'.format(subtags.text))
            else:
                logger.error('Game not found!')
                return
        for subtags in root.findall('./application/games_manager/games/game/working_dir'):
            if self.check_mods_dir_version(subtags.text) and self.check_mods_dir_version(subtags.text):
                self.path_client_set.update([subtags.text])
                self.button_next.Enable()
                logger.info('Game found: {}'.format(subtags.text))
        self.append_path_in_selector()
        self.game_path.SetSelection(0)

    def append_path_in_selector(self):
        self.game_path.Clear()
        for path_client in self.path_client_set:
            self.game_path.Append(path_client)

    def check_mods_dir_version(self, path):
        version_xml = os.path.join(path, 'version.xml')
        if not os.path.isfile(version_xml):
            logger.error('File: {} not found!'.format(version_xml))
            return
        root = et.parse(version_xml).getroot()
        for subtags in root.findall('version'):
            if subtags.text.split()[0] == VERSION_CLIENT:
                return True
            else:
                # todo сделать отдельный метод в template_panel
                logger.error(self.get_text('broken_version') % (subtags.text, VERSION_CLIENT))
                wx.MessageBox(self.get_text('broken_version') % (subtags.text, VERSION_CLIENT), 'Warning')
                return
