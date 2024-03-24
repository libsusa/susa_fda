import wx

class Halfband(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.BACKGROUND_COLOUR = self.GetBackgroundColour()