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


"""Main windows and dialogs of the App """


#region -------------------------------------------------------------> Imports
import _thread

import requests
import wx
import wx.adv as adv
import wx.lib.agw.aui as aui

import dat4s_core.data.method as dtsMethod
import dat4s_core.gui.wx.menu as dtsMenu
import dat4s_core.gui.wx.window as dtsWindow


import config.config as config
import gui.menu as Menu
import gui.tab as Tab
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Methods
def UpdateCheck(ori, win=None):
	""" Check for updates for UMSAP from another thread.
		
		Parameters
		----------
		ori: str
			Origin of the request, 'menu' or 'main'
		win : wx widget
			To center the result window in this widget
	"""
	#region ---------------------------------> Get web page text from Internet
	try:
		r = requests.get(config.url['Update'])
	except Exception as e:
		msg = (
			f"{config.msg['ErrorU']['UpdateCheck']['Failed']}\n\n"
			f"Error message: {e}"
		)
		wx.CallAfter(dtsWindow.MessageDialog, 'errorU', msg)
		return False
	#endregion ------------------------------> Get web page text from Internet
	
	#region --------------------------------------------> Get Internet version
	if r.status_code == requests.codes.ok:
		text = r.text.split('\n')
		for i in text:
			if '<h1>UMSAP' in i:
				versionI = i
				break
		versionI = versionI.split('UMSAP')[1].split('</h1>')[0]
	else:
		msg = f"{config.msg['ErrorU']['UpdateCheck']['Failed']}"
		wx.CallAfter(dtsWindow.MessageDialog, 'errorU', msg)
		return False
	#endregion -----------------------------------------> Get Internet version

	#region -----------------------------------------------> Compare & message
	#--> Compare
	updateAvail = dtsMethod.VersionCompare(versionI, config.version)
	#--> Message
	if updateAvail:
		wx.CallAfter(
			CheckUpdateResult, 
			parent   = win,
			checkRes = versionI,
		)
	elif not updateAvail and ori == 'menu':
		wx.CallAfter(CheckUpdateResult, 
			parent   = win,
			checkRes = None,
		)
	else:
		pass
	#endregion --------------------------------------------> Compare & message
	
	return True
 #---
#---
#endregion ----------------------------------------------------------> Methods

#region -------------------------------------------------------------> Classes
class MainWindow(wx.Frame):
	"""Creates the main window of the App 
	
		Parameters
		----------
		parent : wx widget or None
			parent of the main window
		
		Attributes
		----------
		name : str
			Name to id the window
		tabMethods: dict
			Methods to create the tabs
		menubar : wx.MenuBar
			wx.Menubar associated with the window
		statusbar : wx.StatusBar
			wx.StatusBar associated with the window
		notebook : wx.lib.agw.aui.auibook.AuiNotebook
			Notebook associated with the window
		Sizer : wx.BoxSizer
			Sizer for the window
	"""
	#region -----------------------------------------------------> Class Setup
	tabMenus = { # Keys are the unique names of the tabs
		'Start' : wx.Menu,
		'CorrA' : Menu.ToolsCorrA,
	}
	#endregion --------------------------------------------------> Class Setup
	
	#region --------------------------------------------------> Instance setup
	def __init__(self, parent=None):
		""""""
		#region -----------------------------------------------> Initial setup
		self.name = 'MainW'

		self.tabMethods = { # Keys are the unique names of the tabs
			'Start'  : Tab.Start,
			'CorrA'  : Tab.CorrA,
		}

		super().__init__(
			parent = parent,
			size   = config.size[self.name],
			title  = config.title['MainW'],
		)
		#endregion --------------------------------------------> Initial setup

		#region ---------------------------------------------> Default MenuBar
		self.menubar = Menu.MainMenuBar()
		self.SetMenuBar(self.menubar)
		self.menubar.EnableTop(config.toolsMenuIdx, False)
		#endregion ------------------------------------------> Default MenuBar

		#region -----------------------------------------------------> Widgets
		self.statusbar = self.CreateStatusBar()

		self.notebook = aui.auibook.AuiNotebook(
			self,
			agwStyle=aui.AUI_NB_TOP|aui.AUI_NB_CLOSE_ON_ALL_TABS|aui.AUI_NB_TAB_MOVE,
		)
		#endregion --------------------------------------------------> Widgets

		#region ------------------------------------------------------> Sizers
		self.Sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.Sizer.Add(self.notebook, 1, wx.EXPAND|wx.ALL, 5)
		self.SetSizer(self.Sizer)
		#endregion ---------------------------------------------------> Sizers

		#region --------------------------------------------> Create Start Tab
		self.CreateTab('Start')
		self.notebook.SetCloseButton(0, False)
		#endregion -----------------------------------------> Create Start Tab

		#region ---------------------------------------------> Position & Show
		self.Center()
		self.Show()
		#endregion ------------------------------------------> Position & Show

		#region	------------------------------------------------------> Update
		if config.general["checkUpdate"]:
			_thread.start_new_thread(UpdateCheck, ("main", self))
		else:
			pass
		#endregion	--------------------------------------------------> Update

		#region --------------------------------------------------------> Bind
		self.notebook.Bind(aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.OnTabClose)
		self.notebook.Bind(aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.OnTabChanged)
		#endregion -----------------------------------------------------> Bind
	#---
	#endregion -----------------------------------------------> Instance setup

	#region ----------------------------------------------------> Menu methods
	def OnTabClose(self, event):
		"""Make sure to show the Start Tab if no other tab exists
		
			Parameters
			----------
			event : wx.aui.Event
				Information about the event
		"""
		#--> Close Tab
		event.Skip()
		#--> Number of tabs
		pageC = self.notebook.GetPageCount() - 1
		#--> Remove close button from Start tab
		if pageC == 1:
			if (win := self.FindWindowByName('Start')) is not None:
				self.notebook.SetCloseButton(
					self.notebook.GetPageIndex(win), 
					False,
				)
			else:
				pass
		#--> Show Start Tab without close button, if there is no other tab
		elif pageC == 0:
			self.CreateTab('Start')
			self.notebook.SetCloseButton(
				self.notebook.GetPageIndex(self.FindWindowByName('Start')), 
				False,
			)
		else:
			pass
	#---

	def CreateTab(self, name, iFile=None):
		"""Create a tab
		
			Parameters
			----------
			name : str
				One of the values in config.name for tabs
			iFile : str or Path
				Location of file to open in the new tab
		"""
		#region -----------------------------------------------------> Get tab
		win = self.FindWindowByName(name)
		#endregion --------------------------------------------------> Get tab
		
		#region ------------------------------------------> Find/Create & Show
		if win is None:
		 #--> Create tab
			self.notebook.AddPage(
				self.tabMethods[name](
					self.notebook,
					name,
					self.statusbar,
					iFile,
				),
				config.title[name],
				select = True,
			)
		else:
		 #--> Focus
			self.notebook.SetSelection(self.notebook.GetPageIndex(win))
		#endregion ---------------------------------------> Find/Create & Show

		#region ---------------------------------------------------> Start Tab
		if self.notebook.GetPageCount() > 1:
			winS = self.FindWindowByName('Start')
			if winS is not None:
				self.notebook.SetCloseButton(
					self.notebook.GetPageIndex(winS), 
					True,
				)
			else:
				pass
		else:
			pass
		#endregion ------------------------------------------------> Start Tab
	#---

	def OnTabChanged(self, event):
		"""Updates Tools menu

			Parameters
			----------
			event : aui.Event
				Information about the event
		"""
		#-->
		name = self.notebook.GetPage(self.notebook.GetSelection()).name
		toolMenu = self.tabMenus[name]()
		#-->
		dtsMenu.ReplaceTopMenu(
			self.menubar, 
			config.toolsMenuIdx, 
			toolMenu,
			config.name['Tool'],
		)
		#-->
		event.Skip()
	#---
	#endregion -------------------------------------------------> Menu methods
#---

class CheckUpdateResult(wx.Dialog):
	"""Show a dialog with the result of the check for update operation.
	
		Parameters
		----------
		parent : wx widget or None
			To center the dialog in parent. Default None
		checkRes : str or None
			Internet lastest version. Default None

		Attributes:
		name : str
			Unique window id
	"""
	#region --------------------------------------------------> Instance setup
	def __init__(self, parent=None, checkRes=None):
		""""""
		#region -----------------------------------------------> Initial setup
		self.name = 'CheckUpdateRes'

		style = wx.CAPTION|wx.CLOSE_BOX
		super().__init__(parent, title =config.title[self.name], style=style)
		#endregion --------------------------------------------> Initial setup

		#region -----------------------------------------------------> Widgets
		if checkRes is None:
			msg = config.label[self.name]['Latest']
		else:
			msg = (
				f"UMSAP {checkRes} is already available.\n"
				f"You are currently using UMSAP {config.version}."
			)
		self.stMsg = wx.StaticText(
			self, 
			label = msg,
			style = wx.ALIGN_LEFT,
		)
		if checkRes is not None:
			self.stLink = adv.HyperlinkCtrl(
				self,
				label = 'Read the Release Notes.',
				url   = config.url['Update'],
			)
		else:
			pass
		#endregion --------------------------------------------------> Widgets

		#region ------------------------------------------------------> Sizers
		#--> Button Sizers
		self.btnSizer = self.CreateStdDialogButtonSizer(wx.OK)
		#--> Main Sizer
		self.Sizer = wx.BoxSizer(wx.VERTICAL)
		self.Sizer.Add(self.stMsg, 0, wx.ALIGN_LEFT|wx.ALL, 10)
		if checkRes is not None:
			self.Sizer.Add(self.stLink, 0, wx.ALIGN_RIGHT|wx.ALL, 10)
		else:
			pass
		self.Sizer.Add(self.btnSizer, 0, wx.ALIGN_RIGHT|wx.TOP, 10)
		self.SetSizer(self.Sizer)
		self.Sizer.Fit(self)
		#endregion ---------------------------------------------------> Sizers

		#region --------------------------------------------------------> Bind
		if checkRes is not None:
			self.stLink.Bind(adv.EVT_HYPERLINK, self.OnLink)
		else:
			pass
		#endregion -----------------------------------------------------> Bind

		#region ---------------------------------------------> Position & Show
		if parent is None:
			self.CenterOnScreen()
		else:
			self.CentreOnParent()
		self.ShowModal()
		self.Destroy()
		#endregion ------------------------------------------> Position & Show
	#---
	#endregion -----------------------------------------------> Instance setup
	
	#region ---------------------------------------------------> Class Methods
	def OnLink(self, event):
		"""Process the link event 
		
			Parameters
			----------
			event : wx.adv.Event
				Information about the event
		"""
		event.Skip()
		self.EndModal(1)
		self.Destroy()
	#endregion ------------------------------------------------> Class Methods
#---
#endregion ----------------------------------------------------------> Classes