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


"""Configuration for the protprof module of the app"""


#region -------------------------------------------------------------> Imports
from dataclasses import dataclass, field
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------> Configuration
@dataclass
class Configuration():
    """Configuration for the protprof module"""
    #region ---------------------------------------------------------> Options
    nMod:str  = 'Proteome Profiling'                                            # Name of the Module
    nPane:str = 'Pane ProtProf'                                                 # Name of Conf Pane
    #------------------------------> Converter for user options
    converter:dict = field(default_factory=lambda: {})
    #endregion ------------------------------------------------------> Options
#---
#endregion ----------------------------------------------------> Configuration
