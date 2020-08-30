# ------------------------------------------------------------------------------
#	Copyright (C) 2017 Kenny Bravo Rodriguez <www.umsap.nl>
	
#	This program is distributed for free in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
	
#	See the accompaning licence for more details.
# ------------------------------------------------------------------------------


""" This module creates the window for the ProtProf module of the app """


#region -------------------------------------------------------------- Imports
import pandas as pd
import numpy  as np
import wx
from scipy import stats
from statsmodels.stats.multitest import multipletests 

import config.config        as config
import gui.menu.menu        as menu
import gui.gui_classes      as gclasses
import gui.gui_methods      as gmethods
import data.data_classes    as dclasses 
import data.data_methods    as dmethods
import checks.checks_single as check
#endregion ----------------------------------------------------------- Imports


class WinProtProf(gclasses.WinModule):
	""" To create the gui for the Proteome Profiling module """

	#region --------------------------------------------------- Instance Setup
	def __init__(self, parent=None, style=None):
		""" parent: parent for the widgets
			style: style of the window
		"""
	 #--> Initial Setup 
		self.name         = config.name['ProtProf']
		self.CType        = None # This will be set by the window typing the 
		self.LabelControl = None # column numbers, when loading column numbers 
		self.LabelCond    = None # from a txt or from a uscr 
		self.LabelRP      = None # 
		super().__init__(parent=parent, name=self.name, style=style, length=53)
	 #---
	 #--> Widgets
	  #--> Destroy widgets needed by other modules but not here
		self.WidgetsDestroy(self.name)
	  #---
	  #--> StaticText
		self.stChB     = wx.StaticText(self.boxValues, label='Median correction')
		self.stCorrP   = wx.StaticText(self.boxValues, label='P correction')
		self.stGeneN   = wx.StaticText(self.boxColumns, label='Gene names')
		self.stExclude = wx.StaticText(
			self.boxColumns, 
			label='Exclude proteins'
		)
	  #---
	  #--> CheckBox
		self.chb = wx.CheckBox(self.boxValues, label='')
		self.chb.SetValue(True)
	  #---
	  #--> TextCtrl		
		self.tcGeneN = wx.TextCtrl(
			self.boxColumns, 
			value='', 
			size=config.size['TextCtrl']['ColumnsSect']
		)
		self.tcExclude = wx.TextCtrl(
			  self.boxColumns,
			  value='',
			  size=config.size['TextCtrl']['ColumnsSect']
		)
	  #---		
	  #--> Combobox. #---->>>>>>>> This will be moved to gclasses.WinModule when extending the p values correction to all modules
		self.cbCorrP = wx.ComboBox(self.boxValues, 
			value='Benjamini - Hochberg',  
			choices=config.combobox['CorrectP'], 
			style=wx.CB_READONLY
		)
	  #---
	 #---
	 #--> Dict for menu
		self.ColDic = {
			1: self.tcDetProt,
			2: self.tcGeneN, 
			3: self.tcScore, 
			4: self.tcExclude,
			5: self.tcColExt,
		}
	 #---
	 #--> Sizers
	  #--> Central static boxes
	   #--> Files
		self.sizerboxFilesWid = wx.FlexGridSizer(3, 2, 1, 1)
		self.sizerboxFiles.Add(self.sizerboxFilesWid,    border=2, 
			flag=wx.ALIGN_CENTER_HORIZONTAL|wx.ALL)
		self.sizerboxFilesWid.Add(self.buttonDataFile,  border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL)
		self.sizerboxFilesWid.Add(self.tcDataFile,      border=2, 
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
		self.sizerboxValuesWid = wx.GridBagSizer(1, 1)
		self.sizerboxValues.Add(self.sizerboxValuesWid, border=2, 
			flag=wx.ALIGN_CENTER_HORIZONTAL|wx.ALL)
		self.sizerboxValuesWid.Add(self.stScoreVal,  pos=(0,0), border=2, 
			flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL)
		self.sizerboxValuesWid.Add(self.tcScoreVal,  pos=(0,1), border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerboxValuesWid.Add(self.stDataNorm,  pos=(1,0), border=2, 
			flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL)
		self.sizerboxValuesWid.Add(self.cbDataNorm,  pos=(1,1), border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerboxValuesWid.Add(self.stChB,       pos=(0,2), border=2, 
			flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.ALL)		
		self.sizerboxValuesWid.Add(self.chb,         pos=(0,3), border=2, 
			flag=wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
		self.sizerboxValuesWid.Add(self.stCorrP,     pos=(1,2), border=2, 
			flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.ALL)		
		self.sizerboxValuesWid.Add(self.cbCorrP,     pos=(1,3), border=2, 
			flag=wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)			
	   #---
	   #--> Columns
		self.sizerboxColumnsWid = wx.GridBagSizer(1, 1)
		self.sizerboxColumns.Add(self.sizerboxColumnsWid, border=2, 
			flag=wx.ALIGN_CENTER_HORIZONTAL|wx.ALL)	
		self.sizerboxColumnsWid.Add(self.stDetProt,      pos=(0,0), border=2, 
			flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL)
		self.sizerboxColumnsWid.Add(self.tcDetProt,      pos=(0,1), border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL, span=(0,2))
		self.sizerboxColumnsWid.Add(self.stGeneN,        pos=(1,0), border=2, 
			flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL)
		self.sizerboxColumnsWid.Add(self.tcGeneN,        pos=(1,1), border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL, span=(0,2))			
		self.sizerboxColumnsWid.Add(self.stScore,        pos=(2,0), border=2, 
			flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL)
		self.sizerboxColumnsWid.Add(self.tcScore,        pos=(2,1), border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL, span=(0,2))
		self.sizerboxColumnsWid.Add(self.stExclude,      pos=(3,0), border=2, 
			flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL)
		self.sizerboxColumnsWid.Add(self.tcExclude,      pos=(3,1), border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL, span=(0,2))			
		self.sizerboxColumnsWid.Add(self.stColExt,       pos=(4,0), border=2, 
			flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL)
		self.sizerboxColumnsWid.Add(self.tcColExt,       pos=(4,1), border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL, span=(0,2))
		self.sizerboxColumnsWid.Add(self.stResults,      pos=(5,0), border=2, 
			flag=wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, span=(0,2))		
		self.sizerboxColumnsWid.Add(self.buttonResultsW, pos=(6,0), border=2, 
			flag=wx.ALIGN_RIGHT|wx.ALL)
		self.sizerboxColumnsWid.Add(self.tcResults,      pos=(6,1), border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerboxColumnsWid.Add(self.buttonResultsL, pos=(6,2), border=2, 
			flag=wx.ALIGN_RIGHT|wx.ALL)		
	  #---
	  #--> Fit
		self.sizer.Fit(self)
	  #---
	 #---
	 #--> Tooltips
		self.stScoreVal.SetToolTip(config.tooltip[self.name]['ScoreVal'])
		self.stResults.SetToolTip(config.tooltip[self.name]['Results'])
		self.buttonOutName.SetToolTip(
			config.tooltip[self.name]['OutName'] + config.msg['OptVal'])
		self.stChB.SetToolTip(config.tooltip[self.name]['MedianCorrection'])
		self.stCorrP.SetToolTip(config.tooltip[self.name]['CorrP'])
		self.stGeneN.SetToolTip(config.tooltip[self.name]['GeneN'])
		self.stExclude.SetToolTip(
			config.tooltip[self.name]['Exclude'] + config.msg['OptVal'])
	 #---
	 #--> Binding
		if config.cOS != 'Windows':
			for child in self.GetChildren():
				child.Bind(wx.EVT_RIGHT_DOWN, self.OnPopUpMenu)
		else:
			pass
	 #---
	 #--> Default values
		self.tcOutputFF.SetValue('NA')
		self.tcOutName.SetValue('NA')
		self.tcScoreVal.SetValue('0') 
		self.cbDataNorm.SetValue('Log2')
		self.chb.SetValue(False)
		self.cbCorrP.SetValue('Benjamini - Hochberg')
		self.tcExclude.SetValue('NA')
		self.tcColExt.SetValue('NA')
	 #---

	 
	 #--> INITIAL VALUES FOR TESTING. DELETE BEFORE RELEASING!!!!!!!! ##########
		import getpass
		user = getpass.getuser()
		if config.cOS == 'Darwin':
			self.tcDataFile.SetLabel('/Users/' + str(user) + '/TEMP-GUI/BORRAR-UMSAP/PlayDATA/PROTPROF/proteinGroups-kbr.txt') 
			self.tcOutputFF.SetLabel('/Users/' + str(user) + '/TEMP-GUI/BORRAR-UMSAP/PlayDATA/test')
		elif config.cOS == 'Windows':
			from pathlib import Path
			self.tcDataFile.SetLabel(str(Path('C:/Users/bravo/Desktop/SharedFolders/BORRAR-UMSAP/PlayDATA/PROTPROF/proteinGroups-kbr.txt'))) 
			self.tcOutputFF.SetLabel(str(Path('C:/Users/bravo/Desktop/SharedFolders/BORRAR-UMSAP/PlayDATA/test')))
		else:
			pass
		self.tcOutName.SetValue('myProtTest')
		self.tcScoreVal.SetValue('320')
		self.chb.SetValue(True)
		self.cbCorrP.SetValue('Benjamini - Hochberg')
		self.tcDetProt.SetValue('0')
		self.tcGeneN.SetValue('6')   
		self.tcScore.SetValue('39')     
		self.tcColExt.SetValue('0 1 2 3 4-10')
		self.tcExclude.SetValue('171 172 173')
	   #--> One Control per Row
		# self.tcResults.SetValue('105 115 125, 106 116 126, 101 111 121; 130 131 132, 108 118 128, 103 113 123')         
		# self.CType = 'One Control per Row'
		# self.LabelControl = 'MyControl'
		# self.LabelCond    = ['DMSO', 'H2O']
		# self.LabelRP      = ['30min', '1D']
	   #--> One Control        
		#self.tcResults.SetValue('105 115 125; 106 116 126, 101 111 121; 108 118 128, 103 113 123')
		#self.CType = 'One Control'
		#self.LabelControl = 'MyControl'
		#self.LabelCond    = ['DMSO', 'H2O']
		#self.LabelRP      = ['30min', '1D']
	   #--> One Control per Column, 3 Cond and 2 TP
		# self.tcResults.SetValue('105 115 125, 130 131 132; 106 116 126, 101 111 121; 108 118 128, 103 113 123; 100 110 120, 102 112 122')
		# self.CType = 'One Control per Column'
		# self.LabelControl = 'MyControl'
		# self.LabelCond    = ['DMSO', 'H2O', 'MeOH']
		# self.LabelRP      = ['30min', '1D']		 
	   #--> One Control per Column, 2 Cond and 2 TP
		self.tcResults.SetValue('105 115 125, 130 131 132; 106 116 126, 101 111 121; 108 118 128, 103 113 123')
		self.CType = 'One Control per Column'
		self.LabelControl = 'MyControl'
		self.LabelCond    = ['DMSO', 'H2O']
		self.LabelRP      = ['30min', '1D']		 		
	 #--- INITIAL VALUES FOR TESTING. DELETE BEFORE RELEASING!!!!!!!! ##########


	 #--> Show
		self.Show()
	 #---
	#---

	# ------------------------------------------------------------- My Methods  
	#region -------------------------------------------------- Binding Methods
	def OnClearFilesDef(self):
		""" Specific clear for Files in this module """
		self.tcOutputFF.SetValue('NA')
		self.tcOutName.SetValue('NA')
		self.lb.DeleteAllItems()
		return True
	#---

	def OnClearValuesDef(self):
		""" Specific clear for Values in this module """
		self.tcScoreVal.SetValue('0')
		self.cbDataNorm.SetValue('Log2')
		self.chb.SetValue(False)
		self.cbCorrP.SetValue('Benjamini - Hochberg')
		return True
	#---

	def OnClearColumnsDef(self):
		""" Specific clear for Columns in this module """
		self.tcExclude.SetValue('NA')
		self.tcColExt.SetValue('NA')
		self.CType        = None
		self.LabelControl = None
		self.LabelCond    = None
		self.LabelRP      = None
		return True
	#---
	#endregion ----------------------------------------------- Binding Methods

	#region ----------------------------------------------------- Menu Methods
	def OnSaveInputF(self):
		""" Save the .uscr file with the data in the window """
	 #--> Variables
		k = True
		dlg = gclasses.DlgSaveFile(config.extLong['Uscr'])
	 #---
		if dlg.ShowModal() == wx.ID_OK:
	 	 #--> Dict with values
			temp = {
				          'Data file' : self.tcDataFile.GetValue(),               
				      'Output folder' : self.tcOutputFF.GetValue(),   
				        'Output name' :  self.tcOutName.GetValue(),     
				        'Score value' : self.tcScoreVal.GetValue(),
				 'Data normalization' : self.cbDataNorm.GetValue(),
				  'Median correction' :        self.chb.GetValue(),
				       'P correction' :    self.cbCorrP.GetValue(),              
				  'Detected proteins' :  self.tcDetProt.GetValue(),
						 'Gene names' :    self.tcGeneN.GetValue(),    
				              'Score' :    self.tcScore.GetValue(),
				   'Exclude proteins' :  self.tcExclude.GetValue(),         
				 'Columns to extract' :   self.tcColExt.GetValue(),  		 
				            'Results' :  self.tcResults.GetValue(),
						 'Conditions' : ', '.join(self.LabelCond),      
					'Relevant Points' : ', '.join(self.LabelRP),        
					  'Control Label' : self.LabelControl,
					   'Control Type' :	self.CType, 						
				             'Module' : config.mod[config.name['ProtProf']]	
			}
		 #---
	 	 #--> Write to file
			if dmethods.FFsWriteDict2Uscr(dlg.GetPath(), iDict=temp):
				k = True
			else:
				k = False
		 #---
		else:
			k = False
	 #--> Destroy dlg & Return 
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
	  #--> median correction
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Checking user input: median correction', 1)
		self.d['median'] = self.do['median'] = self.chb.GetValue()
	  #---
	  #--> P correction
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Checking user input: P values correction', 1)
		self.d['CorrP']  = self.cbCorrP.GetValue()
		if self.d['CorrP'] == 'None':
			self.do['CorrP'] = None
		else:
			self.do['CorrP'] = self.d['CorrP']
	  #---
	 #---
	 #--> Columns
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
	  #--> Gene name
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Checking user input: Gene names', 1)
		if self.CheckGui1Number(self.tcGeneN, 
			'GeneNCol',
			config.dictCheckFatalErrorMsg[self.name]['GeneNCol'], 
			t    = config.dictElemGeneNCol[self.name]['t'],
			comp = config.dictElemGeneNCol[self.name]['comp'],
			val  = config.dictElemGeneNCol[self.name]['val'],
			NA   = config.dictElemGeneNCol[self.name]['NA']):
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
	  #--> Exclude proteins
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Checking user input: Exclude proteins', 1)		
		if self.CheckGuiListNumber(self.tcExclude, 
			'ExcludeCol',
			config.dictCheckFatalErrorMsg[self.name]['ExcludeCol'],  
			t         = config.dictElemExclude[self.name]['t'],
			comp      = config.dictElemExclude[self.name]['comp'],
			val       = config.dictElemExclude[self.name]['val'],
			NA        = config.dictElemExclude[self.name]['NA'],
			Range     = config.dictElemExclude[self.name]['Range'],
			Order     = config.dictElemExclude[self.name]['Order'],
			Unique    = config.dictElemExclude[self.name]['Unique'],
			DelRepeat = config.dictElemExclude[self.name]['DelRepeat']):
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
	  #---
	 #---
	 #--> Repeating element
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Checking user input: Unique column numbers', 1)
	  #--> Main list
		self.l = ([self.do['GeneNCol']]
					+ [self.do['DetectProtCol']] 
					+ [self.do['ScoreCol']]
					+ list(set(dmethods.ListFlatNLevels(self.do['Control'], 1)[1]))
					+ dmethods.ListFlatNLevels(self.do['Results'], 2)[1])
	  #---
	  #--> Include excluded columns 
		if self.do['ExcludeCol'] != None:
			self.le = self.l + self.do['ExcludeCol']
		else:
			self.le = self.l
	  #---
	  #--> Check
		if self.CheckGuiListUniqueElements(self.le, 
			config.dictCheckFatalErrorMsg[self.name]['Unique'],
			NA=config.dictElemResultsTP[self.name]['NA']):
			pass
		else:
			return False
	  #---
	 #---
	 #--> Small variables needed further below
		if self.do['ColExtract'] != None:
			self.lcExt = self.le + self.do['ColExtract']							
		else:
			self.lcExt = self.le
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
	  #--> Read
		try:
			self.dataFileObj = dclasses.DataObjDataFile(self.do['Datafile'])
		except Exception:
			return False
	  #---
	  #--> Check number of columns
		if self.CheckGuiColNumbersInDataFile(self.lcExt, self.dataFileObj.nCols,
			config.dictCheckFatalErrorMsg[self.name]['ColNumber'],
			NA=config.dictElemResultsTP[self.name]['NA']):
			pass
		else:
			return False
	  #---
	 #---
	 #--> Return
		return True
	 #---
	#---

	def SetVariable(self):
		""" """
	 #--> Control design
		self.d['LabelCond']    = ', '.join(self.LabelCond)
		self.d['LabelRP']      = ', '.join(self.LabelRP)
		self.do['LabelCond']   = self.LabelCond
		self.do['LabelRP']     = self.LabelRP
		self.d['CType']        = self.do['CType']        = self.CType
		self.d['LabelControl'] = self.do['LabelControl'] = self.LabelControl
	 #---
	 #--> Small variables needed further below
		self.do['NCond']  = len(self.do['LabelCond'])
		self.do['NTimeP'] = len(self.do['LabelRP'])
		self.lNoNa = [x for x in self.l if x != None]
	 #---
	 #--> Column names in the data file
		self.header = self.dataFileObj.header	
	 #---
	 #--> Data frame with the original data
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Setting up the analysis: Initial dataframe', 1)
	  #--> Create dict to assign data type
		self.DtypeDictBuilder()
	  #---
	  #--> Create data frame
		out, self.dataV = dmethods.DFSelSet(
			self.dataFileObj.dataFrame,
			self.lNoNa, 
			self.dtypeDict,
			self.name,
		)
		if out:
			if self.do['ExcludeCol'] != None:
				for col in self.do['ExcludeCol']:
					newCol = self.header[col]
					self.dataV[newCol] = self.dataFileObj.dataFrame[newCol]
			else:
				pass
		else:
			return False
	  #---
	 #---
	 #--> Variables to configure the output dataframe
		if self.do['CType'] == config.combobox['ControlType'][1]:
			self.do['Xv']  = self.do['NTimeP']
			self.do['Yv']  = self.do['NCond']
		else:
			self.do['Xv']  = self.do['NCond']
			self.do['Yv']  = self.do['NTimeP']
		self.do['Xtp'] = self.do['NTimeP']
		self.do['Ytp'] = self.do['NCond']
	 #---
	 #--> output header
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Setting up the analysis: Output header', 1)
		out, self.colOut = dmethods.ListColHeaderProtProfFile(
			self.do['Xv'],
			self.do['Yv'],
			self.do['Xtp'],
			self.do['Ytp'],)
		if out:
			pass
		else:
			return False
	 #---
	 #--> MyTuples. To configure the loops of the self.do['ResultsControl] matrix
	 #	  (x, y, X, Y) x, y coordinates in tc.Results list of list
	 #                 X, Y labels in the output dataframe
		self.do['MyTuples'] = {
			'v'   : [],
			'tpds': [],
			'tpp' : [],
		}
	  #--> vds
		for x in range(0, self.do['Xv'],1):
			for y in range(0, self.do['Yv']+1, 1):
				a = (
					x,
					y,
					'X'+str(x+1),
					'Y'+str(y),
				)
				self.do['MyTuples']['v'].append(a)
	  #---
	  #--> tpds
		if self.do['CType'] == config.combobox['ControlType'][1]:
			for x in range(0, self.do['Xtp'], 1):
				for y in range(1, self.do['Ytp']+1, 1):
					a = (
						x,
						y,
						'T'+str(x+1),
						'C'+str(y),
					)
					self.do['MyTuples']['tpds'].append(a)
		else:
			for x in range(0, self.do['Ytp'], 1):
				for y in range(1, self.do['Xtp']+1, 1):
					a = (
						x,
						y,
						'T'+str(y),
						'C'+str(x+1),
					)
					self.do['MyTuples']['tpds'].append(a)
	  #---
	  #--> tpp
		if self.do['CType'] == config.combobox['ControlType'][1]:
			for x in range(0, self.do['Xtp'], 1):
				l = []
				for y in range(1, self.do['Ytp']+1, 1):
					l.append((x,y))
				a = (
					l,
					'T'+str(x+1),
					'C0',
				)
				self.do['MyTuples']['tpp'].append(a)
		else:
			for y in range(1, self.do['Xtp']+1, 1):
				l = []
				for x in range(0, self.do['Ytp'], 1):
					l.append((x,y))
				a = (
					l,
					'T'+str(y),
					'C0',
				)
				self.do['MyTuples']['tpp'].append(a)
	  #---
	 #---
	 #---->>>> To avoid calculating it when creating the protprofObj
		self.do['loga'] = 0 - np.log10(0.05)
		self.do['ZscoreVal'] = stats.norm.ppf(1 - 0.1)
	 #---
	 #--> Return
		return True	
	 #---
	#---

	def DtypeDictBuilder(self):
		""" Creates the dtype dict to convert the data type in the dataFrame """
	 #--> Create the dict
		self.dtypeDict = {
			self.header[self.do['GeneNCol']] : 'object',
			self.header[self.do['DetectProtCol']] : 'object',
			self.header[self.do['ScoreCol']] : 'float'
		}
		for k, a in enumerate(self.l):
			if k > 1 and a != None:
				self.dtypeDict[self.header[a]] = 'float'
			else:
				pass
	 #---
	 #--> Return
		return True
	 #---
	#---

	def RunAnalysis(self):	
		""" """
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Running the analysis', 1)
	 #--> Remove proteins found in Exclude proteins
		if self.do['ExcludeCol'] != None:
			# a = self.dataFileObj.dataFrame.iloc[:,self.do['ExcludeCol']] == '+'
			# a = a.loc[(a==True).any(axis=1)]
			# idx = a.index
			a = self.dataV == '+'
			a = a.loc[(a==True).any(axis=1)]
			idx = a.index
			self.dataVP = self.dataV.drop(index=idx)
		else:
			self.dataVP = self.dataV
	 #---
	 #--> Remove proteins that where not identified in all experiments
		self.dataVP = self.dataVP.loc[~(self.dataVP==0).any(axis=1)]
	 #---
	 #--> Filter data by Score value
		out, self.dataVPS = dmethods.DFColValFilter(
			self.dataVP,
			self.do['Scorevalue'],
			self.header[self.do['ScoreCol']],
			comp='ge',
			loc=True,	
		)
	 #---
	 #--> Data frame dimensions. Here because self.dataV must be filter by 
	 #    proteins identified in all experiments and score first
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Running the analysis: Data frame dimension', 1)
		self.tentry, self.tcol = self.dataVPS.shape				
		if self.tentry == 0:
			msg = config.dictCheckFatalErrorMsg[self.name]['NoResults']
			gclasses.DlgFatalErrorMsg(msg, nothing='E')
			return False
		else:
			pass
	 #---
	 #--> Normalize
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Running the analysis: Normalizing data', 1)
		if self.do['ExcludeCol'] != None:
			end = self.tcol - len(self.do['ExcludeCol'])
		else:
			end = self.tcol
		out, self.dataVPSN = dmethods.DataNorm(self.dataVPS, 
			sel=list(range(config.protprof['SColNorm'], end, 1)),
			method=self.do['Datanorm'])
		if out:
			pass
		else:
			return False
	 #---
	 #--> Median correction
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Running the analysis: Median correction', 1)
		self.dataVPSNM = self.dataVPSN.copy()			
		if self.do['median']:
			self.dataVPSNM.iloc[:,config.protprof['SColNorm']:] = self.dataVPSNM.iloc[:,config.protprof['SColNorm']:].div(self.dataVPSNM.iloc[:,config.protprof['SColNorm']:].median(axis=0))
		else:
			pass
	 #---
	 #--> Ratios
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Running the analysis: Calculating ratios', 1)
		out, self.dataVPSNMR = dmethods.DataCalcRatios(self.dataVPSNM, 
			self.do['ResultsControl'], self.header)
		if out:
			pass
		else:
			return False
	 #---
	 #--> Run analysis
	  #--> Empty data frame
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Running the analysis: Empty dataframe for results', 1)
		self.dataO = pd.DataFrame(np.nan, columns=self.colOut, index=range(self.tentry))
	  #---
	  #--> Gene names	
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Running the analysis: Extracting Gene names', 1)
		a = self.dataFileObj.header[self.do['GeneNCol']]
		self.dataO[('Gene', 'Gene', 'Gene')] = self.dataVPSNM.loc[:,a]
	  #---
	  #--> Protein Names	
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Running the analysis: Extracting Protein names', 1)
		a = self.dataFileObj.header[self.do['DetectProtCol']]			
		self.dataO[('Protein', 'Protein', 'Protein')] = self.dataVPSNM.loc[:,a]
	  #---
	  #--> Scores	
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Running the analysis: Extracting Scores', 1)
		a = self.dataFileObj.header[self.do['ScoreCol']]			
		self.dataO[('Score', 'Score', 'Score')] = self.dataVPSNM.loc[:,a]
	  #---
	  #--> Ave & Sd
	   #--> v region of the df
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Running the analysis: Calculating averages and standard deviations (1/2)', 1)
		for z in self.do['MyTuples']['v']:
			x,y,a,b = z
			colN = [self.header[h] for h in self.do['ResultsControl'][x][y]]
			dfl = self.dataVPSNM.loc[:,colN]
			self.dataO.loc[:,('v', a, b, 'ave')] = dfl.mean(axis=1, skipna=True).to_numpy()
			self.dataO.loc[:,('v', a, b, 'sd')]  = dfl.std(axis=1, skipna=True).to_numpy()
	   #---
	   #--> tp region of the df
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Running the analysis: Calculating averages and standard deviations (2/2)', 1)	  
		for z in self.do['MyTuples']['tpds']:
			x,y,a,b = z
			colN = [self.header[h] for h in self.do['ResultsControl'][x][y]]
			dfl = self.dataVPSNMR.loc[:,colN]
			self.dataO.loc[:,('tp', a, b,  'ave')] = dfl.mean(axis=1, skipna=True).to_numpy()
			self.dataO.loc[:,('tp', a, b,  'sd')] = dfl.std(axis=1, skipna=True).to_numpy()
	  #---
	  #--> Fold changes and intra condition p value
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Running the analysis: Calculating FC and p values', 1)
	   #--> Variables
		t = self.do['NCond'] * (self.do['NTimeP'])
		c = 1
		k, l, m, n, o, p, q = config.protprof['ColOut']
		for z in self.do['MyTuples']['v']:
			x,y,a,b = z		
	   	 #--> Get reference labels and length
			if y == 0:
				pass
			else:
				ref = [self.header[h] for h in self.do['ResultsControl'][x][0]]
				lref = len(ref)
	   	 #---
		 #--> Check the time point			
				if self.do['ResultsControl'][x][y][0] == None:
					pass
				else:
	   			 #--> Update msg
					msg = ("Running the analysis: Calculating FC and p values ("
						+ str(c) + "/" + str(t) + ")")
					wx.CallAfter(gmethods.UpdateText, self.stProgress, msg)
	   			 #---
				 #--> Get relevant points label and length
					tp = [self.header[h] for h in self.do['ResultsControl'][x][y]]
					ltp = len(tp)
	   			 #---
				 #--> Data Frame section
					dfl = self.dataVPSNM.loc[:,ref+tp]
	   			 #---
				 #--> Calculate p values & FC
					self.dataO[('v', a, b, k)] = dfl.apply(self.TTest, axis=1, raw=True, args=(lref, ltp))
					self.dataO[('v', a, b, o)] = self.dataO[('v', a, b, 'ave')] / self.dataO[('v', a, 'Y0', 'ave')]
				 #---
				c += 1
	   #---
	   #--> Apply log
		idx = pd.IndexSlice
		self.dataO.loc[:,idx['v',:,:,l]] = -1 * np.log10(self.dataO.loc[:,idx['v',:,:,k]].astype('float64')).to_numpy()
		self.dataO.loc[:,idx['v',:,:,p]] = np.log2(self.dataO.loc[:,idx['v',:,:,o]].astype('float64')).to_numpy()
	   #---
	  #---
	  #--> Z scores
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Running the analysis: Calculating Z scores', 1)		
		dv = self.dataO.loc[:,idx['v',:,:,p]]
		dv = (dv - dv.mean()).div(dv.std())
		self.dataO.loc[:,idx['v',:,:,q]] = dv.values	
	  #---
	  #--> p values Time Analysis
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Running the analysis: Calculating TP p values', 1)	 
	   #--> Variables
		tp = self.do['NTimeP']
	   #---
		if self.do['NCond'] == 1:
		 #--> If only one condition do nothing		
			pass 
		else:
			tpc = 1
			for z in self.do['MyTuples']['tpp']:	
				msg = ("Running the analysis: Calculating TP p values ("
					+ str(tpc) + '/' + str(tp) + ")")
				wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, 
					self.stProgress, msg, 1)								
	   	 	 #--> More variables										
				mL = []
				mLn = []
				ntp = 0
				l,a,b = z
			 #---
				for val in l:
					x,y = val						
			 	 #--> Check empty time point					
					if self.do['ResultsControl'][x][y][0] == None:
						pass
					else:
	   			 	 #--> Get column headers						
						mll = [self.header[h] for h in self.do['ResultsControl'][x][y]]
						mL += mll
						mLn.append(len(mll))
						ntp += 1
	   		 #--> Run p calculation						
				if ntp < 2:
					pass
				elif ntp == 2:
					c, d = mLn
					self.dataO[('tp',a,b,'P')] = self.dataVPSNMR.loc[:,mL].apply(self.TTest, axis=1, raw=True, args=(c, d))
				else:
					self.dataO[('tp',a,b,'P')] = self.dataVPSNMR.loc[:,mL].apply(self.TAnova, axis=1, raw=True, args=(mLn,))
			 #---
	   		 #--> Update current time point
				tpc += 1
			 #---
	  #--> Correct p values
		if self.do['CorrP'] == None:
			pass
		else:
	   #--> Correct intra condition
			wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
				'Running the analysis: Correcting p values (1/2)', 1)			
			pval = self.dataO.loc[:,idx['v',:,:,k]].to_numpy().tolist()
			pvalC = self.PCorrect(pval, self.do['CorrP'])[1]
			self.dataO.loc[:,idx['v',:,:,m]] = pvalC
			self.dataO.loc[:,idx['v',:,:,n]] = -1 * np.log(self.dataO.loc[:,idx['v',:,:,m]].astype('float64')).values
	   #--> Correct inter condition
			if self.do['NCond'] > 1:			
				wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
					'Running the analysis: Correcting p values (2/2)', 1)			
				pval = self.dataO.loc[:,idx['tp',:,:,'P']].to_numpy().tolist()
				pvalC = self.PCorrect(pval, self.do['CorrP'])[1]
				self.dataO.loc[:,idx['tp',:,:,'Pc']] = pvalC
			else:
				pass	
	  #--> Final steps for self.dataO
		self.dataO = self.dataO.sort_values(by=config.protprof['SortBy'])
		self.dataO = self.dataO.reset_index(drop=True)
	  #--> Change X, Y, T & C to the given/default names
	   #--> Set col dicts
		colX = {'Gene':'Gene', 'Protein': 'Protein', 'Score':'Score'}
		colY = {'Gene':'Gene', 'Protein': 'Protein', 'Score':'Score'}
		colXt = {'Gene':'Gene', 'Protein': 'Protein', 'Score':'Score'}
		colYt = {'Gene':'Gene', 'Protein': 'Protein', 'Score':'Score'}
		if self.do['CType'] == config.combobox['ControlType'][1]:
			for x in range(0, self.do['Xv']):
				j = x + 1
				colX['X'+str(j)] = self.do['LabelRP'][x]
			for x in range(0, self.do['Yv']+1):
				j = x - 1
				if x == 0:
					colY['Y0'] = self.do['LabelControl']
				else:
					colY['Y'+str(x)] = self.do['LabelCond'][j]
		else:
			for x in range(0, self.do['Xv']):
				j = x + 1
				colX['X'+str(j)] = self.do['LabelCond'][x]
			for x in range(0, self.do['Yv']+1):
				j = x - 1
				if x == 0:
					colY['Y0'] = self.do['LabelControl']
				else:
					colY['Y'+str(x)] = self.do['LabelRP'][j]
		for x in range(0, self.do['Xtp']):
			j = x + 1
			colXt['T'+str(j)] = self.do['LabelRP'][x]
		for x in range(0, self.do['Ytp']+1):
			j = x - 1
			if x == 0:
				colYt['C0'] = self.do['LabelControl']
			else:
				colYt['C'+str(x)] = self.do['LabelCond'][j]	
	   #--> Copy dataframe
		self.dataOW = self.dataO.copy()
	   #--> Change columns name
		for a in [colX, colXt]:
			self.dataOW.rename(columns=a, level=1, inplace=True)
		for a in [colY, colYt]:
			self.dataOW.rename(columns=a, level=2, inplace=True)
	 #--> Return
		return True
	#---

	def WriteOF(self):
		""" """
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Writing output files', 1)
	 #--> Create output folder
		self.do['Outputfolder'].mkdir()
	 #---
	 #--> Intermediate files
		folderD = self.do['Outputfolder'] / 'Data_Steps'
		folderD.mkdir()
		file = folderD / 'data-00-Initial-Values.txt'
		dmethods.FFsWriteCSV(file, self.dataV)
		file = folderD / 'data-01-All_Experiment-Filter.txt'
		dmethods.FFsWriteCSV(file, self.dataVP)		
		file = folderD / 'data-02-Score-Filter.txt'
		dmethods.FFsWriteCSV(file, self.dataVPS)		
		file = folderD / 'data-03-Normalization.txt'
		dmethods.FFsWriteCSV(file, self.dataVPSN)
		file = folderD / 'data-04-Median-Correction.txt'
		dmethods.FFsWriteCSV(file, self.dataVPSNM)
		file = folderD / 'data-05-Ratios.txt'
		dmethods.FFsWriteCSV(file, self.dataVPSNMR)
		file = folderD / 'data-06-Results.txt'
		dmethods.FFsWriteCSV(file, self.dataOW)		
	 #---
	 #--> protprof file
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Writing output files: protprof file', 1)
		name = self.do['Outputname'] + config.extShort['ProtProf'][0]
		self.protprofFile = self.do['Outputfolder'] / name
	  #--> Convert keys to string because json cannot handle tupples as keys
		data = {
			'V' : config.dictVersion, 
			'I'  : self.d,
			'CI' : dmethods.DictVal2String(self.do, 
				keys2string=config.protprof['StringKeys']),
			'R' : dmethods.DictTuplesKey2StringKey(self.dataO.to_dict())
			}
	  #---
	  #--> Write
		dmethods.FFsWriteJSON(self.protprofFile, data)
	  #---
	 #---
	 #--> Create the protprof object
		self.protprofObj = dclasses.DataObjProtProfFile(self.protprofFile)
	 #---
	 #--> uscr file
		self.uscrFile = self.protprofFile.with_suffix(config.extShort['Uscr'][0])
		msg = 'Writing output files: uscr files'
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress, 
				msg, 1)
		#--# Improve Something unexpected may go wrong saving the uscr file (Down)
		dmethods.FFsWriteDict2Uscr(self.uscrFile,
			iDict=self.protprofObj.Fdata['I'],
			hDict=config.dictUserInput2UscrFile[self.name]
		)
		#--# Improve Something unexpected may go wrong saving the uscr file (UP)
	 #---
	 #--> short data
		if self.do['ColExtract'] is None:
			pass
		else:
			self.sdataFile = self.protprofFile.with_suffix('.txt')
			df = dmethods.DFSelCol(self.dataFileObj.dataFrame, 
				self.do['ColExtract'])[1]
			dmethods.FFsWriteCSV(self.sdataFile, df)
	 #---
	 #--> Return
		return True
	 #---
	#---

	def ShowRes(self):
		""" Show the graphical output if any """
		gmethods.UpdateGaugeText(self.gauge, self.stProgress,
			'Generating graphical output', 1)
		gmethods.UpdateGaugeText(self.gauge, self.stProgress,
			'Generating graphical output: protprof file', 1)		
		wx.Yield()
		if gmethods.WinGraphResCreate(config.name['ProtProfRes'],
			self.protprofFile):
			pass
		else:
			return False
		return True
	#---

	def TTest(self, row, lref, ltp):
		""" Calculate t-test 
			---
			row: row from a data frame in a np.array format for greater speed
			lref: number of control replicates (int)
			ltp: number of experiment replicates (int)
			---
			It is assume that control is [0:lref] and experiment [lref:lref+ltp]
		"""
		p = stats.ttest_ind(row[0:lref], 
			row[lref:lref+ltp], 
			equal_var = False
			)[1]
		return p
	#---

	def TAnova(self, row, lind):
		""" Calculate Anova test 
			---
			row: row from a dataframe with np.array format for greater speed
			lind: list with the starting index for each experiment in row
		"""
		val = []
		s = 0
		e = 0
		for x in lind:
			e = e + x
			val.append(row[s:e])
			s = s + x
		p = stats.f_oneway(*val)[1]
		return p 
	#---

	def PCorrect(self, pval, method):
		""" Correct p values using statsmodels.stats.multitest.multipletests
			---
			pval: list of list (2 levels) with the p values. 
			method: method for the p values correction
			---
			It assumes that pval has the same number of element in each inner 
			list
		"""
	 #--> Flat pval
		pvalF = dmethods.ListFlatNLevels(pval)[1]
	 #---
	 #--> method
		methodO = config.dictCorrectP[method]
	 #---
	 #--> Correct pvalues
		pvalCF = multipletests(pvalF, method=methodO)[1]
	 #---
	 #--> pvalC
		pvalC = []
		step = len(pval[0])
		for i in range(0, len(pvalCF), step):
			pvalC.append(pvalCF[i:i+step]) 
	 #---
	 #--> Return
		return [True, pvalC]
	 #---
	#---
	#endregion --------------------------------------------------- Run Methods
#---





