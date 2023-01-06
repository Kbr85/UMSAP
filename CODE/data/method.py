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
