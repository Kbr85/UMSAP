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
import gui.pane as Pane
#endregion ----------------------------------------------------------> Imports

#region -------------------------------------------------------------> Methods
#endregion ----------------------------------------------------------> Methods

#region -------------------------------------------------------------> Classes
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
	def __init__(self, parent, name, statusbar, *args):
		""""""
		#region -----------------------------------------------> Initial setup
		self.name   = name
		self.parent = parent

		super().__init__(parent=parent, name=name)
		#endregion --------------------------------------------> Initial setup
		
		#region -----------------------------------------------------> Widgets
		#--> Statusbar
		self.statusbar = statusbar
		#--> Images
		self.img = wx.StaticBitmap(
			self, 
			bitmap=wx.Bitmap(
				str(config.img[self.name]), 
				wx.BITMAP_TYPE_ANY,
			),
		)
		#---
		#--> Buttons
		self.btnLimProt  = wx.Button(self, label='Limited Proteolysis')
		self.btnProtProf = wx.Button(self, label='Proteome Profiling')
		self.btnTarProt  = wx.Button(self, label='Targeted Proteolysis')
		#endregion --------------------------------------------------> Widgets

		#region ----------------------------------------------------> Tooltips
		self.btnLimProt.SetToolTip(config.tooltip[self.name]['LimProt'])
		self.btnTarProt.SetToolTip(config.tooltip[self.name]['TarProt'])
		self.btnProtProf.SetToolTip(config.tooltip[self.name]['ProtProf'])
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

class CorrA(wx.Panel):
	"""Creates the tab for the corralation analysis 
	
		Parameters
		----------
		parent : wx widget
			Parent of the tab. 
		name : str
			Name of the tab. Unique name for the application
		statusbar : wx.SatusBar
			Statusbar to display info
		corrFiles : tupple
			Location of .corr files to open in the tab
		
		Attributes
		----------
		parent : wx widget
			Parent of the tab. 
		name : str
			Name of the tab. Unique name for the application
		statusbar : wx.SatusBar
			Statusbar to display info
		corrFiles : tupple
			Location of .corr files to open in the tab
		confPane : Pane.CorrAConf or None
			Configuration panel
		_mgr : aui.AuiManager
			Pane manager
	"""
	#region --------------------------------------------------> Instance setup
	def __init__(self, parent, name, statusbar, *corrFiles):
		""""""
		#region -----------------------------------------------> Initial setup
		self.parent    = parent
		self.name      = name
		self.statusbar = statusbar
		self.corrFiles = corrFiles
		self.confPane  = None

		super().__init__(parent=parent, name=name)
		#endregion --------------------------------------------> Initial setup
		
		#region -------------------------------------------------> AUI Control
		self._mgr = aui.AuiManager()
		self._mgr.SetManagedWindow(self)
		#endregion ----------------------------------------------> AUI Control

		#region -----------------------------------------------------> Widgets
		#-->
		if corrFiles[0] is None:
			self.CreateConfPane()
		else:
			pass
		#endregion --------------------------------------------------> Widgets

		#region --------------------------------------------------------> Bind
		self.Bind(aui.EVT_AUI_PANE_CLOSE, self.OnPaneClose)
		#endregion -----------------------------------------------------> Bind
	#endregion -----------------------------------------------> Instance setup
	
	#region ---------------------------------------------------> Class Methods
	def OnPaneClose(self, event):
		"""Adjust self.confPane if the configuration pane is destroy
	
			Parameters
			----------
			event : aui.Event
				Information about the event
		"""
		#-->
		if (tPane := event.GetPane()).name == 'CorrAConf':
			self._mgr.ClosePane(tPane)
			self._mgr.DetachPane(self.confPane)
			self._mgr.Update()
			self.confPane = None
		else:
			pass
		#-->
		event.Skip()
	#---

	def CreateConfPane(self):
		"""Creates the configuration pane
		
			Improve
			-------
			- Restore leaves a non-functional ToolBar icon
		"""
		if self.confPane is None:
			#-->
			self.confPane = Pane.CorrAConf(
				self,
				config.url['CorrA'], 
				self.statusbar,
			)
			#-->
			self._mgr.AddPane(
				self.confPane,
				aui.AuiPaneInfo(
					).CenterPane(
					).Name(
						'CorrAConf'
					).Caption(
						config.title['CorrAConf']
					).CaptionVisible(
					).CloseButton(
					).MinimizeButton(
					).Floatable(
						b=False
					).MinimizeMode(
						aui.AUI_MINIMIZE_POS_TOP
				),
			)
			self._mgr.Update()
		else:
			#-->
			tPane = self._mgr.GetPaneByName('CorrAConf')
			#-->
			if tPane.IsMinimized():
				#-->
				self._mgr.RestorePane(tPane)
				#-->
				for k in self._mgr.GetAllPanes():
					if k.IsToolbar():
						pass
					else:
						pass
			else:
				pass
			#-->
			self._mgr.Update()
			self._mgr.RequestUserAttention(self.confPane)
	#---

	def LoadCorrFile(self, fileP):
		"""Load a corr file
	
			Parameters
			----------
			fileP : Path
				Path to the file
		"""
		pass
	#---
	#endregion ------------------------------------------------> Class Methods
#---
#endregion ----------------------------------------------------------> Classes
