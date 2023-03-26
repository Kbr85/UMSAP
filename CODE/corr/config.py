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
    nwRes:str = 'CorrA CorrAPlot'                                               # Name of the Result Window
    nTab:str  = 'CorrA Tab Correlation Analysis'                                # Name for the Tab
    nPane:str = 'CorrA Pane Correlation Analysis'                               # Name for Conf Pane
    tUtil:str = 'Correlation Analysis'                                          # Name of the Utility
    tTab:str  = 'CorrA'                                                         # Title of the Tab
    #------------------------------> Label
    lmSelCol:str = 'Show Selected Columns'                                      # lm: Label for wx.MenuItem
    lmAllCol:str = 'Show All Columns'
    #------------------------------> Keywords for Menu
    kwCol:str    = 'ToolCorrA Select Column'
    kwColKey:str = 'col'                                                        # Methods keyword
    kwBar:str    = 'bar'
    #------------------------------> Options
    oCorrMethod:list = field(default_factory=lambda:                            # Correlation Methods
        ['', 'Pearson', 'Kendall', 'Spearman'])
    #------------------------------> User Configurable Options
    CMAP:dict = field(default_factory=lambda : {                                # CMAP Colors
        'N' : 128,
        'c1': (255, 0, 0),
        'c2': (255, 255, 255),
        'c3': (0, 0, 255),
        'NA': '#90EE90',
    })
    corrMethod:str = ''                                                         # Default correlation method
    axisLabel:str  = 'Names'                                                    # In Res Plot show column names by default
    showBar:bool   = False                                                      # Do not show color bar by default
    #endregion ------------------------------------------------------> Options
#---
#endregion ----------------------------------------------------> Configuration
