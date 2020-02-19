import wx

from common.constants import SIZE_PANEL
from common.path import MAIN_LOGO_600x100_PATH
from core.panel_template import TemplatePanel


class InstallPanelUi(TemplatePanel):
    def __init__(self, parent, panel_name):
        super(InstallPanelUi, self).__init__(parent, panel_name)
        self.SetSizeHints(minSize=SIZE_PANEL, maxSize=SIZE_PANEL)
        self.logo_image = wx.Bitmap(MAIN_LOGO_600x100_PATH)
        self.main_vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        self.progress_bar = wx.Gauge(self, wx.ID_ANY, style=wx.GA_HORIZONTAL)
        self.button_back = wx.Button(self, wx.ID_ANY, self.get_text('exit_button'))
        self.button_youtube = wx.Button(self, wx.ID_ANY, 'Youtube')
        self.button_donate = wx.Button(self, wx.ID_ANY, 'Donate')

        static_text = wx.StaticText(self, wx.ID_ANY, self.get_text('install_mods'))

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        text_sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, ''), wx.HORIZONTAL)
        text_sizer.Add(static_text, 0, wx.ALL | wx.EXPAND, 5)

        button_sizer.Add(self.button_donate, 1, wx.ALL | wx.EXPAND, 5)
        button_sizer.Add(self.button_youtube, 1, wx.ALL | wx.EXPAND, 5)
        button_sizer.Add(self.button_back, 1, wx.ALL | wx.EXPAND, 5)

        self.main_vertical_sizer.Add(wx.StaticBitmap(self, wx.ID_ANY, self.logo_image), 0, wx.ALL | wx.EXPAND, 0)
        self.main_vertical_sizer.Add(text_sizer, 0, wx.ALL | wx.EXPAND, 5)
        self.main_vertical_sizer.Add(self.progress_bar, 0, wx.ALL | wx.EXPAND, 5)
        self.main_vertical_sizer.Add((0, 0), 1, wx.ALL | wx.EXPAND, 5)
        self.main_vertical_sizer.Add(button_sizer, 0, wx.CENTRE, 5)
        self.button_back.Disable()
        self.SetSizer(self.main_vertical_sizer)
        self.Fit()
        self.Hide()
