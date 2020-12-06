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

import config.config as config
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
	def __init__(self, parent, name, statusbar):
		""""""
		#region -----------------------------------------------> Initial setup
		self.name   = name
		self.parent = parent

		super().__init__(parent = parent)
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
		self.Sizer     = wx.BoxSizer(wx.VERTICAL)
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
			pos    = (0,0),
			flag   = wx.EXPAND|wx.ALL,
			border = 5,
		)
		self.SizerGrid.Add(
			self.SizerBtn, 
			pos    = (0,1),
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
#endregion ----------------------------------------------------------> Classes
