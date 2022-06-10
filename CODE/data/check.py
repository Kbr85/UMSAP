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


"""Classes and methods to check data"""


#region -------------------------------------------------------------> Imports
from typing import Optional

import data.exception as mException
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Methods
def VersionCompare(
    strA: str, strB: str,
    )-> tuple[bool, Optional[tuple[str, Optional[str], str]]]:
    """Basic version comparison.

        Parameters
        ----------
        strA : str
            Expected format is '2.3.4' or '2.3.4 (beta)'.
        strB : str
            Same format as strA is expected.

        Returns
        -------
        tuple
            (True, None)
            (False, ('', '', ''))

        Raise
        -----
        InputError
            When strA or strB cannot be converted to x,y,z integers

        Examples
        --------
        >>> VersionCompare('2.4.7 beta', '2.4.7')
        >>> False
        >>> VersionCompare('2.4.7', '2.4.1')
        >>> True
        >>> VersionCompare('3.4.7 beta', '5.4.1')
        >>> False
    """
    #region -------------------------------------------------> Get number list
    try:
        xA, yA, zA = map(int, strA.strip().split(" ")[0].split("."))
        xB, yB, zB = map(int, strB.strip().split(" ")[0].split("."))
    except ValueError:
        msg = (
            f"The expected input for strA and strB is '2.4.5' or "
            f"'4.10.23 (beta)'."
        )
        raise mException.InputError(msg)
    #endregion ----------------------------------------------> Get number list

    #region ---------------------------------------------------------> Compare
    if xA > xB:
        return (True, None)
    elif xA < xB:
        return (False, ('', '', ''))
    else:
        if yA > yB:
            return (True, None)
        elif yA < yB:
            return (False, ('', '', ''))
        else:
            if zA > zB:
                return (True, None)
            else:
                return (False, ('', '', ''))
    #endregion ------------------------------------------------------> Compare
#---


# def UniqueColNumbers(
#     value: list[str], sepList: list[str]=[' ', ',', ';'],
#     ) -> tuple[bool, Optional[tuple[str, Optional[str], str]]]:
#     """Check value contains unique integers.

#         Parameters
#         ----------
#         value : list[str]
#             List of string with the values to check. The expected values are:
#             ['1 3 4 5-10', '11-13, 14 15; ...', ...]. Only integers are allowed.
#         sepList: list of str
#             Separator used in values.
#             sepList[0] : internal element separator
#             sepList[1] : intrarow separator
#             sepList[2] : interrow separator

#         Returns
#         -------
#         tupple:
#             (True, None)
#             (False, (NotUnique, repeated elements, msg))

#         Raise
#         -----
#         InputError:
#             - When value is not a list of strings
#             - When sepList is not a list with three strings.
#         See also dtsMethod.Str2ListNumber and dtsCheck.ListUnique.
        
#         Notes
#         -----
#         - Both value and sepList will be map to str
#         - Only integers and ranges (4-10) are expected in value.
        
#         Examples
#         --------
#         >>> UniqueColNumbers(['1 2 3', '3-5'], sepList=[' ', ',', ';'])
#         >>> (False, ('NotUnique', '3', 'Duplicated element: 3'))
#     """
#     # Test in test.unit.test_check.Test_UniqueColNumbers
#     def _strip_split(tEle: Union[str, list[str]], sep: str) -> list[str]:
#         """ """
#         #------------------------------> 
#         if isinstance(tEle, str):
#             k = [tEle.strip()]
#         else:
#             k = tEle
#         #------------------------------>
#         out = []
#         for v in k:
#             for j in v.split(sep):
#                 out.append(j)
#         #------------------------------> 
#         return [x.strip() for x in out]
#     #---
    
#     #region -----------------------------------------------------> Check input
#     #------------------------------> 
#     try:
#         if dtsCheck.ListContent(value, tType=str)[0]:
#             value = list(map(str, value))
#             pass
#         else:
#             msg = ('value must be a list of strings.')
#             raise dtsException.InputError(msg)
#     except Exception as e:
#         raise e
#     #------------------------------> 
#     try:
#         if dtsCheck.ListContent(sepList, nN=3, tType=str)[0]:
#             sepList = list(map(str, sepList))
#         else:
#             msg = (
#                 f'sepList "({sepList}" must be a list of three strings. '
#                 f'e.g. [" ", ",", ";"].')
#             raise dtsException.InputError(msg)
#     except Exception as e:
#         raise e
#     #endregion --------------------------------------------------> Check input
    
#     #region ----------------------------------------------------> Get Elements
#     #------------------------------> 
#     values = []
#     #------------------------------> 
#     for k in value:
#         #------------------------------> 
#         for sep in reversed(sepList):
#             k = _strip_split(k, sep)
#         #------------------------------> 
#         values = values + k
#     #------------------------------> 
#     values = sepList[0].join(values)
#     #endregion -------------------------------------------------> Get Elements
    
#     #region --------------------------------------------------> Check Elements
#     #------------------------------> 
#     try:
#         values = dtsMethod.Str2ListNumber(values, numType='int', sep=sepList[0])
#     except Exception as e:
#         raise e
#     #------------------------------> 
#     try:
#         return dtsCheck.ListUnique(values)
#     except Exception as e:
#         raise e
#     #endregion -----------------------------------------------> Check Elements
# #---

# def TcUniqueColNumbers(
#     tcList: list['wx.TextCtrl'], sepList: list[str]=[' ', ',', ';'],
#     ) -> tuple[bool, Optional[tuple[str, Optional[str], str]]]:
#     """Checks that all elements in the wx.TextCtrl(s) are unique.

#         Parameters
#         ----------
#         tcList : list of wx.TextCtrl
#             List of wx.TextCtrl. Individual elements in each wx.TextCtrl value 
#             are separated by sepList[0]. e.g. '1 2 3' if sepList[0] is ' '.
#         sepList: list of str
#             Separator used in tcList and resCtrl. Individual elements in tcList
#             are separated by sepList[0] while elements in resCtrl are separated 
#             by:
#             sepList[0] : internal element separator
#             sepList[1] : intrarow separator
#             sepList[2] : interrow separator

#         Returns
#         -------
#         tupple:
#             (True, None)
#             (False, (NotUnique, repeated elements, msg))
            
#         Raises
#         ------
#         InputError
#             - When tcList is not iterable.
#             - When tcList contains elements that do not support the GetValue()
#                 method
#         See also UniqueColNumbers.
            
#         Notes
#         -----
#         Individual elements in tcList and resCtrl are expected to be integers.
#     """
#     # Partial test in test.unit.test_check.Test_TcUniqueColNumbers
#     #region -------------------------------------------------------> Variables
#     values = []
#     #endregion ----------------------------------------------------> Variables
    
#     #region -------------------------------------------------------> Form list
#     #------------------------------> tcList
#     try:
#         for tc in tcList:
#             try:
#                 values.append(tc.GetValue())
#             except Exception:
#                 msg = 'tcList must contain a list of wx.TextCtrl.'
#                 raise dtsException.InputError(msg)
#     except TypeError:
#         msg = f'tcList must be a list of wx.TextCtrl.'
#         raise dtsException.InputError(msg)
#     #endregion ----------------------------------------------------> Form list
    
#     #region ----------------------------------------------------------> Return
#     try:
#         return UniqueColNumbers(values, sepList=sepList)
#     except Exception as e:
#         raise e
#     #endregion -------------------------------------------------------> Return
# #---
#endregion ----------------------------------------------------------> Methods
