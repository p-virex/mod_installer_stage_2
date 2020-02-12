import wx
import wx.lib.scrolledpanel

class SimpleFrame(wx.Frame):
    def __init__(self, parent):
        super(SimpleFrame, self).__init__(parent)

        # add a panel so it looks the correct on all platforms
        self.frame_panel = wx.Panel(self)
        frame_panel = self.frame_panel
        # image panel
        self.image_panel = wx.lib.scrolledpanel.ScrolledPanel(frame_panel, style=wx.SIMPLE_BORDER)
        image_panel = self.image_panel
        image_panel.SetAutoLayout(True)
        image_panel.SetupScrolling()
        # image panel - image control
        self.image_ctrl = wx.StaticBitmap(image_panel)
        self.image_ctrl.Bind(wx.EVT_MOTION, self.ImageCtrl_OnMouseMove)
        self.img = wx.Image("download.jpg", wx.BITMAP_TYPE_ANY)
        self.image_ctrl.SetBitmap(wx.BitmapFromImage(self.img))
        image_panel.Layout()
        image_sizer = wx.BoxSizer(wx.VERTICAL)
        image_sizer.Add(self.image_ctrl)
        image_panel.SetSizer(image_sizer)
        # frame sizer
        frame_sizer = wx.BoxSizer(wx.HORIZONTAL)
        frame_sizer.Add(image_panel, proportion=1, flag=wx.EXPAND | wx.ALL)
        frame_panel.SetSizer(frame_sizer)
        return

    def ImageCtrl_OnMouseMove(self, event):
        # position in control
        ctrl_pos = event.GetPosition()
        # print("ctrl_pos: " + str(ctrl_pos.x) + ", " + str(ctrl_pos.y))
        pos = self.image_ctrl.ScreenToClient(ctrl_pos)
        # print ("pos relative to screen top left = ", pos)
        screen_pos = self.frame_panel.GetScreenPosition()
        relative_pos_x = pos[0] + screen_pos[0]
        relative_pos_y = pos[1] + screen_pos[1]
        print ("pos relative to image top left = ", relative_pos_x, relative_pos_y)


app = wx.PySimpleApp()
frame = SimpleFrame(None)
frame.Show()
app.MainLoop()