# ------------------------------------------------------------------------------
# 	Copyright (C) 2017 Kenny Bravo Rodriguez <www.umsap.nl>

# 	This program is distributed for free in the hope that it will be useful,
# 	but WITHOUT ANY WARRANTY; without even the implied warranty of
# 	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

# 	See the accompaning licence for more details.
# ------------------------------------------------------------------------------

""" Creates the window showing the results for a .protprof file """

#region -------------------------------------------------------------- Imports
import matplotlib.patches as mpatches
import pandas as pd
import wx
from pathlib import Path
from scipy   import stats

import config.config		  as config
import checks.checks_multiple as checkM
import checks.checks_single   as checkS
import data.data_methods	  as dmethods
import gui.gui_classes		  as gclasses
import gui.gui_methods		  as gmethods
import gui.menu.menu		  as menu
#endregion ----------------------------------------------------------- Imports

class WinProtProfRes(gclasses.WinResDosDos):
	""" To show the results in a protprof file """

	#region --------------------------------------------------- Instance Setup
	def __init__(self, file):
		""" file: path to the protprof file """
		#region ------------------------------------------------ Initial setup
		self.name = config.name["ProtProfRes"]
		self.fileP = Path(file)
		try:
			super().__init__(self, parent=None)
		except Exception:
			raise ValueError("")
		#endregion --------------------------------------------- Initial setup
		
		#region ---------------------------------------------------- Variables
		self.NC                  = self.fileObj.nConds
		self.data                = self.fileObj.dataFrame
		self.data_filtered       = None
		self.start               = True
		self.TP                  = self.fileObj.timeP
		self.NP                  = self.fileObj.NProt
		self.colors              = dmethods.GetColors(self.NC)
		self.colorsL             = dmethods.GetColors(self.NC, "L")
		self.loga                = self.fileObj.loga
		self.aVal                = self.fileObj.aVal
		self.P                   = False
		self.xCoordTimeA         = self.fileObj.xCoordTimeA
		self.ZscoreVal           = self.fileObj.ZscoreVal
		self.ZscoreValP          = self.fileObj.ZscoreValP
		self.ZscoreValD          = self.fileObj.ZscoreVal
		self.ZscoreValDP         = self.fileObj.ZscoreValP
		self.NCondL              = self.fileObj.nCondsL
		self.NTimePL             = self.fileObj.nTimePL
		self.XaxisLabel          = [self.fileObj.ControlLabel] + self.NTimePL
		self.ControlLabel        = self.fileObj.ControlLabel
		self.CType               = self.fileObj.CType
		self.Xv                  = self.fileObj.Xv
		self.Yv                  = self.fileObj.Yv
		#---
		self.n  = 0
		self.tp = 0
		#---
		self.grayC      = False
		self.allL       = False
		self.prot       = False
		self.legendShow = False
		self.CorrP      = False
		self.pP         = config.protprof['ColOut'][1]
		self.pPt        = config.protprof['ColTPp'][0]
		self.PoPc       = config.protprof['ColOut'][0]
		#--- filter methods
		self.filter_method = {
			'Filter_ZScore'   : self.OnFilter_ZScore_Run,
			'Filter_Log2FC'   : self.OnFilter_Log2FC_Run,
			'Filter_P'        : self.OnFilter_P_Run,
			'Filter_Monotonic': self.OnFilter_Monotonic,
			'Filter_Divergent': self.OnFilter_Divergent,
		}
		self.filter_userInput = {
			'Filter_ZScore': config.msg['FilteredValues']['Examples']['Filter_ZScore'],
			'Filter_Log2FC': config.msg['FilteredValues']['Examples']['Filter_Log2FC'],
			'Filter_P'     : config.msg['FilteredValues']['Examples']['Filter_P'],
		}
		self.filter_steps = { # Keys are meaningless, values are:
			# (method_key, method_print, comp, num, (options))
			# ('Filter_P', 'P values'  , comp, num, (lopP, corrP))
		}
		self.col4Export = self.fileObj.col4Export
		#endregion ------------------------------------------------- Variables
	
		#region --------------------------------------------------------- Menu
		self.menubar = menu.MenuBarProtProfRes(
			self.NC,
			self.TP,
			self.NCondL, 
			self.NTimePL, 
			self.n, 
			self.tp, 
			self.allL, 
			self.grayC
		)		
		self.SetMenuBar(self.menubar)
		#endregion ------------------------------------------------------ Menu
		
		#region ------------------------------------------------------ Widgets
		#--> Line
		self.lineHI10 = wx.StaticLine(self.panel)
	  	#--> TextCtrl
		#--> Size for the TextCtrl # Minimum supported screen height 900 px IMPROVED
		h = config.size['Screen'][1] + config.size['TaskBarHeight'] - 650
		if h > config.size['TextCtrl'][self.name]['TextPanel'][1]:
			size = config.size['TextCtrl'][self.name]['TextPanel']
		else:
			h = 230
			size = (config.size['TextCtrl'][self.name]['TextPanel'][0], h)
		#---
		#--> TextCtrl
		self.tcText = wx.TextCtrl(self.panel, 
			size=size, 
			style=wx.BORDER_SIMPLE|wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
		self.tcText.SetFont(config.font[config.name['TarProtRes']])
		#---
	  	#--> Split statusbar
		self.statusbar.SetFieldsCount(number=2, widths=[100, -1])
	  	#---
		#endregion --------------------------------------------------- Widgets

		#region ------------------------------------------------------- Sizers
		#--> Add
		self.sizerIN.Add(self.lineHI10, pos=(1,2), border=2, span=(0,3),
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerIN.Add(self.tcText,   pos=(2,2), border=2, span=(0,3),
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		#--> Modify span
		self.sizerIN.SetItemSpan(self.sizerLB,  (3,0))
		self.sizerIN.SetItemSpan(self.lineVI10, (3,0))
		#--> Fit
		self.sizer.Fit(self)
		#--> Add Grow
		self.sizerIN.AddGrowableCol(0, 1)
		self.sizerIN.AddGrowableRow(2, 1)
		#endregion ---------------------------------------------------- Sizers

		#--> Positions and minimal size
		self.WinPos()
		gmethods.MinSize(self)
		
		#--> Binding
		self.p3.canvas.mpl_connect("button_press_event", self.OnClick3)
		#---
		self.p2.canvas.mpl_connect("button_press_event", self.OnClick2)
		self.p2.canvas.mpl_connect("pick_event", self.OnPick2)
		
		#--> Draw
		self.DrawConfig2()
		self.DrawConfig3()
		
		#--> Show
		self.Show()
	#---
	#endregion ------------------------------------------------ Instance Setup

	#region ---------------------------------------------------------- General
	def WinPos(self):
		""" Set the position of a new window depending on the number of same
		windows already open """
	 #--> Variables
		xw, yw = self.GetSize()
		xo, yo = config.coord["TopXY"]
		xo = config.size["Screen"][0] - xw
		x = ( xo - config.protprof["ExtraX_V"]
			- config.win["ProtProfResNum"] * config.win["DeltaNewWin"])
		y = yo + config.win["ProtProfResNum"] * config.win["DeltaNewWin"]
	 #--> Set
		self.SetPosition(pt=(x, y))
	 #--> Adjust number of created windows
		config.win["ProtProfResNum"] = config.win["ProtProfResNum"] + 1
	 #--> Return
		return True
	#---

	def FilterDataRedraw(self, data=None):
		""" Redraw the window data after filtering the initial data 
			---
			data: df already filtered
		"""
	 
	 #--> Update listbox
		self.FillListBox(df=data)
	 #---
	 #--> Redraw volcano plot
		self.DrawConfig2(df=data)
	 #---
	 #--> Redraw point analysis
		self.DrawConfig3()
	 #---
	 #--> Empty Text
		self.tcText.Clear()		
	 #---
	 #--> Return
		return (True)
	 #---
	#---
	#endregion --------------------------------------------------------- General

	#region ---------------------------------------------------------- Binding
	def OnPick2(self, event):
		""" """
		ind = event.ind
		if len(ind) == 1:
			self.lb.Select(ind[0], on=1)
			self.lb.EnsureVisible(ind)
			self.lb.SetFocus()
		return True
	#---

	def OnPick3(self, event):
		""" """
		ind = self.p3.axes.lines.index(event.artist)
		lind = ind - (ind // self.NP) * self.NP
		self.lb.Select(lind, on=1)
		self.lb.EnsureVisible(lind)
		self.lb.SetFocus()
		return True
	#---

	def OnClick2(self, event):
		""" To process click events """
		if event.button == 3:
	 #-->			
			Tmenu = menu.ToolMenuProtProfResV(
				self.NC, 
				self.TP, 
				self.NCondL,
				self.NTimePL,
				self.n, 
				self.tp)
	 #--> Submenus in pop up menu do not work on Windows
			if config.cOS == 'Windows':
				for i in ['Conditions', 'Relevant Points']:
					Tmenu.DestroyItem(Tmenu.FindItem(i))
			else:
				pass
	 #-->
			self.PopupMenu(Tmenu)
		else:
			pass
		return True
	#---

	def OnClick3(self, event):
		""" To process click events """
		if event.button == 3:
			self.PopupMenu(menu.ToolMenuProtProfResT(self.allL, self.grayC))
		else:
			pass
		return True
	#---   

	def OnListSelect(self, event):
		""" """
	 #--> Draw tp
		self.prot = gmethods.ListCtrlGetColVal(self.lb, col=2, t="str")[0]
		self.DrawConfig3()
	 #--> Draw volcano
		dfP = dmethods.DFColValFilter(self.data, self.prot, 1)[1]
		if self.CType == config.combobox['ControlType'][1]:
			x = dfP[('v', 'X'+str(self.tp+1), "Y"+str(self.n+1), "log2FC")]
			y = dfP[('v', 'X'+str(self.tp+1), "Y"+str(self.n+1), self.pP)]
			
		else:
			x = dfP[('v', 'X'+str(self.n+1), "Y"+str(self.tp+1), "log2FC")]
			y = dfP[('v', 'X'+str(self.n+1), "Y"+str(self.tp+1), self.pP)]		   
		c = config.colors[self.name]["Green"]
		if self.P == False:
			pass
		else:
			self.P.remove()
			self.p2.canvas.draw()
		self.P = self.p2.axes.scatter(
			x, 
			y, 
			color=c, 
			alpha=1, 
			edgecolors="black", 
			linewidths=1, 
			picker=True
		)
		self.p2.canvas.draw()
	 #--> Show text in self.tcText
		self.ShowText(dfP)
	 #--> Return
		return True
	#---

	def OnRightDown(self, event):
		""" Display the popup menu. In this case the list box and search will
		not display anything because is way to messy to have the volcano and
		time menu in a pop menu """
		return True
	#---

	def OnPopUpMenu(self, event):
		""" Show the pop up menu in the wx.ListCtrl. Binding is done in
		 the base class """
		self.PopupMenu(menu.ToolMenuProtProfResFilter())
		return True
	#---
	#endregion ------------------------------------------------------- Binding

    #region ------------------------------------------------------------- Menu
	def OnReset(self, keepState=False):
		""" Reset view 
			---
			keepState: booleans to prevent changing condition and time point 
			when called from OnFilter_Remove
		"""
		self.grayC = False
		self.allL  = False
		self.prot  = False
		#---
		if keepState:
			pass
		else:
			self.n  = 0
			self.tp = 0
		#---
		self.menubar.Check(703, False)
		self.menubar.Check(704, False)
		self.menubar.Check(505, True)
		self.menubar.Check(505 + self.NC, True)
		#--- Reset listbox
		gmethods.ListCtrlDeSelAll(self.lb)
		#--- Reset Z score
		self.ZscoreValD  = self.ZscoreVal
		self.ZscoreValDP = self.ZscoreValP
		#--- Reset data_filtered
		self.data_filtered = None
		#--- Reset filter_steps
		self.filter_steps = {}
		#--- Reset listbox
		self.FillListBox()
		#--- Reset p2 and p3 panel
		self.DrawConfig3()
		self.DrawConfig2()
		#--- Reset SearchCtrl
		self.search.Clear()
		#--- Reset TextCtrl
		self.tcText.Clear() 
		#--- StatusBar
		self.statusbar.SetStatusText('', 1)
		#---
		self.Refresh()
		self.Update()
		#---
		return True
	#---

	def OnCond(self, Mid):
		""" Mid: Id of the selected menu item (int) """
		self.n = Mid - 505
		self.menubar.Check(Mid, True)
		self.DrawConfig2()
		if len(gmethods.ListCtrlGetSelected(self.lb)) > 0:
			self.OnListSelect('event')
		else:
			pass
		return True
	#---

	def OnTP(self, Mid):
		""" Mid: Id of the selected menu item """
		self.tp = Mid - (505 + self.NC)
		self.menubar.Check(Mid, True)
		self.DrawConfig2()
		if len(gmethods.ListCtrlGetSelected(self.lb)) > 0:
			self.OnListSelect('event')
		else:
			pass		
		return True
	#---

	def OnAll(self):
		""" """
		if self.allL == True:
			self.allL = False
		else:
			self.allL = True
		#-->
		if self.allL:
			self.p3.canvas.mpl_connect("pick_event", self.OnPick3)
		else:
			self.p3.canvas.mpl_disconnect("pick_event")
		#-->
		self.menubar.Check(703, self.allL)
		#-->
		self.DrawConfig3()
		#-->
		return True
	#---

	def OnColor(self):
		""" """
		if self.grayC == True:
			self.grayC = False
		else:
			self.grayC = True
		#-->
		self.menubar.Check(704, self.grayC)
		#-->
		self.DrawConfig3()
		#-->
		return True
	#---

	def OnZScore(self):
		""" Set a new Z score threshold """
	 #--> Create dlg
		dlg = gclasses.DlgTextInput(self, 
			config.msg['TextInput']['msg']['ZScoreThreshold'],
			value=str(self.ZscoreValDP),
			caption=config.msg['TextInput']['caption']['ZScoreThreshold'],
		)
	 #--> Show 
		if dlg.ShowModal() == wx.ID_OK:
	 #--> Get & Check value
			num = dlg.GetValue()
			out, newZ = checkM.CheckMNumberComp(num, val2=100)
	 #--> Redraw
			if out:
	  #--> Update Z score
				self.ZscoreValDP = newZ
				self.ZscoreValD = stats.norm.ppf(1 - newZ/100)
				self.DrawConfig2()
	  #--> ListSelect
				if len(gmethods.ListCtrlGetSelected(self.lb)) > 0:
					self.OnListSelect('event')
				else:
					pass
			else:
				pass
		else:
			pass
	 #--> Destroy & Return
		dlg.Destroy()
		return True
	#---

	def OnCorrP(self):
		""" Show corrected P values """
	 #--> Menu options
		if self.CorrP:
			self.CorrP = False
			self.pP	= config.protprof['ColOut'][1]
			self.pPt   = config.protprof['ColTPp'][0]
			self.PoPc  = config.protprof['ColOut'][0]
		else:
			self.CorrP = True
			self.pP	= config.protprof['ColOut'][3]
			self.pPt   = config.protprof['ColTPp'][1]
			self.PoPc  = config.protprof['ColOut'][2]
		self.menubar.Check(599, self.CorrP)
	 #--> Draw 
		if len(gmethods.ListCtrlGetSelected(self.lb)) > 0:
			self.DrawConfig2()
			self.OnListSelect('event')
		else:
			self.DrawConfig2()
	 #--> Return
		return True
	#---
	#endregion ---------------------------------------------------------- Menu

	#region ----------------------------------------------------------- Checks
	def Check_TP(self):
		""" Check number of time points is greater than 1"""
		if self.TP > 1:
			return True
		else:
			msg = config.msg['Errors']['TimePoint_Number'] 
			gclasses.DlgWarningOk(msg, nothing=True)
			return False
	#---

	def Check_NC(self):
		""" Check number of conditions is greater than 1 """
		if self.NC > 1:
			return True
		else:
			msg = config.msg['Errors']['Conditions_Number'] 
			gclasses.DlgWarningOk(msg, nothing=True)
			return False
	#---

	def Check_AppliedFilters(self):
		""" Check that there are at least one filter already applied """
		if len(self.filter_steps) > 0:
			return True
		else:
			msg = config.msg['Errors']['No_Filters'] 
			gclasses.DlgWarningOk(msg, nothing=True)
			return False
	#endregion -------------------------------------------------------- Checks

	#region ---------------------------------------------------------- Filters
	def OnFilter_Data(self):
		""" Set the data to be filter. It also set self.prot to False because
			there is no warranty that the selected protein would be available 
			after filtering
		"""
	 #--> Set self.prot
		self.prot = False
	 #---
	 #--> Set data frame & Return
		if self.data_filtered is None:
			return self.data
		else:
			return self.data_filtered
	 #---
	#---

	def OnFilter_Data_Divergent(self, data):
		""" Add the control columns to the data DF 
			---
			data: DF with the values
			---
			Returns a DF with the control columns added at the begining
		"""
	 #--> Insert control columns
		for k in range(1, self.NC+1, 1):
			idx = pd.IndexSlice
			if self.CType == config.combobox['ControlType'][1]:
				col = idx['Control', 'Control', 'Y'+str(k), 'log2FC']
			else:
				col = idx['Control', 'X'+str(k), 'Control', 'log2FC']
			data.insert(0, col, 0)
	 #---
	 #--> Return
		return data
	 #---
	#---

	def OnFilter_CondTimeP(self):
		""" Return the current condition and time point as needed for the 
			pd.IndexSlice. Here pd.IndexSlice is [a, b, c, d]. Condition and 
			time points are terms b and c depending on the control type used
		"""
	 #--> Set b & c
		if self.CType == config.combobox['ControlType'][1]:
			b = 'X'+str(self.tp+1)
			c = "Y" + str(self.n+1)
		else:
			b = 'X'+str(self.n+1)
			c = "Y" + str(self.tp+1)
	 #---
	 #--> Return
		return (b, c) 
	#---

	def OnFilter_StatusBarText(self, newText):
		""" Set the text in the status bar 
			---
			newText: text to add
		"""
	 #--> Get the current text
		text_now = self.statusbar.GetStatusText(1)
	 #---
	 #--> Set the new one
		text_new = text_now + '| ' + newText + ' '
	 #---
	 #--> Set
		self.statusbar.SetStatusText(text_new, 1)
	 #---
	 #--> Return
		return True
	 #---
	#---

	def OnFilter_Apply(self, filterDict=None):
		""" Apply filter to new condition - time point 
			filter: dict used when the method is call from OnFilter_Remove
		"""
	 #--> First reset self.data_filtered
		self.data_filtered = None
	 #---
	 #--> Set filter dict
		if filterDict is None:
			myFilter = self.filter_steps
		else:
			myFilter = filterDict
			self.statusbar.SetStatusText("", 1) # The number of filters changed
			self.filter_steps = {} # This needs to be filled again
	 #--> Apply filters
		for k, i in myFilter.items():
			method = i[0]
			options = i[2:]
			if filterDict is None:
				self.filter_method[method](*options, addStep=False)
			else:
				self.filter_method[method](*options)
	 #---
	 #--> Redraw
		self.FilterDataRedraw(self.data_filtered)
	 #---
	 #--> Return
		return True
	 #---
	#---

	def OnFilter_GUI(self, filterMethod):
		""" Creates the GUI for user input and call the run method 
			---
			filterMethod: key to id the method to apply (string) e.g. keys in
				self.filter_method
		"""
	 #--> Create dlg
		dlg = gclasses.DlgTextInput(self, 
			config.msg['TextInput']['msg'][filterMethod],
			value=self.filter_userInput[filterMethod],
			caption=config.msg['TextInput']['caption'][filterMethod],
		)
	 #--> Show & Process answer 
		if dlg.ShowModal() == wx.ID_OK:
	 	 #--> Get value
			val = dlg.GetValue()
	 	 #--> Process value
			self.filter_method[filterMethod](val)
		else:
			pass
	 #--> Destroy & Return
		dlg.Destroy()
		return True		
	#---

	def OnFilter_P_GUI(self):
		""""""
	 #--> Create dialog and show it
		dlg = gclasses.DlgFilterPvalues(
			self, 
			title=config.msg['TextInput']['caption']['Filter_P'],
		)
		dlg.CenterOnParent() 
	 #---
	 #--> Proccess answer
		if dlg.ShowModal() == wx.ID_OK:
		 #--> Get values and call Run method
			val   = dlg.tcText.GetValue()
			logP  = dlg.cbLogP.GetValue()
			corrP = dlg.cbCorrP.GetValue()
			self.OnFilter_P_Run(val, logP, corrP)			
		 #---
		else:
			pass
	 #---
	 #--> Destroy & Return
		dlg.Destroy()
		return True
	 #---
	#---

	def OnFilter_None(self):
		""" Reset all filter """
		self.OnReset(keepState=True)
	#---

	def OnFilter_ZScore_Run(self, val, addStep=True):
		""" Filter the results by Z score.
			---
			val: string with format < 10 or > 10
		"""
	 #--> Check user input
		out, num, comp = checkM.CheckMFilterByZscore(val)
		if out:
			pass
		else:
			gclasses.DlgWarningOk(config.msg['Errors']['Filter_ZScore'])
			return False
	 #---
	 #--> Get z score value
		zVal = stats.norm.ppf(1 - num/100)
	 #---
	 #--> Set data
		data = self.OnFilter_Data()
		b, c = self.OnFilter_CondTimeP()
	 #---
	 #--> Filter dataframe
		idx = pd.IndexSlice
		col = idx[:,b,c,'zFC']
		if comp == 'le':
			self.data_filtered = data[((data.loc[:,col] >= zVal) | (data.loc[:,col] <= -zVal)).any(axis=1)]
		elif comp == 'ge':
			self.data_filtered = data[((data.loc[:,col] <= zVal) & (data.loc[:,col] >= -zVal)).any(axis=1)]
	 #---
	 #--> Update GUI, filter_steps & StatusBar
		if addStep:
			self.FilterDataRedraw(self.data_filtered)
			line = 'Zscore ' + str(comp) + ' ' + str(num)
			self.OnFilter_StatusBarText(line)
			self.filter_steps[len(self.filter_steps)+1] = (
				'Filter_ZScore', line, val
			)
		else:
			pass
	 #---
	 #--> Return
		return True
	 #---
	#---

	def OnFilter_Log2FC_Run(self, val, addStep=True):
		""" Filter the results by Log2FC values.
			---
			val: string with format < 10 or > 10
		"""
	 #--> Check user input
		out, num, comp = checkM.CheckMFilterByZscore(val)
		if out:
			pass
		else:
			gclasses.DlgWarningOk(config.msg['Errors']['Filter_Log2FC'])
			return False
	 #---
	 #--> Set data
		data = self.OnFilter_Data()
		b, c = self.OnFilter_CondTimeP()
	 #---		
	 #--> Filter dataframe
		idx = pd.IndexSlice
		col = idx[:,b,c,'log2FC']
		if comp == 'le':
			self.data_filtered = data[((data.loc[:,col] <= num) & (data.loc[:,col] >= -num)).any(axis=1)]
		elif comp == 'ge':
			self.data_filtered = data[((data.loc[:,col] >= num) | (data.loc[:,col] <= -num)).any(axis=1)]
	 #---
	 #--> Update GUI, filter_steps & StatusBar
		if addStep:
			self.FilterDataRedraw(self.data_filtered)
			line = 'Log2FC ' + str(comp) + ' ' + str(num)
			self.OnFilter_StatusBarText(line)
			self.filter_steps[len(self.filter_steps)+1] = (
				'Filter_Log2FC', line, val
			)
		else:
			pass
	 #---	 
	 #--> Return
		return True
	 #---
	#---

	def OnFilter_P_Run(self, val, logP, corrP, addStep=True):
		""" Filter by P values 
			---
			val: string with format > 10 or < 10
			logP: val refer to P (False) or logP (True) values (Boolean)
			corrP: use corrected (True) or regular (False) P values (Boolean)
		"""
	 #--> Check user input
		out, num, comp = checkM.CheckMFilterByZscore(val)
		if out:
			pass
		else:
			gclasses.DlgWarningOk(config.msg['Errors']['Filter_P'])
			return False
	 #---
	 #--> Variables
		data = self.OnFilter_Data()
		b, c = self.OnFilter_CondTimeP()
		if logP:
			d = 'p'
		else:
			d = ''
		if corrP:
			d = d + 'Pc'
		else:
			d = d + 'P'
	 #---		
	 #--> Filter dataframe
		idx = pd.IndexSlice
		col = idx[:,b,c,d]
		if comp == 'le':
			self.data_filtered = data[(data.loc[:,col] <= num).any(axis=1)]
		elif comp == 'ge':
			self.data_filtered = data[(data.loc[:,col] >= num).any(axis=1)]
	 #---
	 #--> Update GUI, filter_steps & StatusBar
		if addStep:
			self.FilterDataRedraw(self.data_filtered)
			line = 'P ' + str(comp) + ' ' + str(num)
			self.OnFilter_StatusBarText(line)			
			self.filter_steps[len(self.filter_steps)+1] = (
				'Filter_P', line, val, logP, corrP
			)
		else:
			pass
	 #---
	 #--> Return
		return True
	 #---		
	#---

	def OnFilter_Monotonic(self, up=False, down=False, both=False, addStep=True):
		""" Proteins with monotonic behavior in at least one condition """
	 #--> Check number of time points
		if self.Check_TP():
			pass
		else:
			return False
	 #---
	 #--> Variables
		data = self.OnFilter_Data()
		b, c = self.OnFilter_CondTimeP()
		idx = pd.IndexSlice
		if self.CType == config.combobox['ControlType'][1]:
			col = idx[:,:,c,'log2FC']
			control = ('Control', 'Control', c,'log2FC')
		else:
			col = idx[:,b,:,'log2FC']
			control = ('Control', b, 'Control','log2FC')
	 #---
	 #--> Filter data
	  #--> Add control column
		data.insert(0, control, 0)
	  #---
	  #--> Filter
		if both:
			self.data_filtered = data[data.loc[:,col].apply(self.OnFilter_Monotonic_Both, axis=1)]
			line = 'Monotonic (Both)'
		elif up:
			self.data_filtered = data[data.loc[:,col].apply(lambda x: x.is_monotonic_increasing, axis=1)]
			line = 'Monotonic (Increasing)'
		elif down:
			self.data_filtered = data[data.loc[:,col].apply(lambda x: x.is_monotonic_decreasing, axis=1)]
			line = 'Monotonic (Decreasing)'
		else:
			return False
	  #---
	  #--> Remove control
		data.drop(control, axis=1, inplace=True)
		self.data_filtered.drop(control, axis=1, inplace=True)
	  #---
	 #---
	 #--> Update GUI, filter_steps & StatusBar
		if addStep:
			self.FilterDataRedraw(self.data_filtered)
			self.OnFilter_StatusBarText(line)			
			self.filter_steps[len(self.filter_steps)+1] = (
				'Filter_Monotonic', line, up, down, both
			)
		else:
			pass
	 #---
	 #--> Return
		return True
	 #---			 
	#---

	def OnFilter_Monotonic_Both(self, row):
		""" Filter for monotonic increasing or decreasing """
		if row.is_monotonic_decreasing or row.is_monotonic_increasing:
			return True
		else:
			return False
	#---

	def OnFilter_Divergent(self, addStep=True):
		""" Get proteins with divergent behavior in at least two conditions """
	 #--> Check NC & TP
	  #--> Check number of conditions
		if self.Check_NC():
			pass
		else:
			return False
	  #---	 
	  #--> Check number of time points
		if self.Check_TP():
			pass
		else:
			return False
	  #---
	 #---
	 #--> Set data
		data = self.OnFilter_Data()
		data = self.OnFilter_Data_Divergent(data)
	 #---
	 #--> Filter
		self.data_filtered = data[data.apply(self.OnFilter_Divergent_Apply, axis=1)]
	 #---
	 #--> Remove control
		idx = pd.IndexSlice
		col = idx['Control',:,:,:]
		del_col = data.loc[:,col].columns.values.tolist()
		data.drop(columns=del_col, axis=1, inplace=True)
		self.data_filtered.drop(columns=del_col, axis=1, inplace=True)	 
	 #---
	 #--> Update GUI, filter_steps & StatusBar
		if addStep:
			self.FilterDataRedraw(self.data_filtered)
			line = 'Divergent'
			self.OnFilter_StatusBarText(line)			
			self.filter_steps[len(self.filter_steps)+1] = (
				'Filter_Divergent', line,
			)
		else:
			pass
	 #---
	 #--> Return
		return True
	 #---				
	#---

	def OnFilter_Divergent_Apply(self, row):
		""" Return if row is divergent or not """
	 #--> Variables 
		up        = False
		up_test   = True
		down      = False
		down_test = True
	 #---
	 #--> Check monotonicity
		for k in range(1, self.NC+1, 1):
		 #--> Create index slice
			idx = pd.IndexSlice
			if self.CType == config.combobox['ControlType'][1]:
				col = idx[:, :, 'Y'+str(k), 'log2FC']
			else:
				col = idx[:, 'X'+str(k), :, 'log2FC']	
		 #---
		 #--> Check up
			if up_test:
				tup = row.loc[col].is_monotonic_increasing
				if tup:
					up = True
					up_test = False
				else:
					pass
			else:
				pass
		 #-->
		 #--> Check Down
			if down_test:
				tdown = row.loc[col].is_monotonic_decreasing
				if tdown:
					down = True
					down_test = False
				else:
					pass
			else:
				pass 
		 #---
	 #---
	 #--> Return
		if up and down:
			return True
		else:
			return False
	 #---
	#---

	def OnFilter_Remove(self):
		""" Remove selected filters """	
	 #--> Check there are applied filters
		if self.Check_AppliedFilters():
			pass
		else:
			return False
	 #---	
	 #--> Create dlg & remove filter
		dlg = gclasses.DlgFilterRemove(
			self,
			self.filter_steps, 
			title=config.msg['TextInput']['caption']['Filter_Remove'],
		)
		if dlg.ShowModal() == wx.ID_OK:
			filterDict = {}
		 #--> Remove selected filters
			for k, i in enumerate(dlg.checkBoxes, start=1):
				if i.GetValue():
					pass
				else:
					filterDict[k] = self.filter_steps[k]
		 #---
		 #--> Apply left filters
			if len(filterDict) > 0:
				self.OnFilter_Apply(filterDict)
			else:
				self.OnReset(keepState=True)
		 #---
		else:
			pass
	 #---
	 #--> Destroy & Return
		dlg.Destroy()
		return True
	 #---
	#---

	def OnFilter_RemoveLast(self):
		""" Remove last added filter """
	 #--> Check there are applied filters
		if self.Check_AppliedFilters():
			pass
		else:
			return False
	 #---
	 #--> Set filterDict
		filterDict = {}
		for k in range(1, len(self.filter_steps)):
			filterDict[k] = self.filter_steps[k]		
	 #---
	 #--> Apply left filters
		if len(filterDict) > 0:
			self.OnFilter_Apply(filterDict)
		else:
			self.OnReset(keepState=True)
	 #---	
	 #--> Return 
		return True
	 #---
	#---
    #endregion ------------------------------------------------------- Filters

    #region ----------------------------------------------------------- Export
	def OnExport(self):
		""" Export protein list 
			---
			all : boolean to export only for this condition / relevant point or
			apply filter to each condition / relevent point and export each
			protein list
		"""
	 #--> Check there are applied filters
		if self.Check_AppliedFilters():
			pass
		else:
			return False
	 #---	
	 #--> Select output file
		dlg = gclasses.DlgSaveFile(config.extLong['Data'])
		if dlg.ShowModal() == wx.ID_OK:
			path = dlg.GetPath()
		else:
			return False
	 #---
	 #--> Get new df with correct labels
		df = self.data_filtered.rename(columns=self.col4Export[1], level=1)
		df.rename(columns=self.col4Export[2], level=2, inplace=True)
	 #---
	 #--> Write
		dmethods.FFsWriteCSV(path, df)
	 #---
	 #--> Return
		return True
	 #---
	#---
    #endregion -------------------------------------------------------- Export	

	#region ---------------------------------------------- Plot3 Time analysis
	def DrawConfig3(self):
		""" """
		if self.prot != False:
			self.title = (gmethods.ListCtrlGetColVal(self.lb, col=0, t="str")[0]
				+ ' - '
				+ gmethods.ListCtrlGetColVal(self.lb, col=1, t="str")[0]
			)
			if self.data_filtered is None:
				self.y = dmethods.DFColValFilter(self.data, self.prot, 1)[1]
			else:
				self.y = dmethods.DFColValFilter(
					self.data_filtered, 
					self.prot, 
					1,
				)[1]
		elif self.allL:
			self.title = "All detected proteins"
		else:
			self.title = ''
		self.Draw3()
		return True
	#---

	def Draw3(self):
		""" """
	 #-->
		self.p3.ClearPlot()
	 #-->
		self.p3.axes.set_title(self.title)
	 #-->
		if self.allL:
			self.DrawAll3()
		else:
			pass
	 #-->
		if self.prot != False:
			self.legendShow = True
			self.legendlist = []
			self.DrawHelper3(self.y, self.colors, 1, lw=3)
			self.legendShow = False
			self.leg = self.p3.axes.legend(handles=self.legendlist, loc='upper left',
			bbox_to_anchor=(1, 1))
			self.leg.get_frame().set_edgecolor('k')	
		else:
			pass
	 #-->
		self.SetAxis3()
	 #-->
		self.p3.canvas.draw()
	#---

	def DrawAll3(self):
		""" Draw all data at the begining """
		if self.grayC:
			color = [config.colors[self.name]["Gray"]] * self.NC
		else:
			color = self.colorsL
		#-->
		if self.data_filtered is None:
			self.DrawHelper3(self.data, color, 1)
		else:
			self.DrawHelper3(self.data_filtered, color, 1)
		#-->
		return True
	#---

	def DrawHelper3(self, df, color, alpha, lw=1):
		""" df: data frame with the data
			color: color for the points & lines (list)
			alpha: transparence (float)
			lw: line width (integer)
		"""
		idx = pd.IndexSlice
		for a in range(0, self.NC, 1):
			x = self.xCoordTimeA[a]
			if self.CType == config.combobox['ControlType'][1]:
				y = df.loc[:, idx['v',:,'Y'+str(a+1),:]]
			else:
				y = df.loc[:, idx['v','X'+str(a+1),:,:]]
			yPlot = y.loc[:, idx[:,:,:,"log2FC"]]
			yPlot.insert(0, "Origin", 0)
			yPlot = yPlot.transpose()
			tcolor = color[a]
			self.p3.axes.plot(
				x, yPlot.values, marker="o", color=tcolor, alpha=alpha, picker=5
			)
			if self.legendShow:
				patch = mpatches.Patch(
					color=tcolor, 
					label=str(self.NCondL[a])
				)
				self.legendlist.append(patch)
			else:
				pass
		return True
	#---

	def SetAxis3(self):
		""" General details of the plot area """
	 #--> Names of the axis
		self.p3.axes.grid(True, linestyle=":")
		self.p3.axes.set_xlabel('Relevant Points', fontweight="bold")
		self.p3.axes.set_ylabel("log$_{2}$[Fold Change]", fontweight="bold")
		self.p3.axes.set_xticks(range(0, len(self.XaxisLabel), 1))
		self.p3.axes.set_xticklabels(self.XaxisLabel)
	 #--> Make symmetric
		ylim = self.p3.axes.get_ylim()
		if abs(ylim[0]) >= abs(ylim[1]):
			self.p3.axes.set_ylim(ylim[0], -ylim[0])
		else:
			self.p3.axes.set_ylim(-ylim[1], ylim[1])
	 #--> Return
		return True
	#---
	#endregion ------------------------------------------- Plot3 Time analysis

	#region ----------------------------------------------- Plot2 Volcano plot
	def DrawConfig2(self, df=None):
		""" """
	 #--> df
		if df is None:
			if self.data_filtered is None:
				df = self.data
			else:
				df = self.data_filtered
		else:
			pass
	 #--> Title of the plot
		self.title = (
			"C: " 
			+ str(self.NCondL[self.n])
			+ "  TP: " 
			+ str(self.NTimePL[self.tp])
			+ "  Z$_{score}$: "
			+ str(self.ZscoreValDP)
			+ "%"
		)
	 #--> Get data
		if self.CType == config.combobox['ControlType'][1]:
			try:
				self.x = df[('v', 'X'+str(self.tp+1), "Y" + str(self.n+1), "log2FC")]
				self.y = df[('v', 'X'+str(self.tp+1), "Y" + str(self.n+1), self.pP)]
				self.z = df[('v', 'X'+str(self.tp+1), "Y" + str(self.n+1), "zFC")]
				self.colorsV = dmethods.GetZColors(
					self.z.to_list(), 
					config.colors[self.name]["Colors"],
					lim=self.ZscoreValD,
				)[1]
				k = True
			except Exception:
				k = False
		else:
			try:
				self.x = df[('v', 'X'+str(self.n+1), "Y" + str(self.tp+1), "log2FC")]
				self.y = df[('v', 'X'+str(self.n+1), "Y" + str(self.tp+1), self.pP)]
				self.z = df[('v', 'X'+str(self.n+1), "Y" + str(self.tp+1), "zFC")]
				self.colorsV = dmethods.GetZColors(
					self.z.to_list(), 
					config.colors[self.name]["Colors"],
					lim=self.ZscoreValD,
				)[1]
				k = True
			except Exception:
				k = False
		if k:
			pass
		else:
			self.x = pd.Series([])
			self.title = "No data found for this relevant point"
	 #--> Plot
		self.Draw2()
	 #--> Return
		return True
	#---

	def Draw2(self):
		""" """
	 #-->
		self.p2.ClearPlot()
	 #-->
		self.p2.axes.set_title(self.title)
	 #-->
		if len(self.x.index) > 0:
			self.p2.axes.scatter(
				self.x,
				self.y,
				c = self.colorsV,
				alpha	  = 1,
				edgecolors = "black",
				linewidths = 1,
				picker	 = True,
			)
		else:
			pass
	 #-->
		xlim = self.p2.axes.get_xlim()
		if abs(xlim[0]) >= abs(xlim[1]):
			self.p2.axes.set_xlim(xlim[0], -xlim[0])
		else:
			self.p2.axes.set_xlim(-xlim[1], xlim[1])
	 #-->
		self.SetAxis2()
		self.p2.canvas.draw()
	 #--> 
		return True
	#---

	def SetAxis2(self):
		""" General details of the plot area """
		self.p2.axes.grid(True, linestyle=":")
		self.p2.axes.axhline(y=self.loga, color="black", dashes=(5, 2, 1, 2), alpha=0.5)
		self.p2.axes.set_xlabel("log$_{2}$[Fold Change]", fontweight="bold")
		self.p2.axes.set_ylabel("-log$_{10}$[p values]", fontweight="bold")
		return True
	#---
	#endregion -------------------------------------------- Plot2 Volcano plot

	#region -------------------------------------------------------- Show Text
	def ShowText(self, df):
		""" Show details for a selection in the wx.ListCtrl
			---
			df: self.data selection with the selected protein
		"""
	 #--> Clear old text
		self.tcText.Clear()
	 #--> Variables
		num   = gmethods.ListCtrlGetColVal(self.lb, col=0, t="str")[0]
		gen   = gmethods.ListCtrlGetColVal(self.lb, col=1, t="str")[0]
	 #--> Write
	  #--> Header
		self.tcText.AppendText('--> Selected entry:\n\n')
		line = ('No.: '
		   + num
		   + " | Gene: "
		   + gen
		   + ' | Protein: '
		   + self.prot
		   + '\n\n'
		)
		self.tcText.AppendText(line)
	  #--> Intra Condition comparison
		self.AddTextCComp(df)
	  #--> Inter Condition comparison
		if self.NC > 1:
			self.AddTextTPComp(df)  
		else:
			pass
	  #--> Ave for Intra Condition comparison
		line = ('--> Intensity averages and standard deviations: \n\n')
		self.tcText.AppendText(line)		   
		self.AddTextAveCond(df)
	  #--> 
		self.AddTextAveTP(df)
	 #--> Get back to first line
		self.tcText.SetInsertionPoint(0)
	 #--> Return  
		return True
	#---

	def AddTextCComp(self, df):
		""" Add table showing the p and log2FC values for each n/tp 
			---
			df: dataframe to get the data
		"""
	 #--> Create dfo
	  #--> MultiIndex
		a = ['          '] + ['P values'] * self.TP + ['log2FC'] * self.TP
		b = ['Conditions'] + 2 * self.NTimePL
		mInd = pd.MultiIndex.from_arrays([a[:],
										  b[:]])
	  #--> dfo
		dfo = pd.DataFrame(columns=mInd, index=range(0, self.NC, 1))
	  #--> add data
		idx = pd.IndexSlice
	   #-->
		dfo.loc[:,idx[:,'Conditions']] = self.NCondL
	   #-->
		pvals = []
		if self.CType == config.combobox['ControlType'][1]:
			for k, e in enumerate(self.NCondL, start=1):
				pvals.append(df.loc[:,idx['v',:,'Y'+str(k), self.PoPc]].to_numpy().tolist()[0])
		else:
			for k, e in enumerate(self.NCondL, start=1):
				pvals.append(df.loc[:,idx['v','X'+str(k),:, self.PoPc]].to_numpy().tolist()[0])
		dfo.loc[:, idx['P values',:]] = pvals
	   #-->
		pvals = []
		if self.CType == config.combobox['ControlType'][1]:
			for k, e in enumerate(self.NCondL, start=1):
				pvals.append(df.loc[:,idx['v',:,'Y'+str(k), 'log2FC']].to_numpy().tolist()[0])
		else:
			for k, e in enumerate(self.NCondL, start=1):
				pvals.append(df.loc[:,idx['v','X'+str(k),:, 'log2FC']].to_numpy().tolist()[0])		
		dfo.loc[:, idx['log2FC',:]] = pvals	   
	  #--> write
		line = '--> Statistical test results and Fold changes: \n'
		self.tcText.AppendText(line)
		line = '	(Selected '+u'\N{GREEK SMALL LETTER ALPHA}'+' level: ' + str(self.aVal) + ')\n\n'
		self.tcText.AppendText(line)
		line = '  -- Volcano plot \n\n'
		self.tcText.AppendText(line)
	   #-->
		dmethods.DFWrite2TextCtrl(dfo, self.tcText, formatters=None)
		self.tcText.AppendText('\n\n')
	 #--> Return
		return True
	#---

	def AddTextTPComp(self, df):
		""" Add the time point comparison text 
			---
			df: data frame with the data for the selected protein
		"""
	 #--> Create dfo
		dfo = pd.DataFrame(
			columns=['Relevant points', 'P values'], 
			index=range(0, self.TP, 1)
		)
	 #--> Add data
		idx = pd.IndexSlice
		dfo['Relevant points'] = self.NTimePL
		dfo['P values'] = df.loc[:,idx['tp',:,:,self.PoPc]].to_numpy().tolist()[0]
	  #--> write
		line = ('  -- Relevant points analysis: \n\n')
		self.tcText.AppendText(line)	  
		dmethods.DFWrite2TextCtrl(dfo, self.tcText, formatters=None)
		self.tcText.AppendText('\n\n')
	 #--> Return
		return True
	#---

	def AddTextAveCond(self, df):
		""" Add the ave +/- std for the conditions 
			---
			df: data frame with the data
		"""
	 #--> Create dfo
	  #--> MultiIndex
		if self.CType == config.combobox['ControlType'][1]:
			a = ['          ']
			for i in self.NTimePL:
				a = a + [i] * 2
			b = ['Conditions'] + ['Ave', 'Std'] * (self.TP)
			l = self.NC + 1			
		else:
			a = ['          ']
			for i in [self.ControlLabel] + self.NTimePL:
				a = a + [i] * 2
			b = ['Conditions'] + ['Ave', 'Std'] * (self.TP+1)			 
			l = self.NC
		mInd = pd.MultiIndex.from_arrays([a[:],
										  b[:]])
	  #--> dfo
		dfo = pd.DataFrame(columns=mInd, index=range(0, l, 1))
	 #--> Add data
		idx = pd.IndexSlice
	  #-->
		if self.CType == config.combobox['ControlType'][1]:
			dfo.loc[:,idx[:,'Conditions']] = [self.ControlLabel] + self.NCondL
		else:
			dfo.loc[:,idx[:,'Conditions']] = self.NCondL
	  #-->
		ave = []
		std = []
		if self.CType == config.combobox['ControlType'][1]:
			for y in range(0, self.Yv+1, 1):
				avec = []
				stdc = []
				for x in range(1, self.Xv+1, 1):
					avec.append(df.loc[:,idx['v','X'+str(x),'Y'+str(y),'ave']].to_numpy().tolist()[0])
					stdc.append(df.loc[:,idx['v','X'+str(x),'Y'+str(y),'sd']].to_numpy().tolist()[0])
				ave.append(avec)
				std.append(stdc)
		else:
			for k in range(1, self.Xv+1, 1):
				ave.append(df.loc[:,idx['v','X'+str(k),:,'ave']].to_numpy().tolist()[0])
				std.append(df.loc[:,idx['v','X'+str(k),:,'sd']].to_numpy().tolist()[0])	 
	  #-->
		dfo.loc[:, idx[:,'Ave']] = ave
		dfo.loc[:, idx[:,'Std']] = std
	 #--> Write
		line = ('  -- Volcano plot: \n\n')
		self.tcText.AppendText(line)	 
		dmethods.DFWrite2TextCtrl(dfo, self.tcText)
		self.tcText.AppendText('\n\n')	   
	 #--> Return
		return True
	#---

	def AddTextAveTP(self, df):
		""" Add the ave +/- std for the relevant points 
			---
			df: data frame with the data
		"""
	 #--> Create dfo
	  #--> MultiIndex
		a = ['          ']
		for i in self.NTimePL:
			a = a + [i] * 2
		b = ['Conditions'] + ['Ave', 'Std'] * (self.TP)
		mInd = pd.MultiIndex.from_arrays([a[:],
										  b[:]])
	  #--> dfo
		dfo = pd.DataFrame(columns=mInd, index=range(0, self.NC, 1))
	 #--> Add data
		idx = pd.IndexSlice
	  #-->
		dfo.loc[:,idx[:,'Conditions']] = self.NCondL
	  #-->
		ave = []
		std = []
		for y in range(1, self.NC+1, 1):
			avec = []
			stdc = []
			for x in range(1, self.TP+1, 1):
				avec.append(df.loc[:,idx['tp','T'+str(x),'C'+str(y),'ave']].to_numpy().tolist()[0])
				stdc.append(df.loc[:,idx['tp','T'+str(x),'C'+str(y),'sd']].to_numpy().tolist()[0])
			ave.append(avec)
			std.append(stdc)
	  #-->
		dfo.loc[:, idx[:,'Ave']] = ave
		dfo.loc[:, idx[:,'Std']] = std 
	 #--> Write
		line = ('  -- Relevant points analysis: \n\n')
		self.tcText.AppendText(line)	 
		dmethods.DFWrite2TextCtrl(dfo, self.tcText)
		self.tcText.AppendText('\n\n')	   
	 #--> Return
		return True
	#---
	#endregion ----------------------------------------------------- Show Text
#---






