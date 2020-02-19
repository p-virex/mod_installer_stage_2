import gettext
import os

import wx

from common.common_utils import resource_path


class TemplatePanel(wx.Panel):
    def __init__(self, parent, panel_name):
        super(TemplatePanel, self).__init__(parent)
        self.set_language()
        self.frame = parent
        self.panel_name = panel_name
        self.Hide()

    @staticmethod
    def set_language():
        os.environ["LANGUAGE"] = "{}.UTF-8".format('RU')
        gettext.bindtextdomain('{}'.format('RU').lower(), resource_path('locales'))
        gettext.textdomain('{}'.format('RU').lower())

    def event_next_step(self, event):
        current_panel_ind = self.frame.panel_ind.get(self.panel_name)
        next_panel_ind = self.frame.ind_panel.get(current_panel_ind + 1)
        self.frame.switch_panel(self.frame.panel_init_dict.get(next_panel_ind))
        event.Skip()

    def event_prev_step(self, event):
        current_panel_ind = self.frame.panel_ind.get(self.panel_name)
        prev_panel_name = self.frame.ind_panel.get(current_panel_ind - 1)
        prev_panel_ind = self.frame.panel_ind.get(prev_panel_name, -1)
        if not prev_panel_name or prev_panel_ind < 0:
            self.frame.Destroy()
        self.frame.switch_panel(self.frame.panel_init_dict.get(prev_panel_name))
        event.Skip()

    @staticmethod
    def set_tooltip(item, text):
        item.SetToolTip(wx.ToolTip(text))

    @staticmethod
    def get_convert_bitmap(image_path):
        return wx.Image(image_path, wx.BITMAP_TYPE_BMP).ConvertToBitmap()

    def get_static_bitmap(self, path_image):
        return wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(path_image))

    @staticmethod
    def get_text(key):
        return gettext.gettext(key)
