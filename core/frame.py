import os
import gettext

import wx

from common.common_utils import resource_path
from common.constants import TITLE, SIZE_FRAME, FRAME_STYLE, DEFAULT_LANG
from common.path import ICON_PATH
from core.logger import logger


class ModsFrame(wx.Frame):
    def __init__(self, panel_info, parent=None):
        super(ModsFrame, self).__init__(parent, wx.ID_ANY, title=TITLE, size=wx.Size(SIZE_FRAME), style=FRAME_STYLE)
        # self.set_language()
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

    @staticmethod
    def set_language():
        """
        Метод устанавливает язык, на даыннй момент по деволту только RU
        """
        logger.info('Set language: {}'.format(DEFAULT_LANG))
        os.environ["LANGUAGE"] = "{}.UTF-8".format(DEFAULT_LANG)
        gettext.bindtextdomain('{}'.format(DEFAULT_LANG).lower(), resource_path('locales'))
        gettext.textdomain('{}'.format(DEFAULT_LANG).lower())

    def index_panel(self):
        """
        Выполняет индексацию панелей, используется для по-шагового переключения кнопками Назад или Далее.
        Создаем 2 словаря:
        {index: name_panel}
        {name_panel: index}
        """
        for i, panel_name in enumerate(self.panel_info.keys()):
            self.ind_panel.update({i: panel_name})
            self.panel_ind.update({panel_name: i})

    def init_hide_panel(self):
        """
        Скрываем все панели, оторажаем только панель приветствия.
        """
        for panel_name, self_panel in self.panel_info.items():
            self_panel.Hide()
        self.panel_init_dict['greeting'].Show()

    def registrate_panel(self):
        """
        Метод осуществляет инициализацию и регистрацию панелей.
        """
        for panel_name, self_panel in self.panel_info.items():
            panel_init = self_panel(self, panel_name)
            self.panel_list.append(panel_init)
            self.panel_init_dict.update({panel_name: panel_init})
        self.index_panel()

    def switch_panel(self, show_panel):
        """
        Метод переключает панель на приходящую и скрывает предыдущую.
        :param show_panel: панель которую необходимо отобразить
        """
        if not show_panel or show_panel.IsShown():
            logger.info('Shown panel {} not found!'.format(show_panel))
            return
        for panel in self.panel_list:
            if panel.IsShown():
                logger.info('Panel: "{}" shown'.format(show_panel.panel_name))
                show_panel.Show()
                show_panel.Layout()
                panel.Hide()
                break
        self.Layout()

    def on_close_window_not_event(self):
        logger.info('App closed')
        self.Destroy()

    def on_close_window(self, event):
        self.on_close_window_not_event()
        event.Skip()
