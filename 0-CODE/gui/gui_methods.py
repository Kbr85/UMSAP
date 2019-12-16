# ------------------------------------------------------------------------------
#	Copyright (C) 2017-2019 Kenny Bravo Rodriguez <www.umsap.nl>
	
#	This program is distributed for free in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
	
#	See the accompaning licence for more details.
# ------------------------------------------------------------------------------


""" This module contains the methods helping to control the GUI of the app """


# ------------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Methods
# ------------------------------------------------------------------------------



#--- Imports
## Standard modules
import wx
import os
import math
import requests
import webbrowser
import pandas as pd
from pathlib import Path
## My modules
import config.config     as config
import gui.gui_classes   as gclasses
import data.data_classes as dclasses
import data.data_methods as dmethods
#---



# -------------------------------------------------------- Window creation
def WinMUCreate(winID):
	""" Creates the window for modules and utilities in the GUI.
		---
		winID : config.name['Win Name']
	"""
 #--> Minimize Main & Util
	if winID in config.winNoMinMainUtil:
		pass
	elif winID != config.name['Main']:
		config.win['Main'].Iconize(True)
		try:
			config.win['Util'].Iconize(True)
		except Exception:
			pass
	else:
		pass	
 #--> Create window or Raise already created window
	if config.win[winID] is None:
		config.win[winID] = config.pointer['gmethods']['WinCreate'][winID]()
		config.win['Open'].append(config.win[winID])
		config.win[winID].Raise()
	else:
		config.win[winID].Iconize(False)
		config.win[winID].Raise()
 #--> Return
	return True	
#---

def WinGraphResCreate(winID, file):
	""" Creates the window for showing results 
		---
		winID : config.name['Win Name']
		file: file with results (string or Path)
	"""
 #--> Create the window
	#try:
	test = config.pointer['gmethods']['WinCreate'][winID](file)
	config.win['Open'].append(test)
	config.win['Main'].Iconize(True)
	#except Exception:
	#	return False
 #--> Return
	return True
#---

def WinTypeResCreate(winID, parent, parentName=None):
	""" Creates windows like the one for typing result column numbers. Since 
		this windows are explicitly destroyed by the user or by the parent 
		module they are not added to the config.win['Open'] list
		---
		winID : config.name['Win Name']
		parent: parent of the window, to close it if the parent window is closed
	"""
 #--> Check that no other window for this module already exists
	if parent.name in config.win['TypeRes'].keys():
		config.win['TypeRes'][parent.name].Iconize(False)
	else:
 #--> Create the window
		config.win['TypeRes'][parent.name] = config.pointer['gmethods']['WinCreate'][winID](parent, parentName)
 #--> Return
	return True
#---
# -------------------------------------------------------- Window creation (END)



# ----------------------------------------------------------------- Update
def UpdateCheck(ori, ):
	""" Check for updates for UMSAP from another thread 
		---
		ori: origin of the request (string)
	"""
 #--> Variables
	k = True
 #--> Get text from Internet
	try:
		r = requests.get(config.url['Update'])
	except Exception:
		k = False
 #--> Get Internet version
	if k:
		if r.status_code == requests.codes.ok:
			text = r.text.split('\n')
			for i in text:
				if 'UMSAP v' in i:
					versionI = i
					break
			versionI = versionI.split('UMSAP v')[1].split()[0].split('.')
			config.versionInternet = list(map(int, versionI))
 #--> Compare with program version
			config.updateAvail = dmethods.VersionCompare()
 #--> Prompt msg
			if config.updateAvail == 1:
				wx.CallAfter(WinMUCreate, config.name['UpdateNotice'])
			elif config.updateAvail == 0 and ori == 'menu':
				wx.CallAfter(WinMUCreate, config.name['UpdateNotice'])
			else:
				pass
		else:
			k = False
	else:
		pass
 #--> Return
	if k:
		return True
	else:
		msg = config.dictCheckFatalErrorMsg[config.name['UpdateNotice']]['UMSAPSite']
		wx.CallAfter(gclasses.DlgFatalErrorMsg, msg)
		return False
#---

def UpdateGaugeText(gauge, sT, msg, val=1):
	""" Update the text and the gauge in the module/util window when running a 
		data processing 
		---
		gauge: wx.Gauge
		sT: wx.TextCtrl
		msg: msg to show (string)
		val: valut to increase the gauge count (int)
	"""
	v = gauge.GetValue()
	v = v + val
	gauge.SetValue(v)
	sT.SetLabel(msg)
	return True
#---

def UpdateText(sT, msg):
	""" Update the text in a module/util window when runnig a data processing 
		---
		st: wx.TextCtrl
		msg: msg to show (string)
	"""
	sT.SetLabel(msg)
	return True
#---
# ----------------------------------------------------------------- Update (END)



# -------------------------------------------------------------- Statusbar
def StatusBarXY(x, y):
	""" Takes x, y coordinates and return formatted string """
	string = "x=" + "{0:.2f}".format(x) + "  y=" + "{0:.2f}".format(y)
	return string
#---
# -------------------------------------------------------------- Statusbar (END)



# ------------------------------------------------------------ wx.ListCtrl
def ListCtrlHeaders(lb, name):
	""" Add the header # and Column Name to a ListCtrl plus the widths 
		---
		lb: wx.ListBox to fill
		name: name of the window to look data in config (string)
	"""
 #--> Get header & size
	header = config.listctrl['Header'][name] 
	size   = config.listctrl['Widths'][name]
 #--> Fill the wx.ListBox
	for i in range(0, len(header), 1):
		lb.InsertColumn(i, header[i])
		lb.SetColumnWidth(i, size[i])		
 #--> Return
	return True
#---

def ListCtrlColNames(file, lb, mode='file', delAll=True, startIn=0):
	""" To fill the listbox in tarprot and tarprotR 
		---
		file: file with the columm names or list of list (string or Path or list of list)
		lb: wx.ListBox to fill
		mode: to know how to treat file (string: 'file' or 'list')
		delAll: delete previous values in wx.ListBox
		startIn: start column numbers in start (int)
	"""
 #--> Set line
	if mode == 'file':
		file = Path(file)
		with file.open(mode='r') as f:
			line = f.readline()
		line = line.split("\t")
	elif mode == 'list':
		line = file
	else:
		return False
 #--> Delete previous values in wx.ListBox and set the value for # column in wx.ListBox
	if delAll:
		lb.DeleteAllItems()
		n = 0 + startIn
	else:
		n = lb.GetItemCount()
 #--> Fill the wx.ListBox
	for i in line:
  #--> Add row number
		index = lb.InsertItem(n, " " + str(n))
  #--> Check i for list of list & write
		if isinstance(i, list):
			col = 1
			for ii in i:
				if ListCtrlColNamesHelper(lb, index, ii, col):
					col += 1			
				else:
					return False
		else:
			if ListCtrlColNamesHelper(lb, index, i):
				pass
			else:
				return False
		n += 1
 #--> Color & Return
	ListCtrlZebraStyle(lb)
	return True
#---

def ListCtrlColNamesHelper(lb, index, i, col=1):
	""" Helper to ListCtrlColNames 
		---
		lb: wx.ListBox to add spot value
		index: current index to write into (wx.ListBox index object)
		i: value to write (string or nan float)
		col: column to write into (int)
	"""
 #--> Check i for non string values, especially nan values
	if isinstance(i, str):
			fi = i
	else:
		if math.isnan(i):
			fi = ''			
		else:
			try:
				fi = str(i)
			except Exception:
				return False
 #--> Fill wx.ListBox	
	lb.SetItem(index, col, fi)
 #--> Return
	return True
#---

def ListCtrlZebraStyle(lb, color=config.colors['listctrlZebra']):
	""" Alternate background color of a wx.Listbox 
		---
		lb: wx.ListBox to color
		color: color to use 
	"""
 #--> Get total items in wx.ListBox
	totalItems = lb.GetItemCount()
 #--> Set color
	for i in range(totalItems):
		r = i % 2
		if r == 0:
			lb.SetItemBackgroundColour(i, color)
		else:
			lb.SetItemBackgroundColour(i, 'white')
 #--> Return
	return True
#---

def ListCtrlGetSelected(lb): 
	""" Get all selected items in a wx.ListCtrl 
		---
		lb: wx.ListBox 
	"""
 #--> Variables
	totalItems = lb.GetItemCount()
	selItems   = []
 #--> Get selected
	#--# IMPROVED (DOWN) This means that you have to iterate the entire list
	# Should be faster with GetFirstSelected, GetNextSelected and GetSelecteItemCount
	for i in range(totalItems):
		if lb.IsSelected(i):
			selItems.append(i)
		else:
			pass
	#--# IMPROVED (UP)
 #--> Return
	return selItems
#---

def ListCtrlDeleteSelected(lb):
	""" Delete selected items in a wx.ListCtrl 
		---
		lb: wx.ListBox
	"""
 #--> Get selected items 
	sel = ListCtrlGetSelected(lb)
	sel.sort(reverse=True)
 #--> Delete in reverse order to avoid changing undeleted indexes
	for i in sel:
		lb.DeleteItem(i)
 #--> Color remaining rows
	if lb.GetItemCount() > 0:
		ListCtrlZebraStyle(lb)
	else:
		pass
 #--> Return
	return True
#---

def ListCtrlGetColVal(lb, col=0, sel=None, t='int'):
	""" Get the values of a column in a wx.ListCtrl, in the same order as shown
		in the wx.ListCtrl. 
		---
		lb: wx.ListCtrl
		col: column to get values from (int)
		sel: selected values in the wx.ListBox
		t: type of extracted values (string: 'int' or 'str')
	"""
 #--> Get selected items if nothing is selected get everything
	if sel == None:
		selItems = ListCtrlGetSelected(lb)
		if len(selItems) == 0:
			selW = range(lb.GetItemCount())
		else:
			selW = selItems
	else:
		selW = sel
 #--> Variables
	colV = []
 #--> Get value in column
	for i in selW:
		colV.append(lb.GetItemText(i, col).strip())
 #--> Adjust type of values
	if t == None:
		pass		
	elif t == 'int':
		colV = list(map(int, colV))
	elif t == 'str':
		colV = list(map(str, colV))
 #--> Return
	return colV
#---

def ListCtrlSearchVal(lb, string, startI=1):
	""" Search a listbox (lb) for string. If string is not 
		found then return a list of rows containing string (*string*). 
		---
		lb: wx.ListBox
		string: string to search in wx.ListBox (string)
		startI : starting number for the row index (int)
	"""
 #--> Variables
	sel  = []
	seqs = []
	totalItems = lb.GetItemCount()
 #--> Search the wx.ListBox
	for i in range(totalItems):
		for c in range(0, lb.GetColumnCount(), 1):
			s = lb.GetItemText(i, c)
			e = [i + startI, s]
			if string in s:
				seqs.append(e)
			else:
				pass
			if s == string:
				sel.append(i)
 #--> Show results
	n = len(sel)
  #--> n>1
	if n > 1:
		msg = ("The string " + string + " was found " + str(n) + " "
			"times in the list.\nThis should not happen.\nIt is recommended to "
			"regenerate the file using UMSAP.")
		gclasses.DlgFatalErrorMsg(msg)
		return False
  #--> n == 1
	elif n == 1:
		ListCtrlDeSelAll(lb)
		lb.Select(sel[0])
		lb.EnsureVisible(sel[0])
  #--> n == 0
	elif n == 0:
		m = len(seqs)
   #--> m > 0 
		if m > 0:
			mes = [str(s[0]) + ' ' + str(s[1]) for s in seqs]
			mes = '\n'.join(mes)
			msg = ("The exact string " + string + " was not found in the list."
				"\n\nThe following entries contain the searched string:\n\n" 
				+ mes)
			gclasses.DlgScrolledDialog(msg)
			return True
   #--> m == 0	
		elif m == 0:
			msg = ("The exact string " + string + " was not found in the list\n"
				"or within any entry in the list.")
			gclasses.DlgWarningOk(msg)
			return True
		else:
			pass
#---

def ListCtrlDeSelAll(lb):
	""" Deselect all items in list box 
		---
		lb: wx.ListCtrl
	"""
 #--> Get Selected
	selected = ListCtrlGetSelected(lb)
 #--> Deselect & Return
	for s in selected:
		lb.Select(s, on=0)
	return True
#---

def ListCtrlRenumberLB(lb):
	""" Renumbers the elements in the list box e.g. after deleting selecting 
		items. It assumes column 0 in the wx.ListBox holds the number of the row.
		---
		lb: wx.ListBox
	"""
 #--> Total item
	totalItems = lb.GetItemCount()	
 #--> Renumber
	for i in range(totalItems):
		j = i + 1
		lb.SetItem(i, 0, ' ' + str(j))
	return True
#---
# ------------------------------------------------------------ wx.ListCtrl (END)



# ------------------------------------------------------------ wx.TextCtrl
def TextCtrlEmpty(sb):
	""" Set the values of all wx.TextCtrl that are children of a wx.StaticBox 
		to ''.
		---
		sb: wx.StaticBox
	"""
 #--> Get all childrens of sb
	children = sb.GetChildren()
 #--> Set wx.TextCtrl to ''
	for child in children:
		if isinstance(child, wx.TextCtrl):
			child.SetValue("")
 #--> Return
	return True
#---

def TextCtrlFromFF(tc, mode='file', msg=None, wcard=None):
	""" Fill a tc with a selected file or folder. mode=[file, folder, save] 
		---
		tc: wx.TextCtrl
		mode: string to know which dlg window to show (string: 'file', 'folder', 'save')
		msg: msg to show in the dlg window (string) 
		wcard: wildcard (config.extLong)
	"""
 #--> Create the corresponding dlg window
	if mode == 'file':
		dlg = gclasses.DlgOpenFile(msg, wcard)
	elif mode ==  'folder':
		dlg = gclasses.DlgOpenDir()
	elif mode == 'save':
		dlg = gclasses.DlgSaveFile(wcard, msg)
	else:
		pass
 #--> Show the window and set the value of wx.TextCtrl 
	if dlg.ShowModal() == wx.ID_OK:
		tc.SetValue(dlg.GetPath())
	else:
		pass	
 #--> Destroy & Return
	dlg.Destroy()
	return True		
#---
# ------------------------------------------------------------ wx.TextCtrl (END)



# ---------------------------------------------- Windows Position and size
def MinSize(win):
	""" Set the minimum size of a window to its minimum size when 
		initially drawn
		---
		min: reference to a window
	"""
	size = win.GetSize()
	win.SetMinSize(size)
	return True
#---
# ---------------------------------------------- Windows Position and size (END)



# ---------------------------------------------------------- Launch module
def LaunchTarProt(data):
	""" Launch the tarprotM with the data from a uscr file 
		---
		data: dict with the data (dict)
	"""
 #--> Create the window
	WinMUCreate(config.name['TarProt'])
 #--> Clear all wx.TextCtrl
	config.win['TarProt'].OnClearAll('event')
 #--> Define dict with the involved widgets. Cannot be in config because
 #		when config is imported for the first type config.win['TarProt'] is None
 # 		and does not have any of the widgets
	widgets = {
		'Datafile'        : config.win['TarProt'].tcDataFile,
		'Seq_rec'         : config.win['TarProt'].tcSeqRecFile,
		'Seq_nat'         : config.win['TarProt'].tcSeqNatFile,
		'PDBfile'         : config.win['TarProt'].tcPDBFile,
		'Outputfolder'    : config.win['TarProt'].tcOutputFF,
		'Outputname'      : config.win['TarProt'].tcOutName,
		'Targetprotein'   : config.win['TarProt'].tcTarprot,
		'Scorevalue'      : config.win['TarProt'].tcScoreVal,
		'Datanorm'        : config.win['TarProt'].cbDataNorm,
		'aVal'            : config.win['TarProt'].cbaVal,
		'Positions'       : config.win['TarProt'].tcPositions,
		'Sequencelength'  : config.win['TarProt'].tcSeqLength,
		'Histogramwindows': config.win['TarProt'].tcHistWin,
		'PDBID'           : config.win['TarProt'].tcPDB,
		'SeqCol'          : config.win['TarProt'].tcSeq,
		'DetectProtCol'   : config.win['TarProt'].tcDetProt,
		'ScoreCol'        : config.win['TarProt'].tcScore,
		'ColExtract'      : config.win['TarProt'].tcColExt,
		'Results'         : config.win['TarProt'].tcResults,
	}
 #--> Set data
	LaunchHelper(data, widgets)	
 #--> Raise the window & Return		
	config.win['TarProt'].Iconize(False)
	return True	
#---

def LaunchLimProt(data):
	""" Launch the tarprotM with the data from a uscr file 
		---
		data: dict with the data (dict)
	"""
 #--> Create the window
	WinMUCreate(config.name['LimProt'])
 #--> Empty all wx.TextCtrl
	config.win['LimProt'].OnClearAll('event')
 #--> Define dict with the involved widgets. Cannot be in config because
 #		when config is imported for the first type config.win['LimProt'] is None
 # 		and does not have any of the widgets
	widgets = {
		'Datafile'      : config.win['LimProt'].tcDataFile,
		'Seq_rec'       : config.win['LimProt'].tcSeqRecFile,
		'Seq_nat'       : config.win['LimProt'].tcSeqNatFile,
		'Outputfolder'  : config.win['LimProt'].tcOutputFF,
		'Outputname'    : config.win['LimProt'].tcOutName,
		'Targetprotein' : config.win['LimProt'].tcTarprot,
		'Scorevalue'    : config.win['LimProt'].tcScoreVal,
		'Datanorm'      : config.win['LimProt'].cbDataNorm,
		'Sequencelength': config.win['LimProt'].tcSeqLength,
		'aVal'          : config.win['LimProt'].cbaVal,
		'bVal'          : config.win['LimProt'].cbbVal,
		'yVal'          : config.win['LimProt'].cbyVal,
		'duVal'         : config.win['LimProt'].tcDeltaU,
		'dmVal'         : config.win['LimProt'].tcDelta,
		'SeqCol'        : config.win['LimProt'].tcSeq,
		'DetectProtCol' : config.win['LimProt'].tcDetProt,
		'ScoreCol'      : config.win['LimProt'].tcScore,
		'ColExtract'    : config.win['LimProt'].tcColExt,
		'Results'       : config.win['LimProt'].tcResults,
	}
 #--> Set data
	LaunchHelper(data, widgets)
 #--> Raise & Return		
	config.win['LimProt'].Iconize(False)
	return True	
#---

def LaunchProtProf(data):
	""" Launch the tarprotM with the data from a uscr file 
		---
		data: dict with the data (dict)
	"""
 #--> Create window
	WinMUCreate(config.name['ProtProf'])
 #--> Empty all wx.TextCtrl
	config.win['ProtProf'].OnClearAll('event')
 #--> Define dict with the involved widgets. Cannot be in config because
 #		when config is imported for the first type config.win['ProtProf'] 
 # 		is None and does not have any of the widgets
	widgets = {
		'Datafile'     : config.win['ProtProf'].tcDataFile,
		'Outputfolder' : config.win['ProtProf'].tcOutputFF,
		'Outputname'   : config.win['ProtProf'].tcOutName,
		'Scorevalue'   : config.win['ProtProf'].tcScoreVal,
		'ZscoreVal'    : config.win['ProtProf'].tcZscore,
		'Datanorm'     : config.win['ProtProf'].cbDataNorm,
		'aVal'         : config.win['ProtProf'].cbaVal,
		'median'       : config.win['ProtProf'].chb,
		'CorrP'        : config.win['ProtProf'].cbCorrP,
		'DetectProtCol': config.win['ProtProf'].tcDetProt,
		'GeneNCol'     : config.win['ProtProf'].tcGeneN,
		'ScoreCol'     : config.win['ProtProf'].tcScore,
		'ExcludeCol'   : config.win['ProtProf'].tcExclude,
		'ColExtract'   : config.win['ProtProf'].tcColExt,
		'Results'      : config.win['ProtProf'].tcResults,
	}
 #--> Fix data type to avoid error in LauchHelper
	try:
		if data['median'] == 'True':
			data['median'] = True
		elif data['median'] == 'False':
			data['median'] = False
		else:
			pass
	except KeyError:
		pass
 #--> Set data
	LaunchHelper(data, widgets)
  #--> Further options
	try:
		config.win['ProtProf'].CType = str(data['CType'])   
	except KeyError:
		pass
	try:
		config.win['ProtProf'].LabelControl = str(data['LabelControl'])
	except KeyError:
		pass
	try:
		a = data['LabelCond'].split(',') 
		config.win['ProtProf'].LabelCond = [x.strip() for x in a] 
	except KeyError:
		pass
	try:
		a = data['LabelRP'].split(',')
		config.win['ProtProf'].LabelRP = [x.strip() for x in a]    
	except KeyError:
		pass
 #--> Raise & Return		
	config.win['ProtProf'].Iconize(False)
	return True	
#---

def LaunchHelper(data, widgets):
	""" Helper to Launch methods 
		---
		data    : dict with keywords - value pairs
		widgets : dict with keywords - widgets pairs
	"""
 #--> Fill widget
	for k, v in data.items():
		try:
			widgets[k].SetValue(v)
		except KeyError:
			pass
 #--> Return
	return True
#---
# ---------------------------------------------------------- Launch module (END)



# ---------------------------------------------------------- Image Methods
def SaveMatPlotImage(figure, wcard, msg):
	""" Save an image to path from a matplotlib figure object 
		---
		figure: matplotlib figure object
		wcard: file extension (config.extLong)
		msg: msg to show (string)
	"""
 #--> Variables
	k   = True
	dlg = gclasses.DlgSaveFile(wcard, msg)
 #--> Show dlg window & Save
	if dlg.ShowModal() == wx.ID_OK:
		path = dlg.GetPath()
		try:
			figure.savefig(path, dpi=config.image['DPI'])
		except Exception:
			gclasses.DlgFatalErrorMsg(config.msg['Errors']['ImgNotSaved'])
			k = False
	else:
		k = False
 #--> Destroy & Return
	dlg.Destroy()
	return k
#---

def NoDataImage(win):
	""" Show an empty plot when no data
		---
		win: reference to the window with the matplotlib figure 
	"""
	win.ClearPlot()
	win.axes.set_title('No data available')
	win.SetAxis()
	win.canvas.draw()
	return True
#---
# ---------------------------------------------------------- Image Methods (END)



# ------------------------------------------------------------------- Menu
####---- 200 Section
#---# Improve (DOWN) Perhaps these methods can be combined in just one
def MenuOnReanalyseTP():
	""" Read a .tarprot file and fill the Tarprot module with the input 
		found in the file so users can make quick changes. It is intended 
		for update and change results from old .tarprot file for wich a 
		configuration file is not available.
	"""
 #--> Variables
	k = True
	dlg = gclasses.DlgOpenFile(config.msg['Open']['TarProtFile'],
		config.extLong['TarProt'])
 #--> Get path to file
	if dlg.ShowModal() == wx.ID_OK:
		fLoc = Path(dlg.GetPath())
 #--> Create tarprot object
		try:
			fileObj = dclasses.DataObjTarProtFile(fLoc)
		except Exception:
			k = False
 #--> Fill the module window
		if k:
			fileObj.TarProtFile2TarProtModule()
		else:
			pass
	else:
		k = False
 #--> Destroy & Return
	dlg.Destroy()
	return k
#---

def MenuOnUpdateTP():
	""" Reads a .tarprot file and creates all the associated files """
 #--> Variables
	k = True
	dlgi = gclasses.DlgOpenFile(config.msg['Open']['TarProtFile'],
		config.extLong['TarProt'])
 #--> Get path to file
	if dlgi.ShowModal() == wx.ID_OK:
		fLoc = Path(dlgi.GetPath())
 #--> Get path to output folder
		dlgo = gclasses.DlgOpenDir()
		if dlgo.ShowModal() == wx.ID_OK:
			fLocO = Path(dlgo.GetPath())
 #--> Create tarprot object
			try:
				fileObj = dclasses.DataObjTarProtFile(fLoc)
			except Exception:
				k = False
 #--> Run update
			if k:			
				if fileObj.TarProtUpdate(fLocO):
					gclasses.DlgSuccessMsg()
				else:
					k = False
			else:
				k = False
		else:
			k = False
 #--> Destroy dlgo
		dlgo.Destroy()	
	else:
		k = False
 #--> Destroy dlgi & Return
	dlgi.Destroy()
	return k
#---

def MenuOnFPList():
	""" Reads a .tarprot file and creates a .filtpept file """
 #--> Variables
	k = True	
	dlgi = gclasses.DlgOpenFile(config.msg['Open']['TarProtFile'],
		config.extLong['TarProt'])
 #--> Get file Path
	if dlgi.ShowModal() == wx.ID_OK:
		fLoc = Path(dlgi.GetPath())
 #--> Get output folder
		dlgo = gclasses.DlgSaveFile(config.extLong['FiltPept'])
		if dlgo.ShowModal() == wx.ID_OK:
			fLocO = Path(dlgo.GetPath())
 #--> Create tarprot object
			try:
				fileObj = dclasses.DataObjTarProtFile(fLoc)
			except Exception:
				k = False
 #--> Create filter peptide file
			if k:
				if fileObj.checkFP:
					if fileObj.TarProt2FiltPept(fLocO):
						gclasses.DlgSuccessMsg()
					else:
						k = False
				else:
					gclasses.DlgFatalErrorMsg(config.msg['FiltPept'])
					k = False				
			else:
				k = False
		else:
			k = False
 #--> Destroy dlgo
		dlgo.Destroy()
	else:
		k = False
 #--> Destroy dlgi & Return
	dlgi.Destroy()
	return k
#---

def MenuOnCInputFile():
	""" Reads a module main output file (.tarprot, etc) and creates a .uscr file
	"""	
 #--> Variables
	k = True
	dlgi = gclasses.DlgOpenFile(config.msg['Open']['UMSAPMFile'],
		config.extLong['UmsapM'])
 #--> Get path to the file
	if dlgi.ShowModal() == wx.ID_OK:
		fLoc = Path(dlgi.GetPath())
 #--> Get path to the output
		dlgo = gclasses.DlgSaveFile(config.extLong['Uscr'])
		if dlgo.ShowModal() == wx.ID_OK:
			fLocO = Path(dlgo.GetPath())
 #--> Get file extension
			ext = fLoc.suffix
 #--> Create file object
			try:
				fileObj = config.pointer['dclasses']['DataObj'][ext](fLoc)
			except Exception:
				k = False
 #--> Create uscr
			if k:
				out = dmethods.FFsWriteDict2Uscr(fLocO,
					iDict=fileObj.Fdata['I'],
					hDict=config.dictUserInput2UscrFile[config.extName[ext]])
				if out:
					gclasses.DlgSuccessMsg()
				else:
					k = False				
			else:
				k = False
		else:
			k = False
 #--> Destroy dlgo
		dlgo.Destroy()
	else:
		k = False
	if k:
 #--> Destroy dlgi & Return
		dlgi.Destroy()
		return k
	else:
 #--> Show unknown error and exit
		msg = config.msg['UErrors']['Unknown']
		gclasses.DlgFatalErrorMsg(msg)
		return False		
#---

def MenuOnCutProp():
	""" Creates the .cutprop file from a .tarprot file """
 #--> Variables
	k = True
	dlgi = gclasses.DlgOpenFile(config.msg['Open']['TarProtFile'], 
		config.extLong['TarProt'])
 #--> Get path to the file
	if dlgi.ShowModal() == wx.ID_OK:
		fLoc = Path(dlgi.GetPath())
 #--> Get path to the output
		dlgo = gclasses.DlgSaveFile(config.extLong['CutProp'])
		if dlgo.ShowModal() == wx.ID_OK:
			fLocO = Path(dlgo.GetPath())
 #--> Create tarprot file
			try:
				tarprotObj = dclasses.DataObjTarProtFile(fLoc)
			except Exception:
				k = False
 #--> Create cutprop file
			if k:
				if tarprotObj.checkFP:
					if tarprotObj.TarProt2CutProp(fLocO):
						WinGraphResCreate(config.name['CutPropRes'], fLocO)
						gclasses.DlgSuccessMsg()
					else:
						k = False
				else:
					gclasses.DlgFatalErrorMsg(config.msg['FiltPept'])
					k = False
			else:
				k = False						
		else:
			k = False
 #--: Destroy dlgo
		dlgo.Destroy()		
	else:
		k = False
 #--> Destroy dlgi & Return
	dlgi.Destroy()
	return k	
#---
#---# Improve (UP) Perhaps these methods can be combined in just one

def MenuOnReadOutFile():
	""" Read a file generated by UMSAP """
 #--> Variables
	k = True
	dlg = gclasses.DlgOpenFile(config.msg['Open']['UMSAPFile'], 
		config.extLong['UmsapR'])
 #--> Get the path to the file
	if dlg.ShowModal() == wx.ID_OK:
		fLoc = Path(dlg.GetPath())
 #--> Get extension & set name
		ext = fLoc.suffix
		#---
		if ext == config.extShort['CorrA'][0]:
			name = [config.name['CorrARes']]
		#---
		elif ext == config.extShort['TarProt'][0]:
			name = [config.name['TarProtRes']]	
		#---
		elif ext == config.extShort['CutProp'][0]:
			name = [config.name['CutPropRes']]		
		#---
		elif ext == config.extShort['Histo'][0]:
			name = [config.name['HistoRes']]	
		#---
		elif ext == config.extShort['AAdist'][0]:
			name = [config.name['AAdistR']]			
		#---
		elif ext == config.extShort['ProtProf'][0]:
			name = [config.name['ProtProfRes']]
		#---
		elif ext == config.extShort['LimProt'][0]:
			name = [config.name['LimProtRes']]
		#---		
		else:
			gclasses.DlgFatalErrorMsg(config.msg['Errors']['FileExt'])
			k = False
 #--> Create window 
		if k:
			for a in name:	
				if WinGraphResCreate(a, fLoc):
					k = True
				else:
					k = False
		else:
			k = False	
	else:
		k = False
 #--> Destroy & Return
	dlg.Destroy()
	return k
#---

####---- 300 Section
def MenuOnHelpManual():
	""" Shows the manual with the default pdfviewer in the system """
 #--> Get path
	manual = str(config.file['Manual'])
 #--> Open file
	if config.cOS == 'Darwin':
		com = "open "
	elif config.cOS == 'Windows':
		com = "start "
	elif config.cOS == 'Linux':
		com = "xdg-open "
	else:
		pass
	try:
		os.system(com + manual)
	except Exception as e:
		gclasses.DlgUnexpectedErrorMsg(str(e))
		return False
 #--> Return
	return True
#---

def MenuOnHelpTutorials():
	""" Shows the tutorial page at umsap.nl """
	try:
		webbrowser.open_new(config.url['Tutorial'])
	except Exception as e:
		gclasses.DlgUnexpectedErrorMsg(e)
		return False
	return True
#---

####---- 400 Section
def MenuOnMinimizeAll():
	""" Minimize all UMSAP windows """
	for v in config.win['Open']:
		try:
			v.Iconize(True)
		except Exception:
			pass
	return True
#---

def MenuOnQuitUMSAP():
	""" This function terminates the application closing all the windows """
	for v in config.win['Open']:
		try:
			v.Destroy()
		except Exception:
			pass
	return True
#---

####---- 600
def MenuOnRInputFile():
	""" Run the script """
 #--> Variables
	k = True
	dlg = gclasses.DlgOpenFile(config.msg['Open']['InputF'],
		config.extLong['Uscr'])
 #--> Get path to the file
	if dlg.ShowModal() == wx.ID_OK:
		fLoc = Path(dlg.GetPath())
 #--> Create script object
		try:
			fileObj = dclasses.DataObjScriptFile(fLoc)
		except Exception:
			k = False
 #--> Launch module
		if k:
			if fileObj.LaunchModule():
				pass
			else:
				k = False
		else:
			k = False
	else:
		k = False
 #--> Destroy & Return
	dlg.Destroy()
	return k
#---
# ------------------------------------------------------------------- Menu (END)

















