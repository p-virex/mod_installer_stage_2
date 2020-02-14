import time
from pprint import pprint

import wx
import wx.lib.agw.customtreectrl as CT

from common.constants import g_MODS_CONFIG


class Popupwindow(wx.MiniFrame):

    def __init__(self, mx, my, image_path, description_mod):

        jpg = wx.Image(image_path, wx.BITMAP_TYPE_JPEG).ConvertToBitmap()
        wd = jpg.GetWidth()
        ht = jpg.GetHeight()
        wx.MiniFrame.__init__(self, None, -1, pos=(mx-20, my-20), size=wx.Size(wd + 150, ht + 50), style=wx.MINIMIZE_BOX)
        self.SetBackgroundColour(wx.Colour(252, 254, 214, 255))
        wx.StaticBitmap(self, -1, jpg, (10, 20), (wd, ht))
        wx.StaticText(self, -1, description_mod, (wd + 40, 40))
        self.Show()

class MyCustomTree(CT.CustomTreeCtrl):
    def __init__(self, parent):
        CT.CustomTreeCtrl.__init__(self, parent)
        myCursor = wx.Cursor(wx.CURSOR_HAND)
        self.SetCursor(myCursor)

    def GetCheckedItems(self, itemParent=None, checkedItems=None):
        if itemParent is None:
            itemParent = self.GetRootItem()

        if checkedItems is None:
            checkedItems = []

        child, cookie = self.GetFirstChild(itemParent)

        while child:

            if self.IsItemChecked(child):
                checkedItems.append(child)

            checkedItems = self.GetCheckedItems(child, checkedItems)
            child, cookie = self.GetNextChild(itemParent, cookie)

        return checkedItems


class MyFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "CustomTreeCtrl Demo")
        self.Centre(direction=wx.BOTH)
        self.panel = wx.Panel(self)
        custom_tree = MyCustomTree(self.panel)
        self.custom_tree = custom_tree
        root = custom_tree.AddRoot("Mods selected")
        self.position_list = list()
        self.info_mods_dict = dict()
        self.PW = None
        #     `ct_type` Value Description
        #     0 - A normal item
        #     1 - A checkbox - like item
        #     2 - A radiobutton - type item
        start_pos = 40
        for mods, info_mods in g_MODS_CONFIG.items():
            if isinstance(info_mods, list):
                custom_tree.AppendItem(root, mods, ct_type=1)
                self.position_list.append([mods, [start_pos, start_pos + 20]])
                self.info_mods_dict.update({mods: {'image': info_mods[0], 'hint': info_mods[-1]}})
                start_pos += 20
            if isinstance(info_mods, dict):
                group = custom_tree.AppendItem(root, mods)
                for category_mods, info in info_mods.items():
                    custom_tree.AppendItem(group, category_mods, ct_type=2)
                    self.position_list.append([category_mods, [start_pos, start_pos + 20]])
                    self.info_mods_dict.update({category_mods: {'image': info[0], 'hint': info[-1]}})
                    start_pos += 20

            self.Bind(CT.EVT_TREE_ITEM_CHECKED, self.ItemChecked)
        btn = wx.Button(self.panel, label="Find Checked Items")
        btn.Bind(wx.EVT_BUTTON, self.getCheckedItems)
        custom_tree.ExpandAll()

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(custom_tree, 1, wx.EXPAND)
        sizer.Add(btn, 0, wx.ALL | wx.CENTER, 5)
        self.panel.SetSizer(sizer)
        # custom_tree.Bind(wx.EVT_ENTER_WINDOW, self.OnEnterPanel)
        custom_tree.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeavePanel)
        self.custom_tree.Bind(wx.EVT_MOTION, self.ImageCtrl_OnMouseMove)

    def ImageCtrl_OnMouseMove(self, event):

        ctrl_pos = event.GetPosition()
        pos = self.panel.ScreenToClient(ctrl_pos)
        # print("pos relative to screen top left = ", pos)
        screen_pos = self.custom_tree.GetScreenPosition()
        relative_pos_x = pos[0] + screen_pos[0]
        relative_pos_y = pos[1] + screen_pos[1]
        if all([relative_pos_y > 40, relative_pos_x > 30, relative_pos_x < 200]):
            for item in self.position_list:
                name = item[0]
                start_pos = item[-1][0]
                end_pos = item[-1][-1]
                if all([relative_pos_y > start_pos, relative_pos_y < end_pos]):
                    if self.PW:
                        self.PW.Destroy()
                    self.PW = Popupwindow(relative_pos_x, relative_pos_y, self.info_mods_dict[name]['image'], self.info_mods_dict[name]['hint'])

                    break
        else:
            if self.PW:
                self.PW.Destroy()


        """
        x: 30 y: 40 шаг 40 + 15 pxl
{'pric 1': 40,
 'pric 2': 60,
 'pric 3': 80,
 'А можно вот  так 1': 160,
 'Да хоть два!!!': 260,
 'Да хоть миллион!': 240,
 'Даже не почувствовал': 280,
 'Короче, я адаптивная панель, влезет сколько надо': 300,
 'Мне надоело придумывать': 140,
 'Мод 3': 200,
 'Очень много модов?': 220,
 'Прикольный мод': 120,
 'Удобный мод на каждый день': 100,
 'мод2 2': 180}
        """

    def OnLeavePanel(self, event):
        # destroy the popup window on leaving the red panel
        if self.PW:
            self.PW.Destroy()

    def ItemChecked(self, event):
        print("Somebody checked something")

    # ----------------------------------------------------------------------
    def getCheckedItems(self, event):
        """"""
        # print(self.custom_tree.CalculateSize())
        checked_items = self.custom_tree.GetCheckedItems()
        for item in checked_items:
            print(item.GetText())


if __name__ == '__main__':
    app = wx.App(False)
    frame = MyFrame(None)
    frame.Show()
    app.MainLoop()
