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
    nMod:str            = 'Targeted Proteolysis'                                # Name of the Module
    nuAA:str            = 'AA Distribution'                                     # Name of the AA Utility
    nuHist:str          = 'Histograms'
    nuCpR:str           = 'Cleavage per Residues'
    nuCEvol:str         = 'Cleavage Evolution'
    nwRes:str           = 'Window Result Targeted Proteolysis'                  # Name of the TarProt Res window
    nwAAPlot:str        = 'Window Result AA Plot'
    nwHistPlot:str      = 'Window Result Hist Plot'
    nwCpRPlot:str       = 'Window Result CpR Plot'
    nwCEvolPlot:str     = 'Window Result CEvol Plot'
    nTab:str            = 'TarProt Configuration Tab'                           # Name of the Conf Tab
    nPane:str           = 'Pane TarProt'                                        # Name of Conf Pane
    npResControlExp:str = 'ResControlExpPaneTarProt'                            # Name of the ResCtrl Conf Pane
    tTab:str            = 'TarProt'                                             # Title of the Conf Tab
    #------------------------------> Label
    lStExp:str          = 'Experiments'                                         # lSt: Label for wx.StaticText
    lmClearPeptide:str  = 'Peptide'                                             # lm: Label for wx.MenuItem
    lmClearFragment:str = 'Fragment'
    lmClearAll:str      = 'All'
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
    dfcolBLevel:list[str] = field(default_factory=lambda: ['Int', 'P'])
    #------------------------------> Colors
    cXaa:str  = 'GREY'
    cCtrl:str = 'black'
    cFragment:list[str] = field(default_factory=lambda:
        ['#ffef96', '#92a8d1', '#b1cbbb', '#eea29a', '#b0aac0',
         '#f4a688', '#d9ecd0', '#b7d7e8', '#fbefcc', '#a2836e',]
    )
    cBarColor:dict = field(default_factory=lambda: {
        'R': '#0099ff', 'K': '#0099ff', 'D': '#ff4d4d', 'W': '#FF51FD',
        'E': '#ff4d4d', 'S': '#70db70', 'T': '#70db70', 'H': '#70db70',
        'N': '#70db70', 'Q': '#70db70', 'C': '#FFFC00', 'G': '#FFFC00',
        'P': '#FFFC00', 'A': '#BEBEBE', 'V': '#BEBEBE', 'I': '#BEBEBE',
        'L': '#BEBEBE', 'M': '#BEBEBE', 'F': '#FF51FD', 'Y': '#FF51FD',
    })
    cChi:dict = field(default_factory=lambda: {
        1 : 'Green',
        0 : 'Red',
        -1: 'Black',
    })
    #------------------------------> Converter for user options
    converter:dict = field(default_factory=lambda: {})
    #endregion ------------------------------------------------------> Options
#---
#endregion ----------------------------------------------------> Configuration
