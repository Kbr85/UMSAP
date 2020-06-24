# ------------------------------------------------------------------------------
#	Copyright (C) 2017 Kenny Bravo Rodriguez <www.umsap.nl>
	
#	This program is distributed for free in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
	
#	See the accompaning licence for more details.
# ------------------------------------------------------------------------------


""" This module creates the window for the TarProt module of the app """


#region -------------------------------------------------------------- Imports
import wx
import pandas as pd

import config.config      as config
import gui.menu.menu      as menu
import gui.gui_classes    as gclasses
import gui.gui_methods    as gmethods
import data.data_classes  as dclasses
import data.data_methods  as dmethods
#endregion ----------------------------------------------------------- Imports


class WinTarProt(gclasses.WinModule):
	""" Creates the window for the TarProt module of the app. """ 

	#region --------------------------------------------------- Instance Setup
	def __init__(self, parent=None, style=None):
		""" parent: parent of the widgets
			style: style of the windows
		"""
	 #--> Initial Setup
		self.name  = config.name['TarProt']
		super().__init__(parent=parent, style=style)
	 #---
	 #--> Variables
		self.CType = config.combobox['ControlType'][0] # Needed for self.CheckGuiResultControl
	 #---
	 #--> Menu
		self.menubar = menu.MainMenuBarWithTools(self.name)
		self.SetMenuBar(self.menubar)
	 #---
	 #--> Sizers
	  #--> Central static boxes
	   #--> Files
		self.sizerboxFilesWid = wx.FlexGridSizer(6, 2, 1, 1)
		self.sizerboxFiles.Add(self.sizerboxFilesWid,    border=2, 
			flag=wx.ALIGN_CENTER_HORIZONTAL|wx.ALL)
		self.sizerboxFilesWid.Add(self.buttonDataFile,  border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL)
		self.sizerboxFilesWid.Add(self.tcDataFile,      border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerboxFilesWid.Add(self.buttonSeqRecFile, border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL)
		self.sizerboxFilesWid.Add(self.tcSeqRecFile,     border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerboxFilesWid.Add(self.buttonSeqNatFile, border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL)
		self.sizerboxFilesWid.Add(self.tcSeqNatFile,     border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerboxFilesWid.Add(self.buttonPDBFile,    border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL)
		self.sizerboxFilesWid.Add(self.tcPDBFile,        border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerboxFilesWid.Add(self.buttonOutputFF,  border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL)
		self.sizerboxFilesWid.Add(self.tcOutputFF,      border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerboxFilesWid.Add(self.buttonOutName,    border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL)
		self.sizerboxFilesWid.Add(self.tcOutName,        border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)		
	   #---
	   #--> Values
		self.sizerboxValuesWid = wx.FlexGridSizer(4, 4, 1, 1)
		self.sizerboxValues.Add(self.sizerboxValuesWid, border=2, 
			flag=wx.ALIGN_CENTER_HORIZONTAL|wx.ALL)
		self.sizerboxValuesWid.Add(self.stTarprot,   border=2, 
			flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL)
		self.sizerboxValuesWid.Add(self.tcTarprot,   border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerboxValuesWid.Add(self.stScoreVal,  border=2, 
			flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL)
		self.sizerboxValuesWid.Add(self.tcScoreVal,  border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerboxValuesWid.Add(self.stDataNorm,  border=2, 
			flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL)
		self.sizerboxValuesWid.Add(self.cbDataNorm,  border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerboxValuesWid.Add(self.staVal,      border=2, 
			flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL)
		self.sizerboxValuesWid.Add(self.cbaVal,      border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerboxValuesWid.Add(self.stPositions, border=2, 
			flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL)
		self.sizerboxValuesWid.Add(self.tcPositions, border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerboxValuesWid.Add(self.stSeqLength, border=2, 
			flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL)
		self.sizerboxValuesWid.Add(self.tcSeqLength, border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerboxValuesWid.Add(self.stHistWin  , border=2, 
			flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL)
		self.sizerboxValuesWid.Add(self.tcHistWin  , border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerboxValuesWid.Add(self.stPDB      , border=2, 
			flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL)
		self.sizerboxValuesWid.Add(self.tcPDB      , border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
	   #---
	   #--> Columns
		self.sizerboxColumnsWid = wx.GridBagSizer(1, 1)
		self.sizerboxColumns.Add(self.sizerboxColumnsWid, border=2, 
			flag=wx.ALIGN_CENTER_HORIZONTAL|wx.ALL)
		self.sizerboxColumnsWid.Add(self.stSeq,           pos=(0,0), border=2, 
			flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL)
		self.sizerboxColumnsWid.Add(self.tcSeq,           pos=(0,1), border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL, span=(0,2))		
		self.sizerboxColumnsWid.Add(self.stDetProt,       pos=(1,0), border=2, 
			flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL)
		self.sizerboxColumnsWid.Add(self.tcDetProt,       pos=(1,1), border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL, span=(0,2))
		self.sizerboxColumnsWid.Add(self.stScore,         pos=(2,0), border=2, 
			flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL)
		self.sizerboxColumnsWid.Add(self.tcScore,         pos=(2,1), border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL, span=(0,2))
		self.sizerboxColumnsWid.Add(self.stColExt,        pos=(3,0), border=2, 
			flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL)
		self.sizerboxColumnsWid.Add(self.tcColExt,        pos=(3,1), border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL, span=(0,2))
		self.sizerboxColumnsWid.Add(self.stResults,       pos=(4,0), border=2, 
			flag=wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL|wx.ALL,
			span=(0,2))		
		self.sizerboxColumnsWid.Add(self.buttonResultsW,  pos=(5,0), border=2, 
			flag=wx.ALIGN_RIGHT|wx.ALL)
		self.sizerboxColumnsWid.Add(self.tcResults,       pos=(5,1), border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerboxColumnsWid.Add(self.buttonResultsL,  pos=(5,2), border=2, 
			flag=wx.ALIGN_RIGHT|wx.ALL)
	   #---
	  #---
	  #--> Fit
		self.sizer.Fit(self)
	  #---
	 #---
	 #--> Tooltips
		self.stResults.SetToolTip(config.tooltip[self.name]['Results'])
	 #---
	 #--> Bind
		self.buttonPDBFile.Bind(wx.EVT_BUTTON, self.OnPDBFile)
		for child in self.GetChildren():
			child.Bind(wx.EVT_RIGHT_DOWN, self.OnPopUpMenu)
	 #---
	 #--> Initial default values
		self.tcSeqNatFile.SetValue('NA')
		self.tcPDBFile.SetValue('NA')
		self.tcPositions.SetValue('NA')  
		self.tcSeqLength.SetValue('NA') 
		self.tcHistWin.SetValue('NA') 
		self.tcPDB.SetValue('NA')
		self.tcScoreVal.SetValue('0') 
	 #---
		
	 
	 #--> INITIAL VALUES FOR TESTING. DELETE BEFORE RELEASING!!!!!!!! ##########
		import getpass
		user = getpass.getuser()
		if config.cOS == 'Darwin':
			self.tcDataFile.SetLabel('/Users/' + str(user) + '/TEMP-GUI/BORRAR-UMSAP/PlayDATA/TARPROT/Mod-Enz-Dig-data-ms.txt')
			self.tcSeqRecFile.SetLabel('/Users/' + str(user) + '/TEMP-GUI/BORRAR-UMSAP/PlayDATA/TARPROT/Mod-Enz-Dig-data-seq.txt')
			self.tcOutputFF.SetLabel('/Users/' + str(user) + '/TEMP-GUI/BORRAR-UMSAP/PlayDATA/test')
		elif config.cOS == 'Windows':
			from pathlib import Path
			self.tcDataFile.SetLabel(str(Path('C:/Users/bravo/Desktop/SharedFolders/BORRAR-GUI/PlayDATA/TarProt/Mod-Enz-Dig-data-ms.txt'))) 
			self.tcSeqRecFile.SetLabel(str(Path('C:/Users/bravo/Desktop/SharedFolders/BORRAR-GUI/PlayDATA/TarProt/Mod-Enz-Dig-data-seq.txt')))
			self.tcOutputFF.SetLabel(str(Path('C:/Users/bravo/Desktop/SharedFolders/BORRAR-GUI/PlayDATA/test2')))
		# 	#self.tcPDBFile.SetLabel(str(Path('C:/Users/bravo/Downloads/2y4f-kbr.pdb')))
		self.tcSeqNatFile.SetLabel('P31545')
		#self.tcSeqNatFile.SetLabel('NA')
		self.tcPDB.SetLabel('NA')       
		self.tcOutName.SetLabel('myTarTest')
		self.tcTarprot.SetLabel('efeB')   
		self.tcScoreVal.SetLabel('200')  
		self.tcPositions.SetLabel('5')  
		self.tcSeqLength.SetLabel('100') 
		self.tcHistWin.SetLabel('50')
		#self.tcPDB.SetLabel('2y4f;A')       
		self.tcPDB.SetLabel('NA')       
		self.tcSeq.SetLabel('0')       
		self.tcDetProt.SetLabel('38')   
		self.tcScore.SetLabel('44')     
		self.tcColExt.SetLabel('0 1 2 3 4-10')
		self.tcResults.SetLabel('98-105; 109-111; 112 113 114; 115-117 120')
		#self.tcResults.SetLabel('98-104; 106 107; 108 109; 110 111; 112 113; 114 115; 116 117; 118 119')
	 #--- INITIAL VALUES FOR TESTING. DELETE BEFORE RELEASING!!!!!!!! ##########
	 
	 
	 #--> Show
		self.Show()
	 #---
	#---
	#endregion ------------------------------------------------ Instance Setup

	# ------------------------------------------------------------- My Methods
	#region -------------------------------------------------- Binding Methods
	def OnClearFilesDef(self):
		""" Specific clear for Files section for this module """
		self.tcPDBFile.SetValue('NA')
		self.tcOutputFF.SetValue('NA')
		self.tcOutName.SetValue('NA')
		self.tcSeqNatFile.SetValue('NA')
		self.lb.DeleteAllItems()
		return True
	#---

	def OnClearValuesDef(self):
		""" Specific clear for Values in this module """
		self.cbDataNorm.SetValue('Log2')
		self.cbaVal.SetValue('0.050')
		self.tcPositions.SetValue('NA')
		self.tcHistWin.SetValue('NA')
		self.tcSeqLength.SetValue('NA')
		self.tcPDB.SetValue('NA')
		self.tcScoreVal.SetValue('0') 
		return True
	#---

	def OnClearColumnsDef(self):
		""" Specific clear for Column section for this module """
		self.tcColExt.SetValue('NA')
		return True
	#---

	def OnPDBFile(self, event):
		""" Select the pdb file """
		if gmethods.TextCtrlFromFF(self.tcPDBFile, 
			msg=config.msg['Open']['PDBFile'], wcard=config.extLong['PDB']):
			return True
		else:
			return False
	#---
	#endregion ----------------------------------------------- Binding Methods

	#region ----------------------------------------------------- Menu Methods
	def OnPopUpMenu(self, event):
		""" Show the pop up menu in the wx.ListCtrl. Binding is done in
			the base class 
		"""
		self.PopupMenu(menu.ToolMenuTarProtMod())
		return True
	#---

	def OnSaveInputF(self):
		""" Save the .uscr file with the data in the window """
	 #--> Variables
		k = True
		dlg = gclasses.DlgSaveFile(config.extLong['Uscr'])
	 #---
		if dlg.ShowModal() == wx.ID_OK:
		 #--> Initial data & path to the uscr file
			temp = {
				          'Data file' :   self.tcDataFile.GetValue(),       
				     'Sequence (rec)' : self.tcSeqRecFile.GetValue(),     
				     'Sequence (nat)' : self.tcSeqNatFile.GetValue(),     
				           'PDB file' :    self.tcPDBFile.GetValue(),         
				      'Output folder' :   self.tcOutputFF.GetValue(),   
				        'Output name' :    self.tcOutName.GetValue(),     
				     'Target protein' :    self.tcTarprot.GetValue(),  
				        'Score value' :   self.tcScoreVal.GetValue(), 
				 'Data normalization' :   self.cbDataNorm.GetValue(),
				            'a-value' :       self.cbaVal.GetValue(),               
				          'Positions' :  self.tcPositions.GetValue(),     
				    'Sequence length' :  self.tcSeqLength.GetValue(), 
				  'Histogram windows' :    self.tcHistWin.GetValue(),   
				             'PDB ID' :        self.tcPDB.GetValue(),          
				           'Sequence' :        self.tcSeq.GetValue(),    
				  'Detected proteins' :    self.tcDetProt.GetValue(),   
				              'Score' :      self.tcScore.GetValue(),          
				 'Columns to extract' :     self.tcColExt.GetValue(),   
				            'Results' :    self.tcResults.GetValue(),
				             'Module' : config.mod[config.name['TarProt']]	
			}
	 	 #---
	 	 #--> Write
			if dmethods.FFsWriteDict2Uscr(dlg.GetPath(), iDict=temp):
				k = True
			else:
				k = False
		 #---
		else:
			k = False
	 #--> Destroy & Return
		dlg.Destroy()
		return k
	 #---
	#---
	#endregion -------------------------------------------------- Menu Methods

	#region ------------------------------------------------------ Run Methods
	def CheckInput(self):
		""" """
	 #--> Files and Folders
	  #--> Data file
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Checking user input: Data file', 1)
		if self.CheckGuiTcFileRead(self.tcDataFile, 
			config.dictElemDataFile[self.name]['ExtShort'], 
			'Datafile',
			config.dictCheckFatalErrorMsg[self.name]['Datafile']):
			pass
		else:
			return False
	  #---
	  #--> Sequence (rec)
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Checking user input: Sequence (rec)', 1)
		if self.CheckGuiTcSeqFileCode(self.tcSeqRecFile,
			config.dictElemSeqRec[self.name]['ExtShort'], 
			'Seq_rec',
			config.dictCheckFatalErrorMsg[self.name]['Seq_rec']):
			pass
		else:
			return False		
	  #---
	  #--> Sequence (nat)
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Checking user input: Sequence (nat)', 1)
		if self.CheckGuiTcSeqFileCode(self.tcSeqNatFile,
			config.dictElemSeqNat[self.name]['ExtShort'], 
			'Seq_nat',
			config.dictCheckFatalErrorMsg[self.name]['Seq_nat'],
			NA=config.dictElemSeqNat[self.name]['NA']):
			pass
		else:
			return False		
	  #---
	  #--> PDB file
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Checking user input: PDB file', 1)
		if self.CheckGuiTcFileRead(self.tcPDBFile,
			config.dictElemPdbFile[self.name]['ExtShort'], 
			'PDBfile',
			config.dictCheckFatalErrorMsg[self.name]['PDBfile'],
			NA=config.dictElemPdbFile[self.name]['NA']):
			pass
		else:
			return False
	  #---
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
	  #---
	  #--> Output name
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Checking user input: Output name', 1)
		if self.CheckGuiStrNotEmpty(self.tcOutName, 
			'Outputname',
			config.dictCheckFatalErrorMsg[self.name]['Outputname'], 
			config.dictElemOutputFileFolder[self.name]['DefNameFile']):
			pass
		else:
			return False		
	  #---
	 #---
	 #--> Values
	  #--> Target protein
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Checking user input: Target protein', 1)
		if self.CheckGuiStrNotEmpty(self.tcTarprot, 
			'Targetprotein',
			config.dictCheckFatalErrorMsg[self.name]['Targetprotein']):
			pass
		else:
			return False
	  #---	
	  #--> Score value
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Checking user input: Score value', 1)
		if self.CheckGui1Number(self.tcScoreVal, 
			'Scorevalue',
			config.dictCheckFatalErrorMsg[self.name]['Scorevalue']):
			pass
		else:
			return False	
	  #---
	  #--> Data normalization
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Checking user input: Data normalization', 1)
		cbal = self.cbDataNorm.GetValue()
		if cbal == 'None':
			cbalO = None
		else:
			cbalO = cbal
		self.d['Datanorm'] = cbal
		self.do['Datanorm'] = cbalO
	  #---
	  #--> alpha value
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Checking user input: alpha value', 1)
		cbal = self.cbaVal.GetValue()
		self.d['aVal'] = cbal
		self.do['aVal'] = float(cbal)
	  #---
	  #--> Positions
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Checking user input: Positions', 1)
		if self.CheckGui1Number(self.tcPositions, 
			'Positions',
			config.dictCheckFatalErrorMsg[self.name]['Positions'], 
			t    = config.dictElemPositions[self.name]['t'],
			comp = config.dictElemPositions[self.name]['comp'],
			NA   = config.dictElemPositions[self.name]['NA']):
			pass
		else:
			return False
	  #---
	  #--> Sequence length
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Checking user input: Sequence length', 1)
		if self.CheckGui1Number(self.tcSeqLength, 
			'Sequencelength',
			config.dictCheckFatalErrorMsg[self.name]['Sequencelength'], 
			t    = config.dictElemSeqLength[self.name]['t'],
			comp = config.dictElemSeqLength[self.name]['comp'],
			NA   = config.dictElemSeqLength[self.name]['NA']):
			pass
		else:
			return False
	  #---
	  #--> Histogram windows
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Checking user input: Histogram windows', 1)
	   #--> General Check
		if self.CheckGuiListNumber(self.tcHistWin, 
			'Histogramwindows',
			config.dictCheckFatalErrorMsg[self.name]['Histogramwindows'],  
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
	   #---
	   #--> When only one value if 0 --> None
		if self.do['Histogramwindows'] is not None:
			if (len(self.do['Histogramwindows']) == 1 and 
				self.do['Histogramwindows'][0] == 0):
				self.do['Histogramwindows'] = None
			else:
				pass
		else:
			pass
	   #---
	  #---
	  #--> PDB ID
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Checking user input: PDB ID', 1)
		if self.CheckGuiPDBID(self.tcPDB, 
			'PDBID', 
			'PDBfile',
			config.dictCheckFatalErrorMsg[self.name]['PDBID']):
			pass
		else:
			return False
		if self.do['PDBID'] == None:
			self.do['PDBID'] = [None, None]
		else:
			pass
	  #---
	 #---
	 #--> Columns
	  #--> Sequences
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Checking user input: Sequences', 1)
		if self.CheckGui1Number(self.tcSeq, 
			'SeqCol',
			config.dictCheckFatalErrorMsg[self.name]['SeqCol'], 
			t    = config.dictElemSeqCol[self.name]['t'],
			comp = config.dictElemSeqCol[self.name]['comp'],
			val  = config.dictElemSeqCol[self.name]['val'],
			NA   = config.dictElemSeqCol[self.name]['NA']):
			pass
		else:
			return False
	  #---		
	  #--> Detected protein
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Checking user input: Detected proteins', 1)
		if self.CheckGui1Number(self.tcDetProt, 
			'DetectProtCol',
			config.dictCheckFatalErrorMsg[self.name]['DetectProtCol'], 
			t    = config.dictElemDetectProtCol[self.name]['t'],
			comp = config.dictElemDetectProtCol[self.name]['comp'],
			val  = config.dictElemDetectProtCol[self.name]['val'],
			NA   = config.dictElemDetectProtCol[self.name]['NA']):
			pass
		else:
			return False		
	  #---
	  #--> Score
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Checking user input: Score', 1)
		if self.CheckGui1Number(self.tcScore, 
			'ScoreCol',
			config.dictCheckFatalErrorMsg[self.name]['ScoreCol'], 
			t    = config.dictElemScoreCol[self.name]['t'],
			comp = config.dictElemScoreCol[self.name]['comp'],
			val  = config.dictElemScoreCol[self.name]['val'],
			NA   = config.dictElemScoreCol[self.name]['NA']):
			pass
		else:
			return False
	  #---
	  #--> Columns to extract
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Checking user input: Columns to extract', 1)		
		if self.CheckGuiListNumber(self.tcColExt, 
			'ColExtract',
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
	  #---
	  #--> Results 
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Checking user input: Results', 1)
	   #--> Check
		if self.CheckGuiResultControl(
			self.tcResults,
			'Results',
			config.dictCheckFatalErrorMsg[self.name]['Results'],
			t         = config.dictElemResultsTP[self.name]['t'],
			comp      = config.dictElemResultsTP[self.name]['comp'],
			val       = config.dictElemResultsTP[self.name]['val'],
			Range     = config.dictElemResultsTP[self.name]['Range'],
			Order     = config.dictElemResultsTP[self.name]['Order'],
			Unique    = config.dictElemResultsTP[self.name]['Unique'],
			DelRepeat = config.dictElemResultsTP[self.name]['DelRepeat'],
			NA        = config.dictElemResultsTP[self.name]['NA'],
			Rep       = config.dictElemResultsTP[self.name]['Replicates'],
			):
			pass
		else:
			return False
	   #---
	   #--> Final setting
		self.do['Control'] = dmethods.ListFlatNLevels(self.do['Control'],1)[1]
		self.do['Results'] = dmethods.ListFlatNLevels(self.do['Results'],1)[1]
	   #---
	  #---
	 #---
	 #--> Repeating element
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Checking user input: Unique column numbers', 1)
		l = ([self.do['SeqCol']] + [self.do['DetectProtCol']] 
			 + [self.do['ScoreCol']] + self.do['Control']
			 + dmethods.ListFlatNLevels(self.do['Results'],1)[1]
		)
		if self.CheckGuiListUniqueElements(l, 
			config.dictCheckFatalErrorMsg[self.name]['Unique']):
			pass
		else:
			return False
	 #---
	 #--> Variables needed below
		self.l = l 
		if self.do['ColExtract'] == None:
			self.lcExt = self.l
		else:
			self.lcExt = self.l + self.do['ColExtract']
	 #---
	 #--> Return
		return True
	 #---
	#---					

	def ReadInputFiles(self):
		""" """
	 #--> Data file
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Reading input files: Data file', 1)
		try:
			self.dataFileObj = dclasses.DataObjDataFile(self.do['Datafile'])
		except Exception:
			return False
	 #---
	 #--> Check column numbers
		if self.CheckGuiColNumbersInDataFile(self.lcExt, self.dataFileObj.nCols,
			config.dictCheckFatalErrorMsg[self.name]['ColNumber']):
			pass
		else:
			return False
	 #---
	 #--> Seq rec file
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Reading input files: Recombinant sequence', 1)
		try:
			self.recSeqObj = dclasses.DataObjSequenceFile(
				seqP=self.do['Seq_rec'])
		except Exception as e:
			return False
	 #---
	 #--> Seq nat file
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Reading input files: Native sequence', 1)
		if self.do['Seq_nat'] != None:
			try:
				self.natSeqObj = dclasses.DataObjSequenceFile(
					seqP=self.do['Seq_nat'])
			except Exception as e:
				return False
		else:
			pass
	 #---
	 #--> PDB file
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Reading input files: PDB file', 1)
		if self.do['PDBID'][1] == None:
			pass
		else:
			self.pdbObj = dclasses.DataObjPDBFile(self.do['PDBfile'], 
				self.do['PDBID'][0], self.do['PDBID'][1])
	  #--> Check that the supplied chain/segment is indeed in the PDB
			if self.CheckGuiCSinPDB(self.pdbObj, self.do['PDBID'][1], 
				config.dictCheckFatalErrorMsg[self.name]['chainSInFile']):
				pass
			else:
				return False
	  #---
	 #---
	 #-->
		return True
	 #---
	#---

	def SetVariable(self):
		""" """
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Setting up the analysis: Data frame', 1)
	 #--> Dict for data frame type assigment
		self.DtypeDictBuilder()
	 #---
	 #--> Data frame	
		out, self.dataV = dmethods.DFSelFilterNSet(self.dataFileObj.dataFrame,
			self.l, 
			[self.do['Targetprotein'], self.do['Scorevalue']], 
			[self.header[self.do['DetectProtCol']], 
			 self.header[self.do['ScoreCol']]],
			['eq', 'ge',], self.name, self.dtypeDict)
		if out:
			pass
		else:
			return False
	 #---
	 #--> Data frame dimension
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Setting up the analysis: Data frame dimension', 1)
		self.tentry, self.tcol = self.dataV.shape
	 #---
	 #--> Sequences
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Setting up the analysis: Recombinant sequence', 1)
		self.recSeqSeq = self.recSeqObj.seq
		self.do['RecSeq'] = self.recSeqSeq
		if self.do['Seq_nat'] == None:
			pass
		else:
			self.natSeqSeq = self.natSeqObj.seq
	 #---
	 #--> Seq Length
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Setting up the analysis: Sequence lengths', 1)
		if self.do['Seq_nat'] == None:
			self.do['protSeqLength'] = (self.recSeqObj.seqLength, None)
		else:
			self.do['protSeqLength'] = (self.recSeqObj.seqLength, 
			self.natSeqObj.seqLength)
	 #---
	 #--> Prot Loc & mist
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Setting up the analysis: Protein location and mistmatch', 1)
		if self.do['Seq_nat'] == None:
			self.do['mist'] = None
			self.do['ProtLoc'] = [None, None]
		else:			
			out, self.do['ProtLoc'], self.do['mist'] = (
				self.recSeqObj.GetprotLocmist(self.natSeqSeq))
			if out:
				pass
			else:
				return False
	 #---
	 #--> nExp
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Setting up the analysis: Number of experiments', 1)
		self.nExp = len(self.do['Results'])
	 #---
	 #--> Output header
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Setting up the analysis: Output header', 1)
		i = 0
		self.colOut, self.colOutExpIndex = dmethods.ListColHeaderTarProtFile(
			self.nExp)
	 #---
	 #--> Return
		return True
	 #---
	#---

	def DtypeDictBuilder(self):
		""" Creates the dtype dict to convert the data type in the dataFrame """
	 #--> Get columns name
		self.header = self.dataFileObj.header
	 #---
	 #--> Create dict
		self.dtypeDict = {
			self.header[self.do['SeqCol']] : 'object',
			self.header[self.do['DetectProtCol']] : 'object',
			self.header[self.do['ScoreCol']] : 'float'
		}
		for a in self.do['Control']:
			self.dtypeDict[self.header[a]] = 'float'
		#--- Flat Results list
		out, res = dmethods.ListFlatNLevels(self.do['Results'])
		for a in res:
			self.dtypeDict[self.header[a]] = 'float'
	 #---
	 #--> Return
		return True
	 #---
	#---

	def RunAnalysis(self):
		""" """	
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Running the analysis', 1)
	 #--> Normalize
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Running the analysis: Normalizing data', 1)
		out, self.dataN = dmethods.DataNorm(self.dataV, 
			sel=list(range(config.tarprot['SColNorm'], self.tcol, 1)),
			method=self.do['Datanorm'])
		if out:
			pass
		else:
			return False
	 #---
	 #--> Run analysis
		rows = []
		i = 1
		for row in self.dataN.itertuples(index=False):
			msg = 'Running the analysis: ' + str(i) + ' / ' + str(self.tentry)  
			wx.CallAfter(gmethods.UpdateText, self.stProgress, msg)
			out, trow = self.RunAnalysisFunction(row)
			if out:
				rows.append(trow)
			else:
				return False
			i += 1
	 #---
	 #--> Create & sort data frame
		self.dataO = pd.DataFrame(rows, columns=self.colOut)
		self.dataO.sort_values(by=config.tarprot['SortBy'], inplace=True)
		self.dataO.reset_index(drop=True, inplace=True)
	 #---
	 #--> Return
		return True
	 #---
	#---

	def RunAnalysisFunction(self, row):
		""" Helper to RunAnalysis. row has the same order as self.l 
			--- 
			row: row from the data frame to analyse
		"""
	 #--> Output list
		rowO = []
	 #---
	 #--> N, C, Nfix and Cfix
		tseq = row[0]
		tscore = row[2]
		out = self.recSeqObj.FindSeq(tseq)
		if out[0]:
			rowO.append(out[1])
			rowO.append(out[2])
			if self.do['ProtLoc'][0] is None:
				rowO.append(None)
				rowO.append(None)
			else:
				if (out[1] >= self.do['ProtLoc'][0] and 
					out[1] <= self.do['ProtLoc'][1]):
					rowO.append(out[1] + self.do['mist'])
				else:
					rowO.append(None)
				if (out[2] >= self.do['ProtLoc'][0] and 
					out[2] <= self.do['ProtLoc'][1]):
					rowO.append(out[2] + self.do['mist'])
				else:
					rowO.append(None)
		else:
			msg = config.dictCheckFatalErrorMsg[self.name]['NoPeptInRecSeq']
			gclasses.DlgFatalErrorMsg(msg, seq=tseq)
			return [False]
	 #---
	 #--> Control
		control = []
		s = 3
		for k, j in enumerate(self.do['Control']):
			control.append(row[s])
			s += 1
		rowO.append(control)
	 #---
	 #--> Exp
		for j in self.do['Results']:
			exp = []
			for k in j:
				exp.append(row[s])
				s += 1
			
			res = dmethods.StatAncova(control, exp, self.do['aVal'], self.name)

			resexp = []
			resexp.append(res)
			resexp.append(exp)
			rowO.append(resexp) 
	 #---
	 #--> Sequence and Score
		rowO.append(tseq)
		rowO.append(tscore)
	 #---
	 #--> Return
		return [True, rowO]
	 #---
	#---

	def WriteOF(self):
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Writing output files', 1)
	 #--> Create output folder
		self.do['Outputfolder'].mkdir()
	 #---
	 #--> Intermediate files
		folderD = self.do['Outputfolder'] / 'Data_Steps'
		folderD.mkdir()
		file = folderD / 'data-00-Extract.txt'
		dmethods.FFsWriteCSV(file, self.dataV)
		file = folderD / 'data-01-Norm.txt'
		dmethods.FFsWriteCSV(file, self.dataN)
		file = folderD / 'data-02-Results.txt'
		dmethods.FFsWriteCSV(file, self.dataO)		
	 #---
	 #--> tarprot file
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Writing output files: tarprot file', 1)
		name = self.do['Outputname'] + config.extShort['TarProt'][0]
		self.tarprotFile = self.do['Outputfolder'] / name
		data = {
			'V' : config.dictVersion, 
			'I'  : self.d,
			'CI' : dmethods.DictVal2String(self.do, 
				keys2string=config.tarprot['StringKeys']),
			'R' : self.dataO.to_dict()
			}
		dmethods.FFsWriteJSON(self.tarprotFile, data)
	 #---
	 #--> Create tarprot object
		self.tarprotObj = dclasses.DataObjTarProtFile(self.tarprotFile)
	 #---
	 #--> uscr file
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Writing output files: uscr file', 1)
		self.uscrFile = self.tarprotFile.with_suffix(config.extShort['Uscr'][0])
		dmethods.FFsWriteDict2Uscr(self.uscrFile,
			iDict=self.tarprotObj.Fdata['I'],
			hDict=config.dictUserInput2UscrFile[self.name]
		)
	 #---
	 #--> Short data files
		if self.do['ColExtract'] is None:
			pass
		else:
			msg = 'Writing output files: short data files'
			wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress, 
				msg, 1)
			self.dataOutFolder = self.do['Outputfolder'] / 'Data'
			self.dataOutFolder.mkdir()
			self.tarprotObj.ToSDataFile(self.dataOutFolder)
	 #---
	 #--> Check if there is something else to write
		if self.tarprotObj.checkFP:
	  	 #--> filtpept file
			wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
				'Writing output files: filtpept file', 1)
			self.filtpeptFile = self.tarprotFile.with_suffix(
				config.extShort['FiltPept'][0])
			self.tarprotObj.TarProt2FiltPept(self.filtpeptFile)
		 #---
	  	 #--> cutprop file
			wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
				'Writing output files: cutprop file', 1)
			self.cutpropFile = self.tarprotFile.with_suffix(
				config.extShort['CutProp'][0])
			self.tarprotObj.TarProt2CutProp(self.cutpropFile)
		 #---
	  	 #--> aadist file
			if self.do['Positions'] is None:
				pass
			else:
				wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, 
					self.stProgress, 'Writing output files: aadist file', 1)
				self.aadistFile = self.tarprotFile.with_suffix(
					config.extShort['AAdist'][0])
				if self.tarprotObj.TarProt2AAdist(self.aadistFile):
					pass
				else:
					return False
	  	 #---
		 #--> histograms				
			if self.do['Histogramwindows'] is None:
				pass
			else:
				msg = 'Writing output files: histogram files'
				wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, 
					self.stProgress, msg, 1)
				self.histoFile = self.tarprotFile.with_suffix(
					config.extShort['Histo'][0])
				self.tarprotObj.TarProt2HistoFile(self.histoFile)
		 #---
	  	 #--> sequence alignments
			if self.do['Sequencelength'] is None:
				pass
			else:
				msg = 'Writing output files: sequence alignment files'
				wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, 
					self.stProgress, msg, 1)
				self.seqAOutFolder = self.do['Outputfolder'] / 'Sequences'
				self.seqAOutFolder.mkdir()
				self.tarprotObj.TarProt2SeqAlign(self.seqAOutFolder)
	  	 #---
		 #--> PDB
			if self.do['PDBID'][1] is None:
				pass
			else:
				msg = 'Writing output files: pdb files'
				wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, 
					self.stProgress, msg, 1)
				self.pdbOutFolder = self.do['Outputfolder'] / 'PDB'
				self.pdbOutFolder.mkdir()
				self.tarprotObj.TarProt2PDB(self.pdbOutFolder, self.pdbObj, 
					self.recSeqObj, self.stProgress)
		else:
			gclasses.DlgFatalErrorMsg(
				config.msg['Errors']['FiltPept'],
				nothing='E',
			)
			return False
	 #---
	 #--> Return
		return True		
	 #---
	#---

	def ShowRes(self):
		""" Show the graphical output if any """
		gmethods.UpdateGaugeText(self.gauge, self.stProgress,
			'Generating graphical output', 1)
	 #--> Check if there is anything to show
		if self.tarprotObj.checkFP:
	 	 #--> .tarprot
			gmethods.UpdateGaugeText(self.gauge, self.stProgress,
				'Generating graphical output: tarprot file', 1)
			wx.Yield()
			gmethods.WinGraphResCreate(config.name['TarProtRes'], 
				self.tarprotFile)	
	 	 #---
		 #--> cutprop
			gmethods.UpdateGaugeText(self.gauge, self.stProgress,
				'Generating graphical output: cutprop file', 1)
			wx.Yield()
			gmethods.WinGraphResCreate(config.name['CutPropRes'], 
				self.cutpropFile)
		 #---
		 #--> histo
			if self.do['Histogramwindows'] != None:
				gmethods.UpdateGaugeText(self.gauge, self.stProgress,
					'Generating graphical output: histo file', 1)
				wx.Yield()
				gmethods.WinGraphResCreate(config.name['HistoRes'], 
					self.histoFile)
			else:
				pass
		 #---
	 	 #--> aadist
			if self.do['Positions']:
				gmethods.UpdateGaugeText(self.gauge, self.stProgress,
					'Generating graphical output: aadist file', 1)
				wx.Yield()
				gmethods.WinGraphResCreate(config.name['AAdistR'], 
					self.aadistFile)							
			else:
				pass
		 #---
		else:
			pass
	 #---
	 #--> Return
		return True
	 #---
	#---
	#endregion --------------------------------------------------- Run Methods
#---













