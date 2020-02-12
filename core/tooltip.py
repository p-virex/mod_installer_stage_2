import wx


class Tooltip(wx.MiniFrame):

    def __init__(self, mx, my, image_path, description_mod):
        print(image_path)
        image = wx.Image(image_path, wx.BITMAP_TYPE_JPEG).ConvertToBitmap()
        wight_image = image.GetWidth()
        height_image = image.GetHeight()
        wx.MiniFrame.__init__(self, None, -1, pos=(mx-20, my-20),
                              size=wx.Size(wight_image + 150, height_image + 10), style=wx.MINIMIZE_BOX)
        self.SetBackgroundColour(wx.Colour(252, 254, 214, 255))
        wx.StaticBitmap(self, -1, image, (10, 20), (wight_image, height_image))
        wx.StaticText(self, -1, description_mod, (wight_image + 40, 40))
        self.Show()
