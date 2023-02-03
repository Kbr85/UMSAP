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
from dataclasses import dataclass, field
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------> Configuration
@dataclass
class Configuration():
    """Configuration for the core module"""
    #region ---------------------------------------------------------> Options
    #------------------------------> Name & Title
    nUtil:str = 'Correlation Analysis'                                          # Name of the Utility
    nwRes:str = 'CorrAPlot'                                                     # Name of the Result Window
    nTab:str  = 'Tab Correlation AnalysisA'                                     # Name for the Tab
    nPane:str = 'Pane Correlation Analysis'                                     # Name for Conf Pane
    tTab:str  = 'CorrA'                                                         # Title of the Tab
    #------------------------------> Label
    lmSelCol:str = 'Select Columns'                                             # lm: Label for wx.MenuItem
    lmAllCol:str = 'All Columns'
    #------------------------------> Keywords for Menu
    kwCol:str = 'ToolCorrA Select Column'
    #------------------------------> Options
    oCorrMethod:list = field(default_factory=lambda:                            # Correlation Methods
        ['', 'Pearson', 'Kendall', 'Spearman'])
    #------------------------------> Colors
    CMAP:dict = field(default_factory=lambda : {                                # CMAP Colors
        'N' : 128,
        'c1': (255, 0, 0),
        'c2': (255, 255, 255),
        'c3': (0, 0, 255),
        'NA': '#90EE90',
    })
    #------------------------------> Converter for user options
    converter:dict = field(default_factory=lambda: {})
    #endregion ------------------------------------------------------> Options
#---
#endregion ----------------------------------------------------> Configuration