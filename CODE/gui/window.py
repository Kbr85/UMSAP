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
import json
from pathlib import Path

import requests
import wx
import wx.adv as adv
import wx.lib.agw.aui as aui

import dat4s_core.data.file as dtsFF
import dat4s_core.data.method as dtsMethod
import dat4s_core.gui.wx.menu as dtsMenu
import dat4s_core.gui.wx.window as dtsWindow
import dat4s_core.gui.wx.widget as dtsWidget

import config.config as config
import data.file as file
import gui.menu as menu
import gui.tab as tab
import gui.dtscore as dtscore
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
		wx.CallAfter(
			dtscore.Notification, 
			'errorU',
			msg        = config.msg['ErrorU']['UpdateCheck']['Failed'],
			tException = e,
		)
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
		wx.CallAfter(
			dtscore.Notification, 
			'errorU', 
			msg = config.msg['ErrorU']['UpdateCheck']['Failed'],
		)
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
#------------------------------> Base classes
class BaseWindow(wx.Frame):
	"""Base window for UMSAP

		Parameters
		----------
		name : str
			Unique name of the window
		parent : wx Widget or None
			Parent of the window

		Attributes
		----------
		name : str
			Unique name of the window
		parent : wx Widget or None
			Parent of the window
		statusbar : wx.StatusBar
			Windows statusbar
	"""
	#region -----------------------------------------------------> Class setup
	#endregion --------------------------------------------------> Class setup

	#region --------------------------------------------------> Instance setup
	def __init__(self, name, parent=None, title=None):
		""" """
		#region -------------------------------------------------> Check Input
		#endregion ----------------------------------------------> Check Input

		#region -----------------------------------------------> Initial Setup
		self.name   = name
		self.parent = parent

		super().__init__(
			parent = parent,
			size   = config.size[self.name]['Window'],
			title  = config.title[self.name] if title is None else title,
			name   = self.name
		)
		#endregion --------------------------------------------> Initial Setup
		
		#region -----------------------------------------------------> Widgets
		self.statusbar = self.CreateStatusBar()
		#endregion --------------------------------------------------> Widgets

		#region --------------------------------------------------------> Menu
		self.menubar = menu.ToolMenuBar(self.name)
		self.SetMenuBar(self.menubar)		
		#endregion -----------------------------------------------------> Menu
		
		#region ------------------------------------------------------> Sizers
		self.Sizer = wx.BoxSizer(wx.VERTICAL)
		#endregion ---------------------------------------------------> Sizers

		#region --------------------------------------------------------> Bind
		#endregion -----------------------------------------------------> Bind
	#---
	#endregion -----------------------------------------------> Instance setup

	#region ---------------------------------------------------> Class methods
	#endregion ------------------------------------------------> Class methods
#---

#------------------------------> wx.Frame
class CorrAPlot(BaseWindow):
	"""Creates the window showing the results of a correlation analysis

		Parameters
		----------
		fileP : Path
			Path to the UMSAP file with results from a correlation analysis
		name : str
			Unique name of the window
		parent : wx Widget or None
			Parent of the window

		Attributes
		----------
		fileP : Path
			Path to the UMSAP file with results from a correlation analysis
		name : str
			Unique name of the window
		parent : wx Widget or None
			Parent of the window
		plot : dtsWidget.MatPlotPanel
			Main plot of the window
	"""
	#region -----------------------------------------------------> Class setup
	#endregion --------------------------------------------------> Class setup

	#region --------------------------------------------------> Instance setup
	def __init__(self, fileP, name='CorrAPlot', parent=None):
		""" """
		#region -------------------------------------------------> Check Input
		#------------------------------> No window with false file
		try:
			self.fileObj = file.CorrAFile(fileP)
		except Exception as e:
			raise e
		#endregion ----------------------------------------------> Check Input

		#region -----------------------------------------------> Initial Setup
		self.fileP = fileP

		super().__init__(
			name, 
			parent = parent,
			title  = config.title[name] + fileP.name
		)		
		#endregion --------------------------------------------> Initial Setup

		#region -----------------------------------------------------> Widgets
		self.plot = dtsWidget.MatPlotPanel(self, statusbar=self.statusbar)
		#endregion --------------------------------------------------> Widgets

		#region ------------------------------------------------------> Sizers
		self.Sizer.Add(self.plot, 1, wx.EXPAND|wx.ALL, 5)
		#endregion ---------------------------------------------------> Sizers

		#region --------------------------------------------------------> Bind
		
		#endregion -----------------------------------------------------> Bind

		self.Show()
	#---
	#endregion -----------------------------------------------> Instance setup

	#region ---------------------------------------------------> Class methods
	
	#endregion ------------------------------------------------> Class methods
#---


class MainWindow(BaseWindow):
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
	tabMethods = { # Keys are the unique names of the tabs
		'Start'  : tab.Start,
		'CorrA'  : tab.CorrA,
	}

	resultWindow = { # Keys are the file extensions e.g. '.corr'
		'.corr' : CorrAPlot,
	}
	#endregion --------------------------------------------------> Class Setup
	
	#region --------------------------------------------------> Instance setup
	def __init__(self, name='MainW', parent=None):
		""""""
		#region -----------------------------------------------> Initial setup
		super().__init__(name, parent=parent)
		#endregion --------------------------------------------> Initial setup

		#region -----------------------------------------------------> Widgets
		self.notebook = aui.auibook.AuiNotebook(
			self,
			agwStyle=aui.AUI_NB_TOP|aui.AUI_NB_CLOSE_ON_ALL_TABS|aui.AUI_NB_TAB_MOVE,
		)
		#endregion --------------------------------------------------> Widgets

		#region ------------------------------------------------------> Sizers
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
		#------------------------------> Close Tab
		event.Skip()
		#------------------------------> Number of tabs
		pageC = self.notebook.GetPageCount() - 1
		#------------------------------> Update tabs & close buttons
		if pageC == 1:
			#------------------------------> Remove close button from Start tab
			if (win := self.FindWindowByName('Start')) is not None:
				self.notebook.SetCloseButton(
					self.notebook.GetPageIndex(win), 
					False,
				)
			else:
				pass
		elif pageC == 0:
			#------------------------------> Show Start Tab with close button
			self.CreateTab('Start')
			self.notebook.SetCloseButton(
				self.notebook.GetPageIndex(self.FindWindowByName('Start')), 
				False,
			)
		else:
			pass
	#---

	def CreateTab(self, name):
		"""Create a tab
		
			Parameters
			----------
			name : str
				One of the values in config.name for tabs
		"""
		#region -----------------------------------------------------> Get tab
		win = self.FindWindowByName(name)
		#endregion --------------------------------------------------> Get tab
		
		#region ------------------------------------------> Find/Create & Show
		if win is None:
			#------------------------------> Create tab
			self.notebook.AddPage(
				self.tabMethods[name](
					self.notebook,
					self.statusbar,
				),
				config.title[name],
				select = True,
			)
		else:
			#------------------------------> Focus
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

	def ReadUMSAPOutFile(self, fileP):
		"""Read and display the information in an UMSAP output file.
	
			Parameters
			----------
			fileP : Path
				Path to the UMSAP output file

		"""
		#region ---------------------------------------------------> Read file
		try:
			self.resultWindow[fileP.suffix](fileP)
		except Exception as e:
			raise e
		#endregion ------------------------------------------------> Read file
			
		return True		
	#---
	#endregion -------------------------------------------------> Menu methods
#---
#------------------------------> wx.Dialog
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
		#------------------------------> Msg
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
		#------------------------------> Link	
		if checkRes is not None:
			self.stLink = adv.HyperlinkCtrl(
				self,
				label = 'Read the Release Notes.',
				url   = config.url['Update'],
			)
		else:
			pass
		#------------------------------> Img
		self.img = wx.StaticBitmap(
			self,
			bitmap = wx.Bitmap(str(config.img['Icon']), wx.BITMAP_TYPE_PNG),
		)
		#endregion --------------------------------------------------> Widgets

		#region ------------------------------------------------------> Sizers
		#------------------------------> Button Sizers
		self.btnSizer = self.CreateStdDialogButtonSizer(wx.OK)
		#------------------------------> TextSizer
		self.tSizer = wx.BoxSizer(wx.VERTICAL)
		
		self.tSizer.Add(self.stMsg, 0, wx.ALIGN_LEFT|wx.ALL, 10)
		if checkRes is not None:
			self.tSizer.Add(self.stLink, 0, wx.ALIGN_CENTER|wx.ALL, 10)
		else:
			pass
		#------------------------------> Image Sizer
		self.imgSizer = wx.BoxSizer(wx.HORIZONTAL)
		
		self.imgSizer.Add(self.img, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
		self.imgSizer.Add(self.tSizer, 0, wx.ALIGN_LEFT|wx.LEFT|wx.TOP|wx.BOTTOM, 5)
		#------------------------------> Main Sizer
		self.Sizer = wx.BoxSizer(wx.VERTICAL)
		
		self.Sizer.Add(self.imgSizer, 0, wx.ALIGN_CENTER|wx.TOP|wx.LEFT|wx.RIGHT, 25)
		self.Sizer.Add(self.btnSizer, 0, wx.ALIGN_RIGHT|wx.RIGHT|wx.BOTTOM, 10)
		
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