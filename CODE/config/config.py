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
from typing import Literal, TYPE_CHECKING

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
    root = cwd.parent.parent
    res = root / 'Resources'
    #------------------------------> Index of the Tool Menu in the MenuBar
    toolsMenuIdx = 2
    #------------------------------> Statusbar split size
    if development:
        sbFieldSize = [-1, 350]
    else:
        sbFieldSize = [-1, 300]
    #------------------------------> Key for shortcuts
    copyShortCut = 'Cmd'
elif cOS == 'Windows':
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
    #------------------------------> Key for shortcuts
    copyShortCut = 'Ctrl'
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
    #------------------------------> Key for shortcuts
    copyShortCut = 'Ctrl'
#endregion ------------------------------------- Platform Dependent Parameters

#region -------------------------------------------------------------> Windows
#------------------------------> Reference to main window
winMain  = None
#------------------------------> Number of windows for screen positioning
# Keys: Windows ID - Values: Total number of opened windows, except conf win
winNumber = {}
#endregion ----------------------------------------------------------> Windows

#region ---------------------------------------------------------------> Names
name = { # Unique names for menus, windows, tabs, panes, files, etc
    #------------------------------> Main windows
    'MainW'       : 'MainW',
    #------------------------------> Dialogs
    'CheckUpdateResDialog': 'CheckUpdateResDialog',
    #------------------------------> Tab for notebook windows
    'StartTab'   : 'StartTab',
    'CorrATab'   : 'CorrATab',
    #------------------------------> Individual Panes
    'CorrAPane': 'CorrAPane',
    #------------------------------> Menu
    'ModuleMenu' : 'ModuleMenu',
    'UtilityMenu': 'UtilityMenu',
    #------------------------------> Files
    
}

nMLimProt  = 'Limited Proteolysis'
nMTarProt  = 'Targeted Proteolysis'
nMProtProf = 'Proteome Profiling'

nUCorrA = 'Correlation Analysis'
nUReadF = 'Read UMSAP File'
#endregion ------------------------------------------------------------> Names

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
fnInitial = "{}-Initial-Data.txt"
fnNorm    = "{}-Normalized-Data.txt"
#endregion ---------------------------------------------------> Path and Files

#region ------------------------------------------------------------------ URL
#------------------------------> www.umsap.nl
urlHome      = 'https://www.umsap.nl'
urlUpdate    = f"{urlHome}/page/release-notes"
urlTutorial  = f"{urlHome}/tutorial/2-1-0"
urlCorrAPane = f"{urlTutorial}/correlation-analysis"

#endregion --------------------------------------------------------------- URL

#region --------------------------------------------------------------> Labels
#------------------------------> Names
lnPaneConf = 'Configuration Options'
lnPDCorrA  = 'Calculating Correlation Coefficients'
#------------------------------> wx.Button
lBtnRun      = 'Start Analysis'
lBtnDataFile = 'Data File'
lBtnOutFile  = 'Output File'
#------------------------------> wx.ListCtrl
lLCtrlColNameI = ['#', 'Name']
#------------------------------> wx.StaticBox
lSbFile   = 'Files && Folders'
lSbValue  = 'User-defined values'
lSbColumn = 'Column numbers'
#------------------------------> wx.Statictext
lStColIFile = "Columns in the {}"
#------------------------------> wx.ComboBox or wx.CheckBox
lCbFileAppend = 'Append new data to selected output file'
lCbNormMethod = 'Normalization Method'
lCbCorrMethod = 'Correlation Method'
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
#endregion ------------------------------------------------------------> Hints

#region ------------------------------------------------------------> Tooltips
#------------------------------> wx.Button
ttBtnDataFile = f"Select the {lBtnDataFile}."
ttBtnOutFile  = f"Select the {lBtnOutFile}."
ttBtnHelp     = f"Read online tutorial at {urlHome}."
ttBtnClearAll = f"Clear all user input."
ttBtnRun      = f"Start the analysis."
#------------------------------> wx.StaticText
ttStNorm = f"Select the {lCbNormMethod}."
ttStCorr = f"Select the {lCbCorrMethod}."
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
oNormMethod = ['', 'None', 'Log2']
oCorrMethod = ['', 'Pearson', 'Kendall', 'Spearman']
#endregion ----------------------------------------------------------> Options

#region ------------------------------------------------------------> Messages
#------------------------------> Files 
mFileBad = "File: '{}'\ncannot be used as {}."
#------------------------------> Not empty
mNotEmpty = "Please select a value for {}"
#------------------------------> Pandas
mPDDataType    = 'Unexpected data type.'
mPDDataTypeCol = 'The {} contains unexpected data type in columns {}.'
#endregion ---------------------------------------------------------> Messages


#region ---------------------------------------------------------------> Sizes
#------------------------------> Full Windows 
sWinRegular = (900, 620)
#------------------------------> wx.StatusBar Fields
sSbarFieldSizeI = sbFieldSize
#------------------------------> wx.ListCtrl
sLCtrlColI = [50, 150] # e.g when Col Labels are #, Name
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
    nUCorrA : { # Color for plot in Correlation Analysis
        'CMAP' : { # CMAP colors and interval
            'N' : 128,
            'c1': [255, 0, 0],
            'c2': [255, 255, 255],
            'c3': [0, 0, 255],
        },
    },
}
#endregion -----------------------------------------------------------> Colors
#endregion ------------------------------------------> CONFIGURABLE PARAMETERS
