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

import dat4s_core.gui.wx.menu as dtsMenu

import config.config as config
import gui.dtscore as dtscore
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
		config.mainW.CreateTab(self.name[event.GetId()])
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
		self.confOpt = getattr(config, 'ModuleMenu')
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
		self.confOpt = getattr(config, self.name)
		self.confMsg = getattr(config, self.name+'Msg')
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
			fileP = dtsMenu.GetFilePath('openM', config.extLong['UMSAP'])
		except Exception as e:
			dtscore.Notification(
				'errorF', 
				msg        = self.confMsg['Selector'],
				tException = e,
				parent     = self.GetWindow(),
			)
			return False
		#endregion ------------------------------------------------> Get files
		
		#region --------------------------------------------------> Open files
		if fileP is not None:
			#-->
			for f in fileP:
				try:
					config.mainW.ReadUMSAPOutFile(Path(f))
				except Exception as e:
					dtscore.Notification(
						'errorF', 
						msg        = str(e),
						tException = e,
						parent     = self.GetWindow(),
					)
			#-->
			return True
		else:
			return False
		#endregion -----------------------------------------------> Open files
	#---
	#endregion ------------------------------------------------> Class Methods
#---

class CorrAPlotToolMenu(wx.Menu, MenuMethods):
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
		self.saveI = self.Append(-1, 'Save Image\tCtrl+S')
		self.AppendSeparator()
		self.zoomR = self.Append(-1, 'Reset Zoom\tCtrl+Z')
		#endregion -----------------------------------------------> Menu Items

		#region --------------------------------------------------------> Bind
		self.Bind(wx.EVT_MENU, self.OnZoomReset, source=self.zoomR)
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