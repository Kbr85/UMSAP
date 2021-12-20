# ------------------------------------------------------------------------------
# Copyright (C) 2017 Kenny Bravo Rodriguez <www.umsap.nl>
#
# Author: Kenny Bravo Rodriguez (kenny.bravorodriguez@mpi-dortmund.mpg.de)
#
# This program is distributed for free in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See the accompaning licence for more details.
# ------------------------------------------------------------------------------


"""Classes and methods to manipulate data """


#region -------------------------------------------------------------> Imports
import itertools
from typing import Literal

import dat4s_core.data.method as dtsMethod
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Methods
def ResControl2ListNumber(
    val: str, sep: list[str]=[' ', ',', ';'], 
    numType: Literal['int', 'float']='int',
    ) -> list[list[list[int]]]:
    """Return a list.
    
        Parameters
        ----------
        val : str
            String with the numbers. e.g. '0-4 6, 7 8 9; 10 13-15, ""; ...'
        sep : list of str
            Separators used in the string
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
        lrow = []
        #------------------------------> 
        for j in k.split(sep[1]):
            colVal = dtsMethod.Str2ListNumber(j, numType=numType, sep=sep[0])
            lrow.append(colVal)
        #------------------------------> 
        l.append(lrow)
    #endregion ----------------------------------------------------> Form list
    
    return l
#---


def ResControl2Flat(val: list[list[list[int]]]) -> list[int]:
    """Result - Control list as a flat list.

        Parameters
        ----------
        val : list of list of list of int
            Result - Control as a list of list of list of int

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
        Empty list as possible to mimic empty conditions in an experiment.
        
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
            if len(col) > 0:
                pass
            else:
                outR.append([])
                continue
            #------------------------------> 
            for k in col:
                outC.append(idx)
                idx += 1
            #------------------------------> 
            outR.append(outC)
        #------------------------------> 
        outL.append(outR)    
    #endregion -----------------------------------------------> Adjust col idx
    
    return outL
#---


def Fragments(df, val, comp, protLoc):
    """

        Parameters
        ----------
        

        Returns
        -------
        

        Raise
        -----
        
    """
    #region -----------------------------------------------------------> dictO
    dictO = {}
    #endregion --------------------------------------------------------> dictO
   
    #region ---------------------------------------------------> 
    for c in range(5, df.shape[1]):
        colK = str(df.columns.values[c])
        #------------------------------> Prepare dictO
        dictO[colK] = {}
        dictO[colK]['Coord'] = []
        dictO[colK]['Seq']   = []
        dictO[colK]['Np']    = []
        dictO[colK]['NpNat'] = []
        dictO[colK]['Nc']    = []
        dictO[colK]['NcNat'] = []
        #------------------------------> Filter df
        dfE = dtsMethod.DFFilterByColN(df, c, val, comp)
        #------------------------------> 
        n       = None
        c       = None
        seq     = None
        np      = None
        npNat   = None
        ncL     = []
        ncLNat  = []
        nctL    = []
        nctLNat = []
        #------------------------------>    
        for r in range(0, dfE.shape[0]):
            if n is None:
                seq = dfE.iat[r,0]
                np = 1
                n = dfE.iat[r,1]
                c = dfE.iat[r,2]
                if n >= protLoc[0] and c <= protLoc[1]:
                    npNat = 1
                else:
                    npNat = 0
                if n >= protLoc[0]:
                    ncLNat.append(n-1)
                    nctLNat.append(n-1)
                else:
                    pass
                if c <= protLoc[1]:
                    ncLNat.append(c)
                    nctLNat.append(c)
                else:
                    pass
                ncL.append(n-1)
                ncL.append(c)
                nctL.append(n-1)
                nctL.append(c)
            else:
                nc = dfE.iat[r,1]
                cc = dfE.iat[r,2]
                seqc = dfE.iat[r,0]
                if nc <= c:
                    seq = f'{seq}\n{(nc-n)*" "}{seqc}'
                    np = np + 1
                    if cc > c:
                        c = cc
                    else:
                        pass
                    if nc >= protLoc[0] and cc <= protLoc[1]:
                        npNat = npNat + 1
                    else:
                        pass
                    if nc >= protLoc[0]:
                        ncLNat.append(nc-1)
                        nctLNat.append(nc-1)
                    else:
                        pass
                    if cc <= protLoc[1]:
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
                    dictO[colK]['Seq'].append(seq)
                    dictO[colK]['Np'].append(np)
                    dictO[colK]['NpNat'].append(npNat)
                    dictO[colK]['Nc'].append(len(list(set(ncL))))
                    dictO[colK]['NcNat'].append(len(list(set(ncLNat))))
                    n = nc
                    c = cc
                    seq = seqc
                    np = 1
                    if n >= protLoc[0] and c <= protLoc[1]:
                        npNat = 1
                    else:
                        npNat = 0
                    ncLNat = []
                    if n >= protLoc[0]:
                        ncLNat.append(n-1)
                        nctLNat.append(n-1)
                    else:
                        pass
                    if c <= protLoc[1]:
                        ncLNat.append(c)
                        nctLNat.append(c)
                    else:
                        pass
                    ncL    = []
                    ncL.append(n-1)
                    ncL.append(c)
                    nctL.append(n-1)
                    nctL.append(c)
        #------------------------------> Catch the last line
        if n is not None:        
            dictO[colK]['Coord'].append((n,c))
            dictO[colK]['Seq'].append(seq)
            dictO[colK]['Np'].append(np)
            dictO[colK]['NpNat'].append(npNat)
            dictO[colK]['Nc'].append(len(list(set(ncL))))
            dictO[colK]['NcNat'].append(len(list(set(ncLNat))))
            dictO[colK]['Nct'] = len(list(set(nctL)))        
            dictO[colK]['NctNat'] = len(list(set(nctLNat)))        
        else:
            pass
    #endregion ------------------------------------------------> 

    return dictO
#---
#endregion ----------------------------------------------------------> Methods
