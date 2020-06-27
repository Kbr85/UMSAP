# ------------------------------------------------------------------------------
#	Copyright (C) 2017 Kenny Bravo Rodriguez <www.umsap.nl>
	
#	This program is distributed for free in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
	
#	See the accompaning licence for more details.
# ------------------------------------------------------------------------------


""" Creates the window showing the results in a .tarprot file """


#region -------------------------------------------------------------- Imports
import wx
import pandas as pd
from pathlib import Path

import config.config     as config
import gui.menu.menu     as menu
import gui.gui_classes   as gclasses
import gui.gui_methods   as gmethods
import data.data_classes as dclasses
import data.data_methods as dmethods
#endregion ----------------------------------------------------------- Imports


class WinTarProtRes(gclasses.WinResUno):
	""" To show the results in a tarprot file """

	#region --------------------------------------------------- Instance Setup
	def __init__(self, file):
		""" file: path to the .tarprot file (string or Path) """
	 #--> Initial Setup
		self.name = config.name['TarProtRes']
		self.fileP = Path(file)
		try:
			self.fileObj = dclasses.DataObjTarProtFile(self.fileP)
		except Exception:
			raise ValueError('')
		self.checkFP = self.fileObj.checkFP
		if self.checkFP:
			pass
		else:
			gclasses.DlgFatalErrorMsg(
				config.dictCheckFatalErrorMsg[self.name]['FiltPept2'])
			raise ValueError('')
		try:
			super().__init__(parent=None)
		except Exception:
			raise ValueError('')
	 #---
	 #--> Variables
		self.locProtType = self.fileObj.locProtType
		self.nExp        = self.fileObj.nExp
		self.nExpLabels  = self.fileObj.nExpLabels
		self.pRes        = self.fileObj.pRes
		self.f           = self.fileObj.Getfragments()
		self.fPlot       = True
		self.lbSelPlot   = False
		self.FragLabel   = 'Experiment   '
		self.kf          = [None, None]
		#--->>>> Needed to have only one OnListSelect method in parentClass
		self.lbSelPlotG = False
		#--->>>> Needed for LimProtRes to work
		self.GelText     = True
	 #---
	 #--> Menu
		self.menubar = menu.MainMenuBarWithTools(self.name)
		self.SetMenuBar(self.menubar)
	 #---
	 #--> Widgets
	  #--> Drawing panel for Gel or Intensity
		self.p2 = gclasses.ElementGraphPanel(parent=self.panel, name=self.name)
	  #---
	 #---
	 #--> Sizers
	  #--> Add
		self.sizerIN.Add(self.p2,      pos=(2,2), border=2,
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
	  #---
	  #--> Fit
		self.sizer.Fit(self)
	  #---
	 #---
	 #--> Positions and minimal size
		gmethods.MinSize(self)
		self.WinPos()	
	 #---
	 #--> Bind
		self.p2.canvas.mpl_connect('button_press_event', self.OnClick)		
	 #---
	 #--> Show
		self.Show()
	 #---
	#---
	#endregion ------------------------------------------------ Instance Setup

	# ------------------------------------------------------------- My Methods
	#region -------------------------------------------------- Binding Methods
	def OnRightDown(self, event):
		""" Display the popup menu """
		self.PopupMenu(menu.ToolsTarProtRes())
		return True
	#---

	def OnClick(self, event):
		""" To process click events """
		if event.button == 3:
			self.PopupMenu(menu.ToolsTarProtRes())
		else:
			pass
		return True
	#---
	#endregion ----------------------------------------------- Binding Methods

	#region ----------------------------------------------------- Menu Methods
	def OnResetView(self):
		""" Reset the view of the window """
	 #--> Reset p1 panel
		self.seqC      = None
		self.kf        = [None, None]
		self.lbSelPlot = False
	 #---
	 #--> Reset listbox
		gmethods.ListCtrlDeSelAll(self.lb)
	 #---
	 #--> Reset p2 panel
		self.p2.axes.clear()
		self.SetAxis()
		self.p2.canvas.draw()
	 #---
	 #--> Reset p3
		self.text.Clear()
	 #---
	 #--> Reset SearchCtrl
		self.search.Clear()
	 #---
	 #-->
		self.Refresh()
		self.Update()
	 #---
	 #--> Return
		return True
	 #---
	#---

	def OnSavePlot(self):
		""" Save plot """
		self.p2.OnSaveImage(config.extLong['MatplotSaveImage'],
			config.msg['Save']['PlotImage'])
		return True
	#---

	def OnExportFP(self):
		""" Export the FP list """
	 #--> Variables
		msg = config.msg['Save']['FiltPept']
		dlg = gclasses.DlgSaveFile(config.extLong['FiltPept'], msg)
	 #---
	 #--> Get path & write
		if dlg.ShowModal() == wx.ID_CANCEL:
			pass
		else:
			p = Path(dlg.GetPath())
			self.fileObj.TarProt2FiltPept(p)
	 #---
	 #--> Destroy & Return 
		dlg.Destroy()
		return True	
	 #---
	#---
	#endregion -------------------------------------------------- Menu Methods

	#region ----------------------------------------------- Intensitiy Methods
	def DFL2DF(self, intL, label):
		""" Takes the intL and converts it to a proper DF 
			---
			intL: list of intensity values (???)
			label: ???
		"""
	 #-->
		lo = {}
		lok = []
		for i in label:
			ints = intL[i].tolist()[0]
			if i == 'Control Exp':
				a      = list(map(float, ints))
				lo[i]  = a[:]
				lok.append(1)
			else:
				lo[i] = list(map(float, ints[1]))
				lok.append(int(ints[0][0]))

		d = pd.DataFrame(dict([(k, pd.Series(v)) for k,v in lo.items()]))
	 #---
	 #-->
		maxV = d.max().max()
		minV = d.min().min()
		intLplot = (d - minV) / (maxV - minV) 
	 #---
	 #--> Return
		return [intLplot, lok]
	 #---
	#---

	def SetAxis(self):
		""" General details of the plot area """

		self.p2.axes.set_xlabel('Experiments', fontweight='bold')
		self.p2.axes.set_ylabel('Normalized Intensities', fontweight='bold')
		self.p2.xticksloc = range(self.nExp + 3)
		self.p2.axes.set_xticks(self.p2.xticksloc)
		self.p2.xlabel = ['', 'C']
		i = 0
		while i < self.nExp:
			j = i + 1
			self.p2.xlabel.append(j)
			i = i + 1
		self.p2.xlabel.append('')
		self.p2.axes.set_xticklabels(self.p2.xlabel)
		return True
	#---

	def DrawI(self, seq, intLplot, lok, label):
		""" Draw the intensities for a selected peptide """
	 #--> Clear plot
		self.p2.axes.clear()
	 #---
	 #--> Get x
		x = list(range(1, self.nExp+2, 1))
	 #---
	 #--> Title
		self.p2.axes.set_title(str(seq))
	 #---
	 #--> Plot errorbar
		tempM = intLplot.mean()
		tempSD = intLplot.std()
		self.p2.axes.errorbar(x, tempM, yerr=tempSD, fmt='D', 
			markeredgecolor='#000000', color='#00FFFF', ecolor='k', 
			markersize=8, capsize=4)
	 #---
	 #--> Plot line
		tx = []
		y = []
		for i in range(0, len(lok), 1):
			j = i + 1
			if lok[i] == 1:
				tx.append(j)
				y.append(tempM[label[i]])
			else:
				pass
		self.p2.axes.plot(tx, y, 'b-')
	 #---
	 #-->  Plot values
		intLplot = intLplot.transpose()
		self.p2.axes.plot(x, intLplot, 'ro', markeredgecolor='#000000')
	 #---
	 #--> Axis & Draw
		self.SetAxis()
		self.p2.canvas.draw()
	 #---
	 #--> Return
		return True
	 #---
	#---
	#endregion --------------------------------------------- Intensity Methods

	#region ----------------------------------------------------- Text Methods
	def ShowFragDet(self):
		""" """
		dmethods.GHelperShowFragDet(self)
		return True
	#---	
	#endregion -------------------------------------------------- Text Methods
#---






