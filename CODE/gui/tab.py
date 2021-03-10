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


""" Tabs of the application"""


#region -------------------------------------------------------------> Imports
import _thread 
from pathlib import Path
from requests.api import get

import wx
import wx.lib.agw.aui as aui

import dat4s_core.data.file as dtsFF
import dat4s_core.data.method as dtsMethod
import dat4s_core.data.statistic as dtsStatistic
import dat4s_core.exception.exception as dtsException
import dat4s_core.gui.wx.validator as dtsValidator
import dat4s_core.gui.wx.widget as dtsWidget
import dat4s_core.gui.wx.window as dtsWindow

import config.config as config
import gui.dtscore as dtscore
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Methods
#endregion ----------------------------------------------------------> Methods


#region -------------------------------------------------------------> Classes
#--> Base classses
# class BaseConfPanel(
# 	wx.Panel,
# 	dtsWidget.StaticBoxes, 
# 	dtsWidget.ButtonOnlineHelpClearAllRun
# 	):
# 	"""Creates the skeleton of a configuration tab. This includes the 
# 		wx.StaticBox, the Bottom Buttons and the statusbar.

# 		See Notes

# 		Parameters
# 		----------
# 		parent : wx Widget
# 			Parent of the widgets
# 		url : str
# 			URL for the Help button
# 		name : str
# 			Unique name of the tab
# 		oMode : str
# 			One of 'openO', 'openM', 'save', 'folder'. Default is 'folder'
# 		ext : str
# 			File extension for output file. Default is None since default for
# 			oMode is 'folder'
# 		statusbar : wx.StatusBar
# 			Statusbar of the application to display messages
# 		labeR : str
# 			Label of the Run button
# 		labelF : str
# 			Label of the File wx.StaticBox
# 		labelV : str
# 			Label of the Value wx.StaticBox
# 		labelC : str
# 			Label of the Column wx.StaticBox
# 		rightDelete : Boolean
# 			Enables clearing wx.StaticBox input with right click

# 		Attributes
# 		----------
# 		lbI : wx.ListCtrl
# 			ListCtrl to show information about the main input file
# 		lbO : wx.ListCtrl
# 			ListCtrl to show selected columns in lbI
# 		lbL : list of wx.ListCtrl
# 			To use when deleting the content on the wx.ListCtrl 
# 			e.g. self.LCtrlEmpty
# 		name : str
# 			Unique name of the tab
# 		btnRun : wx.Button
# 			Run button
# 		btnHelp : wx.Button
# 			Help button
# 		btnClearAll : wx.Button
# 			Clear All button
# 		sbFile : wx.StaticBox
# 			StaticBox to contain the input/output file information
# 		sbValue : wx.StaticBox
# 			StaticBox to contain the user-defined values
# 		sbColumn : wx.StaticBox
# 			StaticBox to contain the column numbers in the input files
# 		sizersbFile : wx.StaticBoxSizer
# 			StaticBoxSizer for sbFile
# 		sizersbValue : wx.StaticBoxSizer
# 			StaticBoxSizer for sbValue
# 		sizersbColumn : wx.StaticBoxSizer
# 			StaticBoxSizer for sbColumn
# 		sizersbFileWid : wx.GridBagSizer
# 			FlexGridSizer for widgets in sbFile
# 		sizersbValueWid : wx.GridBagSizer
# 			FlexGridSizer for widgets in sbValue
# 		sizersbColumnWid : wx.GridBagSizer
# 			FlexGridSizer for widgets in sbColumn		
# 		btnSizer : wx.FlexGridSizer
# 			To align the buttons
# 		Sizer : wx.BoxSizer
# 			Main sizer of the tab
		
# 		Notes
# 		-----
		
# 	"""
# 	#region -----------------------------------------------------> Class setup
	
# 	#endregion --------------------------------------------------> Class setup

# 	#region --------------------------------------------------> Instance setup
# 	def __init__(self, parent, url, name,
# 		oMode       = 'save',
# 		statusbar   = None,
# 		labelR      = config.label['Button']['Run'],
# 		labelF      = config.label['StaticBox']['File'],
# 		labelV      = config.label['StaticBox']['Value'],
# 		labelC      = config.label['StaticBox']['Column'],
# 		rightDelete = True
# 		):
# 		""" """
# 		#region -----------------------------------------------> Initial Setup
# 		self.parent    = parent
# 		self.statusbar = statusbar

# 		wx.Panel.__init__(self, parent, name=name)

# 		dtsWidget.ButtonOnlineHelpClearAllRun.__init__(self, self, url, 
# 			labelR    = labelR,
# 		)

# 		dtsWidget.StaticBoxes.__init__(self, self, 
# 			labelF      = labelF,
# 			labelV      = labelV,
# 			labelC      = labelC,
# 			rightDelete = rightDelete,
# 		)
# 		#endregion --------------------------------------------> Initial Setup

# 		#region -----------------------------------------------------> Widgets
# 		self.iFile = dtsWidget.ButtonTextCtrlFF(self.sbFile,
# 			btnLabel   = config.label[self.name]['iFile'],
# 			ext        = config.extLong['Data'],
# 			tcHint     = config.hint[self.name]['iFile'],
# 			tcStyle    = wx.TE_READONLY,
# 			validator  = wx.DefaultValidator,
# 			ownCopyCut = True,
# 		)

# 		self.oFile = dtsWidget.ButtonTextCtrlFF(self.sbFile,
# 			btnLabel   = config.label[self.name]['oFile'],
# 			mode       = oMode,
# 			ext        = config.extLong['UMSAP'],
# 			tcHint     = config.hint[self.name]['oFile'],
# 			tcStyle    = wx.TE_READONLY,
# 			validator  = wx.DefaultValidator,
# 			ownCopyCut = True,
# 		)

# 		self.checkB = wx.CheckBox(
# 			self.sbFile,
# 			label = config.label[self.name]['Check'],
# 		)
# 		self.checkB.SetValue(True)
# 		#endregion --------------------------------------------------> Widgets

# 		#region ------------------------------------------------------> Sizers
# 		self.sizersbFileWid.Add(
# 			self.iFile.btn,
# 			pos    = (0,0),
# 			flag   = wx.EXPAND|wx.ALL,
# 			border = 5
# 		)
# 		self.sizersbFileWid.Add(
# 			self.iFile.tc,
# 			pos    = (0,1),
# 			flag   = wx.EXPAND|wx.ALL,
# 			border = 5
# 		)
# 		self.sizersbFileWid.Add(
# 			self.oFile.btn,
# 			pos    = (1,0),
# 			flag   = wx.EXPAND|wx.ALL,
# 			border = 5
# 		)
# 		self.sizersbFileWid.Add(
# 			self.oFile.tc,
# 			pos    = (1,1),
# 			flag   = wx.EXPAND|wx.ALL,
# 			border = 5
# 		)
# 		self.sizersbFileWid.Add(
# 			self.checkB,
# 			pos    = (2,1),
# 			flag   = wx.ALIGN_LEFT|wx.ALL,
# 			border = 5,
# 		)
# 		self.sizersbFileWid.AddGrowableCol(1,1)
# 		self.sizersbFileWid.AddGrowableRow(0,1)

# 		self.Sizer = wx.BoxSizer(wx.VERTICAL)

# 		self.Sizer.Add(self.sizersbFile, 0, wx.EXPAND|wx.ALL, 5)
# 		self.Sizer.Add(self.sizersbValue, 0, wx.EXPAND|wx.ALL, 5)
# 		self.Sizer.Add(self.sizersbColumn, 0, wx.EXPAND|wx.ALL, 5)
# 		self.Sizer.Add(self.btnSizer, 0, wx.ALIGN_CENTER|wx.ALL, 5)
# 		#endregion ---------------------------------------------------> Sizers

# 		#region --------------------------------------------------------> Bind
# 		self.oFile.tc.Bind(wx.EVT_TEXT, self.OnOFileChange)
# 		#endregion -----------------------------------------------------> Bind
# 	#---
# 	#endregion -----------------------------------------------> Instance setup

# 	#region ---------------------------------------------------> Class methods
# 	def LCtrlFill(self, fileP):
# 		"""Fill the wx.ListCtrl after selecting path to the folder. This is
# 			called from within self.iFile
	
# 			Parameters
# 			----------
# 			fileP : Path
# 				Folder path
# 		"""
# 		#region ----------------------------------------------------> Del list
# 		self.LCtrlEmpty()
# 		#endregion -------------------------------------------------> Del list
		
# 		#region ---------------------------------------------------> Fill list
# 		try:
# 			dtsMethod.LCtrlFillColNames(self.lbI, fileP)
# 		except Exception as e:
# 			dtscore.Notification(
# 				'errorF',
# 				msg        = str(e),
# 				tException = e,
# 			)
# 			return False
# 		#endregion ------------------------------------------------> Fill list
		
# 		#region -----------------------------------------> Columns in the file
# 		self.NCol = self.lbI.GetItemCount()
# 		#endregion --------------------------------------> Columns in the file

# 		return True
# 	#---	

# 	def OnIFileEmpty(self, event):
# 		"""Clear GUI elements when Data Folder is ''
	
# 			Parameters
# 			----------
# 			event: wx.Event
# 				Information about the event		
# 		"""
# 		if self.iFile.tc.GetValue() == '':
# 			self.LCtrlEmpty()
# 		else:
# 			pass

# 		return True
# 	#---

# 	def LCtrlEmpty(self):
# 		"""Clear wx.ListCtrl and NCol """
# 		#region -------------------------------------------------> Delete list
# 		for l in self.lbL:
# 			l.DeleteAllItems()
# 		#endregion ----------------------------------------------> Delete list
		
# 		#region ---------------------------------------------------> Set NCol
# 		self.NCol = None
# 		#endregion ------------------------------------------------> Set NCol

# 		return True
# 	#---

# 	def OnOFileChange(self, event):
# 		"""Show/Hide self.checkB
	
# 			Parameters
# 			----------
# 			event: wx.Event
# 				Information about the event
# 		"""
# 		if self.oFile.tc.GetValue() == '':
# 			self.sizersbFileWid.Hide(self.checkB)
# 			self.Sizer.Layout()
# 		else:
# 			self.checkB.SetValue(True)
# 			self.sizersbFileWid.Show(self.checkB)
# 			self.Sizer.Layout()
# 	#---
# 	#endregion ------------------------------------------------> Class methods
# #---


class Start(wx.Panel):
	"""Start tab
	
		Parameters
		----------
		parent : wx widget
			Parent of the tab. 
		name : str
			Name of the tab. Unique name for the application
		statusbar : wx.SatusBar
			Statusbar to display info
		args : extra arguments

		Attributes
		----------
		parent : wx widget
			Parent of the tab. 
		name : str
			Name of the tab. Unique name for the application
		statusbar : wx.SatusBar
			Statusbar to display info
		btnLimProt : wx.Button
			Launch the Limited Proteolysis module
		btnProtProf : wx.Button
			Launch the Proteome profiling module
		btnTarProt : wx.Button
			Launch the Targeted Proteolysis module
		Sizer : wx.BoxSizer
			Main sizer of the app
		SizerGrid : wx.GridBagSizer
			Sizer to hold the widgets
		Sizerbtn : wx.BoxSizer
			Sizer for the buttons
	"""

	#region --------------------------------------------------> Instance setup
	def __init__(self, parent, statusbar):
		""""""
		#region -----------------------------------------------> Initial setup
		self.name   = 'StartTab'
		self.parent = parent
		self.confOpt = getattr(config, self.name)

		super().__init__(parent=parent, name=self.name)
		#endregion --------------------------------------------> Initial setup
		
		#region -----------------------------------------------------> Widgets
		#--> Statusbar
		self.statusbar = statusbar
		#--> Images
		self.img = wx.StaticBitmap(
			self, 
			bitmap=wx.Bitmap(
				str(self.confOpt['Img']), 
				wx.BITMAP_TYPE_ANY,
			),
		)
		#---
		#--> Buttons
		self.btnLimProt  = wx.Button(self, label=self.confOpt['LimProtLabel'])
		self.btnProtProf = wx.Button(self, label=self.confOpt['ProtProfLabel'])
		self.btnTarProt  = wx.Button(self, label=self.confOpt['TarProtLabel'])
		#endregion --------------------------------------------------> Widgets

		#region ----------------------------------------------------> Tooltips
		self.btnLimProt.SetToolTip(self.confOpt['LimProtTT'])
		self.btnTarProt.SetToolTip(self.confOpt['TarProtTT'])
		self.btnProtProf.SetToolTip(self.confOpt['ProtProfTT'])
		#endregion -------------------------------------------------> Tooltips
		
		#region ------------------------------------------------------> Sizers
		#--> Sizers
		self.Sizer	 = wx.BoxSizer(wx.VERTICAL)
		self.SizerGrid = wx.GridBagSizer(1,1)
		self.SizerBtn  = wx.BoxSizer(wx.VERTICAL)
		#--> Add widgets
		self.SizerBtn.Add(
			self.btnLimProt, 0, wx.EXPAND|wx.ALL, 5
		)
		self.SizerBtn.Add(
			self.btnProtProf, 0, wx.EXPAND|wx.ALL, 5
		)
		self.SizerBtn.Add(
			self.btnTarProt, 0, wx.EXPAND|wx.ALL, 5
		)

		self.SizerGrid.Add(
			self.img, 
			pos	= (0,0),
			flag   = wx.EXPAND|wx.ALL,
			border = 5,
		)
		self.SizerGrid.Add(
			self.SizerBtn, 
			pos	= (0,1),
			flag   = wx.ALIGN_CENTRE_VERTICAL|wx.ALL,
			border = 5,
		)

		self.Sizer.AddStretchSpacer(1)
		self.Sizer.Add(
			self.SizerGrid, 0, wx.CENTER|wx.ALL, 5
		)
		self.Sizer.AddStretchSpacer(1)

		self.SetSizer(self.Sizer)
		self.Sizer.Fit(self)
		#endregion ---------------------------------------------------> Sizers

		#region --------------------------------------------------------> Bind

		#endregion -----------------------------------------------------> Bind
	#endregion -----------------------------------------------> Instance setup
#---


# class CorrA(BaseConfPanel):
# 	"""Creates the configuration tab for Correlation Analysis
	
# 		Parameters
# 		----------
# 		parent : wx Widget
# 			Parent of the widgets
# 		url : str
# 			URL for the Help button
# 		statusbar : wx.StatusBar
# 			Statusbar of the application to display messages

# 		Attributes
# 		----------
# 		parent : wx Widget
# 			Parent of the widgets
# 		name : str
# 			Unique id of the pane in the app
# 		msgError : Str or None
# 			Error message to show when analysis fails
# 		do : dict
# 			Dict with the processed user input
# 			{
# 				'iFile'     : 'input file path',
# 				'oFolder'   : 'output folder path',
# 				'NormMethod': 'normalization method',
# 				'CorrMethod': 'correlation method',
# 				'Column'    : [selected columns as integers],
# 			}
# 		d : dict
# 			Similar to 'do' but with the values given by the user
# 		dfI : pdDataFrame
# 			Dataframe with initial values after columns were extracted and type
# 			assigned.
# 		dfN : pdDataFrame
# 			Dataframe after normalization
# 		dfCC : pdDataFrame
# 			Dataframe with correlation coefficients
# 		date : str
# 			Date time stamp as given by dtsMethod.StrNow()
# 		corrP : Path
# 			Path to the corr file that will be created


# 		Notes
# 		-----
# 		Running the analysis results in the creation of
# 		OutPut-Folder
# 		|
# 		 - Data
# 		   |
# 		    - OutPut-Folder-1-Data-Initial.txt
# 			- OutPut-Folder-2-Data-Normalization.txt
# 			- OutPut-Folder-3-Data-CC-Values.txt
# 		 - OutPut-Folder.corr
		
# 		The files in Data are regular csv files with the data at the end of the
# 		corresponding step.

# 		The .corr file conteins the information about the calculations, e.g

# 		{
# 			'Correlation-Analysis : {
# 				'20210324-165609': {
# 					'V' : config.dictVersion,
# 					'I' : self.d,
# 					'CI': self.do,
# 					'R' : pd.DataFrame (dict) with the correlation coefficients
# 				}
# 			}
# 		}
# 	"""
# 	#region -----------------------------------------------------> Class Setup
# 	name = 'CorrA'
# 	#endregion --------------------------------------------------> Class Setup
	
# 	#region --------------------------------------------------> Instance setup
# 	def __init__(self, parent, statusbar):
# 		""""""
# 		#region -----------------------------------------------> Initial setup
# 		self.parent   = parent
# 		self.msgError = None # Error msg to show in self.RunEnd
# 		self.d        = {} # Dict with the user input as given
# 		self.do       = {} # Dict with the processed user input
# 		self.dfI      = None # pd.DataFrame for initial, normalized and
# 		self.dfN      = None # correlation coefficients
# 		self.dfCC     = None
# 		self.date     = None # date for corr file
# 		self.corrP    = None # path to the corr file that will be created

# 		super().__init__(
# 			parent, 
# 			config.url[self.name], 
# 			self.name, 
# 			statusbar=statusbar
# 		)
# 		#endregion --------------------------------------------> Initial setup
		
# 		#region -----------------------------------------------------> Widgets
# 		#------------------------------> File
# 		self.iFile.tc.SetValidator(
# 			dtsValidator.InputFF(
# 				fof = 'file',
# 				ext = config.extShort['Data'],
# 			)
# 		)
# 		self.iFile.afterBtn = self.LCtrlFill

# 		self.oFile.tc.SetValidator(
# 			dtsValidator.OutputFF(
# 				fof = 'folder',
# 				opt = False,
# 			)
# 		)
# 		#------------------------------> Values
# 		self.normMethod = dtsWidget.StaticTextComboBox(self.sbValue, 
# 			label     = config.label[self.name]['NormMethod'],
# 			choices   = config.choice[self.name]['NormMethod'],
# 			validator = dtsValidator.IsNotEmpty(),
# 		)
# 		self.corrMethod = dtsWidget.StaticTextComboBox(self.sbValue, 
# 			label     = config.label[self.name]['CorrMethod'],
# 			choices   = config.choice[self.name]['CorrMethod'],
# 			validator = dtsValidator.IsNotEmpty(),
# 		)
# 		#------------------------------> Columns
# 		self.stListI = wx.StaticText(
# 			self.sbColumn, 
# 			label = config.label[self.name]['iList'],
# 		)
# 		self.stListO = wx.StaticText(
# 			self.sbColumn, 
# 			label = config.label[self.name]['oList'],
# 		)

# 		self.lbI = dtsWidget.ListZebra(self.sbColumn, 
# 			colLabel     = config.label[self.name]['ListColumn'],
# 			colSize      = config.size[self.name]['List'],
# 		)
# 		self.lbO = dtsWidget.ListZebra(self.sbColumn, 
# 			colLabel     = config.label[self.name]['ListColumn'],
# 			colSize      = config.size[self.name]['List'],
# 			canPaste     = True,
# 			canCut       = True,
# 		)
# 		self.lbL = [self.lbI, self.lbO]

# 		self.addCol = wx.Button(self.sbColumn, 
# 			label = config.label[self.name]['Add'],
# 		)
# 		self.addCol.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_GO_FORWARD), 
# 			dir = wx.RIGHT,
# 		)
# 		#endregion --------------------------------------------------> Widgets

# 		#region -----------------------------------------------------> Tooltip
# 		self.stListI.SetToolTip(config.tooltip[self.name]['stListI'])
# 		self.stListO.SetToolTip(config.tooltip[self.name]['stListO'])
# 		self.addCol.SetToolTip(config.tooltip[self.name]['btnAddCol'])
# 		#endregion --------------------------------------------------> Tooltip

# 		#region ------------------------------------------------------> Sizers
# 		#------------------------------> Expand Column section
# 		item = self.Sizer.GetItem(self.sizersbColumn)
# 		item.Proportion = 1
# 		item = self.sizersbColumn.GetItem(self.sizersbColumnWid)
# 		item.Proportion = 1
# 		#------------------------------> Values
# 		self.sizersbValueWid.Add(
# 			1, 1,
# 			pos    = (0,0),
# 			flag   = wx.EXPAND|wx.ALL,
# 			border = 5
# 		)
# 		self.sizersbValueWid.Add(
# 			self.normMethod.st,
# 			pos    = (0,1),
# 			flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL,
# 			border = 5,
# 		)
# 		self.sizersbValueWid.Add(
# 			self.normMethod.cb,
# 			pos    = (0,2),
# 			flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL,
# 			border = 5,
# 		)
# 		self.sizersbValueWid.Add(
# 			self.corrMethod.st,
# 			pos    = (0,3),
# 			flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL,
# 			border = 5,
# 		)
# 		self.sizersbValueWid.Add(
# 			self.corrMethod.cb,
# 			pos    = (0,4),
# 			flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL,
# 			border = 5,
# 		)
# 		self.sizersbValueWid.Add(
# 			1, 1,
# 			pos    = (0,5),
# 			flag   = wx.EXPAND|wx.ALL,
# 			border = 5
# 		)
# 		self.sizersbValueWid.AddGrowableCol(0, 1)
# 		self.sizersbValueWid.AddGrowableCol(5, 1)
# 		#------------------------------> Columns
# 		self.sizersbColumnWid.Add(
# 			self.stListI,
# 			pos    = (0,0),
# 			flag   = wx.ALIGN_CENTRE|wx.ALL,
# 			border = 5
# 		)
# 		self.sizersbColumnWid.Add(
# 			self.stListO,
# 			pos    = (0,2),
# 			flag   = wx.ALIGN_CENTRE|wx.ALL,
# 			border = 5
# 		)
# 		self.sizersbColumnWid.Add(
# 			self.lbI,
# 			pos    = (1,0),
# 			flag   = wx.EXPAND|wx.ALL,
# 			border = 20
# 		)
# 		self.sizersbColumnWid.Add(
# 			self.addCol,
# 			pos    = (1,1),
# 			flag   = wx.ALIGN_CENTER|wx.ALL,
# 			border = 20
# 		)
# 		self.sizersbColumnWid.Add(
# 			self.lbO,
# 			pos    = (1,2),
# 			flag   = wx.EXPAND|wx.ALL,
# 			border = 20
# 		)
# 		self.sizersbColumnWid.AddGrowableCol(0, 1)
# 		self.sizersbColumnWid.AddGrowableCol(2, 1)
# 		self.sizersbColumnWid.AddGrowableRow(1, 1)
# 		#------------------------------> Hide Checkbox
# 		if self.oFile.tc.GetValue() == '':
# 			self.sizersbFileWid.Hide(self.checkB)
# 		else:
# 			pass
# 		#------------------------------> Main Sizer
# 		self.SetSizer(self.Sizer)
# 		self.Sizer.Fit(self)
# 		#endregion ---------------------------------------------------> Sizers

# 		#region --------------------------------------------------------> Bind
# 		self.addCol.Bind(wx.EVT_BUTTON, self.OnAdd)
# 		self.iFile.tc.Bind(wx.EVT_TEXT, self.OnIFileEmpty)
# 		#endregion -----------------------------------------------------> Bind
	
# 		#region --------------------------------------------------------> Test
# 		import getpass
# 		user = getpass.getuser()
# 		if config.cOS == "Darwin":
# 			self.iFile.tc.SetValue("/Users/" + str(user) + "/TEMP-GUI/BORRAR-UMSAP/PlayDATA/TARPROT/Mod-Enz-Dig-data-ms.txt")
# 			self.oFile.tc.SetValue("/Users/" + str(user) + "/TEMP-GUI/BORRAR-UMSAP/PlayDATA/TARPROT")
# 		elif config.cOS == 'Windows':
# 			from pathlib import Path
# 			self.iFile.tc.SetValue(str(Path('C:/Users/bravo/Desktop/SharedFolders/BORRAR-UMSAP/PlayDATA/TARPROT/Mod-Enz-Dig-data-ms.txt')))
# 			self.oFile.tc.SetValue(str(Path('C:/Users/bravo/Desktop/SharedFolders/BORRAR-UMSAP/PlayDATA/TARPROT')))
# 		else:
# 			pass
# 		self.normMethod.cb.SetValue("Log2")
# 		self.corrMethod.cb.SetValue("Pearson")
# 		#endregion -----------------------------------------------------> Test
# 	#---
# 	#endregion -----------------------------------------------> Instance setup

# 	#region ---------------------------------------------------> Class Methods
# 	def OnAdd(self, event):
# 		"""Add columns to analyse
	
# 			Parameters
# 			----------
# 			event : wx.Event
# 				Event information
# 		"""
# 		self.lbI.Copy()
# 		self.lbO.Paste()
# 	#---

# 	#-------------------------------------> Run analysis methods
# 	def OnRun(self, event):
# 		""" Start corraltion coefficients calculation

# 			Parameter
# 			---------
# 			event : wx.Event
# 				Event information
# 		"""
# 		#region --------------------------------------------------> Dlg window
# 		self.dlg = dtsWindow.ProgressDialog(
# 			self, 
# 			config.title['CorrA_PD'], 
# 			config.gauge[self.name], 
# 			img = config.img['Icon'],
# 		)
# 		#endregion -----------------------------------------------> Dlg window

# 		#region ------------------------------------------------------> Thread
# 		_thread.start_new_thread(self.Run, ('test',))
# 		#endregion ---------------------------------------------------> Thread

# 		#region ----------------------------------------> Show progress dialog
# 		if self.dlg.ShowModal() == wx.ID_OK:
# 			self.dlg.Destroy()
# 		else:
# 			self.dlg.Destroy()
# 		#endregion -------------------------------------> Show progress dialog

# 		return True
# 	#---

# 	def CheckInput(self):
# 		"""Check user input"""
		
# 		#region ---------------------------------------------------------> Msg
# 		msgPrefix = config.label['DlgProgress']['Check']
# 		#endregion ------------------------------------------------------> Msg
		
# 		#region -------------------------------------------> Individual Fields
# 		#------------------------------> Input file
# 		msgStep = msgPrefix + config.label[self.name]['iFile']
# 		wx.CallAfter(self.dlg.UpdateStG, msgStep)
# 		a, b = self.iFile.tc.GetValidator().Validate()
# 		if a:
# 			pass
# 		else:
# 			self.msgError = config.msg['Error'][self.name]['iFile'][b[0]]
# 			return False
# 		#------------------------------> Output Folder
# 		msgStep = msgPrefix + config.label[self.name]['oFile']
# 		wx.CallAfter(self.dlg.UpdateStG, msgStep)
# 		a, b = self.oFile.tc.GetValidator().Validate()
# 		if a:
# 			pass
# 		else:
# 			self.msgError = config.msg['Error'][self.name]['oFile'][b[0]]
# 			return False
# 		#------------------------------> Normalization
# 		msgStep = msgPrefix + config.label[self.name]['NormMethod']
# 		wx.CallAfter(self.dlg.UpdateStG, msgStep)
# 		if self.normMethod.cb.GetValidator().Validate()[0]:
# 			pass
# 		else:
# 			self.msgError = config.msg['Error'][self.name]['NormMethod']
# 			return False
# 		#------------------------------> Corr Method
# 		msgStep = msgPrefix + config.label[self.name]['CorrMethod']
# 		wx.CallAfter(self.dlg.UpdateStG, msgStep)
# 		if self.corrMethod.cb.GetValidator().Validate()[0]:
# 			pass
# 		else:
# 			self.msgError = config.msg['Error'][self.name]['CorrMethod']
# 			return False
# 		#------------------------------> ListCtrl
# 		msgStep = msgPrefix + config.label[self.name]['oList']
# 		wx.CallAfter(self.dlg.UpdateStG, msgStep)
# 		if self.lbO.GetItemCount() > 1:
# 			pass
# 		else:
# 			self.msgError = config.msg['Error'][self.name]['oList']
# 			return False
# 		#endregion ----------------------------------------> Individual Fields

# 		return True
# 	#---

# 	def PrepareRun(self):
# 		"""Set variable and prepare data for analysis."""
		
# 		#region ---------------------------------------------------------> Msg
# 		msgPrefix = config.label['DlgProgress']['Prepare']
# 		#endregion ------------------------------------------------------> Msg

# 		#region -------------------------------------------------------> Input
# 		msgStep = msgPrefix + 'User input, reading'
# 		wx.CallAfter(self.dlg.UpdateStG, msgStep)
# 		#------------------------------> As given
# 		self.d = {
# 			'iFile'     : self.iFile.tc.GetValue(),
# 			'oFolder'   : self.oFile.tc.GetValue(),
# 			'NormMethod': self.normMethod.cb.GetValue(),
# 			'CorrMethod': self.corrMethod.cb.GetValue(),
# 			'Column'    : [int(x) for x in self.lbO.GetColContent(0)],
# 		}

# 		msgStep = msgPrefix + 'User input, processing'
# 		wx.CallAfter(self.dlg.UpdateStG, msgStep)
# 		#------------------------------> Dict with all values
# 		self.do = {
# 			'iFile'     : Path(self.d['iFile']),
# 			'oFolder'   : Path(self.d['oFolder']),
# 			'NormMethod': self.normMethod.cb.GetValue(),
# 			'CorrMethod': self.corrMethod.cb.GetValue(),
# 			'Column'    : [int(x) for x in self.lbO.GetColContent(0)],
# 		}
# 		#------------------------------> File base name
# 		self.fileBaseName = self.do['oFolder'].name
# 		#------------------------------> Date
# 		self.date = dtsMethod.StrNow()
# 		#endregion ----------------------------------------------------> Input

# 		return True
# 	#---

# 	def ReadInputFiles(self):
# 		"""Read input file and check data"""
# 		#region ---------------------------------------------------------> Msg
# 		msgPrefix = config.label['DlgProgress']['ReadFile']
# 		#endregion ------------------------------------------------------> Msg

# 		#region ---------------------------------------------------> Data file
# 		msgStep = msgPrefix + f"{config.label[self.name]['iFile']}, reading"
# 		wx.CallAfter(self.dlg.UpdateStG, msgStep)
# 		try:
# 			self.iFileObj = dtsFF.CSVFile(self.do['iFile'])
# 		except dtsException.FileIOError as e:
# 			self.msgError = str(e)
# 			return False
# 		#endregion ------------------------------------------------> Data file

# 		#region ------------------------------------------------------> Column
# 		msgStep = msgPrefix + f"{config.label[self.name]['iFile']}, data type"
# 		wx.CallAfter(self.dlg.UpdateStG, msgStep)
# 		self.df = self.iFileObj.df.iloc[:,self.do['Column']]
# 		try:
# 			self.dfI = self.df.astype('float')
# 		except Exception as e:
# 			self.msgError = (
# 				config.msg['Error']['PD']['DataTypeCol']
# 				+ f"\n\nFurther details:\n{e}\n"
# 			)
# 			return False
# 		#endregion ---------------------------------------------------> Column

# 		return True
# 	#---

# 	def RunAnalysis(self):
# 		"""Calculate coefficients"""
# 		#region ---------------------------------------------------------> Msg
# 		msgPrefix = config.label['DlgProgress']['Run']
# 		#endregion ------------------------------------------------------> Msg

# 		#region -----------------------------------------------> Normalization
# 		msgStep = msgPrefix + f"Data normalization"
# 		wx.CallAfter(self.dlg.UpdateStG, msgStep)
# 		if self.do['NormMethod'] != 'None':
# 			try:
# 				self.dfN = dtsStatistic.DataNormalization(
# 					self.dfI,
# 					sel = None,
# 					method = self.do['NormMethod'],
# 				)
# 			except Exception as e:
# 				self.msgError = str(e)
# 				return False
# 		else:
# 			self.dfN = self.dfI.copy()
# 		#endregion --------------------------------------------> Normalization

# 		#region ------------------------------------> Correlation coefficients
# 		msgStep = msgPrefix + f"Correlation coefficients calculation"
# 		wx.CallAfter(self.dlg.UpdateStG, msgStep)
# 		self.dfCC = self.dfN.corr(method=self.do['CorrMethod'].lower())
# 		#endregion ---------------------------------> Correlation coefficients

# 		return True
# 	#---

# 	def WriteOutput(self):
# 		"""Write output. Override as needed """
		
# 		#region ---------------------------------------------------------> Msg
# 		msgPrefix = config.label['DlgProgress']['Write']
# 		#endregion ------------------------------------------------------> Msg
		
# 		#region ----------------------------------------------> Create folders
# 		msgStep = msgPrefix + 'Creating needed folders'
# 		wx.CallAfter(self.dlg.UpdateStG, msgStep)
# 		self.do['oFolder'].mkdir(parents=True, exist_ok=True)
# 		dataFolder = self.do['oFolder']/'Data'
# 		dataFolder.mkdir(parents=True, exist_ok=True)
# 		#endregion -------------------------------------------> Create folders
		
# 		#region --------------------------------------------------> Data files
# 		msgStep = msgPrefix + 'Data files'
# 		wx.CallAfter(self.dlg.UpdateStG, msgStep)

# 		dtsFF.WriteDFs2CSV(
# 			dataFolder, 
# 			{
# 				self.fileBaseName + '-' + config.file['Name']['DataStep']['Init'] : self.dfI,
# 				self.fileBaseName + '-' + config.file['Name']['DataStep']['Norm'] : self.dfN,
# 				self.fileBaseName + '-' + config.file['Name'][self.name]['MainD'] : self.dfCC,
# 			},
# 		)
# 		#endregion -----------------------------------------------> Data files
		
# 		#region --------------------------------------------------> Data files
# 		msgStep = msgPrefix + 'Main file'
# 		wx.CallAfter(self.dlg.UpdateStG, msgStep)

# 		self.corrP = self.do['oFolder'] / (self.fileBaseName + config.extShort[self.name][0])
# 		outData = {
# 			config.file['ID'][self.name]: {
# 				self.date : {
# 					'V' : config.dictVersion,
# 					'I' : self.d,
# 					'CI': dtsMethod.DictVal2Str(
# 						self.do, 
# 						config.changeKey[self.name],
# 						new = True,
# 					),
# 					'R' : self.dfCC.to_dict(),
# 				}
# 			}
# 		}

# 		dtsFF.WriteJSON(self.corrP, outData)
# 		#endregion -----------------------------------------------> Data files

# 		#region ---------------------------------------------------> Print
# 		if config.development:
# 			print('Input')
# 			for k,v in self.do.items():
# 				print(str(k)+': '+str(v))

# 			print("DataFrames: Initial")
# 			print(self.dfI)
# 			print("")
# 			print("DataFrames: Norm")
# 			print(self.dfN)
# 			print("")
# 			print("DataFrames: CC")
# 			print(self.dfCC)
# 		else:
# 			pass
# 		#endregion ------------------------------------------------> Print

# 		return True
# 	#---

# 	def LoadResults(self):
# 		"""Load .corr file"""
# 		#region ---------------------------------------------------------> Msg
# 		msgPrefix = config.label['DlgProgress']['Load']
# 		#endregion ------------------------------------------------------> Msg

# 		#region --------------------------------------------------------> Load
# 		msgStep = msgPrefix + '.corr'
# 		wx.CallAfter(self.dlg.UpdateStG, msgStep)
		
# 		wx.CallAfter(config.mainW.ReadUMSAPOutFile, self.corrP)
# 		#endregion -----------------------------------------------------> Load

# 		return True
# 	#---

# 	def RunEnd(self):
# 		"""Restart GUI and needed variables"""
# 		#region ---------------------------------------> Dlg progress dialogue
# 		if self.msgError is None:
# 			self.dlg.SuccessMessage(config.label['DlgProgress']['Done'])
# 			self.oFile.tc.SetValue('') # Avoid overwrite only if ended fine
# 		else:
# 			self.dlg.ErrorMessage(
# 				config.label['DlgProgress']['Error'], 
# 				error = self.msgError,
# 			)
# 		#endregion ------------------------------------> Dlg progress dialogue

# 		#region -------------------------------------------------------> Reset
# 		self.msgError = None # Error msg to show in self.RunEnd
# 		self.d        = {} # Dict with the user input as given
# 		self.do       = {} # Dict with the processed user input
# 		self.dfI      = None # pd.DataFrame for initial, normalized and
# 		self.dfN      = None # correlation coefficients
# 		self.dfCC     = None
# 		self.date     = None # date for corr file
# 		self.corrP    = None # path to the corr file that will be created
# 		#endregion ----------------------------------------------------> Reset
# 	#---
# 	#endregion ------------------------------------------------> Class Methods
# #---
#endregion ----------------------------------------------------------> Classes
