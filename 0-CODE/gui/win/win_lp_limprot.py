# ------------------------------------------------------------------------------
#	Copyright (C) 2017 Kenny Bravo Rodriguez <www.umsap.nl>
	
#	This program is distributed for free in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
	
#	See the accompaning licence for more details.
# ------------------------------------------------------------------------------


""" This module creates the window for the LimProt module of the app """


#region ------------------------------------------------------------- Imports
import wx
import pandas as pd

import config.config      as config
import gui.menu.menu      as menu
import gui.gui_classes    as gclasses
import gui.gui_methods    as gmethods
import data.data_classes  as dclasses
import data.data_methods  as dmethods
#endregion ----------------------------------------------------------- Imports


class WinLimProt(gclasses.WinModule):
	""" To create the gui for the Proteome Profiling module """
	
	#region --------------------------------------------------- Instance Setup
	def __init__(self, parent=None, style=None):
		""" parent: parent of the widgets
			style: style of the window
		"""
	 #--> Initial Setup
		self.name = config.name['LimProt']
		super().__init__(parent=parent, name=self.name, style=style, length=56)
	 #---
	 #--> Variables
		self.CType = config.combobox['ControlType'][0] # Needed for self.CheckGuiResultControl
	 #---
	 #--> Widgets
	  #--> Destroy unneeded widget from parent class
		self.WidgetsDestroy(self.name)
	  #---
	  #--- TextCtrl
		self.tcDeltaU = wx.TextCtrl(self.boxValues, value="", size=(180, 22))
		self.tcDelta  = wx.TextCtrl(self.boxValues, value="", size=(180, 22))
	  #---
	  #--- StaticText
		self.stDeltaU = wx.StaticText(self.boxValues, 
			label=u'\N{GREEK CAPITAL LETTER THETA}'+ '-value', 
			style=wx.ALIGN_RIGHT) 
		self.stDelta = wx.StaticText(self.boxValues, 
			label=u'\N{GREEK CAPITAL LETTER THETA}'+ 'max-value', 
			style=wx.ALIGN_RIGHT)
		self.stbVal  = wx.StaticText(self.boxValues,  
			label=u'\N{GREEK SMALL LETTER BETA}'+'-value', 
			style=wx.ALIGN_RIGHT)
		self.styVal  = wx.StaticText(self.boxValues, 
			label=u'\N{GREEK SMALL LETTER GAMMA}'+'-value', 
			style=wx.ALIGN_RIGHT)
	  #---
	  #--- ComboBox
		self.cbbVal = wx.ComboBox(self.boxValues, value='Equal alpha', 
			choices=config.combobox['Bvalues'], style=wx.CB_READONLY)
		self.cbyVal = wx.ComboBox(self.boxValues, value='0.8',  
			choices=config.combobox['Yvalues'], style=wx.CB_READONLY)
	  #---
	 #---		
	 #--> Sizers
	  #--> Central static boxes
	   #--> Files
		self.sizerboxFilesWid = wx.FlexGridSizer(5, 2, 1, 1)
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
		self.sizerboxValuesWid = wx.FlexGridSizer(5, 4, 1, 1)
		self.sizerboxValues.Add(self.sizerboxValuesWid, border=2, 
			flag=wx.ALIGN_CENTER_HORIZONTAL|wx.ALL)
		self.sizerboxValuesWid.Add(self.stTarprot,   border=2, 
			flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL)
		self.sizerboxValuesWid.Add(self.tcTarprot,   border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerboxValuesWid.Add(self.staVal,      border=2, 
			flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL)
		self.sizerboxValuesWid.Add(self.cbaVal,      border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerboxValuesWid.Add(self.stScoreVal,  border=2, 
			flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL)
		self.sizerboxValuesWid.Add(self.tcScoreVal,  border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerboxValuesWid.Add(self.stbVal,      border=2, 
			flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL)
		self.sizerboxValuesWid.Add(self.cbbVal,      border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerboxValuesWid.Add(self.stDataNorm,  border=2, 
			flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL)
		self.sizerboxValuesWid.Add(self.cbDataNorm,  border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerboxValuesWid.Add(self.styVal,      border=2, 
			flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL)
		self.sizerboxValuesWid.Add(self.cbyVal,      border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerboxValuesWid.Add(self.stSeqLength, border=2, 
			flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL)
		self.sizerboxValuesWid.Add(self.tcSeqLength, border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerboxValuesWid.Add(self.stDeltaU,    border=2, 
			flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL)
		self.sizerboxValuesWid.Add(self.tcDeltaU,    border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerboxValuesWid.AddStretchSpacer()
		self.sizerboxValuesWid.AddStretchSpacer()
		self.sizerboxValuesWid.Add(self.stDelta,     border=2, 
			flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL)
		self.sizerboxValuesWid.Add(self.tcDelta,     border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
	   #---
	   #--> Columns
		self.sizerboxColumnsWid = wx.GridBagSizer(1, 1)
		self.sizerboxColumns.Add(self.sizerboxColumnsWid, border=2, 
			flag=wx.ALIGN_CENTER_HORIZONTAL|wx.ALL)
		self.sizerboxColumnsWid.Add(self.stSeq,     pos=(0,0), border=2, 
			flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL)
		self.sizerboxColumnsWid.Add(self.tcSeq,     pos=(0,1), border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL, span=(0,2))		
		self.sizerboxColumnsWid.Add(self.stDetProt, pos=(1,0), border=2, 
			flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL)
		self.sizerboxColumnsWid.Add(self.tcDetProt, pos=(1,1), border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL, span=(0,2))
		self.sizerboxColumnsWid.Add(self.stScore,   pos=(2,0), border=2, 
			flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL)
		self.sizerboxColumnsWid.Add(self.tcScore,   pos=(2,1), border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL, span=(0,2))
		self.sizerboxColumnsWid.Add(self.stColExt,  pos=(3,0), border=2, 
			flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL)
		self.sizerboxColumnsWid.Add(self.tcColExt,  pos=(3,1), border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL, span=(0,2))
		self.sizerboxColumnsWid.Add(self.stResults, pos=(4,0), border=2, 
			flag=wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, span=(0,2))
		self.sizerboxColumnsWid.Add(self.buttonResultsW, pos=(5,0), border=2, 
			flag=wx.ALIGN_RIGHT|wx.ALL)
		self.sizerboxColumnsWid.Add(self.tcResults,      pos=(5,1), border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerboxColumnsWid.Add(self.buttonResultsL, pos=(5,2), border=2, 
			flag=wx.ALIGN_RIGHT|wx.ALL)	
	   #---
	  #---		
	  #--> Fit				
		self.sizer.Fit(self)
	  #---
	 #---		
	 #--> Tooltips
		self.buttonOutName.SetToolTip(config.tooltip[self.name]['OutName'])
		self.staVal.SetToolTip(config.tooltip[self.name]['aVal'])
		self.stbVal.SetToolTip(config.tooltip[self.name]['bVal'])
		self.styVal.SetToolTip(config.tooltip[self.name]['yVal'])
		self.stDelta.SetToolTip(config.tooltip[self.name]['dmaxVal'])
		self.stDeltaU.SetToolTip(config.tooltip[self.name]['dVal'])
		self.stSeqLength.SetToolTip(
			config.tooltip[self.name]['SeqLength'] + config.msg['OptVal'])
	 #---
	 #--> Binding
		if config.cOS != 'Windows':
			for child in self.GetChildren():
				child.Bind(wx.EVT_RIGHT_DOWN, self.OnPopUpMenu)
		else:
			pass
	 #---
	 #--> Default values
		self.tcSeqNatFile.SetValue('NA')
		self.tcOutputFF.SetValue('NA')
		self.tcOutName.SetValue('NA')		
		self.tcScoreVal.SetValue('0')
		self.tcSeqLength.SetValue('100')		
		self.tcColExt.SetValue('NA')
	 #---
	

	 #--> INITIAL VALUES FOR TESTING. DELETE BEFORE RELEASING!!!!!!!! ##########
		import getpass
		user = getpass.getuser()
		if config.cOS == 'Darwin':
			self.tcDataFile.SetLabel('/Users/' + str(user) + '/TEMP-GUI/BORRAR-UMSAP/PlayDATA/LIMPROT/Mod-LimProt-data-kbr.txt')
			self.tcSeqRecFile.SetLabel('/Users/' + str(user) + '/TEMP-GUI/BORRAR-UMSAP/PlayDATA/LIMPROT/Mod-LimProt-seqA-PseudoNat.txt')
			self.tcSeqNatFile.SetLabel('/Users/' + str(user) + '/TEMP-GUI/BORRAR-UMSAP/PlayDATA/LIMPROT/Mod-LimProt-seqA.txt')
			self.tcOutputFF.SetLabel('/Users/' + str(user) + '/TEMP-GUI/BORRAR-UMSAP/PlayDATA/test')
		elif config.cOS == 'Windows':
			from pathlib import Path
			self.tcDataFile.SetLabel(str(Path('C:/Users/bravo/Desktop/SharedFolders/BORRAR-UMSAP/PlayDATA/LIMPROT/Mod-LimProt-data-kbr.txt'))) 
			self.tcSeqRecFile.SetLabel(str(Path('C:/Users/bravo/Desktop/SharedFolders/BORRAR-UMSAP/PlayData/LIMPROT/Mod-LimProt-seqA-PseudoNat.txt')))
			self.tcSeqNatFile.SetLabel(str(Path('C:/Users/bravo/Desktop/SharedFolders/BORRAR-UMSAP/PlayDATA/LIMPROT/Mod-LimProt-seqA.txt')))
			self.tcOutputFF.SetLabel(str(Path('C:/Users/bravo/Desktop/SharedFolders/BORRAR-UMSAP/PlayDATA/test')))
		else:
			pass
		self.tcOutName.SetLabel('myLimTest')
		self.tcTarprot.SetLabel('Mis18alpha')   
		self.tcScoreVal.SetLabel('10')
		self.tcSeqLength.SetValue('100')	
		self.tcDelta.SetValue('8') 
		self.tcDeltaU.SetValue('NA') 
		self.tcSeq.SetLabel('0')       
		self.tcDetProt.SetLabel('34')   
		self.tcScore.SetLabel('42')     
		self.tcColExt.SetLabel('0 1 2 3 4-10')
		self.tcResults.SetLabel('69-71; 81-83, 78-80, 75-77, 72-74, NA; NA, NA, NA, 66-68, NA; 63-65, 105-107, 102-104, 99-101, NA; 93-95, 90-92, 87-89, 84-86, 60-62')  
	 #--- INITIAL VALUES FOR TESTING. DELETE BEFORE RELEASING!!!!!!!! ##########
	 
	 
	 #--> Show
		self.Show()
	 #---
	#---
	#endregion ------------------------------------------------ Instance Setup
	
	# ------------------------------------------------------------- My Methods
	#region ----------------------------------------------------- Bind Methods
	def OnClearFilesDef(self):
		""" Specific clear steps in File section for this module """
		self.tcSeqNatFile.SetValue('NA')
		self.tcOutputFF.SetValue('NA')
		self.tcOutName.SetValue('NA')		
		self.lb.DeleteAllItems()
		return True
	#---

	def OnClearValuesDef(self):
		""" Specifics clear steps for Values section for this module """
		self.cbDataNorm.SetValue('Log2')
		self.cbaVal.SetValue('0.050')
		self.cbyVal.SetValue('0.8')
		self.cbbVal.SetValue('Equal alpha')
		self.tcDeltaU.SetValue('NA')
		self.tcScoreVal.SetValue('0')
		self.tcSeqLength.SetValue('NA')			
		return True
	#---

	def OnClearColumnsDef(self):
		""" Specific steps for Column section for this module """
		self.tcColExt.SetValue('NA')
		return True
	#---
	#endregion -------------------------------------------------- Bind Methods

	#region ----------------------------------------------------- Menu Methods
	def OnSaveInputF(self):
		""" Save the .uscr file with the data in the window """
	 #--> Variables
		k = True
		dlg = gclasses.DlgSaveFile(config.extLong['Uscr'])
	 #---
	 #--> Get output file path and save
		if dlg.ShowModal() == wx.ID_OK:
	 	 #--> Temp dict with data
			temp = {
				          'Data file' :   self.tcDataFile.GetValue(),       
				     'Sequence (rec)' : self.tcSeqRecFile.GetValue(),     
				     'Sequence (nat)' : self.tcSeqNatFile.GetValue(),
				      'Output folder' :   self.tcOutputFF.GetValue(),   
				        'Output name' :    self.tcOutName.GetValue(),     
				     'Target protein' :    self.tcTarprot.GetValue(),  
				        'Score value' :   self.tcScoreVal.GetValue(),
				 'Data normalization' :   self.cbDataNorm.GetValue(),
			   	    'Sequence length' :  self.tcSeqLength.GetValue(),
				            'a-value' :       self.cbaVal.GetValue(),               
				            'b-value' :       self.cbbVal.GetValue(),
				            'y-value' :       self.cbyVal.GetValue(),
				            'd-value' :     self.tcDeltaU.GetValue(),
				           'dm-value' :      self.tcDelta.GetValue(),
				           'Sequence' :        self.tcSeq.GetValue(),    
				  'Detected proteins' :    self.tcDetProt.GetValue(),   
				              'Score' :      self.tcScore.GetValue(),          
				 'Columns to extract' :     self.tcColExt.GetValue(),  		    
				            'Results' :    self.tcResults.GetValue(),
				             'Module' : config.mod[config.name['LimProt']]	
			}
		 #---
	 	 #--> Save
			if dmethods.FFsWriteDict2Uscr(dlg.GetPath(), iDict=temp):
				k = True
			else:
				k = False
		 #---
		else:
			k = False
	 #---
	 #--> Destroy dlg & Return
		dlg.Destroy()
		return k
	 #---
	#---
	#endregion -------------------------------------------------- Menu Methods

	#region ------------------------------------------------------ Run Methods
	def CheckInput(self):
		""" Check the user provided input """
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
	  #--> Delta user
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Checking user input: delta user value', 1)
		if self.CheckGui1Number(self.tcDeltaU, 
			'duVal',
			config.dictCheckFatalErrorMsg[self.name]['duVal'],
			NA=True):
			pass
		else:
			return False	
	  #---
	  #--> Delta max
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Checking user input: delta max value', 1)
		if self.CheckGui1Number(self.tcDelta, 
			'dmVal',
			config.dictCheckFatalErrorMsg[self.name]['dmVal']):
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
		self.d ['aVal'] = cbal
		self.do['aVal'] = float(cbal)
	  #---
	  #--> beta value
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Checking user input: beta value', 1)
		cbbl = self.cbbVal.GetValue()
		self.d['bVal'] = cbbl
		try:
			self.do['bVal'] = float(cbbl)							
		except Exception:
			self.do['bVal'] = self.do['aVal']
	  #---
	  #--> y value
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Checking user input: gamma value', 1)
		cbyl = self.cbyVal.GetValue()
		self.d['yVal'] = cbyl
		self.do['yVal'] = float(cbyl)	
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
		self.do['Control'] = self.do['Control'][0]
	   #---
	  #---
	 #---
	 #--> Repeating element
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Checking user input: Unique column numbers', 1)
		self.l = ([self.do['SeqCol']]     + [self.do['DetectProtCol']] 
			 + [self.do['ScoreCol']] + self.do['Control'] 
			 + dmethods.ListFlatNLevels(self.do['Results'], 2)[1])
		if self.CheckGuiListUniqueElements(self.l, 
			config.dictCheckFatalErrorMsg[self.name]['Unique'], NA=True):
			pass
		else:
			return False
	 #---	
	 #--> Small variable needed further below
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
		""" Read the files and creates the dataObjects """
	 #--> Data file
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Reading input files: Data file', 1)
	  #--> Create data object
		try:
			self.dataFileObj = dclasses.DataObjDataFile(self.do['Datafile'])
		except Exception:
			return False
	  #---
	  #--> Check column numbers
		if self.CheckGuiColNumbersInDataFile(self.lcExt, 
			self.dataFileObj.nCols,
			config.dictCheckFatalErrorMsg[self.name]['ColNumber'], 
			NA=True):
			pass
		else:
			return False
	  #---
	 #---
	 #--> Seq rec file
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Reading input files: Recombinant sequence', 1)
		try:
			self.recSeqObj = dclasses.DataObjSequenceFile(
				seqP=self.do['Seq_rec'])
		except Exception:
			return False
	 #---
	 #--> Seq nat file
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Reading input files: Native sequence', 1)
		if self.do['Seq_nat'] != None:
			try:
				self.natSeqObj = dclasses.DataObjSequenceFile(
					seqP=self.do['Seq_nat'])
			except Exception:
				return False
		else:
			pass
	 #---
	 #--> Return
		return True
	 #---
	#---

	def SetVariable(self):
		""" Set extra needed variables """
	 #--> Small variables needed in further steps or limprotRes
		self.lNoNa = [x for x in self.l if x != None]
	 #---
	 #--> data frame with needed columns from data file
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Setting up the analysis: Data frame', 1)
	  #--> Dict with column type to set the data frame
		self.DtypeDictBuilder()
	  #---
	  #--> Get data frame
		out, self.dataV = dmethods.DFSelFilterNSet(self.dataFileObj.dataFrame,
			self.lNoNa, 
			[self.do['Targetprotein'], 
			self.do['Scorevalue']], 
			[self.header[self.do['DetectProtCol']], 
			self.header[self.do['ScoreCol']]],
			['eq', 'ge',], 
			self.name, 
			self.dtypeDict)
		if out:
			pass
		else:
			return False
	  #---
	 #---
	 #--> dataV dimensions
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Setting up the analysis: Data frame dimension', 1)
		self.tentry, self.tcol = self.dataV.shape
	 #---
	 #--> Sequences
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Setting up the analysis: Recombinant sequence', 1)
	  #--> Rec
		self.recSeqSeq = self.recSeqObj.seq
		self.do['RecSeq'] = self.recSeqSeq
	  #---
	  #--> Nat
		if self.do['Seq_nat'] == None:
			self.do['NatSeq'] = None
		else:
			self.do['NatSeq'] = self.natSeqSeq = self.natSeqObj.seq
	  #---
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
	 #--> ProtLoc & mist
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
	 #--> pRes
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Setting up the analysis: pRes', 1)
		self.do['pRes'] = [1, *self.do['ProtLoc'], self.do['protSeqLength'][0]]
	 #---
	 #--> Lanes & Bands
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Setting up the analysis: Lanes and bands in the gel', 1)		
		self.do['Bands'] = len(self.do['Results'])
		self.do['Lanes'] = len(self.do['Results'][0])
	 #---
	 #--> Header for the data frame in the output
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Setting up the analysis: Output header', 1)
		i = 0
		out, self.colOut = dmethods.ListColHeaderLimProtFile(self.do['Bands'], 
			self.do['Lanes'])
	 #---
	 #--> List of Protein for limprotR
		a = self.dataFileObj.dataFrame.iloc[:,self.do['DetectProtCol']]
		self.do['ListOfProt'] = a.dropna().unique().tolist()
		self.do['ListOfProt'].sort()	 
	 #---
	 #--> Return
		return True
	 #---
	#---

	def DtypeDictBuilder(self):
		""" Creates the dtype dict to convert the data type in the dataFrame """
	 #--> Column names of the data frame
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
	  #--> Flat Results list
		out, res = dmethods.ListFlatNLevels(self.do['Results'], 2)
	  #---
	  #--> Add results columns to dict
		for a in res:
			if a != None:
				self.dtypeDict[self.header[a]] = 'float'
			else:
				pass
	  #---
	 #---
	 #--> Return
		return True
	 #---
	#---	

	def RunAnalysis(self):
		""" Run the analysis """
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Running the analysis', 1)
	 #--> Normalize
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Running the analysis: Normalizing data', 1)
		out, self.dataN = dmethods.DataNorm(self.dataV,
			sel=list(range(config.limprot['SColNorm'], self.tcol, 1)),
			method=self.do['Datanorm'])
		if out:
			pass
		else:
			return False
	 #---
	 #--> Create data frame with results
	  #--> Get rows
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
	  #--> Create data frame
		self.dataO = pd.DataFrame(rows, columns=self.colOut)
		self.dataO.sort_values(by=config.limprot['SortBy'], inplace=True)
		self.dataO.reset_index(drop=True, inplace=True)	
	  #---
	 #---
	 #--> Return	
		return True
	 #---
	#---

	def RunAnalysisFunction(self, row):
		""" Helper to RunAnalysis. row has the same order as self.l """
		rowO = []
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
			return [False, False]
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
		for z in self.do['Results']: # Loop Bands
			for j in z: # Loop Lanes
				exp = []
				for k in j: # Loop replicates
					if k == None:
						pass
					else:
						exp.append(row[s])
						s += 1
				if k == None:
					rowO.append(None)
					rowO.append(None)
					rowO.append(None)
					rowO.append(None)					
				else:		
					ttest, delta, tost = dmethods.StatTost(control, exp, 
						self.do['aVal'], self.do['bVal'], self.do['yVal'], 
						self.do['duVal'], self.do['dmVal'])
					rowO.append(ttest)
					rowO.append(delta)
					rowO.append(tost)
					rowO.append(exp)
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
		""" Write the output """
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Writing output files', 1)
	 #--> Create output folder
		self.do['Outputfolder'].mkdir()
	 #---
	 #--> Intermediate files
		msg = 'Writing output files: Intermediate files' 
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			msg, 1)
		folderD = self.do['Outputfolder'] / 'Data_Steps'
		folderD.mkdir()
		file = folderD / 'data-00-Extract.txt'
		dmethods.FFsWriteCSV(file, self.dataV)
		file = folderD / 'data-01-Norm.txt'
		dmethods.FFsWriteCSV(file, self.dataN)
		file = folderD / 'data-02-Results.txt'
		dmethods.FFsWriteCSV(file, self.dataO)		
	 #---
	 #--> limprot file
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Writing output files: limprot file', 1)
		name = self.do['Outputname'] + config.extShort['LimProt'][0]
		self.limprotFile = self.do['Outputfolder'] / name
		data = {
			'V' : config.dictVersion, 
			'I'  : self.d,
			'CI' : dmethods.DictVal2String(self.do, 
				keys2string=config.limprot['StringKeys']),
			'R' : dmethods.DictTuplesKey2StringKey(self.dataO.to_dict())
			}
		dmethods.FFsWriteJSON(self.limprotFile, data)
	 #---
	 #--> Create the limprot object
		self.limprotObj = dclasses.DataObjLimProtFile(self.limprotFile)
	 #---
	 #--> uscr file
		self.uscrFile = self.limprotFile.with_suffix(config.extShort['Uscr'][0])
		msg = 'Writing output files: uscr files'
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress, 
				msg, 1)
		#--# Improve Something unexpected may go wrong saving the uscr file (Down)
		dmethods.FFsWriteDict2Uscr(self.uscrFile,
			iDict=self.limprotObj.Fdata['I'],
			hDict=config.dictUserInput2UscrFile[self.name]
		)
		#--# Improve Something unexpected may go wrong saving the uscr file (UP)
	 #---
	 #--> Files that depend on FP being not empty
		if self.limprotObj.checkExport:
	 	 #--> short data
			if self.do['ColExtract'] is None:
				pass
			else:
				msg = 'Writing output files: short data files'
				wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, 
					self.stProgress, msg, 1)
				self.dataOutFolder = self.do['Outputfolder'] / 'Data'
				self.dataOutFolder.mkdir()
				self.limprotObj.ToSDataFile(self.dataOutFolder)
	 	 #---
		 #--> sequence files
			if self.do['Sequencelength'] != None:
				msg = 'Writing output files: sequence file'
				wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, 
					self.stProgress, msg, 1)
				self.seqFile = self.limprotFile.with_suffix('.seq.pdf')
				self.limprotObj.LimProt2SeqPDF(self.seqFile,
					self.do['Sequencelength'])
		 #---
			else:
				pass
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
		""" Show graphical output """

		gmethods.UpdateGaugeText(self.gauge, self.stProgress,
			'Generating graphical output', 1)
		if self.limprotObj.checkExport:
			gmethods.UpdateGaugeText(self.gauge, self.stProgress,
				'Generating graphical output: limprot file', 1)
			wx.Yield()
			gmethods.WinGraphResCreate(config.name['LimProtRes'], 
				self.limprotFile)	
		else:
			pass		
		return True
	#---
	#endregion --------------------------------------------------- Run Methods
#---








