# ------------------------------------------------------------------------------
# Copyright (C) 2017 Kenny Bravo Rodriguez <www.umsap.nl>
#
# Author: Kenny Bravo Rodriguez (kenny.bravorodriguez@mpi-dortmund.mpg.de)
#
# This program is distributed for free in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See the accompaning licence for more details.
# ------------------------------------------------------------------------------


""" Panels of the application"""


#region -------------------------------------------------------------> Imports
import _thread 
from pathlib import Path

import wx

import dat4s_core.data.file as dtsFF
import dat4s_core.data.method as dtsMethod
import dat4s_core.exception.exception as dtsException
import dat4s_core.gui.wx.validator as dtsValidator
import dat4s_core.gui.wx.widget as dtsWidget
import dat4s_core.data.statistic as dtsStatistic

import config.config as config
import gui.dtscore as dtscore
import gui.method as method
import gui.widget as widget
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Classes
#------------------------------> Base Classes
class BaseConfPanel(
	wx.Panel,
	dtsWidget.StaticBoxes, 
	dtsWidget.ButtonOnlineHelpClearAllRun
	):
	"""Creates the skeleton of a configuration tab. This includes the 
		wx.StaticBox, the Bottom Buttons and the statusbar.

		See Notes

		Parameters
		----------
		parent : wx Widget
			Parent of the widgets
		rightDelete : Boolean
			Enables clearing wx.StaticBox input with right click
		confOpt : dict or None
			Extra options from child class. Default is None
		confMsg : dict or None
			Extra messages from child class. Default is None

		Attributes
		----------
		parent : wx Widget
			Parent of the widgets
		confOpt : dict or None
			Configuration options after updating with info from child class
		confMsg : dict or None
			Error messages after updating with info from child class
		lbI : wx.ListCtrl or None
			Pointer to the default wx.ListCtrl to load Data File content to. 
		lbL : list of wx.ListCtrl
			To clear all wx.ListCtrl in the Tab
		msgError : Str or None
			Error message to show when analysis fails
		d : dict
			Dict with user input. See keys in Child class
		do : dict
			Dict with processed user input. See keys in Child class
		dfI : pdDataFrame or None
			Dataframe with initial values after columns were extracted and type
			assigned.
		dfN : pdDataFrame or None
			Dataframe after normalization
		date : str or None
			Date time stamp as given by dtsMethod.StrNow()
		oFolder : Path or None
			Folder to contain the output
		tException : Exception or None
			Exception raised during analysis
		lbI : wx.ListCtrl
			ListCtrl to show information about the main input file
		lbO : wx.ListCtrl
			ListCtrl to show selected columns in lbI
		lbL : list of wx.ListCtrl
			To use when deleting the content on the wx.ListCtrl 
			e.g. self.LCtrlEmpty
		btnRun : wx.Button
			Run button
		btnHelp : wx.Button
			Help button
		btnClearAll : wx.Button
			Clear All button
		sbFile : wx.StaticBox
			StaticBox to contain the input/output file information
		sbValue : wx.StaticBox
			StaticBox to contain the user-defined values
		sbColumn : wx.StaticBox
			StaticBox to contain the column numbers in the input files
		sizersbFile : wx.StaticBoxSizer
			StaticBoxSizer for sbFile
		sizersbValue : wx.StaticBoxSizer
			StaticBoxSizer for sbValue
		sizersbColumn : wx.StaticBoxSizer
			StaticBoxSizer for sbColumn
		sizersbFileWid : wx.GridBagSizer
			FlexGridSizer for widgets in sbFile
		sizersbValueWid : wx.GridBagSizer
			FlexGridSizer for widgets in sbValue
		sizersbColumnWid : wx.GridBagSizer
			FlexGridSizer for widgets in sbColumn		
		btnSizer : wx.FlexGridSizer
			To align the buttons
		Sizer : wx.BoxSizer
			Main sizer of the tab
		
		Notes
		-----
		
	"""
	#region -----------------------------------------------------> Class setup
	
	#endregion --------------------------------------------------> Class setup

	#region --------------------------------------------------> Instance setup
	def __init__(self, parent, rightDelete=True, confOpt=None, confMsg=None):
		""" """
		#region -----------------------------------------------> Initial Setup
		self.parent = parent
		#------------------------------> Configuration options
		#--------------> From self
		self.confOpt = {
			#------------------------------> Label
			'iFileL'     : config.label['BtnDataFile'],
			'oFileL'     : config.label['BtnOutFile'],
			'NormMethodL': config.label['CbNormalization'],
			'CheckL'     : config.label['CbCheck'],
			'RunBtnL'    : config.label['BtnRun'],
			'FileBoxL'   : config.label['StBoxFile'],
			'ValueBoxL'  : config.label['StBoxValue'],
			'ColumnBoxL' : config.label['StBoxColumn'],
			#------------------------------> Hint
			'iFileH' : f"Path to the {config.label['BtnDataFile']}",
			'oFileH' : f"Path to the {config.label['BtnOutFile']}",
			#------------------------------> Choices
			'NormMethod' : config.choice['NormMethod'],
			#------------------------------> Others
			'oMode' : 'save',
		}
		#--------------> From child class
		if confOpt is not None:
			self.confOpt.update(confOpt)
		else:
			pass
		#------------------------------> Messages
		#--------------> From self
		self.confMsg = { # gui.tab, error msg
			'iFile' : {
				'NotPath' : (
					f"The path to the {self.confOpt['iFileL']} is not valid."),
				'NotFile' : (
					f"The path to the {self.confOpt['iFileL']} does not point "
					f"to a file."),
				'NoRead' : (
					f"The given {self.confOpt['iFileL']} cannot be read."),
				'FileExt' : (
					f"The given {self.confOpt['iFileL']} does not have the "
					f"correct extension."),
			},
			'oFile' : {
				'NotPath' : (
					f"The path to the {self.confOpt['oFileL']} is not valid."),
				'NoWrite' : (
					f"It is not possible to write into the "
					f"{self.confOpt['oFileL']}"),
			},
			'NormMethod' : (
				f"The {self.confOpt['NormMethodL']} was not selected."),
		}
		#--------------> From child class
		if confMsg is not None:
			self.confMsg.update(confMsg)
		else:
			pass
		#------------------------------> This is needed to handle Data File 
		# content load to the wx.ListCtrl in Tabs with multiple panels
		self.lbI       = None # Default wx.ListCtrl to load data file content
		self.lbL       = [self.lbI]
		#------------------------------> Needed to Run the analysis
		self.msgError   = None # Error msg to show in self.RunEnd
		self.d          = {} # Dict with the user input as given
		self.do         = {} # Dict with the processed user input
		self.dfI        = None # pd.DataFrame for initial,
		self.dfN        = None # normalized and
		self.date       = None # date for corr file
		self.oFolder    = None # folder for output
		self.tException = None # Exception raised during analysis
		#------------------------------> Parent init
		wx.Panel.__init__(self, parent, name=self.name)

		dtsWidget.ButtonOnlineHelpClearAllRun.__init__(
			self, 
			self, 
			self.confOpt['URL'], 
			labelR    = self.confOpt['RunBtnL'],
		)

		dtsWidget.StaticBoxes.__init__(self, self, 
			labelF      = self.confOpt['FileBoxL'],
			labelV      = self.confOpt['ValueBoxL'],
			labelC      = self.confOpt['ColumnBoxL'],
			rightDelete = rightDelete,
		)
		#endregion --------------------------------------------> Initial Setup

		#region -----------------------------------------------------> Widgets
		self.iFile = dtsWidget.ButtonTextCtrlFF(self.sbFile,
			btnLabel   = self.confOpt['iFileL'],
			tcHint     = self.confOpt['iFileH'],
			ext        = config.extLong['Data'],
			tcStyle    = wx.TE_READONLY|wx.TE_PROCESS_ENTER,
			validator  = wx.DefaultValidator,
			ownCopyCut = True,
		)
		self.iFile.afterBtn = self.LCtrlFill

		self.oFile = dtsWidget.ButtonTextCtrlFF(self.sbFile,
			btnLabel   = self.confOpt['oFileL'],
			tcHint     = self.confOpt['oFileH'],
			mode       = self.confOpt['oMode'],
			ext        = config.extLong['UMSAP'],
			tcStyle    = wx.TE_READONLY,
			validator  = dtsValidator.OutputFF(
				fof = 'file',
				opt = False,
				ext = config.extShort['UMSAP'][0],
			),
			ownCopyCut = True,
		)

		self.checkB = wx.CheckBox(
			self.sbFile,
			label = self.confOpt['CheckL'],
		)
		self.checkB.SetValue(True)
		#endregion --------------------------------------------------> Widgets

		#region ------------------------------------------------------> Sizers
		self.sizersbFileWid.Add(
			self.iFile.btn,
			pos    = (0,0),
			flag   = wx.EXPAND|wx.ALL,
			border = 5
		)
		self.sizersbFileWid.Add(
			self.iFile.tc,
			pos    = (0,1),
			flag   = wx.EXPAND|wx.ALL,
			border = 5
		)
		self.sizersbFileWid.Add(
			self.oFile.btn,
			pos    = (1,0),
			flag   = wx.EXPAND|wx.ALL,
			border = 5
		)
		self.sizersbFileWid.Add(
			self.oFile.tc,
			pos    = (1,1),
			flag   = wx.EXPAND|wx.ALL,
			border = 5
		)
		self.sizersbFileWid.Add(
			self.checkB,
			pos    = (2,1),
			flag   = wx.ALIGN_LEFT|wx.ALL,
			border = 5,
		)
		self.sizersbFileWid.AddGrowableCol(1,1)
		self.sizersbFileWid.AddGrowableRow(0,1)

		self.Sizer = wx.BoxSizer(wx.VERTICAL)

		self.Sizer.Add(self.sizersbFile, 0, wx.EXPAND|wx.ALL, 5)
		self.Sizer.Add(self.sizersbValue, 0, wx.EXPAND|wx.ALL, 5)
		self.Sizer.Add(self.sizersbColumn, 0, wx.EXPAND|wx.ALL, 5)
		self.Sizer.Add(self.btnSizer, 0, wx.ALIGN_CENTER|wx.ALL, 5)
		#endregion ---------------------------------------------------> Sizers

		#region --------------------------------------------------------> Bind
		self.iFile.tc.Bind(wx.EVT_TEXT, self.OnIFileEmpty)
		self.iFile.tc.Bind(wx.EVT_TEXT_ENTER, self.OnIFileEnter)
		self.oFile.tc.Bind(wx.EVT_TEXT, self.OnOFileChange)
		#endregion -----------------------------------------------------> Bind
	#---
	#endregion -----------------------------------------------> Instance setup

	#region ---------------------------------------------------> Class methods
	def OnIFileEnter(self, event):
		"""Reload column names in the data file when pressing enter
	
			Parameters
			----------
			event : wx.Event
				Information about the event
		"""
		if self.LCtrlFill(self.iFile.tc.GetValue()):
			return True
		else:
			return False
	#---

	def LCtrlFill(self, fileP):
		"""Fill the wx.ListCtrl after selecting path to the folder. This is
			called from within self.iFile
	
			Parameters
			----------
			fileP : Path
				Folder path
		"""
		#region ----------------------------------------------------> Del list
		self.LCtrlEmpty()
		#endregion -------------------------------------------------> Del list
		
		#region ---------------------------------------------------> Fill list
		try:
			dtsMethod.LCtrlFillColNames(self.lbI, fileP)
		except Exception as e:
			dtscore.Notification(
				'errorF',
				msg        = str(e),
				tException = e,
			)
			return False
		#endregion ------------------------------------------------> Fill list
		
		#region -----------------------------------------> Columns in the file
		self.NCol = self.lbI.GetItemCount()
		#endregion --------------------------------------> Columns in the file

		return True
	#---	

	def OnIFileEmpty(self, event):
		"""Clear GUI elements when Data Folder is ''
	
			Parameters
			----------
			event: wx.Event
				Information about the event		
		"""
		if self.iFile.tc.GetValue() == '':
			self.LCtrlEmpty()
		else:
			pass

		return True
	#---

	def LCtrlEmpty(self):
		"""Clear wx.ListCtrl and NCol """
		#region -------------------------------------------------> Delete list
		for l in self.lbL:
			l.DeleteAllItems()
		#endregion ----------------------------------------------> Delete list
		
		#region ---------------------------------------------------> Set NCol
		self.NCol = None
		#endregion ------------------------------------------------> Set NCol

		return True
	#---

	def OnOFileChange(self, event):
		"""Show/Hide self.checkB
	
			Parameters
			----------
			event: wx.Event
				Information about the event
		"""
		if self.oFile.tc.GetValue() == '':
			self.sizersbFileWid.Hide(self.checkB)
			self.Sizer.Layout()
		else:
			if Path(self.oFile.tc.GetValue()).exists():
				self.checkB.SetValue(True)
				self.sizersbFileWid.Show(self.checkB)
				self.Sizer.Layout()
			else:
				self.sizersbFileWid.Hide(self.checkB)
				self.Sizer.Layout()
	#---

	def SetOutputDict(self, dateDict):
		"""Creates the output dictionary to be written to the output file 
		
			Parameters
			----------
			dateDict : dict
				dateDict = {
					date : {
						'V' : config.dictVersion,
						'I' : self.d,
						'CI': dtsMethod.DictVal2Str(
							self.do, 
							self.confOpt['ChangeKey'],
							new = True,
						),
						'R' : Results,
					}
				}
		"""
		if self.do['oFile'].exists():
			print('File Exist')
			if self.do['Check']:
				print('Check is True')
				#--> Read old output
				outData = dtsFF.ReadJSON(self.do['oFile'])
				#--> Append to output
				if outData.get(self.confOpt['Section'], False):
					print('Section exist')
					outData[self.confOpt['Section']][self.date] = dateDict[self.date]
				else:
					print('Section does not exist')
					outData[self.confOpt['Section']] = dateDict	
			else:
				print('Check is False')
				outData = {self.confOpt['Section'] : dateDict}
		else:
			print('File does not exist')
			outData = {self.confOpt['Section'] : dateDict}

		return outData
	#---

	def EqualLenLabel(self, label):
		"""Add empty space to the end of label to match the length of
			self.confOpt['LenLongest']
	
			Parameters
			----------
			label : str
				Original label
	
			Returns
			-------
			str
				Label with added empty strings at the end to match the length of
				self.confOpt['LenLongest']
	
			Raise
			-----
			ExecutionError
				- When self.confOpt does not have LenLongest
		"""
		#region -------------------------------------------------> Check input
		if self.confOpt.get('LenLongest', '') == '':
			raise dtsException.ExecutionError(
				f"The key 'LenLongest' is not present in self.confOpt."
			)
		else:
			return f"{label}{(self.confOpt['LenLongest'] - len(label))*' '}"
		#endregion ----------------------------------------------> Check input
		
	#---
	#endregion ------------------------------------------------> Class methods
#---


class BaseConfModPanel(BaseConfPanel, widget.ResControl):
	"""Base panel for a module

		Parameters
		----------
		parent : wx Widget
			Parent of the widgets
		oMode : str
			One of 'openO', 'openM', 'save', 'folder'. Default is 'folder'
		statusbar : wx.StatusBar
			Statusbar of the application to display messages
		rightDelete : Boolean
			Enables clearing wx.StaticBox input with right click
		confOpt : dict or None
			Extra options from child class. Default is None
		confMsg : dict or None
			Extra messages from child class. Default is None

		Attributes
		----------
		

		Raises
		------
		

		Methods
		-------
		
	"""
	#region -----------------------------------------------------> Class setup
	
	#endregion --------------------------------------------------> Class setup

	#region --------------------------------------------------> Instance setup
	def __init__(self, parent, rightDelete=True, confOpt=None, confMsg=None):
		""" """
		#region -------------------------------------------------> Check Input
		
		#endregion ----------------------------------------------> Check Input

		#region -----------------------------------------------> Initial Setup
		#------------------------------> Configuration options
		#--------------> From self
		confOptM = { 
			#------------------------------> Label
			'ScoreValueL'  : 'Score Value',
			'DetectedProtL': 'Detected Proteins',
			'ScoreL'       : 'Score',
			'ColExtractL'  : 'Columns to Extract',
			'ResultL'      : 'Results - Control experiments',
			'TypeResL'     : 'Type Values',
			'LoadResL'     : 'Load Values',
			#------------------------------> Hint
			
			#------------------------------> Size
			'TwoInRow'  : config.size['TwoInRow'],
		}
		#--------------> From child class
		if confOpt is not None:
			confOptM.update(confOpt)
		else:
			pass
		#------------------------------> Messages
		#--------------> From self
		confMsgM = { }
		#--------------> From child class
		if confMsg is not None:
			confMsgM.update(confMsg)
		else:
			pass

		BaseConfPanel.__init__(self, parent, rightDelete=rightDelete, 
			confOpt=confOptM, confMsg=confMsgM)

		widget.ResControl.__init__(self, self.sbColumn)
		#endregion --------------------------------------------> Initial Setup

		#region --------------------------------------------------------> Menu
		
		#endregion -----------------------------------------------------> Menu

		#region -----------------------------------------------------> Widgets
		self.normMethod = dtsWidget.StaticTextComboBox(
			self.sbValue, 
			label     = self.confOpt['NormMethodL'],
			choices   = self.confOpt['NormMethod'],
			validator = dtsValidator.IsNotEmpty(),
		)

		self.scoreVal = dtsWidget.StaticTextCtrl(
			self.sbValue,
			stLabel   = self.confOpt['ScoreValueL'],
			tcSize    = self.confOpt['TwoInRow'],
			validator = dtsValidator.NumberList(
				numType = 'float',
				nN      = 1,
			)
		)

		self.detectedProt = dtsWidget.StaticTextCtrl(
			self.sbColumn,
			stLabel   = self.confOpt['DetectedProtL'],
			tcSize    = self.confOpt['TwoInRow'],
			validator = dtsValidator.NumberList(
				numType = 'int',
				nN      = 1,
				vMin    = 0,
			)
		)

		self.score = dtsWidget.StaticTextCtrl(
			self.sbColumn,
			stLabel   = self.confOpt['ScoreL'],
			tcSize    = self.confOpt['TwoInRow'],
			validator = dtsValidator.NumberList(
				numType = 'int',
				nN      = 1,
				vMin    = 0,
			)
		)

		self.colExtract = dtsWidget.StaticTextCtrl(
			self.sbColumn,
			stLabel   = self.confOpt['ColExtractL'],
			tcSize    = self.confOpt['TwoInRow'],
			validator = dtsValidator.NumberList(
				numType = 'int',
				nN      = 1,
				vMin    = 0,
			)
		)
		#endregion --------------------------------------------------> Widgets

		#region ------------------------------------------------------> Sizers
		
		#endregion ---------------------------------------------------> Sizers

		#region --------------------------------------------------------> Bind
		
		#endregion -----------------------------------------------------> Bind

		#region ---------------------------------------------> Window position
		
		#endregion ------------------------------------------> Window position
	#---
	#endregion -----------------------------------------------> Instance setup

	#region ---------------------------------------------------> Class methods
	
	#endregion ------------------------------------------------> Class methods
#---


class CorrA(BaseConfPanel):
	"""Creates the configuration tab for Correlation Analysis
	
		Parameters
		----------
		parent : wx Widget
			Parent of the widgets

		Attributes
		----------
		name : str
			Unique id of the pane in the app
		confOpt : dict
			Dict with configuration options
		confMsg dict or None
			Messages for users
		do : dict
			Dict with the processed user input
			{
				'iFile'     : 'input file path',
				'oFolder'   : 'output folder path',
				'NormMethod': 'normalization method',
				'CorrMethod': 'correlation method',
				'Column'    : [selected columns as integers],
				'Check      : 'Append to existing output file or not',
			}
		d : dict
			Similar to 'do' but with the values given by the user and keys as 
			in the GUI of the tab
		dfCC : pdDataFrame
			Dataframe with correlation coefficients
		See parent class for more attributes

		Notes
		-----
		Running the analysis results in the creation of
		Data-20210324-165609-Correlation-Analysis
		output-file.umsap
		
		The files in Data are regular csv files with the data at the end of the
		corresponding step.

		The Correlation Analysis section in output-file.umsap conteins the 
		information about the calculations, e.g

		{
			'Correlation-Analysis : {
				'20210324-165609': {
					'V' : config.dictVersion,
					'I' : self.d,
					'CI': self.do,
					'R' : pd.DataFrame (dict) with the correlation coefficients
				}
			}
		}
	"""
	#region -----------------------------------------------------> Class Setup
	name = 'CorrAPane'
	#endregion --------------------------------------------------> Class Setup
	
	#region --------------------------------------------------> Instance setup
	def __init__(self, parent):
		""""""
		#region -----------------------------------------------> Initial setup
		self.dfCC = None # correlation coefficients
		
		confOpt = { # gui.tab, conf
			#------------------------------> URL
			'URL' : config.url['CorrAPane'],
			#------------------------------> Labels
			'LenLongest' : len(config.label['CbNormalization']),
			'CorrMethodL': 'Correlation Method',
			'ListColumnL': config.label['LCtrlColName_I'],
			'iListL'     : 'Columns in the Data File',
			'oListL'     : 'Columns to Analyse',
			'AddL'       : 'Add columns',
			#------------------------------> Choices
			'CorrMethod' : ['', 'Pearson', 'Kendall', 'Spearman'],
			#------------------------------> Size
			'LCtrlColS' : config.size['LCtrl#Name'],
			#------------------------------> Tooltips
			'iListTT' : (
				f"Selected rows can be copied ({config.copyShortCut}+C) but "
				f"the list cannot be modified."),
			'oListTT' : (
				f"New rows can be pasted ({config.copyShortCut}+V) after the "
				f"last selected element and existing one cut/deleted "
				f"({config.copyShortCut}+X) or copied "
				f"({config.copyShortCut}+C)."),
			'AddTT' : (
				f"Add selected Columns in the Data File to the list of Columns "
				f"to Analyse. New columns will be added after the last "
				f"selected element in Columns to analyse. Duplicate columns "
				f"are discarded."),
			#------------------------------> Progress Dialog
			'TitlePD' : 'Calculating Correlation Coefficients',
			'GaugePD' : 15,
			#------------------------------> Output
			'Section'  : config.nameUtilities['CorrA'],
			'MainData' : 'Data-03-CorrelationCoefficients',
			'ChangeKey': ['iFile', 'oFile'],
		}

		confMsg = { # gui.tab, error msg
			'CorrMethod' : (
				f"The {confOpt['CorrMethodL']} was not selected."),
			'oList' : (
				f"The list of {confOpt['oListL']} must contain at least "
				f"two items."),
		}

		super().__init__(parent, confOpt=confOpt, confMsg=confMsg)
		#endregion --------------------------------------------> Initial setup
		
		#region -----------------------------------------------------> Widgets
		#------------------------------> File
		self.iFile.tc.SetValidator(
			dtsValidator.InputFF(
				fof = 'file',
				ext = config.extShort['Data'],
			)
		)
		#------------------------------> Values
		self.normMethod = dtsWidget.StaticTextComboBox(self.sbValue, 
			label     = self.confOpt['NormMethodL'],
			choices   = self.confOpt['NormMethod'],
			validator = dtsValidator.IsNotEmpty(),
		)
		self.corrMethod = dtsWidget.StaticTextComboBox(self.sbValue, 
			label     = self.confOpt['CorrMethodL'],
			choices   = self.confOpt['CorrMethod'],
			validator = dtsValidator.IsNotEmpty(),
		)
		#------------------------------> Columns
		self.stListI = wx.StaticText(
			self.sbColumn, 
			label = self.confOpt['iListL'],
		)
		self.stListO = wx.StaticText(
			self.sbColumn, 
			label = self.confOpt['oListL'],
		)

		self.lbI = dtscore.ListZebra(self.sbColumn, 
			colLabel        = self.confOpt['ListColumnL'],
			colSize         = self.confOpt['LCtrlColS'],
			copyFullContent = True,
		)
		self.lbO = dtscore.ListZebra(self.sbColumn, 
			colLabel        = self.confOpt['ListColumnL'],
			colSize         = self.confOpt['LCtrlColS'],
			canPaste        = True,
			canCut          = True,
			copyFullContent = True,
		)
		self.lbL = [self.lbI, self.lbO]

		self.addCol = wx.Button(self.sbColumn, 
			label = self.confOpt['AddL'],
		)
		self.addCol.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_GO_FORWARD), 
			dir = wx.RIGHT,
		)
		#endregion --------------------------------------------------> Widgets

		#region -----------------------------------------------------> Tooltip
		self.stListI.SetToolTip(self.confOpt['iListTT'])
		self.stListO.SetToolTip(self.confOpt['oListTT'])
		self.addCol.SetToolTip(self.confOpt['AddTT'])
		#endregion --------------------------------------------------> Tooltip

		#region ------------------------------------------------------> Sizers
		#------------------------------> Expand Column section
		item = self.Sizer.GetItem(self.sizersbColumn)
		item.Proportion = 1
		item = self.sizersbColumn.GetItem(self.sizersbColumnWid)
		item.Proportion = 1
		#------------------------------> Values
		self.sizersbValueWid.Add(
			1, 1,
			pos    = (0,0),
			flag   = wx.EXPAND|wx.ALL,
			border = 5
		)
		self.sizersbValueWid.Add(
			self.normMethod.st,
			pos    = (0,1),
			flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL,
			border = 5,
		)
		self.sizersbValueWid.Add(
			self.normMethod.cb,
			pos    = (0,2),
			flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL,
			border = 5,
		)
		self.sizersbValueWid.Add(
			self.corrMethod.st,
			pos    = (0,3),
			flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL,
			border = 5,
		)
		self.sizersbValueWid.Add(
			self.corrMethod.cb,
			pos    = (0,4),
			flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL,
			border = 5,
		)
		self.sizersbValueWid.Add(
			1, 1,
			pos    = (0,5),
			flag   = wx.EXPAND|wx.ALL,
			border = 5
		)
		self.sizersbValueWid.AddGrowableCol(0, 1)
		self.sizersbValueWid.AddGrowableCol(5, 1)
		#------------------------------> Columns
		self.sizersbColumnWid.Add(
			self.stListI,
			pos    = (0,0),
			flag   = wx.ALIGN_CENTRE|wx.ALL,
			border = 5
		)
		self.sizersbColumnWid.Add(
			self.stListO,
			pos    = (0,2),
			flag   = wx.ALIGN_CENTRE|wx.ALL,
			border = 5
		)
		self.sizersbColumnWid.Add(
			self.lbI,
			pos    = (1,0),
			flag   = wx.EXPAND|wx.ALL,
			border = 20
		)
		self.sizersbColumnWid.Add(
			self.addCol,
			pos    = (1,1),
			flag   = wx.ALIGN_CENTER|wx.ALL,
			border = 20
		)
		self.sizersbColumnWid.Add(
			self.lbO,
			pos    = (1,2),
			flag   = wx.EXPAND|wx.ALL,
			border = 20
		)
		self.sizersbColumnWid.AddGrowableCol(0, 1)
		self.sizersbColumnWid.AddGrowableCol(2, 1)
		self.sizersbColumnWid.AddGrowableRow(1, 1)
		#------------------------------> Hide Checkbox
		if self.oFile.tc.GetValue() == '':
			self.sizersbFileWid.Hide(self.checkB)
		else:
			pass
		#------------------------------> Main Sizer
		self.SetSizer(self.Sizer)
		self.Sizer.Fit(self)
		#endregion ---------------------------------------------------> Sizers

		#region --------------------------------------------------------> Bind
		self.addCol.Bind(wx.EVT_BUTTON, self.OnAdd)
		#endregion -----------------------------------------------------> Bind
	
		#region --------------------------------------------------------> Test
		import getpass
		user = getpass.getuser()
		if config.cOS == "Darwin":
			self.iFile.tc.SetValue("/Users/" + str(user) + "/TEMP-GUI/BORRAR-UMSAP/PlayDATA/TARPROT/Mod-Enz-Dig-data-ms.txt")
			self.oFile.tc.SetValue("/Users/" + str(user) + "/TEMP-GUI/BORRAR-UMSAP/PlayDATA/TARPROT/tarprot.umsap")
		elif config.cOS == 'Windows':
			from pathlib import Path
			self.iFile.tc.SetValue(str(Path('C:/Users/bravo/Desktop/SharedFolders/BORRAR-UMSAP/PlayDATA/TARPROT/Mod-Enz-Dig-data-ms.txt')))
			self.oFile.tc.SetValue(str(Path('C:/Users/bravo/Desktop/SharedFolders/BORRAR-UMSAP/PlayDATA/TARPROT')))
		else:
			pass
		self.normMethod.cb.SetValue("Log2")
		self.corrMethod.cb.SetValue("Pearson")
		#endregion -----------------------------------------------------> Test
	#---
	#endregion -----------------------------------------------> Instance setup

	#region ---------------------------------------------------> Class Methods
	def OnAdd(self, event):
		"""Add columns to analyse
	
			Parameters
			----------
			event : wx.Event
				Event information
		"""
		self.lbI.Copy()
		self.lbO.Paste()
	#---

	#-------------------------------------> Run analysis methods
	def OnRun(self, event):
		""" Start correlation coefficients calculation

			Parameter
			---------
			event : wx.Event
				Event information
		"""
		#region --------------------------------------------------> Dlg window
		self.dlg = dtscore.ProgressDialog(
			self, 
			self.confOpt['TitlePD'], 
			self.confOpt['GaugePD'],
		)
		#endregion -----------------------------------------------> Dlg window

		#region ------------------------------------------------------> Thread
		_thread.start_new_thread(self.Run, ('test',))
		#endregion ---------------------------------------------------> Thread

		#region ----------------------------------------> Show progress dialog
		self.dlg.ShowModal()
		self.dlg.Destroy()
		#endregion -------------------------------------> Show progress dialog

		return True
	#---

	def CheckInput(self):
		"""Check user input"""
		
		#region ---------------------------------------------------------> Msg
		msgPrefix = config.label['PdCheck']
		#endregion ------------------------------------------------------> Msg
		
		#region -------------------------------------------> Individual Fields
		#------------------------------> Input file
		msgStep = msgPrefix + self.confOpt['iFileL']
		wx.CallAfter(self.dlg.UpdateStG, msgStep)
		a, b = self.iFile.tc.GetValidator().Validate()
		if a:
			pass
		else:
			self.msgError = self.confMsg['iFile'][b[0]]
			return False
		#------------------------------> Output Folder
		msgStep = msgPrefix + self.confOpt['oFileL']
		wx.CallAfter(self.dlg.UpdateStG, msgStep)
		a, b = self.oFile.tc.GetValidator().Validate()
		if a:
			pass
		else:
			self.msgError = self.confMsg['oFile'][b[0]]
			return False
		#------------------------------> Normalization
		msgStep = msgPrefix + self.confOpt['NormMethodL']
		wx.CallAfter(self.dlg.UpdateStG, msgStep)
		if self.normMethod.cb.GetValidator().Validate()[0]:
			pass
		else:
			self.msgError = self.confMsg['NormMethod']
			return False
		#------------------------------> Corr Method
		msgStep = msgPrefix + self.confOpt['CorrMethodL']
		wx.CallAfter(self.dlg.UpdateStG, msgStep)
		if self.corrMethod.cb.GetValidator().Validate()[0]:
			pass
		else:
			self.msgError = self.confMsg['CorrMethod']
			return False
		#------------------------------> ListCtrl
		msgStep = msgPrefix + self.confOpt['oListL']
		wx.CallAfter(self.dlg.UpdateStG, msgStep)
		if self.lbO.GetItemCount() > 1:
			pass
		else:
			self.msgError = self.confMsg['oList']
			return False
		#endregion ----------------------------------------> Individual Fields

		return True
	#---

	def PrepareRun(self):
		"""Set variable and prepare data for analysis."""
		
		#region ---------------------------------------------------------> Msg
		msgPrefix = config.label['PdPrepare']
		#endregion ------------------------------------------------------> Msg

		#region -------------------------------------------------------> Input
		msgStep = msgPrefix + 'User input, reading'
		wx.CallAfter(self.dlg.UpdateStG, msgStep)
		#------------------------------> As given
		self.d = {
			self.EqualLenLabel(self.confOpt['iFileL']) : (
				self.iFile.tc.GetValue()),
			self.EqualLenLabel(self.confOpt['oFileL']) : (
				self.oFile.tc.GetValue()),
			self.EqualLenLabel(self.confOpt['NormMethodL']) : (
				self.normMethod.cb.GetValue()),
			self.EqualLenLabel(self.confOpt['CorrMethodL']) : (
				self.corrMethod.cb.GetValue()),
			self.EqualLenLabel('Selected Columns') : (
				[int(x) for x in self.lbO.GetColContent(0)]),
			self.EqualLenLabel('Append to File') : self.checkB.GetValue(),
		}

		msgStep = msgPrefix + 'User input, processing'
		wx.CallAfter(self.dlg.UpdateStG, msgStep)
		#------------------------------> Dict with all values
		self.do = {
			'iFile'     : Path(self.iFile.tc.GetValue()),
			'oFile'     : Path(self.oFile.tc.GetValue()),
			'NormMethod': self.normMethod.cb.GetValue(),
			'CorrMethod': self.corrMethod.cb.GetValue(),
			'Column'    : [int(x) for x in self.lbO.GetColContent(0)],
			'Check'     : self.checkB.GetValue(),
		}
		#------------------------------> File base name
		self.oFolder = self.do['oFile'].parent
		#------------------------------> Date
		self.date = dtsMethod.StrNow()
		#endregion ----------------------------------------------------> Input

		return True
	#---

	def ReadInputFiles(self):
		"""Read input file and check data"""
		#region ---------------------------------------------------------> Msg
		msgPrefix = config.label['PdReadFile']
		#endregion ------------------------------------------------------> Msg

		#region ---------------------------------------------------> Data file
		msgStep = msgPrefix + f"{self.confOpt['iFileL']}, reading"
		wx.CallAfter(self.dlg.UpdateStG, msgStep)
		try:
			self.iFileObj = dtsFF.CSVFile(self.do['iFile'])
		except dtsException.FileIOError as e:
			self.msgError = str(e)
			self.tException = e
			return False
		#endregion ------------------------------------------------> Data file

		#region ------------------------------------------------------> Column
		msgStep = msgPrefix + f"{self.confOpt['iFileL']}, data type"
		wx.CallAfter(self.dlg.UpdateStG, msgStep)
		self.df = self.iFileObj.df.iloc[:,self.do['Column']]
		try:
			self.dfI = self.df.astype('float')
		except Exception as e:
			self.msgError  = config.msg['PDDataTypeCol']
			self.tException = e
			return False
		#endregion ---------------------------------------------------> Column

		return True
	#---

	def RunAnalysis(self):
		"""Calculate coefficients"""
		#region ---------------------------------------------------------> Msg
		msgPrefix = config.label['PdRun']
		#endregion ------------------------------------------------------> Msg

		#region -----------------------------------------------> Normalization
		msgStep = msgPrefix + f"Data normalization"
		wx.CallAfter(self.dlg.UpdateStG, msgStep)
		if self.do['NormMethod'] != 'None':
			try:
				self.dfN = dtsStatistic.DataNormalization(
					self.dfI,
					sel = None,
					method = self.do['NormMethod'],
				)
			except Exception as e:
				self.msgError = str(e)
				self.tException = e
				return False
		else:
			self.dfN = self.dfI.copy()
		#endregion --------------------------------------------> Normalization

		#region ------------------------------------> Correlation coefficients
		msgStep = msgPrefix + f"Correlation coefficients calculation"
		wx.CallAfter(self.dlg.UpdateStG, msgStep)
		try:
			self.dfCC = self.dfN.corr(method=self.do['CorrMethod'].lower())
		except Exception as e:
			self.msgError = str(e)
			self.tException = e
			return False
		#endregion ---------------------------------> Correlation coefficients

		return True
	#---

	def WriteOutput(self):
		"""Write output. Override as needed """
		
		#region ---------------------------------------------------------> Msg
		msgPrefix = config.label['PdWrite']
		#endregion ------------------------------------------------------> Msg
		
		#region -----------------------------------------------> Create folder
		msgStep = msgPrefix + 'Creating needed folder'
		wx.CallAfter(self.dlg.UpdateStG, msgStep)
		dataFolder = f"Data-{self.date}-{self.confOpt['Section']}"
		dataFolder = self.oFolder / dataFolder
		dataFolder.mkdir(parents=True, exist_ok=True)
		#endregion --------------------------------------------> Create folder
		
		#region --------------------------------------------------> Data files
		msgStep = msgPrefix + 'Data files'
		wx.CallAfter(self.dlg.UpdateStG, msgStep)

		dtsFF.WriteDFs2CSV(
			dataFolder, 
			{
				config.file['InitialN']: self.dfI,
				config.file['NormN']   : self.dfN,
				self.confOpt['MainData']  : self.dfCC,
			},
		)
		#endregion -----------------------------------------------> Data files
		
		#region --------------------------------------------------> Data files
		msgStep = msgPrefix + 'Main file'
		wx.CallAfter(self.dlg.UpdateStG, msgStep)
		#------------------------------> Create output dict
		dateDict = {
			self.date : {
				'V' : config.dictVersion,
				'I' : self.d,
				'CI': dtsMethod.DictVal2Str(
					self.do, 
					self.confOpt['ChangeKey'],
					new = True,
				),
				'R' : self.dfCC.to_dict(),
			}
		}
		#------------------------------> Append or not
		outData = self.SetOutputDict(dateDict)
		#------------------------------> Write
		dtsFF.WriteJSON(self.do['oFile'], outData)
		#endregion -----------------------------------------------> Data files

		#region ---------------------------------------------------> Print
		if config.development:
			print('Input')
			for k,v in self.do.items():
				print(str(k)+': '+str(v))

			print("DataFrames: Initial")
			print(self.dfI)
			print("")
			print("DataFrames: Norm")
			print(self.dfN)
			print("")
			print("DataFrames: CC")
			print(self.dfCC)
		else:
			pass
		#endregion ------------------------------------------------> Print

		return True
	#---

	def LoadResults(self):
		"""Load output file"""
		#region ---------------------------------------------------------> Msg
		msgPrefix = config.label['PdLoad']
		#endregion ------------------------------------------------------> Msg

		#region --------------------------------------------------------> Load
		wx.CallAfter(self.dlg.UpdateStG, msgPrefix)
		
		wx.CallAfter(method.LoadUMSAPFile, fileP=self.do['oFile'])
		#endregion -----------------------------------------------------> Load

		return True
	#---

	def RunEnd(self):
		"""Restart GUI and needed variables"""
		#region ---------------------------------------> Dlg progress dialogue
		if self.msgError is None:
			#--> 
			self.dlg.SuccessMessage(
				config.label['PdDone'],
				eTime=(config.label['PdEllapsed'] + self.deltaT),
			)
			#--> Show the 
			self.OnOFileChange('test')
		else:
			self.dlg.ErrorMessage(
				config.label['PdError'], 
				error      = self.msgError,
				tException = self.tException
			)
		#endregion ------------------------------------> Dlg progress dialogue

		#region -------------------------------------------------------> Reset
		self.msgError  = None # Error msg to show in self.RunEnd
		self.d         = {} # Dict with the user input as given
		self.do        = {} # Dict with the processed user input
		self.dfI       = None # pd.DataFrame for initial, normalized and
		self.dfN       = None # correlation coefficients
		self.dfCC      = None
		self.date      = None # date for corr file
		self.oFolder   = None # folder for output
		self.corrP     = None # path to the corr file that will be created
		self.deltaT    = None
		self.tException = None
		#endregion ----------------------------------------------------> Reset
	#---
	#endregion ------------------------------------------------> Class Methods
#---


class ProtProf(BaseConfModPanel):
	"""Creates the Proteome Profiling configuration tab

		Parameters
		----------
		parent

		Attributes
		----------
		

		Raises
		------
		

		Methods
		-------
		
	"""
	#region -----------------------------------------------------> Class setup
	name = 'ProtProfTab'
	#endregion --------------------------------------------------> Class setup

	#region --------------------------------------------------> Instance setup
	def __init__(self, parent):
		""" """
		#region -------------------------------------------------> Check Input
		
		#endregion ----------------------------------------------> Check Input

		#region -----------------------------------------------> Initial Setup
		confOpt = { # gui.tab, conf
			#------------------------------> URL
			'URL' : config.url['ProtProfPane'],
			#------------------------------> Labels
			# 'LenLongest' : len(config.label['CbNormalization']),
			'CorrectPL'   : 'P Correction',
			'MedianL'     : 'Median Correction',
			'GeneNameL'   : 'Gene Names',
			'ExcludeProtL': 'Exclude Proteins',
			#------------------------------> Hint
	
			#------------------------------> Choices
			'CorrectPChoice' : config.choice['CorrectP'],
			'MedianChoice' : config.choice['YesNo'],
			#------------------------------> Size
			
			#------------------------------> Tooltips
			
			#------------------------------> Progress Dialog
			'TitlePD' : f"Running {config.nameModules['ProtProf']} Analysis",
			'GaugePD' : 15,
			#------------------------------> Output
			'Section'  : config.nameModules['ProtProf'],
			# 'MainData' : 'Data-03-CorrelationCoefficients',
			'ChangeKey': ['iFile', 'oFile'],
		}

		confMsg = { # gui.tab, error msg
			
		}

		super().__init__(parent, confOpt=confOpt, confMsg=confMsg)
		#endregion --------------------------------------------> Initial Setup

		#region --------------------------------------------------------> Menu
		
		#endregion -----------------------------------------------------> Menu

		#region -----------------------------------------------------> Widgets
		self.correctP = dtsWidget.StaticTextComboBox(
			self.sbValue,
			self.confOpt['CorrectPL'],
			self.confOpt['CorrectPChoice'],
			validator = dtsValidator.IsNotEmpty(),
		)

		self.median = dtsWidget.StaticTextComboBox(
			self.sbValue,
			self.confOpt['MedianL'],
			self.confOpt['MedianChoice'],
			validator = dtsValidator.IsNotEmpty(),
		)

		self.geneName = dtsWidget.StaticTextCtrl(
			self.sbColumn,
			stLabel   = self.confOpt['GeneNameL'],
			tcSize    = self.confOpt['TwoInRow'],
			validator = dtsValidator.NumberList(
				numType = 'int',
				nN      = 1,
				vMin    = 0,
			)
		)
		
		self.excludeProt = dtsWidget.StaticTextCtrl(
			self.sbColumn,
			stLabel   = self.confOpt['ExcludeProtL'],
			tcSize    = self.confOpt['TwoInRow'],
			validator = dtsValidator.NumberList(
				numType = 'int',
				vMin    = 0,
			)
		)
		#endregion --------------------------------------------------> Widgets

		#region ------------------------------------------------------> Sizers
		#------------------------------> Sizer Values
		self.sizersbValueWid.Add(
			1, 1,
			pos    = (0,0),
			flag   = wx.EXPAND|wx.ALL,
			border = 5,
			span   = (2, 0),
		)
		self.sizersbValueWid.Add(
			self.scoreVal.st,
			pos    = (0,1),
			flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
			border = 5,
		)
		self.sizersbValueWid.Add(
			self.scoreVal.tc,
			pos    = (0,2),
			flag   = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL,
			border = 5,
		)
		self.sizersbValueWid.Add(
			self.normMethod.st,
			pos    = (1,1),
			flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
			border = 5,
		)
		self.sizersbValueWid.Add(
			self.normMethod.cb,
			pos    = (1,2),
			flag   = wx.EXPAND|wx.ALL,
			border = 5,
		)
		self.sizersbValueWid.Add(
			self.median.st,
			pos    = (0,3),
			flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
			border = 5,
		)
		self.sizersbValueWid.Add(
			self.median.cb,
			pos    = (0,4),
			flag   = wx.EXPAND|wx.ALL,
			border = 5,
		)
		self.sizersbValueWid.Add(
			self.correctP.st,
			pos    = (1,3),
			flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
			border = 5,
		)
		self.sizersbValueWid.Add(
			self.correctP.cb,
			pos    = (1,4),
			flag   = wx.EXPAND|wx.ALL,
			border = 5,
		)
		self.sizersbValueWid.Add(
			1, 1,
			pos    = (0,5),
			flag   = wx.EXPAND|wx.ALL,
			border = 5,
			span   = (2, 0),
		)
		self.sizersbValueWid.AddGrowableCol(0, 1)
		self.sizersbValueWid.AddGrowableCol(5, 1)
		#------------------------------> Sizer Columns
		self.sizersbColumnWid.Add(
			self.detectedProt.st,
			pos    = (0,0),
			flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
			border = 5,
		)
		self.sizersbColumnWid.Add(
			self.detectedProt.tc,
			pos    = (0,1),
			flag   = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL,
			border = 5,
		)
		self.sizersbColumnWid.Add(
			self.geneName.st,
			pos    = (0,2),
			flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
			border = 5,
		)
		self.sizersbColumnWid.Add(
			self.geneName.tc,
			pos    = (0,3),
			flag   = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL,
			border = 5,
		)
		self.sizersbColumnWid.Add(
			self.score.st,
			pos    = (0,4),
			flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
			border = 5,
		)
		self.sizersbColumnWid.Add(
			self.score.tc,
			pos    = (0,5),
			flag   = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL,
			border = 5,
		)
		self.sizersbColumnWid.Add(
			self.excludeProt.st,
			pos    = (1,0),
			flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
			border = 5,
		)
		self.sizersbColumnWid.Add(
			self.excludeProt.tc,
			pos    = (1,1),
			flag   = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL,
			border = 5,
			span   = (0, 5),
		)
		self.sizersbColumnWid.Add(
			self.colExtract.st,
			pos    = (2,0),
			flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
			border = 5,
		)
		self.sizersbColumnWid.Add(
			self.colExtract.tc,
			pos    = (2,1),
			flag   = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL,
			border = 5,
			span   = (0, 5),
		)
		self.sizersbColumnWid.Add(
			self.sizerRes,
			pos    = (3,0),
			flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND,
			border = 0,
			span   = (0,6),
		)
		self.sizersbColumnWid.AddGrowableCol(1,1)
		self.sizersbColumnWid.AddGrowableCol(3,1)
		self.sizersbColumnWid.AddGrowableCol(5,1)
		#------------------------------> Hide Checkbox
		if self.oFile.tc.GetValue() == '':
			self.sizersbFileWid.Hide(self.checkB)
		else:
			pass
		#------------------------------> Main Sizer
		self.SetSizer(self.Sizer)
		self.Sizer.Fit(self)
		#endregion ---------------------------------------------------> Sizers

		#region --------------------------------------------------------> Bind
		
		#endregion -----------------------------------------------------> Bind

		#region --------------------------------------------------------> Test
		import getpass
		user = getpass.getuser()
		if config.cOS == "Darwin":
			self.iFile.tc.SetValue("/Users/" + str(user) + "/TEMP-GUI/BORRAR-UMSAP/PlayDATA/PROTPROF/proteinGroups-kbr.txt")
			# self.oFile.tc.SetValue("/Users/" + str(user) + "/TEMP-GUI/BORRAR-UMSAP/PlayDATA/TARPROT/tarprot.umsap")
		elif config.cOS == 'Windows':
			from pathlib import Path
			# self.iFile.tc.SetValue(str(Path('C:/Users/bravo/Desktop/SharedFolders/BORRAR-UMSAP/PlayDATA/TARPROT/Mod-Enz-Dig-data-ms.txt')))
			# self.oFile.tc.SetValue(str(Path('C:/Users/bravo/Desktop/SharedFolders/BORRAR-UMSAP/PlayDATA/TARPROT')))
		else:
			pass
		self.normMethod.cb.SetValue("Log2")
		#endregion -----------------------------------------------------> Test
	#---
	#endregion -----------------------------------------------> Instance setup

	#region ---------------------------------------------------> Class methods
	
	#endregion ------------------------------------------------> Class methods
#---


class ResControlExp(wx.Panel):
	"""

		Parameters
		----------
		

		Attributes
		----------
		

		Raises
		------
		

		Methods
		-------
		
	"""
	#region -----------------------------------------------------> Class setup
	
	#endregion --------------------------------------------------> Class setup

	#region --------------------------------------------------> Instance setup
	def __init__(self, parent):
		""" """
		#region -------------------------------------------------> Check Input
		
		#endregion ----------------------------------------------> Check Input

		#region -----------------------------------------------> Initial Setup
		super().__init__(parent)
		#endregion --------------------------------------------> Initial Setup

		#region --------------------------------------------------------> Menu
		
		#endregion -----------------------------------------------------> Menu

		#region -----------------------------------------------------> Widgets
		
		#endregion --------------------------------------------------> Widgets

		#region ------------------------------------------------------> Sizers
		
		#endregion ---------------------------------------------------> Sizers

		#region --------------------------------------------------------> Bind
		
		#endregion -----------------------------------------------------> Bind

		#region ---------------------------------------------> Window position
		
		#endregion ------------------------------------------> Window position
	#---
	#endregion -----------------------------------------------> Instance setup

	#region ---------------------------------------------------> Class methods
	
	#endregion ------------------------------------------------> Class methods
#---
#endregion ----------------------------------------------------------> Classes


