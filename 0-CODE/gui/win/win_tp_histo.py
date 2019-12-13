# ------------------------------------------------------------------------------
#	Copyright (C) 2017-2019 Kenny Bravo Rodriguez <www.umsap.nl>
	
#	This program is distributed for free in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
	
#	See the accompaning licence for more details.
# ------------------------------------------------------------------------------


""" This module creates the Histograms utility window """


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
import config.config as config
import gui.gui_classes as gclasses
import gui.gui_methods as gmethods
import data.data_classes as dclasses 
#---


class WinHisto(gclasses.WinUtilUno):
	""" Creates the GUI for the Histograms utility. The utility generates 
		histograms from a .tarprot file 
	"""

	def __init__(self, parent=None, style=None):
		""" parent: parent of the widgets
			style: style of the windows
		"""
	 #--> Initial Setup
		self.name = config.name['Histo']
		super().__init__(parent=parent, style=style, length=17)
	 #--> Sizers
		self.sizer.Fit(self)
	 #--> Position
		self.Center()
	 #--> Show
		self.Show()
	#---

	####---- Methods of the class
	##-- Binding
	def OnClearFilesDef(self):
		""" Specific clear for Files section in this window """
		self.tcOutputFF.SetValue('NA')
		return True
	#---

	###--- Run
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
	  #--> Histogram windows
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Checking user input: Histogram windows', 1)
		if self.CheckGuiListNumber(self.TextCtrlorCBox, 
			'Histogramwindows',
			config.dictCheckFatalErrorMsg[self.name]['Histogramwindows2'],  
			t         = config.dictElemHistWin[self.name]['t'],
			comp      = config.dictElemHistWin[self.name]['comp'],
			val       = config.dictElemHistWin[self.name]['val'],
			NA        = config.dictElemHistWin[self.name]['NA'],
			Range     = config.dictElemHistWin[self.name]['Range'],
			Order     = config.dictElemHistWin[self.name]['Order'],
			Unique    = config.dictElemHistWin[self.name]['Unique'],
			DelRepeat = config.dictElemHistWin[self.name]['DelRepeat']):
			pass
		else:
			return False
		if self.do['Histogramwindows'] is not None:
			if (len(self.do['Histogramwindows']) == 1 and 
				self.do['Histogramwindows'][0] == 0):
				self.do['Histogramwindows'] = None
			else:
				pass
		else:
			pass
	 #--> Return
		return True
	#---

	def ReadInputFiles(self):
		""" Read the files and creates the dataObjects """
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Reading input files: Tarprot file', 1)
		try:
			self.tarprotObj = dclasses.DataObjTarProtFile(
				self.do['TarProtFile'])
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
	 #--> Check if there is something to write
		if self.tarprotObj.checkFP:
			wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
				'Writing output files: hist file', 1)
	 #--> Write		
			self.tarprotObj.TarProt2HistoFile(self.do['Outputfile'], 
				self.do['Histogramwindows'])
		else:
			gclasses.DlgFatalErrorMsg(
				config.dictCheckFatalErrorMsg[self.name]['FiltPept2'])
			return False
	 #--> Return			
		return True
	#---

	def ShowRes(self):
		""" Show graph results """
	 #--> Check if there is something to show & Show
		if self.tarprotObj.checkFP:
			gmethods.UpdateGaugeText(self.gauge, self.stProgress,
				'Generating graphical output', 1)			
			gmethods.WinGraphResCreate(config.name['HistoRes'], 
				self.do['Outputfile'])
		else:
			return False
	 #--> Return
		return True
	#---	
#---








	