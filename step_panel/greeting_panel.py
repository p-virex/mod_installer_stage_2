import wx

from common.constants import SIZE_PANEL
from common.path import MAIN_LOGO_600x500_PATH
from core.panel_template import TemplatePanel


class GreetingPanelUi(TemplatePanel):
    def __init__(self, parent, panel_name):
        super(GreetingPanelUi, self).__init__(parent, panel_name)
        self.SetSizeHints(minSize=SIZE_PANEL, maxSize=SIZE_PANEL)

        self.logo_image = wx.Bitmap(MAIN_LOGO_600x500_PATH)
        self.button_back = wx.Button(self, wx.ID_ANY, self.get_text('exit_button'))
        self.button_next = wx.Button(self, wx.ID_ANY, self.get_text('next_button'))
        static_text = wx.StaticText(self, wx.ID_ANY, self.get_text('greeting'))
        self.main_vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        text_sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, ''), wx.HORIZONTAL)
        self.button_sizer.Add(self.button_back, 1, wx.ALL | wx.EXPAND, 5)
        self.button_sizer.Add(self.button_next, 1, wx.ALL | wx.EXPAND, 5)
        text_sizer.Add(static_text, 0, wx.ALL | wx.EXPAND, 5)

        self.main_vertical_sizer.Add(wx.StaticBitmap(self, wx.ID_ANY, self.logo_image), 0, wx.ALL | wx.EXPAND, 0)
        self.main_vertical_sizer.Add(text_sizer, 0, wx.ALL | wx.EXPAND, 5)
        self.main_vertical_sizer.Add((0, 0), 0, wx.ALL | wx.EXPAND, 5)
        self.main_vertical_sizer.Add(self.button_sizer, 1, wx.ALL | wx.CENTRE, 0)
        self.SetSizer(self.main_vertical_sizer)
        self.Show()
        self.Fit()
        self.button_next.Bind(wx.EVT_BUTTON, self.event_next_step)
        self.button_back.Bind(wx.EVT_BUTTON, self.event_prev_step)
