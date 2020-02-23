import wx

from common.constants import SIZE_PANEL
from common.path import MAIN_LOGO_600x100_PATH
from core.panel_template import TemplatePanel


class ChoiceApprovedPanelUi(TemplatePanel):
    def __init__(self, parent, panel_name):
        super(ChoiceApprovedPanelUi, self).__init__(parent, panel_name)
        self.SetSizeHints(minSize=SIZE_PANEL, maxSize=SIZE_PANEL)
        self.main_vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        self.select_mod_ctrl = wx.TextCtrl(self, wx.ID_ANY, '', style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.button_back = wx.Button(self, wx.ID_ANY, self.get_text('back_button'))
        self.button_next = wx.Button(self, wx.ID_ANY, self.get_text('next_button'))
        self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        staticText = wx.StaticText(self, wx.ID_ANY, self.get_text('choice_approved'))
        textSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, ''), wx.HORIZONTAL)
        textSizer.Add(staticText, 0,  wx.ALL | wx.EXPAND, 5)
        self.button_sizer.Add(self.button_back, 1, wx.ALL | wx.EXPAND | wx.RIGHT, 5)
        self.button_sizer.Add(self.button_next, 1, wx.ALL | wx.EXPAND | wx.RIGHT, 5)
        self.main_vertical_sizer.Add(self.get_static_bitmap(MAIN_LOGO_600x100_PATH), 0, wx.ALL | wx.EXPAND, 0)
        self.main_vertical_sizer.Add(textSizer, 0, wx.ALL | wx.EXPAND, 5)
        self.main_vertical_sizer.Add(self.select_mod_ctrl, 1, wx.ALL | wx.EXPAND, 5)
        self.main_vertical_sizer.Add(self.button_sizer, 0, wx.ALL | wx.CENTRE, 5)
        self.SetSizer(self.main_vertical_sizer)
        self.Hide()
        self.Fit()

        self.button_next.Bind(wx.EVT_BUTTON, self.event_next_step)
        self.button_back.Bind(wx.EVT_BUTTON, self.event_prev_step)

    def fill_mods(self):
        select_mods_panel = self.frame.panel_init_dict['select_mods']
        for mods in select_mods_panel.selected_mods_list:
            self.select_mod_ctrl.AppendText(mods + '\n')
