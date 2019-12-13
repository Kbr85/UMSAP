# ------------------------------------------------------------------------------
#	Copyright (C) 2017-2019 Kenny Bravo Rodriguez <www.umsap.nl>
	
#	This program is distributed for free in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
	
#	See the accompaning licence for more details.
# ------------------------------------------------------------------------------


""" This module creates the utility window of the app """


# ------------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Methods
# ------------------------------------------------------------------------------



#--- Imports
## Standard modules
import wx
## My modules
import config.config as config
import gui.gui_classes as gclasses 
#---



class WinUtil(gclasses.WinMyFrame):
	""" Creates the utility window of the application """
	
	def __init__(self, parent=None, style=None):
		""" parent: parent of the widgets
			style: style of teh windows
		"""
	 #--> initial Setup
		self.name = config.name['Util']
		super().__init__(parent=parent, style=style)
	 #--> Widgets
	  #--> Lines
		self.lineVI1 = wx.StaticLine(self.panel, style=wx.LI_VERTICAL)
	  #--> Images
		self.img = wx.StaticBitmap(self.panel, wx.ID_ANY, 
			wx.Bitmap(str(config.image['Util']), wx.BITMAP_TYPE_ANY))
	  #--> Static boxes
		self.boxLimProt = wx.StaticBox(self.panel, label='Limited Proteolysis')
		self.boxTarProt = wx.StaticBox(self.panel, label="Targeted Proteolysis")
		self.boxUtil    = wx.StaticBox(self.panel, label="General Utilities")
	  #--> Buttons
	   #--> LimProt
		self.buttonSeqH = wx.Button(self.boxLimProt,
			label='Sequence highlight')
	   #--> TarProt
		self.buttonAAdist     = wx.Button(self.boxTarProt, 
			label='AA distribution')
		self.buttonCutsPerRes = wx.Button(self.boxTarProt, 
			label='Cleavages per residue')
		self.buttonCuts2PDB   = wx.Button(self.boxTarProt, 
			label='Cleavages to PDB files')
		self.buttonFPL        = wx.Button(self.boxTarProt, 
			label='Filtered peptide list')
		self.buttonCreatehist = wx.Button(self.boxTarProt, 
			label='Histograms')
		self.buttonSeqAlign   = wx.Button(self.boxTarProt, 
			label='Sequence alignments')
		self.buttonUpdateTP   = wx.Button(self.boxTarProt, 
			label='Update results')
		self.buttonReaTP      = wx.Button(self.boxTarProt, 
			label='Custom update of results')
	   #--> General
		self.buttonCorrAnaly  = wx.Button(self.boxUtil, 
			label='Correlation analysis')
		self.buttonAAdistf    = wx.Button(self.boxUtil, 
			label='Merge aadist files')
		self.buttonCInputF    = wx.Button(self.boxUtil, 
			label='Create input file')
		self.buttonShortFile  = wx.Button(self.boxUtil, 
			label='Short data files')						
		self.buttonReadOut    = wx.Button(self.boxUtil, 
			label='Read output file')
		self.buttonRunScript  = wx.Button(self.boxUtil, 
			label='Run input file')
	 #--> Sizers
	  #--> LimProt
		self.sizerboxLimProt = wx.StaticBoxSizer(self.boxLimProt, wx.VERTICAL)
		self.sizerboxLimProt.Add(self.buttonSeqH,     border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)	
	  #--> Tarprot
		self.sizerboxTarProt = wx.StaticBoxSizer(self.boxTarProt, wx.VERTICAL)
		self.sizerboxTarProt.Add(self.buttonAAdist,     border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerboxTarProt.Add(self.buttonCutsPerRes, border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerboxTarProt.Add(self.buttonCuts2PDB,   border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerboxTarProt.Add(self.buttonFPL,        border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerboxTarProt.Add(self.buttonCreatehist, border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerboxTarProt.Add(self.buttonSeqAlign,   border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerboxTarProt.Add(self.buttonUpdateTP,   border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerboxTarProt.Add(self.buttonReaTP,      border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
	  #--> General
		self.sizerboxUtil = wx.StaticBoxSizer(self.boxUtil, wx.VERTICAL)
		self.sizerboxUtil.Add(self.buttonCorrAnaly, border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerboxUtil.Add(self.buttonCInputF,    border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerboxUtil.Add(self.buttonAAdistf,   border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)							
		self.sizerboxUtil.Add(self.buttonReadOut,   border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerboxUtil.Add(self.buttonRunScript, border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerboxUtil.Add(self.buttonShortFile,  border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)					
	  #--> All in statbox
		self.sizerStatBox = wx.GridBagSizer(1,1)
		self.sizerStatBox.Add(self.sizerboxLimProt, pos=(0,0), border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerStatBox.Add(self.sizerboxUtil,    pos=(1,0), border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerStatBox.Add(self.sizerboxTarProt, pos=(0,1), border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL, span=(2,0))
	  #--> All in sizerIn
		self.sizerIN.Add(self.sizerStatBox, pos=(0, 0), border=2, 
			flag=wx.ALIGN_CENTER|wx.ALL)
		self.sizerIN.Add(self.lineVI1,      pos=(0, 1), border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerIN.Add(self.img,          pos=(0, 2), border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
	  #-->
		self.sizer.Fit(self)
	 #--> Position
		self.Center()
	 #--> Bind
		self.buttonSeqH.Bind(wx.EVT_BUTTON, self.menubar.OnSeqH)
		self.buttonReadOut.Bind(wx.EVT_BUTTON, self.menubar.OnReadOutFile)
		self.buttonCutsPerRes.Bind(wx.EVT_BUTTON, self.menubar.OnCutProp)
		self.buttonCuts2PDB.Bind(wx.EVT_BUTTON, self.menubar.OnPDBfiles)
		self.buttonShortFile.Bind(wx.EVT_BUTTON, self.menubar.OnShortDFiles)
		self.buttonAAdist.Bind(wx.EVT_BUTTON, self.menubar.OnAAdist)
		self.buttonSeqAlign.Bind(wx.EVT_BUTTON, self.menubar.OnSeqAlign)
		self.buttonCreatehist.Bind(wx.EVT_BUTTON, self.menubar.OnHisto)
		self.buttonCorrAnaly.Bind(wx.EVT_BUTTON, self.menubar.OnCorrAnalysis)
		self.buttonAAdistf.Bind(wx.EVT_BUTTON, self.menubar.OnMergeAadist)
		self.buttonUpdateTP.Bind(wx.EVT_BUTTON, self.menubar.OnUpdateTP)
		self.buttonReaTP.Bind(wx.EVT_BUTTON, self.menubar.OnReanalyseTP)
		self.buttonCInputF.Bind(wx.EVT_BUTTON, self.menubar.OnCInputFile)
		self.buttonFPL.Bind(wx.EVT_BUTTON, self.menubar.OnFPList)
		self.buttonRunScript.Bind(wx.EVT_BUTTON, self.menubar.OnRInputFile)
	 #--> Tooltips
		self.buttonSeqH.SetToolTip(config.tooltip[self.name]['SeqH'])
		self.buttonAAdist.SetToolTip(config.tooltip[self.name]['AAdist'])
		self.buttonCutsPerRes.SetToolTip(config.tooltip[self.name]['CutPerRes'])
		self.buttonCuts2PDB.SetToolTip(config.tooltip[self.name]['Cuts2PDB'])
		self.buttonCInputF.SetToolTip(config.tooltip[self.name]['CInputFile'])
		self.buttonFPL.SetToolTip(config.tooltip[self.name]['FPList'])
		self.buttonCreatehist.SetToolTip(config.tooltip[self.name]['CHist'])
		self.buttonSeqAlign.SetToolTip(config.tooltip[self.name]['SeqAlign'])
		self.buttonShortFile.SetToolTip(config.tooltip[self.name]['ShortFile'])
		self.buttonCorrAnaly.SetToolTip(config.tooltip[self.name]['CorrA'])
		self.buttonAAdistf.SetToolTip(config.tooltip[self.name]['AAdistM'])
		self.buttonReadOut.SetToolTip(config.tooltip[self.name]['ReadOut'])
		self.buttonUpdateTP.SetToolTip(config.tooltip[self.name]['UpdateTP'])
		self.buttonReaTP.SetToolTip(config.tooltip[self.name]['ReadTP'])
		self.buttonRunScript.SetToolTip(config.tooltip[self.name]['RunScript'])
	 #-->
		self.Show()
	#---
#---

