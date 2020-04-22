import os

import wx
import builtins
import gettext

from common.common_utils import resource_path
from common.constants import DEFAULT_LANG
from core.cache import g_cache
from core.frame import ModsFrame
from core.language_dialog import SelectLanguageDialog
from core.logger import logger
from step_panel.choice_approved_panel import ChoiceApprovedPanelUi
from step_panel.greeting_panel import GreetingPanelUi
from step_panel.install_panel import InstallPanelUi
from step_panel.preparing_client_panel import PreparingClientPanelUi
from step_panel.search_game_panel import SearchGamePanelUi
from step_panel.select_mods_panel import SelectModsPanelUi

PANEL_INFO = {
    'greeting': GreetingPanelUi,
    'search_game': SearchGamePanelUi,
    'select_mods': SelectModsPanelUi,
    'approved_mods': ChoiceApprovedPanelUi,
    'preparing_client': PreparingClientPanelUi,
    'install': InstallPanelUi
}

LANGUAGE = None


def get_text(key):
    """
    Получить текст по ключу.
    :param key: ключ
    """
    msg = gettext.gettext(key)
    if key == msg:
        logger.warning('%s key not found in locale' % key)
    return msg


def set_language():
    """
    Метод устанавливает язык, на даыннй момент по деволту только RU
    """
    LANG = DEFAULT_LANG if not LANGUAGE else LANGUAGE
    os.environ["LANGUAGE"] = "{}.UTF-8".format(LANG)
    gettext.bindtextdomain('{}'.format(LANG).lower(), resource_path('locales'))
    gettext.textdomain('{}'.format(LANG).lower())


def start_main_frame():
    set_language()
    frame = ModsFrame(PANEL_INFO)
    frame.Show(True)
    frame.SetFocus()


builtins.__dict__['_'] = get_text

if __name__ == '__main__':
    app = wx.App(False)
    language = g_cache.get_from_cache('language')
    if not language:
        language_dialog = SelectLanguageDialog(None)
        language_dialog.Show(True)
        app.MainLoop()
        if not language_dialog.init:
            LANGUAGE = language_dialog.lang
            g_cache.set_to_cache('language', language_dialog.lang)
            start_main_frame()
            app.MainLoop()
    else:
        LANGUAGE = language
        start_main_frame()
        app.MainLoop()
