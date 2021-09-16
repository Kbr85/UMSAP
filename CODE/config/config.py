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


"""Configuration parameters of the app """


#region -------------------------------------------------------------> Imports
import platform
from pathlib import Path
from typing import TYPE_CHECKING

#endregion ----------------------------------------------------------> Imports


#region -----------------------------------------> NON-CONFIGURABLE PARAMETERS
#region --------------------------------------------------> General parameters
development = True # Track state, development (True) or production (False)

version     = '2.2.0 (beta)' # String to write in the output files
software    = 'UMSAP'
softwareF   = 'Utilities for Mass Spectrometry Analysis of Proteins'
dictVersion = { # dict for directly write into output files
    'Version': version,
}

cOS = platform.system() # Current operating system
cwd = Path(__file__)

typeCheck = TYPE_CHECKING
#endregion -----------------------------------------------> General parameters


#region ---------------------------------------- Platform Dependent Parameters
# There are some that must be defined in other sections
if cOS == 'Darwin':
    #------------------------------> Root & Resources Folder
    if development:
        root = cwd.parent.parent.parent
    else:
        root = cwd.parent.parent
    res = root / 'Resources'
    #------------------------------> Index of the Tool Menu in the MenuBar
    toolsMenuIdx = 2
    #------------------------------> Statusbar split size
    if development:
        sbFieldSize = [-1, 350]
    else:
        sbFieldSize = [-1, 300]
    sbPlot = [-1, 115]
    #------------------------------> Key for shortcuts
    copyShortCut = 'Cmd'
    #------------------------------> Delta space between consecutive windows
    deltaWin = 23
elif cOS == 'Windows':
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
    sbPlot = [-1, 115]
    #------------------------------> Key for shortcuts
    copyShortCut = 'Ctrl'
    #------------------------------> Delta space between consecutive windows
    deltaWin = 20
elif cOS == 'Linux':
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
    sbPlot = [-1, 115]
    #------------------------------> Key for shortcuts
    copyShortCut = 'Ctrl'
    #------------------------------> Delta space between consecutive windows
    deltaWin = 20
#endregion ------------------------------------- Platform Dependent Parameters


#region -------------------------------------------------------------> Windows
#------------------------------> Reference to main window
winMain  = None
#------------------------------> Number of windows for screen positioning
# Keys: Windows ID - Values: Total number of opened windows, except conf win
winNumber = {}
#------------------------------> Track open umsap files
# Keys: UMSAP File path - Values: Reference to control window
winUMSAP = {}
#endregion ----------------------------------------------------------> Windows


#region ---------------------------------------------------------------> Names
#------------------------------> Default name
nDefName = 'Default name'
#------------------------------> Windows
nwMain         = 'MainW'
nwUMSAPControl = 'UMSAPControl'
nwCorrAPlot    = 'CorrAPlot'
nwProtProf     = 'ProtProfPlot'
#------------------------------> Dialogs
ndCheckUpdateResDialog = 'CheckUpdateResDialog'
ndResControlExp        = 'ResControlExp'
#------------------------------> Tab for notebook windows
ntStart    = 'StartTab'
ntCorrA    = 'CorrATab'
ntProtProf = 'ProtProfTab'
#------------------------------> Individual Panes
npListCtrlSearchPlot    = 'ListCtrlSearchPlot'
npCorrA                 = 'CorrAPane'
npProtProf              = 'ProtProfPane'
npResControlExp         = 'ResControlExpPane'
npResControlExpProtProf = 'ResControlExpPaneProtProf'
#------------------------------> Menu
nMenModule  = 'ModuleMenu'
nMenUtility = 'UtilityMenu'
nMenTool    = 'ToolMenu'
#------------------------------> Files
nfUMSAP = 'UMSAPFile'
#------------------------------> Modules
nmLimProt  = 'Limited Proteolysis'
nmTarProt  = 'Targeted Proteolysis'
nmProtProf = 'Proteome Profiling'
#------------------------------> Utilities
nuDataT = 'Data Transformation'
nuCorrA = 'Correlation Analysis'
nuDataN = 'Data Normalization'
nuReadF = 'Read UMSAP File'
#endregion ------------------------------------------------------------> Names


#region --------------------------------------------------------------> Titles
#------------------------------> Default names
tdW = "Untitled Window"
tdT = "Tab"
tdP = 'Pane'
#------------------------------> 
t = {
    #------------------------------> Windows
    nwMain    : "Analysis Setup",
    #------------------------------> Dialogs
    ndCheckUpdateResDialog : "Check for Updates",
    ndResControlExp : 'Results - Control Experiments',
    #------------------------------> Tabs
    ntStart   : 'Start',
    ntCorrA   : 'CorrA',
    ntProtProf: 'ProtProf',
}
#endregion -----------------------------------------------------------> Titles


#region ----------------------------------------------------------- Extensions
#------------------------------> For wx.Dialogs
elData         = 'txt files (*.txt)|*.txt'
elUMSAP        = 'UMSAP files (*.umsap)|*.umsap'
elMatPlotSaveI = (
    "Portable Document File (*.pdf)|*.pdf|"
    "Portable Network Graphic (*.png)|*.png|"
    "Scalable Vector Graphic (*.svg)|*.svg|"
    "Tagged Image File (*.tif)|*.tif"
)

#------------------------------> File extensions. First item is default
esData  = ['.txt']
esUMSAP = ['.umsap']
#endregion -------------------------------------------------------- Extensions


#region ------------------------------------------------------> Path and Files
#------------------------------> Relevant paths
pImages = res / 'IMAGES' # Images folder
#------------------------------> Location & names of important files
fImgStart = pImages / 'MAIN-WINDOW/p97-2.png'
fImgIcon  = pImages / 'DIALOGUE'/'dlg.png'
#------------------------------> Names
fnInitial   = "{}-Initial-Data.txt"
fnFloat     = "{}-Floated-Data.txt"
fnExclude   = "{}-After-Excluding-Data.txt"
fnScore     = "{}-Score-Filtered-Data.txt"
fnTrans     = "{}-Transformed-Data.txt"
fnNorm      = "{}-Normalized-Data.txt"
fnImp       = "{}-Imputed-Data.txt"
fnDataSteps = 'Steps_Data_Files'
fnDataInit  = 'Input_Data_Files'
#endregion ---------------------------------------------------> Path and Files


#region ------------------------------------------------------------------ URL
#------------------------------> www.umsap.nl
urlHome     = 'https://www.umsap.nl'
urlUpdate   = f"{urlHome}/page/release-notes"
urlTutorial = f"{urlHome}/tutorial/2-1-0"
urlCorrA    = f"{urlTutorial}/correlation-analysis"
urlProtProf = f"{urlTutorial}/proteome-profiling"

#endregion --------------------------------------------------------------- URL


#region --------------------------------------------------------------> Labels
#------------------------------> Names
lnPaneConf = 'Configuration Options'
lnListPane = 'Data File Content'
lnPDCorrA  = 'Calculating Correlation Coefficients'
#------------------------------> wx.Button
lBtnRun      = 'Start Analysis'
lBtnDataFile = 'Data File'
lBtnOutFile  = 'Output File'
lBtnUFile    = 'UMSAP File'
#------------------------------> wx.ListCtrl
lLCtrlColNameI = ['#', 'Name']
#------------------------------> wx.StaticBox
lSbFile         = 'Files && Folders'
lSbData         = 'Data preparation'
lSbValue        = 'User-defined values'
lSbColumn       = 'Column numbers'
lStProtProfCond = 'Conditions'
lStProtProfRP   = 'Relevant Points'
lStCtrlName     = 'Name'
lStCtrlType     = 'Type'  
#------------------------------> wx.Statictext
lStAlpha        = 'Significance level'
lStColIFile     = "Columns in the {}"
lStScoreVal     = 'Score Value'
lStDetectedProt = 'Detected Proteins'
lStScoreCol     = 'Score'
lStColExtract   = 'Columns to Extract'
lStResultCtrl   = 'Results - Control experiments'
#------------------------------> wx.ComboBox or wx.CheckBox
lCbFileAppend  = 'Append new data to selected output file'
lCbTransMethod = 'Transformation'
lCbNormMethod  = 'Normalization'
lCbImputation  = 'Imputation'
lCbCorrMethod  = 'Correlation Method'
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
hTcDataFile = f"Path to the {lBtnDataFile}"
hTcOutFile  = f"Path tot the {lBtnOutFile}"
hTcUFile    = f"Path tot the {lBtnUFile}"
#endregion ------------------------------------------------------------> Hints


#region ------------------------------------------------------------> Tooltips
#------------------------------> wx.Button
ttBtnDataFile = f"Select the {lBtnDataFile}."
ttBtnOutFile  = f"Select the {lBtnOutFile}."
ttBtnUFile  = f"Select the {lBtnUFile}."
ttBtnHelpDef  = f"Read online tutorial at {urlHome}."
ttBtnHelp     = "Read tutorial at {}."
ttBtnClearAll = f"Clear all user input."
ttBtnRun      = f"Start the analysis."
#------------------------------> wx.StaticText
ttStTrans = f"Select the {lCbTransMethod} method."
ttStNorm = f"Select the {lCbNormMethod} method."
ttStImputation = f"Select the {lCbImputation} method."
ttStAlpha = "Significance level for the statistical analysis.\ne.g. 0.05"
ttStCorr = f"Select the {lCbCorrMethod}."
ttStScoreVal = f"Set the minimum acceptable Score value.\ne.g. -4"
ttStPCorrection = "Select the p correction method."
ttStMedianCorr = "Select whether to apply a median correction."
ttStDetectedProtL = (
    f"Set the column number containing the detected proteins.\ne.g. 7")
ttStScore = f"Set the column number containing the Score values.\ne.g. 4"
ttStColExtract = "Set the column numbers to extract from {}.\ne.g. 1-4 7 8"
ttStGenName = "Set the column number containing the gene names.\ne.g. 3"
ttStExcludeProt = (
    "Set the column number containing the protein to exclude.\ne.g. 8 10-12")
#------------------------------> wx.ListCtrl
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
oYesNo = {
    'Empty': '',
    'Yes'  : 'Yes',
    'No'   : 'No',
}
oIntensities = {
    'Empty' : '',
    'RawI'  : 'Raw Intensities',
    'RatioI': 'Ratio of Intensities',
}
oSamples = {
    'Empty': '',
    'IS'   : 'Independent Samples',
    'PS'   : 'Paired Samples',
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
protprofFirstThree = ['Gene', 'Protein', 'Score']
protprofCLevel = ['aveC', 'stdC', 'ave', 'std', 'FC', 'CI', 'FCz']
#endregion --------------------------------------------------> DF Column names


#region ------------------------------------------------------------> Messages
#------------------------------> Files 
mFileSelector = f"It was not possible to show the file selecting dialog."
mFileBad = "File: '{}'\ncannot be used as {}."
mFileRead = 'An error occured when reading file:\n{}'
mFileColNum = (
    "In addition, the values cannot be bigger than the total number of columns "
    "in the {}.")
#------------------------------> Not empty
mNotEmpty = "Please select a value for {}."
#------------------------------> Pandas
mPDDataType       = 'Unexpected data type.'
mPDDataTypeCol    = 'The {} contains unexpected data type in columns {}.'
mPDDataTran       = 'Data Transformation failed.'
mPDDataNorm       = 'Data Normalization failed.'
mPDDataImputation = 'Data Imputation failed.'
#------------------------------> User values
mNumROne = "Only one number can be accepted in {}."
mNumZPlusOne = "Only one non-negative integer can be accepted in {}."
mListNumN0L = (
    "Only a list of unique non-negative integers can be accepted in {}.")
mColNumbers = f"Values in section {lSbColumn} must be unique"+"{}"
mColNumbersNoColExtract = f", excluding {lStColExtract}."
mAlphaRange = "Only one number between 0 and 1 can be accepted in {}."
#endregion ---------------------------------------------------------> Messages


#region ---------------------------------------------------------------> Sizes
#------------------------------> Full Windows 
sWinRegular = (930, 700)
#------------------------------> Plot Window
sWinPlot = (560, 560)
sWinModPlot = (1100, 625)
#------------------------------> wx.StatusBar Fields
sSbarFieldSizeI = sbFieldSize
#------------------------------> wx.ListCtrl
sLCtrlColI = [50, 150] # e.g when Col Labels are #, Name
#------------------------------> wx.TextCtrl
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
    'checkUpdate': True, # True Check, False No check
    'DPI'        : 100,  # DPI for plot images
}
#endregion --------------------------------------------------> General options


#region --------------------------------------------------------------> Colors
color = { # Colors for the app
    'Zebra' : '#ffe6e6',
    'Main' : [ # Lighter colors of the fragments and bands 
		'#ff5ce9', '#5047ff', '#ffa859', '#85ff8c', '#78dbff',
	],
    nuCorrA : { # Color for plot in Correlation Analysis
        'CMAP' : { # CMAP colors and interval
            'N' : 128,
            'c1': [255, 0, 0],
            'c2': [255, 255, 255],
            'c3': [0, 0, 255],
        },
    },
    nwProtProf : {
        'Vol'   : ['#ff3333', '#d3d3d3', '#3333ff'],
        'VolSel': '#6ac653',
        'FCAll' : '#d3d3d3',
    }
}
#endregion -----------------------------------------------------------> Colors
#endregion ------------------------------------------> CONFIGURABLE PARAMETERS
