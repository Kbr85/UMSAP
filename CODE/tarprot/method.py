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


"""Panes for the tarprot module of the app"""


#region -------------------------------------------------------------> Imports
from collections import namedtuple
from dataclasses import dataclass, field
from typing      import Optional, TYPE_CHECKING

import numpy  as np
import pandas as pd

from reportlab.lib.pagesizes import A4
from reportlab.platypus      import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles    import getSampleStyleSheet, ParagraphStyle

from config.config import config as mConfig
from core     import method    as cMethod
from core     import statistic as cStatistic
from dataprep import method    as dataMethod

if TYPE_CHECKING:
    from pathlib import Path
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Classes
@dataclass
class UserData(cMethod.BaseUserData):
    """Representation of the input data for the Target Proteolysis Pane."""
    #region ---------------------------------------------------------> Options
    colFirstPart:list[str] = field(default_factory=lambda:
        mConfig.tarp.dfcolFirstPart)
    colSecLevel:list[str] = field(default_factory=lambda:
        mConfig.tarp.dfcolBLevel)
    #------------------------------>
    dO:list = field(default_factory=lambda:                                     # Attr printed to UMSAP file
        ['iFileN', 'seqFileN', 'ID', 'cero', 'tran', 'norm', 'imp', 'shift',
         'width', 'targetProt', 'scoreVal', 'alpha', 'posAA', 'winHist',
         'ocSeq', 'ocTargetProt', 'ocScore', 'ocColumn', 'resCtrl', 'labelA',
         'ctrlName', 'dfSeq', 'dfTargetProt', 'dfScore', 'dfResCtrl',
         'protLength', 'protLoc', 'protDelta',
        ])
    longestKey:int = 17                                                         # Length of the longest Key in dI
    #endregion ------------------------------------------------------> Options
#---

@dataclass
class TarpAnalysis():
    """Data class to hold the info regarding a Targeted Proteolysis analysis in
        an UMSAP file.
    """
    #region --------------------------------------------------------> Options
    df:pd.DataFrame                                                             # Results as dataframe
    labelA:list[str]                                                            # Exp's labels
    ctrlName:str                                                                # Control Name
    alpha:float                                                                 # Significance level
    protLength:list[int]                                                        # Length of Rec and Nat Prot
    protLoc:list[int]                                                           # Location of Nat Prot in Rec Prot
    protDelta:Optional[int]                                                     # To convert Rec Res Num to Nat Res Num
    targetProt:str                                                              # Name of Target Protein
    CpR:str                                                                     # Name of CpR File
    CEvol:str                                                                   # Name of CEvol file
    AA:dict[str,str]                                                            # Label for Menu Item (key) and File name (value)
    Hist:dict[str,str]                                                          # Label for Menu Item (key) and File name (value)
    #endregion -----------------------------------------------------> Options
#---
#endregion ----------------------------------------------------------> Classes


#region -------------------------------------------------------------> Methods
def TarProt(
    *args,
    df:pd.DataFrame  = pd.DataFrame(),                                          # pylint: disable=unused-argument
    rDO:UserData     = UserData(),
    resetIndex: bool = True,
    **kwargs
    ) -> tuple[dict, str, Optional[Exception]]:
    """Perform a Targeted Proteolysis analysis.

        Parameters
        ----------
        *args:
            Ignored here. Needed for compatibility.
        df: pd.DataFrame
            DataFrame read from CSV file.
        rDO: UserData
            Dataclass with user input.
        resetIndex: bool
            Reset index of dfS (True) or not (False). Default is True.
        **kwargs:
            Ignored here. Needed for compatibility.

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

        Notes
        -----
        *args and **kwargs are ignored here but needed for compatibility.
    """
    # Test in test.unit.tarprot.test_method.Test_TarProt
    #region ------------------------------------------------> Helper Functions
    def _emptyDFR() -> pd.DataFrame:
        """Creates the empty df for the results.

            Returns
            -------
            pd.DataFrame
        """
        #region -------------------------------------------------------> Index
        aL = rDO.colFirstPart
        bL = rDO.colFirstPart
        n = len(rDO.colSecLevel)
        #------------------------------> Ctrl
        aL = aL + n*[rDO.ctrlName]
        bL = bL + rDO.colSecLevel
        #------------------------------> Exp
        for exp in rDO.labelA:
            aL = aL + n*[exp]
            bL = bL + rDO.colSecLevel
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
        df[(rDO.ctrlName, 'P')] = np.nan
        #endregion ----------------------------------------------> Seq & Score

        return df
    #---

    def _prepareAncova(
        rowC:int,
        row:namedtuple,                                                         # type: ignore
        rowN:int
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
        for r in rDO.dfResCtrl[0][0]:
            if np.isfinite(row[r]):
                xC.append(1)
                xCt.append(5)
                yC.append(row[r])
        #--------------> Add to self.dfR
        dfR.at[rowC,(rDO.ctrlName,'Int')] = str(yC)
        #------------------------------> Points
        for k,r in enumerate(rDO.dfResCtrl[1:], start=1):
            #------------------------------>
            xE = []
            yE = []
            #------------------------------>
            for rE in r[0]:
                if np.isfinite(row[rE]):
                    xE.append(5)
                    yE.append(row[rE])
            #------------------------------>
            dfR.at[rowC,(rDO.labelA[k-1], 'Int')] = str(yE)
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
    tOut = dataMethod.DataPreparation(df=df, rDO=rDO, resetIndex=resetIndex)
    if tOut[0]:
        dfS = tOut[0]['dfS']
    else:
        return tOut
    #endregion ---------------------------------------------> Data Preparation

    #region --------------------------------------------------------> Analysis
    #------------------------------> Empty dfR
    dfR = _emptyDFR()
    #------------------------------> N, C Res Num
    dfR, msgError, tException = cMethod.NCResNumbers(dfR, rDO, seqNat=True)
    if dfR.empty:
        return ({}, msgError, tException)
    #------------------------------> P values
    totalRowAncovaDF = 2*max([len(x[0]) for x in rDO.dfResCtrl])
    nGroups = [2 for x in rDO.dfResCtrl]
    nGroups = nGroups[1:]
    idx = pd.IndexSlice
    idx = idx[rDO.labelA, 'P']
    #-------------->
    k = 0
    for row in dfS.itertuples(index=False):
        try:
            #------------------------------> Ancova df & Int
            dfAncova = _prepareAncova(k, row, totalRowAncovaDF)
            #------------------------------> P value
            dfR.loc[k,idx] = cStatistic.Test_slope(dfAncova, nGroups)           # type: ignore
        except Exception as e:
            msg = (f'P value calculation failed for peptide {row[0]}.')
            return ({}, msg, e)
        #------------------------------>
        k = k + 1
    #endregion -----------------------------------------------------> Analysis

    #region -------------------------------------------------> Check P < a
    idx = pd.IndexSlice
    if not (dfR.loc[:,idx[:,'P']] < rDO.alpha).any().any():                  # type: ignore
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


def R2AA(
    df:pd.DataFrame,
    seq:str,
    alpha:float,
    protL:int,
    pos:int = 5,
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
    # Test in test.unit.tarprot.test_method.Test_R2AA
    #region ---------------------------------------------------> Helper Method
    def _addNewAA(
        dfO:pd.DataFrame,
        r:int,
        pos:int,
        seq:str,
        l:str
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
    dfO = pd.DataFrame(0, columns=idx, index=mConfig.core.lAA1+['Chi'])         # type: ignore
    dfO[('AA','AA')] = mConfig.core.lAA1[:]+['Chi']
    #endregion ------------------------------------------------> Empty

    #region ---------------------------------------------------> Fill
    idx = pd.IndexSlice
    for l in df.columns.get_level_values(0)[1:]:
        seqDF = df[df[idx[l,'P']] < alpha].iloc[:,0].to_list()                  # type: ignore
        for s in seqDF:
            #------------------------------>
            n = seq.find(s)
            if n > 0:
                dfO = _addNewAA(dfO, n, pos, seq, l)                             # type: ignore
            #------------------------------>
            c = n+len(s)
            if c < protL:
                dfO = _addNewAA(dfO, c, pos, seq, l)                             # type: ignore
    #endregion ------------------------------------------------> Fill

    #region ---------------------------------------------------> Random Cleavage
    c   = 'ALL_CLEAVAGES_UMSAP'
    aL  = 2*pos*[c]
    bL  = [f'P{x}' for x in range(pos, 0, -1)] + [f"P{x}'" for x in range(1, pos+1,1)]
    idx = pd.MultiIndex.from_arrays([aL[:],bL[:]])
    dfT = pd.DataFrame(0, columns=idx, index=mConfig.core.lAA1+['Chi'])         # type: ignore
    dfO = pd.concat([dfO, dfT], axis=1)
    for k,_ in enumerate(seq[1:-1], start=1):                                   # Exclude first and last residue
        dfO = _addNewAA(dfO, k, pos, seq, c)
    #endregion ------------------------------------------------> Random Cleavage

    #region ---------------------------------------------------> Group
    idx = pd.IndexSlice
    gS = []
    for g in mConfig.core.lAAGroups:
        gS.append(dfO.loc[g,:].sum(axis=0))
    g = pd.concat(gS, axis=1)
    g = g.transpose()

    for l in df.columns.get_level_values(0)[1:]:
        for p in dfO.loc[:,idx[l,:]].columns.get_level_values(1):               # type: ignore
            dfO.at['Chi', idx[l,p]] = cStatistic.Test_chi(                      # type: ignore
                g.loc[:,idx[[l,c],p]], alpha)[0]                                # type: ignore
    #endregion ------------------------------------------------> Group

    return dfO
#---


def R2Hist(
    df:pd.DataFrame,
    alpha:float,
    win:list[int],
    maxL:list[int]
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
    # Test in test.unit.tarprot.test_method.Test_R2Hist
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


def R2CpR(df:pd.DataFrame, alpha:float, protL:list[int]) -> pd.DataFrame:
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
    # Test in test.unit.tarprot.test_method.Test_R2CpR
    #region -------------------------------------------------------------> dfO
    label = df.columns.unique(level=0).tolist()[4:]
    nL    = len(label)
    a     = (nL)*['Rec']+(nL)*['Nat']
    b     = 2*label
    nR    = sorted(protL, reverse=True)[0] if protL[1] else protL[0]
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
        l = [x for x in l if -1 < x < lastR]
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


def R2CEvol(df:pd.DataFrame, alpha:float, protL:list[int]) -> pd.DataFrame:
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
    # Test in test.unit.tarprot.test_method.Test_R2CEvol
    #region -------------------------------------------------> Helper Function
    def _intL2MeanI(a:list, alpha:float) -> float:
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
        dfT.loc[:,idx[e,'Int']] = dfT.loc[:,idx[e,['Int','P']]].apply(_intL2MeanI, axis=1, raw=True, args=[alpha])       # type: ignore
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
            dfT.loc[:,idx[e,'Int']] = dfT.loc[:,idx[e,['Int','P']]].apply(_intL2MeanI, axis=1, raw=True, args=[alpha])   # type: ignore
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
    df:pd.DataFrame,
    alpha:float,
    seqR:str,
    fileP:'Path',
    tLength:int,
    seqN:str = '',
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
    def _getString(
        df:pd.DataFrame,
        seq:str,
        rec:bool,
        alpha:float,
        label:str,
        lSeq:int,
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
        nCero, tString = _getString(df, seqR, True, alpha, e, lenSeqR)
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
            nCero, tString = _getString(df, seqN, False, alpha, e, lenSeqN)
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
