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
    development:bool = True # Development (True) or Production (False)
    #------------------------------>
    version:str      = '2.2.1 (beta)' # String to write in the output files
    software:str     = 'UMSAP' # Software short name
    softwareF:str    = 'Utilities for Mass Spectrometry Analysis of Proteins'
    dictVersion:dict = field(default_factory=lambda: { # To write into out files
        'Version': '2.2.1 (beta)',
    })
    #------------------------------>
    os:str   = platform.system() # Current operating system
    cwd:Path = Path(__file__)    # Config file path
    #------------------------------> Name of windows
    nwDef:str = 'Untitled Window'
    #------------------------------> Modules
    nmLimProt:str  = 'Limited Proteolysis'
    nmProtProf:str = 'Proteome Profiling'
    nmTarProt:str  = 'Targeted Proteolysis'
    #------------------------------> Utilities
    nuCorrA:str    = 'Correlation Analysis'
    nuDataPrep:str = 'Data Preparation'
    nuReadF:str    = 'Read UMSAP File'
    #------------------------------> Title Tab
    tDef:str      = 'Default Tab'
    tCorrA:str    = 'CorrA'
    tDataPrep:str = 'DataPrep'
    tLimProt:str  = 'LimProt'
    tProtProf:str = 'ProtProf'
    tTarProt:str  = 'TarProt'
    #------------------------------> Label for menu items
    lmNatSeq:str = 'Native Sequence'
    #------------------------------> Keywords for menu
    kwCheckDP:str      = 'General Tool Check DP'
    kwDupWin:str       = 'General Tool Duplicate Window'
    kwExpData:str      = 'General Tool Export Data'
    kwExpImg:str       = 'GeneralTool Export Image One'
    kwExpImgAll:str    = 'General Tool Export Image'
    kwWinUpdate:str    = 'General Tool Update Result Window'
    kwZoomReset:str    = 'GeneralTool Reset Zoom One'
    kwZoomResetAll:str = 'General Tool Reset Zoom All'
    #------------------------------> Files
    fConfig:Path = Path.home() / '.umsap_config.json'
    #------------------------------> Sizes
    sWinFull:tuple[int,int] = (990, 775) # Full size window
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
    #------------------------------> Fonts
    fSeqAlign:Union[wx.Font, str]              = ''
    fTreeItem:Union[wx.Font, str]              = ''
    fTreeItemDataFile:Union[wx.Font, str]      = ''
    fTreeItemDataFileFalse:Union[wx.Font, str] = ''
    #------------------------------>
    # User configuration file is Ok
    confUserFile:bool = True
    # Exception thrown when reading conf file
    confUserFileException:Optional[Exception] = None
    # List of wrong options in the file
    confUserWrongOptions:list  = field(default_factory=lambda: [])
    #------------------------------> User Configurable Options
    checkUpdate:bool    = True  # True Check, False No check
    DPI:int             = 100   # DPI for plot images
    MatPlotMargin:float = 0.025 # Margin for the axes range
    #------------------------------> Converter for user options
    converter:dict = field(default_factory=lambda: {
        'checkUpdate': bool,
        'DPI': int,
        'MatPlotMargin': float,
    })
    #------------------------------> Options for post_init
    deltaWin:int = field(init=False)
    toolMenuIdx:int = field(init=False)
    #endregion ------------------------------------------------------> Options

    #region ---------------------------------------------------> Class Methods
    def __post_init__(self):
        """ """
        if self.os == 'Darwin':
            self.deltaWin    = 23 # Horizontal space between top of windows
            self.toolMenuIdx = 2  # Tool place location
        elif self.os == 'Window':
            self.deltaWin    = 20
            self.toolMenuIdx = 2
        else:
            self.deltaWin    = 20
            self.toolMenuIdx = 3
    #endregion ------------------------------------------------> Class Methods
#---
#endregion ----------------------------------------------------> Configuration
