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

import wx

import dat4s_core.gui.wx.window as dtsWindow
import dat4s_core.gui.wx.menu as dtsMenu

import config.config as config
#endregion ----------------------------------------------------------> Imports


#region --------------------------------------------------------> Base Classes
class MenuMethods():
	"""Base class to hold common methods to the menus
	
		Methods
		-------
	"""

	#region ---------------------------------------------------> Class Methods
	def OnCreateTab(self, event):
		"""Creates a new tab in the main window
		
			Parameters
			----------
			event : wx.Event
				Information about the event
		"""
		config.mainW.CreateTab(self.name[event.GetId()])
		return True
	#---
	#endregion ------------------------------------------------> Class Methods
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
		super().__init__()
		#endregion --------------------------------------------> Initial Setup

		#region --------------------------------------------------> Menu items
		self.limprot  = self.Append(-1, 'Limited Proteolysis\tALT+Ctrl+L')
		self.protprof = self.Append(-1, 'Proteome Profiling\tALT+Ctrl+P')
		self.tarprot  = self.Append(-1, 'Targeted Proteolysis\tALT+Ctrl+T')
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
		super().__init__()
		#endregion --------------------------------------------> Initial Setup

		#region --------------------------------------------------> Menu items
		self.corrA   = self.Append(-1, 'Correlation Analysis')
		self.AppendSeparator()
		self.readFile = self.Append(-1, 'Read File\tCtrl+R')
		#endregion -----------------------------------------------> Menu items

		#region -------------------------------------------------------> Names
		self.name = { # Associate IDs with Tab names. Avoid manual set of IDs
			self.corrA.GetId() : 'CorrA',
		}
		#endregion ----------------------------------------------------> Names

		#region --------------------------------------------------------> Bind
		self.Bind(wx.EVT_MENU, self.OnReadFile, source=self.readFile)
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
			fileP = dtsMenu.GetFilePath('openM', config.extLong['UMSAPOut'])
		except Exception as e:
			dtsWindow.NotificationDialog(
				'errorF', 
				details = (
					f"It was not possible to show the file selector dialog."
					f"\n\nFurther details:\n{e}"
				), 
				parent=self.GetWindow(),
				img = config.img['Icon'],
			)
			return False
		#endregion ------------------------------------------------> Get files
		
		#region --------------------------------------------------> Open files
		if fileP is not None:
			#-->
			for f in fileP:
				config.mainW.ReadUMSAPOutFile(f)
			#-->
			return True
		else:
			return False
		#endregion -----------------------------------------------> Open files
	#---
	#endregion ------------------------------------------------> Class Methods
#---

class CorrAPlotToolMenu(wx.Menu):
	""" """
	#region -----------------------------------------------------> Class setup
	
	#endregion --------------------------------------------------> Class setup

	#region --------------------------------------------------> Instance setup
	def __init__(self):
		""" """
		#region -----------------------------------------------> Initial Setup
		super().__init__()
		#endregion --------------------------------------------> Initial Setup

		#region --------------------------------------------------> Menu Items
		self.saveI = self.Append(-1, 'Save Image')
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
		'CorrAPlot' : CorrAPlotToolMenu,
	}
	#endregion --------------------------------------------------> Class Setup
	
	#region --------------------------------------------------- Instance Setup
	def __init__(self, name):
		""" """
		#region -----------------------------------------------> Initial Setup
		super().__init__()
		#endregion --------------------------------------------> Initial Setup
		
		#region -----------------------------------------> Menu items & Append
		if name != 'MainW':
			self.Tool  = self.toolClass[name]()
			self.Insert(config.toolsMenuIdx, self.Tool, 'Tools')
		else:
			pass
		#endregion --------------------------------------> Menu items & Append
	#endregion ------------------------------------------------ Instance Setup
#---
#endregion ----------------------------------------------------------> Menubar