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


#region ----------------------------------------------------> Individual menus
class Module(wx.Menu):
	"""Menu with module entries"""
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
		self.name = { # Associate IDs with Tab names. Avoids IDs manual set
			self.limprot.GetId() : 'LimProt',
			self.protprof.GetId(): 'ProtProf',
			self.tarprot.GetId() : 'TarProt',
		}
		#endregion ----------------------------------------------------> Names

		#region --------------------------------------------------------> Bind
		self.Bind(wx.EVT_MENU, self.OnModule, source=self.limprot)
		self.Bind(wx.EVT_MENU, self.OnModule, source=self.protprof)
		self.Bind(wx.EVT_MENU, self.OnModule, source=self.tarprot)
		#endregion -----------------------------------------------------> Bind
	#endregion ------------------------------------------------ Instance Setup

	#region ---------------------------------------------------> Class Methods
	def OnModule(self, event):
		"""Creates the module configuration tab 
		
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

# class UtilGeneral(wx.Menu):
# 	""" General utilities """
# 	#region --------------------------------------------------> Instance Setup
# 	def __init__(self):
# 		""""""
# 		#region -----------------------------------------------> Initial Setup
# 		super().__init__()
# 		#endregion --------------------------------------------> Initial Setup
		
# 		#region --------------------------------------------------> Menu items
# 		self.corrA   = self.Append(-1, 'Correlation Analysis')
# 		self.inputF  = self.Append(-1, 'Create Input File')
# 		self.export  = self.Append(-1, 'Export Data')
# 		self.mergeAA = self.Append(-1, 'Merge aadist Files')
# 		self.shortDF = self.Append(-1, 'Short Data Files')
# 		#endregion -----------------------------------------------> Menu items

# 		#region --------------------------------------------------------> Bind
# 		self.Bind(wx.EVT_MENU, self.OnCorrA,   source=self.corrA)	 
# 		self.Bind(wx.EVT_MENU, self.OnInputF,  source=self.inputF)
# 		self.Bind(wx.EVT_MENU, self.OnExport,  source=self.export)
# 		self.Bind(wx.EVT_MENU, self.OnMergeAA, source=self.mergeAA)
# 		self.Bind(wx.EVT_MENU, self.OnShortDF, source=self.shortDF)
# 		#endregion -----------------------------------------------------> Bind
# 	#---
# 	#endregion -----------------------------------------------> Instance Setup

# 	#region ---------------------------------------------------> Class Methods
# 	def OnCorrA(self, event):
# 		""" Creates the correlation analysis window """
# 		gmethods.WinMUCreate(config.name['CorrA'])	
# 		return True
# 	#---

# 	def OnInputF(self, event):
# 		""" Reads a .tarprot file and creates a .uscr file """	
# 		if gmethods.MenuOnCInputFile():
# 			return True
# 		else:
# 			return False
# 	#---

# 	def OnExport(self, event):
# 		""" Export data from the json format to csv """
# 		gmethods.MenuOnExport()
# 		return True
# 	#---

# 	def OnMergeAA(self, event):
# 		""" Merge aadist files util window """
# 		gmethods.WinMUCreate(config.name['MergeAA'])
# 		return True
# 	#---

# 	def OnShortDF(self, event):
# 		""" Window to create the short data files from a module main output file
# 		"""
# 		gmethods.WinMUCreate(config.name['ShortDFile'])
# 		return True
# 	#---
# 	#endregion ----------------------------------------------------- MyMethods
# #---
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
		self.Module = Module()
		#endregion -----------------------------------------------> Menu items

		#region -------------------------------------------> Append to menubar
		self.Append(self.Module, '&Modules')
		#endregion ----------------------------------------> Append to menubar
	#endregion ------------------------------------------------ Instance Setup

#endregion ----------------------------------------------------------> Menubar