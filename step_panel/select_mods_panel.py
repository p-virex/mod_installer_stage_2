import wx

from common.constants import MAIN_LOGO_600x100_PATH, SIZE_PANEL, NEXT_BUTTON_PATH, BACK_BUTTON_PATH, MODS_CONFIG
import wx.lib.agw.customtreectrl as CT
from core.panel_template import TemplatePanel
from core.tooltip import Tooltip
from core.tree_selector import ThreeSelector


class SelectModsPanelUi(TemplatePanel):
    def __init__(self, parent, panel_name):
        super(SelectModsPanelUi, self).__init__(parent, panel_name)
        self.position_list = list()
        self.info_mods_dict = dict()
        self.PW = None
        self.SetSizeHints(minSize=SIZE_PANEL, maxSize=SIZE_PANEL)
        self.logo_image = wx.Bitmap(MAIN_LOGO_600x100_PATH)
        self.main_vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        bmp_back = wx.Image(BACK_BUTTON_PATH, wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        bmp_next = wx.Image(NEXT_BUTTON_PATH, wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        self.button_back = wx.BitmapButton(self, wx.ID_ANY, bmp_back)
        self.button_next = wx.BitmapButton(self, wx.ID_ANY, bmp_next)
        self.mods_panel = ThreeSelector(self)
        self.button_sizer.Add(self.button_back, 1, wx.ALL | wx.EXPAND | wx.RIGHT, 5)
        self.button_sizer.Add(self.button_next, 1, wx.ALL | wx.EXPAND | wx.RIGHT, 5)

        self.hor_sel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.hor_sel_sizer.Add(self.mods_panel, 1,  wx.ALL | wx.EXPAND, 5)
        self.main_vertical_sizer.Add(wx.StaticBitmap(self, wx.ID_ANY, self.logo_image), 0, wx.ALL | wx.EXPAND, 0)
        self.main_vertical_sizer.Add(self.hor_sel_sizer, 1, wx.ALL | wx.EXPAND, 5)
        self.main_vertical_sizer.Add(self.button_sizer, 0, wx.CENTRE, 5)

        self.SetSizer(self.main_vertical_sizer)
        self.Hide()
        self.Fit()
        start_pos = 40
        root = self.mods_panel.AddRoot("Mods selected")
        for mods, info_mods in MODS_CONFIG.items():
            if isinstance(info_mods, list):
                self.mods_panel.AppendItem(root, mods, ct_type=1)
                self.position_list.append([mods, [start_pos, start_pos + 20]])
                self.info_mods_dict.update({mods: {'image': info_mods[0], 'hint': info_mods[-1]}})
                start_pos += 20
            if isinstance(info_mods, dict):
                group = self.mods_panel.AppendItem(root, mods)
                for category_mods, info in info_mods.items():
                    self.mods_panel.AppendItem(group, category_mods, ct_type=2)
                    self.position_list.append([category_mods, [start_pos, start_pos + 20]])
                    self.info_mods_dict.update({category_mods: {'image': info[0], 'hint': info[-1]}})
                    start_pos += 20
        self.mods_panel.ExpandAll()
        self.button_next.Bind(wx.EVT_BUTTON, self.event_next_step)
        self.button_back.Bind(wx.EVT_BUTTON, self.event_prev_step)
        self.Layout()
        self.mods_panel.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeavePanel)
        self.mods_panel.Bind(wx.EVT_MOTION, self.ImageCtrl_OnMouseMove)
        print(self.info_mods_dict)
    def ImageCtrl_OnMouseMove(self, event):

        ctrl_pos = event.GetPosition()
        pos = self.ScreenToClient(ctrl_pos)
        # print("pos relative to screen top left = ", pos)
        screen_pos = self.mods_panel.GetScreenPosition()
        relative_pos_x = pos[0] + screen_pos[0]
        relative_pos_y = pos[1] + screen_pos[1]
        if all([relative_pos_y > 40, relative_pos_x > 30, relative_pos_x < 200]):
            for item in self.position_list:
                name = item[0]
                start_pos = item[-1][0]
                end_pos = item[-1][-1]
                if all([relative_pos_y > start_pos, relative_pos_y < end_pos]):
                    print(name, relative_pos_y)
                    if self.PW:
                        self.PW.Destroy()
                    self.PW = Tooltip(relative_pos_x, relative_pos_y, self.info_mods_dict[name]['image'],
                                          self.info_mods_dict[name]['hint'])

                    break
        else:
            if self.PW:
                self.PW.Destroy()

    def ItemChecked(self, event):
        print("Somebody checked something")

    def OnLeavePanel(self, event):
        # destroy the popup window on leaving the red panel
        if self.PW:
            self.PW.Destroy()
