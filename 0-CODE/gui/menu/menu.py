# ------------------------------------------------------------------------------
#	Copyright (C) 2017 Kenny Bravo Rodriguez <www.umsap.nl>
	
#	This program is distributed for free in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
	
#	See the accompaning licence for more details.
# ------------------------------------------------------------------------------


""" This module generates the menus of the app """


#region -------------------------------------------------------------- Imports
import _thread

import wx

import config.config as config
import gui.gui_methods as gmethods
#endregion ----------------------------------------------------------- Imports

#region ----------------------------------------------------------- Base menus
class ModuleUtil(wx.Menu):
	""" Module menu in the main menubar """

	#region --------------------------------------------------- Instance setup
	def __init__(self):
		""" """
		super().__init__()
	 #--> Menu items
		self.limprot  = self.Append(-1, 'Limited Proteolysis\tALT+Ctrl+L')
		self.protprof = self.Append(-1, 'Proteome Profiling\tALT+Ctrl+P')
		self.tarprot  = self.Append(-1, 'Targeted Proteolysis\tALT+Ctrl+T')
		self.AppendSeparator()
		self.util     = self.Append(-1, 'Utilities\tALT+Ctrl+U')
	 #---
	 #--> Bind
		self.Bind(wx.EVT_MENU, self.OnLimProt,  source=self.limprot)
		self.Bind(wx.EVT_MENU, self.OnProtProf, source=self.protprof)
		self.Bind(wx.EVT_MENU, self.OnTarProt,  source=self.tarprot)
		self.Bind(wx.EVT_MENU, self.OnUtil,     source=self.util)
	 #---
	#---
	#endregion ------------------------------------------------ Instance Setup

	#region ------------------------------------------------------- My Methods
	def OnLimProt(self, event):
		""" Creates the Limited Proteolysis module """
		gmethods.WinMUCreate(config.name['LimProt'])
		return True
	#---

	def OnProtProf(self, event):
		""" Creates the Proteome Profiling module """
		gmethods.WinMUCreate(config.name['ProtProf'])
		return True
	#---

	def OnTarProt(self, event):
		""" Creates the Targeted Proteolysis module """
		gmethods.WinMUCreate(config.name['TarProt'])
		return True
	#---

	def OnUtil(self, event):
		""" Creates the Utilities window """
		gmethods.WinMUCreate(config.name['Util'])
		return True
	#---
	#endregion ---------------------------------------------------- My Methods
#---

class UtilLimProt(wx.Menu):
	""" Utilities for the LimProt module """

	#region --------------------------------------------------- Instance Setup
	def __init__(self):
		""""""
		super().__init__()
	 #--> Menu items
		self.seqHigh = self.Append(-1, 'Sequence Highlight')
	 #---
	 #--> Bind
		self.Bind(wx.EVT_MENU, self.OnSeqH, source=self.seqHigh)
	 #---
	#---
	#endregion ------------------------------------------------ Instance Setup

	#region -------------------------------------------------------- MyMethods
	def OnSeqH(self, event):
		""" Sequence highlight window for LimProt """
		gmethods.WinMUCreate(config.name['SeqH'])
		return True
	#---
	#endregion ----------------------------------------------------- MyMethods
#---

class UtilTarProt(wx.Menu):
	""" Utilities for the TarProt module """

	#region --------------------------------------------------- Instance Setup
	def __init__(self):
		""""""
		super().__init__()
	 #--> Menu items
		self.aaDist  = self.Append(-1, 'AA Distribution')
		self.cutRes  = self.Append(-1, 'Cleavages per Residue')
		self.cut2Pdb = self.Append(-1, 'Cleavages to PDB Files')
		self.fpList  = self.Append(-1, 'Filtered Peptide List')
		self.histo   = self.Append(-1, 'Histograms')
		self.seqAli  = self.Append(-1, 'Sequence Alignments')
		self.AppendSeparator()
		self.updateRes    = self.Append(-1, 'Update Results')
		self.customUpdate = self.Append(-1, 'Custom Update of Results')
	 #---
	 #--> Bind
		self.Bind(wx.EVT_MENU, self.OnAAdist,       source=self.aaDist)
		self.Bind(wx.EVT_MENU, self.OnCutRes,       source=self.cutRes)
		self.Bind(wx.EVT_MENU, self.OnCut2Pdb,      source=self.cut2Pdb)	
		self.Bind(wx.EVT_MENU, self.OnFPList,       source=self.fpList)			
		self.Bind(wx.EVT_MENU, self.OnHisto,        source=self.histo)
		self.Bind(wx.EVT_MENU, self.OnSeqAli,       source=self.seqAli)
		self.Bind(wx.EVT_MENU, self.OnUpdateRes,    source=self.updateRes)
		self.Bind(wx.EVT_MENU, self.OnCustomUpdate, source=self.customUpdate)
	 #---
	#---
	#endregion ------------------------------------------------ Instance Setup

	#region -------------------------------------------------------- MyMethods
	def OnAAdist(self, event):
		""" Window to get the aa distribution files from a tarprot file """
		gmethods.WinMUCreate(config.name['AAdist'])	
		return True
	#---

	def OnCutRes(self, event):
		""" Creates the .cutprop file from a .tarprot file """
		if gmethods.MenuOnCutProp():
			return True
		else:
			return False
	#---	

	def OnCut2Pdb(self, event):
		""" Window to map the cleavage per residue to a pdb file from a tarprot 
			file 
		"""
		gmethods.WinMUCreate(config.name['Cuts2PDB'])	
		return True
	#---

	def OnFPList(self, event):
		""" Reads a .tarprot file and creates a .filtpept file """	
		if gmethods.MenuOnFPList():
			return True
		else:
			return False
	#---

	def OnHisto(self, event):
		""" Window to get the histogram files from a tarprot file """
		gmethods.WinMUCreate(config.name['Histo'])	
		return True
	#---

	def OnSeqAli(self, event):
		""" Window to get the sequence alignments files from a tarprot file """
		gmethods.WinMUCreate(config.name['SeqAlign'])	
		return True
	#---

	def OnUpdateRes(self, event):
		""" Reads a .tarprot file and creates all the associated files """
		if gmethods.MenuOnUpdateTP():
			return True
		else:
			return False
	#---

	def OnCustomUpdate(self, event):
		""" Read a tarprot file and fill the Tarprot module with the input 
			found in the file so users can make quick changes. It is intended 
			for update and change results from old .tarprot file for wich a 
			configuration file is not available.
		"""
		if gmethods.MenuOnReanalyseTP():
			return True
		else:
			return False
	#---
	#endregion ----------------------------------------------------- MyMethods
#---

class UtilGeneral(wx.Menu):
	""" General utilities """

	#region --------------------------------------------------- Instance Setup
	def __init__(self):
		""""""
		super().__init__()
	 #--> Menu items
		self.corrA   = self.Append(-1, 'Correlation Analysis')
		self.inputF  = self.Append(-1, 'Create Input File')
		self.mergeAA = self.Append(-1, 'Merge aadist Files')
		self.shortDF = self.Append(-1, 'Short Data Files')
	 #---
	 #--> Bind
		self.Bind(wx.EVT_MENU, self.OnCorrA,   source=self.corrA)	 
		self.Bind(wx.EVT_MENU, self.OnInputF,  source=self.inputF)
		self.Bind(wx.EVT_MENU, self.OnMergeAA, source=self.mergeAA)
		self.Bind(wx.EVT_MENU, self.OnShortDF, source=self.shortDF)
	 #---
	#---
	#endregion ------------------------------------------------ Instance Setup

	#region -------------------------------------------------------- MyMethods
	def OnCorrA(self, event):
		""" Creates the correlation analysis window """
		gmethods.WinMUCreate(config.name['CorrA'])	
		return True
	#---

	def OnInputF(self, event):
		""" Reads a .tarprot file and creates a .uscr file """	
		if gmethods.MenuOnCInputFile():
			return True
		else:
			return False
	#---

	def OnMergeAA(self, event):
		""" Merge aadist files util window """
		gmethods.WinMUCreate(config.name['MergeAA'])
		return True
	#---

	def OnShortDF(self, event):
		""" Window to create the short data files from a module main output file
		"""
		gmethods.WinMUCreate(config.name['ShortDFile'])
		return True
	#---
	#endregion ----------------------------------------------------- MyMethods
#---

class Help(wx.Menu):
	""" Help menu for all OS in the main menubar """
	#region --------------------------------------------------- Instance Setup
	def __init__(self):
		""""""
		super().__init__()
	 #--> Menu items
		self.about = self.Append(-1, 'About UMSAP')
		self.AppendSeparator()
		self.manual    = self.Append(-1, 'Manual')
		self.tutorials = self.Append(-1, 'Tutorials')
		self.AppendSeparator()
		self.checkUpdate = self.Append(-1, 'Check for Updates')
		self.AppendSeparator()
		self.preferences = self.Append(-1, 'Preferences')
	 #---
	 #--> Bind
		self.Bind(wx.EVT_MENU, self.OnAbout,       source=self.about)
		self.Bind(wx.EVT_MENU, self.OnManual,      source=self.manual)
		self.Bind(wx.EVT_MENU, self.OnTutorials,   source=self.tutorials)
		self.Bind(wx.EVT_MENU, self.OnCheckUpdate, source=self.checkUpdate)
		self.Bind(wx.EVT_MENU, self.OnPreferences, source=self.preferences)
	 #---
	#---
	#endregion ------------------------------------------------ Instance Setup

	#region -------------------------------------------------------- MyMethods
	def OnAbout(self, event):
		""" Show the about window """
		gmethods.WinMUCreate(config.name['About'])
		return True
	#---

	def OnManual(self, event):
		""" Shows the manual with the default pdfviewer in the system """
		if gmethods.MenuOnHelpManual():
			return True
		else:
			return False
	#---

	def OnTutorials(self, event):
		""" Shows the tutorial page at umsap.nl """
		if gmethods.MenuOnHelpTutorials():
			return True
		else:
			return False
	#---

	def OnCheckUpdate(self, event):
		""" Manually check for updates"""
		_thread.start_new_thread(gmethods.UpdateCheck, ('menu',))
		return True
	#---

	def OnPreferences(self, event):
		""" Show the window to set the preferences """
		gmethods.WinMUCreate(config.name['Preference'])
		return True
	#---
	#endregion ----------------------------------------------------- MyMethods
#---

class Script(wx.Menu):
	""" Script menu in the main menubar """
	
	#region --------------------------------------------------- Instance Setup
	def __init__(self):
		""""""
		super().__init__()
	 #--> Menu items
		self.read = self.Append(-1, 'Run Input File\tCtrl+I')
	 #---
	 #--> Bind
		self.Bind(wx.EVT_MENU, self.OnRead, source=self.read)
	 #---
	#---
	#endregion ------------------------------------------------ Instance Setup

	#region -------------------------------------------------------- MyMethods
	def OnRead(self, event):
		""" Run the script """
		if gmethods.MenuOnRInputFile():
			return True
		else:
			return False
	#---
	#endregion ----------------------------------------------------- MyMethods
#---

class UMSAPforWinLinux(wx.Menu):
	""" UMSAP menu for Windows or Linux """
	#region --------------------------------------------------- Instance Setup
	def __init__(self):
		""""""
		super().__init__()
	 #--> Menu items
		self.minAll = self.Append(-1, 'Minimize All\tCtrl+M')
		self.quit   = self.Append(-1, 'Quit UMSAP\tCtrl+Q')
	 #---
	 #--> Bind
		self.Bind(wx.EVT_MENU, self.OnMinAll, source=self.minAll)
		self.Bind(wx.EVT_MENU, self.OnQuitUMSAP, source=self.quit)
	 #---
	#---
	#endregion ------------------------------------------------ Instance Setup

	#region -------------------------------------------------------- MyMethods
	def OnMinAll(self, event):
		""" Minimize all UMSAP windows """
		if gmethods.MenuOnMinimizeAll():
			return True
		else:
			return False
	#---
	
	def OnQuitUMSAP(self, event):
		""" This function terminates the application closing all the windows """
		if gmethods.MenuOnQuitUMSAP():
			return True
		else:
			return False
	#---
	#endregion ----------------------------------------------------- MyMethods
#---

class AddSelection(wx.Menu):
	""" Add selection from Data file column names listbox to wx.TextCtrl """

	#region --------------------------------------------------- Instance Setup
	def __init__(self, name):
		""" name: name of the module so you can add the elements from
				config.addColumnsTo
		"""
		super().__init__()
	 #--> Menu items & Bind
		for k,e in enumerate(config.addColumnsTo[name], start=1):
			self.Append(k, e)
			self.Bind(wx.EVT_MENU, self.OnButton, id=k)
	 #---
	#---
	#endregion ------------------------------------------------ Instance Setup

	#region -------------------------------------------------------- MyMethods
	def OnButton(self, event):
		""" Get the id of the menu item triggering the add to event and send it
			to main method 
		"""
		win = self.GetWindow()
		MId = event.GetId()
		win.AddFromList(MId)
		return True		
	#---
	#endregion ----------------------------------------------------- MyMethods
#---
#endregion -------------------------------------------------------- Base menus

#region ---------------------------------------------------------- Mixed menus
class Utilities(wx.Menu):
	""" Utilities menu in main menubar """
	#region --------------------------------------------------- Instance Setup
	def __init__(self):
		""""""
		super().__init__()
	 #--> Menu items
		self.LimProt = UtilLimProt()
		self.TarProt = UtilTarProt()
		self.General = UtilGeneral()
		self.AppendSubMenu(self.LimProt, 'Limited Proteolysis')
		self.AppendSubMenu(self.TarProt, 'Targeted Proteolysis')
		self.AppendSubMenu(self.General, 'General Utilities')
		self.AppendSeparator()
		self.ReadOutF = self.Append(-1, 'Read Output File\tCtrl+R')	
	 #---
	 #--> Bind
		self.Bind(wx.EVT_MENU, self.OnReadOutF, source=self.ReadOutF)
	 #---
	#---
	#endregion ------------------------------------------------ Instance Setup

	#region -------------------------------------------------------- MyMethods
	def OnReadOutF(self, event):
		""" Read a file generated by UMSAP """
		if gmethods.MenuOnReadOutFile():
			return True
		else:
			return False
	#---
	#endregion ----------------------------------------------------- MyMethods
#---

class ToolsModule(wx.Menu):
	""" Tools menu for the modules """

	#region --------------------------------------------------- Instance Setup
	def __init__(self, name):
		""" name: name of the module """
		super().__init__()
	 #--> Menu items
		self.AddTo = AddSelection(name)
		self.AppendSubMenu(self.AddTo, 'Add Selection to')
		self.clear = self.Append(-1, 'Clear List')
		self.AppendSeparator()
		self.save  = self.Append(-1, 'Save uscr File')
	 #---
	 #--> Bind
		self.Bind(wx.EVT_MENU, self.OnClear,      source=self.clear)
		self.Bind(wx.EVT_MENU, self.OnSaveInputF, source=self.save)
	 #---
	#---
	#endregion ------------------------------------------------ Instance Setup

	#region -------------------------------------------------------- MyMethods
	def OnClear(self, event):
		""" Clears the list box in TarProt """
		win = self.GetWindow()
		win.ClearListCtrl()
		return True
	#---

	def OnSaveInputF(self, event):
		""" Save uscr file directly from the module window """
		win = self.GetWindow()
		if win.OnSaveInputF():
			return True
		else:
			return False
	#---
	#endregion ----------------------------------------------------- MyMethods
#---
#endregion ------------------------------------------------------- Mixed menus

#region -------------------------------------------------------------- Menubar
class MainMenuBar(wx.MenuBar):
	""" Creates the application main menu bar. ids with 500s, 700s, 800s are 
		reserved for the optional Tools entries in the derived classes. Usually
		Tools has a submenus with the 500s, 700s, 800s id associated to each
		submenu.
	"""
	
	#region --------------------------------------------------- Instance Setup
	def __init__(self):
		""" """
		super().__init__()
	 #--> Menu items
		self.ModuleUtil = ModuleUtil()
		self.Utilities  = Utilities()
		self.Help       = Help()
		self.Script     = Script()
		if config.cOS != 'Darwin':
			self.UMSAP = UMSAPforWinLinux()
		else:
			pass
	 #---
	 #--> Append to menubar
		if config.cOS != 'Darwin':
			self.Append(UMSAP, '&UMSAP')
		else:
			pass
		self.Append(self.ModuleUtil, '&Modules')
		self.Append(self.Utilities,  '&Utilites')
		self.Append(self.Help,       '&Help')
		self.Append(self.Script,     '&Script')
	 #---
	#---
	#endregion ------------------------------------------------ Instance Setup
#---

class MainMenuBarWithTools(MainMenuBar):
	""" To add a Tools menu to the menubar for specific windows """

	#region --------------------------------------------------- Instance Setup
	def __init__(self, name, *args):
		""" name: Name of the window """
		super().__init__()
	  
	 #--> Menu items
		if len(args) == 0:
			ToolsMenu = config.pointer['menu']['toolmenu'][name]()
		else:
			ToolsMenu = config.pointer['menu']['toolmenu'][name](*args)
	 #---
	 #--> Append to menu bar
		if config.cOS == 'Darwin':
			self.Insert(2, ToolsMenu, '&Tools')
		elif config.cOS == 'Windows':
			self.Insert(3, ToolsMenu, '&Tools')
		elif config.cOS == 'Linux':
			self.Insert(3, ToolsMenu, '&Tools')
		else:
			pass		
	 #---
	#---
	#endregion ------------------------------------------------ Instance Setup
#---
#endregion ----------------------------------------------------------- Menubar


























############################################ OLD

class MenuFilterMonotonicity(wx.Menu):
	""" Creates the monotonicity filter menu """

	kwargs = {
		897: { 'up'  : True, },
		898: { 'down': True, },
		899: { 'both': True, },
	}

	#region --------------------------------------------------- Instance setup
	def __init__(self):
		""" """
		super().__init__()
	 #--> Menu items
		self.Append(897, 'Increasing')
		self.Append(898, 'Decreasing')
		self.Append(899, 'Both')
	 #---
	 #--> Bind
		for k in range(897, 900):
			self.Bind(wx.EVT_MENU, self.Monotonic, id=k)
	 #---
	#---
	#endregion ------------------------------------------------ Instance setup

	#region ------------------------------------------------------- My Methods
	def Monotonic(self, event):
		""" Filter by monotonic behavior """
		eID = event.GetId()
		win = self.GetWindow()
		if win.OnFilter_Monotonic(**self.kwargs[eID]):
			return True
		else:
			return False
	#---
	#endregion ---------------------------------------------------- My Methods
#---

class MenuFilterRemoveFilters(wx.Menu):
	""" Remove filters menu """
	#region --------------------------------------------------- Instance Setup
	def __init__(self):
		""""""
		super().__init__()
	 #--> Menu items
		itemAny  = self.Append(-1, 'Any')
		itemLast = self.Append(-1, 'Last Added\tCtrl+Z')
	 #---
	 #--> Bind
		self.Bind(wx.EVT_MENU, self.OnRemove, source=itemAny)
		self.Bind(wx.EVT_MENU, self.OnRemove_Last, source=itemLast)
	 #---
	#---
	#endregion ------------------------------------------------ Instance Setup

	#region ------------------------------------------------------- My Methods
	def OnRemove(self, event):
		""" Remove selected filters """
		win = self.GetWindow()
		if win.OnFilter_Remove():
			return True
		else:
			return False
	#---

	def OnRemove_Last(self, event):
		""" Remove last added filter """
		win = self.GetWindow()
		if win.OnFilter_RemoveLast():
			return True
		else:
			return False
	#---
	#endregion ---------------------------------------------------- My Methods
#---

class MenuFilterAddFilter(wx.Menu):
	""" Menu to add filter in ProtProfR """

	filter_keys = {
		801 : 'Filter_ZScore',
		802 : 'Filter_Log2FC',
	}

	#region --------------------------------------------------- Instance Setup
	def __init__(self):
		""" """
	
		super().__init__()
	 #--> Submenus
		monotonicMenu = MenuFilterMonotonicity()
	 #--> Menu items
		self.Append(801, 'Z score')
		self.Append(802, 'Log2FC')
		itemP    = self.Append(-1, 'P value')
		itemOneP = self.Append(-1, 'One P value') 
		self.Append(-1, 'Monotonic', monotonicMenu)
		itemDiver = self.Append(-1, 'Divergent')
	 #---

	 #--> Bind
		for k in range(801, 803):
			self.Bind(wx.EVT_MENU, self.OnFilter_Run, id=k)
		self.Bind(wx.EVT_MENU, self.OnFilter_P, source=itemP)
		self.Bind(wx.EVT_MENU, self.OnFilter_Divergent, source=itemDiver)
		self.Bind(wx.EVT_MENU, self.OnFilter_OneP, source=itemOneP)
	 #---
	#---
	#endregion ------------------------------------------------ Instance Setup

	#region ------------------------------------------------------- My Methods
	def OnFilter_Run(self, event):
		""""""
		win = self.GetWindow()
		if win.OnFilter_GUI(self.filter_keys[event.GetId()]):
			return True
		else:
			return False
	#---
	
	def OnFilter_P(self, event):
		""""""
		win = self.GetWindow()
		if win.OnFilter_P_GUI():
			return True
		else:
			return False
	#---

	def OnFilter_OneP(self, event):
		""""""
		win = self.GetWindow()
		if win.OnFilter_OneP_GUI():
			return True
		else:
			return False
	#---	
	
	def OnFilter_Divergent(self, event):
		""" Get proteins with divergent behavior in at least two conditions """
		win = self.GetWindow()
		if win.OnFilter_Divergent():
			return True
		else:
			return False
	#---
	#endregion ---------------------------------------------------- My Methods
#---

class MenuFilterMainMenu(wx.Menu):
	""" Main Menu to control filters """
	#region --------------------------------------------------- Instance Setup
	def __init__(self):
		""""""
		super().__init__()
	 #--> Submenus
		AddMenu    = MenuFilterAddFilter()
		RemoveMenu = MenuFilterRemoveFilters()
	 #---
	 #--> Menu items
		self.Append(850, 'Add', AddMenu)
		self.Append(851, 'Remove', RemoveMenu)
		self.Append(852, 'Reset')
		self.AppendSeparator()
		self.iExport = self.Append(-1, 'Export Results')
	 #---
	 #--> Bind
		self.Bind(wx.EVT_MENU, self.OnReset,  id=852)
		self.Bind(wx.EVT_MENU, self.OnExport, source=self.iExport)
	 #---
	#---
	#endregion ------------------------------------------------ Instance Setup

	#region ------------------------------------------------------- My Methods
	def OnReset(self, event):
		""" Remove all Filters """
		win = self.GetWindow()
		if win.OnFilter_None():
			return True
		else:
			return False
	#---

	def OnExport(self, event):
		""""""
		win = self.GetWindow()
		if win.OnExport():
			return True
		else:
			return False
	#---	
	#endregion ---------------------------------------------------- My Methods
#---


#region ------------------------------------------------ Individual Tool menus
#---# Improve You can create a base class for the menu containing several
#---# methods that appears almost everywhere.
#---# Improve

class ToolMenuTypeResults(wx.Menu):
	""" Tool menu for the Type Results window """

	#region --------------------------------------------------- Instance Setup
	def __init__(self):
		""" """
		super().__init__()
	 #--> Menu items
		self.Append(501, 'Copy\tCtrl+C')
	 #---
	 #--> Bind
		self.Bind(wx.EVT_MENU, self.OnLBoxCopy, id=501)
	 #---
	#---
	#endregion ------------------------------------------------ Instance Setup

	#region ------------------------------------------------------- My Methods
	def OnLBoxCopy(self, event):
		""" Copy the colum numbers of selected rows to the clipboard """
		win = self.GetWindow()
		win.OnLBoxCopy()
		return True
	#---
	#endregion ---------------------------------------------------- My Methods
#---

class ToolMenuCorrAMod(wx.Menu):
	""" Creates the tools menu for the correlation analysis window """
	
	#region --------------------------------------------------- Instance Setup
	def __init__(self):
		""" """
		super().__init__()
	 #--> Menu items
		self.Append(502, 'Delete Selected')
		self.Append(501, 'Clear List')
	 #---
	 #--> Bind
		self.Bind(wx.EVT_MENU, self.OnClearL,      id=501)
		self.Bind(wx.EVT_MENU, self.OnDelSel,      id=502)
	 #---
	#---
	#endregion ------------------------------------------------ Instance Setup

	#region ------------------------------------------------------- My Methods
	def OnClearL(self, event):
		""" Clear all """
		win = self.GetWindow()
		win.OnClearL()
		return True
	#---

	def OnDelSel(self, event):
		""" Delete selected """
		win = self.GetWindow()
		win.OnDelSel()
		return True
	#---
	#endregion ---------------------------------------------------- My Methods
#---

class ToolMenuCorrARes(wx.Menu):
	""" Creates the pop up menu in the correlation results window """
	
	#region --------------------------------------------------- Instance Setup
	def __init__(self):
		""" """
	 #--> Init
		super().__init__()
	 #---
	 #--> Menu items
		self.Append(502, 'Export Data to:')
		for i in config.corr['MenuID'].keys():
			self.Append(int(i), config.corr['MenuID'][i])		
		self.AppendSeparator()
		self.Append(501, 'Save Plot Image')
	 #---
	 #--> Bind
		self.Bind(wx.EVT_MENU, self.OnSavePlot, id=501)
		for i in config.corr['MenuID'].keys():
			self.Bind(wx.EVT_MENU, self.OnExport, id=int(i))
	 #---
	#---
	#endregion ------------------------------------------------ Instance Setup

	#region ------------------------------------------------------- My Methods
	def OnSavePlot(self, event):
		""" Save image of the plot """
		win = self.GetWindow()
		if win.OnSavePlotImage():
			return True
		else:
			return False
	#---

	def OnExport(self, event):
		""" Export columns in the correlation plot """	
		win = self.GetWindow()
		if win.OnExport(event.GetId()):
			return True
		else:
			return True
	#---
	#endregion ---------------------------------------------------- My Methods		
#---

class ToolMenuProtProfResT(wx.Menu):
	""" Tools menu for ProtProfResT """

	#region --------------------------------------------------- Instance Setup
	def __init__(self, allL, grayC):
		""" allL  : Draw all protein lines
			grayC : Draw lines in gray or with different colors
		"""
		super().__init__()
	 #--> Menu items
		self.Append(703, 'Show All',   kind=wx.ITEM_CHECK)
		self.AppendSeparator()
		self.Append(704, 'Same Color', kind=wx.ITEM_CHECK)
		self.AppendSeparator()
		self.Append(702, 'Save Plot Image')
		self.AppendSeparator()
		self.Append(701, 'Reset View')
	 #---
	 #--> Current
		self.CurrentState(allL, grayC)
	 #---
	 #--> Bind
		self.Bind(wx.EVT_MENU, self.OnReset,    id=701)
		self.Bind(wx.EVT_MENU, self.OnSavePlot, id=702)
		self.Bind(wx.EVT_MENU, self.OnAll,      id=703)
		self.Bind(wx.EVT_MENU, self.OnColor,    id=704)
	 #---
	#---
	#endregion ------------------------------------------------ Instance Setup
	
	#region ------------------------------------------------------- My Methods
	def CurrentState(self, allL, grayC):
		""" Check the menu items according to the current state of the window
			---
			allL  : Draw all protein lines
			grayC : Draw lines in gray or with different colors
		"""
		if allL:
			self.Check(703, True)
		else:
			self.Check(703, False)
		if grayC:
			self.Check(704, True)
		else:
			self.Check(704, False)		
		return True
	#---

	def OnAll(self, event):
		""" Show all lines """
		win = self.GetWindow()
		win.OnAll()
		return True
	#---

	def OnColor(self, event):
		""" Gray or not """
		win = self.GetWindow()
		win.OnColor()
		return True
	#---		

	def OnReset(self, event):
		""" Reset the window """
		win = self.GetWindow()
		win.OnReset()
		return True
	#---

	def OnSavePlot(self, event):
		""" Save image of the plot """
		win = self.GetWindow()
		if win.OnSavePlotImage():
			return True
		else:
			return False
	#---
	#endregion ---------------------------------------------------- My Methods
#---

class ToolMenuProtProfResFilter(MenuFilterMainMenu):
	""" Tools menu to show filtered results in protprofRes """

	#region --------------------------------------------------- Instance Setup
	def __init__(self):
		""" """
		super().__init__()
	 #--> Change menu items labels
		self.SetLabel(850, 'Add Filter')
		self.SetLabel(851, 'Remove Filter')
		self.SetLabel(852, 'Reset Filters')
	 #---
	#---
	#endregion ------------------------------------------------ Instance Setup
#---

class ToolMenuProtProfResV(wx.Menu):
	""" Tools menu for ProtProfResV """

	#region --------------------------------------------------- Instance Setup
	def __init__(self, nC, nt, lC, lt, n, tp):
		""" nC : number of conditions
			nt : number of relevant points per conditions 
			lC : conditions legends
			lt : relevant points legend
			n  : current selected condition 
			tp : current selected time point
		"""
		super().__init__()
	 #--> Menu items
	  #--> Condition menu
		self.CondMenu = wx.Menu()
		j = 505
		for i in lC:
			self.CondMenu.Append(j, str(i), kind=wx.ITEM_RADIO)
			j += 1
	  #---
	  #--> Relevant points menu
		self.TPMenu = wx.Menu()
		for i in lt:
			self.TPMenu.Append(j, str(i), kind=wx.ITEM_RADIO) 
			j += 1
	  #---
	  #--> All together
		self.AppendSubMenu(self.CondMenu, 'Conditions')
		self.AppendSubMenu(self.TPMenu, 'Relevant Points')
		self.AppendSeparator()
		self.Append(504, 'Apply Filters')
		self.AppendSeparator()
		self.Append(503, 'Z score Threshold')
		self.AppendSeparator()
		self.Append(502, 'Save Plot Image')
		self.AppendSeparator()
		self.Append(501, 'Reset View')
	  #---
	 #---
	 #--> Bind
		self.Bind(wx.EVT_MENU, self.OnReset,        id=501)
		self.Bind(wx.EVT_MENU, self.OnSavePlot,     id=502)
		self.Bind(wx.EVT_MENU, self.OnZScore,       id=503)
		self.Bind(wx.EVT_MENU, self.OnFilter_Apply, id=504)
		j = 505
		for i in range(0, nC, 1):
			self.CondMenu.Bind(wx.EVT_MENU, self.OnCond, id=j)
			j += 1
		for i in range(0, nt, 1):
			self.TPMenu.Bind(wx.EVT_MENU, self.OnTP, id=j)
			j += 1 
	 #---
	 #--> Current state
		self.CurrentState(nC, n, tp)		
	 #---
	#---
	#endregion ------------------------------------------------ Instance Setup

	#region ------------------------------------------------------- My Methods
	def OnFilter_Apply(self, event):
		""" Apply filter to this condition - time point """
		win = self.GetWindow()
		win.OnFilter_Apply()
		return True
	#---

	def OnZScore(self, event):
		""" Set new Z score threshold in % """
		win = self.GetWindow()
		win.OnZScore()
		return True
	#---

	def OnCond(self, event):
		""" Select condition """ 
		win = self.GetWindow()
		win.OnCond(event.GetId())		
		return True
	#---

	def OnTP(self, event):
		""" Select time point """ 
		win = self.GetWindow()
		win.OnTP(event.GetId())		
		return True
	#---

	def OnReset(self, event):
		""" Reset the window """
		win = self.GetWindow()
		win.OnReset()
		return True
	#---

	def OnSavePlot(self, event):
		""" Save image of the plot """
		win = self.GetWindow()
		if win.OnSavePlotImage():
			return True
		else:
			return False
	#---

	def CurrentState(self, nC, n, tp):
		""" Check the menu items based on the current state of the window
			---
			nC : number of conditions
			n  : current number of condition
			tp : current time point
		"""
		self.CondMenu.Check(505+n, True)
		self.TPMenu.Check(505+nC+tp, True)
		return True
	#---
	#endregion ---------------------------------------------------- My Methods
#---

class ToolMenuCutPropRes(wx.Menu):
	""" To show the pop up menu in CutPropRes """

	#region --------------------------------------------------- Instance Setup
	def __init__(self, nExp, seq, norm, exp, comp):
		""" nExp: Total number of experiments
			seq : 0 Rec Seq, 1 Nat Seq
			norm: 0 Reg Values, 1 Normalized Values
			exp : current experiment
			comp: experiment to compare to
		"""
		super().__init__()	
	 #--> Menu items
	  #--> Experiment menu
		self.ExpMenu = wx.Menu()
		self.ExpMenu.Append(507, 'FP List', kind=wx.ITEM_RADIO)
		for i in range(1, nExp + 1, 1):
			self.Mid = 507 + i
			name = 'Experiment ' + str(i)
			self.ExpMenu.Append(self.Mid, name, kind=wx.ITEM_RADIO)
	  #---
	  #--> Comparison menu
		self.CompMenu = wx.Menu()
		tempID = self.Mid + 1
		self.CompMenu.Append(tempID, 'None', kind=wx.ITEM_RADIO)
		tempID = tempID + 1
		self.CompMenu.Append(tempID, 'FP List', kind=wx.ITEM_RADIO)
		for i in range(1, nExp + 1, 1):
			tempID = tempID + 1 
			name = 'Experiment ' + str(i)
			self.CompMenu.Append(tempID, name, kind=wx.ITEM_RADIO)
	  #---
	  #--> All together
		self.AppendSubMenu(self.ExpMenu, 'Experiments')
		self.AppendSubMenu(self.CompMenu, 'Compare to')
		self.AppendSeparator()
		self.Append(502, 'Native Sequence', kind=wx.ITEM_RADIO)
		self.Append(503, 'Recombinant Sequence', kind=wx.ITEM_RADIO)
		self.AppendSeparator()
		self.Append(504, 'Normalized Values', kind=wx.ITEM_RADIO)
		self.Append(505, 'Regular Values', kind=wx.ITEM_RADIO)
		self.AppendSeparator()
		self.Append(506, 'Save Plot Image')
		self.AppendSeparator()
		self.Append(501, 'Reset View')
	  #---
	  #--> Check defaults
		self.CurrentState(nExp, seq, norm, exp, comp)
	  #---
	 #---
	 #--> Bind
		self.Bind(wx.EVT_MENU, self.OnReset,    id=501)
		self.Bind(wx.EVT_MENU, self.OnSeq,      id=502)
		self.Bind(wx.EVT_MENU, self.OnSeq,      id=503)
		self.Bind(wx.EVT_MENU, self.OnNorm,     id=504)
		self.Bind(wx.EVT_MENU, self.OnNorm,     id=505)
		self.Bind(wx.EVT_MENU, self.OnSavePlot, id=506)
		self.ExpMenu.Bind(wx.EVT_MENU, self.OnExp,      id=507)
		for i in range(1, nExp + 1, 1):
			tMid = 507 + i
			self.ExpMenu.Bind(wx.EVT_MENU, self.OnExp, id=tMid)
		for i in range(1, nExp + 3, 1):
			tMidd = self.Mid + i
			self.CompMenu.Bind(wx.EVT_MENU, self.OnComp, id=tMidd)
	 #---
	#---
	#endregion ------------------------------------------------ Instance Setup

	#region ------------------------------------------------------- My Methods
	def CurrentState(self, nExp, seq, norm, exp, comp):
		""" Check item based on the current window state
			---
			nExp : total number of experiment
			seq  : 0 Rec Seq, 1 Nat Seq 
			norm : 0 Regular values, 1 Normalized values
			exp  : current number of experiment
			comp : compare to
		"""	
		if seq == 0:
			self.Check(503, True)
		else:
			self.Check(502, True)
		if norm == 0:
			self.Check(505, True)
		else:
			self.Check(504, True)
		tMid = 507 + exp
		self.ExpMenu.Check(tMid, True)
		tMid = 507 + nExp
		if comp is None:
			self.CompMenu.Check(tMid + 1, True)
		else:
			tMid = tMid + 2 + comp
			self.CompMenu.Check(tMid, True)
		return True
	#---	

	def OnReset(self, event):
		""" Reset the window """
		win = self.GetWindow()
		win.OnReset(self.Mid)
		return True
	#---

	def OnSeq(self, event):
		""" Change the plot if the sequence changes """
		win = self.GetWindow()
		win.OnSeq(event.GetId())
		return True
	#---

	def OnNorm(self, event):
		""" Change the plot if the normalization changes """
		win = self.GetWindow()
		win.OnNorm(event.GetId())
		return True
	#---

	def OnSavePlot(self, event):
		""" Save image of the plot """
		win = self.GetWindow()
		if win.OnSavePlotImage():
			return True
		else:
			return False
	#---

	def OnExp(self, event):
		""" Change the plot if experiment changes """
		win = self.GetWindow()
		win.OnExp(event.GetId())
		return True
	#--- 

	def OnComp(self, event):
		""" Changes the plot if comp changes """
		win = self.GetWindow()
		win.OnComp(event.GetId(), self.Mid)
		return True
	#---
	#endregion ---------------------------------------------------- My Methods
#---

class ToolMenuHistoRes(wx.Menu):
	""" Add Tools menu to a HistoR window"""

	#region --------------------------------------------------- Instance Setup
	def __init__(self, seq, uni):
		""" seq: 0 Rec Seq, 1 Nat Seq
			uni: 0 All Cuts, 1 Unique Cuts 
		"""
		super().__init__()
	 #--> Menu items
		self.Append(502, 'Native Sequence',      kind=wx.ITEM_RADIO)
		self.Append(503, 'Recombinant Sequence', kind=wx.ITEM_RADIO)
		self.AppendSeparator()
		self.Append(504, 'All cleavages',        kind=wx.ITEM_RADIO)
		self.Append(505, 'Unique cleavages',     kind=wx.ITEM_RADIO)
		self.AppendSeparator()
		self.Append(506, 'Save Plot Image')
		self.AppendSeparator()
		self.Append(501, 'Reset View')
	 #---
	 #--> Check defaults
		self.CurrentState(seq, uni)
	 #---
	 #--> Bind
		self.Bind(wx.EVT_MENU, self.OnReset,    id=501)
		self.Bind(wx.EVT_MENU, self.OnSeq,      id=502)
		self.Bind(wx.EVT_MENU, self.OnSeq,      id=503)
		self.Bind(wx.EVT_MENU, self.OnUni,      id=504)
		self.Bind(wx.EVT_MENU, self.OnUni,      id=505)
		self.Bind(wx.EVT_MENU, self.OnSavePlot, id=506)
	 #---
	#---
	#endregion ------------------------------------------------ Instance Setup

	#region ------------------------------------------------------- My Methods
	def CurrentState(self, seq, uni):
		""" Check the menu items based on the current window state
			---
			seq: 0 Rec Seq, 1 Nat Seq
			uni: 0 All Cuts, 1 Unique Cuts
		"""
		if seq == 0:
			self.Check(503, True)
		else:
			self.Check(502, True)
		if uni == 0:
			self.Check(504, True)
		else:
			self.Check(505, True)
		return True
	#---

	def OnReset(self, event):
		""" Reset the window """
		win = self.GetWindow()
		win.OnReset()
		return True
	#---

	def OnSavePlot(self, event):
		""" Save image of the plot """
		win = self.GetWindow()
		if win.OnSavePlotImage():
			return True
		else:
			return False
	#---

	def OnSeq(self, event):
		""" Change the plot if the sequence changes """
		win = self.GetWindow()
		win.OnSeq(event.GetId())
		return True
	#---

	def OnUni(self, event):
		""" Change the plot if the type of cleavages changes """
		win = self.GetWindow()
		win.OnUni(event.GetId())
		return True
	#---
	#endregion ---------------------------------------------------- My Methods		
#---

class ToolMenuAAdistRes(wx.Menu):
	""" Pop Up menu in AAdistR """

	#region --------------------------------------------------- Instance Setup
	def __init__(self, exp, pos, nExp, nPosName):
		""" exp     : current experiment
			pos     : current position
			nExp    : total number of experiments
			nPosName: list with the positions label 
		"""
		super().__init__()
	 #--> Menu items
	  #--> Experiment menu
		self.ExpMenu = wx.Menu()
		self.ExpMenu.Append(503, 'FP List', kind=wx.ITEM_RADIO)
		for i in range(1, nExp + 1, 1):
			self.Mid = 503 + i
			name = 'Experiment ' + str(i)
			self.ExpMenu.Append(self.Mid, name, kind=wx.ITEM_RADIO)
	  #---
	  #--> Positions menu
		self.CompMenu = wx.Menu()
		tempID = self.Mid + 1
		self.CompMenu.Append(tempID, 'None', kind=wx.ITEM_RADIO)
		for i in nPosName:
			tempID = tempID + 1
			self.CompMenu.Append(tempID, str(i), kind=wx.ITEM_RADIO)			
	  #---
	  #--> All together
		self.AppendSubMenu(self.ExpMenu, 'Experiments')
		self.AppendSubMenu(self.CompMenu, 'Compare Positions')
		self.AppendSeparator()
		self.Append(502, 'Save Plot Image')
		self.AppendSeparator()
		self.Append(501, 'Reset View')
	  #---
	 #---
	 #--> Check defaults
		self.CurrentState(exp, pos)
	 #---
	 #--> Bind
		self.Bind(wx.EVT_MENU, self.OnReset, id=501)
		self.Bind(wx.EVT_MENU, self.OnSavePlotImage, id=502)
		self.ExpMenu.Bind(wx.EVT_MENU, self.OnExp, id=503)
		for i in range(1, nExp + 1, 1):
			tMid = 503 + i
			self.ExpMenu.Bind(wx.EVT_MENU, self.OnExp, id=tMid)
		tempID = tMid + 1
		self.CompMenu.Bind(wx.EVT_MENU, self.OnPos, id=tempID)
		for i in range(1, len(nPosName) + 1, 1):
			TtempID = tempID + i
			self.CompMenu.Bind(wx.EVT_MENU, self.OnPos, id=TtempID)
	 #---
	#---
	#endregion ------------------------------------------------ Instance Setup
		
	#region ------------------------------------------------------- My Methods
	def OnSavePlotImage(self, event):
		""" Save image of the plot """
		win = self.GetWindow()
		if win.OnSavePlotImage():
			return True
		else:
			pass
	#---

	def CurrentState(self, exp, pos):
		""" Mark the current values
			---
			exp: Current experiment
			pos: Current position 
		"""
		self.ExpMenu.Check(503 + exp, True)
		self.CompMenu.Check(self.Mid + 1 + pos, True)
		return True
	#----

	def OnExp(self, event):
		""" Show the AAdist for a particular experiment """
		win = self.GetWindow()
		win.OnExp(event.GetId())
		return True
	#---

	def OnReset(self, event):
		""" Reset the view """
		win = self.GetWindow()
		win.OnReset(self.Mid)
		return True	
	#---

	def OnPos(self, event):
		""" Compare the distribution for a particular position in all 
			experiments 
		"""
		win = self.GetWindow()
		win.OnPos(event.GetId(), self.Mid)
		return True
	#---
	#endregion ---------------------------------------------------- My Methods	
#---

class ToolMenuLimProtRes(wx.Menu):
	""" Tool menu in LimprotRes """
	
	#region --------------------------------------------------- Instance Setup
	def __init__(self, selM):
		""" selM: selection mode. True Select Lane, False Select Band """
		super().__init__()
	 #--> Menu items
		self.Append(505, 'Lane Selection Mode\tCtrl+L', kind=wx.ITEM_CHECK)
		self.AppendSeparator()
		self.Append(504, 'Export Filtered Peptides')
		self.AppendSeparator()
		self.Append(503, 'Save Fragments Image')
		self.Append(502, 'Save Gel Image')
		self.AppendSeparator()
		self.Append(501, 'Reset View')
	 #---
	 #--> Bind
		self.Bind(wx.EVT_MENU, self.OnReset,    id=501)
		self.Bind(wx.EVT_MENU, self.OnSaveGel,  id=502)
		self.Bind(wx.EVT_MENU, self.OnSaveFrag, id=503)
		self.Bind(wx.EVT_MENU, self.OnExportFP, id=504)
		self.Bind(wx.EVT_MENU, self.OnSelM,     id=505)
	 #---
	 #--> Current Status
		if selM:
			self.Check(505, True)
		else:
			self.Check(505, False)
	 #---
	#---
	#endregion ------------------------------------------------ Instance Setup
 	
	#region ------------------------------------------------------- My Methods
	def OnExportFP(self, event):
		""" Export the list of filtered peptides """
		win = self.GetWindow()
		win.OnExportFP()
		return True
	#---

	def OnSaveGel(self, event):
		""" Save image of the plot """
		win = self.GetWindow()
		win.OnSaveGel()
		return True
	#---

	def OnSaveFrag(self, event):
		""" Save an image of the fragments  """
		win = self.GetWindow()
		win.OnSaveFrag()
		return True
	#---		

	def OnSelM(self, event):
		""" Change selection mode """
		win = self.GetWindow()
		win.OnSelM()		
		return True
	#---

	def OnReset(self, event):
		""" Reset the view """
		win = self.GetWindow()
		win.OnResetView()
		return True
	#---
	#endregion ---------------------------------------------------- My Methods	
#---

class ToolMenuTarProtRes(wx.Menu):
	""" Handles the pop up menu in tarprotR """	

	#region --------------------------------------------------- Instance Setup
	def __init__(self):
		""" """
		super().__init__()
	 #--> Menu items
		self.Append(504, 'Export Filtered Peptides')
		self.AppendSeparator()
		self.Append(503, 'Save Fragments Image')
		self.Append(502, 'Save Plot Image')
		self.AppendSeparator()
		self.Append(501, 'Reset View')
	 #---
	 #--> Bind
		self.Bind(wx.EVT_MENU, self.OnReset,    id=501)
		self.Bind(wx.EVT_MENU, self.OnSavePlot, id=502)
		self.Bind(wx.EVT_MENU, self.OnSaveFrag, id=503)
		self.Bind(wx.EVT_MENU, self.OnExportFP, id=504)
	 #---
	#---
	#endregion ------------------------------------------------ Instance Setup
		
	#region ------------------------------------------------------- My Methods
	def OnSavePlot(self, event):
		""" Save image of the plot """
		win = self.GetWindow()
		win.OnSavePlot()
		return True
	#---

	def OnSaveFrag(self, event):
		""" Save an image of the fragments  """
		win = self.GetWindow()
		win.OnSaveFrag()
		return True
	#---		

	def OnReset(self, event):
		""" Reset the view """
		win = self.GetWindow()
		win.OnResetView()
		return True
	#---

	def OnExportFP(self, event):
		""" Export the list of filtered peptides """
		win = self.GetWindow()
		win.OnExportFP()
		return True
	#---
	#endregion ---------------------------------------------------- My Methods	
#---

class ToolMenuMergeAA(wx.Menu):
	""" Tools menu in mergeAA """	

	#region --------------------------------------------------- Instance Setup
	def __init__(self):
		super().__init__()
	 #--> Menu items
		self.Append(501, 'Delete selected paths')
		self.Append(502, 'Delete all paths')
	 #---
	 #--> Bind
		self.Bind(wx.EVT_MENU, self.OnDelSel, id=501)
		self.Bind(wx.EVT_MENU, self.OnDelAll, id=502)
	 #---
	#---
	#endregion ------------------------------------------------ Instance Setup

	#region ------------------------------------------------------- My Methods
	def OnDelAll(self, event):
		""" Del all items in the list """
		win = self.GetWindow()
		win.OnDelAll()
		return True
	#---

	def OnDelSel(self, event):
		""" Del selected items in the list """
		win = self.GetWindow()
		win.OnDelSel()
		return True
	#---
	#endregion ---------------------------------------------------- My Methods
#---
#endregion --------------------------------------------- Individual Tool menus

#region ------------------------------------------------------------ Menu Bars
class MenuBarProtProfRes(MainMenuBar):
	""" Tools for ProtProfResV """
	
	#region --------------------------------------------------- Instance Setup
	def __init__(self, nC, nt, lC, lt, n, tp, allL, grayC):
		""" nC   : Total number of conditions
			nt   : Total number of relevant points,
			lC   : Legend for conditions
			lt   : Legend for relevant points
			n    : Current condition
			tp   : Current relevant points
			allL : Show all lines in Time Analysis (Boolean)
			grayC: Color for the lines in Time Analysis (Boolean)  
		"""
		super().__init__()
	 #--> Menu items
		self.VolcanoPlotMenu  = ToolMenuProtProfResV(nC, nt, lC, lt, n, tp)
		self.TimeAnalysisMenu = ToolMenuProtProfResT(allL, grayC)
		self.FilterMenu       = MenuFilterMainMenu()
		self.ToolsMenu = wx.Menu()
		self.ToolsMenu.AppendSubMenu(self.VolcanoPlotMenu, 'Volcano Plot')
		self.ToolsMenu.AppendSeparator()
		self.ToolsMenu.AppendSubMenu(self.TimeAnalysisMenu, 'Time Analysis')
		self.ToolsMenu.AppendSeparator()
		self.ToolsMenu.AppendSubMenu(self.FilterMenu, 'Filters')
		self.ToolsMenu.AppendSeparator()
		self.ToolsMenu.AppendCheckItem(599, 'Corrected P values')
	 #---
	 #--> Append to menu bar
		if config.cOS == 'Darwin':
			self.Insert(2, self.ToolsMenu, '&Tools')
		elif config.cOS == 'Windows':
			self.Insert(3, self.ToolsMenu, '&Tools')
		elif config.cOS == 'Linux':
			self.Insert(3, self.ToolsMenu, '&Tools')
		else:
			pass
	 #---
	 #--> Bind
		self.Bind(wx.EVT_MENU, self.OnCorrP, id=599)
	 #---
	#---
	#endregion ------------------------------------------------ Instance Setup

	#region ------------------------------------------------------- My Methods
	def OnCorrP(self, event):
		""" Show corrected P values """
		win = self.GetFrame()
		win.OnCorrP()
		return True 
	#---
	#endregion ---------------------------------------------------- My Methods
#---
#endregion --------------------------------------------------------- Menu Bars
