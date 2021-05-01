# ------------------------------------------------------------------------------
# Copyright (C) 2017 Kenny Bravo Rodriguez <www.umsap.nl>
#
# Author: Kenny Bravo Rodriguez (kenny.bravorodriguez@mpi-dortmund.mpg.de)
#
# This program is distributed for free in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See the accompaning licence for more details.
# ------------------------------------------------------------------------------


"""Classes and methods to manipulate data """


#region -------------------------------------------------------------> Imports
import itertools
from typing import Literal, Union

import dat4s_core.data.method as dtsMethod
#endregion ----------------------------------------------------------> Imports

#region -------------------------------------------------------------> Methods
def ResControl2ListNumber(
    val: str, sep: list[str]=[' ', ',', ';'], 
    numType: Literal['int', 'float']='int',
    ) -> list[list[list[Union[int, float]]]]:
    """Return a list 
        Parameters
        ----------
        val : str
            String with the numbers. e.g. '0-4 6', '7 8 9'; '10 13-15', ''; ...
        sep : list of str
            Separators used in the string
        numType: str
            To convert to numbers

        Returns
        -------
        list of list of list of str
        [[[0 1 2 3 4], [7 8 9]], [[10 13 14 15], []], ...]        
    """
    # Test in test.unit.test_method.Test_ResControl2ListNumber
    #region -------------------------------------------------------> Variables
    l = []    
    #endregion ----------------------------------------------------> Variables
    
    #region -------------------------------------------------------> Form list
    for k in val.split(sep[2]):
        #------------------------------> 
        lrow = []
        #------------------------------> 
        for j in k.split(sep[1]):
            colVal = dtsMethod.Str2ListNumber(j, numType=numType, sep=sep[0])
            lrow.append(colVal)
        #------------------------------> 
        l.append(lrow)
    #endregion ----------------------------------------------------> Form list
    
    return l
#---

def ResControl2Flat(val: list[list[list[int]]]) -> list[int]:
    """Result - Control list as a flat list.

        Parameters
        ----------
        val : list of list of list of int
            Result - Control as a list of list of list of int

        Returns
        -------
        list of int
            Flat Result - Control list
    """
    # Test in test.unit.test_method.Test_ResControl2Flat
    return list(itertools.chain(*(itertools.chain(*val))))
#---
#endregion ----------------------------------------------------------> Methods
