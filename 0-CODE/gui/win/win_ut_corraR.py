# ------------------------------------------------------------------------------
#	Copyright (C) 2017 Kenny Bravo Rodriguez <www.umsap.nl>
	
#	This program is distributed for free in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
	
#	See the accompaning licence for more details.
# ------------------------------------------------------------------------------


""" Creates the window showing the results in a .corr file """


#region -------------------------------------------------------------- Imports
import wx
import numpy as np
import matplotlib as mpl

import config.config     as config
import gui.menu.menu     as menu
import gui.gui_classes   as gclasses
import gui.gui_methods   as gmethods
import gui.gui_methods   as dmethods
import data.data_classes as dclasses 
#endregion ----------------------------------------------------------- Imports


class WinCorrARes(gclasses.WinGraph):
	""" Creates the window to show the results in a .corr file """

	#region --------------------------------------------------- Instance Setup
	def __init__(self, file):
		""" file: path to the .corr file (string or Path) """
	 #--> Initial Setup
		self.name = config.name['CorrARes']
		super().__init__(file)
	 #---
	 #--> Variables
		self.colNum = self.fileObj.colNum
		self.data   = self.fileObj.data
		self.fileD  = self.fileObj.fileD
		self.gtitle = self.fileObj.gtitle
		self.numCol = self.fileObj.numCol
		self.mID    = None # To avoid destroying the export window when 
						   # reselecting the same module in the export menu
	 #---
	 #--> Menu
		self.menubar = menu.MainMenuBarWithTools(self.name)
		self.SetMenuBar(self.menubar)
	 #---
	 #--> Draw
		self.Draw()
	 #---
	 #--> Show
		self.Show()
	 #---
	#---
	#endregion ------------------------------------------------ Instance Setup

	# ------------------------------------------------------------- My Methods
	#region -------------------------------------------------- Binding Methods
	def WinPos(self):
		""" Set the position of a new window depending on the number of same 
			windows already open 
		"""
	 #--> Center
		self.Center()
	 #---
	 #--> Coordinates
		xo, yo = self.GetPosition()
		x = xo - config.win['CorrAResNum'] * config.win['DeltaNewWin']
		y = yo + config.win['CorrAResNum'] * config.win['DeltaNewWin']
	 #---
	 #--> Set positions
		self.SetPosition(pt=(x, y))
	 #---
	 #--> Update number of created windows
		config.win['CorrAResNum'] += 1
	 #---
	 #--> Return
		return True
	 #---
	#---

	def OnClick(self, event):
		""" To process click events """
		if event.button == 3:
			self.PopupMenu(menu.ToolMenuCorrARes())
		else:
			pass
		return True
	#---
	#endregion ----------------------------------------------- Binding Methods

	#region ----------------------------------------------------- Menu Methods
	def OnExport(self, mID):
		""" Export columns in the correlation plot 
			---
			mID: menu ID triggering the export
		"""
		if self.mID == None:
	 #--> Check that other CorrARes window has not opened an Export window 
			try:
				config.win['TypeRes'][self.name].Close()
				del(config.win['TypeRes'][self.name])
			except Exception:
				pass			
		elif self.mID == mID:
			pass
		else: 
	 #---
	 #--> Destroy TypeRes window already opened from CorrARes
			config.win['TypeRes'][self.name].Close()
			del(config.win['TypeRes'][self.name])
	 #---
	 #--> Launch the TypeRes window
		gmethods.WinTypeResCreate(
			config.name['TypeRes'], 
			self,
			parentName=config.mod[config.corr['MenuID'][mID]]
		)
	 #---
	 #--> Set self.mID
		self.mID = mID		
	 #---
	 #--> Return
		return True
	 #---
	#---
	#endregion -------------------------------------------------- Menu Methods

	#region ----------------------------------------------------- Plot Methods
	def SetAxis(self):
		""" General details of the plot area """
	 #-->
		self.axes.grid(False)
	 #---
	 #--> 
		if self.numCol <= 30:
			step = 1
		elif self.numCol > 30 and self.numCol <= 60:
			step = 2
		else:
			step = 3
		self.xlabel = []
		self.xticksloc = []
	 #---
	 #-->
		for i in range(0, self.numCol, step):
			self.xticksloc.append(i + 0.5)		
			self.xlabel.append(self.data.columns[i])
	 #---
	 #-->
		self.axes.set_xticks(self.xticksloc)
		self.axes.set_xticklabels(self.xlabel, rotation=90)
	 #---
	 #-->
		self.axes.set_yticks(self.xticksloc)
		self.axes.set_yticklabels(self.xlabel)
	 #---
	 #-->
		self.figure.subplots_adjust(bottom=0.13)
	 #---
	 #-->
		return True
	 #---
	#---

	def Draw(self):
		""" Draw into the plot. """
	 #-->
		self.axes.set_title(self.gtitle)
	 #---
	 #--> Plot
		self.axes.pcolormesh(
			self.data, 
			cmap=self.MatplotLibCmap(),
			vmin=-1, 
			vmax=1,
			antialiased=True,
			edgecolors='k',
			lw=0.005,
		)
	 #---
	 #--> Update axis and draw
		self.SetAxis()
		self.canvas.draw()
	 #---
	 #--> Return
		return True
	 #---
	#---

	def MatplotLibCmap(self, c1='red', c2='white', c3='blue'):
		""" Generate custom matplotlib cmap red->white->blue """
	 #--> Variables
		N = 128
		c1l = [255,   0,   0]
		c2l = [255, 255, 255]
		c3l = [  0,   0, 255]
	 #---
	 #--> red -> white
		vals1 = np.ones((N, 4))
		vals1[:, 0] = np.linspace(c1l[0]/c2l[0], c2l[0]/256, N)
		vals1[:, 1] = np.linspace(c1l[1]/c2l[1], c2l[1]/256, N)
		vals1[:, 2] = np.linspace(c1l[2]/c2l[2], c2l[2]/256, N)
	 #---
	 #--> white to blue
		vals2 = np.ones((N, 4))
		vals2[:, 0] = np.linspace(c2l[0]/256, c3l[0]/256, N)
		vals2[:, 1] = np.linspace(c2l[1]/256, c3l[1]/256, N)
		vals2[:, 2] = np.linspace(c2l[2]/256, c3l[2]/256, N)
	 #---
	 #--> new cmap
		vals = np.vstack((vals1, vals2))
		newmap = mpl.colors.ListedColormap(vals)
	 #---
	 #--> Return
		return newmap
	 #---
	#---

	def UpdateStatusBar(self, event):
		""" Updates the statusbar text """
	 #--> Check location of event
		if event.inaxes:
	 	 #--> Variables 
			x, y = event.xdata, event.ydata
			xf = int(x)
			xs = self.data.columns[xf]
			yf = int(y)
			ys = self.data.columns[yf]
			zf = '{:.2f}'.format(self.data.iat[yf,xf])
		 #---
		 #--> Print
			self.statusbar.SetStatusText("x = " + str(xs) + "  y = " + str(ys) 
				+ "  c = " + str(zf))
		 #---
		else:
			self.statusbar.SetStatusText('')
	 #---
	 #--> Return
		return True
	 #---
	#---
	#endregion -------------------------------------------------- Plot Methods
#---














