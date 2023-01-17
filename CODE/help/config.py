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


"""Configuration for the help module of the app"""


#region -------------------------------------------------------------> Imports
from dataclasses import dataclass, field
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------> Configuration
@dataclass
class Configuration():
    """Configuration for the help module"""
    #------------------------------> Name & Titles
    nwAbout:str                = 'Window About UMSAP'
    ndCheckUpdateResDialog:str = 'Dialog Check for Updates'
    ndPreferences:str          = 'Dialog Preferences'
    ntPrefUpdate:str           = 'Updates'
    npPrefUpdate:str           = 'Pane Preference Update'
    twAbout: str               = 'About UMSAP'
    tdPrefUpdate:str           = 'Preferences'
    tdCheckUpdate:str          = 'Check for Updates'
    #------------------------------> Converter for user options
    converter:dict = field(default_factory=lambda: {})
#---
#endregion ----------------------------------------------------> Configuration
