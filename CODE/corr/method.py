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


"""Methods for the corr module of the app"""


#region -------------------------------------------------------------> Imports
from dataclasses import dataclass, field
from typing      import Optional

import pandas as pd

from core     import method as cMethod
from dataprep import method as dataMethod
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Classes
@dataclass
class UserData(cMethod.BaseUserData):
    """Representation of the input data for the Correlation Analysis Pane."""
    #region ---------------------------------------------------------> Options
    dO:list = field(default_factory=lambda:                                     # Attr printed to UMSAP file
        ['iFileN', 'ID', 'cero', 'tran', 'norm', 'imp', 'shift', 'width',
         'corr', 'labelA', 'ocColumn', 'resCtrl', 'ocResCtrl', 'ocResCtrlFlat',
         'minRep', 'minRepList', 'dfResCtrl',
        ])
    longestKey:int = 18                                                         # Length of the longest Key in dI
    #endregion ------------------------------------------------------> Options
#---

@dataclass
class CorrAnalysis():
    """Data class to hold the info regarding a CorrA in an UMSAP file."""
    #region --------------------------------------------------------> Options
    df:pd.DataFrame                                                             # Results as dataframe
    numCol:int                                                                  # Total number of columns
    numColList:list[int]                                                        # Column numbers
    #endregion -----------------------------------------------------> Options
#---
#endregion ----------------------------------------------------------> Classes


#region -------------------------------------------------------------> Methods
def CorrA(                                                                      # pylint: disable=dangerous-default-value
    *args,                                                                      # pylint: disable=unused-argument
    df:pd.DataFrame = pd.DataFrame(),
    rDO:UserData    = UserData(),
    resetIndex:bool = True,
    **kwargs,
    ) -> tuple[dict, str, Optional[Exception]]:
    """Perform a Correlation Analysis.

        Parameters
        ----------
        *args: These are ignores here.
        df: pd.DataFrame
            DataFrame read from CSV file.
        rDO: dict
            rDO dictionary from the PrepareRun step of the analysis.
        resetIndex: bool
            Reset index of dfS (True) or not (False). Default is True.
        **kwargs: These are ignore here.

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
        *args are ignored. They are needed for compatibility.
        *kwargs are ignored. They are needed for compatibility.
    """
    # Test in test.unit.corr.test_method.Test_CorrA
    #region ------------------------------------------------> Data Preparation
    tOut = dataMethod.RunDataPreparation(df=df, rDO=rDO, resetIndex=resetIndex)
    if not tOut[0]:
        return tOut
    #endregion ---------------------------------------------> Data Preparation

    #region -----------------------------------------------------------> CorrA
    try:
        dfR = tOut[0]['dfIm'].corr(method=rDO.corr.lower())
    except Exception as e:
        return ({}, 'Correlation coefficients calculation failed.', e)
    #------------------------------>
    tOut[0]['dfR'] = dfR
    #endregion --------------------------------------------------------> CorrA

    return (tOut[0], '', None)
#---
#endregion ----------------------------------------------------------> Methods
