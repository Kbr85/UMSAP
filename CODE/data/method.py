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
import itertools
import copy
import traceback
from operator import itemgetter
from datetime import datetime
from pathlib import Path
from typing import Union, Literal

import pandas as pd
import numpy as np
import matplotlib as mpl

import wx

# from reportlab.lib.pagesizes import A4
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

import config.config as mConfig
import data.file as mFile
import data.exception as mException
import data.statistic as mStatistic
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


def StrSetMessage(start:str, end:str, link:str='\n\nFurther details:\n') -> str:
    """Creates a message by concatenating start and end with link.

        Parameters
        ----------
        start: str
            Start of the message
        end : str
            End of the message
        link : str
            Link between start and end

        Returns
        -------
        str:
            Full message

        Examples
        --------
        >>> StrSetMessage('Start', 'End', link=' - ')
        >>> 'Start - End'
        >>> StrSetMessage('Start.', 'End.', link=None)
        >>> 'Start. End.'
    """
    if link is not None:
        return f"{start}{link}{end}"
    else:
        return f"{start} {end}"
#---


def Str2ListNumber(
    tStr: str, 
    numType:mConfig.litNumType='int',
    sep: str=',',
    unique: bool=False
    ) -> Union[list[int], list[float]]:
    """Turn a string into a list of numbers. Ranges are expanded as integers.

        Parameters
        ----------
        tStr: str
            The string containing the numbers and/or range of numbers (4-8)
        numType : str
            One of int, float
        sep : str
            The character to separate numbers in the string
        unique : boolean
            Return only unique values. Order is kept. Default is False.

        Returns
        -------
        list of numbers.

        Examples
        --------
        >>> Str2ListNumber('1, 2, 3, 6-10,  4  ,  5, 6  , 7', sep=',')
        >>> [1, 2, 3, 6, 7, 8, 9, 10, 4, 5, 6, 7]
        >>> Str2ListNumber('1, 2, 3, 6-10,  4  ,  5, 6  , 7', sep=',', unique=True)
        >>> [1, 2, 3, 6, 7, 8, 9, 10, 4, 5]
    """
    #region -------------------------------------------------------> Variables
    lN = []
    values = tStr.strip().split(sep)
    #endregion ----------------------------------------------------> Variables

    #region -----------------------------------------------------> Get numbers
    for k in values:
        if k.strip() != '':
            #------------------------------> Expand ranges
            lK = ExpandRange(k, numType)
            #------------------------------> Get list of numbers
            lN = lN + lK
        else:
            pass
    #endregion --------------------------------------------------> Get numbers

    #region ----------------------------------------------------------> Unique
    if unique:
        lo = ListRemoveDuplicates(lN)
    else:
        lo = lN
    #endregion -------------------------------------------------------> Unique

    return lo
#---


def ResControl2ListNumber(
    val: str, 
    sep: list[str]=[' ', ',', ';'], 
    numType: mConfig.litNumType='int',
    ) -> list[list[list[int]]]:
    """Return a list from a Result - Control string.

        Parameters
        ----------
        val : str
            String with the numbers. e.g. '0-4 6, 7 8 9; 10 13-15, ""; ...'
        sep : list of str
            Separators used in the string e.g. [' ', ',', ';']
        numType: str
            To convert to numbers

        Returns
        -------
        list of list of list of str
        [[[0 1 2 3 4], [7 8 9]], [[10 13 14 15], []], ...]   
        
        Examples
        --------
        >>> ResControl2ListNumber('0 1 2, 3 4 5; 6 7 8, 9 10 11', sep=[' ', ',', ';'], numType='int')
        >>> [[[0,1,2], [3,4,5]], [[6,7,8], [9,10,11]]]
    """
    # Test in test.unit.test_method.Test_ResControl2ListNumber
    #region -------------------------------------------------------> Variables
    l = []
    #endregion ----------------------------------------------------> Variables

    #region -------------------------------------------------------> Form list
    for k in val.split(sep[2]):
        #------------------------------> 
        lRow = []
        #------------------------------> 
        for j in k.split(sep[1]):
            colVal = Str2ListNumber(j, numType=numType, sep=sep[0])
            lRow.append(colVal)
        #------------------------------> 
        l.append(lRow)
    #endregion ----------------------------------------------------> Form list

    return l
#---


def ResControl2Flat(val: list[list[list[int]]]) -> list[int]:
    """Result - Control list as a flat list.

        Parameters
        ----------
        val : list of list of list of int
            Result - Control as a list of list of list of int.

        Returns
        -------
        list of int
            Flat Result - Control list

        Examples
        --------
        >>> ResControl2Flat([[[0,1,2], [3,4,5]], [[6,7,8], [9,10,11]]])
        >>> [0,1,2,3,4,5,6,7,8,9,10,11])
    """
    # Test in test.unit.test_method.Test_ResControl2Flat
    return list(itertools.chain(*(itertools.chain(*val))))
#---


def ResControl2DF(
    val: list[list[list[int]]], start: int
    ) -> list[list[list[int]]]:
    """Convert the Result - Control column numbers in the original file to the
        column numbers of the initial dataframe used in the analysis. 

        Parameters
        ----------
        val : list of list of list of int
            Result - Control as a list of list of list of int
        start : int
            Column index start of the Result - Control columns in the initial
            dataframe 

        Returns
        -------
        list[list[list[int]]]
            The list has the same order as the input val but the column index
            are adjusted.

        Notes
        -----
        It is assumed columns in the DF have the same order as in val.
        Empty list are possible to mimic empty conditions in an experiment.

        Examples
        --------
        >>> ResControl2DF([[[0,1,2], []], [[6,7,8], []]], 1)
        >>> [[[1,2,3],[]], [[4,5,6],[]]]
    """
    # Test in test.unit.test_method.Test_ResControl2DF
    #region -------------------------------------------------------> Variables
    idx  = start
    outL = []
    #endregion ----------------------------------------------------> Variables

    #region --------------------------------------------------> Adjust col idx
    for row in val:
        #------------------------------>
        outR = []
        #------------------------------>
        for col in row:
            #------------------------------>
            outC = []
            #------------------------------>
            for _ in col:
                outC.append(idx)
                idx += 1
            #------------------------------>
            outR.append(outC)
        #------------------------------>
        outL.append(outR)
    #endregion -----------------------------------------------> Adjust col idx

    return outL
#---
#endregion ---------------------------------------------------> String methods


#region ------------------------------------------------------> Number methods
def ExpandRange(
    r: str, numType: mConfig.litNumType='int',
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
        a,b = tr.split('-')
        #-------------->  Check a value
        if a == '':
            #--> Negative number
            return [mConfig.oNumType[numType](tr)]
        else:
            pass
        #-------------->  Check b
        if b == '':
            #--> range like 4-
            raise mException.InputError(mConfig.mRangeNumIE.format(r))
        else:
            pass
        #--------------> Expand range
        a = int(a)
        b = int(b)
        #--> Expand range
        if a < b:
            return [x for x in range(a, b+1, 1)]
        else:
            raise mException.InputError(mConfig.mRangeNumIE.format(r))
    else:
        #------------------------------> Positive number
        return [mConfig.oNumType[numType](tr)]
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
    colNames = mFile.ReadFileFirstLine(fileP)
    #endregion ----------------------------------------------------> Read file

    #region -------------------------------------------------------> Fill List
    #------------------------------> Del items
    lc.DeleteAllItems()
    #------------------------------> Fill
    for k, v in enumerate(colNames):
        index = lc.InsertItem(k, " " + str(k))
        lc.SetItem(index, 1, v)
    #endregion ----------------------------------------------------> Fill List

    return True
#---


def ListRemoveDuplicates(l: Union[list, tuple]) -> list:
    """Remove duplicate elements from l. Order is conserved.

        Parameters
        ----------
        l : list or tuple
            Contain the duplicate elements to remove

        Returns
        -------
        list

        Examples
        --------
        >>> ListRemoveDuplicates([1,2,3,6,4,7,5,6,10,7,8,9])
        >>> [1, 2, 3, 6, 4, 7, 5, 10, 8, 9]
    """
    # Test in tests.unit.data.test_method.Test_ListRemoveDuplicates
    return list(dict.fromkeys(l))
#---
#endregion ------------------------------------------------------> wx.ListCtrl


#region ----------------------------------------------------------------> Dict
def DictVal2Str(
    iDict: dict, 
    changeKey: list=[],
    new: bool=False,
    ) -> dict:
    """Returns a dict with values turn to str for all keys or only those in 
        changeKey.

        Parameters
        ----------
        iDict: dict
            Initial dict.
        changeKey: list of keys
            Only modify this keys.
        new : boolean
            Do not modify iDict (True) or modify in place (False). 
            Default is False.

        Returns
        -------
        dict :
            with the corresponding values turned to str

        Examples
        --------
        >>> DictVal2Str({1:Path('/k/d/c'), 'B':3})
        >>> {1: '/k/d/c', 'B': '3'}
        >>> DictVal2Str({1:Path('/k/d/c'), 'B':3}, changeKey=[1])
        >>> {1: '/k/d/c', 'B': 3}
    """
    #region -------------------------------------------------------> Variables
    if new:
        oDict = copy.deepcopy(iDict)
    else:
        oDict = iDict
    #endregion ----------------------------------------------------> Variables
    
    #region ---------------------------------------------------> Change values
    for k in changeKey:
        oDict[k] = str(oDict[k])
    #endregion ------------------------------------------------> Change values

    return oDict
#---
#endregion -------------------------------------------------------------> Dict


#region --------------------------------------------------------> pd.DataFrame
def DFFilterByColS(
    df:'pd.DataFrame', 
    col: int,
    refStr: str,
    comp: Literal['e', 'ne'],
    ) -> 'pd.DataFrame':
    """Filter rows in the pd.DataFrame based on the string values present in 
        col.

        Parameters
        ----------
        df: pd.DataFrame
        col : int
            The column index used to filter rows
        refStr : string
            Reference string
        comp : str
            Numeric comparison to use in the filter. One of:
            'e', 'ne

        Returns
        -------
        pd.DataFrame

        Notes
        -----
        Rows with values in col that do not comply with c[x] comp refStr are 
        discarded, e.g. c[x] == 'refString'
        
        Assumes all values in col are strings
    """
    #region ----------------------------------------------------------> Filter
    #------------------------------>  Copy
    dfo = df.copy()
    #------------------------------> Filter
    if comp == 'e':
        dfo = df.loc[df.iloc[:,col] == refStr]
    elif comp == 'ne':
        dfo = df.loc[df.iloc[:,col] != refStr]
    else:
        msg = mConfig.mCompNYI.format(comp)
        raise mException.NotYetImplementedError(msg)
    #endregion -------------------------------------------------------> Filter

    return dfo
#---


def DFReplace(
    df: pd.DataFrame, 
    oriVal: list, 
    repVal: Union[list, str, float, int], 
    sel: list[int]=[],
    ) -> pd.DataFrame:
    """Replace values in the dataframe.

        Parameters
        ----------
        df: pd.DataFrame
            Dataframe with the data.
        oriVal: list
            List of values to search and replace.
        repVal: list or single value
            List of values to use as replacement. When only one value is given
            all oriVal are replace with the given value.
        sel : list of int
            Column indexes.

        Returns
        -------
        pd.DataFrame
            With replaced values

        Raise
        -----
        InputError :
            - When selection is not found in df
            - When oriVal and repVal have different length
        ExecutionError :
            - When the replacement procedure does not finish correctly

        Notes
        -----
        Column selection in the df is done by column number.
    """
    #region -----------------------------------------------------> Check input
    if isinstance(repVal, (list, tuple)):
        repValFix = repVal
    else:
        repValFix = len(oriVal) * [repVal]
    #endregion --------------------------------------------------> Check input

    #region ---------------------------------------------------------> Replace
    #------------------------------> Copy
    dfo = df.copy()
    #------------------------------> 
    for k, v in enumerate(oriVal):
        #------------------------------> 
        rep = repValFix[k]
        #------------------------------> 
        if sel is not None:
            dfo.iloc[:,sel] = dfo.iloc[:,sel].replace(v, rep)
        else:
            dfo = dfo.replace(v, rep)
    #endregion ------------------------------------------------------> Replace

    return dfo
#---


def DFExclude(df:'pd.DataFrame', col: list[int]) -> 'pd.DataFrame':
    """Exclude rows in the pd.DataFrame based on the values present in col.

        Parameters
        ----------
        df: pd.DataFrame
        col : list[int]

        Returns
        -------
        pd.DataFrame

        Notes
        -----
        Rows with at least one value other than NA in the given columns are 
        discarded
    """
    #region ----------------------------------------------------------> Exclude
    #------------------------------>  Copy
    dfo = df.copy()
    #------------------------------> Exclude
    a = dfo.iloc[:,col].notna()
    a = a.loc[(a==True).any(axis=1)] # type: ignore
    idx = a.index
    dfo = dfo.drop(index=idx) # type: ignore
    #endregion -------------------------------------------------------> Exclude

    return dfo
#---


def DFFilterByColN(
    df:'pd.DataFrame', 
    col: list[int], 
    refVal: float,
    comp: mConfig.litComp,
    ) -> 'pd.DataFrame':
    """Filter rows in the pd.DataFrame based on the numeric values present in 
        col.

        Parameters
        ----------
        df: pd.DataFrame
        col : list of int
            The column indexes used to filter rows
        refVal : float
            Reference value
        comp : str
            Numeric comparison to use in the filter. One of:
            'lt', 'le', 'e', 'ge', 'gt'

        Returns
        -------
        pd.DataFrame

        Notes
        -----
        Rows with values in col that do not comply with c[x] comp refVal are 
        discarded, e.g. c[x] > 3,45
        
        Assumes all values in col are numbers.
    """
    #region ----------------------------------------------------------> Filter
    #------------------------------>  Copy
    dfo = df.copy()
    #------------------------------> Filter
    if comp == 'lt':
        dfo = df.loc[(df.iloc[:,col] < refVal).any(axis=1)] # type: ignore
    elif comp == 'le':
        dfo = df.loc[(df.iloc[:,col] <= refVal).any(axis=1)] # type: ignore
    elif comp == 'e':
        dfo = df.loc[(df.iloc[:,col] == refVal).any(axis=1)] # type: ignore
    elif comp == 'ge':
        dfo = df.loc[(df.iloc[:,col] >= refVal).any(axis=1)] # type: ignore
    elif comp == 'gt':
        dfo = df.loc[(df.iloc[:,col] > refVal).any(axis=1)] # type: ignore
    else:
        msg = mConfig.mCompNYI.format(comp)
        raise mException.NotYetImplementedError(msg)
    #endregion -------------------------------------------------------> Filter

    return dfo
#---
#endregion -----------------------------------------------------> pd.DataFrame


#region -------------------------------------------------------------> Methods
def MatplotLibCmap(
    N: int=128,
    c1: tuple[int, int, int]=(255, 0, 0),
    c2: tuple[int, int, int]=(255, 255, 255),
    c3: tuple[int, int, int]=(0, 0, 255),
    bad: Union[tuple[float, float, float], str]='',
    ):
    """ Generate custom matplotlib cmap c1->c2->c3.

        Parameters
        ----------
        c1 : list of int
            Color for lowest value. Default is red [255, 0, 0]
        c2 : list of int
            Color for the middle value. Default is white [255, 255, 255]
        c3 : list of int
            Color of the biggest value. Default is blue [0, 0, 255]
        bad : list of int, list of float, str or None
            Color for bad values. Default is None.

        Return
        ------
        Matplotlib color map.

        Raises
        ------
        InputError
            - When N is not an integer
            - When any of the colors is not a proper [r, g, b] color (0 to 255)
    """
    # No test
    #region ----------------------------------------------------------> Colors
    #------------------------------>  c1 -> c2
    try:
        vals1 = np.ones((N, 4))
        vals1[:, 0] = np.linspace(c1[0]/255, c2[0]/255, N)
        vals1[:, 1] = np.linspace(c1[1]/255, c2[1]/255, N)
        vals1[:, 2] = np.linspace(c1[2]/255, c2[2]/255, N)
    except Exception as e:
        raise mException.InputError(str(e))
    #------------------------------>  c2 -> c3
    try:
        vals2 = np.ones((N, 4))
        vals2[:, 0] = np.linspace(c2[0]/255, c3[0]/255, N)
        vals2[:, 1] = np.linspace(c2[1]/255, c3[1]/255, N)
        vals2[:, 2] = np.linspace(c2[2]/255, c3[2]/255, N)
    except Exception as e:
        raise mException.InputError(str(e))
    #endregion -------------------------------------------------------> Colors

    #region ------------------------------------------------------------> CMAP
    #------------------------------> 
    vals   = np.vstack((vals1, vals2))
    newMap = mpl.colors.ListedColormap(vals)
    #------------------------------> 
    if bad is not None:
        newMap.set_bad(color=bad)
    else:
        pass
    #endregion ---------------------------------------------------------> CMAP

    return newMap
#---


def Fragments(
    df: 'pd.DataFrame', val: float, comp: Literal['lt', 'le', 'e', 'ge', 'gt'],
    ) -> dict:
    """Creates the dict holding the fragments identified in the analysis

        Parameters
        ----------
        df: pd.DataFrame with the data from the analysis. The columns in df are
            expected to be:
            Seq Nrec Crec Nnat Cnat Exp1 Exp2 ...... ExpN
        val : float
            Threshold value to filter df and identify relevant peptides
        comp : str
            One of 'lt', 'le', 'e', 'ge', 'gt'

        Returns
        -------
        dict:
            {
                'Exp1' : {
                    'Coord' : [(x1, x2),...., (xN, xM)],
                    'CoordN': [(x1, x2),.(NaN, NaN)..., (xN, xM)]
                    'Seq'   : [Aligned Seq1, ...., Aligned SeqN],
                    'SeqL   : [Flat List with Seqs1, ...., Flat List with SeqsN],
                    'Np'    : [Number of peptides1, ...., NpN],
                    'NpNat  : [Number of native peptides1, ...., NpNatN],
                    'Nc'    : [Number of cleavages1, ...., NcN],
                    'NcNat' : [Number of native cleavages1, ....., NcNatN],
                    'NFrag' : (Number of fragments, Number of fragments Nat),
                    'NcT'   : (Number of cleavages for the Exp as a whole, 
                               Number of cleavages for the Exp as a whole Nat),
                },
                'ExpN' : {},
            }
        - All list inside each Exp have the same length
        - NFrag and NcT are tuples with two values each.
        - Keys Exp1,...,ExpN are variables and depend on the module calling the
        method.
    """
    # No Test
    #region -------------------------------------------------------> Variables
    dictO = {}
    #endregion ----------------------------------------------------> Variables

    #region --------------------------------------------------->
    for c in range(5, df.shape[1]):
        colK = str(df.columns.values[c])
        #------------------------------> Prepare dictO
        dictO[colK]           = {}
        dictO[colK]['Coord']  = []
        dictO[colK]['CoordN'] = []
        dictO[colK]['Seq']    = []
        dictO[colK]['SeqL']   = []
        dictO[colK]['Np']     = []
        dictO[colK]['NpNat']  = []
        dictO[colK]['Nc']     = []
        dictO[colK]['NcNat']  = []
        #------------------------------> Filter df
        dfE = DFFilterByColN(df, [c], val, comp)
        #------------------------------> 
        n       = None
        c       = None
        seq     = None
        seqL    = []
        nP      = None
        npNat   = None
        ncL     = []
        ncLNat  = []
        nctL    = []
        nctLNat = []
        #------------------------------>    
        for r in range(0, dfE.shape[0]):
            if n is None:
                seq = dfE.iat[r,0]
                seqL.append(seq)
                nP = 1
                n  = dfE.iat[r,1]
                c  = dfE.iat[r,2]
                nf = dfE.iat[r,3]
                cf = dfE.iat[r,4]
                if np.isnan(nf) and np.isnan(cf):
                    npNat = 0
                else:
                    npNat = 1
                if np.isnan(nf):
                    pass
                else:
                    ncLNat.append(n-1)
                    nctLNat.append(n-1)
                if np.isnan(cf):
                    pass
                else:
                    ncLNat.append(c)
                    nctLNat.append(c)
                ncL.append(n-1)
                ncL.append(c)
                nctL.append(n-1)
                nctL.append(c)
            else:
                nc   = dfE.iat[r,1]
                cc   = dfE.iat[r,2]
                ncf  = dfE.iat[r,3]
                ccf  = dfE.iat[r,4]
                seqC = dfE.iat[r,0]
                if nc <= c:
                    seq = f'{seq}\n{(nc-n)*" "}{seqC}'
                    seqL.append(seqC)
                    nP = nP + 1 # type: ignore
                    if cc > c:
                        c = cc
                        cf = ccf
                    else:
                        pass
                    if not np.isnan(ncf) and not np.isnan(ccf):
                        npNat = npNat + 1 # type: ignore
                    else:
                        pass
                    if not np.isnan(ncf):
                        ncLNat.append(nc-1)
                        nctLNat.append(nc-1)
                    else:
                        pass
                    if not np.isnan(ccf):
                        ncLNat.append(cc)
                        nctLNat.append(cc)
                    else:
                        pass
                    ncL.append(nc-1)
                    ncL.append(cc)
                    nctL.append(nc-1)
                    nctL.append(cc)
                else:
                    dictO[colK]['Coord'].append((n,c))
                    dictO[colK]['CoordN'].append((nf,cf)) # type: ignore
                    dictO[colK]['Seq'].append(seq)
                    dictO[colK]['SeqL'].append(seqL)
                    dictO[colK]['Np'].append(nP)
                    dictO[colK]['NpNat'].append(npNat)
                    dictO[colK]['Nc'].append(len(list(set(ncL))))
                    dictO[colK]['NcNat'].append(len(list(set(ncLNat))))
                    n    = nc
                    c    = cc
                    nf   = ncf
                    cf   = ccf
                    seq  = seqC
                    seqL = [seqC]
                    nP   = 1
                    if not np.isnan(nf) and not np.isnan(cf):
                        npNat = 1
                    else:
                        npNat = 0
                    ncLNat = []
                    if not np.isnan(nf):
                        ncLNat.append(n-1)
                        nctLNat.append(n-1)
                    else:
                        pass
                    if not np.isnan(cf):
                        ncLNat.append(c)
                        nctLNat.append(c)
                    else:
                        pass
                    ncL = []
                    ncL.append(n-1)
                    ncL.append(c)
                    nctL.append(n-1)
                    nctL.append(c)
        #------------------------------> Catch the last line
        if n is not None:
            dictO[colK]['Coord'].append((n,c))
            dictO[colK]['CoordN'].append((nf,cf)) # type: ignore
            dictO[colK]['Seq'].append(seq)
            dictO[colK]['SeqL'].append(seqL)
            dictO[colK]['Np'].append(nP)
            dictO[colK]['NpNat'].append(npNat)
            dictO[colK]['Nc'].append(len(list(set(ncL))))
            dictO[colK]['NcNat'].append(len(list(set(ncLNat))))
            #------------------------------>
            dictO[colK]['NcT'] = [len(list(set(nctL))), len(list(set(nctLNat)))]
            #------------------------------>
            nFragN = [x for x in dictO[colK]['CoordN'] if not np.isnan(x[0]) or not np.isnan(x[1])]
            dictO[colK]['NFrag'] = [len(dictO[colK]['Coord']), len(nFragN)]
        else:
            dictO[colK]['NcT'] = []
            dictO[colK]['NFrag'] = []
        #------------------------------> All detected peptides as a list
    #endregion ------------------------------------------------>

    return dictO
#---


def MergeOverlappingFragments(
    coord:list[tuple[int, int]], delta:int=0,
    ) -> list[tuple[int, int]]:
    """Merge overlapping fragments in a list of fragments coordinates.

        Parameters
        ----------
        coord: list[tuple[int, int]]
            Fragment coordinates lists
        delta: int
            To adjust the merging of adjacent fragments.

        Returns
        -------
        list[tuple[int, int]]

        Notes
        -----
        An empty list is returned if coord is empty.
    """
    #region ---------------------------------------------------> Variables
    coordO = []
    #endregion ------------------------------------------------> Variables

    #region ------------------------------------------------------> Sort & Dup
    coordS = sorted(list(set(coord)), key=itemgetter(0,1))
    #endregion ---------------------------------------------------> Sort & Dup

    #region -------------------------------------> Merge Overlapping Intervals
    try:
        a,b = coordS[0]
    except IndexError:
        return []
    for ac,bc in coordS[1:]:
        if ac <= b+delta:
            if bc > b:
                b = bc
            else:
                pass
        else:
            coordO.append((a,b))
            a = ac
            b = bc
    #------------------------------> Catch the last one
    coordO.append((a,b))
    #endregion ----------------------------------> Merge Overlapping Intervals

    return coordO
#---


def HCurve(x:Union[float,pd.DataFrame,pd.Series], t0:float, s0:float) -> float:
    """Calculate the hyperbolic curve values according to:
        doi: 10.1142/S0219720012310038

        Parameters
        ----------
        

        Returns
        -------
        float
    """
    #region ---------------------------------------------------> Calculate
    return abs((abs(x)*t0)/(abs(x)-t0*s0)) # type: ignore
    #endregion ------------------------------------------------> Calculate
#---


def Rec2NatCoord(
    coord: list[tuple[int,int]], protLoc:tuple[int,int], delta:int,
    ) -> Union[list[tuple[int,int]], list[str]]:
    """

        Parameters
        ----------
        

        Returns
        -------
        

        Raise
        -----
        
    """
    #region ---------------------------------------------------> Return NA
    if delta == 0 or delta is None or protLoc[0] is None or protLoc[1] is None:
        return ['NA']
    else:
        pass
    #endregion ------------------------------------------------> Return NA

    #region ---------------------------------------------------> Calc
    listO = []
    for a,b in coord:
        if protLoc[0] <= a <= protLoc[1] and protLoc[0] <= b <= protLoc[1]:
            listO.append((a+delta, b+delta))
        else:
            pass
    #endregion ------------------------------------------------> Calc

    return listO
#---


def R2AA(
    df:pd.DataFrame,
    seq: str,
    alpha: float,
    protL: int,
    pos: int=5,
    ) -> pd.DataFrame:
    """AA distribution analysis.

        Parameters
        ----------
        df: pd.DataFrame
            Sequence Label1 LabelN
            Sequence P      P
        seq: str
            Recombinant protein sequence
        alpha: float
            Significance level
        protL: int
            Protein length.
        pos: int
            Number of positions to consider.

        Returns
        -------
        pd.DataFrame
            AA Label1       LabelN
            AA -2 -1 1 2 P  -2 -1 1 2 P
    """
    def AddNewAA(
        dfO: pd.DataFrame, r: int, pos: int, seq: str, l: str
        ) -> pd.DataFrame:
        """Add new amino acids to running total.

            Parameters
            ----------
            dfO: pd.DataFrame
                Running total
            r: int
                AA distance from cleavage site.
            pos: int
                Number of positions to consider.
            seq: str
                Amino acids sequence
            l: str
                Current column label

            Returns
            -------
            pd.DataFrame
        """
        #region ---------------------------------------------------> 
        if r >= pos:
            col = pos
            start = r - pos
        else:
            col = r
            start = 0
        #endregion ------------------------------------------------> 

        #region ---------------------------------------------------> 
        for a in seq[start:r]:
            dfO.at[a,(l,f'P{col}')] = dfO.at[a,(l,f'P{col}')] + 1
            col -= 1
        col = 1
        for a in seq[r:r+pos]:
            dfO.at[a,(l,f"P{col}'")] = dfO.at[a,(l,f"P{col}'")] + 1
            col += 1
        #endregion ------------------------------------------------> 

        return dfO
    #---
    #region ---------------------------------------------------> Empty
    aL = ['AA']
    bL = ['AA']
    for l in df.columns.get_level_values(0)[1:]:
        aL = aL + 2*pos*[l]
        bL = bL + [f'P{x}' for x in range(pos, 0, -1)] + [f'P{x}\'' for x in range(1, pos+1,1)]
    idx = pd.MultiIndex.from_arrays([aL[:],bL[:]])
    dfO = pd.DataFrame(0, columns=idx, index=mConfig.lAA1+['Chi']) # type: ignore
    dfO[('AA','AA')] = mConfig.lAA1[:]+['Chi']
    #endregion ------------------------------------------------> Empty

    #region ---------------------------------------------------> Fill
    idx = pd.IndexSlice
    for l in df.columns.get_level_values(0)[1:]:
        seqDF = df[df[idx[l,'P']] < alpha].iloc[:,0].to_list()
        for s in seqDF:
            #------------------------------> 
            n = seq.find(s)
            if n > 0:
                dfO = AddNewAA(dfO, n, pos, seq, l)
            else:
                pass
            #------------------------------> 
            c = n+len(s)
            if c < protL:
                dfO = AddNewAA(dfO, c, pos, seq, l)
            else:
                pass
    #endregion ------------------------------------------------> Fill

    #region ---------------------------------------------------> Random Cleavage
    c = 'ALL_CLEAVAGES_UMSAP'
    aL = 2*pos*[c]
    bL = [f'P{x}' for x in range(pos, 0, -1)] + [f"P{x}'" for x in range(1, pos+1,1)]
    idx = pd.MultiIndex.from_arrays([aL[:],bL[:]])
    dfT = pd.DataFrame(0, columns=idx, index=mConfig.lAA1+['Chi']) # type: ignore
    dfO = pd.concat([dfO, dfT], axis=1)
    for k,_ in enumerate(seq[1:-1], start=1): # Exclude first and last residue
        dfO = AddNewAA(dfO, k, pos, seq, c)
    #endregion ------------------------------------------------> Random Cleavage

    #region ---------------------------------------------------> Group
    idx = pd.IndexSlice
    gS = []
    for g in mConfig.lAAGroups:
        gS.append(dfO.loc[g,:].sum(axis=0))
    g = pd.concat(gS, axis=1)
    g = g.transpose()

    for l in df.columns.get_level_values(0)[1:]:
        for p in dfO.loc[:,idx[l,:]].columns.get_level_values(1):
            dfO.at['Chi', idx[l,p]] = mStatistic.Test_chi(
                g.loc[:,idx[[l,c],p]], alpha)[0]
    #endregion ------------------------------------------------> Group

    return dfO
#---


def R2Hist(
    df: pd.DataFrame, alpha: float, win: list[int], maxL: list[int]
    ) -> pd.DataFrame:
    """Create the cleavage histograms.

        Parameters
        ----------
        df: pd.DataFrame
            Nterm Cterm NtermF CtermF Exp1 .... ExpN
            Nterm Cterm NtermF CtermF P    .... P
        alpha: float
            Alpha level.
        win: list[int]
            Window definition
        maxL: list[int]
            Protein lengths, Recombinant and Native or None

        Returns
        -------
        pd.DataFrame
    """
    #region ---------------------------------------------------> Variables
    bin = []
    if len(win) == 1:
        bin.append([x for x in range(0, maxL[0]+win[0], win[0])])
        if maxL[1] is not None:
            bin.append([x for x in range(0, maxL[1]+win[0], win[0])])
        else:
            bin.append([None])
    else:
        bin.append(win)
        bin.append(win)
    #endregion ------------------------------------------------> Variables

    #region --------------------------------------------------------> Empty DF
    #------------------------------> Columns
    label = df.columns.unique(level=0).tolist()[4:]
    nL = len(label)
    a = (2*nL+1)*['Rec']+(2*nL+1)*['Nat']
    b = ['Win']+nL*['All']+nL*['Unique']+['Win']+nL*['All']+nL*['Unique']
    c = 2*(['Win']+2*label)
    #------------------------------> Rows
    nR = sorted([len(x) for x in bin])[-1]
    #------------------------------> df
    col = pd.MultiIndex.from_arrays([a[:],b[:],c[:]])
    dfO = pd.DataFrame(np.nan, index=range(0,nR), columns=col) # type: ignore
    #endregion -----------------------------------------------------> Empty DF

    #region ---------------------------------------------------> Fill
    #------------------------------> Windows
    dfO.iloc[range(0,len(bin[0])), dfO.columns.get_loc(('Rec','Win','Win'))] = bin[0]
    if bin[1][0] is not None:
        dfO.iloc[range(0,len(bin[1])), dfO.columns.get_loc(('Nat','Win','Win'))] = bin[1]
    else:
        pass
    #------------------------------> 
    for e in label:
        dfT = df[df[(e,'P')] < alpha]
        #------------------------------> 
        dfR = dfT[[('Nterm','Nterm'),('Cterm', 'Cterm')]].copy()
        dfR[('Nterm','Nterm')] = dfR[('Nterm','Nterm')] - 1
        l = dfR.to_numpy().flatten()
        l = [x for x in l if x > 0 and x < maxL[0]]
        a,_ = np.histogram(l, bins=bin[0])
        dfO.iloc[range(0,len(a)),dfO.columns.get_loc(('Rec','All',e))] = a
        l = list(set(l))
        a,_ = np.histogram(l, bins=bin[0])
        dfO.iloc[range(0,len(a)),dfO.columns.get_loc(('Rec','Unique',e))] = a
        #------------------------------> 
        if bin[1][0] is not None:
            dfR = dfT[[('NtermF','NtermF'),('CtermF', 'CtermF')]].copy()
            dfR[('NtermF','NtermF')] = dfR[('NtermF','NtermF')] - 1
            l = dfR.to_numpy().flatten()
            l = [x for x in l if x > 0 and x < maxL[0]]
            a,_ = np.histogram(l, bins=bin[0])
            dfO.iloc[range(0,len(a)),dfO.columns.get_loc(('Nat','All',e))] = a
            l = list(set(l))
            a,_ = np.histogram(l, bins=bin[0])
            dfO.iloc[range(0,len(a)),dfO.columns.get_loc(('Nat','Unique',e))] = a
        else:
            pass
    #endregion ------------------------------------------------> Fill

    return dfO
#---


def R2CpR(df: pd.DataFrame, alpha: float, protL: list[int]) -> pd.DataFrame:
    """Creates the Cleavage per Residue results.

        Parameters
        ----------
        df: pd.DataFrame
            Nterm Cterm NtermF CtermF Exp1 .... ExpN
            Nterm Cterm NtermF CtermF P    .... P
        alpha: float
            Alpha level
        protL: list[int]
            Protein length, recombinant and native or None.

        Returns
        -------
        pd.DataFrame
    """
    #region -------------------------------------------------------------> dfO
    label = df.columns.unique(level=0).tolist()[4:]
    nL = len(label)
    a = (nL)*['Rec']+(nL)*['Nat']
    b = 2*label
    nR = sorted(protL, reverse=True)[0] if protL[1] is not None else protL[0]
    idx = pd.IndexSlice
    col = pd.MultiIndex.from_arrays([a[:],b[:]])
    dfO = pd.DataFrame(0, index=range(0,nR), columns=col) # type: ignore
    #endregion ----------------------------------------------------------> dfO

    #region ------------------------------------------------------------> Fill
    for e in label:
        dfT = df[df[(e,'P')] < alpha]
        #------------------------------> Rec
        dfR = dfT[[('Nterm','Nterm'),('Cterm', 'Cterm')]].copy()
        #------------------------------> 0 based residue number
        dfR[('Nterm','Nterm')] = dfR[('Nterm','Nterm')] - 2
        dfR[('Cterm','Cterm')] = dfR[('Cterm','Cterm')] - 1
        l = dfR.to_numpy().flatten()
        # No Cleavage in 1 and last residue
        l = [x for x in l if x > -1 and x < protL[0]]
        for x in l:
            dfO.at[x, idx['Rec',e]] = dfO.at[x, idx['Rec',e]] + 1
        #------------------------------> Nat
        if protL[1] is not None:
            dfR = dfT[[('NtermF','NtermF'),('CtermF', 'CtermF')]].copy()
            #------------------------------> 0 based residue number
            dfR[('NtermF','NtermF')] = dfR[('NtermF','NtermF')] - 2
            dfR[('CtermF','CtermF')] = dfR[('CtermF','CtermF')] - 1
            l = dfR.to_numpy().flatten()
            l = [x for x in l if x > -1 and x < protL[0]]
            for x in l:
                dfO.at[x, idx['Nat',e]] = dfO.at[x, idx['Nat',e]] + 1
        else:
            pass
    #endregion ---------------------------------------------------------> Fill

    return dfO
#---


def R2CEvol(df: pd.DataFrame, alpha: float, protL: list[int]) -> pd.DataFrame:
    """
        Parameters
        ----------
        df: pd.DataFrame
            Nterm Cterm NtermF CtermF Exp1     .... ExpN
            Nterm Cterm NtermF CtermF Int P    .... Int P
        alpha: float
            Alpha level
        protL: list[int]
            Protein length, recombinant and native or None.

        Returns
        -------
        pd.DataFrame
    """
    def IntL2MeanI(a: list, alpha: float) -> float:
        """Calculate the intensity average.

            Parameters
            ----------
            a: list
                List with the intensities.
            alpha: float
                Alpha level.
        """
        if a[-1] < alpha:
            l = list(map(float, a[0][1:-1].split(',')))
            return (sum(l)/len(l))
        else:
            return np.nan
    #---
    #region --------------------------------------------------------> 
    idx = pd.IndexSlice
    label = df.columns.unique(level=0).tolist()[4:]
    nL = len(label)
    a = df.columns.tolist()[4:]
    colN = list(range(4, len(a)+4))
    #endregion -----------------------------------------------------> 

    #region --------------------------------------------------------> 
    a = (nL)*['Rec']+(nL)*['Nat']
    b = 2*label
    nR = sorted(protL, reverse=True)[0] if protL[1] is not None else protL[0]
    col = pd.MultiIndex.from_arrays([a[:],b[:]])
    dfO = pd.DataFrame(0, index=range(0,nR), columns=col) # type: ignore
    #endregion -----------------------------------------------------> 

    #region ---------------------------------------------------> 
    dfT = df.iloc[:,[0,1]+colN].copy()
    #------------------------------> 0 range for residue numbers
    dfT.iloc[:,0] = dfT.iloc[:,0]-2
    dfT.iloc[:,1] = dfT.iloc[:,1]-1
    resL = sorted(list(set(dfT.iloc[:,[0,1]].to_numpy().flatten())))
    resL = [x for x in resL if x > -1 and x < protL[0]]
    #------------------------------>
    for e in label:
        dfT.loc[:,idx[e,'Int']] = dfT.loc[:,idx[e,['Int','P']]].apply(IntL2MeanI, axis=1, raw=True, args=[alpha]) # type: ignore
    #------------------------------> 
    maxN = dfT.loc[:,idx[:,'Int']].max().max()
    minN = dfT.loc[:,idx[:,'Int']].min().min()
    if maxN != minN:
        dfT.loc[:,idx[:,'Int']] = 1 + (((dfT.loc[:,idx[:,'Int']] - minN)*(9))/(maxN - minN))
        dfT.loc[:,idx[:,'Int']] = dfT.loc[:,idx[:,'Int']].replace(np.nan, 0)
    else:
        dfT.loc[:,idx[:,'Int']] = dfT.loc[:,idx[:,'Int']].notnull().astype('int')
    #------------------------------>
    for r in resL:
        #------------------------------>
        dfG = dfT.loc[(dfT[('Nterm','Nterm')]==r) | (dfT[('Cterm','Cterm')]==r)].copy()
        #------------------------------>
        dfG = dfG.loc[dfG.loc[:,idx[:,'Int']].any(axis=1)] # type: ignore
        dfG.loc[:,idx[:,'Int']] = dfG.loc[:,idx[:,'Int']].apply(lambda x: x/x.loc[x.ne(0).idxmax()], axis=1)
        #------------------------------>
        dfO.iloc[r, range(0,len(label))] = dfG.loc[:,idx[:,'Int']].sum(axis=0)
    #endregion ------------------------------------------------> 
    
    #region ---------------------------------------------------> 
    if protL[1] is not None:
        dfT = df.iloc[:,[2,3]+colN].copy()
        #------------------------------> 0 range for residue number
        dfT.iloc[:,0] = dfT.iloc[:,0]-2
        dfT.iloc[:,1] = dfT.iloc[:,1]-1
        resL = sorted(list(set(dfT.iloc[:,[0,1]].to_numpy().flatten())))
        resL = [x for x in resL if x > -1 and x < protL[0]]
        #------------------------------> 
        for e in label:
            dfT.loc[:,idx[e,'Int']] = dfT.loc[:,idx[e,['Int','P']]].apply(IntL2MeanI, axis=1, raw=True, args=[alpha]) # type: ignore
        #------------------------------> 
        maxN = dfT.loc[:,idx[:,'Int']].max().max()
        minN = dfT.loc[:,idx[:,'Int']].min().min()
        if maxN != minN:
            dfT.loc[:,idx[:,'Int']] = 1 + (((dfT.loc[:,idx[:,'Int']] - minN)*(9))/(maxN - minN))
            dfT.loc[:,idx[:,'Int']] = dfT.loc[:,idx[:,'Int']].replace(np.nan, 0)
        else:
            dfT.loc[:,idx[:,'Int']] = dfT.loc[:,idx[:,'Int']].notnull().astype('int')    
        #------------------------------> 
        for r in resL:
            dfG = dfT.loc[(dfT[('NtermF','NtermF')]==r) | (dfT[('CtermF','CtermF')]==r)].copy()
            #------------------------------>
            dfG = dfG.loc[dfG.loc[:,idx[:,'Int']].any(axis=1)] # type: ignore
            dfG.loc[:,idx[:,'Int']] = dfG.loc[:,idx[:,'Int']].apply(lambda x: x/x.loc[x.ne(0).idxmax()], axis=1)
            #------------------------------> 
            dfO.iloc[r, range(len(label),2*len(label))] = dfG.loc[:,idx[:,'Int']].sum(axis=0)    
    else:
        pass
    #endregion ------------------------------------------------> 

    return dfO
#---


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
