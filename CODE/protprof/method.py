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


"""Methods for the protprof module of the app"""


#region -------------------------------------------------------------> Imports
from dataclasses import dataclass, field
from typing      import Optional, Union

import pandas as pd
import numpy  as np
from scipy                       import stats
from statsmodels.stats.multitest import multipletests

from config.config import config as mConfig
from core     import method    as cMethod
from core     import statistic as cStatistic
from dataprep import method    as dataMethod
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Classes
@dataclass
class UserData(cMethod.BaseUserData):
    """Representation of the input data for the Proteome Profiling Analysis
        Pane.
    """
    #region ---------------------------------------------------------> Options
    colFirstThree:list[str] = field(default_factory=lambda:
        mConfig.prot.dfcolFirstPart)
    colThirdLevel:list[str] = field(default_factory=lambda:
        mConfig.prot.dfcolFirstPart)
    #------------------------------>
    dO:list = field(default_factory=lambda:                                     # Options for output printing
        ['iFileN', 'ID', 'cero', 'tran', 'norm', 'imp', 'shift',
         'width', 'ocResCtrlFlat', 'dfColumnR', 'dfColumnF', 'dfResCtrlFlat',
        ])
    longestKey:int = 17                                                         # Length of the longest Key in dI
    #endregion ------------------------------------------------------> Options
#---
#endregion ----------------------------------------------------------> Classes


#region -------------------------------------------------------------> Methods
def ProtProf(                                                                   # pylint: disable=dangerous-default-value
    *args,
    df:pd.DataFrame = pd.DataFrame(),                                           # pylint: disable=unused-argument
    rDO:UserData    = UserData(),
    resetIndex:bool = True,
    **kwargs
    ) -> tuple[dict, str, Optional[Exception]]:
    """Perform a Proteome Profiling Analysis.

        Parameters
        ----------
        *args:
            For compatibility. They are ignore here.
        df: pd.DataFrame
            DataFrame read from CSV file.
        rDO: UserData
            Data class with user input.
        resetIndex: bool
            Reset index of dfS (True) or not (False). Default is True.
        **kwargs:
            For compatibility. They are ignore here.

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
        *args and **kwargs are ignored.
    """
    # Test in test.unit.protprof.test_method.Test_ProtProf
    #region ------------------------------------------------> Helper Functions
    def EmptyDFR() -> pd.DataFrame:
        """Creates the empty data frame for the output. This data frame contains
            the values for Gene, Protein and Score.

            Returns
            -------
            pd.DataFrame
        """
        #region -------------------------------------------------------> Index
        #------------------------------> First Three Columns
        aL = rDO.colFirstThree
        bL = rDO.colFirstThree
        cL = rDO.colFirstThree
        #------------------------------> Columns per Point
        n = len(rDO.colThirdLevel)
        #------------------------------> Other columns
        for c in rDO.labelA:
            for t in rDO.labelB:
                aL = aL + n*[c]
                bL = bL + n*[t]
                cL = cL + rDO.colThirdLevel
        #------------------------------>
        idx = pd.MultiIndex.from_arrays([aL[:], bL[:], cL[:]])
        #endregion ----------------------------------------------------> Index

        #region ----------------------------------------------------> Empty DF
        df = pd.DataFrame(np.nan, columns=idx, index=range(dfS.shape[0]))       # type: ignore
        #endregion -------------------------------------------------> Empty DF

        #region -----------------------------------------> First Three Columns
        df[(aL[0], bL[0], cL[0])] = dfS.iloc[:,0]
        df[(aL[1], bL[1], cL[1])] = dfS.iloc[:,1]
        df[(aL[2], bL[2], cL[2])] = dfS.iloc[:,2]
        #endregion --------------------------------------> First Three Columns

        return df
    #---

    def ColCtrlData_OC(c:int, t:int) -> list[list[int]]:
        """Get the Ctrl and Data columns for the given condition and relevant
            point when Control Type is: One Control.

            Parameters
            ----------
            c: int
                Condition index in self.do['df']['ResCtrl]
            t: int
                Relevant point index in self.do['df']['ResCtrl]

            Returns
            -------
            list[list[int]]
        """
        #region ---------------------------------------------------> List
        colC = rDO.dfResCtrl[0][0]
        #------------------------------>
        colD = rDO.dfResCtrl[c+1][t]
        #endregion ------------------------------------------------> List

        return [colC, colD]
    #---

    def ColCtrlData_OCC(c:int, t:int) -> list[list[int]]:
        """Get the Ctrl and Data columns for the given condition and relevant
            point when Control Type is: One Control per Column.

            Parameters
            ----------
            c: int
                Condition index in self.do['df']['ResCtrl]
            t: int
                Relevant point index in self.do['df']['ResCtrl]

            Returns
            -------
            list[list[int]]
        """
        #region ---------------------------------------------------> List
        colC = rDO.dfResCtrl[0][t]
        #------------------------------>
        colD = rDO.dfResCtrl[c+1][t]
        #endregion ------------------------------------------------> List

        return [colC, colD]
    #---

    def ColCtrlData_OCR(c:int, t:int) -> list[list[int]]:
        """Get the Ctrl and Data columns for the given condition and relevant
            point when Control Type is: One Control per Row

            Parameters
            ----------
            c: int
                Condition index in self.do['df']['ResCtrl]
            t: int
                Relevant point index in self.do['df']['ResCtrl]

            Returns
            -------
            list[list[int]]
        """
        #region ---------------------------------------------------> List
        colC = rDO.dfResCtrl[c][0]
        #------------------------------>
        colD = rDO.dfResCtrl[c][t+1]
        #endregion ------------------------------------------------> List

        return [colC, colD]
    #---

    def ColCtrlData_Ratio(c:int, t:int) -> list[list[int]]:
        """Get the Ctrl and Data columns for the given condition and relevant
            point when Control Type is: Data as Ratios.

            Parameters
            ----------
            c: int
                Condition index in self.do['df']['ResCtrl]
            t: int
                Relevant point index in self.do['df']['ResCtrl]

            Returns
            -------
            list[list[int]]
        """
        #region ---------------------------------------------------> List
        colC = []
        #------------------------------>
        colD = rDO.dfResCtrl[c][t]
        #endregion ------------------------------------------------> List

        return [colC, colD]
    #---

    def CalcOutData(cN:str, tN:str, colC:list[int], colD:list[int]) -> bool:
        """Calculate the data for the main output dataframe.

            Parameters
            ----------
            cN: str
                Condition name.
            tN: str
                Relevant point name.
            colC: list[int]
                Column numbers for the control. Empty list for Ration of
                intensities.
            colD: list[int]
                Column numbers for the experiment.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Ave & Std
        if colC:
            dfR.loc[:,(cN, tN, 'aveC')] = dfS.iloc[:,colC].mean(                # type: ignore
                axis=1, skipna=True).to_numpy()
            dfR.loc[:,(cN, tN, 'stdC')] = dfS.iloc[:,colC].std(                 # type: ignore
                axis=1, skipna=True).to_numpy()
        else:
            dfR.loc[:,(cN, tN, 'aveC')] = np.nan                                # type: ignore
            dfR.loc[:,(cN, tN, 'stdC')] = np.nan                                # type: ignore
        #------------------------------>
        dfR.loc[:,(cN, tN, 'ave')] = dfS.iloc[:,colD].mean(                     # type: ignore
            axis=1, skipna=True).to_numpy()
        dfR.loc[:,(cN, tN, 'std')] = dfS.iloc[:,colD].std(                      # type: ignore
            axis=1, skipna=True).to_numpy()
        #endregion ------------------------------------------------> Ave & Std

        #region --------------------------------------------> Log2 Intensities
        dfLogI = dfS.copy()
        if rDO.tran != 'Log2':
            if colC:
                dfLogI.iloc[:,colC+colD] = np.log2(dfLogI.iloc[:,colC+colD])
            else:
                dfLogI.iloc[:,colD] = np.log2(dfLogI.iloc[:,colD])
        #endregion -----------------------------------------> Log2 Intensities

        #region ----------------------------------------------------> Log2(FC)
        if colC:
            FC = (
                dfLogI.iloc[:,colD].mean(axis=1, skipna=True)                   # type: ignore
                - dfLogI.iloc[:,colC].mean(axis=1, skipna=True)                 # type: ignore
            )
        else:
            FC = dfLogI.iloc[:,colD].mean(axis=1, skipna=True)                  # type: ignore
        #------------------------------>
        dfR.loc[:, (cN, tN, 'FC')] = FC.to_numpy()                              # type: ignore
        #endregion -------------------------------------------------> Log2(FC)

        #region ---------------------------------------------------> FCz
        dfR.loc[:,(cN, tN, 'FCz')] = (FC - FC.mean()).div(FC.std()).to_numpy()  # type: ignore
        #endregion ------------------------------------------------> FCz

        #region ---------------------------------------------------> FC CI
        if rDO.rawInt:
            if rDO.indSample:
                dfR.loc[:,(cN, tN, 'CI')] = cStatistic.CI_Mean_Diff(             # type: ignore
                    dfLogI.iloc[:,colC], dfLogI.iloc[:,colD], rDO.alpha
                ).loc[:,'CI'].to_numpy()
            else:
                val = dfLogI.iloc[:,colC] - dfLogI.iloc[:,colD]
                dfR.loc[:,(cN,tN,'CI')] = cStatistic.CI_Sample(                 # type: ignore
                    val, rDO.alpha
                ).loc[:,'CI'].to_numpy()
        else:
            dfR.loc[:,(cN, tN, 'CI')] = cStatistic.CI_Sample(                  # type: ignore
                dfLogI.iloc[:,colD], rDO.alpha
            ).loc[:,'CI'].to_numpy()
        #endregion ------------------------------------------------> FC CI

        #region -----------------------------------------------------------> P
        if rDO.rawInt:
            if rDO.indSample:
                dfR.loc[:,(cN,tN,'P')] = stats.ttest_ind(                       # type: ignore
                    dfLogI.iloc[:,colC],
                    dfLogI.iloc[:,colD],
                    equal_var  = False,
                    nan_policy = 'omit',
                    axis       = 1,
                ).pvalue
            else:
                dfR.loc[:,(cN,tN,'P')] = stats.ttest_rel(                       # type: ignore
                    dfLogI.iloc[:,colC],
                    dfLogI.iloc[:,colD],
                    axis       = 1,
                    nan_policy = 'omit',
                ).pvalue
        else:
            #------------------------------> Dummy 0 columns
            dfLogI['TEMP_Col_Full_00'] = 0
            dfLogI['TEMP_Col_Full_01'] = 0
            colCF = []
            colCF.append(dfLogI.columns.get_loc('TEMP_Col_Full_00'))
            colCF.append(dfLogI.columns.get_loc('TEMP_Col_Full_01'))
            #------------------------------>
            dfR.loc[:,(cN,tN,'P')] = stats.ttest_ind(                           # type: ignore
                dfLogI.iloc[:,colCF],
                dfLogI.iloc[:,colD],
                equal_var  = False,
                nan_policy = 'omit',
                axis       = 1,
            ).pvalue
        #endregion --------------------------------------------------------> P

        #region ----------------------------------------------------------> Pc
        if rDO.correctedP != 'None':
            dfR.loc[:,(cN,tN,'Pc')] = multipletests(                            # type: ignore
                dfR.loc[:,(cN,tN,'P')],                                         # type: ignore
                rDO.alpha,
                mConfig.core.oCorrectP[rDO.correctedP]
            )[1]
        #endregion -------------------------------------------------------> Pc

        #region ------------------------------------------------> Round to .XX
        dfR.loc[:,(cN,tN,rDO.colThirdLevel)] = (                                # type: ignore
            dfR.loc[:,(cN,tN,rDO.colThirdLevel)].round(2)                       # type: ignore
        )
        #endregion ---------------------------------------------> Round to .XX

        return True
    #---
    #endregion ---------------------------------------------> Helper Functions

    #region -------------------------------------------------------> Variables
    dColCtrlData = {
        mConfig.prot.oControlType['OC']   : ColCtrlData_OC,
        mConfig.prot.oControlType['OCC']  : ColCtrlData_OCC,
        mConfig.prot.oControlType['OCR']  : ColCtrlData_OCR,
        mConfig.prot.oControlType['Ratio']: ColCtrlData_Ratio,
    }
    #endregion ----------------------------------------------------> Variables

    #region ------------------------------------------------> Data Preparation
    tOut = dataMethod.DataPreparation(df=df, rDO=rDO, resetIndex=resetIndex)
    if tOut[0]:
        dfS = tOut[0]['dfS']
    else:
        return tOut
    #endregion ---------------------------------------------> Data Preparation

    #region ------------------------------------------------------------> Sort
    dfS.sort_values(
        by=list(dfS.columns[0:2]), inplace=True, ignore_index=True)
    #endregion ---------------------------------------------------------> Sort

    #region -------------------------------------------------------> Calculate
    dfR = EmptyDFR()
    #------------------------------>
    for c, cN in enumerate(rDO.labelA):
        for t, tN in enumerate(rDO.labelB):
            #------------------------------> Control & Data Column
            colC, colD = dColCtrlData[rDO.ctrlType](c, t)
            #------------------------------> Calculate data
            try:
                CalcOutData(cN, tN, colC, colD)
            except Exception as e:
                msg = (f'Calculation of the Proteome Profiling data for '
                       f'point {cN} - {tN} failed.')
                return ({}, msg, e)
    #endregion ----------------------------------------------------> Calculate

    #region --------------------------------------------------->
    dictO = tOut[0]
    dictO['dfR'] = dfR
    return (dictO, '', None)
    #endregion ------------------------------------------------>
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
#endregion ----------------------------------------------------------> Methods
