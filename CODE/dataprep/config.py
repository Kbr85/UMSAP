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
    nUtil:str = 'Data Preparation'                                              # Name of the Utility
    #------------------------------> Normal distribution parameters
    Shift:float = 1.8                                                           # Shifted center
    Width:float = 0.3                                                           # Stdev
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
