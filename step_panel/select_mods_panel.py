import wx

from common.constants import SIZE_PANEL, g_MODS_CONFIG, STREAM_NAMES, g_PRESET_SETTINGS
from common.path import MAIN_LOGO_600x100_PATH
from core.panel_template import TemplatePanel
from core.tooltip import Tooltip
from core.tree_selector import ThreeSelector
import wx.lib.agw.customtreectrl as CT


class SelectModsPanelUi(TemplatePanel):
    def __init__(self, parent, panel_name):
        super(SelectModsPanelUi, self).__init__(parent, panel_name)
        self.tooltip = None
        self.position_list = list()
        self.info_mods_dict = dict()
        self.item_three_dict = dict()
        self.selected_mods_list = list()
        self.SetSizeHints(minSize=SIZE_PANEL, maxSize=SIZE_PANEL)
        self.main_vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # self.button_back = wx.BitmapButton(self, wx.ID_ANY, self.get_convert_bitmap(BACK_BUTTON_PATH))
        # self.button_next = wx.BitmapButton(self, wx.ID_ANY, self.get_convert_bitmap(NEXT_BUTTON_PATH))
        self.button_back = wx.Button(self, wx.ID_ANY, 'Назад')
        self.button_next = wx.Button(self, wx.ID_ANY, 'Далее')
        self.button_next.Disable()
        self.mods_panel = ThreeSelector(self)
        self.choice_stream_settings = wx.Choice(self, wx.ID_ANY, choices=STREAM_NAMES)
        self.choice_stream_settings.SetSelection(0)
        self.button_sizer.Add(self.button_back, 1, wx.ALL | wx.EXPAND | wx.RIGHT, 5)
        self.button_sizer.Add(self.button_next, 1, wx.ALL | wx.EXPAND | wx.RIGHT, 5)
        self.main_vertical_sizer.Add(self.get_static_bitmap(MAIN_LOGO_600x100_PATH), 0, wx.ALL | wx.EXPAND, 0)
        self.main_vertical_sizer.Add(self.choice_stream_settings, 0, wx.ALL | wx.EXPAND, 5)
        self.main_vertical_sizer.Add(self.mods_panel, 1, wx.ALL | wx.EXPAND, 5)
        self.main_vertical_sizer.Add(self.button_sizer, 0, wx.CENTRE, 20)

        self.SetSizer(self.main_vertical_sizer)
        self.Hide()
        self.Fit()
        self.fill_three()
        self.button_next.Bind(wx.EVT_BUTTON, self.event_next_step)
        self.button_back.Bind(wx.EVT_BUTTON, self.event_prev_step)
        self.mods_panel.Bind(wx.EVT_LEAVE_WINDOW, self.event_leave_mouse_panel)
        self.mods_panel.Bind(wx.EVT_MOTION, self.show_tooltip_om_mouse_move)
        self.button_next.Bind(wx.EVT_BUTTON, self.event_checked_select)
        self.button_next.Bind(wx.EVT_BUTTON, self.event_next_step)
        self.button_back.Bind(wx.EVT_BUTTON, self.event_prev_step)
        self.choice_stream_settings.Bind(wx.EVT_CHOICE, self.event_select_preset)
        self.mods_panel.Bind(CT.EVT_TREE_ITEM_CHECKED, self.event_enable_button)
        self.enable_button()

    def fill_three(self):
        start_pos, self.shift_pixel = 0, 19
        root = self.mods_panel.AddRoot('')
        select_preset = self.choice_stream_settings.GetStringSelection()
        for name_mod, info_mods in g_MODS_CONFIG.items():
            if isinstance(info_mods, list):
                item = self.mods_panel.AppendItem(root, name_mod, ct_type=1)
                self.position_list.append([name_mod, [start_pos, start_pos + self.shift_pixel]])
                self.info_mods_dict.update({name_mod: {'image': info_mods[0], 'hint': info_mods[-1]}})
                self.item_three_dict.update({name_mod: item})
                start_pos += self.shift_pixel
                if name_mod in g_PRESET_SETTINGS.get(select_preset):
                    self.mods_panel.SetItem3StateValue(item, True)
            if isinstance(info_mods, dict):
                group = self.mods_panel.AppendItem(root, name_mod)
                check_box = 1 if info_mods.get('checkBox') else 2
                start_pos += self.shift_pixel
                for name_mod_, info in info_mods.items():
                    if name_mod_ in ('checkBox',):
                        continue
                    item = self.mods_panel.AppendItem(group, name_mod_, ct_type=check_box)
                    self.position_list.append([name_mod_, [start_pos, start_pos + self.shift_pixel]])
                    self.info_mods_dict.update({name_mod_: {'image': info[0], 'hint': info[-1]}})
                    self.item_three_dict.update({name_mod_: item})
                    start_pos += self.shift_pixel
                    if name_mod_ in g_PRESET_SETTINGS.get(select_preset):
                        self.mods_panel.SetItem3StateValue(item, True)
        self.mods_panel.ExpandAll()

    def event_select_preset(self, event):
        self.drop_select()
        name_streamer = self.choice_stream_settings.GetStringSelection()
        for name, item in self.item_three_dict.items():
            if name not in g_PRESET_SETTINGS.get(name_streamer):
                continue
            self.mods_panel.SetItem3StateValue(item, True)
        self.enable_button()
        event.Skip()

    def drop_select(self):
        for item in self.item_three_dict.values():
            self.mods_panel.CheckItem(item, False)

    def show_tooltip_om_mouse_move(self, event):
        scroll_pos = self.mods_panel.GetScrollPos(wx.VERTICAL)
        pos_child_panel = self.ScreenToClient(event.GetPosition())
        parent_panel_pos = self.GetScreenPosition()
        relative_pos_x = pos_child_panel[0] + parent_panel_pos[0]
        relative_pos_y = pos_child_panel[1] + parent_panel_pos[1] + (scroll_pos * 10)
        frame_y, frame_x = self.frame.GetPosition()
        if all([relative_pos_y > self.shift_pixel, relative_pos_x > 45, relative_pos_x < 200]):
            for item in self.position_list:
                path_image, hint = self.info_mods_dict[item[0]]['image'], self.info_mods_dict[item[0]]['hint']
                start_pos, end_pos = item[-1]
                if all([relative_pos_y > start_pos, relative_pos_y < end_pos]):
                    if self.tooltip:
                        self.tooltip.Destroy()
                    self.tooltip = Tooltip(frame_y, frame_x, path_image, hint)
                    break
        else:
            if self.tooltip:
                self.tooltip.Destroy()

    def event_leave_mouse_panel(self, event):
        # destroy the popup window on leaving the red panel
        if self.tooltip:
            self.tooltip.Destroy()
        event.Skip()

    def event_enable_button(self, event):
        self.enable_button()
        event.Skip()

    def enable_button(self):
        if self.mods_panel.GetCheckedItems():
            self.button_next.Enable()
        else:
            self.button_next.Disable()

    def event_checked_select(self, event):
        self.selected_mods_list = list()
        checked_items = self.mods_panel.GetCheckedItems()
        approved_mods_panel = self.frame.panel_init_dict['approved_mods']
        approved_mods_panel.select_mod_ctrl.Clear()
        for item in checked_items:
            self.selected_mods_list.append(item.GetText())
            approved_mods_panel.select_mod_ctrl.AppendText(item.GetText() + '\n')
        event.Skip()
