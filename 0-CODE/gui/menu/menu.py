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
		self.export  = self.Append(-1, 'Export Data')
		self.mergeAA = self.Append(-1, 'Merge aadist Files')
		self.shortDF = self.Append(-1, 'Short Data Files')
	 #---
	 #--> Bind
		self.Bind(wx.EVT_MENU, self.OnCorrA,   source=self.corrA)	 
		self.Bind(wx.EVT_MENU, self.OnInputF,  source=self.inputF)
		self.Bind(wx.EVT_MENU, self.OnExport,  source=self.export)
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

	def OnExport(self, event):
		""" Export data from the json format to csv """
		gmethods.MenuOnExport()
		return True
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

class ToolsTypeResults(wx.Menu):
	""" Tool menu for the Type Results window """

	#region --------------------------------------------------- Instance Setup
	def __init__(self):
		""" """
		super().__init__()
	 #--> Menu items
		self.copy = self.Append(-1, 'Copy Selected Columns\tCtrl+C')
	 #---
	 #--> Bind
		self.Bind(wx.EVT_MENU, self.OnLBoxCopy, source=self.copy)
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

class ToolsCorrAUtil(wx.Menu):
	""" Creates the tools menu for the correlation analysis window """
	
	#region --------------------------------------------------- Instance Setup
	def __init__(self):
		""" """
		super().__init__()
	 #--> Menu items
		self.delSel = self.Append(-1, 'Delete Selected')
		self.clearL = self.Append(-1, 'Clear List')
	 #---
	 #--> Bind
		self.Bind(wx.EVT_MENU, self.OnClearL, source=self.clearL)
		self.Bind(wx.EVT_MENU, self.OnDelSel, source=self.delSel)
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

class CorrAResExport(wx.Menu):
	""" Export menu in the Correlation analysis result window """
	#region --------------------------------------------------- Instance Setup
	def __init__(self):
		""""""
		super().__init__()
	 #--> Menu items & Bind
		for k, e in config.modules.items():
			self.Append(k, e)
			self.Bind(wx.EVT_MENU, self.OnExport, id=k)
	 #---
	#---
	#endregion ------------------------------------------------ Instance Setup

	#region -------------------------------------------------------- MyMethods
	def OnExport(self, event):
		""" Export columns in the correlation plot """	
		win = self.GetWindow()
		if win.OnExport(event.GetId()):
			return True
		else:
			return True
	#---
	#endregion ----------------------------------------------------- MyMethods
#---

class ToolsHistoRes(wx.Menu):
	""" Add Tools menu to a Histogram results window. 
	
		In this case is better to use IDs as int for the menu items 
	"""

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

class TarProtFPExp(wx.Menu):
	""" Experiments menu for the TarProt module starting with FP 
	
		Menu items IDs (int) are used to identify the experiments
	"""

	#region --------------------------------------------------- Instance Setup
	def __init__(self, nExp):
		""" nExp: number of experiments in the .tarprot file """
		super().__init__()
	 #--> Menu items
		self.Append(100, 'FP List', kind=wx.ITEM_RADIO)
		for i in range(101, 101 + nExp, 1):
			name = 'Experiment ' + str(i-100)
			self.Append(i, name, kind=wx.ITEM_RADIO)		
	 #---
	 #--> Bind
		for i in range(100, 101+nExp, 1):
			self.Bind(wx.EVT_MENU, self.OnExp, id=i)
	 #---
	#---
	#endregion ------------------------------------------------ Instance Setup

	#region -------------------------------------------------------- MyMethods
	def OnExp(self, event):
		""" Show the AAdist for a particular experiment """
		win = self.GetWindow()
		win.OnExp(event.GetId())
		return True
	#---
	#endregion ----------------------------------------------------- MyMethods
#---

class AAdistResPos(wx.Menu):
	""" Positions menu for the AA distribution result window 
		
		Menu items IDs (int) are used to identify the position
	"""

	#region --------------------------------------------------- Instance Setup
	def __init__(self, nPosName):
		""" nPosName: list with the positions label """
		super().__init__()
	 #--> Menu items
		self.Append(200, 'None', kind=wx.ITEM_RADIO)
		for k, e in enumerate(nPosName, start=201):
			self.Append(k, e, kind=wx.ITEM_RADIO)
	 #---
	 #--> Bind
		for k in range(200, 201 + len(nPosName), 1):
			self.Bind(wx.EVT_MENU, self.OnPos, id=k)
	 #---
	#---
	#endregion ------------------------------------------------ Instance Setup

	#region -------------------------------------------------------- MyMethods
	def OnPos(self, event):
		""" Compare the distribution for a particular position in all 
			experiments 
		"""
		win = self.GetWindow()
		win.OnPos(event.GetId())
		return True
	#---
	#endregion ----------------------------------------------------- MyMethods
#---

class TarProtNoneFPExp(wx.Menu):
	""" Experiments menu for the TarProt module including None and FP """

	#region --------------------------------------------------- Instance Setup
	def __init__(self, nExp):
		""" nExp: number of experiments in the .tarprot file """ 
		super().__init__()
	 #--> Menu items
		self.Append(200, 'None', kind=wx.ITEM_RADIO)
		self.Append(201, 'FP List', kind=wx.ITEM_RADIO)
		for i in range(202, 202+nExp, 1):
			name = 'Experiment ' + str(i-201)
			self.Append(i, name, kind=wx.ITEM_RADIO)				
	 #---
	 #--> Bind
		for i in range(200, 202+nExp, 1):
			self.Bind(wx.EVT_MENU, self.OnComp, id=i)
	 #---
	#---
	#endregion ------------------------------------------------ Instance Setup

	#region -------------------------------------------------------- MyMethods
	def OnComp(self, event):
		""" Changes the plot if comp changes """
		win = self.GetWindow()
		win.OnComp(event.GetId())
		return True
	#---
	#endregion ----------------------------------------------------- MyMethods
#---

class ToolsMergeAA(wx.Menu):
	""" Tools menu in mergeAA """	

	#region --------------------------------------------------- Instance Setup
	def __init__(self):
		super().__init__()
	 #--> Menu items
		self.delSel = self.Append(-1, 'Delete Selected Paths')
		self.delAll = self.Append(-1, 'Delete All Paths')
	 #---
	 #--> Bind
		self.Bind(wx.EVT_MENU, self.OnDelSel, source=self.delSel)
		self.Bind(wx.EVT_MENU, self.OnDelAll, source=self.delAll)
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

class ToolsTarProtRes(wx.Menu):
	""" Handles the pop up menu in tarprotR """	

	#region --------------------------------------------------- Instance Setup
	def __init__(self):
		""" """
		super().__init__()
	 #--> Menu items
		self.expFP = self.Append(-1, 'Export Filtered Peptides')
		self.AppendSeparator()
		self.saveF = self.Append(-1, 'Save Fragments Image')
		self.saveP = self.Append(-1, 'Save Plot Image')
		self.AppendSeparator()
		self.reset = self.Append(-1, 'Reset View')
	 #---
	 #--> Bind
		self.Bind(wx.EVT_MENU, self.OnReset,    source=self.reset)
		self.Bind(wx.EVT_MENU, self.OnSavePlot, source=self.saveP)
		self.Bind(wx.EVT_MENU, self.OnSaveFrag, source=self.saveF)
		self.Bind(wx.EVT_MENU, self.OnExportFP, source=self.expFP)
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

class ConditionsProtProfV(wx.Menu):
	""" Conditions menu in ProtProf results volcano window """
	#region --------------------------------------------------- Instance Setup
	def __init__(self, lC):
		""" lC : conditions legends """
		super().__init__()
	 #--> Menu items & Binding
		for k, i in enumerate(lC, start=100):
			self.Append(k, i, kind=wx.ITEM_RADIO)
			self.Bind(wx.EVT_MENU, self.OnCond, id=k)
	 #---
	#---
	#endregion ------------------------------------------------ Instance Setup

	#region -------------------------------------------------------- MyMethods
	def OnCond(self, event):
		""" Select condition """ 
		win = self.GetWindow()
		win.OnCond(event.GetId())		
		return True
	#---
	#endregion ----------------------------------------------------- MyMethods
#---

class RevPointsProtProfV(wx.Menu):
	""" Relevant points menu in ProtProf results volcano window """
	#region --------------------------------------------------- Instance Setup
	def __init__(self, lRP):
		""" lRP : relevant points legend """
		super().__init__()
	 #--> Menu items & Binding
		for k, i in enumerate(lRP, start=200):
			self.Append(k, i, kind=wx.ITEM_RADIO)
			self.Bind(wx.EVT_MENU, self.OnRP, id=k)
	 #---
	#---
	#endregion ------------------------------------------------ Instance Setup

	#region -------------------------------------------------------- MyMethods
	def OnRP(self, event):
		""" Select time point """ 
		win = self.GetWindow()
		win.OnRP(event.GetId())		
		return True
	#---
	#endregion ----------------------------------------------------- MyMethods
#---

class ToolsProtProfResRP(wx.Menu):
	""" Tools menu for ProtProf relevant points result window """

	#region --------------------------------------------------- Instance Setup
	def __init__(self, allL, grayC):
		""" allL  : Draw all protein lines
			grayC : Draw lines in gray or with different colors
		"""
		super().__init__()
	 #--> Menu items
		self.Append(300, 'Show All',   kind=wx.ITEM_CHECK)
		self.AppendSeparator()
		self.Append(301, 'Same Color', kind=wx.ITEM_CHECK)
		self.AppendSeparator()
		self.saveRP = self.Append(-1, 'Save Plot Image')
		self.AppendSeparator()
		self.reset = self.Append(-1, 'Reset View')
	 #---
	 #--> Current
		self.CurrentState(allL, grayC)
	 #---
	 #--> Bind
		self.Bind(wx.EVT_MENU, self.OnReset,    source=self.reset)
		self.Bind(wx.EVT_MENU, self.OnSavePlot, source=self.saveRP)
		self.Bind(wx.EVT_MENU, self.OnAll,      id=300)
		self.Bind(wx.EVT_MENU, self.OnColor,    id=301)
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
			self.Check(300, True)
		else:
			self.Check(300, False)
		if grayC:
			self.Check(301, True)
		else:
			self.Check(301, False)		
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
		if win.p3.OnSaveImage():
			return True
		else:
			return False
	#---
	#endregion ---------------------------------------------------- My Methods
#---

class FilterElementMonotonicity(wx.Menu):
	""" Creates the monotonicity filter menu """

	kwargs = {
		400: { 'up'  : True, },
		401: { 'down': True, },
		402: { 'both': True, },
	}

	#region --------------------------------------------------- Instance setup
	def __init__(self):
		""" """
		super().__init__()
	 #--> Menu items
		self.Append(400, 'Increasing')
		self.Append(401, 'Decreasing')
		self.Append(402, 'Both')
	 #---
	 #--> Bind
		for k in range(400, 403):
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

class FilterRemove(wx.Menu):
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

class ToolsCorrARes(wx.Menu):
	""" Creates the pop up menu in the correlation results window """
	
	#region --------------------------------------------------- Instance Setup
	def __init__(self):
		""" """
	 #--> Init
		super().__init__()
	 #---
	 #--> Menu items
		self.Export = CorrAResExport()
		self.AppendSubMenu(self.Export, 'Export Data to')
		self.AppendSeparator()
		self.saveImg = self.Append(-1, 'Save Plot Image')
	 #---
	 #--> Bind
		self.Bind(wx.EVT_MENU, self.OnSavePlot, source=self.saveImg)
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
	#endregion ---------------------------------------------------- My Methods		
#---

class ToolsAAdistRes(wx.Menu):
	""" Tools menu for the AA distribution results window """
	
	#region --------------------------------------------------- Instance Setup
	def __init__(self, exp, pos, nExp, nPosName):
		""" exp     : current experiment 0 to nExp
			pos     : current position 0 to len(nPosName)
			nExp    : total number of experiments
			nPosName: list with the positions label 
		"""
		super().__init__()
	 #--> Menu items
		self.Exp = TarProtFPExp(nExp)
		self.Pos = AAdistResPos(nPosName)
		self.AppendSubMenu(self.Exp, 'Experiments')
		self.AppendSubMenu(self.Pos, 'Compare Positions')
		self.AppendSeparator()
		self.save = self.Append(-1, 'Save Plot Image')
		self.AppendSeparator()
		self.reset = self.Append(-1, 'Reset View')
	 #---
	 #--> Bind
		self.Bind(wx.EVT_MENU, self.OnSavePlotImage, source=self.save)
		self.Bind(wx.EVT_MENU, self.OnReset, source=self.reset)
	 #---
	 #--> Check current selected items
		self.CurrentState(exp, pos)
	 #---
	#---
	#endregion ------------------------------------------------ Instance Setup

	#region -------------------------------------------------------- MyMethods
	def CurrentState(self, exp, pos):
		""" Mark the current values
			---
			exp: Current experiment 0 to nExp
			pos: Current position 0 to len(nPosName)
		"""
		self.Exp.Check(100+exp, True)
		self.Pos.Check(200+pos, True)
		return True
	#----

	def OnSavePlotImage(self, event):
		""" Save image of the plot """
		win = self.GetWindow()
		if win.OnSavePlotImage():
			return True
		else:
			pass
	#---

	def OnReset(self, event):
		""" Reset the view """
		win = self.GetWindow()
		win.OnReset()
		return True	
	#---
	#endregion ----------------------------------------------------- MyMethods
#---

class ToolsCutRes(wx.Menu):
	""" Tools menu for the Cleavage per Residue Res utility window """
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
		self.Exp  = TarProtFPExp(nExp)
		self.Comp = TarProtNoneFPExp(nExp)

		self.AppendSubMenu(self.Exp, 'Experiments')
		self.AppendSubMenu(self.Comp, 'Compare to')
		self.AppendSeparator()
		self.Append(301, 'Native Sequence',      kind=wx.ITEM_RADIO)
		self.Append(302, 'Recombinant Sequence', kind=wx.ITEM_RADIO)
		self.AppendSeparator()
		self.Append(303, 'Normalized Values', kind=wx.ITEM_RADIO)
		self.Append(304, 'Regular Values',    kind=wx.ITEM_RADIO)
		self.AppendSeparator()
		self.save = self.Append(-1, 'Save Plot Image')
		self.AppendSeparator()
		self.reset = self.Append(-1, 'Reset View')
	 #---
	 #--> Bind		
		self.Bind(wx.EVT_MENU, self.OnSeq,      id=301)
		self.Bind(wx.EVT_MENU, self.OnSeq,      id=302)
		self.Bind(wx.EVT_MENU, self.OnNorm,     id=303)
		self.Bind(wx.EVT_MENU, self.OnNorm,     id=304)
		self.Bind(wx.EVT_MENU, self.OnSavePlot, source=self.save)
		self.Bind(wx.EVT_MENU, self.OnReset,    source=self.reset)
	 #---
	 #--> Check defaults
		self.CurrentState(nExp, seq, norm, exp, comp)
	 #---	 
	#---
	#endregion ------------------------------------------------ Instance Setup

	#region -------------------------------------------------------- MyMethods
	def CurrentState(self, nExp, seq, norm, exp, comp):
		""" Check item based on the current window state
			---
			nExp : total number of experiment
			seq  : 0 Rec Seq, 2 Nat Seq 
			norm : 0 Regular values, 1 Normalized values
			exp  : current number of experiment
			comp : compare to
		"""	
	 #-->
		self.Exp.Check(100+exp, True)
	 #---
	 #-->
		if comp is None:
			self.Comp.Check(200, True)
		else:
			self.Comp.Check(201+comp, True)
	 #---
	 #-->
		if seq == 0:
			self.Check(302, True)
		else:
			self.Check(301, True)
	 #---
	 #-->
		if norm == 0:
			self.Check(304, True)
		else:
			self.Check(303, True)
	 #---
	 #-->
		return True
	 #---
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

	def OnReset(self, event):
		""" Reset the window """
		win = self.GetWindow()
		win.OnReset()
		return True
	#---
	#endregion ----------------------------------------------------- MyMethods
#---

class ToolsLimProtRes(wx.Menu):
	""" Tool menu in LimprotRes """
	
	#region --------------------------------------------------- Instance Setup
	def __init__(self, selM):
		""" selM: selection mode. True Select Lane, False Select Band """
		super().__init__()
	 #--> Menu items
		self.selM = self.Append(100, 'Lane Selection Mode\tCtrl+L', kind=wx.ITEM_CHECK)
		self.AppendSeparator()
		self.expFP = self.Append(-1, 'Export Filtered Peptides')
		self.AppendSeparator()
		self.saveF = self.Append(-1, 'Save Fragments Image')
		self.saveG = self.Append(-1, 'Save Gel Image')
		self.AppendSeparator()
		self.reset = self.Append(-1, 'Reset View')
	 #---
	 #--> Bind
		self.Bind(wx.EVT_MENU, self.OnReset,    source=self.reset)
		self.Bind(wx.EVT_MENU, self.OnSaveGel,  source=self.saveG)
		self.Bind(wx.EVT_MENU, self.OnSaveFrag, source=self.saveF)
		self.Bind(wx.EVT_MENU, self.OnExportFP, source=self.expFP)
		self.Bind(wx.EVT_MENU, self.OnSelM,     source=self.selM)
	 #---
	 #--> Current Status
		if selM:
			self.Check(100, True)
		else:
			self.Check(100, False)
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

class ToolsProtProfResV(wx.Menu):
	""" Menu for the volcano plot in ProtProf results window """
	#region --------------------------------------------------- Instance Setup
	def __init__(self, lC, lRP, nC, nRP):
		""" lC : conditions legends
			lRP: relevant points legend
			nC : current selected condition
			nRP: current selected relevant point
		"""
		super().__init__()
	 #--> Menu items
		self.Cond = ConditionsProtProfV(lC)
		self.RP   = RevPointsProtProfV(lRP)

		self.AppendSubMenu(self.Cond, 'Conditions')
		self.AppendSubMenu(self.RP, 'Relevant Points')
		self.AppendSeparator()
		self.aFilter = self.Append(-1, 'Apply Filters')
		self.AppendSeparator()
		self.aVal   = self.Append(-1, 'α value')
		self.zScore = self.Append(-1, 'Z score Threshold')
		self.AppendSeparator()
		self.saveV = self.Append(-1, 'Save Plot Image')
		self.AppendSeparator()
		self.reset = self.Append(-1, 'Reset View')
	  #---
	 #---
	 #--> Bind
		self.Bind(wx.EVT_MENU, self.OnReset,        source=self.reset)
		self.Bind(wx.EVT_MENU, self.OnSavePlot,     source=self.saveV)
		self.Bind(wx.EVT_MENU, self.OnaVal,         source=self.aVal)
		self.Bind(wx.EVT_MENU, self.OnZScore,       source=self.zScore)
		self.Bind(wx.EVT_MENU, self.OnFilter_Apply, source=self.aFilter)
	 #---
	 #--> Current state
		self.CurrentState(nC, nRP)		
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

	def OnaVal(self, event):
		""" Set new Z score threshold in % """
		win = self.GetWindow()
		win.OnaVal()
		return True
	#---

	def OnZScore(self, event):
		""" Set new Z score threshold in % """
		win = self.GetWindow()
		win.OnZScore()
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
		if win.p2.OnSaveImage():
			return True
		else:
			return False
	#---

	def CurrentState(self, nC, nRP):
		""" Check the menu items based on the current state of the window
			---
			nC  : current number of condition
			nRP : current relevant points
		"""
		self.Cond.Check(100+nC, True)
		self.RP.Check(200+nRP, True)
		return True
	#---
	#endregion ---------------------------------------------------- My Methods
#---

class FilterAdd(wx.Menu):
	""" Menu to add filter in ProtProfRes """

	filter_keys = {
		500 : 'Filter_ZScore',
		501 : 'Filter_Log2FC',
	}

	#region --------------------------------------------------- Instance Setup
	def __init__(self):
		""" """
		super().__init__()
	 #--> Menu items
		self.Monotonicity = FilterElementMonotonicity()

		self.zScore = self.Append(500, 'Z score')
		self.log2FC = self.Append(501, 'Log2FC')
		self.pVal   = self.Append(-1, 'P value')
		self.oneP   = self.Append(-1, 'α value') 
		self.AppendSubMenu(self.Monotonicity, 'Monotonic')
		self.div    = self.Append(-1, 'Divergent')
	 #---

	 #--> Bind
		for k in range(500, 502):
			self.Bind(wx.EVT_MENU, self.OnFilter_Run, id=k)
		self.Bind(wx.EVT_MENU, self.OnFilter_P, source=self.pVal)
		self.Bind(wx.EVT_MENU, self.OnFilter_Divergent, source=self.div)
		self.Bind(wx.EVT_MENU, self.OnFilter_OneP, source=self.oneP)
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

class Filter(wx.Menu):
	""" Main Menu to control filters """

	#region --------------------------------------------------- Instance Setup
	def __init__(self):
		""""""
		super().__init__()
	 #--> Menu items
		self.Add = FilterAdd()
		self.Remove = FilterRemove()

		self.AppendSubMenu(self.Add, 'Add')
		self.AppendSubMenu(self.Remove, 'Remove')
		self.reset = self.Append(-1, 'Reset')
		self.AppendSeparator()
		self.iExport = self.Append(-1, 'Export Results')
	 #---
	 #--> Bind
		self.Bind(wx.EVT_MENU, self.OnReset,  source=self.reset)
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

class ToolsProtProfRes(wx.Menu):
	""" Tools menu for the ProtProf results window """

	#region --------------------------------------------------- Instance Setup
	def __init__(self, lC, lRP, nC, nRP, allL, grayC):
		""" lC : conditions legends
			lRP  : relevant points legend
			nC   : current selected condition
			nRP  : current selected relevant point
			allL : Draw all protein lines
			grayC: Draw lines in gray or with different colors
		"""
		super().__init__()
	 #--> Menu items
		self.Volcano = ToolsProtProfResV(lC, lRP, nC, nRP)
		self.RP      = ToolsProtProfResRP(allL, grayC)
		self.Filter  = Filter()

		self.AppendSubMenu(self.Volcano, 'Volcano Plot')
		self.AppendSeparator()
		self.AppendSubMenu(self.RP, 'Relevant Points')
		self.AppendSeparator()
		self.AppendSubMenu(self.Filter, 'Filters')
		self.AppendSeparator()
		self.corrP = self.Append(600, 'Corrected P Values', kind=wx.ITEM_CHECK)
	 #---
	 #--> Bind
		self.Bind(wx.EVT_MENU, self.OnCorrP, source=self.corrP)
	 #---
	#---
	#endregion ------------------------------------------------ Instance Setup

	#region -------------------------------------------------------- MyMethods
	def OnCorrP(self, event):
		""" Show corrected P values """
		win = self.GetWindow()
		win.OnCorrP()
		return True 
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
			self.Tools = config.pointer['menu']['toolmenu'][name]()
		else:
			self.Tools = config.pointer['menu']['toolmenu'][name](*args)
	 #---
	 #--> Append to menu bar
		if config.cOS == 'Darwin':
			self.Insert(2, self.Tools, '&Tools')
		elif config.cOS == 'Windows':
			self.Insert(3, self.Tools, '&Tools')
		elif config.cOS == 'Linux':
			self.Insert(3, self.Tools, '&Tools')
		else:
			pass		
	 #---
	#---
	#endregion ------------------------------------------------ Instance Setup
#---

class MenuBarProtProfRes(MainMenuBar):
	""" Tools for ProtProfRes """
	
	#region --------------------------------------------------- Instance Setup
	def __init__(self, lC, lRP, nC, nRP, allL, grayC):
		""" lC : conditions legends
			lRP  : relevant points legend
			nC   : current selected condition
			nRP  : current selected relevant point
			allL : Draw all protein lines
			grayC: Draw lines in gray or with different colors
		"""
		super().__init__()
	 #--> Menu items
		self.Tools = ToolsProtProfRes(lC, lRP, nC, nRP, allL, grayC)
	 #---
	 #--> Append to menu bar
		if config.cOS == 'Darwin':
			self.Insert(2, self.Tools, '&Tools')
		elif config.cOS == 'Windows':
			self.Insert(3, self.Tools, '&Tools')
		elif config.cOS == 'Linux':
			self.Insert(3, self.Tools, '&Tools')
		else:
			pass
	 #---
	#---
	#endregion ------------------------------------------------ Instance Setup
#---
#endregion ----------------------------------------------------------- Menubar






