import wx

from common.constants import TITLE, SIZE_FRAME, FRAME_STYLE, ICON_PATH


class ModsFrame(wx.Frame):
    def __init__(self, panel_info, parent=None):
        super(ModsFrame, self).__init__(parent, wx.ID_ANY, title=TITLE, size=wx.Size(SIZE_FRAME), style=FRAME_STYLE)
        self.SetSizeHints(minSize=SIZE_FRAME, maxSize=SIZE_FRAME)
        self.Centre(direction=wx.BOTH)
        self.SetIcon(wx.Icon(ICON_PATH))
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        self.Bind(wx.EVT_CLOSE, self.on_close_window)
        self.panel_info = panel_info
        self.panel_list = list()
        self.panel_init_dict = dict()
        self.ind_panel = dict()
        self.panel_ind = dict()
        self.registrate_panel()

    def index_panel(self):
        for i, panel_name in enumerate(self.panel_info.keys()):
            self.ind_panel.update({i: panel_name})
            self.panel_ind.update({panel_name: i})

    def init_hide_panel(self):
        for panel_name, self_panel in self.panel_info.items():
            self_panel.Hide()
        self.panel_init_dict['greeting'].Show()

    def registrate_panel(self):
        for panel_name, self_panel in self.panel_info.items():
            panel_init = self_panel(self, panel_name)
            self.panel_list.append(panel_init)
            self.panel_init_dict.update({panel_name: panel_init})
        self.index_panel()

    def switch_panel(self, show_panel):
        if not show_panel or show_panel.IsShown():
            return
        for panel in self.panel_list:
            if panel.IsShown():
                show_panel.Show()
                show_panel.Layout()
                panel.Hide()
                break
        self.Layout()

    def on_close_window_not_event(self):
        self.Destroy()

    def on_close_window(self, event):
        self.on_close_window_not_event()
        event.Skip()
