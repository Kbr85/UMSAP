# ------------------------------------------------------------------------------
# Copyright (C) 2017 Kenny Bravo Rodriguez <www.umsap.nl>
#
# Author: Kenny Bravo Rodriguez (kenny.bravorodriguez@mpi-dortmund.mpg.de)
#
# This program is distributed for free in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See the accompanying license for more details.
# ------------------------------------------------------------------------------


"""Classes and methods to manipulate data """


#region -------------------------------------------------------------> Imports
# import itertools
import traceback
from datetime import datetime
from pathlib import Path
from typing import Union

# import pandas as pd
# import numpy as np

import wx

# from reportlab.lib.pagesizes import A4
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

import config.config as mConfig
import data.file as mFile
import data.exception as mException
#endregion ----------------------------------------------------------> Imports


#region ------------------------------------------------------> String methods
def StrException(
    tException: Exception, tStr: bool=True, tRepr: bool=True, trace: bool=True
    ) -> str:
    """Get a string to print information about tException

        Parameters
        ----------
        tException: Exception
            Exception to print
        tStr : boolean
            Include error message as return by str(tException). Default is True.
        tRepr : boolean
            Include error message as return by repr(tException). 
            Default is True.
        trace : boolean
            Include the traceback. Default is True.

        Returns
        -------
        str
            Error message
    """
    # No test
    #region -------------------------------------------------------> Variables
    msg = ''
    #endregion ----------------------------------------------------> Variables
    
    #region ---------------------------------------------------------> Message
    #------------------------------> str(e)
    if tStr:
        msg = f"{msg}{str(tException)}\n\n"
    else:
        pass
    #------------------------------> repr(e)
    if tRepr:
        msg = f"{msg}{repr(tException)}\n\n"
    else:
        pass
    #------------------------------> traceback
    if trace:
        tTrace = "".join(
            traceback.format_exception(
                type(tException),
                tException,
                tException.__traceback__,
            )
        )
        msg = f"{msg}{tTrace}"
    else:
        pass	
    #endregion ------------------------------------------------------> Message
    
    return msg 
#---


def StrNow(dtFormat: str=mConfig.dtFormat) -> str:
    """Get a formatted datetime.now() string.

        Returns
        -------
        str:
            The now date time as 20210112-140137.
    """
    return datetime.now().strftime(dtFormat)
#---
#endregion ---------------------------------------------------> String methods


#region ------------------------------------------------------> Number methods
def ExpandRange(
    r: str, numType: mConfig.litNumType='int'
    ) -> Union[list[int], list[float]]:
    """Expand a range of numbers: '4-7' --> [4,5,6,7]. Only positive integers 
        are supported.

        Parameters
        ----------
        r : str
            String containing the range
        numType : str
            One of 'int', 'float'. For the case where r is not a range

        Returns
        -------
        list of int

        Examples
        --------
        >>> ExpandRange('0-15', 'int')
        >>> [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        >>> ExpandRange('-5.4', 'float')
        >>> [-5.4]
    """
    #region -------------------------------------------------> Expand & Return
    #------------------------------> Remove flanking empty characters
    tr = r.strip()
    #------------------------------> Expand
    if '-' in tr:
        #------------------------------> Range
        #--------------> Catch more than one - in range
        try:
            a,b = tr.split('-')
        except ValueError:
            raise mException.InputError(mConfig.mRangeNumIE.format(r))
        #-------------->  Check a value
        if a == '':
            #--> Negative number
            try:
                return [mConfig.oNumType[numType](tr)]
            except ValueError:
                raise mException.InputError(mConfig.mRangeNumIE.format(r))
        else:
            pass
        #-------------->  Check b
        if b == '':
            #--> range like 4-
            raise mException.InputError(mConfig.mRangeNumIE.format(r))
        else:
            pass
        #--------------> Expand range
        #--> Convert to int
        try:
            a = int(a)
            b = int(b)
        except ValueError:
            raise mException.InputError(mConfig.mRangeNumIE.format(r))
        #--> Expand range
        if a < b:
            return [x for x in range(a, b+1, 1)]
        else:
            raise mException.InputError(mConfig.mRangeNumIE.format(r))
    else:
        #------------------------------> Positive number
        try:
            return [mConfig.oNumType[numType](tr)]
        except ValueError:
            raise mException.InputError(mConfig.mRangeNumIE.format(r))
    #endregion ----------------------------------------------> Expand & Return
#---
#endregion ---------------------------------------------------> Number methods


#region ---------------------------------------------------------> wx.ListCtrl
def LCtrlFillColNames(lc: wx.ListCtrl, fileP: Union[Path, str]) -> bool:
    """Fill the wx.ListCtrl with the name of the columns in fileP.

        Parameters
        ----------
        lc : wx.ListCtrl
            wx.ListCtrl to fill info into
        fileP : Path
            Path to the file from which to read the column names

        Notes
        -----
        This will delete the wx.ListCtrl before adding the new names.
        wx.ListCtrl is assumed to have at least two columns [#, Name,]
    """
    #region -------------------------------------------------------> Read file
    try:
        colNames = mFile.ReadFileFirstLine(fileP)
    except Exception as e:
        raise e
    #endregion ----------------------------------------------------> Read file

    #region -------------------------------------------------------> Fill List
    try:
        #------------------------------> Del items
        lc.DeleteAllItems()
        #------------------------------> Fill
        for k, v in enumerate(colNames):
            index = lc.InsertItem(k, " " + str(k))
            lc.SetItem(index, 1, v)
    except Exception:
        msg = "It was not possible to fill the list."
        raise mException.ExecutionError(msg)
    #endregion ----------------------------------------------------> Fill List

    return True
#---
#endregion ------------------------------------------------------> wx.ListCtrl

#region -------------------------------------------------------------> Methods
# def ResControl2ListNumber(
#     val: str, sep: list[str]=[' ', ',', ';'], 
#     numType: Literal['int', 'float']='int',
#     ) -> list[list[list[int]]]:
#     """Return a list from a Result - Control string.
    
#         Parameters
#         ----------
#         val : str
#             String with the numbers. e.g. '0-4 6, 7 8 9; 10 13-15, ""; ...'
#         sep : list of str
#             Separators used in the string e.g. [' ', ',', ';']
#         numType: str
#             To convert to numbers

#         Returns
#         -------
#         list of list of list of str
#         [[[0 1 2 3 4], [7 8 9]], [[10 13 14 15], []], ...]   
        
#         Examples
#         --------
#         >>> ResControl2ListNumber('0 1 2, 3 4 5; 6 7 8, 9 10 11', sep=[' ', ',', ';'], numType='int')
#         >>> [[[0,1,2], [3,4,5]], [[6,7,8], [9,10,11]]]
#     """
#     # Test in test.unit.test_method.Test_ResControl2ListNumber
#     #region -------------------------------------------------------> Variables
#     l = []    
#     #endregion ----------------------------------------------------> Variables
    
#     #region -------------------------------------------------------> Form list
#     for k in val.split(sep[2]):
#         #------------------------------> 
#         lrow = []
#         #------------------------------> 
#         for j in k.split(sep[1]):
#             colVal = dtsMethod.Str2ListNumber(j, numType=numType, sep=sep[0])
#             lrow.append(colVal)
#         #------------------------------> 
#         l.append(lrow)
#     #endregion ----------------------------------------------------> Form list
    
#     return l
# #---


# def ResControl2Flat(val: list[list[list[int]]]) -> list[int]:
#     """Result - Control list as a flat list.

#         Parameters
#         ----------
#         val : list of list of list of int
#             Result - Control as a list of list of list of int

#         Returns
#         -------
#         list of int
#             Flat Result - Control list
            
#         Examples
#         --------
#         >>> ResControl2Flat([[[0,1,2], [3,4,5]], [[6,7,8], [9,10,11]]])
#         >>> [0,1,2,3,4,5,6,7,8,9,10,11])
#     """
#     # Test in test.unit.test_method.Test_ResControl2Flat
#     return list(itertools.chain(*(itertools.chain(*val))))
# #---


# def ResControl2DF(
#     val: list[list[list[int]]], start: int
#     ) -> list[list[list[int]]]:
#     """Convert the Result - Control column numbers in the original file to the
#         column numbers of the initial dataframe used in the analysis. 

#         Parameters
#         ----------
#         val : list of list of list of int
#             Result - Control as a list of list of list of int
#         start : int
#             Column index start of the Result - Control columns in the initial
#             dataframe 

#         Returns
#         -------
#         list[list[list[int]]]
#             The list has the same order as the input val but the column index
#             are adjusted.
            
#         Notes
#         -----
#         It is assumed columns in the DF have the same order as in val.
#         Empty list as possible to mimic empty conditions in an experiment.
        
#         Examples
#         --------
#         >>> ResControl2DF([[[0,1,2], []], [[6,7,8], []]], 1)
#         >>> [[[1,2,3],[]], [[4,5,6],[]]]
#     """
#     # Test in test.unit.test_method.Test_ResControl2DF
#     #region -------------------------------------------------------> Variables
#     idx  = start
#     outL = []
#     #endregion ----------------------------------------------------> Variables
    
#     #region --------------------------------------------------> Adjust col idx
#     for row in val:
#         #------------------------------> 
#         outR = []
#         #------------------------------> 
#         for col in row:
#             #------------------------------> 
#             outC = []
#             #------------------------------> 
#             if len(col) > 0:
#                 pass
#             else:
#                 outR.append([])
#                 continue
#             #------------------------------> 
#             for k in col:
#                 outC.append(idx)
#                 idx += 1
#             #------------------------------> 
#             outR.append(outC)
#         #------------------------------> 
#         outL.append(outR)    
#     #endregion -----------------------------------------------> Adjust col idx
    
#     return outL
# #---


# def Fragments(
#     df: 'pd.DataFrame', val: float, comp: Literal['lt', 'le', 'e', 'ge', 'gt'],
#     ) -> dict:
#     """Creates the dict holding the fragments identified in the analysis

#         Parameters
#         ----------
#         df: pd.DataFrame with the data from the analysis. The columns in df are
#             expected to be:
#             Seq Nrec Crec Nnat Cnat Exp1 Exp2 ...... ExpN
#         val : float
#             Threshold value to filter df and identify relevant peptides
#         comp : str
#             One of 'lt', 'le', 'e', 'ge', 'gt'

#         Returns
#         -------
#         dict:
#             {
#                 'Exp1' : {
#                     'Coord' : [(x1, x2),...., (xN, xM)],
#                     'CoordN': [(x1, x2),.(NaN, NaN)..., (xN, xM)]
#                     'Seq'   : [Aligned Seq1, ...., Aligned SeqN],
#                     'SeqL   : [Flat List with Seqs1, ...., Flat List with SeqsN],
#                     'Np'    : [Number of peptides1, ...., NpN],
#                     'NpNat  : [Number of native peptides1, ...., NpNatN],
#                     'Nc'    : [Number of cleavages1, ...., NcN],
#                     'NcNat' : [Number of native cleavages1, ....., NcNatN],
#                     'NFrag' : (Number of fragments, Number of fragments Nat),
#                     'NcT'   : (Number of cleavages for the Exp as a whole, 
#                                Number of cleavages for the Exp as a whole Nat),
#                 },
#                 'ExpN' : {},
#             }
#         - All list inside each Exp have the same length
#         - NFrag and NcT are tuples with two values each.
#         - Keys Exp1,...,ExpN are variables and depend on the module calling the
#         method.
#     """
#     # No Test
#     #region -------------------------------------------------------> Variables
#     dictO = {}
#     #endregion ----------------------------------------------------> Variables

#     #region --------------------------------------------------->
#     for c in range(5, df.shape[1]):
#         colK = str(df.columns.values[c])
#         #------------------------------> Prepare dictO
#         dictO[colK]           = {}
#         dictO[colK]['Coord']  = []
#         dictO[colK]['CoordN'] = []
#         dictO[colK]['Seq']    = []
#         dictO[colK]['SeqL']   = []
#         dictO[colK]['Np']     = []
#         dictO[colK]['NpNat']  = []
#         dictO[colK]['Nc']     = []
#         dictO[colK]['NcNat']  = []
#         #------------------------------> Filter df
#         dfE = dtsMethod.DFFilterByColN(df, [c], val, comp)
#         #------------------------------> 
#         n       = None
#         c       = None
#         seq     = None
#         seqL    = []
#         nP      = None
#         npNat   = None
#         ncL     = []
#         ncLNat  = []
#         nctL    = []
#         nctLNat = []
#         #------------------------------>    
#         for r in range(0, dfE.shape[0]):
#             if n is None:
#                 seq = dfE.iat[r,0]
#                 seqL.append(seq)
#                 nP = 1
#                 n  = dfE.iat[r,1]
#                 c  = dfE.iat[r,2]
#                 nf = dfE.iat[r,3]
#                 cf = dfE.iat[r,4]
#                 if np.isnan(nf) and np.isnan(cf):
#                     npNat = 0
#                 else:
#                     npNat = 1
#                 if np.isnan(nf):
#                     pass
#                 else:
#                     ncLNat.append(n-1)
#                     nctLNat.append(n-1)
#                 if np.isnan(cf):
#                     pass
#                 else:
#                     ncLNat.append(c)
#                     nctLNat.append(c)
#                 ncL.append(n-1)
#                 ncL.append(c)
#                 nctL.append(n-1)
#                 nctL.append(c)
#             else:
#                 nc   = dfE.iat[r,1]
#                 cc   = dfE.iat[r,2]
#                 ncf  = dfE.iat[r,3]
#                 ccf  = dfE.iat[r,4]
#                 seqc = dfE.iat[r,0]
#                 if nc <= c:
#                     seq = f'{seq}\n{(nc-n)*" "}{seqc}'
#                     seqL.append(seqc)
#                     nP = nP + 1
#                     if cc > c:
#                         c = cc
#                         cf = ccf
#                     else:
#                         pass
#                     if not np.isnan(ncf) and not np.isnan(ccf):
#                         npNat = npNat + 1
#                     else:
#                         pass
#                     if not np.isnan(ncf):
#                         ncLNat.append(nc-1)
#                         nctLNat.append(nc-1)
#                     else:
#                         pass
#                     if not np.isnan(ccf):
#                         ncLNat.append(cc)
#                         nctLNat.append(cc)
#                     else:
#                         pass
#                     ncL.append(nc-1)
#                     ncL.append(cc)
#                     nctL.append(nc-1)
#                     nctL.append(cc)
#                 else:
#                     dictO[colK]['Coord'].append((n,c))
#                     dictO[colK]['CoordN'].append((nf,cf))
#                     dictO[colK]['Seq'].append(seq)
#                     dictO[colK]['SeqL'].append(seqL)
#                     dictO[colK]['Np'].append(nP)
#                     dictO[colK]['NpNat'].append(npNat)
#                     dictO[colK]['Nc'].append(len(list(set(ncL))))
#                     dictO[colK]['NcNat'].append(len(list(set(ncLNat))))
#                     n    = nc
#                     c    = cc
#                     nf   = ncf
#                     cf   = ccf
#                     seq  = seqc
#                     seqL = [seqc]
#                     nP   = 1
#                     if not np.isnan(nf) and not np.isnan(cf):
#                         npNat = 1
#                     else:
#                         npNat = 0
#                     ncLNat = []
#                     if not np.isnan(nf):
#                         ncLNat.append(n-1)
#                         nctLNat.append(n-1)
#                     else:
#                         pass
#                     if not np.isnan(cf):
#                         ncLNat.append(c)
#                         nctLNat.append(c)
#                     else:
#                         pass
#                     ncL = []
#                     ncL.append(n-1)
#                     ncL.append(c)
#                     nctL.append(n-1)
#                     nctL.append(c)
#         #------------------------------> Catch the last line
#         if n is not None:
#             dictO[colK]['Coord'].append((n,c))
#             dictO[colK]['CoordN'].append((nf,cf))
#             dictO[colK]['Seq'].append(seq)
#             dictO[colK]['SeqL'].append(seqL)
#             dictO[colK]['Np'].append(nP)
#             dictO[colK]['NpNat'].append(npNat)
#             dictO[colK]['Nc'].append(len(list(set(ncL))))
#             dictO[colK]['NcNat'].append(len(list(set(ncLNat))))
            
#             dictO[colK]['NcT'] = [len(list(set(nctL))), len(list(set(nctLNat)))]
            
#             nFragN = [x for x in dictO[colK]['CoordN'] if not np.isnan(x[0]) or not np.isnan(x[1])]
#             dictO[colK]['NFrag'] = [len(dictO[colK]['Coord']), len(nFragN)]
#         else:
#             dictO[colK]['NcT'] = []
#             dictO[colK]['NFrag'] = []
#         #------------------------------> All detected peptides as a list
#     #endregion ------------------------------------------------>

#     return dictO
# #---


# def HCurve(x:float, t0:float, s0:float) -> float:
#     """Calculate the hyperbolic curve values according to:
#         doi: 10.1142/S0219720012310038

#         Parameters
#         ----------
        

#         Returns
#         -------
        

#         Raise
#         -----
        
#     """
#     #region ---------------------------------------------------> Calculate
#     return abs((abs(x)*t0)/(abs(x)-t0*s0))
#     #endregion ------------------------------------------------> Calculate
# #---


# def Rec2NatCoord(
#     coord: list[tuple[int,int]], protLoc:tuple[int,int], delta:int,
#     ) -> Union[list[tuple[int,int]], list[str]]:
#     """

#         Parameters
#         ----------
        

#         Returns
#         -------
        

#         Raise
#         -----
        
#     """
#     #region ---------------------------------------------------> Return NA
#     if delta == 0 or delta is None or protLoc[0] is None or protLoc[1] is None:
#         return ['NA']
#     else:
#         pass
#     #endregion ------------------------------------------------> Return NA

#     #region ---------------------------------------------------> Calc
#     listO = []
#     for a,b in coord:
#         if protLoc[0] <= a <= protLoc[1] and protLoc[0] <= b <= protLoc[1]:
#             listO.append((a+delta, b+delta))
#         else:
#             pass
#     #endregion ------------------------------------------------> Calc

#     return listO
# #---


# def R2AA(
#     df:pd.DataFrame, seq: str, alpha: float, protL: int, pos: int=5,
#     ) -> pd.DataFrame:
#     """AA distribution analysis

#         Parameters
#         ----------
#         df: pd.DataFrame
#             Sequence Label1 LabelN
#             Sequence P      P
#         seq: str
#             Recombinant protein sequence
#         alpha: float
#             Significance level
#         pos: int
#             Number of positions to consider
            
#         Returns
#         -------
#         pd.DataFrame
#             AA Label1       LabelN
#             AA -2 -1 1 2 P  -2 -1 1 2 P
#     """
#     print('AA NUMBER OF POSITIONS')
#     print(pos)
#     def AddNewAA(dfO, r, pos, seq, l):
#         """
    
#             Parameters
#             ----------
            
    
#             Returns
#             -------
            
    
#             Raise
#             -----
            
#         """
#         #region ---------------------------------------------------> 
#         if r >= pos:
#             col = pos
#             start = r - pos
#         else:
#             col = r
#             start = 0
#         #endregion ------------------------------------------------> 

#         #region ---------------------------------------------------> 
#         for a in seq[start:r]:
#             dfO.at[a,(l,f'P{col}')] = dfO.at[a,(l,f'P{col}')] + 1
#             col -= 1
#         col = 1
#         for a in seq[r:r+pos]:
#             dfO.at[a,(l,f"P{col}'")] = dfO.at[a,(l,f"P{col}'")] + 1
#             col += 1
#         #endregion ------------------------------------------------> 

#         return dfO
#     #---
#     #region ---------------------------------------------------> Empty
#     aL = ['AA']
#     bL = ['AA']
#     for l in df.columns.get_level_values(0)[1:]:
#         aL = aL + 2*pos*[l]
#         bL = bL + [f'P{x}' for x in range(pos, 0, -1)] + [f'P{x}\'' for x in range(1, pos+1,1)]
#     idx = pd.MultiIndex.from_arrays([aL[:],bL[:]])
#     dfO = pd.DataFrame(0, columns=idx, index=config.lAA1+['Chi'])
#     dfO[('AA','AA')] = config.lAA1[:]+['Chi']
#     #endregion ------------------------------------------------> Empty

#     #region ---------------------------------------------------> Fill
#     idx = pd.IndexSlice
#     for l in df.columns.get_level_values(0)[1:]:
#         seqDF = df[df[idx[l,'P']] < alpha].iloc[:,0].to_list()
#         for s in seqDF:
#             #------------------------------> 
#             n = seq.find(s)
#             if n > 0:
#                 dfO = AddNewAA(dfO, n, pos, seq, l)
#             else:
#                 pass
#             #------------------------------> 
#             c = n+len(s)
#             if c < protL:
#                 dfO = AddNewAA(dfO, c, pos, seq, l)
#             else:
#                 pass
#     #endregion ------------------------------------------------> Fill
    
#     #region ---------------------------------------------------> Random Cleavage
#     c = 'ALL_CLEAVAGES_UMSAP'
#     aL = 2*pos*[c]
#     bL = [f'P{x}' for x in range(pos, 0, -1)] + [f"P{x}'" for x in range(1, pos+1,1)]
#     idx = pd.MultiIndex.from_arrays([aL[:],bL[:]])
#     dfT = pd.DataFrame(0, columns=idx, index=config.lAA1+['Chi'])
#     dfO = pd.concat([dfO, dfT], axis=1)
#     for k,_ in enumerate(seq[1:-1], start=1): # Exclude first and last residue
#         dfO = AddNewAA(dfO, k, pos, seq, c)
#     #endregion ------------------------------------------------> Random Cleavage

#     #region ---------------------------------------------------> Group
#     idx = pd.IndexSlice
#     gS = []
#     for g in config.lAAGroups:
#         gS.append(dfO.loc[g,:].sum(axis=0))
#     g = pd.concat(gS, axis=1)
#     g = g.transpose()

#     for l in df.columns.get_level_values(0)[1:]:
#         for p in dfO.loc[:,idx[l,:]].columns.get_level_values(1):
#             dfO.at['Chi', idx[l,p]] = dtsStatistic.test_chi(
#                 g.loc[:,idx[[l,c],p]], alpha)[0]
#     #endregion ------------------------------------------------> Group

#     return dfO
# #---


# def R2Hist(
#     df: pd.DataFrame, alpha: float, win: list[int], maxL: list[int]
#     ) -> pd.DataFrame:
#     """

#         Parameters
#         ----------
#         df: pd.DataFrame
#             Nterm Cterm NtermF CtermF Exp1 .... ExpN
#             Nterm Cterm NtermF CtermF P    .... P
            
#         Returns
#         -------
#         pd.DataFrame
#     """
#     #region ---------------------------------------------------> Variables
#     bin = []
#     if len(win) == 1:
#         bin.append([x for x in range(0, maxL[0]+win[0], win[0])])
#         if maxL[1] is not None:
#             bin.append([x for x in range(0, maxL[1]+win[0], win[0])])
#         else:
#             bin.append([None])
#     else:
#         bin.append(win)
#         bin.append(win)
#     #endregion ------------------------------------------------> Variables
    
#     #region --------------------------------------------------------> Empty DF
#     #------------------------------> Columns
#     label = df.columns.unique(level=0).tolist()[4:]
#     nL = len(label)
#     a = (2*nL+1)*['Rec']+(2*nL+1)*['Nat']
#     b = ['Win']+nL*['All']+nL*['Unique']+['Win']+nL*['All']+nL*['Unique']
#     c = 2*(['Win']+2*label)
#     #------------------------------> Rows
#     nR = sorted([len(x) for x in bin])[-1]
#     #------------------------------> df
#     col = pd.MultiIndex.from_arrays([a[:],b[:],c[:]])
#     dfO = pd.DataFrame(np.nan, index=range(0,nR), columns=col)
#     #endregion -----------------------------------------------------> Empty DF

#     #region ---------------------------------------------------> Fill
#     #------------------------------> Windows
#     dfO.iloc[range(0,len(bin[0])), dfO.columns.get_loc(('Rec','Win','Win'))] = bin[0]
#     if bin[1][0] is not None:
#         dfO.iloc[range(0,len(bin[1])), dfO.columns.get_loc(('Nat','Win','Win'))] = bin[1]
#     else:
#         pass
#     #------------------------------> 
#     for e in label:
#         dfT = df[df[(e,'P')] < alpha]
#         #------------------------------> 
#         dfR = dfT[[('Nterm','Nterm'),('Cterm', 'Cterm')]].copy()
#         dfR[('Nterm','Nterm')] = dfR[('Nterm','Nterm')] - 1
#         l = dfR.to_numpy().flatten()
#         l = [x for x in l if x > 0 and x < maxL[0]]
#         a,_ = np.histogram(l, bins=bin[0])
#         dfO.iloc[range(0,len(a)),dfO.columns.get_loc(('Rec','All',e))] = a
#         l = list(set(l))
#         a,_ = np.histogram(l, bins=bin[0])
#         dfO.iloc[range(0,len(a)),dfO.columns.get_loc(('Rec','Unique',e))] = a
#         #------------------------------> 
#         if bin[1][0] is not None:
#             dfR = dfT[[('NtermF','NtermF'),('CtermF', 'CtermF')]].copy()
#             dfR[('NtermF','NtermF')] = dfR[('NtermF','NtermF')] - 1
#             l = dfR.to_numpy().flatten()
#             l = [x for x in l if x > 0 and x < maxL[0]]
#             a,_ = np.histogram(l, bins=bin[0])
#             dfO.iloc[range(0,len(a)),dfO.columns.get_loc(('Nat','All',e))] = a
#             l = list(set(l))
#             a,_ = np.histogram(l, bins=bin[0])
#             dfO.iloc[range(0,len(a)),dfO.columns.get_loc(('Nat','Unique',e))] = a
#         else:
#             pass
#     #endregion ------------------------------------------------> Fill

#     return dfO
# #---


# def R2CpR(df: pd.DataFrame, alpha: float, protL: list[int]) -> pd.DataFrame:
#     """
#         Parameters
#         ----------
#         df: pd.DataFrame
#             Nterm Cterm NtermF CtermF Exp1 .... ExpN
#             Nterm Cterm NtermF CtermF P    .... P
            
#         Returns
#         -------
#         pd.DataFrame
#     """
#     #region -------------------------------------------------------------> dfO
#     label = df.columns.unique(level=0).tolist()[4:]
#     nL = len(label)
#     a = (nL)*['Rec']+(nL)*['Nat']
#     b = 2*label
#     nR = sorted(protL, reverse=True)[0] if protL[1] is not None else protL[0]
#     idx = pd.IndexSlice
#     col = pd.MultiIndex.from_arrays([a[:],b[:]])
#     dfO = pd.DataFrame(0, index=range(0,nR), columns=col)   
#     #endregion ----------------------------------------------------------> dfO
   
#     #region ------------------------------------------------------------> Fill
#     for e in label:
#         dfT = df[df[(e,'P')] < alpha]
#         #------------------------------> Rec
#         dfR = dfT[[('Nterm','Nterm'),('Cterm', 'Cterm')]].copy()
#         #------------------------------> 0 based residue number
#         dfR[('Nterm','Nterm')] = dfR[('Nterm','Nterm')] - 2
#         dfR[('Cterm','Cterm')] = dfR[('Cterm','Cterm')] - 1
#         l = dfR.to_numpy().flatten()
#         # No Cleavage in 1 and last residue
#         l = [x for x in l if x > -1 and x < protL[0]]
#         for x in l:
#             dfO.at[x, idx['Rec',e]] = dfO.at[x, idx['Rec',e]] + 1
#         #------------------------------> Nat
#         if protL[1] is not None:
#             dfR = dfT[[('NtermF','NtermF'),('CtermF', 'CtermF')]].copy()
#             #------------------------------> 0 based residue number
#             dfR[('NtermF','NtermF')] = dfR[('NtermF','NtermF')] - 2
#             dfR[('CtermF','CtermF')] = dfR[('CtermF','CtermF')] - 1
#             l = dfR.to_numpy().flatten()
#             l = [x for x in l if x > -1 and x < protL[0]]
#             for x in l:
#                 dfO.at[x, idx['Nat',e]] = dfO.at[x, idx['Nat',e]] + 1
#         else:
#             pass
#     #endregion ---------------------------------------------------------> Fill

#     return dfO
# #---


# def R2CEvol(df: pd.DataFrame, alpha: float, protL: list[int]) -> pd.DataFrame:
#     """
#         Parameters
#         ----------
#         df: pd.DataFrame
#             Nterm Cterm NtermF CtermF Exp1     .... ExpN
#             Nterm Cterm NtermF CtermF Int P    .... Int P
            
#         Returns
#         -------
#         pd.DataFrame
#     """
#     def IntL2MeanI(a: list, alpha: float) -> float:
#         """
        
        
#         """
#         if a[-1] < alpha:
#             l = list(map(float, a[0][1:-1].split(',')))
#             return (sum(l)/len(l))
#         else:
#             return np.nan
#     #---
#     #region --------------------------------------------------------> 
#     idx = pd.IndexSlice
#     label = df.columns.unique(level=0).tolist()[4:]
#     nL = len(label)
#     a = df.columns.tolist()[4:]
#     print(a)
#     colN = list(range(4, len(a)+4))
#     print(colN)
#     #endregion -----------------------------------------------------> 
    
#     #region --------------------------------------------------------> 
#     a = (nL)*['Rec']+(nL)*['Nat']
#     b = 2*label
#     nR = sorted(protL, reverse=True)[0] if protL[1] is not None else protL[0]
#     col = pd.MultiIndex.from_arrays([a[:],b[:]])
#     dfO = pd.DataFrame(0, index=range(0,nR), columns=col)
#     #endregion -----------------------------------------------------> 

#     #region ---------------------------------------------------> 
#     dfT = df.iloc[:,[0,1]+colN].copy()
#     #------------------------------> 0 range for residue numbers
#     dfT.iloc[:,0] = dfT.iloc[:,0]-2
#     dfT.iloc[:,1] = dfT.iloc[:,1]-1
#     resL = sorted(list(set(dfT.iloc[:,[0,1]].to_numpy().flatten())))
#     resL = [x for x in resL if x > -1 and x < protL[0]]
#     #------------------------------>
#     for e in label:
#         dfT.loc[:,idx[e,'Int']] = dfT.loc[:,idx[e,['Int','P']]].apply(IntL2MeanI, axis=1, raw=True, args=[alpha])
#     #------------------------------> 
#     maxN = dfT.loc[:,idx[:,'Int']].max().max()
#     minN = dfT.loc[:,idx[:,'Int']].min().min()
#     if maxN != minN:
#         dfT.loc[:,idx[:,'Int']] = 1 + (((dfT.loc[:,idx[:,'Int']] - minN)*(9))/(maxN - minN))
#         dfT.loc[:,idx[:,'Int']] = dfT.loc[:,idx[:,'Int']].replace(np.nan, 0)
#     else:
#         dfT.loc[:,idx[:,'Int']] = dfT.loc[:,idx[:,'Int']].notnull().astype('int')
#     #------------------------------>
#     for r in resL:
#         #------------------------------>
#         dfG = dfT.loc[(dfT[('Nterm','Nterm')]==r) | (dfT[('Cterm','Cterm')]==r)].copy()
#         #------------------------------>
#         dfG = dfG.loc[dfG.loc[:,idx[:,'Int']].any(axis=1)]
#         dfG.loc[:,idx[:,'Int']] = dfG.loc[:,idx[:,'Int']].apply(lambda x: x/x.loc[x.ne(0).idxmax()], axis=1)
#         #------------------------------>
#         dfO.iloc[r, range(0,len(label))] = dfG.loc[:,idx[:,'Int']].sum(axis=0)
#     #endregion ------------------------------------------------> 
    
#     #region ---------------------------------------------------> 
#     if protL[1] is not None:
#         dfT = df.iloc[:,[2,3]+colN].copy()
#         #------------------------------> 0 range for residue number
#         dfT.iloc[:,0] = dfT.iloc[:,0]-2
#         dfT.iloc[:,1] = dfT.iloc[:,1]-1
#         resL = sorted(list(set(dfT.iloc[:,[0,1]].to_numpy().flatten())))
#         resL = [x for x in resL if x > -1 and x < protL[0]]
#         #------------------------------> 
#         for e in label:
#             dfT.loc[:,idx[e,'Int']] = dfT.loc[:,idx[e,['Int','P']]].apply(IntL2MeanI, axis=1, raw=True, args=[alpha])
#         #------------------------------> 
#         maxN = dfT.loc[:,idx[:,'Int']].max().max()
#         minN = dfT.loc[:,idx[:,'Int']].min().min()
#         if maxN != minN:
#             dfT.loc[:,idx[:,'Int']] = 1 + (((dfT.loc[:,idx[:,'Int']] - minN)*(9))/(maxN - minN))
#             dfT.loc[:,idx[:,'Int']] = dfT.loc[:,idx[:,'Int']].replace(np.nan, 0)
#         else:
#             dfT.loc[:,idx[:,'Int']] = dfT.loc[:,idx[:,'Int']].notnull().astype('int')    
#         #------------------------------> 
#         for r in resL:
#             dfG = dfT.loc[(dfT[('NtermF','NtermF')]==r) | (dfT[('CtermF','CtermF')]==r)].copy()
#             #------------------------------>
#             dfG = dfG.loc[dfG.loc[:,idx[:,'Int']].any(axis=1)]
#             dfG.loc[:,idx[:,'Int']] = dfG.loc[:,idx[:,'Int']].apply(lambda x: x/x.loc[x.ne(0).idxmax()], axis=1)
#             #------------------------------> 
#             dfO.iloc[r, range(len(label),2*len(label))] = dfG.loc[:,idx[:,'Int']].sum(axis=0)    
#     else:
#         pass
#     #endregion ------------------------------------------------> 

#     return dfO
# #---


# def R2SeqAlignment(
#     df: pd.DataFrame, alpha: float, seqR: str, seqN: Union[None, str],
#     fileP: 'Path', tLength: int,
#     ) -> bool:
#     """Sequence Alignment for the TarProt Module

#         Parameters
#         ----------
        

#         Returns
#         -------
        

#         Raise
#         -----
        
#     """
#     def GetString(
#         df: pd.DataFrame, seq: str, rec: bool, alpha: float, label: str, 
#         lSeq: int,
#         ) -> tuple[int, list[str]]:
#         """
    
#             Parameters
#             ----------
            
    
#             Returns
#             -------
            
    
#             Raise
#             -----
            
#         """
#         #region --------------------------------------------------------> 
#         idx = pd.IndexSlice
#         df = df[df.loc[:,idx[label,'P']] <= alpha].copy()
#         df = df.reset_index(drop=True)
#         nCero = len(str(df.shape[0]+1))
#         tString = [seq]
#         #endregion -----------------------------------------------------> 

#         #region ---------------------------------------------------> 
#         for r in df.itertuples():
#             n = r[3] if rec else r[5]  
#             tString.append((n-1)*' '+r[1]+(lSeq-n+1-len(r[1]))*' ')
#         #endregion ------------------------------------------------> 
#         return (nCero, tString)
#     #---
    
#     #region ---------------------------------------------------> Variables
#     #------------------------------> 
#     label = df.columns.unique(level=0)[7:].tolist()
#     lenSeqR = len(seqR)
#     lenSeqN = len(seqN) if seqN is not None else None
#     #------------------------------> ReportLab
#     doc = SimpleDocTemplate(fileP, pagesize=A4, rightMargin=25,
#         leftMargin=25, topMargin=25, bottomMargin=25)
#     Story  = []
#     styles = getSampleStyleSheet()
#     styles.add(ParagraphStyle(name='Seq', fontName='Courier', fontSize=8.5))
#     #endregion ------------------------------------------------> Variables
    
#     #region ---------------------------------------------------> 
#     for e in label:
#         #------------------------------> 
#         Story.append(Paragraph(f'{e} Recombinant Sequence'))
#         Story.append(Spacer(1,20))
#         nCero, tString = GetString(df, seqR, True, alpha, e, lenSeqR)
#         for s in range(0, lenSeqR, tLength):
#             #------------------------------> 
#             printString = ''
#             #------------------------------> 
#             for k,v in enumerate(tString):
#                 a = v[s:s+tLength]
#                 if a.strip():
#                     end = k
#                     printString = f"{printString}{str(k).zfill(nCero)}-{a.replace(' ', '&nbsp;')}<br />"
#                 else:
#                     pass
#             #------------------------------> 
#             Story.append(Paragraph(printString, style=styles['Seq']))
#             if end:
#                 Story.append(Spacer(1,10))
#             else:
#                 pass
#         if end:
#             Story.append(Spacer(1,10))
#         else:
#             Story.append(Spacer(1,20))
#     #endregion ------------------------------------------------> 

#     #region ---------------------------------------------------> 
#     if seqN is not None:
#         for e in label:
#             #------------------------------> 
#             Story.append(Paragraph(f'{e} Native Sequence'))
#             Story.append(Spacer(1,20))
#             nCero, tString = GetString(df, seqN, False, alpha, e, lenSeqN)
#             for s in range(0, lenSeqN, tLength):
#                 #------------------------------> 
#                 printString = ''
#                 #------------------------------> 
#                 for k,v in enumerate(tString):
#                     a = v[s:s+tLength]
#                     if a.strip():
#                         end = k
#                         printString = f"{printString}{str(k).zfill(nCero)}-{a.replace(' ', '&nbsp;')}<br />"
#                     else:
#                         pass
#                 #------------------------------> 
#                 Story.append(Paragraph(printString, style=styles['Seq']))
#                 if end:
#                     Story.append(Spacer(1,10))
#                 else:
#                     pass
#             if end:
#                 Story.append(Spacer(1,10))
#             else:
#                 Story.append(Spacer(1,20))
#     #endregion ------------------------------------------------> 
    
#     doc.build(Story)
#     return True
# #---
#endregion ----------------------------------------------------------> Methods
