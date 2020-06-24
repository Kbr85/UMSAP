# ------------------------------------------------------------------------------
#	Copyright (C) 2017 Kenny Bravo Rodriguez <www.umsap.nl>
	
#	This program is distributed for free in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
	
#	See the accompaning licence for more details.
# ------------------------------------------------------------------------------


""" Creates the window showing the preferences """


#region -------------------------------------------------------------- Imports
import wx

import config.config   as config
import gui.gui_classes as gclasses
#endregion ----------------------------------------------------------- Imports


class WinPreferences(gclasses.WinMyFrame):
	""" Creates the window showing the preferences """

	#region --------------------------------------------------- Instance Setup
	def __init__(self, parent=None):
		""" parent: parent for the widgets """
	 #--> Initial Setup
		self.name = config.name['Preference']
		super().__init__(parent=None, style=None)
	 #---
	 #--> Widgets
	  #--> Lines
		self.lineHI1 = wx.StaticLine(self.panel) 
	  #---
	  #--> Buttons
		self.buttonSave = wx.Button(
			self.panel, 
			label='Save'
			)
		self.buttonCancel = wx.Button(
			self.panel, 
			label='Cancel'
			)
		self.buttonDef = wx.Button(
			self.panel, 
			label='Load Default'
			)						
	  #---
	  #--> RadioBox
		self.updateRBox = wx.RadioBox(
	 		self.panel, 
	 		label='Check for Updates',
	 		choices=config.radiobox['CheckUpdate']
	 		)
	  #---
	 #---
	 #--> Sizers
	  #--> New Sizers
		self.sizerButton = wx.FlexGridSizer(1, 3, 1, 1)
	  #---
	  #--> Add
		self.sizerButton.Add(
			self.buttonDef,
			border=5, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL			
		)
		self.sizerButton.Add(
			self.buttonCancel,
			border=5, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL			
		)	
		self.sizerButton.Add(
			self.buttonSave,
			border=5, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL			
		)			
		self.sizerIN.Add(
			self.updateRBox,
			pos=(0, 0), 
			border=2,              
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL
		)
		self.sizerIN.Add(
			self.lineHI1,
			pos=(1, 0), 
			border=2,              
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL
		)	
		self.sizerIN.Add(
			self.sizerButton,
			pos=(2, 0), 
			border=2,              
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL
		)
	  #---				
	  #--> Fit
		self.sizer.Fit(self)
	  #---
	 #---
	 #--> Position
		self.Centre()
	 #---
	 #--> Binding
		self.buttonSave.Bind(wx.EVT_BUTTON, self.OnSave)
		self.buttonCancel.Bind(wx.EVT_BUTTON, self.OnCancel)
		self.buttonDef.Bind(wx.EVT_BUTTON, self.OnDef) 
	 #---
	 #--> Tooltips
		self.buttonSave.SetToolTip(config.tooltip[self.name]['Save'])
		self.buttonCancel.SetToolTip(config.tooltip[self.name]['Cancel'])
		self.buttonDef.SetToolTip(config.tooltip[self.name]['Load'])
	 #---
	 #--> Load modified/default values
		self.ReadConfig()
	 #---
	 #-->
		self.Show()
	 #---
	#---
	#endregion ------------------------------------------------ Instance Setup

	#region ------------------------------------------------------- My Methods
	def ReadConfig(self):
		""" Load the values already defined by the user or the defaults """
	 #--> Updates
		if config.general['checkUpdate'] == 1:
			self.updateRBox.SetSelection(0)
		else:
			self.updateRBox.SetSelection(1)
	 #---
	 #--> Return
		return True
	 #---
	#---

	def OnSave(self, event):
		""" Save the options in the Preference window to config and to the file 
		"""
	 #--> Get the user values
	  #--> Update
		check = self.updateRBox.GetSelection()
		if check == 0:
			config.general['checkUpdate'] = 1
		else:
			config.general['checkUpdate'] = 0
	  #---
	 #---
	 #--> Save & Return
		if config.ConfigSave():
			self.OnClose('event')
			return True
		else:
			msg = config.dictCheckFatalErrorMsg[self.name]['Save']
			gclasses.DlgFatalErrorMsg(msg)
			return False
	 #---
	#---

	def OnCancel(self, event):
		""" Close the window """
		self.OnClose(event)
		return True
	#---

	def OnDef(self, event):
		""" Load default values """
	 #--> Read file with default values
		if config.ConfigLoad(config.file['ConfigDef']):
			pass
		else:
			msg = config.dictCheckFatalErrorMsg[self.name]['Load']
			gclasses.DlgFatalErrorMsg(msg)
			return False	
	 #---		
	 #--> Apply default values to the widgets values
		check = config.general['checkUpdate']
		if check == 1:
			self.updateRBox.SetSelection(0)
		else:
			self.updateRBox.SetSelection(1)
	 #---
	 #--> Return
		return True
	 #---
	#---
	#endregion ---------------------------------------------------- My Methods
#---


