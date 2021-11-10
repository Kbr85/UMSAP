# ------------------------------------------------------------------------------
#	Copyright (C) 2017 Kenny Bravo Rodriguez <www.umsap.nl>
	
#	This program is distributed for free in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
	
#	See the accompaning licence for more details.
# ------------------------------------------------------------------------------


""" Creates the window showing the results in a .aadist file """


#region -------------------------------------------------------------- Imports
import wx
import matplotlib.patches as mpatches
from pathlib import Path

import config.config     as config
import gui.menu.menu     as menu
import gui.gui_classes   as gclasses
import gui.gui_methods   as gmethods
import data.data_classes as dclasses
import data.data_methods as dmethods
#endregion ----------------------------------------------------------- Imports


class WinAAdistRes(gclasses.WinGraph):
	""" Creates the window to show the results in a .aadist file """

	#region ---------------------------------------------------- Initial Setup	
	def __init__(self, file):
		""" file: path to the aadist file (string or Path) """
	 #--> Initial Setup
		self.name = config.name['AAdistR']
		super().__init__(file)
	 #---
	 #--> Variables
		self.dataPC   = self.fileObj.dataPerCent
		self.nExp     = self.fileObj.nExp
		self.nExpFP   = self.fileObj.nExpFP
		self.nPos     = self.fileObj.nPos
		self.nPosD2   = self.fileObj.nPosD2
		self.nPosName = self.fileObj.nPosName
		self.aaKeys   = self.fileObj.aaKeys
		self.barWidth = self.fileObj.barWidth
		self.aaCount  = self.fileObj.aaCount
		self.indKeys  = self.fileObj.indKeys
		#---
		self.aaKeysN  = len(self.aaKeys)
		self.Ncolor   = len(config.colors['Fragments'])
		#---
		self.exp = 0
		self.pos = 0
	 #---
	 #--> Menu
		self.menubar = menu.MainMenuBarWithTools(self.name, 
			self.exp, 
			self.pos, 
			self.nExp,
			self.nPosName)
		self.SetMenuBar(self.menubar)
	 #---
	 #--> Draw
		self.DrawConfig()
	 #---
	 #--> Show
		self.Show()
	 #---
	#---
	#endregion ------------------------------------------------- Initial Setup	

	# ------------------------------------------------------------- My Methods
	#region -------------------------------------------------- Binding Methods
	def WinPos(self):
		""" Set the position of a new window depending on the number of same
			windows already open 
		"""
	 #--> Coordinates
		xw, yw = self.GetSize()
		xo, yo = config.coord['TopXY']
		xo = config.size['Screen'][0] - xw 
		x = xo - config.win['AAdistResNum'] * config.win['DeltaNewWin']
		y = yo + config.win['AAdistResNum'] * config.win['DeltaNewWin']
	 #---
	 #--> Position
		self.SetPosition(pt=(x, y))
	 #---
	 #--> Update number
		config.win['AAdistResNum'] = config.win['AAdistResNum'] + 1
	 #---
	 #--> Return
		return True
	 #---
	#---

	def OnClick(self, event):
		""" To process click events """
		if event.button == 3:
			if config.cOS != 'Windows':
				Tmenu = menu.ToolsAAdistRes(
					self.exp, 
					self.pos,
					self.nExp, 
					self.nPosName
				)
				self.PopupMenu(Tmenu)
			else:
				pass
		else:
			pass
		return True
	#---
	#endregion ----------------------------------------------- Binding Methods
	
	#region ----------------------------------------------------- Menu Methods
	def OnExportData(self):
		""" Export data to a csv file """
	 #--> Variables
		msg = config.msg['Save']['ExportData']
		dlg = gclasses.DlgSaveFile(config.extLong['Data'], msg)
	 #---
	 #--> Get path & write
		if dlg.ShowModal() == wx.ID_CANCEL:
			pass
		else:
			p = Path(dlg.GetPath())
			self.fileObj.ExportData(p)
	 #---
	 #--> Destroy & Return 
		dlg.Destroy()
		return True	
	 #---
	#---	

	def OnExp(self, Mid):
		""" Show the AAdist for a particular experiment 
			---
			Mid: ID of the selected menu item (int)
		"""
		self.exp = Mid - 100
		self.menubar.Check(Mid, True)
		self.pos = 0
		self.DrawConfig()
		return True
	#---

	def OnReset(self):
		""" Reset the view """
	 #-->
		self.exp = 0
		self.pos = 0
	 #---
	 #-->
		self.menubar.Check(100, True)
		self.menubar.Check(200, True)
	 #---
	 #-->
		self.DrawConfig()
	 #---
	 #-->
		return True		
	 #---
	#---

	def OnPos(self, Mid):
		""" Compare the distribution for a particular position in all 
			experiments 
			---
			Mid: ID of the selected menu item (int)
		"""
		self.pos = Mid - 200
		self.menubar.Check(Mid, True)
		self.DrawConfig()
		return True
	#---	
	#endregion -------------------------------------------------- Menu Methods
	
	#region ------------------------------------------------- Plotting Methods
	def DrawConfig(self):
		""" Configure the plot """
	 #--> Set key & title
		if self.exp == 0:
			self.tkey = 'FP'
			self.title = 'AA distribution (FP List)'
		else:
			self.title = 'AA distribution (Exp' + str(self.exp) + ')'
			self.tkey = 'Exp' + str(self.exp)
	 #---
	 #--> Get position and draw position or comparison
		if self.pos == 0:
			self.Draw()
		else:
			if self.pos > self.nPosD2:
				p = self.pos - self.nPosD2
				self.title = 'AA distribution (Pos P' + str(p) + "')"
			elif self.pos <= self.nPosD2:
				p = self.nPosD2 - self.pos + 1
				self.title = 'AA distribution (Pos P' + str(p) + ')'
			self.tpos = self.pos - 1 	
			self.DrawComp()
	 #---
	 #--> Return
		return True
	 #---
	#---

	def SetAxis(self):
		""" General properties of the graph """
		self.axes.grid(False)
		self.axes.set_xlabel('Positions', fontweight='bold')
		self.axes.set_ylabel('AA distribution (%)', fontweight='bold')
		self.xticksloc = range(self.nPos + 2)
		self.axes.set_xticks(self.xticksloc)
		self.xlabel = ['']
		for k, i in enumerate(self.nPosName):
			j = k + 1
			self.xlabel.append(i)
			color = self.fileObj.GetChiColor(self.tkey, k)
			self.axes.get_xticklabels()[j].set_color(color)
		self.xlabel.append('')
		self.axes.set_xticklabels(self.xlabel)
		self.axes.relim()
		self.axes.autoscale_view()
		return True
	#---

	def Draw(self):
		""" Draw bar plot for one experiment """
	 #--> Clear plot
		self.ClearPlot()
	 #---
	 #--> title
		self.axes.set_title(self.title)
	 #---
	 #--> tDF with percent values 
		tDF = self.dataPC.loc[self.tkey]
	 #---
	 #--> Draw bars
		for i in range(0, len(self.nPosName), 1):
			iS = i
			j = i + 1
			#---
			tDFi = tDF.loc[:,['AA', iS]]
			tDFi.sort_values(by=iS, inplace=True, ascending=False)
			#---
			lvs = tDFi.loc[:,iS]
			lbs = dmethods.ListStepSum(lvs, self.name)
			#---
			orderKeys = tDFi.loc[:,'AA'].tolist()
			#---
			color = [config.colors[self.name]['BarColors'][x] 
				if x in config.aaList1 else config.colors[self.name]['Xaa']
				for x in orderKeys]
			#---
			self.axes.bar(j, lvs, align='center', bottom=lbs, color=color,
				width=config.aadist['Twidth'], 
				edgecolor=config.colors[self.name]['BarEdge'])
			#---
			for k, v in enumerate(lvs):
				if v >= 10.0:
					s = orderKeys[k] + '\n' + '{0:.1f}'.format(v)
					y = (v + 2 * lbs[k]) / 2
					self.axes.text(j, y, s, fontsize=9,
						horizontalalignment='center', 
						verticalalignment='center')
				else:
					pass
	 #---
	 #--> Axis, draw & Return
		self.SetAxis()
		self.canvas.draw()
		return True
	 #---
	#---

	def SetAxisComp(self):
		""" Set the axis for the comparison of a position """
		self.axes.grid(True, linestyle=':')
		self.axes.set_xlabel('Amino acids', fontweight='bold')
		self.axes.set_ylabel('AA distribution (%)', fontweight='bold')
		self.xticksloc = range(len(self.aaKeys) + 2)
		self.axes.set_xticks(self.xticksloc)
		self.xlabel = ['']
		self.xlabel = self.xlabel + self.aaKeys
		self.xlabel.append('')
		self.axes.set_xticklabels(self.xlabel)
		self.axes.relim()
		self.axes.autoscale_view()
		return True
	#---

	def DrawComp(self):
		""" Show a comparison of the aadist for a given position for all 
			experiments. 
		"""
	 #--> Clear
		self.ClearPlot()
	 #---
	 #--> Title
		self.axes.set_title(self.title)
	 #---
	 #--> Variables
		p = self.pos - 1
		pl = 0
	 #---
	 #--> Draw bars
		for a in self.aaKeys:
			pl += 1
			s = pl - config.aadist['StartLoc']
			#---
			tDFi = self.dataPC.loc[self.dataPC.loc[:, 'AA'] == a, p]
			for k, i in enumerate(tDFi):
				if k < self.nExp:
					ci = (k + 1) % self.Ncolor
					color = config.colors['Fragments'][ci]
				else:
					color = color = config.colors[self.name]['FPBar'] 
				tx = s + k*self.barWidth
				self.axes.bar(tx, i, align='edge', color=color, 
					width=self.barWidth, 
					edgecolor=config.colors[self.name]['BarEdge'])
	 #---
	 #--> Legend
		self.legendlist = []
		for i in range(1, self.nExpFP, 1):
			ci = i % self.Ncolor
			color = config.colors['Fragments'][ci]	
			name = 'Exp ' + str(i)
			patch = mpatches.Patch(color=color, label=name)
			self.legendlist.append(patch)
		patch = mpatches.Patch(color=config.colors[self.name]['FPBar'],
			label='FP list')
		self.legendlist.append(patch)
		self.leg = self.axes.legend(handles=self.legendlist, loc='upper left',
			bbox_to_anchor=(1, 1))
		self.leg.get_frame().set_edgecolor('k')					
	 #---
	 #--> Axis, draw & Return
		self.SetAxisComp()
		self.canvas.draw()
		return True
	 #---
	#---

	def UpdateStatusBar(self, event):
		""" To update status bar """
	 #--# Improve Is easier to maintain if you split this in two helper functions
	 #--> Check event in axes
		if event.inaxes:
			x, y = event.xdata, event.ydata
			xf = int(x + 0.5) - 1
	 #---
	 #--> Text for positions
			if self.pos == 0 and x > 0.6 and x < self.nPos + 0.4:
				show = None
				xS = xf
				tDF = self.dataPC.loc[self.tkey, ['AA', xS]].sort_values(
					by=xS, ascending=False)
				tDF['CumSum'] = tDF.loc[:,xS].cumsum()
				tDF = tDF.reset_index(drop=False)
				for k in range(0, self.aaKeysN+1,1):
					if y <= tDF.at[k, 'CumSum']:
						show = True
						break
					else:
						pass					
				if show == None:
					self.statusbar.SetStatusText('')
				else:
					pos  = self.nPosName[xf]
					AA   = tDF.at[k, 'AA']
					per  = '{:.2f}'.format(tDF.at[k, xS])
					tind = tDF.at[k, 'index']
					absC = self.fileObj.dataDF.at[(self.tkey, tind), xS]
					inseqC = self.aaCount[AA]
					self.statusbar.SetStatusText('Pos=' + str(pos) + 
						'  AA=' + str(AA) + '  %=' + str(per) + 
						'  Abs=' + str(absC) + '  InSeq=' + str(inseqC))
	 #---
	 #--> Text for comparison
			elif self.pos != 0 and x > 0.6 and x < len(self.aaKeys) + 0.4:
				xS = xf + 1
				p = self.pos - 1 
				show = True
				AA = self.aaKeys[xf]
				s = xS-config.aadist['StartLoc'] + self.barWidth
				e = xS-config.aadist['StartLoc'] + config.aadist['Twidth']
				n = 0
				while s < e:
					if s > x:
						break
					else:
						s = s + self.barWidth
						n += 1
				if show == None:
					self.statusbar.SetStatusText(gmethods.StatusBarXY(x, y))
				else:
					exp    = self.indKeys[n]
					if exp == 'RD':
						self.statusbar.SetStatusText(gmethods.StatusBarXY(x, y))
					else:
						per    = self.dataPC.loc[self.dataPC.loc[:,'AA'] == AA].loc[exp].loc[:,p].values[0]
						per = '{:.2f}'.format(float(per))
						absC   = self.fileObj.dataDF.loc[self.fileObj.dataDF.loc[:,'AA'] == AA].loc[exp, p].values[0]
						inseqC = self.aaCount[AA]
						self.statusbar.SetStatusText("AA=" + str(AA) + 
							"  Exp=" + str(exp) + '  %=' + str(per) +
							'  Abs=' + str(absC) + '  InSeq=' + str(inseqC))
			else:
				self.statusbar.SetStatusText(gmethods.StatusBarXY(x, y))
	 #---
	 #--> No text
		else:
			self.statusbar.SetStatusText('')
	 #---
	 #--> Return
		return True
	 #---
	#---
	#endregion ---------------------------------------------- Plotting Methods
#---














