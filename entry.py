import wx

from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar2Wx
from numpy import arange, sin, pi


class Entry(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.BACKGROUND_COLOUR = wx.Colour((180,180,180))
        self.BACKGROUND_COLOUR = self.GetBackgroundColour()
        self.CreateCtrls()


    def Draw(self):
        pass

    def CreateCtrls(self):
        png = wx.Image("startpage.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.logo = wx.StaticBitmap(self, -1, png, (10, 5), (png.GetWidth(), png.GetHeight()))
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.logo, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, border=10)
        self.SetSizerAndFit(sizer)
