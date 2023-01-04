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


"""Configuration for the limprot module of the app"""


#region -------------------------------------------------------------> Imports
from dataclasses import dataclass, field
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------> Configuration
@dataclass
class Configuration():
    """Configuration for the limprot module"""
    #region ---------------------------------------------------------> Options
    nMod:str = 'Limited Proteolysis'                                            # Name of the Module
    nTab:str = 'LimProt Tab Configuration'                                      # Name of the Config Tab
    nPane:str ='LimProt Pane Configuration'                                     # Name of the Config Pane
    tTab:str = 'LimProt'                                                        # Title of the Config Tab
    #------------------------------> Label
    lStLane:str = 'Lanes'                                                       # lSt: LAbel for wx.StaticText
    lStBand:str = 'Bands'
    #------------------------------> DataFrame Columns
    dfcolFirstPart:list[str] = field(default_factory=lambda:
        ['Sequence', 'Score', 'Nterm', 'Cterm', 'NtermF','CtermF', 'Delta'])
    dfcolCLevel:list[str] = field(default_factory=lambda: ['Ptost'])
    #endregion ------------------------------------------------------> Options
#---
#endregion ----------------------------------------------------> Configuration
