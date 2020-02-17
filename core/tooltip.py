import time

import wx

from common.path import NOT_PATH_DEFAULT


class Tooltip(wx.MiniFrame):

    def __init__(self, mx, my, image_path, description_mod):
        if not image_path:
            image_path = NOT_PATH_DEFAULT
        image = wx.Image(image_path, wx.BITMAP_TYPE_JPEG).ConvertToBitmap()
        wight_image = image.GetWidth()
        height_image = image.GetHeight()
        wx.MiniFrame.__init__(self, None, -1, pos=(mx - height_image, my + 250), size=wx.Size(wight_image, height_image), style=wx.MINIMIZE_BOX)
        self.SetBackgroundColour(wx.Colour(252, 254, 214, 255))
        self.main_vertsizer = wx.BoxSizer(wx.VERTICAL)
        img = wx.StaticBitmap(self, -1, image, (10, 20))
        if not description_mod:
            description_mod = ''
        txt = wx.StaticText(self, -1, description_mod)
        self.main_vertsizer.Add(img)
        self.main_vertsizer.Add(txt)
        self.SetSizer(self.main_vertsizer)
        self.Fit()
        time.sleep(0.1)
        self.Show()
