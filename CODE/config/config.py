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
from typing import Literal
#endregion ----------------------------------------------------------> Imports


#region -----------------------------------------> NON-CONFIGURABLE PARAMETERS
#region --------------------------------------------------> General parameters
development = True # Track state, development (True) or production (False)
#------------------------------> 
version     = '2.2.1 (beta)' # String to write in the output files
software    = 'UMSAP' # Software short name
softwareF   = 'Utilities for Mass Spectrometry Analysis of Proteins'
dictVersion = { # dict for directly write into output files
    'Version': version,
}
# #------------------------------> 
os = platform.system() # Current operating system
cwd = Path(__file__)   # Config file path
# endregion -----------------------------------------------> General parameters


#region ---------------------------------------- Platform Dependent Parameters
# # There are some that must be defined in other sections
if os == 'Darwin':
    #------------------------------> Root & Resources Folder
    root = cwd.parent.parent.parent
    res = root / 'Resources'  # Path to the Resources folder
    #------------------------------> Index of the Tool Menu in the MenuBar
    toolsMenuIdx = 2
#     #------------------------------> Statusbar split size
#     sbPlot2Fields = [-1, 115]
#     sbPlot3Fields = [-1, -1, 115] 
    #------------------------------> Key for shortcuts
    copyShortCut = 'Cmd'
    #------------------------------> Delta space between consecutive windows
    deltaWin = 23
    #------------------------------> 
    commOpen = 'open'
elif os == 'Windows':
    #------------------------------> Root & Resources Folder
    if development:
        root = cwd.parent.parent.parent
        res = root / 'Resources'
    else:
        root = cwd.parent.parent
        res = root / 'RESOURCES/'
    #------------------------------> Index of the Tool Menu in the MenuBar
    toolsMenuIdx = 2
#     #------------------------------> Statusbar split size
#     sbPlot2Fields = [-1, 115]
#     sbPlot3Fields = [-1, -1, 115] 
    #------------------------------> Key for shortcuts
    copyShortCut = 'Ctrl'
    #------------------------------> Delta space between consecutive windows
    deltaWin = 20
    #------------------------------> 
    commOpen = 'start'
else:
    #------------------------------> Root & Resources Folder
    root = cwd.parent
    res = root / 'Resources'
    #------------------------------> Index of the Tool Menu in the MenuBar
    toolsMenuIdx = 3
#     #------------------------------> Statusbar split size
#     sbPlot2Fields = [-1, 115]
#     sbPlot3Fields = [-1, -1, 115] 
    #------------------------------> Key for shortcuts
    copyShortCut = 'Ctrl'
    #------------------------------> Delta space between consecutive windows
    deltaWin = 20
    #------------------------------> 
    commOpen = 'xdg-open'
#endregion ------------------------------------- Platform Dependent Parameters


#region -------------------------------------------------------------> Windows
#------------------------------> Reference to main window
winMain = None
#------------------------------> Number of windows for screen positioning
# Keys: Windows ID - Values: Total number of opened windows, except conf win
winNumber = {}
#------------------------------> Track open umsap files
# Keys: UMSAP File path - Values: Reference to control window
winUMSAP = {}
#endregion ----------------------------------------------------------> Windows


#region ---------------------------------------------------------------> Names
#------------------------------> Default name
nwDef = 'Untitled Window'
#------------------------------> Windows
nwMain          = 'Analysis Setup'
nwUMSAPControl  = 'UMSAP Control'
nwCorrAPlot     = 'CorrAPlot'
nwProtProf      = 'ProtProfPlot'
nwLimProt       = 'LimProtPlot'
nwTarProt       = 'TarProtPlot'
nwCheckDataPrep = 'Data Preparation'
# nwAAPlot        = 'AAPlot'
# nwHistPlot      = 'HistPlot'
# nwCpRPlot       = 'CpRPlot'
# nwCEvolPlot     = 'CEvolPlot'
nwAbout         = 'About UMSAP'
#------------------------------> Dialogs
ndCheckUpdateResDialog = 'Check for Updates'
ndPreferences          = 'Preferences'
ndResControlExp        = 'Results & Control Experiments'
ndFilterRemoveAny      = 'Remove Filters'
#------------------------------> Tab for notebook windows
ntDef        = 'Default Tab'
ntStart      = 'Start'
ntDataPrep   = "DataPrep"
ntCorrA      = 'CorrA'
ntLimProt    = 'LimProt'
ntProtProf   = 'ProtProf'
ntTarProt    = 'TarProt'
ntPrefUpdate = 'Updates'
#------------------------------> Individual Panes
npDef = 'Default Pane'
npListCtrlSearchPlot    = 'ListCtrlSearchPlot'
npNPlot                 = 'NPlot'
npCorrA                 = 'CorrAPane'
npDataPrep              = 'DataPrepPane'
npLimProt               = 'LimProtPane'
npProtProf              = 'ProtProfPane'
npTarProt               = 'TarProtPane'
npResControlExpProtProf = 'ResControlExpPaneProtProf'
npResControlExpLimProt  = 'ResControlExpPaneLimProt'
npResControlExpTarProt  = 'ResControlExpPaneTarProt'
npPrefUpdate            = 'PrefUpdate'
#------------------------------> Modules
nmLimProt  = 'Limited Proteolysis'
nmTarProt  = 'Targeted Proteolysis'
nmProtProf = 'Proteome Profiling'
#------------------------------> Utilities
nuDataPrep = "Data Preparation"
nuCorrA    = 'Correlation Analysis'
# nuAA       = 'AA Distribution'
# nuHist     = 'Histograms'
nuReadF    = 'Read UMSAP File'
# nuCpR      = 'Cleavage per Residues'
# nuCEvol    = 'Cleavage Evolution'
#endregion ------------------------------------------------------------> Names


#region ----------------------------------------------------------- Extensions
#------------------------------> For wx.Dialogs
elData  = 'txt files (*.txt)|*.txt'
elUMSAP = 'UMSAP files (*.umsap)|*.umsap'
# elPDB   = 'PDB files (*.pdb)|*.pdb'
elPDF   = 'PDF files (*.pdf)|*.pdf'
elSeq   = (
    "Text files (*.txt)|*.txt|"
    "Fasta files (*.fasta)|*.fasta"
)
elMatPlotSaveI = (
    "Portable Document File (*.pdf)|*.pdf|"
    "Portable Network Graphic (*.png)|*.png|"
    "Scalable Vector Graphic (*.svg)|*.svg|"
    "Tagged Image File (*.tif)|*.tif"
)
#------------------------------> File extensions. First item is default
esData  = ['.txt']
# esPDB   = ['.pdb']
esPDF   = ['.pdf']
esSeq   = ['.txt', '.fasta']
esUMSAP = ['.umsap']
#endregion -------------------------------------------------------- Extensions


#region ------------------------------------> Keywords for Menu - Method Links
#------------------------------> Help Menu
kwHelpAbout    = 'MenuHelp About UMSAP'
kwHelpManual   = 'MenuHelp Manual'
kwHelpTutorial = 'MenuHelp Tutorial'
kwHelpCheckUpd = 'MenuHelp Check for Updates'
kwHelpPref     = 'MenuHelp Preferences'
#------------------------------> Tool Menu for UMSAPCtrl
kwToolUMSAPCtrlAddDelExp = 'ToolUMSAPCtrl Add Del Export Analysis'
kwToolUMSAPCtrlReload    = 'ToolUMSAPCtrl Reload File'
#------------------------------> Tool Menu for Plot Window. General Items
kwToolWinUpdate    = 'Update Result Window'
kwToolDupWin       = 'Duplicate Window'
kwToolZoomResetAll = 'Reset Zoom All'
kwToolZoomReset    = 'Reset Zoom One'
kwToolExpData      = 'Export Data'
kwToolExpImgAll    = 'Export Image'
kwToolExpImg       = 'Export Image One'
kwToolCheckDP      = 'Check DP'
# klToolExpSeq       = 'Export Sequences'
#------------------------------> Tool Menu for CorrA
kwToolCorrACol  = 'ToolCorrA Select Column'
#------------------------------> Tool Menu for LimProt
kwToolLimProtBandLane = 'Band/Lane Sel'
kwToolLimProtShowAll  = 'Show All'
kwToolLimProtExpSeq   = 'Export Sequence'
# #------------------------------> Tool Menu for AA
# klToolAAExp = 'AA'
# klToolAAPos = 'Pos'
#------------------------------> Volcano Plot
kwToolVolPlot              = 'Volcano Plot CRP'
kwToolVolPlotLabelPick     = 'Vol Plot Pick Label'
kwToolVolPlotLabelProt     = 'Vol Plot Add Label'
kwToolVolPlotColorScheme   = 'Vol Plot Color Scheme'
kwToolVolPlotColorConf     = 'Vol Plot Color Configure'
# klToolVolPlotColorHypCurve = 'Hyperbolic Curve'
# klToolVolPlotColorPFC      = 'P - Log2FC'
# klToolVolPlotColorZ        = 'Z Score'
#------------------------------> Fold Change Evolution
kwToolFCShowAll = 'FC Plot Show All'
# #------------------------------> Further Analysis
# klFACleavageEvol = 'Cleavage Evolution'
# klFACleavagePerRes = 'Cleavage per Residue'
# klFAPDBMap = 'PDB Map'
#endregion ---------------------------------> Keywords for Menu - Method Links


#region ------------------------------------------------------> Path and Files
#------------------------------> Relevant paths
pImages = res / 'IMAGES' # Images folder
#------------------------------> Location & names of important files
fImgStart = pImages / 'MAIN-WINDOW/p97-2.png'
fImgIcon  = pImages / 'DIALOGUE/dlg.png'
fImgAbout = pImages / 'ABOUT/p97-2-about.png'
#------------------------------> Manual
fManual = res / 'MANUAL/manual.pdf'
#------------------------------> 
fConfig = Path.home() / '.umsap_config.json'
fConfigDef = res / 'CONFIG/config_def.json'
#------------------------------> Names
fnInitial    = "{}_{}-Initial-Data.txt"
fnFloat      = "{}_{}-Floated-Data.txt"
fnTrans      = "{}_{}-Transformed-Data.txt"
fnNorm       = "{}_{}-Normalized-Data.txt"
fnImp        = "{}_{}-Imputed-Data.txt"
fnTargetProt = "{}_{}-Target-Protein-Data.txt"
fnExclude    = "{}_{}-After-Excluding-Data.txt"
fnScore      = "{}_{}-Score-Filtered-Data.txt"
fnDataSteps  = 'Steps_Data_Files'
fnDataInit   = 'Input_Data_Files'
#endregion ---------------------------------------------------> Path and Files


#region ------------------------------------------------------------------ URL
#------------------------------> www.umsap.nl
urlHome     = 'https://www.umsap.nl'
urlUpdate   = f"{urlHome}/page/release-notes"
urlTutorial = f"{urlHome}/tutorial/2-2-X"
#endregion --------------------------------------------------------------- URL


#region --------------------------------------------------------------> Labels
#------------------------------> Pane Title
lnPaneConf = 'Configuration Options'
lnListPane = 'Data File Content'
#------------------------------> wx.Button
lBtnTypeResCtrl = 'Type Values'
#------------------------------> wx.ListCtrl
lLCtrlColNameI = ['#', 'Name']
# #------------------------------> wx.StaticBox
lStProtProfCond = 'Conditions'
lStProtProfRP   = 'Relevant Points'
lStLimProtLane  = 'Lanes'
lStLimProtBand  = 'Bands' 
lStTarProtExp   = 'Experiments'
lStCtrlName     = 'Name'
lStCtrlType     = 'Type'
#------------------------------> wx.StaticText
lStColAnalysis = 'Columns for Analysis'
lStScoreVal    = 'Score Value'
lStScoreCol    = 'Score'
lStResultCtrl  = 'Results - Control experiments'
lStResultCtrlS = 'Results - Control'
# lStExcludeRow  = 'Exclude Rows'
lStExcludeProt = 'Exclude Proteins'
lStGeneName    = 'Gene Names'
# #------------------------------> wx.ComboBox or wx.CheckBox
lCbCorrectP    = 'P Correction'
lCbSample      = 'Samples'
# lCbIntensity   = 'Intensities'
#------------------------------> wx.Dialog
lPdError = 'Fatal Error'
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
lmCorrASelCol  = 'Select Columns'
lmCorrAAllCol  = 'All Columns'
# lmNatSeq       = 'Native Sequence'
#endregion -----------------------------------------------------------> Labels


#region ------------------------------------------------------------> Tooltips
#------------------------------> wx.Button
ttBtnHelp = 'Read tutorial at {}.'
#------------------------------> wx.StaticText
ttStScoreVal = f'Set the minimum acceptable Score value.\ne.g. -4'
ttStScoreCol = f'Set the column number containing the {lStScoreVal}.\ne.g. 4'
ttStGenName = f'Set the column number containing the {lStGeneName}.\ne.g. 3'
ttStExcludeProt = (
    "Set the column number containing the data used to exclude proteins."
    "\ne.g. 8 10-12")
# ttStExcludeRow = (
#     'Set the column numbers containing the data used to Exclude Rows.'
#     '\ne.g. 8 10-12')
ttStCorrectP = 'Select the p correction method.'
ttStSample = (f"Specify if samples are independent or paired.\n"
    f"For example, samples are paired when the same Petri dish is "
    f"used for the control and experiment.")
# ttStIntensity = ('Specify if intensities are raw intensity values or are '
#     'already expressed as a ratio (SILAC, TMT/iTRAQ).')
#------------------------------> wx.ListCtrl
ttLCtrlCopyNoMod = (
    f"Selected rows can be copied ({copyShortCut}+C) but "
    f"the table cannot be modified."
)
ttLCtrlPasteMod = (
    f"New rows can be pasted ({copyShortCut}+V) after the "
    f"last selected element and existing ones cut/deleted "
    f"({copyShortCut}+X) or copied "
    f"({copyShortCut}+C)."
)
ttSectionRightClick = (
    'The content of the Section can be deleted with a right click.')
#endregion ---------------------------------------------------------> Tooltips


#region -------------------------------------------------------------> Options
oNumType = { 
    'int'  : int,
    'float': float,
}
oYesNo = {
    ''   : '',
    'Yes': True,
    'No' : False,
}
oTransMethod = {
    ''    : '',
    'None': 'None',
    'Log2': 'Log2',
}
oNormMethod = {
    ''      : '',
    'None'  : 'None',
    'Median': 'Median',
}
oImputation = {
    ''                   : '',
    'None'               : 'None',
    'Normal Distribution': 'ND',
}
oCorrMethod = {
    ''        : '',
    'Pearson' : 'Pearson',
    'Kendall' : 'Kendall',
    'Spearman': 'Spearman',
}
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
oFillLoc = ('end', 'start')



# oMsgType = ('errorF', 'errorU', 'warning', 'success')

# oSelectF = ('openO', 'openM', 'save')
#endregion ----------------------------------------------------------> Options


#region --------------------------------------------------------> Literal
litFFSelect     = Literal['openO', 'openM', 'save', 'folder']
litFSelect      = Literal['openO', 'openM', 'save']
litFoF          = Literal['file', 'folder']
litNumType      = Literal['int', 'float']
litNotification = Literal['errorF', 'errorU', 'warning', 'success', 'question']
litComp         = Literal['lt', 'le', 'e', 'ge', 'gt']
#endregion -----------------------------------------------------> Literal


#region -----------------------------------------------------> DF Column names
dfcolProtprofFirstThree = ['Gene', 'Protein', 'Score']
dfcolProtprofCLevel = ['aveC', 'stdC', 'ave', 'std', 'FC', 'CI', 'FCz']
dfcolLimProtFirstPart = [
    'Sequence', 'Score', 'Nterm', 'Cterm', 'NtermF', 'CtermF', 'Delta']
dfcolLimProtCLevel = ['Ptost']
dfcolTarProtFirstPart = [
    'Sequence', 'Score', 'Nterm', 'Cterm', 'NtermF', 'CtermF']
dfcolTarProtBLevel = ['Int', 'P']
dfcolSeqNC = ['Sequence', 'Nterm', 'Cterm', 'NtermF', 'CtermF']
#endregion --------------------------------------------------> DF Column names


#region -----------------------------------------------------> Important Lists
ltDPKeys = ['dfF', 'dfT', 'dfN', 'dfIm']

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

# oAA3toAA = { # Three to one AA code translation
#     'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D', 
#     'CYS': 'C', 'GLU': 'E', 'GLN': 'Q', 'GLY': 'G',
#     'HIS': 'H', 'ILE': 'I', 'LEU': 'L', 'LYS': 'K', 
#     'MET': 'M', 'PHE': 'F', 'PRO': 'P', 'SER': 'S', 
#     'THR': 'T', 'TRP': 'W', 'TYR': 'Y', 'VAL': 'V',
# }
#endregion --------------------------------------------------> Important Lists


#region ------------------------------------------------------------> Messages
#region -------------------------------------------------------------> Other 
#------------------------------> Unexpected Error
mUnexpectedError = 'UMSAP encountered an unexpected error.'
#------------------------------> Check for Update
mCheckUpdate = 'Check for Updates failed. Check again later.'
#------------------------------> Sequences related errors
mSeqPeptNotFound = ("The peptide '{}' was not found in the sequence of the {} "
    "protein.")
#------------------------------> Optional Field
mOptField = '\nThis field is optional.'
#endregion ----------------------------------------------------------> Other

#region ------------------------------------------------------------> Values
mOneRNumText = "Only one real number can be accepted here."
mOneRPlusNumText = (
    "Only one number equal or greater than zero can be accepted here.")
mOneZPlusNumText = "Only a non-negative integer can be accepted here."
mOne01NumText = "Only one number between 0 and 1 can be accepted here."
mNZPlusNumText = (
    "Only a list of unique non-negative integers can be accepted here.")
#endregion ---------------------------------------------------------> Values

#region ---------------------------------------------------------------> Files
mFileSelector = 'It was not possible to show the file selecting dialog.'
mFileSelUMSAP = 'Select the UMSAP File'
mFileRead = 'An error occurred when reading file:\n{}'
# mWriteErrorIO = "The selected file could not be written.\nSelected file: {}"
#endregion ------------------------------------------------------------> Files

#region ------------------------------------------------------------> Pandas
mPDGetInitCol = ('It was not possible to extract the selected columns ({}) '
    'from the selected {} file:\n{}')
mPDDataTargetProt = ('Selection of Target Protein failed.\nTarget Protein: {} '
    'Detected Proteins column: {}.')
mPDDataExclude = 'Data Exclusion failed.\nColumns used for data exclusion: {}.'
mPDDataScore = ('Data Filtering by Score value failed.\nColumns used for data '
    'filtering by Score value: {}.')
mPDDataTypeCol = 'The {} contains unexpected data type in columns {}.'
#endregion ---------------------------------------------------------> Pandas
 
#region ----------------------------------------------------> For CheckInput
mColNumbers = ('In addition, each value must be smaller than the total '
    'number of columns in the Data file.')
mColNumber = ('In addition, the value must be smaller than the total '
    'number of columns in the Data file.')
mSection = 'Values in section {} must be unique.'
mAllTextFieldEmpty = 'All text fields are empty. Nothing will be done.'
mRepeatColNum = 'There are repeated column numbers in the text fields.'
mRowsInLCtrl = 'There must be at least {} items in {}.'
mNoDataLeft = ('No data left for analysis after all filters (Score, Target '
    'Protein, etc) were applied.')
mFileBad = "File: '{}'\ncannot be used as {} file."
mOptionBad = "Option '{}' cannot be accepted in {}."
mValueBad = "Value '{}' cannot be accepted in {}.\n"
mOneRealNum = f"{mValueBad}{mOneRNumText}"
mOneRPlusNum = f"{mValueBad}{mOneRPlusNumText}"
mOneZPlusNum = f"{mValueBad}{mOneZPlusNumText}"
mOneZPlusNumCol = f"{mOneZPlusNum} {mColNumber}"
mNZPlusNum = f"{mValueBad}{mNZPlusNumText}"
mNZPlusNumCol = f"{mNZPlusNum} {mColNumbers}"
mOne01Num = f"{mValueBad}{mOne01NumText}"
mResCtrl = (
    f"{mValueBad}Please use the {lBtnTypeResCtrl} button to provide a "
    f"correct input.")
mResCtrlWin = ("Value '{}' cannot be accepted as input.\n"f"{mNZPlusNumText}")
mRepNum = ('The number of replicates in some experiments does not match '
    'the number of replicates in the control.')
mRepNumProtProf = ('To perform a Proteome Profiling analysis using Raw '
    'Intensities and Paired Samples the number of replicates in '
    'experiments and the corresponding control must be the '
    'same.\n\nThe number of replicates in the following '
    'experiments does not match the number of replicates in the '
    'corresponding control.\n{}'
)
mCtrlEmpty = 'None of the Control fields can be empty.'
#endregion -------------------------------------------------> For CheckInput

#------------------------------> 
mCompNYI = "Comparison method is not yet implemented: {}."
mPDFilterByCol  = "Filtering process failed."
# mWriteFilesIO = "The selected files could not be written to: {}"
mRangeNumIE = "Invalid range or number: {}"
# mNotIterable = "{} must be iterable but the given value ({}) is not."
# mpdReplaceVal = ("It was not possible to replace {} values with {}.")
# mPDExcludeCol  = "Exclusion process failed."
mNotImplementedFull = ('Option {} is not yet implemented. Valid options for {} '
    'are: {}.')
# mMsgTypeIE = (
#     f"Options for message mode are: {*oMsgType,}. "
#     "Option {} is unknown.")
mwxLCtrNoCopy    = "The elements of this list cannot be copied."
mCopyFailedW     = "Copy operation failed. Try again."
mwxLCtrNoChange  = "This list cannot be modified."
mPasteFailedW    = "Paste operation failed. Try again."
mNothingToPasteW = "Nothing to paste."
mwxLCtrlNColPaste = (
    "The clipboard content cannot be pasted because the number of "
    "columns being pasted is different to the number of columns "
    "in the list."
)
mInvalidValue = "'{}' is an invalid value."
# mPDSelCol  = "The specified columns {} were not found in the dataframe."
# mTransMethodIE = (
#     f"Options for transformation method are: {*oTransMethod,}. "
#     "Option {} is unknown.")
# mNormMethodIE = (
#     f"Options for normalization method are: {*oNormMethod,}. "
#     "Option {} is unknown.")
# mImputationMethodIE = (
#     f"Options for imputation method are: {*oImputation,}. "
#     "Option {} is unknown.")
# mAlpha = (
#     "The significance level (alpha) must be a number between 0 and 1. "
#     "The given value ({}) it is not within this range. ")
# mPairSamplesDiffRep = (
#     'For paired samples the number of replicates in {} and {} must be equal.')
# m1IntGET = ('{} must be an integer greater/equal than/to {}.')
mNotImplemented = 'Option {} is not yet implemented.'
mNotSupported = "{} value '{}' is not supported."
mEmpty = 'The field value cannot be empty.'
#endregion ---------------------------------------------------------> Messages


#region ---------------------------------------------------------> Date & Time
dtFormat = '%Y%m%d-%H%M%S'
#endregion ------------------------------------------------------> Date & Time


#region ---------------------------------------------------------------> Sizes
#------------------------------> Full Windows
sWinRegular = (990, 775)
#------------------------------> Plot Window
sWinPlot = (560, 560)
sWinModPlot = (1100, 625)
#------------------------------> wx.TextCtrl
sTc = (50, 22)
#------------------------------> wx.ListCtrl
sLCtrlColI = [50, 150]
#endregion ------------------------------------------------------------> Sizes
#endregion --------------------------------------> NON-CONFIGURABLE PARAMETERS


#region ---------------------------------------------> CONFIGURABLE PARAMETERS
conflist = ['general']     # Sections to save/load in the configuration file
confUserFile = True          # User configuration file was read
confUserFileException = None # Exception thrown when reading conf file

#------------------------------> These must be dictionaries to save/load from
#------------------------------> configuration file
#region ------------------> Fonts. Set from UMSAP.py, requires a wx.App object
font = {
}
#endregion ---------------> Fonts. Set from UMSAP.py, requires a wx.App object


#region -----------------------------------------------------> General options
general = { # General options
    'checkUpdate'  : True, # True Check, False No check
    'DPI'          : 100,  # DPI for plot images
    'MatPlotMargin': 0.025 # Margin for the axes range
}
#endregion --------------------------------------------------> General options


#region --------------------------------------------------------------> Colors
colorFragments = [
    '#ffef96', '#92a8d1', '#b1cbbb', '#eea29a', '#b0aac0',
    '#f4a688', '#d9ecd0', '#b7d7e8', '#fbefcc', '#a2836e',
]

color = { # Colors for the app
    'Zebra' : '#ffe6e6',
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
#     nwAAPlot : {
#         'BarColor': { 
#             'R': '#0099ff', 'K': '#0099ff', 'D': '#ff4d4d', 'W': '#FF51FD', 
#             'E': '#ff4d4d', 'S': '#70db70', 'T': '#70db70', 'H': '#70db70', 
#             'N': '#70db70', 'Q': '#70db70', 'C': '#FFFC00', 'G': '#FFFC00', 
#             'P': '#FFFC00', 'A': '#BEBEBE', 'V': '#BEBEBE', 'I': '#BEBEBE', 
#             'L': '#BEBEBE', 'M': '#BEBEBE', 'F': '#FF51FD', 'Y': '#FF51FD', 
#         },
#         'Chi' : {
#             1 : 'Green',
#             0 : 'Red',
#             -1: 'Black',
#         },
#         'Xaa' : 'GREY',
#         'Spot' : colorFragments,
#     },
#     nwHistPlot : {
#         'Spot' : colorFragments,
#     },
#     nwCpRPlot : {
#         'Spot' : colorFragments,
#     },
}
#endregion -----------------------------------------------------------> Colors


#region --------------------------------------------------------------> Values
values = {
    nwCheckDataPrep : {
        'Shift' : '1.8',
        'Width' : '0.3',
    }
}
#endregion -----------------------------------------------------------> Values
#endregion ------------------------------------------> CONFIGURABLE PARAMETERS