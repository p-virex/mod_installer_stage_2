import wx
import wx.lib.agw.customtreectrl as CT


class ThreeSelector(CT.CustomTreeCtrl):
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
