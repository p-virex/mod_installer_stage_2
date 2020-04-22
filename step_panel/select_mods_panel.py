import wx

from common.constants import SIZE_PANEL
from common.path import MAIN_LOGO_600x100_PATH, PRESET_NAMES, g_MODS_CONFIG, g_PRESET_SETTINGS
from core.cache import g_cache
from core.logger import logger
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
        self.button_back = wx.Button(self, wx.ID_ANY, _('back_button'))
        self.button_next = wx.Button(self, wx.ID_ANY, _('next_button'))
        self.button_next.Disable()
        self.mods_panel = ThreeSelector(self)
        self.choice_stream_settings = wx.Choice(self, wx.ID_ANY, choices=PRESET_NAMES)
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
        # стартовая позиция в pixel, поправка сдвиг высота зоны 1 ячейки
        start_pos, self.shift_pixel = 0, 19
        # рутовая секция, без нее three не будет работать, по сути обязательный рудимент
        root = self.mods_panel.AddRoot('')
        # выбранный пресет для модов

        cache_mods = g_cache.get_from_cache('last_mods')

        select_preset = self.choice_stream_settings.GetStringSelection()
        if cache_mods:
            self.choice_stream_settings.SetSelection(-1)
        for name_mod, info_mods in g_MODS_CONFIG.items():
            if isinstance(info_mods, list):
                item = self.mods_panel.AppendItem(root, name_mod, ct_type=1)
                self.position_list.append([name_mod, [start_pos, start_pos + self.shift_pixel]])
                self.info_mods_dict.update({name_mod: {'image': info_mods[0], 'hint': info_mods[-1]}})
                self.item_three_dict.update({name_mod: item})
                start_pos += self.shift_pixel
                if not cache_mods and name_mod in g_PRESET_SETTINGS.get(select_preset):
                    self.mods_panel.SetItem3StateValue(item, True)
                else:
                    logger.info('{}, caсhe mods: {}'.format(name_mod, cache_mods))
                    if cache_mods and name_mod in cache_mods:
                        self.mods_panel.SetItem3StateValue(item, True)

            if isinstance(info_mods, dict):
                group = self.mods_panel.AppendItem(root, name_mod)
                check_box = 1 if info_mods.get('checkBox') else 2
                start_pos += self.shift_pixel
                for name_mod_, info in info_mods.items():
                    if name_mod_ in ('checkBox',):
                        # используется только как флаг, 1 - check_box, 2 -  radio_button
                        continue
                    item = self.mods_panel.AppendItem(group, name_mod_, ct_type=check_box)
                    self.position_list.append([name_mod_, [start_pos, start_pos + self.shift_pixel]])
                    self.info_mods_dict.update({name_mod_: {'image': info[0], 'hint': info[-1]}})
                    self.item_three_dict.update({name_mod_: item})
                    start_pos += self.shift_pixel
                    if not cache_mods and name_mod_ in g_PRESET_SETTINGS.get(select_preset):
                        # если элемент находится в пресетах, то установить ему выбор
                        self.mods_panel.SetItem3StateValue(item, True)
                    else:
                        logger.info('{}, cache mods: {}'.format(name_mod_, cache_mods))
                        if cache_mods and name_mod_ in cache_mods:
                            self.mods_panel.SetItem3StateValue(item, True)
        # если не развернуть three то тултипы не будут работать правильно
        self.mods_panel.ExpandAll()

    def event_select_preset(self, event):
        """
        Метод вызывается при изменении выбора в селекторе пресетов
        :param event: wx attr
        """
        self.drop_select()
        name_streamer = self.choice_stream_settings.GetStringSelection()
        for name, item in self.item_three_dict.items():
            if name not in g_PRESET_SETTINGS.get(name_streamer):
                continue
            self.mods_panel.SetItem3StateValue(item, True)
        self.enable_button()
        event.Skip()

    def drop_select(self):
        """
        Сброс всех выбранных значений в three
        :return: None
        """
        for item in self.item_three_dict.values():
            self.mods_panel.CheckItem(item, False)

    def show_tooltip_om_mouse_move(self, event):
        """
        Метод определяет координаты курсора и в зависимости от позиции выводит тултип с подсказкой
        :param event: wx attr
        :return: None
        """
        # позиция скролл бара, необходима для внесени поправок если панель прокручена вниз. Это происходит из-за того,
        # что нельзя (или я не нашел) получить фактический размер панели, а только тот который виден в frame
        scroll_pos = self.mods_panel.GetScrollPos(wx.VERTICAL)
        cursor_position = self.ScreenToClient(event.GetPosition())
        # позиция основной панели
        parent_panel_pos = self.GetScreenPosition()
        # расчитываем координаты, в том числе для у с учетом смещения(прокрутки) панели вниз/вверх
        relative_pos_x = cursor_position[0] + parent_panel_pos[0]
        relative_pos_y = cursor_position[1] + parent_panel_pos[1] + (scroll_pos * 10)
        # координаты окна на мониторе
        frame_y, frame_x = self.frame.GetPosition()
        # 45 - ширина в пикселях зоны, в которой необходимо рисовать тултип: 45 - старт > 200 конец
        if all([relative_pos_y > self.shift_pixel, relative_pos_x > 45, relative_pos_x < 200]):
            for item in self.position_list:
                path_image, hint = self.info_mods_dict[item[0]]['image'], self.info_mods_dict[item[0]]['hint']
                start_pos, end_pos = item[-1]  # координаты текста мода
                if all([relative_pos_y > start_pos, relative_pos_y < end_pos]):  # при вхождении рисуем тултип
                    if self.tooltip:
                        self.tooltip.Destroy()
                    self.tooltip = Tooltip(frame_y, frame_x, path_image, hint)
                    break
        else:
            # предпочитаю разрушить в случае если тултип уже есть
            if self.tooltip:
                self.tooltip.Destroy()

    def event_leave_mouse_panel(self, event):
        # destroy the popup window on leaving the mod panel
        if self.tooltip:
            self.tooltip.Destroy()
        event.Skip()

    def event_enable_button(self, event):
        """
        Запускаем этот ивент при любом изменении состояния флажка в three
        """
        self.enable_button()
        event.Skip()

    def enable_button(self):
        """
        Если никакие значения не выбраны, то блокируем кнопку далее.
        """
        if self.mods_panel.get_checked_items():
            self.button_next.Enable()
        else:
            self.button_next.Disable()

    def event_checked_select(self, event):
        """
        Ивент запускается при нажатии Далее и коллекционирует все выбранные флажки, это важно,
        т.к. список используется в следующих шагах
        :param event: wx attr
        """
        self.selected_mods_list = list()
        checked_items = self.mods_panel.get_checked_items()
        approved_mods_panel = self.frame.panel_init_dict['approved_mods']
        # заранее вносим все выбранные моды в следующую панель, что бы избежать лагов
        approved_mods_panel.select_mod_ctrl.Clear()
        for item in checked_items:
            self.selected_mods_list.append(item.GetText())
            approved_mods_panel.select_mod_ctrl.AppendText(item.GetText() + '\n')
        event.Skip()
