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


"""Panes for the protprof module of the app"""


#region -------------------------------------------------------------> Imports
from dataclasses import dataclass, field
from typing      import Optional

from scipy import stats

import numpy  as np
import pandas as pd

from config.config import config as mConfig
from core     import method    as cMethod
from core     import statistic as cStatistic
from dataprep import method    as dataMethod
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Classes
@dataclass
class UserData(cMethod.BaseUserData):
    """Representation of the input data for the Limited Proteolysis Pane."""
    #region ---------------------------------------------------------> Options
    colFirstPart:list[str] = field(default_factory=lambda:
        mConfig.limp.dfcolFirstPart)
    colThirdLevel:list[str] = field(default_factory=lambda:
        mConfig.limp.dfcolCLevel)
    #------------------------------>
    dO:list = field(default_factory=lambda:                                     # Attr printed to UMSAP file
        ['iFileN', 'seqFileN', 'ID', 'cero', 'tran', 'norm', 'imp', 'shift',
         'width', 'targetProt', 'scoreVal', 'alpha', 'beta', 'gamma', 'theta',
         'thetaM', 'indSample', 'ocSeq', 'ocTargetProt', 'ocScore', 'resCtrl',
         'labelA', 'labelB', 'ctrlName', 'dfSeq', 'dfTargetProt', 'dfScore',
         'dfResCtrl', 'protLength', 'protLoc', 'protDelta',
        ])
    longestKey:int = 17                                                         # Length of the longest Key in dI
    #endregion ------------------------------------------------------> Options
#---

@dataclass
class LimpAnalysis():
    """Data class to hold the info regarding a Targeted Proteolysis analysis in
        an UMSAP file.
    """
    #region --------------------------------------------------------> Options
    df:pd.DataFrame                                                             # Results as dataframe
    labelA:list[str]                                                            # Lane's labels
    labelB:list[str]                                                            # Band's labels
    alpha:float                                                                 # Significance level
    protLength:list[int]                                                        # Length of Rec and Nat proteins
    protLoc:list[int]                                                           # Location of Nat Seq in Rec Seq
    protDelta:Optional[int]                                                     # Used to convert Rec Res Num to Nat Res Num
    targetProt:str                                                              # Name of Target Prot
    #endregion -----------------------------------------------------> Options
#---
#endregion ----------------------------------------------------------> Classes


#region -------------------------------------------------------------> Methods
def LimProt(                                                                    # pylint: disable=dangerous-default-value
    *args,
    df:pd.DataFrame  = pd.DataFrame(),                                          # pylint: disable=unused-argument
    rDO:UserData     = UserData(),
    resetIndex: bool = True,
    equal_var:bool   = False,
    **kwargs,
    ) -> tuple[dict, str, Optional[Exception]]:
    """Perform a Limited Proteolysis analysis.

        Parameters
        ----------
        *args:
            These are ignored here. Needed for compatibility.
        df: pd.DataFrame
            DataFrame read from CSV file.
        rDO: UserData
            Dataclass with user input.
        resetIndex: bool
            Reset index of dfS (True) or not (False). Default is True.
        equal_var: bool
            Assume variances are equal (True) or not (False). Default is False.
        **kwargs:
            These are ignored here. Needed for compatibility.

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
        *args and **kwargs are ignores. But they are needed for compatibility.
    """
    # Test in test.unit.limp.test_method.Test_LimProt
    #region ------------------------------------------------> Helper Functions
    def _emptyDFR() -> 'pd.DataFrame':
        """Creates the empty df for the results.

            Returns
            -------
            pd.DataFrame
        """
        #region -------------------------------------------------------> Index
        #------------------------------>
        aL = rDO.colFirstPart
        bL = rDO.colFirstPart
        cL = rDO.colFirstPart
        #------------------------------>
        n = len(rDO.colThirdLevel)
        #------------------------------>
        for b in rDO.labelB:
            for l in rDO.labelA:
                aL = aL + n*[b]
                bL = bL + n*[l]
                cL = cL + rDO.colThirdLevel
        #------------------------------>
        idx = pd.MultiIndex.from_arrays([aL[:], bL[:], cL[:]])
        #endregion ----------------------------------------------------> Index

        #region ----------------------------------------------------> Empty DF
        df = pd.DataFrame(
            np.nan, columns=idx, index=range(dfS.shape[0]),                     # type: ignore
        )
        #endregion -------------------------------------------------> Empty DF

        #region -------------------------------------------------> Seq & Score
        df[(aL[0], bL[0], cL[0])] = dfS.iloc[:,0]
        df[(aL[1], bL[1], cL[1])] = dfS.iloc[:,2]
        #endregion ----------------------------------------------> Seq & Score

        return df
    #---

    def _calcOutData(
        bN:str,
        lN:str,
        colC:list[int],
        colD:list[int],
        equal_var:bool = False,
        ) -> bool:
        """Performed the tost test.

            Parameters
            ----------
            bN: str
                Band name.
            lN: str
                Lane name.
            colC: list int
                Column numbers of the control.
            colD: list int
                Column numbers of the gel spot.
            equal_var: bool
                Assume variances are equal (True) or not. Default is False.

            Returns
            -------
            bool
        """
        #region ----------------------------------------------> Delta and TOST
        if rDO.indSample == 'p':
            pG = stats.ttest_rel(
                dfS.iloc[:,colC].add(dfR[('Delta', 'Delta', 'Delta')], axis=0),
                dfS.iloc[:,colD],
                axis        = 1,
                nan_policy  = 'omit',
                alternative = 'greater',
            ).pvalue
            pL = stats.ttest_rel(
                dfS.iloc[:,colC].sub(dfR[('Delta', 'Delta', 'Delta')], axis=0),
                dfS.iloc[:,colD],
                axis        = 1,
                nan_policy  = 'omit',
                alternative = 'less',
            ).pvalue
        else:
            pG = stats.ttest_ind(
                dfS.iloc[:,colC].add(dfR[('Delta', 'Delta', 'Delta')], axis=0),
                dfS.iloc[:,colD],
                axis        = 1,
                equal_var   = equal_var,
                nan_policy  = 'omit',
                alternative = 'greater',
            ).pvalue
            pL = stats.ttest_ind(
                dfS.iloc[:,colC].sub(dfR[('Delta', 'Delta', 'Delta')], axis=0),
                dfS.iloc[:,colD],
                axis        = 1,
                equal_var   = equal_var,
                nan_policy  = 'omit',
                alternative = 'less',
            ).pvalue
        #------------------------------>
        if isinstance(pG, np.ma.core.MaskedArray):                              # type: ignore In test is a masked array
            pG = pG.filled(fill_value=np.nan)                                   #              In module a regular array
        if isinstance(pL, np.ma.core.MaskedArray):                              # type: ignore Why?
            pL = pL.filled(fill_value=np.nan)
        pR = np.where(pG >= pL, pG, pL)
        dfR[(bN, lN, 'Ptost')] = pR
        #endregion -------------------------------------------> Delta and TOST

        return True
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
    dfR, msgError, tException = cMethod.NCResNumbers(
        dfR, rDO, seqNat=True)
    if dfR.empty:
        return ({}, msgError, tException)
    #------------------------------> Control Columns
    colC  = rDO.dfResCtrl[0][0]
    #------------------------------> Delta
    if rDO.theta is not None:
        delta = rDO.theta
    else:
        delta = cStatistic.Tost_delta(
            dfS.iloc[:,colC],
            rDO.alpha,
            rDO.beta,
            rDO.gamma,
            deltaMax = rDO.thetaM,
        )
    #------------------------------>
    dfR[('Delta', 'Delta', 'Delta')] = delta
    #------------------------------> Calculate
    for b, bN in enumerate(rDO.labelB):
        for l, lN in enumerate(rDO.labelA):
            #------------------------------> Control & Data Column
            colD = rDO.dfResCtrl[b+1][l]
            #------------------------------> Calculate data
            if colD:
                try:
                    _calcOutData(bN, lN, colC, colD, equal_var=equal_var)
                except Exception as e:
                    msg = (f'Calculation of the Limited Proteolysis data for '
                           f'point {bN} - {lN} failed.')
                    return ({}, msg, e)
    #endregion -----------------------------------------------------> Analysis

    #region -------------------------------------------------> Check P < a
    idx = pd.IndexSlice
    if not (dfR.loc[:,idx[:,:,'Ptost']] < rDO.alpha).any().any():                # type: ignore
        msg = ('There were no peptides detected in the gel '
            'spots with intensity values equivalent to the intensity '
            'values in the control spot. You may run the analysis again '
            'with different values for the configuration options.')
        return ({}, msg, None)
    #endregion ----------------------------------------------> Check P < a

    #region --------------------------------------------------------> Sort
    dfR = dfR.sort_values(
        by=[('Nterm', 'Nterm', 'Nterm'),('Cterm', 'Cterm', 'Cterm')]            # type: ignore
    )
    dfR = dfR.reset_index(drop=True)
    #endregion -----------------------------------------------------> Sort

    dictO = tOut[0]
    dictO['dfR'] = dfR
    return (dictO, '', None)
#---
#endregion ----------------------------------------------------------> Methods
