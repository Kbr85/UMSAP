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
import copy
import traceback
from datetime import datetime
from operator import itemgetter
from pathlib import Path
from typing import Literal, Union, Optional, Any

import pandas as pd
import matplotlib as mpl
import numpy as np
import wx

import config.config as config
import dtscore.exception as dtsException
import dtscore.file as dtsFF
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Numbers
def MergeOverlapingFragments(
    coord:list[tuple[int, int]], delta:int=0) -> list[tuple[int, int]]:
    """Merge overlapping fragments in a list of fragments coordinates

        Parameters
        ----------
        coord: list[tuple[int, int]]
            Fragment coordinates lists
        delta: int
            To adjust the merging of adjacent fragments.  

        Returns
        -------
        list[tuple[int, int]]

        Notes
        -----
        An empty list is returned if coord is empty
    """
    #region ---------------------------------------------------> Variables
    coordO = []
    #endregion ------------------------------------------------> Variables

    #region ------------------------------------------------------> Sort & Dup
    coordS = sorted(list(set(coord)), key=itemgetter(0,1))
    #endregion ---------------------------------------------------> Sort & Dup

    #region -------------------------------------> Merge Overlapping Intervals
    try:
        a,b = coordS[0]
    except IndexError:
        return []
    for ac,bc in coordS[1:]:
        if ac <= b+delta:
            if bc > b:
                b = bc
            else:
                pass
        else:
            coordO.append((a,b))
            a = ac
            b = bc
    #------------------------------> Catch the last one        
    coordO.append((a,b))
    #endregion ----------------------------------> Merge Overlapping Intervals

    return coordO
#---
#endregion ----------------------------------------------------------> Numbers


#region -------------------------------------------------------------> Strings
def StrEqualLength(strL: list[str], char: str=' ', loc:str='end') -> list[str]:
    """Return a list in which every string element has the same length

        Parameters
        ----------
        strL: list[str]
            String with different length
        char: str
            Fill character. Default is empty space.
        loc: str
            Add filling character to start or end of the strings

        Returns
        -------
        list[str]
            String with the same length with the same origina order

        Raise
        -----
        
        Notes
        -----
        Filling characters are added at the end or start of each str.
    """
    #region ---------------------------------------------------> Variables
    long = len(max(strL, key=len))
    lOut = []
    #endregion ------------------------------------------------> Variables
    
    #region ---------------------------------------------------> Fill lOut
    if loc == 'end':
        for x in strL:
            space = (long-len(x))*char
            lOut.append(f'{x}{space}')
    elif loc == 'start':
        for x in strL:
            space = (long-len(x))*char
            lOut.append(f'{space}{x}')
    else:
        msg = config.mNotImplementedFull.format(
            loc, 'loc', config.oFillLoc)
        raise dtsException.ExecutionError(msg)
    #endregion ------------------------------------------------> Fill lOut

    return lOut
#---
#endregion ----------------------------------------------------------> Strings