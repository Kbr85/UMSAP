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
import wx
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
		win = self.GetWindow()
		win.CreateTab(self.name[event.GetId()])
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

class UtilGeneral(wx.Menu, MenuMethods):
	""" General utilities """
	#region --------------------------------------------------> Instance Setup
	def __init__(self):
		""""""
		#region -----------------------------------------------> Initial Setup
		super().__init__()
		#endregion --------------------------------------------> Initial Setup

		#region --------------------------------------------------> Menu items
		self.corrA   = self.Append(-1, 'Correlation Analysis')
		#endregion -----------------------------------------------> Menu items

		#region -------------------------------------------------------> Names
		self.name = { # Associate IDs with Tab names. Avoid manual set of IDs
			self.corrA.GetId() : 'CorrA',
		}
		#endregion ----------------------------------------------------> Names

		#region --------------------------------------------------------> Bind
		self.Bind(wx.EVT_MENU, self.OnCreateTab, source=self.corrA)
		#endregion -----------------------------------------------------> Bind
	#---
	#endregion -----------------------------------------------> Instance Setup
#---

class ToolsCorrA(wx.Menu):
	"""Creates the tools menu for the Correlation Analysis Tab"""
	#region -----------------------------------------------------> Class setup
	#endregion --------------------------------------------------> Class setup

	#region --------------------------------------------------> Instance setup
	def __init__(self):
		""" """
		#region -----------------------------------------------> Initial Setup
		super().__init__()
		#endregion --------------------------------------------> Initial Setup

		#region --------------------------------------------------> Menu Items
		self.confPane = self.Append(-1, 'Create Configuration Panel')
		#endregion -----------------------------------------------> Menu Items

		#region --------------------------------------------------------> Bind
		self.Bind(wx.EVT_MENU, self.OnCreateCorrAConfTab, source=self.confPane)
		#endregion -----------------------------------------------------> Bind
	#---
	#endregion -----------------------------------------------> Instance setup

	#region ---------------------------------------------------> Class methods
	def OnCreateCorrAConfTab(self, event):
		"""Creates the configuration panel"""
		win = self.GetWindow()
		tab = win.FindWindowByName("CorrA")
		tab.CreateConfPane()
	#---
	#endregion ------------------------------------------------> Class methods
#---
#endregion -------------------------------------------------> Individual menus

#region -----------------------------------------------------------> Mix menus
class Utility(wx.Menu):
	"""Utilites menu"""
	#region --------------------------------------------------> Instance Setup
	def __init__(self):
		""""""
		#region -----------------------------------------------> Initial Setup
		super().__init__()
		#endregion --------------------------------------------> Initial Setup

		#region --------------------------------------------------> Menu items
		self.General = UtilGeneral()
		#---
		self.AppendSubMenu(self.General, 'General Utilities')
		self.AppendSeparator()
		self.readFile = self.Append(-1, 'Read File\tCtrl+R')
		#endregion -----------------------------------------------> Menu items

		#region --------------------------------------------------------> Bind
		self.Bind(wx.EVT_MENU, self.OnReadFile, source=self.readFile)
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
		pass
	#---
	#endregion ------------------------------------------------> Class Methods
	
#---
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
		self.Tool    = wx.Menu()
		self.Script  = wx.Menu()
		#endregion -----------------------------------------------> Menu items

		#region -------------------------------------------> Append to menubar
		self.Append(self.Module, '&Modules')
		self.Append(self.Utility, '&Utilities')
		self.Append(self.Tool, '&Tools')
		self.Append(self.Script, '&Script')
		#endregion ----------------------------------------> Append to menubar
	#endregion ------------------------------------------------ Instance Setup
#---
#endregion ----------------------------------------------------------> Menubar