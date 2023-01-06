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


"""Configuration parameters of the app"""


#region -------------------------------------------------------------> Imports
import platform
from pathlib import Path
from typing  import Literal
#endregion ----------------------------------------------------------> Imports


#region -----------------------------------------> NON-CONFIGURABLE PARAMETERS
#region ---------------------------------------------------------------> Names
#------------------------------> Windows
nwProtProf      = 'ProtProfPlot'
nwLimProt       = 'LimProtPlot'
nwTarProt       = 'TarProtPlot'
nwAAPlot        = 'AAPlot'
nwHistPlot      = 'HistPlot'
nwCpRPlot       = 'CpRPlot'
nwCEvolPlot     = 'CEvolPlot'
#------------------------------> Dialogs
ndFilterRemoveAny      = 'Remove Filters'
#------------------------------> Utilities
nuAA       = 'AA Distribution'
nuHist     = 'Histograms'
nuCpR      = 'Cleavage per Residues'
nuCEvol    = 'Cleavage Evolution'
#endregion ------------------------------------------------------------> Names


#region ------------------------------------> Keywords for Menu - Method Links
#------------------------------> Tool Menu for Plot Window. General Items
kwToolExpSeq             = 'GeneralTool Export Sequence'
kwToolExportDataFiltered = 'GeneralTool Export Filtered Data'
#------------------------------> Tool Menu for LimProt
kwToolLimProtBandLane = 'ToolLimProt Band/Lane Sel'
kwToolLimProtShowAll  = 'ToolLimProt Show All'
#------------------------------> Tool Menu for AA
kwToolAAExp = 'ToolAA AA'
kwToolAAPos = 'ToolAA Pos'
#------------------------------> Volcano Plot
kwToolVolPlot            = 'ToolVol Plot CRP'
kwToolVolPlotLabelPick   = 'ToolVol Plot Pick Label'
kwToolVolPlotLabelProt   = 'ToolVol Plot Add Label'
kwToolVolPlotColorScheme = 'ToolVol Plot Color Scheme'
kwToolVolPlotColorConf   = 'ToolVol Plot Color Configure'
#------------------------------> Fold Change Evolution
kwToolFCShowAll = 'FC Plot Show All'
#------------------------------> Further Analysis
kwToolFACleavageEvol   = 'Cleavage Evolution'
kwToolFACleavagePerRes = 'Cleavage per Residue'
kwToolFAPDBMap         = 'PDB Map'
#endregion ---------------------------------> Keywords for Menu - Method Links


#region --------------------------------------------------------------> Labels
#------------------------------> Filters
lFilFCEvol   = 'FC Evolution'
lFilHypCurve = 'Hyp Curve'
lFilFCLog    = 'Log2FC'
lFilPVal     = 'P Val'
lFilZScore   = 'Z Score'
#endregion -----------------------------------------------------------> Labels


#region -------------------------------------------------------------> Options
oIntensities = {
    'Empty' : '',
    'RawI'  : 'Raw Intensities',
    'RatioI': 'Ratio of Intensities',
}
#endregion ----------------------------------------------------------> Options


#region --------------------------------------------------------> Literal
litStartEnd     = Literal['end', 'start']
litTestSide     = Literal['ts', 's', 'l']
#endregion -----------------------------------------------------> Literal


#region -----------------------------------------------------> DF Column names
dfcolSeqNC              = ['Sequence', 'Nterm', 'Cterm', 'NtermF', 'CtermF']
#endregion --------------------------------------------------> DF Column names


#region -----------------------------------------------------> Important Lists
oAA3toAA = { # Three to one AA code translation
    'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D',
    'CYS': 'C', 'GLU': 'E', 'GLN': 'Q', 'GLY': 'G',
    'HIS': 'H', 'ILE': 'I', 'LEU': 'L', 'LYS': 'K',
    'MET': 'M', 'PHE': 'F', 'PRO': 'P', 'SER': 'S',
    'THR': 'T', 'TRP': 'W', 'TYR': 'Y', 'VAL': 'V',
}
#endregion --------------------------------------------------> Important Lists


#region ------------------------------------------------------------> Messages
#region -------------------------------------------------------------> Other
#------------------------------> Check for Update
mCheckUpdate     = 'Check for Updates failed. Check again later.'
#endregion ----------------------------------------------------------> Other

#region ---------------------------------------------------------------> Files
mFileSelector = 'It was not possible to show the file selecting dialog.'
#endregion ------------------------------------------------------------> Files

#region ------------------------------------------------------------> Pandas
mPDGetInitCol     = ('It was not possible to extract the selected columns ({}) '
                     'from the selected {} file:\n{}')
mPDDataTypeCol    = 'The {} contains unexpected data type in columns {}.'
#endregion ---------------------------------------------------------> Pandas

#------------------------------>
mCompNYI            = "Comparison method is not yet implemented: {}."
mPDFilterByCol      = "Filtering process failed."
mNotImplemented     = 'Option {} is not yet implemented.'
mNotSupported       = "{} value '{}' is not supported."
#endregion ---------------------------------------------------------> Messages


#region ---------------------------------------------------------------> Sizes
#------------------------------> Plot Window
sWinModPlot = (1100, 625)
#endregion ------------------------------------------------------------> Sizes
#endregion --------------------------------------> NON-CONFIGURABLE PARAMETERS


#region ---------------------------------------------> CONFIGURABLE PARAMETERS
#region --------------------------------------------------------------> Colors
colorFragments = [
    '#ffef96', '#92a8d1', '#b1cbbb', '#eea29a', '#b0aac0',
    '#f4a688', '#d9ecd0', '#b7d7e8', '#fbefcc', '#a2836e',
]

confColor = { # Colors for the app
    'RecProt' : 'gray',
    'NatProt' : '#c94c4c',
    nwProtProf : {
        'Vol'    : ['#ff3333', '#d3d3d3', '#3333ff'],
        'VolSel' : '#6ac653',
        'FCAll'  : '#d3d3d3',
        'FCLines': ['#ff5ce9', '#5047ff', '#ffa859', '#85ff8c', '#78dbff'],
        'CV'     : 'gray',
    },
    nwLimProt : {
        'Spot' : colorFragments,
    },
    nwTarProt : {
        'Spot' : colorFragments,
        'Ctrl' : 'black',
    },
    nwAAPlot : {
        'BarColor': {
            'R': '#0099ff', 'K': '#0099ff', 'D': '#ff4d4d', 'W': '#FF51FD',
            'E': '#ff4d4d', 'S': '#70db70', 'T': '#70db70', 'H': '#70db70',
            'N': '#70db70', 'Q': '#70db70', 'C': '#FFFC00', 'G': '#FFFC00',
            'P': '#FFFC00', 'A': '#BEBEBE', 'V': '#BEBEBE', 'I': '#BEBEBE',
            'L': '#BEBEBE', 'M': '#BEBEBE', 'F': '#FF51FD', 'Y': '#FF51FD',
        },
        'Chi' : {
            1 : 'Green',
            0 : 'Red',
            -1: 'Black',
        },
        'Xaa' : 'GREY',
        'Spot' : colorFragments,
    },
    nwHistPlot : {
        'Spot' : colorFragments,
    },
    nwCpRPlot : {
        'Spot' : colorFragments,
    },
}
#endregion -----------------------------------------------------------> Colors
#endregion ------------------------------------------> CONFIGURABLE PARAMETERS
