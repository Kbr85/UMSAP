# ------------------------------------------------------------------------------
#	Copyright (C) 2017 Kenny Bravo Rodriguez <www.umsap.nl>
	
#	This program is distributed for free in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
	
#	See the accompaning licence for more details.
# ------------------------------------------------------------------------------


""" This module creates the Cleavages to PDB utility window """


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



class WinCuts2PDB(gclasses.WinUtilUno):
	""" Generates the pdb from a tarprot file and a pdb file """

	def __init__(self, parent=None, style=None):
		""" parent: parent for the widgets
			style: style of the windows
		"""
	 #--> Initial setup
		self.name = config.name['Cuts2PDB']
		super().__init__(parent=parent, style=style, length=18)
	 #--> Widgets
	  #--> Buttons
		self.buttonDF = wx.Button(self.boxFiles, label='PDB file')	
	  #--> TextCtrl
		self.tcDF = wx.TextCtrl(self.boxFiles, value="", 
			size=config.size['TextCtrl']['DataFile'])
	 #--> Tooltips
		msg = config.tooltip[self.name]['PDBFile'] + config.msg['OptVal']
		self.buttonDF.SetToolTip(msg)
	 #--> Sizers
	  #--> Config
		self.sizerboxFilesWid.SetRows(3)
		self.sizerboxFilesWid.Detach(self.buttonOutputFF)
		self.sizerboxFilesWid.Detach(self.tcOutputFF)
	  #--> Add
		self.sizerboxFilesWid.Add(self.buttonDF,  border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL)
		self.sizerboxFilesWid.Add(self.tcDF,  border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL)		
		self.sizerboxFilesWid.Add(self.buttonOutputFF,  border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL)
		self.sizerboxFilesWid.Add(self.tcOutputFF,  border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL)				
	  #--> Fit
		self.sizer.Fit(self)
	 #--> Position
		self.Center()
	 #--> Bind
		self.buttonDF.Bind(wx.EVT_BUTTON, self.OnDF)
	 #--> Default values
		self.tcDF.SetValue('NA')
	 #--> Show	
		self.Show()
	#---

	####---- Methods of the class
	##-- Binding
	def OnClearFilesDef(self):
		""" Specific clear for Files section in this window """
		self.tcOutputFF.SetValue('NA')
		self.tcDF.SetValue('NA')
		return True
	#---

	###--- Run
	def CheckInput(self):
		""" Check the user provided input """
	 #--> Files
	  #--> Tarprot file
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Checking user input: Data file', 1)
		if self.CheckGuiTcFileRead(self.tcDataFile, 
			config.dictElemDataFile[self.name]['ExtShort'], 
			'TarProtFile',
			config.dictCheckFatalErrorMsg[self.name]['TarProtFile']):
			pass
		else:
			return False
	  #--> PDB file
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Checking user input: Data file', 1)
		if self.CheckGuiTcFileRead(self.tcDF, 
			config.dictElemDataFile2[self.name]['ExtShort'], 
			'PDBfile',
			config.dictCheckFatalErrorMsg[self.name]['PDBfile2'],
			config.dictElemDataFile2[self.name]['NA']):
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
	  #--> PDB ID
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Checking user input: PDB ID', 1)
		if self.CheckGuiPDBID(self.TextCtrlorCBox, 
			'PDBID', 
			'PDBfile',
			config.dictCheckFatalErrorMsg[self.name]['PDBID2'], 
			NA=False):
			pass
		else:
			return False
		if self.do['PDBID'] == None:
			self.do['PDBID'] = [None, None]
		else:
			pass
	 #--> Return
		return True
	#---

	def ReadInputFiles(self):
		""" Read the files and creates the dataObjects """
	 #--> Tarprot
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Reading input files: Tarprot file', 1)
		try:
			self.fileObj = dclasses.DataObjTarProtFile(self.do['TarProtFile'])
		except Exception:
			return False
	 #--> Pdb file
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Reading input files: PDB file', 1)
		self.pdbObj = dclasses.DataObjPDBFile(self.do['PDBfile'], 
			self.do['PDBID'][0],
			self.do['PDBID'][1])
	  #--> Check that the supplied chain/segment is indeed in the PDB
		if self.CheckGuiCSinPDB(self.pdbObj, 
			self.do['PDBID'][1], 
			config.dictCheckFatalErrorMsg[self.name]['chainSInFile']):
			pass
		else:
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
		if self.fileObj.checkFP:
			wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
				'Writing output files: pdb files', 1)
	  #--> write		
			self.fileObj.TarProt2PDB(self.do['Outputfolder'], 
				pdbObj=self.pdbObj, stProgress=self.stProgress)
		else:
			gclasses.DlgFatalErrorMsg(
				config.dictCheckFatalErrorMsg[self.name]['FiltPept2'])
			return False		
	 #--> Return
		return True
	#---

	def ShowRes(self):
		""" Show graph results """
		return True
	#---		
#---













