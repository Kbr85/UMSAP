# ------------------------------------------------------------------------------
#	Copyright (C) 2017 Kenny Bravo Rodriguez <www.umsap.nl>
	
#	This program is distributed for free in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
	
#	See the accompaning licence for more details.
# ------------------------------------------------------------------------------


""" This module generate a graphical output for a .cutevo file """


#region -------------------------------------------------------------- Imports
from pathlib import Path 

import wx

import config.config   as config
import gui.menu.menu   as menu
import gui.gui_classes as gclasses
import gui.gui_methods as gmethods
#endregion ----------------------------------------------------------- Imports

class WinCutEvoRes(gclasses.WinResDos):
	""" Creates the window to show the results in a .cutevo file """

	#region --------------------------------------------------- Instance Setup
	def __init__(self, file):
		""" file: path to the .cutevo file (string or Path) """
	 #--> Initial Setup
		self.name  = config.name['CutEvoRes']
		self.fileP = Path(file)
		super().__init__(self, None)
	 #---
	 #--> Variables
		self.data       = self.fileObj.data
		self.dataFilter = None
		self.nExp       = self.fileObj.nExp
		self.x          = [x for x in range(1, self.nExp+1, 1)]
	 #---
	 #--> Menu
		self.menubar = menu.MainMenuBarWithTools(self.name)
		self.SetMenuBar(self.menubar)
	 #---
	 #--> Select first item by default
		self.lb.Select(0, on=1)
	 #---
	 #--> Bind
		if config.cOS != 'Windows':
			self.p2.canvas.mpl_connect('button_press_event', self.OnClick)
		else:
			pass
		self.lb.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnListSelect)
	 #---
	 #--> Draw
		self.DrawConfig()
	 #---
	 #--> Show	
		self.sizer.Fit(self)
		self.Center()
		self.Show()
	 #---
	#---
	#endregion ------------------------------------------------ Instance Setup

	#region ------------------------------------------------------------- Bind
	def OnListSelect(self, event):
		""""""
		self.DrawConfig()
		return True
	#---
	#endregion ---------------------------------------------------------- Bind

	#region ------------------------------------------------------------- Menu
	def OnResetView(self):
		""" Reset view """
		gmethods.ListCtrlDeSelAll(self.lb)
		self.lb.Select(0, on=1)
		return True
	#---

	def OnExportData(self):
		""" Export data to a csv file """
	 #--> Variables
		msg = config.msg['Save']['ExportData']
		dlg = gclasses.DlgSaveFile(config.extLong['Data'], msg)
	 #---
	 #--> Get path & write
		if dlg.ShowModal() == wx.ID_CANCEL:
			pass
		else:
			p = Path(dlg.GetPath())
			self.fileObj.ExportData(p)
	 #---
	 #--> Destroy & Return 
		dlg.Destroy()
		return True	
	 #---
	#---	

	def OnSavePlot(self):
		""""""
		self.p2.OnSaveImage()
		return True
	#---

	def OnRightDown(self, event):
		""""""
		if config.cOS != 'Windows':
			Tmenu = menu.ToolsCutEvoRes()
			self.PopupMenu(Tmenu)
		else:
			pass
		return True
	#---

	def OnClick(self, event):
		""" To process click events """
	 #-->
		if event.button == 3:
			if config.cOS != 'Windows':
				Tmenu = menu.ToolsCutEvoRes()
				self.PopupMenu(Tmenu)
			else:
				pass
		else:
			pass
	 #---
	 #-->
		return True
	 #---
	#---

	def OnMono(self):
		""" Identify residues with monotonic behavior """
		mask = self.data.iloc[:,1:].apply(self.OnMonoFind, axis=1, raw=False)
		df = self.data[mask]
		idx = df.index.values.tolist()
		if idx:
			gmethods.ListCtrlDeSelAll(self.lb)
			for e in idx:
				self.lb.Select(e, on=1)
		else:
			msg = "No residue with monotonic behavior was found."
			gclasses.DlgWarningOk(msg)
			return True
	#---

	def OnMonoFind(self, row):
		""" """
		if row.is_monotonic_increasing:
			return True
		else:
			return False
	#---
	#endregion ---------------------------------------------------------- Menu

	#region ----------------------------------------------------- Draw Methods
	def DrawConfig(self):
		""" Configure the matplot graph """
	 #--> Get row selected in listbox
		self.selRes = gmethods.ListCtrlGetColVal(self.lb, col=1)
	 #--> Draw
		self.Draw()
	 #---
	#---

	def Draw(self):
		""" Draw the plot """
	 #--> Clear
		self.p2.ClearPlot()
	 #---
	 #--> Plot
		for sel in self.selRes:
			y = self.data[self.data['Residue Number']==sel].iloc[:,1:].values.tolist()
			self.p2.axes.plot(self.x, y[0], label=str(sel))
		
		self.p2.axes.legend(loc='upper left', bbox_to_anchor=(1, 1))
	 #---
	 #--> Axis, draw & return
		self.SetAxis()
		self.p2.canvas.draw()
		return True
	 #---
	#---

	def SetAxis(self):
		""" General details of the plot area """
	 #--> Names of the axis
		self.p2.axes.grid(True, linestyle=':')
		self.p2.axes.set_xlabel('Experiment', fontweight='bold')
		self.p2.axes.set_ylabel('Relative cleavage rate', fontweight='bold')
	 #---
	 #--> X ticks
		self.p2.axes.set_xticks(self.x)
	 #---
	#endregion -------------------------------------------------- Draw Methods
#---