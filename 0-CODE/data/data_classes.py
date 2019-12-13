# ------------------------------------------------------------------------------
#	Copyright (C) 2017-2019 Kenny Bravo Rodriguez <www.umsap.nl>
	
#	This program is distributed for free in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
	
#	See the accompaning licence for more details.
# ------------------------------------------------------------------------------


""" This module provides the clasess to handle the data files """


# ------------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Methods
# ------------------------------------------------------------------------------



#--- Imports
## Standard modules
import copy
import itertools
import json
import math
import numpy  as np
import pandas as pd
import wx
from Bio import pairwise2
from Bio.SubsMat.MatrixInfo import blosum62
from fpdf    import FPDF
from pathlib import Path
## My modules 
import config.config        as config
import checks.checks_single as check
import gui.gui_classes      as gclasses
import gui.gui_methods      as gmethods
import data.data_methods    as dmethods
#---



# ------------------------------------------------------ Base Data Classes
class MyModules():
	""" Common methods for classes handling the output files from modules 
		----> Methods of the class
		- SetlocProtType
		- FixRes
		- SetFragments
	"""

	####---- Methods of the class
	#--> locProtType
	def SetlocProtType(self):
		""" Set how to represent the protein in the Fragment view """
		if self.pRes[1] == None and self.pRes[2] == None:
			self.locProtType = 5
		else:
			if self.pRes[1] == self.pRes[0] and self.pRes[2] == self.pRes[3]:
				self.locProtType = 1
			elif self.pRes[1] == self.pRes[0] and self.pRes[2] < self.pRes[3]:
				self.locProtType = 2
			elif self.pRes[1] > self.pRes[0] and self.pRes[2] < self.pRes[3]:
				self.locProtType = 3
			elif self.pRes[1] > self.pRes[0] and self.pRes[2] == self.pRes[3]:
				self.locProtType = 4
			else:
				pass
		return True
	#---

	#--> 
	def FixRes(self, r):
		""" Fix the residue number based on the mistmatch value 
			---
			r: residue number (int)
		"""
		if self.mist != None:
			if r >= self.pRes[1] and r <= self.pRes[2]:
				return r + self.mist
			else:
				return None
		else:
			return None
	#---

	###--- SetFragments Helpers
	#---
	def SetFragmentsHelper0(self, j, k, fpL, fra, L, name):
		""" Helper to SetFragments 
			---
			j: current index in the list of N, C values (int)
			k: current N, C values in a list (list or tuple)
			fpL: list of column names in the data frame with the results (list)
			fra: list for the detected fragments (list)
			L: total number of N, C values (int)
			name: self.name
		"""
	 #--> Start value
		if j == 0:
			#--> Variables
			self.n, self.c   = k
			self.no = self.n
			self.tcuts  = []
			self.tcutsN = []
			#--> Start new fragment
			self.SetFragmentsHelper1(j, self.n, self.no, self.c, fpL)
	 #--> Middle values
		elif j > 0:
			self.nt, self.ct = k
			#--> Current n < n. Fatal Error
			if self.nt < self.n:
				msg = config.dictCheckFatalErrorMsg[self.name]['FileFormatSort']
				gclasses.DlgFatalErrorMsg(msg)
				return False
			#--> Extend fragment
			elif self.nt >= self.n and self.nt <= self.c:
				#--> Update variables
				self.SetFragmentsHelper2(j, self.no, self.nt, self.ct, fpL)
				#--> Update n
				self.n = self.nt
				#--> Update c
				if self.ct > self.c:
					self.c = self.ct
				else:
					pass
			#--> End fragment and start new one
			elif self.nt > self.c:
				#--- End fragment
				self.SetFragmentsHelper3(self.c)
				fra.append(self.lo)
				#--- Start new one
				self.n, self.c   = k
				self.no = self.n
				self.SetFragmentsHelper1(j, self.n, self.no, self.c, fpL)
	 #--> Final value
		if j == L - 1:
			#--- End fragment
			self.SetFragmentsHelper3(self.c)
			fra.append(self.lo)
		else:
			pass
	  #--> Return
		return True
	#---

	def SetFragmentsHelper1(self, j, n, no, c, fpL):
		""" Creates a new fragment. Helper to SetFragments.
			---
			j: current index in the list of N, C values (int)
			n: reference n-term residue number (int)
			no: reference initial n-term residue number (int)
			c: reference c-term residue number (int)
			fpL: list of column names in the data frame with the results (list)
		"""
	  #--> Variables
		self.lo     = ['Temp', 'Temp']
		self.cuts   = []
		self.cutsN  = []
		self.seqP   = []
		self.seqF   = []
		self.seqN   = 0
	  #--> Add to lo
		self.lo.append(n)
		self.lo.append(self.FixRes(n))
	  #--> 
		self.SetFragmentsHelper2(j, no, n, c, fpL)
	  #--> Return
		return True
	#---		

	def SetFragmentsHelper2(self, j, nl, n, c, fpL):
		""" Updates temporal lists. Helper to SetFragments.
			---
			j: current index in the list of N, C values (int)
			nl: reference initial n-term residue number (int)
			n: reference n-term residue number (int)
			c: reference c-term residue number (int)
			fpL: list of column names in the data frame with the results (list)
		"""
	  #--> Cleavages
		if n - 1 > 0: 
			self.cuts.append(n-1)
			self.tcuts.append(n-1)
		else:
			pass
		if c < self.pRes[3]:
			self.cuts.append(c)
			self.tcuts.append(c)
		else:
			pass
	  #--> Native cleavages
		nf = self.FixRes(n)
		if nf != None and nf - 1 > 0:
			self.cutsN.append(nf - 1)
			self.tcutsN.append(nf - 1)
		else:
			pass
		cf = self.FixRes(c)
		if cf != None and cf < self.pLength[1]:
			self.cutsN.append(cf)
			self.tcutsN.append(cf)
		else:
			pass
	  #--> Sequences
		s = n - nl
		seqF = fpL.at[j, 'Sequence']
		seqP = ' ' * s + seqF
		self.seqP.append(seqP)
		self.seqF.append(seqF)
		if self.mist != None:
			if check.CheckabWithincd(n, c, self.pRes[1], self.pRes[2]) == True:
				self.seqN += 1
			else:
				self.seqN = None
		else:
			pass
	  #--> Return
		return True
	#---

	def SetFragmentsHelper3(self, c):
		""" Update lo list and ends the fragment.
			---
			c: c-term reference (int)
		"""
		self.lo.append(c)
		self.lo.append(self.FixRes(c))
		self.lo.append(len(self.seqP))
		self.lo.append(self.seqN)
		self.lo.append(len(set(self.cuts)))
		self.lo.append(len(set(self.cutsN)))
		self.lo.append(self.seqP)
		self.lo.append(' '.join(self.seqF))
		if len(self.seqP) == self.seqN:
			self.lo.append(1)
		else:
			self.lo.append(0)
		return True
	#---
#---
# ------------------------------------------------------ Base Data Classes (END)



# -------------------------------------------------------------- PDF Files
# -----------------
class MyPDF(FPDF):
	""" To create a pdf with footer containing Page #/#T """

	#--> Page footer
	def footer(self):
	  #--> Position at 1.5 cm from bottom
		self.set_y(-15)
	  #--> Arial italic 8
		self.set_font('Arial', 'I', 8)
	  #--> Page number
		self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')
	#---
#---
# -------------------------------------------------------------- PDF Files (END)



# ------------------------------------------ Files used as input for UMSAP
class DataObjDataFile():
	""" Object containing information about a data file. 
		Attributes of the class are set in __init__ or SetVariables, unless they
		require extensive computation. In this case a Get method is provided.
		----> Attributes of the class
		- fileP : path to the data file (__init__)
		- name : name associated with the object. Mainly to search properties in config file (__init__)
		- Fdata  : Dataframe with the content of fileP (__init__)
		- header : a list with the header of each column in the data file
		- dataFrame : pandas representation of the whole data as a copy to modify without changing original data
		- nRows : number of rows in the data file
		- nCols : number of columns in the data file
	"""

	def __init__(self, file):
		""" file is the Path to the data file """
	  #--> Variables
		self.fileP = Path(file)
		self.name = config.name['DataObj']
	  #--> Load the file
		try:
			self.Fdata = dmethods.FFsCVS2DF(self.fileP)	
		except Exception:
			msg = config.dictCheckFatalErrorMsg[self.name]['BadCsvFile']
			gclasses.DlgFatalErrorMsg(msg)
			raise ValueError('')
	  #--> Other variables
		self.SetVariables()
	#---

	def SetVariables(self):
		""" Set other variables needed by the class """
	  #--> header: list with the name of the columns in the data file
		self.header = list(self.Fdata.columns)
	  #--> dataframe : copy of self.Fdata to modify it without altering the original data
		self.dataFrame = self.Fdata.copy()
	  #--> nRows, nCols
		self.nRows, self.nCols = self.dataFrame.shape
		return True
	#---
#---

class DataObjSequenceFile():
	""" This class creates sequence object containing information about a 
		sequence file or a given sequence.
		Attributes of the class are set in __init__ or SetVariables, unless they
		require extensive computation. In this case a Get method is provided.
		----> Attributes of the class:
		- name : name associated with the object. Mainly to search properties in config file (__init__)
		- Fdata: List of list with the content of seqP or seqM (__init__) 
		- seq  : sequence in the file
		- seqLength : number of residues in the sequence
		----> Methods of the class
		- GetAlign 
		- GetseqOverLapRegion	
		- GetlargerSeqOverLapRegion
		- GetprotLoc
		- GetspaceBis (Helper)
		- Getmist
		- GetprotLocmist
		- FindSeq
		- GetresNumMatch	
	"""

	def __init__(self, seqP=None, seqM=None):
		""" seqP : either file path (string or Path) or request response
			seqM : is for directly passing a sequence instead of a file or web content 
		"""
	  #--> name to search for in config file
		self.name = config.name['SeqObj']
	  #--> Fdata: list of list with the sequence 
		if seqP != None:
			if (str(type(seqP)) == "<class 'pathlib.WindowsPath'>" or 
				str(type(seqP)) == "<class 'pathlib.PosixPath'>"):
				self.Fdata = dmethods.FFsRead(seqP, char=None)
				self.Fdata = dmethods.ListFlatNLevels(self.Fdata)[1]
			else:
				self.Fdata = seqP.text.split('\n')
		else:
			if seqM == None:
				msg = config.dictCheckFatalErrorMsg[self.name]['NoSeq']
				gclasses.DlgFatalErrorMsg(msg)
				raise ValueError('')
			else:
				self.Fdata = seqM
	  #--> Other variables
		self.SetVariables()
	#---

	def SetVariables(self):
		""" Set other variables needed by the class """
	  #--> seq as a string
		self.SetSeq()
	  #--> seqLength
		self.seqLength = len(self.seq)
	  #--> Return
		return True
	#---

	####--- SetVariables Helpers
	def SetSeq(self):
		""" Set the sequence in the local or web file """
	  #--> Variables
		datao = []
	  #--> Get lines with residues
		for l in self.Fdata:
			if l == '':
				pass
			elif '>' in l:
				pass
			else:
				datao.append(l)
	  #--> Join to string
		self.seq = ''.join(datao)
	  #--> Return
		return True
	#---

	####---- Methods of the class
	#--> align
	def GetAlign(self, seqB):
		""" Sequence alignment given by BioPython alignment between self.seq 
			and seqB.
			---
			seqB : sequence to align with self.seq (string)
		"""
	  #--> Create alignment & Return
		try:
			return [True, pairwise2.align.globalds(self.seq, seqB, blosum62, 
				-10, -0.5)]
		except Exception:
			msg = config.dictCheckFatalErrorMsg[self.name]['NoAlign'] 
			gclasses.DlgFatalErrorMsg(msg)
			return [False, None]
	#---

	#--> seqOverLapRegion
	def GetseqOverLapRegion(self, seqB, align=None):
		""" List of tuples [(1, 10), (50, 60)] indicating regions in which the 
			sequences are equivalent. The index number are given for the align 
			sequence numbers. Both values in the tupple are included so it is 
			different to python range. 
			---
			seqB : sequence to align to self.seq (string)
			align: to skip calculation of the alignment. It is assume that self.seq is the first sequence in the alignment object (BioPython alignment object)
		"""
	  #--> Check align variables
		if align == None:
			try:
				align = self.GetAlign(seqB)[1]
			except Exception:
				return [False, None]
		else:
			pass
	  #--> Variables
		seqAa            = align[0][0]
		seqBa            = align[0][1]
		seqOverLapRegion = []
		start            = True
		equal            = False
	  #---# Improve with a dataframe perhaps (Down)
		for k in range(0, len(seqAa), 1):
			if start:
				if seqAa[k] == seqBa[k]:
					a = k
					start = False
					equal = True
				else:
					equal = False
			else:
				if seqAa[k] == seqBa[k]:
					if equal:
						pass
					else:
						a = k
						equal = True
				else:
					if equal:
						b = k - 1
						equal = False
						seqOverLapRegion.append((a, b))
					else:
						equal = False
		if equal:
			seqOverLapRegion.append((a, len(seqAa) - 1))
		else:
			pass
	  #---# Improve with a dataframe perhaps (Up)
		return [True, seqOverLapRegion]
	#---

	#--> largerSeqOverLapRegion
	def GetlargerSeqOverLapRegion(self, seqB, align=None):
		""" Identifies the larges overlap region between the sequences.
		    ---
			seqB : sequence to align to self.seq
			align: here is irrelvant. It is given to avoid calculating the align more than once in methods below. 
		"""
	  #--> Get the overlap regions
		try:
			seqOverLapRegion = self.GetseqOverLapRegion(seqB, align=align)[1]
		except Exception:
			return [False, None]
	  ####---- Check the regions
		k = 0 # will hold the current larger region
		e = 0 # will hold the index in seqOverLapRegion with the current largest region
		Nregions = len(seqOverLapRegion)
	  #--> No everlap
		if Nregions == 0:
			msg = config.dictCheckFatalErrorMsg[self.name]['NoOverlap'] 
			gclasses.DlgFatalErrorMsg(msg)
			return [False, None]
	  #--> Only one overlap region
		if Nregions == 1:
			return [True, seqOverLapRegion[0]]
	  #--> More than one overlap regions
		else:
			for j, i in enumerate(seqOverLapRegion):
				diff = i[1] - i[0]
				if k < diff:
					k = diff
					e = j
				else:
					pass
			return [True, seqOverLapRegion[e]]
	#---

	#--> protLoc
	def GetprotLoc(self, seqB, align=None):
		""" Set the residue number for the start and end of the largest overlap
			of self.seq and seqB. The residue numbers are for self.seq. 
			---
			seqB : sequence to align to self.seq
			align: to skip calculation of the alignment. It is assume that self.seq is the first sequence in the alignment object (BioPython alignment object)
		"""
	  #--> Check align variables
		if align == None:
			try:
				align = self.GetAlign(seqB)[1]
			except Exception:
				return [False, None]
		else:
			pass 
	  #--> seqOverLap
		try:
			largerSeqOverLapRegion = self.GetlargerSeqOverLapRegion(seqB,
				align=align)[1]
		except Exception:
			return [False, None]
	  #--> protein location
		seqAa = list(str(align[0][0]))
		tc = self.GetspaceBis(seqAa, largerSeqOverLapRegion[0])
		protLoc = (largerSeqOverLapRegion[0] - tc + 1, 
				   largerSeqOverLapRegion[1] - tc + 1)
	  #--> return
		return [True, protLoc]
	#---

	def GetspaceBis(self, seq, res):
		""" Get all '-' in seq up to index res 
			---
			seq : sequence from an alignment object containing - characters (string)
			res : seq will be scan up to residue res (int)
		"""
	  #--> Variables
		tc = 0
	  #--> Get all - bis res
		for k in range(0, res, 1):
			if seq[k] == '-':
				tc = tc + 1
			else:
				pass
	  #--> Return
		return tc
	#---

	#--> mist
	def Getmist(self, seqB, align=None):
		""" Set the difference between the recombinant residue number and native
			residue number in the larger overlapping region
			RecNum + mist = NatNum 
			---
			seqB: sequence to align to self.seq
			align: to skip calculation of the alignment. It is assume that self.seq is the first sequence in the alignment object (BioPython alignment object)
		"""
	  #--> Check align variables
		if align == None:
			try:
				align = self.GetAlign(seqB)[1]
			except Exception:
				return [False, None]
		else:
			pass 
		try:
			largerSeqOverLapRegion = self.GetlargerSeqOverLapRegion(seqB,
				align=align)[1]
		except Exception:
			return [False, None]
	  #---> Calculate mist			
		res = largerSeqOverLapRegion[0]
		seqAa = list(str(align[0][0]))
		seqBa = list(str(align[0][1]))
		tca = self.GetspaceBis(seqAa, res)
		tcb = self.GetspaceBis(seqBa, res)
		mist = tca - tcb
	  #--> Return
		return [True, mist]
	#---

	#--> protLoc and mist in one go
	def GetprotLocmist(self, seqB, align=None):
		""" Set protLoc and mist in one go
			RecNum + mist = NatNum 
			---
			seqB: sequence to align to self.seq
			align: to skip calculation of the alignment. It is assume that self.seq is the first sequence in the alignment object (BioPython alignment object)		
		"""
	  #--> Check align variables
		if align == None:
			try:
				align = self.GetAlign(seqB)[1]
			except Exception:
				return [False, None, None]
		else:
			pass 
	  #--> overlap region
		try:
			largerSeqOverLapRegion = self.GetlargerSeqOverLapRegion(seqB,
				align=align)[1]
		except Exception:
			return [False, None, None]
	  #-->	mist
		res = largerSeqOverLapRegion[0]
		seqAa = list(str(align[0][0]))
		seqBa = list(str(align[0][1]))
		tca = self.GetspaceBis(seqAa, res)
		tcb = self.GetspaceBis(seqBa, res)
		mist = tca - tcb
	  #--> protLoc
		tc = self.GetspaceBis(seqAa, res)
		protLoc = (largerSeqOverLapRegion[0] - tc + 1, 
				   largerSeqOverLapRegion[1] - tc + 1)
	  #--> Return
		return [True, protLoc, mist]
	#---	

	def FindSeq(self, seq):
		""" Find the seq in self.seq and return the N and C residue number 
			---
			seq : peptide sequence (string)
		"""
	  #--> Check self.seq
		try:
			self.seq
		except Exception:
			self.SetSeq()
	  #--> Find seq in self.seq
		nt = self.seq.find(seq)
	  #--> Get n, c
		if check.CheckNumComp(nt, comp='gt'):
			n = nt + 1
		else:
			return [False, None, None]
		c = n + len(seq) - 1
	  #--> Return
		return [True, n, c]
	#---

	#--- resNumMatch
	def GetresNumMatch(self, pdbDF):
		""" Receive a pdbDF with ['ResName', 'ResNum'] and add a column 
			['ResMatch'] with the ResNum in self.seq that align with the given 
			'ResNum' in the pdb sequence. 'ResName' assume to be one letter code
			and self.rec starts in 1.
			---
			pdbDF : data frame from DataObjPDBFile  
		"""
	  #--> Variables
		seqB = ''.join(pdbDF['ResName'].tolist())
		try:
			align = self.GetAlign(seqB)[1]
		except Exception:
			return False
	  #--> Get the match
		resNumMatch = []
		A = align[0][0]
		B = align[0][1]
		charT = 0
		for k in range(0, len(A), 1):
			if A[k] == '-':
				charT = charT + 1
			else:
				pass
			j = k + 1 - charT			
			if A[k] == B[k]:
				resNumMatch.append(j)
			elif A[k] != B[k] and B[k] != '-':
				resNumMatch.append(None)			
			else:
				pass
		pdbDF.loc[:,'ResMatch'] = resNumMatch
	 #--> Return
		return pdbDF
	#---
#---

class DataObjPDBFile():
	""" To handle pdb files
		Attributes of the class are set in __init__ or SetVariables, unless they
		require extensive computation. In this case a Get method is provided.
		----> Attributes of the class
		- name : name associated with the object. Mainly to search for in config file (__init__)
		- pdbP : path to the pdb file if given (__init__)
		- code : code to the PDB if given (__init__)
		- cs   : chain or segment id (__init__) 
		- Fdata : list of list with the content of the pdb (__init__)
		- atomDF : DF representation of the ATOM and HETATM records in Fdata
		- csInFile : list of lists with [[chains], [segments]] in the pdb file
		----> Methods of the class
		- GetatomDFcs
		- GetProtSeq
		- GetProtSeqResNumDF
		- WritePDB
		- WritePDBHelper
	"""

	def __init__(self, pdbP=None, code=None, cs=None):
		""" pdbP: path to the pdb file (Path) 
			code: is the PDB code or the downloaded content to avoid double download (string or request)
			cs  : is the chain/segment id (string)
		"""
	  #--> Variables
		self.name = config.name['PdbObj']
		self.pdbP = pdbP
		self.code = code
		self.cs   = cs
	  #--> PDB data
		if pdbP != None:
			self.Fdata = dmethods.FFsRead(self.pdbP, char=None)
			self.Fdata = dmethods.ListFlatNLevels(self.Fdata)[1]
		else:
			if isinstance(code, str):
				out, mcode = check.CheckPDB(code)
				if out:
					self.Fdata = mcode.text.split('\n')	 
			else:
				self.Fdata = self.code.text.split('\n')
	  #--> Extra variables
		self.SetVariables()
	#---

	def SetVariables(self):
		""" Set extra variables needed by the class """
	  #--> atomDF
		self.SetatomDF()
	  #--> csInFile
		self.SetcsInFile()
		return True
	#---

	####---- SetVariables Helper
	#--> atomDF
	def SetatomDF(self):
		""" Set a dataframe with all ATOM and HETATM record of the PDB file """
	  #--> Variables
		ldf = []
	  #--> Get data
		for l in self.Fdata:
			if l[0:4] == 'ATOM' or l[0:6] == 'HETATM':
				lo = []
				lo.append(l[ 0: 6].strip())
				lo.append(int(l[ 6:11].strip()))
				lo.append(l[12:16].strip())
				lo.append(l[16].strip())
				lo.append(l[17:20].strip())
				lo.append(l[21].strip())
				lo.append(int(l[22:26].strip()))
				lo.append(l[26].strip())
				lo.append(float(l[30:38].strip()))
				lo.append(float(l[38:46].strip()))
				lo.append(float(l[46:54].strip()))
				lo.append(float(l[54:60].strip()))
				lo.append(float(l[60:66].strip()))
				lo.append(l[72:76].strip())
				lo.append(l[76:78].strip())
				ldf.append(lo)
			else:
				pass
	  #--> Create data frame		
		self.atomDF = pd.DataFrame(ldf, 
			columns=config.pdbFile['Coord records']['DFHeader'])
	  #--> Return
		return True
	#---

	#--> csInFile
	def SetcsInFile(self):
		""" list of list with all [[chains], [segments]] in the pdb """
	  #--> Variables
		self.csInFile = []
	  #--> Get infor from aelf.atomDF data frame
		self.csInFile.append(self.atomDF.Chain.unique().tolist())
		self.csInFile.append(self.atomDF.Segment.unique().tolist())
		return True
	#---

	####---- Methods of the class
	#--> atomDFcs
	def GetatomDFcs(self, cs):
		""" Set a dataframe with the ATOM, HETATM records in the given pdb but 
			only for the given chain/segment 
			---
			cs: chain or segment ID (string, len <= 4)
		"""
	  #--> Set chain or segment
		lcs = len(cs)
		if lcs == 1:
			col = 'Chain'
		elif lcs > 1 and lcs <= 4:
			col = 'Segment'
		else:
			return [False, None]
	  #--> Get data
		atomDFcs = self.atomDF.loc[self.atomDF.loc[:,col] == cs]
	  #--> Return
		return [True, atomDFcs]
	#---

	def GetProtSeq(self, cs, three=True):
		""" Get the sequence in the given chain/segment.
			If three == True then a list is returned otherwise a string with 
			the sequence. 
			Only protein residues are return. 
			---
			cs : chain or segment ID (string)
			three: Return three letter code AA or one letter (Boolean)
		"""
	  #--> Get residues 
		out, df = self.GetatomDFcs(cs)
		if out:
			dfd  = df.drop_duplicates(subset='ResNum', keep='first', inplace=False)
			dfd  = dfd.loc[dfd.loc[:,'ResName'].isin(config.aaList3)]
			seqT = dfd['ResName'].tolist()
		else:
			return [False, None]
	  #--> 1 or 3 letter result
		if three:
			pass
		else:
			seqT = ''.join([config.dictAA3toAA1[v] for v in seqT])
	  #--> Return
		return [True, seqT]
	#---

	def GetProtSeqResNumDF(self, cs, three=True):
		""" Returns a data frame with columns 'ResName', 'ResNum' for a given cs.
			If three == True then 'ResName' is 3 letter code else 1 letter code. 
			Only protein residues are return. 
			---
			cs : chain or segment ID (string)
			three: Return three letter code AA or one letter (Boolean)
		"""
	  #--> Get data
		out, df  = self.GetatomDFcs(cs)
		if out:
			dfd = df.drop_duplicates(subset='ResNum', keep='first', inplace=False)
			dfd = dfd.loc[dfd.loc[:,'ResName'].isin(config.aaList3)]
			dfo = dfd[['ResName', 'ResNum']]
			dfo.reset_index(inplace=True, drop=True)
		else:
			return [False, None]
	  #--> 3 or 1 letter result
		if three:
			pass
		else:
			seqT = dfo['ResName'].tolist()
			seqT = [config.dictAA3toAA1[v] for v in seqT]
			dfo.loc[:,'ResName'] = seqT
	  #--> 
		return [True, dfo]	
	#---

	#--# Improve It is to slow (DOWN)
	def WritePDB(self, file, df):
		""" Takes a df with the structure of self.atomDF and creates a pdb file
			---
			file: path to the output file (string or Path)
			df : data frame with the data
		"""
	  #--> Open file for writing
		fileO = open(file, 'w')
	  #--> Write
		df.apply(self.WritePDBHelper, axis=1, args=[fileO])
		fileO.write('END')
	  #--> Close file
		fileO.close()
	  #--> Return
		return True
	#---

	def WritePDBHelper(self, line, fileO):
		""" Format the line so it can be writen to the pdb file
			---
			line : line from the data frame
			fileO: handler for writting to a file
		"""
	  #--> Line formatting
		l = list(line)
		lo = config.PDBformat.format(*l)
	  #--> Write line to the file
		fileO.write(lo+'\n')
	  #--> Return 
		return True
	#---
	#--# Improve It is to slow (UP)
#---
# ------------------------------------------ Files used as input for UMSAP (END)



# ----------------------------------------------- Files generated by UMSAP
class DataObjCorrFile():
	""" Object containing information about a corr file.
		Attributes of the class are set in __init__ or SetVariables, unless they
		require extensive computation. In this case a Get method is provided.
		----> Attributes of the class
		- fileP : path to the corr file (__init__)
		- name  : name associated with the file. Mainly to search for in config file (__init__)
		- Fdata : Dict with the content of fileP (__init__)
		- data  : is the pandas data frame containig the results 
		- method: method used to calculate the coefficients
		- gtitle: title of the graph
		- numCol: total number of columns in data
		- colNum: the number of the columns in the data file
		- fileD : data file used to calculate the coefficients
		----> Methods of the class
		None
	"""

	def __init__(self, fileP):
		""" fileP: path to the corr file (string or Path)"""
	  #--> Variables
		self.fileP = fileP
		self.name  = config.name['CorrObj']
	  #--> Read .corr file
		try:
			self.Fdata = dmethods.FFsReadJSON(self.fileP)
		except Exception:
			msg = config.dictCheckFatalErrorMsg[self.name]['CorrFileFormat']
			gclasses.DlgFatalErrorMsg(msg)
			raise ValueError('')
	  #--> Extra variables
		self.SetVariables()
	#---

	####---- Methods of the class
	def SetVariables(self):
		""" Set extra variables needed for the class """
		#--> data
		self.data = pd.DataFrame(self.Fdata['R'], dtype='float64')
		#--> method
		self.method = self.Fdata['I']['Method']
		#--> gtitle
		self.gtitle = str(self.method) + ' correlation coefficients'
		#--> numCol
		self.numCol = self.data.shape[0]
		#--> colNum
		self.colNum = self.Fdata['I']['SelCol']
		#--> fileD
		self.fileD = Path(self.Fdata['CI']['Datafile'])
		return True
	#---
#---

class DataObjCutpropFile():
	""" Class to handle a cutprop file 
		Attributes of the class are set in __init__ or SetVariables, unless they
		require extensive computation. In this case a Get method is provided.
		----> Attributes of the class
		- name : name associate with the object. Mainly to search for in config file (__init__)
		- fileP: file path to the given cutprop file (__init__) 
		- Fdata: Dict with the content of the file (__init__)
		- data : Data in the file as a DataFrame
		- nExp : number of experiments 
		- header: columns in the data frame
		- pRes : location of the native protein in the sequence of the rec prot
			as a list u, d, t, c
		- mist : difference between the rec and nat residue number	
		- pResNat: same as pRes but for the native sequence residue numbers
		- natProtPres: boolean to state if there is info about the native sequence in the file
		----> Methods of the class
		None	
	"""

	def __init__(self, file):
		""" file: path to the .cutprop file (string or Path) """
	  #--> Variables
		self.name  = config.name['CutPropObj']
		self.fileP = file
	  #--> Read .cutprop file
		try:
			self.Fdata = dmethods.FFsReadJSON(self.fileP)
		except Exception:
			msg = config.dictCheckFatalErrorMsg[self.name]['CutPropFileFormat']
			gclasses.DlgFatalErrorMsg(msg)
			raise ValueError('')
	  #--> Extra variables
		self.SetVariables()
	#---

	def SetVariables(self):
		""" Set extra vriables needed for the class """
		#--> data  
		self.data = pd.DataFrame(self.Fdata['R'])
		self.data.sort_values(by=config.cutprop['SortBy'], inplace=True)
		#--> nExp    
		self.nExp = self.Fdata['CI']['nExp']
		#--> header  
		self.header = list(self.data.columns)
		#--> pRes    
		self.pRes = self.Fdata['CI']['pRes']
		#--> mist    
		self.mist = self.Fdata['CI']['mist']
		#--> pResNat 
		self.SetpResNat()
		#--> natProtPres
		self.natProtPres = self.Fdata['CI']['natProtPres']	
		return True
	#---

	####---- SetVariables Helpers
	def SetpResNat(self):
		""" Same as pRes but for the native sequence """
	  #--> Check if there is infor about the native sequence and set the pResNat
		if self.mist is None:
			self.pResNat = [None] * 4
		else:
		 	self.pResNat = [1]
		 	self.pResNat.append(self.pRes[1] + self.mist)
		 	self.pResNat.append(self.pRes[2] + self.mist)
		 	self.pResNat.append(self.Fdata['CI']['pLength'][1])
	  #--> Return
		return True
	#---
#---

class DataObjAAdistFile():
	""" Class to handle a aadist file 
		Attributes of the class are set in __init__ or SetVariables, unless they
		require extensive computation. In this case a Get method is provided.
		----> Attributes of the class
		- name  : name to look for in config file (__init__)
		- fileP : path to the file (__init__)
		- Fdata : dict with the data (__init__)
		- dataDF: DFrame with the results. Multiindex DF. (__init__)
		- dataPerCent : All the data without the RD and Pos column and in % 
		- keysInInd : keys in self.Fdata allowing to identify the experiment to plot
		- nExp  : number of experiments in the file
		- nExpFP: number of experiments in the file plus FP
		- nPos  : number of total positions in the file
		- nPosD2 : half of the total number of positions
		- nPosName : list with the position label 
		- aaKeys : list of AA in the dataframes. To account for 
			non-natural AA
		- barWidth : width of each bar in comp mode
		- aaCount : dict with aa : Number in sequence
		- indKey : List with the index key
		- aVal : alpha value used to create the file
		- recSeq : recombinant sequence from which the file was originated
		- dfCol : columns in the dataframe
		----> Methods of the class
		- GetChiColor
	"""

	def __init__(self, file):
		""" file: path to the aadist file (string or Path)"""
	  #--> Variables
		self.name  = config.name['AAdistObj']
		self.fileP = file
	  #--> Read aadist file
		try:
			self.Fdata  = dmethods.FFsReadJSON(self.fileP)
			self.dataDF = dmethods.DictAAdist2DF(self.Fdata['R'],
				int(self.Fdata['CI']['Positions']))
		except Exception:
			msg = config.dictCheckFatalErrorMsg[self.name]['AAdistFileFormat']
			gclasses.DlgFatalErrorMsg(msg)
			raise ValueError('')
	  #--> Extra variables
		self.SetVariables()
	#---	

	def SetVariables(self):
		""" Set extra variables needed by the class """
		#--> keysInInd 
		self.keysInInd = list(set(
			[x[0] for x in self.dataDF.index.values.tolist()]))
		#--> dataPerCent 
		self.SetdataPerCent()
		#--> nExp  
		self.nExp = int(self.Fdata['CI']['nExp'])
		#--> nExpFP
		self.nExpFP = int(self.nExp + 1)
		#--> nPosD2
		self.nPosD2 = int(self.Fdata['CI']['Positions'])
		#--> nPos  
		self.nPos = int(2 * self.nPosD2)
		#--> nPosName 
		self.SetnPosName()
		#--> aaKeys 
		self.aaKeys = [k for k in self.dataDF.loc['FP'].loc[:,'AA'].tolist() 
			if k != config.aadist['Poskey']]
		#--> barWidth 
		self.barWidth = config.aadist['Twidth'] / self.nExpFP
		#--> aaCount 
		self.aaCount = dmethods.ListCharCount(self.Fdata['CI']['RecSeq'])
		#--> indKey 
		self.indKeys = list(self.Fdata['R'].keys())
		#--> aVal
		self.aVal = float(self.Fdata['CI']['aVal'])
		#--> recSeq
		self.recSeq = self.Fdata['CI']['RecSeq']
		#--> dfCol
		self.dfCol = list(self.dataDF.columns.values) 

		return True
	#---

	####---- SetVariables Helper
	#--> dataPerCent
	def SetdataPerCent(self):
		""" Set a df without RD and Pos and in % """
	  #--> Set local variables
		keys = self.keysInInd[:]
		keys.remove(config.aadist['RD'])
		a = self.dataDF.drop(config.aadist['RD'], axis=0)
		a.drop(index=a.loc[a.loc[:,'AA'] == config.aadist['Poskey']].index,
			inplace=True) 
		col = a.iloc[:,1:].columns
	  #--> Calculate %
		for k in keys:
			a.loc[k, col] = a.loc[k, col].div(a.loc[k, col].sum(axis=0), axis=1).multiply(100).values
		self.dataPerCent = a
	  #--> Return
		return True
	#---

	#--> nPosName
	def SetnPosName(self):
		""" Creates a list with the positions labels """
	  #--> Variables
		self.nPosName = []
		i = 1
	  #--> Set positions name
		while i <= self.nPosD2:
			j = self.nPosD2 - i + 1 
			self.nPosName.append('P' + str(j))
			i = i + 1
		while i <= self.nPos:
			j = i - self.nPosD2
			self.nPosName.append('P' + str(j) + '\'')
			i = i + 1
	  #--> Return
		return True
	#---

	####---- Methods of the class
	def GetChiColor(self, tkey, c):
		""" Return a color based on the value of Pos for a given experiment and
			a position 
		"""
	  #--> Variables
		a = self.dataDF.loc[self.dataDF.loc[:, 'AA'] == config.aadist['Poskey']] 
		b = a.loc[tkey].values.tolist()
		val = b[0][c+1]
	  #--> Color & Return
		if val > 0:
			return config.colors[self.name]['ChiColor1']
		elif val == 0:
			return config.colors[self.name]['ChiColor0']
		else:
			return config.colors[self.name]['ChiColor-']
	#---
#---

class DataObjHistFile():
	""" Class to handle a hist file 
		Attributes of the class are set in __init__ or SetVariables, unless they
		require extensive computation. In this case a Get method is provided.
		----> Attributes of the class
		- name : name associated with the object. Mainly to look for in config file. (__init__)
		- fileP : path to the file. Set in def (__init__)
		- Fdata : content of the file as dicts. Set in def (__init__)
		- nExp : number of experiments in the file
		- nExpFP : number of experiments in the file plus the FP "experiment"
		- barWidth : width of each bar in the plot 
		- dfDict : dict containing all four dataframes
		----> Methods of the class
		- GetlWin : list with the windows in a given dataframe
		- GetnWin : number of windows in a given dataframe
	"""

	def __init__(self, file):
		""" file: path to the hist file (string or Path) """
	  #--> Variables
		self.name  = config.name['HistoObj']
		self.fileP = Path(file)
	  #--> Read the file
		try:
			self.Fdata = dmethods.FFsReadJSON(self.fileP)
		except Exception:
			msg = config.dictCheckFatalErrorMsg[self.name]['HistoFileFormat']
			gclasses.DlgFatalErrorMsg(msg)
			raise ValueError('')
	  #--> Extra variables
		self.SetVariables()
	#---

	def SetVariables(self):
		""" Set extra variables needed by the class """
		#--> nExp
		self.nExp = int(self.Fdata['CI']['nExp'])
		#--> nExpFP
		self.nExpFP = int(self.nExp + 1)
		#--> barWidth
		self.barWidth = config.hist['Twidth'] / self.nExpFP
		#--> dfDict
		self.SetdfDict()
		return True
	#---

	####---- SetVariables Helpers 
	#--> dfDict
	def SetdfDict(self):
		""" Set a dict with the same keys and dataframes as values """
	  #--> Variables
		self.dfDict = {}			
	  #--> Fill the dict
		for k in config.hist['DictKeys']:
			if self.Fdata['R'][k] is None:
				self.dfDict[k] = None
			else:
				self.dfDict[k] = pd.DataFrame(self.Fdata['R'][k])
				self.dfDict[k]['Windows'] = self.dfDict[k]['Windows'].apply(
					self.WinFormat)
	  #--> Return
		return True
	#---

	def WinFormat(self, l):
		""" Fix the format of the window for pretty printing """
		a = l[1:-1]
		a = '-'.join(a.split(', '))
		return a
	#---

	####---- Methods of the class
	def GetlWin(self, tkey):
		""" Get a list with the windows in self.dfDict[tkey] """
		return self.dfDict[tkey]['Windows'].tolist()
	#---

	def GetnWin(self, tkey):
		""" Get the number of windows in self.dfDict[tkey] """
		return len(self.GetlWin(tkey))
	#---	
#---

class DataObjScriptFile():
	""" Class to handle a uscr file 
		Attributes of the class are set in __init__ or SetVariables, unless they
		require extensive computation. In this case a Get method is provided.
		----> Attributes of the class
		- name  : name associated with the object. Mainly to look for in config file (__init__)
		- fileP : path to the file (__init__)
		- module : module in the uscr file (__init__)
		- Fdata : raw data in a list of list format (__init__)
		- self.data : dict with the data (__init__)
		----> Methods of the class
		- LaunchModule
	"""

	def __init__(self, file):
		""" file: path to the uscr file (string or Path) """
	 #--> Variables
		self.name  = config.name['ScriptObj']
		self.fileP = Path(file)
		dataD      = {}
	 #--> Read the uscr file and create the temporal data dict
		self.Fdata = dmethods.FFsRead(self.fileP, char=':')
		for e in self.Fdata:
			#--> To keep Windows paths after the splitting in dmethods.FFsRead
			a = [x.strip() for x in e[1:]]
			dataD[e[0]] = ':'.join(a)
	 #--> Get module
		try:
			self.module = dataD['Module']
		except Exception:
			msg = config.dictCheckFatalErrorMsg[self.name]['NoModule']
			gclasses.DlgFatalErrorMsg(msg)
			raise ValueError('')
	 #--> Check module exists 
		if self.module in config.mod.values():
			pass
		else:
			msg = config.dictCheckFatalErrorMsg[self.name]['UnknownModule']
			gclasses.DlgFatalErrorMsg(msg)
			raise ValueError('')
	 #--> Fill self.data dict.					
		self.data = {}
		modname = config.mod[self.module]
		for k,v in config.dictUserInput2UscrFile[modname].items():
			try:
				self.data[k] = dataD[v] # Skip not valid keywords
			except Exception:
				pass
	 #--> Check that there are at least two keywords. Module is already checked
		if len(self.data) > 1:
			pass
		else:
			msg = config.dictCheckFatalErrorMsg[self.name]['NoKeywords']
			gclasses.DlgFatalErrorMsg(msg)
			raise ValueError('')
	#---

	####---- Methods of the class
	def LaunchModule(self):
		""" Launch the module """
		config.pointer['gmethods']['LaunchUscr'][self.module](self.data)
		return True
	#---
#---

class DataObjLimProtFile(MyModules):
	""" To handle limprot files 
		Attributes of the class are set in __init__ or SetVariables, unless they
		require extensive computation. In this case a Get method is provided.
		----> Attributes of the class
		- name : name associated with the object. Mainly used to search in config file (__init__)
		- fileP: path to the limprot file (__init__)
		- Fdata: Dict with all the data from fileP (__init__)
		- dataF: data frame with the Results from fileP
		- aVal : alpha value used for generating the file
		- filterPeptDF: data frame with the filtered peptides
		- Lanes  : total number of declared lanes
		- Bands  : total number of declared bands 
		- nLines : equals Bands. Used to create the fragment using gui.gui_classes.ElementFragPanel
		- nLinesT: higher of Lanes and Bands. Used to create the fragment using gui.gui_classes.ElementFragPanel
		- Results: Dict with the Results
		- Mask: True/False mask to know if peptides were detected in the corresponding (B#, L#, tost). Set in self.filterPeptDF
		- locProtType : To know how to draw the recombinant protein in the fragment panel
		- pRes : list with the location of the Nat Seq inside the Rec Seq [1, protNatStart, protNatends, protRecLength]
		- locProtType : Set how to draw the protein in the fragment panel
		- mist : RecNum + mist = NatNum 
		- pLength : list with [RecLength, NatLength]
		- colHeader : name of the columns in the data frame in Results
		- seqRec : Rec Seq
		- seqNat : Nat Seq
		- natProtPres : boolean to indicate the presence or not of information about Nat
		- listOfProt : list of protein in the data file used to generate the limprot file
		- tarprot : target protein used to generate the limprot file
		----> Methods of the class
		- GetFragments
		- LimProt2FiltPept
		- LimProt2Uscr
		- LimProt2SDataFile
		- LimProt2SeqPDF
	"""

	def __init__(self, file):
		""" file: path to the limprot file (string or Path) """
	  #--> Variables
		self.name  = config.name['LimProtObj']
		self.fileP = Path(file)
	  #--> Read the limprot file
		try:
			self.Fdata      = dmethods.FFsReadJSON(self.fileP)
			self.Fdata['R'] = dmethods.DictStringKey2TuplesKey(self.Fdata['R'])
		except Exception:
			msg = config.dictCheckFatalErrorMsg[self.name]['Fileformat'] 
			gclasses.DlgFatalErrorMsg(msg)
	  #--> Extra variables
		self.SetVariables()
	#---

	def SetVariables(self):
		""" Set extra varaibles needed by the class """
		#--> module so LimProt2Uscr can add the module name
		self.Fdata['I']['Module'] = config.mod[config.name['LimProt']]
		#--> dataF
		self.dataF = pd.DataFrame(self.Fdata['R'])
		self.dataF.sort_values(by=config.limprot['SortBy'], inplace=True)
		self.dataF.reset_index(drop=True, inplace=True)		
		#--> aVal
		self.aVal = self.Fdata['CI']['aVal']
		#--> filterPeptDF
		self.SetfilterPeptDF()
		#--> checkFP
		self.checkFP = True if self.filterPeptDF.shape[0] > 0 else False
		#--> Lanes
		self.Lanes = self.Fdata['CI']['Lanes']
		#--> Bands
		self.Bands = self.Fdata['CI']['Bands']
		#--> nLinesT to determine the h of the ElementFragPanel that goes 
		#    together with the ElementGelPanel
		self.nLinesT = self.Bands if self.Bands > self.Lanes else self.Lanes
		#--> nLines
		self.nLines = self.Bands
		#--> Results
		self.Results = self.Fdata['CI']['Results']
		#--> pRes
		self.pRes = self.Fdata['CI']['pRes']
		#--> locProtType
		self.SetlocProtType()
		#--> mist
		self.mist = self.Fdata['CI']['mist']
		#--> pLength
		self.pLength = self.Fdata['CI']['protSeqLength']
		#--> natProtPres
		self.natProtPres = False if self.pLength[1] == None else True  
		#--> colHeader
		self.colHeader = dmethods.ListColHeaderLimProtFile(self.Bands, 
			self.Lanes)[1] 
		#--> seq
		self.seqRec  = self.Fdata['CI']['RecSeq']
		#--> seqN
		self.seqNat = self.Fdata['CI']['NatSeq']
		#--> listOfProt
		self.listOfProt = self.Fdata['CI']['ListOfProt']
		#--> tarprot
		self.tarprot = self.Fdata['CI']['Targetprotein']
		return True    
	#---

	####---- SetVariables Helpers
	#--> filterPeptDF
	def SetfilterPeptDF(self):
		""" Set the FP dataframe. The data frame has the same structure as the 
			data frame with the results in the limprot file.
		"""
	  #--> Variables
		idx       = pd.IndexSlice
		a         = self.dataF.loc[:,idx[:,:,'tost']] < self.aVal
		self.Mask = a.any(axis=0)
		b         = a.any(axis=1)
	  #--> Set the data frame
		self.filterPeptDF = self.dataF.loc[b.values,:].copy()
		self.filterPeptDF.sort_values(by=config.limprot['SortBy'], inplace=True)
		self.filterPeptDF.reset_index(drop=True, inplace=True)		
	  #--> Return
		return True
	#---

	####---- Methods of the class
	def GetFragments(self):
		""" Creates a data frame to hold the fragments identified in the data 
			The DF looks like
					   TCut TCutNat N Nfix C Cfix NSeq NSeqNat NCut NCutNat Seqs bit
			L1, B1, F1
					F2
					Fn
				B2  F1
					Fn
			L2  B1  F1
					Fn
				Bn
			Ln  Bn  Fn
			           TCut and TCutNat are the same for all Frags in aa L and B
		"""	
	  #--> Variables	
		fragDF_L = [] # Individual data frames to form the multi index DF at the Lane level
		Lkeys    = [] # Keys for the index in fragDF_L
	  #--> For each Lane
		for l in range(1, self.Lanes+1, 1):
			fragDF_B = [] # Individual data frames to form the multi index DF at the Band level
			Bkeys    = [] # Keys for the index in fragDF_B
	  #--> For each Band
			for b in range(1, self.Bands+1, 1):
				#--> Variables
				fra  = [] # Each element is a fragment in the current band/lane
				# True/False values for each tost column in current band/lane 
				mask = self.dataF.loc[:,('B'+str(b),'L'+str(l),'tost')] < self.aVal
				#--> Set the fragments
				if mask.any():					
					#--> Fragment elements
					col = self.dataF.loc[mask.values,config.limprot['ColNamFrags']]
					col.columns = col.columns.droplevel(level=[0,1])
					col = col.reset_index(drop=True)
					NCt = col.iloc[:,[0,1]].values.tolist()
					NCtL = len(NCt)
					for k, m in enumerate(NCt):
						self.SetFragmentsHelper0(k, m, col, fra, NCtL, self.name)
					#--> Total cuts
					tc = len(set(self.tcuts))
					tcN = len(set(self.tcutsN))
					for z in range(0, len(fra), 1):
						fra[z][0] = tc
						fra[z][1] = tcN
					#--> Update lists for Band level
					fragDF_B.append(pd.DataFrame(fra, 
						columns=config.limprot['ColNamFragsOut']))
					Bkeys.append('B'+str(b))
				else:
					pass
			#--> Create Band level entry if there are fragments for this band/lane
			if len(fragDF_B) > 0:
				fragDF_L.append(pd.concat(fragDF_B, keys=Bkeys))
				Lkeys.append('L'+str(l))
			else:
				pass
	  #--> Create DF & Return
		#--> Create the Lane level if there is any band level entry
		if len(fragDF_L) > 0:
			return [True, pd.concat(fragDF_L, keys=Lkeys)]
		else:
			return [False, None]
	#---

	###--- Write to file
	#--> filtpept file
	def LimProt2FiltPept(self, fileO):
		""" Writes a filtered peptide file
			---
			fileO : path to the output file (string or Path)
		"""
	 #--> If there is something to export: Format, Export & Return
		if self.checkFP:
		 #--> Drop columns
			dropL = ['ttest', 'delta', 'I', 'Control Exp']
			filterpeptDF = self.filterPeptDF.drop(columns=dropL, level=2)
		 #--> Format values
			idx = pd.IndexSlice
			filterpeptDF.loc[:,idx[:,:,'tost']] = filterpeptDF.loc[:,idx[:,:,'tost']].apply(self.LimProt2FiltPeptHelper, axis=0)
		 #--> Export to file
			dmethods.FFsWriteCSV(str(fileO), filterpeptDF)
		 #--> Return
			return True		
	 #--> If not, show error msg & Return
		else:
		 #--> Error msg
			gclasses.DlgFatalErrorMsg(config.msg['FiltPept'])
		 #--> Return
			return False
	#---

	def LimProt2FiltPeptHelper(self, col):
		""" Helper to LimProt2FiltPept. Change the values in the tost columns
			to 0 or 1.
			---
			col : column from the data frame
		"""	
	 #--> New values
		nV = []
	 #--> Add values
		for i in col:
			if i == None:
				nV.append(0)
			elif i <= self.aVal:
				nV.append(1)
			else:
				nV.append(0)
	 #--> Return
		return nV
	#---

	#--- short data files. General name needed here
	def ToSDataFile(self, folderO, colOut=None, dataF=None):
		""" Writes the short data files
			---
			folderO: folder to write the short data file to (string or Path)
			colOut : columns to extract from the data file (flat list of int)
			dataF  : dataF path to the data file. If None the record in self.Fdata is used 
		"""
	  #--- Locate and read the dataF
		if dataF is None:
			tdataF = Path(self.Fdata['CI']['Datafile'])
			if check.CheckFileRead(tdataF):
				pass
			else:
				msg = config.dictCheckFatalErrorMsg[self.name]['Datafile']
				gclasses.DlgFatalErrorMsg(msg)
				return False
		else:
			tdataF = dataF
	  #--> Set colOut
		if colOut == None:
			selCol = self.Fdata['CI']['ColExtract']
		else:
			selCol = colOut	
		dataObj = DataObjDataFile(tdataF)
	  #---> Variables, here because the colHeader need the data object
		targetProtN = self.Fdata['CI']['Targetprotein']
		targetProtC = self.Fdata['CI']['DetectProtCol']
		scoreV      = self.Fdata['CI']['Scorevalue']
		scoreC      = self.Fdata['CI']['ScoreCol']
		colHeaderD  = dataObj.header
		typeV       = {colHeaderD[scoreC]:'float'}
		seqColDN    = colHeaderD[self.Fdata['CI']['SeqCol']]
		seqColTN    = self.colHeader[config.limprot['SeqColInd']]
	  #--- Create folderO
		try:
			folderO.mkdir()
		except Exception:
			pass
	  ####---> Write the files
	  #--- all-columns-all-prot-records
		dataF = dmethods.DFColValFilter(dataObj.dataFrame,
			targetProtN, targetProtC)[1]
		name = 'all-columns-all-' + targetProtN + '-records.txt'
		file = folderO / name
		dmethods.FFsWriteCSV(file, dataF)
	  #--- selected-columns-all-prot-records
		dataFS = dmethods.DFSelCol(dataF, selCol)[1]
		name = 'selected-columns-all-' + targetProtN + '-records.txt'
		file = folderO / name
		dmethods.FFsWriteCSV(file, dataFS)
	  #--- selected-columns-relevant-prot-records
		dataFSR = dataF.astype(typeV)
		dataFSR = dataFSR.loc[dataFSR.iloc[:,scoreC] >= scoreV]
		dataFSR = dmethods.DFSelCol(dataFSR, selCol)[1]
		name = 'selected-columns-relevant-' + targetProtN + '-records.txt'
		file = folderO / name
		dmethods.FFsWriteCSV(file, dataFSR)
	  #--- selected-columns-FP-prot-records
		name = 'selected-columns-FP-' + targetProtN + '-records.txt'
		file = folderO / name
		if self.checkFP:
			dataFSF = dataF[dataF[seqColDN].isin(self.filterPeptDF[seqColTN])]
			dataFSF = dmethods.DFSelCol(dataFSF, selCol)[1] 
			dmethods.FFsWriteCSV(file, dataFSF)
		else:
			fileO = open(file, 'w')
			fileO.write(config.dictCheckFatalErrorMsg[self.name]['FiltPept2'])
			fileO.close()
	  #--> Return
		return True
	#---

	##-- seqPDF & Helpers
	#-->   
	def LimProt2SeqPDF(self, fileO, Nres=100):
		""" Write the pdf with the hihglighted sequences 
			---
			fileO: path to the output file (string or path)
			Nres : number of residues per line (int) 
		"""
	  #--> Get fragments
		out, f = self.GetFragments()
		if out:
			pass
		else:
			return False
	  #--> Set the pdf object and its variables
		self.pdf = MyPDF()
		self.pdf.alias_nb_pages()
		#--- Get default margins
		left   = self.pdf.l_margin
		right  = self.pdf.r_margin
		top    = self.pdf.t_margin
		bottom = self.pdf.b_margin
		#--- Effective page width and height
		epw = self.pdf.w - left - right
		eph = self.pdf.h - top - bottom
		#--- Get x
		sx = self.seqRec[0:Nres]
		self.pdf.set_font('Courier', '', 9)
		w = self.pdf.get_string_width(sx)
		x = ((epw - w) / 2) + left		
		#--- 
		self.cont = False
		#--- colors
		self.rColor = config.colors[self.name]['RegColor']
		self.hColor = config.colors[self.name]['HColor']
	  #--> Write to the file
		for i in range(1, self.Lanes+1, 1):
			self.LimProt2SeqPDFHelper(i, 'Lane ', 'L', f, Nres, x)
		for i in range(1, self.Bands+1, 1):
			self.LimProt2SeqPDFHelper(i, 'Band ', 'B', f, Nres, x)
		self.pdf.output(str(fileO), 'F')	
	  #--> Return
		return True
	#---	

	#-->
	def LimProt2SeqPDFHelper(self, i, LBl, LBs, f, Nres, x):
		""" Helper to LimProt2SeqPDF
			---
			i   : current lane/band number (int)
			LBl : label for Lane or Band (string)
			LBs : first letter in label (string)
			f   : DF with the fragments
			NRes: number of residues to write in one line (int)
			x   : adjusted starting x coordinate for the sequence in the pdf   
		"""
	  #--> PDF page setup
		self.pdf.add_page()
		self.pdf.set_font('Arial', 'I', 16)
		self.pdf.set_text_color(0, 0, 0)
		th = self.pdf.font_size
		self.pdf.cell(0, th, LBl + str(i), 0, 0, 'L', 0)
		self.pdf.ln(2*th)
	  #--> Get fragments for the current lane/band
		try:
			if LBs == 'L':
				df = f.loc[LBs+str(i)]
				dfFrag = dmethods.DFGetFragments(df, self.name, strC=False)[1]
				goL = True
			else:
				idx = pd.IndexSlice
				df = f.loc[idx[:,LBs+str(i)],:]
				dfFrag = dmethods.DFGetFragments(df, self.name, strC=False)[1]
				goL = True
		except Exception:
			goL = False
	  #--- Write the sequence
		#---# Improve the function with extra helpers (Down)
		if goL:
			lenS = len(self.seqRec)
			#---
			self.pdf.set_font('Arial', '', 12)
			th = self.pdf.font_size
			self.pdf.cell(0, th, '-- Recombinant sequence:', 0, 0, 'L', 0)
			self.pdf.ln(2*th)
			self.pdf.set_font('Arial', '', 10)
			th = self.pdf.font_size
			self.pdf.cell(0, th, '- Detected fragments:', 0, 0, 'L', 0)
			self.pdf.ln(2*th)
			tfrags = ', '.join(list(map(str, dfFrag)))
			self.pdf.multi_cell(0, th, tfrags, 0, 0, 'L', 0)
			self.pdf.ln(2*th)
			msg = '- Sequence with highlighted fragments:'
			self.pdf.cell(0, th, msg, 0, 0, 'L', 0)
			self.pdf.ln(2*th)
			self.pdf.set_font('Courier', '', 9)
			th = self.pdf.font_size
			#---
			for s in range(0, lenS, Nres):
				self.LimProt2SeqPDFHelper2(s, x, dfFrag, Nres, th)
			#---
			if self.natProtPres:
				lenS = len(self.seqNat)
				#---
				self.pdf.ln(2*th)
				self.pdf.set_font('Arial', '', 12)
				th = self.pdf.font_size
				self.pdf.cell(0, th, '-- Native sequence:', 0, 0, 'L', 0)
				self.pdf.ln(2*th)
				self.pdf.set_font('Arial', '', 10)
				th = self.pdf.font_size
				self.pdf.cell(0, th, '- Detected fragments:', 0, 0, 'L', 0)
				self.pdf.ln(2*th)
				tfrags = dmethods.DHelperFragTuple2NatSeq(self, dfFrag, 
					strC=False)[1]
				tfragsL = ', '.join(list(map(str, tfrags)))
				self.pdf.multi_cell(0, th, tfragsL, 0, 0, 'L', 0)
				self.pdf.ln(2*th)
				msg = '- Sequence with highlighted fragments:'
				self.pdf.cell(0, th, msg, 0, 0, 'L', 0)
				self.pdf.ln(2*th)
				self.pdf.set_font('Courier', '', 9)
				th = self.pdf.font_size
				#---
				for s in range(0, lenS, Nres):
					self.LimProt2SeqPDFHelper2(s, x, tfrags, Nres, th, RN='N')
			else:
				pass
		#---# Improve the function with extra helpers (UP)				
		else:
			self.pdf.set_font('Arial', '', 10)
			th = self.pdf.font_size
			if LBs == 'L':
				self.pdf.cell(0, th, 'Empty Lane', 0, 0, 'L', 0)
			else:
				self.pdf.cell(0, th, 'Empty Band', 0, 0, 'L', 0)
		self.pdf.set_text_color(0,0,0)  
	  #--> Return
		return True
	#---

	#--> 
	def LimProt2SeqPDFHelper1(self, c, sr, th):
		""" Helper to LimProt2SeqPDF 
			---
			c : color in hte format needed by FPDF 
			sr: peptide sequence (string)
			th: line heigth (int)
		"""
		self.pdf.set_text_color(*c)
		wh = self.pdf.get_string_width(sr)
		self.pdf.cell(wh, th, sr, 0, 0, 'L', 0)
		return True
	#---

	#-->
	def LimProt2SeqPDFHelper2(self, s, x, dfFrag, Nres, th, RN='R'):
		""" Helper to LimProt2SeqPDF 
			---
			s: the sequence in the current line starts in index s of the 0-started residue number (int)
			x: the coordinate in the pdf page to start writing the sequence
			dfFrag: data frame with the fragments
			Nres: number of residues per line to write to the pdf file
			th: height of the line
			RN: write the info for the Recombinant or Native protein
		"""
	  #--> Get the correct sequence
		if RN == 'R':
			tseq = self.seqRec
		else:
			tseq = self.seqNat
	  #--> Variables
		self.pdf.set_x(x)
		fr = sfr = s
		end = s + Nres
	  #--> Set the proper color for the residue segments
		for t in dfFrag:
	   #--> Change t[0] and t[1] from residue numbers to list numbers
			n = 'NA' if t[0] == 'NA' else t[0] - 1
			c = 'NA' if t[1] == 'NA' else t[1] - 1
	   #--> Check
			if n >= end:
				pass
			elif n == 'NA' or c == 'NA':
				pass
			else:
				if n == fr and c < end:
					fr = n
					lr = c+1
					sr = tseq[fr:lr]
					#---
					self.LimProt2SeqPDFHelper1(self.hColor, sr, th)
					#---
					fr = end if lr >= end else lr
				elif n > fr and c < end:
					fr = fr
					lr = n
					sr = tseq[fr:lr]
					#---
					self.LimProt2SeqPDFHelper1(self.rColor, sr, th)
					#---
					fr = lr
					lr = c+1
					####----
					sr = tseq[fr:lr]
					#---
					self.LimProt2SeqPDFHelper1(self.hColor, sr, th)
					#---
					fr = end if lr >= end else lr
				elif n == fr and c >= end:
					fr = n
					lr = end
					sr = tseq[fr:lr]
					#---
					self.LimProt2SeqPDFHelper1(self.hColor, sr, th)
					#---
					fr = end
					self.cont = True
					break
				elif n > fr and c >= end:
					fr = fr
					lr = n
					sr = tseq[fr:lr]
					#---
					self.LimProt2SeqPDFHelper1(self.rColor, sr, th)
					#---
					fr = lr
					lr = end
					####----
					sr =tseq[fr:lr]
					#---
					self.LimProt2SeqPDFHelper1(self.hColor, sr, th)
					#---
					fr = end
					self.cont = True
					break
				elif (n < sfr and c > sfr and c < end
					  and self.cont == True):
					lr = c+1
					sr = tseq[fr:lr]
					#---
					self.LimProt2SeqPDFHelper1(self.hColor, sr, th)
					#---
					self.cont = False
					fr = end if lr >= end else lr
				elif (n < sfr and c > sfr and c >= end
					  and self.cont == True):
					sr = tseq[fr:lr]
					#---
					self.LimProt2SeqPDFHelper1(self.rColor, sr, th)
					#---
					fr = end
					self.cont = True
					break																
				else:
					pass
		if fr < end:
			sr = tseq[fr:end]
			#---
			self.LimProt2SeqPDFHelper1(self.rColor, sr, th)
		else:
			pass
		self.pdf.ln(th)
	  #--> Return
		return True
	#---
#---							

class DataObjProtProfFile(MyModules):
	""" To handle protprof files 
		Attributes of the class are set in __init__ or SetVariables, unless they
		require extensive computation. In this case a Get method is provided.
		----> Attributes of the class
		- name       : 
		- fileP      : 
		- Fdata      : 
		- dataFrame  : 
		- checkFP    : check that there are some proteins in self.Fdata['R']
		- nConds     : number of conditions in the file
		- timeP      : number of relevant points per conditions, including the reference
		- loga       : -log10[aVal]
		- aVal       : alpha value used when creating the file
		- NProt      : number of protein detected
		- xCoordTimeA: list of list with x coordinates for the time analysis plot for each condition
		- ZscoreVal  : value of the zscore in the file 
		- ZscoreValP : value of the zscore in the file in % 
		- nCondsL    : list with Conditions name
		- nTimePL    : list with relevant points names including reference
		----> Methods of the class
		None
	"""

	def __init__(self, file):
		""" file: path to the protprof file (string or Path) """
	  #--> Variables
		self.name = config.name['ProtProfObj']
		self.fileP = Path(file)
	  #--> Read the protprof file
		try:
			self.Fdata = dmethods.FFsReadJSON(self.fileP)
			self.Fdata['R'] = dmethods.DictStringKey2TuplesKey(self.Fdata['R'])
		except Exception:
			gclasses.DlgFatalErrorMsg(
				 config.dictCheckFatalErrorMsg[self.name]['FileFormat'])
	  #--> Extra variables neede by the class
		self.SetVariables()
	#---

	def SetVariables(self):
		""" Set extra variables needed by the class """
		#--> To include module in uscr file
		self.Fdata['I']['Module'] = config.mod[config.name['ProtProf']]
		#--> dataFrame
		self.dataFrame = pd.DataFrame(self.Fdata['R'])
		 #--> Sort & Reset is needed bacause writing reading breaks the order
		self.dataFrame.sort_values(by=config.protprof['SortBy'], inplace=True)
		self.dataFrame.reset_index(drop=True, inplace=True)
		#-->  checkFP
		self.checkFP = True if self.dataFrame.shape[0] > 0 else False
		#--> nConds
		self.nConds = self.Fdata['CI']['NCond']
		self.Xv = self.Fdata['CI']['Xv']
		#--> timeP
		self.timeP = self.Fdata['CI']['NTimeP']
		self.Yv = self.Fdata['CI']['Yv']
		#--> loga
		self.loga = self.Fdata['CI']['loga']
		#--> aVal
		self.aVal = self.Fdata['CI']['aVal']
		#--> NProt
		self.NProt = self.dataFrame.shape[0]
		#--> ZscoreVal
		self.ZscoreVal  = self.Fdata['CI']['ZscoreVal']
		self.ZscoreValP = self.Fdata['I']['ZscoreVal'] 
		#--> Legends
		self.nCondsL      = self.Fdata['CI']['LabelCond']
		self.nTimePL      = self.Fdata['CI']['LabelRP']
		self.ControlLabel = self.Fdata['CI']['LabelControl']
		self.CType        = self.Fdata['CI']['CType']
		#--> xCoordTimeA
		self.SetMissingTP()
		return True
	#---

	####---- SetVariables Helpers
	def SetMissingTP(self):
		""" Set a list indicating the x values for the
			time analysis plot in protprofRes 
		"""
	  #--> Variables
		self.xCoordTimeA = []
	  #--> Fill the list
		if self.CType == config.combobox['ControlType'][1]:
			for y in range(1, self.Yv+1, 1):
				xL = [0]
				t  = 1
				for x in range(0, self.Xv, 1):
					val = self.Fdata['CI']['ResultsControl'][x][y]
					if val[0] == None or val[0] == 'None':
						pass
					else:
						xL.append(t)
					t += 1
				self.xCoordTimeA.append(xL)
		else:
			for x in range(0, self.Xv, 1):
				xL = [0]
				t  = 1
				for y in range(1, self.Yv+1, 1):
					val = self.Fdata['CI']['ResultsControl']
					if val[0] == None or val[0] == 'None':
						pass
					else:
						xL.append(t)
					t += 1
				self.xCoordTimeA.append(xL)
	  #--> Return
		return True
	#---

	##--> short data files. General name needed for this method
	def ToSDataFile(self, fileO, colOut=None, dataF=None):
		""" Writes the short data files 
			---
			fileO : file to write the output (string or Path)
			colOut: columns to extract (list of int)
			dataF : path to the data file if None read from tarprot
		"""
	 #--- Locate and read the dataF
		if dataF is None:
			tdataF = Path(self.Fdata['CI']['Datafile'])
			if check.CheckFileRead(tdataF):
				pass
			else:
				msg = config.dictCheckFatalErrorMsg[self.name]['Datafile']
				gclasses.DlgFatalErrorMsg(msg)
				return False
		else:
			tdataF = dataF
	 #--> Set columns to extract
		if colOut == None:
			selCol = self.Fdata['CI']['ColExtract']
		else:
			selCol = colOut	
	 #--> Create data file object
		dataObj = DataObjDataFile(tdataF)
	 #--> Get the data frame
		df = dmethods.DFSelCol(
			dataObj.dataFrame,
			selCol,
		)[1]
	 #-->
		dmethods.FFsWriteCSV(fileO, df)
	 #--> Return
		return True
	#---
#---

class DataObjTarProtFile(MyModules):
	""" Object containing information about a tarprot file.
		Attributes of the class are set in __init__ or SetVariables, unless they
		require extensive computation. In this case a Get method is provided.
		----> Attributes of the class
		- fileP : Path to the tarprot file (__init__)
		- name  : name to look for in config file (__init__)
		- Fdata : dict with the data in the file (__init__) 
		- colHeader : list with the header of the tarprot file (__init__)
		- colExpInd : index of the experiments in colHeader (__init__)
		- dataF  : DF with the result dict and correct types (__init__)
		- nExp   : number of experiments (__init__)
		- nLinesT: = self.nExp. Mainly for ElementFragPanel
		- nLines : = self.nExp. Mainly for ElementFragPanel. It is needed to make the ElementGelPanel to work together with ElementFragPanel 
		- nExpLabels  : Label of the experiments (__init__)
		- filterPeptDF: Dataframe of all peptide identified in at least one exp. It is used everywhere so set in (__init__)
		- checkFP     : True if FP is not empty False otherwise
		- pRes        : numbers for the recProt length, natProt loc (__init__)
		- pLength     : length of the Rec and Nat proteins (__init__)
		- natProtPres : Boolean for the native sequence presence (__init__)
		- mist        : mistmatch (__init__)
		- recSeq      : recombinant protein sequence (__init__)
		- locProtType : how to paint the protein in tarprotR (__init__)
		- fragments   : dataframe with the fragments (ON DEMAND)
		----> Methods of the class 
		- Setfragments, Helpers and Getfragments
		- TarProtFile2TarProtModule
		- FixRes
		- All writing methods
	"""

	def __init__(self, file):
		""" file: path to the tarprot file (string or Path)"""
	  #--> Variables
		self.fileP = Path(file)
		self.name  = config.name['TarProtObj']
	  #--- Read file
		try:
			self.Fdata = dmethods.FFsReadJSON(self.fileP)
		except Exception:
			try:
				temp = dmethods.FFsReadCSV(self.fileP)
				self.CreateFdataDict(temp) # Fix R dict. If no R then exit
			except Exception:
				gclasses.DlgFatalErrorMsg(
				  config.dictCheckFatalErrorMsg[self.name]['TarProtFileFormat'])
				raise ValueError('')
	  #--- Fix for all versions
		self.FixFdataAllV() # R already fix by self.CreateFdataDict
	  #--- Set extra variables
		self.SetVariables()
	#---

	####---- Helpers to __init__
	#-->
	def CreateFdataDict(self, temp):
		""" Create the Fdata dict. Types will be adjusted in another method 
			---
			temp: result from dmethods.FFsReadCSV
		"""
	  #--> Create the dict
		self.Fdata = {
			'I'  : {},
			'CI' : {},
			'R'  : {},
			'V'  : {}
		}
	  #--> Get version
		try:
			version = temp[-1][1]
		except Exception:
			version = '1.0.0'
	  #--> I
		try:
			if version == '1.0.0':
				self.Fdata['I']["Datafile"        ] = temp[5][1]
				self.Fdata['I']["Seq_rec"         ] = temp[6][1]
				self.Fdata['I']["Seq_nat"         ] = 'NA'
				self.Fdata['I']["PDBfile"         ] = 'NA'
				self.Fdata['I']["Outputfolder"    ] = temp[7][1]
				self.Fdata['I']["Outputname"      ] = 'NA'
				self.Fdata['I']["Targetprotein"   ] = temp[9][1]
				self.Fdata['I']["Scorevalue"      ] = temp[10][1]
				self.Fdata['I']["Datanorm"        ] = temp[11][1]
				self.Fdata['I']["aVal"            ] = temp[12][1]
				self.Fdata['I']["Positions"       ] = temp[13][1]
				self.Fdata['I']["Sequencelength"  ] = temp[14][1]
				self.Fdata['I']["Histogramwindows"] = temp[17][1]
				self.Fdata['I']["PDBID"           ] = 'NA'
				self.Fdata['I']["SeqCol"          ] = temp[20][1]
				self.Fdata['I']["DetectProtCol"   ] = temp[23][1]
				self.Fdata['I']["ScoreCol"        ] = temp[24][1]
				self.Fdata['I']["ColExtract"      ] = temp[25][1]
				self.Fdata['I']["Control"         ] = temp[26][1]
				self.Fdata['I']["Results"         ] = (
					temp[27][1].replace('{', '').replace('}', ';')[0:-1])
			elif version == '2.0' or version == '2.0.1':
				self.Fdata['I']["Datafile"        ] = temp[5][1]
				self.Fdata['I']["Seq_rec"         ] = temp[6][1]
				self.Fdata['I']["Seq_nat"         ] = temp[7][1]
				self.Fdata['I']["PDBfile"         ] = temp[8][1]
				self.Fdata['I']["Outputfolder"    ] = temp[9][1]
				self.Fdata['I']["Outputname"      ] = temp[10][1]
				self.Fdata['I']["Targetprotein"   ] = temp[12][1]
				self.Fdata['I']["Scorevalue"      ] = temp[13][1]
				self.Fdata['I']["Datanorm"        ] = temp[14][1]
				self.Fdata['I']["aVal"            ] = temp[15][1]
				self.Fdata['I']["Positions"       ] = temp[16][1]
				self.Fdata['I']["Sequencelength"  ] = temp[17][1]
				self.Fdata['I']["Histogramwindows"] = temp[18][1]
				self.Fdata['I']["PDBID"           ] = temp[19][1]
				self.Fdata['I']["SeqCol"          ] = temp[21][1]
				self.Fdata['I']["DetectProtCol"   ] = temp[22][1]
				self.Fdata['I']["ScoreCol"        ] = temp[23][1]
				self.Fdata['I']["ColExtract"      ] = temp[24][1]
				self.Fdata['I']["Control"         ] = temp[25][1]
				self.Fdata['I']["Results"         ] = temp[26][1]				
			else:
				return False
		except Exception:
			return False
	  #--> CI
		self.Fdata['CI'] = copy.deepcopy(self.Fdata['I'])
		if version == '1.0.0':
			self.Fdata['CI']['RecSeq'] = temp[41][1]
		elif version == '2.0' or version == '2.0.1':
			self.Fdata['CI']['RecSeq'] = temp[32][1]
		else:
			pass 
		self.Fdata['CI']["protSeqLength"] = [temp[-2][0], temp[-2][1]]
		self.Fdata['CI']["mist"] = temp[-2][3]
		self.Fdata['CI']["ProtLoc"] = [temp[-2][4], temp[-2][5]]	
	  #--- R
		if version == '1.0.0':
			lines = temp[48:-2]
		elif version == '2.0' or version == '2.0.1':
			lines = temp[39:-2]
		else:
			return False
		llines = len(lines[0])
		nExp = llines - config.tarprot['NumColsHeader']
		colN = dmethods.ListColHeaderTarProtFile(nExp)[0]
		for k, v in enumerate(colN):
			self.Fdata['R'][v] = {} 
		for k, l in enumerate(lines):
			for j in range(0, llines, 1):
				self.Fdata['R'][colN[j]][str(k)] = l[j]
	  #--- V
		self.Fdata['V']['version'] = version
	  #--- Fix Results & Return
		if self.FixFdataR(nExp, version):
			return True
		else:
			return False
	#---

	###--- Fix data methods
	#-->
	def FixFdataR(self, nExp, version):
		""" Fix the R dicts in Fdata for older versions 
			----
			nExp: number of experiments in the file (int)
			version : version in the file (string)
		"""	
	  #--> Set myF list with fix methods for the control and results experiments
		if version == '1.0.0':
			myF = [self.FixControlExpV1, self.FixExpNV1]
		elif version == '2.0' or version == '2.0.1': 
			myF = [self.FixControlExpV2, self.FixExpNV2]
	  #--> Fix Control
		for k, v in self.Fdata['R']['Control Exp'].items():
			self.Fdata['R']['Control Exp'][k] = myF[0](v)
	  #--> Fix Experiments
		for i in range(1, nExp+1, 1):
			label = 'Exp' + str(i)
			for k, v in self.Fdata['R'][label].items():
				self.Fdata['R'][label][k] = myF[1](v)
	  #--> Fix the column number
		for i in config.tarprot['ColNamFrags']:
			for k, v in self.Fdata['R'][i].items():
				try:
					self.Fdata['R'][i][k] = int(v)
				except Exception:
					try:
						self.Fdata['R'][i][k] = float(v)
					except Exception:
						if str(self.Fdata['R'][i][k]) == 'NA':
							self.Fdata['R'][i][k] = None
						else:
							self.Fdata['R'][i][k] = str(v)
	  #--> Return
		return True
	#---
	
	#-->
	def FixControlExpV1(self, l):
		""" Fix the control experiment in tarprot v.1.0.0 
			---
			l: list with a control experiment entry
		"""
		return list(map(float, l.strip().split(' ')))
	#---

	#-->
	def FixExpNV1(self, l):
		""" Fix the experiment in tarprot v1.0.0 
			---
			l: list with an experiment to fix
		"""
	  #--> Variables
		b = l.split('} {')
		lo = []
	  #--> Fix each element
		for e in b:
			a = e.replace('{', '')
			a = a.replace('}', '')
			a.strip()
			a = a.split(' ')
			lo.append(a)
	  #--> Final Fix & Return
		lo = self.FixExpHelper(lo)
		return lo
	#---

	#-->
	def FixControlExpV2(self, l):
		""" Fix the type in the experiment column of the tarprot file 
			---
			l: control experiment to fix
		"""
		return list(map(float, l[1:-1].strip().split(',')))
	#---

	def FixExpNV2(self, l):
		""" Fix the types in the experiment columns 
			l: experiment entry to fix
		"""
	  #--> Variables
		b  = l[2:-2].split('], [')
		lo = []
	  #--> Fix each element 
		for e in b:
			lo.append(e.strip().split(', '))
	  #--> Final fix & Return
		lo = self.FixExpHelper(lo)	
		return lo
	#---

	#--> 
	def FixExpHelper(self, lo):
		""" Helper to FixExpN 1 and 2 
			---
			lo: list with elements
		"""
		for k, e in enumerate(lo):
			for j, i in enumerate(e):
				try:
					lo[k][j] = int(i)
				except Exception:
					try:
						lo[k][j] = float(i)
					except Exception:
						pass
		return lo
	#---

	#-->
	def FixFdataAllV(self):
		""" Fix I, CI and V """
	  #--> I
	   #--> Remove control and modify results
		try:
			self.Fdata['I']['Results'] = (
				self.Fdata['I']['Control'] 
				+ '; ' 
				+ self.Fdata['I']['Results']
			)
			del(self.Fdata['I']['Control'])
		except Exception:
			pass
	   #--> Module
		self.Fdata['I']['Module'] = config.mod[config.name['TarProt']]
	  #--> CI
	   #--> Data File
		self.Fdata['CI']['Datafile'] = Path(self.Fdata['CI']['Datafile']) 
	   #--> PDB File
		if (self.Fdata['CI']['PDBfile'] == None or 
			self.Fdata['CI']['PDBfile'] == 'None' or
			self.Fdata['CI']['PDBfile'] == 'NA'):
			self.Fdata['CI']['PDBfile'] = None
		else:
			pass
	   #--> Seq_nat
		if (self.Fdata['CI']['Seq_nat'] == None or 
			self.Fdata['CI']['Seq_nat'] == 'None' or
			self.Fdata['CI']['Seq_nat'] == 'NA'):
			self.Fdata['CI']['Seq_nat'] = None
		else:
			pass
	   #--> Scorevalue
		self.Fdata['CI']['Scorevalue'] = float(self.Fdata['CI']['Scorevalue'])
	   #--> aVal
		self.Fdata['CI']['aVal'] = float(self.Fdata['CI']['aVal'])
	   #--> Positions
		try:
			self.Fdata['CI']['Positions'] = int(self.Fdata['CI']['Positions'])
		except Exception:
			pass
	   #--> Sequencelength
		try:
			self.Fdata['CI']['Sequencelength'] = int(
				self.Fdata['CI']['Sequencelength'])
		except Exception:
			pass
	   #--> histogramwindows
		if isinstance(self.Fdata['CI']['Histogramwindows'], list):
			pass
		else:
			if (self.Fdata['CI']['Histogramwindows'] == None or
				self.Fdata['CI']['Histogramwindows'] == 'None' or
				self.Fdata['CI']['Histogramwindows'] == 'NA'):
				self.Fdata['CI']['Histogramwindows'] = None
			else:
				a = list(map(int, 
							(self.Fdata['CI']['Histogramwindows'].split(' '))))
				a.sort()
				self.Fdata['CI']['Histogramwindows'] = a
	   #--> PDB ID
		if self.Fdata['V']['version'] == '1.0.0':
			self.Fdata['CI']['PDBID'] = [None, None]
			char = None
		elif (self.Fdata['V']['version'] == '2.0' or
			  self.Fdata['V']['version'] == '2.0.1'):
			char = ':'
		else:
			char = ';'
		if char == None:
			pass
		else:
			self.Fdata['CI']['PDBID'] = self.Fdata['I']['PDBID'].strip().split(char)
			if len(self.Fdata['CI']['PDBID']) == 2:
				pass
			else:
				if self.Fdata['CI']['PDBfile'] == None:
					self.Fdata['CI']['PDBID'] = [None, None]
				else:
					self.Fdata['CI']['PDBID'] = [None, 
			 			self.Fdata['CI']['PDBID'][0]]
	   #--> SeqCol
		self.Fdata['CI']['SeqCol'] = int(self.Fdata['CI']['SeqCol'])
	   #--> DetectProtCol
		self.Fdata['CI']['DetectProtCol'] = int(
			self.Fdata['CI']['DetectProtCol'])
	   #--> ScoreCol
		self.Fdata['CI']['ScoreCol'] = int(self.Fdata['CI']['ScoreCol'])
	   #--> Detected Columns
		if isinstance(self.Fdata['CI']['ColExtract'], list):
			pass
		elif isinstance(self.Fdata['CI']['ColExtract'], str):
			a = self.Fdata['CI']['ColExtract'].split()
			self.Fdata['CI']['ColExtract'] = dmethods.ListExpand(a)	
		else:
			pass
	   #--> Control and Results
		try:
			self.Fdata['CI']['Results'] = (
				self.Fdata['CI']['Control'] 
				+ '; ' 
				+ self.Fdata['CI']['Results']
			)
			del(self.Fdata['CI']['Control'])
		except Exception:
			pass
	   #--> ProtLoc
		try:
			self.Fdata['CI']['ProtLoc'][0] = int(self.Fdata['CI']['ProtLoc'][0])
			self.Fdata['CI']['ProtLoc'][1] = int(self.Fdata['CI']['ProtLoc'][1])
		except Exception:
			self.Fdata['CI']['ProtLoc'][0] = None
			self.Fdata['CI']['ProtLoc'][1] = None
	   #--> protSeqLength
		self.Fdata['CI']['protSeqLength'][0] = int(
			self.Fdata['CI']['protSeqLength'][0])
		try:
			self.Fdata['CI']['protSeqLength'][1] = int(
				self.Fdata['CI']['protSeqLength'][1])
		except Exception:
			self.Fdata['CI']['protSeqLength'][1] = None
	   #--> mist
		try:
			self.Fdata['CI']['mist'] = int(self.Fdata['CI']['mist'])
		except Exception:
			self.Fdata['CI']['mist'] = None
	   #--> pRes
		self.Fdata['CI']['pRes'] = [
			1, 
			*self.Fdata['CI']['ProtLoc'], 
			self.Fdata['CI']['protSeqLength'][0],
		]
	  #-- Return
		return True
	#---

	###--- SetVariables and helpers
	def SetVariables(self):
		""" Set extra variables needed by the class """
		#--> nExp
		self.nExp = (len(self.Fdata['R'].keys()) 
					 - config.tarprot['NumColsHeader'])
		#--> nLinesT to calculate the h of ElementFragPanel
		self.nLinesT = self.nExp
		#--> nLines for the labels of ElementFragPanel
		self.nLines = self.nExp
		#--> colHeader and colExpInd 
		self.colHeader, self.colExpInd = dmethods.ListColHeaderTarProtFile(self.nExp)     
		#--> dataF
		self.dataF = pd.DataFrame(self.Fdata['R'])
		#--> nExpLabels
		self.nExpLabels = ['Exp'+str(x) for x in range(1, self.nExp+1, 1)]   
		#--> filterPeptDF
		self.SetfilterPeptDF()
		#--> checkFP
		self.checkFP = True if self.filterPeptDF.shape[0] > 0 else False
		#--> pRes 
		self.pRes = self.Fdata['CI']['pRes']
		#--> pLength  
		self.pLength = self.Fdata['CI']["protSeqLength"]
		#--> natProtPres
		self.natProtPres = False if self.pLength[1] == None else True  
		#--> mist    
		self.mist = self.Fdata['CI']['mist']
		#--> recSeq  
		self.recSeq = self.Fdata['CI']['RecSeq']     
		#--> locProtType 
		self.SetlocProtType()
		return True
	#---

	def SetfilterPeptDF(self):
		""" Set the dataframe of peptides that were identified in at least one 
			experiment. It has the same structure as self.Fdata['R']
		"""
		self.filterPeptDF = pd.DataFrame(columns=self.colHeader)
		if self.dataF.empty:
			pass
		else:
		#--# Improve with a mask and any method (Down)	
			for i in self.colExpInd:
				tempDF = self.dataF[self.dataF.iloc[:,i].str[0].str[0].isin([1.0])].copy()
				self.filterPeptDF = self.filterPeptDF.append(tempDF)
			self.filterPeptDF.drop_duplicates(keep='first', inplace=True, 
				subset=config.tarprot['SeqColName'])
			self.filterPeptDF.sort_values(by=config.tarprot['SortBy'], inplace=True)
			self.filterPeptDF.reset_index(drop=True, inplace=True)
		#--# Improve with a mask and any method (UP)
		return True
	#---

	####---- Methods of the class
	#-->
	def FiltPeptDFForOneExp(self, exp):
		""" From self.filterPeptDF extract the peptides for a single 
			experiment 
			---
			exp: experiment number (int)
		"""
	  #--> correct exp to math the index in self.colExpInd
		i = self.colExpInd[exp - 1]
	  #--> Get the data frame
		tempDF = self.filterPeptDF[self.filterPeptDF.iloc[:,i].str[0].str[0].isin([1.0])].copy()
		tempDF.sort_values(by=config.tarprot['SortBy'], inplace=True)
		tempDF.reset_index(drop=True, inplace=True)
	  #--> Return. It could return an empty DF
		return tempDF
	#---

	#--> fragments
	def Getfragments(self):
		""" Set the fragments data frame. This is a multiindex dataframe with
				TCut TCutNat N Nfix C Cfix NSeq NSeqNat NCut NCutNat Seqs bit
			E1 0 
		   	   1
		       2 
		       3
			E2 0
		       1
				TCut and TCutNat are the same for all Frags in an Exp	
		"""
	  #--> Variables
		fragmentsDF = [] # will hold the list of dataframes
		fragmentsLL = [] # will hold the keys used as labels
	  #--> Loop over experiments
		for i in range(1, self.nExp+1, 1):
			fra = []
			fpL = self.FiltPeptDFForOneExp(i)
			fpL = fpL.loc[:,config.tarprot['ColNamFrags']]
			if fpL.empty == True:
				pass
			else:
				NCt = fpL.iloc[:,[0, 1]].values.tolist()
				NCtL = len(NCt)		
				for j, k in enumerate(NCt):
					self.SetFragmentsHelper0(j, k, fpL, fra, 
						NCtL, self.name)
				#---
				tc = len(set(self.tcuts))
				tcN = len(set(self.tcutsN))
				for l in range(0, len(fra), 1):
					fra[l][0] = tc
					fra[l][1] = tcN
				#---
				fragmentsDF.append(pd.DataFrame(fra, 
					columns=config.tarprot['ColNamFragsOut']))
				fragmentsLL.append('E'+str(i))
	  #--> Return
		if len(fragmentsDF) > 0:
			return pd.concat(fragmentsDF, keys=fragmentsLL)
		else:
			return None
	#---

	#-->
	def TarProtFile2TarProtModule(self):
		""" Fill the tarprotM with the variables in the tarprot file to allow
			a custom update
		"""
		config.pointer['gmethods']['LaunchUscr'][config.mod[config.name['TarProt']]](self.Fdata['I'])
		return True
	#---		

	###--- Write output files
	#--> filtpept file
	def TarProt2FiltPept(self, fileO):
		""" Writes a filtered peptide file 
			---
			fileO: path to the output file 
		"""
	 #--> If there is anything to export format Exp columns, Export & Return
		if self.checkFP:
		 #--> Remove control column
			filterPeptDF = self.filterPeptDF.drop(axis=1, labels='Control Exp')
		 #--> Map Exp to 0 or 1
			filterPeptDF.iloc[:,range(4, 4+self.nExp,1)] = filterPeptDF.iloc[:,range(4, 4+self.nExp,1)].apply(self.TarProt2FiltPeptHelper, axis=0, raw=True)
		 #--> Write to file
			dmethods.FFsWriteCSV(str(fileO), filterPeptDF)
	 	 #--> Return
			return True	
	 #--> If not, show error msg & Return	
		else:
		 #--> Error msg
			gclasses.DlgFatalErrorMsg(config.msg['FiltPept'])
		 #--> Return
			return False
	#---

	def TarProt2FiltPeptHelper(self, col):
		""" Helper to TarProt2FiltPept method. Turns the value in an Exp into 
			0 or 1
			---
			col: column from a data frame
		"""
	 #--> List with modified values
		nV = []
	 #--> Add modified values to list
		for i in col:
			nV.append(i[0][0])
	 #--> Return
		return nV
	#---

	##--> cutprop file
	def TarProt2CutProp(self, fileO=None):
		""" Writes a cutprop file based on the tarprot file. 
			If fileO is None returns the dataframe instead of writing to disk  
		"""
	  #--> Check that there is something to write
		if self.checkFP:
			pass
		else:
			gclasses.DlgFatalErrorMsg(config.msg['FiltPept'])
			return False
	  #--- Variables
		u, d, t, c = self.pRes
		colHeader = dmethods.ListColHeaderCutPropFile(self.nExp)[0]
	  #--- Create the empty data frame with 0 in Exp and Totals
		rows = []
		colHeaderLen = len(colHeader)
		for i in range(1, c+1):
			row = [0] * colHeaderLen
			row[0] = i
			if d is not None and t is not None:
				if i < d:
					row[1] = None
				elif i >= d and i <= t:
					row[1] = i + self.Fdata['CI']['mist']
				elif i > t and i <= c:
					row[1] = None
				else:
					return False
			else:
				row[1] = None
			rows.append(row)
		cutpropDF = pd.DataFrame(rows, columns=colHeader)
	  #--- Count the cleavages for each experiment
		for i in range(1, self.nExp+1, 1):
			NC = self.FiltPeptDFForOneExp(i)
			self.TarProt2CutPropHelper(NC, cutpropDF, i)
	  #--- Fill FP columns
		i += 1
		self.TarProt2CutPropHelper(self.filterPeptDF, cutpropDF, i)	
	  #--- Write to file or return cutpropDF
		if fileO is None:
			return cutpropDF
		else:
			data = {
				'V' : config.dictVersion, 
				'CI' : {
					'nExp'       : self.nExp,
					'pRes'       : self.pRes,
					'mist'       : self.Fdata['CI']['mist'],
					'pLength'    : self.Fdata['CI']['protSeqLength'],
					'natProtPres': self.natProtPres
					},
				'R' : cutpropDF.to_dict()				
			}
			dmethods.FFsWriteJSON(fileO, data)
			return True
	#---
	
	#--> 
	def TarProt2CutPropHelper(self, dfi, dfo, i):
		""" Helper to TarProt2 
			---
			dfi: dataframe with the data (DF)
			dfo: dataframe with the output (DF)
			i: number of experiment (int)
		"""
	  #--> Get the cleavages
		dft = pd.DataFrame(dfi['Nterm'].copy())
		dft.loc[:,'Nterm'] = dft['Nterm'] - 1
		l = list(dft['Nterm'].values) + list(dfi['Cterm'].values)
		dft = pd.DataFrame(l, columns=['Merge'])
		count = dft['Merge'].value_counts().to_dict()	
		tindcp = dmethods.CalCutpropInd(i)
	  #--> Assign the values
		#---# Improve (Down) 
		for k in count:
			row = int(k - 1)
			dfo.iat[row, tindcp] = count[k]
		#---# Improve (UP)
		tindcpu = tindcp + 1
		dfo.iloc[:,tindcpu] = dmethods.DataNormDFCol(
			dfo.iloc[:,tindcp])
		tindcpd = tindcp + 2
	  #--> The same for the native sequence
		if self.natProtPres:
			dfo.iloc[:,tindcpd] = dfo.apply(
			  lambda row: None if np.isnan(row[1]) else row[tindcp], axis=1)
		else:
			dfo.iloc[:,tindcpd] = np.nan
	  #--> Normalize values				
		tindcpt = tindcp + 3
		dfo.iloc[:,tindcpt] = dmethods.DataNormDFCol(
			dfo.iloc[:,tindcpd])
	 #--> Return	
		return True
	#---

	##--> aadist file
	def TarProt2AAdist(self, fileO, posI=None):
		""" Creates the aadist file 
			---
			fileO: path to the aadist file (string or Path)
			posI : number of positions to consider (int)
		"""
	  #--> Check that there is indeed something to write
		if self.checkFP:
			pass
		else:
			gclasses.DlgFatalErrorMsg(config.msg['FiltPept'])
			return False			
	  #--> Variables
		if posI == None:
			pos = self.Fdata['CI']['Positions']
		else:
			pos = posI
		aVal   = self.Fdata['CI']['aVal'] 
		aaL    = dmethods.ListAddExtraAA(self.recSeq)
	  #--> Fill the dicts
		aadist = {}
	   #--> Exp
		for i in range(1, self.nExp+1, 1):
			label = 'Exp' + str(i)
			fpDF = self.FiltPeptDFForOneExp(i)
			out = self.AAdistDict(fpDF, pos, aaL)
			if out[0]:
				aadist[label] = out[1]
			else:
				return False
		out = self.AAdistDict(self.filterPeptDF, pos, aaL)
	   #--> FP
		if out[0]:
			aadist[config.aadist['FP']] = out[1]
		else:
			return False
	   #--> RD
		out = self.AAdistDictRD(pos, aaL)
		if out[0]:
			aadist[config.aadist['RD']] = out[1]
		else:
			return False
	  #--> Stats chi comp
		for k in aadist:
			if k != config.aadist['RD']:
				aadist[k]['Pos'] = self.AAdistDictChiComp(aadist[k], 
					aadist[config.aadist['RD']], aVal)
			else:
				aadist[k]['Pos'] = [0] * 2 * pos
	  #--> data
		data = {
			'V' : config.dictVersion, 
			'CI' : {
				'nExp'      : self.nExp,
				'aVal'      : self.Fdata['CI']['aVal'], 
				'Positions' : pos,
				'RecSeq'    : self.Fdata['CI']['RecSeq']
				},
			'R' : aadist			
		}
	  #--> Write to file & Return
		dmethods.FFsWriteJSON(fileO, data)
		return True
	#---

	#-->
	def AAdistDict(self, fpDF, pos, aaL):
		""" Creates the dict for a given experiment or the entire FP list 
			---
			fpDF: filtered peptide data frame for a given experiment (DF)
			pos: number of positions to consider (int)
			aaL: list of one letter aa code to considerer (list)
		"""
	  #--> Create empty output dict
		oDict = dmethods.DictStartAAdist(pos, aaL)
	  #--> Fill the out dict
		for row in fpDF.itertuples(index=False):
			resl = []
			resl.append(row[0] - 1)
			resl.append(row[1])
			for r in resl:
				if r > 0 and r < self.pRes[3]:
					i = r - 1 # Require for StringCharForAAdist
					seq = dmethods.StringCharForAAdist(self.recSeq, i, pos, 
						fill=config.aadist['FillChar'])
					oDict = dmethods.DictUpdateAAdist(oDict, seq)
				else:	
					pass
	  #--> Return	
		return [True, oDict]
	#---

	#-->
	def AAdistDictRD(self, pos, aaL):
		""" Creates the dict for a totally unspecific protease 
			---
			pos: number of positions to consider (int)
			aaL: one letter aa to consider (list)
		"""
	  #--> Create output dict
		oDict = dmethods.DictStartAAdist(pos, aaL)
	  #--> Fill it
		for r in range(1, self.pRes[3]+1, 1):
			if r > 0 and r < self.pRes[3]:
				i = r - 1 # Require for StringCharForAAdist
				seq = dmethods.StringCharForAAdist(self.recSeq, i, pos, 
					fill=config.aadist['FillChar'])
				oDict = dmethods.DictUpdateAAdist(oDict, seq)
			else:
				pass
	  #--> Return
		return [True, oDict]
	#---

	#-->
	def AAdistDictChiComp(self, oDict, eDict, aVal):
		""" Make a chi square test between the observed and expected dict. 
			Returns the list with the result code for each position 
			---
			oDict: dict with the observations (dict)
			eDict: expected values (dict)
			aVal: alpha level (float <= 1)"""
	 #--> Positions list
		PosCol = []
	 #--> Calculate chi for each position in the dict
		for i in range(0, len(oDict['A'])):
	  #--> Merge AA by AA type
			lO = []
			lE = []
			for g in config.aaGroups:
				sO = 0
				sE = 0
				for e in g:
					sO += oDict[e][i]
					sE += eDict[e][i]
				lO.append(sO)
				lE.append(sE)
	  #--> Calculate chi
			PosCol.append(dmethods.StatChiSquare(lO, lE, aVal))
	 #--> Return
		return PosCol
	#---

	##--> short data files. General name needed for this method
	def ToSDataFile(self, folderO, colOut=None, dataF=None):
		""" Writes the short data files 
			---
			folderO: folder to write the output files (string or Path)
			colOut: columns to extract (list of int)
			dataF : path to the data file if None read from tarprot
		"""
	  #--- Locate and read the dataF
		if dataF is None:
			tdataF = Path(self.Fdata['CI']['Datafile'])
			if check.CheckFileRead(tdataF):
				pass
			else:
				msg = config.dictCheckFatalErrorMsg[self.name]['Datafile']
				gclasses.DlgFatalErrorMsg(msg)
				return False
		else:
			tdataF = dataF
	  #--> Set columns to extract
		if colOut == None:
			selCol = self.Fdata['CI']['ColExtract']
		else:
			selCol = colOut	
		dataObj = DataObjDataFile(tdataF)
	  #--> Variables, here because the colHeader need the data object
		targetProtN = self.Fdata['CI']['Targetprotein']
		targetProtC = self.Fdata['CI']['DetectProtCol']
		scoreV      = self.Fdata['CI']['Scorevalue']
		scoreC      = self.Fdata['CI']['ScoreCol']		
		colHeaderD = dataObj.header
		typeV = {colHeaderD[scoreC]:'float'}
		seqColDN = colHeaderD[self.Fdata['CI']['SeqCol']]
		seqColTN = self.colHeader[config.tarprot['SeqColInd']]
	  #--> Create folderO
		try:
			folderO.mkdir()
		except Exception:
			pass
	  #--> all-columns-all-prot-records
		dataF = dmethods.DFColValFilter(dataObj.dataFrame,
			targetProtN, targetProtC)[1]
		name = 'all-columns-all-' + targetProtN + '-records.txt'
		file = folderO / name
		dmethods.FFsWriteCSV(file, dataF)
	  #--> selected-columns-all-prot-records
		dataFS = dmethods.DFSelCol(dataF, selCol)[1]
		name = 'selected-columns-all-' + targetProtN + '-records.txt'
		file = folderO / name
		dmethods.FFsWriteCSV(file, dataFS)
	  #--> selected-columns-relevant-prot-records
		dataFSR = dataF.astype(typeV)
		dataFSR = dataFSR.loc[dataFSR.iloc[:,scoreC] >= scoreV]
		dataFSR = dmethods.DFSelCol(dataFSR, selCol)[1]
		name = 'selected-columns-relevant-' + targetProtN + '-records.txt'
		file = folderO / name
		dmethods.FFsWriteCSV(file, dataFSR)
	  #--> selected-columns-FP-prot-records
		name = 'selected-columns-FP-' + targetProtN + '-records.txt'
		file = folderO / name
		if self.checkFP:
			dataFSF = dataF[dataF[seqColDN].isin(self.filterPeptDF[seqColTN])]
			dataFSF = dmethods.DFSelCol(dataFSF, selCol)[1] 
			dmethods.FFsWriteCSV(file, dataFSF)
		else:
			fileO = open(file, 'w')
			fileO.write(config.dictCheckFatalErrorMsg[self.name]['FiltPept2'])
			fileO.close()
	  #--> Return
		return True
	#---

	##--> histogram file
	def TarProt2HistoFile(self, fileO, win=None):
		""" Creates the histogram file 
			--- 
			fileO: path to the output file (string or Path)
			win: residue numbers forming the windows (list of int)
		"""
	  #--> Check that there is something to write first
		if self.checkFP:
			pass
		else:
			gclasses.DlgFatalErrorMsg(config.msg['FiltPept'])
			return False	
	  #--- Variables
		natLength = self.pLength[1]
		if win is None:
			twin = self.Fdata['CI']['Histogramwindows']
		else:
			twin = win
		if len(twin) > 1:
			histowinRec = twin
			if self.natProtPres:
				histowinNat = twin
			else:
				histowinNat = None 
		else:
			width = twin[0]
			histowinRec = dmethods.ListHistWin(width, self.pRes[3])
			if self.natProtPres:
				histowinNat = dmethods.ListHistWin(width, natLength)
			else:
				histowinNat = None				
	  #--- Create histograms
	   #--> FP and creates the dataframe for output
		labelI = [('Nterm', 'Cterm'), ('Fixed Nterm', 'Fixed Cterm')]
		binI = [histowinRec, histowinNat]
		lFP = self.TarProt2HistoFileHelper(self.filterPeptDF, labelI, binI)
		#---# Improve (Down)
			## Update win last interval for pretty print
		#---# Improve (Up)
		d = {'Windows': lFP[0], 'FP': lFP[1]}
		histoRecAll = pd.DataFrame(data=d)
		d = {'Windows': lFP[0], 'FP': lFP[2]}
		histoRecUni = pd.DataFrame(data=d)
		if self.natProtPres:
			d = {'Windows': lFP[3], 'FP': lFP[4]}
			histoNatAll = pd.DataFrame(data=d)
			d = {'Windows': lFP[3], 'FP': lFP[5]}
			histoNatUni = pd.DataFrame(data=d)		
		else:
			pass
	   #--> Exp
		for i in range(1, self.nExp+1, 1):
			df = self.FiltPeptDFForOneExp(i)
			l = self.TarProt2HistoFileHelper(df, labelI, binI)
			n = 'Exp' + str(i)
			histoRecAll[n] = l[1]
			histoRecUni[n] = l[2]
			if self.natProtPres:
				histoNatAll[n] = l[4]
				histoNatUni[n] = l[5]				
			else:
				pass
	  #--- Writeoutput
		histoRecAll.iloc[:,0] = histoRecAll.iloc[:,0].astype(str)
		histoRecUni.iloc[:,0] = histoRecUni.iloc[:,0].astype(str)
		results = {
			config.hist['DictKeys'][0] : histoRecAll.to_dict(),
			config.hist['DictKeys'][1] : histoRecUni.to_dict()
		}
		if self.natProtPres:
			histoNatAll.iloc[:,0] = histoNatAll.iloc[:,0].astype(str)
			histoNatUni.iloc[:,0] = histoNatUni.iloc[:,0].astype(str)
			results[config.hist['DictKeys'][2]] = histoNatAll.to_dict()
			results[config.hist['DictKeys'][3]] = histoNatUni.to_dict()
		else:
			results[config.hist['DictKeys'][2]] = None
			results[config.hist['DictKeys'][3]] = None
		data = {
			'V' : config.dictVersion,
			'CI' : {
				'nExp' : self.nExp
			}, 
			'R' : results			
		}
		dmethods.FFsWriteJSON(fileO, data)
	  #--> Return
		return True
	#---

	#-->
	def TarProt2HistoFileHelper(self, df, labelI, binI):
		""" Return a list of list with the histogram counts for all and for 
			unique cleavage sites. 
			---
			df: is the dataframe (DF)
			labelI: is a list of tuple with the two columns to be used for Rec and Nat. 
			binI: limits of the bin for the histograms (list of tuples)
		"""
	  #--> Variables
		label = labelI[0]
		binL  = binI[0]
		NCall = pd.DataFrame(df[label[0]].copy())
	  #--> Rec Prot
		NCall[label[0]] = NCall[label[0]] - 1
		l       = list(NCall[label[0]].values) + list(df[label[1]].values)
		NCall   = pd.DataFrame(l, columns=['Merge'])
		a       = pd.cut(NCall['Merge'], binL).value_counts(sort=False)
		winRec  = a.index.values.tolist()
		lrecAll = a.tolist()
		NCall.drop_duplicates(keep='first', inplace=True)
		lrecUni = pd.cut(NCall['Merge'], binL).value_counts(sort=False).tolist()
	  #--> Nat Prot
		if self.pLength[1] is None:
			lnatAll = None
			lnatUni = None
			winNat = None
		else:
			label = labelI[1]
			binL = binI[1]
			NCall = pd.DataFrame(df[label[0]].copy())
			NCall[label[0]] = NCall[label[0]] - 1
			l = list(NCall[label[0]].values) + list(df[label[1]].values)
			NCall = pd.DataFrame(l, columns=['Merge'])
			a = pd.cut(NCall['Merge'], binL).value_counts(sort=False)
			winNat = a.index.values.tolist()
			lnatAll = a.tolist()
			NCall.drop_duplicates(keep='first', inplace=True)
			lnatUni = pd.cut(NCall['Merge'], binL).value_counts(sort=False).tolist()
	  #--> Return
		return [winRec, lrecAll, lrecUni, winNat, lnatAll, lnatUni]
	#---

	##-- sequence alignment file
	def TarProt2SeqAlign(self, folderO, resN=None):
		""" Creates the sequence alignment files 
			---
			folderO: path to the output folder (string or Path)
			resN: number of residue per line (int)
		"""
	  #--> Check that there is anythin to write
		if self.checkFP:
			pass
		else:
			gclasses.DlgFatalErrorMsg(config.msg['FiltPept'])
			return False	
	  #--> Variables
		if resN == None:
			N = self.Fdata['CI']['Sequencelength']
		else:
			N = resN
	  #--> Folder
		try:
			folderO.mkdir()
		except Exception:
			pass
	  #--> Files
		file = folderO / 'FP-rec.txt'
		self.TarProt2SeqAlignHelper(file, self.filterPeptDF, self.recSeq, N)
		file = folderO / 'FP-nat.txt'
		if self.natProtPres:
			df = self.filterPeptDF.dropna()
			self.TarProt2SeqAlignHelper(file, df, self.recSeq, N)			
		else:
			fileO = open(file, 'w')
			fileO.write(config.dictCheckFatalErrorMsg[self.name]['NoNatSeq'])
			fileO.close()
		for i in range(1, self.nExp+1, 1):
			name = 'Exp' + str(i) + '-rec.txt'
			file = folderO / name
			df = self.FiltPeptDFForOneExp(i)
			self.TarProt2SeqAlignHelper(file, df, self.recSeq, N)
			name = 'Exp' + str(i) + '-nat.txt'
			file = folderO / name
			df = df.dropna()
			self.TarProt2SeqAlignHelper(file, df, self.recSeq, N)
	  #--> Return
		return True
	#---

	#-->
	def TarProt2SeqAlignHelper(self, file, df, seq, L=None):
		""" Creates a sequence alignment between seq and all peptides in df, If
			L is an integer creates also the file with L character per line. 
			---
			file: is the path to the output file (string or Path)
			df: data frame with the filtered peptides (DF)
			seq: sequence of the protein (string)
			L: residue number per line (None or int)
		"""
	  #--> Variables
		longL = []
		longL.append(seq)
	  #--> Create long file
		for row in df.itertuples(index=False):
			l = [' '] * int(row[0] - 1)
			l.append(row[-2])
			s = ''.join(l)
			longL.append(s)
		fileO = open(file, 'w')
		[fileO.write(x + '\n') for x in longL]
		fileO.close()
	  #--> Short File
		if L is None:
			pass
		else:
			shortL = []
			for line in longL:
				lt = []
				for i in range(0, len(line), L):
					lt.append(line[i:i+L])
				shortL.append(lt)
			name = str(str(file.name).split('.')[0]) + '-' + str(L) + '.txt'
			file = file.with_name(name)
			fileO = open(file, 'w')
			for i in range(0, len(shortL[0]), 1):
				ln = 0
				for e in shortL:
					ln += 1
					lno = '{:>3}'.format(ln)
					try:
						ee = e[i]
						s = ee.strip()
						if s != '':
							fileO.write(lno + ' ' + ee + '\n')
						else:
							pass	
					except Exception as e:
						pass
				fileO.write('\n')
			fileO.close()
	  #--> Return
		return True
	#---

	##-- pdb files
	def TarProt2PDB(self, folderO, pdbObj=None, recSeqObj=None, 
		stProgress=None):
		""" Creates the pdb files 
			---
			folderO: path to the output folder (string or Path)
			pdbObj: None or pdbObj
			recSeqObj: None or SeqObj
			stProgress: None or stProgress in the GUI
			"""
	  #--> Check that there is something to write
		if self.checkFP:
			pass
		else:
			gclasses.DlgFatalErrorMsg(config.msg['FiltPept'])
			return False	
	  #--- Variables
	   #--> seq object
		if recSeqObj is None:
			recSeqObj = DataObjSequenceFile(seqP=None, seqM=self.recSeq)
		else:
			pass
	   #--> pdb object
		if pdbObj is None:
			pdbObj = DataObjPDBFile(self.Fdata['CI']['PDBfile'],
				self.Fdata['CI']['PDBID'][0],
				self.Fdata['CI']['PDBID'][1])
		else:
			pass
		try:
			pdbObj.atomDF
		except Exception:
			pdbObj.SetatomDF()
		pdbProtSeqResNumDF = pdbObj.GetProtSeqResNumDF(pdbObj.cs, three=False)[1]
	   #--> cuts
		#---# Improvement (DOWN) Could be taken from the window calling
		cutpropDF = self.TarProt2CutProp()
		#---# Improvement (UP)
	  #--> Align recSeq and pdbSeq and ResNumber mapping
		pdbDF = recSeqObj.GetresNumMatch(pdbProtSeqResNumDF)
	  #--> folderO
		try:
			folderO.mkdir()
		except Exception:
			pass
	  #--> Write files
		count = 1
		total = 1 + self.nExp
	   #--> FP		
		indC  = [-4, -3, -2, -1]
		label = 'FP-cleavages-'
		self.TarProt2PDBHelper(count, total, pdbDF, cutpropDF, indC, folderO,
			label, pdbObj, self.Fdata['CI']['PDBID'][1], stProgress)
	   #--> Exp
		for i in range(1, self.nExp+1, 1):
			count += 1
			#---
			s = ((config.cutprop['DistBetExp'] * i) 
				- config.cutprop['NColExpStart'])		
			indC  = list(range(s, s+4, 1))
			label = 'Exp' + str(i) + '-'
			#---
			self.TarProt2PDBHelper(count, total, pdbDF, cutpropDF, indC, 
				folderO, label, pdbObj, self.Fdata['CI']['PDBID'][1],
				stProgress)
	  #--> Return
		return True
	#---

	def TarProt2PDBHelper(self, count, total, pdbDF, cutpropDF, indC, folderO,
		label, pdbObj, cs, stProgress=None):
		""" Updates stProgress and invokes other helpers 
			---
			count: current number of pdb being generated (int)
			total: total number to be generated (int) 
			pdbDF: 
			cutpropDF:
			indC:
			folderO
			label:
			pdbObj,
			cs,
			stProgress
		"""
		if stProgress is None:
			pass
		else:
			msg = ("Writing output files: pdb files (" + str(count) + "/" 
				+ str(total) + ")")   
			wx.CallAfter(gmethods.UpdateText, stProgress, msg)	
		#---
		self.TarProt2PDBHelper2(pdbDF, cutpropDF, indC)
		self.TarProt2PDBHelper3(folderO, label, pdbDF, pdbObj, cs)
		return True
	#---

	def TarProt2PDBHelper2(self, pdbDF, cutDF, indC):
		""" Helper to TarProt2PDB. Basically search cutpropDF to get the cuts
			in indC for every residue in pdbDF. 
			---
			pdbDF
			cutDF
			indC is a list with four number to get BetaR, BetaRNorm, BetaN, BetaNNorm in one go. 
		"""
	  #--- Variables
		cutsR = []
		cutsRNorm = []
		cutsN = []
		cutsNNorm = []
	  #--- 
		for row in pdbDF.itertuples(index=False):
			try:
				a = cutDF.loc[cutDF.iloc[:,0] == row.ResMatch].index.item()
				cutsR.append(cutDF.iat[a, indC[0]])
				cutsRNorm.append(cutDF.iat[a, indC[1]])
				cutsN.append(cutDF.iat[a, indC[2]])
				cutsNNorm.append(cutDF.iat[a, indC[3]]) 
			except Exception:
				cutsR.append(0.00)
				cutsRNorm.append(0.00)
				cutsN.append(0.00)
				cutsNNorm.append(0.00) 
	  #---
		pdbDF.loc[:,'BetaR'] = cutsR
		pdbDF.loc[:,'BetaRNorm'] = cutsRNorm
		pdbDF.loc[:,'BetaN'] = cutsN
		pdbDF.loc[:,'BetaNNorm'] = cutsNNorm
	  #---
		return pdbDF
	#---

	def TarProt2PDBHelper3(self, folderO, label, pdbDF, pdbObj, cs):
		""" Prepares the atomDFcs to be writen to disk
			---
			folderO:
			label:
			pdbDF:
			pdbObj:
			cs:
		"""
	  #--- Variables
		df = pdbObj.GetatomDFcs(cs).copy()[1]
		df2w = df.copy()
	  #---
		betaR     = []
		betaRNorm = []
		betaN     = []
		betaNNorm = []
		for row in df.itertuples(index=False):
			try:
				a = pdbDF.loc[pdbDF.iloc[:,-6] == int(row.ResNum)].index.item()
				if row.ResName in config.aaList3:
					betaR.append(pdbDF.iat[a, -4])    
					betaRNorm.append(pdbDF.iat[a, -3])    
					betaN.append(pdbDF.iat[a, -2])        
					betaNNorm.append(pdbDF.iat[a, -1])    
				else:
					betaR.append(0.00)    
					betaRNorm.append(0.00)
					betaN.append(0.00)
					betaNNorm.append(0.00)
			except Exception:
				betaR.append(0.00)    
				betaRNorm.append(0.00)
				betaN.append(0.00)
				betaNNorm.append(0.00)
	  #---
		df.loc[:,'betaR'] = betaR
		df.loc[:,'betaRNorm'] = betaRNorm
		df.loc[:,'betaN'] = betaN
		df.loc[:,'betaNNorm'] = betaNNorm
	  #---
		df2w.loc[:,'beta'] = df['betaR']
		name = label + 'rec.pdb'
		file = folderO / name
		pdbObj.WritePDB(file, df2w)
		df2w.loc[:,'beta'] = df['betaRNorm']
		name = label + 'rec-norm.pdb'
		file = folderO / name
		pdbObj.WritePDB(file, df2w)
		if self.natProtPres:
			df2w.loc[:,'beta'] = df['betaN']
			name = label + 'nat.pdb'
			file = folderO / name
			pdbObj.WritePDB(file, df2w)
			df2w.loc[:,'beta'] = df['betaNNorm']
			name = label + 'nat-norm.pdb'
			file = folderO / name
			pdbObj.WritePDB(file, df2w)
		else:
			pass
	  #--- 
		return True
	#---

	def TarProtUpdate(self, folderO):
		""" Update the results (format of the output files) in tarprot file 
			---
			folderO: folder to write the output file 
		"""
	  #--> Check that there are FPs in the file
		if self.checkFP:
			pass
		else:
			gclasses.DlgFatalErrorMsg(config.msg['Errors']['FiltPept'])
			return False
	  #--> Check folderO
		folderOF = folderO / 'TarProt-Update'
		if folderOF.is_dir():
			dateN = dmethods.DateTimeNow()
			Fname = 'Tarprot-Update' + dateN
			folderOF = folderO / Fname
		else:
			pass
	  #--> Variables
		pathP = folderOF / self.fileP.name
	  #--> FolderO
		folderOF.mkdir()
	  #--> uscr
		pathP = pathP.with_suffix('.uscr')
		dmethods.FFsWriteDict2Uscr(
			pathP,
			iDict=self.Fdata['I'],
			hDict=config.dictUserInput2UscrFile[config.name['TarProt']]
		)
	  #--> filtlist
		pathP = pathP.with_suffix('.filtpept')
		self.TarProt2FiltPept(pathP)
	  #--> cutprop
		pathP = pathP.with_suffix('.cutprop')
		self.TarProt2CutProp(pathP)
	  #--> aadist
		try:
			aapos = int(self.Fdata['I']["Positions"])
			pathP = pathP.with_suffix('.aadist')
			self.TarProt2AAdist(pathP, aapos)
		except Exception:
			pass
	  #--> Hist
		pathP = pathP.with_suffix('.hist')
		try:
			win = self.Fdata['CI']["Histogramwindows"]
			if win != None:
				self.TarProt2HistoFile(pathP, win=win)
			else:
				pass
		except Exception:
			pass			
	  #--> Seq
		pathP = pathP.parent / 'Sequences'
		try:
			seqL = int(self.Fdata['I']["Sequencelength"])
			self.TarProt2SeqAlign(pathP, resN=seqL)
		except Exception:
			pass
	  #--> data
		colExt = self.Fdata['CI']["ColExtract"]
		dataI = Path(self.Fdata['CI']['Datafile'])
		if colExt != None and dataI.is_file(): 
			pathP = pathP.parent / 'Data'
			try:
				self.TarProt2SDataFile(pathP, colOut=colExt, dataF=dataI)
			except Exception:
				pass
		else:
			pass
	  #--> PDB
		code, cs = self.Fdata['CI']["PDBID"]
		if cs != None:
			#---
			pathP = pathP.parent / 'PDB'
			#---
			pdbFile = self.Fdata['CI']['PDBfile']
			#---
			pdbObj = DataObjPDBFile(pdbFile, code, cs)	
			#---
			self.TarProt2PDB(pathP, pdbObj=pdbObj)
		else:
			pass
	  #--> Copy old file to TarProtUpdate
		name = str(self.fileP.stem) + '_old.tarprot'
		fileO = pathP.parent / name
		fileO.write_text(self.fileP.read_text())
	  #--> Return
		return True
	#---
#---
# ----------------------------------------------- Files generated by UMSAP (END)