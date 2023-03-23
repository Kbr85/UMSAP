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
    nwAbout:str                = 'Help About UMSAP'
    ndCheckUpdateResDialog:str = 'Help Check for Updates'
    ndPreferences:str          = 'Help Preferences'
    ntGeneral:str              = 'Help Tab General'
    ntCorrA:str                = 'Help Tab CorrA'
    ntData:str                 = 'Help Tab DataPrep'
    ntLimProt:str              = 'Help Tab LimProt'
    ntProtProf:str             = 'Help Tab ProtProf'
    ntTarProt:str              = 'Help Tab TarProt'
    npGeneral:str              = 'Help Pane General'
    npCorrA:str                = 'Help Pane CorrA'
    npData:str                 = 'Help Pane DataPrep'
    npLimProt:str              = 'Help Pane LimProt'
    npProtProf:str             = 'Help Pane ProtProf'
    npTarProt:str              = 'Help Pane TarProt'
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
