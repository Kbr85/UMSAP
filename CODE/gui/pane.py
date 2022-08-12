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


"""Panels of the application"""


#region -------------------------------------------------------------> Imports
import _thread
import shutil
from collections import namedtuple
from math import ceil
from pathlib import Path
from typing import Union, Optional

import numpy as np
import pandas as pd
from statsmodels.stats.multitest import multipletests

import wx
import wx.lib.scrolledpanel as scrolled

import config.config as mConfig
import data.check as mCheck
import data.method as mMethod
import data.exception as mException
import data.file as mFile
import data.statistic as mStatistic
import gui.method as gMethod
import gui.validator as mValidator
import gui.widget as mWidget
import gui.window as mWindow
#endregion ----------------------------------------------------------> Imports


#region --------------------------------------------------------> Base Classes
class BaseConfPanel(
    scrolled.ScrolledPanel,
    mWidget.StaticBoxes, 
    mWidget.ButtonOnlineHelpClearAllRun
    ):
    """Creates the skeleton of a configuration panel. This includes the 
        wx.StaticBox, the bottom Buttons, the statusbar and some widgets.

        Parameters
        ----------
        parent : wx Widget
            Parent of the widgets
        rightDelete : Boolean
            Enables clearing wx.StaticBox input with right click

        Attributes
        ----------
        dDataPrep: dict
            Keys are the messages for the Progress Dialog, values are the 
            methods to run the Data Preparation steps. See self.DataPreparation.
        dfI : pd.DataFrame
            DataFrame for the initial values.
        dfF : pd.DataFrame
            DataFrame as float values and 0 and '' as np.nan
        dfT : pd.DataFrame
            DataFrame with the transformed values.
        dfN : pd.DataFrame
            DataFrame with normalized values.
        dfIm : pd.DataFrame
            DataFrame with imputed values.
        dfTP : pd.DataFrame
            DataFrame filtered by Target Protein
        dfE : DataFrame
            Exclude some entries by some parameters
        dfS : DataFrame
            Exclude entries by Score values.
        dfR : pd.DataFrame
            DataFrame with the results values.
        rChangeKey : list of str
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
        rDate : str or None
            Date for the new section in the umsap file.
        rDateID : str or None
            Date + Analysis ID
        rDeltaT: str
            Elapsed analysis time.
        rDFile : list[Path]
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
            Exception raised during analysis   
        rIFileObj: dtsFF.CSVFile or none
            Input Data File Object
        rLCtrlL: list of wx.ListCtrl
            To clear all wx.ListCtrl in the Tab.
        rLLenLongest: int
            Length of longest label.
        rMainData: str
            Name of the file containing the main output data.
        rMsgError: Str or None
            Error message to show when analysis fails
        rNCol: int
            Number of columns in the main input file - 1. Set when the file is
            read.
        rOFolder: Path or None
            Folder to contain the output. Set based on the umsap file path.
        rSeqFileObj: dtsFF.FastaFile
            Object to work with the sequences of the proteins.
    """
    #region --------------------------------------------------> Instance setup
    def __init__(self, parent: wx.Window, rightDelete: bool=True) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.cParent = parent
        #------------------------------> 
        self.cName    = getattr(self, 'cName', mConfig.npDef)
        self.cSection = getattr(self, 'cSection', 'Default Section')
        #------------------------------> For the Progress Dialog
        self.cTitlePD = getattr(self, 'cTitlePD', 'Default Title')
        self.cGaugePD = getattr(self, 'cGaugePD', 50)
        #------------------------------> Labels
        self.cLFileBox     = getattr(self, 'cLFileBox',      'Files')
        self.cLDataBox     = getattr(self, 'cLDataBox',      'Data Preparation')
        self.cLValueBox    = getattr(self, 'cLValueBox',  'User-defined Values')
        self.cLColumnBox   = getattr(self, 'cLColumnBox',    'Column Numbers')
        self.cLuFile       = getattr(self, 'cLuFile',        'UMSAP')
        self.cLiFile       = getattr(self, 'cLiFile',        'Data')
        self.cLId          = getattr(self, 'cLId',           'Analysis ID')
        self.cLCeroTreatD  = getattr(self, 'cLCeroTreatD',   '0s Missing')
        self.cLNormMethod  = getattr(self, 'cLNormMethod',   'Normalization')
        self.cLTransMethod = getattr(self, 'cLTransMethod',  'Transformation')
        self.cLImputation  = getattr(self, 'cLImputation',   'Imputation')
        self.cLShift       = getattr(self, 'cLShift',        'Shift')
        self.cLWidth       = getattr(self, 'cLWidth',        'Width')
        self.cLDetectedProt = getattr(self, 'cLDetectedProt','')
        self.cLSeqFile     = getattr(self, 'cLSeqFile',      '')
        self.cLCeroTreat   = getattr(
            self, 'cLCeroTreat', 'Treat 0s as missing values')
        #------------------------------> For Progress Dialog
        self.cLPdCheck    = getattr(self, 'cLPdCheck',  'Checking user input: ')
        self.cLPdPrepare  = getattr(self, 'cLPdPrepare', 'Preparing analysis: ')
        self.cLPdRun      = getattr(self, 'cLPdRun',     'Running analysis: ')
        self.cLPdWrite    = getattr(self, 'cLPdWrite',   'Writing output: ')
        self.cLPdLoad     = getattr(self, 'cLPdLoad',    'Loading output file')
        self.cLPdError    = getattr(self, 'cLPdError',   mConfig.lPdError)
        self.cLPdDone     = getattr(self, 'cLPdDone',    'All Done')
        self.cLPdElapsed  = getattr(self, 'cLPdElapsed', 'Elapsed time: ')
        self.cLPdReadFile = getattr(
            self, 'cLPdReadFile', 'Reading input files: ')
        #------------------------------> Size
        self.cSTc = getattr(self, 'cSTc', mConfig.sTc)
        #------------------------------> Choices
        self.cOCero = getattr(self, 'cOCero', list(mConfig.oYesNo.keys()))
        self.cONorm = getattr(self, 'cONorm', list(mConfig.oNormMethod.keys()))
        self.cOTrans = getattr(
            self, 'cOTrans', list(mConfig.oTransMethod.keys()))
        self.cOImputation = getattr(
            self, 'cOImputation', list(mConfig.oImputation.keys()))
        #------------------------------> Hints
        self.cHuFile = getattr(
            self, 'cHuFile', f"Path to the {self.cLuFile} file")
        self.cHiFile = getattr(
            self, 'cHiFile', f"Path to the {self.cLiFile} file")
        self.cHId    = getattr(self, 'cHId', 'e.g. HIV inhibitor')
        #------------------------------> Tooltips
        self.cTTRun = getattr(self, 'cTTRun', 'Start the analysis.')
        self.cTTHelp = getattr(
            self, 'cTTHelp', f'Read online tutorial at {mConfig.urlHome}.')
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
        self.cTTShift = getattr(self, 'cTTShift', (f'Factor to shift the '
            f'center of the normal distribution used to replace missing. '
            f'values\ne.g. 1.8'))
        self.cTTWidth = getattr(self, 'cTTWidth', (f'Factor to control the '
            f'width of the normal distribution used to replace missing. '
            f'values\ne.g. 0.3'))
        #------------------------------> URL
        self.cURL = getattr(self, 'cURL', mConfig.urlTutorial)
        #------------------------------> Extensions
        self.cEiFile = getattr(self, 'ciFileE', mConfig.elData)
        #------------------------------> Validator
        self.cVuFile = getattr(self, 'cVuFile', mValidator.OutputFF(fof='file'))
        self.cViFile = getattr(self, 'cViFile', mValidator.InputFF(fof='file'))
        #------------------------------> Values
        self.cValShift = mConfig.values[mConfig.nwCheckDataPrep]['Shift']
        self.cValWidth = mConfig.values[mConfig.nwCheckDataPrep]['Width']
        #------------------------------> To handle Data Preparation Steps
        self.dDataPrep = { # Keys are the messaging for the Progress Dialog
            "Setting Data Types"         : self.DatPrep_Float,
            "Data Transformation"        : self.DatPrep_Transformation,
            "Data Normalization"         : self.DatPrep_Normalization,
            "Data Imputation"            : self.DatPrep_Imputation,
            "Filter Data: Target Protein": self.DatPrep_TargetProt,
            "Filter Data: Exclude Rows"  : self.DatPrep_Exclude,
            "Filter Data: Score Value"   : self.DatPrep_Score,
        }
        #------------------------------> This is needed to handle Data File 
        # content load to the wx.ListCtrl in Tabs with multiple panels
        #--------------> Default wx.ListCtrl to load data file content
        self.wLCtrlI = None 
        #--------------> List to use just in case there are more than 1
        self.rLCtrlL = []
        #------------------------------> Needed to Run the Analysis
        self.rCheckUnique = []
        self.rLLenLongest = getattr(self, 'rLLenLongest', 0)
        self.rMainData = getattr(self, 'rMainData', '')
        #--------------> Dict with the user input as given
        self.rDI = {}
        #--------------> Dict with the processed user input
        self.rDO = {} 
        #--------------> Error message and exception to show in self.RunEnd
        self.rMsgError  = ''
        self.rException = None
        #--------------> pd.DataFrames for:
        self.dfI  = pd.DataFrame() # Initial and
        self.dfF  = pd.DataFrame() # Data as float and 0 and '' values as np.nan
        self.dfT  = pd.DataFrame() # Transformed values
        self.dfN  = pd.DataFrame() # Normalized Values
        self.dfIm = pd.DataFrame() # Imputed values
        self.dfTP = pd.DataFrame() # Select Target Protein
        self.dfE  = pd.DataFrame() # Exclude entries by some parameter
        self.dfS  = pd.DataFrame() # Exclude entries by Score value
        self.dfR  = pd.DataFrame() # Results values
        #--------------> Date for umsap file
        self.rDate = ''
        self.rDateID = ''
        #--------------> folder for output
        self.rOFolder = None
        #--------------> input file for directing repeating analysis from
        # file copied to oFolder
        self.rDFile   = []
        # #--------------> Obj for files
        self.rIFileObj   = None
        self.rSeqFileObj: Optional[mFile.FastaFile] = None
        #------------------------------> 
        self.rChangeKey = getattr(self, 'rChangeKey', ['iFile', 'uFile'])
        #------------------------------> 
        self.rCopyFile = getattr(self, 'rCopyFile', {'iFile':self.cLiFile})
        #------------------------------> Parent init
        scrolled.ScrolledPanel.__init__(self, parent, name=self.cName)

        mWidget.ButtonOnlineHelpClearAllRun.__init__(
            self,
            self,
            self.cURL,
            tooltipR = self.cTTRun,
            tooltipH = self.cTTHelp,
            tooltipC = self.cTTClearAll,
        )

        mWidget.StaticBoxes.__init__(
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
        self.wUFile = mWidget.ButtonTextCtrlFF(
            self.wSbFile,
            btnLabel   = self.cLuFile,
            btnTooltip = self.cTTuFile,
            tcHint     = self.cHuFile,
            mode       = 'save',
            ext        = mConfig.elUMSAP,
            tcStyle    = wx.TE_READONLY,
            validator  = self.cVuFile,
            ownCopyCut = True,
        )
        self.wIFile = mWidget.ButtonTextCtrlFF(
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
        self.wId = mWidget.StaticTextCtrl(
            self.wSbFile,
            stLabel   = self.cLId,
            stTooltip = self.cTTId,
            tcHint    = self.cHId,
            validator = mValidator.IsNotEmpty(),
        )
        self.wCeroB = mWidget.StaticTextComboBox(
            self.wSbData,
            label   = self.cLCeroTreat,
            choices = self.cOCero,
            tooltip = (f'Cero values in the {self.cLiFile} file will '
            f'be treated as missing values when this option is set to Yes and '
            f'as real values when the option is set to No.'),
            validator = mValidator.IsNotEmpty(),
        )
        self.wNormMethod = mWidget.StaticTextComboBox(
            self.wSbData, 
            label     = self.cLNormMethod,
            choices   = self.cONorm,
            tooltip   = self.cTTNormMethod,
            validator = mValidator.IsNotEmpty(),
        )
        self.wTransMethod = mWidget.StaticTextComboBox(
            self.wSbData, 
            label     = self.cLTransMethod,
            choices   = self.cOTrans,
            tooltip   = self.cTTTransMethod,
            validator = mValidator.IsNotEmpty(),
        )
        self.wImputationMethod = mWidget.StaticTextComboBox(
            self.wSbData, 
            label     = self.cLImputation,
            choices   = self.cOImputation,
            tooltip   = self.cTTImputation,
            validator = mValidator.IsNotEmpty(),
        )
        self.wShift = mWidget.StaticTextCtrl(
            self.wSbData,
            stLabel   = self.cLShift,
            stTooltip = self.cTTShift,
            tcSize    = (60,22),
            tcHint    = f'e.g. {self.cValShift}',
            validator = mValidator.NumberList('float', nN=1, vMin=0),
        )
        self.wWidth = mWidget.StaticTextCtrl(
            self.wSbData,
            stLabel   = self.cLWidth,
            stTooltip = self.cTTWidth,
            tcSize    = (60,22),
            tcHint    = f'e.g. {self.cValWidth}',
            validator = mValidator.NumberList('float', nN=1, vMin=0),
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
            self.cLuFile      : [self.wUFile.wTc,            mConfig.mFileBad  ,    False],
            self.cLiFile      : [self.wIFile.wTc,            mConfig.mFileBad  ,    False],
            self.cLId         : [self.wId.wTc,               mConfig.mValueBad ,    False],
            self.cLCeroTreat  : [self.wCeroB.wCb,            mConfig.mOptionBad,    False],
            self.cLTransMethod: [self.wTransMethod.wCb,      mConfig.mOptionBad,    False],
            self.cLNormMethod : [self.wNormMethod.wCb,       mConfig.mOptionBad,    False],
            self.cLImputation : [self.wImputationMethod.wCb, mConfig.mOptionBad,    False],
            self.cLShift      : [self.wShift.wTc,            mConfig.mOneRPlusNum , False],
            self.cLWidth      : [self.wWidth.wTc,            mConfig.mOneRPlusNum , False],
        }
        #endregion ----------------------------------------------> Check Input
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Event Methods
    def OnIFileLoad(self, event: Union[wx.CommandEvent, str]) -> bool:
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
        else:
            return self.IFileEnter(fileP)
    #---

    def OnImpMethod(self, event: Union[wx.CommandEvent, str])-> bool:
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
        else:
            pass
        #endregion --------------------------------------------> Check for lbI

        #region ----------------------------------------------------> Del list
        self.LCtrlEmpty()
        #endregion -------------------------------------------------> Del list

        #region ---------------------------------------------------> Fill list
        try:
            mMethod.LCtrlFillColNames(self.wLCtrlI, fileP)
        except Exception as e:
            mWindow.DialogNotification(
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

    def DataPreparation(self, resetIndex=True) -> bool:
        """Perform the data preparation step.

            Parameters
            ----------
            resetIndex: bool
                If True reset the index of self.dfS.

            Returns
            -------
            bool
        """
        #region ----------------------------------------> Run Data Preparation
        for k, m in self.dDataPrep.items():
            #------------------------------> 
            wx.CallAfter(self.rDlg.UpdateStG, f'{self.cLPdRun} {k}')
            #------------------------------> 
            if m():
                pass
            else:
                return False
        #endregion -------------------------------------> Run Data Preparation

        #region -------------------------------------------------> Reset index
        if resetIndex:
            self.dfS.reset_index(drop=True, inplace=True)
        else:
            pass
        #endregion ----------------------------------------------> Reset index

        #region -------------------------------------------------------> Print
        if mConfig.development:
            #------------------------------> 
            dfL = [
                self.dfI, self.dfF, self.dfT, self.dfN, self.dfIm, 
                self.dfTP, self.dfE, self.dfS, 
            ]
            dfN = ['dfI', 'dfF', 'dfT', 'dfN', 'dfIm', 'dfTP', 'dfEx', 'dfS']
            #------------------------------> 
            print('')
            for i, df in enumerate(dfL):
                if df is not None:
                    print(f'{dfN[i]}: {df.shape}')
                else:
                    print(f'{dfN[i]}: None')
        else:
            pass
        #endregion ----------------------------------------------------> Print

        return True
    #---

    def DatPrep_Float(self) -> bool:
        """Convert or not 0s to NA and then all values to float.

            Returns
            -------
            bool

            Notes
            -----
            Assumes child class has the following attributes:
            - iFileObj: instance of mFile.CSVFile
            - rDO: dict with at least the following key - values pairs:
                'oc' : {
                    'Column' : [List of int],
                },
                'df' : {
                    'ColumnR' : [List of int],
                    'ColumnF' : [List of int],
                }
        """
        #region -----------------------------------------------------> Set dfI
        try:
            self.dfI = self.rIFileObj.rDf.iloc[:,self.rDO['oc']['Column']]      # type: ignore
        except Exception as e:
            self.rMsgError = mConfig.mPDGetInitCol.format(
                self.rDO['oc']['Column'], self.cLiFile, self.rDO['iFile'])
            self.rException = e
            return False
        #endregion --------------------------------------------------> Set dfI

        #region -----------------------------------------------------> Set dfF
        try:
            if self.rDO['Cero']:
                #------------------------------> Replace 0 and ''
                self.dfF = mMethod.DFReplace(
                    self.dfI, [0, ''], np.nan, sel=self.rDO['df']['ColumnR'])   # type: ignore
            else:
                #------------------------------> Replace only ''
                self.dfF = mMethod.DFReplace(
                    self.dfI, [''], np.nan, sel=self.rDO['df']['ColumnR'])      # type: ignore
            #------------------------------> Float
            self.dfF.iloc[:,self.rDO['df']['ColumnF']] = self.dfF.iloc[:,self.rDO['df']['ColumnF']].astype('float')
        except Exception as e:
            self.rMsgError = mConfig.mPDDataTypeCol.format(
                self.cLiFile, ", ".join(map(str, self.rDO['oc']['ColumnF'])))
            self.rException = e
            return False
        #endregion --------------------------------------------------> Set dfF

        return True
    #---

    def DatPrep_Transformation(self) -> bool:
        """Apply selected data transformation.

            Returns
            -------
            bool

            Notes
            -----
            Assumes child class has the following attributes:
            - rDO, dict with at least the following key - values pairs:
                'Cero' : bool, How to treat 0 values,
                'TransMethod': str, Transformation method name,
                'df' : {
                    'ResCtrlFlat' : [List of int],
                },
        """
        #region -----------------------------------------------------> Set rep
        if self.rDO['Cero']:
            rep = np.nan
        else:
            rep = 0
        #endregion --------------------------------------------------> Set rep

        #region ---------------------------------------------------> Transform
        try:
            self.dfT = mStatistic.DataTransformation(
                self.dfF, 
                self.rDO['df']['ResCtrlFlat'], 
                method = self.rDO['TransMethod'],
                rep    = rep,
            )
        except Exception as e:
            self.rMsgError   = 'Data Transformation failed.'
            self.rException = e
            return False 
        #endregion ------------------------------------------------> Transform

        return True
    #---

    def DatPrep_Normalization(self) -> bool:
        """Perform a data normalization.

            Returns
            -------
            bool

            Notes
            -----
            Assumes child class has the following attributes:
            - rDO, dict with at least the following key - values pairs:
                'NormMethod' : str Normalization method selected
                df : dict
                    {
                        'ResCtrlFlat' : list[int]
                    }
        """
        #region -----------------------------------------------> Normalization
        try:
            self.dfN = mStatistic.DataNormalization(
                self.dfT, 
                self.rDO['df']['ResCtrlFlat'], 
                method = self.rDO['NormMethod'],
            )
        except Exception as e:
            self.rMsgError   = 'Data Normalization failed.'
            self.rException = e
            return False
        #endregion --------------------------------------------> Normalization

        return True
    #---

    def DatPrep_Imputation(self) -> bool:
        """Perform a data imputation.

            Returns
            -------
            bool

            Notes
            -----
            Assumes child class has the following attributes:
            - rDO, dict with at least the following key - values pairs:
                'ImpMethod' : str Imputation method selected
                df : dict
                    {
                        'ResCtrlFlat' : list[int]
                    }
        """
        #region --------------------------------------------------> Imputation
        try:
            self.dfIm = mStatistic.DataImputation(
                self.dfN, 
                self.rDO['df']['ResCtrlFlat'],
                method = self.rDO['ImpMethod'],
                shift  = self.rDO['Shift'],
                width  = self.rDO['Width'],
            )
        except Exception as e:
            self.rMsgError   = 'Data Imputation failed.'
            self.rException = e
            return False
        #endregion -----------------------------------------------> Imputation

        return True
    #---

    def DatPrep_TargetProt(self) -> bool:
        """Filter data based on the value of Target Protein.

            Returns
            -------
            bool

            Notes
            -----
            Assumes child class has the following attributes:
            - rDO: dict with at least the following key - values pairs:
                'TargetProt' : str name of the Protein to select in the data
                'df' : {
                    'TargetProtCol' : int,
                }
        """
        #region -------------------------------------------------> Get Protein
        try:
            if self.rDO['df'].get('TargetProtCol', None) is not None:
                self.dfTP = mMethod.DFFilterByColS(
                    self.dfIm, 
                    self.rDO['df']['TargetProtCol'],
                    self.rDO['TargetProt'], 
                    'e',
                )
            else:
                self.dfTP = self.dfIm.copy()
        except Exception as e:
            self.rMsgError = mConfig.mPDDataTargetProt.format(
                self.rDO['TargetProt'], self.rDO['df']['TargetProtCol'])
            self.rException = e
            return False
        #endregion ----------------------------------------------> Get Protein

        return True
    #---

    def DatPrep_Exclude(self) -> bool:
        """Exclude rows from self.dfF based on the content of 
            self.do['df']['ExcludeR'].

            Returns
            -------
            bool

            Notes
            -----
            Assumes child class has the following attributes:
            - rDO: dict with at least the following key - values pairs:
                'df' : {
                    'ExcludeR' : [List of int],
                }
            - dfF: pd.DataFrame with correct data types in each column.

            Rows with at least one value different to NA in 
            self.do['df']['ExcludeR'] are discarded
        """
        #region -----------------------------------------------------> Exclude
        try:
            if self.rDO['df'].get('ExcludeR', None) is not None:
                self.dfE = mMethod.DFExclude(
                    self.dfTP, self.rDO['df']['ExcludeR'])
            else:
                self.dfE = self.dfTP.copy()
        except Exception as e:
            self.rMsgError = mConfig.mPDDataExclude.format(
                self.rDO['df']['ExcludeR'])
            self.rException = e
            return False
        #endregion --------------------------------------------------> Exclude

        return True
    #---

    def DatPrep_Score(self) -> bool:
        """Filter rows in self.dfE by Score values.

            Returns
            -------
            bool

            Notes
            -----
            Assumes child class has the following attributes
            - rDO: dict with at least the following key - values pairs:
                'ScoreVal' : float
                'df' : {
                    'ScoreCol' : int
                }
            - dfE: pd.DataFrame with correct data types in each column

            This is last filter applied. That is why the check for empty df is
            done here. 
        """
        #region ------------------------------------------------------> Filter
        try:
            if self.rDO['df'].get('ScoreCol', None) is not None:
                self.dfS = mMethod.DFFilterByColN(
                    self.dfE, 
                    [self.rDO['df']['ScoreCol']], 
                    self.rDO['ScoreVal'], 
                    'ge'
                )
            else:
                self.dfS = self.dfE.copy()
        except Exception as e:
            self.rMsgError = mConfig.mPDDataScore.format(
                self.rDO['df']['ScoreCol'])
            self.rException = e
            return False
        #endregion ---------------------------------------------------> Filter

        #region -----------------------> Check some Rows are left for Analysis
        if self.dfS.empty:
            self.rMsgError = mConfig.mNoDataLeft
            return False
        else:
            pass
        #endregion --------------------> Check some Rows are left for Analysis

        return True
    #---

    def SetStepDictDP(self) -> dict:
        """Set the Data Processing part of the stepDict to write in the output.

            Returns
            -------
            dict
        """
        stepDict = {
            'DP': {
                mConfig.ltDPKeys[0] : mConfig.fnFloat.format(self.rDate, '02'),
                mConfig.ltDPKeys[1] : mConfig.fnTrans.format(self.rDate, '03'),
                mConfig.ltDPKeys[2] : mConfig.fnNorm.format(self.rDate, '04'),
                mConfig.ltDPKeys[3] : mConfig.fnImp.format(self.rDate, '05'),
            },
        }

        return stepDict
    #---

    def SetOutputDict(self, dateDict) -> dict:
        """Creates the output dictionary to be written to the output file.

            Parameters
            ----------
            dateDict : dict
                dateDict = {
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
                outData = mFile.ReadJSON(self.rDO['uFile'])
            except Exception:
                msg = mConfig.mFileRead.format(self.rDO['uFile'])
                raise mException.ExecutionError(msg)
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

    def SetStepDictDPFileR(self) -> dict:
        """Set the Data Processing, Files & Results parts of the stepDict to 
            write in the output.

            Returns
            -------
            dict
        """
        stepDict = {
            'DP': {
                mConfig.ltDPKeys[0] : mConfig.fnFloat.format(self.rDate, '02'),
                mConfig.ltDPKeys[1] : mConfig.fnTrans.format(self.rDate, '03'),
                mConfig.ltDPKeys[2] : mConfig.fnNorm.format(self.rDate, '04'),
                mConfig.ltDPKeys[3] : mConfig.fnImp.format(self.rDate, '05'),
            },
            'Files' : {
                mConfig.fnInitial.format(self.rDate, '01')   : self.dfI,
                mConfig.fnFloat.format(self.rDate, '02')     : self.dfF,
                mConfig.fnTrans.format(self.rDate, '03')     : self.dfT,
                mConfig.fnNorm.format(self.rDate, '04')      : self.dfN,
                mConfig.fnImp.format(self.rDate, '05')       : self.dfIm,
                mConfig.fnTargetProt.format(self.rDate, '06'): self.dfTP,
                mConfig.fnExclude.format(self.rDate, '07')   : self.dfE,
                mConfig.fnScore.format(self.rDate, '08')     : self.dfS,
                self.rMainData.format(self.rDate, '09')     : self.dfR,
            },
            'R' : self.rMainData.format(self.rDate, '09'),
        }

        return stepDict
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
        dataFolder = self.rOFolder / mConfig.fnDataSteps / dataFolder # type: ignore
        dataFolder.mkdir(parents=True, exist_ok=True)
        #------------------------------> 
        msgStep = self.cLPdWrite + 'Creating needed folders, Data-Initial folder'
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        dataInit = self.rOFolder / mConfig.fnDataInit # type: ignore
        dataInit.mkdir(parents=True, exist_ok=True)
        #endregion --------------------------------------------> Create folder
        
        #region ------------------------------------------------> Data Initial
        msgStep = self.cLPdWrite + 'Data files, Input Data'
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        #------------------------------> 
        puFolder = self.rDO['uFile'].parent / mConfig.fnDataInit
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
            mFile.WriteDFs2CSV(dataFolder, stepDict['Files'])
        except Exception as e:
            self.rMsgError = ('It was not possible to create the files with '
                'the data for the intermediate steps of the analysis.')
            self.rException = e
            return False
        #endregion -----------------------------------------------> Data Steps
        
        #region --------------------------------------------> Further Analysis
        if (aaDict := stepDict.get('AA', False)):
            fileP = dataFolder/aaDict[f'{self.rDate}_{self.rDO["AA"]}'] # type: ignore
            mFile.WriteDF2CSV(fileP, self.dfAA) # type: ignore
        else:
            pass
        
        if (histDict := stepDict.get('Hist', False)):
            fileP = dataFolder/histDict[f'{self.rDate}_{self.rDO["Hist"]}'] # type: ignore
            mFile.WriteDF2CSV(fileP, self.dfHist) # type: ignore
        else:
            pass
        
        if (fileN := stepDict.get('CpR', False)):
            fileP = dataFolder/fileN
            mFile.WriteDF2CSV(fileP, self.dfCpR) # type: ignore
        else:
            pass
        
        if (fileN := stepDict.get('CEvol', False)):
            fileP = dataFolder/fileN
            mFile.WriteDF2CSV(fileP, self.dfCEvol) # type: ignore
        else:
            pass
        #endregion -----------------------------------------> Further Analysis

        #region --------------------------------------------------> UMSAP File
        msgStep = self.cLPdWrite + 'Main file'
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        #------------------------------> Create output dict
        dateDict = {
            self.rDateID : {
                'V' : mConfig.dictVersion,
                'I' : self.rDI,
                'CI': mMethod.DictVal2Str(self.rDO, self.rChangeKey, new=True),
                'DP': {
                    mConfig.ltDPKeys[0] : stepDict['DP'][mConfig.ltDPKeys[0]],
                    mConfig.ltDPKeys[1] : stepDict['DP'][mConfig.ltDPKeys[1]],
                    mConfig.ltDPKeys[2] : stepDict['DP'][mConfig.ltDPKeys[2]],
                    mConfig.ltDPKeys[3] : stepDict['DP'][mConfig.ltDPKeys[3]],
                },
            }
        }
        #--------------> DataPrep Util does not have dfR
        if not self.dfR.empty:
            dateDict[self.rDateID]['R'] = stepDict['R']
        else:
            pass
        #--------------> 
        if self.cName == mConfig.npProtProf:
            #--------------> Filters in ProtProf
            dateDict[self.rDateID]['F'] = {}
        elif self.cName == mConfig.npTarProt:
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
            mFile.WriteJSON(self.rDO['uFile'], outData)
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
        """ Start analysis of the module/utility.

            Parameter
            ---------
            event : wx.Event
                Event information.
                
            Returns
            -------
            bool
        """
        #region --------------------------------------------------> Dlg window
        self.rDlg = mWindow.DialogProgress(
            mConfig.winMain, self.cTitlePD, self.cGaugePD)
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
            if a:
                pass
            else:
                self.rMsgError = mMethod.StrSetMessage(
                    v[1].format(b[1], k), b[2])
                return False
        #endregion ----------------------------------------------------> Check

        #region ---------------------------------------> Unique Column Numbers
        if self.rCheckUnique:
            msgStep = self.cLPdCheck + 'Unique Column Numbers'
            wx.CallAfter(self.rDlg.UpdateStG, msgStep)
            #------------------------------>
            a, b = mCheck.TcUniqueColNumbers(self.rCheckUnique)
            if a:
                pass
            else:
                msg = mConfig.mSection.format(self.cLColumnBox)
                self.rMsgError = mMethod.StrSetMessage(msg, b[2]) # type: ignore
                return False
        else:
            pass
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
        self.rDate = mMethod.StrNow()
        #------------------------------> Output folder
        if self.rDO['uFile'].exists():
            self.rOFolder = self.rDO['uFile'].parent
        else:
            folder = self.rDO['uFile'].parent
            step = folder/mConfig.fnDataSteps
            init = folder/mConfig.fnDataInit
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
            self.rIFileObj = mFile.CSVFile(self.rDO['iFile'])
        except mException.FileIOError as e:
            self.rMsgError = mConfig.mFileRead.format(self.rDO['iFile'])
            self.rException = e
            return False
        #------------------------------> Check Target Protein. It cannot be done
        # before this step
        if 'TargetProt' in self.rDO:
            if self.rIFileObj.StrInCol(
                self.rDO['TargetProt'], self.rDO['oc']['TargetProtCol']):
                pass
            else:
                self.rMsgError = (f'The Target Protein '
                    f'({self.rDO["TargetProt"]}) was not found in the '
                    f'{self.cLDetectedProt} column '
                    f'({self.rDO["oc"]["TargetProtCol"]}).')
                return False
        else:
            pass
        #endregion ------------------------------------------------> Data file

        #region ------------------------------------------------> Seq Rec File
        if 'seqFile' in self.rDO:
            #------------------------------>
            msgStep = self.cLPdReadFile + f"{self.cLSeqFile}, reading"
            wx.CallAfter(self.rDlg.UpdateStG, msgStep)
            #------------------------------>
            try:
                self.rSeqFileObj = mFile.FastaFile(self.rDO['seqFile'])
            except Exception as e:
                self.rMsgError = mConfig.mFileRead.format(self.rDO['seqFile'])
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
        else:
            pass
        #endregion ---------------------------------------------> Seq Rec File

        #region ---------------------------------------------------> Print Dev
        if mConfig.development and self.rSeqFileObj is not None:
            print("Rec Seq: ", self.rSeqFileObj.rSeqRec)
            print("Nat Seq: ", self.rSeqFileObj.rSeqNat)
        else:
            pass
        #endregion ------------------------------------------------> Print Dev

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
        wx.CallAfter(gMethod.LoadUMSAPFile, fileP=self.rDO['uFile'])
        #endregion -----------------------------------------------------> Load

        return True
    #---

    def RunEnd(self) -> bool:
        """Restart GUI and needed variables
        
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


class BaseConfPanelMod(BaseConfPanel, mWidget.ResControl):
    """Base configuration for a panel of a module.

        Parameters
        ----------
        parent : wx Widget
            Parent of the widgets
        rightDelete : Boolean
            Enables clearing wx.StaticBox input with right click
    """
    #region --------------------------------------------------> Instance setup
    def __init__(self, parent: wx.Window, rightDelete: bool=True) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        #------------------------------> Label
        self.cLAlpha    = getattr(self, 'cLAlpha',    'α level')
        self.cLScoreVal = getattr(self, 'cLScoreVal', mConfig.lStScoreVal)
        self.cLScoreCol = getattr(self, 'cLScoreCol', mConfig.lStScoreCol)
        #------------------------------> Tooltips
        self.cTTScore    = getattr(self, 'cTTScore',    mConfig.ttStScoreCol)
        self.cTTScoreVal = getattr(self, 'cTTScoreVal', mConfig.ttStScoreVal)
        self.cTTAlpha    = getattr(
            self, 'cTTAlpha', ('Significance level for the statistical '
                               'analysis.\ne.g. 0.05'))
        self.cTTDetectedProt = getattr(
            self, 'cTTDetectedProtL', ('Set the column number containing the '
                                       'detected proteins.\ne.g. 7'))
        self.rLLenLongest = getattr(
            self, 'rLLenLongest', len(mConfig.lStResultCtrlS))
        #------------------------------> Parent class init
        BaseConfPanel.__init__(self, parent, rightDelete=rightDelete)

        mWidget.ResControl.__init__(self, self.wSbColumn)
        #------------------------------>
        self.rLbDict = {}
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wAlpha = mWidget.StaticTextCtrl(
            self.wSbValue,
            stLabel   = self.cLAlpha,
            stTooltip = self.cTTAlpha,
            tcSize    = self.cSTc,
            tcHint    = 'e.g. 0.05',
            validator = mValidator.NumberList(
                numType='float', nN=1, vMin=0, vMax=1),
        )
        self.wScoreVal = mWidget.StaticTextCtrl(
            self.wSbValue,
            stLabel   = self.cLScoreVal,
            stTooltip = self.cTTScoreVal,
            tcSize    = self.cSTc,
            tcHint    = 'e.g. 320',
            validator = mValidator.NumberList(numType='float', nN=1),
        )
        self.wDetectedProt = mWidget.StaticTextCtrl(
            self.wSbColumn,
            stLabel   = self.cLDetectedProt,
            stTooltip = self.cTTDetectedProt,
            tcSize    = self.cSTc,
            tcHint    = 'e.g. 0',
            validator = mValidator.NumberList(numType='int', nN=1, vMin=0),
        )
        self.wScore = mWidget.StaticTextCtrl(
            self.wSbColumn,
            stLabel   = self.cLScoreCol,
            stTooltip = self.cTTScore,
            tcSize    = self.cSTc,
            tcHint    = 'e.g. 39',
            validator = mValidator.NumberList(numType='int', nN=1, vMin=0),
        )
        #endregion --------------------------------------------------> Widgets
    #---
    #endregion -----------------------------------------------> Instance setup
#---


class BaseConfPanelMod2(BaseConfPanelMod):
    """Base class for the LimProt and TarProt configuration panel.

        Parameters
        ----------
        parent : wx Widget
            Parent of the widgets
        rightDelete : Boolean
            Enables clearing wx.StaticBox input with right click
            
        Attributes
        ----------
        rChangeKey: list[str]
            Keys in self.rDO whose values must be turned to str.
    """
    #region ---------------------------------------------------> Class Setup
    rChangeKey = ['iFile', 'uFile', 'seqFile']
    #endregion ------------------------------------------------> Class Setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent: wx.Window, rightDelete: bool=True) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        #------------------------------> Label
        self.cLSeqFile    = getattr(self, 'cLSeqFile',    'Sequences')
        self.cLTargetProt = getattr(self, 'cLTargetProt', 'Target Protein')
        self.cLSeqCol     = getattr(self, 'cLSeqCol',     'Sequences')
        #------------------------------> Hint
        self.cHTargetProt = getattr(self, 'cHTargetProt', 'e.g. MisAlpha18')
        self.cHSeqCol     = getattr(self, 'cHSeqCol',     'e.g. 1')
        self.cHSeqFile    = getattr(
            self, 'cHSeqFile', f"Path to the {self.cLSeqFile} file")
        #------------------------------> Extensions
        self.cESeqFile = getattr(self, 'cESeqFile', mConfig.elSeq)
        #------------------------------> Tooltip
        self.cTTSeqFile = getattr(
            self, 'cTTSeqFile', f'Select the {self.cLSeqFile} file.')
        self.cTTTargetProt = getattr(
            self, 'cTTTargetProt', f'Set the name of the {self.cLTargetProt}.')
        self.cTTSeqCol = getattr(
            self, 'cTTSeqCol', ('Set the column number containing the '
                                'Sequences.\ne.g. 0'))
        #------------------------------>
        super().__init__(parent, rightDelete=rightDelete)
        #------------------------------>
        self.rCopyFile = {
            'iFile'  : self.cLiFile,
            'seqFile': f'{self.cLSeqFile} File',
        }
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        #------------------------------> Files
        self.wSeqFile = mWidget.ButtonTextCtrlFF(
            self.wSbFile,
            btnLabel   = self.cLSeqFile,
            btnTooltip = self.cTTSeqFile,
            tcHint     = self.cHSeqFile,
            mode       = 'openO',
            ext        = self.cESeqFile,
            tcStyle    = wx.TE_READONLY,
            validator  = mValidator.InputFF(fof='file'),
            ownCopyCut = True,
        )
        #------------------------------> Values
        self.wTargetProt = mWidget.StaticTextCtrl(
            self.wSbValue,
            stLabel   = self.cLTargetProt,
            stTooltip = self.cTTTargetProt,
            tcSize    = self.cSTc,
            tcHint    = self.cHTargetProt,
            validator = mValidator.IsNotEmpty()
        )
        #------------------------------> Columns
        self.wSeqCol = mWidget.StaticTextCtrl(
            self.wSbColumn,
            stLabel   = self.cLSeqCol,
            stTooltip = self.cTTSeqCol,
            tcSize    = self.cSTc,
            tcHint    = self.cHSeqCol,
            validator = mValidator.NumberList(numType='int', nN=1, vMin=0),
        )
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        #------------------------------> Sizer Files
        #--------------> 
        self.sSbFileWid.Detach(self.wId.wSt)
        self.sSbFileWid.Detach(self.wId.wTc)
        #--------------> 
        self.sSbFileWid.Add(
            self.wSeqFile.wBtn,
            pos    = (2,0),
            flag   = wx.EXPAND|wx.ALL,
            border = 5
        )
        self.sSbFileWid.Add(
            self.wSeqFile.wTc,
            pos    = (2,1),
            flag   = wx.EXPAND|wx.ALL,
            border = 5
        )
        self.sSbFileWid.Add(
            self.wId.wSt,
            pos    = (3,0),
            flag   = wx.ALIGN_CENTER|wx.ALL,
            border = 5
        )
        self.sSbFileWid.Add(
            self.wId.wTc,
            pos    = (3,1),
            flag   = wx.EXPAND|wx.ALL,
            border = 5
        )
        #------------------------------> Sizer Columns
        self.sSbColumnWid.Add(
            self.wSeqCol.wSt,
            pos    = (0,0),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sSbColumnWid.Add(
            self.wSeqCol.wTc,
            pos    = (0,1),
            flag   = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sSbColumnWid.Add(
            self.wDetectedProt.wSt,
            pos    = (0,2),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sSbColumnWid.Add(
            self.wDetectedProt.wTc,
            pos    = (0,3),
            flag   = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sSbColumnWid.Add(
            self.wScore.wSt,
            pos    = (0,4),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sSbColumnWid.Add(
            self.wScore.wTc,
            pos    = (0,5),
            flag   = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sSbColumnWid.Add(
            self.sRes,
            pos    = (1,0),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND,
            border = 0,
            span   = (0,6),
        )
        self.sSbColumnWid.AddGrowableCol(1,1)
        self.sSbColumnWid.AddGrowableCol(3,1)
        self.sSbColumnWid.AddGrowableCol(5,1)
        #endregion ---------------------------------------------------> Sizers

        #region -------------------------------------------------> Check Input
        self.rCheckUserInput = { # New order is needed.
            self.cLuFile       :[self.wUFile.wTc,           mConfig.mFileBad       , False],
            self.cLiFile       :[self.wIFile.wTc,           mConfig.mFileBad       , False],
            f'{self.cLSeqFile} file' :[self.wSeqFile.wTc,   mConfig.mFileBad       , False],
            self.cLId          :[self.wId.wTc,              mConfig.mValueBad      , False],
            self.cLCeroTreat   :[self.wCeroB.wCb,           mConfig.mOptionBad     , False],
            self.cLTransMethod :[self.wTransMethod.wCb,     mConfig.mOptionBad     , False],
            self.cLNormMethod  :[self.wNormMethod.wCb,      mConfig.mOptionBad     , False],
            self.cLImputation  :[self.wImputationMethod.wCb,mConfig.mOptionBad     , False],
            self.cLShift       :[self.wShift.wTc,           mConfig.mOneRPlusNum   , False],
            self.cLWidth       :[self.wWidth.wTc,           mConfig.mOneRPlusNum   , False],
            self.cLTargetProt  :[self.wTargetProt.wTc,      mConfig.mValueBad      , False],
            self.cLScoreVal    :[self.wScoreVal.wTc,        mConfig.mOneRealNum    , False],
        }
        #------------------------------> 
        self.rCheckUnique = [self.wSeqCol.wTc, self.wDetectedProt.wTc, 
            self.wScore.wTc, self.wTcResults]
        #------------------------------>
        #endregion ----------------------------------------------> Check Input
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def NCResNumbers(self, seqNat: bool=True) -> bool:
        """Find the residue numbers for the peptides in the sequence of the 
            Recombinant and Native protein.

            Parameters
            ----------
            seqNat: bool
                Calculate N and C residue numbers also for the Native protein

            Returns
            -------
            bool

            Notes
            -----
            Assumes child class has the following attributes:
            - seqFileObj: mFile.FastaFile
                Object with the sequence of the Recombinant and Native protein.
            - do: dict with at least the following key - values pairs
                {
                    'df' : {
                        'SeqCol' : int,
                    },
                    'dfo' : {
                        'NC' : list[int],
                        'NCF': list[int],
                    },
                }
        """
        #region -----------------------------------------------------> Rec Seq
        #------------------------------> 
        msgStep = (f'{self.cLPdRun} Calculating output data - N & C terminal '
            f'residue numbers I')
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        #------------------------------> 
        try:
            self.dfR.iloc[:,self.rDO['dfo']['NC']] = self.dfR.iloc[
                :,[self.rDO['df']['SeqCol'], 1]].apply(
                    self.NCTerm, 
                    axis        = 1,
                    raw         = True,
                    result_type = 'expand',
                    args        = (self.rSeqFileObj, 'Recombinant'),
                )
        except mException.ExecutionError:
            return False
        except Exception as e:
            self.rMsgError  = mConfig.mUnexpectedError
            self.rException = e
            return False
        #endregion --------------------------------------------------> Rec Seq

        #region -----------------------------------------------------> Nat Seq
        #------------------------------> 
        msgStep = (f'{self.cLPdRun} Calculating output data - N & C terminal '
            f'residue numbers II')
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        #------------------------------> 
        if seqNat and self.rSeqFileObj.rSeqNat: # type: ignore
            #------------------------------> 
            delta = self.rSeqFileObj.GetSelfDelta() # type: ignore
            #------------------------------> 
            a = self.dfR.iloc[:,self.rDO['dfo']['NC']] + delta
            self.dfR.iloc[:,self.rDO['dfo']['NCF']] = a
            #------------------------------> 
            m = self.dfR.iloc[:,self.rDO['dfo']['NCF']] > 0
            a = self.dfR.iloc[:,self.rDO['dfo']['NCF']].where(m, np.nan)
            a = a.astype('int')
            self.dfR.iloc[:,self.rDO['dfo']['NCF']] = a
        else:
            pass
        #endregion --------------------------------------------------> Nat Seq

        return True
    #---

    def NCTerm(
        self, row: list[str], seqObj: mFile.FastaFile, seqType: str,
        ) -> tuple[int, int]:
        """Get the N and C terminal residue numbers for a given peptide.

            Parameters
            ----------
            row: list[str]
                List with two elements. The Sequence is in index 0.
            seqObj : mFile.FastaFile
                Object with the protein sequence and the method to search the 
                peptide sequence.
            seqType : str
                For the error message.

            Returns
            -------
            (Nterm, Cterm)
        """
        #region ---------------------------------------------------> Find pept
        nc = seqObj.FindSeq(row[0])
        #endregion ------------------------------------------------> Find pept

        #region ----------------------------------------------------> Check ok
        if nc[0] != -1:
            return nc
        else:
            self.rMsgError = mConfig.mSeqPeptNotFound.format(row[0], seqType)
            raise mException.ExecutionError(self.rMsgError)
        #endregion -------------------------------------------------> Check ok
    #---
    #endregion ------------------------------------------------> Class methods
#---


class BaseResControlExpConf(wx.Panel):
    """Parent class for the configuration panel in the dialog Results - Control
        Experiments.

        Parameters
        ----------
        parent : wx.Widget
            Parent of the widgets.
        name : str
            Unique name of the panel.
        topParent : wx.Widget
            Top parent window.
        NColF : int
            Number of columns in the input file.

        Attributes
        ----------
        rControlVal: str
            Last used control value.
        rFSectStDict: dict[int: [wx.StaticText]]
            Labels for the field section
        rFSectTcDict: dict[int: [wx.TextCtrl]]
            Text fields for the field section.
        rLSectTcDict: dict[int: [wx.TextCtrl]]
            Text fields for the labels in the label section.
        rLSectWidget: list[mWidget.StaticTextCtrl]
            Label and Text field for the number of labels in the label section.
        rNColF: int
            Number of columns in the input file minus 1.
        rPName: str
            Name of the parent window.
        
        Notes
        -----
        The panel is divided in two sections. 
        - Section Label holds information about the label for the experiments 
        and control.
            The number of labels and the name are set in the child class with 
            cStLabel.
            This information is converted to rLSectWidget (name of the label e.g 
            Condition and input of number of each labels).
            The given label are stored in rLSectTcDict.
        - Section Fields that holds the information about the column numbers
            The name of the experiments is shown with rFSectStDict that is populated 
            from rLSectTcDict
            The column numbers are stored in rFSectTcDict.
        
        See Export2TopParent method for information about how the column numbers
        are exported to the parent panel.
    """
    #region --------------------------------------------------> Instance setup
    def __init__(self, parent: wx.Window, name: str, topParent: wx.Window, 
        NColF: int) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.cTopParent = topParent
        #------------------------------>
        self.rPName       = self.cTopParent.cName # type: ignore
        self.rLSectWidget = []
        self.rLSectTcDict = {}
        self.rFSectTcDict = {}
        self.rFSectStDict = {}
        self.rNColF       = NColF - 1
        self.rControlVal  = ''
        #------------------------------> Label
        self.cLSetup    = getattr(self, 'cLSetup',    'Setup Fields')
        self.cLControlN = getattr(self, 'cLControlN', 'Control Name')
        self.cStLabel   = getattr(self, 'cStLabel',   [])
        self.cLabelText = getattr(self, 'cLabelText', [])
        self.cN         = len(self.cStLabel)
        #------------------------------> Hint
        self.cHControlN   = getattr(self, 'cHControlN',   'MyControl')
        self.cHTotalField = getattr(self, 'cHTotalField', '#')
        #------------------------------> Size
        self.cSLabel      = getattr(self, 'cSLabel',      (60,22))
        self.cSSWLabel    = getattr(self, 'cSSWLabel',    (670,135))
        self.cSSWMatrix   = getattr(self, 'cSSWMatrix',   (670,670))
        self.cSTotalField = getattr(self, 'cSTotalField', (35,22))
        #------------------------------> Tooltip
        self.cTTControlN = getattr(
            self, 'cTTControlN', ('Name or ID of the control experiment.\ne.g. '
                                  'MyControl."'))
        self.cTTRight = getattr(self, 'cTTRight', ('Use the right mouse click '
                                        'to clear the content of the window.'))
        self.cTTBtnCreate = getattr(self, 'cTTBtnCreate', ('Create the fields '
                                                'to type the column numbers.'))
        self.cTTTotalField = getattr(self, 'cTTTotalField', [])
        #------------------------------> Validator
        self.cVColNumList = mValidator.NumberList(
            sep=' ', opt=True, vMin=0, vMax=self.rNColF)
        #------------------------------> Messages
        self.mNoControlT = getattr(
            self, 'mNoControl', f'The Control Type must defined.')
        self.mLabelEmpty = getattr(
            self, 'mLabelEmpty', 'All labels and control name must be defined.')
        #------------------------------> super()
        super().__init__(parent, name=name)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        #------------------------------> wx.ScrolledWindow
        self.wSwLabel  = scrolled.ScrolledPanel(self, size=self.cSSWLabel)
        #------------------------------>
        self.wSwMatrix = scrolled.ScrolledPanel(self, size=self.cSSWMatrix)
        self.wSwMatrix.SetBackgroundColour('WHITE')
        #------------------------------> wx.StaticText & wx.TextCtrl
        #--------------> Experiment design
        self.AddLabelFields()
        #------------------------------> Control name
        self.wControlN = mWidget.StaticTextCtrl(
            self.wSwLabel,
            stLabel   = self.cLControlN,
            stTooltip = self.cTTControlN,
            tcHint    = self.cHControlN,
            tcSize    = self.cSLabel,
        )
        #------------------------------> wx.Button
        self.wBtnCreate = wx.Button(self, label=self.cLSetup)
        #endregion --------------------------------------------------> Widgets

        #region -----------------------------------------------------> Tooltip
        self.wBtnCreate.SetToolTip(self.cTTBtnCreate)
        self.wSwLabel.SetToolTip(self.cTTRight)
        self.wSwMatrix.SetToolTip(self.cTTRight)
        #endregion --------------------------------------------------> Tooltip

        #region ------------------------------------------------------> Sizers
        #------------------------------> Sizers for self.swLabel
        self.sSWLabelMain = wx.BoxSizer(wx.VERTICAL)
        self.sSWLabel = wx.FlexGridSizer(self.cN,2,1,1)
        self.Add2SWLabel()
        self.sSWLabelMain.Add(
            self.sSWLabel, 0, wx.EXPAND|wx.ALL, 5)
        self.wSwLabel.SetSizer(self.sSWLabelMain)
        #------------------------------> Sizer with setup btn
        self.sSetup = wx.BoxSizer(wx.VERTICAL)
        self.sSetup.Add(
            self.wBtnCreate, 0, wx.ALIGN_RIGHT|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
        #------------------------------> Sizer for swMatrix
        self.sSWMatrix = wx.FlexGridSizer(1,1,1,1)
        self.wSwMatrix.SetSizer(self.sSWMatrix)
        #------------------------------> All in Sizer
        self.sSizer = wx.BoxSizer(wx.VERTICAL)
        self.sSizer.Add(self.wSwLabel, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, 5)
        self.sSizer.Add(self.sSetup, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
        self.sSizer.Add(self.wSwMatrix, 1, wx.EXPAND|wx.ALL, 5)
        self.SetSizer(self.sSizer)
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind
        self.wBtnCreate.Bind(wx.EVT_BUTTON, self.OnCreate)
        self.wSwLabel.Bind(wx.EVT_RIGHT_DOWN, self.OnClear)
        self.wSwMatrix.Bind(wx.EVT_RIGHT_DOWN, self.OnClear)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Event methods
    def OnCreate(self, event: Union[wx.CommandEvent, str]) -> bool:
        """Create the fields in the white panel. Override as needed.

            Parameters
            ----------
            event : wx.Event
                Information about the event

            Returns
            -------
            True
        """
        return True
    #---

    def OnLabelNumber(self, event: Union[wx.Event, str]) -> bool:
        """Creates fields for names when the total wx.TextCtrl looses focus.

            Parameters
            ----------
            event : wx.Event
                Information about the event.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        vals = []
        #endregion ------------------------------------------------> Variables

        #region -------------------------------------------------> Check input
        for k in range(0, self.cN):
            #------------------------------>
            tc = self.rLSectWidget[k].wTc
            #------------------------------>
            if tc.GetValidator().Validate()[0]:
                vals.append(0 if (x:=tc.GetValue()) == '' else int(x))
            else:
                self.rLSectWidget[k].wTc.SetValue("")
                return False
        #endregion ----------------------------------------------> Check input

        #region ------------------------------------------------> Modify sizer
        vals.sort(reverse=True)
        n = vals[0]
        #------------------------------>
        self.sSWLabel.SetCols(n+2)
        #endregion ---------------------------------------------> Modify sizer

        #region --------------------------------------> Create/Destroy widgets
        for k in range(0, self.cN):
            tN = int(self.rLSectWidget[k].wTc.GetValue())
            lN = len(self.rLSectTcDict[k])
            if tN > lN:
                #------------------------------> Create new widgets
                for knew in range(lN, tN):
                    #-------------->
                    KNEW = knew + 1
                    #-------------->
                    self.rLSectTcDict[k].append(
                        wx.TextCtrl(
                            self.wSwLabel,
                            size  = self.cSLabel,
                            value = f"{self.cLabelText[k]}{KNEW}"
                        )
                    )
            else:
                #------------------------------> Destroy widget
                for knew in range(tN, lN):
                    #------------------------------> Detach
                    self.sSWLabel.Detach(self.rLSectTcDict[k][-1])
                    #------------------------------> Destroy
                    self.rLSectTcDict[k][-1].Destroy()
                    #------------------------------> Remove from list
                    self.rLSectTcDict[k].pop()
        #endregion -----------------------------------> Create/Destroy widgets

        #region ------------------------------------------------> Add to sizer
        self.Add2SWLabel()
        #endregion ---------------------------------------------> Add to sizer

        #region --------------------------------------------------> Event Skip
        if isinstance(event, wx.Event):
            event.Skip()
        else:
            pass
        #endregion -----------------------------------------------> Event Skip

        return True
    #---

    def OnOK(self, export: bool=True) -> tuple[bool, str]:
        """Validate and set the Results - Control Experiments text.

            Parameters
            ---------
            export: bool
                Export data after checks are done.

            Returns
            -------
            tuple[bool, str]
                Str is the string to show in Result - Control.

            Notes
            -----
            See also self.Export2TopParent.
        """
        #region -------------------------------------------------> Check input
        #------------------------------> Variables
        tcList = []
        oText  = ''
        #------------------------------> Individual fields and list of tc
        for v in self.rFSectTcDict.values():
            #--------------> Check values
            for j in v:
                #--------------> Add to lists
                tcList.append(j)
                oText = f"{oText}{j.GetValue()}, "
                #--------------> Check
                a, b = j.GetValidator().Validate()
                if a:
                    pass
                else:
                    msg = mConfig.mResCtrlWin.format(b[1])
                    e = mException.ExecutionError(b[2])
                    mWindow.DialogNotification(
                        'errorF', msg=msg, parent=self, tException=e)
                    j.SetFocus(),
                    return (False,'')
            #--------------> Add row delimiter
            oText = f"{oText[0:-2]}; "
        #------------------------------> All cannot be empty
        a, b = mCheck.AllTcEmpty(tcList)
        if not a:
            pass
        else:
            mWindow.DialogNotification(
                'errorF', msg=mConfig.mAllTextFieldEmpty, parent=self)
            return (False, '')
        #------------------------------> All unique
        a, b = mCheck.TcUniqueColNumbers(tcList)
        if a:
            pass
        else:
            e = mException.InputError(b[2]) # type: ignore
            mWindow.DialogNotification(
                'errorF', msg=mConfig.mRepeatColNum, parent=self, tException=e)
            return (False, '')
        #endregion ----------------------------------------------> Check input

        #region ---------------------------------------------------> Export
        if export:
            self.Export2TopParent(oText)
        else:
            pass
        #endregion ------------------------------------------------> Export

        return (True, oText)
    #---

    def OnClear(self, event: wx.Event) -> bool:
        """Clear all input in the wx.Dialog.

            Parameters
            ----------
            event : wx.Event
                Information about the event

            Returns
            -------
            bool
        """
        #region -----------------------------------------------------> Widgets
        #------------------------------> Labels
        self.sSWLabel.Clear(delete_windows=True)
        #------------------------------> Control
        self.wControlN.wTc.SetValue('')
        try:
            self.wCbControl.SetValue('') # type: ignore
        except Exception:
            pass
        #------------------------------> Fields
        self.sSWMatrix.Clear(delete_windows=True)
        #endregion --------------------------------------------------> Widgets

        #region -------------------------------------------------> List & Dict
        self.rLSectWidget = []
        self.rLSectTcDict = {}
        self.rFSectTcDict = {}
        self.rFSectStDict = {}
        #endregion ----------------------------------------------> List & Dict

        #region --------------------------------------------------> Add Labels
        self.AddLabelFields()
        self.Add2SWLabel()
        #endregion -----------------------------------------------> Add Labels

        return True
    #---
    #endregion ------------------------------------------------> Event methods

    #region --------------------------------------------------> Manage methods
    def Export2TopParent(self, oText) -> bool:
        """Export the data to the top parent.
        
            Parameters
            ----------
            oText: str
                String to show in Result - Control.

            Returns
            -------
            bool
    
            Notes
            -----
            Use after all checks have being done.
            
            This will set the tcResult in the topParent window to a string like:
            1 2 3, 4 5 6; '', 7-10; 11-14, '' where commas separate tc fields
            in the same row and ; separate rows.
            The following dict will be set in topParent.lbDict
            {
                0             : [values], # First row of labels
                N             : [values], # N row of labels
                'Control'     : 'Name',
                'ControlType' : Control type,
            }
            And topParent.controlType will be also set to the corresponding 
            value.
        """
        #region ----------------------------------------> Set parent variables
        #------------------------------> Labels
        self.cTopParent.rLbDict = {} # type: ignore
        for k, v in self.rLSectTcDict.items():
            self.cTopParent.rLbDict[k] = [] # type: ignore
            for j in v:
                self.cTopParent.rLbDict[k].append(j.GetValue()) # type: ignore
        #------------------------------> Control Name
        self.cTopParent.rLbDict['Control'] = [self.wControlN.wTc.GetValue()] # type: ignore
        #------------------------------> Control type if needed
        if self.rPName == 'ProtProfPane' :
            self.cTopParent.rLbDict['ControlType'] = self.rControlVal # type: ignore
        else:
            pass
        #endregion -------------------------------------> Set parent variables

        #region -----------------------------------------------> Set tcResults
        self.cTopParent.wTcResults.SetValue(f"{oText[0:-2]}") # type: ignore
        #endregion --------------------------------------------> Set tcResults

        return True
    #---
    
    def SetInitialState(self) -> bool:
        """Set the initial state of the panel.

            Returns
            -------
            bool
        """
        #region -------------------------------------------------> Check input
        if (tcFieldsVal := self.cTopParent.wTcResults.GetValue()) != '': # type: ignore
            pass
        else:
            return False
        #endregion ----------------------------------------------> Check input

        #region --------------------------------------------------> Add Labels
        #------------------------------> Check the labels
        if mConfig.development:
            for k,v in self.cTopParent.rLbDict.items(): # type: ignore
                print(str(k)+': '+str(v))
            print('')
        else:
            pass
        #------------------------------> Set the label numbers
        for k, v in self.cTopParent.rLbDict.items(): # type: ignore
            if k != 'Control' and k != 'ControlType':
                self.rLSectWidget[k].wTc.SetValue(str(len(v)))
            else:
                pass
        #------------------------------> Create labels fields
        self.OnLabelNumber('test')
        #------------------------------> Fill. 2 iterations needed. Improve
        for k, v in self.cTopParent.rLbDict.items(): # type: ignore
            if k != 'Control' and k != 'ControlType':
                for j, t in enumerate(v):
                    self.rLSectTcDict[k][j].SetValue(t)
            elif k == 'Control':
                self.wControlN.wTc.SetValue(v[0])
            else:
                pass
        #endregion -----------------------------------------------> Add Labels
        
        #region -------------------------------------------------> Set Control
        if self.rPName == 'ProtProfPane':
            #------------------------------> 
            cT = self.cTopParent.rLbDict['ControlType'] # type: ignore
            self.wCbControl.SetValue(cT) # type: ignore
            #------------------------------> 
            if cT == mConfig.oControlTypeProtProf['Ratio']:
                self.wControlN.wTc.SetEditable(False)
            else:
                pass
        else:
            pass
        #endregion ----------------------------------------------> Set Control
        
        #region ---------------------------------------------> Create tcFields
        self.OnCreate('fEvent')
        #endregion ------------------------------------------> Create tcFields

        #region --------------------------------------------> Add Field Values
        row = tcFieldsVal.split(";")
        for k, r in enumerate(row):
            fields = r.split(",")
            for j, f in enumerate(fields):
                self.rFSectTcDict[k][j].SetValue(f)
        #endregion -----------------------------------------> Add Field Values

        return True
    #---

    def Add2SWLabel(self) -> bool:
        """Add the widgets to self.sSWLabel. It assumes sizer already has 
            the right number of columns and rows. 

            Returns
            -------
            bool
        """
        #region ------------------------------------------------------> Remove
        self.sSWLabel.Clear(delete_windows=False)
        n = 0
        #endregion ---------------------------------------------------> Remove

        #region ---------------------------------------------------------> Add
        for k in range(0, self.cN):
            #------------------------------> Add conf fields
            self.sSWLabel.Add(
                self.rLSectWidget[k].wSt,
                0, 
                wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 
                5
            )
            self.sSWLabel.Add(
                self.rLSectWidget[k].wTc,
                0, 
                wx.ALIGN_RIGHT|wx.EXPAND|wx.ALL, 
                5
            )
            #------------------------------> Add user fields
            for tc in self.rLSectTcDict[k]:
                self.sSWLabel.Add(tc, 0, wx.EXPAND|wx.ALL, 5)
            #------------------------------> Add empty space
            n = self.sSWLabel.GetCols()
            l = len(self.rLSectTcDict[k]) + 2
            #-------------->
            if n > l:
                for c in range(l, n):
                    self.sSWLabel.AddSpacer(1)
            else:
                pass
        #endregion ------------------------------------------------------> Add

        #region ------------------------------------------------> Setup Sizers
        #------------------------------> Grow Columns
        for k in range(2, n):
            if not self.sSWLabel.IsColGrowable(k):
                self.sSWLabel.AddGrowableCol(k, 1)
            else:
                pass
        #------------------------------> Update sizer
        self.sSWLabel.Layout()
        #endregion ---------------------------------------------> Setup Sizers

        #region --------------------------------------------------> Set scroll
        self.wSwLabel.SetupScrolling()
        #endregion -----------------------------------------------> Set scroll

        return True
    #---

    def AddLabelFields(self) -> bool:
        """Add the default label fields, name and wx.TextCtrl for number.

            Returns
            -------
            bool
        """
        #region -----------------------------------------------------> Widgets
        for k in range(0, self.cN):
            #------------------------------> tcDict key
            self.rLSectTcDict[k] = []
            #------------------------------> wx.StaticText
            self.rLSectWidget.append(
                mWidget.StaticTextCtrl(
                    parent    = self.wSwLabel,
                    stLabel   = self.cStLabel[k],
                    stTooltip = self.cTTTotalField[k],
                    tcSize    = self.cSTotalField,
                    tcHint    = self.cHTotalField,
                    tcName    = str(k),
                    validator = mValidator.NumberList(vMin=1, nN=1),
            ))
            #------------------------------> Bind
            self.rLSectWidget[k].wTc.Bind(wx.EVT_KILL_FOCUS, self.OnLabelNumber)
        #endregion --------------------------------------------------> Widgets

        return True
    #---

    def CheckLabel(self, ctrlT: bool) -> list[int]:
        """Check the input in the Label section before creating the fields
            for column numbers.

            Parameters
            ----------
            ctrlT: bool
                Check (True) or not (False) the control options.

            Returns
            -------
            list[int]
                Number of labels for each field.
        """
        #region ----------------------------------------> Label numbers & Text
        n = []
        #------------------------------> 
        for k in range(0, self.cN):
            n.append(len(self.rLSectTcDict[k]))
            for w in self.rLSectTcDict[k]:
                if w.GetValue() == '':
                    mWindow.DialogNotification(
                        'errorF', msg=self.mLabelEmpty, parent=self)
                    return []
                else:
                    pass
        #------------------------------>
        if all(n):
            pass
        else:
            mWindow.DialogNotification(
                'errorF', msg=self.mLabelEmpty, parent=self)
            return []
        #endregion -------------------------------------> Label numbers & Text

        #region ---------------------------------------------------> Control
        if self.wControlN.wTc.GetValue() == '':
            mWindow.DialogNotification(
                'errorF', msg=self.mLabelEmpty, parent=self)
            return []
        else:
            pass
        #------------------------------> Control Type
        if ctrlT:
            if self.wCbControl.GetValidator().Validate()[0]:# type: ignore
                pass
            else:
                mWindow.DialogNotification(
                    'errorF', msg=self.mNoControlT, parent=self)
                return []
        else:
            pass
        #endregion ------------------------------------------------> Control

        return n
    #---
    #endregion -----------------------------------------------> Manage methods
#---
#endregion -----------------------------------------------------> Base Classes


#region -------------------------------------------------------------> Classes
class PaneListCtrlSearchPlot(wx.Panel):
    """Creates a panel with a wx.ListCtrl and below it a wx.SearchCtrl.

        Parameters
        ----------
        cParent: wx.Window
            Parent of the panel
        cColLabel : list of str or None
            Name of the columns in the wx.ListCtrl. Default is None
        cColSize : list of int or None
            Size of the columns in the wx.ListCtrl. Default is None
        cStyle : wx.Style
            Style of the wx.ListCtrl. Default is wx.LC_REPORT.
        cTcHint : str
            Hint for the wx.SearchCtrl. Default is ''.
        rData : list of list
            Data for the wx.ListCtrl when in virtual mode. Default is []. 
    """
    #region -----------------------------------------------------> Class setup
    cName = mConfig.npListCtrlSearchPlot
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self, 
        parent: wx.Window, 
        colLabel: list[str]  = [],
        colSize : list[int]  = [],
        data    : list[list] = [],
        style                = wx.LC_REPORT,
        tcHint  : str        = '',
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(parent, name=self.cName)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wLCS = mWidget.ListCtrlSearch(
            self, 
            listT    = 2,
            colLabel = colLabel,
            colSize  = colSize,
            canCut   = False,
            canPaste = False,
            style    = style,
            data     = data,
            tcHint   = tcHint,
        )
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        self.SetSizer(self.wLCS.sSizer)
        #endregion ---------------------------------------------------> Sizers
    #---
    #endregion -----------------------------------------------> Instance setup
#---


class NPlots(wx.Panel):
    """The panel will contain N plots distributed in a wx.FlexGridSizer.

        Parameters
        ----------
        parent: wx.Window
            Parent of the wx.Panel holding the plots.
        tKeys : list of str
            Keys for a dict holding a reference to the plots
        nCol : int
            Number of columns in the wx.FlexGridSizer holding the plots.
            Number of needed rows will be automatically calculated.
        dpi : int
            DPI value for the Matplot plots.
        statusbar : wx.StatusBar or None
            StatusBar to display information about the plots.

        Attributes
        ----------
        dPlot : dict
            Keys are tKeys and values mWidget.MatPlotPanel
        cName : str
            Name of the panel holding the plots.
        nCol : int
            Number of columns in the sizer
        nRow: int
            Number of rows in the sizer.
    """
    #region -----------------------------------------------------> Class setup
    cName = mConfig.npNPlot
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self,
        parent   : wx.Window,
        tKeys    : list[str],
        nCol     : int,
        dpi      : int                    = mConfig.general['DPI'],
        statusbar: Optional[wx.StatusBar] = None,
        ) -> None  : 
        """ """
        #region -----------------------------------------------> Initial Setup
        self.nCol = nCol
        self.nRow = ceil(len(tKeys)/nCol)
        #------------------------------>
        super().__init__(parent, name=self.cName)
        #endregion --------------------------------------------> Initial Setup

        #region ------------------------------------------------------> Sizers
        #------------------------------>
        self.sSizer = wx.FlexGridSizer(self.nRow, self.nCol, 1,1)
        #------------------------------>
        for k in range(0, self.nCol):
            self.sSizer.AddGrowableCol(k,1)
        for k in range(0, self.nRow):
            self.sSizer.AddGrowableRow(k,1)
        #------------------------------>
        self.SetSizer(self.sSizer)
        #endregion ---------------------------------------------------> Sizers

        #region -----------------------------------------------------> Widgets
        self.dPlot = {}
        for k in tKeys:
            #------------------------------> Create
            self.dPlot[k] = mWidget.MatPlotPanel(
                self, dpi=dpi, statusbar=statusbar)
            #------------------------------> Add to sizer
            self.sSizer.Add(self.dPlot[k], 1, wx.EXPAND|wx.ALL, 5)
        #endregion --------------------------------------------------> Widgets
    #---
    #endregion -----------------------------------------------> Instance setup
#---


class PaneCorrA(BaseConfPanel):
    """Creates the configuration tab for Correlation Analysis.
    
        Parameters
        ----------
        parent : wx Widget
            Parent of the widgets.
        dataI : dict or None
            Initial data provided by the user in a previous analysis.
            This contains both I and CI dicts e.g. {'I': I, 'CI': CI}

        Notes
        -----
        The structures of self.rDO and self.rDI are:
        rDO : dict
            Dict with the processed user input
            {
                'uFile'      : 'umsap file path',
                'iFile'      : 'data file path',
                'ID'         : 'Analysis ID',
                "Cero"       : 'Boolean, how to treat cero values',
                'TransMethod': 'transformation method',
                'NormMethod' : 'normalization method',
                'Shift'      : float,
                'Width'      : float,
                'ImpMethod'  : 'imputation method',
                'CorrMethod' : 'correlation method',
                'oc'         : {
                    'Column' : [selected columns as integers],
                    'ColumnF': [columns that must contain floats],
                }
                'df'         : {
                    'ColumnR'     : [cero based list of result columns],  
                    'ColumnF'     : [cero based list of float columns],  
                    'ResCtrlFlat' : [cero based flat list of result & control],
                },
            }
        rDI : dict
            Similar to 'do' but: 
                - No oc and df dict
                - With the values given by the user
                - Keys as in the GUI of the tab plus empty space.

        Running the analysis results in the creation of:
        - Parent Folder/
            - Input_Data_Files/
            - Steps_Data_Files/20210324-165609-Correlation-Analysis/
            - output-file.umsap

        The Input_Data_Files folder contains the original data files. These are 
        needed for data visualization, running analysis again with different 
        parameters, etc.
        The Steps_Data_Files/Date-Section folder contains regular csv files with 
        the step by step data.
    
        The Correlation Analysis section in output-file.umsap contains the 
        information about the calculations, e.g

        {
            'Correlation-Analysis : {
                '20210324-165609 - bla': {
                    'V' : config.dictVersion,
                    'I' : self.d,
                    'CI': self.do,
                    'DP': {
                        'dfF' : pd.DataFrame with initial data as float
                        'dfT' : pd.DataFrame with transformed data.
                        'dfN' : pd.DataFrame with normalized data.
                        'dfIm': pd.DataFrame with imputed data.
                    }
                    'R' : Path to result file
                }
            }
        }

        The data frame has the following structure
                      Intensity 01  Intensity 02  Intensity 03  Intensity 04  Intensity 05
        Intensity 01      1.000000      0.771523      0.162302      0.135884      0.565985
        Intensity 02      0.771523      1.000000      0.190120      0.110859      0.588783
        Intensity 03      0.162302      0.190120      1.000000      0.775442     -0.010327
        Intensity 04      0.135884      0.110859      0.775442      1.000000      0.010221
        Intensity 05      0.565985      0.588783     -0.010327      0.010221      1.000000

        The index and column names are the name of the selected columns in the 
        Data File.
    """
    #region -----------------------------------------------------> Class Setup
    #------------------------------> Label
    cLCorrMethod = 'Correlation Method'
    cLColAnalysis = mConfig.lStColAnalysis
    cLNumName     = mConfig.lLCtrlColNameI
    cSNumName     = mConfig.sLCtrlColI
    #------------------------------> Needed by BaseConfPanel
    cName        = mConfig.npCorrA
    cURL         = f"{mConfig.urlTutorial}/correlation-analysis"
    cSection     = mConfig.nuCorrA
    cTitlePD     = 'Calculating Correlation Coefficients'
    cGaugePD     = 26
    cTTHelp      = mConfig.ttBtnHelp.format(cURL)
    rLLenLongest = len(cLCorrMethod)
    rMainData    = '{}_{}-CorrelationCoefficients-Data.txt'
    #endregion --------------------------------------------------> Class Setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent: wx.Window, dataI: dict={}):
        """"""
        #region -----------------------------------------------> Initial setup
        #------------------------------> Setup attributes in base class 
        super().__init__(parent)
        #endregion --------------------------------------------> Initial setup

        #region -----------------------------------------------------> Widgets
        self.wCorrMethod = mWidget.StaticTextComboBox(self.wSbValue, 
            label     = self.cLCorrMethod,
            tooltip   = f'Select the {self.cLCorrMethod}.',
            choices   = list(mConfig.oCorrMethod.values()),
            validator = mValidator.IsNotEmpty(),
        )
        self.wStListI = wx.StaticText(
            self.wSbColumn, label=f'Columns in the {self.cLiFile}')
        self.wStListO = wx.StaticText(
            self.wSbColumn, label=f'{self.cLColAnalysis}')
        self.wLCtrlI = mWidget.MyListCtrlZebra(self.wSbColumn, 
            colLabel        = self.cLNumName,
            colSize         = self.cSNumName,
            copyFullContent = True,
        )
        self.wLCtrlO = mWidget.MyListCtrlZebra(self.wSbColumn, 
            colLabel        = self.cLNumName,
            colSize         = self.cSNumName,
            canPaste        = True,
            canCut          = True,
            copyFullContent = True,
        )
        self.rLCtrlL = [self.wLCtrlI, self.wLCtrlO]
        self.wAddCol = wx.Button(self.wSbColumn, label='Add columns')
        self.wAddCol.SetBitmap(
            wx.ArtProvider.GetBitmap(wx.ART_GO_FORWARD), dir = wx.RIGHT)
        #endregion --------------------------------------------------> Widgets

        #region -----------------------------------------------------> Tooltip
        self.wStListI.SetToolTip(mConfig.ttLCtrlCopyNoMod)
        self.wStListO.SetToolTip(mConfig.ttLCtrlPasteMod)
        self.wAddCol.SetToolTip(f'Add selected Columns in the Data File to '
            f'the table of Columns to Analyze. New columns will be added after '
            f'the last selected element in Columns to Analyze. Duplicate '
            f'columns are discarded.')
        #endregion --------------------------------------------------> Tooltip

        #region ------------------------------------------------------> Sizers
        #------------------------------> Values
        self.sSbValueWid.Add(
            1, 1,
            pos    = (0,0),
            flag   = wx.EXPAND|wx.ALL,
            border = 5
        )
        self.sSbValueWid.Add(
            self.wCorrMethod.wSt,
            pos    = (0,1),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL,
            border = 5,
        )
        self.sSbValueWid.Add(
            self.wCorrMethod.wCb,
            pos    = (0,2),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL,
            border = 5,
        )
        self.sSbValueWid.Add(
            1, 1,
            pos    = (0,3),
            flag   = wx.EXPAND|wx.ALL,
            border = 5
        )
        self.sSbValueWid.AddGrowableCol(0, 1)
        self.sSbValueWid.AddGrowableCol(3, 1)
        #------------------------------> Columns
        self.sSbColumnWid.Add(
            self.wStListI,
            pos    = (0,0),
            flag   = wx.ALIGN_CENTRE|wx.ALL,
            border = 5
        )
        self.sSbColumnWid.Add(
            self.wStListO,
            pos    = (0,2),
            flag   = wx.ALIGN_CENTRE|wx.ALL,
            border = 5
        )
        self.sSbColumnWid.Add(
            self.wLCtrlI,
            pos    = (1,0),
            flag   = wx.EXPAND|wx.ALL,
            border = 20
        )
        self.sSbColumnWid.Add(
            self.wAddCol,
            pos    = (1,1),
            flag   = wx.ALIGN_CENTER|wx.ALL,
            border = 20
        )
        self.sSbColumnWid.Add(
            self.wLCtrlO,
            pos    = (1,2),
            flag   = wx.EXPAND|wx.ALL,
            border = 20
        )
        self.sSbColumnWid.AddGrowableCol(0, 1)
        self.sSbColumnWid.AddGrowableCol(2, 1)
        self.sSbColumnWid.AddGrowableRow(1, 1)
        #------------------------------> Main Sizer
        #-------------->  Expand Column section
        item = self.sSizer.GetItem(self.sSbColumn)
        item.Proportion = 1
        item = self.sSbColumn.GetItem(self.sSbColumnWid)
        item.Proportion = 1
        self.SetSizer(self.sSizer)
        self.sSizer.Fit(self)
        self.SetupScrolling()
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind
        self.wAddCol.Bind(wx.EVT_BUTTON, self.OnAdd)
        #endregion -----------------------------------------------------> Bind

        #region ----------------------------------------------> checkUserInput
        rCheckUserInput = {
            self.cLCorrMethod : [self.wCorrMethod.wCb,       mConfig.mOptionBad,    False],
        }
        self.rCheckUserInput = self.rCheckUserInput | rCheckUserInput
        #endregion -------------------------------------------> checkUserInput

        #region --------------------------------------------------------> Test
        if mConfig.development:
            import getpass
            user = getpass.getuser()
            if mConfig.os == "Darwin":
                self.wUFile.wTc.SetValue("/Users/" + str(user) + "/TEMP-GUI/BORRAR-UMSAP/umsap-dev.umsap")
                fDataTemp = "/Users/" + str(user) + "/Dropbox/SOFTWARE-DEVELOPMENT/APPS/UMSAP/LOCAL/DATA/UMSAP-TEST-DATA/TARPROT/tarprot-data-file.txt"
                self.wIFile.wTc.SetValue(fDataTemp)
                self.IFileEnter(fDataTemp)
            elif mConfig.os == 'Windows':
                from pathlib import Path
                self.wUFile.wTc.SetValue(str(Path('C:/Users/bravo/Desktop/SharedFolders/BORRAR-UMSAP/umsap-dev.umsap')))
                self.wIFile.wTc.SetValue(str(Path(f'C:/Users/{user}/Dropbox/SOFTWARE-DEVELOPMENT/APPS/UMSAP/LOCAL/DATA/UMSAP-TEST-DATA/TARPROT/tarprot-data-file.txt')))
            else:
                pass
            self.wId.wTc.SetValue("Beta Version Dev")
            self.wCeroB.wCb.SetValue("Yes")
            self.wTransMethod.wCb.SetValue("Log2")
            self.wNormMethod.wCb.SetValue("Median")
            self.wImputationMethod.wCb.SetValue("Normal Distribution")
            self.OnImpMethod('fEvent')
            self.wShift.wTc.SetValue('1.8')
            self.wWidth.wTc.SetValue('0.3')
            self.wCorrMethod.wCb.SetValue("Pearson")
        else:
            pass
        #endregion -----------------------------------------------------> Test

        #region -------------------------------------------------------> DataI
        self.SetInitialData(dataI)
        #endregion ----------------------------------------------------> DataI
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Event Methods
    def OnAdd(self, event: Union[wx.Event, str]) -> bool:
        """Add columns to analyze using the button.

            Parameters
            ----------
            event : wx.Event
                Event information

            Returns
            -------
            bool
        """
        self.wLCtrlI.OnCopy('')
        self.wLCtrlO.OnPaste('')
        return True
    #---
    #endregion ------------------------------------------------> Event Methods

    #region ---------------------------------------------------> Class Methods
    def SetInitialData(self, dataI: dict={}) -> bool:
        """Set initial data.

            Parameters
            ----------
            dataI : dict
                Data to fill all fields and repeat an analysis. See Notes.

            Returns
            -------
            bool
        """
        if dataI:
            #------------------------------> 
            dataInit = dataI['uFile'].parent / mConfig.fnDataInit
            iFile = dataInit / dataI['I'][self.cLiFile]
            #------------------------------> 
            self.wUFile.wTc.SetValue(str(dataI['uFile']))
            self.wIFile.wTc.SetValue(str(iFile))
            self.wId.wTc.SetValue(dataI['CI']['ID'])
            #------------------------------> 
            self.wCeroB.wCb.SetValue(dataI['I'][self.cLCeroTreatD])
            self.wTransMethod.wCb.SetValue(dataI['I'][self.cLTransMethod])
            self.wNormMethod.wCb.SetValue(dataI['I'][self.cLNormMethod])
            self.wImputationMethod.wCb.SetValue(dataI['I'][self.cLImputation])
            self.wShift.wTc.SetValue(dataI['I'].get(self.cLShift, self.cValShift))
            self.wWidth.wTc.SetValue(dataI['I'].get(self.cLWidth, self.cValWidth))
            #------------------------------> 
            if iFile.exists:
                #------------------------------> Add columns with the same order
                l = []
                for k in dataI['CI']['oc']['Column']:
                    if len(l) == 0:
                        #------------------------------>
                        l.append(k)
                        continue
                    else:
                        #------------------------------>
                        if k > l[-1]:
                            #------------------------------>
                            l.append(k)
                            continue
                        else:
                            #------------------------------>
                            self.wLCtrlI.SelectList(l)
                            self.OnAdd('fEvent')
                            #------------------------------>
                            l = [k]
                #------------------------------> Last past
                self.wLCtrlI.SelectList(l)
                self.OnAdd('fEvent')
            else:
                pass
            #------------------------------> 
            self.OnImpMethod('fEvent')
        else:
            pass

        return True
    #---
    #endregion ------------------------------------------------> Class Methods

    #region ---------------------------------------------------> Run Analysis
    def CheckInput(self) -> bool:
        """Check user input

            Returns
            -------
            bool
        """
        #region -------------------------------------------------------> Super
        if super().CheckInput():
            pass
        else:
            return False
        #endregion ----------------------------------------------------> Super

        #region -------------------------------------------> Individual Fields
        #region -------------------------------------------> ListCtrl
        msgStep = self.cLPdCheck +  self.cLColAnalysis
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        if self.wLCtrlO.GetItemCount() > 1:
            pass
        else:
            self.rMsgError = mConfig.mRowsInLCtrl.format(2, self.cLColAnalysis)
            return False
        #endregion ----------------------------------------> ListCtrl
        #endregion ----------------------------------------> Individual Fields

        return True
    #---

    def PrepareRun(self) -> bool:
        """Set variable and prepare data for analysis.

            Returns
            -------
            bool
        """
        #region -------------------------------------------------------> Input
        msgStep = self.cLPdPrepare + 'User input, reading'
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)

        col  = [int(x) for x in self.wLCtrlO.GetColContent(0)]
        colF = [x for x in range(0, len(col))]
        impMethod = self.wImputationMethod.wCb.GetValue()
        #------------------------------> As given
        self.rDI = {
            self.EqualLenLabel(self.cLiFile) : (
                self.wIFile.wTc.GetValue()),
            self.EqualLenLabel(self.cLId) : (
                self.wId.wTc.GetValue()),
            self.EqualLenLabel(self.cLCeroTreatD) : (
                self.wCeroB.wCb.GetValue()),
            self.EqualLenLabel(self.cLTransMethod) : (
                self.wTransMethod.wCb.GetValue()),
            self.EqualLenLabel(self.cLNormMethod) : (
                self.wNormMethod.wCb.GetValue()),
            self.EqualLenLabel(self.cLImputation) : (
                impMethod),
            self.EqualLenLabel(self.cLShift) : (
                self.wShift.wTc.GetValue()),
            self.EqualLenLabel(self.cLWidth) : (
                self.wWidth.wTc.GetValue()),
            self.EqualLenLabel(self.cLCorrMethod) : (
                self.wCorrMethod.wCb.GetValue()),
            self.EqualLenLabel('Selected Columns') : col,
        }
        #------------------------------> 
        msgStep = self.cLPdPrepare + 'User input, processing'
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        #------------------------------> Dict with all values
        self.rDO = {
            'uFile'      : Path(self.wUFile.wTc.GetValue()),
            'iFile'      : Path(self.wIFile.wTc.GetValue()),
            'ID'         : self.wId.wTc.GetValue(),
            'Cero'       : mConfig.oYesNo[self.wCeroB.wCb.GetValue()],
            'TransMethod': self.wTransMethod.wCb.GetValue(),
            'NormMethod' : self.wNormMethod.wCb.GetValue(),
            'ImpMethod'  : impMethod,
            'Shift'      : float(self.wShift.wTc.GetValue()),
            'Width'      : float(self.wWidth.wTc.GetValue()),
            'CorrMethod' : self.wCorrMethod.wCb.GetValue(),
            'oc'         : {
                'Column'  : col,
                'ColumnF' : col,
            },
            'df'         : {
                'ColumnR'    : colF,
                'ColumnF'    : colF,
                'ResCtrlFlat': colF,
            }
        }
        #endregion ----------------------------------------------------> Input

        #region ---------------------------------------------------> Super
        if super().PrepareRun():
            pass
        else:
            self.rMsgError = 'Something went wrong when preparing the analysis.'
            return False
        #endregion ------------------------------------------------> Super

        return True
    #---

    def RunAnalysis(self) -> bool:
        """Calculate coefficients.

            Return
            ------
            bool
        """
        #region -------------------------------------------------------> Print
        if mConfig.development:
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
        else:
            pass
        #endregion ----------------------------------------------------> Print

        #region --------------------------------------------> Data Preparation
        if self.DataPreparation():
            pass
        else:
            return False
        #endregion -----------------------------------------> Data Preparation

        #region ------------------------------------> Correlation coefficients
        #------------------------------> Msg
        msgStep = self.cLPdRun + f"Correlation coefficients calculation"
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        #------------------------------> 
        try:
            self.dfR = self.dfIm.corr(method=self.rDO['CorrMethod'].lower())
        except Exception as e:
            self.rMsgError = str(e)
            self.rException = e
            return False
        #endregion ---------------------------------> Correlation coefficients

        return True
    #---

    def WriteOutput(self):
        """Write output. Override as needed"""
        #region --------------------------------------------------> Data Steps
        stepDict = self.SetStepDictDP()
        stepDict['Files'] = {
            mConfig.fnInitial.format(self.rDate, '01'): self.dfI,
            mConfig.fnFloat.format(self.rDate, '02')  : self.dfF,
            mConfig.fnTrans.format(self.rDate, '03')  : self.dfT,
            mConfig.fnNorm.format(self.rDate, '04')   : self.dfN,
            mConfig.fnImp.format(self.rDate, '05')    : self.dfIm,
            self.rMainData.format(self.rDate, '06')  : self.dfR,
        }
        stepDict['R'] = self.rMainData.format(self.rDate, '06')
        #endregion -----------------------------------------------> Data Steps

        return self.WriteOutputData(stepDict)
    #---
    #endregion ------------------------------------------------> Run Analysis
#---


class PaneDataPrep(BaseConfPanel):
    """Data Preparation utility.

        Parameters
        ----------
        parent: wx.Widget
            Parent of the pane
        dataI : dict or None
            Initial data provided by the user in a previous analysis.
            This contains both I and CI dicts e.g. {'I': I, 'CI': CI}.

        Notes
        -----
        The structure of self.rDO and self.rDI are:
        rDO: dict 
        {
            'iFile'      : Path(self.iFile.tc.GetValue()),
            'uFile'      : Path(self.uFile.tc.GetValue()),
            'ID'         : self.id.tc.GetValue(),
            'Cero'       : self.ceroB.IsChecked(),
            'NormMethod' : self.normMethod.cb.GetValue(),
            'TransMethod': self.transMethod.cb.GetValue(),
            'ImpMethod'  : self.imputationMethod.cb.GetValue(),
            'Shift'      : float,
            'Width'      : float,
            'oc'         : {
                'ColAnalysis': Columns for the analysis,
                'Column'     : Columns for the analysis,
                'ColumnF'    : Columns that must contain floats,
            },
            'df' : {
                'ResCtrlFlat': resCtrlFlat,
                'ColumnF'    : resCtrlFlat,
                'ColumnR'    : resCtrlFlat,
            },
        }
        rDI : dict
            Similar to 'do' but: 
                - No oc and df dict
                - With the values given by the user
                - Keys as in the GUI of the tab plus empty space.

        Running the analysis results in the creation of:
        - Parent Folder/
            - Input_Data_Files/
            - Steps_Data_Files/20210324-165609_Data Preparation/
            - output-file.umsap

        The Input_Data_Files folder contains the original data files. These are 
        needed for data visualization, running analysis again with different 
        parameters, etc.
        The Steps_Data_Files/Date-Section folder contains regular csv files with 
        the step by step data.

        The Data Preparation section in output-file.umsap contains the 
        information about the calculations, e.g
        {
            'Data Preparation : {
                '20210324-165609': {
                    'V' : config.dictVersion,
                    'I' : self.d,
                    'CI': self.do,
                    'DP': {
                        'dfF' : pd.DataFrame with initial data as float,
                        'dfT' : pd.DataFrame with transformed data,
                        'dfN' : pd.DataFrame with normalized data,
                        'dfIm': pd.DataFrame with imputed data,
                    },
                }
            }
        }
    """
    #region -----------------------------------------------------> Class setup
    #------------------------------> Label
    cLColAnalysis = mConfig.lStColAnalysis
    #------------------------------> Tooltips
    cTTColAnalysis = ('Columns on which to perform the Data Preparation.\ne.g. '
        '8 10-12')
    #------------------------------> Needed to Run
    cName        = mConfig.npDataPrep
    cURL         = f'{mConfig.urlTutorial}/data-preparation'
    cTTHelp      = mConfig.ttBtnHelp.format(cURL)
    cSection     = mConfig.nuDataPrep
    cTitlePD     = f"Running {mConfig.nuDataPrep} Analysis"
    cGaugePD     = 24
    rLLenLongest = len(cLColAnalysis)
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent: wx.Window, dataI: dict={}):
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(parent)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wSbValue.Hide()

        self.wColAnalysis = mWidget.StaticTextCtrl(
            self.wSbColumn,
            stLabel   = self.cLColAnalysis,
            stTooltip = self.cTTColAnalysis,
            tcSize    = self.cSTc,
            tcHint    = 'e.g. 130-135',
            validator = mValidator.NumberList(numType='int', sep=' ', vMin=0),
        )
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        #------------------------------> Sizer Columns
        self.sSbColumnWid.Add(
            1, 1,
            pos    = (0,0),
            flag   = wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sSbColumnWid.Add(
            self.wColAnalysis.wSt,
            pos    = (0,1),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT,
            border = 5,
            span   = (0,2),
        )
        self.sSbColumnWid.Add(
            self.wColAnalysis.wTc,
            pos    = (1,1),
            flag   = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL,
            border = 5,
            span   = (0,4),
        )
        self.sSbColumnWid.Add(
            1, 1,
            pos    = (0,5),
            flag   = wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sSbColumnWid.AddGrowableCol(0,1)
        self.sSbColumnWid.AddGrowableCol(2,1)
        self.sSbColumnWid.AddGrowableCol(4,2)
        self.sSbColumnWid.AddGrowableCol(5,1)
        #------------------------------> Main Sizer
        self.SetSizer(self.sSizer)
        self.sSizer.Fit(self)
        self.SetupScrolling()
        #endregion ---------------------------------------------------> Sizers

        #region -------------------------------------------------------> DataI
        self.SetInitialData(dataI)
        #endregion ----------------------------------------------------> DataI

        #region ----------------------------------------------> checkUserInput
        rCheckUserInput = {
            self.cLColAnalysis: [self.wColAnalysis.wTc,     mConfig.mNZPlusNumCol, True ],
        }
        self.rCheckUserInput = self.rCheckUserInput | rCheckUserInput
        #endregion -------------------------------------------> checkUserInput

        #region --------------------------------------------------------> Test
        if mConfig.development:
            import getpass
            user = getpass.getuser()
            if mConfig.os == "Darwin":
                self.wUFile.wTc.SetValue("/Users/" + str(user) + "/TEMP-GUI/BORRAR-UMSAP/umsap-dev.umsap")
                self.wIFile.wTc.SetValue("/Users/" + str(user) + "/Dropbox/SOFTWARE-DEVELOPMENT/APPS/UMSAP/LOCAL/DATA/UMSAP-TEST-DATA/PROTPROF/protprof-data-file.txt")
            elif mConfig.os == 'Windows':
                from pathlib import Path
                self.wUFile.wTc.SetValue(str(Path('C:/Users/bravo/Desktop/SharedFolders/BORRAR-UMSAP/umsap-dev.umsap')))
                self.wIFile.wTc.SetValue(str(Path('C:/Users/bravo/Dropbox/SOFTWARE-DEVELOPMENT/APPS/UMSAP/LOCAL/DATA/UMSAP-TEST-DATA/PROTPROF/protprof-data-file.txt')))
            else:
                pass
            self.wId.wTc.SetValue('Beta Test Dev')
            self.wCeroB.wCb.SetValue('Yes')
            self.wTransMethod.wCb.SetValue('Log2')
            self.wNormMethod.wCb.SetValue('Median')
            self.wImputationMethod.wCb.SetValue('Normal Distribution')  
            self.wColAnalysis.wTc.SetValue('130-135')
            self.OnImpMethod('fEvent')
            self.wShift.wTc.SetValue('1.8')
            self.wWidth.wTc.SetValue('0.3')
        else:
            pass
        #endregion -----------------------------------------------------> Test
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class Methods
    def SetInitialData(self, dataI: dict={}) -> bool:
        """Set initial data.

            Parameters
            ----------
            dataI : dict or None
                Data to fill all fields and repeat an analysis. See Notes.

            Returns
            -------
            True
        """
        #region -------------------------------------------------> Fill Fields
        if dataI:
            #------------------------------> 
            dataInit = dataI['uFile'].parent / mConfig.fnDataInit
            iFile = dataInit / dataI['I'][self.cLiFile]
            #------------------------------> Files
            self.wUFile.wTc.SetValue(str(dataI['uFile']))
            self.wIFile.wTc.SetValue(str(iFile))
            self.wId.wTc.SetValue(dataI['CI']['ID'])
            #------------------------------> Data Preparation
            self.wCeroB.wCb.SetValue(dataI['I'][self.cLCeroTreatD])
            self.wTransMethod.wCb.SetValue(dataI['I'][self.cLTransMethod])
            self.wNormMethod.wCb.SetValue(dataI['I'][self.cLNormMethod])
            self.wImputationMethod.wCb.SetValue(dataI['I'][self.cLImputation])
            self.wShift.wTc.SetValue(dataI['I'].get(self.cLShift, self.cValShift))
            self.wWidth.wTc.SetValue(dataI['I'].get(self.cLWidth, self.cValWidth))
            #------------------------------> Columns
            self.wColAnalysis.wTc.SetValue(dataI['I'][self.cLColAnalysis])
            #------------------------------> 
            self.OnIFileLoad('fEvent')
            self.OnImpMethod('fEvent')
        else:
            pass
        #endregion ----------------------------------------------> Fill Fields

        return True
    #---
    #endregion ------------------------------------------------> Class Methods

    #region ---------------------------------------------------> Run methods
    def CheckInput(self) -> bool:
        """Check user input

            Returns
            -------
            bool
        """
        #region -------------------------------------------------------> Super
        if super().CheckInput():
            pass
        else:
            return False
        #endregion ----------------------------------------------------> Super
        
        #region ----------------------------------------------------> All None
        a = self.wTransMethod.wCb.GetValue()
        b = self.wNormMethod.wCb.GetValue()
        c = self.wImputationMethod.wCb.GetValue()
        #------------------------------> 
        if a == b == c == 'None':
            self.rMsgError = (f'{self.cLTransMethod}, {self.cLNormMethod} and '
                f'{self.cLImputation} methods are all set to None. There is '
                f'nothing to be done.')
            return False
        else:
            pass
        #endregion -------------------------------------------------> All None

        return True
    #---

    def PrepareRun(self) -> bool:
        """Set variable and prepare data for analysis.

            Returns
            -------
            bool
        """
        #region -------------------------------------------------------> Input
        msgStep = self.cLPdPrepare + 'User input, reading'
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        #------------------------------> Variables
        impMethod = self.wImputationMethod.wCb.GetValue()
        #------------------------------> As given
        self.rDI = {
            self.EqualLenLabel(self.cLiFile) : (
                self.wIFile.wTc.GetValue()),
            self.EqualLenLabel(self.cLId) : (
                self.wId.wTc.GetValue()),
            self.EqualLenLabel(self.cLCeroTreatD) : (
                self.wCeroB.wCb.GetValue()),
            self.EqualLenLabel(self.cLTransMethod) : (
                self.wTransMethod.wCb.GetValue()),
            self.EqualLenLabel(self.cLNormMethod) : (
                self.wNormMethod.wCb.GetValue()),
            self.EqualLenLabel(self.cLImputation) : (
                impMethod),
            self.EqualLenLabel(self.cLShift) : (
                self.wShift.wTc.GetValue()),
            self.EqualLenLabel(self.cLWidth) : (
                self.wWidth.wTc.GetValue()),
            self.EqualLenLabel(self.cLColAnalysis): (
                self.wColAnalysis.wTc.GetValue()),
        }
        #------------------------------> Dict with all values
        #-------------->
        msgStep = self.cLPdPrepare + 'User input, processing'
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        #--------------> 
        colAnalysis = mMethod.Str2ListNumber(
            self.wColAnalysis.wTc.GetValue(), sep=' ',
        )
        resCtrlFlat = [x for x in range(0, len(colAnalysis))]
        #--------------> 
        self.rDO  = {
            'iFile'      : Path(self.wIFile.wTc.GetValue()),
            'uFile'      : Path(self.wUFile.wTc.GetValue()),
            'ID'         : self.wId.wTc.GetValue(),
            'Cero'       : mConfig.oYesNo[self.wCeroB.wCb.GetValue()],
            'NormMethod' : self.wNormMethod.wCb.GetValue(),
            'TransMethod': self.wTransMethod.wCb.GetValue(),
            'ImpMethod'  : impMethod,
            'Shift'      : float(self.wShift.wTc.GetValue()),
            'Width'      : float(self.wWidth.wTc.GetValue()),
            'oc'         : {
                'ColAnalysis': colAnalysis,
                'Column'     : colAnalysis,
                'ColumnF'    : colAnalysis,
            },
            'df' : {
                'ColumnR'    : resCtrlFlat,
                'ResCtrlFlat': resCtrlFlat,
                'ColumnF'    : resCtrlFlat,
            },
        }
        #endregion ----------------------------------------------------> Input

        #region ---------------------------------------------------> Super
        if super().PrepareRun():
            pass
        else:
            self.rMsgError = 'Something went wrong when preparing the analysis.'
            return False
        #endregion ------------------------------------------------> Super

        return True
    #---

    def RunAnalysis(self) -> bool:
        """Perform data preparation
        
            Returns
            -------
            bool
        """
        #region -------------------------------------------------------> Print
        if mConfig.development:
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
        else:
            pass
        #endregion ----------------------------------------------------> Print
        
        #region --------------------------------------------> Data Preparation
        if self.DataPreparation():
            pass
        else:
            return False
        #endregion -----------------------------------------> Data Preparation

        return True
    #---

    def WriteOutput(self) -> bool:
        """Write output.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------> Data Steps
        stepDict = self.SetStepDictDP()
        stepDict['Files'] = {
            mConfig.fnInitial.format(self.rDate, '01'): self.dfI,
            mConfig.fnFloat.format(self.rDate, '02')  : self.dfF,
            mConfig.fnTrans.format(self.rDate, '03')  : self.dfT,
            mConfig.fnNorm.format(self.rDate, '04')   : self.dfN,
            mConfig.fnImp.format(self.rDate, '05')    : self.dfIm,
        }
        #endregion -----------------------------------------------> Data Steps

        return self.WriteOutputData(stepDict)
    #---
    #endregion ------------------------------------------------> Run methods
#---


class PaneProtProf(BaseConfPanelMod):
    """Creates the Proteome Profiling configuration tab.

        Parameters
        ----------
        parent: wx.Widget
            Parent of the pane
        dataI : dict or None
            Initial data provided by the user in a previous analysis.
            This contains both I and CI dicts e.g. {'I': I, 'CI': CI}.

        Attributes
        ----------
        dCheckRepNum: dict
            Methods to check the replicate numbers.
        dColCtrlData: dict
            Methods to get the Columns for Control Experiments. 
        rDI: dict
            Dictionary with the user input. Keys are labels in the panel plus:
            {
                config.lStProtProfCond          : [list of conditions],
                config.lStProtProfRP            : [list of relevant points],
                f"Control {config.lStCtrlType}" : "Control Type",
                f"Control {config.lStCtrlName}" : "Control Name",
            }
        rDO: dict
            Dictionary with checked user input. Keys are:
            {
                "iFile"      : "Path to input data file",
                "uFile"      : "Path to umsap file.",
                'ID'         : 'Analysis ID',
                "ScoreVal"   : "Score value threshold",
                "RawI"       : "Raw intensity or not. Boolean",
                "IndS"       : "Independent samples or not. Boolean,
                "Cero"       : Boolean, how to treat cero values,
                "TransMethod": "Transformation method",
                "NormMethod" : "Normalization method",
                "ImpMethod"  : "Imputation method",
                "Shift"      : "float",
                "Width:      : "float",
                "Alpha"      : "Significance level",
                "CorrectP"   : "Method to correct P values",
                "Cond"       : [List of conditions],
                "RP"         : [List of relevant points],
                "ControlT"   : "Control type",
                "ControlL"   : "Control label",
                "oc": {
                    "DetectedP": "Detected Proteins column. Int",
                    "GeneName" : "Gene name column. Int",
                    "ScoreCol" : "Score column. Int",
                    "ExcludeP" : [List of columns to search for proteins to 
                                exclude. List of int],
                    "ResCtrl": [List of columns containing the control and 
                                experiments column numbers],
                    "ColumnF" : [Column that must contain floats],
                    "Column": [Flat list of all column numbers with the 
                              following order: Gene Names, Detected Proteins, 
                              Score, Exclude Proteins, Res & Control]
                },
                "df": { Column numbers in the pd.df created from the input file.
                    "DetectedP": 0,
                    "GeneName" : 1,
                    "ScoreCol" : 2,
                    "ExcludeP" : [list of int],
                    "ResCtrl": [],
                    "ResCtrlFlat": [ResCtrl as a flat list],
                    "ColumnR : [Columns with the results] 
                    "ColumnF": [Columns that must contain only float numbers]
                }
            },    
        rLbDict: dict
            Contains information about the Res - Ctrl e.g.
            {
                0            : ['C1', 'C2'],
                1            : ['RP1', 'RP2'],
                'Control'    : ['TheControl'],
                'ControlType': 'One Control per Column',
            }
        See Parent classes for more attributes.

        Notes
        -----
        Running the analysis results in the creation of:

        - Parent Folder/
            - Input_Data_Files/
            - Steps_Data_Files/20210324-165609-Proteome-Profiling/
            - output-file.umsap

        The Input_Data_Files folder contains the original data files. These are 
        needed for data visualization, running analysis again with different 
        parameters, etc.
        The Steps_Data_Files/Date-Section folder contains regular csv files with 
        the step by step data.

        The Proteome Profiling section in output-file.umsap contains the 
        information about the calculations, e.g

        {
            'Proteome-Profiling : {
                '20210324-165609': {
                    'V' : config.dictVersion,
                    'I' : self.d,
                    'CI': self.do,
                    'DP': {
                        'dfS' : pd.DataFrame with initial data as float and
                                after discarding values by score.
                        'dfT' : pd.DataFrame with transformed data.
                        'dfN' : pd.DataFrame with normalized data.
                        'dfIm': pd.DataFrame with imputed data.
                    }
                    'R' : Path to the file with the calculation results.
                    'F' : Dict for Filters.
                }
            }
        }

        The result data frame has the following structure:

        Gene Protein Score C1 ..... CN
        Gene Protein Score RP1 ..... RPN
        Gene Protein Score aveC stdC ave std P Pc FC CI FCz

        where all FC related values are for log2FC
    """
    #region -----------------------------------------------------> Class setup
    cName = mConfig.npProtProf
    #------------------------------> Needed by BaseConfPanel
    cURL         = f'{mConfig.urlTutorial}/proteome-profiling'
    cSection     = mConfig.nmProtProf
    cTitlePD     = f"Running {mConfig.nmProtProf} Analysis"
    cGaugePD     = 38
    rLLenLongest = len(mConfig.lStResultCtrlS)
    rMainData    = '{}_{}-ProteomeProfiling-Data.txt'
    #------------------------------> Optional configuration
    cTTHelp = mConfig.ttBtnHelp.format(cURL)
    #------------------------------> Label
    cLCorrectP     = mConfig.lCbCorrectP
    cLSample       = mConfig.lCbSample
    cLGene         = mConfig.lStGeneName
    cLExcludeProt  = mConfig.lStExcludeProt
    cLDetectedProt = 'Detected Proteins'
    cLCond         = mConfig.lStProtProfCond
    cLRP           = mConfig.lStProtProfRP
    cLCtrlType     = mConfig.lStCtrlType
    cLCtrlName     = mConfig.lStCtrlName
    cLDFThreeCol   = mConfig.dfcolProtprofFirstThree
    cLDFThirdLevel = mConfig.dfcolProtprofCLevel
    #------------------------------> Choices
    cOCorrectP  = mConfig.oCorrectP
    cOSample    = mConfig.oSamples
    # cOIntensity = mConfig.oIntensities
    #------------------------------> Tooltip
    cTTCorrectP    = mConfig.ttStCorrectP
    cTTSample      = mConfig.ttStSample
    cTTGene        = mConfig.ttStGenName
    cTTExcludeProt = f'{mConfig.ttStExcludeProt}{mConfig.mOptField}'
    #------------------------------> Control Type
    cDCtrlType = mConfig.oControlTypeProtProf
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent, dataI: dict={}):
        """ """
        #region -----------------------------------------------> Initial Setup
        #------------------------------> Base attributes and setup
        super().__init__(parent)
        #------------------------------> Dict with methods
        self.dColCtrlData = {
            self.cDCtrlType['OC']   : self.ColCtrlData_OC,
            self.cDCtrlType['OCC']  : self.ColCtrlData_OCC,
            self.cDCtrlType['OCR']  : self.ColCtrlData_OCR,
            self.cDCtrlType['Ratio']: self.ColCtrlData_Ratio,
        }
        self.dCheckRepNum = {
            self.cDCtrlType['OC']   : self.CheckRepNum_OC,
            self.cDCtrlType['OCC']  : self.CheckRepNum_OCC,
            self.cDCtrlType['OCR']  : self.CheckRepNum_OCR,
            self.cDCtrlType['Ratio']: self.CheckRepNum_Ratio,
        }
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        #------------------------------> Values
        self.wCorrectP = mWidget.StaticTextComboBox(
            self.wSbValue,
            label     = self.cLCorrectP,
            choices   = list(self.cOCorrectP.keys()),
            tooltip   = self.cTTCorrectP,
            validator = mValidator.IsNotEmpty(),
        )
        self.wSample = mWidget.StaticTextComboBox(
            self.wSbValue,
            label     = self.cLSample,
            choices   = list(self.cOSample.keys()),
            tooltip   = self.cTTSample,
            validator = mValidator.IsNotEmpty(),
        )
        #------------------------------> Columns
        self.wGeneName = mWidget.StaticTextCtrl(
            self.wSbColumn,
            stLabel   = self.cLGene,
            stTooltip = self.cTTGene,
            tcSize    = self.cSTc,
            tcHint    = 'e.g. 6',
            validator = mValidator.NumberList(numType='int', nN=1, vMin=0),
        )
        self.wExcludeProt = mWidget.StaticTextCtrl(
            self.wSbColumn,
            stLabel   = self.cLExcludeProt,
            stTooltip = self.cTTExcludeProt,
            tcSize    = self.cSTc,
            tcHint    = 'e.g. 171-173',
            validator = mValidator.NumberList(
                numType='int', sep=' ', vMin=0, opt=True),
        )
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        #------------------------------> Sizer Values
        self.sSbValueWid.Add(
            1, 1,
            pos    = (0,0),
            flag   = wx.EXPAND|wx.ALL,
            border = 5,
            span   = (2, 0),
        )
        self.sSbValueWid.Add(
            self.wScoreVal.wSt,
            pos    = (0,1),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sSbValueWid.Add(
            self.wScoreVal.wTc,
            pos    = (0,2),
            flag   = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sSbValueWid.Add(
            self.wSample.wSt,
            pos    = (1,1),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sSbValueWid.Add(
            self.wSample.wCb,
            pos    = (1,2),
            flag   = wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sSbValueWid.Add(
            self.wAlpha.wSt,
            pos    = (0,3),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sSbValueWid.Add(
            self.wAlpha.wTc,
            pos    = (0,4),
            flag   = wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sSbValueWid.Add(
            self.wCorrectP.wSt,
            pos    = (1,3),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sSbValueWid.Add(
            self.wCorrectP.wCb,
            pos    = (1,4),
            flag   = wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sSbValueWid.Add(
            1, 1,
            pos    = (0,5),
            flag   = wx.EXPAND|wx.ALL,
            border = 5,
            span   = (2, 0),
        )
        self.sSbValueWid.AddGrowableCol(0, 1)
        self.sSbValueWid.AddGrowableCol(5, 1)
        #------------------------------> Sizer Columns
        self.sSbColumnWid.Add(
            self.wDetectedProt.wSt,
            pos    = (0,0),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sSbColumnWid.Add(
            self.wDetectedProt.wTc,
            pos    = (0,1),
            flag   = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sSbColumnWid.Add(
            self.wGeneName.wSt,
            pos    = (0,2),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sSbColumnWid.Add(
            self.wGeneName.wTc,
            pos    = (0,3),
            flag   = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sSbColumnWid.Add(
            self.wScore.wSt,
            pos    = (0,4),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sSbColumnWid.Add(
            self.wScore.wTc,
            pos    = (0,5),
            flag   = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sSbColumnWid.Add(
            self.wExcludeProt.wSt,
            pos    = (1,0),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sSbColumnWid.Add(
            self.wExcludeProt.wTc,
            pos    = (1,1),
            flag   = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL,
            border = 5,
            span   = (0, 5),
        )
        self.sSbColumnWid.Add(
            self.sRes,
            pos    = (2,0),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND,
            border = 0,
            span   = (0,6),
        )
        self.sSbColumnWid.AddGrowableCol(1,1)
        self.sSbColumnWid.AddGrowableCol(3,1)
        self.sSbColumnWid.AddGrowableCol(5,1)
        #------------------------------> Main Sizer
        self.SetSizer(self.sSizer)
        self.sSizer.Fit(self)
        self.SetupScrolling()
        #endregion ---------------------------------------------------> Sizers

        #region ----------------------------------------------> checkUserInput
        rCheckUserInput = {
            self.cLScoreVal    : [self.wScoreVal.wTc,     mConfig.mOneRealNum    , False],
            self.cLSample      : [self.wSample.wCb,       mConfig.mOptionBad     , False],
            self.cLAlpha       : [self.wAlpha.wTc,        mConfig.mOne01Num      , False],
            self.cLCorrectP    : [self.wCorrectP.wCb,     mConfig.mOptionBad     , False],
            self.cLDetectedProt: [self.wDetectedProt.wTc, mConfig.mOneZPlusNumCol, True ],
            self.cLGene        : [self.wGeneName.wTc,     mConfig.mOneZPlusNumCol, True ],
            self.cLScoreCol    : [self.wScore.wTc,        mConfig.mOneZPlusNumCol, True ],
            self.cLExcludeProt : [self.wExcludeProt.wTc,  mConfig.mNZPlusNumCol  , True ],
            self.cLResControl  : [self.wTcResults,        mConfig.mResCtrl       , False]
        }
        self.rCheckUserInput = self.rCheckUserInput | rCheckUserInput
        #------------------------------> 
        self.rCheckUnique = [self.wDetectedProt.wTc, self.wGeneName.wTc,
            self.wScore.wTc, self.wExcludeProt.wTc, self.wTcResults]
        #endregion -------------------------------------------> checkUserInput

        #region -------------------------------------------------------> DataI
        self.SetInitialData(dataI)
        #endregion ----------------------------------------------------> DataI

        #region --------------------------------------------------------> Test
        if mConfig.development:
            import getpass
            user = getpass.getuser()
            if mConfig.os == "Darwin":
                self.wUFile.wTc.SetValue("/Users/" + str(user) + "/TEMP-GUI/BORRAR-UMSAP/umsap-dev.umsap")
                self.wIFile.wTc.SetValue("/Users/" + str(user) + "/Dropbox/SOFTWARE-DEVELOPMENT/APPS/UMSAP/LOCAL/DATA/UMSAP-TEST-DATA/PROTPROF/protprof-data-file.txt")
            elif mConfig.os == 'Windows':
                from pathlib import Path
                self.wUFile.wTc.SetValue(str(Path('C:/Users/bravo/Desktop/SharedFolders/BORRAR-UMSAP/umsap-dev.umsap')))
                self.wIFile.wTc.SetValue(str(Path('C:/Users/bravo/Dropbox/SOFTWARE-DEVELOPMENT/APPS/UMSAP/LOCAL/DATA/UMSAP-TEST-DATA/PROTPROF/protprof-data-file.txt')))
            else:
                pass
            self.wScoreVal.wTc.SetValue('320')
            self.wId.wTc.SetValue('Beta Test Dev')
            self.wCeroB.wCb.SetValue('Yes')
            self.wTransMethod.wCb.SetValue('Log2')
            self.wNormMethod.wCb.SetValue('Median')
            self.wImputationMethod.wCb.SetValue('Normal Distribution')
            self.wAlpha.wTc.SetValue('0.05')
            self.wSample.wCb.SetValue('Independent Samples')
            self.wCorrectP.wCb.SetValue('Benjamini - Hochberg')
            self.wDetectedProt.wTc.SetValue('0')
            self.wGeneName.wTc.SetValue('6')
            self.wScore.wTc.SetValue('39')
            self.wExcludeProt.wTc.SetValue('171 172 173')
            #------------------------------> 
            #--> One Control per Column, 2 Cond and 2 TP
            # self.wTcResults.SetValue('105 115 125, 130 131 132; 106 116 126, 101 111 121; 108 118 128, 103 113 123')
            # self.rLbDict = {
            #     0            : ['C1', 'C2'],
            #     1            : ['RP1', 'RP2'],
            #     'Control'    : ['TheControl'],
            #     'ControlType': 'One Control per Column',
            # }
            #--> One Control per Row, 1 Cond and 2 TP
            # self.wTcResults.SetValue('105 115 125, 106 116 126, 101 111 121')
            # self.rLbDict = {
            #     0            : ['DMSO'],
            #     1            : ['30min', '60min'],
            #     'Control'    : ['MyControl'],
            #     'ControlType': 'One Control per Row',
            # }
            #--> One Control 2 Cond and 2 TP
            self.wTcResults.SetValue('105 115 125; 106 116 126, 101 111 121; 108 118 128, 103 113 123')
            self.rLbDict = {
                0            : ['C1', 'C2'],
                1            : ['RP1', 'RP2'],
                'Control'    : ['1Control'],
                'ControlType': 'One Control',
            }
            #--> Ratio 2 Cond and 2 TP
            # self.wTcResults.SetValue('106 116 126, 101 111 121; 108 118 128, 103 113 123')
            # self.rLbDict = {
            #     0            : ['C1', 'C2'],
            #     1            : ['RP1', 'RP2'],
            #     'Control'    : ['1Control'],
            #     'ControlType': 'Ratio of Intensities',
            # }
            self.OnImpMethod('fEvent')
            self.wShift.wTc.SetValue('1.8')
            self.wWidth.wTc.SetValue('0.3')
        else:
            pass
        #endregion -----------------------------------------------------> Test
    #---
    #endregion -----------------------------------------------> Instance setup

    #region --------------------------------------------------> Class Methods
    def SetInitialData(self, dataI: dict={}) -> bool:
        """Set initial data.

            Parameters
            ----------
            dataI : dict or None
                Data to fill all fields and repeat an analysis. See Notes.

            Returns
            -------
            True
        """
        #region -------------------------------------------------> Fill Fields
        if dataI:
            #------------------------------> 
            dataInit = dataI['uFile'].parent / mConfig.fnDataInit
            iFile = dataInit / dataI['I'][self.cLiFile]
            #------------------------------> 
            self.wUFile.wTc.SetValue(str(dataI['uFile']))
            self.wIFile.wTc.SetValue(str(iFile))
            self.wId.wTc.SetValue(dataI['CI']['ID'])
            #------------------------------> Data Preparation
            self.wCeroB.wCb.SetValue(dataI['I'][self.cLCeroTreatD])
            self.wTransMethod.wCb.SetValue(dataI['I'][self.cLTransMethod])
            self.wNormMethod.wCb.SetValue(dataI['I'][self.cLNormMethod])
            self.wImputationMethod.wCb.SetValue(dataI['I'][self.cLImputation])
            self.wShift.wTc.SetValue(dataI['I'].get(self.cLShift, self.cValShift))
            self.wWidth.wTc.SetValue(dataI['I'].get(self.cLWidth, self.cValWidth))
            #------------------------------> Values
            self.wScoreVal.wTc.SetValue(dataI['I'][self.cLScoreVal])
            self.wSample.wCb.SetValue(dataI['I'][self.cLSample])
            self.wAlpha.wTc.SetValue(dataI['I'][self.cLAlpha])
            self.wCorrectP.wCb.SetValue(dataI['I'][self.cLCorrectP])
            #------------------------------> Columns
            self.wDetectedProt.wTc.SetValue(dataI['I'][self.cLDetectedProt])
            self.wGeneName.wTc.SetValue(dataI['I'][self.cLGene])
            self.wScore.wTc.SetValue(dataI['I'][self.cLScoreCol])
            self.wExcludeProt.wTc.SetValue(dataI['I'][self.cLExcludeProt])
            self.wTcResults.SetValue(dataI['I'][mConfig.lStResultCtrlS])
            self.rLbDict[1] = dataI['I'][self.cLCond]
            self.rLbDict[2] = dataI['I'][self.cLRP]
            self.rLbDict['ControlType'] = dataI['I'][f'Control {self.cLCtrlType}']
            self.rLbDict['Control'] = dataI['I'][f"Control {self.cLCtrlName}"]
            #------------------------------> 
            self.OnIFileLoad('fEvent')
            self.OnImpMethod('fEvent')
        else:
            pass
        #endregion ----------------------------------------------> Fill Fields
        
        return True
    #---

    def CheckNumberReplicates(self) -> bool:
        """Check the number of replicates when samples are paired and raw 
            intensities are used.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> ResCtrl
        resCtrl = mMethod.ResControl2ListNumber(self.wTcResults.GetValue())
        #endregion ------------------------------------------------> ResCtrl

        #region ---------------------------------------------------> Check
        if self.dCheckRepNum[self.rLbDict["ControlType"]](resCtrl):
            return True
        else:
            return False
        #endregion ------------------------------------------------> Check
    #---

    def CheckRepNum_OC(self, resCtrl: list[list[list[int]]]) -> bool:
        """Check equal number of replicas.

            Parameters
            ----------
            resCtrl: list[list[list[int]]]
                Result and Control as a list of list of list of int.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        badRep = []
        #endregion ------------------------------------------------> Variables

        #region ---------------------------------------------------> Check
        #------------------------------> 
        ctrlL = len(resCtrl[0][0])
        #------------------------------> 
        for row in resCtrl:
            for col in row:
                if len(col) == ctrlL:
                    pass
                else:
                    badRep.append(col)
        #endregion ------------------------------------------------> Check

        #region ---------------------------------------------------> Return
        if not badRep:
            return True
        else:
            self.rMsgError = mConfig.mRepNum
            self.rException = mException.InputError(
                mConfig.mRepNumProtProf.format(badRep))
            return False
        #endregion ------------------------------------------------> Return
    #---

    def CheckRepNum_Ratio(self, resCtrl: list[list[list[int]]]) -> bool:
        """Check equal number of replicas. Only needed for completion.

            Parameters
            ----------
            resCtrl: list[list[list[int]]]
                Result and Control as a list of list of list of int.

            Returns
            -------
            bool
        """
        return True
    #---

    def CheckRepNum_OCC(self, resCtrl: list[list[list[int]]]) -> bool:
        """Check equal number of replicas.

            Parameters
            ----------
            resCtrl: list[list[list[int]]]
                Result and Control as a list of list of list of int.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        badRep = []
        rowL = len(resCtrl)
        colL = len(resCtrl[0])
        #endregion ------------------------------------------------> Variables

        #region ---------------------------------------------------> Check
        for colI in range(0, colL):
            ctrlL = len(resCtrl[0][colI])
            for rowI in range(1,rowL):
                if len(resCtrl[rowI][colI]) == ctrlL:
                    pass
                else:
                    badRep.append(resCtrl[rowI][colI])
        #endregion ------------------------------------------------> Check

        #region ---------------------------------------------------> Return
        if not badRep:
            return True
        else:
            self.rMsgError = mConfig.mRepNum
            self.rException = mException.InputError(
                mConfig.mRepNumProtProf.format(badRep))
            return False
        #endregion ------------------------------------------------> Return
    #---

    def CheckRepNum_OCR(self, resCtrl: list[list[list[int]]]) -> bool:
        """Check equal number of replicas.

            Parameters
            ----------
            resCtrl: list[list[list[int]]]
                Result and Control as a list of list of list of int.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        badRep = []
        #endregion ------------------------------------------------> Variables

        #region ---------------------------------------------------> Check
        for row in resCtrl:
            #------------------------------>
            ctrlL = len(row[0])
            #------------------------------>
            for col in row[1:]:
                if len(col) == ctrlL:
                    pass
                else:
                    badRep.append(col)
        #endregion ------------------------------------------------> Check

        #region ---------------------------------------------------> Return
        if not badRep:
            return True
        else:
            self.rMsgError = mConfig.mRepNum
            self.rException = mException.InputError(
                mConfig.mRepNumProtProf.format(badRep))
            return False
        #endregion ------------------------------------------------> Return
    #---

    def EmptyDFR(self) -> pd.DataFrame:
        """Creates the empty data frame for the output. This data frame contains
            the values for Gene, Protein and Score.

            Returns
            -------
            pd.DataFrame
        """
        #region -------------------------------------------------------> Index
        #------------------------------> First Three Columns
        aL = self.cLDFThreeCol
        bL = self.cLDFThreeCol
        cL = self.cLDFThreeCol
        #------------------------------> Columns per Point
        n = len(self.cLDFThirdLevel)
        #------------------------------> Other columns
        for c in self.rDO['Cond']:
            for t in self.rDO['RP']:
                aL = aL + n*[c]
                bL = bL + n*[t]
                cL = cL + self.cLDFThirdLevel
        #------------------------------> 
        idx = pd.MultiIndex.from_arrays([aL[:], bL[:], cL[:]])
        #endregion ----------------------------------------------------> Index

        #region ----------------------------------------------------> Empty DF
        df = pd.DataFrame(np.nan, columns=idx, index=range(self.dfS.shape[0])) # type: ignore
        #endregion -------------------------------------------------> Empty DF

        #region -----------------------------------------> First Three Columns
        df[(aL[0], bL[0], cL[0])] = self.dfS.iloc[:,0]
        df[(aL[1], bL[1], cL[1])] = self.dfS.iloc[:,1]
        df[(aL[2], bL[2], cL[2])] = self.dfS.iloc[:,2]
        #endregion --------------------------------------> First Three Columns

        return df
    #---

    def ColCtrlData_OC(self, c:int, t:int) -> list[list[int]]:
        """Get the Ctrl and Data columns for the given condition and relevant
            point when Control Type is: One Control.

            Parameters
            ----------
            c: int
                Condition index in self.do['df']['ResCtrl]
            t: int
                Relevant point index in self.do['df']['ResCtrl]

            Returns
            -------
            list[list[int]]
        """
        #region ---------------------------------------------------> List
        #------------------------------> 
        colC = self.rDO['df']['ResCtrl'][0][0]
        #------------------------------> 
        colD = self.rDO['df']['ResCtrl'][c+1][t]
        #endregion ------------------------------------------------> List

        return [colC, colD]
    #---

    def ColCtrlData_OCC(self, c:int, t:int) -> list[list[int]]:
        """Get the Ctrl and Data columns for the given condition and relevant
            point when Control Type is: One Control per Column.

            Parameters
            ----------
            c: int
                Condition index in self.do['df']['ResCtrl]
            t: int
                Relevant point index in self.do['df']['ResCtrl]

            Returns
            -------
            list[list[int]]
        """
        #region ---------------------------------------------------> List
        #------------------------------> 
        colC = self.rDO['df']['ResCtrl'][0][t]
        #------------------------------> 
        colD = self.rDO['df']['ResCtrl'][c+1][t]
        #endregion ------------------------------------------------> List

        return [colC, colD]
    #---

    def ColCtrlData_OCR(self, c:int, t:int) -> list[list[int]]:
        """Get the Ctrl and Data columns for the given condition and relevant
            point when Control Type is: One Control per Row

            Parameters
            ----------
            c: int
                Condition index in self.do['df']['ResCtrl]
            t: int
                Relevant point index in self.do['df']['ResCtrl]

            Returns
            -------
            list[list[int]]
        """
        #region ---------------------------------------------------> List
        #------------------------------> 
        colC = self.rDO['df']['ResCtrl'][c][0]
        #------------------------------> 
        colD = self.rDO['df']['ResCtrl'][c][t+1]
        #endregion ------------------------------------------------> List

        return [colC, colD]
    #---

    def ColCtrlData_Ratio(self, c:int, t:int) -> list[list[int]]:
        """Get the Ctrl and Data columns for the given condition and relevant
            point when Control Type is: Data as Ratios.

            Parameters
            ----------
            c: int
                Condition index in self.do['df']['ResCtrl]
            t: int
                Relevant point index in self.do['df']['ResCtrl]

            Returns
            -------
            list[list[int]]
        """
        #region ---------------------------------------------------> List
        #------------------------------> 
        colC = []
        #------------------------------> 
        colD = self.rDO['df']['ResCtrl'][c][t]
        #endregion ------------------------------------------------> List

        return [colC, colD]
    #---

    def CalcOutData(
        self, cN: str, tN: str, colC: list[int], colD: list[int]
    ) -> bool:
        """Calculate the data for the main output dataframe.

            Parameters
            ----------
            cN: str
                Condition name.
            tN: str
                Relevant point name.
            colC: list[int]
                Column numbers for the control. Empty list for Ration of 
                intensities.
            colD: list[int]
                Column numbers for the experiment.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Print
        if mConfig.development:
            print(cN, tN, colC, colD)
        #endregion ------------------------------------------------> Print

        #region ---------------------------------------------------> Ave & Std
        if colC:
            self.dfR.loc[:,(cN, tN, 'aveC')] = self.dfS.iloc[:,colC].mean(
                axis=1, skipna=True).to_numpy() # type: ignore
            self.dfR.loc[:,(cN, tN, 'stdC')] = self.dfS.iloc[:,colC].std(
                axis=1, skipna=True).to_numpy() # type: ignore
        else:
            self.dfR.loc[:,(cN, tN, 'aveC')] = np.nan
            self.dfR.loc[:,(cN, tN, 'stdC')] = np.nan
        #------------------------------>
        self.dfR.loc[:,(cN, tN, 'ave')] = self.dfS.iloc[:,colD].mean(
            axis=1, skipna=True).to_numpy() # type: ignore
        self.dfR.loc[:,(cN, tN, 'std')] = self.dfS.iloc[:,colD].std(
            axis=1, skipna=True).to_numpy() # type: ignore
        #endregion ------------------------------------------------> Ave & Std

        #region --------------------------------------------> Log2 Intensities
        dfLogI = self.dfS.copy() 
        if self.rDO['TransMethod'] == 'Log2':
            pass
        else:
            if colC:
                dfLogI.iloc[:,colC+colD] = np.log2(dfLogI.iloc[:,colC+colD])
            else:
                dfLogI.iloc[:,colD] = np.log2(dfLogI.iloc[:,colD])
        #endregion -----------------------------------------> Log2 Intensities

        #region ----------------------------------------------------> Log2(FC)
        if colC:
            FC = (
                dfLogI.iloc[:,colD].mean(axis=1, skipna=True) # type: ignore
                - dfLogI.iloc[:,colC].mean(axis=1, skipna=True) # type: ignore
            )
        else:
            FC = dfLogI.iloc[:,colD].mean(axis=1, skipna=True) # type: ignore
        #------------------------------>
        self.dfR.loc[:, (cN, tN, 'FC')] = FC.to_numpy() # type: ignore
        #endregion -------------------------------------------------> Log2(FC)

        #region ---------------------------------------------------> FCz
        self.dfR.loc[:,(cN, tN, 'FCz')] = (FC - FC.mean()).div(FC.std()).to_numpy() # type: ignore
        #endregion ------------------------------------------------> FCz

        #region ---------------------------------------------------> FC CI
        if self.rDO['RawI']:
            self.dfR.loc[:,(cN, tN, 'CI')] = mStatistic.CI_Mean_Diff_DF(
                dfLogI,
                colC,
                colD,
                self.rDO['Alpha'],
                self.rDO['IndS'],
                fullCI=False,
            ).to_numpy()
        else:
            self.dfR.loc[:,(cN, tN, 'CI')] = mStatistic.CI_Mean_DF(
                dfLogI.iloc[:,colD], self.rDO['Alpha'], fullCI=False, # type: ignore
            ).to_numpy()
        #endregion ------------------------------------------------> FC CI

        #region -----------------------------------------------------------> P
        if self.rDO['RawI']:
            if self.rDO['IndS']:
                self.dfR.loc[:,(cN,tN,'P')] = mStatistic.Test_t_IS_DF(
                    dfLogI, colC, colD, alpha=self.rDO['Alpha']
                )['P'].to_numpy()
            else:
                self.dfR.loc[:,(cN,tN,'P')] = mStatistic.Test_t_PS_DF(
                    dfLogI, colC, colD, alpha=self.rDO['Alpha']
                )['P'].to_numpy()
        else:
            #------------------------------> Dummy 0 columns
            dfLogI['TEMP_Col_Full_00'] = 0
            dfLogI['TEMP_Col_Full_01'] = 0
            colCF = []
            colCF.append(dfLogI.columns.get_loc('TEMP_Col_Full_00'))
            colCF.append(dfLogI.columns.get_loc('TEMP_Col_Full_01'))
            #------------------------------> 
            self.dfR.loc[:,(cN,tN,'P')] = mStatistic.Test_t_IS_DF(
                dfLogI, colCF, colD, f=True,
            )['P'].to_numpy()
        #endregion --------------------------------------------------------> P

        #region ----------------------------------------------------------> Pc
        if self.rDO['CorrectP'] != 'None':
            self.dfR.loc[:,(cN,tN,'Pc')] = multipletests(
                self.dfR.loc[:,(cN,tN,'P')],
                self.rDO['Alpha'], 
                mConfig.oCorrectP[self.rDO['CorrectP']]
            )[1]
        else:
            pass
        #endregion -------------------------------------------------------> Pc

        #region ------------------------------------------------> Round to .XX
        self.dfR.loc[:,(cN,tN,self.cLDFThirdLevel)] = (
            self.dfR.loc[:,(cN,tN,self.cLDFThirdLevel)].round(2)
        )
        #endregion ---------------------------------------------> Round to .XX

        return True
    #---
    #endregion ----------------------------------------------> Class Methods

    #region -----------------------------------------------------> Run Methods
    def CheckInput(self) -> bool:
        """Check user input

            Returns
            -------
            bool
        """
        #region -------------------------------------------------------> Super
        if super().CheckInput():
            pass
        else:
            return False
        #endregion ----------------------------------------------------> Super

        #region ------------------------------------------------> Mixed Fields
        #region ---------------------------------------------> # of Replicates
        msgStep = self.cLPdCheck + 'Number of Replicates'
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        #------------------------------> 
        a = self.wSample.wCb.GetValue() == 'Paired Samples'
        b = self.rLbDict['Control'] == mConfig.oControlTypeProtProf['Ratio']
        if a and not b:
            if self.CheckNumberReplicates():
                pass
            else:
                return False
        else:
            pass
        #endregion ------------------------------------------> # of Replicates
        #endregion ---------------------------------------------> Mixed Fields

        return True
    #---

    def PrepareRun(self) -> bool:
        """Set variables and prepare data for analysis.

            Returns
            -------
            bool
        """
        #region -------------------------------------------------------> Input
        msgStep = self.cLPdPrepare + 'User input, reading'
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        #------------------------------> As given
        self.rDI = {
            self.EqualLenLabel(self.cLiFile) : (
                self.wIFile.wTc.GetValue()),
            self.EqualLenLabel(self.cLId) : (
                self.wId.wTc.GetValue()),
            self.EqualLenLabel(self.cLCeroTreatD) : (
                self.wCeroB.wCb.GetValue()),
            self.EqualLenLabel(self.cLTransMethod) : (
                self.wTransMethod.wCb.GetValue()),
            self.EqualLenLabel(self.cLNormMethod) : (
                self.wNormMethod.wCb.GetValue()),
            self.EqualLenLabel(self.cLImputation) : (
                self.wImputationMethod.wCb.GetValue()),
            self.EqualLenLabel(self.cLShift) : (
                self.wShift.wTc.GetValue()),
            self.EqualLenLabel(self.cLWidth) : (
                self.wWidth.wTc.GetValue()),
            self.EqualLenLabel(self.cLScoreVal) : (
                self.wScoreVal.wTc.GetValue()),
            self.EqualLenLabel(self.cLSample) : (
                self.wSample.wCb.GetValue()),
            self.EqualLenLabel(self.cLAlpha) : (
                self.wAlpha.wTc.GetValue()),
            self.EqualLenLabel(self.cLCorrectP) : (
                self.wCorrectP.wCb.GetValue()),
            self.EqualLenLabel(self.cLDetectedProt) : (
                self.wDetectedProt.wTc.GetValue()),
            self.EqualLenLabel(self.cLGene) : (
                self.wGeneName.wTc.GetValue()),
            self.EqualLenLabel(self.cLScoreCol) : (
                self.wScore.wTc.GetValue()),
            self.EqualLenLabel(self.cLExcludeProt) : (
                self.wExcludeProt.wTc.GetValue()),
            self.EqualLenLabel(self.cLCond) : (
                self.rLbDict[0]),
            self.EqualLenLabel(self.cLRP) : (
                self.rLbDict[1]),
            self.EqualLenLabel(f"Control {self.cLCtrlType}") : (
                self.rLbDict['ControlType']),
            self.EqualLenLabel(f"Control {self.cLCtrlName}") : (
                self.rLbDict['Control']),
            self.EqualLenLabel(mConfig.lStResultCtrlS): (
                self.wTcResults.GetValue()),
        }
        #------------------------------> Dict with all values
        #--------------> 
        msgStep = self.cLPdPrepare + 'User input, processing'
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        #--------------> 
        detectedProt = int(self.wDetectedProt.wTc.GetValue())
        geneName     = int(self.wGeneName.wTc.GetValue())
        scoreCol     = int(self.wScore.wTc.GetValue())
        excludeProt  = mMethod.Str2ListNumber(
            self.wExcludeProt.wTc.GetValue(), sep=' ')
        resCtrl       = mMethod.ResControl2ListNumber(self.wTcResults.GetValue())
        resCtrlFlat   = mMethod.ResControl2Flat(resCtrl)
        resCtrlDF     = mMethod.ResControl2DF(resCtrl, 2+len(excludeProt)+1)
        resCtrlDFFlat = mMethod.ResControl2Flat(resCtrlDF)
        #--------------> 
        self.rDO  = {
            'iFile'      : Path(self.wIFile.wTc.GetValue()),
            'uFile'      : Path(self.wUFile.wTc.GetValue()),
            'ID'         : self.wId.wTc.GetValue(),
            'ScoreVal'   : float(self.wScoreVal.wTc.GetValue()),
            'RawI'       : False if self.rLbDict['ControlType'] == mConfig.oControlTypeProtProf['Ratio'] else True,
            'IndS'       : True if self.wSample.wCb.GetValue() == 'Independent Samples' else False,
            'Cero'       : mConfig.oYesNo[self.wCeroB.wCb.GetValue()],
            'NormMethod' : self.wNormMethod.wCb.GetValue(),
            'TransMethod': self.wTransMethod.wCb.GetValue(),
            'ImpMethod'  : self.wImputationMethod.wCb.GetValue(),
            'Shift'      : float(self.wShift.wTc.GetValue()),
            'Width'      : float(self.wWidth.wTc.GetValue()),
            'Alpha'      : float(self.wAlpha.wTc.GetValue()),
            'CorrectP'   : self.wCorrectP.wCb.GetValue(),
            'Cond'       : self.rLbDict[0],
            'RP'         : self.rLbDict[1],
            'ControlT'   : self.rLbDict['ControlType'],
            'ControlL'   : self.rLbDict['Control'],
            'oc'         : {
                'DetectedP' : detectedProt,
                'GeneName'  : geneName,
                'ScoreCol'  : scoreCol,
                'ExcludeP'  : excludeProt,
                'ResCtrl'   : resCtrl,
                'ColumnF'   : [scoreCol] + resCtrlFlat,
                'Column'    : (
                    [geneName, detectedProt, scoreCol]+excludeProt+resCtrlFlat),# type: ignore
            },
            'df' : {
                'DetectedP'  : 0,
                'GeneName'   : 1,
                'ScoreCol'   : 2,
                'ExcludeP'   : [2+x for x in range(1, len(excludeProt)+1)],
                'ResCtrl'    : resCtrlDF,
                'ResCtrlFlat': resCtrlDFFlat,
                'ColumnR'    : resCtrlDFFlat,
                'ColumnF'    : [2] + resCtrlDFFlat,
            },
        }
        #endregion ----------------------------------------------------> Input

        #region ---------------------------------------------------> Super
        if super().PrepareRun():
            pass
        else:
            self.rMsgError = 'Something went wrong when preparing the analysis.'
            return False
        #endregion ------------------------------------------------> Super

        return True
    #---

    def RunAnalysis(self) -> bool:
        """Calculate proteome profiling data.

            Returns
            -------
            bool
        """
        #region -------------------------------------------------------> Print
        if mConfig.development:
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
        else:
            pass
        #endregion ----------------------------------------------------> Print

        #region --------------------------------------------> Data Preparation
        if self.DataPreparation():
            pass
        else:
            return False
        #endregion -----------------------------------------> Data Preparation

        #region --------------------------------------------------------> Sort
        self.dfS.sort_values(
            by=list(self.dfS.columns[0:2]), inplace=True, ignore_index=True,
        )
        #endregion -----------------------------------------------------> Sort

        #region ----------------------------------------------------> Empty DF
        #------------------------------> Msg
        msgStep = (
            f'{self.cLPdRun}'
            f'Calculating output data - Creating empty dataframe'
        )  
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        #------------------------------> 
        self.dfR = self.EmptyDFR()

        if mConfig.development:
            print('self.dfR.shape: ', self.dfR.shape)
            print(self.dfR.head())
            print('')
        else:
            pass
        #endregion -------------------------------------------------> Empty DF

        #region --------------------------------------------> Calculate values
        #------------------------------> Msg
        msgStep = (
            f'{self.cLPdRun}'
            f'Calculating output data'
        )  
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        #------------------------------> Calculate data
        for c, cN in enumerate(self.rDO['Cond']):
            for t, tN in enumerate(self.rDO['RP']):
                #------------------------------> Message
                msgStep = (
                    f'{self.cLPdRun}'
                    f'Calculating output data for {cN} - {tN}'
                )  
                wx.CallAfter(self.rDlg.UpdateSt, msgStep)
                #------------------------------> Control & Data Column
                colC, colD = self.dColCtrlData[self.rDO['ControlT']](c, t)
                #------------------------------> Calculate data
                try:
                    self.CalcOutData(cN, tN, colC, colD)
                except Exception as e:
                    self.rMsgError = (
                        f'Calculation of the Proteome Profiling data for '
                        f'point {cN} - {tN} failed.'
                    )
                    self.rException = e
                    return False
        #------------------------------>
        if mConfig.development:
            print('self.dfR.shape: ', self.dfR.shape)
            print(self.dfR.head())
            print('')
        else:
            pass
        #endregion -----------------------------------------> Calculate values

        return True
    #---
    #endregion --------------------------------------------------> Run Methods
#---


class PaneLimProt(BaseConfPanelMod2):
    """Configuration Pane for the Limited Proteolysis module.

        Parameters
        ----------
        parent: wx.Widget
            Parent of the pane
        dataI : dict
            Initial data provided by the user in a previous analysis.
            This contains both I and CI dicts e.g. {'I': I, 'CI': CI}.

        Attributes
        ----------
        rDI: dict
            Dictionary with the user input. Keys are labels in the panel plus:
            {
                config.lStLimProtLane           : [list of lanes],
                config.lStLimProtBand           : [list of bands],
                f"Control {config.lStCtrlName}" : "Control Name",
            }
        rDO: dict
            Dictionary with checked user input. Keys are:
            {
                "iFile"      : "Path to input data file",
                "uFile"      : "Path to umsap file.",
                'seqFile'    : "Path to the sequence file",
                'ID'         : "Analysis ID",
                "Cero"       : "Boolean, how to treat cero values",
                "TransMethod": "Transformation method",
                "NormMethod" : "Normalization method",
                "ImpMethod"  : "Imputation method",
                "Shift"      : float,
                "Width"      : float,
                "TargetProt" : "Target Protein",
                "ScoreVal"   : "Score value threshold",
                'Sample'     : 'Independent or dependent samples',
                "Alpha"      : "Significance level",
                "Beta"       : "Beta level',
                'Gamma'      : "Gamma level",
                'Theta'      : Theta value or None,
                'Theta Max'  : Theta maximum,
                "Lane"       : [List of lanes],
                "Band"       : [List of bands],
                "ControlL"   : "Control label",
                "oc": {
                    "SeqCol"       : Column of Sequences,
                    "TargetProtCol": Column of Proteins,
                    "ScoreCol"     : Score column,
                    "ResCtrl"      : [List of columns containing the control and 
                        experiments column numbers],
                    "ColumnF" : [Flat list of all columns containing floats],
                    "Column": [Flat list of all column numbers with the 
                              following order: SeqCol, TargetProtCol, 
                              ScoreColRes & Control]
                },
                "df": { Column numbers in the pd.df created from the input file.
                    "SeqCol"       : 0,
                    "TargetProtCol": 1,
                    "ScoreCol"     : 2,
                    "ResCtrl"      : [[[]], [[]],...,[[]]],
                    "ResCtrlFlat"  : [ResCtrl as a flat list],
                    "ColumnR"      : [Columns with the results],
                    "ColumnF"      : [Columns that must contain only floats],
                },
                "dfo" : {
                    "NC" : [Columns for the N and C residue numbers in the 
                        output df],
                    "NCF" : [Columns for the nNat and cNat residue numbers in 
                        the output df],
                },
                "ProtLength": "Length of the Recombinant protein",
                "ProtLoc"   : "Location of the Nat Seq in the Rec Seq",
                "ProtDelta" : "To adjust Res Number. Nat = Res + Delta",
            },    
        rLbDict: dict
            Contains information about the Res - Ctrl e.g.
            {
                0        : ['L1', 'L2'],
                1        : ['B1', 'B2'],
                'Control': ['TheControl'],
            }
        See Parent classes for more attributes.

        Notes
        -----
        Running the analysis results in the creation of:
        
        - Parent Folder/
            - Input_Data_Files/
            - Steps_Data_Files/20220104-214055_Limited Proteolysis/
            - output-file.umsap
        
        The Input_Data_Files folder contains the original data files. These are 
        needed for data visualization, running analysis again with different 
        parameters, etc.
        The Steps_Data_Files/Date-Section folder contains regular csv files with 
        the step by step data.
    
        The Limited Proteolysis section in output-file.umsap contains the 
        information about the calculations, e.g

        {
            'Limited Proteolysis : {
                '20210324-165609': {
                    'V' : config.dictVersion,
                    'I' : self.d,
                    'CI': self.do,
                    'DP': {
                        'dfS' : pd.DataFrame with initial data as float and
                                after discarding values by score.
                        'dfT' : pd.DataFrame with transformed data.
                        'dfN' : pd.DataFrame with normalized data.
                        'dfIm': pd.DataFrame with imputed data.
                    }
                    'R' : Path to file with the analysis results.
                }
            }
        }

        The result data frame has the following structure:

        Sequence Score Nterm Cterm NtermF CtermF Delta Band1 ... BandN
        Sequence Score Nterm Cterm NtermF CtermF Delta Lane1 ... LaneN
        Sequence Score Nterm Cterm NtermF CtermF Delta P     ... P
    """
    #region -----------------------------------------------------> Class setup
    cName = mConfig.npLimProt
    #------------------------------> Label
    cLBeta         = "β level"
    cLGamma        = "γ level"
    cLTheta        = "Θ value"
    cLThetaMax     = "Θmax value"
    cLSample       = 'Samples'
    cLLane         = mConfig.lStLimProtLane
    cLBand         = mConfig.lStLimProtBand
    cLCtrlName     = mConfig.lStCtrlName
    cLDFFirstThree = mConfig.dfcolLimProtFirstPart
    cLDFThirdLevel = mConfig.dfcolLimProtCLevel
    #------------------------------> Choices
    cOSample = mConfig.oSamples
    #------------------------------> Hints
    cHBeta = 'e.g. 0.05'
    cHGamma = 'e.g. 0.8'
    cHTheta = 'e.g. 4.5'
    cHThetaMax = 'e.g. 8'
    #------------------------------> Tooltips
    cTTSample = mConfig.ttStSample
    cTTBeta = ('Beta level for the analysis.\ne.g. 0.05')
    cTTGamma = ('Confidence limit level for estimating the measuring '
                'precision.\ne.g. 0.80')
    cTTTheta = ('Confidence interval used in the analysis. The value depends '
        'on the Data Preparation selected. An empty values means that the '
        'confidence interval will be calculated for each peptide.\ne.g. 3')
    cTTThetaMax = (f'Maximum value for the calculated Confidence interval. It '
        f'is only used if {cLTheta} is left empty.\ne.g. 8')
    #------------------------------> Needed by BaseConfPanel
    cURL         = f"{mConfig.urlTutorial}/limited-proteolysis"
    cSection     = mConfig.nmLimProt
    cTitlePD     = f"Running {mConfig.nmLimProt} Analysis"
    cGaugePD     = 44
    rMainData    = '{}_{}-LimitedProteolysis-Data.txt'
    #------------------------------> Optional configuration
    cTTHelp = mConfig.ttBtnHelp.format(cURL)
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent, dataI: dict={}) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(parent)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        #------------------------------> Values
        self.wBeta = mWidget.StaticTextCtrl(
            self.wSbValue,
            stLabel   = self.cLBeta,
            stTooltip = self.cTTBeta,
            tcSize    = self.cSTc,
            tcHint    = self.cHBeta,
            validator = mValidator.NumberList(
                numType='float', nN=1, vMin=0, vMax=1),
        )
        self.wGamma = mWidget.StaticTextCtrl(
            self.wSbValue,
            stLabel   = self.cLGamma,
            stTooltip = self.cTTGamma,
            tcSize    = self.cSTc,
            tcHint    = self.cHGamma,
            validator = mValidator.NumberList(
                numType='float', nN=1, vMin=0, vMax=1),
        )
        self.wTheta = mWidget.StaticTextCtrl(
            self.wSbValue,
            stLabel   = self.cLTheta,
            stTooltip = self.cTTTheta,
            tcSize    = self.cSTc,
            tcHint    = self.cHTheta,
            validator = mValidator.NumberList(
                numType='float', nN=1, vMin=0.01, opt=True),
        )
        self.wThetaMax = mWidget.StaticTextCtrl(
            self.wSbValue,
            stLabel   = self.cLThetaMax,
            stTooltip = self.cTTThetaMax,
            tcSize    = self.cSTc,
            tcHint    = self.cHThetaMax,
            validator = mValidator.NumberList(
                numType='float', nN=1, vMin=0.01),
        )
        self.wSample = mWidget.StaticTextComboBox(
            self.wSbValue,
            label     = self.cLSample,
            choices   = list(self.cOSample.keys()),
            tooltip   = self.cTTSample,
            validator = mValidator.IsNotEmpty(),
        )
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        #------------------------------> Sizer Values
        self.sSbValueWid.Add(
            1, 1,
            pos    = (0,0),
            flag   = wx.EXPAND|wx.ALL,
            border = 5,
            span   = (2, 0),
        )
        self.sSbValueWid.Add(
            self.wTargetProt.wSt,
            pos    = (0,1),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sSbValueWid.Add(
            self.wTargetProt.wTc,
            pos    = (0,2),
            flag   = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sSbValueWid.Add(
            self.wScoreVal.wSt,
            pos    = (1,1),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sSbValueWid.Add(
            self.wScoreVal.wTc,
            pos    = (1,2),
            flag   = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sSbValueWid.Add(
            self.wSample.wSt,
            pos    = (2,1),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sSbValueWid.Add(
            self.wSample.wCb,
            pos    = (2,2),
            flag   = wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sSbValueWid.Add(
            self.wAlpha.wSt,
            pos    = (3,1),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sSbValueWid.Add(
            self.wAlpha.wTc,
            pos    = (3,2),
            flag   = wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sSbValueWid.Add(
            self.wBeta.wSt,
            pos    = (0,3),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sSbValueWid.Add(
            self.wBeta.wTc,
            pos    = (0,4),
            flag   = wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sSbValueWid.Add(
            self.wGamma.wSt,
            pos    = (1,3),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sSbValueWid.Add(
            self.wGamma.wTc,
            pos    = (1,4),
            flag   = wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sSbValueWid.Add(
            self.wTheta.wSt,
            pos    = (2,3),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sSbValueWid.Add(
            self.wTheta.wTc,
            pos    = (2,4),
            flag   = wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sSbValueWid.Add(
            self.wThetaMax.wSt,
            pos    = (3,3),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sSbValueWid.Add(
            self.wThetaMax.wTc,
            pos    = (3,4),
            flag   = wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sSbValueWid.Add(
            1, 1,
            pos    = (0,5),
            flag   = wx.EXPAND|wx.ALL,
            border = 5,
            span   = (2, 0),
        )
        self.sSbValueWid.AddGrowableCol(0, 1)
        self.sSbValueWid.AddGrowableCol(2, 1)
        self.sSbValueWid.AddGrowableCol(4, 1)
        self.sSbValueWid.AddGrowableCol(5, 1)
        #------------------------------> Main Sizer
        self.SetSizer(self.sSizer)
        self.sSizer.Fit(self)
        self.SetupScrolling()
        #endregion ---------------------------------------------------> Sizers
        
        #region ----------------------------------------------> checkUserInput
        rCheckUserInput = {
            self.cLSample:[self.wSample.wCb, mConfig.mOptionBad     , False],
            self.cLAlpha :[self.wAlpha.wTc,  mConfig.mOne01Num      , False],
            self.cLBeta  :[self.wBeta.wTc,   mConfig.mOne01Num      , False],
            self.cLGamma :[self.wGamma.wTc,  mConfig.mOne01Num      , False],
            self.cLTheta :[self.wTheta.wTc,  mConfig.mOneZPlusNumCol, False],
            f'{self.cLSeqCol} column' :[self.wSeqCol.wTc,   mConfig.mOneZPlusNumCol, True ],
            self.cLDetectedProt:[self.wDetectedProt.wTc,    mConfig.mOneZPlusNumCol, True ],
            self.cLScoreCol    :[self.wScore.wTc,           mConfig.mOneZPlusNumCol, True ],
            self.cLResControl  :[self.wTcResults,           mConfig.mResCtrl       , False]
        }
        self.rCheckUserInput = self.rCheckUserInput | rCheckUserInput
        #endregion -------------------------------------------> checkUserInput

        #region -------------------------------------------------------> DataI
        self.SetInitialData(dataI)
        #endregion ----------------------------------------------------> DataI

        #region --------------------------------------------------------> Test
        if mConfig.development:
            import getpass
            user = getpass.getuser()
            if mConfig.os == "Darwin":
                self.wUFile.wTc.SetValue("/Users/" + str(user) + "/TEMP-GUI/BORRAR-UMSAP/umsap-dev.umsap")
                self.wIFile.wTc.SetValue("/Users/" + str(user) + "/Dropbox/SOFTWARE-DEVELOPMENT/APPS/UMSAP/LOCAL/DATA/UMSAP-TEST-DATA/LIMPROT/limprot-data-file.txt")
                self.wSeqFile.wTc.SetValue("/Users/" + str(user) + "/Dropbox/SOFTWARE-DEVELOPMENT/APPS/UMSAP/LOCAL/DATA/UMSAP-TEST-DATA/LIMPROT/limprot-seq-both.txt")
            elif mConfig.os == 'Windows':
                self.wUFile.wTc.SetValue("C:/Users/" + str(user) + "/Desktop/SharedFolders/BORRAR-UMSAP/umsap-dev.umsap")
                self.wIFile.wTc.SetValue("C:/Users/" + str(user) + "/Dropbox/SOFTWARE-DEVELOPMENT/APPS/UMSAP/LOCAL/DATA/UMSAP-TEST-DATA/LIMPROT/limprot-data-file.txt")
                self.wSeqFile.wTc.SetValue("C:/Users/" + str(user) + "/Dropbox/SOFTWARE-DEVELOPMENT/APPS/UMSAP/LOCAL/DATA/UMSAP-TEST-DATA/LIMPROT/limprot-seq-both.txt")
            else:
                pass
            self.wId.wTc.SetValue('Beta Test Dev')
            self.wCeroB.wCb.SetValue('Yes')
            self.wTransMethod.wCb.SetValue('Log2')
            self.wNormMethod.wCb.SetValue('Median')
            self.wImputationMethod.wCb.SetValue('Normal Distribution')
            self.wTargetProt.wTc.SetValue('Mis18alpha')
            self.wScoreVal.wTc.SetValue('10')
            self.wAlpha.wTc.SetValue('0.05')
            self.wBeta.wTc.SetValue('0.05')
            self.wGamma.wTc.SetValue('0.8')
            self.wTheta.wTc.SetValue('')
            self.wThetaMax.wTc.SetValue('8')
            self.wSample.wCb.SetValue('Independent Samples')
            self.wSeqCol.wTc.SetValue('0')
            self.wDetectedProt.wTc.SetValue('34')
            self.wScore.wTc.SetValue('42')
            self.wTcResults.SetValue('69-71; 81-83, 78-80, 75-77, 72-74, ; , , , 66-68, ; 63-65, 105-107, 102-104, 99-101, ; 93-95, 90-92, 87-89, 84-86, 60-62')
            self.rLbDict = {
                0        : ['Lane1', 'Lane2', 'Lane3', 'Lane4', 'Lane5'],
                1        : ['Band1', 'Band2', 'Band3', 'Band4'],
                'Control': ['Ctrl'],
            }
            self.OnImpMethod('fEvent')
            self.wShift.wTc.SetValue('1.8')
            self.wWidth.wTc.SetValue('0.3')
        else:
            pass
        #endregion -----------------------------------------------------> Test
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class Event
    def SetInitialData(self, dataI: dict={}) -> bool:
        """Set initial data.

            Parameters
            ----------
            dataI : dict
                Data to fill all fields and repeat an analysis.

            Returns
            -------
            bool
        """
        #region -------------------------------------------------> Fill Fields
        if dataI:
            #------------------------------> 
            dataInit = dataI['uFile'].parent / mConfig.fnDataInit
            iFile = dataInit / dataI['I'][self.cLiFile]
            seqFile = dataInit / dataI['I'][f'{self.cLSeqFile} File']
            #------------------------------> Files
            self.wUFile.wTc.SetValue(str(dataI['uFile']))
            self.wIFile.wTc.SetValue(str(iFile))
            self.wSeqFile.wTc.SetValue(str(seqFile))
            self.wId.wTc.SetValue(dataI['CI']['ID'])
            #------------------------------> Data Preparation
            self.wCeroB.wCb.SetValue(dataI['I'][self.cLCeroTreatD])
            self.wTransMethod.wCb.SetValue(dataI['I'][self.cLTransMethod])
            self.wNormMethod.wCb.SetValue(dataI['I'][self.cLNormMethod])
            self.wImputationMethod.wCb.SetValue(dataI['I'][self.cLImputation])
            self.wShift.wTc.SetValue(dataI['I'].get(self.cLShift, self.cValShift))
            self.wWidth.wTc.SetValue(dataI['I'].get(self.cLWidth, self.cValWidth))
            #------------------------------> Values
            self.wTargetProt.wTc.SetValue(dataI['I'][self.cLTargetProt])
            self.wScoreVal.wTc.SetValue(dataI['I'][self.cLScoreVal])
            self.wAlpha.wTc.SetValue(dataI['I'][self.cLAlpha])
            self.wSample.wCb.SetValue(dataI['I'][self.cLSample])
            self.wBeta.wTc.SetValue(dataI['I'][self.cLBeta])
            self.wGamma.wTc.SetValue(dataI['I'][self.cLGamma])
            self.wTheta.wTc.SetValue(dataI['I'][self.cLTheta])
            self.wThetaMax.wTc.SetValue(dataI['I'][self.cLThetaMax])
            #------------------------------> Columns
            self.wSeqCol.wTc.SetValue(dataI['I'][f'{self.cLSeqCol} Column'])
            self.wDetectedProt.wTc.SetValue(dataI['I'][self.cLDetectedProt])
            self.wScore.wTc.SetValue(dataI['I'][self.cLScoreCol])
            self.wTcResults.SetValue(dataI['I'][mConfig.lStResultCtrlS])
            self.rLbDict[0] = dataI['I'][self.cLLane]
            self.rLbDict[1] = dataI['I'][self.cLBand]
            self.rLbDict['Control'] = dataI['I'][f"Control {self.cLCtrlName}"]
            #------------------------------> 
            self.OnIFileLoad('fEvent')
            self.OnImpMethod('fEvent')
        else:
            pass
        #endregion ----------------------------------------------> Fill Fields

        return True
    #---

    def EmptyDFR(self) -> 'pd.DataFrame':
        """Creates the empty df for the results.

            Returns
            -------
            pd.DataFrame
        """
        #region -------------------------------------------------------> Index
        #------------------------------> 
        aL = self.cLDFFirstThree
        bL = self.cLDFFirstThree
        cL = self.cLDFFirstThree
        #------------------------------> 
        n = len(self.cLDFThirdLevel)
        #------------------------------> 
        for b in self.rDO['Band']:
            for l in self.rDO['Lane']:
                aL = aL + n*[b]
                bL = bL + n*[l]
                cL = cL + self.cLDFThirdLevel
        #------------------------------> 
        idx = pd.MultiIndex.from_arrays([aL[:], bL[:], cL[:]])
        #endregion ----------------------------------------------------> Index

        #region ----------------------------------------------------> Empty DF
        df = pd.DataFrame(
            np.nan, columns=idx, index=range(self.dfS.shape[0]), # type: ignore
        )
        #endregion -------------------------------------------------> Empty DF

        #region -------------------------------------------------> Seq & Score
        df[(aL[0], bL[0], cL[0])] = self.dfS.iloc[:,0]
        df[(aL[1], bL[1], cL[1])] = self.dfS.iloc[:,2]
        #endregion ----------------------------------------------> Seq & Score

        return df
    #---

    def CalcOutData(
        self, bN: str,  lN: str, colC: list[int], colD: list[int],
        ) -> bool:
        """Performed the tost test
    
            Parameters
            ----------
            bN: str
                Band name
            lN : str
                Lane name
            colC : list int
                Column numbers of the control
            colD : list int
                Column numbers of the gel spot

            Returns
            -------
            bool
        """
        #region ----------------------------------------------> Delta and TOST
        a = mStatistic.Test_tost(
            self.dfS, 
            colC, 
            colD, 
            sample = self.rDO['Sample'],
            delta  = self.dfR[('Delta', 'Delta', 'Delta')],
            alpha  = self.rDO['Alpha'],
        ) 
        self.dfR[(bN, lN, 'Ptost')] = a['P'].to_numpy()
        #endregion -------------------------------------------> Delta and TOST

        return True
    #---
    #endregion ------------------------------------------------> Class Event

    #region ---------------------------------------------------> Run Method
    def CheckInput(self) -> bool:
        """Check user input.

            Returns
            -------
            bool
        """
        #region -------------------------------------------------------> Super
        if super().CheckInput():
            pass
        else:
            return False
        #endregion ----------------------------------------------------> Super

        #region ------------------------------------------------> Mixed Fields
        #region -------------------------------------------------------> Theta
        msgStep = self.cLPdCheck + f'{self.cLThetaMax}'
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        #------------------------------>
        if self.wTheta.wTc.GetValue() == '':
            a, b = self.wThetaMax.wTc.GetValidator().Validate()
            if a:
                pass
            else:
                self.rMsgError = mMethod.StrSetMessage(
                    mConfig.mOneZPlusNum.format(b[1], self.cLThetaMax), b[2])
                return False
        else:
            pass
        #endregion ----------------------------------------------------> Theta

        #region ----------------------------------------------> Paired Samples
        msgStep = self.cLPdCheck + f'{self.cLSample}'
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        #------------------------------>
        if self.wSample.wCb.GetValue() == 'Paired Samples':
            resCtrl = mMethod.ResControl2ListNumber(self.wTcResults.GetValue())
            n = [len(x) for y in resCtrl for x in y if len(x) != 0]
            if len(set(n)) == 1:
                pass
            else:
                self.rMsgError = (f'The Pair Samples analysis requires all gel '
                    f'spots and control to have the same number of replicates.')
                return False
        else:
            pass
        #endregion -------------------------------------------> Paired Samples
        #endregion ---------------------------------------------> Mixed Fields

        return True
    #---

    def PrepareRun(self) -> bool:
        """Set variable and prepare data for analysis.

            Returns
            -------
            bool
        """
        #region -----------------------------------------------------------> d
        msgStep = self.cLPdPrepare + 'User input, reading'
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        #------------------------------> Variables
        impMethod = self.wImputationMethod.wCb.GetValue()
        #------------------------------> As given
        self.rDI = {
            self.EqualLenLabel(self.cLiFile) : (
                self.wIFile.wTc.GetValue()),
            self.EqualLenLabel(f'{self.cLSeqFile} File') : (
                self.wSeqFile.wTc.GetValue()),
            self.EqualLenLabel(self.cLId) : (
                self.wId.wTc.GetValue()),
            self.EqualLenLabel(self.cLCeroTreatD) : (
                self.wCeroB.wCb.GetValue()),
            self.EqualLenLabel(self.cLTransMethod) : (
                self.wTransMethod.wCb.GetValue()),
            self.EqualLenLabel(self.cLNormMethod) : (
                self.wNormMethod.wCb.GetValue()),
            self.EqualLenLabel(self.cLImputation) : (
                impMethod),
            self.EqualLenLabel(self.cLShift) : (
                self.wShift.wTc.GetValue()),
            self.EqualLenLabel(self.cLWidth) : (
                self.wWidth.wTc.GetValue()),
            self.EqualLenLabel(self.cLTargetProt) : (
                self.wTargetProt.wTc.GetValue()),
            self.EqualLenLabel(self.cLScoreVal) : (
                self.wScoreVal.wTc.GetValue()),
            self.EqualLenLabel(self.cLSample) : (
                self.wSample.wCb.GetValue()),
            self.EqualLenLabel(self.cLAlpha) : (
                self.wAlpha.wTc.GetValue()),
            self.EqualLenLabel(self.cLBeta) : (
                self.wBeta.wTc.GetValue()),
            self.EqualLenLabel(self.cLGamma) : (
                self.wGamma.wTc.GetValue()),
            self.EqualLenLabel(self.cLTheta) : (
                self.wTheta.wTc.GetValue()),
            self.EqualLenLabel(self.cLThetaMax) : (
                self.wThetaMax.wTc.GetValue()),
            self.EqualLenLabel(f'{self.cLSeqCol} Column') : (
                self.wSeqCol.wTc.GetValue()),
            self.EqualLenLabel(self.cLDetectedProt) : (
                self.wDetectedProt.wTc.GetValue()),
            self.EqualLenLabel(self.cLScoreCol) : (
                self.wScore.wTc.GetValue()),
            self.EqualLenLabel(mConfig.lStResultCtrlS): (
                self.wTcResults.GetValue()),
            self.EqualLenLabel(self.cLLane) : (
                self.rLbDict[0]),
            self.EqualLenLabel(self.cLBand) : (
                self.rLbDict[1]),
            self.EqualLenLabel(f"Control {self.cLCtrlName}") : (
                self.rLbDict['Control']),
        }
        #endregion --------------------------------------------------------> d
        
        #region ----------------------------------------------------------> do
        #------------------------------> Dict with all values
        #--------------> Step
        msgStep = self.cLPdPrepare + 'User input, processing'
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        #--------------> Theta
        thetaVal = self.wTheta.wTc.GetValue()
        theta = float(thetaVal) if thetaVal != '' else None
        thetaMaxVal = self.wThetaMax.wTc.GetValue()
        thetaMax = float(thetaMaxVal) if thetaMaxVal != '' else None
        #--------------> Columns
        seqCol       = int(self.wSeqCol.wTc.GetValue())
        detectedProt = int(self.wDetectedProt.wTc.GetValue())
        scoreCol     = int(self.wScore.wTc.GetValue())
        resCtrl       = mMethod.ResControl2ListNumber(self.wTcResults.GetValue())
        resCtrlFlat   = mMethod.ResControl2Flat(resCtrl)
        resCtrlDF     = mMethod.ResControl2DF(resCtrl, 3)
        resCtrlDFFlat = mMethod.ResControl2Flat(resCtrlDF)
        #--------------> 
        self.rDO  = {
            'iFile'      : Path(self.wIFile.wTc.GetValue()),
            'uFile'      : Path(self.wUFile.wTc.GetValue()),
            'seqFile'    : Path(self.wSeqFile.wTc.GetValue()),
            'ID'         : self.wId.wTc.GetValue(),
            'Cero'       : mConfig.oYesNo[self.wCeroB.wCb.GetValue()],
            'TransMethod': self.wTransMethod.wCb.GetValue(),
            'NormMethod' : self.wNormMethod.wCb.GetValue(),
            'ImpMethod'  : impMethod,
            'Shift'      : float(self.wShift.wTc.GetValue()),
            'Width'      : float(self.wWidth.wTc.GetValue()),
            'TargetProt' : self.wTargetProt.wTc.GetValue(),
            'ScoreVal'   : float(self.wScoreVal.wTc.GetValue()),
            'Sample'     : self.cOSample[self.wSample.wCb.GetValue()],
            'Alpha'      : float(self.wAlpha.wTc.GetValue()),
            'Beta'       : float(self.wBeta.wTc.GetValue()),
            'Gamma'      : float(self.wGamma.wTc.GetValue()),
            'Theta'      : theta,
            'ThetaMax'   : thetaMax,
            'Lane'       : self.rLbDict[0],
            'Band'       : self.rLbDict[1],
            'ControlL'   : self.rLbDict['Control'],
            'oc'         : { # Column numbers in the initial dataframe
                'SeqCol'       : seqCol,
                'TargetProtCol': detectedProt,
                'ScoreCol'     : scoreCol,
                'ResCtrl'      : resCtrl,
                'ColumnF'      : [scoreCol] + resCtrlFlat,
                'Column'       : (
                    [seqCol, detectedProt, scoreCol] + resCtrlFlat),
            },
            'df' : { # Column numbers in the selected data dataframe
                'SeqCol'       : 0,
                'TargetProtCol': 1,
                'ScoreCol'     : 2,
                'ResCtrl'      : resCtrlDF,
                'ResCtrlFlat'  : resCtrlDFFlat,
                'ColumnR'      : resCtrlDFFlat,
                'ColumnF'      : [2] + resCtrlDFFlat,
            },
            'dfo' : { # Column numbers in the output dataframe
                'NC' : [2,3], # N and C Term Res Numbers in the Rec Seq
                'NCF': [4,5], # N and C Term Res Numbers in the Nat Seq
            }
        }
        #endregion -------------------------------------------------------> do

        #region ---------------------------------------------------> Super
        if super().PrepareRun():
            pass
        else:
            self.rMsgError = 'Something went wrong when preparing the analysis.'
            return False
        #endregion ------------------------------------------------> Super

        return True
    #---

    def RunAnalysis(self) -> bool:
        """Performs the equivalence tests.

            Returns
            -------
            bool
        """
        #region -------------------------------------------------> Print d, do
        if mConfig.development:
            print('')
            print('self.d:')
            for k,v in self.rDI.items():
                print(str(k)+': '+str(v))
            print('')
            print('self.do')
            for k,v in self.rDO.items():
                if k in ['oc', 'df', 'dfo']:
                    print(k)
                    for j,w in v.items():
                        print(f'\t{j}: {w}')
                else:
                    print(str(k)+': '+str(v))
            print('')
        else:
            pass
        #endregion ----------------------------------------------> Print d, do

        #region --------------------------------------------> Data Preparation
        if self.DataPreparation():
            pass
        else:
            return False
        #endregion -----------------------------------------> Data Preparation

        #region ----------------------------------------------------> Empty DF
        #------------------------------> Msg
        msgStep = f'{self.cLPdRun} Creating empty dataframe'
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        #------------------------------> 
        self.dfR = self.EmptyDFR()
        #endregion -------------------------------------------------> Empty DF

        #region ------------------------------------------------> N, C Res Num
        if self.NCResNumbers(seqNat=True):
            pass
        else:
            return False
        #endregion ---------------------------------------------> N, C Res Num

        #region -------------------------------------------------------> Delta
        #------------------------------> Msg
        msgStep = f'{self.cLPdRun} Delta values'
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        #------------------------------> 
        colC = self.rDO['df']['ResCtrl'][0][0]
        #------------------------------> 
        if self.rDO['Theta'] is not None:
            delta = self.rDO['Theta']
        else:
            delta = mStatistic.Test_tost_delta(
                self.dfS.iloc[:,colC], 
                self.rDO['Alpha'],
                self.rDO['Beta'],
                self.rDO['Gamma'], 
                deltaMax=self.rDO['ThetaMax'],
            )
        #------------------------------>
        self.dfR[('Delta', 'Delta', 'Delta')] = delta
        #endregion ----------------------------------------------------> Delta

        #region ---------------------------------------------------> Calculate
        for b, bN in enumerate(self.rDO['Band']):
            for l, lN in enumerate(self.rDO['Lane']):
                #------------------------------> Message
                msgStep = (
                    f'{self.cLPdRun}'
                    f'Gel spot {bN} - {lN}'
                )  
                wx.CallAfter(self.rDlg.UpdateSt, msgStep)
                #------------------------------> Control & Data Column
                colD = self.rDO['df']['ResCtrl'][b+1][l]
                #------------------------------> Calculate data
                if colD:
                    try:
                        self.CalcOutData(bN, lN, colC, colD)
                    except Exception as e:
                        self.rMsgError = (
                            f'Calculation of the Limited Proteolysis data for '
                            f'point {bN} - {lN} failed.'
                        )
                        self.rException = e
                        return False
                else:
                    pass
        #endregion ------------------------------------------------> Calculate

        #region -------------------------------------------------> Check P < a
        idx = pd.IndexSlice
        if (self.dfR.loc[:,idx[:,:,'Ptost']] < self.rDO['Alpha']).any().any():
            pass
        else:
            self.rMsgError = ('There were no peptides detected in the gel '
                'spots with intensity values equivalent to the intensity '
                'values in the control spot. You may run the analysis again '
                'with different values for the configuration options.')
            return False
        #endregion ----------------------------------------------> Check P < a

        #region --------------------------------------------------------> Sort
        self.dfR = self.dfR.sort_values(
            by=[('Nterm', 'Nterm', 'Nterm'),('Cterm', 'Cterm', 'Cterm')] # type: ignore
        )
        self.dfR = self.dfR.reset_index(drop=True)
        #endregion -----------------------------------------------------> Sort

        if mConfig.development:
            print('self.dfR.shape: ', self.dfR.shape)
            print('')
            print(self.dfR)
            print('')

        return True
    #---

    def WriteOutput(self):
        """Write output. Override as needed"""
        #region --------------------------------------------------> Data Steps
        stepDict = self.SetStepDictDP()
        stepDict['Files'] = {
            mConfig.fnInitial.format(self.rDate, '01')   : self.dfI,
            mConfig.fnFloat.format(self.rDate, '02')     : self.dfF,
            mConfig.fnTrans.format(self.rDate, '03')     : self.dfT,
            mConfig.fnNorm.format(self.rDate, '04')      : self.dfN,
            mConfig.fnImp.format(self.rDate, '05')       : self.dfIm,
            mConfig.fnTargetProt.format(self.rDate, '06'): self.dfTP,
            mConfig.fnScore.format(self.rDate, '07')     : self.dfS,
            self.rMainData.format(self.rDate, '08')     : self.dfR,
        }
        stepDict['R'] = self.rMainData.format(self.rDate, '08')
        #endregion -----------------------------------------------> Data Steps

        return self.WriteOutputData(stepDict)
    #---

    def RunEnd(self) -> bool:
        """"""
        #------------------------------> 
        if self.rDFile:
            self.wSeqFile.wTc.SetValue(str(self.rDFile[1]))
        else:
            pass
        #------------------------------>
        return super().RunEnd()
    #---
    #endregion ------------------------------------------------> Run Method
#---


class PaneTarProt(BaseConfPanelMod2):
    """Configuration Pane for the Targeted Proteolysis module.

        Parameters
        ----------
        parent: wx.Widget
            Parent of the pane
        dataI : dict or None
            Initial data provided by the user in a previous analysis.
            This contains both I and CI dicts e.g. {'I': I, 'CI': CI}.

        Attributes
        ----------
        rDI: dict
            Dictionary with the user input. Keys are labels in the panel plus:
            {
                config.lStTarProtExp            : [list of experiments],
                f"Control {config.lStCtrlName}" : "Control Name",
            }
        rDO: dict
            Dictionary with checked user input. Keys are:
            {
                "iFile"      : "Path to input data file",
                "uFile"      : "Path to umsap file.",
                "seqFile"    : "Path to the sequence file",
                "ID"         : "Analysis ID",
                "Cero"       : Boolean, how to treat cero values,
                "TransMethod": "Transformation method",
                "NormMethod" : "Normalization method",
                "ImpMethod"  : "Imputation method",
                "Shift"      : float,
                "Width"      : float,
                "TargetProt" : "Target Protein",
                "ScoreVal"   : "Score value threshold",
                "Alpha"      : "Significance level",
                "SeqLength"  : "Sequence length",
                "AA"         : "Positions to analyze during the AA distribution",
                "Hist"       : "Windows width for the Histograms",
                "Exp"        : "['Exp1', 'Exp2', 'Exp3']",
                "ControlL"   : ['Ctrl']
                "oc" : {
                    "SeqCol"       : Column of Sequences,
                    "TargetProtCol": Column of Proteins,
                    "ScoreCol"     : Score column,
                    "ResCtrl"      : [List of columns containing the control and 
                        experiments column numbers],
                    "ColumnF"      : [Flat list with float columns],
                    "Column"       : [Flat list of all column numbers with the 
                              following order: SeqCol, TargetProtCol, 
                              ScoreColRes & Control]
                },
                "df" : { Colum numbers if the pd.df created from the input file
                    "SeqCol"       : 0,
                    "TargetProtCol": 1,
                    "ScoreCol"     : 2,
                    "ResCtrl"      : [[[]], [[]],...,[[]]],
                    "ResCtrlFlat"  : Flat ResCtrl,
                    "ColumnR"      : [Columns with the results],
                    "ColumnF"      : [Columns that must contain only floats],
                },
                "dfo" : {
                    "NC" : [Columns for the N and C residue numbers in the 
                        output df],
                    "NCF" : [Columns for the nNat and cNat residue numbers in 
                        the output df],   
                },
                "ProtLength": "Length of the Recombinant protein",
                "ProtLoc"   : "Location of the Nat Seq in the Rec Seq",
                "ProtDelta" : "To adjust Res Number. Nat = Res + Delta",
            }
        rLbDict: dict
            Contains information about the Res - Ctrl e.g.
            {
                0        : ['Exp1', 'Exp1'],
                'Control': ['TheControl'],
            }
        See Parent classes for more attributes.

        Notes
        -----
        Running the analysis results in the creation of:
        
        - Parent Folder/
            - Input_Data_Files/
            - Steps_Data_Files/20220104-214055_Targeted Proteolysis/
            - output-file.umsap

        The Input_Data_Files folder contains the original data files. These are 
        needed for data visualization, running analysis again with different 
        parameters, etc.
        The Steps_Data_Files/Date-Section folder contains regular csv files with 
        the step by step data.

        The Targeted Proteolysis section in output-file.umsap contains the 
        information about the calculations, e.g

        {
            'Targeted Proteolysis : {
                '20210324-165609': {
                    'V' : config.dictVersion,
                    'I' : self.d,
                    'CI': self.do,
                    'DP': {
                        'dfS' : pd.DataFrame with initial data as float and
                                after discarding values by score.
                        'dfT' : pd.DataFrame with transformed data.
                        'dfN' : pd.DataFrame with normalized data.
                        'dfIm': pd.DataFrame with imputed data.
                    }
                    'R' : pd.DataFrame (dict) with the calculation results.
                }
            }
        }

        The result data frame has the following structure:

        Sequence Score Nterm Cterm NtermF CtermF Exp1, Exp1,..., ExpN, ExpN
        Sequence Score Nterm Cterm NtermF CtermF IntL,    P,..., IntL, P
    """
    #region -----------------------------------------------------> Class setup
    cName = mConfig.npTarProt
    #------------------------------> Label
    cLAAPos    = 'AA Positions'
    cLHist     = 'Histogram Windows'
    cLExp      = mConfig.lStTarProtExp
    cLCtrlName = mConfig.lStCtrlName
    cLDFFirst  = mConfig.dfcolTarProtFirstPart
    cLDFSecond = mConfig.dfcolTarProtBLevel
    #------------------------------> Hint
    cHAAPos = 'e.g. 5'
    cHHist  = 'e.g. 50 or 50 100 200'
    #------------------------------> Tooltip
    cTTAAPos = (f'Number of positions around the cleavage sites to consider '
        f'for the AA distribution analysis.\ne.g. 5{mConfig.mOptField}')
    cTTHist = (f'Size of the histogram windows. One number will result in '
        f'equally spaced windows. Multiple numbers allow defining custom sized '
        f'windows.\ne.g. 50 or 0 50 100 150 500{mConfig.mOptField}')
    #------------------------------> Needed by BaseConfPanel
    cURL         = f"{mConfig.urlTutorial}/targeted-proteolysis"
    cSection     = mConfig.nmTarProt
    cTitlePD     = f"Running {mConfig.nmTarProt} Analysis"
    cGaugePD     = 60
    rMainData    = '{}_{}-TargetedProteolysis-Data.txt'
    #------------------------------> Optional configuration
    cTTHelp = mConfig.ttBtnHelp.format(cURL)
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent, dataI: dict={}) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(parent)
        #------------------------------>
        self.dfAA    = pd.DataFrame()
        self.dfHist  = pd.DataFrame()
        self.dfCpR   = pd.DataFrame()
        self.dfCEvol = pd.DataFrame()
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        #------------------------------> Values
        self.wAAPos = mWidget.StaticTextCtrl(
            self.wSbValue,
            stLabel   = self.cLAAPos,
            stTooltip = self.cTTAAPos,
            tcSize    = self.cSTc,
            tcHint    = self.cHAAPos,
            validator = mValidator.NumberList(
                numType='int', nN=1, vMin=0, opt=True)
        )
        self.wHist = mWidget.StaticTextCtrl(
            self.wSbValue,
            stLabel   = self.cLHist,
            stTooltip = self.cTTHist,
            tcSize    = self.cSTc,
            tcHint    = self.cHHist,
            validator = mValidator.NumberList(
                numType='int', vMin=0, sep=' ', opt=True),
        )
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        #------------------------------> Values
        self.sSbValueWid.Add(
            1, 1,
            pos    = (0,0),
            flag   = wx.EXPAND|wx.ALL,
            border = 5,
            span   = (2, 0),
        )
        self.sSbValueWid.Add(
            self.wTargetProt.wSt,
            pos    = (0,1),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sSbValueWid.Add(
            self.wTargetProt.wTc,
            pos    = (0,2),
            flag   = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sSbValueWid.Add(
            self.wScoreVal.wSt,
            pos    = (1,1),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sSbValueWid.Add(
            self.wScoreVal.wTc,
            pos    = (1,2),
            flag   = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sSbValueWid.Add(
            self.wAlpha.wSt,
            pos    = (2,1),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sSbValueWid.Add(
            self.wAlpha.wTc,
            pos    = (2,2),
            flag   = wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sSbValueWid.Add(
            self.wAAPos.wSt,
            pos    = (0,3),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sSbValueWid.Add(
            self.wAAPos.wTc,
            pos    = (0,4),
            flag   = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sSbValueWid.Add(
            self.wHist.wSt,
            pos    = (1,3),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sSbValueWid.Add(
            self.wHist.wTc,
            pos    = (1,4),
            flag   = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sSbValueWid.Add(
            1, 1,
            pos    = (0,5),
            flag   = wx.EXPAND|wx.ALL,
            border = 5,
            span   = (2, 0),
        )

        self.sSbValueWid.AddGrowableCol(0, 1)
        self.sSbValueWid.AddGrowableCol(2, 1)
        self.sSbValueWid.AddGrowableCol(4, 1)
        self.sSbValueWid.AddGrowableCol(5, 1)
        #------------------------------> Main Sizer
        self.SetSizer(self.sSizer)
        self.sSizer.Fit(self)
        self.SetupScrolling()
        #endregion ---------------------------------------------------> Sizers

        #region ----------------------------------------------> checkUserInput
        rCheckUserInput = {
            self.cLAlpha       :[self.wAlpha.wTc,           mConfig.mOne01Num      , False],
            self.cLAAPos       :[self.wAAPos.wTc,           mConfig.mOneZPlusNum   , False],
            self.cLHist        :[self.wHist.wTc,            mConfig.mValueBad      , False],
            f'{self.cLSeqCol} column' :[self.wSeqCol.wTc,   mConfig.mOneZPlusNumCol, True ],
            self.cLDetectedProt:[self.wDetectedProt.wTc,    mConfig.mOneZPlusNumCol, True ],
            self.cLScoreCol    :[self.wScore.wTc,           mConfig.mOneZPlusNumCol, True ],
            self.cLResControl  :[self.wTcResults,          mConfig.mResCtrl       , False]
        }
        self.rCheckUserInput = self.rCheckUserInput | rCheckUserInput
        #endregion -------------------------------------------> checkUserInput

        #region -------------------------------------------------------> DataI
        self.SetInitialData(dataI)
        #endregion ----------------------------------------------------> DataI

        #region --------------------------------------------------------> Test
        if mConfig.development:
            import getpass
            user = getpass.getuser()
            if mConfig.os == "Darwin":
                self.wUFile.wTc.SetValue("/Users/" + str(user) + "/TEMP-GUI/BORRAR-UMSAP/umsap-dev.umsap")
                self.wIFile.wTc.SetValue("/Users/" + str(user) + "/Dropbox/SOFTWARE-DEVELOPMENT/APPS/UMSAP/LOCAL/DATA/UMSAP-TEST-DATA/TARPROT/tarprot-data-file.txt")
                self.wSeqFile.wTc.SetValue("/Users/" + str(user) + "/Dropbox/SOFTWARE-DEVELOPMENT/APPS/UMSAP/LOCAL/DATA/UMSAP-TEST-DATA/TARPROT/tarprot-seq-both.txt")
                # self.wSeqFile.tc.SetValue("/Users/" + str(user) + "/Dropbox/SOFTWARE-DEVELOPMENT/APPS/UMSAP/LOCAL/DATA/UMSAP-TEST-DATA/TARPROT/tarprot-seq-rec.txt")
            elif mConfig.os == 'Windows':
                self.wUFile.wTc.SetValue("C:/Users/" + str(user) + "/Desktop/SharedFolders/BORRAR-UMSAP/umsap-dev.umsap")
                self.wIFile.wTc.SetValue("C:/Users/" + str(user) + "/Dropbox/SOFTWARE-DEVELOPMENT/APPS/UMSAP/LOCAL/DATA/UMSAP-TEST-DATA/TARPROT/tarprot-data-file.txt")
                self.wSeqFile.wTc.SetValue("C:/Users/" + str(user) + "/Dropbox/SOFTWARE-DEVELOPMENT/APPS/UMSAP/LOCAL/DATA/UMSAP-TEST-DATA/TARPROT/tarprot-seq-both.txt")
            else:
                pass
            self.wId.wTc.SetValue('Beta Test Dev')
            self.wCeroB.wCb.SetValue('Yes')
            self.wTransMethod.wCb.SetValue('Log2')
            self.wNormMethod.wCb.SetValue('Median')
            self.wImputationMethod.wCb.SetValue('Normal Distribution')
            self.wTargetProt.wTc.SetValue('efeB')
            self.wScoreVal.wTc.SetValue('200')
            self.wAAPos.wTc.SetValue('5')
            self.wHist.wTc.SetValue('25')
            self.wAlpha.wTc.SetValue('0.05')
            self.wSeqCol.wTc.SetValue('0')
            self.wDetectedProt.wTc.SetValue('38')
            self.wScore.wTc.SetValue('44')
            self.wTcResults.SetValue('98-105; 109-111; 112 113 114; 115-117 120')
            self.rLbDict = {
                0        : ['Exp1', 'Exp2', 'Exp3'],
                'Control': ['Ctrl'],
            }
            self.OnImpMethod('fEvent')
            self.wShift.wTc.SetValue('1.8')
            self.wWidth.wTc.SetValue('0.3')
        else:
            pass
        #endregion -----------------------------------------------------> Test
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class Event
    def SetInitialData(self, dataI: dict={}) -> bool:
        """Set initial data.

            Parameters
            ----------
            dataI : dict
                Data to fill all fields and repeat an analysis.

            Returns
            -------
            bool
        """
        #region -------------------------------------------------> Fill Fields
        if dataI is not None:
            #------------------------------> 
            dataInit = dataI['uFile'].parent / mConfig.fnDataInit
            iFile    = dataInit / dataI['I'][self.cLiFile]
            seqFile  = dataInit / dataI['I'][f'{self.cLSeqFile} File']
            #------------------------------> Files
            self.wUFile.wTc.SetValue(str(dataI['uFile']))
            self.wIFile.wTc.SetValue(str(iFile))
            self.wSeqFile.wTc.SetValue(str(seqFile))
            self.wId.wTc.SetValue(dataI['CI']['ID'])
            #------------------------------> Data Preparation
            self.wCeroB.wCb.SetValue(dataI['I'][self.cLCeroTreatD])
            self.wTransMethod.wCb.SetValue(dataI['I'][self.cLTransMethod])
            self.wNormMethod.wCb.SetValue(dataI['I'][self.cLNormMethod])
            self.wImputationMethod.wCb.SetValue(dataI['I'][self.cLImputation])
            self.wShift.wTc.SetValue(dataI['I'].get(self.cLShift, self.cValShift))
            self.wWidth.wTc.SetValue(dataI['I'].get(self.cLWidth, self.cValWidth))
            #------------------------------> Values
            self.wTargetProt.wTc.SetValue(dataI['I'][self.cLTargetProt])
            self.wScoreVal.wTc.SetValue(dataI['I'][self.cLScoreVal])
            self.wAlpha.wTc.SetValue(dataI['I'][self.cLAlpha])
            self.wAAPos.wTc.SetValue(dataI['I'][self.cLAAPos])
            self.wHist.wTc.SetValue(dataI['I'][self.cLHist])
            #------------------------------> Columns
            self.wSeqCol.wTc.SetValue(dataI['I'][f'{self.cLSeqCol} Column'])
            self.wDetectedProt.wTc.SetValue(dataI['I'][self.cLDetectedProt])
            self.wScore.wTc.SetValue(dataI['I'][self.cLScoreCol])
            self.wTcResults.SetValue(dataI['I'][mConfig.lStResultCtrlS])
            self.rLbDict[0] = dataI['I'][self.cLExp]
            self.rLbDict['Control'] = dataI['I'][f"Control {self.cLCtrlName}"]
            #------------------------------> 
            self.OnIFileLoad('fEvent')
            self.OnImpMethod('fEvent')
        else:
            pass
        #endregion ----------------------------------------------> Fill Fields

        return True
    #---

    def EmptyDFR(self) -> 'pd.DataFrame':
        """Creates the empty df for the results.

            Returns
            -------
            pd.DataFrame
        """
        #region -------------------------------------------------------> Index
        aL = self.cLDFFirst
        bL = self.cLDFFirst
        n = len(self.cLDFSecond)
        #------------------------------> Ctrl
        aL = aL + n*self.rDO['ControlL']
        bL = bL + self.cLDFSecond
        #------------------------------> Exp
        for exp in self.rDO['Exp']:
            aL = aL + n*[exp]
            bL = bL + self.cLDFSecond
        #------------------------------> 
        idx = pd.MultiIndex.from_arrays([aL[:], bL[:]])
        #endregion ----------------------------------------------------> Index

        #region ----------------------------------------------------> Empty DF
        df = pd.DataFrame(
            np.nan, columns=idx, index=range(self.dfS.shape[0]), # type: ignore
        )
        idx = pd.IndexSlice
        df.loc[:,idx[:,'Int']] = df.loc[:,idx[:,'Int']].astype('object')
        #endregion -------------------------------------------------> Empty DF

        #region -------------------------------------------------> Seq & Score
        df[aL[0]] = self.dfS.iloc[:,0]
        df[aL[1]] = self.dfS.iloc[:,2]
        df[(self.rDO['ControlL'][0], 'P')] = np.nan
        #endregion ----------------------------------------------> Seq & Score

        return df
    #---

    def PrepareAncova(
        self, rowC: int, row: 'namedtuple', rowN: int # type: ignore
        ) -> 'pd.DataFrame':
        """Prepare the dataframe used to perform the ANCOVA test and add the
            intensity to self.dfR.

            Parameters
            ----------
            rowC: int
                Current row index in self.dfR.
            row: namedtuple
                Row from self.dfS.
            rowN: int
                Maximum number of rows in the output pd.df.

            Returns
            -------
            pd.DataFrame
                Dataframe to use in the ANCOVA test
                Xc1, Yc1, Xe1, Ye1,....,XcN, YcN, XeN, YeN
        """
        #region ---------------------------------------------------> Variables
        dfAncova = pd.DataFrame(index=range(0,rowN))
        xC  = []
        xCt = []
        yC  = []
        #endregion ------------------------------------------------> Variables

        #region ---------------------------------------------------> 
        #------------------------------> Control
        #--------------> List
        for r in self.rDO['df']['ResCtrl'][0][0]:
            if np.isfinite(row[r]):
                xC.append(1)
                xCt.append(5)
                yC.append(row[r])
            else:
                pass
        #--------------> Add to self.dfR
        self.dfR.at[rowC,(self.rDO['ControlL'],'Int')] = str(yC)
        #------------------------------> Points
        for k,r in enumerate(self.rDO['df']['ResCtrl'][1:], start=1):
            #------------------------------> 
            xE = []
            yE = []
            #------------------------------> 
            for rE in r[0]:
                if np.isfinite(row[rE]):
                    xE.append(5)
                    yE.append(row[rE])
                else:
                    pass
            #------------------------------> 
            self.dfR.at[rowC,(self.rDO['Exp'][k-1], 'Int')] = str(yE)
            #------------------------------> 
            a = xC + xCt
            b = yC + yC
            c = xC + xE
            d = yC + yE
            #------------------------------> 
            dfAncova.loc[range(0, len(a)),f'Xc{k}'] = a # type: ignore
            dfAncova.loc[range(0, len(b)),f'Yc{k}'] = b # type: ignore
            dfAncova.loc[range(0, len(c)),f'Xe{k}'] = c # type: ignore
            dfAncova.loc[range(0, len(d)),f'Ye{k}'] = d # type: ignore
        #endregion ------------------------------------------------> 
        return dfAncova
    #---
    #endregion ------------------------------------------------> Class Event

    #region ---------------------------------------------------> Run methods
    def PrepareRun(self) -> bool:
        """Set variable and prepare data for analysis.

            Returns
            -------
            bool
        """
        #region -----------------------------------------------------------> d
        msgStep = self.cLPdPrepare + 'User input, reading'
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        #------------------------------> As given
        self.rDI = {
            self.EqualLenLabel(self.cLiFile) : (
                self.wIFile.wTc.GetValue()),
            self.EqualLenLabel(f'{self.cLSeqFile} File') : (
                self.wSeqFile.wTc.GetValue()),
            self.EqualLenLabel(self.cLId) : (
                self.wId.wTc.GetValue()),
            self.EqualLenLabel(self.cLCeroTreatD) : (
                self.wCeroB.wCb.GetValue()),
            self.EqualLenLabel(self.cLTransMethod) : (
                self.wTransMethod.wCb.GetValue()),
            self.EqualLenLabel(self.cLNormMethod) : (
                self.wNormMethod.wCb.GetValue()),
            self.EqualLenLabel(self.cLImputation) : (
                self.wImputationMethod.wCb.GetValue()),
            self.EqualLenLabel(self.cLShift) : (
                self.wShift.wTc.GetValue()),
            self.EqualLenLabel(self.cLWidth) : (
                self.wWidth.wTc.GetValue()),
            self.EqualLenLabel(self.cLTargetProt) : (
                self.wTargetProt.wTc.GetValue()),
            self.EqualLenLabel(self.cLScoreVal) : (
                self.wScoreVal.wTc.GetValue()),
            self.EqualLenLabel(self.cLAlpha) : (
                self.wAlpha.wTc.GetValue()),
            self.EqualLenLabel(self.cLAAPos) : (
                self.wAAPos.wTc.GetValue()),
            self.EqualLenLabel(self.cLHist) : (
                self.wHist.wTc.GetValue()),
            self.EqualLenLabel(f'{self.cLSeqCol} Column') : (
                self.wSeqCol.wTc.GetValue()),
            self.EqualLenLabel(self.cLDetectedProt) : (
                self.wDetectedProt.wTc.GetValue()),
            self.EqualLenLabel(self.cLScoreCol) : (
                self.wScore.wTc.GetValue()),
            self.EqualLenLabel(mConfig.lStResultCtrlS): (
                self.wTcResults.GetValue()),
            self.EqualLenLabel(self.cLExp) : (
                self.rLbDict[0]),
            self.EqualLenLabel(f"Control {self.cLCtrlName}") : (
                self.rLbDict['Control']),
        }
        #endregion --------------------------------------------------------> d

        #region ----------------------------------------------------------> do
        #------------------------------> Dict with all values
        #--------------> Step
        msgStep = self.cLPdPrepare + 'User input, processing'
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        #--------------> SeqLength
        aaPosVal     = self.wAAPos.wTc.GetValue()
        aaPos        = int(aaPosVal) if aaPosVal != '' else None
        histVal      = self.wHist.wTc.GetValue()
        hist         = [int(x) for x in histVal.split()] if histVal != '' else None
        #--------------> Columns
        seqCol        = int(self.wSeqCol.wTc.GetValue())
        detectedProt  = int(self.wDetectedProt.wTc.GetValue())
        scoreCol      = int(self.wScore.wTc.GetValue())
        resCtrl       = mMethod.ResControl2ListNumber(self.wTcResults.GetValue())
        resCtrlFlat   = mMethod.ResControl2Flat(resCtrl)
        resCtrlDF     = mMethod.ResControl2DF(resCtrl, 3)
        resCtrlDFFlat = mMethod.ResControl2Flat(resCtrlDF)
        #--------------> 
        self.rDO  = {
            'iFile'      : Path(self.wIFile.wTc.GetValue()),
            'uFile'      : Path(self.wUFile.wTc.GetValue()),
            'seqFile'    : Path(self.wSeqFile.wTc.GetValue()),
            'ID'         : self.wId.wTc.GetValue(),
            'Cero'       : mConfig.oYesNo[self.wCeroB.wCb.GetValue()],
            'TransMethod': self.wTransMethod.wCb.GetValue(),
            'NormMethod' : self.wNormMethod.wCb.GetValue(),
            'ImpMethod'  : self.wImputationMethod.wCb.GetValue(),
            'Shift'      : float(self.wShift.wTc.GetValue()),
            'Width'      : float(self.wWidth.wTc.GetValue()),
            'TargetProt' : self.wTargetProt.wTc.GetValue(),
            'ScoreVal'   : float(self.wScoreVal.wTc.GetValue()),
            'Alpha'      : float(self.wAlpha.wTc.GetValue()),
            'AA'         : aaPos,
            'Hist'       : hist,
            'Exp'        : self.rLbDict[0],
            'ControlL'   : self.rLbDict['Control'],
            'oc'         : { # Column numbers in the initial dataframe
                'SeqCol'       : seqCol,
                'TargetProtCol': detectedProt,
                'ScoreCol'     : scoreCol,
                'ResCtrl'      : resCtrl,
                'ColumnF'      : [scoreCol] + resCtrlFlat,
                'Column'       : (
                    [seqCol, detectedProt, scoreCol] + resCtrlFlat),
            },
            'df' : { # Column numbers in the selected data dataframe
                'SeqCol'       : 0,
                'TargetProtCol': 1,
                'ScoreCol'     : 2,
                'ResCtrl'      : resCtrlDF,
                'ResCtrlFlat'  : resCtrlDFFlat,
                'ColumnR'      : resCtrlDFFlat,
                'ColumnF'      : [2] + resCtrlDFFlat,
            },
            'dfo' : { # Column numbers in the output dataframe
                'NC' : [2,3], # N and C Term Res Numbers in the Rec Seq
                'NCF': [4,5], # N and C Term Res Numbers in the Nat Seq
            }
        }
        #endregion -------------------------------------------------------> do

        #region ---------------------------------------------------> Super
        if super().PrepareRun():
            pass
        else:
            self.rMsgError = 'Something went wrong when preparing the analysis.'
            return False
        #endregion ------------------------------------------------> Super

        return True
    #---

    def RunAnalysis(self) -> bool:
        """Perform the equivalence tests.

            Returns
            -------
            bool
        """
        #region -------------------------------------------------> Print d, do
        if mConfig.development:
            print('')
            print('self.d:')
            for k,v in self.rDI.items():
                print(str(k)+': '+str(v))
            print('')
            print('self.do')
            for k,v in self.rDO.items():
                if k in ['oc', 'df', 'dfo']:
                    print(k)
                    for j,w in v.items():
                        print(f'\t{j}: {w}')
                else:
                    print(str(k)+': '+str(v))
            print('')
        else:
            pass
        #endregion ----------------------------------------------> Print d, do

        #region --------------------------------------------> Data Preparation
        if self.DataPreparation():
            pass
        else:
            return False
        #endregion -----------------------------------------> Data Preparation

        #region ----------------------------------------------------> Empty DF
        #------------------------------> Msg
        msgStep = f'{self.cLPdRun} Creating empty dataframe'
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        #------------------------------> 
        self.dfR = self.EmptyDFR()
        #endregion -------------------------------------------------> Empty DF

        #region ------------------------------------------------> N, C Res Num
        if self.NCResNumbers(seqNat=True):
            pass
        else:
            return False
        #endregion ---------------------------------------------> N, C Res Num

        #region ----------------------------------------------------> P values
        #------------------------------> 
        totalPeptide = len(self.dfS)
        totalRowAncovaDF = 2*max([len(x[0]) for x in self.rDO['df']['ResCtrl']])
        nGroups = [2 for x in self.rDO['df']['ResCtrl']]
        nGroups = nGroups[1:]
        idx = pd.IndexSlice
        idx = idx[self.rDO['Exp'], 'P']
        #------------------------------> 
        k = 0
        for row in self.dfS.itertuples(index=False):
            #------------------------------> Msg
            msgStep = (f'{self.cLPdRun} Calculating P values for peptide '
                f'{k+1} ({totalPeptide})')
            wx.CallAfter(self.rDlg.UpdateStG, msgStep)
            #------------------------------> 
            try:
                #------------------------------> Ancova df & Int
                dfAncova = self.PrepareAncova(k, row, totalRowAncovaDF)
                #------------------------------> P value
                self.dfR.loc[k,idx] = mStatistic.Test_slope( # type: ignore
                    dfAncova, nGroups)
            except Exception as e:
                self.rMsgError = (f'P value calculation failed for peptide '
                    f'{row[0]}.')
                self.rException = e
                return False
            #------------------------------> 
            k = k + 1
        #endregion -------------------------------------------------> P values

        #region -------------------------------------------------> Check P < a
        idx = pd.IndexSlice
        if (self.dfR.loc[:,idx[:,'P']] < self.rDO['Alpha']).any().any():
            pass
        else:
            self.rMsgError = ('There were no peptides detected with intensity '
                'values significantly higher to the intensity values in the '
                'controls. You may run the analysis again with different '
                'values for the configuration options.')
            return False
        #endregion ----------------------------------------------> Check P < a

        #region --------------------------------------------------------> Sort
        self.dfR = self.dfR.sort_values(
            by=[('Nterm', 'Nterm'),('Cterm', 'Cterm')] # type: ignore
        )
        self.dfR = self.dfR.reset_index(drop=True)
        #endregion -----------------------------------------------------> Sort

        # Further Analysis
        #region ----------------------------------------------------> Cleavage
        msgStep = (f'{self.cLPdRun} Cleavage per Residue')
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        #------------------------------> 
        a = self.cLDFFirst[2:]+self.rDO['Exp']
        b = self.cLDFFirst[2:]+['P']
        tIdxH = idx[a,b] # Also used for Hist
        #------------------------------> 
        try:
            self.dfCpR = mMethod.R2CpR(
                self.dfR.loc[:, tIdxH],
                self.rDO['Alpha'],
                self.rDO['ProtLength'],
            )
        except Exception as e:
            self.rMsgError = 'The Cleavage per Residue method failed.'
            self.rException = e
            return False
        #endregion -------------------------------------------------> Cleavage

        #region ---------------------------------------------------> CutEvo
        msgStep = (f'{self.cLPdRun} Cleavage Evolution')
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        #------------------------------> 
        a = self.cLDFFirst[2:]+self.rDO['Exp']
        b = self.cLDFFirst[2:]+['Int', 'P']
        tIdx = idx[a,b]
        #------------------------------> 
        try:
            self.dfCEvol = mMethod.R2CEvol(
                self.dfR.loc[:, tIdx], 
                self.rDO['Alpha'], 
                self.rDO['ProtLength'],
            )
        except Exception as e:
            self.rMsgError = 'The Cleavage Evolution method failed.'
            self.rException = e
            return False
        #endregion ------------------------------------------------> CutEvo

        #region ----------------------------------------------------------> AA
        if self.rDO['AA'] is not None:
            #------------------------------> 
            msgStep = (f'{self.cLPdRun} AA Distribution')
            wx.CallAfter(self.rDlg.UpdateStG, msgStep)
            #------------------------------> 
            tIdx = idx[['Sequence']+self.rDO['Exp'],['Sequence', 'P']]
            try:
                self.dfAA = mMethod.R2AA(
                    self.dfR.loc[:,tIdx], 
                    self.rSeqFileObj.rSeqRec, # type: ignore
                    self.rDO['Alpha'],
                    self.rDO['ProtLength'][0],
                    pos=self.rDO['AA'],
                )
            except Exception as e:
                self.rMsgError = 'Amino acid distribution calculation failed.'
                self.rException = e
                return False
        else:
            pass
        #endregion -------------------------------------------------------> AA

        #region --------------------------------------------------------> Hist
        if self.rDO['Hist'] is not None:
            #------------------------------> 
            msgStep = (f'{self.cLPdRun} Histograms')
            wx.CallAfter(self.rDlg.UpdateStG, msgStep)
            #------------------------------> 
            try:
                self.dfHist = mMethod.R2Hist(
                    self.dfR.loc[:,tIdxH], 
                    self.rDO['Alpha'],
                    self.rDO['Hist'],
                    self.rDO['ProtLength']
                )
            except Exception as e:
                self.rMsgError = 'The Histogram generation method failed.'
                self.rException = e
                return False
        else:
            pass
        #endregion -----------------------------------------------------> Hist

        if mConfig.development:
            print('self.dfR.shape: ', self.dfR.shape)
            print('')
            print(self.dfR)
        else:
            pass

        return True
    #---

    def WriteOutput(self) -> bool:
        """Write output.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------> Data Steps
        stepDict = self.SetStepDictDP()
        stepDict['Files'] = {
            mConfig.fnInitial.format(self.rDate, '01')   : self.dfI,
            mConfig.fnFloat.format(self.rDate, '02')     : self.dfF,
            mConfig.fnTrans.format(self.rDate, '03')     : self.dfT,
            mConfig.fnNorm.format(self.rDate, '04')      : self.dfN,
            mConfig.fnImp.format(self.rDate, '05')       : self.dfIm,
            mConfig.fnTargetProt.format(self.rDate, '06'): self.dfTP,
            mConfig.fnScore.format(self.rDate, '07')     : self.dfS,
            self.rMainData.format(self.rDate, '08')     : self.dfR,
        }
        stepDict['R'] = self.rMainData.format(self.rDate, '08')
        #endregion -----------------------------------------------> Data Steps

        #region --------------------------------------------> Further Analysis
        #------------------------------> 
        stepDict['CpR'] = f'{self.rDate}_CpR.txt'
        stepDict['CEvol'] = f'{self.rDate}_CEvol.txt'
        #------------------------------> 
        stepDict['AA']= {}
        if self.rDO['AA'] is not None:
            stepDict['AA'][f'{self.rDate}_{self.rDO["AA"]}'] = (
                f'{self.rDate}_AA-{self.rDO["AA"]}.txt')
        else:
            pass
        #------------------------------> 
        stepDict['Hist']= {}
        if self.rDO['Hist'] is not None:
            stepDict['Hist'][f'{self.rDate}_{self.rDO["Hist"]}'] = (
                f'{self.rDate}_Hist-{self.rDO["Hist"]}.txt')
        else:
            pass
        #endregion -----------------------------------------> Further Analysis

        return self.WriteOutputData(stepDict)
    #---
    
    def RunEnd(self) -> bool:
        """"""
        #------------------------------>
        if self.rDFile:
            self.wSeqFile.wTc.SetValue(str(self.rDFile[1]))
        else:
            pass
        #------------------------------>
        self.dfAA    = pd.DataFrame()
        self.dfHist  = pd.DataFrame()
        self.dfCpR   = pd.DataFrame()
        self.dfCEvol = pd.DataFrame()
        #------------------------------>
        return super().RunEnd()
    #---
    #endregion ------------------------------------------------> Run methods
#---


class PaneResControlExpConfProtProf(BaseResControlExpConf):
    """Creates the configuration panel for the Results - Control Experiments
        dialog when called from the ProtProf Tab

        Parameters
        ----------
        parent : wx.Widget
            Parent of the panel
        topParent : wx.Widget
            Top parent window
        NColF : int
            Total number of columns present in the Data File

        Attributes
        ----------
        dAddWidgets: dict
            Methods to add the widgets depending on the control type.
    """
    #region -----------------------------------------------------> Class setup
    cName = mConfig.npResControlExpProtProf
    #------------------------------> 
    cCtrlType = mConfig.oControlTypeProtProf
    #------------------------------> Needed by ResControlExpConfBase
    cStLabel = [f"{mConfig.lStProtProfCond}:", f"{mConfig.lStProtProfRP}:"]
    cLabelText = ['C', 'RP']
    #------------------------------>
    cTTTotalField = [
        f'Set the number of {cStLabel[0]}.',
        f'Set the number of {cStLabel[1]}.',
    ]
    #------------------------------> 
    cLCtrlType = mConfig.lStCtrlType
    #------------------------------> Error messages
    # mNoCondRP = (
    #     f'Both {cStLabel[1][:-1]} and {cStLabel[2][:-1]} must be defined.')
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self, parent: wx.Window, topParent: wx.Window, NColF: int
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.dAddWidget = {
            self.cCtrlType['OC']   : self.AddWidget_OC,
            self.cCtrlType['OCC']  : self.AddWidget_OCC,
            self.cCtrlType['OCR']  : self.AddWidget_OCR,
            self.cCtrlType['Ratio']: self.AddWidget_Ratio,
        }
        #--------------> Control type from previous call to Setup Fields
        self.rControlVal = ''
        #------------------------------> Super init
        super().__init__(parent, self.cName, topParent, NColF)
        #------------------------------> Choices
        self.cControlTypeO = [x for x in self.cCtrlType.values()]
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        #------------------------------> wx.StaticText
        self.wStControl = wx.StaticText(
            self.wSwLabel, label='Control Experiment:')
        self.wStControlT = wx.StaticText(
            self.wSwLabel, label=self.cLCtrlType)
        #------------------------------> wx.ComboBox
        self.wCbControl = wx.ComboBox(
            self.wSwLabel, 
            style     = wx.CB_READONLY,
            choices   = self.cControlTypeO,
            validator = mValidator.IsNotEmpty(),
        )
        #endregion --------------------------------------------------> Widgets

        #region -----------------------------------------------------> Tooltip
        self.wStControl.SetToolTip(
            'Set the Type and Name of the control experiment.')
        self.wStControlT.SetToolTip('Set the Type of the control experiment.')
        #endregion --------------------------------------------------> Tooltip
        
        #region ------------------------------------------------------> Sizers
        #------------------------------> 
        self.sSWLabelControl = wx.BoxSizer(wx.HORIZONTAL)
        self.sSWLabelControl.Add(
            self.wStControl, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.sSWLabelControl.Add(
            self.wStControlT, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.sSWLabelControl.Add(self.wCbControl, 0, wx.EXPAND|wx.ALL, 5)
        self.sSWLabelControl.Add(
            self.wControlN.wSt, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.sSWLabelControl.Add(self.wControlN.wTc, 1, wx.EXPAND|wx.ALL, 5)
        #------------------------------> 
        self.sSWLabelMain.Add(
            self.sSWLabelControl, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        #------------------------------> 
        self.sSizer.Fit(self)
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind
        self.wCbControl.Bind(wx.EVT_COMBOBOX, self.OnControl)
        #endregion -----------------------------------------------------> Bind

        #region -----------------------------------------------> Initial State
        self.SetInitialState()
        #endregion --------------------------------------------> Initial State
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Event methods
    def OnControl(self, event: wx.CommandEvent) -> bool:
        """Enable/Disable the Control name when selecting control type.

            Parameters
            ----------
            event:wx.Event
                Information about the event.

            Returns
            -------
            True
        """
        #region ---------------------------------------------------> Get value
        control = self.wCbControl.GetValue()
        #endregion ------------------------------------------------> Get value

        #region ------------------------------------------------------> Action
        if control == self.cCtrlType['Ratio']:
            self.wControlN.wTc.SetValue('None')
            self.wControlN.wTc.SetEditable(False)
        else:
            self.wControlN.wTc.SetEditable(True)
        #endregion ---------------------------------------------------> Action

        return True
    #---

    def OnCreate(self, event: wx.CommandEvent) -> bool:
        """Create the widgets in the white panel.

            Parameters
            ----------
            event:wx.Event
                Information about the event.

            Returns
            -------
            bool
        """
        #region -------------------------------------------------> Check input
        if (n := self.CheckLabel(True)):
            pass
        else:
            return False
        #endregion ----------------------------------------------> Check input

        #region ---------------------------------------------------> Variables
        control = self.wCbControl.GetValue()
        #------------------------------>
        if control == self.cCtrlType['OCR']:
            Nc   = n[0]     # Number of rows of tc needed
            Nr   = n[1] + 1 # Number of tc needed for each row
            NCol = n[1] + 2 # Number of columns in the sizer
            NRow = n[0] + 1 # Number of rows in the sizer
        elif control == self.cCtrlType['Ratio']:
            Nc   = n[0]     
            Nr   = n[1]     
            NCol = n[1] + 1 
            NRow = n[0] + 1 
        else:
            Nc   = n[0] + 1
            Nr   = n[1]
            NCol = n[1] + 1
            NRow = n[0] + 2
        #endregion ------------------------------------------------> Variables

        #region -------------------------------------------> Remove from sizer
        self.sSWMatrix.Clear(delete_windows=False)
        #endregion ----------------------------------------> Remove from sizer

        #region --------------------------------> Create/Destroy wx.StaticText
        #------------------------------> Destroy
        for k, v in self.rFSectStDict.items():
            for j in range(0, len(v)):
                v[-1].Destroy()
                v.pop()
        #------------------------------> Create
        #--------------> Labels
        for k, v in self.rLSectTcDict.items():
            #--------------> New row
            row = []
            #--------------> Fill row
            for j in v:
                row.append(wx.StaticText(self.wSwMatrix, label=j.GetValue()))
            #--------------> Assign
            self.rFSectStDict[k] = row
        #--------------> Control
        self.rFSectStDict['Control'] = [
            wx.StaticText(self.wSwMatrix, label=self.wControlN.wTc.GetValue())]
        if control == self.cCtrlType['Ratio']:
            self.rFSectStDict['Control'][0].Hide()
        else:
            pass
        #endregion -----------------------------> Create/Destroy wx.StaticText

        #region ----------------------------------> Create/Destroy wx.TextCtrl
        #------------------------------> Widgets
        for k in range(0, Nc):
            #------------------------------> Get row
            row = self.rFSectTcDict.get(k, [])
            lRow = len(row)
            #------------------------------> First row is especial
            if k == 0 and control == self.cCtrlType['OC']:
                if control == self.rControlVal:
                    continue
                else:
                    #--------------> Destroy old widgets
                    for j in row:
                        j.Destroy()
                    #--------------> New Row and wx.TextCtrl
                    row = []
                    row.append(
                        wx.TextCtrl(
                            self.wSwMatrix,
                            size      = self.cSLabel,
                            validator = self.cVColNumList,
                        )
                    )
                    #--------------> Assign & Continue to next for step
                    self.rFSectTcDict[k] = row
                    continue
            else:
                pass
            #------------------------------> Create destroy
            if Nr > lRow:
                #-------------->  Create
                for j in range(lRow, Nr):
                    row.append(
                        wx.TextCtrl(
                            self.wSwMatrix,
                            size      = self.cSLabel,
                            validator = self.cVColNumList,
                        )
                    )
                #-------------->  Add to dict
                self.rFSectTcDict[k] = row
            else:
                for j in range(Nr, lRow):
                    #-------------->  Destroy
                    row[-1].Destroy()
                    #--------------> Remove from list
                    row.pop()
        #------------------------------> Drop keys and destroy from dict
        dK = [x for x in self.rFSectTcDict.keys()]
        for k in dK:
            if k+1 > Nc:
                #--------------> Destroy this widget
                for j in self.rFSectTcDict[k]:
                    j.Destroy()
                #--------------> Remove key
                del(self.rFSectTcDict[k])
            else:
                pass
        #------------------------------> Clear value if needed
        if control != self.rControlVal:
            for v in self.rFSectTcDict.values():
                for j in v:
                    j.SetValue('')
        else:
            pass
        #endregion -------------------------------> Create/Destroy wx.TextCtrl

        #region ------------------------------------------------> Setup Sizers
        #------------------------------> Adjust size
        self.sSWMatrix.SetCols(NCol)
        self.sSWMatrix.SetRows(NRow)
        #------------------------------> Add widgets
        self.dAddWidget[control](NCol, NRow)
        #------------------------------> Grow Columns
        for k in range(1, NCol):
            if not self.sSWMatrix.IsColGrowable(k):
                self.sSWMatrix.AddGrowableCol(k, 1)
            else:
                pass
        #------------------------------> Update sizer
        self.sSWMatrix.Layout()
        #endregion ---------------------------------------------> Setup Sizers

        #region --------------------------------------------------> Set scroll
        self.wSwMatrix.SetupScrolling()
        #endregion -----------------------------------------------> Set scroll

        #region -------------------------------------------> Update controlVal
        self.rControlVal = control
        #endregion ----------------------------------------> Update controlVal

        return True
    #---

    def OnOK(self) -> bool:
        """Check wx.Dialog content and send values to topParent.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        ctrlType = self.wCbControl.GetValue()
        ctrl = True
        #endregion ------------------------------------------------> Variables

        #region ---------------------------------------------------> Super
        a, oText = super().OnOK(export=False)
        if a:
            pass
        else:
            return False
        #endregion ------------------------------------------------> Super

        #region --------------------------------------------------> Check Ctrl
        if ctrlType  == self.cCtrlType['OC']:
            if self.rFSectTcDict[0][0].GetValue().strip() == '':
                ctrl = False
            else:
                pass
        elif ctrlType == self.cCtrlType['OCC']:
            for w in self.rFSectTcDict[0]:
                if w.GetValue().strip() == '':
                    ctrl = False
                    break
                else:
                    pass
        else:
            for w in self.rFSectTcDict.values():
                if w[0].GetValue().strip() == '':
                    ctrl = False
                    break
                else:
                    pass
        #------------------------------> 
        if ctrl:
            pass
        else:
            mWindow.DialogNotification(
                'errorF', msg=mConfig.mCtrlEmpty, parent=self)
            return False
        #endregion -----------------------------------------------> Check Ctrl

        #region ---------------------------------------------------> 
        self.Export2TopParent(oText)
        #endregion ------------------------------------------------> 

        return True
    #---
    #endregion ------------------------------------------------> Event Methods

    #region --------------------------------------------------> Class Methods
    def AddWidget_OC(self, NCol: int, NRow: int) -> bool:
        """Add the widget when Control Type is One Control.

            Parameters
            ----------
            NCol : int
                Number of columns in the sizer.
            NRow : int
                Number of rows in the sizer.

            Returns
            -------
            bool
        """
        #region -------------------------------------------------> Control Row
        self.sSWMatrix.Add(
            self.rFSectStDict['Control'][0],
            0,
            wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL,
            5
        )
        self.sSWMatrix.Add(self.rFSectTcDict[0][0], 0, wx.EXPAND|wx.ALL, 5)
        #------------------------------> 
        for k in range(2, NCol):
            self.sSWMatrix.AddSpacer(1)
        #endregion ----------------------------------------------> Control Row

        #region ---------------------------------------------------> RP Labels
        #--------------> Empty space
        self.sSWMatrix.AddSpacer(1)
        #--------------> Labels
        for k in self.rFSectStDict[1]:
            self.sSWMatrix.Add(k, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        #endregion ------------------------------------------------> RP Labels

        #region ------------------------------------------------> Other fields
        K = 1
        for k in self.rFSectStDict[0]:
            #--------------> Add Label
            self.sSWMatrix.Add(
                k,
                0,
                wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL|wx.ALL,
                5
            )
            #--------------> Add tc
            for j in self.rFSectTcDict[K]:
                self.sSWMatrix.Add(j, 0, wx.EXPAND|wx.ALL, 5)
            K += 1
        #endregion ---------------------------------------------> Other fields

        return True
    #---

    def AddWidget_OCC(self, NCol: int, NRow: int) -> bool:
        """Add the widget when Control Type is One Control.

            Parameters
            ----------
            NCol : int
                Number of columns in the sizer.
            NRow : int
                Number of rows in the sizer.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> RP Labels
        self.sSWMatrix.AddSpacer(1)
        #------------------------------>
        for k in self.rFSectStDict[1]:
            self.sSWMatrix.Add(k, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        #endregion ------------------------------------------------> RP Labels

        #region -------------------------------------------------> Control Row
        self.sSWMatrix.Add(
            self.rFSectStDict['Control'][0],
            0,
            wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL|wx.ALL,
            5
        )
        #------------------------------> 
        for k in self.rFSectTcDict[0]:
            self.sSWMatrix.Add(
                k,
                0,
                wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL,
                5
            )    
        #endregion ----------------------------------------------> Control Row

        #region --------------------------------------------------> Other Rows
        for k, v in self.rFSectTcDict.items():
            #------------------------------> Skip control row
            if k == 0:
                continue
            else:
                pass
            #------------------------------> Add Label
            self.sSWMatrix.Add(
                self.rFSectStDict[0][k-1],
                0,
                wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL|wx.ALL,
                5
            )
            #------------------------------> Add wx.TextCtrl
            for j in v:
                self.sSWMatrix.Add(
                    j, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL,5)
        #endregion -----------------------------------------------> Other Rows

        return True
    #---

    def AddWidget_OCR(self, NCol: int, NRow: int) -> bool:
        """Add the widget when Control Type is One Control.

            Parameters
            ----------
            NCol : int
                Number of columns in the sizer.
            NRow : int
                Number of rows in the sizer.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> RP Labels
        self.sSWMatrix.AddSpacer(1)
        #------------------------------>
        self.sSWMatrix.Add(
            self.rFSectStDict['Control'][0], 0, wx.ALIGN_CENTER|wx.ALL, 5)
        #------------------------------>
        for k in self.rFSectStDict[1]:
            self.sSWMatrix.Add(k, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        #endregion ------------------------------------------------> RP Labels

        #region --------------------------------------------------> Other rows
        for k, v in self.rFSectTcDict.items():
            #------------------------------>
            self.sSWMatrix.Add(
                self.rFSectStDict[0][k],
                0,
                wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL|wx.ALL,
                5
            )
            #------------------------------>
            for j in v:
                self.sSWMatrix.Add(j, 0, wx.EXPAND|wx.ALL, 5)
        #endregion -----------------------------------------------> Other rows

        return True
    #---

    def AddWidget_Ratio(self, NCol: int, NRow: int) -> bool:
        """Add the widget when Control Type is Data as Ratios. 

            Parameters
            ----------
            NCol : int
                Number of columns in the sizer.
            NRow : int
                Number of rows in the sizer.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> RP Labels
        self.sSWMatrix.AddSpacer(1)
        #------------------------------>
        for k in self.rFSectStDict[1]:
            self.sSWMatrix.Add(k, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        #endregion ------------------------------------------------> RP Labels

        #region --------------------------------------------------> Other rows
        for k, v in self.rFSectTcDict.items():
            #------------------------------>
            self.sSWMatrix.Add(
                self.rFSectStDict[0][k],
                0,
                wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL|wx.ALL,
                5
            )
            #------------------------------>
            for j in v:
                self.sSWMatrix.Add(j, 0, wx.EXPAND|wx.ALL, 5)
        #endregion -----------------------------------------------> Other rows

        return True
    #---
    #endregion -----------------------------------------------> Class Methods
#---


class PaneResControlExpConfLimProt(BaseResControlExpConf):
    """Creates the configuration panel for the Results - Control Experiments
        dialog when called from the LimProt Tab.

        Parameters
        ----------
        parent : wx.Widget
            Parent of the panel
        topParent : wx.Widget
            Top parent window
        NColF : int
            Total number of columns present in the Data File
    """
    #region -----------------------------------------------------> Class setup
    cName = mConfig.npResControlExpLimProt
    #------------------------------> Needed by ResControlExpConfBase
    cStLabel   = [f"{mConfig.lStLimProtLane}:", f"{mConfig.lStLimProtBand}:"]
    cLabelText = ['L','B']
    #------------------------------> Tooltips
    cTTTotalField = [
        f'Set the number of {cStLabel[0]}.',
        f'Set the number of {cStLabel[1]}.',
    ]  
    #------------------------------> Error messages
    # mNoBL = (f"Both {cStLabel[0]} and {cStLabel[1]} must be defined.")
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent, topParent, NColF):
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(parent, self.cName, topParent, NColF)
        #endregion --------------------------------------------> Initial Setup

        #region ------------------------------------------------------> Sizers
        #------------------------------> 
        self.sSWLabelControl = wx.FlexGridSizer(1,2,5,5)    
        self.sSWLabelControl.Add(
            self.wControlN.wSt, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.sSWLabelControl.Add(
            self.wControlN.wTc, 0, wx.EXPAND|wx.ALL, 5)
        self.sSWLabelControl.AddGrowableCol(1,1)
        #------------------------------> 
        self.sSWLabelMain.Add(
            self.sSWLabelControl, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
        #endregion ---------------------------------------------------> Sizers

        #region -----------------------------------------------> Initial State
        self.SetInitialState()
        #endregion --------------------------------------------> Initial State
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Event Methods
    def OnCreate(self, event: wx.CommandEvent) -> bool:
        """Create the fields in the white panel.

            Parameters
            ----------
            event : wx.Event
                Information about the event.

            Return
            ------
            bool
        """
        #region -------------------------------------------------> Check input
        if (n := self.CheckLabel(False)):
            pass
        else:
            return False
        #endregion ----------------------------------------------> Check input

        #region ---------------------------------------------------> Variables
        Nl = n[0]
        NCol = n[0]+1
        Nb = n[1]
        NRow = n[1]+2
        #endregion ------------------------------------------------> Variables

        #region -------------------------------------------> Remove from sizer
        self.sSWMatrix.Clear(delete_windows=False)
        #endregion ----------------------------------------> Remove from sizer

        #region --------------------------------> Create/Destroy wx.StaticText
        #------------------------------> Destroy
        for k, v in self.rFSectStDict.items():
            for j in range(0, len(v)):
                v[-1].Destroy()
                v.pop()
        #------------------------------> Create
        #--------------> Labels
        for k, v in self.rLSectTcDict.items():
            #--------------> New row
            row = []
            #--------------> Fill row
            for j in v:
                row.append(wx.StaticText(self.wSwMatrix, label=j.GetValue()))
            #--------------> Assign
            self.rFSectStDict[k] = row
        #--------------> Control
        self.rFSectStDict['Control'] = [
            wx.StaticText(self.wSwMatrix, label=self.wControlN.wTc.GetValue())]
        #endregion -----------------------------> Create/Destroy wx.StaticText

        #region ----------------------------------> Create/Destroy wx.TextCtrl
        #------------------------------> Add/Destroy new/old fields
        for k in range(0, Nb+1):
            #------------------------------> 
            row = self.rFSectTcDict.get(k, [])
            lRow = len(row)
            #------------------------------> Control
            if k == 0:
                if lRow:
                    continue
                else:
                    #------------------------------> 
                    row.append(wx.TextCtrl(
                        self.wSwMatrix, 
                        size      = self.cSLabel,
                        validator = self.cVColNumList,
                    ))
                    #------------------------------> 
                    self.rFSectTcDict[k] = row
                    #------------------------------> 
                    continue
            else:
                pass
            #------------------------------> One row for each band
            if Nl >= lRow:
                #------------------------------> Create new fields
                for j in range(lRow, Nl):
                    #------------------------------> 
                    row.append(wx.TextCtrl(
                        self.wSwMatrix, 
                        size      = self.cSLabel,
                        validator = self.cVColNumList,
                    ))
                    #------------------------------> 
                    self.rFSectTcDict[k] = row
            else:
                #------------------------------> Destroy old fields
                for j in range(Nl, lRow):
                    row[-1].Destroy()
                    row.pop()
        #------------------------------> Remove old bands not needed anymore
        # Get keys because you cannot iterate and delete keys
        dK = [x for x in self.rFSectTcDict.keys()]
        #------------------------------> 
        for k in dK:
            if k > Nb:
                #------------------------------> 
                for j in self.rFSectTcDict[k]:
                    j.Destroy()
                #------------------------------> 
                del(self.rFSectTcDict[k])
            else:
                pass
        #endregion -------------------------------> Create/Destroy wx.TextCtrl

        #region ------------------------------------------------> Setup Sizers
        #------------------------------> Adjust size
        self.sSWMatrix.SetCols(NCol)
        self.sSWMatrix.SetRows(NRow)
        #------------------------------> Add widgets
        #--------------> Control row
        self.sSWMatrix.Add(
            self.rFSectStDict['Control'][0],
            0,
            wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL,
            5
        )
        self.sSWMatrix.Add(self.rFSectTcDict[0][0], 0, wx.EXPAND|wx.ALL, 5)
        #------------------------------>
        for k in range(2, NCol):
            self.sSWMatrix.AddSpacer(1)
        #--------------> Lane Labels
        self.sSWMatrix.AddSpacer(1)
        for l in self.rFSectStDict[0]:
            self.sSWMatrix.Add(l, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        #--------------> Bands
        for r, l in enumerate(self.rFSectStDict[1], 1):
            #--------------> 
            self.sSWMatrix.Add(
                l, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            #--------------> 
            for btc in self.rFSectTcDict[r]:
                self.sSWMatrix.Add(btc, 0, wx.EXPAND|wx.ALL, 5)
        #------------------------------> Grow Columns
        for k in range(1, NCol):
            if not self.sSWMatrix.IsColGrowable(k):
                self.sSWMatrix.AddGrowableCol(k, 1)
            else:
                pass
        #------------------------------> Update sizer
        self.sSWMatrix.Layout()
        #endregion ---------------------------------------------> Setup Sizers

        #region --------------------------------------------------> Set scroll
        self.wSwMatrix.SetupScrolling()
        #endregion -----------------------------------------------> Set scroll

        return True
    #---

    def OnOK(self) -> bool:
        """Check wx.Dialog content and send values to topParent.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Super
        if super().OnOK()[0]:
            return True
        else:
            return False
        #endregion ------------------------------------------------> Super
    #---
    #endregion ------------------------------------------------> Event Methods
#---


class PaneResControlExpConfTarProt(BaseResControlExpConf):
    """Creates the configuration panel for the Results - Control Experiments
        dialog when called from the TarProt Tab.

        Parameters
        ----------
        parent : wx.Widget
            Parent of the panel
        topParent : wx.Widget
            Top parent window
        NColF : int
            Total number of columns present in the Data File
    """
    #region -----------------------------------------------------> Class setup
    cName = mConfig.npResControlExpLimProt
    #------------------------------> Needed by ResControlExpConfBase
    cStLabel = [f"{mConfig.lStTarProtExp}:"]
    cLabelText = ['Exp']
    #------------------------------> Tooltips
    cTTTotalField = [f'Set the number of {cStLabel[0]}.']
    #------------------------------> Error messages
    # mNoBL = f'{cStLabel[1][:-1]} must be defined.'
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent, topParent, NColF):
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(parent, self.cName, topParent, NColF)
        #endregion --------------------------------------------> Initial Setup

        #region ------------------------------------------------------> Sizers
        #------------------------------> 
        self.sSWLabelControl = wx.FlexGridSizer(1,2,5,5)
        self.sSWLabelControl.Add(
            self.wControlN.wSt, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5,
        )
        self.sSWLabelControl.Add(self.wControlN.wTc, 0, wx.EXPAND|wx.ALL, 5)
        self.sSWLabelControl.AddGrowableCol(1,1)
        #------------------------------> 
        self.sSWLabelMain.Add(
            self.sSWLabelControl, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
        #endregion ---------------------------------------------------> Sizers

        #region -----------------------------------------------> Initial State
        self.SetInitialState()
        #endregion --------------------------------------------> Initial State
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def OnCreate(self, event: wx.CommandEvent) -> bool:
        """Create the fields in the white panel.

            Parameters
            ----------
            event : wx.Event
                Information about the event.

            Return
            ------
            bool
        """
        #region -------------------------------------------------> Check input
        if (n := self.CheckLabel(False)):
            pass
        else:
            return False
        #endregion ----------------------------------------------> Check input

        #region ---------------------------------------------------> Variables
        NCol = 2
        NRow = n[0]+1
        NExp = n[0]
        #endregion ------------------------------------------------> Variables

        #region -------------------------------------------> Remove from sizer
        self.sSWMatrix.Clear(delete_windows=False)
        #endregion ----------------------------------------> Remove from sizer

        #region --------------------------------> Create/Destroy wx.StaticText
        #------------------------------> Destroy
        for k, v in self.rFSectStDict.items():
            for j in range(0, len(v)):
                v[-1].Destroy()
                v.pop()
        #------------------------------> Create
        #--------------> Labels
        for k, v in self.rLSectTcDict.items():
            #--------------> New row
            row = []
            #--------------> Fill row
            for j in v:
                row.append(wx.StaticText(self.wSwMatrix, label=j.GetValue()))
            #--------------> Assign
            self.rFSectStDict[k] = row
        #--------------> Control
        self.rFSectStDict['Control'] = [
            wx.StaticText(self.wSwMatrix, label=self.wControlN.wTc.GetValue())]
        #endregion -----------------------------> Create/Destroy wx.StaticText

        #region ----------------------------------> Create/Destroy wx.TextCtrl
        #------------------------------> Add new fields
        for k in range(0, NExp+1):
            #------------------------------> 
            row = self.rFSectTcDict.get(k, [])
            lRow = len(row)
            #------------------------------> Control & Exp
            if lRow:
                continue
            else:
                #------------------------------> 
                row.append(wx.TextCtrl(
                    self.wSwMatrix, 
                    size      = self.cSLabel,
                    validator = self.cVColNumList,
                ))
                #------------------------------> 
                self.rFSectTcDict[k] = row
                #------------------------------> 
                continue
        #------------------------------> Destroy not needed old field
        for k in range(NExp+1, len(self.rFSectTcDict.keys())+1):
            row = self.rFSectTcDict.get(k, [])
            if len(row):
                row[0].Destroy()
                row.pop
                self.rFSectTcDict.pop(k)
        #endregion -------------------------------> Create/Destroy wx.TextCtrl

        #region ------------------------------------------------> Setup Sizers
        #------------------------------> Adjust size
        self.sSWMatrix.SetCols(NCol)
        self.sSWMatrix.SetRows(NRow)
        #------------------------------> Add widgets
        #--------------> Control row
        self.sSWMatrix.Add(
            self.rFSectStDict['Control'][0],
            0,
            wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL,
            5
        )
        self.sSWMatrix.Add(self.rFSectTcDict[0][0], 0, wx.EXPAND|wx.ALL, 5)
        #--------------> Experiments
        for r, l in enumerate(self.rFSectStDict[0], 1):
            #--------------> 
            self.sSWMatrix.Add(
                l, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.sSWMatrix.Add(self.rFSectTcDict[r][0], 0, wx.EXPAND|wx.ALL, 5)
        #------------------------------> Grow Columns
        for k in range(1, NCol):
            if not self.sSWMatrix.IsColGrowable(k):
                self.sSWMatrix.AddGrowableCol(k, 1)
            else:
                pass
        #------------------------------> Update sizer
        self.sSWMatrix.Layout()
        #endregion ---------------------------------------------> Setup Sizers

        #region --------------------------------------------------> Set scroll
        self.wSwMatrix.SetupScrolling()
        #endregion -----------------------------------------------> Set scroll

        return True
    #---

    def OnOK(self) -> bool:
        """Check wx.Dialog content and send values to topParent.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Super
        if super().OnOK()[0]:
            return True
        else:
            return False
        #endregion ------------------------------------------------> Super
    #---
    #endregion ------------------------------------------------> Class methods
#---


class PanePrefUpdate(wx.Panel):
    """Panel for the Preferences window.

        Parameters
        ----------
        parent: wx.Window
            Parent of the pane.
    """
    #region -----------------------------------------------------> Class setup
    cName = mConfig.npPrefUpdate
    #------------------------------>
    cLTab = mConfig.ntPrefUpdate
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent):
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(parent, name=self.cName)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wRBox = wx.RadioBox(
            self, 
            label   = 'Check for Updates',
            choices = ['Always', 'Never'],
         )
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        self.sSizer = wx.BoxSizer(orient=wx.VERTICAL)

        self.sSizer.Add(self.wRBox, 0, wx.EXPAND|wx.ALL, 5)

        self.SetSizer(self.sSizer)
        #endregion ---------------------------------------------------> Sizers
    #---
    #endregion -----------------------------------------------> Instance setup
#---
#endregion ----------------------------------------------------------> Classes


