import wx
import wx.lib.intctrl

from typing import Any, List

from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

from designer.winfir import WindowDesign, FilterResponse, WindowType
from controls import LabelCheckBoxSizer, LabelIntSizer, LabelComboSizer
from cursor import Cursor

import logging
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def get_object_fields(the_object: Any) -> List[str]:
    """
    gets the public attributes of an object, if possible
    the creation order is preserved
    """
    if hasattr(the_object, '__dict__'):
        fields = the_object.__dict__.keys()
    elif hasattr(the_object, '__slots__'):
        fields = the_object.__slots__
    else:
        fields = dir(the_object)
    fields = [field for field in fields if not field.startswith('_')]
    return fields
class Window(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.BACKGROUND_COLOUR = self.GetBackgroundColour()
        self.design = WindowDesign()
        self.CreateCtrls()
        self.DoLayout()
        self.Update()


    def CreateCtrls(self):
        self.figure = Figure(figsize=(10,5), dpi=100, tight_layout=True)
        color = (self.BACKGROUND_COLOUR.Red()/255.0, self.BACKGROUND_COLOUR.Green()/255.0, self.BACKGROUND_COLOUR.Blue()/255.0)
        self.figure.set_facecolor(color)
        self.canvas = FigureCanvas(self, -1, self.figure)


    def DoLayout(self):
        size=(200,-1)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        grid = wx.GridSizer(rows=3, cols=3, hgap=5, vgap=5)
        self.sam_freq = LabelIntSizer(self, "Sampling Frequency (Hz)", size=size)
        self.num_taps = LabelIntSizer(self, "Number of Taps", size=size)
        self.num_shifts = LabelIntSizer(self, "Number of Shifts", size=size)
        self.low_freq = LabelIntSizer(self, "Low Frequency (Hz)", size=size)
        self.high_freq = LabelIntSizer(self, "High Frequency (Hz)", size=size)
        self.filter_response = LabelComboSizer(self, "Response Type", choices=get_object_fields(FilterResponse), size=size)
        self.win_type = LabelComboSizer(self, "Window Type", choices=get_object_fields(WindowType), size=size)
        self.causal = LabelCheckBoxSizer(self, "Linear-Phase and Causal", size=(200, -1))
        self.btn_design = wx.Button(self, label="Design")

        self.causal.Bind(wx.EVT_CHECKBOX, self.OnCausalChanged)
        self.btn_design.Bind(wx.EVT_BUTTON, self.OnDesignButton)
        self.filter_response.Bind(wx.EVT_COMBOBOX, self.OnFilterTypeChanged)
        self.num_taps.Bind(wx.lib.intctrl.EVT_INT, self.OnTapsChanged)
        self.num_taps.Bind(wx.EVT_KILL_FOCUS, self.OnTapsKeys)

        grid.AddMany([(self.sam_freq, wx.EXPAND), (self.num_taps, wx.EXPAND), (self.causal, wx.EXPAND),
                      (self.num_shifts, wx.EXPAND), (self.low_freq, wx.EXPAND), (self.high_freq, wx.EXPAND),
                      (self.filter_response, wx.EXPAND), (self.win_type, wx.EXPAND)])


        self.causal.SetValue(True)
        self.num_shifts.Disable()
        self.sam_freq.SetValue(1000)
        self.num_taps.SetValue(161)
        self.num_shifts.SetValue(80)
        self.num_shifts.SetMin(0)
        self.low_freq.SetValue(10)
        self.high_freq.SetValue(100)
        self.win_type.SetValue(self.design.WIN_TYPE.value - 1)
        self.filter_response.SetValue(self.design.RESPONSE_TYPE.value - 1)

        vsizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        hsizer.Add(grid)
        hsizer.Add(self.btn_design, 0, wx.RIGHT)
        vsizer.Add(hsizer, flag=wx.EXPAND | wx.GROW)
        self.SetSizer(vsizer)
        vsizer.SetSizeHints(self.GetParent())
        self.Fit()


    def Draw(self):
        color = (self.BACKGROUND_COLOUR.Red()/255.0, self.BACKGROUND_COLOUR.Green()/255.0, self.BACKGROUND_COLOUR.Blue()/255.0)
        self.figure.clf()
        self.ax_fir = self.figure.add_subplot(2, 2, 1)
        self.ax_fir.set_facecolor(color)
        self.ax_fir.grid(linestyle=':', alpha=0.5)
        self.ax_fir.set_title('Filter Impulse Response')
        self.ax_fir.set_ylabel("Amplitude")
        self.ax_fir.set_xlabel("Time (s)")
        self.ax_fir.plot(self.design.vec_time, self.design.wir)

        self.ax_win = self.figure.add_subplot(2, 2, 2)
        self.ax_win.set_facecolor(color)
        self.ax_win.grid(linestyle=':', alpha=0.5)
        self.ax_win.set_title('Window')
        self.ax_win.set_ylabel("Amplitude")
        self.ax_win.set_xlabel("Time (s)")
        self.ax_win.plot(self.design.vec_time, self.design.window)

        self.ax_wirb = self.figure.add_subplot(2, 2, 3)
        self.ax_wirb.set_facecolor(color)
        self.ax_wirb.grid(linestyle=':', alpha=0.5)
        self.ax_wirb.set_title('Windowed Impulse Response Bode')
        self.ax_wirb.set_ylabel("20 log |H|")
        self.ax_wirb.set_xlabel("Frequency (Hz)")
        self.ax_wirb.plot(self.design.vec_freqs, self.design.bode_wir)

        self.snap_cursor_wirb = Cursor(self.ax_wirb, self.GetParent(), 'Frequency [Hz]', 'Power Attenuation [dB]')
        self.canvas.mpl_connect('motion_notify_event', self.snap_cursor_wirb.on_mouse_move)

        self.ax_wb = self.figure.add_subplot(2, 2, 4)
        self.ax_wb.set_facecolor(color)
        self.ax_wb.grid(linestyle=':', alpha=0.5)
        self.ax_wb .set_title('Window Bode')
        self.ax_wb .set_ylabel("20 log |H|")
        self.ax_wb .set_xlabel("Frequency (Hz)")
        self.ax_wb.plot(self.design.vec_freqs, self.design.bode_window)

        self.snap_cursor_wb = Cursor(self.ax_wb, self.GetParent(), 'Frequency [Hz]', 'Power Attenuation [dB]')
        self.canvas.mpl_connect('motion_notify_event', self.snap_cursor_wb.on_mouse_move)

        self.canvas.draw()


    def Update(self):
        self.design.NUM_TOTAL_SAMPLES = self.num_taps.GetValue()
        self.design.NUM_SHIFT_SAMPLES = self.num_shifts.GetValue()
        self.design.SAMPLE_TIME_S = 1.0 / self.sam_freq.GetValue()
        self.design.CUTOFF_FREQUENCY_HZ = self.low_freq.GetValue()
        self.design.CUTOFF_FREQUENCY2_HZ = self.high_freq.GetValue()
        self.design.WIN_TYPE = WindowType[self.win_type.combo.GetValue()]
        self.design.RESPONSE_TYPE =  FilterResponse[self.filter_response.combo.GetValue()]

        logger.debug(f'number of shifts: {self.design.NUM_SHIFT_SAMPLES}')

        self.design.update()
        self.Draw()

    def OnCausalChanged(self, event):
        logger.debug('causal check box changed')
        if self.causal.check.GetValue():
            self.num_shifts.integer.SetValue(int(self.num_taps.GetValue() / 2))
            self.num_shifts.Disable()
        else:
            self.num_shifts.Enable()

    def OnDesignButton(self, event):
        logger.debug('design button pressed')
        self.Update()

    def OnTapsChanged(self, event):
        if self.causal.check.GetValue():
            self.num_shifts.integer.SetValue(int(self.num_taps.GetValue() / 2))

    def OnTapsKeys(self, event):
        num_taps = self.num_taps.GetValue()
        if (num_taps % 2) == 0:
            num_taps += 1
            self.num_taps.SetValue(num_taps)

    def OnFilterTypeChanged(self, event):
        logger.debug('filter type changed')
        selected_type = FilterResponse[self.filter_response.combo.GetValue()]

        if selected_type == FilterResponse.HighPass:
            self.high_freq.Disable()
        else:
            self.high_freq.Enable()

        if selected_type == FilterResponse.LowPass:
            self.low_freq.Disable()
        else:
            self.low_freq.Enable()
