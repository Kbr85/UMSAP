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
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import data.file as file
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

# obj: Optional['file.UMSAPFile'] = None # To reload UMSAP file

typeCheck = TYPE_CHECKING
#endregion -----------------------------------------------> General parameters


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
#     sbPlot2Fields = [-1, 115]
#     sbPlot3Fields = [90, -1, 115] 
    #------------------------------> Key for shortcuts
    copyShortCut = 'Cmd'
#     #------------------------------> Delta space between consecutive windows
#     deltaWin = 23
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
#     sbPlot = [-1, 115]
    #------------------------------> Key for shortcuts
    copyShortCut = 'Ctrl'
#     #------------------------------> Delta space between consecutive windows
#     deltaWin = 20
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
#     sbPlot = [-1, 115]
    #------------------------------> Key for shortcuts
    copyShortCut = 'Ctrl'
#     #------------------------------> Delta space between consecutive windows
#     deltaWin = 20
#endregion ------------------------------------- Platform Dependent Parameters


#region -------------------------------------------------------------> Windows
# #------------------------------> Reference to main window
winMain = None
#------------------------------> Number of windows for screen positioning
# Keys: Windows ID - Values: Total number of opened windows, except conf win
winNumber = {}
# #------------------------------> Track open umsap files
# # Keys: UMSAP File path - Values: Reference to control window
# winUMSAP = {}
#endregion ----------------------------------------------------------> Windows


#region ---------------------------------------------------------------> Names
# #------------------------------> Default name
nDefName = 'Default name'
# #------------------------------> Windows
nwMain          = 'MainW'
# nwUMSAPControl  = 'UMSAPControl'
# nwCorrAPlot     = 'CorrAPlot'
# nwProtProf      = 'ProtProfPlot'
# nwLimProt       = 'LimProtPlot'
# nwCheckDataPrep = 'CheckDataPrep'
#------------------------------> Dialogs
ndCheckUpdateResDialog = 'CheckUpdateResDialog'
# ndResControlExp        = 'ResControlExp'
# ndFilterRemoveAny      = 'Remove Filters'
# #------------------------------> Tab for notebook windows
ntStart    = 'StartTab'
ntDataPrep = "DataPrepTab"
ntCorrA    = 'CorrATab'
ntLimProt  = 'LimProtTab'
ntProtProf = 'ProtProfTab'
ntTarProt  = 'TarProtTab'
#------------------------------> Individual Panes
# npListCtrlSearchPlot    = 'ListCtrlSearchPlot'
npCorrA                 = 'CorrAPane'
npDataPrep              = "DataPrepPane"
# npLimProt               = "LimProtPane"
npProtProf              = 'ProtProfPane'
# npResControlExp         = 'ResControlExpPane'
# npResControlExpProtProf = 'ResControlExpPaneProtProf'
# npResControlExpLimProt  = 'ResControlExpPaneLimProt'
# #------------------------------> Menu
# nMenModule  = 'ModuleMenu'
# nMenUtility = 'UtilityMenu'
# nMenTool    = 'ToolMenu'
# #------------------------------> Files
# nfUMSAP = 'UMSAPFile'
# #------------------------------> Modules
nmLimProt  = 'Limited Proteolysis'
nmTarProt  = 'Targeted Proteolysis'
nmProtProf = 'Proteome Profiling'
# #------------------------------> Utilities
nuDataPrep = "Data Preparation"
nuCorrA    = 'Correlation Analysis'
nuReadF    = 'Read UMSAP File'
#endregion ------------------------------------------------------------> Names


#region --------------------------------------------------------------> Titles
# #------------------------------> Default names
tdW = "Untitled Window"
tdT = "Tab"
tdP = 'Pane'
#------------------------------> 
t = {
    #------------------------------> Windows
    nwMain : "Analysis Setup",
    #------------------------------> Dialogs
    ndCheckUpdateResDialog: "Check for Updates",
#     ndResControlExp       : 'Results - Control Experiments',
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
# elSeq          = (
#     "Text files (*.txt)|*.txt|"
#     "Fasta files (*.fasta)|*.fasta"
# )
elUMSAP        = 'UMSAP files (*.umsap)|*.umsap'
# elMatPlotSaveI = (
#     "Portable Document File (*.pdf)|*.pdf|"
#     "Portable Network Graphic (*.png)|*.png|"
#     "Scalable Vector Graphic (*.svg)|*.svg|"
#     "Tagged Image File (*.tif)|*.tif"
# )

# #------------------------------> File extensions. First item is default
esData  = ['.txt']
# esSeq   = ['.txt', '.fasta']
esUMSAP = ['.umsap']
#endregion -------------------------------------------------------- Extensions


#region ------------------------------------------------------> Path and Files
#------------------------------> Relevant paths
pImages = res / 'IMAGES' # Images folder
#------------------------------> Location & names of important files
fImgStart = pImages / 'MAIN-WINDOW/p97-2.png'
fImgIcon  = pImages / 'DIALOGUE'/'dlg.png'
#------------------------------> Names
fnInitial    = "{}-Initial-Data-{}.txt"
fnFloat      = "{}-Floated-Data-{}.txt"
# fnTargetProt = "{}-Target-Protein-Data-{}.txt"
fnExclude    = "{}-After-Excluding-Data-{}.txt"
fnScore      = "{}-Score-Filtered-Data-{}.txt"
fnTrans      = "{}-Transformed-Data-{}.txt"
fnNorm       = "{}-Normalized-Data-{}.txt"
fnImp        = "{}-Imputed-Data-{}.txt"
fnDataSteps  = 'Steps_Data_Files'
fnDataInit   = 'Input_Data_Files'
fnMainDataCorrA = '{}-CorrelationCoefficients-Data-{}.txt'
#endregion ---------------------------------------------------> Path and Files


#region ------------------------------------------------------------------ URL
#------------------------------> www.umsap.nl
urlHome     = 'https://www.umsap.nl'
urlUpdate   = f"{urlHome}/page/release-notes"
urlTutorial = f"{urlHome}/tutorial/2-1-0"
urlCorrA    = f"{urlTutorial}/correlation-analysis"
# urlLimProt  = f"{urlTutorial}/limited-proteolysis"
urlProtProf = f"{urlTutorial}/proteome-profiling"
urlDataPrep = f"{urlTutorial}/data-preparation"
#endregion --------------------------------------------------------------- URL


#region --------------------------------------------------------------> Labels
#------------------------------> Names
lnPaneConf = 'Configuration Options'
lnListPane = 'Data File Content'
lnPDCorrA  = 'Calculating Correlation Coefficients'
# #------------------------------> wx.Button
lBtnRun         = 'Start Analysis'
lBtnDataFile    = 'Data'
# lBtnOutFile     = 'Output File'
lBtnUFile       = 'UMSAP'
# lBtnSeqFile     = 'Sequences'
lBtnTypeResCtrl = 'Type Values'
lBtnAddCol = 'Add columns'
# #------------------------------> wx.ListCtrl
lLCtrlColNameI = ['#', 'Name']
# #------------------------------> wx.StaticBox
lSbFile         = 'Files && Folders'
lSbData         = 'Data preparation'
lSbValue        = 'User-defined values'
lSbColumn       = 'Column numbers'
lStProtProfCond = 'Conditions'
lStProtProfRP   = 'Relevant Points'
# lStLimProtLane  = 'Lanes'
# lStLimProtBand  = 'Bands' 
lStCtrlName     = 'Name'
lStCtrlType     = 'Type'  
#------------------------------> adv.HyperlinkCtrl
lHlcReadRelNotes = 'Read the Release Notes.'
#------------------------------> wx.Statictext
lStUpdateCheckLast = 'You are using the latest version of UMSAP.'
lStUpdateCheckAvail = ('UMSAP {} is already available.\nYou are currently '
    'using UMSAP {}.')
# lStSeqFile      = 'Sequences'
lStId           = 'Analysis ID'
lStAlpha        = 'Significance Level'
lStColIFile     = "Columns in the {}"
lStScoreVal     = 'Score Value'
# lStSeqLength    = 'Sequence Length'
# lStTargetProt   = "Target Protein"
lStDetectedProt = 'Detected Proteins'
# lStSeqCol       = 'Sequences'
lStScoreCol     = 'Score'
lStResultCtrl   = 'Results - Control experiments'
lStColAnalysis = 'Columns to Analyse'
lStExcludeRow = 'Exclude Rows'
lStExcludeProt = 'Exclude Proteins'
lStColAnalysis = 'Columns to Consider'
lStGeneName    = 'Gene Names'
# #------------------------------> wx.ComboBox or wx.CheckBox
# lCbFileAppend  = 'Append new data to selected output file'
lCbCeroTreat   = 'Treat 0s as missing values'
lCbCeroTreatD  = '0s Missing'
lCbTransMethod = 'Transformation'
lCbNormMethod  = 'Normalization'
lCbImputation  = 'Imputation'
lCbCorrMethod  = 'Correlation Method'
lCbCorrectP    = 'P Correction'
lCbSample      = 'Samples'
lCbIntensity   = 'Intensities'
#------------------------------> Progress Dialog
lPdCheck    = 'Checking user input: '
lPdPrepare  = 'Preparing analysis: '
lPdReadFile = 'Reading input files: '
lPdRun      = 'Running analysis: '
lPdWrite    = 'Writing output: '
lPdLoad     = 'Loading output file'
lPdError    = 'Fatal Error'
lPdDone     = 'All Done'
lPdEllapsed = 'Ellapsed time: '
#endregion -----------------------------------------------------------> Labels


#region ---------------------------------------------------------------> Hints
hTcDataFile = f"Path to the {lBtnDataFile} file"
# hTcOutFile  = f"Path to the {lBtnOutFile} file"
hTcUFile    = f"Path to the {lBtnUFile} file"
# hTcSeqFile  = f"Path to the {lBtnSeqFile} file"
hTcId       = 'e.g. HIV inhibitor'
#endregion ------------------------------------------------------------> Hints


#region ------------------------------------------------------------> Tooltips
#------------------------------> wx.Button
ttBtnDataPrep = f'Start the utility {nuDataPrep}'
ttBtnCorrA    = f'Start the utility {nuCorrA}'
ttBtnLimProt  = f'Start the module {nmLimProt}'
ttBtnTarProt  = f'Start the module {nmTarProt}'
ttBtnProtProf = f'Start the module {nmProtProf}'
ttBtnDataFile = f'Select the {lBtnDataFile}.'
# ttBtnOutFile  = f"Select the {lBtnOutFile}."
ttBtnUFile  = f'Select the {lBtnUFile}.'
ttBtnHelpDef  = f'Read online tutorial at {urlHome}.'
ttBtnHelp     = 'Read tutorial at {}.'
ttBtnClearAll = f'Clear all user input.'
ttBtnRun      = f'Start the analysis.'
ttBtnAddCol = (
    f'Add selected Columns in the Data File to the list of Columns '
    f'to Analyse. New columns will be added after the last '
    f'selected element in Columns to analyse. Duplicate columns '
    f'are discarded.')
ttBtnTypeRes = 'Type the column numbers in a helper window.'
# #------------------------------> wx.StaticText
ttStId = ('Short text to id the analysis. Do not include the date of the '
    'analysis.')
ttStCeroTreatment = (f'Cero values in the {lBtnDataFile} File will be treated '
    f'as missing values when this option is selected or as real values when '
    f'the option is not selected.')
ttStTrans = f'Select the Data {lCbTransMethod} method.'
ttStNorm = f'Select the Data {lCbNormMethod} method.'
ttStImputation = f'Select the Data {lCbImputation} method.'
ttStAlpha = 'Significance level for the statistical analysis.\ne.g. 0.05'
ttStCorr = f'Select the {lCbCorrMethod}.'
ttStScoreVal = f'Set the minimum acceptable Score value.\ne.g. -4'
ttStPCorrection = "Select the p correction method."
# ttStMedianCorr = "Select whether to apply a median correction."
ttStDetectedProtL = (
    'Set the column number containing the detected proteins.\ne.g. 7')
ttStScore = 'Set the column number containing the Score values.\ne.g. 4'
ttStGenName = "Set the column number containing the gene names.\ne.g. 3"
ttStExcludeProt = (
    "Set the column number containing the data used to exclude proteins."
    "\ne.g. 8 10-12")
ttStExcludeRow = (
    'Set the column numbers containing the data used to exclude rows.'
    '\ne.g. 8 10-12')
# ttStControlN = "Name or ID of the control experiment.\ne.g. MyControl."
ttStSample = (f"Specify if samples are independent or paired.\n"
    f"For example, samples are paired when the same Petri dish is "
    f"used for the control and experiment.")
ttStColAnalysis = ('Columns on which to perform the Data Preparation.\ne.g. '
    '8 10-12')
ttStResult = ('Set the column numbers containing the control and experiment '
    'results.')
ttStRawI = ('Specify if intensities are raw intensity values or are already '
    'expressed as a ratio (SILAC, TMT/iTRAQ).')
# #------------------------------> wx.ListCtrl
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
# oYesNo = {
#     'Empty': '',
#     'Yes'  : 'Yes',
#     'No'   : 'No',
# }
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
# oControlTypeProtProf = {
#     'Empty': '',
#     'OC'   : 'One Control',
#     'OCC'  : 'One Control per Column',
#     'OCR'  : 'One Control per Row',
#     'Ratio': oIntensities['RatioI'],
# }
#endregion ----------------------------------------------------------> Options


#region -----------------------------------------------------> DF Column names
# dfcolProtprofFirstThree = ['Gene', 'Protein', 'Score']
# dfcolProtprofCLevel = ['aveC', 'stdC', 'ave', 'std', 'FC', 'CI', 'FCz']
# dfcolDataCheck = [
#     'Data', 'N', 'NaN', 'Mean', 'Median', 'SD', 'Kurtosis', 'Skewness']
# dfcolLimProtFirstPart = [
#     'Sequence', 'Score', 'Nterm', 'Cterm', 'NtermF', 'CtermF', 'Delta']
# dfcolLimProtCLevel = ['Ptost']
#endregion --------------------------------------------------> DF Column names


#region -----------------------------------------------------> Important Lists
ltDPKeys = ['dfS', 'dfT', 'dfN', 'dfIm']
#endregion --------------------------------------------------> Important Lists


#region ------------------------------------------------------------> Messages
#region -------------------------------------------------------------> Other 
#------------------------------> Update Check Failed
mCheckUpdateFailed = 'Check for Updates failed. Please try again later.'
# #------------------------------> Unexpected Error
# mUnexpectedError = 'An uexpected error was encountered.'
# #------------------------------> Not empty
# mNotEmpty = "Please select a value for {}."
# #------------------------------> Sequences related errors
# mSeqPeptNotFound = ("The peptide '{}' was not found in the sequence of the {} "
#     "protein.")
#endregion ----------------------------------------------------------> Other

#region ------------------------------------------------------------> Values
mOneRNumText = "Only one real number can be accepted here."
mOneZPlusNumText = "Only a non-negative integer can be accepted here."
# mOneZNumText = "Only one positive integer can be accepted here."
mOne01NumText = "Only one number between 0 and 1 can be accepted here"
mNZPlusNumText = (
    "Only a list of unique non-negative integers can be accepted here.")
# mNumROne = "Only one number can be accepted in {}."
# mNumZPlusOne = "Only one non-negative integer can be accepted in {}."
# mListNumN0L = (
#     "Only a list of unique non-negative integers can be accepted in {}.")
mColNumbers = f'Values in section {lSbColumn} must be unique.'
# mAlphaRange = "Only one number between 0 and 1 can be accepted in {}."
#endregion ---------------------------------------------------------> Values

#region ---------------------------------------------------------------> Files
mFileUMSAPDict = ('It was not possible to create the dictionary with the '
    'UMSAP data.')
mFileUMSAP = ('It was not possible to write the results of the analysis to '
    'the selected UMSAP file.')
mFiledataSteps = ('It was not possible to create the files with the data for '
    'the intermediate steps of the analysis.')
mFileDataExport = 'It was not possible to write the data to the selected file.'
# mFileSelector = f"It was not possible to show the file selecting dialog."
mFileRead = 'An error occured when reading file:\n{}'
# mFileColNum = (
#     "In addition, the values cannot be bigger than the total number of columns "
#     "in the {}.")
# mUMSAPFile = 'Select the UMSAP File'
#endregion ------------------------------------------------------------> Files

#region ------------------------------------------------------------> Pandas
mPDGetInitCol = ('It was not possible to extract the selected columns {} from '
    'the selected {}:.\n{}')
mPDDataTargetProt = ('Selection of Target Protein failed.\nTarget Protein: {} '
    'Detected Proteins column: {}.')
mPDDataExclude = 'Data Exclusion failed.\nColumns used for data exclusion: {}.'
mPDDataScore = ('Data Filtering by Score value failed.\nColumns used for data '
    'filtering by Score value: {}.')
# mPDDataType       = 'Unexpected data type.'
mPDDataTypeCol    = 'The {} contains unexpected data type in columns {}.'
mPDDataTran       = 'Data Transformation failed.'
mPDDataNorm       = 'Data Normalization failed.'
mPDDataImputation = 'Data Imputation failed.'
#endregion ---------------------------------------------------------> Pandas
 
#region ----------------------------------------------------> For CheckInput
mRowsInLCtrl = 'There must be at least two items in {}.'
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
# mResCtrlWin = ("Value '{}' cannot be accepted as input.\n"f"{mNZPlusNumText}")
#endregion -------------------------------------------------> For CheckInput
#endregion ---------------------------------------------------------> Messages


#region ---------------------------------------------------------------> Sizes
#------------------------------> Full Windows 
sWinRegular = (990, 775)
# #------------------------------> Plot Window
# sWinPlot = (560, 560)
# sWinModPlot = (1100, 625)
#------------------------------> wx.StatusBar Fields
sSbarFieldSizeI = sbFieldSize
#------------------------------> wx.ListCtrl
sLCtrlColI = [50, 150] # e.g when Col Labels are #, Name
# #------------------------------> wx.TextCtrl
sTc = (50, 22)
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
#     'DPI'          : 100,  # DPI for plot images
#     'MatPlotMargin': 0.025 # Margin for the axes range
}
#endregion --------------------------------------------------> General options


#region --------------------------------------------------------------> Colors
color = { # Colors for the app
    'Zebra' : '#ffe6e6',
#     'Main' : [ # Lighter colors of the fragments and bands 
# 		'#ff5ce9', '#5047ff', '#ffa859', '#85ff8c', '#78dbff',
# 	],
#     'RecProt' : 'gray',
#     'NatProt' : '#c94c4c',
#     nuCorrA : { # Color for plot in Correlation Analysis
#         'CMAP' : { # CMAP colors and interval
#             'N' : 128,
#             'c1': [255, 0, 0],
#             'c2': [255, 255, 255],
#             'c3': [0, 0, 255],
#             'NA': '#90EE90',
#         },
#     },
#     nwProtProf : {
#         'Vol'   : ['#ff3333', '#d3d3d3', '#3333ff'],
#         'VolSel': '#6ac653',
#         'FCAll' : '#d3d3d3',
#     },
#     nwLimProt : {
#         'Spot' : [
#             '#ffef96', '#92a8d1', '#b1cbbb', '#eea29a', '#b0aac0',
#             '#f4a688', '#d9ecd0', '#b7d7e8', '#fbefcc', '#a2836e', 
#         ],
#     },
}
#endregion -----------------------------------------------------------> Colors
#endregion ------------------------------------------> CONFIGURABLE PARAMETERS
