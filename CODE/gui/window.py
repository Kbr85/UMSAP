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
from pathlib import Path

import requests
import wx
import wx.adv as adv
import wx.lib.agw.aui as aui
import wx.lib.agw.customtreectrl as wxCT

import dat4s_core.data.method as dtsMethod
import dat4s_core.gui.wx.widget as dtsWidget
import dat4s_core.gui.wx.window as dtsWindow
import dat4s_core.generator.generator as dtsGenerator

import config.config as config
import gui.menu as menu
import gui.tab as tab
import gui.dtscore as dtscore
import gui.method as method
import gui.pane as pane
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
	#region ---------------------------------------------------------> Options
	confOpt = { # UpdateCheck Method in gui.window, conf & msg
		'UpdateUrl' : config.url['Update'],
		'UpdateCheckFailed' : (
			f"Check for Updates failed. Please try again later."),
	}
	#endregion ------------------------------------------------------> Options
	
	#region ---------------------------------> Get web page text from Internet
	try:
		r = requests.get(confOpt['UpdateUrl'])
	except Exception as e:
		wx.CallAfter(
			dtscore.Notification, 
			'errorU',
			msg        = confOpt['UpdateCheckFailed'],
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
		versionI = versionI.strip()
	else:
		wx.CallAfter(
			dtscore.Notification, 
			'errorU', 
			msg = confOpt['UpdateCheckFailed'],
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
		menuDate : dict or None
			Date entries for menu of plotting windows
		confOpt : dict or None
			Extra options from child class. Default is None
		confMsg : dict or None
			Extra messages from child class. Default is None

		Attributes
		----------
		name : str
			Unique name of the window
		parent : wx Widget or None
			Parent of the window
		confOpt : dict or None
			Configuration options after updating with info from child class
		confMsg : dict or None
			Error messages after updating with info from child class
		statusbar : wx.StatusBar
			Windows statusbar
	"""
	#region -----------------------------------------------------> Class setup
	#endregion --------------------------------------------------> Class setup

	#region --------------------------------------------------> Instance setup
	def __init__(self, name, parent=None, menuDate=None, confOpt=None, 
		confMsg=None):
		""" """
		#region -------------------------------------------------> Check Input
		#endregion ----------------------------------------------> Check Input

		#region -----------------------------------------------> Initial Setup
		self.name   = name
		self.parent = parent
		#------------------------------> Configuration options
		#--------------> From self
		self.confOpt = {}
		#--------------> From child class
		if confOpt is not None:
			self.confOpt.update(confOpt)
		else:
			pass
		#------------------------------> Messages
		#--------------> From self
		self.confMsg = { }
		#--------------> From child class
		if confMsg is not None:
			self.confMsg.update(confMsg)
		else:
			pass
		#------------------------------> Parent init
		super().__init__(
			parent = parent,
			size   = self.confOpt['Size'],
			title  = self.confOpt['Title'],
			name   = self.name
		)
		#endregion --------------------------------------------> Initial Setup
		
		#region -----------------------------------------------------> Widgets
		self.statusbar = self.CreateStatusBar()
		#endregion --------------------------------------------------> Widgets

		#region --------------------------------------------------------> Menu
		self.menubar = menu.ToolMenuBar(self.name, menuDate)
		self.SetMenuBar(self.menubar)		
		#endregion -----------------------------------------------------> Menu
		
		#region ------------------------------------------------------> Sizers
		self.Sizer = wx.BoxSizer(wx.VERTICAL)
		self.SetSizer(self.Sizer)
		#endregion ---------------------------------------------------> Sizers

		#region --------------------------------------------------------> Bind
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		#endregion -----------------------------------------------------> Bind
	#---
	#endregion -----------------------------------------------> Instance setup

	#region ---------------------------------------------------> Class methods
	def OnClose(self, event):
		"""Destroy window. Override as needed
	
			Parameters
			----------
			event: wx.Event
				Information about the event
		"""
		#region -------------------------------------------> Reduce win number
		try:
			config.winNumber[self.name] -= 1
		except Exception:
			pass
		#endregion ----------------------------------------> Reduce win number
		
		#region -----------------------------------------------------> Destroy
		self.Destroy()
		#endregion --------------------------------------------------> Destroy
		
		return True
	#---
	#endregion ------------------------------------------------> Class methods
#---


class BaseWindowPlot(BaseWindow):
	"""Base class for windows showing a plot with common methods

		Parameters
		----------
		name : str
			Name of the window
		parent : wx.Window or None
			Parent of the window
		menuDate : dict or None
			Date entries for menu of plotting windows
		confOpt : dict or None
			Extra options from child class. Default is None
		confMsg : dict or None
			Extra messages from child class. Default is None
	"""
	#region -----------------------------------------------------> Class setup
	
	#endregion --------------------------------------------------> Class setup

	#region --------------------------------------------------> Instance setup
	def __init__(self, name, parent, menuDate, confOpt=None, confMsg=None):
		""" """
		#region -----------------------------------------------> Initial Setup

		super().__init__(name, parent=parent, menuDate=menuDate, 
			confOpt=confOpt, confMsg=confMsg)
		#endregion --------------------------------------------> Initial Setup

		#region -----------------------------------------------------> Widgets
		self.statusbar.SetFieldsCount(2, config.sbPlot)
		#endregion --------------------------------------------------> Widgets
		
		#region --------------------------------------------------------> Bind
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		#endregion -----------------------------------------------------> Bind
	#---
	#endregion -----------------------------------------------> Instance setup

	#region ---------------------------------------------------> Class methods
	def OnSavePlot(self):
		"""Save an image of the plot.	"""
		try:
			self.plot.SaveImage(
				ext=config.extLong['MatPlotSaveI'],
				parent=self, 
				)
		except Exception as e:
			dtscore.Notification(
				'errorF',
				msg        = str(e),
				tException = e,
				parent     = self,
			)
	#---

	def OnClose(self, event):
		"""Close window and uncheck section in UMSAPFile window
	
			Parameters
			----------
			event: wx.Event
				Information about the event
		"""
		#region -----------------------------------------------> Update parent
		self.parent.UnCheckSection(self.confOpt['Section'])		
		#endregion --------------------------------------------> Update parent
		
		#region ------------------------------------> Reduce number of windows
		config.winNumber[self.name] -= 1
		#endregion ---------------------------------> Reduce number of windows
		
		#region -----------------------------------------------------> Destroy
		self.Destroy()
		#endregion --------------------------------------------------> Destroy
		
		return True
	#---
	#endregion ------------------------------------------------> Class methods
#---


#------------------------------> wx.Frame
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
		confOpt : dict
			Dict with configuration options
		confMsg dict or None
			Messages for users
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
		'StartTab'   : tab.Start,
		'CorrATab'   : tab.CorrA,
		'ProtProfTab': tab.ProtProf,
	}
	#endregion --------------------------------------------------> Class Setup
	
	#region --------------------------------------------------> Instance setup
	def __init__(self, name='MainW', parent=None):
		""""""
		#region -----------------------------------------------> Initial setup
		confOpt = { # Main Window, conf
			#------------------------------> Titles
			'Title': "Analysis Setup",
			'TitleTab' : {
				'StartTab' : 'Start',
				'CorrATab' : config.nameUtilities['CorrA'],
				'ProtProfTab' : config.nameModules['ProtProf'],
			},
			#------------------------------> Size
			'Size' : (900, 620),
		}

		super().__init__(name, parent=parent, confOpt=confOpt)
		#endregion --------------------------------------------> Initial setup

		#region -----------------------------------------------------> Widgets
		#------------------------------> StatusBar fields
		self.statusbar.SetFieldsCount(2, config.sbConf)
		self.statusbar.SetStatusText(f"{config.softwareF} {config.version}", 1)
		#------------------------------> Notebook
		self.notebook = aui.auibook.AuiNotebook(
			self,
			agwStyle=aui.AUI_NB_TOP|aui.AUI_NB_CLOSE_ON_ALL_TABS|aui.AUI_NB_TAB_MOVE,
		)
		#endregion --------------------------------------------------> Widgets

		#region ------------------------------------------------------> Sizers
		self.Sizer.Add(self.notebook, 1, wx.EXPAND|wx.ALL, 5)
		#endregion ---------------------------------------------------> Sizers

		#region --------------------------------------------> Create Start Tab
		self.CreateTab('StartTab')
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
			if (win := self.FindWindowByName('StartTab')) is not None:
				self.notebook.SetCloseButton(
					self.notebook.GetPageIndex(win), 
					False,
				)
			else:
				pass
		elif pageC == 0:
			#------------------------------> Show Start Tab with close button
			self.CreateTab('StartTab')
			self.notebook.SetCloseButton(
				self.notebook.GetPageIndex(self.FindWindowByName('StartTab')), 
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
				),
				self.confOpt['TitleTab'][name],
				select = True,
			)
		else:
			#------------------------------> Focus
			self.notebook.SetSelection(self.notebook.GetPageIndex(win))
		#endregion ---------------------------------------> Find/Create & Show

		#region ---------------------------------------------------> Start Tab
		if self.notebook.GetPageCount() > 1:
			winS = self.FindWindowByName('StartTab')
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

	def OnClose(self, event):
		"""Destroy window and set config.MainW
	
			Parameters
			----------
			event: wx.Event
				Information about the event
		"""
		config.mainW = None
		self.Destroy()
	#---
	#endregion -------------------------------------------------> Menu methods
#---


class UMSAPControl(BaseWindow):
	"""Control for an umsap file. 

		Parameters
		----------
		obj : file.UMSAPFile
			UMSAP File obj for the window
		shownSection : list of str or None
			If called from Update File Content menu list the sections that were
			checked when starting the update
		name : str
			Unique window ID
		parent : wx.Window or None
			Parent of the window

		Attributes
		----------
		name : str
			Name of the window. Basically fileP.name
		obj : file.UMSAPFile
			Object to handle UMSAP files
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
	def __init__(self, obj, shownSection=None, name='UMSAPF', parent=None):
		""" """
		#region -------------------------------------------------> Check Input
		
		#endregion ----------------------------------------------> Check Input

		#region -----------------------------------------------> Initial Setup
		self.obj = obj

		confOpt = {
			'Title': self.obj.fileP.name,
			'Size' : (400, 700),
			'Plot' : { # Methods to create plot windows
				config.nameUtilities['CorrA'] : CorrAPlot
			},
			'FileLabelCheck' : ['Data File'],
			'Section' : { # Reference to section items in wxCT.CustomTreeCtrl
			},
			'Window' : { # Reference to plot windows
			},
		}

		self.obj = obj

		super().__init__(name, parent=parent, confOpt=confOpt)
		#endregion --------------------------------------------> Initial Setup

		#region -----------------------------------------------------> Widgets
		self.trc = wxCT.CustomTreeCtrl(self)
		self.trc.SetFont(config.font['TreeItem'])
		self.SetTree()
		#endregion --------------------------------------------------> Widgets

		#region ------------------------------------------------------> Sizers
		self.Sizer.Add(self.trc, 1, wx.EXPAND|wx.ALL, 5)
		#endregion ---------------------------------------------------> Sizers

		#region --------------------------------------------------------> Bind
		self.trc.Bind(wxCT.EVT_TREE_ITEM_CHECKING, self.OnCheckItem)
		#endregion -----------------------------------------------------> Bind

		#region ---------------------------------------------> Window position
		self.WinPos()
		self.Show()
		#endregion ------------------------------------------> Window position

		#region ----------------------------------------> Show opened Sections
		if shownSection is not None:
			for k in shownSection:
				try:
					self.trc.CheckItem(
						self.confOpt['Section'][k],
						checked=True,
					)
				except Exception:
					pass
		else:
			pass
		#endregion -------------------------------------> Show opened Sections
	#---
	#endregion -----------------------------------------------> Instance setup

	#region ---------------------------------------------------> Class methods
	def WinPos(self):
		"""Set the position on the screen and adjust the total number of
			shown windows
		"""
		#region ---------------------------------------------------> Variables
		info = method.GetDisplayInfo(self)
		#endregion ------------------------------------------------> Variables
				
		#region ------------------------------------------------> Set Position
		self.SetPosition(pt=(
			info['D']['xo'] + info['W']['N']*config.deltaWin,
			info['D']['yo'] + info['W']['N']*config.deltaWin,
		))
		#endregion ---------------------------------------------> Set Position

		#region ----------------------------------------------------> Update N
		config.winNumber[self.name] = info['W']['N'] + 1
		#endregion -------------------------------------------------> Update N

		return True
	#---

	def SetTree(self):
		"""Set the elements of the wx.TreeCtrl """
		#region ----------------------------------------------------> Add root
		root = self.trc.AddRoot(self.obj.fileP.name)
		#endregion -------------------------------------------------> Add root
		
		#region ------------------------------------------------> Add elements
		for a, b in self.obj.data.items():
			#------------------------------> Add section node
			if self.obj.confTree['Sections'][a]:
				childa = self.trc.AppendItem(root, a, ct_type=1)
			else:
				childa = self.trc.AppendItem(root, a, ct_type=0)
				self.trc.SetItemFont(childa, config.font['TreeItemFalse'])
			#------------------------------> Keep reference
			self.confOpt['Section'][a] = childa
			
			for c, d in b.items():
				#------------------------------> Add date node
				childb = self.trc.AppendItem(childa, c)
				#------------------------------> Set font
				if self.obj.confTree[a][c]:
					pass
				else:
					self.trc.SetItemFont(childb, config.font['TreeItemFalse'])

				for e, f in d['I'].items():
					#------------------------------> Add date items
					childc = self.trc.AppendItem(childb, f"{e}: {f}")
					#------------------------------> Set font
					if e.strip() in self.confOpt['FileLabelCheck']:
						if Path(f).exists():
							self.trc.SetItemFont(
							childc, 
							config.font['TreeItemDataFile']
						)
						else:
							self.trc.SetItemFont(
							childc, 
							config.font['TreeItemDataFileFalse']
						)
					else:		
						self.trc.SetItemFont(
							childc, 
							config.font['TreeItemDataFile']
						)
		#endregion ---------------------------------------------> Add elements
		
		#region -------------------------------------------------> Expand root
		self.trc.Expand(root)		
		#endregion ----------------------------------------------> Expand root
		
		return True
	#---

	def OnCheckItem(self, event):
		"""Show window when section is checked
	
			Parameters
			----------
			event : wxCT.Event
				Information about the event
		"""
		#region ------------------------------------------> Get Item & Section
		item    = event.GetItem()
		section = self.trc.GetItemText(item)
		#endregion ---------------------------------------> Get Item & Section

		#region ----------------------------------------------> Destroy window
		#------------------------------> Event trigers before checkbox changes
		if self.trc.IsItemChecked(item):
			self.confOpt['Window'][section].Destroy()
			event.Skip()
			return True
		else:
			pass
		#endregion -------------------------------------------> Destroy window
		
		#region -----------------------------------------------> Create window
		try:
			self.confOpt['Window'][section] = (
				self.confOpt['Plot'][section](self)
			)
		except Exception as e:
			dtscore.Notification('errorU', msg=str(e), tException=e)
			return False
		#endregion --------------------------------------------> Create window
		
		event.Skip()
		return True
	#---

	def UnCheckSection(self, sectionName):
		"""Method to uncheck a section when the plot window is closed by the 
			user
	
			Parameters
			----------
			sectionName : str
				Section name like in config.nameModules config.nameUtilities
		"""
		#region -----------------------------------------------------> Uncheck
		self.trc.SetItem3StateValue(
			self.confOpt['Section'][sectionName],
			wx.CHK_UNCHECKED,
		)		
		#endregion --------------------------------------------------> Uncheck
		
		#region -----------------------------------------------------> Repaint
		self.Update()
		self.Refresh()		
		#endregion --------------------------------------------------> Repaint
		
		return True
	#---

	def GetCheckedSection(self):
		"""Get a list with the name of all checked sections """
		return [k for k, v in self.confOpt['Section'].items() if v.IsChecked()]
	#---
	
	def OnClose(self, event):
		"""Destroy window and remove reference from config.umsapW
	
			Parameters
			----------
			event: wx.Event
				Information about the event
		"""
		#region -----------------------------------> Update list of open files
		del(config.umsapW[self.obj.fileP])
		#endregion --------------------------------> Update list of open files
		
		#region ------------------------------------> Reduce number of windows
		config.winNumber[self.name] -= 1
		#endregion ---------------------------------> Reduce number of windows
		
		#region -----------------------------------------------------> Destroy
		#------------------------------> Childs
		for child in dtsGenerator.FindTopLevelChildren(self):
			child.Close()
		#------------------------------> Self
		self.Destroy()
		#endregion --------------------------------------------------> Destroy
		
		return True
	#---

	def UpdateFileContent(self):
		"""Update the content of the file. """
		method.LoadUMSAPFile(
			fileP        = self.obj.fileP,
			shownSection = self.GetCheckedSection(),
		)

		return True
	#---
	#endregion ------------------------------------------------> Class methods
#---


class CorrAPlot(BaseWindowPlot):
	"""Creates the window showing the results of a correlation analysis

		Parameters
		----------
		obj : data.fileUMSAPFile
			Reference to the UMSAP file object created in UMSAPControl
		parent : wx Widget or None
			Parent of the window

		Attributes
		----------
		name : str
			Unique name of the window
		parent : wx Widget or None
			Parent of the window
		confOpt : dict
			Configuration options
		confMsg : dict
			User's messages
		obj : parent.obj
			Pointer to the UMSAPFile object in parent. Instead of modifying this
			object here, modify the configure step or add a Get method
		data : parent.obj.confData[Section]
			Data for the Correlation Analysis section
		date : parent.obj.confData[Section].keys()
			List of dates availables for plotting
		cmap : Matplotlib cmap
			CMAP to use in the plot
		plot : dtsWidget.MatPlotPanel
			Main plot of the window
	"""
	#region -----------------------------------------------------> Class setup
	name='CorrAPlot'
	#endregion --------------------------------------------------> Class setup

	#region --------------------------------------------------> Instance setup
	def __init__(self, parent):
		""" """
		#region -------------------------------------------------> Check Input
		
		#endregion ----------------------------------------------> Check Input

		#region -----------------------------------------------> Initial Setup
		confOpt = {
			'Section' : config.nameUtilities['CorrA'],
			'Title' : (
				f"{parent.confOpt['Title']} - {config.nameUtilities['CorrA']}"),
			'Size' : config.size['Plot'],
		}

		confMsg = {
			'ExportFailed' : (
				f"It was not possible to write the data to the selected file"),
		}

		self.obj     = parent.obj
		self.section = confOpt['Section']
		self.data    = self.obj.confData[self.section]
		self.date    = [x for x in self.data.keys()]
		self.cmap    = dtsMethod.MatplotLibCmap(
			N  = config.color[self.section]['CMAP']['N'],
			c1 = config.color[self.section]['CMAP']['c1'],
			c2 = config.color[self.section]['CMAP']['c2'],
			c3 = config.color[self.section]['CMAP']['c3'],
		)

		super().__init__(self.name, parent, self.date, confOpt=confOpt,
			confMsg=confMsg)
		#endregion --------------------------------------------> Initial Setup

		#region -----------------------------------------------------> Widgets
		self.plot = dtsWidget.MatPlotPanel(
			self, 
			statusbar    = self.statusbar,
			statusMethod = self.UpdateStatusBar,
			dpi          = config.general['DPI'],
		)
		#endregion --------------------------------------------------> Widgets

		#region ------------------------------------------------------> Sizers
		self.Sizer.Add(self.plot, 1, wx.EXPAND|wx.ALL, 5)

		self.SetSizer(self.Sizer)
		#endregion ---------------------------------------------------> Sizers

		#region --------------------------------------------------------> Bind
		
		#endregion -----------------------------------------------------> Bind

		#region ----------------------------------------------------> Position
		self.Draw(self.date[0])
		self.WinPos()
		self.Show()
		#endregion -------------------------------------------------> Position
	#---
	#endregion -----------------------------------------------> Instance setup

	#region ---------------------------------------------------> Class methods
	def WinPos(self):
		"""Set the position on the screen and adjust the total number of
			shown windows
		"""
		#region ---------------------------------------------------> Variables
		info = method.GetDisplayInfo(self)
		#endregion ------------------------------------------------> Variables
				
		#region ------------------------------------------------> Set Position
		self.SetPosition(pt=(
			info['D']['w'] - (info['W']['N']*config.deltaWin + info['W']['w']),
			info['D']['yo'] + info['W']['N']*config.deltaWin,
		))
		#endregion ---------------------------------------------> Set Position

		#region ----------------------------------------------------> Update N
		config.winNumber[self.name] = info['W']['N'] + 1
		#endregion -------------------------------------------------> Update N

		return True
	#---

	def Draw(self, tDate):
		""" Plot data from a given date.
		
			Paramenters
			-----------
			tDate : str
				A date-time string available in the section for plotting
		"""
		#region --------------------------------------------------------> Plot
		self.plot.axes.pcolormesh(
			self.data[tDate]['DF'], 
			cmap=self.cmap,
			vmin=-1, 
			vmax=1,
			antialiased=True,
			edgecolors='k',
			lw=0.005,
		)		
		#endregion -----------------------------------------------------> Plot
		
		#region -------------------------------------------------> Axis & Plot
		#------------------------------> Axis properties
		self.SetAxis(tDate)
		#------------------------------> Zoom Out level
		self.plot.ZoomResetSetValues()
		#------------------------------> Draw
		self.plot.canvas.draw()
		#endregion ----------------------------------------------> Axis & Plot

		#region ---------------------------------------------------> Statusbar
		self.statusbar.SetStatusText(tDate, 1)
		#endregion ------------------------------------------------> Statusbar
		
		
		return True
	#---

	def SetAxis(self, tDate):
		""" General details of the plot area 
		
			Parameters
			----------
			tDate : str
				A date-time string available in the section for plotting
		"""
		#region --------------------------------------------------------> Grid
		self.plot.axes.grid(True)		
		#endregion -----------------------------------------------------> Grid
		
		#region ---------------------------------------------------> Variables
		xlabel    = []
		xticksloc = []
		
		if (self.data[tDate]['NumCol']) <= 30:
			step = 1
		elif self.data[tDate]['NumCol'] > 30 and self.data[tDate]['NumCol'] <= 60:
			step = 2
		else:
			step = 3		
		#endregion ------------------------------------------------> Variables
		
		#region ---------------------------------------------------> Set ticks
		for i in range(0, self.data[tDate]['NumCol'], step):
			xticksloc.append(i + 0.5)		
			xlabel.append(self.data[tDate]['DF'].columns[i])

		self.plot.axes.set_xticks(xticksloc)
		self.plot.axes.set_xticklabels(xlabel, rotation=90)

		self.plot.axes.set_yticks(xticksloc)
		self.plot.axes.set_yticklabels(xlabel)
		#endregion ------------------------------------------------> Set ticks
		
		#region -----------------------------------------------> Adjust figure
		self.plot.figure.subplots_adjust(bottom=0.13)
		#endregion --------------------------------------------> Adjust figure

		return True
	#---

	def UpdateStatusBar(self, event):
		"""Update the statusbar info
	
			Parameters
			----------
			event: matplotlib event
				Information about the event
		"""
		#region ---------------------------------------------------> Variables
		tDate = self.statusbar.GetStatusText(1)
		#endregion ------------------------------------------------> Variables
		
		#region ----------------------------------------------> Statusbar Text
		if event.inaxes:
			try:
				#------------------------------> Set variables
				x, y = event.xdata, event.ydata
				xf = int(x)
				xs = self.data[tDate]['DF'].columns[xf]
				yf = int(y)
				ys = self.data[tDate]['DF'].columns[yf]
				zf = '{:.2f}'.format(self.data[tDate]['DF'].iat[yf,xf])
				#------------------------------> Print
				self.statusbar.SetStatusText(
					f"x = '{str(xs)}'   y = '{str(ys)}'   cc = {str(zf)}"
				)
			except Exception:
				self.statusbar.SetStatusText('')
		else:
			self.statusbar.SetStatusText('')
		#endregion -------------------------------------------> Statusbar Text
		
		return True
	#---

	def OnExportPlotData(self):
		""" Export data to a csv file """
		#region --------------------------------------------------> Dlg window
		dlg = dtsWindow.FileSelectDialog(
			'save',
			config.extLong['Data'],
			parent=self
		)
		#endregion -----------------------------------------------> Dlg window
		
		#region ---------------------------------------------------> Get Path
		if dlg.ShowModal() == wx.ID_OK:
			#------------------------------> Variables
			p     = Path(dlg.GetPath())
			tDate = self.statusbar.GetStatusText(1)
			#------------------------------> Export
			try:
				self.obj.ExportPlotData(self.section, tDate, p)
			except Exception as e:
				dtscore.Notification(
					'errorF',
					msg        = self.confMsg['ExportFailed'],
					tException = e,
					parent     = self,
				)
		else:
			pass
		#endregion ------------------------------------------------> Get Path
	 
		dlg.Destroy()
		return True	
	 #---
	#---	
	#endregion ------------------------------------------------> Class methods
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
		confOpt : dict
			Dict with configuration options
		name : str
			Unique window id
	"""
	#region --------------------------------------------------> Instance setup
	def __init__(self, parent=None, checkRes=None):
		""""""
		#region -----------------------------------------------> Initial setup
		self.name = 'CheckUpdateResDialog'
		
		self.confOpt = {
			#------------------------------> Title
			'Title'    : f"Check for Updates",
			#------------------------------> Label
			'LabelLatest': "You are using the latest version of UMSAP.",
			'LabelLink'  : 'Read the Release Notes.',
			#------------------------------> URL
			'UpdateUrl'  : config.url['Update'],
			#------------------------------> Files
			'Icon' : config.file['ImgIcon'],
		}

		style = wx.CAPTION|wx.CLOSE_BOX
		super().__init__(parent, title=self.confOpt['Title'], style=style)
		#endregion --------------------------------------------> Initial setup

		#region -----------------------------------------------------> Widgets
		#------------------------------> Msg
		if checkRes is None:
			msg = self.confOpt['LabelLatest']
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
				label = self.confOpt['LabelLink'],
				url   = self.confOpt['UpdateUrl'],
			)
		else:
			pass
		#------------------------------> Img
		self.img = wx.StaticBitmap(
			self,
			bitmap = wx.Bitmap(str(self.confOpt['Icon']), wx.BITMAP_TYPE_PNG),
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


class ResControlExp(wx.Dialog):
	"""

		Parameters
		----------
		parent : wx.Panel
			This is the pane calling the dialog

		Attributes
		----------
		parent : wx.Panel
			This is the pane calling the dialog
		confOpt : dict
			Configuration options

		Raises
		------
		

		Methods
		-------
		
	"""
	#region -----------------------------------------------------> Class setup
	name = 'ResControlExp'
	#endregion --------------------------------------------------> Class setup

	#region --------------------------------------------------> Instance setup
	def __init__(self, parent):
		""" """
		#region -------------------------------------------------> Check Input
		if (iFile := parent.iFile.tc.GetValue()) == '':
			dlg = dtsWindow.FileSelectDialog(
				'openO',
				config.extLong['Data'],
				parent = parent
			)
			if dlg.ShowModal() == wx.ID_OK:
				iFile = Path(dlg.GetPath()[0])
				dlg.Destroy()
			else:
				dlg.Destroy()
				raise Exception
		else:
			pass
		#endregion ----------------------------------------------> Check Input

		#region -----------------------------------------------> Initial Setup
		self.parent = parent

		self.confOpt = {
			'Title' : f"Results - Control Experiments",
			#------------------------------> Label
			'ColLabel' : config.label['LCtrlColName_I'],
			'TP_List'  : config.label['TP_ListPane'],
			'TP_Conf'  : config.label['TP_ConfPane'],
			#------------------------------> Size
			'ColSize'  : config.size['LCtrl#Name'],
		}
		
		style=wx.CAPTION|wx.CLOSE_BOX|wx.RESIZE_BORDER
		super().__init__(parent, title=self.confOpt['Title'], style=style)
		#endregion --------------------------------------------> Initial Setup

		#region --------------------------------------------------------> Menu
		
		#endregion -----------------------------------------------------> Menu

		#region -----------------------------------------------------> Widgets
		self.conf = pane.ResControlExp(self)
		#------------------------------> ListCtrl and fill it
		self.lc = dtscore.ListZebraMaxWidth(
			self, 
			colLabel        = self.confOpt['ColLabel'],
			colSize         = self.confOpt['ColSize'],
		)
		dtsMethod.LCtrlFillColNames(self.lc, iFile)
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
					visible=True,
			),
		)

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
					visible=True,
			),
		)

		self._mgr.Update()
		#endregion ----------------------------------------------> Aui control

		#region --------------------------------------------------------> Bind
		
		#endregion -----------------------------------------------------> Bind

		#region ---------------------------------------------> Window position
		self.CenterOnParent()
		#endregion ------------------------------------------> Window position
	#---
	#endregion -----------------------------------------------> Instance setup

	#region ---------------------------------------------------> Class methods
	
	#endregion ------------------------------------------------> Class methods
#---
#endregion ----------------------------------------------------------> Classes












