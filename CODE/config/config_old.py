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
#region -------------------------------------------------------------> Windows
#------------------------------> Number of windows for screen positioning
# Keys: Windows ID - Values: Total number of opened windows, except conf win
winNumber = {}
#------------------------------> Track open umsap files
# Keys: UMSAP File path - Values: Reference to control window
winUMSAP = {}
#endregion ----------------------------------------------------------> Windows


#region ---------------------------------------------------------------> Names
#------------------------------> Name of Utilities
nuReadF:str    = 'Read UMSAP File'
#------------------------------> Title of Tabs

tDataPrep:str = 'DataPrep'
tLimProt:str  = 'LimProt'
tProtProf:str = 'ProtProf'
tTarProt:str  = 'TarProt'
#------------------------------> Windows
nwUMSAPControl  = 'UMSAP Control'
nwCorrAPlot     = 'CorrAPlot'
nwProtProf      = 'ProtProfPlot'
nwLimProt       = 'LimProtPlot'
nwTarProt       = 'TarProtPlot'
nwCheckDataPrep = 'Data Preparation'
nwAAPlot        = 'AAPlot'
nwHistPlot      = 'HistPlot'
nwCpRPlot       = 'CpRPlot'
nwCEvolPlot     = 'CEvolPlot'
#------------------------------> Dialogs
ndResControlExp        = 'Results & Control Experiments'
ndFilterRemoveAny      = 'Remove Filters'
#------------------------------> Tab for notebook windows
#------------------------------> Individual Panes
npListCtrlSearchPlot    = 'ListCtrlSearchPlot'
npNPlot                 = 'NPlot'
npDataPrep              = 'DataPrepPane'
npLimProt               = 'LimProtPane'
npResControlExpProtProf = 'ResControlExpPaneProtProf'
npResControlExpLimProt  = 'ResControlExpPaneLimProt'
npResControlExpTarProt  = 'ResControlExpPaneTarProt'
#------------------------------> Utilities
nuAA       = 'AA Distribution'
nuHist     = 'Histograms'
nuCpR      = 'Cleavage per Residues'
nuCEvol    = 'Cleavage Evolution'
#endregion ------------------------------------------------------------> Names


#region ------------------------------------> Keywords for Menu - Method Links
#------------------------------> Tool Menu for UMSAPCtrl
kwToolUMSAPCtrlAddDelExp = 'ToolUMSAPCtrl Add Del Export Analysis'
kwToolUMSAPCtrlReload    = 'ToolUMSAPCtrl Reload File'
#------------------------------> Tool Menu for Plot Window. General Items
kwToolExpSeq             = 'GeneralTool Export Sequence'
kwToolExportDataFiltered = 'GeneralTool Export Filtered Data'
#------------------------------> Tool Menu for CorrA
kwToolCorrACol  = 'ToolCorrA Select Column'
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
#------------------------------> Pane Title

lnListPane = 'Data File Content'
#------------------------------> wx.Button

#------------------------------> wx.ListCtrl

# #------------------------------> wx.StaticBox
lStProtProfCond = 'Conditions'
lStProtProfRP   = 'Relevant Points'
lStLimProtLane  = 'Lanes'
lStLimProtBand  = 'Bands'
lStTarProtExp   = 'Experiments'
lStCtrlName     = 'Name'
lStCtrlType     = 'Type'
#------------------------------> wx.StaticText
lStScoreVal    = 'Score Value'
lStScoreCol    = 'Score'
lStResultCtrlS = 'Results - Control'
lStExcludeProt = 'Exclude Proteins'
lStGeneName    = 'Gene Names'
# #------------------------------> wx.ComboBox or wx.CheckBox
lCbCorrectP    = 'P Correction'
lCbSample      = 'Samples'
#------------------------------> Filters
lFilFCEvol   = 'FC Evolution'
lFilHypCurve = 'Hyp Curve'
lFilFCLog    = 'Log2FC'
lFilPVal     = 'P Val'
lFilZScore   = 'Z Score'
#------------------------------> wx.Menu
lmToolUMSAPCtrlAdd = 'Add Analysis'
lmToolUMSAPCtrlDel = 'Delete Analysis'
lmToolUMSAPCtrlExp = 'Export Analysis'
lmCorrASelCol      = 'Select Columns'
lmCorrAAllCol      = 'All Columns'
#endregion -----------------------------------------------------------> Labels


#region ------------------------------------------------------------> Tooltips
#------------------------------> wx.StaticText
ttStScoreVal    = 'Set the minimum acceptable Score value.\ne.g. -4'
ttStScoreCol    = f'Set the column number containing the {lStScoreVal}.\ne.g. 4'
ttStGenName     = f'Set the column number containing the {lStGeneName}.\ne.g. 3'
ttStExcludeProt = ("Set the column number containing the data used to exclude "
                   "proteins.\ne.g. 8 10-12")
ttStCorrectP    = 'Select the p correction method.'
ttStSample      = ("Specify if samples are independent or paired.\n"
                   "For example, samples are paired when the same Petri dish "
                   "is used for the control and experiment.")
#endregion ---------------------------------------------------------> Tooltips


#region -------------------------------------------------------------> Options
oIntensities = {
    'Empty' : '',
    'RawI'  : 'Raw Intensities',
    'RatioI': 'Ratio of Intensities',
}
oSamples = {
    '': '',
    'Independent Samples': 'i',
    'Paired Samples': 'p',
}
oCorrectP = {
    ''                     : '',
    'None'                 : 'None',
    'Bonferroni'           : 'bonferroni',
    'Sidak'                : 'sidak',
    'Holm - Sidak'         : 'holm-sidak',
    'Holm'                 : 'holm',
    'Simes - Hochberg'     : 'simes-hochberg',
    'Hommel'               : 'hommel',
    'Benjamini - Hochberg' : 'fdr_bh',
    'Benjamini - Yekutieli': 'fdr_by',
}
oControlTypeProtProf = {
    'Empty': '',
    'OC'   : 'One Control',
    'OCC'  : 'One Control per Column',
    'OCR'  : 'One Control per Row',
    'Ratio': oIntensities['RatioI'],
}
#endregion ----------------------------------------------------------> Options


#region --------------------------------------------------------> Literal
litComp         = Literal['lt', 'le', 'e', 'ge', 'gt']
litStartEnd     = Literal['end', 'start']
litTestSide     = Literal['ts', 's', 'l']
#endregion -----------------------------------------------------> Literal


#region -----------------------------------------------------> DF Column names
dfcolProtprofFirstThree = ['Gene', 'Protein', 'Score']
dfcolProtprofCLevel     = ['aveC', 'stdC', 'ave', 'std', 'FC', 'CI', 'FCz']
dfcolLimProtFirstPart   = ['Sequence', 'Score', 'Nterm', 'Cterm', 'NtermF',
                           'CtermF', 'Delta']
dfcolLimProtCLevel      = ['Ptost']
dfcolTarProtFirstPart   = ['Sequence', 'Score', 'Nterm', 'Cterm', 'NtermF',
                           'CtermF']
dfcolTarProtBLevel      = ['Int', 'P']
dfcolSeqNC              = ['Sequence', 'Nterm', 'Cterm', 'NtermF', 'CtermF']
#endregion --------------------------------------------------> DF Column names


#region -----------------------------------------------------> Important Lists
lAA1 = [ # AA one letter codes
    'A', 'I', 'L', 'V', 'M', 'F', 'W', 'Y', 'R', 'K', 'D', 'E', 'C', 'Q',
    'H', 'S', 'T', 'N', 'G', 'P'
]

lAAGroups = [ # AA groups
    ['A', 'I', 'L', 'V', 'M'],
    ['F', 'W', 'Y'],
    ['R', 'K'],
    ['D', 'E'],
    ['C', 'Q', 'H', 'S', 'T', 'N'],
    ['G', 'P']
]

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
#------------------------------> Unexpected Error
mUnexpectedError = 'UMSAP encountered an unexpected error.'
#------------------------------> Check for Update
mCheckUpdate     = 'Check for Updates failed. Check again later.'
#------------------------------> Sequences related errors
mSeqPeptNotFound = ("The peptide '{}' was not found in the sequence of the {} "
    "protein.")
#------------------------------> Optional Field
mOptField        = '\nThis field is optional.'
#endregion ----------------------------------------------------------> Other

#region ------------------------------------------------------------> Values
mOneZPlusNumText = "Only a non-negative integer can be accepted here."
mOne01NumText    = "Only one number between 0 and 1 can be accepted here."
mNZPlusNumText   = (
    "Only a list of unique non-negative integers can be accepted here.")
#endregion ---------------------------------------------------------> Values

#region ---------------------------------------------------------------> Files
mFileSelector = 'It was not possible to show the file selecting dialog.'
#endregion ------------------------------------------------------------> Files

#region ------------------------------------------------------------> Pandas
mPDGetInitCol     = ('It was not possible to extract the selected columns ({}) '
                     'from the selected {} file:\n{}')
mPDDataTargetProt = ('Selection of Target Protein failed.\nTarget Protein: {} '
                     'Detected Proteins column: {}.')
mPDDataExclude    = ('Data Exclusion failed.\nColumns used for data exclusion: '
                    '{}.')
mPDDataScore      = ('Data Filtering by Score value failed.\nColumns used for '
                     'data filtering by Score value: {}.')
mPDDataTypeCol    = 'The {} contains unexpected data type in columns {}.'
#endregion ---------------------------------------------------------> Pandas

#region ----------------------------------------------------> For CheckInput
mColNumbers        = ('In addition, each value must be smaller than the total '
                      'number of columns in the Data file.')
mColNumber         = ('In addition, the value must be smaller than the total '
                      'number of columns in the Data file.')
mAllTextFieldEmpty = 'All text fields are empty. Nothing will be done.'
mRepeatColNum      = 'There are repeated column numbers in the text fields.'
mRowsInLCtrl       = 'There must be at least {} items in {}.'
mNoDataLeft        = ('No data left for analysis after all filters (Score, '
                      'Target Protein, etc) were applied.')
mOneRealNum        = f"{mValueBad}{mOneRNumText}"
mOneZPlusNum       = f"{mValueBad}{mOneZPlusNumText}"
mOneZPlusNumCol    = f"{mOneZPlusNum} {mColNumber}"
mNZPlusNum         = f"{mValueBad}{mNZPlusNumText}"
mNZPlusNumCol      = f"{mNZPlusNum} {mColNumbers}"
mOne01Num          = f"{mValueBad}{mOne01NumText}"
mResCtrl           = (f"{mValueBad}Please use the {lBtnTypeResCtrl} button to "
                      f"provide a correct input.")
mResCtrlWin        = ("Value '{}' cannot be accepted as input.\n"
                      f"{mNZPlusNumText}")
mRepNum            = ('The number of replicates in some experiments does not '
                      'match the number of replicates in the control.')
mRepNumProtProf    = ('To perform a Proteome Profiling analysis using Raw '
                      'Intensities and Paired Samples the number of replicates '
                      'in experiments and the corresponding control must be '
                      'the same.\n\nThe number of replicates in the following '
                      'experiments does not match the number of replicates in '
                      'the corresponding control.\n{}'
)
mCtrlEmpty         = 'None of the Control fields can be empty.'
#endregion -------------------------------------------------> For CheckInput

#------------------------------>
mCompNYI            = "Comparison method is not yet implemented: {}."
mPDFilterByCol      = "Filtering process failed."
mNotImplemented     = 'Option {} is not yet implemented.'
mNotSupported       = "{} value '{}' is not supported."
#endregion ---------------------------------------------------------> Messages


#region ---------------------------------------------------------------> Sizes
#------------------------------> Plot Window
sWinPlot    = (560, 560)
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
    nuCorrA : { # Color for plot in Correlation Analysis
        'CMAP' : { # CMAP colors and interval
            'N' : 128,
            'c1': (255, 0, 0),
            'c2': (255, 255, 255),
            'c3': (0, 0, 255),
            'NA': '#90EE90',
        },
    },
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
