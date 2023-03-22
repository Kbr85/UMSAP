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


"""Exceptions for the app"""


#region -------------------------------------------------------------> Imports
from pathlib import Path
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Classes
class Nothing2Plot(Exception):
    """Section in the UMSAP file has no results.

        Parameters
        ----------
        section:str
            Section in the umsap file with the problem.
        fileP: Path
            Path to the file
    """
    #region --------------------------------------------------> Instance setup
    def __init__(self, section:str, fileP:Path):
        """ """
        #region -----------------------------------------------> Initial Setup
        self.msg = (f'All entries for {section} in file '
                   f'{fileP.name} are corrupted or were not found.')
        #------------------------------>
        super().__init__(self.msg)
        #endregion --------------------------------------------> Initial Setup
        #---
    #endregion -----------------------------------------------> Instance setup
#---
#endregion ----------------------------------------------------------> Classes
