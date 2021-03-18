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


""" Menus of the application"""


#region -------------------------------------------------------------> Imports
from pathlib import Path
import _thread
import wx

import dat4s_core.gui.wx.menu as dtsMenu

import config.config as config
import gui.dtscore as dtscore
import gui.window as window
import gui.method as guiMethod
import data.file as file
#endregion ----------------------------------------------------------> Imports


#region --------------------------------------------------------> Base Classes
class MenuMethods():
	"""Base class to hold common methods to the menus """

	#region ---------------------------------------------------> Class Methods
	def OnCreateTab(self, event):
		"""Creates a new tab in the main window
		
			Parameters
			----------
			event : wx.Event
				Information about the event
		"""
		#region -------------------------------------------------> Check MainW
		if config.mainW is None:
			config.mainW = window.MainWindow()
		else:
			pass
		#endregion ----------------------------------------------> Check MainW
		
		#region --------------------------------------------------> Create Tab
		config.mainW.CreateTab(self.name[event.GetId()])		
		#endregion -----------------------------------------------> Create Tab
		
		return True
	#---

	def OnZoomReset(self, event):
		"""Reset the zoom level of a matlibplot. Assumes the plot comes from
			dtsWidget.MatPlotPanel and it is called plot in the window.
	
			Parameters
			----------
			event : wx.Event
				Information about the event
		"""
		win = self.GetWindow()
		win.plot.ZoomResetPlot()
		return True
	#---

	def AddDateItems(self, menuDate):
		"""Add and bind the date to plot
	
			Parameters
			----------
			menuDate: list
				Available dates to plot
		"""
		#region ---------------------------------------------------> Variables
		self.plotDate = {

		}
		#endregion ------------------------------------------------> Variables
		
		#region ---------------------------------------------------> Add items
		for k in menuDate:
			#------------------------------> Add item
			i = self.AppendRadioItem(-1, k)
			#------------------------------> Add to plotDate
			self.plotDate[i.GetId()] = k
			#------------------------------> Bind
			self.Bind(wx.EVT_MENU, self.OnPlotDate, source=i)
		#endregion ------------------------------------------------> Add items
		
		#region -----------------------------------------------> Add Separator
		self.AppendSeparator()
		#endregion --------------------------------------------> Add Separator
	#---

	def OnPlotDate(self, event):
		"""Plot a date of a section in an UMSAP file
	
			Parameters
			----------
			event : wx.Event
				Information about the event
		
		"""
		win = self.GetWindow()
		win.Draw(self.plotDate[event.GetId()])
		return True
	#---

	def OnExportPlotData(self, event):
		"""Export plotted data 

			Parameters
			----------
			event : wx.Event
				Information about the event
		"""
		win = self.GetWindow()
		win.OnExportPlotData()
		return True
	#---

	def OnSavePlot(self, event):
		"""Save an image of a plot
	
			Parameters
			----------
			event : wx.Event
				Information about the event
		"""
		win = self.GetWindow()
		win.OnSavePlot()
		return True
	#---
	#endregion ------------------------------------------------> Class Methods
#---


class PlotMenu(wx.Menu, MenuMethods):
	"""Menu for a window plotting results, like Correlation Analysis
	
		Parameters
		----------
		menuDate : list of str
			List of available dates for the menu
	
	"""
	#region -----------------------------------------------------> Class setup
	
	#endregion --------------------------------------------------> Class setup

	#region --------------------------------------------------> Instance setup
	def __init__(self, menuDate):
		""" """
		#region -----------------------------------------------> Initial Setup
		super().__init__()
		#endregion --------------------------------------------> Initial Setup

		#region --------------------------------------------------> Menu Items
		#------------------------------> Add Dates
		self.AddDateItems(menuDate)
		#------------------------------> Other items
		self.saveD = self.Append(-1, 'Export Data\tCtrl+E')
		self.saveI = self.Append(-1, 'Save Image\tCtrl+I')
		self.AppendSeparator()
		self.zoomR = self.Append(-1, 'Reset Zoom\tCtrl+Z')
		#endregion -----------------------------------------------> Menu Items

		#region --------------------------------------------------------> Bind
		self.Bind(wx.EVT_MENU, self.OnZoomReset,      source=self.zoomR)
		self.Bind(wx.EVT_MENU, self.OnExportPlotData, source=self.saveD)
		self.Bind(wx.EVT_MENU, self.OnSavePlot,       source=self.saveI)
		#endregion -----------------------------------------------------> Bind
	#---
	#endregion -----------------------------------------------> Instance setup

	#region ---------------------------------------------------> Class methods
	
	#endregion ------------------------------------------------> Class methods
#---	
#endregion -----------------------------------------------------> Base Classes


#region ----------------------------------------------------> Individual menus
class Module(wx.Menu, MenuMethods):
	"""Menu with module entries
	
		Attributes
		----------
		name : dict
			Keys are the menu ids and values the tupples to create the tabs
	"""
	#region --------------------------------------------------- Instance setup
	def __init__(self):
		""" """
		#region -----------------------------------------------> Initial Setup
		self.confOpt = {
			#------------------------------> Labels
			'LimProt' : config.nameModules['LimProt'],
			'TarProt' : config.nameModules['TarProt'],
			'ProtProf': config.nameModules['ProtProf'],
		}

		super().__init__()
		#endregion --------------------------------------------> Initial Setup

		#region --------------------------------------------------> Menu items
		self.limprot  = self.Append(-1, self.confOpt['LimProt']+'\tALT+Ctrl+L')
		self.protprof = self.Append(-1, self.confOpt['ProtProf']+'\tALT+Ctrl+P')
		self.tarprot  = self.Append(-1, self.confOpt['TarProt']+'\tALT+Ctrl+T')
		#endregion -----------------------------------------------> Menu items

		#region -------------------------------------------------------> Names
		self.name = { # Associate IDs with Tab names. Avoid manual set of IDs
			self.limprot.GetId() : 'LimProt',
			self.protprof.GetId(): 'ProtProf',
			self.tarprot.GetId() : 'TarProt',
		}
		#endregion ----------------------------------------------------> Names

		#region --------------------------------------------------------> Bind
		self.Bind(wx.EVT_MENU, self.OnCreateTab, source=self.limprot)
		self.Bind(wx.EVT_MENU, self.OnCreateTab, source=self.protprof)
		self.Bind(wx.EVT_MENU, self.OnCreateTab, source=self.tarprot)
		#endregion -----------------------------------------------------> Bind
	#endregion ------------------------------------------------ Instance Setup
#---


class Utility(wx.Menu, MenuMethods):
	"""Utilites menu"""
	#region --------------------------------------------------> Instance Setup
	def __init__(self):
		""""""
		#region -----------------------------------------------> Initial Setup
		self.name = 'UtilityMenu'
		
		self.confOpt = { # Utility menu, conf
			#------------------------------> Labels
			'CorrA' : config.nameUtilities['CorrA'],
			'ReadF' : config.nameUtilities['ReadF'],
		}
		
		self.confMsg = {
			'Selector': config.msg['FileSelector'],
		}
		
		super().__init__()
		#endregion --------------------------------------------> Initial Setup

		#region --------------------------------------------------> Menu items
		self.corrA   = self.Append(-1, self.confOpt['CorrA'])
		self.AppendSeparator()
		self.readFile = self.Append(-1, self.confOpt['ReadF']+'\tCtrl+R')
		#endregion -----------------------------------------------> Menu items

		#region -------------------------------------------------------> Names
		self.name = { # Associate IDs with Tab names. Avoid manual set of IDs
			self.corrA.GetId() : 'CorrATab',
		}
		#endregion ----------------------------------------------------> Names

		#region --------------------------------------------------------> Bind
		self.Bind(wx.EVT_MENU, self.OnReadFile,  source=self.readFile)
		self.Bind(wx.EVT_MENU, self.OnCreateTab, source=self.corrA)
		#endregion -----------------------------------------------------> Bind
	#endregion -----------------------------------------------> Instance Setup

	#region ---------------------------------------------------> Class Methods
	def OnReadFile(self, event):
		"""Read an UMSAP output file
	
			Parameters
			----------
			event : wx.EVENT
				Information about the event

		"""
		#region ---------------------------------------------------> Get files
		try:
			fileP = dtsMenu.GetFilePath('openO', config.extLong['UMSAP'])
		except Exception as e:
			dtscore.Notification(
				'errorF', 
				msg        = self.confMsg['Selector'],
				tException = e,
				parent     = self.GetWindow(),
			)
			return False
		#endregion ------------------------------------------------> Get files
		
		#region ----------------------------------------------------> Get Path
		if fileP is None:
			return False
		else:
			fileP = Path(fileP[0])
		#endregion -------------------------------------------------> Get Path

		#region ------------------------> Raise window if file is already open
		if config.umsapW.get(fileP, '') != '':
			config.umsapW[fileP].Raise()
			return True
		else:
			pass		
		#endregion ---------------------> Raise window if file is already open

		#region ---------------------------------------------> Progress Dialog
		dlg = dtscore.ProgressDialog(None, f"Analysing file {fileP.name}", 100)
		#endregion ------------------------------------------> Progress Dialog

		#region -----------------------------------------------> Configure obj
		#------------------------------> UMSAPFile obj is placed in config.obj
		_thread.start_new_thread(guiMethod.LoadUMSAPFile, (fileP, dlg))
		#endregion --------------------------------------------> Configure obj

		#region --------------------------------------------------> Show modal
		if dlg.ShowModal() == 1:
			config.umsapW[fileP] = window.UMSAPControl(config.obj)
		else:
			pass

		dlg.Destroy()
		#endregion -----------------------------------------------> Show modal

		return True
	#---
	#endregion ------------------------------------------------> Class Methods
#---


class FileControlToolMenu(wx.Menu):
	"""Tool menu for the UMSAP file control window """
	#region -----------------------------------------------------> Class setup
	
	#endregion --------------------------------------------------> Class setup

	#region --------------------------------------------------> Instance setup
	def __init__(self, *args, **kwargs):
		"""*args and **kwargs are needed to use this menu with ToolMenuBar
			All of them are ignored here.
		"""
		#region -----------------------------------------------> Initial Setup
		super().__init__()
		#endregion --------------------------------------------> Initial Setup

		#region --------------------------------------------------> Menu Items
		self.updateFile = self.Append(-1, 'Update File Content')
		self.AppendSeparator()
		self.exportData = self.Append(-1, 'Export Data')
		#endregion -----------------------------------------------> Menu Items

		#region --------------------------------------------------------> Bind
		
		#endregion -----------------------------------------------------> Bind
	#---
	#endregion -----------------------------------------------> Instance setup

	#region ---------------------------------------------------> Class methods
	
	#endregion ------------------------------------------------> Class methods
#---


class CorrAPlotToolMenu(PlotMenu):
	""" """
	#region -----------------------------------------------------> Class setup
	
	#endregion --------------------------------------------------> Class setup

	#region --------------------------------------------------> Instance setup
	def __init__(self, menuDate):
		""" """
		#region -----------------------------------------------> Initial Setup
		super().__init__(menuDate)
		#endregion --------------------------------------------> Initial Setup

		#region --------------------------------------------------> Menu Items

		#endregion -----------------------------------------------> Menu Items

		#region --------------------------------------------------------> Bind

		#endregion -----------------------------------------------------> Bind
	#---
	#endregion -----------------------------------------------> Instance setup

	#region ---------------------------------------------------> Class methods
	
	#endregion ------------------------------------------------> Class methods
#---
#endregion -------------------------------------------------> Individual menus


#region -----------------------------------------------------------> Mix menus

#endregion --------------------------------------------------------> Mix menus


#region -------------------------------------------------------------> Menubar
class MainMenuBar(wx.MenuBar):
	""" Creates the application menu bar"""
	
	#region --------------------------------------------------- Instance Setup
	def __init__(self):
		""" """
		#region -----------------------------------------------> Initial Setup
		super().__init__()
		#endregion --------------------------------------------> Initial Setup
		
		#region --------------------------------------------------> Menu items
		self.Module  = Module()
		self.Utility = Utility()
		#endregion -----------------------------------------------> Menu items

		#region -------------------------------------------> Append to menubar
		self.Append(self.Module, '&Modules')
		self.Append(self.Utility, '&Utilities')
		#endregion ----------------------------------------> Append to menubar
	#endregion ------------------------------------------------ Instance Setup
#---


class ToolMenuBar(MainMenuBar):
	"""Menu bar for a window showing the corresponding tool menu"""

	#region -----------------------------------------------------> Class Setup
	toolClass = { # Key are window name
		'MainW'    : None,
		'UMSAPF'   : FileControlToolMenu,
		'CorrAPlot': CorrAPlotToolMenu,
		'ProtProf' : None,
	}
	#endregion --------------------------------------------------> Class Setup
	
	#region --------------------------------------------------- Instance Setup
	def __init__(self, name, menuDate=None):
		""" """
		#region -----------------------------------------------> Initial Setup
		super().__init__()
		#endregion --------------------------------------------> Initial Setup
		
		#region -----------------------------------------> Menu items & Append
		if self.toolClass[name] is not None:
			self.Tool  = self.toolClass[name](menuDate)
			self.Insert(config.toolsMenuIdx, self.Tool, 'Tools')
		else:
			pass
		#endregion --------------------------------------> Menu items & Append
	#endregion ------------------------------------------------ Instance Setup
#---
#endregion ----------------------------------------------------------> Menubar