import wx
import wx.lib.agw.customtreectrl


class ThreeSelector(wx.lib.agw.customtreectrl.CustomTreeCtrl):
    def __init__(self, parent):
        frame_styles = wx.TR_HIDE_ROOT | wx.TR_MULTIPLE | wx.TR_LINES_AT_ROOT
        wx.lib.agw.customtreectrl.CustomTreeCtrl.__init__(self, parent, agwStyle=frame_styles)
        myCursor = wx.Cursor(wx.CURSOR_HAND)
        self.SetCursor(myCursor)
        self.SetBackgroundColour(wx.WHITE)

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
