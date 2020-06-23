# ------------------------------------------------------------------------------
# 	Copyright (C) 2017 Kenny Bravo Rodriguez <www.umsap.nl>

# 	This program is distributed for free in the hope that it will be useful,
# 	but WITHOUT ANY WARRANTY; without even the implied warranty of
# 	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

# 	See the accompaning licence for more details.
# ------------------------------------------------------------------------------


""" This module display the information in a histo file """


# ------------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Methods
# ------------------------------------------------------------------------------


# --- Imports
## Standard modules
import matplotlib.patches as mpatches
import numpy as np
## My modules
import config.config as config
import gui.menu.menu as menu
import gui.gui_classes as gclasses
import gui.gui_methods as gmethods
import data.data_classes as dclasses
#---


class WinHistoRes(gclasses.WinGraph):
    """ Creates the window to show the results in a .hist file """

    def __init__(self, file):
        """ file: path to the .hist file (string or Path)"""
     #--> Initial Setup
        self.name = config.name["HistoRes"]
        try:
            super().__init__(file)
        except Exception:
            raise ValueError("")
     #--> Variables
        self.nExpFP = self.fileObj.nExpFP
        self.barWidth = self.fileObj.barWidth
        self.dfDict = self.fileObj.dfDict
        #---
        self.Ncolor = len(config.colors["Fragments"])
        #---
        self.seq = 0  # 0 Rec 2 Nat
        self.uni = 0  # 0 All 1 Unique
     #--> Menu
        self.menubar = menu.MainMenuBarWithTools(self.name, self.seq, self.uni)
        self.SetMenuBar(self.menubar)
     #--> Draw
        self.DrawConfig()
     #--> Show
        self.Show()
    #---

    ####---- Methods of the class
    ##-- Binding
    def WinPos(self):
        """ Set the position of a new window depending on the number of same
		    windows already open. 
        """
     #--> Coordinates
        xw, yw = self.GetSize()
        xo = 0
        yo = config.size["Screen"][1] - yw + config.size["TaskBarHeight"]
        x = xo + config.win["HistoResNum"] * config.win["DeltaNewWin"]
        y = yo - config.win["HistoResNum"] * config.win["DeltaNewWin"]
     #--> Position
        self.SetPosition(pt=(x, y))
     #--> Number of already created windows
        config.win["HistoResNum"] = config.win["HistoResNum"] + 1
     #--> Return
        return True
    #---

    def OnClick(self, event):
        """ To process click events """
        if event.button == 3:
            self.PopupMenu(menu.ToolMenuHistoRes(self.seq, self.uni))
        else:
            pass
        return True
    #---

    ##-- Menu
    def OnReset(self):
        """ Reset the window """
        self.uni = 0
        self.seq = 0
        self.menubar.Check(503, True)
        self.menubar.Check(504, True)
        self.DrawConfig()
        return True
    #---

    def OnSavePlot(self):
        """ Save image of the plot """
        if self.OnSaveImage(config.extLong["MatplotSaveImage"], 
            config.msg["Save"]["PlotImage"]):
            return True
        else:
            return False
    #---

    def OnSeq(self, Mid):
        """ Change the plot if the sequence changes 
            ---
            Mid: ID of the selected menu item
        """
        if Mid == 502:
            self.seq = 2
        else:
            self.seq = 0
        self.menubar.Check(Mid, True)
        self.DrawConfig()
        return True
    #---

    def OnUni(self, Mid):
        """ Change the plot if the type of cleavages changes 
            ---
            Mid: ID of the selected menu item
        """
        if Mid == 505:
            self.uni = 1
        else:
            self.uni = 0
        self.menubar.Check(Mid, True)
        self.DrawConfig()
        return True
    #---

    ##-- Plotting
    def DrawConfig(self):
        """ Configure the plot """
     #--> Variables
        #-->
        if self.seq == 0:
            prot = "Recombinant sequence"
        else:
            prot = "Native sequence"
        if self.uni == 0:
            val = "All cleavages"
        else:
            val = "Unique cleavages"
        self.tkey   = config.hist["DictKeys"][self.seq + self.uni]
        self.plotDf = self.dfDict[self.tkey]
        #--> 
        if self.plotDf is None:
            gmethods.NoDataImage(self)
            return True
        else:
            pass
        #-->
        self.title = prot + ", " + val
        self.lWin = self.fileObj.GetlWin(self.tkey)
        self.nWin = len(self.lWin)
        self.header = list(self.plotDf.columns)[1:]
        self.header.append(self.header[0])
        self.header = self.header[1:]
        #-->
        self.x = range(1, self.nWin + 1, 1)
     #--> Draw & Return
        self.Draw()
        return True
    #---

    def Draw(self):
        """ Draw into the plot. """
     #--> Clear plot
        self.ClearPlot()
     #--> Set Title
        self.axes.set_title(self.title)
     #--> Plot bars
        c = 0
        for k in self.plotDf:
      #--> FP
            if k == "FP":
                tx = [x + config.hist["StartLoc"] for x in self.x]
                color = config.colors[self.name]["FPBar"]
                self.axes.bar(
                    tx,
                    self.plotDf[k],
                    align="edge",
                    width=-self.barWidth,
                    color=color,
                    edgecolor=config.colors[self.name]["EdgeC"],
                )
      #--> Experimnets
            elif k != "Windows":
                ci = (c + 1) % self.Ncolor
                color = config.colors["Fragments"][ci]
                tx = [x - config.hist["StartLoc"] + c * self.barWidth for x in self.x]
                self.axes.bar(
                    tx,
                    self.plotDf[k],
                    align="edge",
                    width=self.barWidth,
                    color=color,
                    edgecolor=config.colors[self.name]["EdgeC"],
                )
                c += 1
            else:
                pass
     #--> Legend
        self.legendlist = []
        for i in range(1, self.nExpFP, 1):
            ci = i % self.Ncolor
            color = config.colors["Fragments"][ci]
            name = "Exp " + str(i)
            patch = mpatches.Patch(color=color, label=name)
            self.legendlist.append(patch)
        patch = mpatches.Patch(color=config.colors[self.name]["FPBar"], label="FP list")
        self.legendlist.append(patch)
        self.leg = self.axes.legend(
            handles=self.legendlist, loc="upper left", bbox_to_anchor=(1, 1)
        )
        self.leg.get_frame().set_edgecolor("k")
     #--> Update axis & Draw
        self.SetAxis()
        self.canvas.draw()
     #--> Return
        return True
    #---

    def SetAxis(self):
        """ General details of the plot area """
        self.axes.grid(True, linestyle=":")
        self.axes.set_xlabel("Windows", fontweight="bold")
        self.axes.set_ylabel("Number of cleavages", fontweight="bold")
        self.xticksloc = range(0, self.nWin + 2, 1)
        self.axes.set_xticks(self.xticksloc)
        self.xlabel = [""]
        self.xlabel = self.xlabel + self.lWin
        self.xlabel.append("")
        self.axes.set_xticklabels(self.xlabel, rotation=45)
        self.figure.subplots_adjust(bottom=0.2)
        return True
    #---

    def UpdateStatusBar(self, event):
        """ Update the status bar text """
        if event.inaxes:
            x, y = event.xdata, event.ydata
            if self.plotDf is not None:
                if x > 0.6 and x < self.nWin + 0.4:
                    xf = int(x + 0.5) - 1
                    winx = self.lWin[xf]
                    xfp = xf + 1
                    s = xfp - config.hist["StartLoc"]
                    e = s + config.hist["Twidth"]
                    xr = np.arange(s, e + self.barWidth, self.barWidth)
                    i = 0
                    exp = None
                    while i < xr.shape[0] - 1:
                        if xr[i] < x and x <= xr[i + 1]:
                            exp = self.header[i]
                            break
                        else:
                            pass
                        i += 1
                    if exp is None:
                        self.statusbar.SetStatusText(gmethods.StatusBarXY(x, y))
                    else:
                        cuts = self.plotDf[str(exp)][xf]
                        self.statusbar.SetStatusText(
                            "Win="
                            + str(winx)
                            + "  Exp="
                            + str(exp)
                            + "  Cleavages="
                            + str(cuts)
                        )
                else:
                    self.statusbar.SetStatusText(gmethods.StatusBarXY(x, y))
            else:
                self.statusbar.SetStatusText(gmethods.StatusBarXY(x, y))
        else:
            self.statusbar.SetStatusText("")
        return True
    #---
#---

