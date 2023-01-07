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
