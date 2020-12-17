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


""" Panes of the application"""

#region -------------------------------------------------------------> Imports
import wx

import webbrowser

import dat4s_core.widget.wx_widget as dtsWidget
import dat4s_core.validator.validator as dtsValidator

import config.config as config
#endregion ----------------------------------------------------------> Imports

#region -------------------------------------------------------------> Methods
#endregion ----------------------------------------------------------> Methods

#region -------------------------------------------------------------> Classes
class BaseConfPane(wx.Panel,
	dtsWidget.StaticBoxes, 
	dtsWidget.ButtonOnlineHelpClearAllRun
	):
	"""Creates the skeleton of a configuration pane. This includes the 
		wx.StaticBox and the Bottom Buttons

		Parameters
		----------
		parent : wx Widget
			Parent of the widgets
		url : str
			URL for the Help button
		name : str
			Unique name of the pane
		statusbar : wx.StatusBar
			Statusbar of the application to display messages
		labeR : str
			Label of the Run button
		labelF : str
			Label of the File wx.StaticBox
		labelV : str
			Label of the Value wx.StaticBox
		labelC : str
			Label of the Column wx.StaticBox

		Attributes
		----------
		name : str
			Unique name of the pane
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
			Main sizer of the pane
		
		Methods
		-------
		
	"""
	#region -----------------------------------------------------> Class setup
	
	#endregion --------------------------------------------------> Class setup

	#region --------------------------------------------------> Instance setup
	def __init__(self, parent, url, name,  
		statusbar = None,
		labelR    = config.label['Button']['Run'],
		labelF    = config.label['StaticBox']['File'],
		labelV    = config.label['StaticBox']['Value'],
		labelC    = config.label['StaticBox']['Column'],
		):
		""" """
		#region -----------------------------------------------> Initial Setup
		self.name   = name
		self.parent = parent

		wx.Panel.__init__(self, parent, name=name)

		dtsWidget.ButtonOnlineHelpClearAllRun.__init__(self, self, url, 
			labelR    = labelR,
			statusbar = statusbar,
		)

		dtsWidget.StaticBoxes.__init__(self, self, 
			labelF = labelF,
			labelV = labelV,
			labelC = labelC,
		)
		#endregion --------------------------------------------> Initial Setup

		#region -----------------------------------------------------> Widgets
		self.iFile = dtsWidget.ButtonTextCtrlFF(self.sbFile,
			btnLabel  = config.label[self.name]['iFile'],
			ext       = config.extLong['Data'],
			tcHint    = config.hint[self.name]['iFile'],
			validator = dtsValidator.IsNotEmpty(
				self,
				message = config.msg['Error'][self.name]['iFile'],
			)
		)
		self.oFile = dtsWidget.ButtonTextCtrlFF(self.sbFile,
			btnLabel  = config.label[self.name]['oFile'],
			mode      = 'save',
			ext       = config.extLong['Data'],
			tcHint    = config.hint[self.name]['oFile'],
			validator = dtsValidator.IsNotEmpty(
				self,
				message = config.msg['Error'][self.name]['oFile'],
			)
		)
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
		self.sizersbFileWid.AddGrowableCol(1,1)
		self.sizersbFileWid.AddGrowableRow(0,1)

		self.Sizer = wx.BoxSizer(wx.VERTICAL)

		self.Sizer.Add(self.sizersbFile, 0, wx.EXPAND|wx.ALL, 5)
		self.Sizer.Add(self.sizersbValue, 0, wx.EXPAND|wx.ALL, 5)
		self.Sizer.Add(self.sizersbColumn, 0, wx.EXPAND|wx.ALL, 5)
		self.Sizer.Add(self.btnSizer, 0, wx.ALIGN_CENTER|wx.ALL, 5)
		#endregion ---------------------------------------------------> Sizers

		#region --------------------------------------------------------> Bind
		
		#endregion -----------------------------------------------------> Bind
	#---
	#endregion -----------------------------------------------> Instance setup

	#region ---------------------------------------------------> Class methods
	#endregion ------------------------------------------------> Class methods
#---

class CorrAConf(BaseConfPane):
	"""Creates the configuration pane for Correlation Analysis
	
		Parameters
		----------
		parent : wx Widget
			Parent of the widgets
		url : str
			URL for the Help button
		statusbar : wx.StatusBar
			Statusbar of the application to display messages

		Attributes
		----------

	"""
	#region --------------------------------------------------> Instance setup
	def __init__(self, parent, url, statusbar):
		""""""
		#region -----------------------------------------------> Initial setup
		self.parent = parent
		self.name = 'CorrAConf'

		super().__init__(parent, url, self.name)
		#endregion --------------------------------------------> Initial setup
		
		#region -----------------------------------------------------> Widgets
		#--> Values
		self.normMethod = dtsWidget.StaticTextComboBox(self.sbValue, 
			label     = config.label[self.name]['NormMethod'],
			choices   = config.choice[self.name]['NormMethod'],
			validator = dtsValidator.IsNotEmpty(
				self,
				message = config.msg['Error'][self.name]['NormMethod'],
			),
		)
		self.corrMethod = dtsWidget.StaticTextComboBox(self.sbValue, 
			label     = config.label[self.name]['CorrMethod'],
			choices   = config.choice[self.name]['CorrMethod'],
			validator = dtsValidator.IsNotEmpty(
				self,
				message = config.msg['Error'][self.name]['CorrMethod'],
			),
		)
		#--> Columns
		self.btnAdd = wx.Button(
			self.sbColumn, 
			label = config.label[self.name]['Add'],
		)
		self.stListI = wx.StaticText(
			self.sbColumn, 
			label = config.label[self.name]['iList'],
		)
		self.stListO = wx.StaticText(
			self.sbColumn, 
			label = config.label[self.name]['oList'],
		)
		self.lbI = dtsWidget.ListZebra(self.sbColumn, 
			colLabel = config.label[self.name]['ListColumn'],
			colSize  = config.size[self.name]['List'],
		)
		self.lbO = dtsWidget.ListZebra(self.sbColumn, 
			colLabel = config.label[self.name]['ListColumn'],
			colSize  = config.size[self.name]['List'],
		)

		self.iFile.listCtrl = self.lbI
		#endregion --------------------------------------------------> Widgets

		#region ------------------------------------------------------> Sizers
		#--> Expand Column section
		item = self.Sizer.GetItem(self.sizersbColumn)
		item.Proportion = 1
		item = self.sizersbColumn.GetItem(self.sizersbColumnWid)
		item.Proportion = 1
		#--> Values
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
		
		#--> Columns
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
			border = 5
		)
		self.sizersbColumnWid.Add(
			self.btnAdd,
			pos    = (1,1),
			flag   = wx.ALIGN_CENTRE_VERTICAL|wx.ALL,
			border = 5
		)
		self.sizersbColumnWid.Add(
			self.lbO,
			pos    = (1,2),
			flag   = wx.EXPAND|wx.ALL,
			border = 5
		)
		self.sizersbColumnWid.AddGrowableCol(0, 1)
		self.sizersbColumnWid.AddGrowableCol(2, 1)
		self.sizersbColumnWid.AddGrowableRow(1, 1)

		#--> Main Sizer
		self.SetSizer(self.Sizer)
		self.Sizer.Fit(self)
		#endregion ---------------------------------------------------> Sizers

		#region --------------------------------------------------------> Bind
		
		#endregion -----------------------------------------------------> Bind
	#endregion -----------------------------------------------> Instance setup
#endregion ----------------------------------------------------------> Classes
