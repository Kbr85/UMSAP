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


"""Classes and methods to check data """


#region -------------------------------------------------------------> Imports
from typing import Optional, Literal

import dat4s_core.data.method as dtsMethod
import dat4s_core.data.check as dtsCheck

import config.config as config

if config.typeCheck:
    import wx
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Methods
def UniqueColNumbers(
    tcList: list['wx.TextCtrl'], resCtrl: 'wx.TextCtrl', 
    numType: Literal['int', 'float']='int', sepList: str=' ', 
    sepRes: list[str]=[',', ';']
    ) -> tuple[bool, Optional[tuple[str, Optional[str], str]]]:
    """Checks elements in the wx.TextCtrl are unique

        Parameters
        ----------
        tcList : list of wx.TextCtrl
            List of wx.TextCtrl. Elements in each one are separated by sep
        resCtrl: wx.TextCtrl  
            wx.TextCtrl with the result - control values. Elements here are 
            separated by sepList. e.g. '1 2 3', '4-10'; ....
        numType : str
            One of 'int', 'float'
        sepList: str
            Separator used in tcList and inner values of resCtrl
        sepRes : list of str
            Element and row separator in resCtrl 

        Returns
        -------
        tupple:
            (True, None)
            (False, (NotUnique, repeated elements, msg))
    """
    # No Test
    #region -------------------------------------------------------> Variables
    values = tcList[0].GetValue()
    #endregion ----------------------------------------------------> Variables
    
    #region ------------------------------------------------------> Get values
    #------------------------------> Values from list
    for k in tcList[1:]:
        values = f"{values}{sepList} {k.GetValue()}"
    #------------------------------> Values from res-ctrl
    for k in resCtrl.GetValue().split(sepRes[1]):
        for j in k.split(sepRes[0]):
            values = f"{values}{sepList} {j}"
    #------------------------------> Values
    try:
        values = dtsMethod.Str2ListNumber(values, numType=numType, sep=sepList)
    except Exception as e:
        raise e
    #endregion ---------------------------------------------------> Get values

    #region ----------------------------------------------------> Check unique
    return dtsCheck.ListUnique(values)
    #endregion -------------------------------------------------> Check unique
#---
#endregion ----------------------------------------------------------> Methods
