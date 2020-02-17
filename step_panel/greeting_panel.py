import wx

from common.constants import SIZE_PANEL
from common.path import MAIN_LOGO_600x500_PATH, BACK_BUTTON_PATH, NEXT_BUTTON_PATH
from core.panel_template import TemplatePanel


class GreetingPanelUi(TemplatePanel):
    def __init__(self, parent, panel_name):
        super(GreetingPanelUi, self).__init__(parent, panel_name)
        self.SetSizeHints(minSize=SIZE_PANEL)

        self.logo_image = wx.Bitmap(MAIN_LOGO_600x500_PATH)

        # bmp_back = wx.Image(BACK_BUTTON_PATH, wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        # bmp_next = wx.Image(NEXT_BUTTON_PATH, wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        # self.button_back = wx.BitmapButton(self, wx.ID_ANY, bmp_back)
        # self.button_next = wx.BitmapButton(self, wx.ID_ANY, bmp_next)

        self.button_back = wx.Button(self, wx.ID_ANY, 'Выход')
        self.button_next = wx.Button(self, wx.ID_ANY, 'Далее')
        text = """Вас приветствует программа установки модификаций Sharewax. Здесь собраны лучшие\nмодификации специально для Вас. Для продолжения работа, нажмите кнопку Далее или кнопку\nВыход для выхода из программы установки"""
        staticText = wx.StaticText(self, wx.ID_ANY, text, style=wx.ALIGN_LEFT)
        self.main_vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        textSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, ''), wx.HORIZONTAL)
        self.button_sizer.Add(self.button_back, 1, wx.ALL | wx.EXPAND | wx.RIGHT, 5)
        self.button_sizer.Add(self.button_next, 1, wx.ALL | wx.EXPAND | wx.RIGHT, 5)
        textSizer.Add(staticText, 0, wx.CENTRE, 5)

        self.main_vertical_sizer.Add(wx.StaticBitmap(self, wx.ID_ANY, self.logo_image), 0, wx.ALL | wx.EXPAND, 0)
        self.main_vertical_sizer.Add(textSizer, 0, wx.ALL | wx.EXPAND, 5)
        self.main_vertical_sizer.Add(self.button_sizer, 0, wx.ALL | wx.CENTRE, 5)
        self.SetSizer(self.main_vertical_sizer)
        self.Show()
        self.Fit()
        self.button_next.Bind(wx.EVT_BUTTON, self.event_next_step)
        self.button_back.Bind(wx.EVT_BUTTON, self.event_prev_step)
