from collections import OrderedDict

import wx

from core.frame import ModsFrame
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

if __name__ == '__main__':
    app = wx.App(False)
    frame = ModsFrame(PANEL_INFO)
    frame.Show(True)
    frame.SetFocus()
    app.MainLoop()
