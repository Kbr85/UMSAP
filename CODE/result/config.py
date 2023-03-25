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


"""Configuration for the result module of the app"""


#region -------------------------------------------------------------> Imports
from dataclasses import dataclass, field
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------> Configuration
@dataclass
class Configuration():
    """Configuration for the result module"""
    #region ---------------------------------------------------------> Options
    #------------------------------> Names & Titles
    nUtil:str          = 'Load UMSAP File'                                      # Name of the Util
    nwUMSAPControl:str = 'Window UMSAP Control'                                 # Name of window
    #------------------------------> Window Trackers
    winUMSAP:dict = field(default_factory=lambda: {})                           # Keys: UMSAP File path - Values: Reference to control window
    #------------------------------> Labels
    lmToolAdd:str    = 'Add Analysis'                                           # lm: Label for wx.MenuItem
    lmToolDel:str    = 'Delete Analysis'
    lmToolExp:str    = 'Export Analysis'
    lmToolReload:str = 'Reload File'
    #------------------------------> Key words for Menu
    kwToolAddDelExp:str = 'ToolUMSAPCtrl Add Del Export Analysis'
    kwToolReload:str    = 'ToolUMSAPCtrl Reload File'
    #endregion ------------------------------------------------------> Options
#---
#endregion ----------------------------------------------------> Configuration
