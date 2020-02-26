# ------------------------------------------------------------------------------
#	Copyright (C) 2017-2019 Kenny Bravo Rodriguez <www.umsap.nl>
	
#	This program is distributed for free in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
	
#	See the accompaning licence for more details.
# ------------------------------------------------------------------------------


""" This module contains the base classes for the GUI of the app """


# ------------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Methods
# ------------------------------------------------------------------------------



#--- Imports
## Standard modules
import wx
import wx.lib.dialogs
import webbrowser
import _thread
import pandas as pd
import matplotlib as mpl
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.widgets import Cursor
from pathlib import Path
## My modules
import config.config          as config
import gui.menu.menu          as menu
import gui.gui_methods        as gmethods
import data.data_classes      as dclasses
import data.data_methods      as dmethods
import checks.checks_multiple as checkM
import checks.checks_single   as check
#---



# ----------------------------------------------------------- GUI ELEMENTS
class ElementHelpRun():
	""" A sizer with the Help and Start buttoms. Between the buttons there is a 
		static text and below the text a gauge. """

	def __init__(self, parent, length=25):
		""" parent: parent of the widgets
			length: length of the gauge
		"""
	  #--> Widgets
	   #--> StaticText
		self.stProgress = wx.StaticText(
			parent, 
			label='', 
			style=wx.ALIGN_LEFT
		)
	   #--> Button
		self.buttonHelp = wx.Button(
			parent, 
			label=config.dictElemHelpRun['Help']
		)
		self.buttonRun = wx.Button(
			parent, 
			label=config.dictElemHelpRun['Run']
		)
	   #--> Gauge
		self.gauge = wx.Gauge(parent=parent, range=length)
		self.gauge.SetValue(0)
	  #--> Sizers
	   #--> New sizers
		self.sizerBottom = wx.GridBagSizer(1, 1)
	   #--> Add elements
		self.sizerBottom.Add(self.buttonHelp, pos=(0, 0), 
			border=2, 
			flag=wx.ALIGN_LEFT|wx.ALL)
		self.sizerBottom.Add(self.stProgress, pos=(0, 1), 
			border=2, 
			flag=wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
		self.sizerBottom.Add(self.buttonRun,  pos=(0, 2), 
			border=2, 
			flag=wx.ALIGN_RIGHT|wx.ALL)
		self.sizerBottom.Add(self.gauge,      pos=(1, 0), span=(0, 3),
			border=2, 
			flag=wx.EXPAND|wx.ALIGN_LEFT|wx.ALL)
	   #--> Grow able columns
		self.sizerBottom.AddGrowableCol(1, 1)
	  #--> Tooltips
		self.buttonRun.SetToolTip(config.tooltip['HelpRun']['Run'])
		self.buttonHelp.SetToolTip(config.tooltip['HelpRun']['Help'])
	  #--> Bind
		self.buttonHelp.Bind(wx.EVT_BUTTON, self.OnHelp)
		self.buttonRun.Bind(wx.EVT_BUTTON, self.OnRun)
	#---

	####---- Methods of the class
	def OnHelp(self, event):
		""" Default behavior of Help button: go to UMSAP v2.1 tutorial """
		webbrowser.open_new(config.url['Tutorial'])
		return True
	#---

	def OnRun(self, event):
		""" Start the data processing in a separate thread """
		self.buttonRun.Disable()
		self.buttonRun.SetLabel('Running')
		self.runEnd = False
		_thread.start_new_thread(self.run, ('test',))
		return True
	#---

	def run(self, test):
		""" Analyse the data and generate the results """
	  #--> Variables
		self.dateN = dmethods.DateTimeNow()	
		self.d  = {}
		self.do = {}
	  #--> Check input
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Checking user input', 2)
		if self.CheckInput():
			pass
		else:
			wx.CallAfter(self.Checkrun)
			return False
	  #--> Start analysis
	  #--> Read input files
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Reading files', 2)		
		if self.ReadInputFiles():
			pass
		else:
			wx.CallAfter(self.Checkrun)
			return False
	  #--> Set initial variables
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Setting variables', 2)		
		if self.SetVariable():
			pass
		else:
			wx.CallAfter(self.Checkrun)
			return False
	  #--> Run the analysis
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Running analysis', 2)
		if self.RunAnalysis():
			pass
		else:
			wx.CallAfter(self.Checkrun)
			return False
	  #--> Write the output
		wx.CallAfter(gmethods.UpdateGaugeText, self.gauge, self.stProgress,
			'Writing output', 2)
		if self.WriteOF():
			pass
		else:
			wx.CallAfter(self.Checkrun)
			return False
	  #--> Call Checkrun to launch Show Results from the main thread
		self.runEnd = True
		wx.CallAfter(self.Checkrun)
	  #--> Return
		return True
	#---

	def Checkrun(self):
		""" Check if the thread finished correctly. Runs from the main thread """
	  #--> Check if self.run finished ok
		if self.runEnd:
	  #--> Show graphic output. Needs to be from main thread in macOS
			if self.ShowRes():
				DlgSuccessMsg()
			else:
				pass
		else:
			pass
	  #--> Restore module initial state 
		self.stProgress.SetLabel('')
		self.gauge.SetValue(0)
		self.buttonRun.Enable()
		self.buttonRun.SetLabel(config.dictElemHelpRun['Run'])
		self.runEnd = False
		self.overW = False
	  #--> Return
		return True
	#---

	####---- Dummy methods to avoid errors when method not needed. 
	#		 Override as needed
	def CheckInput(self):
		""" Check the user provided input """
		return True
	#---

	def ReadInputFiles(self):
		""" Read the files and creates the dataObjects """
		return True
	#---

	def SetVariable(self):
		""" Set extra needed variables """
		return True
	#---

	def RunAnalysis(self):
		""" Run the analysis """
		return True
	#---

	def WriteOF(self):
		""" Write the output """
		return True
	#---

	def ShowRes(self):
		""" Show graphical output """
		return True
	#---
#---

class ElementClearAFVC():
	""" Clear buttons in the left of the modules. It is assume that a 
		wx.StaticBox with wx.TextCtrl for Files, Values and Columns exists and 
		the clear methods will set the value of the wx.TextCtrl to '' 
	"""

	def __init__(self, parent):
		""" parent: parent of the class """
	  #--> Variables
		self.parent = parent
	  #--> Widgets
	   #--> Button
		self.buttonClearAll     = wx.Button(parent, label='Clear all')
		self.buttonClearFiles   = wx.Button(parent, label='Clear files')
		self.buttonClearValues  = wx.Button(parent, label='Clear values')
		self.buttonClearColumns = wx.Button(parent, label='Clear columns')
	  #--> Sizer
	   #--> New sizers
		self.sizerClear = wx.BoxSizer(wx.VERTICAL)
	   #--> Add Elements
		self.sizerClear.Add(self.buttonClearAll,     
			border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerClear.Add(self.buttonClearFiles,   
			border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerClear.Add(self.buttonClearValues,  
			border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerClear.Add(self.buttonClearColumns, 
			border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
	  #--> Tooltips
		self.buttonClearAll.SetToolTip(config.tooltip['Clear']['All'])
		self.buttonClearFiles.SetToolTip(config.tooltip['Clear']['Files'])
		self.buttonClearValues.SetToolTip(config.tooltip['Clear']['Values'])
		self.buttonClearColumns.SetToolTip(config.tooltip['Clear']['Cols'])
	  #--> Bind
		self.buttonClearFiles.Bind(wx.EVT_BUTTON, self.OnClearFiles)
		self.buttonClearValues.Bind(wx.EVT_BUTTON, self.OnClearValues)
		self.buttonClearColumns.Bind(wx.EVT_BUTTON, self.OnClearColumns)
		self.buttonClearAll.Bind(wx.EVT_BUTTON, self.OnClearAll)
	#---

	####---- Methods of the class
	def OnClearFiles(self, event):
		""" Set the value of all wx.TextCtrl in a wx.StaticBox to ''. Override
			as needed 
		"""
		gmethods.TextCtrlEmpty(self.boxFiles)
		#--> Perform other actions depending on the specific window
		self.OnClearFilesDef() 
		return True
	#---

	def OnClearFilesDef(self):
		""" To restore default values after deleting or something else.
			Override as needed. 
		"""
		pass
	#---

	def OnClearValues(self, event):
		""" Set the value of all wx.TextCtrl in a wx.StaticBox to ''. 
			Override as needed 
		"""
		gmethods.TextCtrlEmpty(self.boxValues)
		#--> Perform other actions depending on the specific window
		self.OnClearValuesDef()
		return True
	#---

	def OnClearValuesDef(self):
		""" To restore default values after deleting or something else.
			Override as needed 
		"""
		pass
	#---

	def OnClearColumns(self, event):
		""" Set the value of all wx.TextCtrl in a wx.StaticBox to ''. 
			Override as needed 
		"""
		gmethods.TextCtrlEmpty(self.boxColumns)
		#--> Perform other actions depending on the specific window
		self.OnClearColumnsDef()
		return True
	#---

	def OnClearColumnsDef(self):
		""" To restore default values after deleting or something else.
			Override as needed 
		"""
		pass
	#---		

	def OnClearAll(self, event):
		""" Clears all sections in the modules """
		self.OnClearFiles(event)
		self.OnClearValues(event)
		self.OnClearColumns(event)
		return True
	#---
#---

class ElementClearAF(ElementClearAFVC):
	""" Clear all and Clear files buttons in the left of the module. """
	
	def __init__(self, parent):
		""" parent: parent of the widgets """

		super().__init__(parent=parent)
	  #--> Widgets
	   #--> Buttons
		self.buttonClearValues.Destroy()
		self.buttonClearColumns.Destroy()
	#---

	####---- Methods of the class
	def OnClearAll(self, event):
		""" Override to ElementClearAFVC """
		self.OnClearFiles(event)
		return True
	#---
#---

class ElementClearAFV(ElementClearAFVC):
	""" Clear values button in the left of the module. """
	
	def __init__(self, parent):
		""" parent: parent of the widgets """

		super().__init__(parent)
	  #--> Widgets
	   #--> Button
		self.buttonClearColumns.Destroy()
	#---

	####---- Methods of the class
	def OnClearAll(self, event):
		""" Override to ElementClearAFVC """
		self.OnClearFiles(event)
		self.OnClearValues(event)
		return True
	#---
#---

class ElementClearAFC(ElementClearAFVC):
	""" Clear column button in the left of the module """
	
	def __init__(self, parent):
		""" parent: parent of the widgets """

		super().__init__(parent)
	  #--> Widgets
	   #--> Buttons
		self.buttonClearValues.Destroy()
	#---

	####---- Methods of the class
	def OnClearAll(self, event):
		""" Override to ElementClearAFVC """
		self.OnClearFiles(event)
		self.OnClearColumns(event)
		return True
	#---
#---

class ElementDataFile():
	""" Creates the button and text ctrl for the data file in modules and 
		utilities 
	"""

	def __init__(self, parent):
		""" parent: parent of the widgets """
	
	  #--> Widgets
	   #--> Buttons
		self.buttonDataFile = wx.Button(parent=parent, 
			label=config.dictElemDataFile[self.name]['ButtonLabel'])
	   #--> TextCtrl
		self.tcDataFile = wx.TextCtrl(parent=parent, value="", 
			size=config.size['TextCtrl']['DataFile'])
	  #--> Tooltips
		self.buttonDataFile.SetToolTip(
			config.dictElemDataFile[self.name]['ButtonTooltip'])
	  #--> Bind
		self.buttonDataFile.Bind(wx.EVT_BUTTON, self.OnDataFile)
		if config.dictElemDataFile[self.name]['BindEnter']:
			self.tcDataFile.Bind(wx.EVT_CHAR_HOOK, self.OnDataInputEnter)
		else:
			pass
	#---

	####---- Methods of the class
	def OnDataFile(self, event):
		""" Select the data file and fill the list box """
	  #--> Variables
		k     = True
		msg   = config.dictElemDataFile[self.name]['MsgOpenFile']
		wcard = config.dictElemDataFile[self.name]['ExtLong']
	  #--> Open File & Fill/Empty wx.ListBox
		dlg = DlgOpenFile(msg, wcard)
		if dlg.ShowModal() == wx.ID_OK:
			#--> Put path in wx.TextCtrl
			self.tcDataFile.SetValue(dlg.GetPath())
			#--> Fill wx.ListBox if needed
			if config.dictElemDataFile[self.name]['FillListCtrl']:
				if gmethods.ListCtrlColNames(dlg.GetPath(), self.lb, 
					mode='file'):
					#--> Empty second wx.ListBox if needed
					go = (
					  config.dictElemDataFile[self.name]['EmptySecondListCtrl'])
					if go: 
						self.lbo.DeleteAllItems()
						self.lboE = []
					else:
						pass
				else:
					k = False
			else:
				pass
		else:
			k = False
	  #--- Destroy & Return
		dlg.Destroy()
		return k
	#---

	def OnDataInputEnter(self, event):
		""" Enter Key Action on the wx.TexTCtrl with the data file path """
	  #--> Process enter key stroke
		if event.GetKeyCode() == wx.WXK_RETURN:		
	   #--> Get file path
			file = self.tcDataFile.GetValue()
	   #--> Check file can be read
			if checkM.CheckMFileRead(file,  
					config.dictElemDataFile[self.name]['ExtShort']):
	   #--> Fill first wx.ListBox
				if config.dictElemDataFile[self.name]['FillListCtrl']:
					if gmethods.ListCtrlColNames(file, self.lb, mode='file'):
	   #--> Empty second wx.ListBox if needed
						go = (
					  	config.dictElemDataFile[self.name]['EmptySecondListCtrl'])
						if go: 
							self.lbo.DeleteAllItems()
							self.lboE = []
						else:
							pass
					else:
						return False
				else:
					pass
			else:
				msg = config.dictCheckFatalErrorMsg[self.name]['Datafile']
				DlgFatalErrorMsg(msg)
				return False
		else:
			pass
	  #--> Skip event & Return
		event.Skip()
		return True
	#---
#---

class ElementOutputFileFolder():
	""" Creates the button and text ctrl for the output file or folder in 
		modules and utilities 
	"""
	
	def __init__(self, parent):
		""" parent: parent of the widgets """
	  #--> Variables
		self.overW = False
	  #--> Widgets
	   #--> Buttons
		self.buttonOutputFF = wx.Button(parent=parent, 
			label=config.dictElemOutputFileFolder[self.name]['ButtonLabel'])
	   #--> TextCtrl
		self.tcOutputFF = wx.TextCtrl(parent=parent, value="", 
			size=config.size['TextCtrl']['OutputFF'])
	  #--> Tooltips
		msg = (config.dictElemOutputFileFolder[self.name]['ButtonTooltip']
			+ config.msg['OptVal'])
		self.buttonOutputFF.SetToolTip(msg)
	  #--> Bind
		if config.dictElemOutputFileFolder[self.name]['FolderOrFile']:
			self.buttonOutputFF.Bind(wx.EVT_BUTTON, self.OnOutputFolder)
		else:
			self.buttonOutputFF.Bind(wx.EVT_BUTTON, self.OnOutputFile)
	   #--> Conditional Binding 
		temp = 'Output file'
		if config.dictElemOutputFileFolder[self.name]['ButtonLabel'] == temp:
			self.tcOutputFF.Bind(wx.EVT_TEXT, self.OnTextChange)
		else:
			pass
	  #--> Default values
		if config.dictElemOutputFileFolder[self.name]['NA']:
			self.tcOutputFF.SetValue('NA')
		else:
			pass
	#---

	####---- Methods of the class
	def OnTextChange(self, event):
		""" Set self.overW = False if the user change the path to the file """
		self.overW = False
		return True
	#---

	def OnOutputFolder(self, event):
		""" Select the output folder to save the generated data """
		if gmethods.TextCtrlFromFF(self.tcOutputFF, mode='folder'):
			return True
		else:
			return False
	#---

	def OnOutputFile(self, event):
		""" Select the output file to save the generated data """
		if gmethods.TextCtrlFromFF(self.tcOutputFF, 
			wcard=config.dictElemOutputFileFolder[self.name]['ExtLong'],
			mode='save'):
			#--> If the user select to overwrite the output file then you overwrite the output file
			self.overW = True
			return True
		else:
			return False
	#---
#---

class ElementResults():
	""" To create the Results widgets, tooltips and methods """
	
	def __init__(self, parent):
		""" parent: parent of the widgets 
		"""
	 #--> Variables
		self.MyOptHandler = { # To handle loading a file with options
			config.name['ProtProf'] : self.MyOptHandlerProtProf,
		}
	 #--> Widgets
	  #--> TextCtrl
		self.tcResults = wx.TextCtrl(
			parent=parent, 
			value="", 
			size=config.size['TextCtrl'][self.name]['tcResults']
		)
	  #--> StaticText
		self.stResults = wx.StaticText(
			parent=parent, 
			label="Results - Control experiments", 
			style=wx.ALIGN_RIGHT
		)		
	  #--> Buttons
		self.buttonResultsW = wx.Button(parent=parent, label='Type values')
		self.buttonResultsL = wx.Button(parent=parent, label='Load values')	
	 #--> Tooltips
		self.stResults.SetToolTip(config.tooltip[self.name]['Results'])
		self.buttonResultsW.SetToolTip(config.tooltip[self.name]['ResultsW'])
		self.buttonResultsL.SetToolTip(config.tooltip[self.name]['ResultsL'])
	 #--> Bind
		self.buttonResultsW.Bind(wx.EVT_BUTTON, self.OnResW)
		self.buttonResultsL.Bind(wx.EVT_BUTTON, self.OnResL)			
	#---

	####---- Methods of the class
	def OnResW(self, event):
		""" Open the win_ut_typeRes window to write the results columns. """
		#--# Improve Should read the value of self.tcResults and show it with
		# with the correct format
		try:
			gmethods.WinTypeResCreate(config.name['TypeRes'], self)
		except Exception:
			pass
		return True
	#---

	def OnResL(self, event):
		""" Load the results from a text file """
	 #--> Variables
		k = True
	 #--> Open file
		dlg = DlgOpenFile(
			config.dictElemDataFile2[self.name]['MsgOpenFile'],
			config.dictElemDataFile2[self.name]['ExtLong'])
	 #--> If file selected 
		if dlg.ShowModal() == wx.ID_OK:
	 #--> Read file		
			lines = dmethods.FFsRead(dlg.GetPath(), char=None)
	 #--> Create string
			myRes = ''
			myOpt = {}
			for l in lines:
				if ':' in l[0]:
					k, v = [x.strip() for x in l[0].split(':')]
					myOpt[k] = v						
				else:
					myRes = (
						myRes 
						+ ', '.join([x.strip() for x in l[0].split(',')])
					)
					myRes = myRes + '; '
			myRes = myRes[0:-2]
	 #--> Place string
			self.tcResults.SetValue(myRes)
	 #--> Variables in parent module
			if myOpt:
				self.MyOptHandler[self.name](myOpt)
			else:
				pass
		else:
			k = False
	  #--> Destroy modal window & Return
		dlg.Destroy()
		return k
	#---

	def MyOptHandlerProtProf(self, iDict):
		""" Set the options in the loaded file for the protprof module 
			---
			iDict: keys are the option name and values are the values
		""" 
		try:
			self.CType = iDict[config.dictUserLoadRes[self.name]['CType']]
		except Exception:
			pass
		try:
			self.LabelControl = iDict[config.dictUserLoadRes[self.name]['LabelControl']]
		except Exception:
			pass
		try:
			val = iDict[config.dictUserLoadRes[self.name]['LabelCond']]
			val = [x.strip() for x in val.split(',')]
			self.LabelCond = val
		except Exception:
			pass
		try:
			val = iDict[config.dictUserLoadRes[self.name]['LabelRP']]
			val = [x.strip() for x in val.split(',')]
			self.LabelRP = val
		except Exception:
			pass
	 #--> Return
		return True
	#---
#---

class ElementGelPanel():
	""" To handle the panel showing the gel in limprotR.

		The class assume there is a self.p1 (ElementFragPanel) to plot the 
		fragment when selecting a lane or a band

		There is also a self.selM attribute to control wether to select a lane
		or a band

		There is also a self.text to write the details of the fragments or bands

		Information comes from a data frame with the following structure
		      Columns .... Nterm Cterm ....  All other columns
		L1 B1 0
		      1
		      2
		      3
		      N
		   B2 0
		      M
		   BK L
		LX BY Z
		The first and second index must be one letter plus number E1 or B1 
		Columns Nterm and Cterm must be present in the data frame
		The content of the df are the fragment for each band (BY) in each lane (LX)
	"""

	def __init__(self, parent):
		""" parent: parent of the widgets"""
	  #--> Widgets
	   #--> Panel
		self.p2 = wx.Panel(parent=parent, 
			size=config.size['Panel'][self.name]['PanelGel'])
		self.p2.SetBackgroundColour('WHITE')
	  #--> Bind
		self.p2.Bind(wx.EVT_PAINT, self.OnPaintGel)
		self.p2.Bind(wx.EVT_LEFT_UP, self.OnP2LeftUp)
		self.p2.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
	#---

	####---- Methods of the class
	def OnSaveGel(self):
		""" Save image of the fragments """	
	  #--> Adjust the height
		h = (config.size['Panel'][self.name]['PanelGel'][1] 
			+ config.tarprot['ImageH'])
	  #--> Create the bitmap
		bmp = wx.Bitmap(self.p2.w, h)
	  #--> Create memDC
		memDC = wx.MemoryDC()
	  #--> Select object for the memDC
		memDC.SelectObject(bmp)
	  #--> Draw
		memDC.SetBrush(wx.Brush(wx.Colour('WHITE')))
		memDC.DrawRectangle(0, 0, self.p2.w, h)
		self.DrawGel(memDC)
		self.DrawGelLabels(memDC)
		self.DrawHGel(memDC)
		self.DrawSGel(memDC)
		self.DrawTGel(memDC)
	  #--> Deselect bitmap
		memDC.SelectObject(wx.NullBitmap)
	  #--> Save
		img = bmp.ConvertToImage()
		msg = config.msg['Save']['LimProtGelImg']
		dlg = DlgSaveFile(config.extLong['FragImage'], msg)
		if dlg.ShowModal() == wx.ID_CANCEL:
			pass
		else:
			p = Path(dlg.GetPath())
			e = p.suffix
			if e == '.png':
				img.SaveFile(str(p), wx.BITMAP_TYPE_PNG)
			elif e == '.tiff':
				img.SaveFile(str(p), wx.BITMAP_TYPE_TIFF)
			elif e == '':
				p = p / '.png'
				img.SaveFile(str(p), wx.BITMAP_TYPE_PNG)
			else:
				pass
	  #--> Destroy modal window & Return
		dlg.Destroy()
		return True
	#---

	def OnSetFocus(self, event):
		""" Override as needed """
		self.p2.SetFocus()
		event.Skip()
		return True
	#---

	def OnP2LeftUp(self, event):
		""" Select whole lane, whole band or a particular spot """
	  #--> Event coordinates
		x              = event.x
		y              = event.y
		LaneBandOld    = (self.TLane, self.TBand)
	  #--> Get Lane, Band selected
		out, self.TLane, self.TBand = dmethods.GHelperXYLocate(x, y, 
			self.coordsGel)
	  #--- Nothing selected leave
		if (self.TLane == None and self.selM == True or 
			self.TBand == None and self.selM == False):
			self.TLane, self.TBand = LaneBandOld
			return True
		else:
			pass
	  #--- Keep selected fragment selected if the same lane/band is clicked
		if ((self.selM == True and LaneBandOld[0] == self.TLane and self.TBand == None) or
			(self.selM != True and LaneBandOld[1] == self.TBand and self.TLane == None)):
			self.TLane, self.TBand = LaneBandOld
			return True
		else:
			self.kf = [None, None]
	  #--- Do nothing if clicked in non-used band-lane positions
		if self.TLane != None and self.TBand != None:
			b = self.TBand - 1
			l = self.TLane
			if (self.Results[b][l][0] == None or 
				self.Results[b][l][0] == 'None'):
				if self.selM:
					if self.TLane == LaneBandOld[0]:
						self.TLane, self.TBand = LaneBandOld
						return True						
					else:
						self.TBand = None
				else:
					if self.TBand == LaneBandOld[1]:
						self.TLane, self.TBand = LaneBandOld
						return True						
					else:
						self.TLane = None					
			else:
				self.GelText = True			
				self.kf = [None, None]		
		else:
			pass
	  #--- Select the lane or the band 
		if self.selM == True:
			try:
				l = self.TLane + 1
				self.f = self.fAll.loc['L'+str(l),:]
				self.fPlot = True
			except Exception as e:
				self.fPlot = False
				self.f     = None
		else:
			try:
				idx = pd.IndexSlice
				self.f = self.fAll.loc[idx[:,'B'+str(self.TBand)],:]
				self.fPlot = True
			except Exception as e:
				self.fPlot = False
				self.f     = None
	  #--- Select the sequence in list box
		if self.selSeq == None:
			self.lbSelPlotG = False
			self.lbSelPlot = False
		else:
			dmethods.GHelperLBSelUpdate(self)			
	  #--- Final configuration and print to wx.TextCtrl
		self.GetLBF()
		self.PrintW()
		self.ShowDetails()
	  #--- Draw
		self.Refresh()
		self.Update()
	  #--- Return
		return True
	#---

	def GetLBF(self):
		""" Set the variables needed for printing lane, bands or fragments 
			details 
		"""
	  #--> Lane and Band
		if self.selM:
			try:
				self.TextL = self.TLane + 1	
			except Exception:
				self.TextL = None
			#---
			if self.kf[0] != None:
				self.TextB = self.kf[0]
			elif self.kf[0] == None and self.TBand != None:
				self.TextB = self.TBand
			else:
				self.TextB = None
		else:
			self.TextB = self.TBand
			#---
			if self.kf[0] != None:
				self.TextL = self.kf[0]
			elif self.kf[0] == None and self.TLane != None:
				self.TextL = self.TLane + 1
			else:
				self.TextL = None	
	  #--- Fragment
		if self.kf[1] == None:
			self.TextF = None
		else:
			self.TextF = self.kf[1] + 1 
	  #--- Return
		return True
	#---

	def PrintW(self):
		""" 0 No write 
			1 Write only a lane
			2 Write only a band
			3 Write lane, band
			4 Write lane, band ,fragment 
		""" 
		if self.TextL == None and self.TextB == None and self.TextF == None:
			self.TextM = 0
		elif (self.TextL != None and self.TextB == None and self.TextF == None
			and self.selM == True):
			self.TextM = 1
		elif (self.TextL == None and self.TextB != None and self.TextF == None
			and self.selM == False):
			self.TextM = 2
		elif self.TextL != None and self.TextB != None and self.TextF == None:
			self.TextM = 3
		elif self.TextF != None:
			self.TextM = 4	
		return True
	#---	

	## Paint Gel
	def OnPaintGel(self, event):
		""" Handles the PAINT event. Split in parts for easier handling. """
	  #--> Variables
		dc = wx.PaintDC(self.p2)
		self.p2.w, self.p2.h = self.p2.GetSize()
		self.coordsGel = {
			'y' : {},
			'x' : {}
		}
	  #--> Paint
		self.DrawGel(dc)
		self.DrawGelLabels(dc)
		self.DrawHGel(dc)
		self.DrawSGel(dc)
		self.DrawTGel(dc)
	  #-- Results
		return True
	#---

	def DrawGel(self, dc):
		""" Draw the spots 
			---
			dc: paint handler
		"""
	  #--> Variables
		self.GrH, self.GrHT, self.GrCH, self.GrW, self.GrWT, self.GrCW = self.SetUpGel()
	  #--> Draw spots
		for b in range(1, self.Bands+1, 1): # Loop bands
			bb = b - 1
			for l in range(1, self.Lanes+1, 1): # Loop lanes
				ll = l - 1
				if (self.Results[bb][ll][0] == None or 
					self.Results[bb][ll][0] == 'None'):
					#--> Cannot pass here because need coordinates
					self.DrawOneFragmentG(dc, b, l, 'White')
				else:
					self.DrawOneFragmentG(dc, b, l, 'Black')
	  #--> Return
		return True
	#---

	def DrawGelLabels(self, dc):
		""" Draw the labels in the gel panel 
			---
			dc : draw handler
		"""
	  #--> Draw Lane labels
		for i in range(1, self.Lanes+1, 1):
			xi = config.limprot['RectSxg'] + (i - 1) * self.GrWT + self.GrCW
			y  = 0
			w  = self.GrW
			h  = config.limprot['RectSxg']
			rect = (xi, y, w, h)
			dc.DrawLabel('Lane'+str(i), rect, alignment=wx.ALIGN_CENTER)
	  #--> Draw Band labels
		for i in range(1, self.Bands+1, 1):
			x = 0
			y = config.limprot['RectSxg'] + (i - 1) * self.GrHT + self.GrCH  
			w = config.limprot['RectSxg']
			h = self.GrH
			rect = (x,y,w,h)
			dc.DrawLabel('Band'+str(i), rect, alignment=wx.ALIGN_CENTER)
	  #--> Return
		return True
	#---

	def DrawHGel(self, dc):
		""" Draw the line highlighting the selected lane/band 
			---
			dc : draw handler
		"""
	  #--> Lane
		if self.selM == True and self.TLane != None:
			xi, xf = self.coordsGel['x'][1][self.TLane]
			xi = xi - config.limprot['LBLineW']
			xf = xf + config.limprot['LBLineW']
			bs = list(self.coordsGel['y'].keys())
			yi = self.coordsGel['y'][bs[0]][0][0] - config.limprot['LBLineW']
			yf = self.coordsGel['y'][bs[-1]][0][1] + config.limprot['LBLineW']
			dc.SetBrush(wx.Brush(wx.TRANSPARENT_BRUSH)) 
			dc.SetPen(wx.Pen(config.colors[self.name]['GBBorder'], 
				config.limprot['LBLineW'], wx.SOLID))
			dc.DrawRectangle(xi, yi, xf-xi, yf-yi)
	  #--> Band
		elif self.selM == False and self.TBand != None:
			yi, yf = self.coordsGel['y'][self.TBand][0]
			yi = yi - config.limprot['LBLineW']
			yf = yf + config.limprot['LBLineW']
			bs = list(self.coordsGel['x'].keys())
			xi = self.coordsGel['x'][self.TBand][0][0] - config.limprot['LBLineW']
			xf = self.coordsGel['x'][self.TBand][-1][1] + config.limprot['LBLineW']
			dc.SetBrush(wx.Brush(wx.TRANSPARENT_BRUSH)) 
			dc.SetPen(wx.Pen(config.colors[self.name]['GBBorder'], 
				config.limprot['LBLineW'], wx.SOLID))
			dc.DrawRectangle(xi, yi, xf-xi, yf-yi)			
		else:
			pass
	  #--> Return
		return True
	#---

	def DrawSGel(self, dc):
		""" Highlight the selection in wx.ListBox 
			---
			dc: draw handler
		"""
		if self.lbSelPlotG:
			self.seqG.apply(self.DrawSGelApply, axis=1, args=(dc,))
		else:
			pass
		return True
	#---

	def DrawSGelApply(self, ll, dc):
		""" Helper to self.DrawSGel 
			---
			ll: row from a data frame
			dc: draw handler
		"""
	  #--> Variables
		l = int(ll.name[0][1:]) - 1
		b = int(ll.name[1][1:])
	  #--> Get coordinates for the rectangle
	   #--> y
		yi, yf = self.coordsGel['y'][b][0]
		y = yi + config.limprot['LBTopGap']
		h = (yf - y - 1 * config.limprot['LBTopGap'])
	   #--> x
		xi, xf = self.coordsGel['x'][b][l]
		xi = xi + config.limprot['LBTopGap']
		xf = xf - config.limprot['LBTopGap']
	  #--> Draw
		dc.SetBrush(wx.Brush(wx.TRANSPARENT_BRUSH)) 
		dc.SetPen(wx.Pen(config.colors[self.name]['LBBorder'], 
			config.limprot['LBLineW'], wx.SOLID))
		dc.DrawRectangle(xi, y, xf-xi, h)		
	  #--> Return
		return True
	#---

	def DrawTGel(self, dc):
		""" Highlight the selected spot 
			---
			dc : draw handler
		"""
	  #--> Draw
	   #--> Locate the spot 
		if self.TBand != None and self.TLane != None and self.GelText == True:
			b = self.TBand - 1
			l = self.TLane
			if (self.Results[b][l][0] == None or 
				self.Results[b][l][0] == 'None'):
				pass
			else:
	   #--> Set coordinates
	   #--> x
				xi, xf = self.coordsGel['x'][self.TBand][self.TLane]
				xi = xi + 4 * config.lpprot[self.name]['TextRectWLat']
				xf = xf - 4 * config.lpprot[self.name]['TextRectWLat']
	   #--> y
				yi, yf = self.coordsGel['y'][self.TBand][0]
				a = yf - yi
				y = yi + (a / 2) - config.lpprot[self.name]['LBTopGap']
	   #--> Draw
				dc.SetBrush(wx.Brush(config.colors[self.name]['Lines'])) 
				dc.SetPen(wx.Pen(config.colors[self.name]['Lines'], 
					config.limprot['LBLineW'], wx.SOLID))
				dc.DrawRectangle(xi, y, xf-xi, 
					config.lpprot[self.name]['LBTopGap'])				
		else:
			pass
	  #--> Return
		return True
	#---

	def DrawOneFragmentG(self, dc, b, l, c):
		""" Draw one fragment. l is the current lane b is the current band 
			---
			dc: draw handler
			b: band
			l: lane
			c: color
		"""
	  #--> Coordinates
		y  = config.limprot['RectSxg'] + (b - 1) * self.GrHT + self.GrCH
		xi = config.limprot['RectSxg'] + (l - 1) * self.GrWT + self.GrCW
		xf = xi + self.GrW
	  #--> Pen & Brush for painting
		dc.SetPen(wx.Pen(c, 1, wx.SOLID))
		if self.Mask[('B'+str(b), 'L'+str(l), 'tost')]:
			if self.selM:
				dc.SetBrush(wx.Brush(wx.Colour(self.Colors[b-1]))) 
			else:
				dc.SetBrush(wx.Brush(wx.Colour(self.Colors[l-1])))
		else:
			dc.SetBrush(wx.Brush(wx.Colour('WHITE')))
	  #--> Draw
		dc.DrawRectangle(xi, y, self.GrW, self.GrH)
	  #--> Record coordinates
	   #--> y
		if b in self.coordsGel['y'].keys():
			pass
		else:
			self.coordsGel['y'][b] = []
			self.coordsGel['y'][b].append((y, y+self.GrH))
	   #--> x
		if b in self.coordsGel['x'].keys():
			pass
		else:
			self.coordsGel['x'][b] = []
		self.coordsGel['x'][b].append((xi, xf))
	  #--> Return
		return True
	#---

	def SetUpGel(self):
		""" calculate the dimensions of each Rect in the Gel """
		spaceAround = config.limprot['RectSxg'] + config.limprot['RectSxg']
		rHT = (self.p2.h - spaceAround) / self.Bands
		rH  = config.limprot['RectHRatio'] * rHT
		rCH = (rHT - rH) / 2 
		rWT = (self.p2.w - spaceAround) / self.Lanes
		rW  = config.limprot['RectWRatio'] * rWT
		rCW = (rWT - rW) / 2
		return [rH, rHT, rCH, rW, rWT, rCW]
	#---	
#---

class ElementFragPanel():
	""" To handle the panel showing the fragments in tarprotR and limprotR.
		Fragments comes from a data frame with the following structure
		      Columns .... Nterm Cterm ....  All other columns
		E1 0
		   1
		   2
		   3
		   N
		E2 0
		   M
		EK L
		The first index must be one letter number E1 or B1 or L1. Columns
		Nterm and Cterm must be present in the data frame
	"""

	def __init__(self, parent):
		""" parent: parent of the widgets """
	  #--> Variables
		self.lbSelH = (config.lpprot[self.name]['RectH'] 
					   - 2 * config.lpprot[self.name]['LBTopGap'])
	  #--> Widgets
	   #--> Panel
		self.p1 = wx.ScrolledWindow(parent=parent, size=(1000, self.h))
		self.p1.SetVirtualSize(1000, self.hT)
		self.p1.SetScrollRate(20, 20)
		self.p1.SetBackgroundColour('WHITE')
	  #--> Bind
		self.p1.Bind(wx.EVT_PAINT, self.OnPaint)
		self.p1.Bind(wx.EVT_LEFT_UP, self.OnLeftUpFrag)
	#---

	####---- Methods of the class
	def OnSaveFrag(self):
		""" Save image of the fragments """	
	  #--> Adjust the height
		h = self.hT + config.tarprot['ImageH']
	  #--> Create the bitmap
		bmp = wx.Bitmap(self.p1.w, h)
	  #--> Create memDC
		memDC = wx.MemoryDC()
	  #--> Select object for the memDC
		memDC.SelectObject(bmp)
	  #--> Draw
		memDC.SetBrush(wx.Brush(wx.Colour('WHITE')))
		memDC.DrawRectangle(0, 0, self.p1.w, h)
		self.DrawLabel(memDC)
		self.DrawReProtein(memDC)
		self.DrawAllFrag(memDC)
		self.DrawLbInfoFrag(memDC)
		self.DrawTeInfo(memDC)
		self.DrawLines(memDC)
	  #--> Deselect bitmap
		memDC.SelectObject(wx.NullBitmap)
	  #--> Save
		img = bmp.ConvertToImage()
		msg = config.msg['Save']['TarProtFragImg']
		dlg = DlgSaveFile(config.extLong['FragImage'], msg)
		if dlg.ShowModal() == wx.ID_CANCEL:
			pass
		else:
			p = Path(dlg.GetPath())
			e = p.suffix
			if e == '.png':
				img.SaveFile(str(p), wx.BITMAP_TYPE_PNG)
			elif e == '.tiff':
				img.SaveFile(str(p), wx.BITMAP_TYPE_TIFF)
			elif e == '':
				p = p / '.png'
				img.SaveFile(str(p), wx.BITMAP_TYPE_PNG)
			else:
				pass
	  #--> Destroy modal windows & Return
		dlg.Destroy()
		return True
	#---

	def OnLeftUpFrag(self, event):
		""" When selecting a fragment in p1 show a black line and text in p3 """
	  #--> Get coordinates
		self.kf = [None, None]
		scrollX = self.p1.GetScrollPos(wx.VERTICAL)
		scrollStep = self.p1.GetScrollPixelsPerUnit()[1]
		x, y = event.GetPosition()
		y = y + scrollX * scrollStep
	  #--> Get Experiment
		for k in self.coordsFrag['y'].keys():
			yi, yo = self.coordsFrag['y'][k][0]
			if check.CheckabWithincd(y, y, yi, yo):
				self.kf[0] = k
				break
			else:
				pass
	  #--> Get Fragment
		if self.kf[0] != None and len(self.coordsFrag['x'][self.kf[0]]) > 0:
			for j, l in enumerate(self.coordsFrag['x'][k]):
				xi, xo = l
				if check.CheckabWithincd(x, x, xi, xo):
					self.kf[1] = j
					break
				else:
					pass
		else:
			pass
	  #--> Draw
		if self.kf[0] != None and self.kf[1] != None:
			#<<<--->>> Needed for LimProtRes to work
			self.GelText = False
			#---
			self.Refresh()
			self.Update()
			self.ShowFragDet()
		else:
			pass
	  #--> Return
		return True
	#---		

	def OnPaint(self, event):
		""" Handles the PAINT event. Split in parts for easier handling. """
	  #--> Variables
		dc = wx.PaintDC(self.p1)
		self.p1.PrepareDC(dc)
		self.p1.w, self.p1.h = self.p1.GetSize()
		self.coordsFrag = {
			'y' : {},
			'x' : {}
		}
	  #--> Draw
		self.DrawLabel(dc)
		self.DrawReProtein(dc)
		self.DrawAllFrag(dc)
		self.DrawLbInfoFrag(dc)
		self.DrawTeInfo(dc)
		self.DrawLines(dc)
	  #--> Return
		return True
	#---

	def DrawLabel(self, dc):
		""" Draw the labels 
			---
			dc: paint handler
		"""
	  #--> Residue numbers Top
		rect = (config.lpprot[self.name]['RectSx'], 0, 
				config.lpprot[self.name]['LabelW'], 
				config.lpprot[self.name]['RectT'])
		dc.DrawLabel('1', rect, alignment=wx.ALIGN_LEFT)
		rect = (self.p1.w - config.lpprot[self.name]['RectSx'], 0, 
				(config.lpprot[self.name]['RectSx'] 
				 - config.lpprot[self.name]['RectEx']), 
				config.lpprot[self.name]['RectT'])
		dc.DrawLabel(str(self.pRes[3]), rect, alignment=wx.ALIGN_RIGHT)
	  #--> Residue numbers bottom
		if self.locProtType == 2:
			xi = self.Res2Pix(self.pRes[2]) - 52
			rect = (xi, config.lpprot[self.name]['LabelpLocY'], 
					config.lpprot[self.name]['LabelW'], 
					config.lpprot[self.name]['RectH'])
			dc.DrawLabel(str(self.pRes[2]), rect, alignment=wx.ALIGN_RIGHT)
		elif self.locProtType == 3:
			xi = self.Res2Pix(self.pRes[2]) - 52
			rect = (xi, config.lpprot[self.name]['LabelpLocY'], 
					config.lpprot[self.name]['LabelW'], 
					config.lpprot[self.name]['RectH'])
			dc.DrawLabel(str(self.pRes[2]), rect, alignment=wx.ALIGN_RIGHT)
			xi = self.Res2Pix(self.pRes[1]) + 2
			rect = (xi, config.lpprot[self.name]['LabelpLocY'], 
					config.lpprot[self.name]['LabelW'], 
					config.lpprot[self.name]['RectH'])
			dc.DrawLabel(str(self.pRes[1]), rect, alignment=wx.ALIGN_LEFT)
		elif self.locProtType == 4:
			xi = self.Res2Pix(self.pRes[1]) + 2
			rect = (xi, config.lpprot[self.name]['LabelpLocY'], 
					config.lpprot[self.name]['LabelW'], 
					config.lpprot[self.name]['RectH'])
			dc.DrawLabel(str(self.pRes[1]), rect, alignment=wx.ALIGN_LEFT)
	  #--> Experiments labels
		i = 0
		while i < self.nLines:
			j = i + 1
			text = self.FragLabel + str(j) + ':'
			y = self.Exp2Piy(i)
			rect = (0, y, config.lpprot[self.name]['RectSx'], 
				config.lpprot[self.name]['RectH'])
			dc.DrawLabel(text, rect, alignment=wx.ALIGN_CENTER)
			i = i + 1
	  #--> Return
		return True
	#---

	def DrawReProtein(self, dc):
		""" Draw the recombinant protein. 
			---
			dc: paint handler
		"""
	  #--> Type 1
		if self.locProtType == 1:
			dc.SetBrush(wx.Brush(wx.Colour(config.colors[self.name]['Nat'])))
			xi = self.Res2Pix(self.pRes[0])
			xf = self.Res2Pix(self.pRes[3])
			w  = self.FragWidth(xi, xf) 
			dc.DrawRectangle(xi, config.lpprot[self.name]['RectH'], 
							  w, config.lpprot[self.name]['RectH'])
	  #--> Type 2
		elif self.locProtType == 2:
			dc.SetBrush(wx.Brush(wx.Colour(config.colors[self.name]['Nat'])))
			xi = self.Res2Pix(self.pRes[0])
			xf = self.Res2Pix(self.pRes[2])
			w  = self.FragWidth(xi, xf) 
			dc.DrawRectangle(xi, config.lpprot[self.name]['RectH'], 
							  w, config.lpprot[self.name]['RectH'])
			dc.SetBrush(wx.Brush(wx.Colour(config.colors[self.name]['Rec'])))
			xi = self.Res2Pix(self.pRes[2])
			xf = self.Res2Pix(self.pRes[3])
			w  = self.FragWidth(xi, xf) 
			dc.DrawRectangle(xi, config.lpprot[self.name]['RectH'], 
							  w, config.lpprot[self.name]['RectH'])						
	  #--> Type 3
		elif self.locProtType == 3:
			dc.SetBrush(wx.Brush(wx.Colour(config.colors[self.name]['Rec'])))
			xi = self.Res2Pix(self.pRes[0])
			xf = self.Res2Pix(self.pRes[1])
			w  = self.FragWidth(xi, xf) 
			dc.DrawRectangle(xi, config.lpprot[self.name]['RectH'], 
							  w, config.lpprot[self.name]['RectH'])
			dc.SetBrush(wx.Brush(wx.Colour(config.colors[self.name]['Nat'])))
			xi = self.Res2Pix(self.pRes[1])
			xf = self.Res2Pix(self.pRes[2])
			w  = self.FragWidth(xi, xf) 
			dc.DrawRectangle(xi, config.lpprot[self.name]['RectH'], 
							  w, config.lpprot[self.name]['RectH'])
			dc.SetBrush(wx.Brush(wx.Colour(config.colors[self.name]['Rec'])))
			xi = self.Res2Pix(self.pRes[2])
			xf = self.Res2Pix(self.pRes[3])
			w  = self.FragWidth(xi, xf) 
			dc.DrawRectangle(xi, config.lpprot[self.name]['RectH'], 
							  w, config.lpprot[self.name]['RectH'])						
	  #--> Type 4
		elif self.locProtType == 4:
			dc.SetBrush(wx.Brush(wx.Colour(config.colors[self.name]['Rec'])))
			xi = self.Res2Pix(self.pRes[0])
			xf = self.Res2Pix(self.pRes[1])
			w  = self.FragWidth(xi, xf) 
			dc.DrawRectangle(xi, config.lpprot[self.name]['RectH'], 
							  w, config.lpprot[self.name]['RectH'])
			dc.SetBrush(wx.Brush(wx.Colour(config.colors[self.name]['Nat'])))
			xi = self.Res2Pix(self.pRes[1])
			xf = self.Res2Pix(self.pRes[2])
			w  = self.FragWidth(xi, xf) 
			dc.DrawRectangle(xi, config.lpprot[self.name]['RectH'], 
							  w, config.lpprot[self.name]['RectH'])
	  #--> Type 5
		elif self.locProtType == 5:
			dc.SetBrush(wx.Brush(wx.Colour(config.colors[self.name]['Rec']))) 
			xi = self.Res2Pix(self.pRes[0])
			xf = self.Res2Pix(self.pRes[3])
			w  = self.FragWidth(xi, xf) 
			dc.DrawRectangle(xi, config.lpprot[self.name]['RectH'], 
							  w, config.lpprot[self.name]['RectH'])
	  #--> Return
		return True
	#---

	def DrawAllFrag(self, dc):
		""" Draw the fragments 
			---
			dc: paint handlers
		"""
		if self.fPlot == True:
			self.f.apply(self.DrawOneFragment, axis=1, args=(dc,))
		else:
			pass
		return True
	#---	

	def DrawOneFragment(self, ll, dc):
		""" Draw one fragment 
			---
			ll: row from a data frame
			dc: paint handler
		"""
	  #--> Variables
		b = int(ll.name[0][1:])
		xi = self.Res2Pix(ll['Nterm'])
		xf = self.Res2Pix(ll['Cterm'])
		w = self.FragWidth(xi, xf)
		dc.SetBrush(wx.Brush(wx.Colour(self.Colors[b-1]))) 
		y = self.Exp2Piy(b-1)
	  #--> Draw
		dc.DrawRectangle(xi, y, w, config.lpprot[self.name]['RectH'])
	  #--> Coordinates
	   #--> y
		if b in self.coordsFrag['y'].keys():
			pass
		else:
			self.coordsFrag['y'][b] = []
			self.coordsFrag['y'][b].append((y, 
					y + config.lpprot[self.name]['RectH']))
	   #--> x
		if b in self.coordsFrag['x'].keys():
			pass
		else:
			self.coordsFrag['x'][b] = []
		self.coordsFrag['x'][b].append((xi, xf))
	  #--> Return
		return True
	#---

	def DrawLbInfoFrag(self, dc):
		""" Highlight selection from wx.ListBox 
			---
			dc: paint handler
		"""
		if self.lbSelPlot:
			self.seq.apply(self.DrawLbInfoFragApply, axis=1, args=(dc,))
		else:
			pass
		return True
	#---

	def DrawLbInfoFragApply(self, ll, dc):
		""" Highlight the fragment containing selected entry in wx.ListBox 
			---
			ll: row from data frame
			dc: paint handler
		"""
	  #--> Coordinates
		yk, xInd = ll.name
		yk = int(yk[1:])
		xInd = int(xInd)
		y = (self.coordsFrag['y'][yk][0][0] 
			+ config.lpprot[self.name]['LBTopGap'])
		xi, xf = self.coordsFrag['x'][yk][xInd]
		xi = xi + config.lpprot[self.name]['LBTopGap']
		xf = xf - config.lpprot[self.name]['LBTopGap']
	  #--> Pen & Brush
		dc.SetBrush(wx.Brush(wx.TRANSPARENT_BRUSH)) 
		dc.SetPen(wx.Pen(config.colors[self.name]['LBBorder'], 
			config.lpprot[self.name]['LBLineW'], wx.SOLID))
	  #--> Draw
		dc.DrawRectangle(xi, y, xf-xi, self.lbSelH)		
	  #--> Return
		return True
	#---

	def DrawTeInfo(self, dc):
		""" Highlights the fragment selected for Text display 
			---
			dc: paint handler
		"""
	  #--> Get fragment
		if self.kf[0] != None and self.kf[1] != None:
			k = self.kf[0]
			b = self.kf[1]	
	  #--> Pen & Brush
			dc.SetPen(wx.Pen(config.colors[self.name]['FragLines'], 
				config.lpprot[self.name]['LBLineW'], wx.SOLID))				
			dc.SetBrush(wx.Brush(wx.Colour(
				config.colors[self.name]['FragLines'])))
	  #--> Coordinates
			a = (config.lpprot[self.name]['RectH'] 
				 - config.lpprot[self.name]['TextRectH'])
			y = (self.coordsFrag['y'][k][0][0] + (a / 2))
			xi, xf = self.coordsFrag['x'][k][b]
			xi = xi + 4 * config.lpprot[self.name]['TextRectWLat']
			xf = xf - 4 * config.lpprot[self.name]['TextRectWLat']
	  #--> Draw
			dc.DrawRectangle(xi, y, xf-xi, config.lpprot[self.name]['TextRectH'])
		else:
			pass
	  #--> Return	
		return True
	#---				

	def DrawLines(self, dc):
		""" Draw lines at the start end of native sequence 
			---
			dc: paint handler
		"""
	  #--> Pen
		dc.SetPen(wx.Pen(config.colors[self.name]['Lines'], 1, wx.DOT))
	  #--> Type 2
		if self.locProtType == 2:
			xi = self.Res2Pix(self.pRes[2])
			yi = config.lpprot[self.name]['RectT']
			xf = xi
			yf = self.hT + 20
			dc.DrawLine(xi, yi, xf, yf)
	  #--> Type 3
		elif self.locProtType == 3:
			for i in [self.pRes[2], self.pRes[1]]:
				xi = self.Res2Pix(i)
				yi = config.lpprot[self.name]['RectT']
				xf = xi
				yf = self.hT + 20
				dc.DrawLine(xi, yi, xf, yf)
	  #--> Type 4
		elif self.locProtType == 4:
			xi = self.Res2Pix(self.pRes[1])
			yi = config.lpprot[self.name]['RectT']
			xf = xi
			yf = self.hT + 20
			dc.DrawLine(xi, yi, xf, yf)
		else:
			pass
	  #--> Return
		return True
	#---	

	def Res2Pix(self, res):
		""" Convert the residue number to a pixel value in order to draw a
			fragment. This gives the x coordinate, basically. 
			---
			res: residue number (int)
		"""
	  #--> Variables
		Sx  = config.lpprot[self.name]['RectSx']
		Ex  = self.p1.w - config.lpprot[self.name]['RectEx']
		Exx = self.pRes[3]
	  #--> Get x
		x = ((Ex - Sx) / (Exx - 1)) * (res - 1) + Sx
	  #--- Return
		return x
	#---

	def Exp2Piy(self, exp):
		""" Calculates the y coordinate for the fragments. 
			---
			exp: Experiment number (int)
		"""
		y = (exp * config.lpprot[self.name]['RectT'] 
			+ config.lpprot[self.name]['LabelFirstExp'])
		return y
	#---

	def FragWidth(self, xi, xf):
		""" Calculates a the width of a fragment """
		w = xf - xi
		return w
	#---
#---

class ElementListCtrlSearch():
	""" Creates a list ctrl and a search ctrl separated by a line inside a
		sizer 
	"""

	def __init__(self, parent):
		""" parent: parent for the widgets """

	  #--> Widgets
	   #--> Listbox
		self.lb = wx.ListCtrl(parent=parent, 
			size=config.size['ListBox'][self.name], 
			style=wx.LC_REPORT|wx.BORDER_SIMPLE)
		gmethods.ListCtrlHeaders(self.lb, self.name)
	  #--> Line
		self.lineHI1 = wx.StaticLine(parent=parent)
	  #--> SearchCtrl
		self.search = wx.SearchCtrl(parent=parent, 
			size=config.size['SearchCtrl'][self.name], 
			style=wx.TE_PROCESS_ENTER)
	  #--> Sizers
	   #--> New Sizer
		self.sizerLB = wx.GridBagSizer(1, 1)
	   #--> Add
		self.sizerLB.Add(self.lb,       pos=(0, 0), 
			border=2, 
			flag=wx.EXPAND|wx.ALIGN_TOP|wx.ALL)
		self.sizerLB.Add(self.lineHI1 , pos=(1, 0), 
			border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerLB.Add(self.search,   pos=(2, 0), 
			border=2, 
			flag=wx.EXPAND|wx.ALIGN_BOTTOM|wx.ALL)
	   #--> Grow Row/Col
		self.sizerLB.AddGrowableRow(0, 1)
		self.sizerLB.AddGrowableCol(0, 1)
	  #--> Binding
		self.lb.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
		self.lb.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnListSelect)	
		#---
		self.search.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.OnSearchCtrl)
		self.search.Bind(wx.EVT_TEXT_ENTER, self.OnSearchCtrl)
		self.search.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)	
	#---

	####---- Methods of the class
	def OnRightDown(self, event):
		""" To show pop up menu over the listbox. Overrride as needed """
		return True
	#---

	def OnListSelect(self, event):
		""" Do something when selecting from the listbox. Override as needed """
		return True
	#---

	def OnSearchCtrl(self, event):
		""" Search for a sequence """
		val = event.GetString()
		val = val.strip().upper()
		gmethods.ListCtrlSearchVal(self.lb, val)
		self.lb.SetFocus()
		return True
	#---
#---

class ElementGraphPanel(wx.Panel):
	""" This class handle the creation and functioning of a panel containing
		a matplotlib plot 
	"""

	def __init__(self, parent, name, stBar=False, dpi=None, id=wx.ID_ANY, 
		pos=wx.DefaultPosition, size=None):
		""" parent: parent for the widgets
			name: mainly to search for in config file (string)
			stBar: reference to the windows status bar if any ()
			dpi : dpi for saving images (int)
			id: id for the panel
			pos: position of the panel
			size: size of the panel
		"""
	  #--> Variables
		self.name = name
		if size == None:
			size = config.size['GraphPanel'][self.name]
		else:
			pass
		self.statusbar = stBar
	  #--> Widgets
	   #--> Panel
		super().__init__(parent, id, pos, size, style=wx.BORDER_SIMPLE)
	   #--> Plot area
		self.figure  = mpl.figure.Figure(dpi=dpi, figsize=(5, 5))
		self.figure.set_tight_layout(True)
		self.axes    = self.figure.add_subplot(111)
		self.canvas  = FigureCanvas(self, -1, self.figure)
		self.annot = self.axes.annotate("", xy=(0,0), xytext=(-20,20),
			textcoords="offset points", bbox=dict(boxstyle="round", fc="w"),
            arrowprops=dict(arrowstyle="->"))
		self.annot.set_visible(False)
		self.canvas.mpl_connect("motion_notify_event", self.OnHover)
	  #--> Sizers
	   #--> New Sizers
		self.sizerPlot = wx.BoxSizer(wx.VERTICAL)
	   #--> Add
		self.sizerPlot.Add(self.canvas, 1, wx.EXPAND)
	   #--> Set & Fit sizer
		self.SetSizer(self.sizerPlot)
		self.sizerPlot.Fit(self)	
	  #--> Bind
		if stBar != False:
			self.canvas.mpl_connect('motion_notify_event', self.UpdateStatusBar)
		else:
			pass	
	#---

	####---- Methods of the class
	def OnHover(self, event):
		""" To annotate text when mouse over. Override as needed """
		pass
	#---

	def OnSaveImage(self, wcard=None, msg=None):
		""" Save an image of the plot. 
			---
			wcard: file extension as needed by wxPython
			msg: msg to show (string) 
		"""
	  #--> Msg
		if msg == None:
			msg = config.msg['Save']['PlotImage']
		else:
			pass
	  #--> Wcard
		if wcard == None:
			wcard = config.extLong['MatplotSaveImage']
		else:
			pass
	  #--> Save & Return
		if gmethods.SaveMatPlotImage(self.figure, wcard, msg):
			return True
		else:
			return False
	#---

	def ClearPlot(self):
		""" Clears the plot area """
		self.axes.clear()
		self.canvas.draw()
		return True
	#---

	def UpdateStatusBar(self, event):
		""" To update status bar. Basic functionality. Override as needed """
		if event.inaxes:
			x, y = event.xdata, event.ydata
			self.statusbar.SetStatusText(gmethods.StatusBarXY(x, y))
		else:
			self.statusbar.SetStatusText('') 
		return True
	#---
#---
# ----------------------------------------------------------- GUI ELEMENTS (END)



# ------------------------------------------------------------- GUI-Checks
class GuiChecks():
	""" This class holds all checks needed in the GUI for the user input 
		In addition, the methods fill the self.d and self.do dicts 
	"""
	
	####---- Methods of the class
	def CheckGuiTcFileRead(self, tc, ext, n, msg, NA=False):
		""" Checks that a tc holds the path to a file with extention ext that 
			can be read. 
			---
			tc : wx.TextCtrl instance
			ext: extension expected in the file (config.extShort[X])  
			n : dicts key to hold output (string)
			msg: error msg (string)
			NA: empty wx.TextCtrl is possible or not (boolean)
		"""
	  #--> Initial set
		self.SetInitVal(tc, n)
	  #--> Check NA
		if self.do[n] == None:
			if self.CheckNA(n, NA):
				return True
			else:
				DlgFatalErrorMsg(msg)
				return False
		else:
			pass
	  #--> Check file can be read & create Path instance for self.do[n]
		if checkM.CheckMFileRead(self.d[n], ext):
			self.do[n] = Path(self.d[n])
			return True
		else:
			pass				
	  #--> If not error msg & Return
		DlgFatalErrorMsg(msg)
		return False
	#---

	def CheckGuiTcSeqFileCode(self, tc, ext, n, msg, NA=False):
		""" Checks if the tc holds a UNIPROT code if not then checks that the tc
			holds the path to a file with extention ext that can be read.
			---
			tc : wx.TextCtrl instance
			ext : extension expected in the file (config.extShort[X])
			n: dict key to store output 
			msg: error msg, 
			NA: is to flag element as optional  
		"""
	  #--> Initial set
		self.SetInitVal(tc, n)
	  #--> Check NA
		if self.do[n] == None:
			if self.CheckNA(n, NA):
				return True
			else:
				DlgFatalErrorMsg(msg)
				return False
		else:
			pass
	  #--> Check file can be read
		if checkM.CheckMFileRead(self.d[n], ext):
			self.do[n] = Path(self.d[n])
			return True
		else:
			pass
	  #--> If not assume uniprot code		
		out, self.do[n] = check.CheckUniprot(self.d[n])
		if out:
			return True
		else:
			pass
	  #--> If nothing error msg & Return 
		DlgFatalErrorMsg(msg)
		return False					
	#---

	def CheckGuiTcOutputFolder(self, tcout, tcin, n, msg):
		""" Check if a tcout contains the path to an output folder and the path
			can be used. If non given use tcin for default folder loc and 
			self.name for default folder name. If only a name given use tcin for
			default folder loc. 
			---
			tcout: wx.TextCtrl instance with the output folder path
			tcin : wx.TextCtrl instance with the data file path
			n: dict key to store output (string)
			msg: error msg (string)
		"""
	  #--> Initial set
		self.SetInitVal(tcout, n)
	  #--> Check Output folder can be used
		out, self.do[n] = checkM.CheckMOutputFolder(tcout, tcin,
			config.dictElemOutputFileFolder[self.name]['DefNameFolder'],
			self.dateN)
		if out:
			return True
		else:
			pass
	  #--> Error msg & Return
		DlgFatalErrorMsg(msg)
		return False
	#---

	def CheckGuiTcOutputFile(self, tcout, tcin, defName, ext, n, msg):
		""" Check that tcout holds the path to the output file and the path can
			be used. If non given use tcin for default folder loc and self.name 
			for default file name. If only a name then use tcin for location.
			---
			tcout: wx.TextCtrl instance with the output file path
			tcin : wx.TextCtrl instance with the data file path			
			defName: default name for the output file (string)
			ext: element of config.extShort 
			n: dict key to store output (string)
			msg: error msg (string)
		"""
	  #--> Initial set
		self.SetInitVal(tcout, n)
	  #--> Check output file
		extStr = ext[0]
		#---# Improve checkM.CheckMOutputFile handle tcin=None
		out, self.do[n] = checkM.CheckMOutputFile(tcout, tcin, defName, extStr, 
			self.overW, self.dateN)
		#---# Improve (UP)
		if out:
			return True
		else:
			pass
	  #--> Error msg & Return
		DlgFatalErrorMsg(msg)
		return False		
	#--- 

	def CheckGuiTcOutputFile2(self, tcout, ext, n, msg):
		""" To handle the case tcin=None. Delete when CheckGuiTcOutputFile is 
		improved """
		fileO = self.d[n] = tcout.GetValue()
		out, self.do[n] = checkM.CheckMOutputFile2(tcout, ext[0], self.overW, 
			self.dateN)
		if out:
			return True
		else:
			DlgFatalErrorMsg(msg)
			return False
	#---

	def CheckGuiStrNotEmpty(self, tc, n, msg, defName=None):
		""" Check fields that holds a string but cannot be empty 
			---
			tc: wx.TextCtrl instance
			n: dicts key to hold output (string)
			msg: error msg (string)
			defName: default name for the variable (string)
		"""
	  #--> Variables	
		var = tc.GetValue()
		k   = True
	  #--> Check default name
		if var in config.naVals and defName == None:
			k = False
		elif var in config.naVals and defName != None:
			var = defName
		else:
			pass
	  #--> Set self.d[n] & self.do[n]
		if k:
			self.d[n] = var
			self.do[n] = var
			return True
		else:
			pass
	  #--> Error msg & Return
		DlgFatalErrorMsg(msg)
		return False
	#---

	def CheckGui1Number(self, tc, n, msg, t='float', comp='egt', val=0, 
		val2=None, NA=False):
		""" Checks a field that has one number.
			---
			tc: wx.TextCtrl instance
			n: dicts key to hold output (string)
			msg: error msg (string)			
			t: float, int (string)
			comp: egt >= val, e == val, gt > val, elt <= val, lt < val (string)
			val: value to compare against (number)
			NA: NA allowed (boolean)
			 """
	  #--> Initial set
		self.SetInitVal(tc, n)
	  #--> Check NA
		if self.do[n] == None:
			if self.CheckNA(n, NA):
				return True
			else:
				DlgFatalErrorMsg(msg)
				return False
		else:
			pass
	  #--> Compare
		out, self.do[n] = checkM.CheckMNumberComp(self.d[n], t, comp, val, val2)
		if out:
			return True
		else:
			pass
	  #--> Error msg & Return
		DlgFatalErrorMsg(msg)
		return False
	#---

	def CheckGuiListNumber(self, tc, n, msg, t='int', comp='egt', val=0, 
		NA=False, Range=False, Order=False, Unique=True, DelRepeat=False):
		""" Check that tc has a list of numbers 
			---
			tc: wx.TextCtrl instance
			n: dicts key to hold output (string)
			msg: error msg (string)
			t: float, int (string)
			comp: egt >= val, e == val, gt > val, elt <= val, lt < val (string)
			val: value to compare against (number)
			NA: NA allowed (boolean)
			Rage: Range allowed (boolean)
			Order: list must be ordered low -> high (boolean)
			Unique: elements must be unique (boolean)
			DelRepeat: delete repeating elements (boolean)								
		"""
	  #--> Initial set
		self.SetInitVal(tc, n)
	  #--> Check NA
		if self.do[n] == None:
			if self.CheckNA(n, NA):
				return True
			else:
				DlgFatalErrorMsg(msg)
				return False
		else:
			pass
	  #--> Check list elements
		out, self.do[n] = checkM.CheckMListNumber(self.d[n], 
			t=t, 
			comp=comp, 
			val=val, 
			Range=Range, 
			Order=Order, 
			Unique=Unique, 
			DelRepeat=DelRepeat,
		)
		if out:
			return True
		else:
			pass
	  #--> Error msg & Return
		DlgFatalErrorMsg(msg)
		return False					
	#---

	def CheckGuiListUniqueElements(self, l, msg, NA=False):
		""" Check that a list contains unique elements to avoid having repeated 
			elements in the input 
			---
			l: list with values (list)
			msg: error msg (string)
			NA: NA values allowed (boolean)
		"""
	  #--> Check list
		out, elem = dmethods.ListUnique(l, NA=NA)
		if out:
			return True
		else:
			pass
	  #--> Error msg & Return
		mmsg  = msg
		mmsg += '\nRepeated values: ' + ', '.join(list(map(str, elem)))
		DlgFatalErrorMsg(mmsg)
		return False
	#---

	def CheckGuiColNumbersInDataFile(self, l, nCols, msg, NA=False):
		""" Check that all columns in l are < nCols. To check that a column 
			number can be found in a data file 
			l: list with column numbers (list)
			nCols: total number of columns in the data file (int)
			msg: error msg (string)
			NA: NA values allowed (boolean)
		"""
	  #--> Remove NA values if needed
		if NA == True:
			l = [x for x in l if x != None]
		else:
			pass
	  #--> Needed to correct the cero based counting
		col = nCols - 1
	  #--> Get values > nCols - 1 
		h = [x for x in l if x > col]
	  #--> Error msg & Return
		if len(h) > 0:
			mmsg = msg
			mmsg += '\nNumber of columns: ' + str(nCols)
			mmsg += '\nRequested columns: ' + ', '.join(list(map(str, h)))
			DlgFatalErrorMsg(mmsg)
			return False
		else:
			return True
	#---  

	def CheckGuiPDBID(self, tc, n, nold, msg, NA=True):
		""" Check that tc holds a valid PDB ID 2y4f;A or 2y4f;PROA. 
			Proper values are given if a local pdb file is already given in 
			self.do[nold] 
			---
			tc: wx.TextCtrl instance with the pdb ID
			n: dict key to store results (string)
			nold dict key with the pdb file value (string)
			msg: error msg (string)
			NA: NA values allowed (boolean)
		"""
	  #--> Initial set
		self.SetInitVal(tc, n)
	  #--> PDBFile & PDBID both None
		if self.do[n] == None and self.do[nold] == None:
			return True
		else:
			pass
	  #--> Set code and cs as a list in val	
		val = [x.strip() for x in self.d[n].split(';')]			
	  #--> Set len(val)
		lval = len(val)
	  #--> More than three values in PDBID 
		if lval > 2:
			DlgFatalErrorMsg(msg)
			return False
		else:
			pass
	  #--> Two values in PDBID
		if lval == 2:
	   #--> First check valid chain or segment ID
			if len(val[1]) >= 5:
				DlgFatalErrorMsg(msg)
				return False
			else:
   	   #--> PDBFile != None
				if lval == 2 and self.do[nold] != None:
					self.do[n] = [None, val[1]]
					return True
				else:
					pass
	   #--> PDBFile == None
				if lval == 2 and self.do[nold] == None:
					out, pdb = check.CheckPDB(val[0])
					if out:
						self.do[n] = [pdb, val[1]]
						return True
					else:
						DlgFatalErrorMsg(msg)
						return False
				else:
					pass
		else:
			pass
	  #--> One value in PDBID
		if lval == 1:
	   #--> PDBFile == None
			if self.do[nold] == None:
				DlgFatalErrorMsg(msg)
				return False
			else:
				pass
	   #--> Check valid chain or segment ID
			if len(val[0]) >= 5:
				DlgFatalErrorMsg(msg)
				return False
			else:
				pass
	   #--> PDBFile != None				
			if self.do[nold] != None:
				self.do[n] = [None, val[0]]
				return True
			else:
				pass
		else:
			pass
	  #--> Unknown error & Return
		DlgFatalErrorMsg(config.msg['Unknown'])
		return False					
	#---

	def CheckGuiResultControl(self, tc, n, msg, t, comp, val, Range, Order, 
		Unique, DelRepeat, NA, Rep):
		""" Check that res hold a valid results input. This method sets
			self.d[n], self.do[n] and self.do['Control']
			---
			tc: wx.TextCtrl instance
			n: dicts key to hold output (string)
			msg: error msg (string)
			t: float, int (string)
			comp: egt >= val, e == val, gt > val, elt <= val, lt < val (string)
			val: value to compare against (number)
			Rage: Range allowed (boolean)
			Order: list must be ordered low -> high (boolean)
			Unique: elements must be unique (boolean)
			DelRepeat: delete repeating elements (boolean)
			NA: NA allowed (boolean)
			Rep: Enforce same number of replicates for each band/cond (boolean)
		"""
	 #--> Get user given value
		res = self.d[n] = tc.GetValue()
	 #--> Check empty value
		if check.CheckVarEmpty(res):
	 #--> Turn string into list of list
			out, resS = dmethods.ListResult(res, self.name, self.CType)
			if out:
				pass
			else:
				return False
	 #--> Check Control is not empty or NA
			if check.CheckControlExpNA(resS):
				pass
			else:
				return False
	 #--> Check proper shape of matrix
			if check.CheckListNElements(resS, mod=self.name):
				pass
			else:
				return False
	 #--> Check elements
			resO = []
			for e in resS: # Loop cond/band
				resE = []
				for i in e: # Loop tp/lane
					for o in i: # Loop replicates
						out, ifix = checkM.CheckMListNumber(o, t=t, comp=comp, 
							val=val, Range=Range, Order=Order, Unique=Unique, 
							DelRepeat=DelRepeat, NA=NA)
						if out:
							resE.append(ifix)
						else:
							DlgFatalErrorMsg(msg)
							return False
				resO.append(resE)
	 #--> Check number of replicates
			if Rep:
				if check.CheckListEqualElements(
					resO, 
					config.dictCheckFatalErrorMsg[self.name]['EqualNElem']
				):
					pass
				else:
					return False					
			else:	
				pass	
	 #--> Flat list and Check Unique
			onlyRes = [x[1:] for x in resO]
			onlyCon = [x[0] for x in resO]
			resFlat = dmethods.ListFlatNLevels(onlyRes, 2)[1]
			conFlat = dmethods.ListFlatNLevels(onlyCon, 1)[1]
			conFlat = list(set(conFlat))
			if check.CheckListUniqueElements(resFlat+conFlat, NA=NA):
				self.do['ResultsControl'] = resO
				self.do['Results'] = onlyRes
				self.do['Control'] = onlyCon
			else:
				DlgFatalErrorMsg(msg)
				return False					
		else:
			DlgFatalErrorMsg(msg)
			return False											
	 #--> Return
		return True			
	#---

	def CheckGuiCSinPDB(self, pdbObj, cs, msg):
		""" Check that the supplied chain/segment (cs) is indeed in the pdb 
			---
			pdbObj: pdb object
			cs : chain or segment ID (string less than 5 characters)
			msg : error msg (string)
		"""
	  #--> Get cs in object
		csInFile = pdbObj.csInFile
	  #--> Check if given cs is found in object & Return
		if cs in csInFile[0] or cs in csInFile[1]:
			return True
		else:
			DlgFatalErrorMsg(msg)
			return False
	#---

	####---- Helper methods
	def SetInitVal(self, tc, n):
		""" Set the initial value for self.d[n] and self.do[n] 
			---
			tc: wx.TextCtrl with the user given value
			n: key for self.d & self.do
		"""
	  #--> Get string in tc
		val = tc.GetValue()
	  #--> Set self.d[n] & self.do[n]
		if val in config.naVals:
			self.d[n] = val
			self.do[n] = None
		else:
			self.d[n] = self.do[n] = val
	  #--> Return	
		return True
	#---

	def CheckNA(self, n, NA):
		""" Check if NA values are allowed
			Return: True (nothing else need to be check, Return True)
				    False (NA value found but not allowed, Return False)
			---
			n: dict key to check (string)
			NA: NA values are allowed or not (boolean) 
		"""
	  #--> Check NA
		if NA:
			return True
		else:
			return False
	#---
#---
# ------------------------------------------------------------- GUI-Checks (END)



# ------------------------------------------------------------ DLG WINDOWS
class DlgOpenDir(wx.DirDialog):
	""" Select folder dialog """
	
	def __init__(self, message=None):
		""" message: msg to show (string) """
		if message == None:
			message = 'Select the output folder'
		super().__init__(None, message=message, 
			style=wx.DD_DEFAULT_STYLE|wx.DD_CHANGE_DIR)
	#---
#---

class DlgSaveFile(wx.FileDialog):
	""" My save file dialog """
	
	def __init__(self, wildcard, message=None,):
		""" wildcard: extension of the file to save (config.extLong) 
			message: msg to show (string)
		"""
		if message == None:
			msg = config.msg['Save']['OutFile']
		else:
			msg = message
		super().__init__(None, message=msg, wildcard=wildcard, 
			style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT)
	#---
#---

class DlgOpenFile(wx.FileDialog):
	""" Creates the open file dialog """
	
	def __init__(self, message, wildcard):
		""" message: msg to show (string)
			wildcard: extension of the file to be open (config.extLong)
		"""
		super().__init__(None, message=message, wildcard=wildcard, 
		  style=wx.FD_OPEN|wx.FD_CHANGE_DIR|wx.FD_FILE_MUST_EXIST|wx.FD_PREVIEW)
		self.Center()
	#---
#---

class DlgTextInput(wx.TextEntryDialog):
	""" Creates a Text Input Dialog """

	def __init__(self, parent, message, value=''):
		""" message: msg to show """
		super().__init__(parent, message, value=value)
		self.Center()
	#---
#---

class DlgOpenFileS(wx.FileDialog):
	""" Creates the open file dialog """
	
	def __init__(self, message, wildcard):
		""" message: msg to show (string)
			wildcard: extension of the file to be open (config.extLong)
		"""
		super().__init__(None, message=message, wildcard=wildcard, 
		  style=(wx.FD_MULTIPLE|wx.FD_OPEN|wx.FD_CHANGE_DIR|
		  	wx.FD_FILE_MUST_EXIST|wx.FD_PREVIEW))
		self.Center()
	#---
#---

class DlgWarningYesNo(wx.MessageDialog):
	""" A Yes/No warning message.

		It cannot auto destroy because the Yes/No must be processed. 
	"""

	def __init__(self, message):
		""" message: msg to show (string) """
		super().__init__(None, message=message, caption='Warning',
			style=wx.YES_NO|wx.ICON_EXCLAMATION)
		self.Center()
	#---
#---

####---- These dialogs show and destroy themselves
class DlgFatalErrorMsg(wx.MessageDialog):
	""" A fatal error message """
	
	def __init__(self, message, nothing=True, seq=None):
		""" message: msg to show (string)
			nothing: add string to msg (boolean)
		"""
		if seq != None:
			msg = message + '\n\nConflicting sequence: ' + str(seq) + '\n'
		else:
			msg = message
		if nothing == True:
			msg = msg + '\nNothing will be done.'
		elif nothing == 'E':
			msg = msg + '\nNothing else will be done.'
		else:
			msg = msg
		super().__init__(None, message=msg, caption='Fatal Error Detected',
			style=wx.OK|wx.ICON_ERROR)
		self.Center()
		self.ShowModal()
		self.Destroy()
	#---
#---

class DlgUnexpectedErrorMsg(wx.MessageDialog):
	""" A fatal error message """

	def __init__(self, message):
		""" message: msg to show (string) """
		super().__init__(None, message=message, caption='Unexpected Error',
			style=wx.OK|wx.ICON_ERROR)
		self.Center()
		self.ShowModal()
		self.Destroy()
	#---
#---		

class DlgSuccessMsg(wx.MessageDialog):
	""" A success message """
	
	def __init__(self, message=None):
		""" message: msg to show (string or None) """
		if message is None:
			msg = 'Analysis finished successfully.'
		else:
			msg = message
		super().__init__(None, message=msg, caption='All done', 
			style=wx.OK|wx.ICON_INFORMATION)
		self.Center()
		self.ShowModal()
		self.Destroy()
	#---
#---

class DlgWarningOk(wx.MessageDialog):
	""" Defines a custom warning message """

	def __init__(self, message):
		""" message: msg to show (string) """
		super().__init__(None, message=message, caption='Warning', 
			style=wx.OK|wx.ICON_EXCLAMATION)
		self.Center()
		self.ShowModal()
		self.Destroy()
	#---
#---

class DlgScrolledDialog(wx.lib.dialogs.ScrolledMessageDialog):
	""" Show a scrolled window message. Used in SearchCtrl in TarProt """

	def __init__(self, message, caption=None):
		""" message: msg to show (string) 
			caption: windows caption (string or None)
		"""
		if caption == None:
			caption = 'Warning'
		else:
			pass
		super().__init__(None, msg=message, caption=caption)
		self.Center()
		self.ShowModal()
		self.Destroy()
	#--
#---
# ------------------------------------------------------------ DLG WINDOWS (END)



# ------------------------------------------------------------ GUI WINDOWS
class WinMyFrame(wx.Frame):
	""" Base class for all windows.	
		The class define the outer borders and a sizerIN to hold all other 
		widgets. In addition, the general menu is defined and the windows icon 
		is set. 
	"""

	def __init__(self, parent, title=None, style=None):
		""" parent: parent of the widgets 
			title: title of the window (string or None)
			style: style of the window
		"""
	 #--> Initial Setup
		if style is None:
			style = wx.DEFAULT_FRAME_STYLE&~(wx.RESIZE_BORDER|wx.MAXIMIZE_BOX)
		else:
			pass
		if title is None:
			self.title = config.title[self.name]
		else:
			self.title = title
		super().__init__(parent=parent, title=self.title, style=style)
	 #--> Menu
		self.menubar = menu.MainMenuBar()
		self.SetMenuBar(self.menubar) 
	 #--> Widgets
	  #--> Panel
		self.panel   = wx.Panel(self)
	  #--> Lines
		self.lineH1 = wx.StaticLine(self.panel)
		self.lineH2 = wx.StaticLine(self.panel)		
		self.lineV1 = wx.StaticLine(self.panel, style=wx.LI_VERTICAL)
		self.lineV2 = wx.StaticLine(self.panel, style=wx.LI_VERTICAL)
	 #--> Sizers
	  #--> New Sizers
		self.sizer   = wx.GridBagSizer(1, 1)
		self.sizerIN = wx.GridBagSizer(1, 1)
	  #--> Add
		self.sizer.Add(self.lineH1,  pos=(0, 1), border=2, 
			flag=wx.EXPAND|wx.TOP|wx.BOTTOM|wx.ALIGN_CENTER)
		self.sizer.Add(self.lineH2,  pos=(2, 1), border=2, 
			flag=wx.EXPAND|wx.TOP|wx.BOTTOM|wx.ALIGN_CENTER)
		self.sizer.Add(self.lineV1,  pos=(1, 0), border=2, 
			flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER)
		self.sizer.Add(self.lineV2,  pos=(1, 2), border=2, 
			flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER)
		self.sizer.Add(self.sizerIN, pos=(1, 1), flag=wx.EXPAND|wx.ALIGN_CENTER)
	  #--> Grow Col/Row
		self.sizer.AddGrowableCol(0, 0)
		self.sizer.AddGrowableCol(1, 1)
		self.sizer.AddGrowableCol(2, 0)
		self.sizer.AddGrowableRow(0, 0)
		self.sizer.AddGrowableRow(1, 1)
		self.sizer.AddGrowableRow(2, 0)
	  #--> Set sizer
		self.panel.SetSizer(self.sizer)
	 #--> Icon
		self.SetIcon(wx.Icon(str(config.image['icon'])))	
	 #--> Bind
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.Bind(wx.EVT_CHAR_HOOK, self.CloseThisWin)
	#---

	####---- Methods of the class
	def OnClose(self, event):
		""" Update config.winOpen, config.WinNameVar and close the window 
			It mus be override for results windows and for TypeRes windows
		"""
	 #--> Remove from Open list
		config.win['Open'].remove(config.win[self.name])
	 #--> Set win to None to be able to create a new window like this
		if self.name in config.win.keys():
			config.win[self.name] = None
		else:
			pass
	 #--> Check that the TypeResults window is also deleted
		try:
			del(config.win['TypeRes'][self.name])
		except Exception:
			pass
	 #--> Destroy & Return
		self.Destroy()
		return True
	#--- 

	def CloseThisWin(self, event):
		""" Close this window with keyboard Ctr/Cmd+D """
	 #--> Get pressed key & Close or pass
		if event.ControlDown():
			if event.GetUnicodeKey() == 68:
				self.Close()
				return True
			else:
				pass
		else:
			pass
	 #--> Skip event for furhter system processing of the keyboard input
		event.Skip()		
	 #--> Return
		return True
	#---
#---

class WinGraph(WinMyFrame):
	""" Creates a window showing a graph """
	
	def __init__(self, file, style=wx.DEFAULT_FRAME_STYLE, 
		parent=None, dpi=None):
		""" file: file with the results (string or Path)
			style: style of the windows
			parent: parent of the widgets
			dpi: dpi resolution of the image
		"""
	 #--> Initial Setup
		self.fileP = Path(file)
		try:
			self.fileObj = config.pointer['dclasses']['DataObj'][self.name](self.fileP)
		except Exception:
			raise ValueError('')
		fname = file.name
		title = config.title[self.name] + ' (' + str(fname) + ')'
		super().__init__(parent=parent, title=title, style=style)
	 #--> Widgets
	  #--> Panel
		self.p = wx.Panel(self.panel, style=wx.BORDER_SIMPLE)
	  #--> Figure
		self.figure  = mpl.figure.Figure(dpi=dpi, figsize=(5, 5))
		self.figure.set_tight_layout(True)
		self.axes    = self.figure.add_subplot(111)
		self.canvas  = FigureCanvas(self.p, -1, self.figure)
		self.axes.set_axisbelow(True)
	  #--> Statusbar
		self.statusbar = self.CreateStatusBar()
	 #--> Sizers
	  #--> New Sizers
		self.sizerPlot = wx.BoxSizer(wx.VERTICAL)
	  #--> Add
		self.sizerPlot.Add(self.canvas, 1, wx.EXPAND)
	  #--> Set
		self.p.SetSizer(self.sizerPlot)
	  #--> All together in sizerin
		self.sizerIN.Add(self.p, pos=(0, 0), border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
	  #--> Fit sizer
		self.sizerPlot.Fit(self)
		self.sizer.Fit(self)
	  #--> Set growable col/rwo
		self.sizerIN.AddGrowableCol(0, 1)
		self.sizerIN.AddGrowableRow(0, 1)			
	 #--> Positions and minimal size
		gmethods.MinSize(self)
		self.WinPos()
	 #--> Bind
		self.canvas.mpl_connect('motion_notify_event', self.UpdateStatusBar)
		self.canvas.mpl_connect('button_press_event', self.OnClick)
		self.cursor = Cursor(self.axes, useblit=True, 
			color=config.colors['cursorColor'], 
			linewidth=config.cursor['lineWidth'], 
			linestyle=config.cursor['lineStyle'])
	#---

	####---- Methods of the class
	def OnSavePlotImage(self, wcard=None, msg=None):
		""" Save an image of the plot.
			---
			wcard : extension for the file (config.extLong)
			msg: msg to show (string)
		"""
	 #--> Variables
		if msg == None:
			msg = config.msg['Save']['PlotImage']
		else:
			pass
		if wcard == None:
			wcard = config.extLong['MatplotSaveImage']
		else:
			pass
	 #--> Save & Return
		if gmethods.SaveMatPlotImage(self.figure, wcard, msg):
			return True
		else:
			return False
	#---

	def ClearPlot(self):
		""" Clears the plot area """
		self.axes.clear()
		self.canvas.draw()
		return True
	#---

	def SetAxis(self):
		""" To draw the axes labels and ticks. Override as needed """		
		pass
	#---

	def UpdateStatusBar(self, event):
		""" To update status bar. Basic functionality. Override as needed """
		if event.inaxes:
			x, y = event.xdata, event.ydata
			self.statusbar.SetStatusText(gmethods.StatusBarXY(x, y))
		else:
			self.statusbar.SetStatusText('') 
		return True
	#---

	def WinPos(self):
		""" Override as needed """
		pass
	#---

	def OnClick(self, event):
		""" To get click events. Override as needed """
		pass
	#---

	def OnClose(self, event):
		""" Update config.winOpen. Override from parent	"""
		config.win['Open'].remove(self)
		self.Destroy()
		return True
	#--- 
#---

class WinModule(WinMyFrame, GuiChecks, ElementClearAFVC, ElementHelpRun, 
	ElementDataFile, ElementOutputFileFolder, ElementResults):
	""" Basic elements of the modules windows. Used in TarProt, LimProt """
	
	def __init__(self, parent, style=None, length=60):
		""" parent: parent of the widgets
			style: style of the window
			length: length of the gauge in ElementHelpRun
		"""
	 #--> Initial Setup 
		WinMyFrame.__init__(self, parent=parent, style=style)
		ElementClearAFVC.__init__(self, self.panel)
		ElementHelpRun.__init__(self, self.panel, length=length)
	 #--> Widgets
	  #--> Lines
		self.lineHI1 = wx.StaticLine(self.panel)
		self.lineVI1 = wx.StaticLine(self.panel, style=wx.LI_VERTICAL)
		self.lineVI2 = wx.StaticLine(self.panel, style=wx.LI_VERTICAL)
	  #--> Static boxes
		self.boxFiles   = wx.StaticBox(
			self.panel, 
			label=config.msg['StaticBoxNames']['Files']
		)
		self.boxValues  = wx.StaticBox(
			self.panel, 
			label=config.msg['StaticBoxNames']['Values']
		)
		self.boxColumns = wx.StaticBox(
			self.panel, 
			label=config.msg['StaticBoxNames']['Columns']
		)
	  #--> Needs to be here because of self.boxFiles
		ElementDataFile.__init__(self, self.boxFiles)
		ElementOutputFileFolder.__init__(self, self.boxFiles)
		ElementResults.__init__(self, self.boxColumns)
	  #--> Buttons
		self.buttonSeqRecFile = wx.Button(self.boxFiles, label='Sequence (rec)')
		self.buttonSeqNatFile = wx.Button(self.boxFiles, label='Sequence (nat)')
		self.buttonPDBFile    = wx.Button(self.boxFiles, label='PDB file')
		self.buttonOutName    = wx.Button(self.boxFiles, label='Output name')
	  #--> Static text
		self.stTarprot    = wx.StaticText(self.boxValues, 
			label='Target protein', style=wx.ALIGN_RIGHT)
		self.stScoreVal   = wx.StaticText(self.boxValues, 
			label='Score value', style=wx.ALIGN_RIGHT)
		self.stDataNorm   = wx.StaticText(self.boxValues, 
			label='Data normalization', style=wx.ALIGN_RIGHT)
		self.staVal       = wx.StaticText(self.boxValues, 
		   label=u'\N{GREEK SMALL LETTER ALPHA}'+'-value', style=wx.ALIGN_RIGHT)
		self.stPositions  = wx.StaticText(self.boxValues, 
		label='Positions', style=wx.ALIGN_RIGHT)
		self.stSeqLength  = wx.StaticText(self.boxValues, 
			label='Sequence length', style=wx.ALIGN_RIGHT)
		self.stHistWin    = wx.StaticText(self.boxValues, 
			label='Histogram windows', style=wx.ALIGN_RIGHT)
		self.stPDB        = wx.StaticText(self.boxValues, 
			label='PDB ID', style=wx.ALIGN_RIGHT)		
		self.stSeq        = wx.StaticText(self.boxColumns, 
			label='Sequences', style=wx.ALIGN_RIGHT)
		self.stDetProt    = wx.StaticText(self.boxColumns, 
			label='Detected proteins', style=wx.ALIGN_RIGHT)
		self.stScore      = wx.StaticText(self.boxColumns, 
			label='Score', style=wx.ALIGN_RIGHT)
		self.stColExt     = wx.StaticText(self.boxColumns, 
			label='Columns to extract', style=wx.ALIGN_RIGHT)
	  #--> Text control
		self.tcSeqRecFile = wx.TextCtrl(self.boxFiles, value="", size=(495, 22))
		self.tcSeqNatFile = wx.TextCtrl(self.boxFiles, value="", size=(495, 22))
		self.tcOutName    = wx.TextCtrl(self.boxFiles, value="", size=(495, 22))
		self.tcTarprot   = wx.TextCtrl(self.boxValues, value="", size=(180, 22))
		self.tcScoreVal  = wx.TextCtrl(self.boxValues, value="", size=(180, 22))
		self.tcSeq      = wx.TextCtrl(self.boxColumns, value="", size=(470, 22))		
		self.tcDetProt  = wx.TextCtrl(self.boxColumns, value="", size=(470, 22))		
		self.tcScore    = wx.TextCtrl(self.boxColumns, value="", size=(470, 22))
		self.tcColExt   = wx.TextCtrl(self.boxColumns, value="", size=(470, 22))	
		self.tcPDBFile    = wx.TextCtrl(self.boxFiles, value="", size=(495, 22))
		self.tcPositions = wx.TextCtrl(self.boxValues, value="", size=(180, 22))
		self.tcSeqLength = wx.TextCtrl(self.boxValues, value="", size=(180, 22))		
		self.tcHistWin   = wx.TextCtrl(self.boxValues, value="", size=(180, 22))		
		self.tcPDB       = wx.TextCtrl(self.boxValues, value="", size=(180, 22))	
	  #--> Combo box
		self.cbDataNorm = wx.ComboBox(self.boxValues, value='Log2',  
			choices=config.combobox['NormValues'], style=wx.CB_READONLY)		
		self.cbaVal     = wx.ComboBox(self.boxValues, value='0.050', 
			choices=config.combobox['Avalues'], style=wx.CB_READONLY)
	  #--> Listbox
		self.lb = wx.ListCtrl(self.panel, 
			size=config.size['ListBox'][self.name], 
			style=wx.LC_REPORT|wx.BORDER_SIMPLE)
		gmethods.ListCtrlHeaders(self.lb, self.name)
	 #--> Dict for adding from listbox. Override as needed
		self.ColDic = {
			101: self.tcSeq, 
			102: self.tcDetProt, 
			103: self.tcScore, 
			104: self.tcColExt,
		}
	 #--> Sizers
	  #--> Central static boxes
		self.sizerboxFiles = wx.StaticBoxSizer(self.boxFiles, wx.VERTICAL)
		self.sizerboxValues = wx.StaticBoxSizer(self.boxValues, wx.VERTICAL)
		self.sizerboxColumns = wx.StaticBoxSizer(self.boxColumns, wx.VERTICAL)
		self.sizerBoxes = wx.BoxSizer(wx.VERTICAL)
	  #--> Add
		self.sizerBoxes.Add(self.sizerboxFiles,   border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerBoxes.Add(self.sizerboxValues,  border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerBoxes.Add(self.sizerboxColumns, border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
	  #--> All together in sizerin
		self.sizerIN.Add(self.sizerClear, pos=(0, 0), border=2, 
			flag=wx.EXPAND|wx.ALIGN_TOP|wx.ALL)
		self.sizerIN.Add(self.lineVI1,       pos=(0, 1), border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerIN.Add(self.sizerBoxes,    pos=(0, 2), border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerIN.Add(self.lineVI2,       pos=(0, 3), border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerIN.Add(self.lb,            pos=(0, 4), border=2, 
			flag=wx.EXPAND|wx.ALIGN_TOP|wx.ALL)
		self.sizerIN.Add(self.lineHI1,       pos=(1, 0), border=2, span=(0, 5),
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerIN.Add(self.sizerBottom, pos=(2, 0), border=2, span=(0, 5),
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
	 #--> Position
		self.SetPosition(pt=config.coord['TopLeft'])
	 #--> Tooltips
	  #--> Buttons
		self.buttonSeqRecFile.SetToolTip(config.tooltip['WinModule']['SeqRec'])
		self.buttonSeqNatFile.SetToolTip(
			config.tooltip['WinModule']['SeqNat'] + config.msg['OptVal'])
		self.buttonPDBFile.SetToolTip(
			config.tooltip['WinModule']['PDBFile'] + config.msg['OptVal'])
		self.buttonOutName.SetToolTip(
			config.tooltip['WinModule']['OutName'] + config.msg['OptVal'])
	  #--> Static Text
		self.stTarprot.SetToolTip(config.tooltip['WinModule']['TarProt'])
		self.stScoreVal.SetToolTip(config.tooltip['WinModule']['ScoreVal'])
		self.stDataNorm.SetToolTip(config.tooltip['WinModule']['DataNorm'])
		self.staVal.SetToolTip(config.tooltip['WinModule']['aVal']) 
		self.stPositions.SetToolTip(
			config.tooltip['WinModule']['Positions'] + config.msg['OptVal'])
		self.stSeqLength.SetToolTip(
			config.tooltip['WinModule']['SeqLength'] + config.msg['OptVal'])
		self.stHistWin.SetToolTip(
			config.tooltip['WinModule']['HistWin'] + config.msg['OptVal'])
		self.stPDB.SetToolTip(
			config.tooltip['WinModule']['PDBID'] + config.msg['OptVal'])
		#-->
		self.stSeq.SetToolTip(config.tooltip['WinModule']['Sequence'])
		self.stDetProt.SetToolTip(config.tooltip['WinModule']['DetProt'])
		self.stScore.SetToolTip(config.tooltip['WinModule']['Score'])
		self.stColExt.SetToolTip(
			config.tooltip['WinModule']['ColExt'] + config.msg['OptVal'])
	 #--> Binding
		self.buttonSeqRecFile.Bind(wx.EVT_BUTTON, self.OnSeqRecFile)
		self.buttonSeqNatFile.Bind(wx.EVT_BUTTON, self.OnSeqNatFile)
	 #--> Default values
		self.tcOutputFF.SetValue('NA')
		self.tcOutName.SetValue('NA')
		self.tcColExt.SetValue('NA')
		self.tcScoreVal.SetValue('0')
	#---

	####---- Methods of the class
	##-- General	
	def WidgetsDestroy(self, name):
		""" Destroy default widgets not needed for window with name """
	 #--> ProtProf
		if name == config.name['ProtProf']:
			l = [self.buttonSeqRecFile, self.tcSeqRecFile, 
				 self.buttonSeqNatFile, self.tcSeqNatFile, 
				 self.buttonPDBFile,    self.tcPDBFile,
				 self.stTarprot,        self.tcTarprot,
				 self.stPositions,      self.tcPositions,
				 self.stHistWin,        self.tcHistWin,
				 self.stPDB,            self.tcPDB,
				 self.stSeqLength,      self.tcSeqLength,
				 self.stSeq,            self.tcSeq,
				 ]
	 #--> Limprot
		elif name == config.name['LimProt']:
			l = [self.buttonPDBFile,    self.tcPDBFile,
				 self.stPositions,      self.tcPositions,
				 self.stHistWin,        self.tcHistWin,
				 self.stPDB,            self.tcPDB,
	 			 ]
		else:
			pass
	 #--> Destroy
		for k in l:
			k.Destroy()	
	 #--> Return
		return True
	#---

	##-- Bind
	def OnPopUpMenu(self, event):
		""" Show the pop up menu in the wx.ListCtrl. Override as needed """
		pass
	#---

	def OnSeqRecFile(self, event):
		""" Select the recombinant sequence file"""
		if gmethods.TextCtrlFromFF(self.tcSeqRecFile, 
			msg=config.msg['Open']['SeqRecFile'], 
			wcard=config.extLong['Seq']):
			return True
		else:
			return False
	#---

	def OnSeqNatFile(self, event):
		""" Select the native sequence file """
		if gmethods.TextCtrlFromFF(self.tcSeqNatFile,
			msg=config.msg['Open']['SeqNatFile'], 
			wcard=config.extLong['Seq']):
			return True
		else:
			return False
	#---
	##-- Menu
	def AddFromList(self, MId):
		""" Adds the selected columns in the list box to the appropiate field in
			Columns in the input file. 
			---
			MId: ID from the pop up menu. It matches one key in self.ColDic (int)
		"""
	 #--> Variables
		addlist = gmethods.ListCtrlGetSelected(self.lb)
		target  = self.ColDic[MId] # wx.TextCtrl to write to the selected columns in the wx.ListBox
	 #--> Add values
		if addlist:
			val = target.GetValue()
	  #--> Check initial value in wx.TextCtrl before adding the new column numbers 
			if val == '' or val in config.naVals:
				target.SetValue(' '.join(str(e) for e in addlist))
			else:
				val = val.split(' ')
				val = val + addlist
				target.SetValue(' '.join(str(e) for e in val))
		else:
			pass
	 #--> Return
		return True
	#---

	def ClearListCtrl(self):
		""" Empty wx.ListCtrl as indicated from PopUp menu """
		self.lb.DeleteAllItems()
		return True
	#---

	def OnSaveInputF(self):
		""" Save a uscr directly from the module. Override in module """
		pass
	#---	
#---

class WinUtilUno(WinMyFrame, GuiChecks, ElementClearAFV, ElementHelpRun, 
	ElementDataFile, ElementOutputFileFolder):
	""" Basic elements for the util windows. Used in: AA dist, Correlation,
		Histograms, Sequence Alignment """

	def __init__(self, parent, style=None, length=20):
		""" parent: parent of the widgets 
			style: style of the widgets
			length: length for the gauge in ElementHelpRun
		"""
	 #--> Initial Setup
		WinMyFrame.__init__(self, parent=parent, style=style)
		ElementClearAFV.__init__(self, self.panel)
		ElementHelpRun.__init__(self, self.panel, length=length)
	 #--> Widgets
	  #--> Lines
		self.lineHI1 = wx.StaticLine(self.panel)
		self.lineHI2 = wx.StaticLine(self.panel)
		self.lineVI1 = wx.StaticLine(self.panel, style=wx.LI_VERTICAL)
	  #--> Static boxes
		self.boxFiles   = wx.StaticBox(
			self.panel, 
			label=config.msg['StaticBoxNames']['Files']
		)
		self.boxValues  = wx.StaticBox(
			self.panel, 
			label=config.msg['StaticBoxNames']['Values']
		)
	  #--> Needs to be here because of self.boxFiles
		ElementDataFile.__init__(self, self.boxFiles)
		ElementOutputFileFolder.__init__(self, self.boxFiles)
	  #--> StaticText
		self.stValue = wx.StaticText(self.boxValues, 
			label=config.dictWinUtilUno[self.name]['StaticLabel'], 
			style=wx.ALIGN_RIGHT)
	  #--> TextCtrl or ComboBox and Extra Horizontal line
		if self.name == config.name['CorrA']:
			self.TextCtrlorCBox = wx.ComboBox(self.boxValues, value='Log2',  
				choices=config.combobox['NormValues'], style=wx.CB_READONLY)
			self.TextCtrlorCBox2 = wx.ComboBox(self.boxValues, value='Pearson',
				choices=config.combobox['CorrAMethod'], style=wx.CB_READONLY)
			self.stMethod = wx.StaticText(self.boxValues, 
				label='Correlation method', style=wx.ALIGN_RIGHT)
		else:
			self.TextCtrlorCBox = wx.TextCtrl(self.boxValues, value="", 
				size=(450, 22))	
	 #--> Tooltips
		self.stValue.SetToolTip(config.tooltip[self.name]['ValueFieldTooltip'])	
	 #--> Sizers
	  #--> Central static boxes
	   #--> Files
		self.sizerboxFiles = wx.StaticBoxSizer(self.boxFiles, wx.VERTICAL)
		self.sizerboxFilesWid = wx.FlexGridSizer(2, 2, 1, 1)
	    #--> Add
		self.sizerboxFiles.Add(self.sizerboxFilesWid,    border=2, 
			flag=wx.ALIGN_CENTER_HORIZONTAL|wx.ALL)
		self.sizerboxFilesWid.Add(self.buttonDataFile,  border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL)
		self.sizerboxFilesWid.Add(self.tcDataFile,      border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerboxFilesWid.Add(self.buttonOutputFF,  border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL)
		self.sizerboxFilesWid.Add(self.tcOutputFF,      border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
	   #--> Values
		self.sizerboxValues = wx.StaticBoxSizer(self.boxValues, wx.VERTICAL)
		if self.name == config.name['CorrA']:
			self.sizerboxValuesWid = wx.FlexGridSizer(1, 4, 1, 1)
		else:
			self.sizerboxValuesWid = wx.FlexGridSizer(1, 2, 1, 1)
		#--> Add
		self.sizerboxValues.Add(self.sizerboxValuesWid, border=2, 
			flag=wx.ALIGN_CENTER_HORIZONTAL|wx.ALL)
		self.sizerboxValuesWid.Add(self.stValue,   border=2, 
			flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL)
		self.sizerboxValuesWid.Add(self.TextCtrlorCBox,   border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		if self.name == config.name['CorrA']:
			self.sizerboxValuesWid.Add(self.stMethod, border=2, 
				flag=wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL)
			self.sizerboxValuesWid.Add(self.TextCtrlorCBox2,   border=2, 
				flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		else:
			pass
	  #--> Central Sizer
		self.sizerBoxes = wx.BoxSizer(wx.VERTICAL)
		self.sizerBoxes.Add(self.sizerboxFiles,   border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerBoxes.Add(self.sizerboxValues,  border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
	  #--- All together in sizerin
		self.sizerIN.Add(self.sizerBoxes,    pos=(0, 2), border=2, 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		if self.name == config.name['CorrA']:
			self.sizerIN.Add(self.sizerClear, pos=(0, 0), border=2, span=(3, 0), 
				flag=wx.EXPAND|wx.ALIGN_TOP|wx.ALL)
			self.sizerIN.Add(self.lineVI1, pos=(0, 1), border=2, span=(3, 0), 
				flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
			self.sizerIN.Add(self.lineHI1, pos=(1, 2), border=2,
				flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
			self.sizerIN.Add(self.lineHI2, pos=(3, 0), border=2, span=(0, 3),
				flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
			self.sizerIN.Add(self.sizerBottom, pos=(4, 0), border=2, 
				span=(0, 3), flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		else:
			self.sizerIN.Add(self.sizerClear, pos=(0, 0), border=2, 
				flag=wx.EXPAND|wx.ALIGN_TOP|wx.ALL)
			self.sizerIN.Add(self.lineVI1,       pos=(0, 1), border=2, 
				flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
			self.sizerIN.Add(self.lineHI1, pos=(1, 0), border=2, span=(0, 3),
				flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
			self.sizerIN.Add(self.sizerBottom, pos=(2, 0), border=2, 
				span=(0, 3), flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)		
	#---

	####---- Methods of the class
	def OnDF(self, event):
		""" To select the data/pdb file in shortDF and cuts2PDB """
	 #--> Variables
		k = True
		msg = config.dictElemDataFile2[self.name]['MsgOpenFile']
		wcard = config.dictElemDataFile2[self.name]['ExtLong']	
		dlg = DlgOpenFile(msg, wcard)
	 #--> Open file
		if dlg.ShowModal() == wx.ID_OK:
			self.tcDF.SetValue(dlg.GetPath())
		else:
			k = False
	 #--> Destroy & Return
		dlg.Destroy()	
		return k
	#---
#---

class WinRes(WinMyFrame, ElementListCtrlSearch):
	""" Basic elements for the util windows. Used in: tarprotR and limprotR """

	def __init__(self, parent=None, style=wx.DEFAULT_FRAME_STYLE):
		""" parent: parent of the widgets 
			style: style of the window
		"""
	 #--> Initial Setup
		fname = self.fileP.name
		title = config.title[self.name] + ' (' + str(fname) + ')'
		WinMyFrame.__init__(self, parent=parent, title=title, style=style)
	 #---

	 #--> Widgets
	  #--> wx.ListBox & wx.SearchCtrl
		ElementListCtrlSearch.__init__(self, parent=self.panel)
		self.lb.SetWindowStyleFlag(
			style=wx.LC_REPORT|wx.BORDER_SIMPLE|wx.LC_SINGLE_SEL)
	  #--- Lines
		self.VI1 = wx.StaticLine(self.panel, style=wx.LI_VERTICAL)
	 #---

	 #--> Automatically create the file object based on self.name
		try:
			self.fileObj
		except Exception:
			try:
				self.fileObj = config.pointer['dclasses']['DataObj'][self.name](self.fileP)
			except Exception as e:
				raise ValueError('')
	 #---

	 #--> Automatically fill the listbox
		try:
			self.FillListBox()
		except Exception as e:
			DlgUnexpectedErrorMsg(str(e))
			raise ValueError('')
	 #---

	 #--> Bind
		if config.cOS == 'Darwin':
			self.lb.Bind(wx.EVT_KILL_FOCUS, self.OnFocusKill)
		else:
			pass
	 #---
	#---

	####---- Methods of the class
	def FillListBox(self, col=None, df=None):
		""" Fill the list box depending on self.name """
	 #--> Empty the listctrl
		self.lb.DeleteAllItems()
	 #--> Get new information
		l = config.pointer['dmethods']['fillListCtrl'][self.name](
			self,
			col=col, 
			df=df,
		)
	 #--> Show the new info
		gmethods.ListCtrlColNames(l, self.lb, mode='list', startIn=1)
	 #-->
		return True
	#---
	
	def OnClose(self, event):
		""" Update config.winOpen. Override from parent	"""
		config.win['Open'].remove(self)
		self.Destroy()
		return True
	#--- 

	def OnFocusKill(self, event):
		""" To avoid lb lossing the focus and changing the color of the 
			selected peptide 

			It only work in macOS. In Win10 prevents the entire window to loose
			focus
		"""
		self.lb.SetFocus()
		return True
	#---	
#---

class WinResUno(WinRes, ElementFragPanel):
	""" Basic elements for the util windows. Used in: tarprotR and limprotR """

	def __init__(self, parent=None, style=wx.DEFAULT_FRAME_STYLE):
		""" parent: parent of the widgets 
			style: style of the window
		"""
	 #--> Initial Setup
		try:
			WinRes.__init__(self, parent=parent, style=style)
		except Exception:
			raise ValueError('')
	 #--> Variables
	  #--> nLines is the number of experiments in tarprotR or the maximum
	  #    number of bands in limprotR
		self.nLinesT = self.fileObj.nLinesT
		self.nLines  = self.fileObj.nLines
	  #--> Colors
		self.Colors = dmethods.GetColors(self.nLines)
	  #--> Total height of self.p1		
		self.hT = (config.lpprot[self.name]['RectH'] 
			+ (self.nLinesT + 1) * config.lpprot[self.name]['RectT'])
		hAvail = (config.size['Screen'][1] 
				  - config.lpprot[self.name]['PanelBelow'])
		if self.hT >= hAvail:
			self.h = (config.size['Screen'][1] 
					- config.lpprot[self.name]['PanelBelow'])
		else:
			self.h = self.hT				
	 #--> Widgets
	  #--> Frag panel
		ElementFragPanel.__init__(self, parent=self.panel)
	  #--> Text Ctrl
		self.text = wx.TextCtrl(self.panel, 
			size=config.size['TextCtrl'][self.name]['TextPanel'], 
			style=wx.BORDER_SIMPLE|wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
		self.text.SetFont(config.font[self.name])
	  #--> Lines
		self.VI1 = wx.StaticLine(self.panel, style=wx.LI_VERTICAL)
		self.lineHI1 = wx.StaticLine(self.panel)
		self.lineVI2 = wx.StaticLine(self.panel, style=wx.LI_VERTICAL)
	 #--> Sizers
	  #--> Add 	
		self.sizerIN.Add(self.sizerLB, pos=(0,0), border=2, span=(3, 0), 
			flag=wx.EXPAND|wx.ALIGN_TOP|wx.ALL)
		self.sizerIN.Add(self.VI1,     pos=(0,1), border=2, span=(3, 0),
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerIN.Add(self.p1,      pos=(0,2), border=2, span=(0, 3),
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerIN.Add(self.lineHI1, pos=(1,2), border=2, span=(0, 3),
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		#--->>> space for self.p2 at pos(2, 2)
		self.sizerIN.Add(self.lineVI2, pos=(2,3), border=2,
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerIN.Add(self.text,    pos=(2,4), border=2,
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
	  #--> Grow Col/Row
		self.sizerIN.AddGrowableRow(2, 0)
		self.sizerIN.AddGrowableCol(2, 0)
		self.sizerIN.AddGrowableCol(4, 0)		
	 #--> Automatically fill the listbox
		self.FillListBox()
	 #--> Bind
		self.Bind(wx.EVT_SIZE, self.OnSize)
		#---
		self.p1.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
		self.p1.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
		#---
		self.text.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)	
	#---

	####---- Methods of the class
	def OnClick(self, event):
		""" To show the menu in the matplotlib panel. Override as needed """
		return True
	#---

	def OnRightDown(self, event):
		""" Display the popup menu Override as needed"""
		return True
	#---

	def OnSetFocus(self, event):
		""" When p1 get the focus return it to the listbox. Mainly for MacOS
		"""
		self.lb.SetFocus()
		event.Skip()
		return True
	#---

	def OnSize(self, event):
		""" To control the update of FraP because of OnPaint does not do it. 
		PROBABLY A PROBLEM IN WIN7??? """
		self.p1.Refresh()
		self.p1.Update()
		self.p2.Refresh()
		self.p2.Update()
		event.Skip()
		return True
	#---

	def OnListSelect(self, event):
		""" When selecting a sequence in the list show intensities and fragments
		"""
	 #--> Get seq, intL and draw on p2
		self.selSeq  = gmethods.ListCtrlGetColVal(self.lb, col=1, t='str')[0]
		if self.name == config.name['TarProtRes']:
			#--> Get all fragments containing self.selSeq. 
			# It could be partially contained in a bigger peptide 
			self.seq = self.f[self.f.loc[:,'Sequence'].str.contains(self.selSeq, regex=False)]
			a = self.seq.apply(self.SeqMatch, axis=1, args=[self.selSeq], raw=True)
			self.seq = self.seq.loc[a,:]
			#-->
			self.lbSelPlot = True	
			intL = self.fileObj.dataF.loc[self.fileObj.dataF.loc[:,'Sequence']==self.selSeq]
			#-->
			label = ['Control Exp']
			for i in range(1, self.nExp+1, 1):
				label.append('Exp' + str(i))
			#-->
			intLplot, lok = self.DFL2DF(intL, label)
			#-->
			self.DrawI(self.selSeq, intLplot, lok, label)
		elif self.name == config.name['LimProtRes']:
			dmethods.GHelperLBSelUpdate(self)
		else:
			pass
	 #--> Draw
		self.p1.Refresh()
		self.p2.Refresh()
		self.Update()
	 #--> Return
		return True
	#---

	def WinPos(self):
		""" Set the position of a new window depending on the number of same
		windows already open """
	 #--> Variables
		xo, yo = config.coord['TopXY']
	 #--> Number of windows already created
		if self.name == config.name['TarProtRes']:
			Nwin = config.win['TarProtResNum']
		elif self.name == config.name['LimProtRes']:
			Nwin = config.win['LimProtResNum']
	 #--> Position of the new window
		x = xo + Nwin * config.win['DeltaNewWin']
		y = yo + Nwin * config.win['DeltaNewWin']
		self.SetPosition(pt=(x, y))
	 #--> Update the number of created windows
		if self.name == config.name['TarProtRes']:
			config.win['TarProtResNum'] = config.win['TarProtResNum'] + 1
		elif self.name == config.name['LimProtRes']:
			config.win['LimProtResNum'] = config.win['LimProtResNum'] + 1		
	 #--> Return
		return True 
	#---

	def SeqMatch(self, row, seqS):
		""" Makes sure seqS appears exactly in row and not just as part of
			a bigger peptide
			---
			row: row from the data frame
			seqS: sequence to search (string) 
		"""
		seqL = row[-2].split(' ')
		if seqS in seqL:
			return True
		else:
			return False
	#--- 
#---

class WinResDos(WinRes):
	""" To show a window with the listbox/search tuple plus a matplotlib panel
	"""

	def __init__(self, win, parent):
		""" win: reference to the window to create the statusbar 
			parent: parent for the widgets
		"""
	 #--> Initial Setup
		try:
			super().__init__(parent=parent)
		except Exception:
			raise ValueError('')			
	 #--> Widgets
	  #--> Lines
		self.lineVI10 = wx.StaticLine(self.panel, style=wx.LI_VERTICAL)
	  #--> Status bar
		self.statusbar = win.CreateStatusBar()
	  #--> Graph panel
		self.p2 = ElementGraphPanel(self.panel, self.name, stBar=self.statusbar)
	 #--> Sizers
	  #--> Add
		self.sizerIN.Add(self.sizerLB,  pos=(0,0), border=2,
			flag=wx.EXPAND|wx.ALIGN_TOP|wx.ALL)
		self.sizerIN.Add(self.lineVI10, pos=(0,1), border=2,
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerIN.Add(self.p2,       pos=(0,2), border=2,
			flag=wx.EXPAND|wx.ALIGN_TOP|wx.ALL)
	  #--> Grow Col/Row
		self.sizerIN.AddGrowableRow(0, 1)
		self.sizerIN.AddGrowableCol(2, 1)
	#---

	####---- Methods of the class
	##-- Menu
	def OnSavePlotImage(self):
		""" Save plot in the graph """
		if self.p3.OnSaveImage():
			return True
		else:
			return False
	#---
#---

class WinResDosDos(WinResDos):
	""" To show a window like in ProtProfRes """

	def __init__(self, win, parent):
		""" win: reference to the window to create the status bar
			parent: parent of the widgets
		"""
	 #--> Initial Setup
		try:
			super().__init__(win, parent)
		except Exception:
			raise ValueError('')
	 #--> Widgets
	  #--> Second Graph panel
		self.p3 = ElementGraphPanel(self.panel, self.name, stBar=self.statusbar)
	  #--> Vertical line
		self.VI2 = wx.StaticLine(self.panel, style=wx.LI_VERTICAL)
	 #--> Sizers
	  #--> Add
		self.sizerIN.Add(self.VI2, pos=(0,3), border=2,
			flag=wx.EXPAND|wx.ALIGN_TOP|wx.ALL)
		self.sizerIN.Add(self.p3,  pos=(0,4), border=2,
			flag=wx.EXPAND|wx.ALIGN_TOP|wx.ALL)	
	  #--> Grow Col/Row
		self.sizerIN.AddGrowableCol(4, 1)		
	#---
#---
# ------------------------------------------------------------ GUI WINDOWS (END)




