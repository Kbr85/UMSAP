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
from typing import Optional

from scipy import stats

import numpy  as np
import pandas as pd

from core     import method    as cMethod
from core     import statistic as cStatistic
from dataprep import method    as dataMethod
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Methods
def LimProt(                                                                    # pylint: disable=dangerous-default-value
    *args,
    df:pd.DataFrame  = pd.DataFrame(),                                          # pylint: disable=unused-argument
    rDO:dict         = {},
    rDExtra:dict     = {},
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
        rDO: dict
            rDO dictionary from the PrepareRun step of the analysis.
        rDExtra: dict
            Extra parameters.
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
    def EmptyDFR() -> 'pd.DataFrame':
        """Creates the empty df for the results.

            Returns
            -------
            pd.DataFrame
        """
        #region -------------------------------------------------------> Index
        #------------------------------>
        aL = rDExtra['cLDFFirstThree']
        bL = rDExtra['cLDFFirstThree']
        cL = rDExtra['cLDFFirstThree']
        #------------------------------>
        n = len(rDExtra['cLDFThirdLevel'])
        #------------------------------>
        for b in rDO['Band']:
            for l in rDO['Lane']:
                aL = aL + n*[b]
                bL = bL + n*[l]
                cL = cL + rDExtra['cLDFThirdLevel']
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

    def CalcOutData(
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
        if rDO['Sample'] == 'p':
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
    dfR = EmptyDFR()
    #------------------------------> N, C Res Num
    dfR, msgError, tException = cMethod.NCResNumbers(
        dfR, rDO, rDExtra['rSeqFileObj'], seqNat=True)
    if dfR.empty:
        return ({}, msgError, tException)
    #------------------------------> Control Columns
    colC  = rDO['df']['ResCtrl'][0][0]
    #------------------------------> Delta
    if rDO['Theta'] is not None:
        delta = rDO['Theta']
    else:
        delta = cStatistic.Tost_delta(
            dfS.iloc[:,colC],
            rDO['Alpha'],
            rDO['Beta'],
            rDO['Gamma'],
            deltaMax = rDO['ThetaMax'],
        )
    #------------------------------>
    dfR[('Delta', 'Delta', 'Delta')] = delta
    #------------------------------> Calculate
    for b, bN in enumerate(rDO['Band']):
        for l, lN in enumerate(rDO['Lane']):
            #------------------------------> Control & Data Column
            colD = rDO['df']['ResCtrl'][b+1][l]
            #------------------------------> Calculate data
            if colD:
                try:
                    CalcOutData(bN, lN, colC, colD, equal_var=equal_var)
                except Exception as e:
                    msg = (f'Calculation of the Limited Proteolysis data for '
                           f'point {bN} - {lN} failed.')
                    return ({}, msg, e)
    #endregion -----------------------------------------------------> Analysis

    #region -------------------------------------------------> Check P < a
    idx = pd.IndexSlice
    if not (dfR.loc[:,idx[:,:,'Ptost']] < rDO['Alpha']).any().any():                # type: ignore
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
