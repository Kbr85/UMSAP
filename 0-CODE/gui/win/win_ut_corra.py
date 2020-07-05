# ------------------------------------------------------------------------------
# 	Copyright (C) 2017 Kenny Bravo Rodriguez <www.umsap.nl>

# 	This program is distributed for free in the hope that it will be useful,
# 	but WITHOUT ANY WARRANTY; without even the implied warranty of
# 	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

# 	See the accompaning licence for more details.
# ------------------------------------------------------------------------------


""" This module creates the Correlation analysis utility window """


#region -------------------------------------------------------------- Imports  
import wx
import json

import config.config as config
import gui.menu.menu as menu
import gui.gui_classes as gclasses
import gui.gui_methods as gmethods
import data.data_classes as dclasses
import data.data_methods as dmethods
import checks.checks_single as check
#endregion ----------------------------------------------------------- Imports


class WinCorrA(gclasses.WinUtilUno):
	""" Creates the GUI for the Correlation Analysis utility """

	#region --------------------------------------------------- Instance Setup
	def __init__(self, parent=None, style=None):
		""" parent: parent for the widgets
			style: style of the windows
		"""
	 #--> Initial Setup
		self.name = config.name["CorrA"]
		super().__init__(parent=parent, style=style, length=22)
	 #---
	 #--> Variables
		self.overW = False
		self.lboE = []
	 #---
	 #--> Menu
		self.menubar = menu.MainMenuBarWithTools(self.name)
		self.SetMenuBar(self.menubar)
	 #---
	 #--> Widgets
	  #--> Listbox
		self.lb = wx.ListCtrl(
			self.panel, size=(250, 500), style=wx.LC_REPORT | wx.BORDER_SIMPLE
		)
		self.lbo = wx.ListCtrl(
			self.panel, size=(250, 500), style=wx.LC_REPORT | wx.BORDER_SIMPLE
		)
		gmethods.ListCtrlHeaders(self.lb, self.name)
		gmethods.ListCtrlHeaders(self.lbo, "CorrA2")
	  #---
	  #--> Button
		self.buttonAddCol = wx.Button(self.panel, label="--Add columns->")
	  #---
	  #--> StaticText
		self.stColI = wx.StaticText(
			self.panel, label="Columns in the data file", style=wx.ALIGN_CENTER
		)
		self.stColC = wx.StaticText(self.panel, label="", style=wx.ALIGN_CENTER)
		self.stColO = wx.StaticText(
			self.panel, label="Columns to analyze", style=wx.ALIGN_CENTER
		)
	  #---
	 #---
	 #--> Sizers
	  #--> Listboxes
		self.sizerboxL = wx.FlexGridSizer(2, 3, 1, 1)
		self.sizerboxL.Add(self.stColI, border=2, flag=wx.ALIGN_CENTER | wx.ALL)
		self.sizerboxL.Add(self.stColC, border=2, flag=wx.ALIGN_CENTER | wx.ALL)
		self.sizerboxL.Add(self.stColO, border=2, flag=wx.ALIGN_CENTER | wx.ALL)
		self.sizerboxL.Add(self.lb, border=2, flag=wx.EXPAND | wx.ALIGN_CENTER | wx.ALL)
		self.sizerboxL.Add(self.buttonAddCol, border=2, flag=wx.ALIGN_CENTER | wx.ALL)
		self.sizerboxL.Add(
			self.lbo, border=2, flag=wx.EXPAND | wx.ALIGN_CENTER | wx.ALL
		)
	  #---
	  #--> add to sizerIn
		self.sizerIN.Add(
			self.sizerboxL, pos=(2, 2), border=2, flag=wx.EXPAND | wx.ALIGN_TOP | wx.ALL
		)
	  #---
	  #--> Fit
		self.sizer.Fit(self)
	  #---
	 #---
	 #--> Position
		self.Center()
	 #---
	 #--> Tooltips
		self.buttonAddCol.SetToolTip(config.tooltip[self.name]["AddCol"])
		self.stMethod.SetToolTip(config.tooltip[self.name]["CorrelationM"])
	 #---
	 #--> Bind
		for child in self.GetChildren():
			child.Bind(wx.EVT_RIGHT_DOWN, self.OnPopUpMenu)
		self.lb.Bind(wx.EVT_RIGHT_DOWN, self.OnPopUpMenu)
		self.lbo.Bind(wx.EVT_RIGHT_DOWN, self.OnPopUpMenu)
		self.buttonAddCol.Bind(wx.EVT_BUTTON, self.OnAddCol)
	 #---
	 #--> Default values
		self.tcOutputFF.SetValue("NA")
	 #---


	 #--> INITIAL VALUES FOR TESTING. DELETE BEFORE RELEASING!!!!!!!! ##########
		import getpass
		user = getpass.getuser()
		if config.cOS == "Darwin":
			self.tcDataFile.SetValue("/Users/" + str(user) + "/TEMP-GUI/BORRAR-UMSAP/PlayDATA/TARPROT/Mod-Enz-Dig-data-ms.txt")
			self.tcOutputFF.SetValue("/Users/" + str(user) + "/TEMP-GUI/BORRAR-UMSAP/PlayDATA/TARPROT/Untitled.corr")
		elif config.cOS == 'Windows':
			from pathlib import Path
			self.tcDataFile.SetValue(str(Path('C:/Users/bravo/Desktop/SharedFolders/BORRAR-UMSAP/PlayDATA/TARPROT/Mod-Enz-Dig-data-ms.txt')))
			self.tcOutputFF.SetValue(str(Path('C:/Users/bravo/Desktop/SharedFolders/BORRAR-UMSAP/PlayDATA/test.corr')))
		else:
			pass
	 #--- INITIAL VALUES FOR TESTING. DELETE BEFORE RELEASING!!!!!!!! ##########


	 #--> Show
		self.Show()
	 #---
	#---
	#endregion ------------------------------------------------ Instance Setup

	# ------------------------------------------------------------- My Methods
	#region -------------------------------------------------- Binding Methods
	def OnClearFilesDef(self):
		""" Specific clear for File section in this window """
		for lb in [self.lb, self.lbo]:
			lb.DeleteAllItems()
		self.lboE = []
		self.tcOutputFF.SetValue("NA")
		return True
	#---

	def OnClearValuesDef(self):
		""" Specific clear for Values section in this window """
		self.TextCtrlorCBox.SetValue("Log2")
		self.TextCtrlorCBox2.SetValue("Pearson")
		return True
	#---

	def OnAddCol(self, event):
		""" Add selected columns in self.lb to self.lbo. Columns are added 
			only once 
		"""
	 #--> Variables
		col = self.lb.GetColumnCount()
		sel = gmethods.ListCtrlGetSelected(self.lb)
	 #---
	 #--> Add only NEW columns. 
		for i in sel:
			num = int(self.lb.GetItemText(i))
			if num not in self.lboE:
				self.lboE.append(num)
				index = self.lbo.InsertItem(
					self.lbo.GetItemCount(), self.lb.GetItemText(i)
				)
				for c in range(1, col):
					self.lbo.SetItem(index, c, self.lb.GetItemText(i, c))
			else:
				pass
	 #---
	 #--> Color
		gmethods.ListCtrlZebraStyle(self.lbo)
	 #---
	 #--> Return
		return True
	 #---
	#---
	#endregion ----------------------------------------------- Binding Methods

	#region ----------------------------------------------------- Menu Methods
	def OnPopUpMenu(self, event):
		""" Show the popup menu over self.lbo """
		self.PopupMenu(menu.ToolsCorrAUtil())
		return True
	#---

	def OnClearL(self):
		""" Delete all from the wx.ListCtrl in the right"""
		self.lbo.DeleteAllItems()
		self.lboE = []
		return True
	#---

	def OnDelSel(self):
		""" Delete selected item from the wx.ListCtrl in the right """
	 #--> Get selection
		sel = gmethods.ListCtrlGetSelected(self.lbo)
	 #---
	 #--> Remove item
		for i in sel:
			num = int(self.lbo.GetItemText(i))
			self.lboE.remove(num)
	 #---
	 #--> Color
		gmethods.ListCtrlDeleteSelected(self.lbo)
	 #---
	 #--> Return
		return True
	 #---
	#---
	#endregion -------------------------------------------------- Menu Methods

	#region ------------------------------------------------------ Run Methods
	def CheckInput(self):
	 #--> Files and Folders
	  #--> Data file
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			"Checking user input: Data file", 1)
		if self.CheckGuiTcFileRead(self.tcDataFile,
			config.dictElemDataFile[self.name]["ExtShort"],
			"Datafile",
			config.dictCheckFatalErrorMsg[self.name]["Datafile"]):
			pass
		else:
			return False
	  #---
	  #--> Output file
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			"Checking user input: Output file", 1)
		if self.CheckGuiTcOutputFile(self.tcOutputFF,
			self.tcDataFile,
			config.dictElemOutputFileFolder[self.name]["DefNameFile"],
			config.dictElemOutputFileFolder[self.name]["ExtShort"],
			"Outputfile",
			config.dictCheckFatalErrorMsg[self.name]["OutputFile"]):
			pass
		else:
			return False
	  #---
	 #---
	 #--> Values
	  #--> Norm method
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			"Checking user input: Data normalization method", 1)
		val = self.TextCtrlorCBox.GetValue()
		if val == "None":
			valO = None
		else:
			valO = val
		self.d["Datanorm"] = val
		self.do["Datanorm"] = valO
	  #---
	  #--> Corr method
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			"Checking user input: Correlation method", 1)
		val = self.TextCtrlorCBox2.GetValue()
		self.d["Method"] = val
		self.do["Method"] = val.lower()
	  #---
	 #---
	 #--> ListCtrl
	  #--> Check that something is in self.lbo
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			"Checking user input: Items in the list box", 1)
		if check.CheckListCtrlEmpty(self.lbo,
			msg=config.dictCheckFatalErrorMsg[self.name]["ListCtrlRightEmpty"],
			nEle=2):
			pass
		else:
			return False
	  #---
	 #---
	 #--> Return
		return True
	 #---
	#---

	def ReadInputFiles(self):
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			"Reading files: Data file", 1)
		try:
			self.fileObj = dclasses.DataObjDataFile(self.do["Datafile"])
		except Exception:
			return False
		return True
	#---

	def SetVariable(self):
		""" """
	 #--> Get the list of columns indixes selected or all of them
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			"Setting variables: Column's indexes", 1)
		self.colCorr = gmethods.ListCtrlGetColVal(self.lbo, t="int")
		self.d["SelCol"] = self.colCorr
		self.do["SelCol"] = self.colCorr
	 #---
	 #--> Dat frame
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			"Setting variables: Pandas data frame", 1)
		out, self.dataFrame = dmethods.DFSelSet(
			self.fileObj.dataFrame, 
			self.colCorr, 
			"float", 
			self.name
		)
	 #---
	 #--> Return
		if out:
			return True
		else:
			return False
	 #---
	#---

	def RunAnalysis(self):
		""" """
	 #--> Normalization
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			"Running analysis: Normalizing data", 1)
		out, self.dataFrameN = dmethods.DataNorm(
			self.dataFrame, method=self.do["Datanorm"])
		if out:
			pass
		else:
			return False
	 #---
	 #--> Correlation
		l = len(self.colCorr)
		cT = l * l
		msg = ("Running analysis: Calculating " + str(cT) + " correlation " 
			"coefficients")
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress, msg, 1)
		self.corrCoeff = self.dataFrameN.corr(self.do["Method"])
	 #---
	 #--> Return
		return True
	 #---
	#---

	def WriteOF(self):
		""" """
	 #--> Values to string
		keys2string = ["Datafile", "Outputfile"]
		data = {
			"V": config.dictVersion,
			"I": self.d,
			"CI": dmethods.DictVal2String(self.do, keys2string),
			"R": self.corrCoeff.to_dict(),
		}
	 #---
	 #--> Write
		dmethods.FFsWriteJSON(self.do["Outputfile"], data)
	 #---
	 #--> Return
		return True
	 #---
	#---

	def ShowRes(self):
		msg = "Generating graphical representation of results"
		gmethods.UpdateGaugeText(self.gauge, self.stProgress, msg, 1)
		wx.Yield()
		if gmethods.WinGraphResCreate(config.name["CorrARes"], self.do["Outputfile"]):
			return True
		else:
			return False
	#---
	#endregion --------------------------------------------------- Run Methods
#---

