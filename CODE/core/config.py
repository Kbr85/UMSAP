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
    commOpen:str        = field(init=False)                                     # Root folder
    copyShortCut:str    = field(init=False)                                     # Tool place location
    deltaWin:int        = field(init=False)                                     # Command to open files
    res:Path            = field(init=False)                                     # Key for shortcuts
    root:Path           = field(init=False)                                     # Horizontal space between top of windows
    toolMenuIdx:int     = field(init=False)                                     # Path to the Resources folder
    pImages:Path        = field(init=False)                                     # Path to Images
    fImgAbout:Path      = field(init=False)                                     # Path to File
    fImgIcon:Path       = field(init=False)
    fImgStart:Path      = field(init=False)
    fManual:Path        = field(init=False)
    fConfigDef:Path     = field(init=False)
    #------------------------------> General Options
    development:bool = True                                                     # Development (True) or Production (False)
    software:str     = 'UMSAP'                                                  # Software short name
    softwareF:str    = 'Utilities for Mass Spectrometry Analysis of Proteins'   # Software full name
    version:str      = '2.2.1 (beta)'                                           # String to write in the output files
    dictVersion:dict = field(default_factory=lambda: {                          # To write into output files
        'Version': '2.2.1 (beta)',
    })
    os:str         = platform.system()                                          # Current operating system
    cwd:Path       = Path(__file__)                                             # Config file path
    winNumber:dict = field(default_factory=lambda: {})                          # Keys: Windows ID - Values: Total number of opened windows, except conf win
    dtFormat:str   = '%Y%m%d-%H%M%S'                                            # Date Time format
    #------------------------------> Name & Title
    nwDef:str                = 'Name Default Window'
    ndResControlExp:str      = 'Results & Control Experiments'
    ntDef:str                = 'Name Default Tab'
    npDef:str                = 'Name Default Pane'
    npListCtrlSearchPlot:str = 'ListCtrlSearchPlot'
    npNPlot:str              = 'NPlot'
    tTabDef:str              = 'Tab'
    tPaneConf:str            = 'Configuration Options'
    tListPane:str            = 'Data File Content'
    #------------------------------> Label for Widgets
    lmNatSeq:str        = 'Native Sequence'                                     # lm: Label for wx.MenuItem
    lBtnTypeResCtrl:str = 'Type Values'                                         # lBtn: Label for wx.Button
    lStResultCtrl:str   = 'Results - Control experiments'                       # lSt: Label for wx.StaticText
    lStColAnalysis:str  = 'Columns for Analysis'
    lStScoreVal:str     = 'Score Value'
    lStScoreCol:str     = 'Score'
    lStResultCtrlS:str  = 'Results - Control'
    lStExcludeProt:str  = 'Exclude Proteins'
    lStGeneName:str     = 'Gene Names'
    lStCtrlName:str     = 'Name'
    lStCtrlType:str     = 'Type'
    lCbCorrectP:str     = 'P Correction'                                        # lCb: Label for wx.ComboBox
    lCbSample:str       = 'Samples'
    lPdError:str        = 'Fatal Error'                                         # lPd: Label for Progress Dialog
    #------------------------------> wx.ListCtrl Column names
    lLCtrlColNameI:list[str] = field(default_factory=lambda: ['#', 'Name'])
    #------------------------------> Messages
    mUnexpectedError:str = 'UMSAP encountered an unexpected error.'
    mOptField:str       = '\nThis field is optional.'
    mFileSelUMSAP:str   = 'Select the UMSAP File'
    mFileRead:str       = 'An error occurred when reading file:\n{}'
    mCopyFailedW:str    = "Copy operation failed. Try again."
    mPasteFailedW:str   = "Paste operation failed. Try again."
    mNothing2PasteW:str = "Nothing to paste."
    mLCtrNoCopy:str     = "The elements of this list cannot be copied."
    mLCtrNoChange:str   = "This list cannot be modified."
    mLCtrlNColPaste:str = ("The clipboard content cannot be pasted because the "
                           "number of columns being pasted is different to the "
                           "number of columns in the list.")
    mNZPlusNumText:str  = ("Only a list of unique non-negative integers can be "
                        "accepted here.")
    mColNumbers:str     = ('In addition, each value must be smaller than the '
                           'total number of columns in the Data file.')
    mRangeNumIE:str     = "Invalid range or number: {}"
    mInvalidValue:str   = "'{}' is an invalid value."
    mEmpty:str          = 'The field value cannot be empty.'
    mFileBad:str        = "File: '{}'\ncannot be used as {} file."
    mOptionBad:str      = "Option '{}' cannot be accepted in {}."
    mValueBad:str       = "Value '{}' cannot be accepted in {}.\n"
    mOneRNumText:str    = "Only one real number can be accepted here."
    mRowsInLCtrl:str    = 'There must be at least {} items in {}.'
    mOneRPlusNumText:str = ("Only one number equal or greater than zero can be "
                            "accepted here.")
    mSection:str        = 'Values in section {} must be unique.'
    mNotImplementedFull:str = ('Option {} is not yet implemented. Valid '
                               'options for {} are: {}.')
    mPDDataTargetProt:str = ('Selection of Target Protein failed.\nTarget '
                             'Protein: {} Detected Proteins column: {}.')
    mPDDataExclude:str    = ('Data Exclusion failed.\nColumns used for data '
                             'exclusion: {}.')
    mPDDataScore:str      = ('Data Filtering by Score value failed.\nColumns '
                             'used for data filtering by Score value: {}.')
    mNoDataLeft:str       = ('No data left for analysis after all filters '
                             '(Score, Target Protein, etc) were applied.')
    mColNumber:str        = ('In addition, the value must be smaller than the '
                             'total number of columns in the Data file.')
    mOne01NumText:str = "Only one number between 0 and 1 can be accepted here."
    mOneZPlusNumText:str = "Only a non-negative integer can be accepted here."
    mAllTextFieldEmpty:str = 'All text fields are empty. Nothing will be done.'
    mRepeatColNum:str = 'There are repeated column numbers in the text fields.'
    mCtrlEmpty:str         = 'None of the Control fields can be empty.'
    mRepNum:str    = ('The number of replicates in some experiments does not '
                      'match the number of replicates in the control.')
    mSeqPeptNotFound:str = ("The peptide '{}' was not found in the sequence of "
                            "the {} protein.")
    mOneRPlusNum:str    = f"{mValueBad}{mOneRPlusNumText}"
    mNZPlusNum:str      = f"{mValueBad}{mNZPlusNumText}"
    mNZPlusNumCol:str   = f"{mNZPlusNum} {mColNumbers}"
    mOneRealNum:str     = f"{mValueBad}{mOneRNumText}"
    mOne01Num:str       = f"{mValueBad}{mOne01NumText}"
    mOneZPlusNum:str    = f"{mValueBad}{mOneZPlusNumText}"
    mOneZPlusNumCol:str = f"{mOneZPlusNum} {mColNumber}"
    mResCtrl:str        = (f"{mValueBad} Please use the "
                          f"{lBtnTypeResCtrl} button to provide a "
                          f"correct input.")
    mResCtrlWin:str     = ("Value '{}' cannot be accepted as input.\n"
                          f"{mNZPlusNumText}")
    #------------------------------> Tooltips
    ttSectionRightClick:str = ('The content of the Section can be deleted with '
                               'a right click.')
    ttBtnHelp:str = 'Read tutorial at {}.'
    ttLCtrlCopyNoMod:str = (f"Selected rows can be copied ({copyShortCut}+C) "
                            "but the table cannot be modified.")
    ttLCtrlPasteMod:str = (f"New rows can be pasted ({copyShortCut}+V) after "
                           f"the last selected element and existing ones "
                           f"cut/deleted ({copyShortCut}+X) or copied "
                           f"({copyShortCut}+C).")
    ttStScoreVal:str    = 'Set the minimum acceptable Score value.\ne.g. -4'
    ttStScoreCol:str    = (f'Set the column number containing the '
                           f'{lStScoreVal}.\ne.g. 4')
    ttStGenName:str     = (f'Set the column number containing the '
                           f'{lStGeneName}.\ne.g. 3')
    ttStExcludeProt:str = ("Set the column number containing the data used to "
                           "exclude proteins.\ne.g. 8 10-12")
    ttStCorrectP:str    = 'Select the p correction method.'
    ttStSample:str      = ("Specify if samples are independent or paired.\n"
                           "For example, samples are paired when the same "
                           "Petri dish is used for the control and experiment.")
    #------------------------------> Keywords for Menu
    kwCheckDP:str      = 'General Tool Check DP'
    kwDupWin:str       = 'General Tool Duplicate Window'
    kwExpData:str      = 'General Tool Export Data'
    kwExpImg:str       = 'General Tool Export Image One'
    kwExpImgAll:str    = 'General Tool Export Image'
    kwExpSeq:str       = 'GeneralTool Export Sequence'
    kwWinUpdate:str    = 'General Tool Update Result Window'
    kwZoomReset:str    = 'General Tool Reset Zoom One'
    kwZoomResetAll:str = 'General Tool Reset Zoom All'
    #------------------------------> Files
    fConfig:Path = Path.home() / '.umsap_config.json'
    #------------------------------> Sizes
    sWinFull:tuple[int,int] = (990, 775)                                        # Full window size
    sWinPlot:tuple[int,int] = (560, 560)                                        # Result window size
    sTc:tuple[int,int]      = (50, 22)                                          # wx.TextCtrl
    sLCtrlColI:list[int]    = field(default_factory=lambda: [50, 150])          # Size for # Name columns in a wx.ListCtrl
    #------------------------------> File Extensions
    elData:str         = 'txt files (*.txt)|*.txt'                              # For wx.Dialogs
    elUMSAP:str        = 'UMSAP files (*.umsap)|*.umsap'
    elPDB:str          = 'PDB files (*.pdb)|*.pdb'
    elPDF:str          = 'PDF files (*.pdf)|*.pdf'
    elSeq:str          = ('Text files (*.txt)|*.txt|'
                          'Fasta files (*.fasta)|*.fasta')
    elMatPlotSaveI:str = ('Portable Document File (*.pdf)|*.pdf|'
                          'Portable Network Graphic (*.png)|*.png|'
                          'Scalable Vector Graphic (*.svg)|*.svg|'
                          'Tagged Image File (*.tif)|*.tif')
    esData:list  = field(default_factory=lambda: ['.txt'])                      # First item is default
    esPDB:list   = field(default_factory=lambda: ['.pdb'])
    esPDF:list   = field(default_factory=lambda: ['.pdf'])
    esSeq:list   = field(default_factory=lambda: ['.txt', '.fasta'])
    esUMSAP:list = field(default_factory=lambda: ['.umsap'])
    #------------------------------> URLs
    urlHome     = 'https://www.umsap.nl'
    urlTutorial = f"{urlHome}/tutorial/2-2-X"
    urlUpdate   = f"{urlHome}/page/release-notes"
    #------------------------------> List
    dfcolSeqNC:list[str] = field(default_factory=lambda:                        # Column names in result dataframe
        ['Sequence', 'Nterm', 'Cterm', 'NtermF', 'CtermF'])
    ltDPKeys:list[str] = field(default_factory=lambda: ['dfF', 'dfT', 'dfN', 'dfIm'])
    lAA1:list[str] = field(default_factory=lambda: [                            # AA one letter codes
        'A', 'I', 'L', 'V', 'M', 'F', 'W', 'Y', 'R', 'K', 'D', 'E', 'C', 'Q',
        'H', 'S', 'T', 'N', 'G', 'P'])
    lAAGroups:list[list[str]] = field(default_factory=lambda: [                 # AA groups
        ['A', 'I', 'L', 'V', 'M'],
        ['F', 'W', 'Y'],
        ['R', 'K'],
        ['D', 'E'],
        ['C', 'Q', 'H', 'S', 'T', 'N'],
        ['G', 'P']])
    #------------------------------> Options
    oYesNo:dict = field(default_factory=lambda: {                               # Cast to bool
        ''   : False,
        'Yes': True,
        'No' : False,
    })
    oNumType:dict = field(default_factory=lambda: {                             # Cast Numbers
        'int'  : int,
        'float': float,
    })
    oSamples:dict = field(default_factory=lambda: {                             # Sample type for statistics
        '': '',
        'Independent Samples': 'i',
        'Paired Samples': 'p',
    })
    oCorrectP:dict = field(default_factory=lambda: {                            # P Correction
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
    })
    oAA3toAA:dict = field(default_factory=lambda: {                             # Three to one AA code translation
        'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D',
        'CYS': 'C', 'GLU': 'E', 'GLN': 'Q', 'GLY': 'G',
        'HIS': 'H', 'ILE': 'I', 'LEU': 'L', 'LYS': 'K',
        'MET': 'M', 'PHE': 'F', 'PRO': 'P', 'SER': 'S',
        'THR': 'T', 'TRP': 'W', 'TYR': 'Y', 'VAL': 'V',
    })
    #------------------------------> Names for output folder and files
    fnInitial:str    = "{}_{}-Initial-Data.txt"
    fnFloat:str      = "{}_{}-Floated-Data.txt"
    fnTrans:str      = "{}_{}-Transformed-Data.txt"
    fnNorm:str       = "{}_{}-Normalized-Data.txt"
    fnImp:str        = "{}_{}-Imputed-Data.txt"
    fnTargetProt:str = "{}_{}-Target-Protein-Data.txt"
    fnExclude:str    = "{}_{}-After-Excluding-Data.txt"
    fnScore:str      = "{}_{}-Score-Filtered-Data.txt"
    fnDataSteps:str  = 'Steps_Data_Files'
    fnDataInit:str   = 'Input_Data_Files'
    #------------------------------> Fonts
    fSeqAlign:Union[wx.Font, str]              = ''
    fTreeItem:Union[wx.Font, str]              = ''
    fTreeItemDataFile:Union[wx.Font, str]      = ''
    fTreeItemDataFileFalse:Union[wx.Font, str] = ''
    #------------------------------> To Load user configuration options
    confUserFile:bool = True                                                    # User configuration file is Ok
    confUserFileException:Optional[Exception] = None                            # Exception thrown when reading conf file
    confUserWrongOptions:list = field(default_factory=lambda: [])               # List of wrong options in the file
    confList:list = field(default_factory=lambda: ['core'])                     # Config modules with user configurable options
    #------------------------------> User Configurable Options
    checkUpdate:bool    = True                                                  # True Check, False No check
    DPI:int             = 100                                                   # DPI for plot images
    MatPlotMargin:float = 0.025                                                 # Margin for the axes range
    #--------------> Colors
    cZebra: str          = '#ffe6e6'                                            # Zebra style in wx.ListCrl
    cRecProt:str         = 'gray'                                               # Color in Fragment representation
    cNatProt:str         = '#c94c4c'                                            # Color in Fragment representation
    cFragments:list[str] = field(default_factory=lambda: [                      # Color for Exp/Cond in Fragments
        '#ffef96', '#92a8d1', '#b1cbbb', '#eea29a', '#b0aac0',
        '#f4a688', '#d9ecd0', '#b7d7e8', '#fbefcc', '#a2836e',
    ])
    #------------------------------> Converter for user options
    converter:dict = field(default_factory=lambda: {
        'checkUpdate'  : bool,
        'DPI'          : int,
        'MatPlotMargin': float,
        'cZebra'       : str,
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
