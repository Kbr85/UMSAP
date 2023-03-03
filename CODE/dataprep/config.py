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
    nwRes:str = 'Data Preparation'                                              # Name of the Result Window
    nTab:str  = 'Tab Data Preparation'                                          # Name of Config Tab
    nPane:str = 'Pane Data Preparation'                                         # Name of Config Panel
    tTab:str  = 'DataPrep'                                                      # Title of the tab in Main Window
    #------------------------------> Label
    lONormDist: str = 'Normal Distribution'
    #------------------------------> PubSub Message
    psResDataPrep: str = 'data.ResDataPrep'
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
    #------------------------------> User defined options
    ceroT:str      = ''
    tranMethod:str = ''                                                         # Default Method
    normMethod:str = ''                                                         # Default Method
    impMethod:str  = ''                                                         # Default Method
    shift:str      = '1.8'                                                      # Shifted center
    width:str      = '0.3'                                                      # Stdev
    cBar:str       = '#3b75af'
    cBarI:str      = '#519e3E'
    cPDF:str       = '#ef8838'
    #endregion ------------------------------------------------------> Options
#---
#endregion ----------------------------------------------------> Configuration
