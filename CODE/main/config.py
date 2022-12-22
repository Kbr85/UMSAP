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


"""Configuration for the main module of the app"""


#region -------------------------------------------------------------> Imports
from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from main import window as mWindow
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------> Configuration
@dataclass
class Configuration():
    """Configuration for the main module"""
    #------------------------------> Names
    nwMain:str          = 'Analysis Setup'
    #------------------------------> Keyword for Menu items

    #------------------------------> Reference to main window
    mainWin:Optional['mWindow.WindowMain'] = None
    #------------------------------> Converter for user options
    converter:dict = field(default_factory=lambda: {})
#---
#endregion ----------------------------------------------------> Configuration
