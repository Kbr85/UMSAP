# ------------------------------------------------------------------------------
#	Copyright (C) 2017-2019 Kenny Bravo Rodriguez <www.umsap.nl>
	
#	This program is distributed for free in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
	
#	See the accompaning licence for more details.
# ------------------------------------------------------------------------------


""" This module creates the window showing the found (or not) update notice """


# ------------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Methods
# ------------------------------------------------------------------------------



#--- Imports
## Standard modules
import wx
import webbrowser
## My modules
import config.config	 as config
import gui.gui_classes   as gclasses
import data.data_methods as dmethods
#---


class WinUpdateNotice(gclasses.WinMyFrame):
	""" Show the Update check results """

	def __init__(self, parent=None, style=None):
		""" parent: parent of the widgets
			style: style of the windows
		"""
	 #--> Initial Setup
		self.name = config.name['UpdateNotice']
		super().__init__(parent=parent, style=style)		   
	 #--> Widgets
	  #--> Lines
		self.lineHI1 = wx.StaticLine(self.panel)
	  #--> Buttons
		self.buttonOk   = wx.Button(self.panel, label='Ok')
		self.buttonRead = wx.Button(self.panel, label='Release Notes')
	  #--> StaticText
		self.stMsg = wx.StaticText(
			self.panel, 
			label='',
			style=wx.ALIGN_CENTRE_HORIZONTAL
		)
	 #--> Variables, here to hide self.buttonRead if needed
		if config.updateAvail == 0:
			msg = "You are using the latest version of UMSAP.\n"
			self.buttonRead.Hide()
		elif config.updateAvail == 1:
			versionI = dmethods.VersionJoin(config.versionInternet) 
			msg =  ("UMSAP " + versionI + " is already available.\n\n")
			msg += ("You are currently using UMSAP " + config.version + ".\n") 
		self.stMsg.SetLabel(msg)
	 #--> Sizers
	  #--> New sizers
		self.sizerB = wx.BoxSizer()
	  #--> Add
		self.sizerB.Add(self.buttonRead, border=2, flag=wx.ALL)	 
		self.sizerB.Add(self.buttonOk,   border=2, flag=wx.ALL)   
		self.sizerIN.Add(
			self.stMsg,
			pos=(0,0),
			border=2,
			flag=wx.ALIGN_CENTER|wx.ALL,
		)
		self.sizerIN.Add(
			self.lineHI1,
			pos=(1,0),
			border=2,
			flag=wx.ALIGN_CENTER|wx.EXPAND|wx.ALL,
		)
		self.sizerIN.Add(
			self.sizerB,
			pos=(2,0),
			border=2,
			flag=wx.ALIGN_RIGHT|wx.ALL,
		)
		self.sizer.Fit(self)
	 #--> Tooltips
		self.buttonOk.SetToolTip(config.tooltip[self.name]['Ok'])
		self.buttonRead.SetToolTip(config.tooltip[self.name]['Read'])
	 #--> Bind
		self.buttonOk.Bind(wx.EVT_BUTTON, self.OnClose)
		self.buttonRead.Bind(wx.EVT_BUTTON, self.OnRead)
	 #--> Show
		self.Center()
		self.Show()
	#---

	def OnRead(self, event):
		""" Go to umsap.nl and close the window """
	 #--> Go to web
		webbrowser.open_new(config.url['Update'])
	 #--> Return
		return True
	#---

#---