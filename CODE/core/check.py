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


"""Checks for the app"""


#region -------------------------------------------------------------> Imports
from typing import Optional
#endregion ----------------------------------------------------------> Imports

#region -------------------------------------------------------------> Methods
def VersionCompare(
    strA:str,
    strB:str,
    )-> tuple[bool, Optional[tuple[str, Optional[str], str]]]:
    """Basic version comparison.

        Parameters
        ----------
        strA: str
            Expected format is '2.3.4' or '2.3.4 (beta)'.
        strB: str
            Same format as strA is expected.

        Returns
        -------
        tuple
            (True, None)
            - (False, (code, value, msg))
                code is:
                - Exception, Input is not valid.
                - '', First version is lower than the second version.

        Notes
        -----
        Return True only if first argument is greater than the second.

        Examples
        --------
        >>> VersionCompare('2.4.7 beta', '2.4.7')
        >>> False
        >>> VersionCompare('2.4.7', '2.4.1')
        >>> True
        >>> VersionCompare('3.4.7 beta', '5.4.1')
        >>> False
    """
    # Test in test.unit.test_check.Test_VersionCompare
    #region -------------------------------------------------> Get number list
    try:
        xA, yA, zA = map(int, strA.strip().split(" ")[0].split("."))
        xB, yB, zB = map(int, strB.strip().split(" ")[0].split("."))
    except Exception as e:
        return (False, ('Exception', None, str(e)))
    #endregion ----------------------------------------------> Get number list

    #region ---------------------------------------------------------> Compare
    #------------------------------> First number
    if xA > xB:
        return (True, None)
    if xA < xB:
        return (False, ('', '', ''))
    #------------------------------> Second number
    if yA > yB:
        return (True, None)
    if yA < yB:
        return (False, ('', '', ''))
    #------------------------------> Third number
    if zA > zB:
        return (True, None)
    #endregion ------------------------------------------------------> Compare

    return (False, ('', '', ''))
#---
#endregion ----------------------------------------------------------> Methods
