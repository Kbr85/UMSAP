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
import copy
import itertools
import traceback
from collections import namedtuple
from datetime    import datetime
from operator    import itemgetter
from pathlib     import Path
from typing      import Union, Optional

import numpy      as np
import matplotlib as mpl
import pandas     as pd
from scipy                       import stats
from statsmodels.stats.multitest import multipletests

from reportlab.lib.pagesizes import A4
from reportlab.platypus      import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles    import getSampleStyleSheet, ParagraphStyle

import config.config  as mConfig
import data.exception as mException
import data.file      as mFile
import data.statistic as mStatistic
#endregion ----------------------------------------------------------> Imports


# Pandas lead to long lines, so this check will be disabled for this module
# pylint: disable=line-too-long


#region ------------------------------------------------------> String methods
def StrEqualLength(
    strL: list[str],
    char: str=' ',
    loc : mConfig.litStartEnd='end',
    ) -> list[str]:
    """Return a list in which every string element has the same length.

        Parameters
        ----------
        strL: list[str]
            String with different length.
        char: str
            Fill character. Default is empty space ' '.
        loc: str
            Add filling character to start or end of the strings.

        Returns
        -------
        list[str]
            String with the same length with the same original order.

        Notes
        -----
        Filling characters are added at the end or start of each str.
    """
    # Test in test.unit.test_method.Test_StrEqualLength
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
        msg = mConfig.mNotImplementedFull.format(
            loc, 'loc', mConfig.litStartEnd)
        raise mException.InputError(msg)
    #endregion ------------------------------------------------> Fill lOut

    return lOut
#---
#endregion ---------------------------------------------------> String methods


#region -------------------------------------------------------------> Methods
def MatplotLibCmap(
    N  : int                                    = 128,
    c1 : tuple[int, int, int]                   = (255, 0, 0),
    c2 : tuple[int, int, int]                   = (255, 255, 255),
    c3 : tuple[int, int, int]                   = (0, 0, 255),
    bad: Union[tuple[float, float, float], str] = '',
    ):
    """Generate custom matplotlib cmap c1->c2->c3.

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
    newMap = mpl.colors.ListedColormap(vals)                                    # type: ignore
    #------------------------------>
    if bad is not None:
        newMap.set_bad(color=bad)
    #endregion ---------------------------------------------------------> CMAP

    return newMap
#---


def Fragments(
    df     : 'pd.DataFrame',
    val    : float,
    comp   : mConfig.litComp,
    protL  : int,
    protLoc: list[int],
    ) -> dict:
    """Creates the dict holding the fragments identified in the analysis.

        Parameters
        ----------
        df: pd.DataFrame with the data from the analysis. The columns in df are
            expected to be:
            Seq Nrec Crec Nnat Cnat Exp1 Exp2 ...... ExpN
            Seq Nrec Crec Nnat Cnat    P    P           P
        val : float
            Threshold value to filter df and identify relevant peptides
        comp : str
            One of 'lt', 'le', 'e', 'ge', 'gt'
        protL: int
            Length of recombinant protein.
        protLoc: list[int]
            Location of the native protein in the recombinant sequence

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
    # Test in test.unit.test_method.Test_Fragments
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
        #------------------------------> Total cleavages for the experiment
        nctL    = []
        nctLNat = []
        #------------------------------> First row
        if dfE.shape[0] > 0:
            #------------------------------> Values from dfE
            seq     = dfE.iat[0,0]
            n       = dfE.iat[0,1]
            c       = dfE.iat[0,2]
            nf      = dfE.iat[0,3]
            cf      = dfE.iat[0,4]
            ncL     = []
            ncLNat  = []
            #------------------------------>
            seqL = [seq]
            #------------------------------> Number of peptides
            nP = 1
            if pd.isna(nf) and pd.isna(cf):
                npNat = 0
            else:
                npNat = 1
            #------------------------------> Cleavages Rec
            if n != 1:
                ncL.append(n-1)
                nctL.append(n-1)
            if c != protL:
                ncL.append(c)
                nctL.append(c)
            #------------------------------> Cleavages Nat
            if not pd.isna(nf):
                if nf != 1:
                    ncLNat.append(nf-1)
                    nctLNat.append(nf-1)
            if not pd.isna(cf):
                if cf != protL != protLoc[1]:
                    ncLNat.append(cf)
                    nctLNat.append(cf)
        else:
            dictO[colK]['NcT'] = []
            dictO[colK]['NFrag'] = []
            continue
        #------------------------------> Other rows
        for r in range(1, dfE.shape[0]):
            #------------------------------> Values from dfE
            seqC = dfE.iat[r,0]
            nc   = dfE.iat[r,1]
            cc   = dfE.iat[r,2]
            ncf  = dfE.iat[r,3]
            ccf  = dfE.iat[r,4]
            if nc <= c:
                #------------------------------>
                seq = f'{seq}\n{(nc-n)*" "}{seqC}'
                seqL.append(seqC)
                #------------------------------> Number of peptides
                nP = nP + 1
                if not pd.isna(ncf) and not pd.isna(ccf):
                    npNat = npNat + 1
                #------------------------------> Cleavages Rec
                if nc != 1:
                    ncL.append(nc-1)
                    nctL.append(nc-1)
                if cc != protL:
                    ncL.append(cc)
                    nctL.append(cc)
                #------------------------------> Cleavages Nat
                if not pd.isna(ncf):
                    if ncf != 1:
                        ncLNat.append(nc-1)
                        nctLNat.append(nc-1)
                if not pd.isna(ccf):
                    if ccf != protL != protLoc[1]:
                        ncLNat.append(ccf)
                        nctLNat.append(ccf)
                #------------------------------> Update c residue
                if cc > c:
                    c = cc
                    cf = ccf
            else:
                #------------------------------> Add Fragment
                dictO[colK]['Coord'].append((n,c))
                dictO[colK]['CoordN'].append((nf,cf))
                dictO[colK]['Seq'].append(seq)
                dictO[colK]['SeqL'].append(seqL)
                dictO[colK]['Np'].append(nP)
                dictO[colK]['NpNat'].append(npNat)
                dictO[colK]['Nc'].append(len(set(ncL)))
                dictO[colK]['NcNat'].append(len(set(ncLNat)))
                #------------------------------> Start new Fragment
                seq     = seqC
                n       = nc
                c       = cc
                nf      = ncf
                cf      = ccf
                ncL     = []
                ncLNat  = []
                #------------------------------>
                seqL = [seqC]
                #------------------------------> Number of peptides
                nP   = 1
                if pd.isna(nf) and pd.isna(cf):
                    npNat = 0
                else:
                    npNat = 1
                #------------------------------> Cleavages Rec
                if n != 1:
                    ncL.append(n-1)
                    nctL.append(n-1)
                if c != protL:
                    ncL.append(c)
                    nctL.append(c)
                #------------------------------> Cleavages Nat
                if not pd.isna(nf):
                    if nf != 1:
                        ncLNat.append(nf-1)
                        nctLNat.append(nf-1)
                if not pd.isna(cf):
                    if cf != protL != protLoc[1]:
                        ncLNat.append(cf)
                        nctLNat.append(cf)
        #------------------------------> Catch the last line
        dictO[colK]['Coord'].append((n,c))
        dictO[colK]['CoordN'].append((nf,cf))
        dictO[colK]['Seq'].append(seq)
        dictO[colK]['SeqL'].append(seqL)
        dictO[colK]['Np'].append(nP)
        dictO[colK]['NpNat'].append(npNat)
        dictO[colK]['Nc'].append(len(set(ncL)))
        dictO[colK]['NcNat'].append(len(set(ncLNat)))
        #------------------------------>
        dictO[colK]['NcT'] = [len(set(nctL)), len(set(nctLNat))]
        #------------------------------>
        nFragN = [x for x in dictO[colK]['CoordN'] if not pd.isna(x[0]) or not pd.isna(x[1])]
        dictO[colK]['NFrag'] = [len(dictO[colK]['Coord']), len(nFragN)]
    #endregion ------------------------------------------------>

    return dictO
#---


def MergeOverlappingFragments(
    coord: list[tuple[int, int]],
    delta: int=0,
    ) -> list[tuple[int, int]]:
    """Merge overlapping fragments in a list of fragments coordinates.

        Parameters
        ----------
        coord: list[tuple[int, int]]
            Fragment coordinates lists.
        delta: int
            To adjust the merging of adjacent fragments.

        Returns
        -------
        list[tuple[int, int]]

        Notes
        -----
        An empty list is returned if coord is empty.
    """
    # Test in test.unit.test_method.Test_MergeOverlappingFragments
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
        x: float, pd.DataFrame or pd.Series
            X value of the Hyperbolic Curve.
        t0: float
            T0 parameter.
        s0: float
            S0 parameter.

        Returns
        -------
        float
    """
    # No test
    #region ---------------------------------------------------> Calculate
    return abs((abs(x)*t0)/(abs(x)-t0*s0))                                      # type: ignore
    #endregion ------------------------------------------------> Calculate
#---


def TarProt(
    df        : pd.DataFrame,
    rDO       : dict,
    rDExtra   : dict,
    resetIndex: bool=True,
    ) -> tuple[dict, str, Optional[Exception]]:
    """Perform a Limited Proteolysis analysis.

        Parameters
        ----------
        df: pd.DataFrame
            DataFrame read from CSV file.
        rDO: dict
            rDO dictionary from the PrepareRun step of the analysis.
        rDExtra: dict
            Extra parameters.
        resetIndex: bool
            Reset index of dfS (True) or not (False). Default is True.

        Returns
        -------
        tuple:
            -   (
                    {
                        'dfI' : pd.DataFrame,
                        'dfF' : pd.DataFrame,
                        'dfT' : pd.DataFrame,
                        'dfN' : pd.DataFrame,
                        'dfIm': pd.DataFrame,
                        'dfTP': pd.DataFrame,
                        'dfE' : pd.DataFrame,
                        'dfS' : pd.DataFrame,
                        'dfR' : pd.DataFrame,
                    },
                    '',
                    None
                )                                  when everything went fine.
            -   ({}, 'Error message', Exception)   when something went wrong.
    """
    # Test in test.unit.test_method.Test_TarProt
    #region ------------------------------------------------> Helper Functions
    def EmptyDFR() -> pd.DataFrame:
        """Creates the empty df for the results.

            Returns
            -------
            pd.DataFrame
        """
        #region -------------------------------------------------------> Index
        aL = rDExtra['cLDFFirst']
        bL = rDExtra['cLDFFirst']
        n = len(rDExtra['cLDFSecond'])
        #------------------------------> Ctrl
        aL = aL + n*rDO['ControlL']
        bL = bL + rDExtra['cLDFSecond']
        #------------------------------> Exp
        for exp in rDO['Exp']:
            aL = aL + n*[exp]
            bL = bL + rDExtra['cLDFSecond']
        #------------------------------>
        idx = pd.MultiIndex.from_arrays([aL[:], bL[:]])
        #endregion ----------------------------------------------------> Index

        #region ----------------------------------------------------> Empty DF
        df = pd.DataFrame(
            np.nan, columns=idx, index=range(dfS.shape[0]),                     # type: ignore
        )
        idx = pd.IndexSlice
        df.loc[:,idx[:,'Int']] = df.loc[:,idx[:,'Int']].astype('object')        # type: ignore
        #endregion -------------------------------------------------> Empty DF

        #region -------------------------------------------------> Seq & Score
        df[aL[0]] = dfS.iloc[:,0]
        df[aL[1]] = dfS.iloc[:,2]
        df[(rDO['ControlL'][0], 'P')] = np.nan
        #endregion ----------------------------------------------> Seq & Score

        return df
    #---

    def PrepareAncova(
        rowC: int,
        row : namedtuple,                                                       # type: ignore
        rowN: int
        ) -> pd.DataFrame:
        """Prepare the dataframe used to perform the ANCOVA test and add the
            intensity to self.dfR.

            Parameters
            ----------
            rowC: int
                Current row index in self.dfR.
            row: namedtuple
                Row from self.dfS.
            rowN: int
                Maximum number of rows in the output pd.df.

            Returns
            -------
            pd.DataFrame
                Dataframe to use in the ANCOVA test
                Xc1, Yc1, Xe1, Ye1,....,XcN, YcN, XeN, YeN
        """
        #region ---------------------------------------------------> Variables
        dfAncova = pd.DataFrame(index=range(0,rowN))
        xC  = []
        xCt = []
        yC  = []
        #endregion ------------------------------------------------> Variables

        #region --------------------------------------------------->
        #------------------------------> Control
        #--------------> List
        for r in rDO['df']['ResCtrl'][0][0]:
            if np.isfinite(row[r]):
                xC.append(1)
                xCt.append(5)
                yC.append(row[r])
            else:
                pass
        #--------------> Add to self.dfR
        dfR.at[rowC,(rDO['ControlL'],'Int')] = str(yC)
        #------------------------------> Points
        for k,r in enumerate(rDO['df']['ResCtrl'][1:], start=1):
            #------------------------------>
            xE = []
            yE = []
            #------------------------------>
            for rE in r[0]:
                if np.isfinite(row[rE]):
                    xE.append(5)
                    yE.append(row[rE])
                else:
                    pass
            #------------------------------>
            dfR.at[rowC,(rDO['Exp'][k-1], 'Int')] = str(yE)
            #------------------------------>
            a = xC + xCt
            b = yC + yC
            c = xC + xE
            d = yC + yE
            #------------------------------>
            dfAncova.loc[range(0, len(a)),f'Xc{k}'] = a                         # type: ignore
            dfAncova.loc[range(0, len(b)),f'Yc{k}'] = b                         # type: ignore
            dfAncova.loc[range(0, len(c)),f'Xe{k}'] = c                         # type: ignore
            dfAncova.loc[range(0, len(d)),f'Ye{k}'] = d                         # type: ignore
        #endregion ------------------------------------------------>
        return dfAncova
    #---
    #endregion ---------------------------------------------> Helper Functions

    #region ------------------------------------------------> Data Preparation
    tOut = mStatistic.DataPreparation(df, rDO, resetIndex=resetIndex)
    if tOut[0]:
        dfS = tOut[0]['dfS']
    else:
        return tOut
    #endregion ---------------------------------------------> Data Preparation

    #region --------------------------------------------------------> Analysis
    #------------------------------> Empty dfR
    dfR = EmptyDFR()
    #------------------------------> N, C Res Num
    dfR, msgError, tException = NCResNumbers(
        dfR, rDO, rDExtra['rSeqFileObj'], seqNat=True)
    if dfR.empty:
        return ({}, msgError, tException)
    else:
        pass
    #------------------------------> P values
    # totalPeptide = len(dfS)
    totalRowAncovaDF = 2*max([len(x[0]) for x in rDO['df']['ResCtrl']])
    nGroups = [2 for x in rDO['df']['ResCtrl']]
    nGroups = nGroups[1:]
    idx = pd.IndexSlice
    idx = idx[rDO['Exp'], 'P']
    #-------------->
    k = 0
    for row in dfS.itertuples(index=False):
        try:
            #------------------------------> Ancova df & Int
            dfAncova = PrepareAncova(k, row, totalRowAncovaDF)
            #------------------------------> P value
            dfR.loc[k,idx] = mStatistic.Test_slope(dfAncova, nGroups)           # type: ignore
        except Exception as e:
            msg = (f'P value calculation failed for peptide {row[0]}.')
            return ({}, msg, e)
        #------------------------------>
        k = k + 1
    #endregion -----------------------------------------------------> Analysis

    #region -------------------------------------------------> Check P < a
    idx = pd.IndexSlice
    if (dfR.loc[:,idx[:,'P']] < rDO['Alpha']).any().any():                      # type: ignore
        pass
    else:
        msg = ('There were no peptides detected with intensity '
            'values significantly higher to the intensity values in the '
            'controls. You may run the analysis again with different '
            'values for the configuration options.')
        return ({}, msg, None)
    #endregion ----------------------------------------------> Check P < a

    #region --------------------------------------------------------> Sort
    dfR = dfR.sort_values(by=[('Nterm', 'Nterm'),('Cterm', 'Cterm')])           # type: ignore
    dfR = dfR.reset_index(drop=True)
    #endregion -----------------------------------------------------> Sort

    dictO = tOut[0]
    dictO['dfR'] = dfR
    return (dictO, '', None)
#---


def Rec2NatCoord(
    coord  : list[tuple[int,int]],
    protLoc: tuple[int,int],
    delta  : int,
    ) -> Union[list[tuple[int,int]], list[str]]:
    """Translate residue numbers from the recombinant sequence to the native
        sequence.

        Parameters
        ----------
        coord: list of tuples(int, int)
            Residue numbers in the recombinant sequence.
        protLoc: tuple(int, int)
            Location of the native protein in the recombinant sequence.
        delta: int
            Difference in residue numbers.

        Returns
        -------
        list of tuples(int. int)
            Residue number in the native sequence.

        Notes
        -----
        Returns ['NA'] if delta is None or any of the protLoc items is None.

        Examples
        --------
        >>> Rec2NatCoord([(1,42), (38, 50), (201, 211), (247, 263)], (10, 300)), 10)
        >>> [(48, 60), (211, 221), (257, 273)]
        >>> Rec2NatCoord([(1,42), (38, 50), (201, 211), (247, 263)], (100, 230)), 10)
        >>> [(211, 221)]
    """
    # Test in test.unit.test_method.Test_Rec2NatCoord
    #region ---------------------------------------------------> Return NA
    if delta is None or protLoc[0] is None or protLoc[1] is None:
        return ['NA']
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
    df   : pd.DataFrame,
    seq  : str,
    alpha: float,
    protL: int,
    pos  : int=5,
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
    # Test in test.unit.test_method.Test_R2AA
    #region ---------------------------------------------------> Helper Method
    def AddNewAA(
        dfO: pd.DataFrame,
        r  : int,
        pos: int,
        seq: str,
        l  : str
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
    #endregion ------------------------------------------------> Helper Method

    #region ---------------------------------------------------> Empty
    aL = ['AA']
    bL = ['AA']
    for l in df.columns.get_level_values(0)[1:]:
        aL = aL + 2*pos*[l]
        bL = bL + [f'P{x}' for x in range(pos, 0, -1)] + [f'P{x}\'' for x in range(1, pos+1,1)]
    idx = pd.MultiIndex.from_arrays([aL[:],bL[:]])
    dfO = pd.DataFrame(0, columns=idx, index=mConfig.lAA1+['Chi'])              # type: ignore
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
            #------------------------------>
            c = n+len(s)
            if c < protL:
                dfO = AddNewAA(dfO, c, pos, seq, l)
    #endregion ------------------------------------------------> Fill

    #region ---------------------------------------------------> Random Cleavage
    c   = 'ALL_CLEAVAGES_UMSAP'
    aL  = 2*pos*[c]
    bL  = [f'P{x}' for x in range(pos, 0, -1)] + [f"P{x}'" for x in range(1, pos+1,1)]
    idx = pd.MultiIndex.from_arrays([aL[:],bL[:]])
    dfT = pd.DataFrame(0, columns=idx, index=mConfig.lAA1+['Chi'])              # type: ignore
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
        for p in dfO.loc[:,idx[l,:]].columns.get_level_values(1):               # type: ignore
            dfO.at['Chi', idx[l,p]] = mStatistic.Test_chi(
                g.loc[:,idx[[l,c],p]], alpha)[0]                                # type: ignore
    #endregion ------------------------------------------------> Group

    return dfO
#---


def R2Hist(
    df   : pd.DataFrame,
    alpha: float,
    win  : list[int],
    maxL : list[int]
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
    # Test in test.unit.test_method.Test_R2Hist
    #region ---------------------------------------------------> Variables
    tBin = []
    if len(win) == 1:
        tBin.append(list(range(0, maxL[0]+win[0], win[0])))
        if maxL[1] is not None:
            tBin.append(list(range(0, maxL[1]+win[0], win[0])))
        else:
            tBin.append([None])
    else:
        tBin.append(win)
        tBin.append(win)
    #endregion ------------------------------------------------> Variables

    #region --------------------------------------------------------> Empty DF
    #------------------------------> Columns
    label = df.columns.unique(level=0).tolist()[4:]
    nL    = len(label)
    a     = (2*nL+1)*['Rec']+(2*nL+1)*['Nat']
    b     = ['Win']+nL*['All']+nL*['Unique']+['Win']+nL*['All']+nL*['Unique']
    c     = 2*(['Win']+2*label)
    #------------------------------> Rows
    nR = sorted([len(x) for x in tBin])[-1]
    #------------------------------> df
    col = pd.MultiIndex.from_arrays([a[:],b[:],c[:]])
    dfO = pd.DataFrame(np.nan, index=range(0,nR), columns=col)                  # type: ignore
    #endregion -----------------------------------------------------> Empty DF

    #region ---------------------------------------------------> Fill
    #------------------------------> Windows
    dfO.iloc[range(0,len(tBin[0])), dfO.columns.get_loc(('Rec','Win','Win'))] = tBin[0]             # type: ignore
    if tBin[1][0] is not None:
        dfO.iloc[range(0,len(tBin[1])), dfO.columns.get_loc(('Nat','Win','Win'))] = tBin[1]         # type: ignore
    #------------------------------>
    for e in label:
        dfT = df[df[(e,'P')] < alpha]
        #------------------------------>
        dfR = dfT[[('Nterm','Nterm'),('Cterm', 'Cterm')]].copy()
        dfR[('Nterm','Nterm')] = dfR[('Nterm','Nterm')] - 1
        l = dfR.to_numpy().flatten()
        l = [x for x in l if x > 0 and x < maxL[0]]
        a,_ = np.histogram(l, bins=tBin[0])
        dfO.iloc[range(0,len(a)),dfO.columns.get_loc(('Rec','All',e))] = a      # type: ignore
        l = list(set(l))
        a,_ = np.histogram(l, bins=tBin[0])
        dfO.iloc[range(0,len(a)),dfO.columns.get_loc(('Rec','Unique',e))] = a   # type: ignore
        #------------------------------>
        if tBin[1][0] is not None:
            dfR = dfT[[('NtermF','NtermF'),('CtermF', 'CtermF')]].copy()
            dfR[('NtermF','NtermF')] = dfR[('NtermF','NtermF')] - 1
            l = dfR.to_numpy().flatten()
            l = [x for x in l if not pd.isna(x) and x > 0 and x < maxL[1]]
            a,_ = np.histogram(l, bins=tBin[0])
            dfO.iloc[range(0,len(a)),dfO.columns.get_loc(('Nat','All',e))] = a  # type: ignore
            l = list(set(l))
            a,_ = np.histogram(l, bins=tBin[0])
            dfO.iloc[range(0,len(a)),dfO.columns.get_loc(('Nat','Unique',e))] = a                   # type: ignore
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
    # Test in test.unit.test_method.Test_R2CpR
    #region -------------------------------------------------------------> dfO
    label = df.columns.unique(level=0).tolist()[4:]
    nL    = len(label)
    a     = (nL)*['Rec']+(nL)*['Nat']
    b     = 2*label
    nR    = sorted(protL, reverse=True)[0] if protL[1] is not None else protL[0]
    idx   = pd.IndexSlice
    col   = pd.MultiIndex.from_arrays([a[:],b[:]])
    dfO   = pd.DataFrame(0, index=range(0,nR), columns=col)                       # type: ignore
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
        lastR = protL[0] - 1
        l = [x for x in l if x > -1 and x < lastR]
        for x in l:
            dfO.at[x, idx['Rec',e]] = dfO.at[x, idx['Rec',e]] + 1
        #------------------------------> Nat
        if protL[1] is not None:
            dfR = dfT[[('NtermF','NtermF'),('CtermF', 'CtermF')]].copy()
            #------------------------------> 0 based residue number
            dfR[('NtermF','NtermF')] = dfR[('NtermF','NtermF')] - 2
            dfR[('CtermF','CtermF')] = dfR[('CtermF','CtermF')] - 1
            l = dfR.to_numpy().flatten()
            # No Cleavage in 1 and last residue
            lastR = protL[1] - 1
            l = [x for x in l if not pd.isna(x) and x > -1 and x < lastR]
            for x in l:
                dfO.at[x, idx['Nat',e]] = dfO.at[x, idx['Nat',e]] + 1
    #endregion ---------------------------------------------------------> Fill

    return dfO
#---


def R2CEvol(df: pd.DataFrame, alpha: float, protL: list[int]) -> pd.DataFrame:
    """Creates the cleavage evolution DataFrame.

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
    # Test in test.unit.test_method.Test_R2CEvol
    #region -------------------------------------------------> Helper Function
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
        #------------------------------>
        return np.nan
    #---
    #endregion ----------------------------------------------> Helper Function

    #region -------------------------------------------------------->
    idx   = pd.IndexSlice
    label = df.columns.unique(level=0).tolist()[4:]
    nL    = len(label)
    a     = df.columns.tolist()[4:]
    colN  = list(range(4, len(a)+4))
    #endregion ----------------------------------------------------->

    #region -------------------------------------------------------->
    a   = (nL)*['Rec']+(nL)*['Nat']
    b   = 2*label
    nR  = sorted(protL, reverse=True)[0] if protL[1] is not None else protL[0]
    col = pd.MultiIndex.from_arrays([a[:],b[:]])
    dfO = pd.DataFrame(0, index=range(0,nR), columns=col)                                                               # type: ignore
    #endregion ----------------------------------------------------->

    #region --------------------------------------------------->
    dfT = df.iloc[:,[0,1]+colN].copy()
    #------------------------------> 0 range for residue numbers
    dfT.iloc[:,0] = dfT.iloc[:,0]-2
    dfT.iloc[:,1] = dfT.iloc[:,1]-1
    resL  = sorted(list(set(dfT.iloc[:,[0,1]].to_numpy().flatten())))
    lastR = protL[0] - 1
    resL  = [x for x in resL if x > -1 and x < lastR]
    #------------------------------>
    for e in label:
        dfT.loc[:,idx[e,'Int']] = dfT.loc[:,idx[e,['Int','P']]].apply(IntL2MeanI, axis=1, raw=True, args=[alpha])       # type: ignore
    #------------------------------>
    maxN = dfT.loc[:,idx[:,'Int']].max().max()                                                                          # type: ignore
    minN = dfT.loc[:,idx[:,'Int']].min().min()                                                                          # type: ignore
    if maxN != minN:
        dfT.loc[:,idx[:,'Int']] = 1 + (((dfT.loc[:,idx[:,'Int']] - minN)*(9))/(maxN - minN))                            # type: ignore
        dfT.loc[:,idx[:,'Int']] = dfT.loc[:,idx[:,'Int']].replace(np.nan, 0)                                            # type: ignore
    else:
        dfT.loc[:,idx[:,'Int']] = dfT.loc[:,idx[:,'Int']].notnull().astype('int')                                       # type: ignore
    #------------------------------>
    for r in resL:
        #------------------------------>
        dfG = dfT.loc[(dfT[('Nterm','Nterm')]==r) | (dfT[('Cterm','Cterm')]==r)].copy()
        #------------------------------>
        dfG = dfG.loc[dfG.loc[:,idx[:,'Int']].any(axis=1)]                                                              # type: ignore
        dfG.loc[:,idx[:,'Int']] = dfG.loc[:,idx[:,'Int']].apply(lambda x: x/x.loc[x.ne(0).idxmax()], axis=1)            # type: ignore
        #------------------------------>
        dfO.iloc[r, range(0,len(label))] = dfG.loc[:,idx[:,'Int']].sum(axis=0)                                          # type: ignore
    #endregion ------------------------------------------------>

    #region --------------------------------------------------->
    if protL[1] is not None:
        dfT = df.iloc[:,[2,3]+colN].copy()
        #------------------------------> 0 range for residue number
        dfT.iloc[:,0] = dfT.iloc[:,0]-2
        dfT.iloc[:,1] = dfT.iloc[:,1]-1
        resL = list(set(dfT.iloc[:,[0,1]].to_numpy().flatten()))
        lastR = protL[1] - 1
        resL = [x for x in resL if not pd.isna(x) and x > -1 and x < lastR]
        resL = sorted(resL)
        #------------------------------>
        for e in label:
            dfT.loc[:,idx[e,'Int']] = dfT.loc[:,idx[e,['Int','P']]].apply(IntL2MeanI, axis=1, raw=True, args=[alpha])   # type: ignore
        #------------------------------>
        maxN = dfT.loc[:,idx[:,'Int']].max().max()                                                                      # type: ignore
        minN = dfT.loc[:,idx[:,'Int']].min().min()                                                                      # type: ignore
        if maxN != minN:
            dfT.loc[:,idx[:,'Int']] = 1 + (((dfT.loc[:,idx[:,'Int']] - minN)*(9))/(maxN - minN))                        # type: ignore
            dfT.loc[:,idx[:,'Int']] = dfT.loc[:,idx[:,'Int']].replace(np.nan, 0)                                        # type: ignore
        else:
            dfT.loc[:,idx[:,'Int']] = dfT.loc[:,idx[:,'Int']].notnull().astype('int')                                   # type: ignore
        #------------------------------>
        for r in resL:
            dfG = dfT.loc[(dfT[('NtermF','NtermF')]==r) | (dfT[('CtermF','CtermF')]==r)].copy()
            #------------------------------>
            dfG = dfG.loc[dfG.loc[:,idx[:,'Int']].any(axis=1)]                                                          # type: ignore
            dfG.loc[:,idx[:,'Int']] = dfG.loc[:,idx[:,'Int']].apply(lambda x: x/x.loc[x.ne(0).idxmax()], axis=1)        # type: ignore
            #------------------------------>
            dfO.iloc[r, range(len(label),2*len(label))] = dfG.loc[:,idx[:,'Int']].sum(axis=0)                           # type: ignore
    #endregion ------------------------------------------------>

    return dfO
#---


def R2SeqAlignment(
    df     : pd.DataFrame,
    alpha  : float,
    seqR   : str,
    fileP  : 'Path',
    tLength: int,
    seqN   : str='',
    ) -> bool:
    """Sequence Alignment for the TarProt Module.

        Parameters
        ----------
        df: pd.DataFrame
            Full LimProt/TarProt DataFrame.
        alpha: float
            Significance level.
        seqR: str
            Sequence of the recombinant protein.
        seqN: str
            Sequence of the native protein.
        fileP: Path
            Output file path.
        tLength: int
            Residues per line.

        Returns
        -------
        bool
    """
    # No Test
    #region -------------------------------------------------> Helper Function
    def GetString(
        df   : pd.DataFrame,
        seq  : str,
        rec  : bool,
        alpha: float,
        label: str,
        lSeq : int,
        ) -> tuple[int, list[str]]:
        """Get line text.

            Parameters
            ----------
            df: pd.DataFrame
                Full LimProt/TarProt DataFrame.
            seq: str
                Sequence.
            rec: bool
                True if sequence is for the recombinant protein or False.
            alpha: float
                Significance level.
            label: str
                Experiment label.
            lSeq: int
                Length of the recombinant sequence.

            Returns
            -------
            tuple(int, list[str])
        """
        #region -------------------------------------------------------->
        idx     = pd.IndexSlice
        df      = df[df.loc[:,idx[label,'P']] <= alpha].copy()                       # type: ignore
        df      = df.reset_index(drop=True)
        nCero   = len(str(df.shape[0]+1))
        tString = [seq]
        #endregion ----------------------------------------------------->

        #region --------------------------------------------------->
        for r in df.itertuples():
            n = r[3] if rec else r[5]
            tString.append((n-1)*' '+r[1]+(lSeq-n+1-len(r[1]))*' ')
        #endregion ------------------------------------------------>
        return (nCero, tString)
    #---
    #endregion ----------------------------------------------> Helper Function

    #region ---------------------------------------------------> Variables
    label   = df.columns.unique(level=0)[7:].tolist()
    lenSeqR = len(seqR)
    lenSeqN = len(seqN) if seqN else 0
    end     = 0
    #------------------------------> ReportLab
    doc = SimpleDocTemplate(fileP, pagesize=A4, rightMargin=25,
        leftMargin=25, topMargin=25, bottomMargin=25)
    Story  = []
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Seq', fontName='Courier', fontSize=8.5))
    #endregion ------------------------------------------------> Variables

    #region --------------------------------------------------->
    for e in label:
        #------------------------------>
        Story.append(Paragraph(f'{e} Recombinant Sequence'))
        Story.append(Spacer(1,20))
        nCero, tString = GetString(df, seqR, True, alpha, e, lenSeqR)
        for s in range(0, lenSeqR, tLength):
            #------------------------------>
            printString = ''
            #------------------------------>
            for k,v in enumerate(tString):
                a = v[s:s+tLength]
                if a.strip():
                    end = k
                    printString = f"{printString}{str(k).zfill(nCero)}-{a.replace(' ', '&nbsp;')}<br />"
            #------------------------------>
            Story.append(Paragraph(printString, style=styles['Seq']))
            if end:
                Story.append(Spacer(1,10))
        if end:
            Story.append(Spacer(1,10))
        else:
            Story.append(Spacer(1,20))
    #endregion ------------------------------------------------>

    #region --------------------------------------------------->
    if seqN:
        for e in label:
            #------------------------------>
            Story.append(Paragraph(f'{e} Native Sequence'))
            Story.append(Spacer(1,20))
            nCero, tString = GetString(df, seqN, False, alpha, e, lenSeqN)
            for s in range(0, lenSeqN, tLength):
                #------------------------------>
                printString = ''
                #------------------------------>
                for k,v in enumerate(tString):
                    a = v[s:s+tLength]
                    if a.strip():
                        end = k
                        printString = f"{printString}{str(k).zfill(nCero)}-{a.replace(' ', '&nbsp;')}<br />"
                #------------------------------>
                Story.append(Paragraph(printString, style=styles['Seq']))
                if end:
                    Story.append(Spacer(1,10))
            if end:
                Story.append(Spacer(1,10))
            else:
                Story.append(Spacer(1,20))
    #endregion ------------------------------------------------>

    doc.build(Story)
    return True
#---
#endregion ----------------------------------------------------------> Methods
