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


#region ----------------------------------------------------> Data Description
def DataRange(
    x:Union[pd.DataFrame, pd.Series, np.ndarray, list, tuple],
    margin:float = 0,
    symm:bool    = False
    ) -> list[float]:
    """Return the range of x with an optional margin applied.
        Useful to set the axes limit in a matplotlib plot.

        Parameters
        ----------
        x: pd.DataFrame, pd.Series, np.array, list or tuple of numbers.
            Data with only numbers.
        margin: float
            Expand the range by (max(x) - min(x)) * margin. Default is 0,
            meaning that no expansion of the max(x) and min(x) is done.
        symm: bool
            Make output symmetric around 0.

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
    # Test in test.unit.core.test_statistic.Test_DataRange
    #region --------------------------------------------------> Helper Methods
    def _list_tuple() -> tuple[float, float]:
        """Find the minimum and maximum value in a list or tuple.

            Returns
            -------
            tuple[min, max]
        """
        nL = list(map(float, x))
        return (min(nL), max(nL))
    #---

    def _pd_series() -> tuple[float, float]:
        """Find the minimum and maximum value in a pd.Series.

            Returns
            -------
            tuple[min, max]
        """
        s = pd.to_numeric(x, errors='coerce')                                   # type: ignore
        return (s.min(), s.max())
    #---

    def _pd_df() -> tuple[float, float]:
        """Find the minimum and maximum value in a pd.DataFrame.

            Returns
            -------
            tuple[min, max]
        """
        df = x.apply(pd.to_numeric, errors='coerce')                            # type: ignore
        return (df.min().min(), df.max().max())
    #---

    def _np_ndarray() -> tuple[float, float]:
        """Find the minimum and maximum value in a np.ndarray.

            Returns
            -------
            tuple[min, max]
        """
        npA:np.ndarray = x.astype(np.float64)                                   # type: ignore
        return (np.amin(npA), np.amax(npA))
    #---
    #endregion -----------------------------------------------> Helper Methods

    #region -------------------------------------------------------> Variables
    dictM = {
        list        : _list_tuple,
        tuple       : _list_tuple,
        pd.Series   : _pd_series,
        pd.DataFrame: _pd_df,
        np.ndarray  : _np_ndarray,
    }
    #endregion ----------------------------------------------------> Variables

    #region -----------------------------------------------------> Check Input
    tType = type(x)
    #------------------------------>
    tMin, tMax = dictM[tType]()
    #------------------------------>
    if symm:
        tMin = abs(tMin)
        tMax = abs(tMax)
        #------------------------------>
        if tMin >= tMax:
            tMin = -tMin
            tMax = tMin
        else:
            tMin = -tMax
    #------------------------------>
    dm = (tMax - tMin) * margin
    #endregion --------------------------------------------------> Check Input

    return [tMin - dm, tMax + dm]
#---

def HistBin(x: pd.Series) -> tuple[float, float]:
    """Calculate the bin width for a histogram according to the
        Freedman – Diaconis rule.

        Parameters
        ----------
        x: pd.Series
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


#region -------------------------------------------------------------> Methods
def CI_Sample(
    df:pd.DataFrame,
    alpha:float,
    axis:Literal[0,1]    = 1,
    roundN:Optional[int] = None,
    ) -> pd.DataFrame:
    """Calculate the confidence interval for a sample.

        Parameters
        ----------
        df: pd.DataFrame
            Dataframe with the data
        alpha: float
            Significance level. CI will be calculated for 1-alpha.
        axis: int
            Axis for the calculation, 0 for each column 1 for each row.
            Default is 1.
        roundN: int
            Round results to the given number of decimal.

        Return
        ------
        pd.DataFrame
            Columns in the dataframe are 'CI', 'LL', 'LU'

        Notes
        -----
        http://www.biostathandbook.com/confidence.html
        https://www.statskingdom.com/confidence-interval-calculator.html
    """
    # Test in test.unit.core.test_statistic.Test_CI_Sample
    #region --------------------------------------------------->
    res = stats.t.interval(
        1-alpha,
        df.count(axis=axis)-1,                                                  # Exclude NA values
        loc   = df.mean(axis=axis, skipna=True),
        scale = df.sem(axis=axis,  skipna=True),
    )
    #------------------------------>
    dfOut = pd.DataFrame({
        'CI' : (res[1] - res[0])/2,
        'LL' : res[0],
        'UL' : res[1],
    })
    #endregion ------------------------------------------------>

    #region -----------------------------------------------------------> Round
    if roundN is not None:
        dfOut = dfOut.round(int(roundN))
    #endregion --------------------------------------------------------> Round

    return dfOut
#---


def CI_Mean_Diff(
    dfA:pd.DataFrame,
    dfB:pd.DataFrame,
    alpha:float,
    equal_var:bool       = True,
    axis:Literal[0,1]    = 1,
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
        equal_var: bool
            Assume equal variance (True) or not (False). Default is False.
        axis: int
            Axis for the calculation, 0 for each column 1 for each row.
            Default is 0.
        roundN: int or None
            Round numbers to the given number of decimal places.
            Default is None.

        Returns
        -------
        pd.Dataframe
            Columns in the dataframe are 'CI', 'LL', 'LU'

        Notes
        -----
        - Further details:
            https://www.statskingdom.com/difference-confidence-interval-calculator.html
    """
    # Test in test.unit.core.test_statistic.Test_CI_Mean_Diff_DF
    #region ----------------------------------------------------------> Values
    if not axis:
        dfB.set_axis(dfA.columns.values.tolist(), axis=1, inplace=True)         # type: ignore
    #------------------------------>
    var1 = dfA.var(axis=axis, skipna=True)                                      # type: ignore
    var2 = dfB.var(axis=axis, skipna=True)                                      # type: ignore
    n1   = dfA.count(axis=axis)                                                 # Remove NA values
    n2   = dfB.count(axis=axis)                                                 # Remove NA values
    #------------------------------> SEM & df
    if equal_var:
        dfT = n1 + n2 - 2
        sem = np.sqrt((1/n1)+(1/n2))*np.sqrt(((n1-1)*var1+(n2-1)*var2)/dfT)
    else:
        dfT = ((var1/n1)+(var2/n2))**2/((var1**2/((n1-1)*n1**2))+(var2**2/((n2-1)*n2**2)))
        sem = np.sqrt((var1/n1)+(var2/n2))
    #------------------------------>
    q = 1-(alpha/2)
    t = stats.t.ppf(q, dfT)
    #------------------------------>
    ci = t*sem        # type: ignore
    #endregion -------------------------------------------------------> Values

    #region --------------------------------------------------------------> DF
    diffMean21 = (
        dfA.mean(axis=axis, skipna=True)                                    # type: ignore
       -dfB.mean(axis=axis, skipna=True)                                    # type: ignore
    )
    #------------------------------>
    dfO = pd.DataFrame({
        'CI' : ci,
        'LL' : diffMean21 - ci,
        'UL' : diffMean21 + ci,
    })
    dfO.reset_index(drop=True, inplace=True)
    #endregion -----------------------------------------------------------> DF

    #region -----------------------------------------------------------> Round
    if roundN is not None:
        dfO = dfO.round(int(roundN))
    #endregion --------------------------------------------------------> Round

    return dfO
#---


def Tost_delta(
    df:pd.DataFrame,
    alpha:float,
    beta:float,
    gamma:float,
    axis:int                 = 1,
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
        axis: int
            Axis for the calculation, 0 for each column 1 for each row.
            Default is 1.
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
    # Test in test.unit.core.test_statistic.Test_tost_delta
    #region -------------------------------------------------------> Variables
    s    = df.std(axis=axis)                                                    # type: ignore
    n    = df.count(axis=axis)                                                  # type: ignore
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
        delta = pd.Series(np.where(delta > deltaMax, deltaMax, delta))
    #endregion -----------------------------------------------> Check deltaMax

    return delta
#---


def Test_chi(df:pd.DataFrame, alpha:float, check5:bool=True) -> list:
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
        - Threshold of number of cells with values less than 5 from:
        D. Yates, D. Moore, G. McCabe, The practice of Statistics
        (Freeman, New York, 1999), p. 734.
        - https://www.statskingdom.com/doc_chi_squared.html
    """
    # Test in test.unit.core.test_statistic.Test_chi
    #region ---------------------------------------------------> Remove 0 rows
    dfT = df[df.any(axis=1)]
    #endregion ------------------------------------------------> Remove 0 rows

    #region ---------------------------------------------------> Check < 5
    if check5:
        a,b = dfT.shape
        n = np.count_nonzero(dfT < 5)
        if not n/(a*b) < 0.2:
            return [-1,[]]
    #endregion ------------------------------------------------> Check < 5

    #region ---------------------------------------------------> Calculate
    try:
        chi = stats.chi2_contingency(dfT)
    except Exception:
        return [-1,[]]
    #endregion ------------------------------------------------> Calculate

    return [1,chi] if chi[1] < alpha else [0, chi]
#---


def Test_slope(df:pd.DataFrame, nL:list[int]=[]) -> list[float]:                # pylint: disable=dangerous-default-value
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
    # Test in test.unit.core.test_statistic.Test_test_slope
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
            sswgx = ss.iloc[range(k,k+2*nG,2)].sum()                            # type: ignore
            sswgy = ss.iloc[range(k+1,k+2*nG,2)].sum()                          # type: ignore
            #------------------------------> SUM(SC^2/SS) - SCwg^2/SSwg
            a = sc.iloc[j:j+nG].pow(2)
            b = ss.iloc[range(k,k+2*nG,2)].set_axis(a.index.values)             # type: ignore
            ssb_reg = (a/b).sum() - ((scwg*scwg)/sswgx)
            #------------------------------>
            ssy_rem = sswgy - ((scwg*scwg)/sswgx) - ssb_reg
            #------------------------------>
            dfb_reg = nG-1
            dfy_rem = n.iloc[range(k,k+2*nG,2)].sum() - 2*nG                    # type: ignore
            #------------------------------> F value
            f = (ssb_reg/dfb_reg)/(ssy_rem/dfy_rem)
            #------------------------------> P value
            p.append(stats.f.sf(f, dfb_reg, dfy_rem))
        except Exception:
            p.append(np.nan)
        #------------------------------> Next Group
        k = k + 2*nG
        j = j + nG
    #endregion -----------------------------------------------------> Run

    return p
#---
#endregion ----------------------------------------------------------> Methods
