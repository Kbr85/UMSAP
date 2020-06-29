# ------------------------------------------------------------------------------
#	Copyright (C) 2017 Kenny Bravo Rodriguez <www.umsap.nl>
	
#	This program is distributed for free in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
	
#	See the accompaning licence for more details.
# ------------------------------------------------------------------------------


""" Creates the window showing the results in a .limprot file """


#region -------------------------------------------------------------- Imports
from pathlib import Path

import wx
import pandas as pd

import config.config     as config
import gui.menu.menu     as menu
import gui.gui_methods   as gmethods
import gui.gui_classes   as gclasses
import data.data_classes as dclasses
import data.data_methods as dmethods
import checks.checks_single as check
#endregion ----------------------------------------------------------- Imports


class WinLimProtRes(gclasses.WinResUno, gclasses.ElementGelPanel):
	""" To show the results in a limprot file """

	#region --------------------------------------------------- Instance Setup
	def __init__(self, file):
		""" file: path to the file with the results """
	 #--> Initial Variables
		self.name = config.name['LimProtRes']
		self.fileP = Path(file)
		try:
			self.fileObj = dclasses.DataObjLimProtFile(self.fileP)
		except Exception:
			raise ValueError('')
	 #---
	 #--> Check that there is something to show
		self.checkFP = self.fileObj.checkFP
		if self.checkFP:
			pass
		else:
			gclasses.DlgFatalErrorMsg(
				config.dictCheckFatalErrorMsg[self.name]['FiltPept2'])
			raise ValueError('')
	 #---
	 #--> Initial Setup
		try:
			gclasses.WinResUno.__init__(self, parent=None)
			gclasses.ElementGelPanel.__init__(self, parent=self.panel)
		except Exception:
			raise ValueError('')
	 #---
	 #--> More Variables
	  #-->
		self.Lanes       = self.fileObj.Lanes
		self.Bands       = self.fileObj.Bands
		self.nLines      = self.fileObj.nLines
		self.nLinesT     = self.fileObj.nLinesT     
		self.Results     = self.fileObj.Results
		self.listOfProt  = self.fileObj.listOfProt
		self.tarprot     = self.fileObj.tarprot
		self.Colors      = dmethods.GetColors(self.nLinesT)
		self.Mask        = self.fileObj.Mask
		self.pRes        = self.fileObj.pRes
		self.mist        = self.fileObj.mist
		self.natProtPres = self.fileObj.natProtPres
		self.locProtType = self.fileObj.locProtType
		self.TLane       = None       
		self.TBand       = None      
	  #-->                          
		self.fAll   = self.fileObj.GetFragments()[1]
	  #--->>>> self.fPlot and self.f needed for ElementFragPanel to work
		self.fPlot       = False      
		self.f           = None       
		self.lbSelPlot   = False      
		self.FragLabel   = 'Band   '  
		self.kf          = [None, None]
		self.GelText     = True       
	  #-->                          
		self.lbSelPlotG  = False      
		self.selSeq      = None       
	  #-->                          
		self.selM        = True # In the Gel select Lanes Bands otherwise
	  #-->                          
		self.mist        = self.fileObj.mist
	  #-->                          
		self.TextL       = None             
		self.TextB       = None             
		self.TextF       = None             
		self.TextM       = 0            
	 #---
	 #--> Menu
		self.menubar = menu.MainMenuBarWithTools(self.name, self.selM)
		self.SetMenuBar(self.menubar)
	 #---
	 #--> Sizers
	  #--> Add
		self.sizerIN.Add(self.p2,      pos=(2,2), border=2,
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
	  #---
	  #--> Fit
		self.sizer.Fit(self)
	  #---
	 #---
	 #--> Positions and minimal size
		gmethods.MinSize(self)
		self.WinPos()
	 #---
	 #--> Binding
		self.p2.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
	 #---
	 #--> Show
		self.Show()
	 #---
	#---
	#endregion ------------------------------------------------ Instance Setup

	# ------------------------------------------------------------- My Methods
	#region -------------------------------------------------- Binding Methods
	def OnRightDown(self, event):
		""" Display the popup menu """
		self.PopupMenu(menu.ToolsLimProtRes(self.selM))
		return True
	#---
	#endregion ----------------------------------------------- Binding Methods

	#region ----------------------------------------------------- Menu Methods
	def OnExportFP(self):
		""" Export the FP list """
	 #--> Variables
		msg = config.msg['Save']['FiltPept']
		dlg = gclasses.DlgSaveFile(config.extLong['FiltPept'], msg)
	 #---
	 #--> Get path & save	
		if dlg.ShowModal() == wx.ID_CANCEL:
			pass
		else:
			p = Path(dlg.GetPath())
			self.fileObj.LimProt2FiltPept(p)
	 #---
	 #--> Destroy & Return
		dlg.Destroy()
		return True	
	 #---
	#---

	def OnResetView(self):
		""" Reset the view of the window """
	
	 #--> Variables
		self.TLane       = None
		self.HLane       = False		
		#-->
		self.fPlot       = False
		self.f           = None
		#-->
		self.lbSelPlot   = False
		self.FragLabel   = 'Band   '
		self.kf          = [None, None]
		#-->
		self.lbSelPlotG  = False
		self.selSeq      = None
		#--> 
		self.selM        = True
	 #---
	 #--> Update GUI
		gmethods.ListCtrlDeSelAll(self.lb)
		#-->
		self.search.Clear()
		#-->
		self.text.Clear()		
		#-->
		self.menubar.Check(100, True)
		#-->
		self.Refresh()
		self.Update()
	 #---
	 #--> Return
		return True
	 #---
	#---

	def OnSelM(self):
		""" Select a Lane or a Band. Upon menu selection change settings """
	 #-->
		if self.selM:
			self.selM = False
			self.FragLabel = 'Lane   '
			self.menubar.Check(100, False)
	 #---
	 #-->
		else:
			self.selM = True
			self.FragLabel = 'Band   ' 
			self.menubar.Check(100, True)
	 #---
	 #-->
		return True
	 #---
	#---
	#endregion -------------------------------------------------- Menu Methods

	#region ----------------------------------------------------- Text Details
	def ShowFragDet(self):
		""" Needed because ElementFragPanel expect this method in the class """
		self.GetLBF()
		self.PrintW()
		self.ShowDetails()
		return True
	#---

	def ShowDetails(self):
		""" Show detail for selected Lane/Band, Spot or Fragment """
	 #--> Nothing selected
		if self.TextM == 0:
			pass
	 #---
	 #--> Lane selected
		elif self.TextM == 1:
			#-->
			try:
				df = self.fAll.loc['L'+str(self.TextL),:]
				out = True
			except Exception:
				out = False
			#-->
			self.text.Clear()	
			self.text.AppendText('Details for Lane ' + str(self.TextL) + '\n\n')
			if out:
				self.DataForSingleBandLane(df)
			else:
				self.DataForEmptySpot(label='lane')
	 #---
	 #--> Band
		elif self.TextM == 2:
			#-->
			try:
				idx = pd.IndexSlice
				df = self.fAll.loc[idx[:, 'B'+str(self.TextB)],:]
				out = True
			except Exception:
				out = False
			#-->
			self.text.Clear()
			self.text.AppendText('Details for Band ' + str(self.TextB) + '\n\n')
			if out:
				self.DataForSingleBandLane(df)
			else:
				self.DataForEmptySpot(label='band')
	 #---
	 #--> Spot
		elif self.TextM == 3:
			#-->
			try:
				df = self.fAll.loc[('L'+str(self.TextL), 'B'+str(self.TextB)),:]
				out = True
			except Exception:
				out = False
			#-->
			self.text.Clear()
			self.text.AppendText('Details for Lane ' + str(self.TextL) + 
				' and Band ' + str(self.TextB) + '\n\n')
			if out:
				self.DataForBandLane(df)
			else:
				self.DataForEmptySpot()
	 #---
	 #--> Fragment
		elif self.TextM == 4:
			dmethods.GHelperShowFragDet(self)
	 #---
	 #--> Return
		return True
	 #---
	#---

	def DataForEmptySpot(self, label='spot'):
		""" Write details for empty spot """
	 #-->
		self.text.AppendText("There were no peptides from " 
			+ self.tarprot 
			+ " identified in this "
			+ label
			+ ".\n\n")
	 #---
	 #-->
		self.text.AppendText("Other proteins detected in the gel:\n\n")
		for i in self.listOfProt:
			if ';' in i:
				ii = i.split(';')
				for iii in ii:
					self.text.AppendText(str(iii) + '\n')
			else:
				self.text.AppendText(str(i) + '\n')
	 #---
	 #--> Set pointer in the first line. Otherwise wx.TextCtrl is at the end of the text
		self.text.SetInsertionPoint(0)
	 #---
	 #--> Return
		return True
	 #---
	#---

	def DataForBandLane(self, df):
		""" Write details for a Spot in the gel
			---
			df: data frame with the data
		"""
	 #--> Variables
		fra  = str(df.shape[0])
		seqN = str(df['SeqN'].sum())
		seqL = ', '.join(list(map(str, df['SeqN'].tolist())))
		l = [tuple(x) for x in df.loc[:,['Nterm', 'Cterm']].values.tolist()]
		proR = '; '.join(list(map(str, l)))
		proRNat = dmethods.DHelperFragTuple2NatSeq(self, l)[1]
	 #---
	 #--> Write
		self.text.AppendText('--> Fragments: ' + fra + '\n\n')
		self.text.AppendText('--> Number of FP: ' + seqN + ' (' + seqL + ')'+'\n\n')
		self.text.AppendText('--> Detected protein regions:\n\n')
		self.text.AppendText('Recombinant protein:\n')
		self.text.AppendText(proR+'\n\n')
		self.text.AppendText('Native protein:\n')
		self.text.AppendText(proRNat+'\n')
	 #---
	 #--> Return
		return True
	 #---
	#---

	def DataForSingleBandLane(self, df):
		""" Details for a Lane/Band
			---
			df: data frame with the data
		"""
	 #--> Variables
	  #-->
		dV = {}
	  #---
	  #-->
		t = df.index.unique(level=0)
		dV['nBL_PN'] = str(len(t))
	  #---
	  #-->
		t = [int(x[1:]) for x in t]
		t.sort()
	  #---
	  #-->
		if self.TextM == 1:
			TLane = self.TextL - 1
			dV['nBL_T'] = str(len([y[TLane] for y in self.Results 
													if y[TLane][0] != None]))
			t = ['B'+str(x) for x in t]
		elif self.TextM == 2:
			TBand = self.TextB - 1
			dV['nBL_T'] = str(len([y for y in self.Results[TBand] 
														if y[0] != None]))			
			t = ['L'+str(x) for x in t]
		else:
			pass
	  #---
	  #-->
		dV['nBL_PL'] = ', '.join(t)
	  #---
	  #-->
		sl = []
		fl = []
		for b in t:
			dfb = df.loc[b]
			sl.append(dfb['SeqN'].sum())
			idx = dfb.index.unique().tolist()
			if self.TextM == 1:
				idx.sort()
				fl.append(idx[-1] + 1)
			elif self.TextM == 2:
				fl.append(idx[-1][-1] + 1)
			else:
				pass
		dV['nSeq']  = str(sum(sl))
		dV['nSeqL'] = ', '.join(list(map(str, sl)))
		dV['nFrag'] = str(sum(fl))
		dV['nFragL'] = ', '.join(list(map(str,fl)))
	  #---
	  #-->
		dV['ProtFrag'] = dmethods.DFGetFragments(df, self.name, strC=False)[1]
		dV['ProtFragN'] = dmethods.DHelperFragTuple2NatSeq(self, 
			dV['ProtFrag'])[1]
		dV['ProtFrag'] = '; '.join(list(map(str, dV['ProtFrag'])))
	  #---
	 #---
	 #--> Write
		if self.TextM == 1:
			self.text.AppendText('--> Analyzed Bands\n\n')
			self.text.AppendText("Total Bands  : " + dV['nBL_T'] + '\n')
			self.text.AppendText("Bands with FP: "
					+ dV['nBL_PN'] + " (" + dV['nBL_PL']  + ")" +'\n')
		elif self.TextM == 2:
			self.text.AppendText('--> Analyzed Lanes\n\n')
			self.text.AppendText("Total Lanes  : " + dV['nBL_T'] + '\n')
			self.text.AppendText("Lanes with FP: "
					+ dV['nBL_PN'] + " (" + dV['nBL_PL']  + ")" +'\n')
		self.text.AppendText("Fragments    : "
					+ dV['nFrag'] + " (" + dV['nFragL']  + ")" +'\n')
		self.text.AppendText("Number of FP : "
					+ dV['nSeq'] + " (" + dV['nSeqL']  + ")" +'\n\n')
		self.text.AppendText("--> Detected protein regions:\n\n")
		self.text.AppendText('Recombinant protein sequence:\n')
		self.text.AppendText(dV['ProtFrag']+'\n\n')
		self.text.AppendText('Native protein sequence:\n')
		self.text.AppendText(dV['ProtFragN']+'\n\n')
	 #---
     #--> Get back to first line
		self.text.SetInsertionPoint(0)
	 #---
	 #--> Return
		return True
	 #---
	#---
	#endregion -------------------------------------------------- Text Details
#---













