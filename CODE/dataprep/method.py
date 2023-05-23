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


"""Methods for the data preparation module of the app"""


#region -------------------------------------------------------------> Imports
from dataclasses import dataclass, field
from typing      import Optional, Union, Literal

import numpy  as np
import pandas as pd

from config.config import config as mConfig
from core import method as cMethod
#endregion ----------------------------------------------------------> Imports


LIT_Tran = Literal['', 'None', 'Log2']
LIT_Norm = Literal['', 'None', 'Median']
LIT_Imp  = Literal['', 'None', 'Normal Distribution']


#region -------------------------------------------------------------> Classes
@dataclass
class UserData(cMethod.BaseUserData):
    """Representation of the input data for the Correlation Analysis Pane"""
    #region ---------------------------------------------------------> Options
    dO:list = field(default_factory=lambda:                                     # Attr printed to UMSAP file
        ['iFileN', 'ID', 'cero', 'tran', 'norm', 'imp', 'shift',
         'width', 'ocResCtrlFlat', 'ocColumn', 'dfColumnR', 'dfColumnF',
         'dfResCtrlFlat',
        ])
    longestKey:int = 20                                                         # Length of the longest Key in dI
    #endregion ------------------------------------------------------> Options
#---

@dataclass
class DataSteps():
    """Data class to hold the pd.DataFrames for the Data Preparation steps"""
    #region ---------------------------------------------------------> Options
    dfF:pd.DataFrame  = pd.DataFrame()                                          # Floated data
    dfT:pd.DataFrame  = pd.DataFrame()                                          # Transformed data
    dfN:pd.DataFrame  = pd.DataFrame()                                          # Normalized data
    dfIm:pd.DataFrame = pd.DataFrame()                                          # Imputed data
    #endregion ------------------------------------------------------> Options
#---


@dataclass
class DataAnalysis():
    """Data class to hold the info regarding a DataPrep in an UMSAP file."""
    #region --------------------------------------------------------> Options
    dp:DataSteps                                                                # Results as dataframe
    numColList:list[int]                                                        # Column numbers
    #endregion -----------------------------------------------------> Options
#endregion ----------------------------------------------------------> Classes


#region -------------------------------------------------------------> Methods
#region ----------------------------------------------------> Data Preparation
def RunDataPreparation(                                                            # pylint: disable=dangerous-default-value
    *args,                                                                      # pylint: disable=unused-argument
    df:pd.DataFrame          = pd.DataFrame(),
    rDO:cMethod.BaseUserData = cMethod.BaseUserData(),
    resetIndex: bool         = True,
    **kwargs
    ) -> tuple[dict, str, Optional[Exception]]:
    """Perform the data preparation steps.

        Parameters
        ----------
        *args:
            Ignore here but needed for compatibility.
        df: pd.DataFrame
            DataFrame read from CSV file.
        rDO: dict
            rDO dictionary from the PrepareRun step of the analysis.
        resetIndex: bool
            Reset index of dfS (True) or not (False). Default is True.
        **kwargs:
            Ignore here but needed for  compatibility.

        Returns
        -------
        tuple:
            -   (
                    {
                        'dfI' : pd.DataFrame,
                        'dfF' : pd.DataFrame,
                        'dfMR': pd.DataFrame,
                        'dfT' : pd.DataFrame,
                        'dfN' : pd.DataFrame,
                        'dfIm': pd.DataFrame,
                        'dfTP': pd.DataFrame,
                        'dfE' : pd.DataFrame,
                        'dfS' : pd.DataFrame
                    },
                    '',
                    None
                )                                  when everything went fine.
            -   ({}, 'Error message', Exception)   when something went wrong.

        Notes
        -----
        *args are ignored. They are needed for compatibility.
        *kwargs are ignored. They are needed for compatibility.
    """
    # Test in test.unit.data.test_method.DataPreparation
    #region -------------------------------------------------------->
    try:
        return DataPreparation(
            *args, df=df, rDO=rDO, resetIndex=resetIndex, **kwargs)
    except Exception as e:
        return ({}, str(e), e)
    #endregion ----------------------------------------------------->
#---


def DataPreparation(                                                            # pylint: disable=dangerous-default-value
    *args,                                                                      # pylint: disable=unused-argument
    df:pd.DataFrame          = pd.DataFrame(),
    rDO:cMethod.BaseUserData = cMethod.BaseUserData(),
    resetIndex: bool         = True,
    **kwargs
    ) -> tuple[dict, str, Optional[Exception]]:
    """Perform the data preparation steps.

        Parameters
        ----------
        *args:
            Ignore here but needed for compatibility.
        df: pd.DataFrame
            DataFrame read from CSV file.
        rDO: dict
            rDO dictionary from the PrepareRun step of the analysis.
        resetIndex: bool
            Reset index of dfS (True) or not (False). Default is True.
        **kwargs:
            Ignore here but needed for  compatibility.

        Returns
        -------
        tuple:
            -   (
                    {
                        'dfI' : pd.DataFrame,
                        'dfF' : pd.DataFrame,
                        'dfMR': pd.DataFrame,
                        'dfT' : pd.DataFrame,
                        'dfN' : pd.DataFrame,
                        'dfIm': pd.DataFrame,
                        'dfTP': pd.DataFrame,
                        'dfE' : pd.DataFrame,
                        'dfS' : pd.DataFrame
                    },
                    '',
                    None
                )                                  when everything went fine.
            -   ({}, 'Error message', Exception)   when something went wrong.

        Notes
        -----
        *args are ignored. They are needed for compatibility.
        *kwargs are ignored. They are needed for compatibility.
    """
    #region ----------------------------------------> Run Data Preparation
    #------------------------------> dfI & dfF
    dfI, dfF = DataPrep_Float(
        df,
        rDO.cero,
        rDO.ocColumn,
        rDO.dfColumnR,
        rDO.dfColumnF,
    )
    #------------------------------> Minimum Number of Valid Replicates
    dfMR = DataPrep_MinRep(dfF, rDO.dfResCtrl, rDO.minRepList)
    #------------------------------> Transformation
    dfT = DataTransformation(
        dfMR,
        rDO.dfResCtrlFlat,
        method = rDO.tran,
        rep    = np.nan if rDO.cero else 0,
    )
    #------------------------------> Normalization
    dfN = DataNormalization(dfT, rDO.dfResCtrlFlat, method=rDO.norm)
    #------------------------------> Imputation
    dfIm = DataImputation(
        dfN,
        rDO.dfResCtrlFlat,
        method = rDO.imp,
        shift  = rDO.shift,
        width  = rDO.width,
    )
    #------------------------------> Target Protein
    if rDO.targetProt:
        dfTP = cMethod.DFFilterByColS(
            dfIm, rDO.dfTargetProt, rDO.targetProt, 'e')
    else:
        dfTP = dfIm.copy()
    #------------------------------> Exclude
    if rDO.dfExcludeR:
        dfE = cMethod.DFExclude(dfTP, rDO.dfExcludeR)
    else:
        dfE = dfTP.copy()
    #------------------------------> Score
    if rDO.dfScore > -1:
        dfS = cMethod.DFFilterByColN(
            dfE, [rDO.dfScore], rDO.scoreVal, 'ge')
    else:
        dfS = dfE.copy()
    #------------------------------> Check not Empty
    if dfS.empty:
        return ({}, mConfig.core.mNoDataLeft, None)
    #endregion -------------------------------------> Run Data Preparation

    #region -------------------------------------------------> Reset index
    if resetIndex:
        dfS.reset_index(drop=True, inplace=True)
    #endregion ----------------------------------------------> Reset index

    #region --------------------------------------------------->
    dictO = {
        'dfI' : dfI,
        'dfF' : dfF,
        'dfMR': dfMR,
        'dfT' : dfT,
        'dfN' : dfN,
        'dfIm': dfIm,
        'dfTP': dfTP,
        'dfE' : dfE,
        'dfS' : dfS,
    }
    return (dictO, '', None)
    #endregion ------------------------------------------------>
#---


def DataPrep_Float(
    df:pd.DataFrame,
    cero:bool,
    col:list[int],
    colCero:list[int],
    colFloat:list[int]
    ) -> list:
    """Replace cero and missing values in df and convert to float the
        appropriate columns.

        Attributes
        ----------
        df: pd.DataFrame
            DataFrame with all the initial data.
        cero: bool
            Replace (True) or keep (False) cero values.
        col: list[int]
            Columns to be kept. All other columns in df are discarded.
        colCero: list[int]
            Columns in which '' and/or 0 will be replaced with np.nan.
        colFloat: list[int]
            Columns for which the float type will be enforced.

        Returns
        -------
        list
            [dfI, dfF]
    """
    # Test in test.unit.data.test_method.Test_DataPrep_Float
    #region -------------------------------------------------------->
    dfI = df.iloc[:,col]
    #------------------------------>
    if cero:
        dfF = cMethod.DFReplace(dfI, [0, ''], np.nan, sel=colCero)
    else:
        dfF = cMethod.DFReplace(dfI, [''], np.nan, sel=colCero)
    #------------------------------>
    dfF.iloc[:,colFloat] = dfF.iloc[:,colFloat].astype('float')                 # type: ignore
    #endregion ----------------------------------------------------->

    return [dfI, dfF]
#---


def DataPrep_MinRep(
    df:pd.DataFrame,
    resCtrl:list,
    minRep:list
    ) -> pd.DataFrame:
    """Eliminate rows in which at least one group does not posses the minimum
        number of valid replicates.

        Attributes
        ----------
        df: pd.DataFrame
            DataFrame with all the initial data.
        resCtrl: list
            List of groups including controls.
        minRep: list
            List with the minimum number of valid replicates for each group.

        Returns
        -------
        pd.DataFrame

        Notes
        -----
        resCtrl and minRep have the same structure.
    """
    # CREATE TEST. TEST NEEDED!!!!!!
    #region -------------------------------------------------------->
    dfO = df.copy()
    #------------------------------>
    for k,a in enumerate(minRep):
        for j,b in enumerate(a):
            for c in b:
                #------------------------------> Skip if no min rep
                if not c:
                    continue
                #------------------------------> Columns
                col = [dfO.columns[x] for x in resCtrl[k][j]]
                #------------------------------> Drop
                dfO = dfO.dropna(subset=col, thresh=c)
    #------------------------------> Index
    dfO = dfO.reset_index(drop=True)
    #endregion ----------------------------------------------------->

    return dfO
#---
#endregion -------------------------------------------------> Data Preparation


#region -------------------------------------------------> Data Transformation
def _DataTransformation_None(
    df:pd.DataFrame,                                                            # pylint: disable=unused-argument
    *args,
    **kwargs,
    ) -> pd.DataFrame:
    """This will just return the original df.

        Parameters
        ----------
        df: pd.DataFrame
            Dataframe with the data.

        Returns
        -------
        Dataframe
            Without any transformation.
    """
    # Test in test.unit.data.test_method.Test_DataTransformation
    return df
#---


def _DataTransformation_Log2(                                                   # pylint: disable=dangerous-default-value
    df:pd.DataFrame,
    sel:list[int]                    = [],
    rep:Union[None, str, float, int] = None,
    ) -> pd.DataFrame:
    """Performs a Log2 transformation of selected columns in df.

        Parameters
        ----------
        df: pd.DataFrame
            Dataframe with the data
        sel: list of int
            Column indexes
        method: str
            Transformation method. One of dtsConfig.oTransMethod
        rep: None, str, int, float
            To replace values in called method.

        Returns
        -------
        Dataframe
            With transformed columns.

        Notes
        -----
        - df is expected to be a copy whose values can be changed during
        transformation.
    """
    # Test in test.unit.data.test_method.Test_DataTransformation
    #region ---------------------------------------------> Log2 transformation
    #------------------------------> Log2
    if sel:
        df.iloc[:,sel] = np.log2(df.iloc[:,sel])
    else:
        df = np.log2(df)                                                        # type: ignore
    #------------------------------> Replace inf values
    if rep is not None:
        df = df.replace(-np.inf, rep)
    #endregion ------------------------------------------> Log2 transformation

    return df
#---


TRANS_METHOD = {
    'None' : _DataTransformation_None,
    'Log2' : _DataTransformation_Log2,
}


def DataTransformation(                                                         # pylint: disable=dangerous-default-value
    df:pd.DataFrame,
    sel:list[int]                    = [],
    method:LIT_Tran                  = 'Log2',
    rep:Union[None, str, float, int] = None,
    ) -> pd.DataFrame:
    """Performs a data transformation over the selected columns in the
        dataframe.

        Parameters
        ----------
        df: pd.DataFrame
            Dataframe with the data.
        sel: list of int
            Column indexes.
        method: str
            Transformation method. One of dtsConfig.oTransMethod.
        rep: None, str, int, float
            To replace values in called method.

        Returns
        -------
        pd.DataFrame
            With transformed values.

        Notes
        -----
        Correct data types in df are expected.
    """
    # Test in test.unit.data.test_method.Test_DataTransformation
    #region --------------------------------------------------> Transformation
    return TRANS_METHOD[method](df.copy(), sel=sel, rep=rep)
    #endregion -----------------------------------------------> Transformation
#---
#endregion ----------------------------------------------> Data Transformation


#region --------------------------------------------------> Data Normalization
def _DataNormalization_None(
    df:pd.DataFrame,                                                          # pylint: disable=unused-argument
    *args,
    **kwargs,
    ) -> pd.DataFrame:
    """This will just return the original df.

        Parameters
        ----------
        df: pd.DataFrame
            Dataframe with the data.

        Returns
        -------
        Dataframe
            Without any normalization.
    """
    # Test in test.unit.data.test_method.Test_DataNormalization
    return df
#---


def _DataNormalization_Median(                                                  # pylint: disable=dangerous-default-value
    df:pd.DataFrame,
    sel:list[int] = []
    ) -> pd.DataFrame:
    """Performs a Median normalization of selected columns in df.

        Parameters
        ----------
        df: pd.DataFrame
            Dataframe with the data.
        sel: list of int
            List of columns to normalize.

        Returns
        -------
        Dataframe
            With normalized columns.

        Notes
        -----
        - df is expected to be a copy whose values can be changed during
        normalization.
        - The median normalization is performed column wise.
        - NA values are skipped.
    """
    # Test in test.unit.data.test_method.Test_DataNormalization
    #region --------------------------------------------> Median Normalization
    if sel:
        median = df.iloc[:,sel].median(axis=0, skipna=True)
        df.iloc[:,sel] = df.iloc[:,sel].subtract(median, axis=1)                # type: ignore
    else:
        median = df.median(axis=0, skipna=True)
        df = df.subtract(median, axis=1)
    #endregion -----------------------------------------> Median Normalization

    return df
#---


NORM_METHOD = {
    'None'   : _DataNormalization_None,
    'Median' : _DataNormalization_Median,
}


def DataNormalization(                                                          # pylint: disable=dangerous-default-value
    df:pd.DataFrame,
    sel:list[int]   = [],
    method:LIT_Norm = 'Median'
    ) -> pd.DataFrame:
    """Perform a data normalization over the selected columns in the
        dataframe.

        Parameters
        ----------
        df: pd.DataFrame
            Dataframe with the data.
        sel: list of int
            Column indexes.
        method: str
            Normalization method. One of dtsConfig.oNormMethod.

        Returns
        -------
        pd.DataFrame
            With transformed values

        Notes
        -----
        Correct data types in df are expected.
    """
    # Test in test.unit.data.test_method.Test_DataNormalization
    #region ---------------------------------------------------> Normalization
    return NORM_METHOD[method](df.copy(), sel=sel)
    #endregion ------------------------------------------------> Normalization
#---
#endregion -----------------------------------------------> Data Normalization


#region -----------------------------------------------------> Data Imputation
def _DataImputation_None(df:pd.DataFrame, *args, **kwargs) -> pd.DataFrame: # pylint: disable=unused-argument
    """This will just return the original df.

        Parameters
        ----------
        df: pd.DataFrame
            Dataframe with the data.

        Returns
        -------
        Dataframe
            Without any imputation.
    """
    # Test in test.unit.data.test_method.Test_DataImputation
    return df
#---


def _DataImputation_NormalDistribution(                                         # pylint: disable=dangerous-default-value
    df:pd.DataFrame,                                                          # pylint: disable=unused-argument
    sel:list[int]=[],
    shift:float=float(mConfig.data.shift),
    width:float=float(mConfig.data.width),
    **kwargs
    ) -> pd.DataFrame:
    """Performs a Normal Distribution imputation of selected columns in df.

        Parameters
        ----------
        df: pd.DataFrame
            Dataframe with the data.
        sel: list of int
            List of columns to impute
        shift: float
            Shift for the center of the distribution.
        width: float
            Width of the distribution.

        Returns
        -------
        Dataframe
            With imputed columns.

        Notes
        -----
        - df is expected to be a copy whose values can be changed during
        imputation
        - The imputation is performed column wise.
    """
    # No Test. Random numbers
    #region ---------------------------------------------------------> Columns
    if sel:
        col = df.iloc[:,sel].columns
    else:
        col = df.columns
    #endregion ------------------------------------------------------> Columns

    #region ----------------------------------> Normal Distribution imputation
    for c in col:
        #------------------------------>
        std    = df[c].std(skipna=True)
        median = df[c].median(skipna=True)
        tIDX   = np.where(df[c].isna())[0]
        #------------------------------>
        df.loc[tIDX, c] = np.random.default_rng().normal(                       # type: ignore
            median-std*shift, std*width, len(tIDX))                             # type: ignore
    #endregion -------------------------------> Normal Distribution imputation

    return df
#---


IMPUTATION_METHOD = {
    'None'                : _DataImputation_None,
    'Normal Distribution' : _DataImputation_NormalDistribution,
}


def DataImputation(                                                             # pylint: disable=dangerous-default-value
    df:pd.DataFrame,
    sel:list[int]                                 = [],
    method:LIT_Imp = 'Normal Distribution',
    **kwargs
    ) -> pd.DataFrame:
    """Perform a data imputation over the selected columns in the
        dataframe.

        Parameters
        ----------
        df: pd.DataFrame
            Dataframe with the data
        sel: list of int
            Column indexes
        method: str
            Imputation method. One of dtsConfig.oImputationMethod

        Returns
        -------
        pd.DataFrame
            With transformed values

        Notes
        -----
        Correct data types in df are expected.
        For most methods, only np.nan values will be replaced.
    """
    # Test in test.unit.data.test_method.Test_DataImputation
    #region ------------------------------------------------------> Imputation
    return IMPUTATION_METHOD[method](df.copy(), sel=sel, **kwargs)
    #endregion ---------------------------------------------------> Imputation
#---
#endregion --------------------------------------------------> Data Imputation
#endregion ----------------------------------------------------------> Methods
