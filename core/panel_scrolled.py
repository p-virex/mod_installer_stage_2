import wx
import wx.lib.scrolledpanel as scrolled

from common.constants import g_MODS_CONFIG


class BaseScrolledPanel(scrolled.ScrolledPanel):
    def __init__(self, parent):
        scrolled.ScrolledPanel.__init__(self, parent, -1)
        self.SetSize(600, 400)
        self.SetBackgroundColour(wx.WHITE)
        self.vertical_box = wx.BoxSizer(wx.VERTICAL)

        for name_mods, mods in g_MODS_CONFIG.items():
            # self.vertical_box.Add(wx.StaticText(self, -1, name_mods), 0, wx.ALL, 5)
            if isinstance(mods, dict):
                fill_mods(self, mods, name=name_mods)
        self.SetSizer(self.vertical_box)
        self.SetupScrolling()


def fill_mods(panel, mods, name=None, border=0):
    if name:
        panel.vertical_box.Add(wx.StaticText(panel, -1, name), 0, wx.ALL, 5)
    for name_mod, path_mod in mods.items():
        temp_sizer = wx.BoxSizer(wx.HORIZONTAL)
        temp_sizer.Add((0, 0), 0, wx.ALL, 10)
        temp_sizer.Add((0, 0), 0, wx.ALL, 10)
        temp_sizer.Add((0, 0), 0, wx.ALL, 10)
        if border:
            temp_sizer.Add((0, 0), 0, wx.ALL, 10)
        temp_sizer.Add(wx.CheckBox(panel, -1, name_mod.encode('utf-8')), 1, wx.ALL, 5)
        panel.vertical_box.Add(temp_sizer)
        if isinstance(path_mod, dict):
            fill_mods(panel, path_mod, border=1)
