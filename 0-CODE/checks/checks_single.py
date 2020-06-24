# ------------------------------------------------------------------------------
#	Copyright (C) 2017 Kenny Bravo Rodriguez <www.umsap.nl>
	
#	This program is distributed for free in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
	
#	See the accompaning licence for more details.
# ------------------------------------------------------------------------------


""" This module contains methods to check the user input data """


#region -------------------------------------------------------------- Imports
import requests
from pathlib import Path

import config.config as config
import gui.gui_classes as gclasses
import gui.gui_methods as gmethods
#endregion ----------------------------------------------------------- Imports

#region ------------------------------------------------------------ Variables
def CheckVarEmpty(var):
	""" Check if a a widget value is different than ''. 
		---
		var: value to check
		---
		Return True if var != '' else False
	"""
 #--> Check & Return
	return var != ''
 #---
#---

def CheckNumType(var, t='float'):
	""" Check that var holds a number of type t. 
		Returns the number with the correct type. 
		---
		var : variable to check
		t   : possible values: float, int
	"""
 #--> Variables
	k = True
 #---
 #--> Set the correct type
	if t == 'float':
		try:
			varT = float(var)
		except Exception:
			k = False
	elif t == 'int':
		try:
			varT = int(var)
		except Exception:
			k = False
	else:
		### DlgBugMsg
		pass
 #---
 #--> Return
	if k:
		return [True, varT]
	else:
		return [False, None]
 #---
#---

def CheckNumComp(num, comp='egt', val=0):
	""" Compare num to val using comp
		---
		num : number to use in the comparison (int, float, etc)
		comp: egt >= val, e == val, gt > val, elt <= val, lt < val (string)
		val : value to compare against (int, float, etc) 
	"""
 #--> Variables
	k = True
 #---
 #--> Compare
	if comp == 'gt':
		if num > val:
			return True
		else:
			k = False
	elif comp == 'egt':
		if num >= val:
			return True
		else:
			k = False
	elif comp == 'e':
		if num == val:
			return True
		else:
			k = False
	elif comp == 'elt':
		if num <= val:
			return True
		else:
			k = False
	elif comp == 'lt':
		if num < val:
			return True
		else:
			k = False
	else:
		### DlgBugMsg
		pass
 #---
 #--> Return
	if k:
		return True
	else:
		return False
 #---
#---

def CheckaWithincd(a, c, d):
	""" Check that a >= c & a <= d
		---
		a : number to check (int, float, etc)
		b, c : limits of the interval (int, float, etc)
	"""
 #--> Check & Return
	if c <= a and a <= d:
		return True
	else:
		return False
 #---
#---

def CheckabWithincd(a, b, c, d):
	""" Checks that a and b are both >= c and <= d 
		---
		a, b: numbers to check (int, float, etc)
		c, d: limits of the interval (int, float, etc)
	"""
 #--> Check & Return
	if c <= a and a <= d:
		if c <= b and b <= d:
			return True
		else:
			pass
	else:
		pass
	return False
 #---
#---  

def CheckControlExpNA(l):
	""" Check that control experiments in l is not NA 
		---
		l: three level list of list in which the first innermost element is the
		   control experiment. Values are still strings.
		   [[[C0], [E01], [E02]],
			[[C1], [E11], [E12]],
		   					    ]
	"""
 #--> Variables
	k = True
 #---
 #--> Check
	for x in l:
		if x[0][0] in config.naVals:
			k = False
			break
		else:
			pass
		for e in config.naVals[0:-1]:
			if e in x[0][0]:
				k = False
				break
			else:
				pass
 #---
 #--> Return
	if k:
		return True
	else:
		msg = config.msg['Errors']['ControlNA']
		gclasses.DlgFatalErrorMsg(msg)
		return False 
 #---
#---
#endregion --------------------------------------------------------- Variables

#region ---------------------------------------------------------------- Lists
def CheckListUniqueElements(l, NA=False):
	""" Check that a list does not contains repeated elements
		---
		l : flat list
		NA: allow NA elements in the list or not (boolean)
	"""
 #--> Remove multiple NA elements if they are allowed
	if NA == False:
		lo = list(set(l))
	else:
		l = [x for x in l if x != None]
		lo = list(set(l))
 #---
 #--> Compare length of l & lo and Return
	if len(lo) == len(l):
		return True
	else:
		return False
 #---
#---

def CheckListNElements(l, mod=None, msg=None):
	""" Check that a list of list (3 levels) has the same number of elements in
		each level 2. Basically check that each cond/band has the same number of
		tp/lanes. tp/lanes could be just NA but must be present in l.
		---
		l: list of elements (list of list)
		msg: error msg (string)
	"""
 #--> Get number of elements in each element
	n = [len(x) for x in l]
 #---
 #--> Check if they are the same
	if len(list(set(n))) > 1:
		if msg == None:
			if mod == None:
				msgs = config.msg['Errors']['ResultsShape']
			else:
				msgs = config.dictCheckFatalErrorMsg[mod]['ResMatrixShape']
		else:
			msgs = msg
		gclasses.DlgFatalErrorMsg(msgs)
		return False
	else:
		return True
 #---
#---

def CheckListEqualElements(l, msg=None, NA=True):
	""" Takes a list of list (3 levels) and check that each 2 level list has the
		same number of elements in level 3. Basically check that each tp/lane 
		has the same number of replicates in each cond/band 
		---
		l: Results list (3 level list of list)
		msg : Error message to show (string)
		NA: NA values are allowed or not (boolean)
	"""
 #--> Check
	for a in l: # For each cond/band
	 #--> Get number of replicates in each tp/lane
		if NA:
			e = [len(b) for b in a if b[0] != None]
		else:
			e = [len(b) for b in a]
	 #---
	 #--> Check number of replicates
		if len(list(set(e))) > 1:
			if msg == None:
				pass
			else:
				gclasses.DlgFatalErrorMsg(msg)
			return False	
		else:
			pass
	 #---
 #---
 #--> Return
	return True
 #---
#---
#endregion ------------------------------------------------------------- Lists

#region ---------------------------------------------------- Files and Folders
def CheckFileRead(var):
	""" Check if var points to a file that can be read in.
		---
		var : path the file (string or path)
	"""
 #--> Variables
	mfile = Path(var)
 #---
 #--> Check & Return
	try:
		fo = open(mfile, 'r')
		fo.close()
		return True
	except Exception:
		return False
 #---
#---

def CheckFileExtension(var, ext):
	""" Check the extension of a given file. 
		---
		var : path to the file (string or path)
		ext : must have the dot(.) .txt (list from config.extShort)
	"""
 #--> Set variables
	mfile = Path(var)
	myext = str(mfile.suffix)
 #---
 #--> Check & Return
	for e in ext:
		if myext == e:
			return True
		else:
			pass
	return False
 #---
#---
#endregion ------------------------------------------------- Files and Folders

#region ---------------------------------------------------------- wx.ListCtrl
def CheckListCtrlEmpty(lb, msg=None, nEle=1, empty=False, dlgShow=True):
	""" Check that the wx.ListCtrl has some items 
		---
		lb     : (wx.ListCtrl)
		msg    : error message to show (None or string)
		nEle   : minimum number of elements in lb (int)
		empty  : lb can be empty or not (boolean)
		dlgShow: show or not the error message 
	"""
 #--> Get number of items in lb 
	items = lb.GetItemCount()
 #---
 #--> Compare against nEle and empty and return if True
	if items >= nEle and empty == False:
		return True
	elif items >= nEle and empty == True:
		pass
	elif items <= nEle and empty == False:
		pass
	elif items <= nEle and empty == True:
		return True
	else:
		gclasses.DlgUnexpectedErrorMsg(config.msg['UErrors']['Unknown'])
		return False
 #---
 #--> Show error message or not and return
	if dlgShow:
		gclasses.DlgFatalErrorMsg(msg)
		return False
	else:
		return False
 #---
#---
#endregion ------------------------------------------------------- wx.ListCtrl

#region -------------------------------------------------------------- Uniprot
def CheckUniprot(code, ext='.fasta'):
	""" Check if a given UNIPROT CODE exists.
		---
		code: temptative UNIPROT code (string)
		ext : extension to create the url. Must include the dot if needed. (string) 
	"""
 #--> form & request the url
	if code != '':
		url = config.url['Uniprot'] + code + ext
		uniprot = requests.get(url)
 #---
 #--> Check uniprot & Return
		if 	uniprot.ok:
			return [True, uniprot]
		else:
			return [False, None]
	else:
		return [False, None]
 #---
#---
#endregion ----------------------------------------------------------- Uniprot

#region ------------------------------------------------------------------ PDB
def CheckPDB(code, ext='.pdb'):
	""" Check if a given PDB CODE exists. 
		---
		code: tentative PDB code (string)
		ext : extension to create the url. Must include the dot if needed. (string) 
	"""
 #--> form & request the url
	if code != '':
		url = config.url['Pdb'] + code + ext
		pdb = requests.get(url)
 #---
 #--> Check PDB 
		if pdb.ok:
			return [True, pdb]
		else:
			return [False, None]
	else:
		return [False, None]	
 #---
#---
#endregion --------------------------------------------------------------- PDB






