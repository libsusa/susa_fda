import wx
import numpy as np

class Cursor:

    def __init__(self, ax, frame : wx.Frame, xlabel :str, ylabel :str):
        self.ax = ax
        self.horizontal_line = ax.axhline(color='k', lw=0.8, ls='--')
        self.vertical_line = ax.axvline(color='k', lw=0.8, ls='--')
        line = self.ax.lines[0]
        self.x, self.y = line.get_data()
        self._last_index = None
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.frame = frame

    def set_cross_hair_visible(self, visible):
        need_redraw = self.horizontal_line.get_visible() != visible
        self.horizontal_line.set_visible(visible)
        self.vertical_line.set_visible(visible)
        return need_redraw

    def on_mouse_move(self, event):
        if not event.inaxes:
            self._last_index = None
            need_redraw = self.set_cross_hair_visible(False)
            if need_redraw:
                self.ax.figure.canvas.draw()
        elif event.inaxes == self.ax:
            self.set_cross_hair_visible(True)
            x, y = event.xdata, event.ydata
            index = min(np.searchsorted(self.x, x), len(self.x) - 1)
            if index == self._last_index:
                return

            self._last_index = index
            x = self.x[index]
            y = self.y[index]

            self.horizontal_line.set_ydata(y)
            self.vertical_line.set_xdata(x)
            self.frame.statusbar.SetStatusText(f'{self.xlabel} : {x:.2f}  -  {self.ylabel} : {y:.2f}')
            self.ax.figure.canvas.draw()