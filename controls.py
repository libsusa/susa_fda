import wx
import wx.lib.intctrl
from typing import Any

class LabelIntSizer(wx.BoxSizer):
    def __init__(self, parent, label, size=wx.DefaultSize, value=0):
        super().__init__(wx.HORIZONTAL)

        self.label = wx.StaticText(parent, label=label, size=size)
        self.integer = wx.lib.intctrl.IntCtrl(parent, value=value, size=(100,20))

        self.Add(self.label, flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT)
        self.Add(self.integer)

    def Bind(self, event : Any, handler : Any):
        self.integer.Bind(event, handler)

    def SetValue(self, value : int):
        self.integer.SetValue(value)

    def GetValue(self) -> int:
        return self.integer.GetValue()

    def SetMin(self, min : int) -> None:
        self.integer.SetMin(min)

    def Disable(self):
        self.integer.Disable()
        self.label.Disable()

    def Enable(self):
        self.integer.Enable()
        self.label.Enable()

class LabelComboSizer(wx.BoxSizer):
    def __init__(self, parent, label, size=wx.DefaultSize, choices=[]):
        super().__init__(wx.HORIZONTAL)

        self.label = wx.StaticText(parent, label=label, size=size)
        self.combo = wx.ComboBox(parent, choices = choices, size=(100,20))

        self.Add(self.label, flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT)
        self.Add(self.combo)

    def Bind(self, event : Any, handler : Any):
        self.combo.Bind(event, handler)

    def SetValue(self, value : int):
        self.combo.SetSelection(value)

    def GetValue(self) -> int:
        return self.combo.GetSelection()

    def Disable(self):
        self.combo.Disable()
        self.label.Disable()

    def Enable(self):
        self.combo.Enable()
        self.label.Enable()
class LabelCheckBoxSizer(wx.BoxSizer):
    def __init__(self, parent, label, size=wx.DefaultSize):
        super().__init__(wx.HORIZONTAL)

        self.label = wx.StaticText(parent, label=label, size=size)
        self.check = wx.CheckBox(parent)

        self.Add(self.label, flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT)
        self.Add(self.check)

    def Bind(self, event : Any, handler : Any):
        self.check.Bind(event, handler)

    def SetValue(self, value : bool):
        self.check.SetValue(value)

    def GetValue(self) -> bool:
        return self.check.GetValue()

    def Disable(self):
        self.check.Disable()
        self.label.Disable()

    def Enable(self):
        self.check.Enable()
        self.label.Enable()