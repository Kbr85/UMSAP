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
from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from main import window as mWindow
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------> Configuration
@dataclass
class Configuration():
    """Configuration for the main module"""
    #------------------------------> Name & Title
    nwMain:str  = 'Window Analysis Setup'
    ntStart:str = 'Tab Start'
    twMain:str  = 'Analysis Setup'
    ttStart:str = 'Start'
    #------------------------------> Reference to main window
    mainWin:Optional['mWindow.WindowMain'] = None
#---
#endregion ----------------------------------------------------> Configuration
