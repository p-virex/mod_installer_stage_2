import wx

from common.constants import SELECT_LANG


class SelectLanguageDialog(wx.Dialog):
    def __init__(self, parent, id=wx.ID_ANY, title="", pos=wx.DefaultPosition,
                 size=(200, 180), style=wx.TAB_TRAVERSAL | wx.BORDER):
        wx.Dialog.__init__(self, parent, id, title, pos, size, style)
        self.SetSizeHints(minSize=(200, 180), maxSize=(200, 180))
        self.Centre(direction=wx.BOTH)
        self.init = True
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        self.text = wx.StaticText(self, wx.ID_ANY, 'Выберите язык\nSelect language')
        self.choice = wx.Choice(self, wx.ID_ANY, choices=SELECT_LANG)
        self.choice.SetSelection(0)
        self.button_ok = wx.Button(self, wx.ID_ANY, 'Ok')
        self.button_cancel = wx.Button(self, wx.ID_EXIT)
        vertical_sizer.Add(self.text, 0, wx.CENTER | wx.ALL, 5)
        vertical_sizer.Add(self.choice, 0, wx.EXPAND | wx.ALL, 5)
        vertical_sizer.Add(self.button_ok, 0, wx.EXPAND | wx.ALL, 5)
        vertical_sizer.Add(self.button_cancel, 0, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(vertical_sizer, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(main_sizer)
        main_sizer.Layout()
        self.button_ok.Bind(wx.EVT_BUTTON, self.start)
        self.button_cancel.Bind(wx.EVT_BUTTON, self.cancel)

    def start(self, event):
        self.init = False
        self.lang = self.choice.GetStringSelection()
        self.Destroy()

    def cancel(self, event):
        self.Destroy()
