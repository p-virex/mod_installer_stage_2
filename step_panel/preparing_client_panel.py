import wx

from common.constants import SIZE_PANEL
from common.path import MAIN_LOGO_600x100_PATH
from core.panel_template import TemplatePanel


class PreparingClientPanelUi(TemplatePanel):
    def __init__(self, parent, panel_name):
        super(PreparingClientPanelUi, self).__init__(parent, panel_name)
        self.SetSizeHints(minSize=SIZE_PANEL, maxSize=SIZE_PANEL)
        self.main_vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        self.select_mod_ctrl = wx.TextCtrl(self, wx.ID_ANY, '', style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.button_back = wx.Button(self, wx.ID_ANY, 'Назад')
        self.button_next = wx.Button(self, wx.ID_ANY, 'Далее')
        self.checkbox_del_mods_cache = wx.CheckBox(self, wx.ID_ANY, 'Удалить кеш модификаций')
        self.checkbox_del_game_cache = wx.CheckBox(self, wx.ID_ANY, 'Удалить кеш игры')
        self.checkbox_backup = wx.CheckBox(self, wx.ID_ANY, 'Сделать копию установленных модификаций')
        self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        checkBoxSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, ''), wx.VERTICAL)
        checkBoxSizer.Add(self.checkbox_del_mods_cache, 0, wx.ALL, 5)
        checkBoxSizer.Add(self.checkbox_del_game_cache, 0, wx.ALL, 5)
        checkBoxSizer.Add(self.checkbox_backup, 0, wx.ALL, 5)
        self.button_sizer.Add(self.button_back, 1, wx.ALL | wx.EXPAND | wx.RIGHT, 5)
        self.button_sizer.Add(self.button_next, 1, wx.ALL | wx.EXPAND | wx.RIGHT, 5)
        self.main_vertical_sizer.Add(self.get_static_bitmap(MAIN_LOGO_600x100_PATH), 0, wx.ALL | wx.EXPAND, 0)
        self.main_vertical_sizer.Add(checkBoxSizer, 0, wx.ALL | wx.EXPAND, 5)
        self.main_vertical_sizer.Add((0, 0), 1, wx.ALL | wx.EXPAND, 5)
        self.main_vertical_sizer.Add(self.button_sizer, 0, wx.ALL | wx.CENTRE, 5)
        self.SetSizer(self.main_vertical_sizer)
        self.Hide()
        self.Fit()

        self.button_next.Bind(wx.EVT_BUTTON, self.event_next_step)
        self.button_back.Bind(wx.EVT_BUTTON, self.event_prev_step)
