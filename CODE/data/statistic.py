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
#endregion -------------------------------------------------------------> TEST
