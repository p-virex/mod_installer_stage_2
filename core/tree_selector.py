import wx
import wx.lib.agw.customtreectrl


class ThreeSelector(wx.lib.agw.customtreectrl.CustomTreeCtrl):
    def __init__(self, parent):
        frame_styles = wx.TR_HIDE_ROOT | wx.TR_MULTIPLE | wx.TR_LINES_AT_ROOT
        wx.lib.agw.customtreectrl.CustomTreeCtrl.__init__(self, parent, agwStyle=frame_styles)
        cursor = wx.Cursor(wx.CURSOR_HAND)
        self.SetCursor(cursor)
        self.SetBackgroundColour(wx.WHITE)

    def get_checked_items(self, item_parent=None, checked_items=None):
        if item_parent is None:
            item_parent = self.GetRootItem()

        if checked_items is None:
            checked_items = []

        child, cookie = self.GetFirstChild(item_parent)

        while child:

            if self.IsItemChecked(child):
                checked_items.append(child)

            checked_items = self.get_checked_items(child, checked_items)
            child, cookie = self.GetNextChild(item_parent, cookie)

        return checked_items
