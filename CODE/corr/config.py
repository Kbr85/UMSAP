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
    nUtil:str  = 'Correlation Analysis'                                         # Name of the Utility
    nTab:str   = 'Tab Correlation AnalysisA'                                    # Name for the Tab
    nPane:str  = 'Pane Correlation Analysis'                                    # Name for Conf Pane
    tCorrA:str = 'CorrA'                                                        # Title of the Tab
    #------------------------------> Label for wx.StaticText
    lStColAnalysis:str = 'Columns for Analysis'
    #------------------------------> Options
    oCorrMethod:dict = field(default_factory=lambda: {
        ''        : '',
        'Pearson' : 'Pearson',
        'Kendall' : 'Kendall',
        'Spearman': 'Spearman',
    })
    #endregion ------------------------------------------------------> Options
#---
#endregion ----------------------------------------------------> Configuration
