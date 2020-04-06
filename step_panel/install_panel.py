import wx

from common.common_utils import open_web_page
from common.constants import SIZE_PANEL
from common.path import MAIN_LOGO_600x100_PATH
from core.cache import g_cache
from core.worked_thread import WorkedThread
from core.panel_template import TemplatePanel
from step_panel.install_backend import InstallScenario


class InstallPanelUi(TemplatePanel):
    def __init__(self, parent, panel_name):
        super(InstallPanelUi, self).__init__(parent, panel_name)
        self.SetSizeHints(minSize=SIZE_PANEL, maxSize=SIZE_PANEL)
        self.logo_image = wx.Bitmap(MAIN_LOGO_600x100_PATH)
        self.main_vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        self.progress_bar = wx.Gauge(self, wx.ID_ANY, style=wx.GA_HORIZONTAL)
        self.logging_window = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_MULTILINE | wx.TE_READONLY, size=(-1, 300))
        self.button_back = wx.Button(self, wx.ID_ANY, self.get_text('exit_button'))
        self.button_youtube = wx.Button(self, wx.ID_ANY, 'Youtube')
        self.button_donate = wx.Button(self, wx.ID_ANY, 'Donate')
        self.event_list = list()
        static_text = wx.StaticText(self, wx.ID_ANY, self.get_text('install_mods'))

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        text_sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, ''), wx.HORIZONTAL)
        text_sizer.Add(static_text, 0, wx.ALL | wx.EXPAND, 5)

        button_sizer.Add(self.button_donate, 1, wx.ALL | wx.EXPAND, 5)
        button_sizer.Add(self.button_youtube, 1, wx.ALL | wx.EXPAND, 5)
        button_sizer.Add(self.button_back, 1, wx.ALL | wx.EXPAND, 5)

        logging_sizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, ''), wx.HORIZONTAL)

        logging_sizer.Add(self.logging_window, 1, wx.ALL | wx.EXPAND, 5)

        self.main_vertical_sizer.Add(wx.StaticBitmap(self, wx.ID_ANY, self.logo_image), 0, wx.ALL | wx.EXPAND, 0)
        self.main_vertical_sizer.Add(text_sizer, 0, wx.ALL | wx.EXPAND, 5)
        self.main_vertical_sizer.Add(self.progress_bar, 0, wx.ALL | wx.EXPAND, 5)
        self.main_vertical_sizer.Add(logging_sizer, 0, wx.ALL | wx.EXPAND, 5)
        self.main_vertical_sizer.Add((0, 0), 1, wx.ALL | wx.EXPAND, 5)
        self.main_vertical_sizer.Add(button_sizer, 0, wx.CENTRE, 5)
        self.button_back.Disable()
        self.SetSizer(self.main_vertical_sizer)
        self.Fit()
        self.Hide()
        self.button_back.Bind(wx.EVT_BUTTON, self.event_close)
        self.button_donate.Bind(wx.EVT_BUTTON, self.event_donate)
        self.button_youtube.Bind(wx.EVT_BUTTON, self.event_youtube)

    def run_install(self):
        mods_panel = self.frame.panel_init_dict['select_mods']
        if not mods_panel.selected_mods_list:
            self.logging_window.AppendText('Модификации для установки не выбраны' + '\n')
            return
        self.check_event()
        self.event_list += mods_panel.selected_mods_list
        self.progress_bar.SetRange(len(self.event_list))
        WorkedThread(InstallScenario, frame=self.frame, install_panel=self, event_list=self.event_list)
        self.event_save_to_cache()

    def event_save_to_cache(self):
        select_clint = self.frame.panel_init_dict['search_game'].game_path.GetStringSelection()
        g_cache.set_to_cache('last_client', select_clint)
        last_mods = self.frame.panel_init_dict['select_mods'].selected_mods_list
        g_cache.set_to_cache('last_mods', last_mods)

    def check_event(self):
        pre_panel = self.frame.panel_init_dict['preparing_client']
        if pre_panel.checkbox_del_mods_cache.GetValue():
            self.event_list.append('del_mods_cache')
        if pre_panel.checkbox_del_game_cache.GetValue():
            self.event_list.append('del_game_cache')
        if pre_panel.checkbox_backup.GetValue():
            self.event_list.append('backup')
        if pre_panel.checkbox_del_old_mods.GetValue():
            self.event_list.append('del_mods')

    def event_close(self, event):
        self.frame.Destroy()
        event.Skip()

    def event_donate(self, event):
        open_web_page('https://unihelp.by/')
        event.Skip()

    def event_youtube(self, event):
        open_web_page('https://www.youtube.com/user/WorldOfTanks')
        event.Skip()
