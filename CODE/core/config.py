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
    commOpen:str         = field(init=False)                                    # Command to open files
    copyShortCut:str     = field(init=False)                                    # Key for shortcuts
    deltaWin:int         = field(init=False)                                    # Horizontal space between top of windows
    fConfigDef:Path      = field(init=False)                                    # Path to File
    fImgAbout:Path       = field(init=False)
    fImgIcon:Path        = field(init=False)
    fImgStart:Path       = field(init=False)
    fManual:Path         = field(init=False)
    pImages:Path         = field(init=False)                                    # Path to Images
    res:Path             = field(init=False)                                    # Path to the Resources folder
    root:Path            = field(init=False)                                    # Root folder
    toolMenuIdx:int      = field(init=False)                                    # Tool place location
    ttLCtrlCopyNoMod:str = field(init=False)
    ttLCtrlPasteMod:str  = field(init=False)
    #------------------------------> General Options
    cwd:Path         = Path(__file__)                                           # Config file path
    development:bool = True                                                     # Development (True) or Production (False)
    dictVersion:dict = field(default_factory=lambda: {                          # To write into output files
        'Version': '2.3.0 (beta)',
    })
    dtFormat:str     = '%Y%m%d-%H%M%S'                                          # Date Time format
    fConfig:Path     = Path.home() / '.umsap_config.json'                       # Path to user configuration file
    os:str           = platform.system()                                        # Current operating system
    software:str     = 'UMSAP'                                                  # Software short name
    softwareF:str    = 'Utilities for Mass Spectrometry Analysis of Proteins'   # Software full name
    version:str      = '2.3.0 (beta)'                                           # String to write in the output files
    winNumber:dict   = field(default_factory=lambda: {})                        # Keys: Windows ID - Values: Total number of opened windows, except conf win
    #------------------------------> Name & Title
    ndResCtrlExp:str      = 'Name Dialog Results & Control Experiments'         # Unique name for wx, not shown to user
    npDef:str             = 'Name Pane Default'
    npLCtrlSearchPlot:str = 'Name Pane ListCtrl Search Plot'
    npNPlot:str           = 'Name Pane NPlot'
    ntDef:str             = 'Name Tab Default'
    nwDef:str             = 'Name Window Default'
    tpConf:str            = 'Configuration Options'                             # Titles, shown to user
    tpList:str            = 'Data File Content'
    ttDef:str             = 'Tab'
    twResCtrl:str         = 'Result & Control Experiments'
    #------------------------------> Label for Widgets
    lBtnTypeResCtrl:str = 'Type Values'                                         # lBtn: Label for wx.Button
    lCbCorrectP:str     = 'P Correction'                                        # lCb: Label for wx.ComboBox
    lCbSample:str       = 'Samples'
    lmNatSeq:str        = 'Native Sequence'                                     # lm: Label for wx.MenuItem
    lmPCorrected:str    = 'Corrected P Values'
    lmTools:str         = 'Tools'
    lPdError:str        = 'Fatal Error'                                         # lPd: Label for Progress Dialog
    lPdDone:str         = 'All Done'
    lStAAPos:str        = 'AA Positions'                                        # lSt: Label for wx.StaticText
    lStAlpha:str        = 'α Level'
    lStBeta:str         = 'β Level'
    lStColAnalysis:str  = 'Columns for Analysis'
    lStCtrlName:str     = 'Name'
    lStCtrlType:str     = 'Type'
    lStExcludeProt:str  = 'Exclude Proteins'
    lStGamma:str        = 'γ Level'
    lStGeneName:str     = 'Gene Names'
    lStHistWind:str     = 'Histogram Windows'
    lStLog2FC:str       = 'Log2FC'
    lStP:str            = 'P'
    lStProtein:str      = 'Proteins'
    lStResCtrl:str      = 'Results - Control experiments'
    lStResCtrlS:str     = 'Results - Control'
    lStS0:str           = 's0'
    lStSample:str       = 'Sample'
    lStScoreCol:str     = 'Score'
    lStScoreVal:str     = 'Score Value'
    lStT0:str           = 't0'
    lStTheta:str        = 'θ Value'
    lStThetaMax:str     = 'θ Max Value'
    lStZScore:str       = 'Z Score'
    #------------------------------> wx.ListCtrl Column names
    lLCtrlColNameI:list[str] = field(default_factory=lambda: ['#', 'Name'])
    #------------------------------> Keywords for Menu
    kwCheckDP:str      = 'General Tool Check DP'
    kwDupWin:str       = 'General Tool Duplicate Window'
    kwExpData:str      = 'General Tool Export Data'
    kwExpImg:str       = 'General Tool Export Image One'
    kwExpImgAll:str    = 'General Tool Export Image'
    kwExpSeq:str       = 'General Tool Export Sequence'
    kwWinUpdate:str    = 'General Tool Update Result Window'
    kwZoomReset:str    = 'General Tool Reset Zoom One'
    kwZoomResetAll:str = 'General Tool Reset Zoom All'
    kwNat:str          = 'nat'                                                  # Methods keywords
    kwShift:str        = 'Shift'
    kwAlt:str          = 'Alt'
    kwMain:str         = 'Main'
    kwSec:str          = 'Sec'
    kwPCorrected:str   = 'corrP'
    #------------------------------> Sizes
    sLCtrlColI:list[int] = field(default_factory=lambda: [50, 150])             # Size for # Name columns in a wx.ListCtrl
    sTc:tuple[int,int]         = (50, 22)                                       # wx.TextCtrl
    sTcS:tuple[int,int]        = (70,22)
    sWinFull:tuple[int,int]    = (990, 775)                                     # Full window size
    sWinModPlot:tuple[int,int] = (1100, 625)                                    # Result Window for a Module
    sWinPlot:tuple[int,int]    = (560, 560)                                     # Result window size
    #------------------------------> File Extensions
    elData:str         = 'txt files (*.txt)|*.txt'                              # For wx.Dialogs
    elMatPlotSaveI:str = ('Portable Network Graphic (*.png)|*.png|'
                          'Scalable Vector Graphic (*.svg)|*.svg|'
                          'Tagged Image File (*.tiff)|*.tiff')
    elPDB:str          = 'PDB files (*.pdb)|*.pdb'
    elPDF:str          = 'PDF files (*.pdf)|*.pdf'
    elSeq:str          = ('Text files (*.txt)|*.txt|'
                          'Fasta files (*.fasta)|*.fasta')
    elUMSAP:str        = 'UMSAP files (*.umsap)|*.umsap'
    #-->
    esData:list[str]         = field(default_factory=lambda: ['.txt'])          # First item is default
    esMatPlotSaveI:list[str] = field(default_factory=lambda:
        ['png', 'svg', 'tiff'])
    esPDB:list[str]          = field(default_factory=lambda: ['.pdb'])
    esPDF:list[str]          = field(default_factory=lambda: ['.pdf'])
    esSeq:list[str]          = field(default_factory=lambda: ['.txt', '.fasta'])
    esUMSAP:list[str]        = field(default_factory=lambda: ['.umsap'])
    #------------------------------> URLs
    urlHome     = 'https://www.umsap.nl'
    urlTutorial = f'{urlHome}/tutorial/2-2-X'
    urlUpdate   = f'{urlHome}/page/release-notes'
    #------------------------------> List
    dfcolSeqNC:list[str]      = field(default_factory=lambda:                   # Column names in result dataframe
        ['Sequence', 'Nterm', 'Cterm', 'NtermF', 'CtermF'])
    ltDPKeys:list[str]        = field(default_factory=lambda:                   # ID of Data Prep data frames
        ['dfF', 'dfT', 'dfN', 'dfIm'])
    lAA1:list[str]            = field(default_factory=lambda:                   # AA one letter codes
        ['A', 'I', 'L', 'V', 'M', 'F', 'W', 'Y', 'R', 'K', 'D', 'E', 'C', 'Q',
        'H', 'S', 'T', 'N', 'G', 'P'])
    lAAGroups:list[list[str]] = field(default_factory=lambda:                   # AA groups
        [['K', 'R'],
         ['C', 'H', 'Q', 'N', 'S', 'T'],
         ['G', 'P'],
         ['D', 'E'],
         ['A', 'I', 'L', 'V', 'M'],
         ['F', 'W', 'Y']])
    #------------------------------> Options
    oYesNo:dict    = field(default_factory=lambda: {                            # Cast to bool
        ''   : False,
        'Yes': True,
        'No' : False,
    })
    oNumType:dict  = field(default_factory=lambda: {                            # Cast Numbers
        'int'  : int,
        'float': float,
    })
    oSamples:dict  = field(default_factory=lambda: {                            # Sample type for statistics
        '': '',
        'Independent Samples': 'i',
        'Paired Samples': 'p',
    })
    oSamplesP:dict  = field(default_factory=lambda: {                           # Sample type for statistics
        'i': 'Independent Samples',
        'p': 'Paired Samples',
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
    oAA3toAA:dict  = field(default_factory=lambda: {                            # Three to one AA code translation
        'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D',
        'CYS': 'C', 'GLU': 'E', 'GLN': 'Q', 'GLY': 'G',
        'HIS': 'H', 'ILE': 'I', 'LEU': 'L', 'LYS': 'K',
        'MET': 'M', 'PHE': 'F', 'PRO': 'P', 'SER': 'S',
        'THR': 'T', 'TRP': 'W', 'TYR': 'Y', 'VAL': 'V',
    })
    #------------------------------> Names for output folder and files
    fnInitial:str    = '{}_{}-Initial-Data.txt'
    fnFloat:str      = '{}_{}-Floated-Data.txt'
    fnTrans:str      = '{}_{}-Transformed-Data.txt'
    fnNorm:str       = '{}_{}-Normalized-Data.txt'
    fnImp:str        = '{}_{}-Imputed-Data.txt'
    fnTargetProt:str = '{}_{}-Target-Protein-Data.txt'
    fnExclude:str    = '{}_{}-After-Excluding-Data.txt'
    fnScore:str      = '{}_{}-Score-Filtered-Data.txt'
    fnDataSteps:str  = 'Steps_Data_Files'
    fnDataInit:str   = 'Input_Data_Files'
    #------------------------------> Messages
    mAllTextFieldEmpty:str  = 'All text fields are empty. Nothing will be done.'
    mColNumber:str          = ('In addition, the value must be smaller than '
                               'the total number of columns in the Data file.')
    mColNumbers:str         = ('In addition, each value must be smaller than '
                               'the total number of columns in the Data file.')
    mCopyFailedW:str        = 'Copy operation failed. Try again.'
    mCtrlEmpty:str          = 'None of the Control fields can be empty.'
    mEmpty:str              = 'The field value cannot be empty.'
    mFileBad:str            = "File: '{}'\ncannot be used as {} file."
    mFileRead:str           = 'An error occurred when reading file:\n{}'
    mFileSelUMSAP:str       = 'Select the UMSAP File'
    mInvalidValue:str       = "'{}' is an invalid value."
    mLCtrlNColPaste:str     = ('The clipboard content cannot be pasted because '
        'the number of columns being pasted is different to the number of '
        'columns in the list.')
    mLCtrNoChange:str       = 'This list cannot be modified.'
    mLCtrNoCopy:str         = 'The elements of this list cannot be copied.'
    mNoDataLeft:str         = ('No data left for analysis after all filters '
                               '(Score, Target Protein, etc) were applied.')
    mNothing2PasteW:str     = 'Nothing to paste.'
    mNotImplementedFull:str = ('Option {} is not yet implemented. Valid '
                               'options for {} are: {}.')
    mNZPlusNumText:str      = ('Only a list of unique non-negative integers '
                               'can be accepted here.')
    mOne01NumText:str       = ('Only one number between 0 and 1 can be '
                               'accepted here.')
    mOne0100NumText:str     = ('Only one number between 0 and 100 can be '
                               'accepted here.')
    mOneRNumText:str        = 'Only one real number can be accepted here.'
    mOneRPlusNumText:str    = ('Only one number equal or greater than zero can '
                               'be accepted here.')
    mOneZPlusNumText:str    = ('Only a non-negative integer can be accepted '
                               'here.')
    mOptField:str           = '\nThis field is optional.'
    mOptionBad:str          = "Option '{}' cannot be accepted in {}."
    mPasteFailedW:str       = 'Paste operation failed. Try again.'
    mPDDataExclude:str      = ('Data Exclusion failed.\nColumns used for data '
                               'exclusion: {}.')
    mPDDataScore:str        = ('Data Filtering by Score value failed.\nColumns '
                               'used for data filtering by Score value: {}.')
    mPDDataTargetProt:str   = ('Selection of Target Protein failed.\nTarget '
                               'Protein: {} Detected Proteins column: {}.')
    mRangeNumIE:str         = 'Invalid range or number: {}'
    mRepeatColNum:str       = ('There are repeated column numbers in the text '
                               'fields.')
    mRepNum:str             = ('The number of replicates in some experiments '
        'does not match the number of replicates in the control.')
    mRowsInLCtrl:str        = 'There must be at least {} items in {}.'
    mSection:str            = 'Values in section {} must be unique.'
    mSeqPeptNotFound:str    = ("The peptide '{}' was not found in the sequence "
                               "of the {} protein.")
    mUnexpectedError:str    = 'UMSAP encountered an unexpected error.'
    mValueBad:str           = "Value '{}' cannot be accepted in {}.\n"
    mNoPCorr:str            = ('This analysis does not contain information '
                               'about corrected P values.')
    #-->
    mOneRPlusNum:str    = f'{mValueBad}{mOneRPlusNumText}'
    mNZPlusNum:str      = f'{mValueBad}{mNZPlusNumText}'
    mNZPlusNumCol:str   = f'{mNZPlusNum} {mColNumbers}'
    mOneRealNum:str     = f'{mValueBad}{mOneRNumText}'
    mOne01Num:str       = f'{mValueBad}{mOne01NumText}'
    mOne0100Num:str     = f'{mValueBad}{mOne0100NumText}'
    mOneZPlusNum:str    = f'{mValueBad}{mOneZPlusNumText}'
    mOneZPlusNumCol:str = f'{mOneZPlusNum} {mColNumber}'
    mResCtrl:str        = (f'{mValueBad} Please use the '
                          f'{lBtnTypeResCtrl} button to provide a '
                          f'correct input.')
    mResCtrlWin:str     = ("Value '{}' cannot be accepted as input.\n"
                          f"{mNZPlusNumText}")
    #------------------------------> Tooltips
    ttBtnHelp:str           = 'Read tutorial at {}.'
    ttSectionRightClick:str = ('The content of the Section can be deleted with '
                               'a right click.')
    ttStCorrectP:str        = 'Select the p correction method.'
    ttStExcludeProt:str     = ('Set the column number containing the data used '
                               'to exclude proteins.\ne.g. 8 10-12')
    ttStGenName:str         = (f'Set the column number containing the '
                               f'{lStGeneName}.\ne.g. 3')
    ttStSample:str          = ('Specify if samples are independent or paired.\n'
        'For example, samples are paired when the same Petri dish is used '
        'for the control and experiment.')
    ttStScoreCol:str        = (f'Set the column number containing the '
                               f'{lStScoreVal}.\ne.g. 4')
    ttStScoreVal:str        = 'Set the minimum acceptable Score value.\ne.g. -4'
    ttAAPos = (f'Number of positions around the cleavage sites to consider '
        f'for the AA distribution analysis.\ne.g. 5{mOptField}')
    ttHist = (f'Size of the histogram windows. One number will result in '
        f'equally spaced windows. Multiple numbers allow defining custom sized '
        f'windows.\ne.g. 50 or 0 50 100 150 500{mOptField}')
    #------------------------------> Fonts
    fSeqAlign:Union[wx.Font, str]              = ''
    fTreeItem:Union[wx.Font, str]              = ''
    fTreeItemDataFile:Union[wx.Font, str]      = ''
    fTreeItemDataFileFalse:Union[wx.Font, str] = ''
    #------------------------------> Other
    MatPlotMargin:float = 0.025                                                 # Margin for the axes range
    cChi:dict = field(default_factory=lambda: {                                 # Chi results in AA
        1 : 'Green',
        0 : 'Red',
        -1: 'Black',
    })
    #------------------------------> To Load user configuration options
    confUserFile:bool = True                                                    # User configuration file is Ok
    confUserFileException:Optional[Exception] = None                            # Exception thrown when reading conf file
    confUserWrongOptions:list = field(default_factory=lambda: [])               # List of wrong options in the file
    confList:list = field(default_factory=lambda: ['core'])                     # Config modules with user configurable options
    #------------------------------> User Configurable Options
    checkUpdate:bool    = True                                                  # True Check, False No check
    DPI:int             = 100                                                   # DPI for plot images
    imgFormat:str       = 'png'                                                 # Default format when saving multiple images
    #--------------> Colors
    cZebra: str         = '#ffe6e6'                                             # Zebra style in wx.ListCrl
    cRecProt:str        = 'gray'                                                # Color in Fragment representation
    cNatProt:str        = '#c94c4c'                                             # Color in Fragment representation
    cFragment:list[str] = field(default_factory=lambda: [                       # Color for Exp/Cond in Fragments
        '#ffef96', '#92a8d1', '#b1cbbb', '#eea29a', '#b0aac0',
        '#f4a688', '#d9ecd0', '#b7d7e8', '#fbefcc', '#a2836e',
    ])
    cBarColor:dict = field(default_factory=lambda: {
        'R': '#0099ff', 'K': '#0099ff', 'D': '#ff4d4d', 'W': '#FF51FD',
        'E': '#ff4d4d', 'S': '#70db70', 'T': '#70db70', 'H': '#70db70',
        'N': '#70db70', 'Q': '#70db70', 'C': '#70db70', 'G': '#FFFC00',
        'P': '#FFFC00', 'A': '#BEBEBE', 'V': '#BEBEBE', 'I': '#BEBEBE',
        'L': '#BEBEBE', 'M': '#BEBEBE', 'F': '#FF51FD', 'Y': '#FF51FD',
    })
    #endregion ------------------------------------------------------> Options

    #region ---------------------------------------------------> Class Methods
    def __post_init__(self):
        """Set values depending on OS specific parameters"""
        #------------------------------> Platform dependent parameters
        if self.os == 'Darwin':
            self.commOpen     = 'open'
            self.copyShortCut = 'Cmd'
            self.deltaWin     = 23
            self.root         = self.cwd.parent.parent.parent
            self.res          = self.root / 'Resources'
            self.toolMenuIdx  = 2
        elif self.os == 'Windows':
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
        #------------------------------> Tooltips
        self.ttLCtrlCopyNoMod = (f'Selected rows can be copied '
            f'({self.copyShortCut}+C) but the table cannot be modified.')
        self.ttLCtrlPasteMod  = (f'New rows can be pasted '
            f'({self.copyShortCut}+V) after the last selected element and '
            f'existing ones cut/deleted ({self.copyShortCut}+X) or copied '
            f'({self.copyShortCut}+C).')
    #endregion ------------------------------------------------> Class Methods
#---
#endregion ----------------------------------------------------> Configuration
