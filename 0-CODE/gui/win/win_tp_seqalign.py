# ------------------------------------------------------------------------------
#	Copyright (C) 2017-2019 Kenny Bravo Rodriguez <www.umsap.nl>
	
#	This program is distributed for free in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
	
#	See the accompaning licence for more details.
# ------------------------------------------------------------------------------


""" This module creates the Sequence alignments utility window """


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
import config.config   as config
import gui.gui_classes as gclasses
import gui.gui_methods as gmethods 
import data.data_classes as dclasses 
#---



class WinSeqAlign(gclasses.WinUtilUno):
	""" Creates the GUI for the Sequence alignments utility. The utility 
		generates sequence alignments from a .tarprot file 
	"""

	def __init__(self, parent=None, style=None):
		""" parent: parent of the widgets 
			style: style of the window
		"""
	 #--> Initial Setup
		self.name = config.name['SeqAlign']
		super().__init__(parent=parent, style=style, length=16)
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
		""" """
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
	  #--> Output folder
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Checking user input: Output folder', 1)
		if self.CheckGuiTcOutputFolder(self.tcOutputFF, 
			self.tcDataFile, 
			'Outputfolder',
			config.dictCheckFatalErrorMsg[self.name]['Outputfolder']):
			pass
		else:
			return False
	 #--> Values	
	  #--> Seq Length
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Checking user input: Sequence length', 1)
		if self.CheckGui1Number(self.TextCtrlorCBox, 
			'Sequencelength',
			config.dictCheckFatalErrorMsg[self.name]['Sequencelength'], 
			t    = config.dictElemSeqLength[self.name]['t'],
			comp = config.dictElemSeqLength[self.name]['comp'],
			NA   = config.dictElemSeqLength[self.name]['NA']):
			pass
		else:
			return False	
		return True
	#---

	def ReadInputFiles(self):
		""" Read the files and creates the dataObjects """
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Reading input files: Tarprot file', 1)
		try:
			self.fileObj = dclasses.DataObjTarProtFile(self.do['TarProtFile'])
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
	 #--> Check if there is something to write & Write
		if self.fileObj.checkFP:
			wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
				'Writing output files: txt files', 1)		
			self.fileObj.TarProt2SeqAlign(self.do['Outputfolder'], 
				self.do['Sequencelength'])
		else:
			gclasses.DlgFatalErrorMsg(
				config.dictCheckFatalErrorMsg[self.name]['FiltPept2'])
			return False		
		return True
	#---

	def ShowRes(self):
		""" Show graph results """
		return True
	#---
#---





	