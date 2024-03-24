import wx
import os
from entry import Entry
from window import Window

import logging
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
class Frame(wx.Frame):

    ID_WINFIR=1000
    ID_QUIT=1001
    ID_EXPORT=1002
    ID_IMPORT=1003
    ID_HALFBAND=1004

    def __init__(self, title):
        wx.Frame.__init__(self, None, -1, title, size=(620, 620))
        self.statusbar = self.CreateStatusBar()
        self.BACKGROUND_COLOUR = wx.Colour((180,180,180))
        self.BACKGROUND_COLOUR = self.GetBackgroundColour()
        self.panel = None

        self.icons_dir = wx.GetApp().GetIconsDir()

        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        fileItem = fileMenu.Append(Frame.ID_QUIT, 'Quit', 'Quit application')
        exportItem = fileMenu.Append(Frame.ID_EXPORT, 'Export', 'Export')
        importItem = fileMenu.Append(Frame.ID_IMPORT, 'Import', 'Import')
        menubar.Append(fileMenu, '&File')

        toolMenu = wx.Menu()
        windowItem = toolMenu.Append(Frame.ID_WINFIR, 'Window FIR', 'Window FIR')
        halfbandItem = toolMenu.Append(Frame.ID_HALFBAND, 'Half-band', 'Half-band')
        menubar.Append(toolMenu, '&Designer')

        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.OnQuit, fileItem)
        self.Bind(wx.EVT_MENU, self.OnWindow, windowItem)
        self.Bind(wx.EVT_MENU, self.OnHalfband, halfbandItem)
        self.Bind(wx.EVT_MENU, self.OnExport, exportItem)
        self.Bind(wx.EVT_MENU, self.OnImport, importItem)
        self.Bind(wx.EVT_SYS_COLOUR_CHANGED, self.OnColourChanged)

        self.SetProperties()
        self.SetEntry()
        self.Center()

    def OnColourChanged(self, event):
        sys_appearance = wx.SystemSettings.GetAppearance()
        dark = sys_appearance.IsDark()
        logger.debug("dark = %s" % dark)

    def SetProperties(self):

        self.SetMinSize((620, 620))
        frameIcon = wx.Icon(os.path.join(self.icons_dir, "wxwin.ico"), type=wx.BITMAP_TYPE_ICO)
        self.SetIcon(frameIcon)

    def SetEntry(self):
        if self.panel:
            self.panel.Destroy()
            del self.panel

        self.panel = Entry(self)
        self.panel.Draw()

    def SetWindow(self):
        if self.panel:
            self.panel.Destroy()
            del self.panel
        self.panel = Window(self)
        self.panel.Draw()

    def OnWindow(self, event):
        event.Skip()
        self.SetWindow()

    def OnHalfband(self, event):
        event.Skip()

    def OnExport(self, event):
        event.Skip()

    def OnImport(self, event):
        event.Skip()

    def OnQuit(self, event):
        event.Skip()
        self.Destroy()