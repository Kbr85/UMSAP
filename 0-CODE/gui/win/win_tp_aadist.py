# ------------------------------------------------------------------------------
#	Copyright (C) 2017-2019 Kenny Bravo Rodriguez <www.umsap.nl>
	
#	This program is distributed for free in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
	
#	See the accompaning licence for more details.
# ------------------------------------------------------------------------------


""" This module creates the AA distribution utility window """


# ------------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Methods
# ------------------------------------------------------------------------------



#--- Imports
## Standard modules
import wx
## My modules
import config.config     as config
import gui.gui_classes   as gclasses
import gui.gui_methods   as gmethods
import data.data_classes as dclasses
#---



class WinAAdist(gclasses.WinUtilUno):
	""" Creates the GUI for the AA distribution utility. The utility generates 
		the distributions from a .tarprot file """
	
	def __init__(self, parent=None, style=None):
		""" parent: parent of the widgets
			style: style of the windows
		"""
	 #--> Initial setup
		self.name = config.name['AAdist']
		super().__init__(parent=parent, style=style, length=17)
	 #--> Sizers
		self.sizer.Fit(self)
	 #--> Position
		self.Center()
	 #--> Show
		self.Show()
	#---

	####---- Methods of the class
	##-- Binding here of parent classes
	def OnClearFilesDef(self):
		""" """
		if config.dictElemOutputFileFolder[self.name]['NA']:
			self.tcOutputFF.SetValue('NA')
		else:
			pass
		return True
	#---

	##-- Run
	def CheckInput(self):
		""" Check the user provided input """
	 #--> Files
	  #--> Data file
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Checking user input: Data file', 1)
		if self.CheckGuiTcFileRead(self.tcDataFile, 
			config.dictElemDataFile[self.name]['ExtShort'], 
			'TarProtFile',
			config.dictCheckFatalErrorMsg[self.name]['TarProtFile']):
			pass
		else:
			return False
	  #--> Output file
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Checking user input: Output file', 1)
		if self.CheckGuiTcOutputFile(self.tcOutputFF, 
			self.tcDataFile, 
			config.dictElemOutputFileFolder[self.name]['DefNameFile'],
			config.dictElemOutputFileFolder[self.name]['ExtShort'], 
			'Outputfile',
			config.dictCheckFatalErrorMsg[self.name]['OutputFile']):
			pass
		else:
			return False
	 #--> Values		
	  #--> Positions
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Checking user input: Positions', 1)
		if self.CheckGui1Number(self.TextCtrlorCBox, 
			'Positions',
			config.dictCheckFatalErrorMsg[self.name]['Positions2'], 
			t=config.dictElemPositions[self.name]['t'],
			comp=config.dictElemPositions[self.name]['comp'], 
			NA=config.dictElemPositions[self.name]['NA']):
			pass
		else:
			return False
	 #--> Return
		return True
	#---

	def ReadInputFiles(self):
		""" Read the files and creates the dataObjects """
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Reading input files: Tarprot file', 1)
		try:
			self.tarprotObj = dclasses.DataObjTarProtFile(self.do['TarProtFile'])
		except Exception:
			return False
		return True
	#---

	def SetVariable(self):
		""" Set extra needed variables """
		return True
	#---

	def RunAnalysis(self):
		""" Run the analysis """
		return True
	#---

	def WriteOF(self):
		""" Write the output """
	 #--> Check if there is something to write & write
		if self.tarprotObj.checkFP:
			wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
				'Writing output files: aadist file', 1)		
			self.tarprotObj.TarProt2AAdist(self.do['Outputfile'], 
				self.do['Positions'])
		else:
			gclasses.DlgFatalErrorMsg(
				config.dictCheckFatalErrorMsg[self.name]['FiltPept2'])
			return False
	 #--> Return			
		return True
	#---

	def ShowRes(self):
		""" Show graph results """
	 #--> Check if there is something to show & show
		if self.tarprotObj.checkFP:
			gmethods.UpdateGaugeText(self.gauge, self.stProgress,
			'Generating graphical output', 1)
			gmethods.WinGraphResCreate(config.name['AAdistR'],
				self.do['Outputfile'])
		else:
			return False
	 #--> Return
		return True
	#---	
#---




	