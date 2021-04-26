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
    #------------------------------> Individual Panes
    
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

#region ------------------------------------------------------> Path and Files
#------------------------------> Relevant paths
pImages = res / 'IMAGES' # Images folder
#------------------------------> Location & names of important files
fImgStart = pImages / 'MAIN-WINDOW/p97-2.png'
fImgIcon  = pImages / 'DIALOGUE'/'dlg.png'

#endregion ---------------------------------------------------> Path and Files

#region --------------------------------------------------------------> Labels
#------------------------------> Titles 
lTabStart = 'Start'
#endregion -----------------------------------------------------------> Labels

#region ---------------------------------------------------------------> Sizes
#------------------------------> Full Windows 
sWinRegular = (900, 620)
#------------------------------> wx.StatusBar Fields
sSbarFieldSizeI = sbFieldSize
#endregion ------------------------------------------------------------> Sizes

#region ------------------------------------------------------------------ URL
#------------------------------> www.umsap.nl
urlHome   = 'https://www.umsap.nl'
urlUpdate = f"{urlHome}/page/release-notes"
#endregion --------------------------------------------------------------- URL
#endregion --------------------------------------> NON-CONFIGURABLE PARAMETERS


#region ---------------------------------------------> CONFIGURABLE PARAMETERS
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




#endregion ------------------------------------------> CONFIGURABLE PARAMETERS
