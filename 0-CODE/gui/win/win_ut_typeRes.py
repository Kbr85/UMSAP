# ------------------------------------------------------------------------------
#	Copyright (C) 2017 Kenny Bravo Rodriguez <www.umsap.nl>
	
#	This program is distributed for free in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
	
#	See the accompaning licence for more details.
# ------------------------------------------------------------------------------


""" This module creates the window for typing the results columns in modules """


#region -------------------------------------------------------------- Imports
import wx
from pathlib import Path

import config.config      as config
import gui.menu.menu      as menu
import gui.gui_classes    as gclasses
import gui.gui_methods    as gmethods
import data.data_methods  as dmethods
import checks.checks_multiple as checkM
#endregion ----------------------------------------------------------- Imports


class WinTypeRes(gclasses.WinMyFrame, gclasses.GuiChecks):
	""" To create the gui for typing the results columns in a module """

	#region --------------------------------------------------- Instance Setup
	def __init__(self, parent, parentName=None, style=wx.DEFAULT_FRAME_STYLE):
		""" parent: parent of the widgets
			style: style of the window
		"""
	 #--> Initial Setup
	  #--> Variables
		self.parent = parent
		self.name   = config.name['TypeRes']
		self.CType  = None # To control the Control experiment display
		# eName is used to know which module will receive the exported data 
		if parentName == None:
			self.eName = self.parent.name
		else:
			self.eName = parentName
	  #---
 	  #--> Check that data file is defined
	   #--> Get the path first
		if self.parent.name == config.name['CorrARes']:
			self.dataFilePath = self.parent.fileObj.fileD
		else:
			self.dataFilePath = self.parent.tcDataFile.GetValue()
	   #---
	   #--> Check
		if checkM.CheckMFileRead(self.dataFilePath, config.extShort['Data']):
			pass
		else:
			msg   = config.dictElemDataFile[self.name]['MsgOpenFile']
			wcard = config.dictElemDataFile[self.name]['ExtLong']
			dlg   = gclasses.DlgOpenFile(msg, wcard)
			if dlg.ShowModal() == wx.ID_OK:
				self.dataFilePath = Path(dlg.GetPath())
			else:
				raise ValueError('')
	   #---
	  #---
	  #--> Finish initial setup
		self.title  = (config.title[self.name] 
			+ ' (' 
			+ config.mod[self.eName] 
			+ ')')
		super().__init__(parent=self.parent, title=self.title, style=style)
	  #---
	 #---
	 #--> Variables
		self.d  = {} # Needed to use the same g.classes.GuiChecks methods
		self.do = {}
		self.oldRes = [] # List with the column numbers read from Result field
		self.SetRowsColsTS = { # Configure the values of RowsT, RowsS, ColsT and ColsS for each module
			config.name['TarProt'] : self.SetRowsColsTSTarProt,
			config.name['LimProt'] : self.SetRowsColsTSLimProt,
			config.name['ProtProf']: self.SetRowsColsTSProtProf,		
		}
		self.CreateExtraWidgets = { # Create extra widgets for each module
			config.name['TarProt'] : self.CreateExtraWidgetsTarProt,
			config.name['LimProt'] : self.CreateExtraWidgetsLimProt,
			config.name['ProtProf']: self.CreateExtraWidgetsProtProf,				
		}		
		self.ConfigSizerRows = { # Configure the sizerRows and hide not needed widgets
			config.name['TarProt'] : self.ConfigSizersRowsTarProt,
			config.name['LimProt'] : self.ConfigSizersRowsLimProt,
			config.name['ProtProf']: self.ConfigSizersRowsProtProf,				
		}
		self.SetMyToolTip = { # Configure the tooltips
			config.name['TarProt'] : self.SetMyToolTipTarProt,
			config.name['LimProt'] : self.SetMyToolTipLimProt,
			config.name['ProtProf']: self.SetMyToolTipProtProf,					
		}
		self.MatrixWidget = { # To create and distribute the widgets in the matrix
			config.name['TarProt']  : self.MatrixWidgetTarProt,
			config.name['LimProt']  : self.MatrixWidgetLimProt,
			config.name['ProtProf'] : self.MatrixWidgetProtProf,
		}
		self.ReadRes = { # Read the value in tc.Results and set Rows and Cols
			config.name['TarProt'] : self.ReadResTarProt,
			config.name['LimProt'] : self.ReadResLimProt,
			config.name['ProtProf']: self.ReadResProtProt,			
		}
		self.ExportRes = { # Export the values to tc.Results
			config.name['TarProt'] : self.ExportResTarProt,
			config.name['LimProt'] : self.ExportResLimProt,
			config.name['ProtProf']: self.ExportResProtProf,			
		}
		self.EmptyWin = { # To set default variables if reading tcResults goes wrong 
			config.name['TarProt'] : self.EmptyWinTarProt,
			config.name['LimProt'] : self.EmptyWinLimProt,
			config.name['ProtProf']: self.EmptyWinProtProf,
		}	
	 #---	
	 #--> Menu
		self.menubar = menu.MainMenuBarWithTools(self.name)
		self.SetMenuBar(self.menubar)
	 #---
	 #--> Common Widgets
	  #--> Lines
		self.lineHI1 = wx.StaticLine(self.panel)
		self.lineHI2 = wx.StaticLine(self.panel)
		self.lineVI1 = wx.StaticLine(self.panel, style=wx.LI_VERTICAL)
	  #---
	  #--> TextCtrl
		self.tcRows = wx.TextCtrl(self.panel, value='', 
			size=config.size['TextCtrl'][self.name]['Rows'])
		self.tcCols = wx.TextCtrl(self.panel, value='', 
			size=config.size['TextCtrl'][self.name]['Rows'])
	  #---
	  #--> StaticText
		self.stRows = wx.StaticText(self.panel, 
			label=config.typeRes['labelRow'][self.eName])
		self.stCols = wx.StaticText(self.panel,
			label=config.typeRes['labelCol'][self.eName])
	  #---
	  #--> Buttons
		self.btnCreate = wx.Button(self.panel, label='Create matrix')
		self.btnOk     = wx.Button(self.panel, label='Export')
		self.btnCancel = wx.Button(self.panel, label='Cancel')
	  #---
	  #--> Listbox
		self.lb = wx.ListCtrl(self.panel, 
			size=config.size['ListBox'][self.name], 
			style=wx.LC_REPORT|wx.BORDER_SIMPLE)
		gmethods.ListCtrlHeaders(self.lb, self.name)
		gmethods.ListCtrlColNames(self.dataFilePath, self.lb, mode='file')
	  #---
	  #--> ScrolledWindow
		self.swMatrix = wx.ScrolledWindow(self.panel, 
			size=config.size['ScrolledW'][self.name])
		self.swMatrix.SetBackgroundColour('WHITE')
	  #---
	 #---
	 #--> Unique Widgets
		self.CreateExtraWidgets[self.eName]()
	 #---
	 #--> Sizers
	  #--> New sizers
		self.sizerRows = wx.FlexGridSizer(1,1,1,1)
		self.sizerOk   = wx.BoxSizer(wx.HORIZONTAL)
		self.sizerFlex = wx.FlexGridSizer(1,1,1,1)
	  #---
	  #--> Assign sizerFlex
		self.swMatrix.SetSizer(self.sizerFlex)
	  #---
	  #--> Add
	   #--> Rows	  
		self.ConfigSizerRows[self.eName]()
	   #---
	   #--> Ok
		self.sizerOk.AddMany([
			(self.btnCancel, 0, wx.ALIGN_CENTER|wx.ALL, 2),
			(self.btnOk,     0, wx.ALIGN_CENTER|wx.ALL, 2),
		]) 
	   #---	
	   #-->
		self.sizerIN.Add(self.sizerRows,  pos=(0,0), border=2, 
			flag=wx.ALIGN_CENTER|wx.ALL)
		self.sizerIN.Add(self.lineVI1,    pos=(0,1), border=2, span=(3,0),
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerIN.Add(self.lb,         pos=(0,2), border=2, span=(3,0),
			flag=wx.EXPAND|wx.ALIGN_TOP|wx.ALL)
		self.sizerIN.Add(self.lineHI1,    pos=(1,0), border=2,
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerIN.Add(self.swMatrix,   pos=(2,0), border=2,
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerIN.Add(self.lineHI2,    pos=(3,0), border=2, span=(0, 3),
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerIN.Add(self.sizerOk,    pos=(4,0), border=2, span=(0,3),
			flag=wx.ALIGN_RIGHT|wx.ALL)
	   #---
	  #---
	  #--> Fit
		self.sizer.Fit(self)
	  #---
	  #--> Grow Row/Col
		self.sizerIN.AddGrowableRow(2, 0)
		self.sizerIN.AddGrowableCol(0, 0)
	  #---
	 #---
     #--> Position
		self.Center()
		gmethods.MinSize(self)
	 #---
	 #--> Tooltips
	  #--> Common
		self.btnCancel.SetToolTip(config.tooltip[self.name]['Cancel'])
		self.btnOk.SetToolTip(config.tooltip[self.name]['Ok'])
		self.btnCreate.SetToolTip(config.tooltip[self.name]['Create'])
	  #---
	  #--> Unique
		self.SetMyToolTip[self.eName]()
	  #---
	 #---
	 #--> Bind
		self.btnCreate.Bind(wx.EVT_BUTTON, self.CreateM)
		self.btnCancel.Bind(wx.EVT_BUTTON, self.OnClose)
		self.btnOk.Bind(wx.EVT_BUTTON, self.OnExport)
		self.lb.Bind(wx.EVT_RIGHT_DOWN, self.OnPopUpMenu)
	 #---
	 #--> If Results has information fill swMatrix
	  #--> Get rows and cols
		try:
			oldRes = self.parent.tcResults.GetValue()
		except Exception:
			oldRes = ''
		if oldRes == '':
			pass
		else:
			out, self.oldRes = self.ReadRes[self.eName](oldRes)
			if out:
				self.CreateM('event')
			else:
				self.EmptyWin[self.eName]()
	  #---
	 #---
	 #--> Show
		self.Show()
	 #---
	#-->
	#endregion ------------------------------------------------ Instance Setup

	# ------------------------------------------------------------- My Methods
	#region ----------------------------------------------------- Bind Methods
	def OnClose(self, event):
		""" Destroy the window. Override parent class """
	 #--> Update config.win['TypeRes']
		del(config.win['TypeRes'][self.parent.name])
	 #---
	 #--> Set self.mID in parent for mod/util that can create several TypeRes windows
		try:
			self.parent.mID = None
		except Exception:
			pass
	 #---
	 #--> Destroy & Return	
		self.Destroy()
		return True
	 #---
	#---

	def CreateM(self, event):
		""" Creates the fields for the column numbers and the labels """
	 #--> Update self.CType
		try:
			self.CType = self.cbCType.GetValue()
		except Exception:
			self.CType = 'One Control'
	 #---
	 #--> Check Rows & Columns
			# RowsU user defined number of rows
			# RowsT number of rows having a wx.TextCtrl
			# RowsS number of rows needed in the sizer
			# ColsU user defined number of columns
			# ColsT number of columns having a wx.TextCtrl
			# ColsS number of columns needed in the sizer	  		 
	  #--> Rows        		
	   #-->
		minVal = str(config.typeRes['minValRow'][self.eName])
		msg = (config.typeRes['labelRow'][self.eName]
			+ ' ' 
			+ config.dictCheckFatalErrorMsg[self.name]['RowCol']
			+ '\n' 
			+ 'Minimum accepted value: ' 
			+ minVal
		)
	   #---
	   #-->
		if self.CheckGui1Number(self.tcRows,
			'RowsU',
			msg,
			t    = config.dictElemRowsCols['Rows']['t'],
			comp = config.dictElemRowsCols['Rows']['comp'],
			val  = config.typeRes['minValRow'][self.eName],
			NA   = config.dictElemRowsCols['Rows']['NA']
		):
			pass
		else:
			return False
	   #---
	  #---
	  #--> Cols
	   #-->
		minVal = str(config.typeRes['minValCol'][self.eName])
		msg = (config.typeRes['labelCol'][self.eName]
			+ ' ' 
			+ config.dictCheckFatalErrorMsg[self.name]['RowCol']
			+ '\n' 
			+ 'Minimum accepted value: ' 
			+ minVal
		)
	   #---
	   #-->
		if self.CheckGui1Number(self.tcCols,
			'ColsU',
			msg,
			t    = config.dictElemRowsCols['Rows']['t'],
			comp = config.dictElemRowsCols['Rows']['comp'],
			val  = config.typeRes['minValRow'][self.eName],
			NA   = config.dictElemRowsCols['Rows']['NA']	
		):
			pass
		else:
			return False
	   #---
	  #---
	  #--> Set RowsT, RowsS, ColsT and ColsS
		if self.SetRowsColsTS[self.eName]():
			pass
		else:
			return False
	  #---
	 #---
	 #--> Destroy old widgets and reset lists
		self.sizerFlex.Clear(delete_windows=True)
		self.rowLabels = []
		self.colLabels = []
		self.tcMatrix  = []
	 #---
	 #--> Create & distribute widgets
		self.MatrixWidget[self.eName]()
	 #---
	 #--> Sizer
	  #--> Fit & Keep the physical size of self.swMatrix
		self.sizerFlex.Fit(self.swMatrix)	
	  #---
	 #---
	 #--> Adjust the size & virtual size of swMatrix
	  #--> Sizer
		sFlexSize = self.sizerFlex.GetSize() # Size of the sizer containing the widgets
		sCellSize = self.sizerIN.GetCellSize(2,0) # Size of the cell containing swMatrix in sizerIn
		sCellSize[0] -= 4 # This the sum of hgap in sizerIn and the border 
		sCellSize[1] -= 4 # of the widgets
		w = sCellSize[0] - sFlexSize[0]
		h = sCellSize[1] - sFlexSize[1]
		if w < 0:
			w = sFlexSize[0]
		else:
			w = config.size['ScrolledW'][self.name][0]
		if h < 0:
			h = sFlexSize[1]
		else:
			h = config.size['ScrolledW'][self.name][1]
	  #---
	  #--> Configure swMatrix
		self.swMatrix.SetSize(sCellSize)
		self.swMatrix.SetVirtualSize(w, h)
		self.swMatrix.SetScrollRate(20, 20)
	  #---
	 #---
	 #--> Bind the wx.TextCtrl
		for i in range(0, len(self.tcMatrix), 1):
			self.tcMatrix[i].Bind(wx.EVT_ENTER_WINDOW, self.OnSetTooltip)		
	 #---
	 #--> Write values from Results field
		n = len(self.oldRes) 
		if n == 0:
			pass
		else:
			for i in range(0, n, 1):
				self.tcMatrix[i].SetValue(self.oldRes[i].strip())
			self.oldRes = []
	 #---
	 #--> Return
		return True
	 #---
	#---

	def OnSetTooltip(self, event):
		""" Set the tooltip of the wx.TextCtrl to see its content """
		tc = event.GetEventObject()
		tc.SetToolTip(tc.GetValue())
	#---

	def OnExport(self, event):
		""" Export the values for the wx.TextCtrl to the Results field in the
			parent window
		"""
	 #--> Check there are wx.TextCtrl to export
		try:
			self.tcMatrix
		except Exception:
			msg = config.dictCheckFatalErrorMsg[self.name]['NoExport']
			gclasses.DlgWarningOk(msg)
			return False
	 #---
	 #--> Check no mixing NA value
		l = []
		for i in self.tcMatrix:
			val = i.GetValue()
			vall = val.split()
			if 'NA' in vall and len(vall) > 1:
				msg = config.msg['Errors']['MixNA']
				msg += '\nMixed input: '
				msg += val
				gclasses.DlgFatalErrorMsg(msg)
				return False
			elif val == '':
				l.append(val)
			else:
				pass
	 #---
	 #--> Check that not all wx.TextCtrl are empty
		if len(l) == len(self.tcMatrix):
			msg = config.dictCheckFatalErrorMsg[self.name]['NoExport']
			gclasses.DlgWarningOk(msg)
			return False
		else:
			pass
	 #---
	 #--> Create the window of the module if comming from CorrARes
		if self.parent.name == config.name['CorrARes']:
			gmethods.WinMUCreate(self.eName)
		else:
			pass 
		self.eWin = config.win[self.eName]
	 #---
	 #--> Export
		if self.ExportRes[self.eName](self.eWin):
	  	 #--> Export data file path 
			self.eWin.tcDataFile.SetValue(str(self.dataFilePath))
		 #---
		 #--> Populate wx.ListBox in the module
			gmethods.ListCtrlColNames(
				self.dataFilePath, 
				self.eWin.lb, 
				mode='file'
			)
		 #---
		else:
			return False
			#--# Improve (UP)
	 #---
	 #--> Return
		self.OnClose(event)
		return True
	 #---
	#---
	#endregion -------------------------------------------------- Bind Methods

	#region ----------------------------------------------------- Menu Methods
	def OnLBoxCopy(self):
		""" Copy selected items in wx.ListBox to the clipboard """
	 #--> Check that something is selected
		sel = gmethods.ListCtrlGetSelected(self.lb)
		if len(sel) > 0:
			pass
		else:
			return True
	 #---
	 #--> Get data
		sel = gmethods.ListCtrlGetColVal(self.lb, sel=sel, t='str')
	 #---
	 #--> Create clipboard data
		clipdata = wx.TextDataObject()
		clipdata.SetText(' '.join(sel))
	 #---
	 #--> Copy to clipboard
		wx.TheClipboard.Open()
		wx.TheClipboard.SetData(clipdata)
		wx.TheClipboard.Close()	
	 #---
	#---

	def OnPopUpMenu(self, event):
		""" Pop up menu in wx.ListBox """
		self.PopupMenu(menu.ToolMenuTypeResults())
		return True	
	#---
	#endregion -------------------------------------------------- Menu Methods

	#region --------------------------------------------------- Unique Widgets
	def CreateExtraWidgetsTarProt(self):
		""" Creates unique widgets to the tarprot module
		"""
		return True
	#---

	def CreateExtraWidgetsLimProt(self):
		""" Creates unique widgets to the limprot module
		"""
		return True
	#---	

	def CreateExtraWidgetsProtProf(self):
		""" Creates unique widgets to the protprof module
		"""
	 #--> wx.StaticText
		self.stCondName = wx.StaticText(
			self.panel,
			label='Names:',
		)
		self.stCondNumber = wx.StaticText(
			self.panel,
			label='#:',
		)		
		self.stRPName = wx.StaticText(
			self.panel,
			label='Names:',
		)	
		self.stRPNumber = wx.StaticText(
			self.panel,
			label='#:',
		)			
		self.stControl = wx.StaticText(
			self.panel,
			label='Control:',
		)		
		self.stControlName = wx.StaticText(
			self.panel,
			label='Name:',
		)
		self.stControlType = wx.StaticText(
			self.panel,
			label='Type:',
		)	
	 #---
	 #--> wx.TextCtrl
		self.tcCondName = wx.TextCtrl(
			self.panel, 
			value='', 
			size=config.size['TextCtrl'][self.name]['Names']
		)		
		self.tcRPName = wx.TextCtrl(
			self.panel, 
			value='', 
			size=config.size['TextCtrl'][self.name]['Names']
		)
		self.tcControlName = wx.TextCtrl(
			self.panel, 
			value='', 
			size=config.size['TextCtrl'][self.name]['Rows']
		)
	 #---		
	 #--> wx.ComboBox
		self.cbCType = wx.ComboBox(
			self.panel, 
			value   = 'One Control',
			choices = config.combobox['ControlType'],
			style   = wx.CB_READONLY,
		)
	 #---
	 #-->
		return True
	 #---
	#---
	#endregion ------------------------------------------------ Unique Widgets	

	#region ---------------------------------------------- Set RowsT and RowsS
	def SetRowsColsTSTarProt(self):
		""" Set the values of RowsT, RowsS, ColsT and ColsS for the TarProt 
			module
			---
			RowsT is the number of rows with at least one wx.TextCtrl
			RowsS is the total number of rows in the sizer
			The same goes for ColsT and ColsS
		"""
		self.do['RowsT'] = self.do['RowsU'] + 1
		self.do['RowsS'] = self.do['RowsU'] + 1
		self.do['ColsT'] = self.do['ColsU']
		self.do['ColsS'] = self.do['ColsU'] + 1
		return True
	#---

	def SetRowsColsTSLimProt(self):
		""" Set the values of RowsT, RowsS, ColsT and ColsS for the LimProt 
			module
			---
			RowsT is the number of rows with at least one wx.TextCtrl
			RowsS is the total number of rows in the sizer
			The same goes for ColsT and ColsS
		"""
		self.do['RowsT'] = self.do['RowsU'] + 1
		self.do['RowsS'] = self.do['RowsU'] + 2
		self.do['ColsT'] = self.do['ColsU']
		self.do['ColsS'] = self.do['ColsU'] + 1 
		return True
	#---

	def SetRowsColsTSProtProf(self):
		""" Set the values of RowsT, RowsS, ColsT and ColsS for the ProtProf 
			module
			---
			RowsT is the number of rows with at least one wx.TextCtrl
			RowsS is the total number of rows in the sizer
			The same goes for ColsT and ColsS
		"""
		if (self.CType == config.combobox['ControlType'][0] or 
			self.CType == config.combobox['ControlType'][1]):
			self.do['RowsT'] = self.do['RowsU'] + 1
			self.do['RowsS'] = self.do['RowsU'] + 2
			self.do['ColsT'] = self.do['ColsU']
			self.do['ColsS'] = self.do['ColsU'] + 1 
			return True
		elif self.CType == config.combobox['ControlType'][2]:
			self.do['RowsT'] = self.do['RowsU']
			self.do['RowsS'] = self.do['RowsU'] + 1
			self.do['ColsT'] = self.do['ColsU'] + 1
			self.do['ColsS'] = self.do['ColsU'] + 2
			return True
		else:
			msg = 'Unknown Control Type options'
			gclasses.DlgFatalErrorMsg(msg)
			return False 			
	#---	
	#endregion ------------------------------------------- Set RowsT and RowsS

	#region --------------------------------------------- Configure sizersRows
	def ConfigSizersRowsTarProt(self):
		""" Configure the sizersRows for the TarProt module 
		"""
	 #--> Add widgets
		self.sizerRows.SetCols(4)
		self.sizerRows.AddMany([
			(self.stRows,    0, wx.ALIGN_CENTER|wx.ALL, 2),
			(self.tcRows,    0, wx.ALIGN_CENTER|wx.ALL, 2),
			(25, 0, 1),
			(self.btnCreate, 0, wx.ALIGN_CENTER|wx.ALL, 2),
		])	
	 #---
	 #--> Hide the ones not needed and set value for tcCols
		self.stCols.Hide()
		self.tcCols.Hide()
		self.tcCols.SetValue('1')
	 #---
	 #--> Return
		return True
	 #---
	#---

	def ConfigSizersRowsLimProt(self):
		""" Configure the sizersRows for the LimProt module
		"""
	 #--> Add widgets
		self.sizerRows.SetCols(7)
		self.sizerRows.AddMany([
			(self.stRows,    0, wx.ALIGN_CENTER|wx.ALL, 2),
			(self.tcRows,    0, wx.ALIGN_CENTER|wx.ALL, 2),
			(25, 0, 1),
			(self.stCols,    0, wx.ALIGN_CENTER|wx.ALL, 2),
			(self.tcCols,    0, wx.ALIGN_CENTER|wx.ALL, 2),
			(25, 0, 1),
			(self.btnCreate, 0, wx.ALIGN_CENTER|wx.ALL, 2),
		])
	 #---
	 #--> Return
		return True
	 #---
	#---	

	def ConfigSizersRowsProtProf(self):
		""" Configure the sizersRows for the ProtProf module 
		"""
	 #--> Add widgets
		self.sizerRows.SetRows(3)
		self.sizerRows.SetCols(8)
		self.sizerRows.AddMany([
			(self.stRows,    0, wx.ALIGN_RIGHT|wx.ALL, 2),
			(self.stCondNumber, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2),
			(self.tcRows,    0, wx.ALIGN_CENTER|wx.ALL, 2),
			(25, 0, 1),
			(self.stCondName, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2),
			(self.tcCondName, 0, wx.ALIGN_CENTER|wx.ALL, 2),
			(25, 0, 1),
			(25, 0, 1),
			(self.stCols,    0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2),
			(self.stRPNumber, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2),
			(self.tcCols,    0, wx.ALIGN_CENTER|wx.ALL, 2),
			(25, 0, 1),
			(self.stRPName, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2),
			(self.tcRPName, 0, wx.ALIGN_CENTER|wx.ALL, 2),
			(25, 0, 1),
			(self.btnCreate, 0, wx.ALIGN_CENTER|wx.ALL, 2),
			(self.stControl, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2),
			(self.stControlName, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2),
			(self.tcControlName, 0, wx.ALIGN_CENTER|wx.ALL, 2),
			(25, 0, 1),
			(self.stControlType, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 2),
			(self.cbCType,   0, wx.EXPAND|wx.ALIGN_CENTER|wx.ALL, 2),
			(25, 0, 1),
			(25, 0, 1),
		])
	 #---
	 #--> Return
		return True
	 #---
	#---
	#endregion ------------------------------------------ Configure sizersRows

	#region ------------------------------------------------- Set the tooltips
	def SetMyToolTipTarProt(self):
		""" Set the tooltips for the widgets created for module tarprot
		"""
		self.stRows.SetToolTip(
			config.tooltip[self.name][self.eName]['Experiments']
		)
		return True
	#---

	def SetMyToolTipLimProt(self):
		""" Set the tooltips for the widgets created for module tarprot
		"""
		self.stRows.SetToolTip(
			config.tooltip[self.name][self.eName]['Bands']
		)
		self.stCols.SetToolTip(
			config.tooltip[self.name][self.eName]['Lanes']
		)					
		return True
	#---

	def SetMyToolTipProtProf(self):
		""" Set the tooltips for the widgets created for module tarprot
		"""
		self.stRows.SetToolTip(
			config.tooltip[self.name][self.eName]['Conditions']
		)
		self.stCondName.SetToolTip(
			config.tooltip[self.name][self.eName]['ConditionsNa']
		)
		self.stCondNumber.SetToolTip(
			config.tooltip[self.name][self.eName]['ConditionsNu']
		)		
		self.stCols.SetToolTip(
			config.tooltip[self.name][self.eName]['RP']
		)	
		self.stRPName.SetToolTip(
			config.tooltip[self.name][self.eName]['RPNa']
		)
		self.stRPNumber.SetToolTip(
			config.tooltip[self.name][self.eName]['RPNu']
		)
		self.stControl.SetToolTip(
			config.tooltip[self.name][self.eName]['Control']
		)
		self.stControlName.SetToolTip(
			config.tooltip[self.name][self.eName]['ControlNa']
		)
		self.stControlType.SetToolTip(
			config.tooltip[self.name][self.eName]['ControlType']
		)		
		return True
	#---
	#endregion ---------------------------------------------- Set the tooltips

	#region ------------------------------- Create widgets and distribute them
	def CreateLabel(self, l, N, label, labelDef=None):
		""" Create static texts for the matrix 
			---
			l: list to hold the wx.StaticText
			N: number of labels to create (int)
			label : initial label text (string) or list of labels (list)
			labelDef: default value for label when N > label (string)
		"""
		if isinstance(label, str):
			for i in range(1, N+1, 1):
				l.append(wx.StaticText(
					self.swMatrix, 
					label = label + ' ' + str(i)
					)
				)
		elif isinstance(label, list):
			for i in range(1, N+1, 1):
				try:
					myLabel = label[i-1]
				except Exception:
					myLabel = labelDef + ' ' + str(i)
				l.append(wx.StaticText(
					self.swMatrix,
					label=myLabel
					)
				)
		return True
	#---

	def CreateLabelHelper(self, tc, l, N, labelDef):
		""" Configure labelR and labelDef and create the labels
			---
			tc: wx.TextCtrl to read the user names 
			l: list to store the wx.StaticText (list)
			N: number of wx.StaticText to create (int)
			labelDef: default values (str)
		"""
	 #-->
		val = tc.GetValue()
		if val == '':
			labelR = labelDef
			labelDefC = None	
		else:
			labelR = val.split(',')
			labelR = [x.strip() for x in labelR]
			labelDefC = labelDef
	 #---
	 #--> Create labels
		self.CreateLabel(l, N, labelR, labelDefC)
	 #---
	 #--> Return
		return True
	 #---
	#---

	def CreateTextCtrl(self, N):
		""" Create N wx.TextCtrl 
			---
			N number of wx.TextCtrl to create (int) 
		"""
		for i in range(0, N, 1):
			self.tcMatrix.append(wx.TextCtrl(
				self.swMatrix, 
				value='', 
				size=config.size['TextCtrl'][self.name]['Flex']
				)
			)
		return True
	#---

	def MatrixWidgetTarProt(self):
		""" Creates the widgets and distibute them for the TarProt module 
		""" 
	 #--> Labels
	  #--> Rows
		self.rowLabels.append(wx.StaticText(
			self.swMatrix, 
			label = 'Control'
			)
		)
		labelR = config.typeRes['labelRow'][self.eName][0:-1]
		self.CreateLabel(self.rowLabels, self.do['RowsU'], labelR)
	  #---
	  #--> Cols
		self.colLabels.append(0)
	  #---
	 #---
	 #--> TextCtrl	  
		self.CreateTextCtrl(self.do['RowsT'])
	 #---
	 #--> Sizers
	  #--> Configure
		self.sizerFlex.SetRows(self.do['RowsS'])
		self.sizerFlex.SetCols(self.do['ColsS']) 
	  #---
	  #--> Add	
		for i in range(0, self.do['RowsS'], 1):
			self.sizerFlex.Add(self.rowLabels[i], 0, wx.ALIGN_CENTER|wx.ALL, 2)
			self.sizerFlex.Add(self.tcMatrix[i],  0, wx.ALIGN_CENTER|wx.ALL, 2)
	  #---
	 #---
	 #--> Returns
		return True
	 #---
	#---

	def MatrixWidgetLimProt(self):
		""" Creates the widgets and distibute them for the LimProt module 
		""" 
	 #--> Labels
	  #--> Rows
		self.rowLabels.append(wx.StaticText(
			self.swMatrix, 
			label = 'Control'
			)
		)
		labelR = config.typeRes['labelRow'][self.eName][0:-1]
		self.CreateLabel(self.rowLabels, self.do['RowsU'], labelR)
	  #---
	  #--> Cols
		labelC = config.typeRes['labelCol'][self.eName][0:-1]
		self.CreateLabel(self.colLabels, self.do['ColsU'], labelC)
	  #---
	 #---
	 #--> TextCtrl	 
		self.CreateTextCtrl(self.do['RowsU']*self.do['ColsU']+1) 
	 #---
	 #--> Sizers
	  #--> Configure
		self.sizerFlex.SetRows(self.do['RowsS'])
		self.sizerFlex.SetCols(self.do['ColsS']) 
	  #---
	  #--> Add
		self.sizerFlex.Add(self.rowLabels[0], 0, wx.ALIGN_CENTER|wx.ALL, 2)
		self.sizerFlex.Add(self.tcMatrix[0], 0, wx.ALIGN_CENTER|wx.ALL, 2)
		for i in range(0, self.do['ColsU'], 1):
			self.sizerFlex.Add(0, 0, 0)
		for i in range(0, self.do['ColsU'], 1):
			self.sizerFlex.Add(self.colLabels[i], 0, wx.ALIGN_CENTER|wx.ALL, 2)
		j = 1
		for i in range(1, self.do['RowsU']+1, 1):
			self.sizerFlex.Add(self.rowLabels[i], 0, wx.ALIGN_CENTER|wx.ALL, 2)
			for _ in range(0, self.do['ColsU'], 1):
				self.sizerFlex.Add(
					self.tcMatrix[j], 0, wx.ALIGN_CENTER|wx.ALL, 2)
				j += 1
	  #---
	 #---
	 #--> Return
		return True
	 #---
	#---

	def MatrixWidgetProtProf(self):
		""" Creates the widgets and distribute them for the ProtProf module 
		"""
	 #--> Labels
	  #--> Control
	   #--> Control name and label
		val = self.tcControlName.GetValue()
		if val == '':
			labelC = 'Control'
		else:
			labelC = val
	   #---
	   #--> Control label in col or row
		if self.CType == config.combobox['ControlType'][2]:
			self.colLabels.append(wx.StaticText(
				self.swMatrix, 
				label = labelC
				)
			)
		else:
			self.rowLabels.append(wx.StaticText(
				self.swMatrix, 
				label = labelC
				)
			)
	   #---		
	  #---
	  #--> Rows
		self.CreateLabelHelper(
			self.tcCondName,
			self.rowLabels,
			self.do['RowsU'],
			config.typeRes['labelRow'][self.eName][0:-1],
		)
	  #---
	  #--> Cols
		self.CreateLabelHelper(
			self.tcRPName,
			self.colLabels,
			self.do['ColsU'],
			config.typeRes['labelCol'][self.eName][0:-1],
		)
	  #---
	 #---	
	 #--> wx.TextCtrl
		if self.CType == config.combobox['ControlType'][0]:
			self.CreateTextCtrl(self.do['RowsU']*self.do['ColsU']+1) 
		else:
			self.CreateTextCtrl(self.do['RowsT']*self.do['ColsT'])
	 #---
	 #--> Sizers
	  #--> Configure
		self.sizerFlex.SetRows(self.do['RowsS'])
		self.sizerFlex.SetCols(self.do['ColsS']) 		
	  #---
	  #--> Add
		if self.CType == config.combobox['ControlType'][0]:
			self.sizerFlex.Add(self.rowLabels[0], 0, wx.ALIGN_CENTER|wx.ALL, 2)
			self.sizerFlex.Add(self.tcMatrix[0], 0, wx.ALIGN_CENTER|wx.ALL, 2)
			for i in range(0, self.do['ColsU'], 1):
				self.sizerFlex.Add(0, 0, 0)
			for i in range(0, self.do['ColsU'], 1):
				self.sizerFlex.Add(
					self.colLabels[i], 0, wx.ALIGN_CENTER|wx.ALL, 2)
			j = 1
			for i in range(1, self.do['RowsU']+1, 1):
				self.sizerFlex.Add(
					self.rowLabels[i], 0, wx.ALIGN_CENTER|wx.ALL, 2)
				for _ in range(0, self.do['ColsU'], 1):
					self.sizerFlex.Add(
						self.tcMatrix[j], 0, wx.ALIGN_CENTER|wx.ALL, 2)
					j += 1
		elif (self.CType == config.combobox['ControlType'][1] or 
			self.CType == config.combobox['ControlType'][2]):
			self.sizerFlex.Add(0, 0, 0)
			for i in self.colLabels:
				self.sizerFlex.Add(i, 0, wx.ALIGN_CENTER|wx.ALL, 2)
			j = 0
			for i in self.rowLabels:
				self.sizerFlex.Add(i, 0, wx.ALIGN_CENTER|wx.ALL, 2)
				for _ in range(1, self.do['ColsS'], 1):
					self.sizerFlex.Add(
						self.tcMatrix[j], 0, wx.ALIGN_CENTER|wx.ALL, 2)
					j += 1
		else:
			msg = 'Unknown Control Type options'
			gclasses.DlgFatalErrorMsg(msg)
			return False 
	  #---
	 #---	
	 #--> Return
		return True
	 #---
	#---
	#endregion ---------------------------- Create widgets and distribute them

	#region Configure Rows and Cols and values to write when there is something in tc.Results
	def ReadResTarProt(self, l):
		""" Configure Rows, Cols for TarProt 
			---
			l: value of tc.Results as a string
		"""
	 #--> Get nRows
		oldRes = l.split(';')
		ll = len(oldRes)
		if ll > 1:
			self.tcRows.SetValue(str(len(oldRes)-1))
		elif ll == 1:
			self.tcRows.SetValue(str(1))
		else:
			return [False, []]
	 #---
	 #--> Return
		return [True, oldRes]
	 #---
	#---

	def ReadResLimProt(self, l):
		""" Configure Rows and Cols for LimProt 
			---
			l: value of tc.Results as a string
		"""
	 #--> Get nRows
		oldRes = l.split(';')
		ll = len(oldRes)
		if ll > 1:
			self.tcRows.SetValue(str(len(oldRes)-1))
		else:
			return [False, []]
	 #---
	 #-->  Get nCols
		oldRes = [x.split(',') for x in oldRes]
	  #--> Check that each row has the same number of columns
		nCols = len(list(set([len(x) for x in oldRes])))
		if nCols == 1: # Only 1 Lane
			self.tcCols.SetValue(str(1))
		elif nCols == 2: # Several lanes per band
			self.tcCols.SetValue(str(len(oldRes[1])))
		else:
			return [False, []]
	  #---
	 #--- 
	 #--> Flat res list
		oldRes = dmethods.ListFlatNLevels(oldRes)[1]
	 #---
	 #--> Return
		return [True, oldRes]
	 #---
	#---

	def ReadResProtProt(self, l):
		""" Configure Rows and Cols for LimProt 
			---
			l: value of tc.Results as a string
		"""
	 #--> Check if parent.Ctype is defined
		if self.parent.CType == None:
			return [False, []]	
		else:
			self.CType = self.parent.CType
	 #---
	 #--> Get labels
		if self.parent.LabelCond != None:
			self.tcCondName.SetValue(', '.join(self.parent.LabelCond))
		else:
			pass
		if self.parent.LabelControl != None:
			self.tcControlName.SetValue(self.parent.LabelControl)
		else:
			pass		
		if self.parent.LabelRP != None:
			self.tcRPName.SetValue(', '.join(self.parent.LabelRP))
		else:
			pass		
	 #---
	 #--> Get nRows
		oldRes = l.split(';')
		ll = len(oldRes)
		if self.CType == config.combobox['ControlType'][2]:
			self.tcRows.SetValue(str(ll))
		else:
			self.tcRows.SetValue(str(ll - 1))
	 #---
	 #--> Get nCols
		oldRes = [x.split(',') for x in oldRes]
	  #--> Check that each row has the same number of columns
		nCols = len(list(set([len(x) for x in oldRes])))
		if nCols == 1:
			pass
		else:
			return [False, []] 
	  #---
	  #-->
		if self.CType == config.combobox['ControlType'][2]:
			self.tcCols.SetValue(str(len(oldRes[0]) - 1))
		else:
			self.tcCols.SetValue(str(len(oldRes[1])))		
	 #---
	 #--> Flat res list
		oldRes = dmethods.ListFlatNLevels(oldRes)[1]
	 #---
	 #--> Set the value of the combobox
		self.cbCType.SetValue(self.CType)
	 #---
	 #--> Return
		return [True, oldRes]
	 #---
	#---
	#endregion Configure Rows and Cols and values to write when there is something in tc.Results

	#region --------------- Set default values if reading rcresults goes wrong
	def EmptyWinTarProt(self):
		""" Set default values if reading rcResults goes wrong 
		"""
		self.tcRows.SetValue('')
		return True
	#---

	def EmptyWinLimProt(self):
		""" Set default values if reading rcResults goes wrong 
		"""
		self.tcRows.SetValue('')
		self.tcCols.SetValue('')
		return True
	#---

	def EmptyWinProtProf(self):
		""" Set default values if reading rcResults goes wrong 
		"""
		self.tcRows.SetValue('')
		self.tcCols.SetValue('')
		self.CType = 'One Control'
		self.tcCondName.SetValue('')
		self.tcControlName.SetValue('')
		self.tcRPName.SetValue('')
		return True
	#---
	#endregion Configure Rows and Cols and values to write when there is something in tc.Results

	#region ----------------- Export data to tc.Results, see description below
	 # This methods will export a matrix with the input column numbers as values:

	 # 		Control Y1 ... Ym
	 # X1
	 # X2
	 # Xn
	
	 # For all modules and control designs the data is arranged to this matrix.
	 # Therefore, the meaning of X and Y will change.

	def ExportResTarProt(self, eWin):
		""" Export the typed results to tc.Results in the tarprot module 
			---
			eWin: reference to the window importing the data
		"""
	 #--> Get string
		myRes = self.ExportMatrix()[1]
	 #---
	 #--> Set eWin.tc
		eWin.tcResults.SetValue(myRes)
	 #---
	 #--> Return
		return True
	 #---
	#---

	def ExportResLimProt(self, eWin):
		""" Export the typed results to tc.Results in the limprot module 
			---
			eWin: reference to the window importing the data
		"""
	 #--> Get string
		myRes = self.tcMatrix[0].GetValue() + '; '
		myRes = myRes + self.ExportMatrix(s=1, r=1)[1]
	 #---
	 #--> Set eWin.tc
		eWin.tcResults.SetValue(myRes)
	 #---
	 #--> Return
		return True
	 #---
	#---

	def ExportResProtProf(self, eWin):
		""" Export the typed results to tc.Results in the protprof module 
			---
			eWin: reference to the window importing the data
		"""
	 #--> Get string
		if self.CType == config.combobox['ControlType'][0]:
			myRes = self.tcMatrix[0].GetValue() + '; '
			s = r = 1
		else:
			myRes = ''
			s = r = 0
		#-->
		myRes = myRes + self.ExportMatrix(s=s, r=r)[1]
	 #---
	 #--> Set eWin.tc
		eWin.tcResults.SetValue(myRes)
	 #---
	 #--> Export value of self.CType
		eWin.CType = self.CType
	 #---
	 #--> Export names
		if self.CType == config.combobox['ControlType'][2]:
			eWin.LabelControl = self.colLabels[0].GetLabel()
			eWin.LabelRP      = [x.GetLabel() for x in self.colLabels[1:]]
			eWin.LabelCond    = [x.GetLabel() for x in self.rowLabels]
		else:
			eWin.LabelControl = self.rowLabels[0].GetLabel()
			eWin.LabelCond    = [x.GetLabel() for x in self.rowLabels[1:]]			
			eWin.LabelRP      = [x.GetLabel() for x in self.colLabels]
	 #---
	 #--> Return
		return True
	 #---
	#---

	def ExportMatrix(self, s=0, r=0):
		""" Export rectangular matrix
			---
			s: index in self.tcMatrix list for the first element to get the 
				value from (int)
			r: number of rows to substract from self.do['RowsT] to get the rows 
				in the rectangular matrix (int)
		"""
	 #-->
		myRes = ''
		for i in range(0, self.do['RowsT']-r, 1): # Loop Rows in the rectangular matrix
			for j in range(0, self.do['ColsT'], 1): # Loop Cols in the rectangular matrix
				val = self.tcMatrix[s].GetValue().strip()
				if val == '':
					val = 'NA'
				else:
					pass
				myRes = myRes + val + ', '
				s += 1
			myRes = myRes[0:-2]
			myRes = myRes + '; '
		myRes = myRes[0:-2]
	 #---
	 #--> Return
		return [True, myRes]
	 #---
	#---
	#endregion -------------- Export data to tc.Results, see description below
#---