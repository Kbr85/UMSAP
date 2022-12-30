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


"""Configuration for the corr module of the app"""


#region -------------------------------------------------------------> Imports
from dataclasses import dataclass
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------> Configuration
@dataclass
class Configuration():
    """Configuration for the core module"""
    #region ---------------------------------------------------------> Options
    nUtil:str = 'Correlation Analysis'                                          # Name of the Utility
    #endregion ------------------------------------------------------> Options
#---
#endregion ----------------------------------------------------> Configuration
