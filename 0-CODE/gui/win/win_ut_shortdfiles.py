# ------------------------------------------------------------------------------
#	Copyright (C) 2017-2019 Kenny Bravo Rodriguez <www.umsap.nl>
	
#	This program is distributed for free in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
	
#	See the accompaning licence for more details.
# ------------------------------------------------------------------------------


""" This module creates the Short Data Files utility window """


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



class WinShortDataFiles(gclasses.WinUtilUno):
	""" Creates the GUI for the Short data file utility. The utility generates 
		short data files from a module main output file and a data file 
	"""

	def __init__(self, parent=None, style=None):
		""" parent: parent for the widgets
			style: style of the window
		"""
	 #--> Initial Setup
		self.name = config.name['ShortDFile']
		super().__init__(parent=parent, style=style, length=17)
	 #--> Variables
		self.folder = True
	 #--> Widgets
	  #--> Buttons
		self.buttonDF = wx.Button(self.boxFiles, label='Data file')	
	  #--> TextCtrl
		self.tcDF = wx.TextCtrl(self.boxFiles, value="", 
			size=config.size['TextCtrl']['DataFile'])
	  #--> Rename
		self.boxValues.SetLabel(config.msg['StaticBoxNames']['Columns'])
		self.buttonClearValues.SetLabel('Clear columns')
	 #--> Tooltips
		self.buttonClearValues.SetToolTip(config.tooltip['Clear']['Cols'])
		msg = config.tooltip[self.name]['DataFile'] + config.msg['OptVal']
		self.buttonDF.SetToolTip(msg)
	 #--> Sizers
	  #--> Configure
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
		""" Specific clear for File section ni this window """
		self.tcOutputFF.SetValue('NA')
		self.tcDF.SetValue('NA')
		return True
	#---

	def OnDataFile(self, event):
		""" Select the data file and fill the list box.
			Overwrite to gclasses.ElementDataFile
		"""
	 #--> Variables
		k = True
		msg   = config.dictElemDataFile[self.name]['MsgOpenFile']
		wcard = config.dictElemDataFile[self.name]['ExtLong']
	 #--> Open File & Change GUI and variables based on file extension
		dlg = gclasses.DlgOpenFile(msg, wcard)
		if dlg.ShowModal() == wx.ID_OK:
	  #--> Put path in wx.TextCtrl
			self.tcDataFile.SetValue(dlg.GetPath())
	  #--> Get extension
			ext = dlg.GetPath().split('.')[-1].strip()
			if ext == 'protprof':
				self.buttonOutputFF.SetLabel('Output file')
				msg = (
					config.msg['Button']['OutputFileUMSAPFile']
					+ config.msg['OptVal']
				)
				self.buttonOutputFF.SetToolTip(msg)
				self.buttonOutputFF.Bind(wx.EVT_BUTTON, self.OnOutputFile)
				self.folder = False
			else:
				self.buttonOutputFF.SetLabel('Output folder')
				msg = (
					config.dictElemOutputFileFolder[self.name]['ButtonTooltip']
					+ config.msg['OptVal']
				)
				self.buttonOutputFF.SetToolTip(msg)		
				self.buttonOutputFF.Bind(wx.EVT_BUTTON, self.OnOutputFolder)		
				self.folder = True
		else:
			k = False
	  #--- Destroy & Return
		dlg.Destroy()
		return k
	#---	

	###--- Run
	def CheckInput(self):
		""" Check the user provided input """
	 #--> Files
	  #--> UMSAP file
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Checking user input: UMSAP file', 1)
	   #--> Check file
		if self.CheckGuiTcFileRead(self.tcDataFile, 
			config.dictElemDataFile[self.name]['ExtShort'], 
			'UMSAPFile',
			config.dictCheckFatalErrorMsg[self.name]['UMSAPFile']):
			pass
		else:
			return False
	   #--> Get extension of the file
		self.ext = self.do['UMSAPFile'].suffix
	  #--> Data file
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Checking user input: Data file', 1)
		if self.CheckGuiTcFileRead(self.tcDF, 
			config.dictElemDataFile2[self.name]['ExtShort'], 
			'DataFile',
			config.dictCheckFatalErrorMsg[self.name]['DataFile'],
			config.dictElemDataFile2[self.name]['NA']):
			pass
		else:
			return False			
	  #--> Output folder | file
		if self.folder:
			wx.CallAfter(
				gmethods.UpdateGaugeText, 
				self.gauge, 
				self.stProgress,
				'Checking user input: Output folder', 
				1
			)
			if self.CheckGuiTcOutputFolder(
				self.tcOutputFF, 
				self.tcDataFile, 
				'Outputfolder',
				config.dictCheckFatalErrorMsg[self.name]['Outputfolder']
			):
				pass
			else:
				return False
		else:
			wx.CallAfter(
				gmethods.UpdateGaugeText, 
				self.gauge, 
				self.stProgress,
				'Checking user input: Output file', 
				1
			)
			if self.CheckGuiTcOutputFile(
				self.tcOutputFF, 
				self.tcDataFile, 
				config.dictElemOutputFileFolder[self.name]['DefNameFile'],
				config.dictElemOutputFileFolder[self.name]['ExtShort'],
				'Outputfolder',
				config.dictCheckFatalErrorMsg[self.name]['Outputfile'],
			):
				pass
			else:
				return False			
	 #--> Values
	  #--> Columns to extract
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Checking user input: Columns to extract', 1)		
		if self.CheckGuiListNumber(self.TextCtrlorCBox, 'ColExtract',
			config.dictCheckFatalErrorMsg[self.name]['ColExtract'],  
			t         = config.dictElemColExtract[self.name]['t'],
			comp      = config.dictElemColExtract[self.name]['comp'],
			val       = config.dictElemColExtract[self.name]['val'],
			NA        = config.dictElemColExtract[self.name]['NA'],
			Range     = config.dictElemColExtract[self.name]['Range'],
			Order     = config.dictElemColExtract[self.name]['Order'],
			Unique    = config.dictElemColExtract[self.name]['Unique'],
			DelRepeat = config.dictElemColExtract[self.name]['DelRepeat']):
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
			self.fileObj = config.pointer['dclasses']['DataObj'][self.ext](self.do['UMSAPFile'])
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
			if self.fileObj.ToSDataFile(
				self.do['Outputfolder'], 
				colOut=self.do['ColExtract'], 
				dataF=self.do['DataFile']
			):
				pass
			else:
				return False
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
