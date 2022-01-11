# ------------------------------------------------------------------------------
# Copyright (C) 2017 Kenny Bravo Rodriguez <www.umsap.nl>
#
# Author: Kenny Bravo Rodriguez (kenny.bravorodriguez@mpi-dortmund.mpg.de)
#
# This program is distributed for free in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See the accompaning licence for more details.
# ------------------------------------------------------------------------------


"""Configuration parameters of the app"""


#region -------------------------------------------------------------> Imports
import platform
from pathlib import Path
#endregion ----------------------------------------------------------> Imports


#region -----------------------------------------> NON-CONFIGURABLE PARAMETERS
#region --------------------------------------------------> General parameters
development = True # Track state, development (True) or production (False)

version     = '2.2.0 (beta)' # String to write in the output files
software    = 'UMSAP' # Software short name
softwareF   = 'Utilities for Mass Spectrometry Analysis of Proteins'
dictVersion = { # dict for directly write into output files
    'Version': version,
}

os = platform.system() # Current operating system
cwd = Path(__file__)    # Config file path

# # obj: Optional['file.UMSAPFile'] = None # To reload UMSAP file
# #endregion -----------------------------------------------> General parameters


#region ---------------------------------------- Platform Dependent Parameters
# There are some that must be defined in other sections
if os == 'Darwin':
    #------------------------------> Root & Resources Folder
    if development:
        root = cwd.parent.parent.parent
    else:
        root = cwd.parent.parent
    res = root / 'Resources'  # Path to the Resources folder
    #------------------------------> Index of the Tool Menu in the MenuBar
    toolsMenuIdx = 2
    #------------------------------> Statusbar split size
    if development:
        sbFieldSize = [-1, 350]
    else:
        sbFieldSize = [-1, 300]
# #     sbPlot2Fields = [-1, 115]
# #     sbPlot3Fields = [90, -1, 115] 
    #------------------------------> Key for shortcuts
    copyShortCut = 'Cmd'
# #     #------------------------------> Delta space between consecutive windows
# #     deltaWin = 23
elif os == 'Windows':
    #------------------------------> Root & Resources Folder
    root = cwd.parent.parent.parent
    res = root / 'Resources'
    #------------------------------> Index of the Tool Menu in the MenuBar
    toolsMenuIdx = 2
    #------------------------------> Statusbar split size
    if development:
        sbFieldSize = [-1, 325]
    else:
        sbFieldSize = [-1, 300]
# #     sbPlot = [-1, 115]
    #------------------------------> Key for shortcuts
    copyShortCut = 'Ctrl'
# #     #------------------------------> Delta space between consecutive windows
# #     deltaWin = 20
else:
    #------------------------------> Root & Resources Folder
    root = cwd.parent
    res = root / 'Resources'
    #------------------------------> Index of the Tool Menu in the MenuBar
    toolsMenuIdx = 3
    #------------------------------> Statusbar split size
    if development:
        sbFieldSize = [-1, 350]
    else:
        sbFieldSize = [-1, 300]
# #     sbPlot = [-1, 115]
    #------------------------------> Key for shortcuts
    copyShortCut = 'Ctrl'
# #     #------------------------------> Delta space between consecutive windows
# #     deltaWin = 20
#endregion ------------------------------------- Platform Dependent Parameters


#region -------------------------------------------------------------> Windows
# #------------------------------> Reference to main window
winMain = None
#------------------------------> Number of windows for screen positioning
# Keys: Windows ID - Values: Total number of opened windows, except conf win
winNumber = {}
# # #------------------------------> Track open umsap files
# # # Keys: UMSAP File path - Values: Reference to control window
# # winUMSAP = {}
#endregion ----------------------------------------------------------> Windows


#region ---------------------------------------------------------------> Names
#------------------------------> Default name
nDefName = 'Default name'
#------------------------------> Windows
nwMain          = 'MainW'
# # nwUMSAPControl  = 'UMSAPControl'
# # nwCorrAPlot     = 'CorrAPlot'
# # nwProtProf      = 'ProtProfPlot'
# # nwLimProt       = 'LimProtPlot'
# # nwCheckDataPrep = 'CheckDataPrep'
#------------------------------> Dialogs
ndCheckUpdateResDialog = 'CheckUpdateResDialog'
ndResControlExp        = 'ResControlExp'
# # ndFilterRemoveAny      = 'Remove Filters'
#------------------------------> Tab for notebook windows
ntStart    = 'StartTab'
ntDataPrep = "DataPrepTab"
ntCorrA    = 'CorrATab'
ntLimProt  = 'LimProtTab'
ntProtProf = 'ProtProfTab'
ntTarProt  = 'TarProtTab'
#------------------------------> Individual Panes
# # npListCtrlSearchPlot    = 'ListCtrlSearchPlot'
npCorrA                 = 'CorrAPane'
npDataPrep              = "DataPrepPane"
# # npLimProt               = "LimProtPane"
npProtProf              = 'ProtProfPane'
# # npResControlExp         = 'ResControlExpPane'
npResControlExpProtProf = 'ResControlExpPaneProtProf'
# # npResControlExpLimProt  = 'ResControlExpPaneLimProt'
# # #------------------------------> Files
# # nfUMSAP = 'UMSAPFile'
#------------------------------> Modules
nmLimProt  = 'Limited Proteolysis'
nmTarProt  = 'Targeted Proteolysis'
nmProtProf = 'Proteome Profiling'
#------------------------------> Utilities
nuDataPrep = "Data Preparation"
nuCorrA    = 'Correlation Analysis'
nuReadF    = 'Read UMSAP File'
#endregion ------------------------------------------------------------> Names


#region --------------------------------------------------------------> Titles
# # #------------------------------> Default names
tdW = "Untitled Window"
tdT = "Tab"
# tdP = 'Pane'
#------------------------------> 
t = {
    #------------------------------> Windows
    nwMain : "Analysis Setup",
    #------------------------------> Dialogs
    ndCheckUpdateResDialog: "Check for Updates",
    ndResControlExp       : 'Results - Control Experiments',
#     ndFilterRemoveAny     : 'Remove Filters',
    #------------------------------> Tabs
    ntStart   : 'Start',
    ntDataPrep: 'DataPrep',
    ntCorrA   : 'CorrA',
#     ntLimProt : 'LimProt',
    ntProtProf: 'ProtProf',
}
#endregion -----------------------------------------------------------> Titles


#region ----------------------------------------------------------- Extensions
#------------------------------> For wx.Dialogs
elData         = 'txt files (*.txt)|*.txt'
elSeq          = (
    "Text files (*.txt)|*.txt|"
    "Fasta files (*.fasta)|*.fasta"
)
elUMSAP        = 'UMSAP files (*.umsap)|*.umsap'
elMatPlotSaveI = (
    "Portable Document File (*.pdf)|*.pdf|"
    "Portable Network Graphic (*.png)|*.png|"
    "Scalable Vector Graphic (*.svg)|*.svg|"
    "Tagged Image File (*.tif)|*.tif"
)
#------------------------------> File extensions. First item is default
esData  = ['.txt']
esSeq   = ['.txt', '.fasta']
esUMSAP = ['.umsap']
#endregion -------------------------------------------------------- Extensions


#region ------------------------------------------------------> Path and Files
#------------------------------> Relevant paths
pImages = res / 'IMAGES' # Images folder
#------------------------------> Location & names of important files
fImgStart = pImages / 'MAIN-WINDOW/p97-2.png'
fImgIcon  = pImages / 'DIALOGUE'/'dlg.png'
# #------------------------------> Names
fnInitial    = "{}-Initial-Data-{}.txt"
fnFloat      = "{}-Floated-Data-{}.txt"
# # fnTargetProt = "{}-Target-Protein-Data-{}.txt"
fnExclude    = "{}-After-Excluding-Data-{}.txt"
fnScore      = "{}-Score-Filtered-Data-{}.txt"
fnTrans      = "{}-Transformed-Data-{}.txt"
fnNorm       = "{}-Normalized-Data-{}.txt"
fnImp        = "{}-Imputed-Data-{}.txt"
fnDataSteps  = 'Steps_Data_Files'
fnDataInit   = 'Input_Data_Files'
fnMainDataProtProf = '{}-ProteomeProfiling-Data-{}.txt'
#endregion ---------------------------------------------------> Path and Files


#region ------------------------------------------------------------------ URL
#------------------------------> www.umsap.nl
urlHome     = 'https://www.umsap.nl'
urlUpdate   = f"{urlHome}/page/release-notes"
urlTutorial = f"{urlHome}/tutorial/2-1-0"
# # urlLimProt  = f"{urlTutorial}/limited-proteolysis"
#endregion --------------------------------------------------------------- URL


#region --------------------------------------------------------------> Labels
#------------------------------> Pane Title
lnPaneConf = 'Configuration Options'
lnListPane = 'Data File Content'
#------------------------------> wx.Button
lBtnTypeResCtrl = 'Type Values'
# # lBtnOutFile     = 'Output File'
# # lBtnSeqFile     = 'Sequences'
#------------------------------> wx.ListCtrl
lLCtrlColNameI = ['#', 'Name']
#------------------------------> wx.StaticBox
lStProtProfCond = 'Conditions'
lStProtProfRP   = 'Relevant Points'
# # lStLimProtLane  = 'Lanes'
# # lStLimProtBand  = 'Bands' 
lStCtrlName     = 'Name'
lStCtrlType     = 'Type'
#------------------------------> wx.Statictext
lStColAnalysis = 'Columns for Analysis'
# # lStSeqFile      = 'Sequences'
lStScoreVal     = 'Score Value'
# # lStSeqLength    = 'Sequence Length'
# # lStTargetProt   = "Target Protein"
# # lStSeqCol       = 'Sequences'
lStScoreCol     = 'Score'
lStResultCtrl   = 'Results - Control experiments'
lStExcludeRow = 'Exclude Rows'
lStExcludeProt = 'Exclude Proteins'
# lStColAnalysis = 'Columns to Consider'
lStGeneName    = 'Gene Names'
#------------------------------> wx.ComboBox or wx.CheckBox
# # lCbFileAppend  = 'Append new data to selected output file'
lCbCorrectP    = 'P Correction'
lCbSample      = 'Samples'
lCbIntensity   = 'Intensities'
#endregion -----------------------------------------------------------> Labels


#region ---------------------------------------------------------------> Hints
# # hTcOutFile  = f"Path to the {lBtnOutFile} file"
# # hTcSeqFile  = f"Path to the {lBtnSeqFile} file"
# hTcId       = 
#endregion ------------------------------------------------------------> Hints


#region ------------------------------------------------------------> Tooltips
# #------------------------------> wx.Button
# # ttBtnOutFile  = f"Select the {lBtnOutFile}."
ttBtnHelp = 'Read tutorial at {}.'
#------------------------------> wx.StaticText
ttStScoreVal = f'Set the minimum acceptable Score value.\ne.g. -4'
# # ttStMedianCorr = "Select whether to apply a median correction."
ttStScoreCol = f'Set the column number containing the {lStScoreVal}.\ne.g. 4'
ttStGenName = f'Set the column number containing the {lStGeneName}.\ne.g. 3'
ttStExcludeProt = (
    "Set the column number containing the data used to exclude proteins."
    "\ne.g. 8 10-12")
ttStExcludeRow = (
    'Set the column numbers containing the data used to Exclude Rows.'
    '\ne.g. 8 10-12')
ttStCorrectP = 'Select the p correction method.'
ttStSample = (f"Specify if samples are independent or paired.\n"
    f"For example, samples are paired when the same Petri dish is "
    f"used for the control and experiment.")
ttStIntensity = ('Specify if intensities are raw intensity values or are '
    'already expressed as a ratio (SILAC, TMT/iTRAQ).')
# # #------------------------------> wx.ListCtrl
ttLCtrlCopyNoMod = (
    f"Selected rows can be copied ({copyShortCut}+C) but "
    f"the list cannot be modified."
)
ttLCtrlPasteMod = (
    f"New rows can be pasted ({copyShortCut}+V) after the "
    f"last selected element and existing ones cut/deleted "
    f"({copyShortCut}+X) or copied "
    f"({copyShortCut}+C)."    
)
#endregion ---------------------------------------------------------> Tooltips


#region -------------------------------------------------------------> Options
oTransMethod = {
    'Empty': '',
    'None' : 'None',
    'Log2' : 'Log2',
}
oNormMethod = {
    'Empty' : '',
    'None'  : 'None',
    'Median': 'Median',
}
oImputation = {
    'Empty': '',
    'None' : 'None',
    'ND'   : 'Normal Distribution',
}
oCorrMethod = {
    'Empty'   : '',
    'Pearson' : 'Pearson',
    'Kendall' : 'Kendall',
    'Spearman': 'Spearman',
}
# # oYesNo = {
# #     'Empty': '',
# #     'Yes'  : 'Yes',
# #     'No'   : 'No',
# # }
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
    'Simes-Hochberg'       : 'simes-hochberg',
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


#region -----------------------------------------------------> DF Column names
dfcolProtprofFirstThree = ['Gene', 'Protein', 'Score']
dfcolProtprofCLevel = ['aveC', 'stdC', 'ave', 'std', 'FC', 'CI', 'FCz']
# # dfcolDataCheck = [
# #     'Data', 'N', 'NaN', 'Mean', 'Median', 'SD', 'Kurtosis', 'Skewness']
# # dfcolLimProtFirstPart = [
# #     'Sequence', 'Score', 'Nterm', 'Cterm', 'NtermF', 'CtermF', 'Delta']
# # dfcolLimProtCLevel = ['Ptost']
#endregion --------------------------------------------------> DF Column names


#region -----------------------------------------------------> Important Lists
ltDPKeys = ['dfS', 'dfT', 'dfN', 'dfIm']
#endregion --------------------------------------------------> Important Lists


#region ------------------------------------------------------------> Messages
# #region -------------------------------------------------------------> Other 
# # #------------------------------> Unexpected Error
# # mUnexpectedError = 'An uexpected error was encountered.'
# # #------------------------------> Not empty
# # mNotEmpty = "Please select a value for {}."
# # #------------------------------> Sequences related errors
# # mSeqPeptNotFound = ("The peptide '{}' was not found in the sequence of the {} "
# #     "protein.")
# #endregion ----------------------------------------------------------> Other

# #region ------------------------------------------------------------> Values
mOneRNumText = "Only one real number can be accepted here."
mOneZPlusNumText = "Only a non-negative integer can be accepted here."
# # mOneZNumText = "Only one positive integer can be accepted here."
mOne01NumText = "Only one number between 0 and 1 can be accepted here"
mNZPlusNumText = (
    "Only a list of unique non-negative integers can be accepted here.")
# # mNumROne = "Only one number can be accepted in {}."
# # mNumZPlusOne = "Only one non-negative integer can be accepted in {}."
# # mListNumN0L = (
# #     "Only a list of unique non-negative integers can be accepted in {}.")
# # mAlphaRange = "Only one number between 0 and 1 can be accepted in {}."
# #endregion ---------------------------------------------------------> Values

#region ---------------------------------------------------------------> Files
# mFileUMSAP = ('It was not possible to write the results of the analysis to '
#     'the selected UMSAP file.')
# mFileDataExport = 'It was not possible to write the data to the selected file.'
# # mFileSelector = f"It was not possible to show the file selecting dialog."
mFileRead = 'An error occured when reading file:\n{}'
# # mFileColNum = (
# #     "In addition, the values cannot be bigger than the total number of columns "
# #     "in the {}.")
# # mUMSAPFile = 'Select the UMSAP File'
#endregion ------------------------------------------------------------> Files

#region ------------------------------------------------------------> Pandas
mPDGetInitCol = ('It was not possible to extract the selected columns ({}) '
    'from the selected {} file:\n{}')
mPDDataTargetProt = ('Selection of Target Protein failed.\nTarget Protein: {} '
    'Detected Proteins column: {}.')
mPDDataExclude = 'Data Exclusion failed.\nColumns used for data exclusion: {}.'
mPDDataScore = ('Data Filtering by Score value failed.\nColumns used for data '
    'filtering by Score value: {}.')
# # mPDDataType       = 'Unexpected data type.'
mPDDataTypeCol = 'The {} contains unexpected data type in columns {}.'
#endregion ---------------------------------------------------------> Pandas
 
#region ----------------------------------------------------> For CheckInput
mSection = 'Values in section {} must be unique.'
mAllTextFieldEmpty = 'All text fields are empty. Nothing will be done.'
mRepeatColNum = 'There are repeated column numbers in the text fields.'
mRowsInLCtrl = 'There must be at least {} items in {}.'
mNoDataLeft = ('No data left for analysis after all filters (Score, Target '
    'Protein, etc) were applied.')
mFileBad = "File: '{}'\ncannot be used as {}."
mOptionBad = "Option '{}' cannot be accepted in {}."
mValueBad = "Value '{}' cannot be accepted in {}.\n"
mOneRealNum = f"{mValueBad}{mOneRNumText}"
mOneZPlusNum = f"{mValueBad}{mOneZPlusNumText}"
mNZPlusNum = f"{mValueBad}{mNZPlusNumText}"
mOne01Num = f"{mValueBad}{mOne01NumText}"
mResCtrl = (
    f"{mValueBad}Please use the {lBtnTypeResCtrl} button to provide a "
    f"correct input.")
mResCtrlWin = ("Value '{}' cannot be accepted as input.\n"f"{mNZPlusNumText}")
#endregion -------------------------------------------------> For CheckInput
#endregion ---------------------------------------------------------> Messages


#region ---------------------------------------------------------------> Sizes
#------------------------------> Full Windows 
sWinRegular = (990, 775)
# # #------------------------------> Plot Window
# # sWinPlot = (560, 560)
# # sWinModPlot = (1100, 625)
#------------------------------> wx.StatusBar Fields
sSbarFieldSizeI = sbFieldSize
#------------------------------> wx.TextCtrl
sTc = (50, 22)
#------------------------------> wx.ListCtrl
sLCtrlColI = [50, 150]
#endregion ------------------------------------------------------------> Sizes
#endregion --------------------------------------> NON-CONFIGURABLE PARAMETERS


#region ---------------------------------------------> CONFIGURABLE PARAMETERS
#------------------------------> These must be dictionaries to save/load from
#------------------------------> configuration file
#region ------------------> Fonts. Set from UMSAP.py, requires a wx.App object
font = {
}
#endregion ---------------> Fonts. Set from UMSAP.py, requires a wx.App object


#region -----------------------------------------------------> General options
general = { # General options
    'checkUpdate'  : True, # True Check, False No check
# #     'DPI'          : 100,  # DPI for plot images
# #     'MatPlotMargin': 0.025 # Margin for the axes range
}
#endregion --------------------------------------------------> General options


#region --------------------------------------------------------------> Colors
color = { # Colors for the app
    'Zebra' : '#ffe6e6',
# #     'Main' : [ # Lighter colors of the fragments and bands 
# # 		'#ff5ce9', '#5047ff', '#ffa859', '#85ff8c', '#78dbff',
# # 	],
# #     'RecProt' : 'gray',
# #     'NatProt' : '#c94c4c',
# #     nuCorrA : { # Color for plot in Correlation Analysis
# #         'CMAP' : { # CMAP colors and interval
# #             'N' : 128,
# #             'c1': [255, 0, 0],
# #             'c2': [255, 255, 255],
# #             'c3': [0, 0, 255],
# #             'NA': '#90EE90',
# #         },
# #     },
# #     nwProtProf : {
# #         'Vol'   : ['#ff3333', '#d3d3d3', '#3333ff'],
# #         'VolSel': '#6ac653',
# #         'FCAll' : '#d3d3d3',
# #     },
# #     nwLimProt : {
# #         'Spot' : [
# #             '#ffef96', '#92a8d1', '#b1cbbb', '#eea29a', '#b0aac0',
# #             '#f4a688', '#d9ecd0', '#b7d7e8', '#fbefcc', '#a2836e', 
# #         ],
# #     },
}
#endregion -----------------------------------------------------------> Colors
#endregion ------------------------------------------> CONFIGURABLE PARAMETERS
