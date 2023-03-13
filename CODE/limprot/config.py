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
    #------------------------------> Names & Titles
    nMod:str            = 'Limited Proteolysis'                                 # Name of the Module
    nwRes:str           = 'Window Result LimProt'                               # Name for the Result Window
    nTab:str            = 'LimProt Tab Configuration'                           # Name of the Config Tab
    nPane:str           = 'LimProt Pane Configuration'                          # Name of the Config Pane
    npResControlExp:str = 'ResControlExp Pane LimProt'                          # Name of the ResCtrl Config Pane
    tTab:str            = 'LimProt'                                             # Title of the Config Tab
    #------------------------------> Label
    lStLane:str         = 'Lanes'                                               # lSt: Label for wx.StaticText
    lStBand:str         = 'Bands'
    lmClearPeptide:str  = 'Peptide'                                             # lm: Label for wx.MenuItem
    lmClearFragment:str = 'Fragment'
    lmClearGelSpot:str  = 'Gel Spot'
    lmClearBandLane:str = 'Band/Lane'
    lmClearAll:str      = 'All'
    lmToolLaneSel:str   = 'Lane Selection Mode'
    lmToolShowAll:str   = 'Show All'
    lmToolFrag:str      = 'Fragments'
    lmToolGel:str       = 'Gel'
    lmToolClearSel:str  = 'Clear Selection'
    lmToolExportSeq:str = 'Export Sequences'
    #------------------------------> Keywords for wx.Menu
    kwBandLane:str      = 'Tool LimProt Select Band/Lane'
    kwShowAll:str       = 'Tool LimProt Select Show All'
    kwClearPeptide:str  = 'Tool LimProt Clear Peptide'
    kwClearFragment:str = 'Tool LimProt Clear Fragment'
    kwClearGelSpot:str  = 'Tool LimProt Clear Gel Spot'
    kwClearBandLane:str = 'Tool LimProt Clear Band/Lane'
    kwClearAll:str      = 'Tool LimProt Clear All'
    #------------------------------> DataFrame Columns
    dfcolFirstPart:list[str] = field(default_factory=lambda:
        ['Sequence', 'Score', 'Nterm', 'Cterm', 'NtermF','CtermF', 'Delta'])
    dfcolCLevel:list[str] = field(default_factory=lambda: ['Ptost', 'Pc'])
    #------------------------------> Hints
    hBeta:str     = 'e.g. 0.05'
    hGamma:str    = 'e.g. 0.8'
    hTheta:str    = 'e.g. 4.5'
    hThetaMax:str = 'e.g. 8'
    #------------------------------> Tooltips
    ttBeta = ('Beta level for the analysis.\ne.g. 0.05')
    ttGamma = ('Confidence limit level for estimating the measuring '
                'precision.\ne.g. 0.80')
    ttTheta = ('Equivalence interval used in the analysis. The value depends '
        'on the Data Preparation selected. An empty values means that the '
        'equivalence interval will be calculated for each peptide.\ne.g. 3')
    ttThetaMax = ('Maximum value for the calculated Equivalence interval.'
                   '\ne.g. 8')
    #------------------------------> User defined options
    alpha:str    = ''
    beta:str     = ''
    gamma:str    = ''
    theta:str    = ''
    thetaMax:str = ''
    scoreVal:str = ''
    correctP:str = ''
    #endregion ------------------------------------------------------> Options
#---
#endregion ----------------------------------------------------> Configuration
