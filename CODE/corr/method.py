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
from typing import Optional

import pandas as pd

from dataprep import method as dataMethod
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Methods
def CorrA(                                                                      # pylint: disable=dangerous-default-value
    *args,                                                                      # pylint: disable=unused-argument
    df:pd.DataFrame = pd.DataFrame(),
    rDO:dict        = {},
    resetIndex:bool = True,
    **kwargs,
    ) -> tuple[dict, str, Optional[Exception]]:
    """Perform a Correlation Analysis.

        Parameters
        ----------
        *args : These are ignores here.
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
    # Test in test.unit.test_method.Test_CorrA
    #region ------------------------------------------------> Data Preparation
    tOut = dataMethod.DataPreparation(df, rDO, resetIndex=resetIndex)
    if not tOut[0]:
        return tOut
    #endregion ---------------------------------------------> Data Preparation

    #region -----------------------------------------------------------> CorrA
    try:
        dfR = tOut[0]['dfIm'].corr(method=rDO['CorrMethod'].lower())
    except Exception as e:
        return ({}, 'Correlation coefficients calculation failed.', e)
    else:
        dictO = tOut[0]
        dictO['dfR'] = dfR
        return (dictO, '', None)
    #endregion --------------------------------------------------------> CorrA
#---
#endregion ----------------------------------------------------------> Methods
