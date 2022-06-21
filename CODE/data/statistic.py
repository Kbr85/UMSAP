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

import numpy as np
import pandas as pd
import scipy.stats as sStats

import config.config as mConfig
import data.check as mCheck
import data.exception as mException
#endregion ----------------------------------------------------------> Imports


#region ----------------------------------------------------> Data Description
# def DataRange(
#     x: Union[pd.Series, np.ndarray, list, tuple], margin: float=0
#     ) -> list[float]:
#     """Return the range of x with an optional margin applied. 
#         Usefull to set the axes limit in a matplotlib plot.
    
#         See Notes below for more details.

#         Parameters
#         ----------
#         x : pd.Serie, np.array, list or tuple of numbers
#         margin : float
#             Expand the range by (max(x) - min(x)) * margin. Default is 0, 
#             meaning that no expansion of the max(x) and min(x) is done.

#         Returns
#         -------
#         list of floats
#             [min value, max value]

#         Raise
#         -----
#         InputError:
#             - When x is not pd.Series or list
#             - When elements in x cannot be cast to float.
#             - When x is empty
            
#         Notes
#         -----
#         The return values will be calculated as:
#             dm = (max(x) - min(x)) * margin
#             [min(x) - dm, max(x) + dm]
#         When margin is 0 then the return will simply be [min(x), max(x)]
#     """
#     #region -------------------------------------------------------> Variables
#     msg = 'x must contain only numbers.'
#     #endregion ----------------------------------------------------> Variables
    
#     #region -----------------------------------------------------> Check Input
#     #------------------------------> Type and Float
#     #-------------->  
#     tType = type(x)
#     #--------------> 
#     if tType == list or tType == tuple:
#         try:
#             nL = list(map(float, x))
#         except Exception:
#             raise dtsException.InputError(msg)
#     elif tType == pd.Series:
#         try:
#             nL = list(map(float, x.values.tolist()))
#         except Exception:
#             raise dtsException.InputError(msg)
#     elif tType == np.ndarray:
#         try:
#             if x.ndim == 1:
#                 nL = list(map(float, x.tolist()))
#             else:
#                 msg = 'A one dimensional np.array is expected here.'
#                 raise dtsException.InputError(msg)
#         except Exception:
#             raise dtsException.InputError(msg)
#     else:
#         msg = 'x must be a tuple, list, numpy.ndarray or pandas.Series.'
#         raise dtsException.InputError(msg)        
#     #------------------------------> Not empty
#     if nL:
#         pass
#     else:
#         msg = 'x cannot be empty.'
#         raise dtsException.InputError(msg)
#     #endregion --------------------------------------------------> Check Input
    
#     #region ----------------------------------------------------------> Values
#     #------------------------------> 
#     tmax = max(nL)
#     tmin = min(nL)
#     #------------------------------> 
#     dm = (tmax - tmin) * margin
#     #endregion -------------------------------------------------------> Values
    
#     return [tmin - dm, tmax + dm]
# #---

# def HistBin(x: pd.Series) -> tuple[float, float]:
#     """Calculate the bin width for a histogram according to Freedman–Diaconis 
#         rule

#         Parameters
#         ----------
#         x : pd.Series
#             Values 

#         Returns
#         -------
#         tuple of float:
#             (number_of_bins, bind_width)
#     """
#     #region --------------------------------------------------> Get Percentile
#     q25, q75 = np.percentile(x, [25, 75])
#     #endregion -----------------------------------------------> Get Percentile
    
#     #region -------------------------------------------------------------> Bin
#     width = 2 * (q75 - q25) * len(x) ** (-1/3)
#     n = round((x.max() - x.min()) / width)    
#     #endregion ----------------------------------------------------------> Bin
    
#     return (n, width)
# #---
#endregion -------------------------------------------------> Data Description


#region -------------------------------------------------> Data Transformation
def _DataTransformation_None(
    df: 'pd.DataFrame', 
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
    return df
#---


def _DataTransformation_Log2(
    df: 'pd.DataFrame', 
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
    #region ---------------------------------------------> Log2 transformation
    #------------------------------> Log2
    if sel:
        df.iloc[:,sel] = np.log2(df.iloc[:,sel])
    else:
        df = np.log2(df)
    #------------------------------> Replace inf values
    if rep is not None:
        df = df.replace(-np.inf, rep)
    else:
        pass
    #endregion ------------------------------------------> Log2 transformation 

    return df
#---


#------------------------------> Here to reference the module methods
TRANS_METHOD = {
    'None' : _DataTransformation_None,
    'Log2' : _DataTransformation_Log2,
}


def DataTransformation(
    df: 'pd.DataFrame', 
    sel: list[int]=[], 
    method: Literal['Log2']='Log2',
    rep: Union[None, str, float, int]=None,
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
    #region --------------------------------------------------> Transformation
    return TRANS_METHOD[method](df.copy(), sel=sel, rep=rep)
    #endregion -----------------------------------------------> Transformation
#---
#endregion ----------------------------------------------> Data Transformation


#region --------------------------------------------------> Data Normalization
def _DataNormalization_None(
    df: 'pd.DataFrame', *args, **kwargs,
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
    return df
#---


def _DataNormalization_Median(
    df: 'pd.DataFrame', 
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
    #region --------------------------------------------> Median Normalization
    #------------------------------> Median
    if sel:
        median = df.iloc[:,sel].median(axis=0, skipna=True)
    else:
        median = df.median(axis=0, skipna=True)
    #------------------------------> Normalization
    if sel:
        df.iloc[:,sel] = df.iloc[:,sel].subtract(median, axis=1)
    else:
        df = df.subtract(median, axis=1)
    #endregion -----------------------------------------> Median Normalization

    return df
#---


#------------------------------> Here to reference the module methods
NORM_METHOD = {
    'None'   : _DataNormalization_None,
    'Median' : _DataNormalization_Median,
}


def DataNormalization(
    df: 'pd.DataFrame', 
    sel: list[int]=[], 
    method: Literal['Median']='Median'
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
    #region ---------------------------------------------------> Normalization
    return NORM_METHOD[method](df.copy(), sel=sel) 
    #endregion ------------------------------------------------> Normalization
#---
#endregion -----------------------------------------------> Data Normalization


#region -----------------------------------------------------> Data Imputation
def _DataImputation_None(df: 'pd.DataFrame', *args, **kwargs) -> 'pd.DataFrame':
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
    return df
#---


def _DataImputation_NormalDistribution(
    df: 'pd.DataFrame', 
    sel: list[int]=[],
    shift=mConfig.values[mConfig.nwCheckDataPrep]['Shift'],
    width=mConfig.values[mConfig.nwCheckDataPrep]['Width'],
    **kwargs
    ) -> 'pd.DataFrame':
    """Performs a Normal Distribution imputation of selected columns in df. 
    
        See Notes below for more details.

        Parameters
        ----------
        df: pd.DataFrame
            Dataframe with the data.
        sel: list of int
            List of columns to impute

        Returns
        -------
        Dataframe
            With imputed columns
        
        Raise
        -----
        ExecutionError
            - When imputation fails

        Notes
        -----
        - Input check is performed in DataImputation
        - df is expected to be a copy whose values can be changed during 
        imputation
        - The imputation is performed column wise.
        - Data is expected to be normalized to a mean of 0.
    """
    #region ---------------------------------------------------------> Columns
    if sel is not None:
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
        df.loc[tIDX, c] = np.random.default_rng().normal(       # type: ignore
            median-std*shift, std*width, len(tIDX))             # type: ignore
    #endregion -------------------------------> Normal Distribution imputation

    return df
#---


#------------------------------> Here to reference the module methods
IMPUTATION_METHOD = {
    'None'                : _DataImputation_None,
    'Normal Distribution' : _DataImputation_NormalDistribution,
}


def DataImputation(
    df: 'pd.DataFrame', 
    sel: list[int]=[], 
    method: Literal['Normal Distribution']='Normal Distribution',
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
    #region ------------------------------------------------------> Imputation
    return IMPUTATION_METHOD[method](df.copy(), sel=sel, **kwargs)
    #endregion ---------------------------------------------------> Imputation
#---
#endregion --------------------------------------------------> Data Imputation


#region -------------------------------------------------> Confidence Interval
def _CI_Mean_Diff_DF_True(
    df: 'pd.DataFrame',
    col1: list[int],
    col2: list[int],
    alpha: float,
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
    #region ----------------------------------------------------------> Values
    #------------------------------> 
    diffMean21 = (
        df.iloc[:,col2].mean(axis=1, skipna=True)
        -df.iloc[:,col1].mean(axis=1, skipna=True)
    )
    var1 = df.iloc[:,col1].var(axis=1, skipna=True)
    var2 = df.iloc[:,col2].var(axis=1, skipna=True)
    n1   = len(col1)
    n2   = len(col2)
    dfT  = n1 + n2 - 2
    #------------------------------> 
    q    = 1-(alpha/2)
    t    = sStats.t.ppf(q, dfT)
    F    = np.where(var2 > var1, var2/var1, var1/var2)
    #------------------------------> 
    ci = np.where(
        F > t, 
        t*np.sqrt((var1/n1)+(var2/n2)), 
        t*np.sqrt((1/n1)+(1/n2))*np.sqrt(((n1-1)*var1+(n2-1)*var2)/dfT),    
    )
    #endregion -------------------------------------------------------> Values

    #region --------------------------------------------------------> Empty DF
    if fullCI:
        #------------------------------> 
        dfO = pd.DataFrame(
            np.nan, columns=['CI_l', 'CI_u'], index=range(df.shape[0]) # type: ignore
        )
        #------------------------------> 
        dfO['CI_l'] = diffMean21 - ci
        dfO['CI_u'] = diffMean21 + ci
    else:
        #------------------------------> 
        dfO = pd.DataFrame(np.nan, columns=['CI'], index=range(df.shape[0])) # type: ignore
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
    df: 'pd.DataFrame',
    col1: list[int],
    col2: list[int],
    alpha: float,
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
    #region ----------------------------------------------------------> New Df
    ndf = pd.DataFrame(
        df.iloc[:,col2].values - df.iloc[:,col1].values,
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
    df: 'pd.DataFrame',
    col1: list[int],
    col2: list[int],
    alpha: float,
    ind: bool,
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
    #region -------------------------------------------------------> Calculate
    try:
        return CI_MEAN_DIFF[ind](
            df, col1, col2, alpha, fullCI=fullCI, roundN=roundN)
    except Exception as e:
        raise e
    #endregion ----------------------------------------------------> Calculate
#---


def CI_Mean_DF(
    df: 'pd.DataFrame',
    alpha: float,
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
            np.nan, columns=['CI_l', 'CI_u'], index=range(df.shape[0]) # type: ignore
        )
        #------------------------------>
        dfO['CI_l'] = mean - ci
        dfO['CI_u'] = mean + ci
    else:
        #------------------------------>
        dfO = pd.DataFrame(np.nan, columns=['CI'], index=range(df.shape[0])) # type: ignore
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
    df: 'pd.DataFrame',
    col1: list[int],
    col2: list[int],
    alpha:float=0.05,
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
    #region --------------------------------------------------------> Empty DF
    dfO = pd.DataFrame(
        np.nan, columns=['f', 'P', 'S'], index=range(df.shape[0]) # type: ignore
    )
    F = pd.DataFrame(
        np.nan, columns=['F', 'N', 'D'], index=range(df.shape[0]) # type: ignore
    )
    #endregion -----------------------------------------------------> Empty DF

    #region ----------------------------------------------------------> Values
    N1 = len(col1)-1
    N2 = len(col2)-1
    var1 = df.iloc[:,col1].var(axis=1, skipna=True)
    var2 = df.iloc[:,col2].var(axis=1, skipna=True)
    F['F'] = np.where(var2 > var1, var2/var1, var1/var2)
    F['N'] = np.where(var2 > var1, N2, N1)
    F['D'] = np.where(var2 > var1, N1, N2)
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

# def test_chi(df:pd.DataFrame, alpha:float, check5: bool=True) -> list:
#     """
    
#         Notes
#         -----
#         Threshold of number of cells with values less than 5 from:
#         D. Yates, D. Moore, G. McCabe, The practice of Statistics 
#         (Freeman, New York, 1999), p. 734.
#     """
#     #region ---------------------------------------------------> Remove 0 rows
#     dfT = df[df.any(axis=1)]
#     #endregion ------------------------------------------------> Remove 0 rows
    
#     #region ---------------------------------------------------> Check < 5
#     if check5:
#         a,b = dfT.shape
#         n = np.count_nonzero(dfT < 5)
#         if n/(a*b) < 0.2:
#             pass
#         else:
#             return [-1,[]]
#     else:
#         pass
#     #endregion ------------------------------------------------> Check < 5

#     #region ---------------------------------------------------> Calculate
#     try:
#         chi = sStats.chi2_contingency(dfT)
#     except Exception:
#         return [-1,[]]
#     #endregion ------------------------------------------------> Calculate

#     return [1,chi] if chi[1] < alpha else [0, chi]
# #---


def Test_t_getP(
    t: 'pd.DataFrame',
    tdf: Union['pd.DataFrame', int],
    test: Literal['ts', 's', 'l'],
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
    #region -----------------------------------------------------> Get P value
    if test == 'ts':
        return 2 * sStats.t.sf(np.abs(t), tdf)
    elif test == 's':
        return sStats.t.cdf(t, tdf) # type: ignore
    elif test == 'l':
        return sStats.t.sf(t, tdf) # type: ignore
    else:
        msg = mConfig.mNotImplemented.format(test)
        raise mException.ExecutionError(msg)
    #endregion --------------------------------------------------> Get P value
#---


def Test_t_PS_DF(
    df: 'pd.DataFrame',
    col1: list[int],
    col2: list[int],
    value: float=0,
    alpha: float=0.05,
    roundTo: Optional[int]=None,
    tType: Literal['ts','l','s']='ts',
    delta: float = 0,
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
    #region ----------------------------------------------------------> Values
    ndf = pd.DataFrame(
        df.iloc[:,col2].values - df.iloc[:,col1].values,
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
        np.nan, columns=['t', 'P', 'S'], index=range(df.shape[0]) # type: ignore
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
    df: 'pd.DataFrame',
    col1: list[int],
    col2: list[int], 
    alpha:float=0.05,
    f:Literal[None, True, False]=None,
    roundTo: Optional[int]=None,
    tType: Literal['ts', 'l', 's']='ts',
    delta: float=0,
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
    #region ----------------------------------------------------------> Values
    #------------------------------> m, s, n
    m1 = df.iloc[:,col1].mean(axis=1, skipna=True)
    m2 = df.iloc[:,col2].mean(axis=1, skipna=True)
    var1 = df.iloc[:,col1].var(axis=1, skipna=True)
    var2 = df.iloc[:,col2].var(axis=1, skipna=True)
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
        (m2 - m1 - delta)/(np.sqrt((var1/n1)+(var2/n2))),
        (m2 - m1 - delta)/(np.sqrt((1/n1)+(1/n2))*np.sqrt(((n1-1)*var1+(n2-1)*var2)/(dem))),
    )
    tdf = np.where(
        F['S'],
        np.square((var1/n1)+(var2/n2))/(((var1*var1)/(n1*n1*(n1-1)))+((var2*var2)/(n2*n2*(n2-1)))),
        dfN,
    )
    #endregion -------------------------------------------------------> Values
    
    #region ----------------------------------------------------------> DF Out
    #------------------------------> 
    dfO = pd.DataFrame(
        np.nan, columns=['t', 'P', 'S'], index=range(df.shape[0]), # type: ignore
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
    df: 'pd.DataFrame',
    col1: list[int],
    col2: list[int],
    sample: Literal['p', 'i'],
    f:Literal[None, True, False]=None,
    delta: Optional['pd.DataFrame']=None,
    alpha: float=0.05,
    beta: float=0.05,
    gamma: float=0.80,
    d: float=0,
    deltaMax: Optional[float]=None,
    ) -> 'pd.DataFrame':
    """

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
            Performed an F test or not
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
    #region --------------------------------------------------------> Empty df
    dfo = pd.DataFrame(
        np.nan, # type: ignore
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
            df, col1, col2, delta=-tDelta, alpha=alpha, tType='l').to_numpy() # type: ignore
        dfo.loc[:,['t2', 'p2', 's2']] = Test_t_PS_DF(
            df, col1, col2, delta=tDelta, alpha=alpha, tType='s').to_numpy() # type: ignore
    else:
        dfo.loc[:,['t1', 'p1', 's1']] = Test_t_IS_DF(
            df, col1, col2, delta=-tDelta, alpha=alpha, f=f, tType='l' # type: ignore
        ).to_numpy()
        dfo.loc[:,['t2', 'p2', 's2']] = Test_t_IS_DF(
            df, col1, col2, delta=tDelta, alpha=alpha, f=f, tType='s' # type: ignore
        ).to_numpy()
    #endregion -------------------------------------------------------> T test

    #region ---------------------------------------------------------------> P
    dfo['P'] = np.where(dfo['p1'] > dfo['p2'], dfo['p1'], dfo['p2'])
    #endregion ------------------------------------------------------------> P

    return dfo
#---


def Test_tost_delta(
    df: Union['pd.DataFrame', 'pd.Series'],
    alpha: float,
    beta: float,
    gamma: float,
    d: float=0, 
    deltaMax: Optional[float]=None,
    ) -> pd.Series:
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
    #region -------------------------------------------------------> Variables
    s = df.std(axis=1)
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


# def test_slope(df: 'pd.DataFrame', nL: Optional[list[int]]=None) -> list[float]:
#     """Perform a Test for Homogeneity of Regression.

#         Parameters
#         ----------
#         df: pd.DataFrame
#             DataFrame with the x,y values for each regression line e.g.
#             X1 Y1 X2 Y2 Xn Yn
#         nL: list of int or None
#             Columns in df will be grouped with the size of each group given by
#             the elements in n and the total number of groups being equal to the
#             number of elements in n. If None only one group is created.
        
#         Returns
#         -------
#         list[float]
#             One P value for each group. See n in Parameters.

#         Raise
#         -----

#         Notes
#         -----
#         The procedure used here is described in:
#         http://vassarstats.net/textbook/index.html Chapter 17.
        
#         If df has columns X1,Y1,X2,Y2,X3,Y3,X4,Y4,X5,Y5 and n is [3,2]
#         then two P values will be returned one for test performed with 
#         X1,Y1,X2,Y2,X3,Y3 and one for X4,Y4,X5,Y5.
        
#         X,Y pairs in a group can be of different length but X and Y must have 
#         the same number of elements.
#     """
#     #region -------------------------------------------------------> Variables
#     p = []
    
#     if nL is None:
#         nL = [1]
#     else:
#         pass
#     #endregion ----------------------------------------------------> Variables

#     #region --------------------------------------------------------> Run
#     #------------------------------> Number of points in each column N
#     n = df.notna().sum() 
#     #------------------------------> SUM(X)
#     sumCol = df.sum(axis=0)
#     #------------------------------> SUM(X^2)
#     sumCol2 = (df.pow(2)).sum(axis=0)
#     #------------------------------> SUM(XY)
#     sumXY = pd.DataFrame(index=df.index)
#     for k in range(0, df.shape[1], 2):
#         sumXY[k] = df.iloc[:,k] * df.iloc[:,k+1]
#     sumXY = sumXY.sum(axis=0)
#     #------------------------------> SUM(X) - (SUM(X)^2)/N
#     ss = sumCol2 - sumCol.pow(2)/n
#     #------------------------------> SUM(XY) - SUM(X)SUM(Y)/N
#     sc = pd.Series(index=sumXY.index)
#     for k in range(0, df.shape[1], 2):
#         sc[k] = sumXY[k] - ((sumCol[k]*sumCol[k+1])/n.iloc[k])
#     #------------------------------> 
#     k = 0
#     j = 0
#     for nG in nL:
#         try:
#             #------------------------------> SUM(SC) for Group
#             scwg = sc.iloc[j:j+nG].sum()
#             #------------------------------> SUM(SS) for Group
#             sswgx = ss.iloc[range(k,k+2*nG,2)].sum()
#             sswgy = ss.iloc[range(k+1,k+2*nG,2)].sum()
#             #------------------------------> SUM(SC^2/SS) - SCwg^2/SSwg
#             a = sc.iloc[j:j+nG].pow(2)
#             b = ss.iloc[range(k,k+2*nG,2)].set_axis(a.index.values)
#             ssb_reg = (a/b).sum() - ((scwg*scwg)/sswgx)
#             #------------------------------> 
#             ssy_rem = sswgy - ((scwg*scwg)/sswgx) - ssb_reg
#             #------------------------------> 
#             dfb_reg = nG-1
#             dfy_rem = n.iloc[range(k,k+2*nG,2)].sum() - 2*nG
#             #------------------------------> F value
#             f = (ssb_reg/dfb_reg)/(ssy_rem/dfy_rem)
#             #------------------------------> P value
#             p.append(sStats.f.sf(f, dfb_reg, dfy_rem))
#         except Exception as e:
#             p.append(np.nan)
#         #------------------------------> Next Group
#         k = k + 2*nG
#         j = j + nG
#     #endregion -----------------------------------------------------> Run

#     return p
# #---
#endregion -------------------------------------------------------------> TEST

