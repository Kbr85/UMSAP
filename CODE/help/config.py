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
from dataclasses import dataclass
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------> Configuration
@dataclass
class Configuration():
    """Configuration for the help module"""
    #------------------------------> Name & Titles
    nwAbout:str                = 'Window About UMSAP'
    ndCheckUpdateResDialog:str = 'Dialog Check for Updates'
    ndPreferences:str          = 'Dialog Preferences'
    ntGeneral:str              = 'General'
    ntCorrA:str                = 'CorrA'
    ntData:str                 = 'DataPrep'
    ntProtProf:str             = 'ProtProf'
    npGeneral:str              = 'Pane Preference General'
    npCorrA:str                = 'Pane Preference CorrA'
    npData:str                 = 'Pane Preference DataPrep'
    npProtProf:str             = 'Pane Preference ProtProf'
    twAbout: str               = 'About UMSAP'
    tdPrefUpdate:str           = 'Preferences'
    tdCheckUpdate:str          = 'Check for Updates'
    #------------------------------>
    kwAbout:str      = 'help.About'
    kwTutorial:str   = 'help.Tutorial'
    kwManual:str     = 'help.Manual'
    kwCheckUp:str    = 'help.CheckUp'
    kwPreference:str = 'help.Preference'
#---
#endregion ----------------------------------------------------> Configuration
