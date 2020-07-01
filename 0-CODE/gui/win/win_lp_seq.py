# ------------------------------------------------------------------------------
#	Copyright (C) 2017 Kenny Bravo Rodriguez <www.umsap.nl>
	
#	This program is distributed for free in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
	
#	See the accompaning licence for more details.
# ------------------------------------------------------------------------------


""" This module creates the Sequence utility window for LimProt module """


#region -------------------------------------------------------------- Imports
import wx

import config.config   as config
import gui.gui_classes as gclasses
import gui.gui_methods as gmethods 
import data.data_classes as dclasses 
#endregion ----------------------------------------------------------- Imports


class WinSeqAlignLP(gclasses.WinUtilUno):
	""" Creates the GUI for the Sequence Highlight utility in LimProt. """

	#region --------------------------------------------------- Instance Setup
	def __init__(self, parent=None, style=None):
		""" parent: parent of the widgets
			style: style of the window
		"""
	 #--> Initial setup
		self.name = config.name['SeqH']
		super().__init__(parent=parent, style=style, length=16)
	 #---
	 #--> Sizers
		self.sizer.Fit(self)
	 #---
	 #--> Position
		self.Center()
	 #---
	 #--> Show	
		self.Show()
	 #---
	#---
	#endregion ------------------------------------------------ Instance Setup

	# ------------------------------------------------------------- My Methods
	#region -------------------------------------------------- Binding Methods
	def OnClearFilesDef(self):
		""" Specific clear for Files section in the window """
		self.tcOutputFF.SetValue('NA')
		return True
	#---
	#endregion ----------------------------------------------- Binding Methods

	#region ------------------------------------------------------ Run Methods
	def CheckInput(self):
		""" """
	 #--> Files
	  #--> Data file
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Checking user input: Data file', 1)
		if self.CheckGuiTcFileRead(self.tcDataFile, 
			config.dictElemDataFile[self.name]['ExtShort'], 
			'LimProtFile',
			config.dictCheckFatalErrorMsg[self.name]['LimProtFile']):
			pass
		else:
			return False
	  #---
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
	  #---
	 #---
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
	  #---
	 #---
	 #--> Return	
		return True
	 #---
	#---

	def ReadInputFiles(self):
		""" Read the files and creates the dataObjects """
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Reading input files: Limprot file', 1)
		try:
			self.fileObj = dclasses.DataObjLimProtFile(self.do['LimProtFile'])
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
		#--> Check if there is something to write before writting
		if self.fileObj.checkFP:
			wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
				'Writing output file: seq.pdf file', 1)		
			self.fileObj.LimProt2SeqPDF(self.do['Outputfile'], 
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
	#endregion --------------------------------------------------- Run Methods	
#---		