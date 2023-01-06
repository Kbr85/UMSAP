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


"""Menu for the dataprep module of the app"""


#region -------------------------------------------------------------> Imports
from core import menu as cMenu
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Classes
class ToolDataPrep(cMenu.BaseMenuMainResult):
    """Tool menu for the Data Preparation Plot window.

        Parameters
        ----------
        menuData: dict
            Data needed to build the menu. See Notes for more details.

        Notes
        -----
        menuData has the following structure:
        {
            'MenuDate' : [List of dates as str],
        }
    """
    #region --------------------------------------------------> Instance setup
    def __init__(self, menuData:dict={}) -> None:                               # pylint: disable=dangerous-default-value
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(menuData)
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        self.AddLastItems(False)
        #------------------------------> Remove Check Data Prep
        self.DestroyItem(self.miCheckDP)
        #endregion -----------------------------------------------> Menu Items
    #---
    #endregion -----------------------------------------------> Instance setup
#---
#endregion ----------------------------------------------------------> Classes
