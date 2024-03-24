import wx
import os
import sys

from frame import Frame

class App(wx.App):
    def OnInit(self):

        self.installDir = os.path.split(os.path.abspath(sys.argv[0]))[0]

        frame = Frame("Susa FDA")
        self.SetTopWindow(frame)
        frame.Show(True)

        return True

    def GetInstallDir(self):
        """
        Return the installation directory for my application.
        """

        return self.installDir


    def GetIconsDir(self):
        """
        Return the icons directory for my application.
        """

        icons_dir = os.path.join(self.installDir, ".")
        return icons_dir