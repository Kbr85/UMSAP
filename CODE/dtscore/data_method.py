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


"""General classes and methods for data manipulation"""


#region -------------------------------------------------------------> Imports
from typing import Literal

import pandas as pd

import config.config as config
import dtscore.exception as dtsException
#endregion ----------------------------------------------------------> Imports


#region -----------------------------------------------------------> Pandas DF
def DFFilterByColS(
    df:'pd.DataFrame', col: int, refStr: str,
    comp: Literal['e', 'ne'],
    ) -> 'pd.DataFrame':
    """Filter rows in the pd.DataFrame based on the string values present in 
        col.
    
        See Notes for more details.

        Parameters
        ----------
        df: pd.DataFrame
        col : int
            The column index used to filter rows
        refStr : string
            Reference string
        comp : str
            Numeric comparison to use in the filter. One of:
            'e', 'ne

        Returns
        -------
        pd.DataFrame

        Raise
        -----
        InputError :
            - When col is not an integer
            - When col is not found in df
            - When comp is not one of the valid options
        NotYetImplement : 
            - When comp is in config.oStrComp but the option has not being 
            implemented here
            
        Notes
        -----
        Rows with values in col that do not comply with c[x] comp refStr are 
        discarded, e.g. c[x] == 'refString'
        
        Assumes all values in col are strings
    """
    # Test in tests.unit.data.test_method.Test_DFFilterByColS
    #region ----------------------------------------------------------> Filter
    #------------------------------>  Copy
    dfo = df.copy()
    #------------------------------> Filter
    try:
        if comp == 'e':
            dfo = df.loc[df.iloc[:,col] == refStr]
        elif comp == 'ne':
            dfo = df.loc[df.iloc[:,col] != refStr]
        else:
            msg = config.mCompNYI.format(comp)
            raise dtsException.NotYetImplementedError(msg)
    except Exception:
        raise dtsException.ExecutionError(config.mPDFilterByCol)
    #endregion -------------------------------------------------------> Filter
    
    return dfo
#---
#endregion --------------------------------------------------------> Pandas DF
