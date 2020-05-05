# ------------------------------------------------------------------------------
#	Copyright (C) 2017-2019 Kenny Bravo Rodriguez <www.umsap.nl>
	
#	This program is distributed for free in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
	
#	See the accompaning licence for more details.
# ------------------------------------------------------------------------------


""" This module creates the main window of the app """


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
import gui.gui_methods as gmethods
import gui.gui_classes as gclasses 
#---



class WinMain(gclasses.WinMyFrame):
	""" Creates the main frame of the application """

	def __init__(self, parent=None, style=None):
		""" parent: parent of the widgets
			style: style of the windows
		"""
	 #--> Initial Setup
		self.name = config.name['Main']
		super().__init__(parent=parent, style=style)
	 #--> Widgets
	  #--> Lines
		self.lineHI1 = wx.StaticLine(self.panel)
		self.lineVI1 = wx.StaticLine(self.panel, style=wx.LI_VERTICAL)
	  #--> Images
		self.img = wx.StaticBitmap(
			self.panel, 
			wx.ID_ANY,
			wx.Bitmap(
				str(config.image['Main']), 
				wx.BITMAP_TYPE_ANY,
			),
		)
	  #--> Buttons
		self.buttonLimProt = wx.Button(self.panel, label='Limited Proteolysis')
		self.buttonProtProf= wx.Button(self.panel, label='Proteome Profiling')
		self.buttonTarProt = wx.Button(self.panel, label='Targeted Proteolysis')
		self.buttonUtil    = wx.Button(self.panel, label='Utilities')
	  #--> Static text
		self.text1 = wx.StaticText(
			self.panel, 
			label='Fast Post-Processing of Mass Spectrometry Data'
		)
		self.text2 = wx.StaticText(
			self.panel, 
			label='Copyright © 2017 Kenny Bravo Rodriguez'
		)
	 #--> Sizers
	  #--> New
		self.sizerButton = wx.BoxSizer(wx.VERTICAL)
	  #--> Add
		self.sizerButton.Add(
			self.buttonLimProt,  
			border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL
		)
		self.sizerButton.Add(
			self.buttonProtProf, 
			border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL
		)
		self.sizerButton.Add(
			self.buttonTarProt,  
			border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL
		)
		self.sizerButton.Add(
			self.buttonUtil,     
			border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL
		)
		self.sizerIN.Add(
			self.img,         
			pos=(0, 0), 
			border=2, 
			span=(1, 2), 
			flag=wx.ALIGN_CENTER|wx.EXPAND|wx.ALL
		)
		self.sizerIN.Add(
			self.lineVI1,     
			pos=(0, 2), 
			border=2,              
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL
		)
		self.sizerIN.Add(
			self.sizerButton, 
			pos=(0, 3), 
			border=2,              
			flag=wx.ALIGN_CENTER|wx.ALL
		)
		self.sizerIN.Add(
			self.lineHI1,     
			pos=(1, 0), 
			border=2, 
			span=(1, 4), 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL
		)
		self.sizerIN.Add(
			self.text1,       
			pos=(2, 0), 
			border=2,              
			flag=wx.EXPAND|wx.ALIGN_LEFT|wx.ALL
		)
		self.sizerIN.Add(
			self.text2,       
			pos=(2, 1),
			border=2, 
			span=(1, 3), 
			flag=wx.ALIGN_RIGHT|wx.ALL
		)
	  #--> Fit
		self.sizer.Fit(self)
	 #--> Position
		self.Centre()
	 #--> Tooltips
		self.buttonProtProf.SetToolTip(config.tooltip[self.name]['ProtProf'])
		self.buttonTarProt.SetToolTip(config.tooltip[self.name]['TarProt'])
		self.buttonLimProt.SetToolTip(config.tooltip[self.name]['LimProt'])
		self.buttonUtil.SetToolTip(config.tooltip[self.name]['Util'])
	 #--> Bind
		self.buttonUtil.Bind(wx.EVT_BUTTON, self.OnUtil)
		self.buttonTarProt.Bind(wx.EVT_BUTTON, self.menubar.OnTarProt)	
		self.buttonLimProt.Bind(wx.EVT_BUTTON, self.menubar.OnLimProt)	
		self.buttonProtProf.Bind(wx.EVT_BUTTON, self.menubar.OnProtProf)	
	 #--> Show
		self.Show()
	#---

	####---- Methods of the class
	def OnUtil(self, event):
		""" Creates the utility window """
		gmethods.WinMUCreate(config.name['Util'])
	#---
#---

