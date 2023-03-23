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
    nwAbout:str                = 'Name Window Help About UMSAP'
    ndCheckUpdateResDialog:str = 'Name Dialog Help Check for Updates'
    ndPreferences:str          = 'Name Dialog Help Preferences'
    ntGeneral:str              = 'Name Tab Preferences General'
    ntCorrA:str                = 'Name Tab Preferences CorrA'
    ntData:str                 = 'Name Tab Preferences DataPrep'
    ntLimProt:str              = 'Name Tab Preferences LimProt'
    ntProtProf:str             = 'Name Tab Preferences ProtProf'
    ntTarProt:str              = 'Name Tab Preferences TarProt'
    npGeneral:str              = 'Name Pane Preference General'
    npCorrA:str                = 'Name Pane Preference CorrA'
    npData:str                 = 'Name Pane Preference DataPrep'
    npLimProt:str              = 'Name Pane Preference LimProt'
    npProtProf:str             = 'Name Pane Preference ProtProf'
    npTarProt:str              = 'Name Pane Preference TarProt'
    twAbout: str               = 'About UMSAP'
    tdPrefUpdate:str           = 'Preferences'
    tdCheckUpdate:str          = 'Check for Updates'
    ttGeneral:str              = 'General'
    ttCorrA:str                = 'CorrA'
    ttData:str                 = 'DataPrep'
    ttLimProt:str              = 'LimProt'
    ttProtProf:str             = 'ProtProf'
    ttTarProt:str              = 'TarProt'
    #------------------------------>
    kwPubAbout:str      = 'pub.help.About'
    kwPubTutorial:str   = 'pub.help.Tutorial'
    kwPubManual:str     = 'pub.help.Manual'
    kwPubCheckUp:str    = 'pub.help.CheckUp'
    kwPubPreference:str = 'pub.help.Preference'
#---
#endregion ----------------------------------------------------> Configuration
