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


"""Configuration for the dataprep module of the app"""


#region -------------------------------------------------------------> Imports
from dataclasses import dataclass, field
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------> Configuration
@dataclass
class Configuration():
    """Configuration for the dataprep module"""
    #region ---------------------------------------------------------> Options
    #------------------------------> Name & Title
    nUtil:str      = 'Data Preparation'                                         # Name of the Utility
    ntDataPrep:str = 'Tab Data Preparation'                                     # Name of Config Tab
    npDataPrep:str = 'Pane Data Preparation'                                    # Name of Config Panel
    ttDataPrep:str = 'DataPrep'                                                 # Title of the tab in Main Window
    #------------------------------> Normal distribution parameters
    Shift:str = '1.8'                                                           # Shifted center
    Width:str = '0.3'                                                           # Stdev
    #------------------------------> Options
    oTransMethod:dict = field(default_factory=lambda: {                         # Transformation Methods
        ''    : '',
        'None': 'None',
        'Log2': 'Log2',
    })
    oNormMethod:dict = field(default_factory=lambda: {                          # Normalization Methods
        ''      : '',
        'None'  : 'None',
        'Median': 'Median',
    })
    oImputation:dict = field(default_factory=lambda: {                          # Imputation Methods
        ''                   : '',
        'None'               : 'None',
        'Normal Distribution': 'ND',
    })
    #endregion ------------------------------------------------------> Options
#---
#endregion ----------------------------------------------------> Configuration
