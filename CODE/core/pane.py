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


"""Base Pane for the app"""


#region -------------------------------------------------------------> Imports
import _thread
import shutil
from pathlib import Path
from typing  import Optional, Union

import pandas as pd

import wx
import wx.lib.scrolledpanel as scrolled

from config.config import config as mConfig
from core import check     as cCheck
from core import file      as cFile
from core import method    as cMethod
from core import validator as cValidator
from core import widget    as cWidget
from core import window    as cWindow
#endregion ----------------------------------------------------------> Imports


ANALYSIS_METHOD = {
    # mConfig.npCorrA   : mMethod.CorrA,
    # mConfig.npDataPrep: mStatistic.DataPreparation,
    # mConfig.npProtProf: mMethod.ProtProf,
    # mConfig.npLimProt : mMethod.LimProt,
    # mConfig.npTarProt : mMethod.TarProt,
}


#region -------------------------------------------------------------> Classes
class BaseConfPanel(
    scrolled.ScrolledPanel,
    cWidget.StaticBoxes,
    cWidget.ButtonOnlineHelpClearAllRun
    ):
    """Creates the skeleton of a configuration panel. This includes the
        wx.StaticBox, the bottom Buttons, the statusbar and some widgets.

        Parameters
        ----------
        parent: wx.Window
            Parent of the widgets.
        rightDelete: Boolean
            Enables clearing wx.StaticBox input with right click.

        Attributes
        ----------
        dfI: pd.DataFrame
            DataFrame for the initial values.
        dfF: pd.DataFrame
            DataFrame as float values and 0 and '' as np.nan.
        dfT: pd.DataFrame
            DataFrame with the transformed values.
        dfN: pd.DataFrame
            DataFrame with normalized values.
        dfIm: pd.DataFrame
            DataFrame with imputed values.
        dfTP: pd.DataFrame
            DataFrame filtered by Target Protein.
        dfE: DataFrame
            Exclude some entries by some parameters.
        dfS: DataFrame
            Exclude entries by Score values.
        dfR: pd.DataFrame
            DataFrame with the results values.
        rChangeKey: list of str
            Keys in do whose values will be turned into a str. Default to
            ['iFile', 'uFile].
        rCheckUnique: list of wx.TextCtrl
            These fields must contain unique column numbers.
        rCheckUserInput: dict
            To check user input in the correct order.
            Keys are widget labels and values a list with [widget,
            error message, bool]. Error message must be like mConfig.mFileBad.
            Boolean is True when the column numbers in the Data file are needed
            to check user input.
        rCopyFile: dict
            Keys are the keys in self.rDO and values label of the widget.
        rDate: str
            Date for the new section in the umsap file.
        rDateID: str
            Date + Analysis ID
        rDeltaT: str
            Elapsed analysis time.
        rDExtra: dict
            Extra options for the Analysis methods.
        rDFile: list[Path]
            Full paths to copied input files. Needed to repeat the analysis
            directly after running.
        rDI: dict
            Dict with user input.
            The following key-value pairs are expected.
            'oc' : {
                'Column' : [list of int],
            }
            See Child class for other key - value pairs.
        rDO: dict
            Dict with processed user input.
            The following key-value pairs are expected.
            'Cero' : bool,
            'df' : {
                'ColumnF' : [list of int],
                'ExcludeP': [list of int],
            }
            See Child class for other key - value pairs.
        rDlg: dtscore.ProgressDialog
            Progress dialog.
        rException: Exception or None
            Exception raised during analysis.
        rIFileObj: dtsFF.CSVFile or none
            Input Data File Object.
        rLCtrlL: list of wx.ListCtrl
            To clear all wx.ListCtrl in the Tab.
        rLLenLongest: int
            Length of longest label.
        rMainData: str
            Name of the file containing the main output data.
        rMsgError: Str
            Error message to show when analysis fails.
        rNCol: int
            Number of columns in the main input file - 1. Set when the file is
            read.
        rOFolder: Path or None
            Folder to contain the output. Set based on the umsap file path.
        rSeqFileObj: dtsFF.FastaFile
            Object to work with the sequences of the proteins.
    """
    #region --------------------------------------------------> Instance setup
    def __init__(self, parent:wx.Window, rightDelete:bool=True) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.cParent = parent
        #------------------------------>
        self.cName    = getattr(self, 'cName', mConfig.core.npDef)
        self.cSection = getattr(self, 'cSection', 'Default Section')
        #------------------------------> For the Progress Dialog
        self.cTitlePD = getattr(self, 'cTitlePD', 'Default Title')
        self.cGaugePD = getattr(self, 'cGaugePD', 50)
        #------------------------------> Labels
        self.cLFileBox      = getattr(self, 'cLFileBox',      'Files')
        self.cLDataBox      = getattr(self, 'cLDataBox',      'Data Preparation')
        self.cLValueBox     = getattr(self, 'cLValueBox',     'User-defined Values')
        self.cLColumnBox    = getattr(self, 'cLColumnBox',    'Column Numbers')
        self.cLuFile        = getattr(self, 'cLuFile',        'UMSAP')
        self.cLiFile        = getattr(self, 'cLiFile',        'Data')
        self.cLId           = getattr(self, 'cLId',           'Analysis ID')
        self.cLCeroTreatD   = getattr(self, 'cLCeroTreatD',   '0s Missing')
        self.cLNormMethod   = getattr(self, 'cLNormMethod',   'Normalization')
        self.cLTransMethod  = getattr(self, 'cLTransMethod',  'Transformation')
        self.cLImputation   = getattr(self, 'cLImputation',   'Imputation')
        self.cLShift        = getattr(self, 'cLShift',        'Shift')
        self.cLWidth        = getattr(self, 'cLWidth',        'Width')
        self.cLDetectedProt = getattr(self, 'cLDetectedProt', '')
        self.cLSeqFile      = getattr(self, 'cLSeqFile',      '')
        self.cLCeroTreat    = getattr(self, 'cLCeroTreat',    'Treat 0s as missing values')
        #------------------------------> For Progress Dialog
        self.cLPdCheck    = getattr(self, 'cLPdCheck',    'Checking user input: ')
        self.cLPdPrepare  = getattr(self, 'cLPdPrepare',  'Preparing analysis: ')
        self.cLPdRun      = getattr(self, 'cLPdRun',      'Running analysis: ')
        self.cLPdRunText  = getattr(self, 'cLPdRunText',  'Main Analysis')
        self.cLPdWrite    = getattr(self, 'cLPdWrite',    'Writing output: ')
        self.cLPdLoad     = getattr(self, 'cLPdLoad',     'Loading output file')
        self.cLPdError    = getattr(self, 'cLPdError',    mConfig.core.lPdError)
        self.cLPdDone     = getattr(self, 'cLPdDone',     'All Done')
        self.cLPdElapsed  = getattr(self, 'cLPdElapsed',  'Elapsed time: ')
        self.cLPdReadFile = getattr(self, 'cLPdReadFile', 'Reading input files: ')
        #------------------------------> Size
        self.cSTc = getattr(self, 'cSTc', mConfig.core.sTc)
        #------------------------------> Choices
        self.cOCero = getattr(self, 'cOCero', list(mConfig.core.oYesNo.keys()))
        self.cONorm = getattr(self, 'cONorm', list(mConfig.data.oNormMethod.keys()))
        self.cOTrans = getattr(
            self, 'cOTrans', list(mConfig.data.oTransMethod.keys()))
        self.cOImputation = getattr(
            self, 'cOImputation', list(mConfig.data.oImputation.keys()))
        #------------------------------> Hints
        self.cHuFile = getattr(
            self, 'cHuFile', f"Path to the {self.cLuFile} file")
        self.cHiFile = getattr(
            self, 'cHiFile', f"Path to the {self.cLiFile} file")
        self.cHId    = getattr(self, 'cHId', 'e.g. HIV inhibitor')
        #------------------------------> Tooltips
        self.cTTRun  = getattr(self, 'cTTRun', 'Start the analysis.')
        self.cTTHelp = getattr(
            self, 'cTTHelp', f'Read online tutorial at {mConfig.core.urlHome}.')
        self.cTTClearAll = getattr(
            self, 'cTTClearAll', 'Clear all user input.')
        self.cTTuFile = getattr(
            self, 'cTTuFile', f'Select the {self.cLuFile} file.')
        self.cTTiFile = getattr(
            self, 'cTTiFile', f'Select the {self.cLiFile} file.')
        self.cTTId  = getattr(
            self, 'cTTId', ('Short text to identify the analysis. The date of '
            'the analysis will be automatically included.\ne.g. HIV inhibitor'))
        self.cTTNormMethod = getattr(
            self, 'cTTNormMethod', (f'Select the Data {self.cLNormMethod} '
                                    f'method.'))
        self.cTTTransMethod = getattr(
            self, 'cTTTransMethod', (f'Select the Data {self.cLTransMethod} '
                                     f'method.'))
        self.cTTImputation  = getattr(
            self, 'cTTImputation', (f'Select the Data {self.cLImputation} '
                                    f'method.'))
        self.cTTShift = getattr(
            self, 'cTTShift', ('Factor to shift the center of the normal '
                               'distribution used to replace missing. '
                               'values\ne.g. 1.8'))
        self.cTTWidth = getattr(
            self, 'cTTWidth', ('Factor to control the width of the normal '
                               'distribution used to replace missing. '
                               'values\ne.g. 0.3'))
        #------------------------------> URL
        self.cURL = getattr(self, 'cURL', mConfig.core.urlTutorial)
        #------------------------------> Extensions
        self.cEiFile = getattr(self, 'ciFileE', mConfig.core.elData)
        #------------------------------> Validator
        self.cVuFile = getattr(self, 'cVuFile', cValidator.OutputFF(fof='file'))
        self.cViFile = getattr(self, 'cViFile', cValidator.InputFF(fof='file'))
        #------------------------------> Values
        self.cValShift = mConfig.data.Shift
        self.cValWidth = mConfig.data.Width
        #------------------------------> This is needed to handle Data File
        # content load to the wx.ListCtrl in Tabs with multiple panels
        #--------------> Default wx.ListCtrl to load data file content
        self.wLCtrlI = None
        #--------------> List to use just in case there are more than 1
        self.rLCtrlL = []
        #------------------------------> Number of columns in the wx.ListCtrl
        self.rNCol   = None
        #------------------------------> Needed to Run the Analysis
        self.rCheckUnique = []
        self.rLLenLongest = getattr(self, 'rLLenLongest', 0)
        self.rMainData    = getattr(self, 'rMainData', '')
        #--------------> Dict with the user input as given
        self.rDI = {}
        #--------------> Dict with the processed user input
        self.rDO = {}
        #--------------> Dict with extra options for Run Analysis methods
        self.rDExtra = getattr(self, 'rDExtra', {})
        #--------------> Error message and exception to show in self.RunEnd
        self.rMsgError  = ''
        self.rException = None
        #--------------> pd.DataFrames for:
        self.dfI  = pd.DataFrame()                                              # Initial and
        self.dfF  = pd.DataFrame()                                              # Data as float and 0 and '' values as np.nan
        self.dfT  = pd.DataFrame()                                              # Transformed values
        self.dfN  = pd.DataFrame()                                              # Normalized Values
        self.dfIm = pd.DataFrame()                                              # Imputed values
        self.dfTP = pd.DataFrame()                                              # Select Target Protein
        self.dfE  = pd.DataFrame()                                              # Exclude entries by some parameter
        self.dfS  = pd.DataFrame()                                              # Exclude entries by Score value
        self.dfR  = pd.DataFrame()                                              # Results values
        #--------------> Date for umsap file
        self.rDate   = ''
        self.rDateID = ''
        #--------------> folder for output
        self.rOFolder = None
        #--------------> input file for directing repeating analysis from
        # file copied to oFolder
        self.rDFile   = []
        # #--------------> Obj for files
        self.rIFileObj   = None
        self.rSeqFileObj: Optional[cFile.FastaFile] = None
        #------------------------------>
        self.rChangeKey = getattr(self, 'rChangeKey', ['iFile', 'uFile'])
        #------------------------------>
        self.rCopyFile = getattr(self, 'rCopyFile', {'iFile':self.cLiFile})
        #------------------------------> Parent init
        scrolled.ScrolledPanel.__init__(self, parent, name=self.cName)

        cWidget.ButtonOnlineHelpClearAllRun.__init__(
            self,
            self,
            self.cURL,
            tooltipR = self.cTTRun,
            tooltipH = self.cTTHelp,
            tooltipC = self.cTTClearAll,
        )

        cWidget.StaticBoxes.__init__(
            self,
            self,
            labelF      = self.cLFileBox,
            labelD      = self.cLDataBox,
            labelV      = self.cLValueBox,
            labelC      = self.cLColumnBox,
            rightDelete = rightDelete,
        )
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wUFile = cWidget.ButtonTextCtrlFF(
            self.wSbFile,
            btnLabel   = self.cLuFile,
            btnTooltip = self.cTTuFile,
            tcHint     = self.cHuFile,
            mode       = 'save',
            ext        = mConfig.core.elUMSAP,
            tcStyle    = wx.TE_READONLY,
            validator  = self.cVuFile,
            ownCopyCut = True,
        )
        self.wIFile = cWidget.ButtonTextCtrlFF(
            self.wSbFile,
            btnLabel   = self.cLiFile,
            btnTooltip = self.cTTiFile,
            tcHint     = self.cHiFile,
            ext        = self.cEiFile,
            mode       = 'openO',
            tcStyle    = wx.TE_READONLY|wx.TE_PROCESS_ENTER,
            validator  = self.cViFile,
            ownCopyCut = True,
        )
        self.wId = cWidget.StaticTextCtrl(
            self.wSbFile,
            stLabel   = self.cLId,
            stTooltip = self.cTTId,
            tcHint    = self.cHId,
            validator = cValidator.IsNotEmpty(),
        )
        self.wCeroB = cWidget.StaticTextComboBox(
            self.wSbData,
            label   = self.cLCeroTreat,
            choices = self.cOCero,
            tooltip = (f'Cero values in the {self.cLiFile} file will '
            f'be treated as missing values when this option is set to Yes and '
            f'as real values when the option is set to No.'),
            validator = cValidator.IsNotEmpty(),
        )
        self.wNormMethod = cWidget.StaticTextComboBox(
            self.wSbData,
            label     = self.cLNormMethod,
            choices   = self.cONorm,
            tooltip   = self.cTTNormMethod,
            validator = cValidator.IsNotEmpty(),
        )
        self.wTransMethod = cWidget.StaticTextComboBox(
            self.wSbData,
            label     = self.cLTransMethod,
            choices   = self.cOTrans,
            tooltip   = self.cTTTransMethod,
            validator = cValidator.IsNotEmpty(),
        )
        self.wImputationMethod = cWidget.StaticTextComboBox(
            self.wSbData,
            label     = self.cLImputation,
            choices   = self.cOImputation,
            tooltip   = self.cTTImputation,
            validator = cValidator.IsNotEmpty(),
        )
        self.wShift = cWidget.StaticTextCtrl(
            self.wSbData,
            stLabel   = self.cLShift,
            stTooltip = self.cTTShift,
            tcSize    = (60,22),
            tcHint    = f'e.g. {self.cValShift}',
            validator = cValidator.NumberList('float', nN=1, vMin=0),
        )
        self.wWidth = cWidget.StaticTextCtrl(
            self.wSbData,
            stLabel   = self.cLWidth,
            stTooltip = self.cTTWidth,
            tcSize    = (60,22),
            tcHint    = f'e.g. {self.cValWidth}',
            validator = cValidator.NumberList('float', nN=1, vMin=0),
        )
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        #------------------------------> File
        self.sSbFileWid.Add(
            self.wUFile.wBtn,
            pos    = (0,0),
            flag   = wx.EXPAND|wx.ALL,
            border = 5
        )
        self.sSbFileWid.Add(
            self.wUFile.wTc,
            pos    = (0,1),
            flag   = wx.EXPAND|wx.ALL,
            border = 5
        )
        self.sSbFileWid.Add(
            self.wIFile.wBtn,
            pos    = (1,0),
            flag   = wx.EXPAND|wx.ALL,
            border = 5
        )
        self.sSbFileWid.Add(
            self.wIFile.wTc,
            pos    = (1,1),
            flag   = wx.EXPAND|wx.ALL,
            border = 5
        )
        self.sSbFileWid.Add(
            self.wId.wSt,
            pos    = (2,0),
            flag   = wx.ALIGN_CENTER|wx.ALL,
            border = 5
        )
        self.sSbFileWid.Add(
            self.wId.wTc,
            pos    = (2,1),
            flag   = wx.EXPAND|wx.ALL,
            border = 5
        )
        self.sSbFileWid.AddGrowableCol(1,1)
        self.sSbFileWid.AddGrowableRow(0,1)
        #------------------------------> Data
        self.sCeroTreat = wx.BoxSizer(wx.HORIZONTAL)
        self.sCeroTreat.Add(self.wCeroB.wSt, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        self.sCeroTreat.Add(self.wCeroB.wCb, 0, wx.ALIGN_CENTER|wx.ALL, 5)

        self.sImpNorm = wx.BoxSizer(wx.HORIZONTAL)
        self.sImpNorm.Add(self.wShift.wSt, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.sImpNorm.Add(self.wShift.wTc, 0, wx.EXPAND|wx.ALL, 5)
        self.sImpNorm.Add(self.wWidth.wSt, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.sImpNorm.Add(self.wWidth.wTc, 0, wx.EXPAND|wx.ALL, 5)

        self.sSbDataWid.Add(
            1, 1,
            pos    = (0,0),
            flag   = wx.EXPAND|wx.ALL,
            border = 5
        )
        self.sSbDataWid.Add(
            self.sCeroTreat,
            pos    = (0,1),
            flag   = wx.ALIGN_CENTER|wx.ALL,
            border = 5,
            span   = (0, 6),
        )
        self.sSbDataWid.Add(
            self.wTransMethod.wSt,
            pos    = (1,1),
            flag   = wx.ALL|wx.ALIGN_CENTER,
            border = 5,
        )
        self.sSbDataWid.Add(
            self.wTransMethod.wCb,
            pos    = (1,2),
            flag   = wx.ALL|wx.EXPAND,
            border = 5,
        )
        self.sSbDataWid.Add(
            self.wNormMethod.wSt,
            pos    = (1,3),
            flag   = wx.ALL|wx.ALIGN_CENTER,
            border = 5,
        )
        self.sSbDataWid.Add(
            self.wNormMethod.wCb,
            pos    = (1,4),
            flag   = wx.ALL|wx.EXPAND,
            border = 5,
        )
        self.sSbDataWid.Add(
            self.wImputationMethod.wSt,
            pos    = (1,5),
            flag   = wx.ALL|wx.ALIGN_CENTER,
            border = 5,
        )
        self.sSbDataWid.Add(
            self.wImputationMethod.wCb,
            pos    = (1,6),
            flag   = wx.ALL|wx.EXPAND,
            border = 5,
        )
        self.sSbDataWid.Add(
            self.sImpNorm,
            pos    = (2,5),
            flag   = wx.ALL|wx.ALIGN_CENTER,
            border = 5,
            span   = (0,2),
        )
        self.sSbDataWid.Add(
            1, 1,
            pos    = (0,7),
            flag   = wx.EXPAND|wx.ALL,
            border = 5
        )
        self.sSbDataWid.AddGrowableCol(0,1)
        self.sSbDataWid.AddGrowableCol(7,1)
        #------------------------------>
        self.sSizer = wx.BoxSizer(wx.VERTICAL)
        self.sSizer.Add(self.sSbFile,   0, wx.EXPAND|wx.ALL,       5)
        self.sSizer.Add(self.sSbData,   0, wx.EXPAND|wx.ALL,       5)
        self.sSizer.Add(self.sSbValue,  0, wx.EXPAND|wx.ALL,       5)
        self.sSizer.Add(self.sSbColumn, 0, wx.EXPAND|wx.ALL,       5)
        self.sSizer.Add(self.sBtnSizer, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        #------------------------------>
        self.sSizer.Hide(self.sImpNorm, recursive=True)
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind
        self.wIFile.wTc.Bind(wx.EVT_TEXT, self.OnIFileLoad)
        self.wImputationMethod.wCb.Bind(wx.EVT_COMBOBOX, self.OnImpMethod)
        #endregion -----------------------------------------------------> Bind

        #region -------------------------------------------------> Check Input
        self.rCheckUserInput = {
            self.cLuFile      : [self.wUFile.wTc,            mConfig.core.mFileBad  ,    False],
            self.cLiFile      : [self.wIFile.wTc,            mConfig.core.mFileBad  ,    False],
            self.cLId         : [self.wId.wTc,               mConfig.core.mValueBad ,    False],
            self.cLCeroTreat  : [self.wCeroB.wCb,            mConfig.core.mOptionBad,    False],
            self.cLTransMethod: [self.wTransMethod.wCb,      mConfig.core.mOptionBad,    False],
            self.cLNormMethod : [self.wNormMethod.wCb,       mConfig.core.mOptionBad,    False],
            self.cLImputation : [self.wImputationMethod.wCb, mConfig.core.mOptionBad,    False],
            self.cLShift      : [self.wShift.wTc,            mConfig.core.mOneRPlusNum , False],
            self.cLWidth      : [self.wWidth.wTc,            mConfig.core.mOneRPlusNum , False],
        }
        #endregion ----------------------------------------------> Check Input
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Event Methods
    def OnIFileLoad(self, event: Union[wx.CommandEvent, str]) -> bool:          # pylint: disable=unused-argument
        """Clear GUI elements when Data Folder is ''.

            Parameters
            ----------
            event: wx.CommandEvent or str
                Information about the event.

            Return
            ------
            bool
        """
        if (fileP := self.wIFile.wTc.GetValue()) == '':
            return self.LCtrlEmpty()
        #------------------------------>
        return self.IFileEnter(fileP)
    #---

    def OnImpMethod(self, event: Union[wx.CommandEvent, str])-> bool:           # pylint: disable=unused-argument
        """Show/Hide the Imputation options.

            Parameters
            ----------
            event: wx.CommandEvent or str
                Information about the event.

            Returns
            -------
            bool
        """
        if self.wImputationMethod.wCb.GetValue() == 'Normal Distribution':
            self.sSizer.Show(self.sImpNorm, show=True, recursive=True)
            self.sSizer.Layout()
            self.SetupScrolling()
        else:
            self.sSizer.Show(self.sImpNorm, show=False, recursive=True)
            self.wShift.wTc.SetValue(self.cValShift)
            self.wWidth.wTc.SetValue(self.cValWidth)
            self.sSizer.Layout()
            self.SetupScrolling()
        #------------------------------>
        return True
    #---

    def OnClear(self, event: wx.CommandEvent) -> bool:
        """Clear all input, including the Imputation options.

            Parameters
            ----------
            event: wx.CommandEvent
                Information about the event.

            Returns
            -------
            bool
        """
        super().OnClear(event)
        self.OnImpMethod('fEvent')
        #------------------------------>
        return True
    #---
    #endregion ------------------------------------------------> Event Methods

    #region ---------------------------------------------------> Class Methods
    def LCtrlEmpty(self) -> bool:
        """Clear wx.ListCtrl and NCol.

            Returns
            -------
            bool

            Notes
            -----
            Helper function to accommodate several wx.ListCtrl in the panel.
        """
        #region -------------------------------------------------> Delete list
        for l in self.rLCtrlL:
            l.DeleteAllItems()
        #endregion ----------------------------------------------> Delete list

        #region ---------------------------------------------------> Set NCol
        self.rNCol = None
        #endregion ------------------------------------------------> Set NCol

        return True
    #---

    def IFileEnter(self, fileP: Union[Path, str]) -> bool:
        """Fill the wx.ListCtrl after selecting path to the input file.

            Parameters
            ----------
            fileP : Path
                Folder path

            Notes
            -----
            Silently ignores the absence of a wx.ListCtrl as self.lbI
        """
        #region -----------------------------------------------> Check for lbI
        if self.wLCtrlI is None:
            return True
        #endregion --------------------------------------------> Check for lbI

        #region ----------------------------------------------------> Del list
        self.LCtrlEmpty()
        #endregion -------------------------------------------------> Del list

        #region ---------------------------------------------------> Fill list
        try:
            cMethod.LCtrlFillColNames(self.wLCtrlI, fileP)
        except Exception as e:
            cWindow.Notification(
                'errorF', parent=self, msg=str(e), tException=e)
            self.wIFile.wTc.SetValue('')
            return False
        #endregion ------------------------------------------------> Fill list

        #region -----------------------------------------> Columns in the file
        self.rNCol = self.wLCtrlI.GetItemCount() - 1
        #endregion --------------------------------------> Columns in the file

        return True
    #---

    def EqualLenLabel(self, label: str) -> str:
        """Add empty space to the end of label to match the length of
            self.rLLenLongest.

            Parameters
            ----------
            label : str
                Original label

            Returns
            -------
            str
                Label with added empty strings at the end to match the length of
                self.rLLenLongest

            Notes
            -----
            It assumes child class defines a self.rLLenLongest with the length
            of the longest name for the input fields.
        """
        return f"{label}{(self.rLLenLongest - len(label))*' '}"
    #---

    def SetStepDictDP(self) -> dict:
        """Set the Data Processing part of the stepDict to write in the output.

            Returns
            -------
            dict
        """
        #region --------------------------------------------------->
        stepDict = {
            'DP': {
                mConfig.core.ltDPKeys[0] : mConfig.core.fnFloat.format(self.rDate, '02'),
                mConfig.core.ltDPKeys[1] : mConfig.core.fnTrans.format(self.rDate, '03'),
                mConfig.core.ltDPKeys[2] : mConfig.core.fnNorm.format(self.rDate, '04'),
                mConfig.core.ltDPKeys[3] : mConfig.core.fnImp.format(self.rDate, '05'),
            },
        }
        #endregion ------------------------------------------------>

        return stepDict
    #---

    def SetStepDictDPFileR(self) -> dict:
        """Set the Data Processing, Files & Results parts of the stepDict to
            write in the output.

            Returns
            -------
            dict
        """
        #region --------------------------------------------------->
        stepDict = {
            'DP': {
                mConfig.core.ltDPKeys[0] : mConfig.core.fnFloat.format(self.rDate, '02'),
                mConfig.core.ltDPKeys[1] : mConfig.core.fnTrans.format(self.rDate, '03'),
                mConfig.core.ltDPKeys[2] : mConfig.core.fnNorm.format(self.rDate, '04'),
                mConfig.core.ltDPKeys[3] : mConfig.core.fnImp.format(self.rDate, '05'),
            },
            'Files' : {
                mConfig.core.fnInitial.format(self.rDate, '01')   : self.dfI,
                mConfig.core.fnFloat.format(self.rDate, '02')     : self.dfF,
                mConfig.core.fnTrans.format(self.rDate, '03')     : self.dfT,
                mConfig.core.fnNorm.format(self.rDate, '04')      : self.dfN,
                mConfig.core.fnImp.format(self.rDate, '05')       : self.dfIm,
                mConfig.core.fnTargetProt.format(self.rDate, '06'): self.dfTP,
                mConfig.core.fnExclude.format(self.rDate, '07')   : self.dfE,
                mConfig.core.fnScore.format(self.rDate, '08')     : self.dfS,
                self.rMainData.format(self.rDate, '09')     : self.dfR,
            },
            'R' : self.rMainData.format(self.rDate, '09'),
        }
        #endregion ------------------------------------------------>

        return stepDict
    #---

    def SetOutputDict(self, dateDict) -> dict:
        """Creates the output dictionary to be written to the output file.

            Parameters
            ----------
            dateDict : dict
                {
                    date : {
                        'V' : config.dictVersion,
                        'I' : self.d,
                        'CI': dtsMethod.DictVal2Str(
                            self.do, self.changeKey, new=True,
                        ),
                        'R' : Results,
                    }
                }

            Return
            ------
            dict
                Output data as a dict

            Notes
            -----
            If the output file already exists the new data is added to the
            existing data in the corresponding section.
            It assumes child class defines a self.cSection attributes with the
            section name of the analysis.
        """
        #region ---------------------------------------------------> Read File
        if self.rDO['uFile'].exists():
            try:
                outData = cFile.ReadJSON(self.rDO['uFile'])
            except Exception as e:
                msg = mConfig.core.mFileRead.format(self.rDO['uFile'])
                raise RuntimeError(msg) from e
        else:
            outData = {}
        #endregion ------------------------------------------------> Read File

        #region ------------------------------------------------> Add new data
        if outData.get(self.cSection, False):
            outData[self.cSection][self.rDateID] = dateDict[self.rDateID]
        else:
            outData[self.cSection] = dateDict
        #endregion ---------------------------------------------> Add new data

        return outData
    #---

    def WriteOutputData(self, stepDict: dict) -> bool:
        """Write output.

            Parameters
            ----------
            stepDict : dict
                Dict with the data to write the step by step data files
                Keys are file names and values pd.DataFrame with the values

            Return
            ------
            bool
        """
        #region -----------------------------------------------> Create folder
        #------------------------------>
        msgStep = self.cLPdWrite + 'Creating needed folders, Data-Steps folder'
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        dataFolder = f"{self.rDate}_{self.cSection.replace(' ', '-')}"
        dataFolder = self.rOFolder / mConfig.core.fnDataSteps / dataFolder      # type: ignore
        dataFolder.mkdir(parents=True, exist_ok=True)
        #------------------------------>
        msgStep = self.cLPdWrite + 'Creating needed folders, Data-Initial folder'
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        dataInit = self.rOFolder / mConfig.core.fnDataInit                      # type: ignore
        dataInit.mkdir(parents=True, exist_ok=True)
        #endregion --------------------------------------------> Create folder

        #region ------------------------------------------------> Data Initial
        msgStep = self.cLPdWrite + 'Data files, Input Data'
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        #------------------------------>
        puFolder = self.rDO['uFile'].parent / mConfig.core.fnDataInit
        #------------------------------>
        for k,v in self.rCopyFile.items():
            if self.rDI[self.EqualLenLabel(v)] != '':
                #------------------------------>
                piFolder = self.rDO[k].parent
                #------------------------------>
                if not piFolder == puFolder:
                    #------------------------------>
                    tStem = self.rDO[k].stem.replace(' ', '-')
                    tStem = tStem.replace('_', '-')
                    name = f"{self.rDate}_{tStem}{self.rDO[k].suffix}"
                    file = puFolder/name
                    #------------------------------>
                    shutil.copy(self.rDO[k], file)
                    #------------------------------>
                    self.rDI[self.EqualLenLabel(v)] = str(file.name)
                    #------------------------------>
                    self.rDFile.append(file)
                else:
                    #------------------------------>
                    self.rDI[self.EqualLenLabel(v)] = str(self.rDO[k].name)
                    #------------------------------>
                    self.rDFile.append(self.rDO[k])
            else:
                self.rDFile.append('')
        #endregion ---------------------------------------------> Data Initial

        #region --------------------------------------------------> Data Steps
        msgStep = self.cLPdWrite + 'Data files, Output Data'
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        try:
            cFile.WriteDFs2CSV(dataFolder, stepDict['Files'])
        except Exception as e:
            self.rMsgError = ('It was not possible to create the files with '
                'the data for the intermediate steps of the analysis.')
            self.rException = e
            return False
        #endregion -----------------------------------------------> Data Steps

        #region --------------------------------------------> Further Analysis
        if (aaDict := stepDict.get('AA', False)):
            fileP = dataFolder/aaDict[f'{self.rDate}_{self.rDO["AA"]}']         # type: ignore
            cFile.WriteDF2CSV(fileP, self.dfAA)                                 # type: ignore
        else:
            pass

        if (histDict := stepDict.get('Hist', False)):
            fileP = dataFolder/histDict[f'{self.rDate}_{self.rDO["Hist"]}']     # type: ignore
            cFile.WriteDF2CSV(fileP, self.dfHist)                               # type: ignore
        else:
            pass

        if (fileN := stepDict.get('CpR', False)):
            fileP = dataFolder/fileN
            cFile.WriteDF2CSV(fileP, self.dfCpR)                                # type: ignore
        else:
            pass

        if (fileN := stepDict.get('CEvol', False)):
            fileP = dataFolder/fileN
            cFile.WriteDF2CSV(fileP, self.dfCEvol)                              # type: ignore
        else:
            pass
        #endregion -----------------------------------------> Further Analysis

        #region --------------------------------------------------> UMSAP File
        msgStep = self.cLPdWrite + 'Main file'
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        #------------------------------> Create output dict
        dateDict = {
            self.rDateID : {
                'V' : mConfig.core.dictVersion,
                'I' : self.rDI,
                'CI': cMethod.DictVal2Str(self.rDO, self.rChangeKey, new=True),
                'DP': {
                    mConfig.core.ltDPKeys[0] : stepDict['DP'][mConfig.core.ltDPKeys[0]],
                    mConfig.core.ltDPKeys[1] : stepDict['DP'][mConfig.core.ltDPKeys[1]],
                    mConfig.core.ltDPKeys[2] : stepDict['DP'][mConfig.core.ltDPKeys[2]],
                    mConfig.core.ltDPKeys[3] : stepDict['DP'][mConfig.core.ltDPKeys[3]],
                },
            }
        }
        #--------------> DataPrep Util does not have dfR
        if not self.dfR.empty:
            dateDict[self.rDateID]['R'] = stepDict['R']
        else:
            pass
        #-------------->
        if self.cName == mConfig.prot.nPane:
            #--------------> Filters in ProtProf
            dateDict[self.rDateID]['F'] = {}
        elif self.cName == mConfig.tarp.nPane:
            #--------------> TarProt
            dateDict[self.rDateID]['CpR'] = stepDict['CpR']
            dateDict[self.rDateID]['CEvol'] = stepDict['CEvol']
        else:
            pass
        #--------------> Further Analysis
        if stepDict.get('AA', None) is not None:
            dateDict[self.rDateID]['AA'] = stepDict['AA']
        else:
            pass
        if stepDict.get('Hist', None) is not None:
            dateDict[self.rDateID]['Hist'] = stepDict['Hist']
        else:
            pass
        #------------------------------> Append or not
        try:
            outData = self.SetOutputDict(dateDict)
        except Exception as e:
            self.rMsgError = ('It was not possible to create the dictionary '
                'with the UMSAP data.')
            self.rException = e
            return False
        #------------------------------> Write
        try:
            cFile.WriteJSON(self.rDO['uFile'], outData)
        except Exception as e:
            self.rMsgError = ('It was not possible to create the dictionary '
                'with the UMSAP data.')
            self.rException = e
            return False
        #endregion -----------------------------------------------> UMSAP File

        return True
    #---
    #endregion ------------------------------------------------> Class Methods

    #region ----------------------------------------------------> Run Analysis
    def OnRun(self, event: wx.CommandEvent) -> bool:
        """Start analysis of the module/utility.

            Parameter
            ---------
            event : wx.Event
                Event information.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------> Dlg window
        self.rDlg = cWindow.Progress(                                     # pylint: disable=attribute-defined-outside-init
            mConfig.main.mainWin, self.cTitlePD, self.cGaugePD)
        #endregion -----------------------------------------------> Dlg window

        #region ------------------------------------------------------> Thread
        _thread.start_new_thread(self.Run, ('test',))
        #endregion ---------------------------------------------------> Thread

        #region ----------------------------------------> Show progress dialog
        self.rDlg.ShowModal()
        self.rDlg.Destroy()
        #endregion -------------------------------------> Show progress dialog

        return True
    #---

    def CheckInput(self) -> bool:
        """Check individual fields in the user input.

            Returns
            -------
            bool

            Notes
            -----
            BaseErrorMessage must be a string with two placeholder for the
            error value and Field label in that order. For example:
            'File: {bad_path_placeholder}\n cannot be used as
                                                    {Field_label_placeholder}'

            The child class must define a rCheckUserInput dict with the correct
            order for the checking process.

            rCheckUserInput = {'Field label':[Widget, BaseErrorMessage, Bool],}

            The child class must define a rCheckUnique list with the wx.TextCtrl
            that must hold unique column numbers.
        """
        #region -------------------------------------------------------> Check
        for k,v in self.rCheckUserInput.items():
            #------------------------------>
            msgStep = self.cLPdCheck + k
            wx.CallAfter(self.rDlg.UpdateStG, msgStep)
            #------------------------------>
            if v[2]:
                a, b = v[0].GetValidator().Validate(vMax=self.rNCol)
            else:
                a, b = v[0].GetValidator().Validate()
            #------------------------------>
            if not a:
                self.rMsgError = cMethod.StrSetMessage(
                    v[1].format(b[1], k), b[2])
                return False
        #endregion ----------------------------------------------------> Check

        #region ---------------------------------------> Unique Column Numbers
        if self.rCheckUnique:
            msgStep = self.cLPdCheck + 'Unique Column Numbers'
            wx.CallAfter(self.rDlg.UpdateStG, msgStep)
            #------------------------------>
            a, b = cCheck.TcUniqueColNumbers(self.rCheckUnique)
            if not a:
                msg = mConfig.core.mSection.format(self.cLColumnBox)
                self.rMsgError = cMethod.StrSetMessage(msg, b[2])               # type: ignore
                return False
        #endregion ------------------------------------> Unique Column Numbers

        return True
    #---

    def PrepareRun(self) -> bool:
        """Set variable and prepare data for analysis.

            Returns
            -------
            bool
        """
        #------------------------------> Date
        self.rDate = cMethod.StrNow()
        #------------------------------> Output folder
        if self.rDO['uFile'].exists():
            self.rOFolder = self.rDO['uFile'].parent
        else:
            folder = self.rDO['uFile'].parent
            step = folder/mConfig.core.fnDataSteps
            init = folder/mConfig.core.fnDataInit
            #------------------------------>
            if step.exists() or init.exists():
                self.rOFolder = folder/f'{self.rDate}'
                self.rDO['uFile'] = self.rOFolder/self.rDO['uFile'].name
            else:
                self.rOFolder = self.rDO['uFile'].parent
        #------------------------------> DateID
        self.rDateID = f'{self.rDate} - {self.rDO["ID"]}'
        #------------------------------> Remove Shift & Width if not needed
        if self.wImputationMethod.wCb.GetValue() == 'Normal Distribution':
            pass
        else:
            del self.rDI[self.EqualLenLabel(self.cLShift)]
            del self.rDI[self.EqualLenLabel(self.cLWidth)]

        return True
    #---

    def ReadInputFiles(self) -> bool:
        """Read input file and check data.

            Return
            ------
            bool

            Notes
            -----
            Assumes child class has the following attributes:
            - rDO: dict with at least the following key - values:
                {
                    'iFile' : Path to data file,
                    'seqFile' : Path to the sequence file or no key - value,
                }
        """
        #region ---------------------------------------------------> Data file
        #------------------------------>
        msgStep = self.cLPdReadFile + f"{self.cLiFile}, reading"
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        #------------------------------>
        try:
            self.rIFileObj = cFile.CSVFile(self.rDO['iFile'])
        except Exception as e:
            self.rMsgError = mConfig.core.mFileRead.format(self.rDO['iFile'])
            self.rException = e
            return False
        #------------------------------> Check Target Protein. It cannot be done
        # before this step
        if 'TargetProt' in self.rDO:
            a = self.rIFileObj.StrInCol(
                self.rDO['TargetProt'], self.rDO['oc']['TargetProtCol'])
            if not a:
                self.rMsgError = (f'The Target Protein '
                    f'({self.rDO["TargetProt"]}) was not found in the '
                    f'{self.cLDetectedProt} column '
                    f'({self.rDO["oc"]["TargetProtCol"]}).')
                return False
        #endregion ------------------------------------------------> Data file

        #region ------------------------------------------------> Seq Rec File
        if 'seqFile' in self.rDO:
            #------------------------------>
            msgStep = self.cLPdReadFile + f"{self.cLSeqFile}, reading"
            wx.CallAfter(self.rDlg.UpdateStG, msgStep)
            #------------------------------>
            try:
                self.rSeqFileObj = cFile.FastaFile(self.rDO['seqFile'])
            except Exception as e:
                self.rMsgError = mConfig.core.mFileRead.format(self.rDO['seqFile'])
                self.rException = e
                return False
            #------------------------------>
            try:
                ProtLoc = self.rSeqFileObj.GetNatProtLoc()
            except Exception:
                ProtLoc = (None, None)
            #------------------------------>
            self.rDO['ProtLength'] = [
                self.rSeqFileObj.rSeqLengthRec, self.rSeqFileObj.rSeqLengthNat]
            self.rDO['ProtLoc'] = ProtLoc
            #------------------------------>
            try:
                ProtDelta = self.rSeqFileObj.GetSelfDelta()
            except Exception:
                ProtDelta = None
            #------------------------------>
            self.rDO['ProtDelta'] = ProtDelta
        #endregion ---------------------------------------------> Seq Rec File

        #region ---------------------------------------------------> Print Dev
        if mConfig.core.development and self.rSeqFileObj is not None:
            print("Rec Seq: ", self.rSeqFileObj.rSeqRec)
            print("Nat Seq: ", self.rSeqFileObj.rSeqNat)
        #endregion ------------------------------------------------> Print Dev

        return True
    #---

    def RunAnalysis(self) -> bool:
        """Run the analysis of the module.

            Returns
            -------
            bool
        """
        #region -------------------------------------------------------> Print
        if mConfig.core.development:
            print('RunAnalysis')
            print('d:')
            for k,v in self.rDI.items():
                print(str(k)+': '+str(v))
            print('')
            print('do:')
            for k,v in self.rDO.items():
                if k not in ['df', 'oc', 'dfo']:
                    print(str(k)+': '+str(v))
                else:
                    print(k)
                    for j,w in v.items():
                        print(f'\t{j}: {w}')
            print('')
        #endregion ----------------------------------------------------> Print

        #region ----------------------------------------------------> Analysis
        msgStep = self.cLPdRun + self.cLPdRunText
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        #------------------------------>
        dfDict, self.rMsgError, self.rException = ANALYSIS_METHOD[self.cName](
            self.rIFileObj.rDf, self.rDO, self.rDExtra)                         # type: ignore
        #------------------------------>
        if dfDict:
            for k,v in dfDict.items():
                setattr(self, k, v)
        else:
            return False
        #endregion -------------------------------------------------> Analysis

        return True
    #---

    def WriteOutput(self) -> bool:
        """Write output for a module

            Returns
            -------
            bool
        """
        #region --------------------------------------------------> Data Steps
        stepDict = self.SetStepDictDPFileR()
        #endregion -----------------------------------------------> Data Steps

        return self.WriteOutputData(stepDict)
    #---

    def LoadResults(self) -> bool:
        """Load output file.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------------> Load
        wx.CallAfter(self.rDlg.UpdateStG, self.cLPdLoad)
        #------------------------------>
        # wx.CallAfter(gMethod.LoadUMSAPFile, fileP=self.rDO['uFile'])
        #endregion -----------------------------------------------------> Load

        return True
    #---

    def RunEnd(self) -> bool:
        """Restart GUI and needed variables.

            Returns
            -------
            bool
        """
        #region ---------------------------------------> Dlg progress dialogue
        if not self.rMsgError:
            self.rDFile.append(self.rDO['uFile'])
            self.rDlg.SuccessMessage(
                self.cLPdDone, eTime=f"{self.cLPdElapsed} {self.rDeltaT}")
        else:
            self.rDlg.ErrorMessage(
                self.cLPdError,error=self.rMsgError,tException=self.rException)
        #endregion ------------------------------------> Dlg progress dialogue

        #region -------------------------------------------------------> Reset
        self.rMsgError  = '' # Error msg to show in self.RunEnd
        self.rException = None # Exception
        self.rDI        = {} # Dict with the user input as given
        self.rDO        = {} # Dict with the processed user input
        self.dfI        = pd.DataFrame() # pd.DataFrame for initial, normalized
        self.dfF        = pd.DataFrame() # etc
        self.dfTP       = pd.DataFrame()
        self.dfE        = pd.DataFrame()
        self.dfS        = pd.DataFrame()
        self.dfT        = pd.DataFrame()
        self.dfN        = pd.DataFrame()
        self.dfIm       = pd.DataFrame()
        self.dfR        = pd.DataFrame()
        self.rDate      = '' # date for corr file
        self.rDateID    = ''
        self.rOFolder   = None # folder for output
        self.rIFileObj  = None
        self.rDeltaT    = ''

        if self.rDFile:
            self.wUFile.wTc.SetValue(str(self.rDFile[-1]))
            self.wIFile.wTc.SetValue(str(self.rDFile[0]))
            self.rDFile = []
        else:
            pass
        #endregion ----------------------------------------------------> Reset

        return True
    #---
    #endregion -------------------------------------------------> Run Analysis
#---
#endregion ----------------------------------------------------------> Classes
