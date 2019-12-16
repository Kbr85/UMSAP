# ------------------------------------------------------------------------------
#	Copyright (C) 2017-2019 Kenny Bravo Rodriguez <www.umsap.nl>
	
#	This program is distributed for free in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
	
#	See the accompaning licence for more details.
# ------------------------------------------------------------------------------


""" This module generates the menus of the app """


# ------------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Methods
# ------------------------------------------------------------------------------



#--- Imports
## Standard modules
import wx
import _thread
## My modules
import config.config as config
import gui.gui_methods as gmethods
#---



# -------------------------------------------------- Individual Tool menus
#---# Improve You can create a base class for the menu containing several
#---# methods that appears almost everywhere.
#---# Improve

class ToolMenuTypeResults(wx.Menu):
	""" Tool menu for the Type Results window """

	def __init__(self):
		""" """
		super().__init__()
	 #--> Menu items
		self.Append(501, 'Copy\tCtrl+C')
	 #--> Bind
		self.Bind(wx.EVT_MENU, self.OnLBoxCopy, id=501)
	#---

	####---- Methods of the class
	def OnLBoxCopy(self, event):
		""" Copy the colum numbers of selected rows to the clipboard """
		win = self.GetWindow()
		win.OnLBoxCopy()
		return True
	#---
#---

class ToolMenuCorrAMod(wx.Menu):
	""" Creates the tools menu for the correlation analysis window """
	
	def __init__(self):
		""" """
		super().__init__()
		####---- Menu items
		self.Append(502, 'Delete Selected')
		self.Append(501, 'Clear List')
		####---- Bind
		self.Bind(wx.EVT_MENU, self.OnClearL,      id=501)
		self.Bind(wx.EVT_MENU, self.OnDelSel,      id=502)
	#---

	####---- Methods of the class
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
#---

class ToolMenuCorrARes(wx.Menu):
	""" Creates the pop up menu in the correlation results window """
	
	def __init__(self):
		""" """
	 #--> Init
		super().__init__()
	 #--> Menu items
		self.Append(502, 'Export Data to:')
		for i in config.corr['MenuID'].keys():
			self.Append(int(i), config.corr['MenuID'][i])		
		self.AppendSeparator()
		self.Append(501, 'Save Plot Image')
	 #---> Bind
		self.Bind(wx.EVT_MENU, self.OnSavePlot, id=501)
		for i in config.corr['MenuID'].keys():
			self.Bind(wx.EVT_MENU, self.OnExport, id=int(i))
	#---

	####---- Methods of the class
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
#---

class ToolMenuProtProfResT(wx.Menu):
	""" Tools menu for ProtProfResT """

	def __init__(self, allL, grayC):
		""" allL  : Draw all protein lines
			grayC : Draw lines in gray or with different colors
		"""
		super().__init__()

		####---- Menu items
		self.Append(703, 'Show All',   kind=wx.ITEM_CHECK)
		self.AppendSeparator()
		self.Append(704, 'Same Color', kind=wx.ITEM_CHECK)
		self.AppendSeparator()
		self.Append(702, 'Save Plot Image')
		self.AppendSeparator()
		self.Append(701, 'Reset View')
		####---- Current
		self.CurrentState(allL, grayC)
		####---- Bind
		self.Bind(wx.EVT_MENU, self.OnReset,    id=701)
		self.Bind(wx.EVT_MENU, self.OnSavePlot, id=702)
		self.Bind(wx.EVT_MENU, self.OnAll,      id=703)
		self.Bind(wx.EVT_MENU, self.OnColor,    id=704)
	#---

	####---- Methods of the class
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
#---

class ToolMenuProtProfResFilter(wx.Menu):
	""" Tools menu to show filtered results in protprofRes """

	def __init__(self):
		""" """
		super().__init__()
		self.Append(800, 'None',      kind=wx.ITEM_RADIO)
		self.Append(800, 'Z score',   kind=wx.ITEM_RADIO)
		self.Append(801, 'Log2FC',    kind=wx.ITEM_RADIO)
		self.Append(802, 'Monotonic', kind=wx.ITEM_RADIO)
	#---
#---

class ToolMenuProtProfResV(wx.Menu):
	""" Tools menu for ProtProfResV """

	def __init__(self, nC, nt, lC, lt, n, tp):
		""" nC : number of conditions
			nt : number of relevant points per conditions 
			lC : conditions legends
			lt : relevant points legend
			n  : current selected condition 
			tp : current selected time point
		"""
		super().__init__()

	  ####---- Menu items
	  #--> Condition menu
		self.CondMenu = wx.Menu()
		j = 504
		for i in lC:
			self.CondMenu.Append(j, str(i), kind=wx.ITEM_RADIO)
			j += 1
	  #--> Relevant points menu
		self.TPMenu = wx.Menu()
		for i in lt:
			self.TPMenu.Append(j, str(i), kind=wx.ITEM_RADIO) 
			j += 1
	  #--> All together
		self.AppendSubMenu(self.CondMenu, 'Conditions')
		self.AppendSubMenu(self.TPMenu, 'Relevant Points')
		self.AppendSeparator()
		self.Append(503, 'Z score Threshold')
		self.AppendSeparator()
		self.Append(502, 'Save Plot Image')
		self.AppendSeparator()
		self.Append(501, 'Reset View')
	  ####---- Bind
		self.Bind(wx.EVT_MENU, self.OnReset,    id=501)
		self.Bind(wx.EVT_MENU, self.OnSavePlot, id=502)
		self.Bind(wx.EVT_MENU, self.OnZScore,   id=503)
		j = 504
		for i in range(0, nC, 1):
			self.CondMenu.Bind(wx.EVT_MENU, self.OnCond, id=j)
			j += 1
		for i in range(0, nt, 1):
			self.TPMenu.Bind(wx.EVT_MENU, self.OnTP, id=j)
			j += 1 
	  ####---- Current state
		self.CurrentState(nC, n, tp)		
	#---

	####---- Methods of the class
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
		self.CondMenu.Check(504+n, True)
		self.TPMenu.Check(504+nC+tp, True)
		return True
	#---
#---

class ToolMenuCutPropRes(wx.Menu):
	""" To show the pop up menu in CutPropRes """

	def __init__(self, nExp, seq, norm, exp, comp):
		""" nExp: Total number of experiments
			seq : 0 Rec Seq, 1 Nat Seq
			norm: 0 Reg Values, 1 Normalized Values
			exp : current experiment
			comp: experiment to compare to
		"""
		super().__init__()	
	  ####---- Menu items
	  #--> Experiment menu
		self.ExpMenu = wx.Menu()
		self.ExpMenu.Append(507, 'FP List', kind=wx.ITEM_RADIO)
		for i in range(1, nExp + 1, 1):
			self.Mid = 507 + i
			name = 'Experiment ' + str(i)
			self.ExpMenu.Append(self.Mid, name, kind=wx.ITEM_RADIO)
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
	  ####---- Check defaults
		self.CurrentState(nExp, seq, norm, exp, comp)
	  ####---- Bind
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

	####---- Methods of the class
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
#---

class ToolMenuHistoRes(wx.Menu):
	""" Add Tools menu to a HistoR window"""

	def __init__(self, seq, uni):
		""" seq: 0 Rec Seq, 1 Nat Seq
			uni: 0 All Cuts, 1 Unique Cuts 
		"""
		super().__init__()

	  ####---- Menu items
		self.Append(502, 'Native Sequence',      kind=wx.ITEM_RADIO)
		self.Append(503, 'Recombinant Sequence', kind=wx.ITEM_RADIO)
		self.AppendSeparator()
		self.Append(504, 'All cleavages',        kind=wx.ITEM_RADIO)
		self.Append(505, 'Unique cleavages',     kind=wx.ITEM_RADIO)
		self.AppendSeparator()
		self.Append(506, 'Save Plot Image')
		self.AppendSeparator()
		self.Append(501, 'Reset View')
	  ####---- Check defaults
		self.CurrentState(seq, uni)
	  ####---- Bind
		self.Bind(wx.EVT_MENU, self.OnReset,    id=501)
		self.Bind(wx.EVT_MENU, self.OnSeq,      id=502)
		self.Bind(wx.EVT_MENU, self.OnSeq,      id=503)
		self.Bind(wx.EVT_MENU, self.OnUni,      id=504)
		self.Bind(wx.EVT_MENU, self.OnUni,      id=505)
		self.Bind(wx.EVT_MENU, self.OnSavePlot, id=506)
	#---

	####---- Methods of the class
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
#---

class ToolMenuAAdistRes(wx.Menu):
	""" Pop Up menu in AAdistR """

	def __init__(self, exp, pos, nExp, nPosName):
		""" exp     : current experiment
			pos     : current position
			nExp    : total number of experiments
			nPosName: list with the positions label 
		"""
		super().__init__()

	  ####---- Menu items
	  #--> Experiment menu
		self.ExpMenu = wx.Menu()
		self.ExpMenu.Append(503, 'FP List', kind=wx.ITEM_RADIO)
		for i in range(1, nExp + 1, 1):
			self.Mid = 503 + i
			name = 'Experiment ' + str(i)
			self.ExpMenu.Append(self.Mid, name, kind=wx.ITEM_RADIO)
	  #---> Positions menu
		self.CompMenu = wx.Menu()
		tempID = self.Mid + 1
		self.CompMenu.Append(tempID, 'None', kind=wx.ITEM_RADIO)
		for i in nPosName:
			tempID = tempID + 1
			self.CompMenu.Append(tempID, str(i), kind=wx.ITEM_RADIO)			
	  #---- All together
		self.AppendSubMenu(self.ExpMenu, 'Experiments')
		self.AppendSubMenu(self.CompMenu, 'Compare Positions')
		self.AppendSeparator()
		self.Append(502, 'Save Plot Image')
		self.AppendSeparator()
		self.Append(501, 'Reset View')
	  ####---- Check defaults
		self.CurrentState(exp, pos)
	  ####---- Bind
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
		
	####---- Methods of the class
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
#---

class ToolMenuLimProtRes(wx.Menu):
	""" Tool menu in LimprotRes """

	def __init__(self, selM):
		""" selM: selection mode. True Select Lane, False Select Band """
		super().__init__()

	  ####---- Menu items
		self.Append(505, 'Lane Selection Mode\tCtrl+L', kind=wx.ITEM_CHECK)
		self.AppendSeparator()
		self.Append(504, 'Export Filtered Peptides')
		self.AppendSeparator()
		self.Append(503, 'Save Fragments Image')
		self.Append(502, 'Save Gel Image')
		self.AppendSeparator()
		self.Append(501, 'Reset View')
	  ####---- Bind
		self.Bind(wx.EVT_MENU, self.OnReset,    id=501)
		self.Bind(wx.EVT_MENU, self.OnSaveGel,  id=502)
		self.Bind(wx.EVT_MENU, self.OnSaveFrag, id=503)
		self.Bind(wx.EVT_MENU, self.OnExportFP, id=504)
		self.Bind(wx.EVT_MENU, self.OnSelM,     id=505)
	  ####---- Current Status
		if selM:
			self.Check(505, True)
		else:
			self.Check(505, False)
	#---
		
	####---- Methods of the class
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
#---

class ToolMenuTarProtRes(wx.Menu):
	""" Handles the pop up menu in tarprotR """	

	def __init__(self):
		""" """
		super().__init__()

	  ####---- Menu items
		self.Append(504, 'Export Filtered Peptides')
		self.AppendSeparator()
		self.Append(503, 'Save Fragments Image')
		self.Append(502, 'Save Plot Image')
		self.AppendSeparator()
		self.Append(501, 'Reset View')
	  ####---- Bind
		self.Bind(wx.EVT_MENU, self.OnReset,    id=501)
		self.Bind(wx.EVT_MENU, self.OnSavePlot, id=502)
		self.Bind(wx.EVT_MENU, self.OnSaveFrag, id=503)
		self.Bind(wx.EVT_MENU, self.OnExportFP, id=504)
	#---
		
	####---- Methods of the class
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
#---

class ToolMenuMergeAA(wx.Menu):
	""" Tools menu in mergeAA """	

	def __init__(self):
		super().__init__()

	  ####---- Menu items
		self.Append(501, 'Delete selected paths')
		self.Append(502, 'Delete all paths')
	  ####---- Bind
		self.Bind(wx.EVT_MENU, self.OnDelSel, id=501)
		self.Bind(wx.EVT_MENU, self.OnDelAll, id=502)
	#---

	####---- Methods of the class
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
#---

class ToolMenuTarProtMod(wx.Menu):
	""" Popup menu for the wx.ListCtrl in the TarProt module """
	
	def __init__(self):
		""" """
		super().__init__()
	  ####---- Menu items
		self.Append(100, 'Add selection to:')
		self.Append(101, 'Sequence')
		self.Append(102, 'Detected proteins')
		self.Append(103, 'Score')
		self.Append(104, 'Columns to extract')
		self.AppendSeparator()
		self.Append(105, 'Clear list')
		self.AppendSeparator()
		self.Append(106, 'Save input file')
	  ####---- Bind
		for i in range(101, 105, 1):
			self.Bind(wx.EVT_MENU, self.OnButton, id=i)
		self.Bind(wx.EVT_MENU, self.OnClear,      id=105)
		self.Bind(wx.EVT_MENU, self.OnSaveInputF, id=106)
	#---

	####---- Methods of the class
	def OnButton(self, event):
		""" Get the id of the menu item triggering the add to event and send it
			to main method 
		"""
		win = self.GetWindow()
		MId = event.GetId()
		win.AddFromList(MId)
		return True		
	#---

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
#---

class ToolMenuProtProfMod(ToolMenuTarProtMod):
	""" Tool menu for the ProtProf """

	def __init__(self):
		""" """
		super().__init__()
	  
	  ####---- Destroy old items
		for i in self.GetMenuItems():
			self.DestroyItem(i)
	  ####---- Creates the one needed 
		self.Append(100, 'Add selection to:')
		self.Append(101, 'Detected proteins')
		self.Append(102, 'Gene names')
		self.Append(103, 'Score')
		self.Append(104, 'Exclude proteins')
		self.Append(105, 'Columns to extract')
		self.AppendSeparator()
		self.Append(106, 'Clear list')
		self.AppendSeparator()
		self.Append(107, 'Save input file')
	  ####---- Bind
		for i in range(101, 106, 1):
			self.Bind(wx.EVT_MENU, self.OnButton, id=i)
		self.Bind(wx.EVT_MENU, self.OnClear,      id=106)
		self.Bind(wx.EVT_MENU, self.OnSaveInputF, id=107)
	#---
#---

class ToolMenuLimProtMod(ToolMenuTarProtMod):
	""" To handel tool and pop up menu in LimProt module """

	def __init__(self):
		""" """
		super().__init__()
	#---
#---
# -------------------------------------------------- Individual Tool menus (END)



#--------------------------------------------------------------- Menu Bars
class MainMenuBar(wx.MenuBar):
	""" Creates the application main menu bar. ids with 500s, 700s, 800s are 
		reserved for the optional Tools entries in the derived classes. Usually
		Tools has a submenus with the 500s, 700s, 800s id associated to each
		submenu.
	"""
	
	def __init__(self):
		""" """
		super().__init__()
	  ####---- Menu items
	  #--> Modules
		Modmenu = wx.Menu()
		Modmenu.Append(102, 'Limited Proteolysis\tALT+Ctrl+L')
		Modmenu.Append(104, 'Proteome Profiling\tALT+Ctrl+P')
		Modmenu.Append(101, 'Targeted Proteolysis\tALT+Ctrl+T')
		Modmenu.AppendSeparator()
		Modmenu.Append(103, 'Utilities\tALT+Ctrl+U')
	  #--> Utilities
		LimProtMenu = wx.Menu()
		LimProtMenu.Append(214, 'Sequence Highlight')
		TarProtmenu = wx.Menu()
		TarProtmenu.Append(201, 'AA Distribution')
		TarProtmenu.Append(202, 'Cleavages per Residue')
		TarProtmenu.Append(208, 'Cleavages to PDB Files')
		TarProtmenu.Append(213, 'Filtered Peptide List')
		TarProtmenu.Append(203, 'Histograms')
		TarProtmenu.Append(204, 'Sequence Alignments')
		TarProtmenu.AppendSeparator()
		TarProtmenu.Append(210, 'Update Results')
		TarProtmenu.Append(211, 'Custom Update of Results')
		Genmenu = wx.Menu()
		Genmenu.Append(206, 'Correlation Analysis')
		Genmenu.Append(212, 'Create Input File')
		Genmenu.Append(209, 'Merge aadist Files')
		Genmenu.Append(205, 'Short Data Files')
		Utilmenu = wx.Menu()
		Utilmenu.AppendSubMenu(LimProtMenu, 'Limited Proteolysis')
		Utilmenu.AppendSubMenu(TarProtmenu, 'Targeted Proteolysis')
		Utilmenu.AppendSubMenu(Genmenu, 'General Utilities')
		Utilmenu.AppendSeparator()
		Utilmenu.Append(207, 'Read Output File\tCtrl+R')		
	  #--> Help
		Helpmenu = wx.Menu()
		Helpmenu.Append(301, 'Manual')
		Helpmenu.Append(302, 'Tutorials')
		if config.cOS == 'Darwin':
			Helpmenu.Append(wx.ID_ABOUT, 'About UMSAP')
		else:
			pass
		Helpmenu.AppendSeparator()
		Helpmenu.Append(303, 'Check for Updates')
		if config.cOS != 'Darwin':
			Helpmenu.AppendSeparator()
		else:
			pass
		Helpmenu.Append(wx.ID_PREFERENCES, 'Preferences')
	  #--> Script
		Scriptmenu = wx.Menu()
		Scriptmenu.Append(601, 'Run Input File\tCtrl+I')
	  #--> UMSAP menu in Win/Linux/Mac
		if config.cOS == 'Windows':
			UMSAPmenu = wx.Menu()
			UMSAPmenu.Append(403, 'About UMSAP')
			UMSAPmenu.AppendSeparator()
			UMSAPmenu.Append(401, 'Minimize All\tCtrl+M')
			UMSAPmenu.Append(402, 'Quit UMSAP\tCtrl+Q')
		elif config.cOS == 'Linux':
			UMSAPmenu = wx.Menu()
			UMSAPmenu.Append(403, 'About UMSAP')
			UMSAPmenu.AppendSeparator()
			UMSAPmenu.Append(401, 'Minimize All\tCtrl+M')
			UMSAPmenu.Append(402, 'Quit UMSAP\tCtrl+Q')			
		else:
			pass
	  ####---- Append to menubar
		if config.cOS == 'Windows':
			self.Append(UMSAPmenu, '&UMSAP')
		elif config.cOS == 'Linux':
			self.Append(UMSAPmenu, '&UMSAP')
		else:
			pass
		self.Append(Modmenu,    '&Module')
		self.Append(Utilmenu,   '&Utilites')
		self.Append(Helpmenu,   '&Help')
		self.Append(Scriptmenu, '&Script')
	  ####---- Bind
	  #--> 100
		self.Bind(wx.EVT_MENU, self.OnTarProt,         id=101)
		self.Bind(wx.EVT_MENU, self.OnLimProt,         id=102)
		self.Bind(wx.EVT_MENU, self.OnUtil,            id=103)
		self.Bind(wx.EVT_MENU, self.OnProtProf,        id=104)
	  #--> 200
		self.Bind(wx.EVT_MENU, self.OnAAdist,          id=201)
		self.Bind(wx.EVT_MENU, self.OnCutProp,         id=202)
		self.Bind(wx.EVT_MENU, self.OnHisto,           id=203)
		self.Bind(wx.EVT_MENU, self.OnSeqAlign,        id=204)
		self.Bind(wx.EVT_MENU, self.OnShortDFiles,     id=205)
		self.Bind(wx.EVT_MENU, self.OnCorrAnalysis,    id=206)
		self.Bind(wx.EVT_MENU, self.OnReadOutFile,     id=207)
		self.Bind(wx.EVT_MENU, self.OnPDBfiles,        id=208)
		self.Bind(wx.EVT_MENU, self.OnMergeAadist,     id=209)
		self.Bind(wx.EVT_MENU, self.OnUpdateTP,        id=210)
		self.Bind(wx.EVT_MENU, self.OnReanalyseTP,     id=211)
		self.Bind(wx.EVT_MENU, self.OnCInputFile,      id=212)
		self.Bind(wx.EVT_MENU, self.OnFPList,          id=213)
		self.Bind(wx.EVT_MENU, self.OnSeqH,            id=214)
	  #--> 300
		self.Bind(wx.EVT_MENU, self.OnHelpManual,      id=301)
		self.Bind(wx.EVT_MENU, self.OnHelpTutorials,   id=302)
		self.Bind(wx.EVT_MENU, self.OnCheckUpdate,     id=303)
		self.Bind(wx.EVT_MENU, self.OnPreferences,     id=wx.ID_PREFERENCES)		
	  #--> 400
		if config.cOS == 'Darwin':
			self.Bind(wx.EVT_MENU, self.OnAbout,       id=wx.ID_ABOUT)
		elif config.cOS == 'Windows':
			self.Bind(wx.EVT_MENU, self.OnMinimizeAll, id=401)
			self.Bind(wx.EVT_MENU, self.OnQuitUMSAP,   id=402)
			self.Bind(wx.EVT_MENU, self.OnAbout,       id=403)
		elif config.cOS == 'Linux':
			self.Bind(wx.EVT_MENU, self.OnMinimizeAll, id=401)
			self.Bind(wx.EVT_MENU, self.OnQuitUMSAP,   id=402)
			self.Bind(wx.EVT_MENU, self.OnAbout,       id=403)
		else:
			pass
	  #--> 600
		self.Bind(wx.EVT_MENU, self.OnRInputFile,      id=601)
	#---

	####---- Methods of the class
	#--> 100
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

	def OnLimProt(self, event):
		""" Creates the Limited Proteolysis module """
		gmethods.WinMUCreate(config.name['LimProt'])
		return True
	#---

	def OnUtil(self, event):
		""" Creates the Utilities window """
		gmethods.WinMUCreate(config.name['Util'])
		return True
	#---

	#--> 200
	def OnSeqH(self, event):
		""" Sequence highlight window for LimProt """
		gmethods.WinMUCreate(config.name['SeqH'])
		return True
	#---

	def OnMergeAadist(self, event):
		""" Merge aadist files util window """
		gmethods.WinMUCreate(config.name['MergeAA'])
		return True
	#---

	def OnShortDFiles(self, event):
		""" Window to create the short data files from a module main output file
		"""
		gmethods.WinMUCreate(config.name['ShortDFile'])
		return True
	#---

	def OnPDBfiles(self, event):
		""" Window to map the cleavage per residue to a pdb file from a tarprot 
			file 
		"""
		gmethods.WinMUCreate(config.name['Cuts2PDB'])	
		return True
	#---

	def OnAAdist(self, event):
		""" Window to get the aa distribution files from a tarprot file """
		gmethods.WinMUCreate(config.name['AAdist'])	
		return True
	#---

	def OnHisto(self, event):
		""" Window to get the histogram files from a tarprot file """
		gmethods.WinMUCreate(config.name['Histo'])	
		return True
	#---

	def OnSeqAlign(self, event):
		""" Window to get the sequence alignments files from a tarprot file """
		gmethods.WinMUCreate(config.name['SeqAlign'])	
		return True
	#---

	def OnCorrAnalysis(self, event):
		""" Creates the correlation analysis window """
		gmethods.WinMUCreate(config.name['CorrA'])	
		return True
	#---

	def OnReanalyseTP(self, event):
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

	def OnUpdateTP(self, event):
		""" Reads a .tarprot file and creates all the associated files """
		if gmethods.MenuOnUpdateTP():
			return True
		else:
			return False
	#---

	def OnFPList(self, event):
		""" Reads a .tarprot file and creates a .filtpept file """	
		if gmethods.MenuOnFPList():
			return True
		else:
			return False
	#---

	def OnCInputFile(self, event):
		""" Reads a .tarprot file and creates a .uscr file """	
		if gmethods.MenuOnCInputFile():
			return True
		else:
			return False
	#---

	def OnCutProp(self, event):
		""" Creates the .cutprop file from a .tarprot file """
		if gmethods.MenuOnCutProp():
			return True
		else:
			return False
	#---

	def OnReadOutFile(self, event):
		""" Read a file generated by UMSAP """
		if gmethods.MenuOnReadOutFile():
			return True
		else:
			return False
	#---

	#--> 300
	def OnHelpManual(self, event):
		""" Shows the manual with the default pdfviewer in the system """
		if gmethods.MenuOnHelpManual():
			return True
		else:
			return False
	#---

	def OnHelpTutorials(self, event):
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

	#--> 400
	def OnAbout(self, event):
		""" Show the about window """
		gmethods.WinMUCreate(config.name['About'])
		return True
	#---	

	def OnMinimizeAll(self, event):
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

	#--> 600
	def OnRInputFile(self, event):
		""" Run the script """
		if gmethods.MenuOnRInputFile():
			return True
		else:
			return False
	#---
#---

class MainMenuBarWithTools(MainMenuBar):
	""" To add a Tools menu to the menubar for specific windows """

	def __init__(self, name, *args):
		""" name: Name of the window """
		super().__init__()
	  
	  ####---- Menu items
		if len(args) == 0:
			ToolsMenu = config.pointer['menu']['toolmenu'][name]()
		else:
			ToolsMenu = config.pointer['menu']['toolmenu'][name](*args)
	  ####---- Append to menu bar
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

class MenuBarProtProfRes(MainMenuBar):
	""" Tools for ProtProfResV """
	
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

	 ####---- Menu items
		self.VolcanoPlotMenu  = ToolMenuProtProfResV(nC, nt, lC, lt, n, tp)
		self.TimeAnalysisMenu = ToolMenuProtProfResT(allL, grayC)
		self.FilterMenu       = ToolMenuProtProfResFilter()
		self.ToolsMenu = wx.Menu()
		self.ToolsMenu.AppendSubMenu(self.VolcanoPlotMenu, 'Volcano Plot')
		self.ToolsMenu.AppendSeparator()
		self.ToolsMenu.AppendSubMenu(self.TimeAnalysisMenu, 'Time Analysis')
		self.ToolsMenu.AppendSeparator()
		self.ToolsMenu.AppendSubMenu(self.FilterMenu, 'Filtered Results')
		self.ToolsMenu.AppendSeparator()
		self.ToolsMenu.AppendCheckItem(599, 'Corrected P values')
	 ####---- Append to menu bar
		if config.cOS == 'Darwin':
			self.Insert(2, self.ToolsMenu, '&Tools')
		elif config.cOS == 'Windows':
			self.Insert(3, self.ToolsMenu, '&Tools')
		elif config.cOS == 'Linux':
			self.Insert(3, self.ToolsMenu, '&Tools')
		else:
			pass
	 ####---- Bind
		self.Bind(wx.EVT_MENU, self.OnCorrP, id=599)
	#---

	####---- Methods of the class
	def OnCorrP(self, event):
		""" Show corrected P values """
		win = self.GetFrame()
		win.OnCorrP()
		return True 
	#---
#---
#--------------------------------------------------------------- Menu Bars (END)
