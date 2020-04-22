import os

import wx

from common.constants import SIZE_PANEL
from common.path import MAIN_LOGO_600x100_PATH
from core.panel_template import TemplatePanel


class PreparingClientPanelUi(TemplatePanel):
    def __init__(self, parent, panel_name):
        super(PreparingClientPanelUi, self).__init__(parent, panel_name)
        self.SetSizeHints(minSize=SIZE_PANEL, maxSize=SIZE_PANEL)
        self.main_vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        self.button_back = wx.Button(self, wx.ID_ANY, _('back_button'))
        self.button_next = wx.Button(self, wx.ID_ANY, _('next_button'))
        self.checkbox_del_mods_cache = wx.CheckBox(self, wx.ID_ANY, _('mods_del_cache'))
        self.checkbox_del_mods_cache.SetValue(True)
        self.checkbox_del_game_cache = wx.CheckBox(self, wx.ID_ANY, _('game_del_cache'))
        self.checkbox_backup = wx.CheckBox(self, wx.ID_ANY, _('backup_mods'))
        self.checkbox_del_old_mods = wx.CheckBox(self, wx.ID_ANY, _('del_mods'))
        self.checkbox_del_old_mods.SetValue(True)

        checkbox_fine = wx.CheckBox(self, wx.ID_ANY, _('fine'))
        static_text = wx.StaticText(self, wx.ID_ANY, _('preparing'))
        checkbox_fine.SetValue(True)
        self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        text_sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, ''), wx.HORIZONTAL)
        check_box_sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, ''), wx.VERTICAL)
        check_box_sizer.Add(self.checkbox_del_old_mods, 0, wx.ALL, 5)
        check_box_sizer.Add(self.checkbox_del_mods_cache, 0, wx.ALL, 5)
        check_box_sizer.Add(self.checkbox_del_game_cache, 0, wx.ALL, 5)
        check_box_sizer.Add(self.checkbox_backup, 0, wx.ALL, 5)
        check_box_sizer.Add(checkbox_fine, 0, wx.ALL, 5)
        text_sizer.Add(static_text, 0, wx.ALL, 5)
        self.button_sizer.Add(self.button_back, 1, wx.ALL | wx.EXPAND | wx.RIGHT, 5)
        self.button_sizer.Add(self.button_next, 1, wx.ALL | wx.EXPAND | wx.RIGHT, 5)
        self.main_vertical_sizer.Add(self.get_static_bitmap(MAIN_LOGO_600x100_PATH), 0, wx.ALL | wx.EXPAND, 0)
        self.main_vertical_sizer.Add(text_sizer, 0, wx.ALL | wx.EXPAND, 5)
        self.main_vertical_sizer.Add(check_box_sizer, 0, wx.ALL | wx.EXPAND, 5)
        self.main_vertical_sizer.Add((0, 0), 1, wx.ALL | wx.EXPAND, 5)
        self.main_vertical_sizer.Add(self.button_sizer, 0, wx.ALL | wx.CENTRE, 5)
        self.SetSizer(self.main_vertical_sizer)
        self.Hide()
        self.Fit()

        self.button_next.Bind(wx.EVT_BUTTON, self.event_next_step)
        self.button_next.Bind(wx.EVT_BUTTON, self.init_run_install)
        self.button_back.Bind(wx.EVT_BUTTON, self.event_prev_step)

    def init_run_install(self, event):
        self.frame.panel_init_dict['install'].run_install()
        event.Skip()
