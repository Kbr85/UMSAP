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
from typing import Literal, Union

import pandas as pd
from numpy import nan as nan

import dat4s_core.data.method as dtsMethod

import config.config as config
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Methods
def ResControl2ListNumber(
    val: str, sep: list[str]=[' ', ',', ';'], 
    numType: Literal['int', 'float']='int',
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
        dfE = dtsMethod.DFFilterByColN(df, [c], val, comp)
        #------------------------------> 
        n       = None
        c       = None
        seq     = None
        seqL    = []
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
                seqL.append(seq)
                np = 1
                n  = dfE.iat[r,1]
                c  = dfE.iat[r,2]
                nf = dfE.iat[r,3]
                cf = dfE.iat[r,4]
                if nf != nan and cf != nan:
                    npNat = 1
                else:
                    npNat = 0
                if nf != nan:
                    ncLNat.append(n-1)
                    nctLNat.append(n-1)
                else:
                    pass
                if cf != nan:
                    ncLNat.append(c)
                    nctLNat.append(c)
                else:
                    pass
                ncL.append(n-1)
                ncL.append(c)
                nctL.append(n-1)
                nctL.append(c)
            else:
                nc   = dfE.iat[r,1]
                cc   = dfE.iat[r,2]
                ncf  = dfE.iat[r,3]
                ccf  = dfE.iat[r,4]
                seqc = dfE.iat[r,0]
                if nc <= c:
                    seq = f'{seq}\n{(nc-n)*" "}{seqc}'
                    seqL.append(seqc)
                    np = np + 1
                    if cc > c:
                        c = cc
                    else:
                        pass
                    if ncf != nan and ccf != nan:
                        npNat = npNat + 1
                    else:
                        pass
                    if ncf != nan:
                        ncLNat.append(nc-1)
                        nctLNat.append(nc-1)
                    else:
                        pass
                    if ccf != nan:
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
                    dictO[colK]['CoordN'].append((nf,cf))
                    dictO[colK]['Seq'].append(seq)
                    dictO[colK]['SeqL'].append(seqL)
                    dictO[colK]['Np'].append(np)
                    dictO[colK]['NpNat'].append(npNat)
                    dictO[colK]['Nc'].append(len(list(set(ncL))))
                    dictO[colK]['NcNat'].append(len(list(set(ncLNat))))
                    n    = nc
                    c    = cc
                    nf   = ncf
                    cf   = ccf
                    seq  = seqc
                    seqL = [seqc]
                    np   = 1
                    if nf != nan and cf != nan:
                        npNat = 1
                    else:
                        npNat = 0
                    ncLNat = []
                    if nf != nan:
                        ncLNat.append(n-1)
                        nctLNat.append(n-1)
                    else:
                        pass
                    if cf != nan:
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
            dictO[colK]['CoordN'].append((nf,cf))
            dictO[colK]['Seq'].append(seq)
            dictO[colK]['SeqL'].append(seqL)
            dictO[colK]['Np'].append(np)
            dictO[colK]['NpNat'].append(npNat)
            dictO[colK]['Nc'].append(len(list(set(ncL))))
            dictO[colK]['NcNat'].append(len(list(set(ncLNat))))
            
            dictO[colK]['NcT'] = [len(list(set(nctL))), len(list(set(nctLNat)))]
            
            nFragN = [x for x in dictO[colK]['CoordN'] if x[0] is not nan or x[1] is not nan]
            dictO[colK]['NFrag'] = [len(dictO[colK]['Coord']), len(nFragN)]
        else:
            dictO[colK]['NcT'] = []
            dictO[colK]['NFrag'] = []
        #------------------------------> All detected peptides as a list
    #endregion ------------------------------------------------> 

    return dictO
#---


def HCurve(x:float, t0:float, s0:float) -> float:
    """Calculate the hyperbolic curve values according to:
        doi: 10.1142/S0219720012310038

        Parameters
        ----------
        

        Returns
        -------
        

        Raise
        -----
        
    """
    #region ---------------------------------------------------> Calculate
    return abs((abs(x)*t0)/(abs(x)-t0*s0))
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


def R2AA(df:pd.DataFrame, seq: str, alpha: float, pos: int=5) -> pd.DataFrame:
    """

        Parameters
        ----------
        

        Returns
        -------
        

        Raise
        -----
        
    """
    print(df.to_string())
    print(seq)
    print(alpha)
    print(pos)
    #region ---------------------------------------------------> Empty
    aL = ['AA']
    bL = ['AA']
    for l in df.columns.get_level_values(0)[1:]:
        aL = aL + 2*pos*[l]
        bL = bL + [f'{-x}' for x in range(pos, 0, -1)] + [f'{x}' for x in range(1, pos+1,1)]
    idx = pd.MultiIndex.from_arrays([aL[:],bL[:]])
    dfO = pd.DataFrame(0, columns=idx, index=config.lAA1)
    dfO[('AA','AA')] = config.lAA1[:]
    #endregion ------------------------------------------------> Empty


    #region ---------------------------------------------------> Fill
    idx = pd.IndexSlice
    for l in df.columns.get_level_values(0)[1:]:
        seqDF = df[df[idx[l,'P']] < alpha].iloc[:,0].to_list()
        for s in seqDF:
            n = seq.find(s)
            c = n+len(s)
            col = -pos
            for a,b in zip(seq[n-pos:n], seq[c-pos:c]):
                dfO.at[a,(l,f'{col}')] = dfO.at[a,(l,f'{col}')] + 1
                dfO.at[b,(l,f'{col}')] = dfO.at[b,(l,f'{col}')] + 1
                col += 1
            col = 1
            for a,b in zip(seq[n:n+pos], seq[c:c+pos]):
                dfO.at[a,(l,f'{col}')] = dfO.at[a,(l,f'{col}')] + 1
                dfO.at[b,(l,f'{col}')] = dfO.at[b,(l,f'{col}')] + 1
                col += 1
    #endregion ------------------------------------------------> Fill

    return dfO
#---
#endregion ----------------------------------------------------------> Methods
