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
    val: str, sep: list[str]=[' ', ',', ';'], numType: str='int',
    ) -> list[list[list[int]]]:
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

def ResControl2DF(
    val: list[list[list[int]]], start: int
    ) -> list[list[list[int]]]:
    """Convert the Result - Control column numbers in the original file to the
        column numbers of the initial dataframe used in the analysis. 

        Parameters
        ----------
        val : list of list of list of int
            Result - Control as a list of list of list of int
        start : int
            Column index start of the Result - Control columns in the initial
            dataframe 

        Returns
        -------
        list[list[list[int]]]
            The list has the same order as the input val but the column index
            are adjusted
    """
    # Test in test.unit.test_method.Test_ResControl2DF
    #region -------------------------------------------------------> Variables
    idx  = start
    outL = []
    #endregion ----------------------------------------------------> Variables
    
    #region --------------------------------------------------> Adjust col idx
    for row in val:
        #------------------------------> 
        outR = []
        #------------------------------> 
        for col in row:
            #------------------------------> 
            outC = []
            #------------------------------> 
            if len(col) > 0:
                pass
            else:
                outR.append([])
                continue
            #------------------------------> 
            for k in col:
                outC.append(idx)
                idx += 1
            #------------------------------> 
            outR.append(outC)
        #------------------------------> 
        outL.append(outR)    
    #endregion -----------------------------------------------> Adjust col idx
    
    return outL
#---
#endregion ----------------------------------------------------------> Methods
