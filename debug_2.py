import os
import wx


########################################################################
class MyForm(wx.Frame):

    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY,
                          "File and Folder Dialogs Tutorial")
        panel = wx.Panel(self, wx.ID_ANY)
        self.currentDirectory = os.getcwd()

        dirDlgBtn = wx.Button(panel, label="Show DirDialog")
        dirDlgBtn.Bind(wx.EVT_BUTTON, self.onDir)

    #----------------------------------------------------------------------
    def onDir(self, event):
        """
        Show the DirDialog and print the user's choice to stdout
        """
        dlg = wx.DirDialog(self, "Choose a directory:",
                           style=wx.DD_DEFAULT_STYLE
                           #| wx.DD_DIR_MUST_EXIST
                           #| wx.DD_CHANGE_DIR
                           )
        if dlg.ShowModal() == wx.ID_OK:
            print ("You chose %s" % dlg.GetPath())
        dlg.Destroy()

#----------------------------------------------------------------------
# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = MyForm()
    frame.Show()
    app.MainLoop()