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


"""Configuration for the core module of the app"""


#region -------------------------------------------------------------> Imports
import platform
from dataclasses import dataclass, field
from pathlib     import Path
from typing      import Union, Optional

import wx
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------> Configuration
@dataclass
class Configuration():
    """Configuration for the core module"""
    #region ---------------------------------------------------------> Options
    #------------------------------> Options for post_init
    deltaWin:int     = field(init=False)                                        # Command to open files
    res:Path         = field(init=False)                                        # Key for shortcuts
    root:Path        = field(init=False)                                        # Horizontal space between top of windows
    toolMenuIdx:int  = field(init=False)                                        # Path to the Resources folder
    commOpen:str     = field(init=False)                                        # Root folder
    copyShortCut:str = field(init=False)                                        # Tool place location
    #------------------------------>
    development:bool = True                                                     # Development (True) or Production (False)
    #------------------------------>
    version:str      = '2.2.1 (beta)'                                           # String to write in the output files
    software:str     = 'UMSAP'                                                  # Software short name
    softwareF:str    = 'Utilities for Mass Spectrometry Analysis of Proteins'   # Software full name
    dictVersion:dict = field(default_factory=lambda: {                          # To write into output files
        'Version': '2.2.1 (beta)',
    })
    #------------------------------>
    os:str   = platform.system()                                                # Current operating system
    cwd:Path = Path(__file__)                                                   # Config file path
    #------------------------------>
    winNumber:dict = field(default_factory=lambda: {})                          # Keys: Windows ID - Values: Total number of opened windows, except conf win
    #------------------------------> Name of Windows
    nwDef:str = 'Untitled Window'
    #------------------------------> Label for Menu Items
    lmNatSeq:str = 'Native Sequence'
    #------------------------------> Keywords for Menu
    kwCheckDP:str      = 'General Tool Check DP'
    kwDupWin:str       = 'General Tool Duplicate Window'
    kwExpData:str      = 'General Tool Export Data'
    kwExpImg:str       = 'General Tool Export Image One'
    kwExpImgAll:str    = 'General Tool Export Image'
    kwWinUpdate:str    = 'General Tool Update Result Window'
    kwZoomReset:str    = 'General Tool Reset Zoom One'
    kwZoomResetAll:str = 'General Tool Reset Zoom All'
    #------------------------------> Files
    fConfig:Path = Path.home() / '.umsap_config.json'
    #------------------------------> Sizes
    sWinFull:tuple[int,int] = (990, 775)                                        # Full size window
    #------------------------------> Extensions
    #--> For wx.Dialogs
    elData:str         = 'txt files (*.txt)|*.txt'
    elUMSAP:str        = 'UMSAP files (*.umsap)|*.umsap'
    elPDB:str          = 'PDB files (*.pdb)|*.pdb'
    elPDF:str          = 'PDF files (*.pdf)|*.pdf'
    elSeq:str          = ('Text files (*.txt)|*.txt|'
                          'Fasta files (*.fasta)|*.fasta')
    elMatPlotSaveI:str = ('Portable Document File (*.pdf)|*.pdf|'
                          'Portable Network Graphic (*.png)|*.png|'
                          'Scalable Vector Graphic (*.svg)|*.svg|'
                          'Tagged Image File (*.tif)|*.tif')
    #-->  File extensions. First item is default
    esData:list  = field(default_factory=lambda: ['.txt'])
    esPDB:list   = field(default_factory=lambda: ['.pdb'])
    esPDF:list   = field(default_factory=lambda: ['.pdf'])
    esSeq:list   = field(default_factory=lambda: ['.txt', '.fasta'])
    esUMSAP:list = field(default_factory=lambda: ['.umsap'])
    #------------------------------> Messages
    mFileSelUMSAP:str = 'Select the UMSAP File'
    #------------------------------> URLs
    urlHome     = 'https://www.umsap.nl'
    urlUpdate   = f"{urlHome}/page/release-notes"
    urlTutorial = f"{urlHome}/tutorial/2-2-X"
    #------------------------------> Fonts
    fSeqAlign:Union[wx.Font, str]              = ''
    fTreeItem:Union[wx.Font, str]              = ''
    fTreeItemDataFile:Union[wx.Font, str]      = ''
    fTreeItemDataFileFalse:Union[wx.Font, str] = ''
    #------------------------------>
    confUserFile:bool = True                                                    # User configuration file is Ok
    confUserFileException:Optional[Exception] = None                            # Exception thrown when reading conf file
    confUserWrongOptions:list = field(default_factory=lambda: [])               # List of wrong options in the file
    confList:list = field(default_factory=lambda: ['core'])                     # Config modules with user configurable options
    #------------------------------> User Configurable Options
    checkUpdate:bool    = True                                                  # True Check, False No check
    DPI:int             = 100                                                   # DPI for plot images
    MatPlotMargin:float = 0.025                                                 # Margin for the axes range
    #------------------------------> Converter for user options
    converter:dict = field(default_factory=lambda: {
        'checkUpdate'  : bool,
        'DPI'          : int,
        'MatPlotMargin': float,
    })
    #endregion ------------------------------------------------------> Options

    #region ---------------------------------------------------> Class Methods
    def __post_init__(self):
        """ """
        #------------------------------> Platform dependent parameters
        if self.os == 'Darwin':
            self.commOpen     = 'open'
            self.copyShortCut = 'Cmd'
            self.deltaWin     = 23
            self.root         = self.cwd.parent.parent.parent
            self.res          = self.root / 'Resources'
            self.toolMenuIdx  = 2
        elif self.os == 'Window':
            self.commOpen     = 'start'
            self.copyShortCut = 'Ctrl'
            self.deltaWin     = 20
            self.toolMenuIdx  = 2
            if self.development:
                self.root = self.cwd.parent.parent.parent
                self.res  = self.root / 'Resources'
            else:
                self.root = self.cwd.parent.parent
                self.res  = self.root / 'RESOURCES/'
        else:
            self.commOpen     = 'xdg-open'
            self.copyShortCut = 'Ctrl'
            self.deltaWin     = 20
            self.root         = self.cwd.parent
            self.res          = self.root / 'Resources'
            self.toolMenuIdx  = 3
        #------------------------------> Relevant Paths
        self.pImages = self.res / 'IMAGES'                                      # Images folder
        #------------------------------> Files
        self.fImgAbout  = self.pImages / 'ABOUT/p97-2-about.png'
        self.fImgIcon   = self.pImages / 'DIALOGUE/dlg.png'
        self.fImgStart  = self.pImages / 'MAIN-WINDOW/p97-2.png'
        self.fManual    = self.res / 'MANUAL/manual.pdf'
        self.fConfigDef = self.res / 'CONFIG/config_def.json'
    #endregion ------------------------------------------------> Class Methods
#---
#endregion ----------------------------------------------------> Configuration
