# ------------------------------------------------------------------------------
#	Copyright (C) 2017-2019 Kenny Bravo Rodriguez <www.umsap.nl>
	
#	This program is distributed for free in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
	
#	See the accompaning licence for more details.
# ------------------------------------------------------------------------------


""" This module contains methods to proccess data """


# ------------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Methods
# ------------------------------------------------------------------------------



#--- Imports
## Standard modules
import copy
import csv
import datetime
import itertools
import json
import numpy as np
import pandas as pd
from collections import Counter
from math import sqrt
from statistics import stdev
from numpy import inf
from scipy import stats
from statsmodels.stats.weightstats import ttost_ind
## My modules
import config.config as config
import gui.gui_classes as gclasses
import checks.checks_single as check
#--- 



# ------------------------------------------------------ Files and Folders
def FFsRead(fileP, char='\t'):
	""" Reads a file. Empty lines are discarded. 
		---
		fileP: path to the file (string or path)
		char: each line is splitted with cha 
	"""
  #--> Variables
	fileP = str(fileP)
	data = []
  #--> Read and split lines
	with open(fileP, 'r') as file:
		for line in file:
			#--> To considerer mac \n or windows \r\n files
			l  = line.split('\n')[0]
			ll = l.split('\r')[0]
			if ll == '' or ll.strip() == '':
				pass
			else:
				if char == None:
					data.append([ll])
				else:
					lll = ll.split(char)
					data.append(lll)
  #--> Return
	return data
#---

def FFsReadCSV(fileP, char='\t'):
	""" Similar to FFsRead but using the CVS module 
		---
		fileP: path to the file (string or Path)
		char: character used to split each line
	"""
  #--> Variables
	data = []
  #--> Read and split the file
	with open(fileP, 'r') as tsv:
		for line in csv.reader(tsv, delimiter=char):
			if line == '':
				pass
			else:
				data.append(line)
  #--> Return
	return data
#---

def FFsReadJSON(fileP):
	""" Reads a file with a json format 
		---
		fileP: path to the file (string or Path)
	"""
	with open(fileP, 'r') as file:
		data = json.load(file)
	return data
#---

def FFsCVS2DF(fileP, sep='\t', index_col=None):
	""" Reads a cvs file and returns a dataframe 
		---
		fileP: path to the file (string or Path)
		sep: character used to split line records
		index_col: to specify the column containing the row indexes
	"""
	return pd.read_csv(str(fileP), sep=sep, index_col=index_col)
#---

def FFsWriteJSON(fileP, data):
	""" Writes a json file 
		---
		fileP: path to the file (string or Path)
		data: data to be written (dict)
	"""
	with open(fileP, 'w') as filew:
		json.dump(data, filew, indent=4)
	return True
#---

def FFsWriteCSV(fileP, df, index=False):
	""" Writes a dataframe to csv formatted file 
		---
		fileP: path to the file (string or Path)
		df: data frame to be written (DF)
		index: write index columns (Boolean)
	"""
	df.to_csv(str(fileP), sep='\t', na_rep='NA', index=index)
	return True
#---

def FFsWriteDict2Uscr(fileP, iDict, hDict=None):
	""" Takes a dict and write a file for the input file. hDict is to quickly
		fix the keys in iDict 
		---
		fileP: path to the output uscr (string or Path)
		iDict: dict with the data to save (dict)
		hDict: dict to translate keywords from d or &do dict to output (dict)
	"""
 #--> Open file for output
	file = open(str(fileP), 'w')
 #--> Write key : values
	for k, v in iDict.items():
		if hDict == None:
			# Writting something wrong here will not be passed to the module
			# because dclasses.DataObjScriptFile.__init__ remove these 
			file.write(str(k) + ': ' + str(v) + '\n')
		else:
			# Here the error must be handled
			try:
				file.write(str(hDict[k]) + ': ' + str(v) + '\n')
			except KeyError:
				pass
 #--> Close file & Return
	file.close()
	return True
#---
# ------------------------------------------------------ Files and Folders (END)



# ------------------------------------------------------------------ Lists
def ListResult(line, mod, CType):
	""" Takes a line like the input in Results and returns a list of list with
		three levels. The return list has the structure:
			[[[C0], [E01],    [] .... [E0m]],
			 [[C1],    [], [E12] ....    []],
			 [[Cn],    [],    [] .... [Enm]],
			]
		---
		line: line with the list (string)
		mod: name of the module (string)
		CType: control type (string)
	"""
 #--> Check CType
	if CType == None:
		msg = config.msg['Errors']['CType']
		gclasses.DlgFatalErrorMsg(msg)
		return [False, False]
	else:
		pass
 #--> Variables
	temp = line.split(';')
 #--> Check Module and do custom proccesing	
  #--> TarProt
	if mod == config.name['TarProt']:
		temp = [[x.strip()] for x in temp]
		resS = [temp]
  #--> LimProt
	elif mod == config.name['LimProt']:
		resS = ListResultHelper(temp)
  #--> ProtProf
	elif mod == config.name['ProtProf']:
		if CType == config.combobox['ControlType'][0]:
			resS = ListResultHelper(temp)
		elif CType == config.combobox['ControlType'][1]:
			out, resS = ListResultHelper2(temp)
			if out:
				pass
			else:
				return [False, False]
		elif CType == config.combobox['ControlType'][2]:
			resS = ListResultHelper3(temp)
		
		else:
			pass
	else:
		return [False, False]
 #--> Return
	return [True, resS]
#---

def ListResultHelper(temp):
	""" Helper to ListResult. It processes the case of one control
		---
		temp: list from ListResult
	"""
 #--> Variables
	resS = []
 #--> Get control
	c = temp[0].strip()
 #--> 
	temp = temp[1:]	
	temp = [x.strip().split(',') for x in temp]
	for x in temp:
		l = []
		l.append([c])
		for y in x:
			l.append([y.strip()])
		resS.append(l)
 #--> Return
	return resS
#---

def ListResultHelper2(temp):
	""" Helper to ListResult. It processes the case of one control per column
		---
		temp: list from ListResult
	"""
 #--> Variables
	resS = []
 #--> Get control
	c = [x.strip() for x in temp[0].strip().split(',')]
 #--> 
	temp = temp[1:]	
	temp = [x.strip().split(',') for x in temp]
	try:
		for i in range(0, len(c), 1):
			l = []
			l.append([c[i]])
			for j in range(0, len(temp), 1):
				l.append([temp[j][i].strip()])
			resS.append(l)
	except Exception:
		msg = config.msg['Errors']['ResMatrixShape']
		gclasses.DlgFatalErrorMsg(msg)
		return [False, False]
 #--> Return
	return [True, resS]
#---

def ListResultHelper3(temp):
	""" Helper to ListResult. It processes the case of one control per row
		---
		temp: list from ListResult
	"""
 #--> Variables
	resS = []
 #--> 
	temp = [x.strip().split(',') for x in temp]
	for x in temp:
		l = []
		for y in x:
			l.append([y.strip()])
		resS.append(l)	
 #--> Return
	return resS
#---

def ListResultNoNa(l):
	""" Remove a level in l that is None. Mainly to remove empty experiments in
		the Results list 
		---
		l: full Result list (list of list with three level)
	"""
  #--> Variables
	lo = []
  #--> Scan the list and remove None elements
	for a in l: # For each cond/band
		la = []
		for e in a: # For each tp/lane
			if e[0] != None:
				la.append(e)
			else:
				pass
		lo.append(la)
  #--> Return
	return [True, lo]
#---
		
def ListFlatNLevels(l, N=1):
	""" Take a list and flatten the first N levels. It flattens from the outside
		to the inside 
		---
		l: multi level list
		N: number of levels to flat
	"""
  #--> Variables
	lo = l[:]
  #--> Flat the outer N levels & Return
	try:
		for _ in range(0, N, 1):
			lo = list(itertools.chain(*lo))
		return [True, lo]
	except Exception:
		return [False, None]
#---
	
def ListExpand(l):
	""" Takes a list of positive integers and expand all ranges. 
		In a range a-b a < b 
		l: one level list of positive integer (string)
	"""
  #--> Variables
	lo = []
  #--> Set types and expand ranges
	for e in l:
		if '-' not in e:
			lo.append(int(e))
		else:
			a, b = map(int, e.split('-'))
			lo += range(a, b + 1)
  #--> Return
	return lo
#---

def ListColHeaderTarProtFile(nExp):
	""" Creates the list with the header for the data frame in the tarprot file. 
		---
		nExp: number of experiment (int)
	"""
  #--> Variables
	colOut = config.tarprot['ColNames'][:] # Name of the columns
	ind    = [] # List with the index of the columns
	iPoint = config.tarprot['InsertPoint']
  #--> 
	for i in range(0, nExp, 1):
		exp = nExp - i
		label = 'Exp' + str(exp)
		colOut.insert(iPoint, label)
		ind.append(iPoint + i)
  #--> Return
	return [colOut, ind]
#---

def ListColHeaderLimProtFile(nB, nL):
	""" Creates the list with the header for the limprot file.
		---
		nB: number of bands (int)
		nL: number of lanes (int)
	"""
  #--> Variables
	col = config.limprot['ColOut']
  #--> First col index level
	a = config.limprot['ColNames'][0:-2]
	for i in range(1, nB+1, 1):
		a = a + ['B'+str(i)] * nL * len(col)
	a = a + config.limprot['ColNames'][-2:]	 
  #--> Second col index level
	b = config.limprot['ColNames'][0:-2]
	for i in range (1, nB+1, 1):
		for e in range(1, nL+1, 1):
			b = b + ['L'+str(e)] * len(col)
	b = b + config.limprot['ColNames'][-2:]	 
  #--> Third col index level
	c = config.limprot['ColNames'][0:-2]
	for i in range(1, nB+1, 1):
		for e in range(1, nL+1, 1):
			c = c + config.limprot['ColOut']
	c = c + config.limprot['ColNames'][-2:]	 
  #--> Create the multi index
	col = pd.MultiIndex.from_arrays([a[:],
									 b[:],
									 c[:]])
  #--> Return
	return [True, col]
#---

def ListColHeaderCutPropFile(nExp):
	""" Creates the header column for the cutprop dataframe 
		---
		nExp: number of experiments (int)
	"""
  #--> Varaibles
	colOut = config.cutprop['ColNames'][:]
  #--> Add columns
	for i in range(0, nExp, 1):
		exp = nExp - i
		label = 'Exp' + str(exp) + ' Nat Norm'
		colOut.insert(2, label)
		label = 'Exp' + str(exp) + ' Nat'
		colOut.insert(2, label)		
		label = 'Exp' + str(exp) + ' Rec Norm'
		colOut.insert(2, label)
		label = 'Exp' + str(exp) + ' Rec'
		colOut.insert(2, label)
	ind = list(range(2, len(colOut)-config.cutprop['NumColsHeader']+2,
		1))
  #--> Return	
	return [colOut, ind]
#---

def ListColHeaderProtProfFile(Xv, Yv, Xtp, Ytp):
	""" Generates the multiindex columns for the output in ProtProf.
		This is meant to hold the analysis done over a matrix like:
		
			Control Y1 ... Ym
		X1
		X2
		Xn

		Depending on the control type X(Y) are conditions or relevant point
		---
		Xv : number of X in the matrix (int)
		Yv : number of Y in the matrix (int) 
		Xtp: number of relevant points per condition (int)
		Ytp: number of conditions (int)

	"""
  #--> Variables
	col    = config.protprof['ColOut']
	colL   = len(col)
	colTP  = config.protprof['ColTPp']
	colTPL = len(colTP)
	colDS  = config.protprof['ColDS']
	colDSL  = len(colDS)
  #--> First columns index level --> ColNames, c for conditions & tp for relevant points
	a = config.protprof['ColNames']
	a = (a 
		+ ['v'] * Xv * (colDSL + Yv * (colDSL+colL)) 
		+ ['tp'] * Xtp * (colTPL + Ytp * colDSL)
	)
  #--> Second columns index level --> ColNames, N for c & TP for tp
	b = config.protprof['ColNames']
	for i in range(1, Xv+1, 1):
		b = b + ['X' + str(i)] * (2 + Yv * (colL + colDSL))
	for i in range(1, Xtp+1, 1):
		b = b + ['T'+str(i)] * (colTPL + Ytp * (colDSL))	
  #--> Third columns index level --> ColNames, TP for c & N for tp
	c = config.protprof['ColNames']
	for _ in range(0, Xv, 1):
		c = c + ['Y0'] * colDSL
		for i in range(1, Yv+1, 1):
			c = c + ['Y' + str(i)] * (colL + colDSL) 
	for _ in range(1, Xtp+1, 1):
		c = c + ['C0'] * colTPL
		for i in range(1, Ytp+1, 1):
			c = c + ['C' + str(i)] * colDSL 	
  #--> Fourth columns index level ---> ColNames, name of the columns
	d = config.protprof['ColNames']
	d = d + Xv * (colDS + Yv * (col + colDS)) + Xtp * (colTP + Ytp * (colDS))
  #--> Set the multi index
	col = pd.MultiIndex.from_arrays([a[:],
									 b[:],
									 c[:],
									 d[:]])
  #--> Return
	return [True, col]
#---

def ListAddExtraAA(seq):
	""" Updates the list of AA in config. Non-natural aminoacids found in the 
		sequence are added to the temporal list. Lower case character are 
		discarded. Thus, pY is treated as T. 
		---
		seq: sequence of the protein (string)
	"""
  #--> Variables
	aaL = config.aaList1
	l = list(set(list(seq)))
  #--> Update aaL
	for i in l:
		if i.islower():
			pass
		else:
			if any(i in s for s in aaL):
				pass
			else:
				aaL.append(i)
  #--> Return
	return aaL
#---

def ListHistWin(width, seqLength, start=0):
	""" Creates equally spaced windows from start to seqLength or the closest
		larger number 
		---
		width: width of the windows (int)
		seqLength: length of the sequence (int)
		start: start the windows in this number (int)
	"""
  #--> Create windows
	lo = list(range(start, seqLength, width))
  #--> Fix first element because protein residue numbers start in 1 not 0
	if start == 0:
		lo[0] = 1
	else:
		pass
  #--> Add last residue number & Return
	lo.append(seqLength - 1)
	return lo
#---

def ListStepSum(l, rangeR, start=0):
	""" Return a list with the step sum of l.
		---
		l: list of values (list of numbers)
		rangeR: modify the output (string)
		start: number for starting the sum
	"""
  #--> Variables
	lo = [start]
  #--> Step sum
	for k, i in enumerate(l):
		lo.append(lo[k] + i)
  #--> Return
	if rangeR == config.name['AAdistR']:
		return lo[0:-1]
	else:
		return lo
#---

def ListCharCount(seq):
	""" Takes a string and return a dict with charInSeq : Number 
		---
		seq: sequence of a protein (string)
		"""
	return Counter(seq)
#---

def ListUnique(l, NA=False):
	""" Find repeating elements in l 
		---
		l: flat list to scan (flat list)
		NA: NA values are allowed or not (boolean)
	"""
  #--> Remove NA values if NA == True
	if NA == True:
		l = [x for x in l if x != None]
	else:
		pass
  #--> Find repeated elements
	re = [i for i, count in Counter(l).items() if count > 1]
  #--> Return
	if len(re) > 0:
		return [False, re]
	else:
		return [True, None]
#---
# ------------------------------------------------------------------ Lists (END)



# ------------------------------------------------------------------ Dicts
def DictVal2String(iDict, keys2string=None):
	""" Takes a dict and returns the same dict but all values are converted to 
		str 
		---
		iDict: initial values (dict)
		keys2strig: keys whose values will be converted to string. If None convert everything. (list of strings)
	"""
  #--> Convert
	#--> Everything
	if keys2string is None:
		oDict = {}
		for k, i in iDict.items():
			oDict[k] = str(i)
	#--> Selected few
	else:
		oDict = copy.deepcopy(iDict)
		for i in keys2string:
			oDict[i] = str(oDict[i])
  #--> Return
	return oDict
#---

def DictStartAAdist(pos, aaL, v=0):
	""" Creates a dict with one-letter code for AA as keys and the elements are
		list with length pos and initial val for each element in the list 
		---
		pos: number of positions (int)
		aaL: list with one letter codes (list of string)
		v: initial value for each position 
	"""
  #--> Variables
	d = {}
	l = [0] * 2 * pos
  #--> Fill dict
	for i in aaL:
		d[i] = list(l)
  #--> Return
	return d
#---

def DictUpdateAAdist(iDict, seq):
	""" Update the temporal dict in AAdist with a new seq 
		---
		iDict: aa and values (dict)
		seq: peptide sequence (string)
	"""
  #--> Variables
	seql = list(seq)
  #--> Update dict
	for k, s in enumerate(seql):
		if s != config.aadist['FillChar']:
			iDict[s][k] = iDict[s][k] + 1
		else:
			pass
  #--> Return
	return iDict
#---

def DictAAdist2DF(iDict, pos):
	""" Takes the aadist dict and converts it into a multiindex df 
		---
		iDict: aa and values (dict)
		pos: number of positions (int)

		The output data frame has the following format
		         AA   0 ... n
		Exp1 0   AAx
		     n   AAy
			 n+1 Pos
		Expn 0   AAx
		     n+1 Pos
		FP   0   AAx
		     n+1 Pos
		RD   0   AAx
		     n+1 Pos 0 0 0 0 0 0 0 0
	"""
  #--> Variables
	ln = ['AA'] + list(range(0, 2*pos)) 
	dfL  = []
	indL = []
  #--> Creates the data frame
	for k in iDict: # Loop the keys Exp#, FP & RD
		ll = []
		indL.append(k)
		for kk in iDict[k]: # Loop the AA
			l = [kk] + iDict[k][kk]
			ll.append(l)
		#--> Create data frame for each experiment
		dfL.append(pd.DataFrame(ll, columns=ln)) 
	#--> Create multi level data frame
	dfo = pd.concat(dfL, keys=indL)
  #--> Return
	return dfo
#---

def DictTuplesKey2StringKey(iDict):
	""" Convert all tuple keys to string keys. The rest are unchanged  
		---
		iDict: initial dictionary (dict)
	"""
  #--> Variables
	oDict = {}
  #--> Change keys
	for k in iDict:
		if isinstance(k, tuple):
			nk = config.protprof['Join'].join(k) # You might need to change the join char 
			oDict[nk] = iDict[k]
		else:
			oDict[k] = iDict[k]
  #--> Return
	return oDict
#---

def DictStringKey2TuplesKey(iDict, char=','):
	""" Split all keys by char and convert the result to a tuple.
		---
		iDict: initial values (dict)
		char: character to use for spliting (string)
	"""
  #--> Variables
	oDict = {}
  #--> Split keys
	for k in iDict:
		nk = tuple(k.split(char))
		oDict[nk] = iDict[k]
  #--> Return
	return oDict
#---
# ------------------------------------------------------------------ Dicts (END)


# ---------------------------------------------------------------- Strings
def StringCharForAAdist(string, ind, N, fill=None):
	""" Returns the characters in string around ind up to N as a str. 
		For example: (ABCDEFGH, 3, 2) centers the function in D and returns CDEF
		---
		string: string to search in (string)
		ind : index in the string (int)
		N: number of character around ind to return (int)
		fill: Optionally fill missing characters with this value (string or None) 
	"""
  #--> Variables
	s = ind - N + 1
	e = ind + N
  #--> Search string
	try:
		seq = string[s:e+1]
	except Exception:
		seq = []
		for i in range(s, e+1, 1):
			try:
				seq.append(string[i])
			except Exception:
				if fill is None:
					pass
				else:
					seq.append(fill)
		seq = str(''.join(seq))
  #--> Return
	return seq
#---
# ---------------------------------------------------------------- Strings (END)


# --------------------------------------------------------- UMSAP versions
def VersionCompare(la=None, lb=None):
	""" Compare config.versionUpdate and config.versionInternet. 
		In general compares two lists with three values each and elements are 
		ordered from the highest to the lowest hierarchy. 
		Returns:
		0  list la = lb
		1  list la > lb Update available
		-1 list la < lb Using a beta version? 
		---
		la : first list (list 3 elements)
		lb : second list (list 3 elements)
	"""
  #--> Variables
	if la == None:
		la = config.versionInternet
	else:
		pass
	if lb == None:
		lb = config.versionUpdate
	else:
		pass
  #--> Compare & Return
	if la != None:
		xI, yI, zI = la
		xU, yU, zU = lb
		if xI > xU:
			return 1
		elif xI == xU:
			if yI > yU:
				return 1
			elif yI == yU:
				if zI > zU:
					return 1
				elif zI == zU:
					return 0
				else:
					return -1
			else:
				return -1
		else:
			return -1
	else:
		return 0
#---

def VersionJoin(l):
	""" Takes a version list [2, 0, 1] and returns a string 2.0.1 
		---
		l: list 
	"""
	li = list(map(str, l))
	return ".".join(li) 
#---
# --------------------------------------------------------- UMSAP versions (END)



# --------------------------------------------- Date and time manipulation
def DateTimeNow():
	""" Return the current date and time with the format 
		YMDHMS: 20190204050204 """
	now = datetime.datetime.now()
	return now.strftime("%Y%m%d%H%M%S")
#---
# --------------------------------------------- Date and time manipulation (END)



# ------------------------------------------------------------- Statistics
def StatAncova(c, e, a, mod):
	""" Run Ancova for c and e. Depending on mod c and e may be altered. 
		c: control (list of numbers)
		e: experiments (list of numbers)
		a: alpha level (float)
		mod: module (string)
	"""
  #--> Update c and e depending on mod
	if mod is None:
		cok = c
		eok = e
	elif mod == config.name['TarProt']:
		cok, eok = StatPrepAncova(c, e, mod)
	else:
		pass
  #--> Run & Return
	ancovaRes = StatRunAncova(cok, eok, a)
	return ancovaRes
#---

def StatPrepAncova(c, e, mod='TarProt'):
	""" Finish preparing the data for the Ancova test 
		c: control (list of numbers)
		e: experiments (list of numbers)
		mod: module (string)		
	"""
  #--> TarProt preps
	if mod == 'TarProt':
   #--> Variables		
		xC  = []
		xCt = []
		yC  = []
		xE  = []
		yE  = []
   #--> Fill the control and first point for experiment
	#--> First point for control and experiment 
		for y in c:
			xC.append(1)
			xCt.append(5)
			xE.append(1)
			yC.append(y)
			yE.append(y)
	#--> Duplicate point
		xC  = xC + xCt
		yC  = yC + yC
	#--> Make array
		cA = np.array([xC, yC], dtype='float')
   #--> Experiment, second point	
	#--> Second point, first done with control 
		for y in e:
			xE.append(5)
			yE.append(y)	
	#--> MAke array
		eA = np.array([xE, yE], dtype='float')	
   #--> Return 
		return [cA, eA]	
	else:
		pass	
#---

def StatRunAncova(c, e, a, k=2):
	""" Run the ancova test. c and e are np arrays 
		NOTE: The implementation is restricted to k = 2

		stest: -3 No idea about why it crashed
		       -2 No Ft value was found
		       -1 Fslope > Fc and slope < 0
		        0 Fslope < Fc
		        1 Fslope > Fc and slope > 0
	
		ANCOVA CALCULATIONS FROM http://vassarstats.net/textbook/index.html 
		---
		c: control values (np.array)
		e: experiment values (np.array)
		a: alpha value

	"""
  #--> Total sum
	Sum_Yc = np.sum(c[1])
	Sum_Ye = np.sum(e[1])
	Sum_Yc_Ye = Sum_Yc + Sum_Ye
  #--> Quit if everythin is 0
	if Sum_Yc_Ye == 0:
		return [0, 'NAF']
	else:
		pass
  #--> Other sum
	Sum_Xc   = np.sum(c[0])
	Sum_Xe   = np.sum(e[0])
	Sum_XcYc = np.sum(np.prod(c, axis=0))
	Sum_XeYe = np.sum(np.prod(e, axis=0))
	Sum_Xc2  = np.sum(np.square(c[0]))
	Sum_Xe2  = np.sum(np.square(e[0]))
	Sum_Yc2  = np.sum(np.square(c[1]))
	Sum_Ye2  = np.sum(np.square(e[1]))
  #--> Number of points
	Nc = c.shape[1]
	Ne = e.shape[1]
	Nt = Ne + Nc 
  #--> Other values
	SCc        = Sum_XcYc - ((Sum_Xc * Sum_Yc) / (1.0 * Nc))
	SCe        = Sum_XeYe - ((Sum_Xe * Sum_Ye) / (1.0 * Ne))
	SCwg       = SCc + SCe
	SS_Xc      = Sum_Xc2 - ((Sum_Xc * Sum_Xc) / (1.0 * Nc))
	SS_Xe      = Sum_Xe2 - ((Sum_Xe * Sum_Xe) / (1.0 * Ne))
	SSwg_X     = SS_Xc + SS_Xe
	SS_Yc      = Sum_Yc2 - ((Sum_Yc * Sum_Yc) / (1.0 * Nc))
	SS_Ye      = Sum_Ye2 - ((Sum_Ye * Sum_Ye) / (1.0 * Ne))
	SSwg_Y     = SS_Yc + SS_Ye
	adj_SSwg_Y = SSwg_Y - ((SCwg * SCwg)/(1.0 * SSwg_X))	
  #--> Slope
	SSnum_Slope =  (((SCc * SCc)/(SS_Xc)) + ((SCe * SCe)/(SS_Xe)) 
				   - ((SCwg * SCwg)/(SSwg_X)))
	SSden_Slope =  adj_SSwg_Y - SSnum_Slope
	dfnum_Slope = k - 1 
	dfden_Slope = Nt - (2 * k)
	F_Slope     = float(((SSnum_Slope)/(dfnum_Slope)) 
					   / ((SSden_Slope)/(dfden_Slope)))
	slope       = SCe / (1.0 * SS_Xe)
  #--> F value
	Ft = stats.f.ppf(1-a, dfnum_Slope, dfden_Slope)
  #--> Results & Return	
	if Ft == 'NA':
		stest = -2
	elif F_Slope > Ft and slope > 0:
		stest = 1
	elif F_Slope > Ft and slope < 0:
		stest = -1
	elif F_Slope <= Ft:
		stest = 0
	else:
		stest = -3
	return [stest, F_Slope, Ft, slope]
#---

def StatChiSquare(lo, le, aVal):
	""" Performs a chi squared test for a contingency table with two columns
		and multiple rows. 
		Returns:
	 	1 p < aVal and number of cells < 5 > 20%
	 	0 p > aVal and number of cells < 5 > 20%
	   -1 if the test cannot be performed for any reason 
		---
		lo: list with observed values
		le: list with expected values
		aVal: alpha level (float)
	"""
 #--> Remove sum that are 0 in both
	for i in range(0, len(lo)):
		if lo[i] + le[i] == 0:
			del lo[i]
			del le[i]
		else:
			pass
 #--> Calculate & Return
	lenlo = len(lo)
	if lenlo > 1:
		data = np.array([lo, le])
		#--> Catch error in scipy calculation
		try:
			chi = stats.chi2_contingency(data)
		except Exception:
			return -1
		#--- Check contingency table for values below 5
		val5 = np.count_nonzero(chi[3] < 5.0)
		elt5 = val5 / (2 * lenlo)
		if elt5 < 0.2:
			if chi[1] < aVal:
				return 1
			else:
				return 0
		else:
			return -1	
	else:
		return -1
#---

def StatTost(c, e, a, b, y, d, dm):
	""" Runs a t-test and a TOST with delta value. Same a value for both
		---
		c: control (list or np.array)
		e: experiment (list or np.array)
		a: alpha value (float)
		b: beta value (float)
		y: chi squared estimation level (float)
		d: delta value manual (float)
		dm: maximum delta value (float)
	"""
  #--> Calculate t
	t_R = stats.ttest_ind(c, e, equal_var=False)
  #--> Estimate delta
	if d != None:
		tdelta = d
	else:
		Edelta = StatEstimateDeltaTost(c, a, b, y)
		if Edelta > dm:
			tdelta = dm
		else:
			tdelta = Edelta
  #--> Calculate tost
	tost_R = ttost_ind(c, e, -tdelta, tdelta, usevar='unequal')
  #--> Return
	return [t_R.pvalue, tdelta, tost_R[0]]
#---
	
def StatEstimateDeltaTost(c, a, b, y):
	""" Estimate delta for the equivalence test doi:10.1021/ac053390m
		---
		c: control (list or np.array)
		a: alpha value (float)
		b: beta value (float)
		y: chi level value (float)
	"""
  #--> Variables
	n      = len(c)  
	s      = stdev(c) 
	chi    = stats.chi2.ppf(1 - y, n - 1)
	ta1    = stats.t.ppf(1 - a, 2*n - 2)
	tb1    = stats.t.ppf(1 - b/2, 2*n -2)
	s_corr = s * sqrt((n - 1)/(chi))
  #--> delta
	delta = s_corr * (ta1 + tb1) * sqrt(2/n)
  #--> Return
	return delta
#---
# ------------------------------------------------------------- Statistics (END)



# ----------------------------------------------------- Data Normalization
def DataNorm(pdFi, sel=None, method=None):
	""" Normalize a pandas data frame (pdF) or selected columns using the 
		specified method. -inf are replaced with 0 
		---
		pdFi: data frame (DF)
		sel: list of columns (list)
		method: (string)
	"""
  #--> Copy to avoid changing the original
	pdF = pdFi.copy()
  #--> Normalize & Return
   #--> None
	if method is None:
		return [True, pdF]
   #--> Log2
	elif method == 'Log2':
		if sel is None:
			pdFN = np.log2(pdF)
			pdFN = pdFN.replace(-inf, 0)
		else:
			pdFN = pdF
			pdFN.iloc[:,sel] = np.log2(pdFN.iloc[:,sel])
			pdFN = pdFN.replace(-inf, 0)
		return [True, pdFN]			
   #--> Unknown method
	else:
		gclasses.DlgFatalErrorMsg(config.msg['Errors']['NormMethod'])
		return [False, False]
#---

def DataNormDFCol(pdFCol):
	""" Put a column in the 0 to 1 range.
		---
		pdfCol: column in a data frame
	"""
	colO = (pdFCol - pdFCol.min()) / (pdFCol.max() - pdFCol.min())
	return colO
#---

def DataCalcRatios(dfi, col, header):
	""" Calculates the ratio for the ProtProf module. 
		---
		dfi: data frame with the information
		col: list of list (3 level) in which the first element (2 level) is the 
		list of reference columns for condition n (level 2). Replicates in level
		3 must be organized in the same order (list of list 3 levels)
		header: name of the columns in the data frame (list)
	"""
  #--> Copy df to avoid changing the original data	
	df = dfi.copy()
  #--> Calculate ratios
	for k, a in enumerate(col): # Loop cond/bands
		tp = len(a)
		for l, b in enumerate(a[0]): # Loop reference in given cond/band
			ref = header[b]
			tc = []
			for c in range(0, tp, 1): # Loop tp/lanes
				if col[k][c][0] == None:
					pass
				else:
					tc.append(header[col[k][c][l]])
			df[tc] = df[tc].div(df[ref], axis=0)
  #--> Return
	return [True, df]
#---
# ----------------------------------------------------- Data Normalization (END)



# ------------------------------------------ pandas.DataFrame manipulation
def DFSelCol(df, sel, loc=False):
	""" Select all rows from columns in sel by loc method
		---
		df: data frame
		sel: list with column names or column indexes (list)
		loc: True .loc method False .iloc method	
	"""
  #--> Variables
	k = True
  #--> Select
	if loc:
		try:
			dfo = df.loc[:,sel]
		except Exception:
			k = False
	else:
		try:
			dfo = df.iloc[:,sel]
		except Exception:
			k = False
  #--> Return
	if k:
		return [True, dfo]
	else:
		return [False, None]
#---

def DFSetColType(df, typeV, name):
	""" Set the type of the data in the columns of the data frame 
		---
		df: data frame
		typeV: col name : type paired values (dict)
		name: for looking error msg (string)
	"""
  #--> Variables
	k = True
  #--> Assign types
	try:
		df = df.astype(typeV)
	except Exception as e:
		error = str(e).split(':')[1]
		k = False
  #--> Return
	if k:
		return [True, df]
	else:
		msg = config.dictCheckFatalErrorMsg[name]['NoFloatInColumns']
		msg += '\nNon-numeric value: ' + str(error)
		gclasses.DlgFatalErrorMsg(msg)
		return [False, None]			
#---

def DFColValFilter(df, val, col, comp='eq', reset=True, loc=False):
	""" Filter the dataFrame by a val in a col 
		---
		df: data frame
		val: value to look for in the column (int)
		col: col name or index (list of strings or integers)
		comp: comparison (string)
		reset: reset the df index after filtering or not
		loc: True .loc False .iloc
	"""
  #--> Filter
	try:
		if comp == 'eq':
			if loc:
				dfo = df.loc[df.loc[:,col] == val]			
			else:
				dfo = df.loc[df.iloc[:,col] == val]	
		elif comp == 'ge':
			if loc:
				dfo = df.loc[df.loc[:,col] >= val]			
			else:
				dfo = df.loc[df.iloc[:,col] >= val]
	except Exception:
		return [False, None]
  #--> Reset				
	if reset:
		dfo.reset_index(drop=True, inplace=True)
	else:
		pass
  #--> Return
	return [True, dfo]
#---

def DFCharFilter(df, char, col, pres=False, loc=False, reset=True):
	""" Filter the data frame by the presence or not of char in col index
		---
		df: data frame
		char: character to look for (str)
		col: column in which to look char (list of string or integers)
		pres: look for presence (True) or absence of char (False)
		loc: True .loc False .iloc
		reset: reset the df index after filtering or not
	"""
  #--> Look up char
	if pres:
		try:
			if loc:
				dfo = df[df.loc[:,col].str.contains(char)]
			else:
				dfo = df[df.iloc[:,col].str.contains(char)]
		except Exception:
			return [False, None]
	else:
		try:
			if loc:
				dfo = df[~df.loc[:,col].str.contains(char)]
			else:
				dfo = df[~df.iloc[:,col].str.contains(char)]
		except Exception:
			return [False, None]
  #--> Reset
	if reset:
		dfo.reset_index(drop=True, inplace=True)
	else:
		pass
  #--> Return			
	return [True, dfo]
#---

#--- Several steps
def DFSelSet(df, sel, typeV, name, locT=False):
	""" Run DFSelCol and DFSetColType 
		---
		df: data frame
		sel: list with column names or column indexes (list)
		typeV: col name : type paired values (dict)
		name: for looking error msg (string)
		locT: True .loc method False .iloc method 	
	"""
  #--> DFselCol
	out, df = DFSelCol(df, sel, locT)
  #--> DFSetColType
	if out:
		out, df = DFSetColType(df, typeV, name)
		if out:
			return [True, df]
		else:
			return [False, None]
	else:
		return [False, None]
#---

def DFSelFilterNSet(df, sel, val, col, comp, name, typeV, locT=False):
	""" Run DFSelCol, DFColValFilter and DFSetColType in this order
		val, col and comp are lists to allow N filters; locT is the value for 
		the first sel because the other must be loc=True  
		---
		df: data frame 
		sel: list with column names or column indexes (list)
		val: values to filter the df
		col: columns to look for val
		comp: comparison to llok val in col
		name: name for error message
		typeV: col name : type pairs (dict) 
		locT: True .loc methos False .iloc method
	"""
  #--> DFSelCol
	out, df = DFSelCol(df, sel, locT)
  #--> DFColValFilter len(val) times
	if out:
		for k in range(0, len(val)):
			out, df = DFColValFilter(df, val[k], col[k], comp[k], loc=True)
			if out:
				pass
			else:
				return [False, False]
  #--> Col types
		out, df = DFSetColType(df, typeV, name)
		if out:
			return [True, df]
		else:
			return [False, False]
	else:
		return [False, False]
#---

def DFSelCharFilterNSet(df, sel, char, colC, val, col, comp, name, typeV, 
	locT=False):
	""" Select column then filter by character then filter by col values N times
		and finally set types. val, col and comp are lists to allow N filters. 
		locT is the value for the first sel because the other must be loc=True   
		---
		df: data frame 
		sel: list with column names or column indexes (list)
		char: character to look for (str)
		colC: column in which to look char (list of string or integers)		
		val: values to filter the df
		col: columns to look for val
		comp: comparison to llok val in col
		name: name for error message
		typeV: col name : type pairs (dict) 
		locT: True .loc methos False .iloc method	
	"""
  #--> Sel col
	out, df = DFSelCol(df, sel, locT)
  #--> Fiter by char
	if out:	
		out, df = DFCharFilter(df, char, colC)
  #--> Filter by val len(val) times 
		if out:
			for k in range(0, len(val)):
				out, df = DFColValFilter(df, val[k], col[k], comp[k], loc=True)
				if out:
					pass
				else:
					return [False, False]
  #--> Set types
			out, df = DFSetColType(df, typeV, name)
			if out:
				return [True, df]
			else:
				return [False, False]
		else:
			return [False, False]
	else:
		return [False, False]	
#---

def DFGetFragments(df, name, strC=True):
	""" Receive a df containing at least two columns Nterm and Cterm and returns
		the fragments containing a list of (start, end) for each fragment
		---
		df: data frame
		name: name for error msg
		strC: return a string (True) or a list (False)  
	"""
  #--> Get N, C pairs from the df
	dvS = df.loc[:,['Nterm', 'Cterm']]
	dvS = dvS.drop_duplicates()
	dvS = dvS.sort_values(by=['Nterm', 'Cterm'], axis=0)
	dvSL = dvS.values.tolist()
	l = len(dvSL)
	lm = l - 1
	frags = []
  #--- Make the fragments
	for k, v in enumerate(dvSL):
		if k == 0:
			n, c = v
		elif k < l:
			tn ,tc = v
			if tn < n:
				msg = config.dictCheckFatalErrorMsg[name]['FileFormatSort']
				gclasses.DlgFatalErrorMsg(msg)
				return [False, None]
			elif n <= tn and tn <= c:
				if tc > c:
					c = tc
				else:
					pass
			else:
				frags.append((n, c))
				n, c = v
			if k == lm:
				frags.append((n, c))
			else:
				pass
		else:
			pass
  #--> Convert to string or not & Return
	if strC:
		return [True, '; '.join(list(map(str, frags)))]
	else:
		return [True, frags]
#---

def DFWrite2TextCtrl(df, tc, formatters=None):
    """ Write the content of df to tc 
        ---
        df: data frame to be written
        tc: text control to receive the text
    """
    lines = df.to_string(index=False, justify='left', formatters=formatters)
    for i in lines:
        tc.AppendText(i)
 #--> Return
    return True
#--- 		
# ------------------------------------------ pandas.DataFrame manipulation (END)			



# ------------------------------------------------------------------- Calc
def CalCutpropInd(i):
	""" Returns the starting index of an experiment in the cutpropObj.data
		dataframe 
		---
		i : experiment (int)
	"""
	ind = ((config.cutprop['DistBetExp'] * i) - config.cutprop['NColExpStart'])
	return ind
#---
# ------------------------------------------------------------------- Calc (END)



# ----------------------------------------------------------------- Colors
def GetColors(N, t='S'):
	""" Get N colors from config.colors['Fragments'] 
		---
		N: number of colors (int)
		t: (S)olid or (L)ight colors (string)
	"""
  #--> Variables
	if t == 'S':
		Ncolor = len(config.colors['Fragments'])
		colors = config.colors['Fragments']
	elif t == 'L':
		Ncolor = len(config.colors['FragmentsLight'])
		colors = config.colors['FragmentsLight']		
	Nlist = []
  #--> Get the colors
	for i in range(1, N+1, 1):
		ci = i % Ncolor
		Nlist.append(colors[ci])
  #--> Return
	return Nlist
#---

def GetZColors(y, colors, lim=2):
	""" Get color from a list based on a property value
		---
		y: property value (list of floats)
		colors: three elements list with the possible colors
		lim: boundary for selecting the color from colors 
		---
	"""
  #--> Variables
	colO = []
  #--> Select color
	for z in y:
		if z >= lim:
			colO.append(colors[0])
		elif z <= -lim:
			colO.append(colors[2])
		else:
			colO.append(colors[1])
  #--> Return
	return [True, colO]
#---
# ----------------------------------------------------------------- Colors (END)



# ------------------------------------------------------- gclasses Helpers
def GHelperLBSelUpdate(self):
	""" To update selections in ElementGelPanel and WinResUno """
  #-->
	self.seqG = self.fAll[self.fAll.loc[:,'Sequence'].str.contains(self.selSeq, regex=False)]
  #-->
	if self.seqG.empty == False:
		self.lbSelPlotG = True
		if self.selM == True and self.TLane != None:
			try:
				l = self.TLane + 1
				self.seq = self.seqG.loc['L'+str(l),:]
				if self.seq.empty == False:
					self.lbSelPlot = True
				else:
					self.lbSelPlot = False
			except Exception:
				self.lbSelPlot = False	
		elif self.selM != True and self.TBand != None:
			try:
				idx = pd.IndexSlice
				self.seq = self.seqG.loc[idx[:,'B'+str(self.TBand)],:]
				self.seq.index = self.seq.index.droplevel(1)
				if self.seq.empty == False:
					self.lbSelPlot = True
				else:
					self.lbSelPlot = False
			except Exception:
				self.lbSelPlot = False	
		else:
			self.lbSelPlot = False								
	else:
		self.lbSelPlotG = False
#---

def GHelperXYLocate(x, y, coordDict):
	""" To locate the fragment/gel in ElementFragPanel and ElementGelPanel 
		x, y mouse event coordinates
		coordDict is like:
		{'y': {1: [(yi, yf)], n: [(yi, yf)]}, 'x': {1: [(), ()], 2: [(),()]}}
		The keys in x match the ones in y. Basically you have the y values and
		for each y values you have the x in the y row.
	"""
  #--> Default values
	yo = None
	xo = None
  #--> Locate y
	for k in coordDict['y'].keys():
		yi, yf = coordDict['y'][k][0]
		if yi <= y and y <= yf:
			yo = k
			break
		else:
			pass
  #--> Locate x
	if yo == None:
		for k in coordDict['x'].keys():
			if xo == None:
				for j, e in enumerate(coordDict['x'][k]):
					xi, xf = e
					if xi <= x and x <= xf:
						xo = j
						break
					else:
						pass
			else:
				break
	else:
		for j, e in enumerate(coordDict['x'][k]):
			xi, xf = e
			if xi <= x and x <= xf:
				xo = j
				break
			else:
				pass
  #--> Return
	return [True, xo, yo]		
#---

def GHelperShowFragDet(self):
	""" Show fragments details depending of self. Used in TarProtRes and 
		LimProtRes 
	"""
  #--> Get fragment number info
	k  = self.kf[0]
	b  = self.kf[1]
	bp = b + 1
  #--> Locate the fragment in data frame
	if self.name == config.name['TarProtRes']:
		tf  = self.f.loc['E' + str(k),:]
	elif self.name == config.name['LimProtRes']:
		if self.selM:
			tf  = self.f.loc['B' + str(k),:]
		else:
			tf  = self.f.loc['L' + str(k),:] 
			tf = tf.droplevel(0, axis=0)
	else:
		pass
  #--> Get info for experiment
	eF  = tf.shape[0]
	eFN = tf['Bit'].sum()
	eC  = int(tf.at[0,'TCuts'])
	eCN = int(tf.at[0,'TCutsNat'])
	eS  = tf['SeqN'].sum(skipna=True)
	eSN = int(tf['SeqNNat'].sum(skipna=True))
  #--> Get info for fragment
	tff = tf.loc[b,:]
	n   = int(tff['Nterm'])
	try:
		nf = int(tff['Fixed Nterm'])
	except Exception:
		nf = 'NA'
	c   = int(tff['Cterm'])
	try:
		cf = int(tff['Fixed Cterm'])	
	except Exception:
		cf = 'NA' 
	sF  = int(tff['SeqN'])
	try:
		snF = int(tff['SeqNNat'])
	except Exception:
		snF = 'NA'
	cF  = int(tff['Cuts'])
	try:
		cnF = int(tff['CutsNat'])
	except Exception:
		cnF = 'NA'
  #--> Extra space for printing
	sku, sfu, sd = GHelperGetSpan(k, bp)
  #--> Write into text box
	self.text.Clear()
	#---
	if self.name == config.name['TarProtRes']:
		text = ("Details for Experiment " + str(k) + " and Fragment " 
			+ str(bp) + "\n\n")
		self.text.AppendText(text)
		text = ("Experiment" + sku * " " + str(k) + ":  Fragments " + str(eF) 
			+ "(" + str(eFN) + ")," + "  Cleavage sites " + str(eC) + "(" 
			+ str(eCN) + "),\n")
		self.text.AppendText(text)
	elif self.name == config.name['LimProtRes']:
		text = ("Details for Lane " + str(self.TextL) + ", Band " 
			+ str(self.TextB) + " and Fragment " + str(bp) + "\n\n")
		self.text.AppendText(text)
		if self.selM:
			text = ("Band" + (sku+6) * " " + str(k) + ":  Fragments " 
				+ str(eF) + "(" + str(eFN) + ")," + "  Cleavage sites " 
				+ str(eC) + "(" + str(eCN) + "),\n")
		else:
			text = ("Lane" + (sku+6) * " " + str(k) + ":  Fragments " 
				+ str(eF) + "(" + str(eFN) + ")," + "  Cleavage sites " 
				+ str(eC) + "(" + str(eCN) + "),\n")
		self.text.AppendText(text)		
	else:
		pass
	#---
	text = (sd * " " + "Sequences " + str(eS) + "(" + str(eSN) + ")\n\n")
	self.text.AppendText(text)
	text = ("Fragment" + sfu * " " + str(bp) + ":  Nterm " + str(n) 
		+ "(" + str(nf) + ")," + " Cterm " + str(c) + "(" 
		+ str(cf) + ")\n")
	self.text.AppendText(text)
	text = (sd * " " + "Sequences " + str(sF) + "(" + str(snF) + ")," 
		+ " Cleavage sites " + str(cF) + "(" + str(cnF) + ")\n\n")
	self.text.AppendText(text)		
	self.text.AppendText('Sequences in the fragment:\n\n')
	for i in tff['SeqSpace']:
		self.text.AppendText(str(i) + '\n')
	self.text.SetInsertionPoint(0)
  #--> Return
	return True
#---	

def GHelperGetSpan(k, F):
	""" Get the first span value for experiments and fragments. Mainly a 
		helper to GHelperShowFragDet 
		---
		k: experiment (int)
		F: fragment number (int)
	"""
  #--> Length of the numbers
	sk = len(str(k))
	sF = len(str(F))
  #--> Length needed to write the string
	lk = 11 + sk # These numbers are related to what you write in text box
	lf = 9 + sF
  #--> Extra space to make it even
	if lk > lf:
		sku = 1
		sfu = 1 + lk - lf
		sd = lk + 3
	else:
		sku = lf - lk - 1
		sfu = 1
		sd = lf + 3
  #--> Return
	return [sku, sfu, sd]
#---
# ------------------------------------------------------- gclasses Helpers (END)



# ------------------------------------------------------- dclasses Helpers
def DHelperFragTuple2NatSeq(self, tup, strC=True):
	""" Convert the fragment N, C tuple to the native sequence residue numbers
		---
		tup: tupple (N, C)
		strC: True covert to string False return list
	"""
  #--> Variables
	l = []
  #--> Native residue numbers
	if self.natProtPres:
		for t in tup:
			lt = []
			for _, e in enumerate(t):
				if check.CheckabWithincd(e, e, self.pRes[1], 
					self.pRes[2]):
					lt.append(e + self.mist)
				else:
					lt.append('NA')
			l.append(tuple(lt))
   #--> Convert to string or not 
		if strC:
			l = '; '.join(list(map(str, l)))
		else:
			pass
	else:
		l = 'NA'
  #--> Return
	return [True, l]
#---
# ------------------------------------------------------- dclasses Helpers (END)


# ------------------------------- Data to fill ListCtrl in a Result Window
# This methods get information from a dataframe and the information is used to
# fill a ListCtrl. They are intended to be called from within a class
def Get_Data4ListCtrl_TarProtRes(self, col=None, df=None):
	""" 	"""
 #--> Default values
	if col is None:
		col = [('Sequence')]
	else:
		pass
	if df is None:
		df = self.fileObj.filterPeptDF
	else:
		pass
 #--> Get info
	l = df.loc[:,col].values.tolist()
 #--> Return
	return l
#---

def Get_Data4ListCtrl_LimProtRes(self, col=None, df=None):
	""" 	"""
 #--> Default values
	if col is None:
		col = [('Sequence','Sequence','Sequence')]
	else:
		pass
	if df is None:
		df = self.fileObj.filterPeptDF
	else:
		pass
 #--> Get info
	l = df.loc[:,col].values.tolist()
 #--> Return
	return l
#---

def Get_Data4ListCtrl_ProtProfRes(self, col=None, df=None):
	""" 	"""
 #--> Default values
	if col is None:
		col = [('Gene','Gene','Gene','Gene'), ('Protein','Protein','Protein','Protein')]
	else:
		pass
	if df is None:
		df = self.fileObj.dataFrame
	else:
		pass
 #--> Get info
	l = df.loc[:,col].values.tolist()
 #--> Return
	return l
#---
# ------------------------------- Data to fill ListCtrl in a Result Window (END)
