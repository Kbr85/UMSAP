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


"""Statistic calculations"""


#region -------------------------------------------------------------> Imports
from typing import Literal, Union, Optional

import numpy       as np
import pandas      as pd
import scipy.stats as sStats

import config.config  as mConfig
import data.method    as mMethod
import data.exception as mException
#endregion ----------------------------------------------------------> Imports


# Pandas lead to long lines, so this check will be disabled for this module
# pylint: disable=line-too-long


#region ----------------------------------------------------> Data Description
def DataRange(
    x     : Union[pd.Series, np.ndarray, list, tuple],
    margin: float=0,
    ) -> list[float]:
    """Return the range of x with an optional margin applied.
        Useful to set the axes limit in a matplotlib plot.

        Parameters
        ----------
        x : pd.Series, np.array, list or tuple of numbers.
        margin : float
            Expand the range by (max(x) - min(x)) * margin. Default is 0,
            meaning that no expansion of the max(x) and min(x) is done.

        Returns
        -------
        list of floats
            [min value, max value]

        Notes
        -----
        The return values will be calculated as:
            dm = (max(x) - min(x)) * margin
            [min(x) - dm, max(x) + dm]
        When margin is 0 then the return will simply be [min(x), max(x)]
    """
    # Test in test.unit.test_statistic.Test_DataRange
    #region -------------------------------------------------------> Variables
    msg = 'x must contain only numbers.'
    #endregion ----------------------------------------------------> Variables

    #region -----------------------------------------------------> Check Input
    #------------------------------> Type and Float
    #-------------->
    tType = type(x)
    #-------------->
    if tType == list or tType == tuple:
        try:
            nL = list(map(float, x))
        except Exception as e:
            raise mException.InputError(msg) from e
    elif tType == pd.Series:
        try:
            nL = list(map(float, x.values.tolist()))                            # type: ignore
        except Exception as e:
            raise mException.InputError(msg) from e
    elif tType == np.ndarray:
        if x.ndim == 1:                                                         # type: ignore
            try:
                nL = list(map(float, x.tolist()))                               # type: ignore
            except Exception as e:
                raise mException.InputError(msg) from e
        else:
            msg = 'A one dimensional np.array is expected here.'
            raise mException.InputError(msg)
    else:
        msg = 'x must be a tuple, list, numpy.ndarray or pandas.Series.'
        raise mException.InputError(msg)
    #------------------------------> Not empty
    if nL:
        pass
    else:
        msg = 'x cannot be empty.'
        raise mException.InputError(msg)
    #endregion --------------------------------------------------> Check Input

    #region ----------------------------------------------------------> Values
    #------------------------------>
    tMax = max(nL)
    tMin = min(nL)
    #------------------------------>
    dm = (tMax - tMin) * margin
    #endregion -------------------------------------------------------> Values

    return [tMin - dm, tMax + dm]
#---

def HistBin(x: pd.Series) -> tuple[float, float]:
    """Calculate the bin width for a histogram according to Freedman–Diaconis
        rule.

        Parameters
        ----------
        x : pd.Series
            Values.

        Returns
        -------
        tuple of float:
            (number_of_bins, bind_width)
    """
    # No Test
    #region --------------------------------------------------> Get Percentile
    q25, q75 = np.percentile(x, [25, 75])
    #endregion -----------------------------------------------> Get Percentile

    #region -------------------------------------------------------------> Bin
    width = 2 * (q75 - q25) * len(x) ** (-1/3)
    n = round((x.max() - x.min()) / width)
    #endregion ----------------------------------------------------------> Bin

    return (n, width)
#---
#endregion -------------------------------------------------> Data Description


#region ----------------------------------------------------> Data Preparation
def DataPreparation(
    df        : pd.DataFrame,                                                   # pylint: disable=unused-argument
    rDO       : dict,
    *args,
    resetIndex: bool=True,
    ) -> tuple[dict, str, Optional[Exception]]:
    """Perform the data preparation steps.

        Parameters
        ----------
        df: pd.DataFrame
            DataFrame read from CSV file.
        rDO: dict
            rDO dictionary from the PrepareRun step of the analysis.
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
                        'dfS' : pd.DataFrame
                    },
                    '',
                    None
                )                                  when everything went fine.
            -   ({}, 'Error message', Exception)   when something went wrong.

        Notes
        -----
        *args are ignored. They are needed for compatibility.
    """
    # Test in test.unit.test_statistic.DataPreparation
    #region ----------------------------------------> Run Data Preparation
    #------------------------------> dfI & dfF
    try:
        dfI, dfF = DataPrep_Float(
            df,
            rDO['Cero'],
            rDO['oc']['Column'],
            rDO['df']['ColumnR'],
            rDO['df']['ColumnF'],
        )
    except Exception as e:
        return ({}, 'Data Preparation failed', e)
    #------------------------------> Transformation
    try:
        dfT = DataTransformation(
            dfF,
            rDO['df']['ResCtrlFlat'],
            method = rDO['TransMethod'],
            rep    = np.nan if rDO['Cero'] else 0,
        )
    except Exception as e:
        return ({}, 'Data Transformation failed.', e)
    #------------------------------> Normalization
    try:
        dfN = DataNormalization(
            dfT, rDO['df']['ResCtrlFlat'], method=rDO['NormMethod'])
    except Exception as e:
        return ({}, 'Data Normalization failed.', e)
    #------------------------------> Imputation
    try:
        dfIm = DataImputation(
            dfN,
            rDO['df']['ResCtrlFlat'],
            method = rDO['ImpMethod'],
            shift  = rDO['Shift'],
            width  = rDO['Width'],
        )
    except Exception as e:
        return ({}, 'Data Imputation failed.', e)
    #------------------------------> Target Protein
    try:
        if rDO['df'].get('TargetProtCol', None) is not None:
            dfTP = mMethod.DFFilterByColS(
                dfIm, rDO['df']['TargetProtCol'], rDO['TargetProt'], 'e')
        else:
            dfTP = dfIm.copy()
    except Exception as e:
        msg = mConfig.mPDDataTargetProt.format(
            rDO['TargetProt'], rDO['df']['TargetProtCol'])
        return ({}, msg, e)
    #------------------------------> Exclude
    try:
        if rDO['df'].get('ExcludeR', None) is not None:
            dfE = mMethod.DFExclude(dfTP, rDO['df']['ExcludeR'])
        else:
            dfE = dfTP.copy()
    except Exception as e:
        msg = mConfig.mPDDataExclude.format(rDO['df']['ExcludeR'])
        return ({}, msg, e)
    #------------------------------> Score
    #-------------->
    try:
        if rDO['df'].get('ScoreCol', None) is not None:
            dfS = mMethod.DFFilterByColN(
                dfE, [rDO['df']['ScoreCol']], rDO['ScoreVal'], 'ge')
        else:
            dfS = dfE.copy()
    except Exception as e:
        msg = mConfig.mPDDataScore.format(rDO['df']['ScoreCol'])
        return ({}, msg, e)
    #-------------->
    if dfS.empty:
        return ({}, mConfig.mNoDataLeft, None)
    else:
        pass
    #endregion -------------------------------------> Run Data Preparation

    #region -------------------------------------------------> Reset index
    if resetIndex:
        dfS.reset_index(drop=True, inplace=True)
    else:
        pass
    #endregion ----------------------------------------------> Reset index

    #region -------------------------------------------------------> Print
    if mConfig.development:
        #------------------------------>
        dfList = [dfI, dfF, dfT, dfN, dfIm, dfTP, dfE, dfS]
        dfName = ['dfI', 'dfF', 'dfT', 'dfN', 'dfIm', 'dfTP', 'dfE', 'dfS']
        #------------------------------>
        print('')
        for i, a in enumerate(dfList):
            if a is not None:
                print(f'{dfName[i]}: {a.shape}')
            else:
                print(f'{dfName[i]}: None')
    else:
        pass
    #endregion ----------------------------------------------------> Print

    #region --------------------------------------------------->
    dictO = {
        'dfI' : dfI,
        'dfF' : dfF,
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
    df      : pd.DataFrame,
    cero    : bool,
    col     : list[int],
    colCero : list[int],
    colFloat: list[int]
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
    # Test in test.unit.test_statistic.Test_DataPrep_Float
    #region -------------------------------------------------------->
    dfI = df.iloc[:,col]
    #------------------------------>
    if cero:
        dfF = mMethod.DFReplace(dfI, [0, ''], np.nan, sel=colCero)
    else:
        dfF = mMethod.DFReplace(dfI, [''], np.nan, sel=colCero)
    #------------------------------>
    dfF.iloc[:,colFloat] = dfF.iloc[:,colFloat].astype('float')                 # type: ignore
    #endregion ----------------------------------------------------->

    return [dfI, dfF]
#endregion -------------------------------------------------> Data Preparation


#region -------------------------------------------------> Data Transformation
def _DataTransformation_None(
    df: 'pd.DataFrame',                                                         # pylint: disable=unused-argument
    *args,
    **kwargs,
    ) -> 'pd.DataFrame':
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
    # Test in test.unit.test_statistic.Test_DataTransformation
    return df
#---


def _DataTransformation_Log2(                                                   # pylint: disable=dangerous-default-value
    df : 'pd.DataFrame',
    sel: list[int]=[],
    rep: Union[None, str, float, int]=None,
    ) -> 'pd.DataFrame':
    """Performs a Log2 transformation of selected columns in df.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe with the data
        sel : list of int
            Column indexes
        method : str
            Transformation method. One of dtsConfig.oTransMethod
        rep: None, str, int, float
            To replace values in called method.

        Returns
        -------
        Dataframe
            With transformed columns

        Notes
        -----
        - df is expected to be a copy whose values can be changed during
        transformation.
    """
    # Test in test.unit.test_statistic.Test_DataTransformation
    #region ---------------------------------------------> Log2 transformation
    #------------------------------> Log2
    if sel:
        df.iloc[:,sel] = np.log2(df.iloc[:,sel])
    else:
        df = np.log2(df)                                                        # type: ignore
    #------------------------------> Replace inf values
    if rep is not None:
        df = df.replace(-np.inf, rep)
    else:
        pass
    #endregion ------------------------------------------> Log2 transformation

    return df
#---


TRANS_METHOD = {
    'None' : _DataTransformation_None,
    'Log2' : _DataTransformation_Log2,
}


def DataTransformation(                                                         # pylint: disable=dangerous-default-value
    df    : 'pd.DataFrame',
    sel   : list[int]=[],
    method: Literal['Log2', 'None']='Log2',
    rep   : Union[None, str, float, int]=None,
    ) -> 'pd.DataFrame':
    """Performs a data transformation over the selected columns in the
        dataframe.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe with the data
        sel : list of int
            Column indexes
        method : str
            Transformation method. One of dtsConfig.oTransMethod
        rep: None, str, int, float
            To replace values in called method.

        Returns
        -------
        pd.DataFrame
            With transformed values

        Notes
        -----
        Correct data types in df are expected.
    """
    # Test in test.unit.test_statistic.Test_DataTransformation
    #region --------------------------------------------------> Transformation
    return TRANS_METHOD[method](df.copy(), sel=sel, rep=rep)
    #endregion -----------------------------------------------> Transformation
#---
#endregion ----------------------------------------------> Data Transformation


#region --------------------------------------------------> Data Normalization
def _DataNormalization_None(
    df: 'pd.DataFrame',                                                         # pylint: disable=unused-argument
    *args,
    **kwargs,
    ) -> 'pd.DataFrame':
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
    # Test in test.unit.test_statistic.Test_DataNormalization
    return df
#---


def _DataNormalization_Median(                                                  # pylint: disable=dangerous-default-value
    df : 'pd.DataFrame',
    sel: list[int]=[]
    ) -> 'pd.DataFrame':
    """Performs a Median normalization of selected columns in df.

        Parameters
        ----------
        df: pd.DataFrame
            Dataframe with the data.
        sel: list of int
            List of columns to normalize

        Returns
        -------
        Dataframe
            With normalized columns

        Notes
        -----
        - df is expected to be a copy whose values can be changed during
        normalization.
        - The median normalization is performed column wise.
        - NA values are skipped.
    """
    # Test in test.unit.test_statistic.Test_DataNormalization
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
    df    : 'pd.DataFrame',
    sel   : list[int]=[],
    method: Literal['Median', 'None']='Median'
    ) -> 'pd.DataFrame':
    """Perform a data normalization over the selected columns in the
        dataframe.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe with the data
        sel : list of int
            Column indexes
        method : str
            Normalization method. One of dtsConfig.oNormMethod

        Returns
        -------
        pd.DataFrame
            With transformed values

        Notes
        -----
        Correct data types in df are expected.
    """
    # Test in test.unit.test_statistic.Test_DataNormalization
    #region ---------------------------------------------------> Normalization
    return NORM_METHOD[method](df.copy(), sel=sel)
    #endregion ------------------------------------------------> Normalization
#---
#endregion -----------------------------------------------> Data Normalization


#region -----------------------------------------------------> Data Imputation
def _DataImputation_None(df: 'pd.DataFrame', *args, **kwargs) -> 'pd.DataFrame':# pylint: disable=unused-argument
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
    # Test in test.unit.test_statistic.Test_DataImputation
    return df
#---


def _DataImputation_NormalDistribution(                                         # pylint: disable=dangerous-default-value
    df   : 'pd.DataFrame',                                                      # pylint: disable=unused-argument
    sel  : list[int]=[],
    shift: float=float(mConfig.confValues[mConfig.nwCheckDataPrep]['Shift']),
    width: float=float(mConfig.confValues[mConfig.nwCheckDataPrep]['Width']),
    **kwargs
    ) -> 'pd.DataFrame':
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
        std = df[c].std(skipna=True)
        median = df[c].median(skipna=True)
        tIDX = np.where(df[c].isna())[0]
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
    df    : 'pd.DataFrame',
    sel   : list[int]=[],
    method: Literal['Normal Distribution', 'None']='Normal Distribution',
    **kwargs
    ) -> 'pd.DataFrame':
    """Perform a data imputation over the selected columns in the
        dataframe.

        Parameters
        ----------
        df : pd.DataFrame
            Dataframe with the data
        sel : list of int
            Column indexes
        method : str
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
    # Test in test.unit.test_statistic.Test_DataImputation
    #region ------------------------------------------------------> Imputation
    return IMPUTATION_METHOD[method](df.copy(), sel=sel, **kwargs)
    #endregion ---------------------------------------------------> Imputation
#---
#endregion --------------------------------------------------> Data Imputation


#region -------------------------------------------------> Confidence Interval
def _CI_Mean_Diff_DF_True(
    df    : 'pd.DataFrame',
    col1  : list[int],
    col2  : list[int],
    alpha : float,
    fullCI: bool=True,
    roundN: Optional[int]=None,
    ) -> 'pd.DataFrame':
    """Calculate the confidence interval for the difference between means when
        samples are independent.

        Parameters
        ----------
        df: pd.DataFrame
            DataFrame with all the data
        col1: list[int]
            Control columns
        col2: list[int]
            Experiment columns
        alpha: float
            Significance level
        fullCI : bool
            Return full interval (True) or just (False) the CI value. Default is
            to return full interval.
        roundN : int or None
            Round numbers to the given number of decimal places.
            Default is None.

        Returns
        -------
        pd.Dataframe
            With two columns CI_l and CI_u if fullCI is True else one column CI.

        Notes
        -----
        - Input Check is performed CI_Mean_Diff_DF.
        - Further details:
            https://calcworkshop.com/confidence-interval/difference-in-means/
    """
    # Test in test.unit.test_statistic.Test_CI_Mean_Diff_DF
    #region ----------------------------------------------------------> Values
    #------------------------------>
    diffMean21 = (
        df.iloc[:,col2].mean(axis=1, skipna=True)                               # type: ignore
        -df.iloc[:,col1].mean(axis=1, skipna=True)                              # type: ignore
    )
    var1 = df.iloc[:,col1].var(axis=1, skipna=True)                             # type: ignore
    var2 = df.iloc[:,col2].var(axis=1, skipna=True)                             # type: ignore
    n1   = len(col1)
    n2   = len(col2)
    dfT  = n1 + n2 - 2
    #------------------------------>
    q    = 1-(alpha/2)
    t    = sStats.t.ppf(q, dfT)
    F    = np.where(var2 > var1, var2/var1, var1/var2)                          # type: ignore
    #------------------------------>
    ci = np.where(
        F > t,
        t*np.sqrt((var1/n1)+(var2/n2)),                                         # type: ignore
        t*np.sqrt((1/n1)+(1/n2))*np.sqrt(((n1-1)*var1+(n2-1)*var2)/dfT),        # type: ignore
    )
    #endregion -------------------------------------------------------> Values

    #region --------------------------------------------------------> Empty DF
    if fullCI:
        #------------------------------>
        dfO = pd.DataFrame(
            np.nan, columns=['CI_l', 'CI_u'], index=range(df.shape[0])          # type: ignore
        )
        #------------------------------>
        dfO['CI_l'] = diffMean21 - ci
        dfO['CI_u'] = diffMean21 + ci
    else:
        #------------------------------>
        dfO = pd.DataFrame(np.nan, columns=['CI'], index=range(df.shape[0]))    # type: ignore
        #------------------------------>
        dfO['CI'] = ci
    #endregion -----------------------------------------------------> Empty DF

    #region -----------------------------------------------------------> Round
    if roundN is not None:
        dfO = dfO.round(int(roundN))
    else:
        pass
    #endregion --------------------------------------------------------> Round

    return dfO
#---


def _CI_Mean_Diff_DF_False(
    df    : 'pd.DataFrame',
    col1  : list[int],
    col2  : list[int],
    alpha : float,
    fullCI: bool=True,
    roundN: Optional[int]=None,
    ) -> 'pd.DataFrame':
    """Calculate the confidence interval for the difference between means when
        samples are not independent.

        Parameters
        ----------
        df: pd.DataFrame
            DataFrame with all the data
        col1: list[int]
            Control columns
        col2: list[int]
            Experiment columns
        alpha: float
            Significance level
        fullCI : bool
            Return full interval (True) or just (False) the CI value. Default is
            to return full interval.
        roundN : int or None
            Round numbers to the given number of decimal places.
            Default is None.

        Returns
        -------
        pd.Dataframe
            With two columns CI_l and CI_u if fullCI is True else one column CI.

        Notes
        -----
        - Input Check is performed CI_Mean_Diff_DF.
        - It is expected that samples are paired in col1 and col2 like:
            col1 = (C1, C2, C3) and col2 = (E1, E2, E3)
        - Further details:
            https://calcworkshop.com/confidence-interval/difference-in-means/
    """
    # Test in test.unit.test_statistic.Test_CI_Mean_Diff_DF
    #region ----------------------------------------------------------> New Df
    ndf = pd.DataFrame(
        df.iloc[:,col2].values - df.iloc[:,col1].values,                        # type: ignore
        columns=range(len(col1))
    )
    #endregion -------------------------------------------------------> New Df

    return CI_Mean_DF(ndf, alpha, fullCI=fullCI, roundN=roundN)
#---


CI_MEAN_DIFF = {
    True : _CI_Mean_Diff_DF_True,
    False: _CI_Mean_Diff_DF_False,
}


def CI_Mean_Diff_DF(
    df    : 'pd.DataFrame',
    col1  : list[int],
    col2  : list[int],
    alpha : float,
    ind   : bool,
    fullCI: bool=True,
    roundN: Optional[int]=None,
    ) -> pd.DataFrame:
    """Calculate the confidence interval for the difference between means.

        Parameters
        ----------
        df: pd.DataFrame
            DataFrame with all the data
        col1: list[int]
            Control columns
        col2: list[int]
            Experiment columns
        alpha: float
            Significance level
        ind: bool
            Samples are independent (True) or not (False)
        fullCI : bool
            Return full interval (True) or just (False) the CI value. Default is
            to return full interval.
        roundN : int or None
            Round numbers to the given number of decimal places.
            Default is None.

        Returns
        -------
        pd.Dataframe
            With two columns CI_l and CI_u if fullCI is True else one column CI.

        Notes
        -----
        - The mean difference is calculated as ave(col2) - ave(col1)
        - For paired samples it is expected that samples are paired in col1 and
            col2 like: col1 = (C1, C2, C3) and col2 = (E1, E2, E3)
        - See also the _CI_Mean_Diff_DF_True and _CI_Mean_Diff_DF_False
        - Further details:
            https://calcworkshop.com/confidence-interval/difference-in-means/
    """
    # Test in test.unit.test_statistic.Test_CI_Mean_Diff_DF
    #region -------------------------------------------------------> Calculate
    return CI_MEAN_DIFF[ind](df, col1, col2, alpha, fullCI=fullCI,roundN=roundN)
    #endregion ----------------------------------------------------> Calculate
#---


def CI_Mean_DF(
    df    : 'pd.DataFrame',
    alpha : float,
    fullCI: bool=True,
    roundN: Optional[int]=None,
    ) -> 'pd.DataFrame':
    """Calculate the confidence interval for the mean.

        Parameters
        ----------
        df: pd.DataFrame
            Calculation will be performed for each row in the df. Each column in
            the row is considered as a measurement.
        alpha: float
            Significance level
        fullCI : bool
            Return full interval (True) or just (False) the CI value. Default is
            to return full interval.
        roundN : int or None
            Round numbers to the given number of decimal places.
            Default is None.

        Returns
        -------
        pd.Dataframe
            With two columns CI_l and CI_u if fullCI is True else one column CI.

        Notes
        -----
        - It is expected that df has no NA values.
        - Further details:
            https://calcworkshop.com/confidence-interval/difference-in-means/
    """
    # Test in test.unit.test_statistic.Test_CI_Mean_DF
    #region -------------------------------------------------------> Variables
    q = 1 - (float(alpha)/2)
    #endregion ----------------------------------------------------> Variables

    #region ----------------------------------------------------------> Values
    var  = df.var(axis=1, skipna=True)
    mean = df.mean(axis=1, skipna=True)
    t    = sStats.t.ppf(q, df.shape[1]-1)
    ci   = t*(var/np.sqrt(df.shape[1]))
    #endregion -------------------------------------------------------> Values

    #region --------------------------------------------------------------> DF
    if fullCI:
        #------------------------------>
        dfO = pd.DataFrame(
            np.nan, columns=['CI_l', 'CI_u'], index=range(df.shape[0])          # type: ignore
        )
        #------------------------------>
        dfO['CI_l'] = mean - ci
        dfO['CI_u'] = mean + ci
    else:
        #------------------------------>
        dfO = pd.DataFrame(np.nan, columns=['CI'], index=range(df.shape[0]))    # type: ignore
        #------------------------------>
        dfO['CI'] = ci
    #endregion -----------------------------------------------------------> DF

    #region -----------------------------------------------------------> Round
    if roundN is not None:
        dfO = dfO.round(int(roundN))
    else:
        pass
    #endregion --------------------------------------------------------> Round

    return dfO
#---
#endregion ----------------------------------------------> Confidence Interval


#region ----------------------------------------------------------------> TEST
def Test_f_DF(
    df     : 'pd.DataFrame',
    col1   : list[int],
    col2   : list[int],
    alpha  : float=0.05,
    roundTo: Optional[int]=None,
    ) -> 'pd.DataFrame':
    """Perform a test for equal variance.

        Parameters
        ----------
        df: pd.DataFrame
            Calculation will be performed for each row in the df. Each column in
            the row is considered as a measurement.
        col1: list[int]
            Control columns
        col2: list[int]
            Experiment columns
        alpha: float
            Significance level
        roundTo: int
            Number of decimal places for the value of f and P in the output df.

        Returns
        -------
        pd.DataFrame
            With three columns ['f', 'P', 'S']

        Notes
        -----
        - The test is conducted taking the greater variance in the numerator of
            F and P as the two tail value.
        - Invalid values in the input for roundTo are silently ignored and the
            df with full length values is returned.
    """
    # Test in test.unit.test_statistic.Test_f_DF
    #region --------------------------------------------------------> Empty DF
    dfO = pd.DataFrame(
        np.nan, columns=['f', 'P', 'S'], index=range(df.shape[0])               # type: ignore
    )
    F = pd.DataFrame(
        np.nan, columns=['F', 'N', 'D'], index=range(df.shape[0])               # type: ignore
    )
    #endregion -----------------------------------------------------> Empty DF

    #region ----------------------------------------------------------> Values
    N1 = len(col1)-1
    N2 = len(col2)-1
    var1 = df.iloc[:,col1].var(axis=1, skipna=True)                             # type: ignore
    var2 = df.iloc[:,col2].var(axis=1, skipna=True)                             # type: ignore
    F['F'] = np.where(var2 > var1, var2/var1, var1/var2)                        # type: ignore
    F['N'] = np.where(var2 > var1, N2, N1)                                      # type: ignore
    F['D'] = np.where(var2 > var1, N1, N2)                                      # type: ignore
    #endregion -------------------------------------------------------> Values

    #region ---------------------------------------------------------> Fill DF
    #------------------------------>
    dfO['f'] = F['F'].to_numpy()
    dfO['P'] = 2 * sStats.f.sf(F['F'], F['N'], F['D'])
    dfO['S'] = np.where(dfO['P'] < alpha, True, False)
    #------------------------------>
    if roundTo is not None:
        try:
            dfO[['f', 'P']] = dfO[['f', 'P']].round(int(roundTo))
        except Exception:
            pass
    else:
        pass
    #endregion ------------------------------------------------------> Fill DF

    return dfO
#---


def Test_chi(df:pd.DataFrame, alpha:float, check5: bool=True) -> list:
    """Performs a chi square test.

        Parameters
        ----------
        df: pd.DataFrame
            Data
        alpha: float
            Alpha level
        check5: bool
            Check correct number of values.

        Returns
        -------
        list[int, sStats.chi2_contingency]

        Notes
        -----
        Threshold of number of cells with values less than 5 from:
        D. Yates, D. Moore, G. McCabe, The practice of Statistics
        (Freeman, New York, 1999), p. 734.
    """
    # Test in test.unit.test_statistic.Test_chi
    #region ---------------------------------------------------> Remove 0 rows
    dfT = df[df.any(axis=1)]
    #endregion ------------------------------------------------> Remove 0 rows

    #region ---------------------------------------------------> Check < 5
    if check5:
        a,b = dfT.shape
        n = np.count_nonzero(dfT < 5)
        if n/(a*b) < 0.2:
            pass
        else:
            return [-1,[]]
    else:
        pass
    #endregion ------------------------------------------------> Check < 5

    #region ---------------------------------------------------> Calculate
    try:
        chi = sStats.chi2_contingency(dfT)
    except Exception:
        return [-1,[]]
    #endregion ------------------------------------------------> Calculate

    return [1,chi] if chi[1] < alpha else [0, chi]
#---


def Test_t_getP(
    t   : Union['pd.DataFrame', 'np.ndarray'],
    tdf : Union['pd.DataFrame', 'np.ndarray', 'int'],
    test: mConfig.litTestSide,
    ) -> 'pd.DataFrame':
    """Get p value for a given t value.

        Parameters
        ----------
        t: pd.DataFrame
            Calculated t values.
        tdf: pd.DataFrame or int
            Calculated degrees of freedom.
        test: str
            Type of t test. Default is 'ts'.

        Returns
        -------
        pd.DataFrame with the p values.
    """
    # No Test
    #region -----------------------------------------------------> Get P value
    if test == 'ts':
        return 2 * sStats.t.sf(np.abs(t), tdf)                                  # type: ignore
    elif test == 's':
        return sStats.t.cdf(t, tdf)                                             # type: ignore
    elif test == 'l':
        return sStats.t.sf(t, tdf)                                              # type: ignore
    else:
        msg = mConfig.mNotImplemented.format(test)
        raise mException.ExecutionError(msg)
    #endregion --------------------------------------------------> Get P value
#---


def Test_t_PS_DF(
    df     : 'pd.DataFrame',
    col1   : list[int],
    col2   : list[int],
    value  : float=0,
    alpha  : float=0.05,
    roundTo: Optional[int]=None,
    tType  : mConfig.litTestSide='ts',
    delta  : float = 0,
    ) -> 'pd.DataFrame':
    """Perform a t test for paired samples.

        Parameters
        ----------
        df: pd.DataFrame
            Calculation will be performed for each row in the df. Each column in
            the row is considered as a measurement.
        col1: list[int]
            Control columns
        col2: list[int]
            Experiment columns
        value: float
            Hypothetical value for the mean difference. Default is 0.
        alpha: float
            Significance level
        roundTo: int
            Number of decimal places for the value of t and P in the output df.
        tType: str
            Type of T test. One of 'ts','l','s'. Default is 'ts'
        delta: float
            For TOST equivalence test. Default is 0, regular T test.

        Returns
        -------
        pd.DataFrame
            With three columns ['t', 'P', 'S']

        Notes
        -----
        - Invalid values in the input for roundTo are silently ignored and the
            df with full length values is returned.
        https://www.reneshbedre.com/blog/ttest.html
        https://www.datanovia.com/en/lessons/t-test-formula/
    """
    # Test in test.unit.test_statistic.Test_t_PS_DF
    #region ----------------------------------------------------------> Values
    ndf = pd.DataFrame(
        df.iloc[:,col2].values - df.iloc[:,col1].values,                        # type: ignore
        columns=range(len(col1)),
    )
    #------------------------------> m, s, n, t
    m = ndf.mean(axis=1, skipna=True)
    s = ndf.std(axis=1, skipna=True)
    n = ndf.shape[1]
    t = (m-value-delta)/(s/np.sqrt(n))
    #endregion -------------------------------------------------------> Values

    #region ----------------------------------------------------------> DF out
    #------------------------------>
    dfO = pd.DataFrame(
        np.nan, columns=['t', 'P', 'S'], index=range(df.shape[0])               # type: ignore
    )
    #------------------------------>
    dfO['t'] = t.to_numpy()
    dfO['P'] = Test_t_getP(t, n-1, tType)
    dfO['S'] = np.where(dfO["P"] < alpha, True, False)
    #------------------------------>
    if roundTo is not None:
        try:
            dfO[['t', 'P']] = dfO[['t', 'P']].round(int(roundTo))
        except Exception:
            pass
    else:
        pass
    #endregion -------------------------------------------------------> DF out

    return dfO
#---


def Test_t_IS_DF(
    df     : 'pd.DataFrame',
    col1   : list[int],
    col2   : list[int],
    alpha  : float=0.05,
    f      : Literal[None, True, False]=None,
    roundTo: Optional[int]=None,
    tType  : mConfig.litTestSide='ts',
    delta  : float=0,
    ) -> 'pd.DataFrame':
    """Perform a t test for independent samples.

        Parameters
        ----------
        df: pd.DataFrame
            Calculation will be performed for each row in the df. Each column in
            the row is considered as a measurement.
        col1: list[int]
            Control columns
        col2: list[int]
            Experiment columns
        alpha: float
            Significance level
        f: None, True, False
            Perform F-test (None) or assume result will be significant (True) or
            not (False)
        roundTo: int
            Number of decimal places for the value of t and P in the output df.
        tType: One of ts, l, s
            Type of t test to perform.
        delta: float
            For TOST equivalence test. Default is 0, regular T test.

        Returns
        -------
        pd.DataFrame

        Notes
        -----
        - Invalid values in the input for roundTo are silently ignored and the
            df with full length values is returned.
        - Further details
            https://www.reneshbedre.com/blog/ttest.html
            https://www.datanovia.com/en/lessons/t-test-formula/
    """
    # Test in test.unit.test_statistic.Test_t_IS_DF
    #region ----------------------------------------------------------> Values
    #------------------------------> m, s, n
    m1 = df.iloc[:,col1].mean(axis=1, skipna=True)                              # type: ignore
    m2 = df.iloc[:,col2].mean(axis=1, skipna=True)                              # type: ignore
    var1 = df.iloc[:,col1].var(axis=1, skipna=True)                             # type: ignore
    var2 = df.iloc[:,col2].var(axis=1, skipna=True)                             # type: ignore
    n1 = len(col1)
    n2 = len(col2)
    dem = n1 + n2 - 2
    dfN = n1 + n2 - 1
    #------------------------------> F
    if f is None:
        F = Test_f_DF(df, col1, col2, alpha)
    elif f:
        F = pd.DataFrame(
            df.shape[0]*[True], columns=['S'], index=range(df.shape[0])
        )
    else:
        F = pd.DataFrame(
            df.shape[0]*[False], columns=['S'], index=range(df.shape[0])
        )
    #------------------------------> t, ndf
    tt = np.where(
        F['S'],
        (m2 - m1 - delta)/(np.sqrt((var1/n1)+(var2/n2))),                                           # type: ignore
        (m2 - m1 - delta)/(np.sqrt((1/n1)+(1/n2))*np.sqrt(((n1-1)*var1+(n2-1)*var2)/(dem))),        # type: ignore
    )

    tdf = np.where(
        F['S'],
        np.square((var1/n1)+(var2/n2))/(((var1*var1)/(n1*n1*(n1-1)))+((var2*var2)/(n2*n2*(n2-1)))), # type: ignore
        dfN,
    )
    #endregion -------------------------------------------------------> Values

    #region ----------------------------------------------------------> DF Out
    #------------------------------>
    dfO = pd.DataFrame(
        np.nan, columns=['t', 'P', 'S'], index=range(df.shape[0]),              # type: ignore
    )
    #------------------------------>
    dfO['t'] = tt
    dfO['P'] = Test_t_getP(tt, tdf, tType)
    dfO['S'] = np.where(dfO["P"] < alpha, True, False)
    #------------------------------>
    if roundTo is not None:
        try:
            dfO[['t', 'P']] = dfO[['t', 'P']].round(int(roundTo))
        except Exception:
            pass
    else:
        pass
    #endregion -------------------------------------------------------> DF Out

    return dfO
#---


def Test_tost(
    df      : 'pd.DataFrame',
    col1    : list[int],
    col2    : list[int],
    sample  : Literal['p', 'i'],
    f       : Literal[None, True, False]=None,
    delta   : Optional['pd.DataFrame']=None,
    alpha   : float=0.05,
    beta    : float=0.05,
    gamma   : float=0.80,
    d       : float=0,
    deltaMax: Optional[float]=None,
    ) -> 'pd.DataFrame':
    """Perform a TOST test.

        Parameters
        ----------
        df: pd.DataFrame
            DataFrame with data.
        col1: list[int]
            Column numbers if df for control
        col2: list[int]
            Column numbers in df for experiment
        sample: One of 'p' or 'i'
            Paired or Independent samples.
        f: Bool or None
            Perform F-test (None) or assume result will be significant (True) or
            not (False).
        delta: pd.DataFrame
            Delta value for peptides in df.
        alpha: float
            Alpha level
        beta: float
            Beta level
        gamma: float
            Gamma level
        d: float
            Absolute difference. Default to 0.
        deltaMax: float
            Maximum value for delta.

        Returns
        -------
        pd.DataFrame
            Columns in the df are:
            P t1, p1, s1, t2, p2, s2

        Notes
        -----
        https://pubs.acs.org/doi/pdf/10.1021/ac053390m
    """
    # Test in test.unit.data.test_statistic.Test_tost
    #region --------------------------------------------------------> Empty df
    dfo = pd.DataFrame(
        np.nan,                                                                 # type: ignore
        columns=['P','t1', 'p1', 's1', 't2', 'p2', 's2'],
        index=range(df.shape[0])
    )
    #endregion -----------------------------------------------------> Empty df

    #region -----------------------------------------------------------> Delta
    if delta is not None:
        tDelta = delta
    else:
        try:
            tDelta = Test_tost_delta(
                df.iloc[:,col1], alpha, beta, gamma, d=d, deltaMax=deltaMax)
        except Exception as e:
            raise e
    #endregion --------------------------------------------------------> Delta

    #region ----------------------------------------------------------> T test
    if sample == 'p':
        dfo.loc[:,['t1', 'p1', 's1']] = Test_t_PS_DF(
            # pylint: disable-next=invalid-unary-operand-type
            df, col1, col2, delta=-tDelta, alpha=alpha, tType='l').to_numpy()   # type: ignore
        dfo.loc[:,['t2', 'p2', 's2']] = Test_t_PS_DF(
            df, col1, col2, delta=tDelta, alpha=alpha, tType='s').to_numpy()    # type: ignore
    else:
        dfo.loc[:,['t1', 'p1', 's1']] = Test_t_IS_DF(
            # pylint: disable-next=invalid-unary-operand-type
            df, col1, col2, delta=-tDelta, alpha=alpha, f=f, tType='l'          # type: ignore
        ).to_numpy()
        dfo.loc[:,['t2', 'p2', 's2']] = Test_t_IS_DF(
            df, col1, col2, delta=tDelta, alpha=alpha, f=f, tType='s'           # type: ignore
        ).to_numpy()
    #endregion -------------------------------------------------------> T test

    #region ---------------------------------------------------------------> P
    dfo['P'] = np.where(dfo['p1'] > dfo['p2'], dfo['p1'], dfo['p2'])
    #endregion ------------------------------------------------------------> P

    return dfo
#---


def Test_tost_delta(
    df      : Union['pd.DataFrame', 'pd.Series'],
    alpha   : float,
    beta    : float,
    gamma   : float,
    d       : float=0,
    deltaMax: Optional[float]=None,
    ) -> Union[pd.Series, 'np.ndarray']:
    """Calculate the delta values for a TOST test.

        Parameters
        ----------
        df: pd.DataFrame
            DataFrame with the values.
        alpha: float
            Alpha level.
        beta: float
            Beta level.
        gamma: float
            Gamma level.
        d: float
            Absolute difference. Default is 0.
        deltaMax: float or None
            Maximum allowed value for delta.

        Returns
        -------
        pd.Series
            Delta value for all peptides in df.

        Notes
        -----
        Delta is calculated according to:
        https://pubs.acs.org/doi/pdf/10.1021/ac053390m
    """
    # Test in test.unit.test_statistic.Test_tost_delta
    #region -------------------------------------------------------> Variables
    s = df.std(axis=1)                                                          # type: ignore
    n = df.shape[1]
    chi2 = sStats.chi2.ppf(1-gamma, (n-1))
    #------------------------------>
    sCorr = s * np.sqrt((n-1)/chi2)
    #------------------------------>
    ta1 = sStats.t.ppf(1 - alpha, 2*n - 2)
    tb1 = sStats.t.ppf(1 - beta/2, 2*n -2)
    #------------------------------>
    delta = d + sCorr * (ta1 + tb1) * np.sqrt(2/n)
    #endregion ----------------------------------------------------> Variables

    #region --------------------------------------------------> Check deltaMax
    if deltaMax is not None:
        delta = np.where(delta > deltaMax, deltaMax, delta)
    else:
        pass
    #endregion -----------------------------------------------> Check deltaMax

    return delta
#---


def Test_slope(df: 'pd.DataFrame', nL: list[int]=[]) -> list[float]:            # pylint: disable=dangerous-default-value
    """Perform a Test for Homogeneity of Regression.

        Parameters
        ----------
        df: pd.DataFrame
            DataFrame with the x,y values for each regression line e.g.
            X1 Y1 X2 Y2 Xn Yn
        nL: list of int
            Columns in df will be grouped with the size of each group given by
            the elements in n and the total number of groups being equal to the
            number of elements in n. If None only one group is created.

        Returns
        -------
        list[float]
            One P value for each group. See n in Parameters.

        Notes
        -----
        The procedure used here is described in:
        http://vassarstats.net/textbook/index.html Chapter 17.

        If df has columns X1,Y1,X2,Y2,X3,Y3,X4,Y4,X5,Y5 and n is [3,2]
        then two P values will be returned one for test performed with
        X1,Y1,X2,Y2,X3,Y3 and one for X4,Y4,X5,Y5.

        X,Y pairs in a group can be of different length but X and Y must have
        the same number of elements.
    """
    # Test in test.unit.test_statistic.Test_test_slope
    #region -------------------------------------------------------> Variables
    p = []
    nL = nL if nL else [1]
    #endregion ----------------------------------------------------> Variables

    #region --------------------------------------------------------> Run
    #------------------------------> Number of points in each column N
    n = df.notna().sum()
    #------------------------------> SUM(X)
    sumCol = df.sum(axis=0)
    #------------------------------> SUM(X^2)
    sumCol2 = (df.pow(2)).sum(axis=0)
    #------------------------------> SUM(XY)
    sumXY = pd.DataFrame(index=df.index)
    for k in range(0, df.shape[1], 2):
        sumXY[k] = df.iloc[:,k] * df.iloc[:,k+1]
    sumXY = sumXY.sum(axis=0)
    #------------------------------> SUM(X) - (SUM(X)^2)/N
    ss = sumCol2 - sumCol.pow(2)/n
    #------------------------------> SUM(XY) - SUM(X)SUM(Y)/N
    sc = pd.Series(index=sumXY.index)
    for k in range(0, df.shape[1], 2):
        sc[k] = sumXY[k] - ((sumCol[k]*sumCol[k+1])/n.iloc[k])
    #------------------------------>
    k = 0
    j = 0
    for nG in nL:
        try:
            #------------------------------> SUM(SC) for Group
            scwg = sc.iloc[j:j+nG].sum()
            #------------------------------> SUM(SS) for Group
            sswgx = ss.iloc[range(k,k+2*nG,2)].sum()     # type: ignore
            sswgy = ss.iloc[range(k+1,k+2*nG,2)].sum()   # type: ignore
            #------------------------------> SUM(SC^2/SS) - SCwg^2/SSwg
            a = sc.iloc[j:j+nG].pow(2)
            b = ss.iloc[range(k,k+2*nG,2)].set_axis(a.index.values) # type: ignore
            ssb_reg = (a/b).sum() - ((scwg*scwg)/sswgx)
            #------------------------------>
            ssy_rem = sswgy - ((scwg*scwg)/sswgx) - ssb_reg
            #------------------------------>
            dfb_reg = nG-1
            dfy_rem = n.iloc[range(k,k+2*nG,2)].sum() - 2*nG # type: ignore
            #------------------------------> F value
            f = (ssb_reg/dfb_reg)/(ssy_rem/dfy_rem)
            #------------------------------> P value
            p.append(sStats.f.sf(f, dfb_reg, dfy_rem))
        except Exception:
            p.append(np.nan)
        #------------------------------> Next Group
        k = k + 2*nG
        j = j + nG
    #endregion -----------------------------------------------------> Run

    return p
#---
#endregion -------------------------------------------------------------> TEST
