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


"""General classes and methods for data manipulation"""


#region -------------------------------------------------------------> Imports
import copy
import traceback
from datetime import datetime
from operator import itemgetter
from pathlib import Path
from typing import Literal, Union, Optional, Any

import pandas as pd
import matplotlib as mpl
import numpy as np
import wx

import config.config as config
import dtscore.exception as dtsException
import dtscore.file as dtsFF
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Numbers
def ExpandRange(
    r: str, numType: Literal['int', 'float']='int'
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

        Raise
        -----
        InputError:
            - When range in a is not properly defined
            - When numType is not in config.opt['NumType']
            
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
            raise dtsException.InputError(config.mRangeNumIE.format(r))
        #-------------->  Check a value
        if a == '':
            #--> Negative number
            try:
                return [config.oNumType[numType](tr)]
            except ValueError:
                raise dtsException.InputError(config.mRangeNumIE.format(r))
        else:
            pass
        #-------------->  Check b
        if b == '':
            #--> range like 4-
            raise dtsException.InputError(config.mRangeNumIE.format(r))
        else:
            pass
        #--------------> Expand range
        #--> Convert to int
        try:
            a = int(a)
            b = int(b)
        except ValueError:
            raise dtsException.InputError(config.mRangeNumIE.format(r))
        #--> Expand range
        if a < b:
            return [x for x in range(a, b+1, 1)]	
        else:
            raise dtsException.InputError(config.mRangeNumIE.format(r))
    else:
        #------------------------------> Positive number
        try:
            return [config.oNumType[numType](tr)]
        except ValueError:
            raise dtsException.InputError(config.mRangeNumIE.format(r))
    #endregion ----------------------------------------------> Expand & Return
#---

def MergeOverlapingFragments(
    coord:list[tuple[int, int]], delta:int=0) -> list[tuple[int, int]]:
    """Merge overlapping fragments in a list of fragments coordinates

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
        An empty list is returned if coord is empty
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
#endregion ----------------------------------------------------------> Numbers


#region -------------------------------------------------------------> Strings
def Str2ListNumber(
    tStr: str, numType: Literal['int', 'float']='int', sep: Optional[str]=',', 
    unique: bool=False) -> Union[list[int], list[float]]:
    """Turn a string into a list of numbers. Ranges are expanded as integers.

        Parameters
        ----------
        tStr: str
            The string containing the numbers and/or range of numbers (4-8)
        numType : str
            One of int, float
        sep : str or None
            The character to separate numbers in the string
        unique : boolean
            Return only unique values. Order is kept. Default is False.

        Returns
        -------
        list of numbers

        Raise
        -----
        InputError
            - When the string contains non numbers
            - When numType is not in config.opt['NumType']
        
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
            try:
                lK = ExpandRange(k, numType)
            except dtsException.InputError as e:
                raise e
            #------------------------------> Get list of numbers
            lN = lN + lK
        else:
            pass
    #endregion --------------------------------------------------> Get numbers
    
    #region ----------------------------------------------------------> Unique
    if unique:
        try:
            lo = ListRemoveDuplicates(lN)
        except Exception as e:
            raise e
    else:
        lo = lN
    #endregion -------------------------------------------------------> Unique
    
    return lo
#---

def StrSetMessage(start: str, end: str, link: str='\n\nFurther details:\n'
    ) -> str:
    """Creates a message by concatenating start and end with link.
    
        See the Examples

        Parameters
        ----------
        start: str
            Start of the message
        end : str
            End of the message
        link : str or None
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

def StrNow(dtFormat: str=config.dtFormat) -> str:
    """Get a formatted datetime.now() string.

        Returns
        -------
        str:
            The now date time as 20210112-140137	
    """
    # No test
    try:
        return datetime.now().strftime(dtFormat)
    except Exception as e:
        raise e
#---

def StrEqualLength(strL: list[str], char: str=' ', loc:str='end') -> list[str]:
    """Return a list in which every string element has the same length

        Parameters
        ----------
        strL: list[str]
            String with different length
        char: str
            Fill character. Default is empty space.
        loc: str
            Add filling character to start or end of the strings

        Returns
        -------
        list[str]
            String with the same length with the same origina order

        Raise
        -----
        
        Notes
        -----
        Filling characters are added at the end or start of each str.
    """
    #region ---------------------------------------------------> Variables
    long = len(max(strL, key=len))
    lOut = []
    #endregion ------------------------------------------------> Variables
    
    #region ---------------------------------------------------> Fill lOut
    if loc == 'end':
        for x in strL:
            space = (long-len(x))*char
            lOut.append(f'{x}{space}')
    elif loc == 'start':
        for x in strL:
            space = (long-len(x))*char
            lOut.append(f'{space}{x}')
    else:
        msg = config.mNotImplementedFull.format(
            loc, 'loc', config.oFillLoc)
        raise dtsException.ExecutionError(msg)
    #endregion ------------------------------------------------> Fill lOut

    return lOut
#---

def StrException(
    tException: Exception, tStr: bool=True, tRepr: bool=True, trace: bool=True
    ) -> str:
    """Get a string to print information about tException

        Parameters
        ----------
        tException: Exception
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

#endregion ----------------------------------------------------------> Strings


#region -------------------------------------------------------> List & Tuples
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
    try:
        return list(dict.fromkeys(l))
    except TypeError:
        msg = config.mNotIterable.format('l', l)
        raise dtsException.InputError(msg)
#---

def LCtrlFillColNames(lc: wx.ListCtrl, fileP: Path) -> bool:
    """Fill the wx.ListCtrl with the name of the columns in fileP
        
        See Notes for more details.

        Parameters
        ----------
        lc : wx.ListCtrl
            wx.ListCtrl to fill info into
        fileP : Path
            Path to the file from which to read the column names
        
        Raise
        -----
        InputError:
            - When file cannot be read.

        Notes
        -----
        This will delete the wx.ListCtrl before adding the new names.
        wx.ListCtrl is assumed to have at least two columns [#, Name,]
    """
    #region -------------------------------------------------------> Read file
    try:
        colNames = dtsFF.ReadFileFirstLine(fileP)
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
        raise dtsException.ExecutionError(msg)
    #endregion ----------------------------------------------------> Fill List
    
    return True
#---
#endregion ----------------------------------------------------> List & Tuples


#region ----------------------------------------------------------------> Dict
def DictVal2Str(
    iDict: dict, changeKey: Optional[list]=None, new: bool=False
    ) -> dict:
    """Returns a dict with values turn to str for all keys or only those in 
        changeKey
        
        Parameters
        ----------
        iDict: dict
            Initial dict
        changeKey: list of keys
            Only modify this keys
        new : boolean
            Do not modify iDict (True) or modify in place (False). 
            Default is False.

        Raises
        ------
        InputError:
            - When any key in changeKey is not present in iDict
        ExecutionError:
            - When the value for a key cannot be converted to string

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
    #region ------------------------------------------> Check input & Set keys
    if changeKey is not None:
        #------------------------------> 
        mKey = []
        #------------------------------> 
        for k in changeKey:
            try:
                iDict[k]
            except KeyError:
                mKey.append(str(k)) # avoid str error in join below
        #------------------------------> 
        if (lKey := len(mKey)) == 0:
            pass
        else:
            #------------------------------> 
            msg = f"All keys in changeKey must be present in iDict."
            #------------------------------> 
            if lKey == 1:
                msg = f"{msg} Missing key: {mKey[0]}"
            else:
                msg = f"{msg} Missing keys: {' '.join(*mKey,)}"
            #------------------------------> 
            raise dtsException.InputError(msg)
        #------------------------------> 
        keys = changeKey
    else:
        keys = iDict.keys()
    #endregion ---------------------------------------> Check input & Set keys
    
    #region -------------------------------------------------------> Variables
    if new:
        oDict = copy.deepcopy(iDict)
    else:
        oDict = iDict
    #endregion ----------------------------------------------------> Variables
    
    #region ---------------------------------------------------> Change values
    #------------------------------> 
    badKey = []
    #------------------------------> 
    for k in keys:
        try:
            oDict[k] = str(oDict[k])
        except Exception:
            badKey.append(k)
    #------------------------------> 
    if (lbadKey := len(badKey)) != 0:
        #------------------------------> 
        if lbadKey == 1:
            msg = f"The value for key {badKey[0]}"
        else:
            msg = f"The values for keys {', '.join(map(str, badKey))}"
        #------------------------------> 
        msg = f"{msg} cannot be converted to string."
        raise dtsException.ExecutionError(msg)
    else:
        pass
    #endregion ------------------------------------------------> Change values

    return oDict
#---
#endregion -------------------------------------------------------------> Dict


#region ----------------------------------------------------------> Matplotlib
def MatplotLibCmap(
    N: int=128, c1: list[int]=[255, 0, 0], c2: list[int]=[255, 255, 255], 
    c3: list[int]=[0, 0, 255], 
    bad: Union[list[int], list[float], str, None]=None):
    """ Generate custom matplotlib cmap c1->c2->c3
    
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
        Matplotlib color map

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
        raise dtsException.InputError(str(e))
    #------------------------------>  c2 -> c3
    try:
        vals2 = np.ones((N, 4))
        vals2[:, 0] = np.linspace(c2[0]/255, c3[0]/255, N)
        vals2[:, 1] = np.linspace(c2[1]/255, c3[1]/255, N)
        vals2[:, 2] = np.linspace(c2[2]/255, c3[2]/255, N)
    except Exception as e:
        raise dtsException.InputError(str(e))
    #endregion -------------------------------------------------------> Colors
    
    #region ------------------------------------------------------------> CMAP
    #------------------------------> 
    vals   = np.vstack((vals1, vals2))
    newmap = mpl.colors.ListedColormap(vals)
    #------------------------------> 
    if bad is not None:
        newmap.set_bad(color=bad)
    else:
        pass
    #endregion ---------------------------------------------------------> CMAP

    return newmap
#---
#endregion -------------------------------------------------------> Matplotlib


#region -----------------------------------------------------------> Pandas DF
def DFFilterByColS(
    df:'pd.DataFrame', col: int, refStr: str,
    comp: Literal['e', 'ne'],
    ) -> 'pd.DataFrame':
    """Filter rows in the pd.DataFrame based on the string values present in 
        col.
    
        See Notes for more details.

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

        Raise
        -----
        InputError :
            - When col is not an integer
            - When col is not found in df
            - When comp is not one of the valid options
        NotYetImplement : 
            - When comp is in config.oStrComp but the option has not being 
            implemented here
            
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
    try:
        if comp == 'e':
            dfo = df.loc[df.iloc[:,col] == refStr]
        elif comp == 'ne':
            dfo = df.loc[df.iloc[:,col] != refStr]
        else:
            msg = config.mCompNYI.format(comp)
            raise dtsException.NotYetImplementedError(msg)
    except Exception:
        raise dtsException.ExecutionError(config.mPDFilterByCol)
    #endregion -------------------------------------------------------> Filter
    
    return dfo
#---

def DFFilterByColN(
    df:'pd.DataFrame', col: list[int], refVal: float,
    comp: Literal['lt', 'le', 'e', 'ge', 'gt'],
    ) -> 'pd.DataFrame':
    """Filter rows in the pd.DataFrame based on the numeric values present in 
        col.
    
        See Notes for more details.

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

        Raise
        -----
        InputError :
            - When col is not an integer
            - When col is not found in df
            - When comp is not one of the valid options
        NotYetImplement : 
            - When comp is in dtsConfig.oNumComp but the option has not being 
            implemented here
            
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
    try:
        if comp == 'lt':
            dfo = df.loc[(df.iloc[:,col] < refVal).any(axis=1)]
        elif comp == 'le':
            dfo = df.loc[(df.iloc[:,col] <= refVal).any(axis=1)]
        elif comp == 'e':
            dfo = df.loc[(df.iloc[:,col] == refVal).any(axis=1)]
        elif comp == 'ge':
            dfo = df.loc[(df.iloc[:,col] >= refVal).any(axis=1)]
        elif comp == 'gt':
            dfo = df.loc[(df.iloc[:,col] > refVal).any(axis=1)]
        else:
            msg = config.mCompNYI.format(comp)
            raise dtsException.NotYetImplementedError(msg)
    except Exception:
        raise dtsException.ExecutionError(config.mPDFilterByCol)
    #endregion -------------------------------------------------------> Filter
    
    return dfo
#---

def DFReplace(
    df: 'pd.DataFrame', oriVal: list, repVal: Union[list, Any], 
    sel: Optional[list[int]]=None,
    ) -> 'pd.DataFrame':
    """Replace values in the dataframe
    
        See Notes below for more details.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe with the data
        oriVal: list
            List of values to search and replace
        repVal: list or single value
            List of values to use as replacement. When only one value is given
            all oriVal are replace with the given value
        sel : list of int
            Column indexes

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
        if len(oriVal) != len(repVal):
            msg = f"The lengths of oriVal and repVal do not match."
            raise dtsException.InputError(msg)
        else:
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
            try:
                dfo.iloc[:,sel] = dfo.iloc[:,sel].replace(v, rep)
            except Exception:
                msg = config.mpdReplaceVal.format(v, rep)
                raise dtsException.ExecutionError(msg)
        else:
            try:
                dfo = dfo.replace(v, rep)
            except Exception:
                msg = config.mpdReplaceVal.format(v, rep)
                raise dtsException.ExecutionError(msg)
    #endregion ------------------------------------------------------> Replace
    
    return dfo
#---

def DFExclude(df:'pd.DataFrame', col: list[int]) -> 'pd.DataFrame':
    """Exclude rows in the pd.DataFrame based on the values present in col.
    
        See Notes for more details.

        Parameters
        ----------
        df: pd.DataFrame
        col : list[int]

        Returns
        -------
        pd.DataFrame

        Raise
        -----
        InputError :
            - When selection is not found in df
            
        Notes
        -----
        Rows with at least one value other than NA in the given columns are 
        discarded
    """
    #region ----------------------------------------------------------> Exclude
    #------------------------------>  Copy
    dfo = df.copy()
    #------------------------------> Exclude
    try:
        a = dfo.iloc[:,col].notna()
        a = a.loc[(a==True).any(axis=1)]
        idx = a.index
        dfo = dfo.drop(index=idx)
    except Exception:
        raise dtsException.ExecutionError(config.mPDExcludeCol)
    #endregion -------------------------------------------------------> Exclude
    
    return dfo
#---

#endregion --------------------------------------------------------> Pandas DF
