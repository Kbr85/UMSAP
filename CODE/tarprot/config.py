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
    #------------------------------> Names & Titles
    nwRes:str           = 'TarProt Window Result Targeted Proteolysis'          # Name of the TarProt Res window
    nwAAPlot:str        = 'TarProt Window Result AA Plot'
    nwHistPlot:str      = 'TarProt Window Result Hist Plot'
    nwCpRPlot:str       = 'TarProt Window Result CpR Plot'
    nwCEvolPlot:str     = 'TarProt Window Result CEvol Plot'
    nTab:str            = 'TarProt Configuration Tab'                           # Name of the Conf Tab
    nPane:str           = 'Pane TarProt'                                        # Name of Conf Pane
    npResControlExp:str = 'ResControlExpPaneTarProt'                            # Name of the ResCtrl Conf Pane
    tMod:str            = 'Targeted Proteolysis'                                # Name of the Module
    tuAA:str            = 'AA Distribution'                                     # Name of the AA Utility
    tuHist:str          = 'Histograms'
    tuCpR:str           = 'Cleavage per Residues'
    tuCEvol:str         = 'Cleavage Evolution'
    tTab:str            = 'TarProt'                                             # Title of the Conf Tab
    #------------------------------> Label
    lStExp:str          = 'Experiments'                                         # lSt: Label for wx.StaticText
    lmClearPeptide:str  = 'Peptide'                                             # lm: Label for wx.MenuItem
    lmClearFragment:str = 'Fragment'
    lmClearAll:str      = 'All'
    lOSampleReq:str     = 't-Test'                                              # Option label
    #------------------------------> Keywords for wx.MenuItems
    kwClearPeptide:str     = 'Tool Clear Peptide'
    kwClearFragment:str    = 'Tool Clear Fragment'
    kwClearAll:str         = 'Tool Clear All'
    kwFACleavageEvol:str   = 'Tool Further Analysis Cleavage Evolution'
    kwFACleavagePerRes:str = 'Tool Further Analysis Cleavage per Residue'
    kwFAPDBMap             = 'Tool Further Analysis PDB Map'
    kwAAExp:str            = 'Tool AA AA'
    kwAAPos:str            = 'Tool AA Pos'
    kwMon:str              = 'mon'                                              # Methods keywords
    kwAllCleavage:str      = 'allC'
    #------------------------------> DF Columns
    dfcolFirstPart:list[str] = field(default_factory=lambda:
        ['Sequence', 'Score', 'Nterm', 'Cterm', 'NtermF','CtermF'])
    dfcolBLevel:list[str]    = field(default_factory=lambda: ['Int', 'P', 'Pc'])
    #------------------------------> Options
    oMethod:dict = field(default_factory=lambda: {                              # Analysis Method
        ''      : '',
        'Slope' : 'slope',
        't-Test': 'ttest',
    })
    oMethodP:dict = field(default_factory=lambda: {                             # Pretty print method
        'slope' : 'Slope',
        'ttest' : 't-Test',
    })
    #------------------------------> Further Analysis Key in UMSAP File
    faID:list[str] = field(default_factory=lambda: ['AA', 'Hist'])
    #------------------------------> Messages
    mRepNum:str = ('To perform a Targeted Proteolysis analysis using Paired '
                   'Samples the number of replicates in experiments and the '
                   'control must be the same.\nThe number of replicates in '
                   'the following experiments does not match the number of '
                   'replicates in the control.\n{}'
    )
    #------------------------------> Colors
    cXaa:str  = 'GREY'
    #------------------------------> User defined options
    alpha:str    = ''
    scoreVal:str = ''
    correctP:str = ''
    aaPos:str    = ''
    histWind:str = ''
    cCtrl:str    = 'black'
    cAve:str     = 'cyan'
    cAveL:str    = '#417ab1'
    #endregion ------------------------------------------------------> Options
#---
#endregion ----------------------------------------------------> Configuration
