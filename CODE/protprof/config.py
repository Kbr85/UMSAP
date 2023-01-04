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
    nMod:str            = 'Proteome Profiling'                                  # Name of the Module
    nTab:str            = 'Tab Proteome Profiling'                              # Name of Conf Tab
    nPane:str           = 'Pane ProtProf'                                       # Name of Conf Pane
    npResControlExp:str = 'ResControlExpPaneProtProf'
    tTab:str            = 'ProtProf'                                            # Title of Conf Tab
    #------------------------------> Labels
    lStCond:str = 'Conditions'                                                  # lSt: Label for wx.StaticText
    lStRP:str   = 'Relevant Points'
    #------------------------------> DataFrame Columns
    dfcolProtprofFirstThree:list[str] = field(default_factory=lambda: ['Gene', 'Protein', 'Score'])
    dfcolProtprofCLevel:list[str]     = field(default_factory=lambda: ['aveC', 'stdC', 'ave', 'std', 'FC', 'CI', 'FCz'])
    #------------------------------> Options
    oControlType:dict = field(default_factory=lambda: {                         # Control Type for the Res - Ctrl wx.Dialog
        'Empty': '',
        'OC'   : 'One Control',
        'OCC'  : 'One Control per Column',
        'OCR'  : 'One Control per Row',
        'Ratio': 'Ratio of Intensities',
    })
    #------------------------------> Messages
    mRepNum:str = ('To perform a Proteome Profiling analysis using Raw '
                   'Intensities and Paired Samples the number of replicates '
                   'in experiments and the corresponding control must be '
                   'the same.\n\nThe number of replicates in the following '
                   'experiments does not match the number of replicates in '
                   'the corresponding control.\n{}'
    )
    #------------------------------> Converter for user options
    converter:dict = field(default_factory=lambda: {})
    #endregion ------------------------------------------------------> Options
#---
#endregion ----------------------------------------------------> Configuration
