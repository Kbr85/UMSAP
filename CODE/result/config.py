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
    """Configuration for the core module"""
    #region ---------------------------------------------------------> Options
    #------------------------------> Names & Titles
    nUtil:str          = 'Read UMSAP File'                                      # Name of the Util
    nwUMSAPControl:str = 'Window UMSAP Control'                                 # Name of window
    #------------------------------> Window Trackers
    winUMSAP:dict = field(default_factory=lambda: {})                           # Keys: UMSAP File path - Values: Reference to control window
    #------------------------------> Labels
    lmToolUMSAPCtrlAdd:str = 'Add Analysis'                                     # lm: Label for wx.MenuItem
    lmToolUMSAPCtrlDel:str = 'Delete Analysis'
    lmToolUMSAPCtrlExp:str = 'Export Analysis'
    #------------------------------> Key words for Menu
    kwToolUMSAPCtrlAddDelExp:str = 'ToolUMSAPCtrl Add Del Export Analysis'
    kwToolUMSAPCtrlReload:str    = 'ToolUMSAPCtrl Reload File'
    #------------------------------> Converter for user options
    converter:dict = field(default_factory=lambda: {})
    #endregion ------------------------------------------------------> Options
#---
#endregion ----------------------------------------------------> Configuration
