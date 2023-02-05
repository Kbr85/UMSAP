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


"""Methods for the main module of the app"""


#region -------------------------------------------------------------> Imports
import wx

from core import window as cWindow
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Classes
def BadUserConfFile(tException:Exception) -> bool:
    """Show error message when user configuration file could not be read.

        Parameters
        ----------
        tException: Exception
            Error exception.

        Returns
        -------
        bool

        Notes
        -----
        Always called from another thread.
    """
    # No Test
    msg = 'It was not possible to read the user configuration file.'
    wx.CallAfter(cWindow.Notification,'errorU', msg=msg, tException=tException)
    #------------------------------>
    return True
#---


def BadUserConfOptions(badOpt: list[str]) -> bool:
    """Show error message when user configuration file has invalid options.

        Parameters
        ----------
        badOpt: list[str]
            Bad options in the file.

        Returns
        -------
        bool

        Notes
        -----
        Always called from another thread.
    """
    # No Test
    #region -------------------------------------------------------->
    msg = 'The configuration file contains unknown options.'
    badOptList = ('The following options, present in the configuration file, '
                  'are unknown:\n')
    for k in badOpt:
        badOptList = f'{badOptList}{k}\n'
    #------------------------------>
    wx.CallAfter(cWindow.Notification,'errorU', msg=msg, tException=badOptList)
    #endregion ----------------------------------------------------->

    return True
#---
#endregion ----------------------------------------------------------> Classes
