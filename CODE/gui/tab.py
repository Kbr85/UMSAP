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
import wx
import wx.lib.agw.aui as aui

import config.config as config
import gui.pane as pane
import gui.dtscore as dtscore
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Methods

#endregion ----------------------------------------------------------> Methods


#region -------------------------------------------------------------> Classes
#------------------------------> Base classses
class BaseConfTab(wx.Panel):
	"""Base class for a Tab containing only a configuration panel. 

		Parameters
		----------
		parent : wx.Window
			Parent of the tab 

		Attributes
		----------
		parent : wx.Window
			Parent of the tab 
		confClass : dict
			Classes to create the configuration panel. Keys are Tab names
		confOpt : dict
			Configuration options

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
		#region -----------------------------------------------> Initial Setup
		self.parent = parent
		self.confClass = {
			'CorrATab'   : pane.CorrA,
			'ProtProfTab': pane.ProtProf,
		}
		self.confOpt = {
			'TP_Conf' : config.label['TP_ConfPane'],
		}
		
		super().__init__(parent, name=self.name)
		#endregion --------------------------------------------> Initial Setup

		#region --------------------------------------------------------> Menu
		
		#endregion -----------------------------------------------------> Menu

		#region -----------------------------------------------------> Widgets
		self.conf = self.confClass[self.name](self)
		#endregion --------------------------------------------------> Widgets
		
		#region -------------------------------------------------> Aui control
		#------------------------------> AUI control
		self._mgr = aui.AuiManager()
		#------------------------------> AUI which frame to use
		self._mgr.SetManagedWindow(self)
		#------------------------------> Add Configuration panel
		self._mgr.AddPane( 
			self.conf, 
			aui.AuiPaneInfo(
				).Center(
				).Caption(
					self.confOpt['TP_Conf']
				).Floatable(
					b=False
				).CloseButton(
					visible=False
				).Movable(
					b=False
				).PaneBorder(
					visible=False,
			),
		)
		#endregion ----------------------------------------------> Aui control
	#---
	#endregion -----------------------------------------------> Instance setup

	#region ---------------------------------------------------> Class methods
	
	#endregion ------------------------------------------------> Class methods
#---


class BaseConfListTab(BaseConfTab):
	"""Base class for a Tab containing a configuration panel and a right list
		panel. 

		Parameters
		----------
		parent : wx.Window
			Parent of the tab 

		Attributes
		----------
		parent : wx.Window
			Parent of the tab 

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
		#region -----------------------------------------------> Initial Setup
		confOpt = {
			#------------------------------> Labels
			'ColLabel' : config.label['LCtrlColName_I'],
			'ColSize'  : config.size['LCtrl#Name'],
			'TP_List'  : config.label['TP_ListPane'],
		}

		super().__init__(parent)

		self.confOpt.update(confOpt)
		#endregion --------------------------------------------> Initial Setup

		#region -----------------------------------------------------> Widgets
		self.lc = dtscore.ListZebraMaxWidth(
			self, 
			colLabel=self.confOpt['ColLabel'],
			colSize=self.confOpt['ColSize'],
		)
		#----------------------------> Pointer to lc to load data file content
		self.conf.lbI = self.lc
		self.conf.lbL = [self.lc]
		#endregion --------------------------------------------------> Widgets
		
		#region -------------------------------------------------> Aui control
		self._mgr.AddPane(
			self.lc, 
			aui.AuiPaneInfo(
				).Right(
				).Caption(
					self.confOpt['TP_List']
				).Floatable(
					b=False
				).CloseButton(
					visible=False
				).Movable(
					b=False
				).PaneBorder(
					visible=False,
			),
		)
		#endregion ----------------------------------------------> Aui control
	#---
	#endregion -----------------------------------------------> Instance setup

	#region ---------------------------------------------------> Class methods
	
	#endregion ------------------------------------------------> Class methods
#---
#------------------------------> 
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
		confOpt : dict
			Dict with configuration options
		confMsg dict or None
			Messages for users
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
	def __init__(self, parent):
		""""""
		#region -----------------------------------------------> Initial setup
		self.name    = 'StartTab'
		self.parent  = parent
		
		self.confOpt = {
			#------------------------------> Labels
			'LimProtL' : config.nameModules['LimProt'],
			'TarProtL' : config.nameModules['TarProt'],
			'ProtProfL': config.nameModules['ProtProf'],
			#------------------------------> Tooltips
			'LimProtTT' : 'Start the module Limited Proteolysis',
			'TarProtTT' : 'Start the module Target Proteolysis',
			'ProtProfTT': 'Start the module Proteome Profiling',
			#------------------------------> Files
			'Img' : config.file['ImgStart'],
		}

		super().__init__(parent=parent, name=self.name)
		#endregion --------------------------------------------> Initial setup
		
		#region -----------------------------------------------------> Widgets
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
		self.btnLimProt  = wx.Button(self, label=self.confOpt['LimProtL'])
		self.btnProtProf = wx.Button(self, label=self.confOpt['ProtProfL'])
		self.btnTarProt  = wx.Button(self, label=self.confOpt['TarProtL'])
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
		self.btnProtProf.Bind(
			wx.EVT_BUTTON, 
			lambda event: config.mainW.CreateTab('ProtProfTab')
		)
		#endregion -----------------------------------------------------> Bind
	#endregion -----------------------------------------------> Instance setup
#---


class CorrA(BaseConfTab):
	"""Creates the tab for the Correlation Analysis

		Parameters
		----------
		parent : wx.Window
			Parent of the Tab

		Attributes
		----------
		name : str
			Unique window ID
	"""
	#region -----------------------------------------------------> Class setup
	name = 'CorrATab'
	#endregion --------------------------------------------------> Class setup

	#region --------------------------------------------------> Instance setup
	def __init__(self, parent):
		""" """
		#region -------------------------------------------------> Check Input
		#endregion ----------------------------------------------> Check Input

		#region -----------------------------------------------> Initial Setup
		super().__init__(parent)
		#endregion --------------------------------------------> Initial Setup

		#region -------------------------------------------------> Aui control
		self._mgr.Update()
		#endregion ----------------------------------------------> Aui control
	#---
	#endregion -----------------------------------------------> Instance setup

	#region ---------------------------------------------------> Class methods
	
	#endregion ------------------------------------------------> Class methods
#---


class ProtProf(BaseConfListTab):
	"""Tab with the configuration panels for a Proteome Profiling analysis

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
	name = 'ProtProfTab'
	#endregion --------------------------------------------------> Class setup

	#region --------------------------------------------------> Instance setup
	def __init__(self, parent):
		""" """
		#region -------------------------------------------------> Check Input
		
		#endregion ----------------------------------------------> Check Input

		#region -----------------------------------------------> Initial Setup
		super().__init__(parent)
		#endregion --------------------------------------------> Initial Setup

		#region -------------------------------------------------> Aui control
		self._mgr.Update()
		#endregion ----------------------------------------------> Aui control
	#---
	#endregion -----------------------------------------------> Instance setup

	#region ---------------------------------------------------> Class methods
	
	#endregion ------------------------------------------------> Class methods
#---

#endregion ----------------------------------------------------------> Classes
