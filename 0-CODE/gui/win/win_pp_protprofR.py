# ------------------------------------------------------------------------------
# 	Copyright (C) 2017-2019 Kenny Bravo Rodriguez <www.umsap.nl>

# 	This program is distributed for free in the hope that it will be useful,
# 	but WITHOUT ANY WARRANTY; without even the implied warranty of
# 	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

# 	See the accompaning licence for more details.
# ------------------------------------------------------------------------------


""" Creates the window showing the results for a .protprof file """


# ------------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Methods
# ------------------------------------------------------------------------------



#--- Imports
## Standard modules
import wx
import pandas as pd
import matplotlib.patches as mpatches
from pathlib import Path
from scipy import stats
## My modules
import config.config		  as config
import gui.menu.menu		  as menu
import gui.gui_classes		as gclasses
import gui.gui_methods		as gmethods
import data.data_methods	  as dmethods
import checks.checks_multiple as checkM
#---



class WinProtProfRes(gclasses.WinResDosDos):
	""" To show the results in a protprof file """

	def __init__(self, file):
		""" file: path to the protprof file """
	 #--> Initial setup
		self.name = config.name["ProtProfRes"]
		self.fileP = Path(file)
		try:
			super().__init__(self, parent=None)
		except Exception:
			raise ValueError("")
	 #--> Variables
		self.NC		   = self.fileObj.nConds
		self.data		 = self.fileObj.dataFrame
		self.start		= True
		self.TP		   = self.fileObj.timeP
		self.NP		   = self.fileObj.NProt
		self.colors	   = dmethods.GetColors(self.NC)
		self.colorsL	  = dmethods.GetColors(self.NC, "L")
		self.loga		 = self.fileObj.loga
		self.aVal		 = self.fileObj.aVal
		self.P			= False
		self.xCoordTimeA  = self.fileObj.xCoordTimeA
		self.ZscoreVal	= self.fileObj.ZscoreVal
		self.ZscoreValP   = self.fileObj.ZscoreValP
		self.ZscoreValD   = self.fileObj.ZscoreVal
		self.ZscoreValDP  = self.fileObj.ZscoreValP
		self.NCondL	   = self.fileObj.nCondsL
		self.NTimePL	  = self.fileObj.nTimePL
		self.XaxisLabel   = [self.fileObj.ControlLabel] + self.NTimePL
		self.ControlLabel = self.fileObj.ControlLabel
		self.CType		= self.fileObj.CType
		self.Xv		   = self.fileObj.Xv
		self.Yv		   = self.fileObj.Yv
		#---
		self.n  = 0
		self.tp = 0
		#---
		self.grayC	  = False
		self.allL	   = False
		self.prot	   = False
		self.legendShow = False
		self.CorrP	  = False
		self.pP		 = config.protprof['ColOut'][1]
		self.pPt		= config.protprof['ColTPp'][0]
		self.PoPc	   = config.protprof['ColOut'][0]
	 #--> Menu
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
	 #--> Widgets
	  #--> Line
		self.lineHI10 = wx.StaticLine(self.panel)
	  #--> TextCtrl
		self.tcText = wx.TextCtrl(self.panel, 
			size=config.size['TextCtrl'][self.name]['TextPanel'], 
			style=wx.BORDER_SIMPLE|wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
		self.tcText.SetFont(config.font[config.name['TarProtRes']])
	 #--> Sizers
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

	####---- Methods of the classs
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

	##-- Binding
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

	##-- Menu
	def OnReset(self):
		""" Reset view """
		self.grayC = False
		self.allL  = False
		self.prot  = False
		#---
		self.n = 0
		self.tp = 0
		#---
		self.menubar.Check(703, False)
		self.menubar.Check(704, False)
		self.menubar.Check(504, True)
		self.menubar.Check(504 + self.NC, True)
		#--- Reset listbox
		gmethods.ListCtrlDeSelAll(self.lb)
		#--- Reset Z score
		self.ZscoreValD  = self.ZscoreVal
		self.ZscoreValDP = self.ZscoreValP
		#--- Reset p2 and p3 panel
		self.DrawConfig3()
		self.DrawConfig2()
		#--- Reset SearchCtrl
		self.search.Clear()
		#--- Reset TextCtrl
		self.tcText.Clear() 
		#---
		self.Refresh()
		self.Update()
		return True
	#---

	def OnCond(self, Mid):
		""" Mid: Id of the selected menu item (int) """
		self.n = Mid - 504
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
		self.tp = Mid - (504 + self.NC)
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
			config.msg['TextInput']['ZScoreThreshold'],
			value=str(self.ZscoreValDP)
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

	##-- Plot3 Time analysis
	def DrawConfig3(self):
		""" """
		if self.prot != False:
			self.title = (gmethods.ListCtrlGetColVal(self.lb, col=0, t="str")[0]
				+ ' - '
				+ gmethods.ListCtrlGetColVal(self.lb, col=1, t="str")[0]
			)
			self.y = dmethods.DFColValFilter(self.data, self.prot, 1)[1]
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
		self.DrawHelper3(self.data, color, 1)
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
		self.p3.axes.set_ylabel("log$_{2}$[fold change]", fontweight="bold")
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

	##-- Plot2 Volcano plot
	def DrawConfig2(self):
		""" """
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
				self.x = self.data[('v', 'X'+str(self.tp+1), "Y" + str(self.n+1), "log2FC")]
				self.y = self.data[('v', 'X'+str(self.tp+1), "Y" + str(self.n+1), self.pP)]
				self.z = self.data[('v', 'X'+str(self.tp+1), "Y" + str(self.n+1), "zFC")]
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
				self.x = self.data[('v', 'X'+str(self.n+1), "Y" + str(self.tp+1), "log2FC")]
				self.y = self.data[('v', 'X'+str(self.n+1), "Y" + str(self.tp+1), self.pP)]
				self.z = self.data[('v', 'X'+str(self.n+1), "Y" + str(self.tp+1), "zFC")]
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
		self.p2.axes.set_xlabel("log$_{2}$[fold change]", fontweight="bold")
		self.p2.axes.set_ylabel("-log$_{10}$[p values]", fontweight="bold")
		return True
	#---

	##-- Show Text 
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
		line = '	(True: p < '+u'\N{GREEK SMALL LETTER ALPHA}'+', False: p > '+u'\N{GREEK SMALL LETTER ALPHA}'+')\n\n'
		self.tcText.AppendText(line)
		line = '  -- Volcano plot \n\n'
		self.tcText.AppendText(line)
	   #-->
		myDict = {i:lambda x: 'True' if x <= self.aVal else 'False' 
			for i in dfo.loc[:, idx['P values',:]].columns}	  
	   #-->
		dmethods.DFWrite2TextCtrl(dfo, self.tcText, formatters=myDict)
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
		myDict = {'P values':lambda x: 'True' if x <= self.aVal else 'False'}  
	  #--> write
		line = ('  -- Relevant points analysis: \n\n')
		self.tcText.AppendText(line)	  
		dmethods.DFWrite2TextCtrl(dfo, self.tcText, formatters=myDict)
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
#---

