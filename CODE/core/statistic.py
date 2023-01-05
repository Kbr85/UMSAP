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


"""Statistic methods for the app"""


#region -------------------------------------------------------------> Imports
from typing import Literal, Optional, Union

import numpy  as np
import pandas as pd
from scipy import stats
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Methods
def CI_Sample(
    df:pd.DataFrame,
    alpha:float,
    fullCI:bool       = False,
    axis:Literal[0,1] = 1,
    ) -> pd.DataFrame:
    """Calculate the confidence interval for a sample.

        Parameters
        ----------
        df: pd.DataFrame
            Dataframe with the data
        alpha: float
            Significance level. CI will be calculated for 1-alpha.
        fullCI: bool
            Full confidence interval (True) or not (False). Default is False.
        axis: int
            Calculate for row (1) in df or columns (0)
    """
    #region --------------------------------------------------->
    res = stats.t.interval(
        1-alpha,
        df.count(axis=axis)-1,                                                  # Exclude NA values
        loc   = df.mean(axis=axis, skipna=True),
        scale = df.std(axis=axis,  skipna=True),
    )
    #------------------------------>
    if fullCI:
        dfOut = pd.DataFrame({
            'LL' : res[0],
            'UL' : res[1],
        })
    else:
        dfOut = pd.DataFrame({
            'CI' : (res[1] - res[0])/2,
        })
    #endregion ------------------------------------------------>

    return dfOut
#---

def CI_Mean_Diff(
    dfA:pd.DataFrame,
    dfB:pd.DataFrame,
    alpha:float,
    axis:Literal[0,1]    = 1,
    fullCI:bool          = False,
    roundN:Optional[int] = None,
    ) -> 'pd.DataFrame':
    """Calculate the confidence interval for the difference between means when
        samples are independent.

        Parameters
        ----------
        dfA: pd.DataFrame
            DataFrame with sample A.
        dfB: pd.DataFrame
            DataFrame with sample B.
        alpha: float
            Significance level
        axis: int
            Axis to calculate on. 1 row based calculation, 0 column based.
        fullCI: bool
            Return full interval (True) or just (False) the CI value. Default is
            to return full interval.
        roundN: int or None
            Round numbers to the given number of decimal places.
            Default is None.

        Returns
        -------
        pd.Dataframe
            With two columns CI_l and CI_u if fullCI is True else one column CI.

        Notes
        -----
        Assumes samples does not have equal variance
        - Further details:
            https://calcworkshop.com/confidence-interval/difference-in-means/
    """
    # Test in test.unit.test_statistic.Test_CI_Mean_Diff_DF
    #region ----------------------------------------------------------> Values
    var1 = dfA.var(axis=axis, skipna=True)                                      # type: ignore
    var2 = dfB.var(axis=axis, skipna=True)                                      # type: ignore
    n1   = dfA.count(axis=axis)
    n2   = dfB.count(axis=axis)
    dfT  = n1 + n2 - 2
    #------------------------------>
    q = 1-(alpha/2)
    t = stats.t.ppf(q, dfT)
    #------------------------------>
    ci = t*np.sqrt((1/n1)+(1/n2))*np.sqrt(((n1-1)*var1+(n2-1)*var2)/dfT)        # type: ignore
    #endregion -------------------------------------------------------> Values

    #region --------------------------------------------------------> Empty DF
    if fullCI:
        diffMean21 = (
            dfA.mean(axis=axis, skipna=True)                                    # type: ignore
           -dfB.mean(axis=axis, skipna=True)                                    # type: ignore
        )
        #------------------------------>
        dfO = pd.DataFrame(
            np.nan, columns=['CI_l', 'CI_u'], index=range(dfA.shape[0])          # type: ignore
        )
        #------------------------------>
        dfO['CI_l'] = diffMean21 - ci
        dfO['CI_u'] = diffMean21 + ci
    else:
        #------------------------------>
        dfO = pd.DataFrame(np.nan, columns=['CI'], index=range(dfA.shape[0]))    # type: ignore
        #------------------------------>
        dfO['CI'] = ci
    #endregion -----------------------------------------------------> Empty DF

    #region -----------------------------------------------------------> Round
    if roundN is not None:
        dfO = dfO.round(int(roundN))
    #endregion --------------------------------------------------------> Round

    return dfO
#---


def Tost_delta(
    df:Union[pd.DataFrame, pd.Series],
    alpha:float,
    beta:float,
    gamma:float,
    d:float                  = 0,
    deltaMax:Optional[float] = None,
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
    chi2 = stats.chi2.ppf(1-gamma, (n-1))
    #------------------------------>
    sCorr = s * np.sqrt((n-1)/chi2)
    #------------------------------>
    ta1 = stats.t.ppf(1 - alpha, 2*n - 2)
    tb1 = stats.t.ppf(1 - beta/2, 2*n -2)
    #------------------------------>
    delta = d + sCorr * (ta1 + tb1) * np.sqrt(2/n)
    #endregion ----------------------------------------------------> Variables

    #region --------------------------------------------------> Check deltaMax
    if deltaMax is not None:
        delta = np.where(delta > deltaMax, deltaMax, delta)
    #endregion -----------------------------------------------> Check deltaMax

    return delta
#---
#endregion ----------------------------------------------------------> Methods
