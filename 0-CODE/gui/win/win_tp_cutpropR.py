# ------------------------------------------------------------------------------
#	Copyright (C) 2017 Kenny Bravo Rodriguez <www.umsap.nl>
	
#	This program is distributed for free in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
	
#	See the accompaning licence for more details.
# ------------------------------------------------------------------------------


""" This module generate a graphical output for a cutprop file """


# ------------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Methods
# ------------------------------------------------------------------------------



#--- Imports
## Standard modules
import pandas as pd
from pathlib import Path
## My modules
import config.config     as config
import gui.menu.menu     as menu
import gui.gui_classes   as gclasses
import gui.gui_methods   as gmethods
import data.data_methods as dmethods
import data.data_classes as dclasses 
#---



class WinCutPropRes(gclasses.WinGraph):
	""" Creates the window to show the results in a .cutprop file """

	def __init__(self, file):
		""" file: path to the .cutprop file (string or Path) """
	 #--> Initial Setup
		self.name = config.name['CutPropRes']
		super().__init__(file)
	 #--> Variables
		self.data    = self.fileObj.data
		self.nExp    = self.fileObj.nExp
		self.header  = self.fileObj.header
		self.pRes    = self.fileObj.pRes
		self.mist    = self.fileObj.mist
		self.pResNat = self.fileObj.pResNat
		self.natProt = self.fileObj.natProtPres
		#---
		self.seq  = 0    # 0 Rec 2 Nat
		self.norm = 0    # 0 Reg 1 Norm 
		self.exp  = 0    # 0 Total 1, 2, 3 .... 
		self.comp = None # 0 Total 1, 2, 3 ....
	 #--> Menu
		self.menubar = menu.MainMenuBarWithTools(
			self.name, 
			self.nExp, 
			self.seq, 
			self.norm, 
			self.exp, 
			self.comp)
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
			windows already open 
		"""
	 #--> Coordinates
		xw, yw = self.GetSize()
		xo = config.size['Screen'][0] - xw
		yo = config.size['Screen'][1] - yw + config.size['TaskBarHeight']
		x = xo - config.win['CutpropResNum'] * config.win['DeltaNewWin']
		y = yo - config.win['CutpropResNum'] * config.win['DeltaNewWin']
	 #--> Position
		self.SetPosition(pt=(x, y))
	 #--> Number of created windows
		config.win['CutpropResNum'] = config.win['CutpropResNum'] + 1
	 #--> Return
		return True
	#---

	def OnClick(self, event):
		""" To process click events """
		if event.button == 3:
	 #-->
			Tmenu = menu.ToolMenuCutPropRes(
				self.nExp, 
				self.seq, 
				self.norm, 
				self.exp, 
				self.comp
			)
	 #--> Submenus in pop up menu do not work on Windows
			if config.cOS == 'Windows':
				for i in ['Experiments', 'Compare to']:
					Tmenu.DestroyItem(Tmenu.FindItem(i))
				self.PopupMenu(Tmenu)
			else:
				pass
	 #-->
			self.PopupMenu(Tmenu)
		else:
			pass
		return True
	#---

	##-- Menu
	def OnReset(self, Mid):
		""" Reset the window 
			---
			Mid: ID of the selected menu item (int)
		"""
		self.norm = 0
		self.seq =  0
		self.exp =  0
		self.comp = None
		self.menubar.Check(503, True)
		self.menubar.Check(505, True)
		self.menubar.Check(507, True)
		self.menubar.Check(Mid+1, True)
		self.DrawConfig()
		return True
	#---

	def OnSeq(self, Mid):
		""" Change the plot if the sequence changes 
			---
			Mid: ID of the selected menu item
		"""
		self.menubar.Check(Mid, True)
		if Mid == 502:
			self.seq = 2
		else:
			self.seq = 0
		self.DrawConfig()
		return True
	#---

	def OnNorm(self, Mid):
		""" Change the plot if the normalization changes
			---
			Mid: ID of the selected menu item 
		"""
		self.menubar.Check(Mid, True)
		if Mid == 504:
			self.norm = 1
		else:
			self.norm = 0
		self.DrawConfig()
		return True
	#---

	def OnExp(self, Mid):
		""" Change the plot if experiment changes 
			---
			Mid: ID of the selected menu item (int)
		"""
		self.menubar.Check(Mid, True)
		self.exp = Mid - 507
		self.DrawConfig()
		return True
	#--- 

	def OnComp(self, Mid, rMid):
		""" Changes the plot if comp changes 
			---
			Mid: ID of the selected menu item (int)
			rMid: reference ID (int)
		"""
		self.menubar.Check(Mid, True)
		val = Mid - rMid - 1
		if val == 0:
			self.comp = None
		else:
			self.comp = val - 1 
		self.DrawConfig()
		return True
	#---

	##-- Plot
	def DrawConfig(self):
		""" Configure the plot """
	 #--> Variables
		if self.seq == 0:
			prot = 'Recombinant sequence'
		else:
			if self.natProt:
				prot = 'Native sequence'
			else:
				gmethods.NoDataImage(self)
				return True
		if self.norm == 0:
			val = 'Absolute values'
		else:
			val = 'Normalized values'
	 #--> x values
		xcol = int(self.seq / 2)
		self.x = self.data.iloc[:,xcol]
	 #--> Get exp or FP values
		if self.exp == 0:
			indy = config.cutprop['NColFPStart'] + self.seq + self.norm
			yTitle = "FP List"
			self.labelxy = 'FP List'
			self.title = (yTitle + "\n(" + prot + ", " +  val + ")")
		else:
			indy = dmethods.CalCutpropInd(self.exp) + self.seq + self.norm
			self.labelxy = 'Exp ' + str(self.exp)
			yTitle = "Experiment " + str(self.exp)
			self.title = (yTitle + "\n(" + prot + ", " +  val + ")")
		self.y = self.data.iloc[:,indy]
	 #--> Comparison
		if self.comp is None:
			self.z = None
		else:
			if self.comp == 0:
				indz = config.cutprop['NColFPStart'] + self.seq + self.norm
				self.labelxz = 'FP List'
				self.title = (yTitle + " vs FP List\n(" + prot + ", " 
					+  val + ")")
			else:
				indz = dmethods.CalCutpropInd(self.comp) + self.seq + self.norm
				self.labelxz = 'Exp ' + str(self.comp)
				self.title = (yTitle + " vs Experiment " + str(self.comp) 
					+  "\n(" + prot + ", " +  val + ")")
			self.z = self.data.iloc[:,indz]
	 #--> Coordinates of the highlight symbol
		self.charXY, self.charY = self.DrawConfigHelper(self.y)
		if self.z is None:
			pass
		else:
			self.charXZ, self.charZ = self.DrawConfigHelper(self.z)
	 #--> Draw & Return
		self.Draw() 
		return True
	#---

	def DrawConfigHelper(self, y):
		""" To set the coordinates of the * in the plot 
			---
			y: y values (list)
		"""
		maxV = y.max()
		Ty = maxV / config.cutpropU['Threshold']
		tempDF = pd.DataFrame([self.x, y]).transpose()
		tempDF = tempDF.loc[tempDF.iloc[:,1] >= Ty]
		return [tempDF.iloc[:,0].tolist(), tempDF.iloc[:,1].tolist()] 
	#---

	def Draw(self):
		""" Draw the plot """
	 #--> Clear
		self.ClearPlot()
	 #--> Title
		self.axes.set_title(self.title)
	 #--> Draw
		#---# Improve two colors to highlight the nat and rec sequence (Down)
		self.axes.plot(self.x, self.y, 'b-', label=self.labelxy)
		if self.z is None:
			pass
		else:
			self.axes.plot(self.x, self.z, 'r-', label=self.labelxz)
			self.axes.legend(loc='upper left', bbox_to_anchor=(1, 1))
		#---# Improve two colors to highlight the nat and rec sequence (Up)			
	 #--> Plot highlight
		self.DrawHelper(self.charXY, self.charY)
		if self.z is None:
			pass
		else:
			self.DrawHelper(self.charXZ, self.charZ)
	 #--> Axis, draw & return
		self.SetAxis()
		self.canvas.draw()
		return True
	#---

	def DrawHelper(self, x, y):
		""" Plot the char in the graph 
			---
			x: list with x values 
			y: list with y values
		"""
		for i in range(0, len(y)):
			self.axes.text(x[i], y[i], config.cutpropU['Char'], 
				color=config.cutpropU['CharColor'], fontweight='bold', 
				horizontalalignment='center')
		return True
	#---

	def SetAxis(self):
		""" General details of the plot area """
	 #--> Names of the axis
		self.axes.grid(True, linestyle=':')
		self.axes.set_xlabel('Residue number', fontweight='bold')
		self.axes.set_ylabel('Number of cleavages', fontweight='bold')
	 #--> Vertical lines to be removed if you managed bocolored line
		#---# Improve two colors to highlight the nat and rec sequence (Down)
		if self.seq == 0 and self.natProt:
			if self.pRes[1] is None:
				pass
			else:
				self.axes.axvline(self.pRes[1], linestyle='--',
					color=config.colors[self.name]['vline'])			
			if self.pRes[2] is None:
				pass
			else:
				self.axes.axvline(self.pRes[2], linestyle='--',
					color=config.colors[self.name]['vline'])
		elif self.seq != 0 and self.natProt:
			self.axes.axvline(self.pResNat[1], linestyle='--',
					color=config.colors[self.name]['vline'])
			self.axes.axvline(self.pResNat[2], linestyle='--',
					color=config.colors[self.name]['vline'])			
		else:
			pass
		#---# Improve two colors to highlight the nat and rec sequence (Up)
	 #-->
		self.axes.relim()
		self.axes.set_xlim([self.pRes[0], self.pRes[3]])
		self.axes.autoscale_view(scalex=False)
	 #--> Return
		return True
	#---

	def UpdateStatusBar(self, event):
		""" Updates the status bar text """
		if event.inaxes:
			x, y = event.xdata, event.ydata
			if self.seq == 0 and self.natProt:
				if x >= 1 and x <= self.pRes[3]:
					self.UpdateStatusBarHelper(x, y)
				else:
					self.statusbar.SetStatusText(gmethods.StatusBarXY(x, y))
			elif self.seq != 0 and self.natProt:
				if x >= 1 and x <= self.pResNat[3]:
					self.UpdateStatusBarHelper(x, y)
				else:
					self.statusbar.SetStatusText(gmethods.StatusBarXY(x, y))				
			elif not self.natProt:
				self.statusbar.SetStatusText(gmethods.StatusBarXY(x, y))
		else:
			self.statusbar.SetStatusText('')
		return True
	#---

	def UpdateStatusBarHelper(self, x, y):
		""" Helper tp UpdateStatusBar """ 
		xf = int(x)
		xfo = self.UpdateStatusBarHelper2(xf)
		xl = xf - 1
		if self.seq == 0:
			pass
		else:
			xl = xl - self.mist
		yf = self.y[xl]
		if self.z is None:
			zf = None
		else:
			zf = self.z[xl]
		if self.norm == 0:
			yf = '{:.0f}'.format(yf)
			try:
				zf = '{:.0f}'.format(zf)
			except Exception:
				pass
		else:
			yf = '{:.2f}'.format(yf)
			try:
				zf = '{:.2f}'.format(zf)
			except Exception:
				pass 
		if zf is None:
			self.statusbar.SetStatusText("Res = " + str(xfo) + "  "
				"Cleavages=" + str(yf))
		else:
			self.statusbar.SetStatusText("Res=" + str(xf) + "  "
				"Cleavages=(" + str(yf) + ', ' + str(zf) + ')')
		return True
	#---		

	def UpdateStatusBarHelper2(self, x):
		""" Get the residue string for status bar """
		if self.pRes[1] is None and self.pRes[2] is None:
			xo = str(x) + ' (NA)'
		else:
			if self.seq == 0:
				if self.pRes[1] <= x and x <= self.pRes[2]:
					xnat = x + self.mist
					xo = str(x) + ' (' + str(xnat) + ')'
				else:
					xo = str(x) + ' (NA)'
			else:
				if self.pResNat[1] <= x and x <= self.pResNat[2]:
					xrec = x - self.mist
					xo = str(x) + ' (' + str(xrec) + ')'
				else:
					xo = str(x) + ' (NA)'			
		return xo
	#--- 
#---





