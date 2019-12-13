# ------------------------------------------------------------------------------
# 	Copyright (C) 2017-2019 Kenny Bravo Rodriguez <www.umsap.nl>

# 	This program is distributed for free in the hope that it will be useful,
# 	but WITHOUT ANY WARRANTY; without even the implied warranty of
# 	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

# 	See the accompaning licence for more details.
# ------------------------------------------------------------------------------


""" This module contains methods to check the user input data """


# ------------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Methods
# ------------------------------------------------------------------------------


#--- Imports
## Standard modules
from pathlib import Path
## My modules
import config.config as config
import gui.gui_classes as gclasses
import data.data_methods as dmethods
import checks.checks_single as check
#---


# ------------------------------------------------------ Files and Folders
def CheckMFileRead(var, ext):
	""" Check if a variable points to a file with extension ext that can be
		read.
		---
		var : variable holding a path (path or string)
		ext : extension expected in the file (config.extShort[X])
	"""
  #--> Extension of the file
	if check.CheckFileExtension(var, ext):
		pass
	else:
		return False
  #--> File can be read
	if check.CheckFileRead(var):
		pass
	else:
		return False
  #--> Return
	return True
#---

def CheckMOutputFolder(tcout, tcin, defName, dateN=None):
	""" Check if a folder can be used as output folder. If no folder is given 
		set a default value. dateN is to avoid overwriting the content of a 
		folder.
		---
		tcout  : wx.TextCtrl with the path to the output folder 
		tcin   : wx.TextCtrl with the path to the data file used as input
		defName: Default name for the output folder (string)
		dateN  : Current datetime to the second to avoid overwritting files (string)
	"""
  #--> Set dateN
	if dateN == None:
		dateN = dmethods.DateTimeNow()
	else:
		pass
  #--> Set the path to the output folder
	folderStr = tcout.GetValue()
	if folderStr in config.naVals:
		folderDef = Path(tcin.GetValue()).parent
		folderO = folderDef / defName
	elif "/" not in folderStr:
		folderDef = Path(tcin.GetValue()).parent
		folderO = folderDef / folderStr / defName
	else:
		folderO = Path(folderStr) / defName
  #--> Avoid overwiriting folder 
	name = folderO.name
	if folderO.is_dir():
		name = str(name) + "-" + dateN
		folderO = folderO.with_name(name)
	else:
		pass
  #--> Check that the folder can be used to write into it
	try:
		folderO.mkdir(parents=True)
		file = folderO / "test.test"
		file.touch()
		file.unlink()
		folderO.rmdir()
	except Exception:
		return [False, None]
  #--> Return
	return [True, folderO]
#---

def CheckMOutputFile(tcout, tcin, defName, ext, overW=False, dateN=None):
	""" Check if the given output file can be used or create one based on 
		default parameters. ext in this case is a string with the dot.
		---
		tcout   : wx.TextCtrl with the path to the output file
		tcin    : wx.TextCtrl with the path to the data file used as input
		defName : default name for the output file (string)
		ext     : extension for the output file (string e.g. .txt) 
		overW   : overwrite eisting file or not (Boolean)
		dateN   : final part of the name to avoid overwrite (string)
	"""
  #--> Set dateN
	if dateN == None:
		dateN = dmethods.DateTimeNow()
	else:
		pass
  #--> Set the path to the output file
	fileI = tcout.GetValue()
	if fileI in config.naVals:
		fileI = "NA"
		fileDef = Path(tcin.GetValue()).parent
		fileO = fileDef / defName
	elif "/" not in fileI:
		fileDef = Path(tcin.GetValue()).parent
		fileO = fileDef / fileI
	else:
		fileO = Path(fileI)
  #--> Set the extension of the output file
	fileO = fileO.with_suffix(ext)
	name = fileO.stem
  #--> Avoid unintentional overwrite
	if fileO.is_file() and overW == False:
		name = str(name) + "-" + dateN + ext
		fileO = fileO.with_name(name)
	else:
		pass
  #--> Check that file can be written
	try:
		fileO.touch()
		fileO.unlink()
	except Exception:
		return [False, None]
  #--> Return
	return [True, fileO]
#---

def CheckMOutputFile2(tcout, ext, overW=False, dateN=None):
	""" Check if the given output file can be used. 
		---
		tcout   : wx.TextCtrl with the path to the output file
		ext     : extension for the output file (string e.g. .txt) 
		overW   : overwrite eisting file or not (Boolean)
		dateN   : final part of the name to avoid overwrite (string)
	"""
  #--> Set dateN
	if dateN == None:
		dateN = dmethods.DateTimeNow()
	else:
		pass
  #--> Set the path to the output file
	try:
		fileI = Path(tcout.GetValue())
	except Exception:
		return [False, None]
  #--> Set the extension of the output file
	try:
		fileO = fileI.with_suffix(ext)
		name = fileO.stem
	except Exception:
		return [False, None]
  #--> Avoid unintentional overwrite
	if fileO.is_file() and overW == False:
		name = str(name) + "-" + dateN + ext
		fileO = fileO.with_name(name)
	else:
		pass
  #--> Check that indeed can be used
	try:
		fileO.touch()
		fileO.unlink()
	except Exception:
		return [False, None]
  #--> Return
	return [True, fileO]
#---
# ------------------------------------------------------ Files and Folders (END)


# ----------------------------------------------------------------- Values
def CheckMNumberComp(num, t="float", comp="egt", val=0, val2=None):
	""" Check if a number is of type t and compare the number to val
		---
		num : variable holding the number (float or string)
		t   : possible values; float, int, etc (string)
		comp: possible values; egt, e, gt, elt, lt (string) 
		val : value to compare against (float)
		val2: value to define a range in wich num must be (float)
	"""
  #--> Check var empty
	if check.CheckVarEmpty(num):
		pass
	else:
		return [False, None]
  #--> Check num type
	out, numT = check.CheckNumType(num, t)
	if out:
		pass
	else:
		return [False, None]
  #--> Compare & Return
	if val2 == None:
		if check.CheckNumComp(numT, comp, val):
			return [True, numT]
		else:
			return [False, None]
	else:
		if check.CheckaWithincd(numT, val, val2):
			return [True, numT]
		else:
			return [False, None]
#---

def CheckMListNumber(listV, t="float", comp="egt", val=0, Range=False,
	Order=False, Unique=True, DelRepeat=False, NA=False):
	""" Check if a list contains only number of type t and compare to val.
		Check also for range of numbers, unique elements and order. 
		Return list has proper type and expanded ranges. 
		---
		listV : list with the values (string)
		t     : possible values; float, int, etc (string)
		comp  : possible values; egt, e, gt, elt, lt (string)
		val   : value to compare against (float)
		Range : range allows in values
		Order : number must be in ascending order or not
		Unique: numbers must be unique or not
		DelRepeat : delete repeated elements or not
		NA    : NA values could be present or not
	"""
	# This is meant for user-built lists so multiple iteration over the list
	# will not have a big impact over execution time. So split for easier
	# mantienance and expansion
 #--> Check if var is empty
	if check.CheckVarEmpty(listV):
		pass
	else:
		return [False, None]
 #--> Split string into a list
	lin  = listV.strip().split(" ")
	lout = []
 #--> NA values
	if 'NA' in lin:
		if NA:
			if len(lin) == 1:
				lout.append(None)
				return [True, lout]
			else:
				return [False, None]
		else:
			return [False, None]
	else:
		pass
 #--> Fix each element
	for i in lin:
		#--> Empty element comming from split &| user input
		if i == "" or i == " ":
			pass
		#--> Number
		elif "-" not in i:
			out, num = CheckMNumberComp(i, t, comp, val)
			if out:
				lout.append(num)
			else:
				return [False, None]
		#--> Range or negative number
		else:
			ii = i.split("-")
			lii = len(ii)
			#--> Extra - character in range/number
			if lii > 2:
				return [False, None]
			#--> Negative number
			elif lii == 2 and ii[0] == "":
				out, num = CheckMNumberComp(i, t, comp, val)
				if out:
					lout.append(num)
				else:
					return [False, None]
			#--> Actual range
			elif lii == 2 and ii[0] != "":
				if Range:
					iie = []
					#--> Check range limit values against t, comp & val input
					for x in ii:
						out, num = CheckMNumberComp(x, t, comp, val)
						if out:
							iie.append(num)
						else:
							return [False, None]
					#--> Check a < b in range a-b
					if iie[0] >= iie[1]:
						return [False, None]
					else:
						#--> Expand range
						lout += range(iie[0], iie[1] + 1)
				else:
					return [False, None]
			else:
				# DlgBugMsg
				pass
 #--> Unique elements. Must be here to catch repeated elements after range
 #	 expansion
	if Unique:
		if check.CheckListUniqueElements(lout):
			pass
		else:
			#--> Remove duplicates
			if DelRepeat:
				lout = list(dict.fromkeys(lout))
			else:
				return [False, None]
	else:
		pass		
 #--> Order the list
	if Order:
		lout.sort()
	else:
		pass
 #--> Return
	return [True, lout]
#---
# ----------------------------------------------------------------- Values (END)
