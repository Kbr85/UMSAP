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


"""Configuration for the tarprot module of the app"""


#region -------------------------------------------------------------> Imports
from dataclasses import dataclass, field
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------> Configuration
@dataclass
class Configuration():
    """Configuration for the tarprot module"""
    #region ---------------------------------------------------------> Options
    nMod:str            = 'Targeted Proteolysis'                                # Name of the Module
    nTab:str            = 'TarProt Configuration Tab'                           # Name of the Conf Tab
    nPane:str           = 'Pane TarProt'                                        # Name of Conf Pane
    npResControlExp:str = 'ResControlExpPaneTarProt'                            # Name of the ResCtrl Conf Pane
    tTab:str            = 'TarProt'                                             # Title of the Conf Tab
    #------------------------------> Label
    lStExp:str = 'Experiments'                                           # lSt: Label for wx.StaticText
    #------------------------------> DF Columns
    dfcolFirstPart:list[str] = field(default_factory=lambda:
        ['Sequence', 'Score', 'Nterm', 'Cterm', 'NtermF','CtermF'])
    dfcolBLevel:list[str] = field(default_factory=lambda: ['Int', 'P'])
    #------------------------------> Converter for user options
    converter:dict = field(default_factory=lambda: {})
    #endregion ------------------------------------------------------> Options
#---
#endregion ----------------------------------------------------> Configuration
