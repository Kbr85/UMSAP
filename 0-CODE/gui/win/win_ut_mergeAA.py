# ------------------------------------------------------------------------------
#	Copyright (C) 2017 Kenny Bravo Rodriguez <www.umsap.nl>
	
#	This program is distributed for free in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
	
#	See the accompaning licence for more details.
# ------------------------------------------------------------------------------


""" Creates the window to merge aadist files """


# ------------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Methods
# ------------------------------------------------------------------------------



#--- Imports
## Standard modules
import wx
from pathlib import Path
## My modules
import config.config     as config
import gui.menu.menu     as menu
import gui.gui_classes   as gclasses
import gui.gui_methods   as gmethods
import data.data_classes as dclasses
import data.data_methods as dmethods
#---



class WinMergeAAFiles(gclasses.WinMyFrame, gclasses.ElementHelpRun, 
	gclasses.ElementClearAF):
	""" Creates the window to merge aadist files """

	def __init__(self, parent=None, style=None, length=17):
		""" parent: parent of the widgets
			style: style of the windows
			length: length for the gauge
		"""
	 #--> Initial Setup
		self.name = config.name['MergeAA']
		self.fileL = []
		self.overW = False
		gclasses.WinMyFrame.__init__(self, parent=None, style=style)
		gclasses.ElementHelpRun.__init__(self, self.panel, length=length)
		gclasses.ElementClearAF.__init__(self, self.panel)
	 #--> Menu
		self.menubar = menu.MainMenuBarWithTools(self.name)
		self.SetMenuBar(self.menubar)		
	 #--> Widgets
	  #--> Lines
		self.lineHI1 = wx.StaticLine(self.panel)
		self.lineHI2 = wx.StaticLine(self.panel)
		self.lineVI1 = wx.StaticLine(self.panel, style=wx.LI_VERTICAL)
	  #--> ListBox
		self.lb = wx.ListCtrl(self.panel, 
			size=config.size['ListBox'][self.name], 
			style=wx.LC_REPORT|wx.BORDER_SIMPLE)
		gmethods.ListCtrlHeaders(self.lb, self.name)
	  #--> StaticBox
		self.boxFiles   = wx.StaticBox(self.panel, label="Files")
	  #--> Static text
		self.stColExt = wx.StaticText(self.boxFiles, label='Output file', 
			style=wx.ALIGN_RIGHT)
		self.stEmpty  = wx.StaticText(self.boxFiles, label='', 
			style=wx.ALIGN_RIGHT)
	  #--> Text control
		self.tcOutFile = wx.TextCtrl(self.boxFiles, value="", 
			size=config.size['TextCtrl']['MergeOut'])
		self.tcOutFile.SetBackgroundColour('WHITE')
	  #--> Buttons
		self.buttonFile    = wx.Button(self.boxFiles, label='aadist files')
		self.buttonOutFile = wx.Button(self.boxFiles, label='Output file')
	 #--> Sizers
	  #--> box sizer
		self.sizerboxFiles = wx.StaticBoxSizer(self.boxFiles, wx.VERTICAL)
		self.sizerboxFilesWid = wx.GridBagSizer(2, 2)
		self.sizerboxFiles.Add(self.sizerboxFilesWid, border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerboxFilesB = wx.FlexGridSizer(1, 2, 1, 1)
		self.sizerboxFilesB.Add(self.buttonFile,      border=2, 
			flag=wx.ALIGN_CENTER|wx.ALL)
		self.sizerboxFilesB.Add(self.buttonOutFile,   border=2, 
			flag=wx.ALIGN_CENTER|wx.ALL)
		self.sizerboxFilesWid.Add(self.sizerboxFilesB, pos=(0, 2), border=2, 
			flag=wx.ALIGN_CENTER|wx.ALL)
		self.sizerboxFilesWid.Add(self.stColExt,       pos=(1, 1), border=2, 
			flag=wx.ALIGN_CENTER|wx.ALL)
		self.sizerboxFilesWid.Add(self.tcOutFile,      pos=(1, 2), border=2, 
			flag=wx.ALIGN_CENTER|wx.ALL)
		self.sizerboxFilesWid.Add(self.stEmpty,        pos=(1, 3), border=2, 
			flag=wx.ALIGN_CENTER|wx.ALL)
	  #--> sizerIN
		self.sizerIN.Add(self.sizerClear ,   pos=(0,0), border=2, span=(3, 0),
			flag=wx.EXPAND|wx.ALIGN_TOP|wx.ALL)
		self.sizerIN.Add(self.lineVI1,       pos=(0,1), border=2, span=(3, 0),
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerIN.Add(self.sizerboxFiles, pos=(0,2), border=2,
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerIN.Add(self.lineHI1,       pos=(1,2), border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerIN.Add(self.lb,            pos=(2,2), border=2,
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerIN.Add(self.lineHI2,       pos=(3,0), border=2, span=(0, 3),
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerIN.Add(self.sizerBottom,   pos=(4,0), border=2, span=(0, 3),
			flag=wx.EXPAND|wx.ALIGN_TOP|wx.ALL)
	  #--> Fit
		self.sizer.Fit(self)
	 #--> Position
		self.Center()
	 #--> Tooltips
		self.buttonFile.SetToolTip(config.tooltip[self.name]['aadistFile'])
		self.buttonOutFile.SetToolTip(
			config.tooltip[self.name]['OutputFileB'])
		self.stColExt.SetToolTip(config.tooltip[self.name]['OutputFileT'])
	 #--> Binding
		self.buttonOutFile.Bind(wx.EVT_BUTTON, self.OnOutFile)
		self.buttonFile.Bind(wx.EVT_BUTTON, self.OnAAfiles)
		self.lb.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
		self.tcOutFile.Bind(wx.EVT_TEXT, self.OnTextChange)
	 #--> Show
		self.Show()
	#---

	####---- Methods of the class
	##-- Binding
	def OnClearFilesDef(self):
		""" Override to ElementClearAFVC """
		self.lb.DeleteAllItems()
		self.fileL = []
		return True
	#---

	def OnTextChange(self, event):
		""" Set self.overW = False if the user change the path to the file """
		self.overW = False
		return True
	#---

	def OnAAfiles(self, event):
		""" """
	 #--> Variables
		msg = config.dictElemDataFile2[self.name]['MsgOpenFile']
		wcard = config.dictElemDataFile2[self.name]['ExtLong']
		dlg = gclasses.DlgOpenFileS(msg, wcard)
	 #--> Get path to the file
		if dlg.ShowModal() == wx.ID_OK:
			fileL = dlg.GetPaths()
	 #--> Check file not already added & add & renumber
			for i in fileL:
				if i not in self.fileL:
					self.fileL.append(i)
				else:
					pass
			gmethods.ListCtrlColNames(self.fileL, self.lb, mode='list', 
				startIn=1)
		else:
			pass
	 #--> Destroy & Return
		dlg.Destroy()		
		return True
	#---

	def OnOutFile(self, event):
		""" Selec output file """
	 #-->
		dlg = gclasses.DlgSaveFile(
			config.dictElemOutputFileFolder[self.name]['ExtLong'])
	 #-->
		if dlg.ShowModal() == wx.ID_OK:
			self.tcOutFile.SetValue(dlg.GetPath())
			self.overW = True
		else:
			pass
	 #-->
		dlg.Destroy() 
		return True
	#---

	def OnRightDown(self, event):
		""" """
		self.PopupMenu(menu.ToolMenuMergeAA())
		return True
	#---

	##-- Menu
	def OnDelAll(self):
		""" Delete all paths """
		self.lb.DeleteAllItems()
		self.fileL = []
		return True
	#---

	def OnDelSel(self):
		""" Del selected paths """
	 #--> Get selected
		selInd = gmethods.ListCtrlGetSelected(self.lb)
	 #--> Delete
		if len(selInd) > 0:
			gmethods.ListCtrlDeleteSelected(self.lb)
			for i in reversed(selInd):
				del self.fileL[i]
		else:
			pass
	 #--> Renumber recolor
		gmethods.ListCtrlRenumberLB(self.lb)
		gmethods.ListCtrlZebraStyle(self.lb)
	 #--> Return
		return True
	#---

	###---Run
	def CheckInput(self):
		""" """
	 #--> Output file
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Checking user input: Output file', 1)
		if self.CheckGuiTcOutputFile2(self.tcOutFile, 
			config.dictElemOutputFileFolder[self.name]['ExtShort'], 
			'Outputfile',
			config.dictCheckFatalErrorMsg[self.name]['OutputFile']):
			pass
		else:
			return False		
	 #--> Number of files
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Checking user input: Number of files', 1)
		self.nFiles = self.lb.GetItemCount()
		if self.nFiles < 2:
			gclasses.DlgFatalErrorMsg(
				config.dictCheckFatalErrorMsg[self.name]['NoAAdistFiles'])
			return False
		else:
			pass
	 #--> Return			
		return True
	#---

	def ReadInputFiles(self):
		""" Read input files and check their content """
	 #--> Variables
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Reading input files: aadist files', 1)
		self.objList = []
		aVal = []
		nPos = []
		recSeq = []
	 #--> Read
		for k in range(0, self.nFiles, 1):
			msg = ("Reading input files: aadist files (" + str(k) + "/" 
				+ str(self.nFiles) + ")") 
			wx.CallAfter(gmethods.UpdateText, self.stProgress, msg)
			fileP = Path(self.lb.GetItemText(0, col=1))
			self.objList.append(dclasses.DataObjAAdistFile(fileP))
			aVal.append(self.objList[k].aVal)
			nPos.append(self.objList[k].nPos)
			recSeq.append(self.objList[k].recSeq)
	 #--> Check alpha
		if len(set(aVal)) != 1:
			msg = ("The alpha values used to create the files are different.\n"
				"Please remove the appropiate files.\nalpha-values in the "
				"files:\n" + str(aVal))
			gclasses.DlgFatalErrorMsg(msg)
			return False
		else:
			pass
	 #--> Check Pos
		if len(set(nPos)) != 1:
			msg = ("The number of analysed positions in the files are "
				"different.\nPlease remove the appropiate files.\nNumber of "
				"positions in the files:\n" + str(nPos))
			gclasses.DlgFatalErrorMsg(msg)
			return False
	 #--> Check seqs
		if len(set(recSeq)) != 1:
			simL = [1]
			for k in range(1, self.nFiles, 1):
				if recSeq[k] == recSeq[0]:
					simL.append(1)
				else:
					simL.append(0)
			msg = ("The protein sequences used to generate the given files are "
				"different.\nPlease remove the appropiate files.\nIdentity of "
				"the sequences in the files relative to hte sequence in the "
				"first file:\n" + str(simL))
			gclasses.DlgFatalErrorMsg(msg)
			return False
		else:
			pass
	 #--> Return			
		return True
	#---
	
	def SetVariable(self):
		""" """
		return True
	#---

	def RunAnalysis(self):
		""" """
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Running the analysis', 1)
	 #--> Variables			
		rows = self.objList[0].indKeys[0:-1]
		col  = self.objList[0].dfCol[1:]
		dfo  = self.objList[0].dataDF
		for i in range(1, self.nFiles, 1):
			dfo.loc[rows,col] = dfo.loc[rows,col].add(self.objList[i].dataDF.loc[rows,col])
	 #--> Temporal dicts 
		tDict = dfo.loc[config.aadist['RD']]
		tDict = tDict.loc[tDict.loc[:,'AA'] != 'Pos']
		tDict = tDict.to_dict(orient='split')
		rDict = self.RunAnalysisHelper(tDict)
	 #--> aadist dict
		self.aadist = {}
		for k in self.objList[0].indKeys[0:-1]:
			tDict = dfo.loc[k]
			tDict = tDict.loc[tDict.loc[:,'AA'] != 'Pos']
			tDict = tDict.to_dict(orient='split')					
			eDict = self.RunAnalysisHelper(tDict)
			self.aadist[k] = eDict
			pos = dclasses.DataObjTarProtFile.AAdistDictChiComp(
				'bla', eDict, rDict, aVal=self.objList[0].aVal)
			self.aadist[k][config.aadist['Poskey']] = pos
	 #--> RD dict in aadist
		self.aadist[config.aadist['RD']] = rDict
		self.aadist[config.aadist['RD']][config.aadist['Poskey']] = (
			[0] * self.objList[0].nPos)
	 #--> Return
		return True		
	#---

	def RunAnalysisHelper(self, iDict):
		""" Fix the dict comming from the dataframe 
			iDict: initial dict (dict)
		"""
		oDict = {}
		for e in iDict['data']:
			oDict[e[0]] = e[1:]
		return oDict
	#---

	def WriteOF(self):
		""" """
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Writing output file: aadist file', 1)	
		#-->
		data = {
			'V' : config.dictVersion, 
			'CI': self.objList[0].Fdata['CI'],
			'R' : self.aadist,			
		}
		#-->
		dmethods.FFsWriteJSON(self.do['Outputfile'], data)
		#-->
		return True
	#---

	def ShowRes(self):
		""" Show the graphical output if any """
		gmethods.UpdateGaugeText(self.gauge, self.stProgress,
			'Generating graphical output', 1)
		gmethods.WinGraphResCreate(config.name['AAdistR'], 
				self.do['Outputfile'])	
		return True
	#---
#---












