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


"""Panels of the application"""


#region -------------------------------------------------------------> Imports
import _thread 
import shutil
from pathlib import Path
from typing import Optional, Union

import numpy as np
import pandas as pd
# # from statsmodels.stats.multitest import multipletests

import wx
import wx.lib.scrolledpanel as scrolled

# import dat4s_core.data.check as dtsCheck
import dat4s_core.data.file as dtsFF
import dat4s_core.data.method as dtsMethod
import dat4s_core.data.statistic as dtsStatistic
import dat4s_core.exception.exception as dtsException
import dat4s_core.gui.wx.validator as dtsValidator
import dat4s_core.gui.wx.widget as dtsWidget

import config.config as config
import data.check as check
# # import data.method as dmethod
import gui.dtscore as dtscore
# # import gui.method as gmethod
# import gui.widget as widget

# # if config.typeCheck:
# #     import pandas as pd
#endregion ----------------------------------------------------------> Imports


#region --------------------------------------------------------> Base Classes
class BaseConfPanel(
    scrolled.ScrolledPanel,
    dtsWidget.StaticBoxes, 
    dtsWidget.ButtonOnlineHelpClearAllRun
    ):
    """Creates the skeleton of a configuration panel. This includes the 
        wx.StaticBox, the bottom Buttons, the statusbar and some widgets.

        Parameters
        ----------
        cParent : wx Widget
            Parent of the widgets
        cRightDelete : Boolean
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
        dfTP : pd.DataFrame
            DataFrame filtered by Target Protein
        dfE : DataFrame
            Exclude some entries by some parameters
        dfS : DataFrame
            Exclude entries by Score values.
        dfT : pd.DataFrame
            DataFrame with the transformed values.
        dfN : pd.DataFrame
            DataFrame with normalized values.
        dfIm : pd.DataFrame
            DataFrame with imputed values.
        dfR : pd.DataFrame
            DataFrame with the results values.
        rChangeKey : list of str
            Keys in do whose values will be turned into a str. Default to
            ['iFile', 'uFile].
        rDate : str or None
            Date for the new section in the umsap file.
        rDateID : str or None
            Date + Analysis ID
        rDFile : Path
            Full path to copy the given input file if not in Data-Files.
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
        rMsgError: Str or None
            Error message to show when analysis fails
        rNCol: int
            Number of columns in the main input file - 1. Set when the file is
            read.
        rOFolder: Path or None
            Folder to contain the output. Set based on the umsap file path.
        rSeqFileObj: dtsFF.FastaFile
            Object to work with the sequences of the proteins 
        
            
        Notes
        -----
        The following attributes must be set in the child class
        cGaugePD : int 
            Number of steps for the wx.Gauge in the Progress Dialog shown when 
            running analysis        
        cName : str
            Unique name of the pane
        cSection : str 
            Section in the UMSAP file. One of the values in config.nameModules 
            or config.nameUtilities
        cTitlePD : str
            Title for the Progress Dialog shown when running analysis
        cURL : str 
            URL for the Help wx.Button
        rCheckUserInput : dict
            Dict to check individual fields in the user input in the correct 
            order. See CheckInput method for more details.
        rLLenLongest : int 
            Length of the longest label in output dict
    """
    #region -----------------------------------------------------> Class setup
    
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, cParent: wx.Window, cRightDelete: bool=True) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.cParent = cParent
        #------------------------------> Labels
        self.cLId          = getattr(self, 'cLId',          'Analysis ID')
        self.cLuFile       = getattr(self, 'cLuFile',       'UMSAP')
        self.cLiFile       = getattr(self, 'cLiFile',       'Data')
        self.cLRunBtn      = getattr(self, 'cLRunBtn',      'Start Analysis')        
        self.cLFileBox     = getattr(self, 'cLFileBox',     'Files && Folders')
        self.cLDataBox     = getattr(self, 'cLDataBox',     'Data Preparation')
        self.cLColumnBox   = getattr(self, 'cLColumnBox',   'Column numbers')
        self.cLCeroTreatD  = getattr(self, 'cLCeroTreatD',  '0s Missing')
        self.cLNormMethod  = getattr(self, 'cLNormMethod',  'Normalization')
        self.cLImputation  = getattr(self, 'cLImputation',  'Imputation')
        self.cLTransMethod = getattr(self, 'cLTransMethod', 'Transformation')
        self.cLValueBox  = getattr(self, 'cLValueBox', 'User-defined values')
        self.cLCeroTreat = getattr(
            self, 'cLCeroTreat', 'Treat 0s as missing values')
        # For Progress Dialog
        self.cLPdCheck    = getattr(self, 'cLPdCheck',  'Checking user input: ')
        self.cLPdPrepare  = getattr(self, 'cLPdPrepare', 'Preparing analysis: ')
        self.cLPdReadFile = getattr(
            self, 'cLPdReadFile', 'Reading input files: ')
        self.cLPdRun      = getattr(self, 'cLPdRun',     'Running analysis: ')
        self.cLPdWrite    = getattr(self, 'cLPdWrite',   'Writing output: ')
        self.cLPdLoad     = getattr(self, 'cLPdLoad',    'Loading output file')
        self.cLPdError    = getattr(self, 'cLPdError',   'Fatal Error')
        self.cLPdDone     = getattr(self, 'cLPdDone',    'All Done')
        self.cLPdEllapsed = getattr(self, 'cLPdEllapsed','Ellapsed time: ')
        #------------------------------> Size
        self.cSTc = getattr(self, 'cSTc', config.sTc)
        #------------------------------> Choices
        self.cONorm = getattr(self, 'cONorm', list(config.oNormMethod.values()))
        self.cOTrans = getattr(
            self, 'cOTrans', list(config.oTransMethod.values()))
        self.cOImputation = getattr(
            self, 'cOImputation', list(config.oImputation.values()))
        #------------------------------> Hints
        self.cHId    = getattr(self, 'cHId', 'e.g. HIV inhibitor')
        self.cHuFile = getattr(
            self, 'cHuFile', f"Path to the {self.cLuFile} file")
        self.cHiFile = getattr(
            self, 'cHiFile', f"Path to the {self.cLiFile} file")
        #------------------------------> Tooltips
        self.cTTRun = getattr(self, 'cTTRun', 'Start the analysis.')
        self.cTTHelp = getattr(
            self, 'cTTHelp', f'Read online tutorial at {config.urlHome}.')
        self.cTTuFile = getattr(
            self, 'cTTuFile', f'Select the {self.cLuFile} file.')
        self.cTTiFile = getattr(
            self, 'cTTiFile', f'Select the {self.cLiFile} file.')
        self.cTTClearAll = getattr(
            self, 'cTTClearAll', 'Clear all user input.')
        self.cTTId  = getattr(
            self, 'cTTId', ('Short text to id the analysis. Do not include the '
                            ' date of the analysis.'))
        self.cTTNormMethod = getattr(
            self, 'cTTNormMethod', (f'Select the Data {self.cLNormMethod} '
                                    f'method.'))
        self.cTTTransMethod = getattr(
            self, 'cTTTransMethod', (f'Select the Data {self.cLTransMethod} '
                                     f'method.'))
        self.cTTImputation  = getattr(
            self, 'cTTImputation', (f'Select the Data {self.cLImputation} '
                                    f'method.'))
        #------------------------------> Extensions
        self.cEiFile = getattr(self, 'ciFileE', config.elData)
        #------------------------------> Validator
        self.cVuFile = getattr(
            self, 
            'cVuFile',
            dtsValidator.OutputFF(fof='file', ext=config.esUMSAP[0], opt=False),
        )
        self.cViFile = getattr(
            self, 
            'cViFile',
            dtsValidator.InputFF(fof='file', ext=config.esData),
        )
        #------------------------------> To handle Data Preparation Steps
        self.dDataPrep = { # Keys are the messaging for the Progress Dialog
            "Setting Data Types"         : self.DatPrep_0_Float,
            "Filter Data: Target Protein": self.DatPrep_TargetProt,
            "Filter Data: Exclude Rows"  : self.DatPrep_Exclude,
            "Filter Data: Score Value"   : self.DatPrep_Score,
            "Data Transformation"        : self.DatPrep_Transformation,
            "Data Normalization"         : self.DatPrep_Normalization,
            "Data Imputation"            : self.DatPrep_Imputation,
        }
        #------------------------------> This is needed to handle Data File 
        # content load to the wx.ListCtrl in Tabs with multiple panels
        #--------------> Default wx.ListCtrl to load data file content
        self.wLCtrlI = None 
        #--------------> List to use just in case there are more than 1 
        self.rLCtrlL = []
        #------------------------------> Needed to Run the analysis
        #--------------> Dict with the user input as given
        self.rDI = {}
        #--------------> Dict with the processed user input
        self.rDO = {} 
        #--------------> Error message and exception to show in self.RunEnd
        self.rMsgError  = None 
        self.rException = None
        #--------------> pd.DataFrames for:
        self.dfI  = pd.DataFrame() # Initial and
        self.dfF  = pd.DataFrame() # Data as float and 0 and '' values as np.nan
        self.dfTP = pd.DataFrame() # Select Target Protein
        self.dfE  = pd.DataFrame() # Exclude entries by some parameter
        self.dfS  = pd.DataFrame() # Exclude entries by Score value
        self.dfT  = pd.DataFrame() # Transformed values
        self.dfN  = pd.DataFrame() # Normalized Values
        self.dfIm = pd.DataFrame() # Imputed values
        self.dfR  = pd.DataFrame() # Results values
        #--------------> date for umsap file
        self.rDate = None
        self.rDateID = None
        #--------------> folder for output
        self.rOFolder = None
        #--------------> input file for directing repeating analysis from
        # file copied to oFolder
        self.rDFile   = None
        #--------------> Obj for files
        self.rIFileObj   = None
        self.rSeqFileObj = None
        #------------------------------> 
        self.rChangeKey = getattr(self, 'changeKey', ['iFile', 'uFile'])
        #------------------------------> Parent init
        scrolled.ScrolledPanel.__init__(self, cParent, name=self.cName)

        dtsWidget.ButtonOnlineHelpClearAllRun.__init__(
            self, self, self.cURL, 
            labelR   = self.cLRunBtn,
            tooltipR = self.cTTRun,
            tooltipH = self.cTTHelp,
            tooltipC = self.cTTClearAll,
        )

        dtsWidget.StaticBoxes.__init__(self, self, 
            labelF      = self.cLFileBox,
            labelD      = self.cLDataBox,
            labelV      = self.cLValueBox,
            labelC      = self.cLColumnBox,
            rightDelete = cRightDelete,
        )
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wUFile = dtsWidget.ButtonTextCtrlFF(self.sbFile,
            btnLabel   = self.cLuFile,
            btnTooltip = self.cTTuFile,
            tcHint     = self.cHuFile,
            mode       = 'save',
            ext        = config.elUMSAP,
            tcStyle    = wx.TE_READONLY,
            validator  = self.cVuFile,
            ownCopyCut = True,
        )
        
        self.wIFile = dtsWidget.ButtonTextCtrlFF(self.sbFile,
            btnLabel   = self.cLiFile,
            btnTooltip = self.cTTiFile,
            tcHint     = self.cHiFile,
            ext        = self.cEiFile,
            mode       = 'openO',
            tcStyle    = wx.TE_READONLY|wx.TE_PROCESS_ENTER,
            validator  = self.cViFile,
            ownCopyCut = True,
        )
        
        self.wId = dtsWidget.StaticTextCtrl(
            self.sbFile,
            stLabel   = self.cLId,
            stTooltip = self.cTTId,
            tcHint    = self.cHId,
        )

        self.wCeroB = wx.CheckBox(self.sbData, label=self.cLCeroTreat)
        self.wCeroB.SetValue(True)
        self.wCeroB.SetToolTip(f'Cero values in the {self.cLiFile} File will '
            f'be treated as missing values when this option is selected or as '
            f'real values when the option is not selected.')
        
        self.wNormMethod = dtsWidget.StaticTextComboBox(
            self.sbData, 
            label     = self.cLNormMethod,
            choices   = self.cONorm,
            tooltip   = self.cTTNormMethod,
            validator = dtsValidator.IsNotEmpty(),
        )
        
        self.wTransMethod = dtsWidget.StaticTextComboBox(
            self.sbData, 
            label     = self.cLTransMethod,
            choices   = self.cOTrans,
            tooltip   = self.cTTTransMethod,
            validator = dtsValidator.IsNotEmpty(),
        )
        
        self.wImputationMethod = dtsWidget.StaticTextComboBox(
            self.sbData, 
            label     = self.cLImputation,
            choices   = self.cOImputation,
            tooltip   = self.cTTImputation,
            validator = dtsValidator.IsNotEmpty(),
        )
        #endregion --------------------------------------------------> Widgets
        
        #region -----------------------------------------------------> Tooltip
        
        #endregion --------------------------------------------------> Tooltip
        
        #region ------------------------------------------------------> Sizers
        self.sizersbFileWid.Add(
            self.wUFile.btn,
            pos    = (0,0),
            flag   = wx.EXPAND|wx.ALL,
            border = 5
        )
        self.sizersbFileWid.Add(
            self.wUFile.tc,
            pos    = (0,1),
            flag   = wx.EXPAND|wx.ALL,
            border = 5
        )
        self.sizersbFileWid.Add(
            self.wIFile.btn,
            pos    = (1,0),
            flag   = wx.EXPAND|wx.ALL,
            border = 5
        )
        self.sizersbFileWid.Add(
            self.wIFile.tc,
            pos    = (1,1),
            flag   = wx.EXPAND|wx.ALL,
            border = 5
        )
        self.sizersbFileWid.Add(
            self.wId.st,
            pos    = (2,0),
            flag   = wx.ALIGN_CENTER|wx.ALL,
            border = 5
        )
        self.sizersbFileWid.Add(
            self.wId.tc,
            pos    = (2,1),
            flag   = wx.EXPAND|wx.ALL,
            border = 5
        )
        self.sizersbFileWid.AddGrowableCol(1,1)
        self.sizersbFileWid.AddGrowableRow(0,1)
        
        self.sizersbDataWid.Add(
            1, 1,
            pos    = (0,0),
            flag   = wx.EXPAND|wx.ALL,
            border = 5
        )
        self.sizersbDataWid.Add(
            self.wCeroB,
            pos    = (0,1),
            flag   = wx.ALIGN_CENTER|wx.ALL,
            border = 5,
            span   = (0, 6),
        )
        self.sizersbDataWid.Add(
            self.wTransMethod.st,
            pos    = (1,1),
            flag   = wx.ALL|wx.ALIGN_CENTER,
            border = 5,
        )
        self.sizersbDataWid.Add(
            self.wTransMethod.cb,
            pos    = (1,2),
            flag   = wx.ALL|wx.EXPAND,
            border = 5,
        )
        self.sizersbDataWid.Add(
            self.wNormMethod.st,
            pos    = (1,3),
            flag   = wx.ALL|wx.ALIGN_CENTER,
            border = 5,
        )
        self.sizersbDataWid.Add(
            self.wNormMethod.cb,
            pos    = (1,4),
            flag   = wx.ALL|wx.EXPAND,
            border = 5,
        )
        self.sizersbDataWid.Add(
            self.wImputationMethod.st,
            pos    = (1,5),
            flag   = wx.ALL|wx.ALIGN_CENTER,
            border = 5,
        )
        self.sizersbDataWid.Add(
            self.wImputationMethod.cb,
            pos    = (1,6),
            flag   = wx.ALL|wx.EXPAND,
            border = 5,
        )
        self.sizersbDataWid.Add(
            1, 1,
            pos    = (0,7),
            flag   = wx.EXPAND|wx.ALL,
            border = 5
        )
        self.sizersbDataWid.AddGrowableCol(0,1)
        self.sizersbDataWid.AddGrowableCol(7,1)

        self.sSizer = wx.BoxSizer(wx.VERTICAL)

        self.sSizer.Add(self.sizersbFile,   0, wx.EXPAND|wx.ALL,       5)
        self.sSizer.Add(self.sizersbData,   0, wx.EXPAND|wx.ALL,       5)
        self.sSizer.Add(self.sizersbValue,  0, wx.EXPAND|wx.ALL,       5)
        self.sSizer.Add(self.sizersbColumn, 0, wx.EXPAND|wx.ALL,       5)
        self.sSizer.Add(self.btnSizer,      0, wx.ALIGN_CENTER|wx.ALL, 5)
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind
        self.wIFile.tc.Bind(wx.EVT_TEXT,       self.OnIFileLoad)
        self.wIFile.tc.Bind(wx.EVT_TEXT_ENTER, self.OnIFileLoad)
        self.wUFile.tc.Bind(wx.EVT_TEXT,       self.OnUFileChange)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #------------------------------> Class Methods
    #region ---------------------------------------------------> Event Methods
    def OnUFileChange(self, event: wx.CommandEvent) -> bool:
        """Adjust the default initial path to search for input files when an 
            UMSAP file is selected.
    
            Parameters
            ----------
            event: wx.Event
                Information about the event
            
            Returns
            -------
            bool
        """
        #region -------------------------------------------------> Set defPath
        if (fileP := self.wUFile.tc.GetValue()) == '':
            self.wIFile.defPath = None
        else:
            #------------------------------> 
            p = Path(fileP).parent / config.fnDataInit
            #------------------------------> 
            if p.exists():
                self.wIFile.defPath = p
            else:
                self.wIFile.defPath = None
        #endregion ----------------------------------------------> Set defPath
        
        return True
    #---
    
    def OnIFileLoad(self, event: wx.CommandEvent) -> bool:
        """Clear GUI elements when Data Folder is ''
    
            Parameters
            ----------
            event: wx.Event
                Information about the event		
                
            Return
            ------
            bool
        """
        if (fileP := self.wIFile.tc.GetValue()) == '':
            return self.LCtrlEmpty()
        else:
            return self.OnIFileEnter(fileP)
    #---
    
    def OnIFileEnter(self, fileP: Path) -> bool:
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
            dtsMethod.LCtrlFillColNames(self.wLCtrlI, fileP)
        except Exception as e:
            dtscore.Notification('errorF', msg=str(e), tException=e)
            return False
        #endregion ------------------------------------------------> Fill list
        
        #region -----------------------------------------> Columns in the file
        self.rNCol = self.wLCtrlI.GetItemCount() - 1
        #endregion --------------------------------------> Columns in the file

        return True
    #---	
    #endregion ------------------------------------------------> Event Methods

    #region ---------------------------------------------------> Other Methods
    def LCtrlEmpty(self) -> bool:
        """Clear wx.ListCtrl and NCol 
        
            Returns
            -------
            bool
        
            Notes
            -----
            Helper function to accomodate several wx.ListCtrl in the panel.
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
    #endregion ------------------------------------------------> Other Methods
    
    #region ----------------------------------------------------> Run Analysis
    def OnRun(self, event: wx.CommandEvent) -> bool:
        """ Start analysis of the module/utility

            Parameter
            ---------
            event : wx.Event
                Event information
                
            Returns
            -------
            bool
        """
        #region --------------------------------------------------> Dlg window
        self.rDlg = dtscore.ProgressDialog(
            config.winMain, self.cTitlePD, self.cGaugePD)
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
    
    def UniqueColumnNumber(self, l: list[wx.TextCtrl]) -> bool:
        """Check l contains unique numbers. 
    
            Parameters
            ----------
            l: list of wx.TextCtrl
                List of wx.TextCtrl that must contain column numbers.
    
            Returns
            -------
            bool
            
            Notes
            -----
            Needed here to make sure that all wx.TextCtrl in l contains valid
            input.
        """
        #region -----------------------------------------------------> Message
        msgStep = self.cLPdCheck + 'Unique column numbers'
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        #endregion --------------------------------------------------> Message
        
        #region -------------------------------------------------------> Check
        a, b = check.TcUniqueColNumbers(l)
        if a:
            pass
        else:
            msg = config.mSection.format(self.cLColumnBox)
            self.msgError = dtscore.StrSetMessage(msg, b[2])
            return False
        #endregion ----------------------------------------------------> Check
        
        return True
    #---
    
    def CheckInput(self) -> bool:
        """Check individual fields in the user input.
        
            Returns
            -------
            bool
        
            Notes
            -----
            The child class must define a rCheckUserInput dict with the correct
            order for the checking process.
            
            rCheckUserInput = {
                'Field label' : [Widget, BaseErrorMessage]
            }
            
            BaseErrorMessage must be a string with two placeholder for the 
            error value and Field label in that order. For example:
            'File: {bad_path_placeholder}\n cannot be used as 
                                                    {Field_label_placeholder}'
        """
        #region -------------------------------------------------------> Check
        for k,v in self.rCheckUserInput.items():
            #------------------------------> 
            msgStep = self.cLPdCheck + k
            wx.CallAfter(self.rDlg.UpdateStG, msgStep)
            #------------------------------> 
            a, b = v[0].GetValidator().Validate()
            if a:
                pass
            else:
                self.rMsgError = dtscore.StrSetMessage(
                    v[1].format(b[1], k), b[2])
                return False
        #endregion ----------------------------------------------------> Check
        
        return True
    #---
    
    def EqualLenLabel(self, label: str) -> str:
        """Add empty space to the end of label to match the length of
            self.rLLenLongest
    
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
    
    def PrepareRun(self) -> bool:
        """Set variable and prepare data for analysis.
        
            Returns
            -------
            bool
        """
        #------------------------------> File base name
        self.rOFolder = self.rDO['uFile'].parent
        #------------------------------> Date
        self.rDate = dtsMethod.StrNow()
        #------------------------------> DateID
        if self.rDO['ID']:
            self.rDateID = f'{self.rDate} - {self.rDO["ID"]}'
        else:
            self.rDateID = f'{self.rDate}'
        #endregion ----------------------------------------------------> Input
    
        return True
    #---

    
    def ReadInputFiles(self) -> bool:
        """Read input file and check data
        
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
            self.rIFileObj = dtsFF.CSVFile(self.rDO['iFile'])
        except dtsException.FileIOError as e:
            self.rMsgError = config.mFileRead.format(self.rDO['iFile'])
            self.rException = e
            return False
        #endregion ------------------------------------------------> Data file
        
        #region ------------------------------------------------> Seq Rec File
        if 'seqFile' in self.rDO:
            #------------------------------> 
            msgStep = self.cLPdReadFile + f"{self.cLSeqFile}, reading"
            wx.CallAfter(self.rDlg.UpdateStG, msgStep)
            #------------------------------> 
            try:
                self.rSeqFileObj = dtsFF.FastaFile(self.rDO['seqFile'])
            except Exception as e:
                self.msgError = config.mFileRead.format(self.rDO['seqFile'])
                self.tException = e
                return False
        else:
            pass
        #endregion ---------------------------------------------> Seq Rec File
        
        #region ---------------------------------------------------> Print Dev
        if config.development and self.rSeqFileObj is not None:
            print("Rec Seq: ", self.rSeqFileObj.seqRec)
            print("Nat Seq: ", self.rSeqFileObj.seqNat)
        else:
            pass
        #endregion ------------------------------------------------> Print Dev
        
        return True
    #---
    
    def DataPreparation(self, resetIndex=True) -> bool:
        """Perform the data preparation step.
            
            Parameters
            ----------
            resetIndex: bool
                If True reset the index of self.dfImp
    
            Returns
            -------
            bool
    
            Notes
            -----
            See the Notes for the individual methods:
                self.DatPrep_0_Float, 
                self.DatPrep_TargetProt,
                self.DatPrep_Exclude, 
                self.DatPrep_Score,
                self.DatPrep_Transformation,
                self.DatPrep_Normalization,
                self.DatPrep_Imputation,
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
            self.dfIm.reset_index(drop=True, inplace=True)
        else:
            pass
        #endregion ----------------------------------------------> Reset index
        
        #region -------------------------------------------------------> Print
        if config.development:
            #------------------------------> 
            dfL = [
                self.dfI, self.dfF, self.dfTP, self.dfE, self.dfS, self.dfT, 
                self.dfN, self.dfIm
            ]
            dfN = ['dfI', 'dfF', 'dfTP', 'dfEx', 'dfS', 'dfT', 'dfN', 'dfIm']
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
    
    def DatPrep_0_Float(self) -> bool:
        """Convert or not 0s to NA and then all values to float.
        
            Returns
            -------
            bool
                
            Notes
            -----
            Assumes child class has the following attributes:
            - iFileObj: instance of dtsFF.CSVFile
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
            self.dfI = self.rIFileObj.df.iloc[:,self.rDO['oc']['Column']]
        except Exception as e:
            self.rMsgError = config.mPDGetInitCol.format(
                self.rDO['oc']['Column'], self.cLiFile, self.rDO['iFile'])
            self.rException = e
            return False
        #endregion --------------------------------------------------> Set dfI
        
        #region -----------------------------------------------------> Set dfF
        try:
            if self.rDO['Cero']:
                #------------------------------> Replace 0 and ''
                self.dfF = dtsMethod.DFReplace(
                    self.dfI, [0, ''], np.nan, sel=self.rDO['df']['ColumnR'])
            else:
                #------------------------------> Replace only ''
                self.dfF = dtsMethod.DFReplace(
                    self.dfI, [''], np.nan, sel=self.rDO['df']['ColumnR'])
            #------------------------------> Float
            self.dfF.iloc[:,self.rDO['df']['ColumnF']] = self.dfF.iloc[:,self.rDO['df']['ColumnF']].astype('float')
        except Exception as e:
            self.rMsgError = config.mPDDataTypeCol.format(
                self.cLiFile, ", ".join(map(str, self.rDO['df']['ColumnF'])))
            self.rException = e
            return False
        #endregion --------------------------------------------------> Set dfF
        
        return True
    #---
    
    def DatPrep_TargetProt(self) -> bool:
        """Filter data based on the value of Target Protein.
        
            See Notes below for more details
    
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
                self.dfTP = dtsMethod.DFFilterByColS(
                    self.dfF, 
                    self.rDO['df']['TargetProtCol'],
                    self.rDO['TargetProt'], 
                    'e',
                )
            else:
                self.dfTP = self.dfF.copy()
        except Exception as e:
            self.rMsgError = config.mPDDataTargetProt.format(
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
                self.dfE = dtsMethod.DFExclude(
                    self.dfTP, self.rDO['df']['ExcludeR'])
            else:
                self.dfE = self.dfTP.copy()
        except Exception as e:
            self.rMsgError = config.mPDDataExclude.format(
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
                self.dfS = dtsMethod.DFFilterByColN(
                    self.dfE, 
                    [self.rDO['df']['ScoreCol']], 
                    self.rDO['ScoreVal'], 
                    'ge'
                )
            else:
                self.dfS = self.dfE.copy()
        except Exception as e:
            self.rMsgError = config.mPDDataScore.format(
                self.rDO['df']['ScoreCol'])
            self.rException = e
            return False
        #endregion ---------------------------------------------------> Filter
        
        #region -----------------------> Check some Rows are left for Analysis
        if self.dfS.empty:
            self.rMsgError = config.mNoDataLeft
            return False
        else:
            pass
        #endregion --------------------> Check some Rows are left for Analysis

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
            self.dfT = dtsStatistic.DataTransformation(
                self.dfS, 
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
            self.dfN = dtsStatistic.DataNormalization(
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
            self.dfIm = dtsStatistic.DataImputation(
                self.dfN, 
                self.rDO['df']['ResCtrlFlat'], 
                method = self.rDO['ImpMethod'],
            )
        except Exception as e:
            self.rMsgError   = 'Data Imputation failed.'
            self.rException = e
            return False
        #endregion -----------------------------------------------> Imputation
        
        return True
    #---
    
    def SetOutputDict(self, dateDict) -> dict:
        """Creates the output dictionary to be written to the output file 
        
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
                outData = dtsFF.ReadJSON(self.rDO['uFile'])
            except Exception as e:
                msg = config.mFileRead.format(self.rDO['uFile'])
                raise dtsException.ExecutionError(msg)
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
        dataFolder = f"{self.rDate}_{self.cSection}"
        dataFolder = self.rOFolder / config.fnDataSteps / dataFolder
        dataFolder.mkdir(parents=True, exist_ok=True)
        #------------------------------> 
        msgStep = self.cLPdWrite + 'Creating needed folders, Data-Initial folder'
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        dataInit = self.rOFolder / config.fnDataInit
        dataInit.mkdir(parents=True, exist_ok=True)
        #endregion --------------------------------------------> Create folder
        
        #region ------------------------------------------------> Data Initial
        msgStep = self.cLPdWrite + 'Data files, Data file'
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        #------------------------------> 
        piFolder = self.rDO['iFile'].parent
        puFolder = self.rDO['uFile'].parent / config.fnDataInit
        #------------------------------>
        if not piFolder == puFolder:
            #------------------------------> 
            name = (
                f"{self.rDate}-{self.rDO['iFile'].stem}{self.rDO['iFile'].suffix}")
            self.rDFile = puFolder/name
            #------------------------------> 
            shutil.copy(self.rDO['iFile'], self.rDFile)
            #------------------------------> 
            self.rDI[self.EqualLenLabel(self.cLiFile)] = str(self.rDFile)
        else:
            self.rDFile = None
        #endregion ---------------------------------------------> Data Initial
        
        #region --------------------------------------------------> Data Steps
        msgStep = self.cLPdWrite + 'Data files, Step by Step Data files'
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        try:
            dtsFF.WriteDFs2CSV(dataFolder, stepDict)
        except Exception as e:
            self.rMsgError = ('It was not possible to create the files with '
                'the data for the intermediate steps of the analysis.')
            self.rException = e
            return False
        #endregion -----------------------------------------------> Data Steps
        
        #region --------------------------------------------------> UMSAP File
        msgStep = self.cLPdWrite + 'Main file'
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        #------------------------------> Create output dict
        dateDict = {
            self.rDateID : {
                'V' : config.dictVersion,
                'I' : self.rDI,
                'CI': dtsMethod.DictVal2Str(self.rDO, self.rChangeKey, new=True),
                'DP': {
                    config.ltDPKeys[0] : self.dfS.to_dict(),
                    config.ltDPKeys[1] : self.dfT.to_dict(),
                    config.ltDPKeys[2] : self.dfN.to_dict(),
                    config.ltDPKeys[3] : self.dfIm.to_dict(),
                },
            }
        }
        #-------------->  DataPrep Util does not have dfR
        if self.dfR is not None:
            dateDict[self.rDateID]['R'] = dtsMethod.DictTuplesKey2StringKey(
                self.dfR.to_dict()
            )
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
            dtsFF.WriteJSON(self.rDO['uFile'], outData)
        except Exception as e:
            self.rMsgError = ('It was not possible to create the dictionary '
                'with the UMSAP data.')
            self.rException = e
            return False
        #endregion -----------------------------------------------> UMSAP File

        return True
    #---
    
    def LoadResults(self) -> bool:
        """Load output file
        
            Returns
            -------
            bool
        """
        #region --------------------------------------------------------> Load
        wx.CallAfter(self.rDlg.UpdateStG, self.cLPdLoad)
        
        # wx.CallAfter(gmethod.LoadUMSAPFile, fileP=self.do['uFile'])
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
        if self.rMsgError is None:
            #--> 
            self.rDlg.SuccessMessage(
                self.cLPdDone, eTime=f"{self.cLPdEllapsed} {self.deltaT}")
        else:
            self.rDlg.ErrorMessage(
                self.cLPdError,error=self.rMsgError,tException=self.rException)
        #endregion ------------------------------------> Dlg progress dialogue

        #region -------------------------------------------------------> Reset
        self.rMsgError  = None # Error msg to show in self.RunEnd
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
        self.rDate      = None # date for corr file
        self.rDateID    = None
        self.rOFolder   = None # folder for output
        self.rIFileObj  = None
        self.deltaT     = None # Defined in DAT4S 
        
        if self.rDFile is not None:
            self.wIFile.tc.SetValue(str(self.rDFile))
        else:
            pass
        self.rDFile = None # Data File copied to Data-Initial
        #endregion ----------------------------------------------------> Reset
        
        return True
    #---
    #endregion -------------------------------------------------> Run Analysis
#---
    
    
# class BaseConfModPanel(BaseConfPanel, widget.ResControl):
#     """Base configuration for a panel of a module.

#         Parameters
#         ----------
#         cParent : wx Widget
#             Parent of the widgets
#         cRightDelete : Boolean
#             Enables clearing wx.StaticBox input with right click
#     """
#     #region -----------------------------------------------------> Class setup
    
#     #endregion --------------------------------------------------> Class setup

#     #region --------------------------------------------------> Instance setup
#     def __init__(self, cParent: wx.Window, cRightDelete: bool=True) -> None:
#         """ """
#         #region -------------------------------------------------> Check Input
        
#         #endregion ----------------------------------------------> Check Input

#         #region -----------------------------------------------> Initial Setup
#         #------------------------------> Label
#         self.cLAlpha    = getattr(self, 'cLAlpha',    'Significance Level')
#         self.cLScoreVal = getattr(self, 'cLScoreVal', config.lStScoreVal)
#         self.cLScoreCol = getattr(self, 'cLScoreCol', config.lStScoreCol)
#         self.cLDetectedProt = getattr(
#             self, 'cLDetectedProt', 'Detected Proteins')
#         #------------------------------> Tooltips
#         self.cTTAlpha        = getattr(self, 'cTTAlpha',    config.ttStAlpha)
#         self.cTTScore        = getattr(self, 'cTTScore',    config.ttStScore)
#         self.cTTScoreVal     = getattr(self, 'cTTScoreVal', config.ttStScoreVal)
#         self.cTTDetectedProt = getattr(
#             self, 'cTTDetectedProtL', config.ttStDetectedProtL)
#         #------------------------------> Parent class init
#         BaseConfPanel.__init__(self, cParent, cRightDelete=cRightDelete)

#         widget.ResControl.__init__(self, self.sbColumn)
#         #endregion --------------------------------------------> Initial Setup

#         #region --------------------------------------------------------> Menu
        
#         #endregion -----------------------------------------------------> Menu

#         #region -----------------------------------------------------> Widgets
#         self.wAlpha = dtsWidget.StaticTextCtrl(
#             self.sbValue,
#             stLabel   = self.cLAlpha,
#             stTooltip = self.cTTAlpha,
#             tcSize    = self.cSTc,
#             tcHint    = 'e.g. 0.05',
#             validator = dtsValidator.NumberList(
#                 numType='float', nN=1, vMin=0, vMax=1),
#         )

#         self.wScoreVal = dtsWidget.StaticTextCtrl(
#             self.sbValue,
#             stLabel   = self.cLScoreVal,
#             stTooltip = self.cTTScoreVal,
#             tcSize    = self.cSTc,
#             tcHint    = 'e.g. 320',
#             validator = dtsValidator.NumberList(numType='float', nN=1),
#         )

#         self.wDetectedProt = dtsWidget.StaticTextCtrl(
#             self.sbColumn,
#             stLabel   = self.cLDetectedProt,
#             stTooltip = self.cTTDetectedProt,
#             tcSize    = self.cSTc,
#             tcHint    = 'e.g. 0',
#             validator = dtsValidator.NumberList(numType='int', nN=1, vMin=0),
#         )

#         self.wScore = dtsWidget.StaticTextCtrl(
#             self.sbColumn,
#             stLabel   = self.cLScoreCol,
#             stTooltip = self.cTTScore,
#             tcSize    = self.cSTc,
#             tcHint    = 'e.g. 39',
#             validator = dtsValidator.NumberList(numType='int', nN=1, vMin=0),
#         )
#         #endregion --------------------------------------------------> Widgets

#         #region -----------------------------------------------------> Tooltip
        
#         #endregion --------------------------------------------------> Tooltip
        
#         #region ------------------------------------------------------> Sizers
        
#         #endregion ---------------------------------------------------> Sizers

#         #region --------------------------------------------------------> Bind
        
#         #endregion -----------------------------------------------------> Bind

#         #region ---------------------------------------------> Window position
        
#         #endregion ------------------------------------------> Window position
#     #---
#     #endregion -----------------------------------------------> Instance setup

#     #region ---------------------------------------------------> Class methods
    
#     #endregion ------------------------------------------------> Class methods
# #---


# # class BaseConfModPanel2(BaseConfModPanel):
# #     """Base class for the LimProt and TarProt configuration panel.

# #         Parameters
# #         ----------
# #         parent : wx Widget
# #             Parent of the widgets
# #         rightDelete : Boolean
# #             Enables clearing wx.StaticBox input with right click

# #         Attributes
# #         ----------
# #         #------------------------------> Configuration
# #         cEseqFile: wxPython extension list
# #             Extension for sequence files
# #         cHSeqFile: str
# #             Hint for the Sequences File
# #         cLSeqCol: str
# #             Label for Sequences in the Columns section
# #         cLSeqFile : str
# #             Label for the Sequence File
# #         cLSeqLength: str
# #             Label for the Sequence Length
# #         cLTargetProt: str
# #             Label for the Target Protein
# #         cMseqFile : str
# #             Mode to search for the sequence file
# #     """
# #     #region -----------------------------------------------------> Class setup
    
# #     #endregion --------------------------------------------------> Class setup

# #     #region --------------------------------------------------> Instance setup
# #     def __init__(self, parent: wx.Window, rightDelete: bool=True) -> None:
# #         """ """
# #         #region -------------------------------------------------> Check Input
        
# #         #endregion ----------------------------------------------> Check Input

# #         #region -----------------------------------------------> Initial Setup
# #         #------------------------------> Label
# #         self.cLSeqFile    = getattr(self, 'cLSeqFile', config.lStSeqFile)
# #         self.cLSeqLength  = getattr(self, 'cLSeqLength', config.lStSeqLength)
# #         self.cLTargetProt = getattr(self, 'cLtargetProt', config.lStTargetProt)
# #         self.cLSeqCol     = getattr(self, 'cLSeqCol', config.lStSeqCol)
# #         #------------------------------> Hint
# #         self.cHSeqFile = getattr(self, 'cHSeqFile', config.hTcSeqFile)
# #         #------------------------------> Mode
# #         self.cMseqFile = getattr(self, 'cMseqFile', 'openO')
# #         #------------------------------> Extensions
# #         self.cEseqFile = getattr(self, 'cEseqFile', config.elSeq)
# #         #------------------------------> 
# #         super().__init__(parent, rightDelete=rightDelete)
# #         #endregion --------------------------------------------> Initial Setup

# #         #region --------------------------------------------------------> Menu
        
# #         #endregion -----------------------------------------------------> Menu

# #         #region -----------------------------------------------------> Widgets
# #         #------------------------------> Files
# #         self.seqFile = dtsWidget.ButtonTextCtrlFF(
# #             self.sbFile,
# #             btnLabel   = self.cLSeqFile,
# #             tcHint     = self.cHSeqFile,
# #             mode       = self.cMseqFile,
# #             ext        = self.cEseqFile,
# #             tcStyle    = wx.TE_READONLY,
# #             validator  = dtsValidator.InputFF(fof='file', ext=config.esSeq),
# #             ownCopyCut = True,
# #         )
# #         #------------------------------> Values
# #         self.targetProt = dtsWidget.StaticTextCtrl(
# #             self.sbValue,
# #             stLabel   = self.cLTargetProt,
# #             tcSize    = self.cSTc,
# #             validator = dtsValidator.IsNotEmpty()
# #         )
# #         self.seqLength = dtsWidget.StaticTextCtrl(
# #             self.sbValue,
# #             stLabel   = self.cLSeqLength,
# #             tcSize    = self.cSTc,
# #             validator = dtsValidator.NumberList(
# #                 numType = 'int',
# #                 nN      = 1,
# #                 vMin    = 1,
# #                 opt     = True,
# #             )
# #         )
# #         #------------------------------> Columns
# #         self.seqCol = dtsWidget.StaticTextCtrl(
# #             self.sbColumn,
# #             stLabel   = self.cLSeqCol,
# #             tcSize    = self.cSTc,
# #             validator = dtsValidator.NumberList(
# #                 numType = 'int',
# #                 nN      = 1,
# #                 vMin    = 0,
# #             )
# #         )
# #         #endregion --------------------------------------------------> Widgets

# #         #region ------------------------------------------------------> Sizers
# #         #------------------------------> Sizer Files
# #         #--------------> 
# #         self.sizersbFileWid.Detach(self.id.st)
# #         self.sizersbFileWid.Detach(self.id.tc)
# #         #--------------> 
# #         self.sizersbFileWid.Add(
# #             self.seqFile.btn,
# #             pos    = (2,0),
# #             flag   = wx.EXPAND|wx.ALL,
# #             border = 5
# #         )
# #         self.sizersbFileWid.Add(
# #             self.seqFile.tc,
# #             pos    = (2,1),
# #             flag   = wx.EXPAND|wx.ALL,
# #             border = 5
# #         )
# #         self.sizersbFileWid.Add(
# #             self.id.st,
# #             pos    = (3,0),
# #             flag   = wx.ALIGN_CENTER|wx.ALL,
# #             border = 5
# #         )
# #         self.sizersbFileWid.Add(
# #             self.id.tc,
# #             pos    = (3,1),
# #             flag   = wx.EXPAND|wx.ALL,
# #             border = 5
# #         )
# #         #------------------------------> Sizer Columns
# #         self.sizersbColumnWid.Add(
# #             self.seqCol.st,
# #             pos    = (0,0),
# #             flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
# #             border = 5,
# #         )
# #         self.sizersbColumnWid.Add(
# #             self.seqCol.tc,
# #             pos    = (0,1),
# #             flag   = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL,
# #             border = 5,
# #         )
# #         self.sizersbColumnWid.Add(
# #             self.detectedProt.st,
# #             pos    = (0,2),
# #             flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
# #             border = 5,
# #         )
# #         self.sizersbColumnWid.Add(
# #             self.detectedProt.tc,
# #             pos    = (0,3),
# #             flag   = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL,
# #             border = 5,
# #         )
# #         self.sizersbColumnWid.Add(
# #             self.score.st,
# #             pos    = (0,4),
# #             flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
# #             border = 5,
# #         )
# #         self.sizersbColumnWid.Add(
# #             self.score.tc,
# #             pos    = (0,5),
# #             flag   = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL,
# #             border = 5,
# #         )
# #         self.sizersbColumnWid.Add(
# #             self.sizerRes,
# #             pos    = (1,0),
# #             flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND,
# #             border = 0,
# #             span   = (0,6),
# #         )
# #         self.sizersbColumnWid.AddGrowableCol(1,1)
# #         self.sizersbColumnWid.AddGrowableCol(3,1)
# #         self.sizersbColumnWid.AddGrowableCol(5,1)
# #         #endregion ---------------------------------------------------> Sizers

# #         #region --------------------------------------------------------> Bind
        
# #         #endregion -----------------------------------------------------> Bind

# #         #region ---------------------------------------------> Window position
        
# #         #endregion ------------------------------------------> Window position
# #     #---
# #     #endregion -----------------------------------------------> Instance setup

# #     #region ---------------------------------------------------> Class methods
# #     def NCResNumbers(self, seqNat: bool=True) -> bool:
# #         """Find the residue numbers for the peptides in the sequence of the 
# #             Recombinant and Native protein.
            
# #             Parameters
# #             ----------
# #             seqNat: bool
# #                 Calculate N and C residue numbers also for the Native protein
                
# #             Returns
# #             -------
# #             bool
            
# #             Notes
# #             -----
# #             Assumes child class has the following attributes:
# #             - seqFileObj: dtsFF.FastaFile
# #                 Object with the sequence of the Recombinant and Native protein
# #             - do: dict with at least the following key - values pairs
# #                 {
# #                     'df' : {
# #                         'SeqCol' : int,
# #                     },
# #                     'dfo' : {
# #                         'NC' : list[int],
# #                         'NCF': list[int],
# #                     },
# #                 }
# #         """
# #         #region ---------------------------------------------------------> Msg
# #         msgPrefix = config.lPdRun
# #         #endregion ------------------------------------------------------> Msg
        
# #         #region -----------------------------------------------------> Rec Seq
# #         #------------------------------> 
# #         msgStep = (f'{msgPrefix} Calculating output data - N & C terminal '
# #             f'residue numbers I')
# #         wx.CallAfter(self.dlg.UpdateStG, msgStep)
# #         #------------------------------> 
# #         try:
# #             self.dfR.iloc[:,self.do['dfo']['NC']] = self.dfR.iloc[
# #                 :,[self.do['df']['SeqCol'], 1]].apply(
# #                     self.NCTerm, 
# #                     axis        = 1,
# #                     raw         = True,
# #                     result_type = 'expand',
# #                     args        = (self.seqFileObj, 'Recombinant'),
# #                 )
# #         except dtsException.ExecutionError:
# #             return False
# #         except Exception as e:
# #             self.msgError = config.mUnexpectedError
# #             self.tException = e
# #             return False
# #         #endregion --------------------------------------------------> Rec Seq
        
# #         #region -----------------------------------------------------> Nat Seq
# #         #------------------------------> 
# #         msgStep = (f'{msgPrefix} Calculating output data - N & C terminal '
# #             f'residue numbers II')
# #         wx.CallAfter(self.dlg.UpdateStG, msgStep)
# #         #------------------------------> 
# #         if seqNat and self.seqFileObj.seqNat is not None:
# #             #------------------------------> 
# #             delta = self.seqFileObj.GetSelfDelta()
# #             #------------------------------> 
# #             a = self.dfR.iloc[:,self.do['dfo']['NC']] + delta
# #             self.dfR.iloc[:,self.do['dfo']['NCF']] = a
# #             #------------------------------> 
# #             m = self.dfR.iloc[:,self.do['dfo']['NCF']] > 0
# #             a = self.dfR.iloc[:,self.do['dfo']['NCF']].where(m, np.nan)
# #             a = a.astype('Int16')
# #             self.dfR.iloc[:,self.do['dfo']['NCF']] = a
# #         else:
# #             pass
# #         #endregion --------------------------------------------------> Nat Seq
        
# #         return True
# #     #---
    
# #     def NCTerm(
# #         self, row: list[str], seqObj: 'dtsFF.FastaFile', seqType: str
# #         ) -> tuple[int, int]:
# #         """Get the N and C terminal residue numbers for a given peptide.
    
# #             Parameters
# #             ----------
# #             row: list[str]
# #                 List with two elements. The Sequence is in index 0.
# #             seqObj : dtsFF.FastaFile
# #                 Object with the protein sequence and the method to search the 
# #                 peptide sequence.
# #             seqType : str
# #                 For the error message.
    
# #             Returns
# #             -------
# #             (Nterm, Cterm)
    
# #             Raise
# #             -----
# #             ExecutionError:
# #                 - When the peptide was not found in the sequence of the protein.
# #         """
# #         #region ---------------------------------------------------> Find pept
# #         nc = seqObj.FindSeq(row[0])
# #         #endregion ------------------------------------------------> Find pept
        
# #         #region ----------------------------------------------------> Check ok
# #         if nc[0] != -1:
# #             return nc
# #         else:
# #             self.msgError = config.mSeqPeptNotFound.format(row[0], seqType)
# #             raise dtsException.ExecutionError(self.msgError)
# #         #endregion -------------------------------------------------> Check ok
# #     #---
# #     #endregion ------------------------------------------------> Class methods
# #---


# class ResControlExpConfBase(wx.Panel):
#     """Parent class for the configuration panel in the dialog Results - Control
#         Experiments.

#         Parameters
#         ----------
#         cParent : wx.Widget
#             Parent of the widgets
#         cName : str	
#             Unique name of the panel
#         cTopParent : wx.Widget
#             Top parent window
#         cNColF : int
#             Number of columns in the input file.

#         Attributes
#         ----------
#         rLbDict : dict of lists of wx.StaticText for user-given labels
#             Keys are 1 to N plus 'Control' and values are the lists.
#             List of wx.StaticText to show the given user labels in the Field
#             region.    
#         rNColF: int
#             Number of columns in the input file minus 1.
#         rPName: str
#             Name of the parent window.
#         rStLabel : list of wx.StaticText
#             List of wx.StaticText with the label names. e.g. Conditions
#         rTcDict : dict of lists of wx.TextCtrl for labels
#             Keys are 1 to N and values are lists of wx.TextCtrl for the user 
#             given label.
#             List of wx.TextCtrl to input the number of labels.
#         rTcDictF : dict of lists of wx.TextCtrl for fields
#             Keys are 1 to NRow and values are lists of wx.TextCtrl for the user
#             given column numbers. 
#         rTcLabel : list of wx.TextCtrl
#             To give the number of user defined labels. e.g. 2 Conditions.
        
#         Notes
#         -----
#         The following attributes must be set in the child class
#         cHTotalField: str
#             Hint for the total number of required labels.
#         cLabelText: dict
#             Keys are 1 to cN and values the prefix for the label values. e.g. C
#         cStLabel: dict
#             Keys are 1 to cN and values the text of the labels. e.g. Condition.
#         cN: int
#             Number of labels excluding control labels.
#         cTTTotalField: list of str
#             Tooltips for the labels
        
#         The panel is divided in two sections. 
#         - Section Label holds information about the label for the experiments 
#         and control.
#             The number of labels and the name are set in the child class with 
#             cStLabel and cN.
#             This information is converted to rStLabel (name of the label e.g 
#             Condition), rTcLabel (input of number of each labels) and rTcDict 
#             (name of the experiment points e.g. Cond1).
#         - Section Fields that holds the information about the column numbers
#             The name of the experiments is shown with rLbDict that is populated 
#             from rTcDict
#             The column numbers are stored in rTcDictF.
        
#         See OnOk method for information about how the column numbers are
#         exported to the parent panel.
#     """
#     #region -----------------------------------------------------> Class setup
    
#     #endregion --------------------------------------------------> Class setup

#     #region --------------------------------------------------> Instance setup
#     def __init__(self, cParent: wx.Window, cName: str, cTopParent: wx.Window, 
#         cNColF: int) -> None:
#         """ """
#         #region -----------------------------------------------> Initial Setup        
#         self.cTopParent = cTopParent
#         self.rPName     = self.cTopParent.cName
#         #------------------------------> 
#         self.rTcDictF   = {}
#         #------------------------------> User given labels
#         self.rLbDict    = {}
#         self.rNColF     = cNColF - 1
#         #------------------------------> Label
#         self.cLSetup    = getattr(self, 'cLSetup',    'Setup Fields')
#         self.cLControlN = getattr(self, 'cLControlN', 'Control Name')
#         #------------------------------> Hint
#         self.cHControlN   = getattr(self, 'cHControlN',   'MyControl')
#         self.cHTotalField = getattr(self, 'cHTotalField', '#')
#         #------------------------------> Size
#         self.cSLabel      = getattr(self, 'cSLabel',      (60,22))
#         self.cSSWLabel    = getattr(self, 'cSSWLabel',    (670,135))
#         self.cSSWMatrix   = getattr(self, 'cSSWMatrix',   (670,670))
#         self.cSTotalField = getattr(self, 'cSTotalField', (35,22))
#         #------------------------------> Tooltip
#         self.cTTControlN = getattr(self, 'cTTControlN', config.ttStControlN)     
#         #------------------------------> Validator
#         self.cVColNumList = dtsValidator.NumberList(
#             sep=' ', opt=True, vMin=0, vMax=self.rNColF 
#         )
#         #------------------------------> super()
#         super().__init__(cParent, name=cName)
#         #endregion --------------------------------------------> Initial Setup

#         #region --------------------------------------------------------> Menu
        
#         #endregion -----------------------------------------------------> Menu

#         #region -----------------------------------------------------> Widgets
#         #------------------------------> wx.ScrolledWindow
#         self.wSwLabel  = scrolled.ScrolledPanel(self, size=self.cSSWLabel)
        
#         self.wSwMatrix = scrolled.ScrolledPanel(self, size=self.cSSWMatrix)
#         self.wSwMatrix.SetBackgroundColour('WHITE')
#         #------------------------------> wx.StaticText & wx.TextCtrl
#         #--------------> Experiment design
#         self.rStLabel = []
#         self.rTcLabel = []
#         self.rTcDict = {}
#         for k in range(1, self.cN+1):
#             #------------------------------> tcDict key
#             self.rTcDict[k] = []
#             #------------------------------> wx.StaticText
#             a = wx.StaticText(self.wSwLabel, label=self.cStLabel[k])
#             a.SetToolTip(self.cTTTotalField[k-1])
#             self.rStLabel.append(a)
#             #------------------------------> wx.TextCtrl for the label
#             a = wx.TextCtrl(
#                     self.wSwLabel,
#                     size      = self.cSTotalField,
#                     name      = str(k),
#                     validator = dtsValidator.NumberList(vMin=1, nN=1),
#                 )
#             a.SetHint(self.cHTotalField)
#             self.rTcLabel.append(a)
#         #------------------------------> Control name
#         self.wControlN = dtsWidget.StaticTextCtrl(
#             self.wSwLabel,
#             stLabel   = self.cLControlN,
#             stTooltip = self.cTTControlN,
#             tcHint    = self.cHControlN,
#             tcSize    = self.cSLabel,
#         )
#         #------------------------------> wx.Button
#         self.wBtnCreate = wx.Button(self, label=self.cLSetup)
#         #endregion --------------------------------------------------> Widgets

#         #region -----------------------------------------------------> Tooltip
#         self.wBtnCreate.SetToolTip(
#             'Create the fields to type the column numbers.')
#         #endregion --------------------------------------------------> Tooltip
        
#         #region ------------------------------------------------------> Sizers
#         #------------------------------> Main Sizer
#         self.sSizer = wx.BoxSizer(wx.VERTICAL)
#         #------------------------------> Sizers for self.swLabel
#         self.sSWLabelMain = wx.BoxSizer(wx.VERTICAL)
#         self.sSWLabel = wx.FlexGridSizer(self.cN,2,1,1)

#         self.Add2SWLabel()

#         self.sSWLabelMain.Add(self.sSWLabel, 0, wx.EXPAND|wx.ALL, 5)

#         self.wSwLabel.SetSizer(self.sSWLabelMain)
#         #------------------------------> Sizer with setup btn
#         self.sSetup = wx.BoxSizer(wx.VERTICAL)
#         self.sSetup.Add(self.wBtnCreate, 0, wx.ALIGN_RIGHT|wx.ALL, 5)
#         #------------------------------> Sizer for swMatrix
#         self.sSWMatrix = wx.FlexGridSizer(1,1,1,1)
#         self.wSwMatrix.SetSizer(self.sSWMatrix)
#         #------------------------------> All in Sizer
#         self.sSizer.Add(self.wSwLabel,    0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, 5)
#         self.sSizer.Add(self.sSetup, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
#         self.sSizer.Add(self.wSwMatrix,   1, wx.EXPAND|wx.ALL, 5)
#         self.SetSizer(self.sSizer)
#         #endregion ---------------------------------------------------> Sizers

#         #region --------------------------------------------------------> Bind
#         for k in range(0, self.cN):
#             self.rTcLabel[k].Bind(wx.EVT_KILL_FOCUS, self.OnLabelNumber)

#         self.wBtnCreate.Bind(wx.EVT_BUTTON, self.OnCreate)
#         #endregion -----------------------------------------------------> Bind

#         #region ---------------------------------------------> Window position
        
#         #endregion ------------------------------------------> Window position
#     #---
#     #endregion -----------------------------------------------> Instance setup

#     #region ---------------------------------------------------> Event methods
#     def OnCreate(self, event: Union[wx.CommandEvent, str]) -> bool:
#         """Create the fields in the white panel. Override as needed.
            
#             Parameters
#             ----------
#             event : wx.Event
#                 Information about the event
            
    
#             Returns
#             -------
#             True
#         """
#         return True
#     #---

#     def OnLabelNumber(self, event: Union[wx.Event, str]) -> bool:
#         """Creates fields for names when the total wx.TextCtrl looses focus
    
#             Parameters
#             ----------
#             event : wx.Event
#                 Information about the event
            
    
#             Returns
#             -------
#             True
#         """
#         #region -------------------------------------------------> Check input
#         for k in range(0, self.cN):
#             if self.rTcLabel[k].GetValidator().Validate()[0]:
#                 pass
#             else:
#                 self.rTcLabel[k].SetValue("")
#                 return False
#         #endregion ----------------------------------------------> Check input
        
#         #region ---------------------------------------------------> Variables
#         vals = []
#         for k in self.rTcLabel:
#             vals.append(0 if (x:=k.GetValue()) == '' else int(x))
#         vals.sort(reverse=True)
#         n = vals[0]
#         #endregion ------------------------------------------------> Variables
        
#         #region ------------------------------------------------> Modify sizer
#         if (N := n + 2) != self.sSWLabel.GetCols():
#             self.sSWLabel.SetCols(N)
#         else:
#             pass
#         #endregion ---------------------------------------------> Modify sizer
        
#         #region --------------------------------------> Create/Destroy widgets
#         for k in range(0, self.cN):
#             K = k + 1
#             tN = int(self.rTcLabel[k].GetValue())
#             lN = len(self.rTcDict[k+1])
#             if tN > lN:
#                 #------------------------------> Create new widgets
#                 for knew in range(lN, tN):
#                     KNEW = knew + 1
#                     self.rTcDict[K].append(
#                         wx.TextCtrl(
#                             self.wSwLabel,
#                             size  = self.cSLabel,
#                             value = f"{self.cLabelText[K]}{KNEW}"
#                         )
#                     )
#             else:
#                 #------------------------------> Destroy widget
#                 for knew in range(tN, lN):
#                     #------------------------------> Detach
#                     self.sSWLabel.Detach(self.rTcDict[K][-1])
#                     #------------------------------> Destroy
#                     self.rTcDict[K][-1].Destroy()
#                     #------------------------------> Remove from list
#                     self.rTcDict[K].pop()
#         #endregion -----------------------------------> Create/Destroy widgets

#         #region ------------------------------------------------> Add to sizer
#         self.Add2SWLabel()
#         #endregion ---------------------------------------------> Add to sizer
        
#         #region --------------------------------------------------> Event Skip
#         if isinstance(event, str):
#             pass
#         else:
#             event.Skip()
#         #endregion -----------------------------------------------> Event Skip
        
#         return True
#     #---

#     def OnOK(self) -> bool:
#         """Validate and set the Results - Control Experiments text.
        
#             Returns
#             -------
#             bool
        
#             Notes
#             -----
#             This will set the tcResult in the topParent window to a string like:
#             1 2 3, 4 5 6; '', 7-10; 11-14, '' where commas separate tcfields
#             in the same row and ; separate rows.
#             The following dict will be set in topParent.lbDict
#             {
#                 1             : [values], # First row of labels
#                 N             : [values], # N row of labels
#                 'Control'     : 'Name',
#                 'ControlType' : Control type,
#             }
#             And topParent.controlType will be also set to the corresponding 
#             value
#         """
#         #region -------------------------------------------------> Check input
#         #------------------------------> Variables
#         tcList = []
#         oText  = ''
#         #------------------------------> Individual fields and list of tc
#         for v in self.rTcDictF.values():
#             #--------------> Check values
#             for j in v:
#                 #--------------> Add to lists
#                 tcList.append(j)
#                 oText = f"{oText}{j.GetValue()}, "
#                 #--------------> Check
#                 a, b = j.GetValidator().Validate()
#                 if a:
#                     pass
#                 else:
#                     msg = config.mResCtrlWin.format(b[1])
#                     e = dtsException.ExecutionError(b[2])
#                     dtscore.Notification(
#                         'errorF', msg=msg, parent=self, tException=e)
#                     j.SetFocus(),
#                     return False
#             #--------------> Add row delimiter
#             oText = f"{oText[0:-2]}; "
#         #------------------------------> All cannot be empty
#         a, b = dtsCheck.AllTcEmpty(tcList)
#         if not a:
#             pass
#         else:
#             dtscore.Notification(
#                 'errorF', msg=config.mAllTextFieldEmpty, parent=self)
#             return False
#         #------------------------------> All unique
#         a, b = dtsCheck.UniqueNumbers(tcList, sep=' ')
#         if a:
#             pass
#         else:
#             e = dtsException.InputError(b[2])
#             dtscore.Notification(
#                 'errorF', msg=config.mRepeatColNum, parent=self, tException=e)
#             return False
#         #endregion ----------------------------------------------> Check input
        
#         #region -----------------------------------------------> Set tcResults
#         self.cTopParent.wTcResults.SetValue(f"{oText[0:-2]}")
#         #endregion --------------------------------------------> Set tcResults
        
#         #region ----------------------------------------> Set parent variables
#         #------------------------------> Labels        
#         self.cTopParent.rLbDict = {}
#         for k, v in self.rLbDict.items():
#             self.cTopParent.rLbDict[k] = []
#             for j in v:
#                 self.cTopParent.rLbDict[k].append(j.GetLabel())
                
#         #------------------------------> Control type if needed
#         if self.rPName == 'ProtProfPane' :
#             self.cTopParent.rLbDict['ControlType'] = self.rControlVal
#         else:
#             pass
#         #endregion -------------------------------------> Set parent variables
#         return True
#     #---
#     #endregion ------------------------------------------------> Event methods
    
#     #region --------------------------------------------------> Manage methods
#     def SetInitialState(self) -> bool:
#         """Set the initial state of the panel. This assumes that the needed
#             values in topParent are properly configured.
            
#             Returns
#             -------
#             bool
#         """
#         #region -------------------------------------------------> Check input
#         if (tcFieldsVal := self.cTopParent.wTcResults.GetValue()) != '':
#             pass
#         else:
#             return False
#         #endregion ----------------------------------------------> Check input

#         #region --------------------------------------------------> Add Labels
#         #------------------------------> Check the labels
#         if config.development:
#             for k,v in self.cTopParent.rLbDict.items():
#                 print(str(k)+': '+str(v))
#         else:
#             pass
#         #------------------------------> Set the label numbers
#         for k, v in self.cTopParent.rLbDict.items():
#             if k != 'Control' and k != 'ControlType':
#                 self.rTcLabel[k-1].SetValue(str(len(v)))
#             else:
#                 pass
#         #------------------------------> Create labels fields
#         self.OnLabelNumber('test')
#         #------------------------------> Fill. 2 iterations needed. Improve
#         for k, v in self.cTopParent.rLbDict.items():
#             if k != 'Control' and k != 'ControlType':
#                 for j, t in enumerate(v):
#                     self.rTcDict[k][j].SetValue(t)
#             elif k == 'Control':
#                 self.wControlN.tc.SetValue(v[0])
#             else:
#                 pass
#         #endregion -----------------------------------------------> Add Labels
        
#         #region -------------------------------------------------> Set Control
#         if self.rPName == 'ProtProfPane':
#             #------------------------------> 
#             cT = self.cTopParent.rLbDict['ControlType']
#             self.wCbControl.SetValue(cT)
#             #------------------------------> 
#             if cT == config.oControlTypeProtProf['Ratio']:
#                 self.wControlN.tc.SetEditable(False)
#             else:
#                 pass
#         else:
#             pass
#         #endregion ----------------------------------------------> Set Control
        
#         #region ---------------------------------------------> Create tcFields
#         self.OnCreate('fEvent')
#         #endregion ------------------------------------------> Create tcFields
        
#         #region --------------------------------------------> Add Field Values
#         row = tcFieldsVal.split(";")
#         for k, r in enumerate(row, start=1):
#             fields = r.split(",")
#             for j, f in enumerate(fields):
#                 self.rTcDictF[k][j].SetValue(f)
#         #endregion -----------------------------------------> Add Field Values
        
#         return True
#     #---
    
#     def Add2SWLabel(self) -> bool:
#         """Add the widgets to self.sSWLabel. It assumes sizer already has 
#             the right number of columns and rows. 
            
#             Returns
#             -------
#             bool
#         """
#         #region ------------------------------------------------------> Remove
#         self.sSWLabel.Clear(delete_windows=False)
#         #endregion ---------------------------------------------------> Remove
        
#         #region ---------------------------------------------------------> Add
#         for k in range(0, self.cN):
#             #------------------------------> 
#             K = k + 1
#             #------------------------------> Add conf fields
#             self.sSWLabel.Add(
#                 self.rStLabel[k], 
#                 0, 
#                 wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 
#                 5
#             )
#             self.sSWLabel.Add(
#                 self.rTcLabel[k], 
#                 0, 
#                 wx.ALIGN_RIGHT|wx.EXPAND|wx.ALL, 
#                 5
#             )
#             #------------------------------> Add user fields
#             for tc in self.rTcDict[K]:
#                 self.sSWLabel.Add(
#                     tc, 
#                     0, 
#                     wx.EXPAND|wx.ALL, 
#                     5
#             )
#             #------------------------------> Add empty space
#             n = self.sSWLabel.GetCols()
#             l = len(self.rTcDict[K]) + 2
            
#             if n > l:
#                 for c in range(l, n):
#                     self.sSWLabel.AddSpacer(1)
#             else:
#                 pass
#         #endregion ------------------------------------------------------> Add

#         #region ------------------------------------------------> Setup Sizers
#         #------------------------------> Grow Columns
#         for k in range(2, n):
#             if not self.sSWLabel.IsColGrowable(k):
#                 self.sSWLabel.AddGrowableCol(k, 1)
#             else:
#                 pass
#         #------------------------------> Update sizer
#         self.sSWLabel.Layout()
#         #endregion ---------------------------------------------> Setup Sizers
        
#         #region --------------------------------------------------> Set scroll
#         self.wSwLabel.SetupScrolling()
#         #endregion -----------------------------------------------> Set scroll
        
#         return True
#     #---
#     #endregion -----------------------------------------------> Manage methods
# #---
#endregion -----------------------------------------------------> Base Classes


#region -------------------------------------------------------------> Classes
# # #------------------------------> Panes
# # class ListCtrlSearchPlot(wx.Panel):
# #     """Creates a panel with a wx.ListCtrl and below it a wx.SearchCtrl.

# #         Parameters
# #         ----------
# #         parent: wx.Window
# #             Parent of the panel
# #         colLabel : list of str or None
# #             Name of the columns in the wx.ListCtrl. Default is None
# #         colSize : list of int or None
# #             Size of the columns in the wx.ListCtlr. Default is None
# #         data : list of list
# #             Data for the wx.ListCtrl when in virtual mode. Default is []. 
# #         style : wx.Style
# #             Style of the wx.ListCtrl. Default is wx.LC_REPORT.
# #         tcHint : str
# #             Hint for the wx.SearchCtrl. Default is ''.

# #         Attributes
# #         ----------
# #         name : str
# #             Name of the panel. Default is config.npListCtrlSearchPlot.
# #         lcs : dtsWidget.ListCtrlSearch
# #     """
# #     #region -----------------------------------------------------> Class setup
# #     name = config.npListCtrlSearchPlot
# #     #endregion --------------------------------------------------> Class setup

# #     #region --------------------------------------------------> Instance setup
# #     def __init__(
# #         self, parent: wx.Window, colLabel: Optional[list[str]]=None, 
# #         colSize: Optional[list[int]]=None, data: list[list]=[],
# #         style = wx.LC_REPORT, tcHint: str = ''
# #         ) -> None:
# #         """ """
# #         #region -------------------------------------------------> Check Input
        
# #         #endregion ----------------------------------------------> Check Input

# #         #region -----------------------------------------------> Initial Setup
# #         super().__init__(parent, name=self.name)
# #         #endregion --------------------------------------------> Initial Setup

# #         #region --------------------------------------------------------> Menu
        
# #         #endregion -----------------------------------------------------> Menu

# #         #region -----------------------------------------------------> Widgets
# #         #------------------------------> 
# #         self.lcs = dtsWidget.ListCtrlSearch(
# #             self, 
# #             listT    = 2,
# #             colLabel = colLabel,
# #             colSize  = colSize,
# #             canCut   = False,
# #             canPaste = False,
# #             style    = style,
# #             data     = data,
# #             tcHint   = tcHint,
# #         )
# #         #endregion --------------------------------------------------> Widgets

# #         #region ------------------------------------------------------> Sizers
# #         self.SetSizer(self.lcs.Sizer)
# #         #endregion ---------------------------------------------------> Sizers

# #         #region --------------------------------------------------------> Bind
        
# #         #endregion -----------------------------------------------------> Bind

# #         #region ---------------------------------------------> Window position
        
# #         #endregion ------------------------------------------> Window position
# #     #---
# #     #endregion -----------------------------------------------> Instance setup

# #     #region ---------------------------------------------------> Class methods
    
# #     #endregion ------------------------------------------------> Class methods
# # #---


#------------------------------> Utils
class CorrA(BaseConfPanel):
    """Creates the configuration tab for Correlation Analysis
    
        Parameters
        ----------
        cParent : wx Widget
            Parent of the widgets
        cDataI : dict or None
            Initial data provided by the user in a previous analysis.
            This contains both I and CI dicts e.g. {'I': I, 'CI': CI}

        Attributes
        ----------
        rCheckUserInput : dict
            To check the user input in the right order. 
            See pane.BaseConfPanel.CheckInput for a description of the dict.
        rLCTrlL: list of wx.ListCtrl
            List of wx.ListCtrl to support showing two wx.ListCtrl.
        rLLenLongest : int
            Length of the longest label.     
        rMainData : str
            Name of the file with the correlation coefficient values.
        rMsgError: str
            Error method to show to the user.
            
        See parent class for more attributes.
        
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
                'ImpMethod'  : 'imputation method',
                'CorrMethod' : 'correlation method',
                'oc'         : {
                    'Column' : [selected columns as integers],
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
                        'dfS' : pd.DataFrame with initial data as float and
                                after discarding values by score.
                        'dfT' : pd.DataFrame with transformed data.
                        'dfN' : pd.DataFrame with normalized data.
                        'dfIm': pd.DataFrame with imputed data.
                    }
                    'R' : pd.DataFrame (dict) with the correlation coefficients
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
    cLColAnalysis = config.lStColAnalysis
    #------------------------------> Needed by BaseConfPanel
    cName        = config.npCorrA
    cURL         = f"{config.urlTutorial}/correlation-analysis"
    cSection     = config.nuCorrA
    cTitlePD     = 'Calculating Correlation Coefficients'
    cGaugePD     = 24
    cTTHelp      = config.ttBtnHelp.format(cURL)
    rLLenLongest = len(cLCorrMethod)
    rMainData    = '{}-CorrelationCoefficients-Data-{}.txt'
    #endregion --------------------------------------------------> Class Setup
    
    #region --------------------------------------------------> Instance setup
    def __init__(self, cParent: wx.Window, cDataI: Optional[dict]):
        """"""
        #region -----------------------------------------------> Initial setup
        #------------------------------> Setup attributes in base class 
        super().__init__(cParent)
        #endregion --------------------------------------------> Initial setup
        
        #region -----------------------------------------------------> Widgets
        #------------------------------> dtsWidget.StaticTextComboBox
        self.wCorrMethod = dtsWidget.StaticTextComboBox(self.sbValue, 
            label     = self.cLCorrMethod,
            tooltip   = f'Select the {self.cLCorrMethod}.',
            choices   = list(config.oCorrMethod.values()),
            validator = dtsValidator.IsNotEmpty(),
        )
        #------------------------------> wx.StaticText
        self.wStListI = wx.StaticText(
            self.sbColumn, label=f'Columns in the {self.cLiFile}')
        self.wStListO = wx.StaticText(
            self.sbColumn, label=self.cLColAnalysis)
        #------------------------------> dtscore.ListZebra
        self.wLCtrlI = dtscore.ListZebra(self.sbColumn, 
            colLabel        = self.cLNumName,
            colSize         = self.cSNumName,
            copyFullContent = True,
        )
        self.wLCtrlO = dtscore.ListZebra(self.sbColumn, 
            colLabel        = self.cLNumName,
            colSize         = self.cSNumName,
            canPaste        = True,
            canCut          = True,
            copyFullContent = True,
        )
        self.rLCtrlL = [self.wLCtrlI, self.wLCtrlO]
        #------------------------------> wx.Button
        self.wAddCol = wx.Button(self.sbColumn, label='Add columns')
        #------------------------------> 
        self.wAddCol.SetBitmap(
            wx.ArtProvider.GetBitmap(wx.ART_GO_FORWARD), dir = wx.RIGHT)
        #endregion --------------------------------------------------> Widgets
        
        #region ----------------------------------------------> checkUserInput
        self.rCheckUserInput = {
            self.cLuFile      : [self.wUFile.tc,            config.mFileBad],
            self.cLiFile      : [self.wIFile.tc,            config.mFileBad],
            self.cLTransMethod: [self.wTransMethod.cb,      config.mOptionBad],
            self.cLNormMethod : [self.wNormMethod.cb,       config.mOptionBad],
            self.cLImputation : [self.wImputationMethod.cb, config.mOptionBad],
            self.cLCorrMethod : [self.wCorrMethod.cb,       config.mOptionBad],
        }        
        #endregion -------------------------------------------> checkUserInput
    
        #region -----------------------------------------------------> Tooltip
        self.wStListI.SetToolTip(config.ttLCtrlCopyNoMod)
        self.wStListO.SetToolTip(config.ttLCtrlPasteMod)
        self.wAddCol.SetToolTip(f'Add selected Columns in the Data File to '
            f'the list of Columns to Analyse. New columns will be added after '
            f'the last selected element in Columns to analyse. Duplicate '
            f'columns are discarded.')
        #endregion --------------------------------------------------> Tooltip

        #region ------------------------------------------------------> Sizers
        #------------------------------> Expand Column section
        item = self.sSizer.GetItem(self.sizersbColumn)
        item.Proportion = 1
        item = self.sizersbColumn.GetItem(self.sizersbColumnWid)
        item.Proportion = 1
        #------------------------------> Values
        self.sizersbValueWid.Add(
            1, 1,
            pos    = (0,0),
            flag   = wx.EXPAND|wx.ALL,
            border = 5
        )
        self.sizersbValueWid.Add(
            self.wCorrMethod.st,
            pos    = (0,1),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL,
            border = 5,
        )
        self.sizersbValueWid.Add(
            self.wCorrMethod.cb,
            pos    = (0,2),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL,
            border = 5,
        )
        self.sizersbValueWid.Add(
            1, 1,
            pos    = (0,3),
            flag   = wx.EXPAND|wx.ALL,
            border = 5
        )
        self.sizersbValueWid.AddGrowableCol(0, 1)
        self.sizersbValueWid.AddGrowableCol(3, 1)
        #------------------------------> Columns
        self.sizersbColumnWid.Add(
            self.wStListI,
            pos    = (0,0),
            flag   = wx.ALIGN_CENTRE|wx.ALL,
            border = 5
        )
        self.sizersbColumnWid.Add(
            self.wStListO,
            pos    = (0,2),
            flag   = wx.ALIGN_CENTRE|wx.ALL,
            border = 5
        )
        self.sizersbColumnWid.Add(
            self.wLCtrlI,
            pos    = (1,0),
            flag   = wx.EXPAND|wx.ALL,
            border = 20
        )
        self.sizersbColumnWid.Add(
            self.wAddCol,
            pos    = (1,1),
            flag   = wx.ALIGN_CENTER|wx.ALL,
            border = 20
        )
        self.sizersbColumnWid.Add(
            self.wLCtrlO,
            pos    = (1,2),
            flag   = wx.EXPAND|wx.ALL,
            border = 20
        )
        self.sizersbColumnWid.AddGrowableCol(0, 1)
        self.sizersbColumnWid.AddGrowableCol(2, 1)
        self.sizersbColumnWid.AddGrowableRow(1, 1)
        #------------------------------> Main Sizer
        self.SetSizer(self.sSizer)
        self.sSizer.Fit(self)
        self.SetupScrolling()
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind
        self.wAddCol.Bind(wx.EVT_BUTTON, self.OnAdd)
        #endregion -----------------------------------------------------> Bind
    
        #region --------------------------------------------------------> Test
        if config.development:
            import getpass
            user = getpass.getuser()
            if config.os == "Darwin":
                self.wUFile.tc.SetValue("/Users/" + str(user) + "/TEMP-GUI/BORRAR-UMSAP/umsap-dev.umsap")
                self.wIFile.tc.SetValue("/Users/" + str(user) + "/Dropbox/SOFTWARE-DEVELOPMENT/APPS/UMSAP/LOCAL/DATA/UMSAP-TEST-DATA/TARPROT/tarprot-data-file.txt")
            elif config.os == 'Windows':
                from pathlib import Path
                self.wUFile.tc.SetValue(str(Path('C:/Users/bravo/Desktop/SharedFolders/BORRAR-UMSAP/umsap-dev.umsap')))
                self.wIFile.tc.SetValue(str(Path(f'C:/Users/{user}/Dropbox/SOFTWARE-DEVELOPMENT/APPS/UMSAP/LOCAL/DATA/UMSAP-TEST-DATA/TARPROT/tarprot-data-file.txt')))
            else:
                pass
            self.wId.tc.SetValue("Beta Version Dev")
            self.wTransMethod.cb.SetValue("Log2")
            self.wNormMethod.cb.SetValue("Median")
            self.wImputationMethod.cb.SetValue("Normal Distribution")
            self.wCorrMethod.cb.SetValue("Pearson")
        else:
            pass
        #endregion -----------------------------------------------------> Test
        
        #region -------------------------------------------------------> DataI
        self.SetInitialData(cDataI)
        #endregion ----------------------------------------------------> DataI
    #---
    #endregion -----------------------------------------------> Instance setup
    
    #region ---------------------------------------------------> Event Methods
    def OnAdd(self, event: Union[wx.Event, str]) -> bool:
        """Add columns to analyse using the button.
    
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
    
    #region --------------------------------------------------> Manage Methods
    def SetInitialData(self, dataI: Optional[dict]=None) -> bool:
        """Set initial data
    
            Parameters
            ----------
            dataI : dict or None
                Data to fill all fields and repeat an analysis. See Notes.
    
            Returns
            -------
            True
        """
        if dataI is not None:
            #------------------------------> 
            self.wUFile.tc.SetValue(dataI['CI']['uFile'])
            self.wIFile.tc.SetValue(dataI['I']['Data File'])
            self.wId.tc.SetValue(dataI['CI']['ID'])
            #------------------------------> 
            self.wCeroB.SetValue(dataI['I'][self.cLCeroTreatD])
            self.wTransMethod.cb.SetValue(dataI['CI']['TransMethod'])
            self.wNormMethod.cb.SetValue(dataI['CI']['NormMethod'])
            self.wImputationMethod.cb.SetValue(dataI['CI']['ImpMethod'])
            self.wCorrMethod.cb.SetValue(dataI['CI']['CorrMethod'])
            #------------------------------> 
            if Path(self.wIFile.tc.GetValue()).exists:
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
        else:
            pass
        
        return True
    #---
    #endregion -----------------------------------------------> Manage Methods

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
            self.rMsgError = config.mRowsInLCtrl.format(2, self.cLColAnalysis)
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
        
        col = [int(x) for x in self.wLCtrlO.GetColContent(0)]
        colF = [x for x in range(0, len(col))]
        
        #------------------------------> As given
        self.rDI = {
            self.EqualLenLabel(self.cLiFile) : (
                self.wIFile.tc.GetValue()),
            self.EqualLenLabel(self.cLuFile) : (
                self.wUFile.tc.GetValue()),
            self.EqualLenLabel(self.cLId) : (
                self.wId.tc.GetValue()),
            self.EqualLenLabel(self.cLCeroTreatD) : (
                self.wCeroB.IsChecked()),
            self.EqualLenLabel(self.cLTransMethod) : (
                self.wTransMethod.cb.GetValue()),
            self.EqualLenLabel(self.cLNormMethod) : (
                self.wNormMethod.cb.GetValue()),
            self.EqualLenLabel(self.cLImputation) : (
                self.wImputationMethod.cb.GetValue()),
            self.EqualLenLabel(self.cLCorrMethod) : (
                self.wCorrMethod.cb.GetValue()),
            self.EqualLenLabel('Selected Columns') : col,
        }

        msgStep = self.cLPdPrepare + 'User input, processing'
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        #------------------------------> Dict with all values
        self.rDO = {
            'uFile'      : Path(self.wUFile.tc.GetValue()),
            'iFile'      : Path(self.wIFile.tc.GetValue()),
            'ID'         : self.wId.tc.GetValue(),
            'Cero'       : self.wCeroB.IsChecked(),
            'TransMethod': self.wTransMethod.cb.GetValue(),
            'NormMethod' : self.wNormMethod.cb.GetValue(),
            'ImpMethod'  : self.wImputationMethod.cb.GetValue(),
            'CorrMethod' : self.wCorrMethod.cb.GetValue(),
            'oc'         : {
                'Column'     : col,
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
        
        #region -------------------------------------------------------> Print
        if config.development:
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
    
        return True
    #---

    def RunAnalysis(self):
        """Calculate coefficients"""
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
        """Write output. Override as needed """
        #region --------------------------------------------------> Data Steps
        stepDict = {
            config.fnInitial.format('01', self.rDate): self.dfI,
            config.fnFloat.format('02', self.rDate)  : self.dfS,
            config.fnTrans.format('03', self.rDate)  : self.dfT,
            config.fnNorm.format('04', self.rDate)   : self.dfN,
            config.fnImp.format('05', self.rDate)    : self.dfIm,
            self.rMainData.format('06', self.rDate)  : self.dfR,
        }
        #endregion -----------------------------------------------> Data Steps
        
        #region ---------------------------------------------------> Print
        if config.development:
            print("DataFrames: Initial")
            print(self.dfI.head())
            print(self.dfI.shape)
            print("")
            print("DataFrames: CC")
            print(self.dfR.head())
            print(self.dfR.shape)
        else:
            pass
        #endregion ------------------------------------------------> Print

        return self.WriteOutputData(stepDict)
    #---
    #endregion ------------------------------------------------> Run Analysis
#---


class DataPrep(BaseConfPanel):
    """Data Preparation utility.

        Parameters
        ----------
        cParent: wx.Widget
            Parent of the pane
        cDataI : dict or None
            Initial data provided by the user in a previous analysis.
            This contains both I and CI dicts e.g. {'I': I, 'CI': CI}.

        Attributes
        ----------
        rCheckUserInput : dict
            To check the user input in the right order. 
            See pane.BaseConfPanel.CheckInput for a description of the dict.
        rDI: dict
            Similar to do but with the user given data. Keys are labels in the 
            panel.
        rDO: dict 
        {
            'iFile'      : Path(self.iFile.tc.GetValue()),
            'uFile'      : Path(self.uFile.tc.GetValue()),
            'ID'         : self.id.tc.GetValue(),
            'Cero'       : self.ceroB.IsChecked(),
            'NormMethod' : self.normMethod.cb.GetValue(),
            'TransMethod': self.transMethod.cb.GetValue(),
            'ImpMethod'  : self.imputationMethod.cb.GetValue(),
            'ScoreVal'   : float(self.scoreVal.tc.GetValue()),
            'oc'         : {
                'ScoreCol'   : scoreCol,
                'ExcludeP'   : excludeRow,
                'ColAnalysis': colAnalysis,
                'Column'     : [scoreCol] + excludeRow + colAnalysis,
            },
            'df' : {
                'ScoreCol'   : 0,
                'ExcludeP'   : [x for x in range(1, len(excludeRow)+1)],
                'ResCtrlFlat': resCtrlFlat,
                'ColumnF'    : [0]+resCtrlFlat,
                'ColumnR'    : resCtrlFlat,
            },
        }        
        rLLenLongest: int
            Length of the longest label in the panel.
        
        Notes
        -----
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
    
        The Data Preparation section in output-file.umsap conteins the 
        information about the calculations, e.g

        {
            'Data Preparation : {
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
                    },
                    R : {}
                }
            }
        }
        
        The R entry is empty in this case.
    """
    #region -----------------------------------------------------> Class setup
    #------------------------------> Label
    cLColAnalysis = config.lStColAnalysis
    cLScoreVal    = config.lStScoreVal
    cLScoreCol    = config.lStScoreCol
    cLExcludeRow  = config.lStExcludeRow
    #------------------------------> Tooltips
    cTTScoreVal    = config.ttStScoreVal
    cTTScoreCol    = config.ttStScoreCol
    cTTExcludeRow  = config.ttStExcludeRow
    cTTColAnalysis = ('Columns on which to perform the Data Preparation.\ne.g. '
        '8 10-12')
    #------------------------------> Neeed to Run
    cName        = config.npDataPrep
    cURL         = f'{config.urlTutorial}/data-preparation'
    cTTHelp      = config.ttBtnHelp.format(cURL)
    cSection     = config.nuDataPrep
    cTitlePD     = f"Running {config.nuDataPrep} Analysis"
    cGaugePD     = 27
    rLLenLongest = len(cLColAnalysis)
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, cParent: wx.Window, cDataI: Optional[dict]):
        """ """
        #region -------------------------------------------------> Check Input
        
        #endregion ----------------------------------------------> Check Input

        #region -----------------------------------------------> Initial Setup
        super().__init__(cParent)
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------------> Menu
        
        #endregion -----------------------------------------------------> Menu

        #region -----------------------------------------------------> Widgets
        self.wScoreVal = dtsWidget.StaticTextCtrl(
            self.sbValue,
            stLabel   = self.cLScoreVal,
            stTooltip = self.cTTScoreVal,
            tcSize    = self.cSTc,
            tcHint    = 'e.g. 320',
            validator = dtsValidator.NumberList(numType='float', nN=1),
        )
        
        self.wScore = dtsWidget.StaticTextCtrl(
            self.sbColumn,
            stLabel   = self.cLScoreCol,
            stTooltip = self.cTTScoreCol,
            tcSize    = self.cSTc,
            tcHint    = 'e.g. 39',
            validator = dtsValidator.NumberList(numType='int', nN=1, vMin=0),
        )
        
        self.wExcludeRow = dtsWidget.StaticTextCtrl(
            self.sbColumn,
            stLabel   = self.cLExcludeRow,
            stTooltip = self.cTTExcludeRow,
            tcSize    = self.cSTc,
            tcHint    = 'e.g. 171 172 173',
            validator = dtsValidator.NumberList(
                numType='int', sep=' ', vMin=0, opt=True),
        )
        
        self.wColAnalysis = dtsWidget.StaticTextCtrl(
            self.sbColumn,
            stLabel   = self.cLColAnalysis,
            stTooltip = self.cTTColAnalysis,
            tcSize    = self.cSTc,
            tcHint    = 'e.g. 130-135',
            validator = dtsValidator.NumberList(numType='int', sep=' ', vMin=0),
        )
        #endregion --------------------------------------------------> Widgets
        
        #region ----------------------------------------------> checkUserInput
        self.rCheckUserInput = {
            self.cLuFile      : [self.wUFile.tc,           config.mFileBad],
            self.cLiFile      : [self.wIFile.tc,           config.mFileBad],
            self.cLTransMethod: [self.wTransMethod.cb,     config.mOptionBad],
            self.cLNormMethod : [self.wNormMethod.cb,      config.mOptionBad],
            self.cLImputation : [self.wImputationMethod.cb,config.mOptionBad],
            self.cLScoreVal   : [self.wScoreVal.tc,        config.mOneRealNum],
            self.cLScoreCol   : [self.wScore.tc,           config.mOneZPlusNum],
            self.cLExcludeRow : [self.wExcludeRow.tc,      config.mNZPlusNum],
            self.cLColAnalysis: [self.wColAnalysis.tc,     config.mNZPlusNum],
        }        
        #endregion -------------------------------------------> checkUserInput
        
        #region -----------------------------------------------------> Tooltip
        
        #endregion --------------------------------------------------> Tooltip

        #region ------------------------------------------------------> Sizers
        #------------------------------> Sizer Values
        self.sizersbValueWid.Add(
            1, 1,
            pos    = (0,0),
            flag   = wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sizersbValueWid.Add(
            self.wScoreVal.st,
            pos    = (0,1),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sizersbValueWid.Add(
            self.wScoreVal.tc,
            pos    = (0,2),
            flag   = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sizersbValueWid.Add(
            1, 1,
            pos    = (0,3),
            flag   = wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sizersbValueWid.AddGrowableCol(0, 1)
        self.sizersbValueWid.AddGrowableCol(2, 1)
        self.sizersbValueWid.AddGrowableCol(3, 1)
        #------------------------------> Sizer Columns
        self.sizersbColumnWid.Add(
            1, 1,
            pos    = (0,0),
            flag   = wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sizersbColumnWid.Add(
            self.wScore.st,
            pos    = (0,1),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT,
            border = 5,
        )
        self.sizersbColumnWid.Add(
            self.wScore.tc,
            pos    = (0,2),
            flag   = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sizersbColumnWid.Add(
            self.wExcludeRow.st,
            pos    = (0,3),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT,
            border = 5,
        )
        self.sizersbColumnWid.Add(
            self.wExcludeRow.tc,
            pos    = (0,4),
            flag   = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sizersbColumnWid.Add(
            self.wColAnalysis.st,
            pos    = (1,1),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT,
            border = 5,
            span   = (0,2),
        )
        self.sizersbColumnWid.Add(
            self.wColAnalysis.tc,
            pos    = (2,1),
            flag   = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL,
            border = 5,
            span   = (0,4),
        )
        self.sizersbColumnWid.Add(
            1, 1,
            pos    = (0,5),
            flag   = wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sizersbColumnWid.AddGrowableCol(0,1)
        self.sizersbColumnWid.AddGrowableCol(2,1)
        self.sizersbColumnWid.AddGrowableCol(4,2)
        self.sizersbColumnWid.AddGrowableCol(5,1)
        #------------------------------> Main Sizer
        self.SetSizer(self.sSizer)
        self.sSizer.Fit(self)
        self.SetupScrolling()
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind
        
        #endregion -----------------------------------------------------> Bind

        #region ---------------------------------------------> Window position
        
        #endregion ------------------------------------------> Window position
        
        #region --------------------------------------------------------> Test
        if config.development:
            import getpass
            user = getpass.getuser()
            if config.os == "Darwin":
                self.wUFile.tc.SetValue("/Users/" + str(user) + "/TEMP-GUI/BORRAR-UMSAP/umsap-dev.umsap")
                self.wIFile.tc.SetValue("/Users/" + str(user) + "/Dropbox/SOFTWARE-DEVELOPMENT/APPS/UMSAP/LOCAL/DATA/UMSAP-TEST-DATA/PROTPROF/protprof-data-file.txt")
            elif config.os == 'Windows':
                from pathlib import Path
                # self.iFile.tc.SetValue(str(Path('C:/Users/bravo/Desktop/SharedFolders/BORRAR-UMSAP/PlayDATA/TARPROT/Mod-Enz-Dig-data-ms.txt')))
                # self.oFile.tc.SetValue(str(Path('C:/Users/bravo/Desktop/SharedFolders/BORRAR-UMSAP/PlayDATA/TARPROT')))
            else:
                pass
            self.wScoreVal.tc.SetValue('320')
            self.wId.tc.SetValue('Beta Test Dev')
            self.wTransMethod.cb.SetValue('Log2')
            self.wNormMethod.cb.SetValue('Median')
            self.wImputationMethod.cb.SetValue('Normal Distribution')  
            self.wScore.tc.SetValue('39')     
            self.wExcludeRow.tc.SetValue('171 172 173')
            self.wColAnalysis.tc.SetValue('130-135')
        else:
            pass
        #endregion -----------------------------------------------------> Test
        
        #region -------------------------------------------------------> DataI
        self.SetInitialData(cDataI)
        #endregion ----------------------------------------------------> DataI
    #---
    #endregion -----------------------------------------------> Instance setup

    #------------------------------> Class Methods
    #region --------------------------------------------------> Manage Methods
    def SetInitialData(self, dataI: Optional[dict]=None) -> bool:
        """Set initial data
    
            Parameters
            ----------
            dataI : dict or None
                Data to fill all fields and repeat an analysis. See Notes.
    
            Returns
            -------
            True
        """
        #region -------------------------------------------------> Fill Fields
        if dataI is not None:
            #------------------------------> Files
            self.wUFile.tc.SetValue(dataI['CI']['uFile'])
            self.wIFile.tc.SetValue(dataI['I'][self.cLiFile])
            self.wId.tc.SetValue(dataI['CI']['ID'])
            #------------------------------> Data Preparation
            self.wCeroB.SetValue(dataI['I'][self.cLCeroTreatD])
            self.wTransMethod.cb.SetValue(dataI['I'][self.cLTransMethod])
            self.wNormMethod.cb.SetValue(dataI['I'][self.cLNormMethod])
            self.wImputationMethod.cb.SetValue(dataI['I'][self.cLImputation])
            #------------------------------> Values
            self.wScoreVal.tc.SetValue(dataI['I'][self.cLScoreVal])
            #------------------------------> Columns
            self.wScore.tc.SetValue(dataI['I'][self.cLScoreCol])
            self.wExcludeRow.tc.SetValue(dataI['I'][self.cLExcludeRow])
            self.wColAnalysis.tc.SetValue(dataI['I'][self.cLColAnalysis])
        else:
            pass
        #endregion ----------------------------------------------> Fill Fields
        
        return True
    #---
    #endregion -----------------------------------------------> Manage Methods

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
        
        #region -------------------------------------------> Individual Fields
        
        #endregion ----------------------------------------> Individual Fields
        
        #region ------------------------------------------------> Mixed Fields
        #region ---------------------------------------> Unique Column Numbers
        msgStep = self.cLPdCheck + 'Unique Column Numbers'
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        #------------------------------> 
        l = [self.wScore.tc, self.wExcludeRow.tc, self.wColAnalysis.tc]
        #------------------------------>
        if self.UniqueColumnNumber(l):
            pass
        else:
            return False
        #endregion ------------------------------------> Unique Column Numbers
        #endregion ---------------------------------------------> Mixed Fields
        
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
        #------------------------------> As given
        self.rDI = {
            self.EqualLenLabel(self.cLiFile) : (
                self.wIFile.tc.GetValue()),
            self.EqualLenLabel(self.cLuFile) : (
                self.wUFile.tc.GetValue()),
            self.EqualLenLabel(self.cLId) : (
                self.wId.tc.GetValue()),
            self.EqualLenLabel(self.cLCeroTreatD) : (
                self.wCeroB.IsChecked()),
            self.EqualLenLabel(self.cLTransMethod) : (
                self.wTransMethod.cb.GetValue()),
            self.EqualLenLabel(self.cLNormMethod) : (
                self.wNormMethod.cb.GetValue()),
            self.EqualLenLabel(self.cLImputation) : (
                self.wImputationMethod.cb.GetValue()),
            self.EqualLenLabel(self.cLScoreVal) : (
                self.wScoreVal.tc.GetValue()),
            self.EqualLenLabel(self.cLScoreCol) : (
                self.wScore.tc.GetValue()),
            self.EqualLenLabel(self.cLExcludeRow) : (
                self.wExcludeRow.tc.GetValue()),
            self.EqualLenLabel(self.cLColAnalysis) : (
                self.wColAnalysis.tc.GetValue()),
        }
        #------------------------------> Dict with all values
        #--------------> 
        msgStep = self.cLPdPrepare + 'User input, processing'
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        #--------------> 
        scoreCol   = int(self.wScore.tc.GetValue())
        excludeRow = dtsMethod.Str2ListNumber(
            self.wExcludeRow.tc.GetValue(), sep=' ',
        )
        colAnalysis = dtsMethod.Str2ListNumber(
            self.wColAnalysis.tc.GetValue(), sep=' ',
        )
        resCtrlFlat = [x for x in range(1+len(excludeRow), 1+len(excludeRow)+len(colAnalysis))]
        #--------------> 
        self.rDO  = {
            'iFile'      : Path(self.wIFile.tc.GetValue()),
            'uFile'      : Path(self.wUFile.tc.GetValue()),
            'ID'         : self.wId.tc.GetValue(),
            'Cero'       : self.wCeroB.IsChecked(),
            'NormMethod' : self.wNormMethod.cb.GetValue(),
            'TransMethod': self.wTransMethod.cb.GetValue(),
            'ImpMethod'  : self.wImputationMethod.cb.GetValue(),
            'ScoreVal'   : float(self.wScoreVal.tc.GetValue()),
            'oc'         : {
                'ScoreCol'   : scoreCol,
                'ExcludeP'   : excludeRow,
                'ColAnalysis': colAnalysis,
                'Column'     : [scoreCol] + excludeRow + colAnalysis,
            },
            'df' : {
                'ScoreCol'   : 0,
                'ExcludeP'   : [x for x in range(1, len(excludeRow)+1)],
                'ColumnR'    : resCtrlFlat,
                'ResCtrlFlat': resCtrlFlat,
                'ColumnF'    : [0]+resCtrlFlat,
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

        #region -------------------------------------------------> Print d, do
        if config.development:
            print('')
            print('self.d:')
            for k,v in self.rDI.items():
                print(str(k)+': '+str(v))
            print('')
            print('self.do')
            for k,v in self.rDO.items():
                if k in ['oc', 'df']:
                    print(k)
                    for j,w in v.items():
                        print(f'\t{j}: {w}')
                else:
                    print(str(k)+': '+str(v))
            print('')
        else:
            pass
        #endregion ----------------------------------------------> Print d, do
        
        return True
    #---
    
    def RunAnalysis(self) -> bool:
        """Perform data preparation
        
            Returns
            -------
            bool
        """
        #region --------------------------------------------> Data Preparation
        if self.DataPreparation():
            pass
        else:
            return False
        #endregion -----------------------------------------> Data Preparation
        
        return True
    #---
    
    def WriteOutput(self) -> bool:
        """Write output 
        
            Returns
            -------
            bool
        """
        #region --------------------------------------------------> Data Steps
        stepDict = {
            config.fnInitial.format('01', self.rDate) : self.dfI,
            config.fnFloat.format('02',   self.rDate) : self.dfF,
            config.fnExclude.format('03', self.rDate) : self.dfE,
            config.fnScore.format('04',   self.rDate) : self.dfS,
            config.fnTrans.format('05',   self.rDate) : self.dfT,
            config.fnNorm.format('06',    self.rDate) : self.dfN,
            config.fnImp.format('07',     self.rDate) : self.dfIm,
        }
        #endregion -----------------------------------------------> Data Steps

        return self.WriteOutputData(stepDict)
    #---
    #endregion ------------------------------------------------> Run methods
#---


# #------------------------------> Modules
# class ProtProf(BaseConfModPanel):
#     """Creates the Proteome Profiling configuration tab.

#         Parameters
#         ----------
#         parent: wx.Widget
#             Parent of the pane
#         dataI : dict or None
#             Initial data provided by the user in a previous analysis.
#             This contains both I and CI dicts e.g. {'I': I, 'CI': CI}.

#         Attributes
#         ----------
#         name : str
#             Name of the pane. Default to config.npProtProf.
#         cURL : str
#             URL for the online help.
#         #------------------------------> Configuration
#         cLCorrectP : str
#             Label for the P correction field.
#         cLExcludeProt : str
#             Label for the Exclude Protein field.
#         cLGeneName : str
#             Label for the Gene Name field.
#         cLRawI : str
#             Label for the Intensity field.
#         cLSample : str
#             Label for Sample field.
#         cOCorrectP : list of str
#             Options to correct P values.
#         cORawI : list of str
#             Options for intensity values
#         cOSample : list of str
#             Options for sample relationship.
#         cTTCorrectP : str
#             Tooltip for the correction of P values field.
#         cTTExcludeProt : str
#             Tooltip for the exclude protein field.
#         cTTGeneName : str
#             Tooltip for the Gene name field.
#         cTTHelp : str
#             Tooltip for the help button.
#         cTTRawI : str
#             Tooltip for the intensity field.
#         cTTSample : str
#             Tooltip for the sample field.
#         #------------------------------> To Run Analysis
#         checkUserInput : dict
#             To check the user input in the right order. 
#             See pane.BaseConfPanel.CheckInput for a description of the dict.
#         cColCtrlData : dict
#             Keys are control type and values methods to get the Ctrl and 
#             Data columns for the given condition and relevant point.
#         cGaugePD : int
#             Number of steps for the Progress Dialog.
#         cLLenLongest : int
#             Length of the longest label in the panel.
#         cMainData : str
#             Name of file containing the results in Steps_Data_File.
#         cSection : str
#             Name of the section. Default to config.nmProtProf.
#         cTitlePD : str
#             Name of the Progress Dialog window.
#         do: dict
#             Dictionary with checked user input. Keys are:
#             {
#                 "iFile"      : "Path to input data file",
#                 "uFile"      : "Path to umsap file.",
#                 'ID'         : 'Analysis ID',
#                 "ScoreVal"   : "Score value threshold",
#                 "RawI"       : "Raw intensity or not. Boolean",
#                 "IndS"       : "Independent sampels or not. Boolean,
#                 "Cero"       : Boolean, how to treat cero values,
#                 "TransMethod": "Transformation method",
#                 "NormMethod" : "Normalization method",
#                 "ImpMethod"  : "Imputation method",
#                 "Alpha"      : "Significance level",
#                 "CorrectP"   : "Method to correct P values",
#                 "Cond"       : [List of conditions],
#                 "RP"         : [List of relevent points],
#                 "ControlT"   : "Control type",
#                 "ControlL"   : "Control label",
#                 "oc": {
#                     "DetectedP": "Detected Proteins column. Int",
#                     "GeneName" : "Gene name column. Int",
#                     "ScoreCol" : "Score column. Int",
#                     "ExcludeP" : [List of columns to search for proteins to 
#                                 exclude. List of int],
#                     "ResCtrl": [List of columns containing the control and 
#                                 experiments column numbers],
#                     "Column": [Flat list of all column numbers with the 
#                               following order: Gene Names, Detected Proteins, 
#                               Score, Exclude Proteins, Res & Control]
#                 },
#                 "df": { Column numbers in the pd.df created from the input file.
#                     "DetectedP": 0,
#                     "GeneName" : 1,
#                     "ScoreCol" : 2,
#                     "ExcludeP" : [list of int],
#                     "ResCtrl": [],
#                     "ResCtrlFlat": [ResCtrl as a flat list],
#                     "ColumnR : [Columns with the results] 
#                     "ColumnF": [Columns that must contain only float numbers]
#                 }
#             },    
#         d: dict
#             Dictionary with the user input. Keys are labels in the panel plus:
#             {
#                 config.lStProtProfCond          : [list of conditions],
#                 config.lStProtProfRP            : [list of relevant points],
#                 f"Control {config.lStCtrlType}" : "Control Type",
#                 f"Control {config.lStCtrlName}" : "Control Name",
#             }
            
#         See Parent classes for more aatributes.
        
#         Notes
#         -----
#         Running the analysis results in the creation of:
        
#         - Parent Folder/
#             - Input_Data_Files/
#             - Steps_Data_Files/20210324-165609-Proteome-Profiling/
#             - output-file.umsap
        
#         The Input_Data_Files folder contains the original data files. These are 
#         needed for data visualization, running analysis again with different 
#         parameters, etc.
#         The Steps_Data_Files/Date-Section folder contains regular csv files with 
#         the step by step data.
    
#         The Proteome Profiling section in output-file.umsap conteins the 
#         information about the calculations, e.g

#         {
#             'Proteome-Profiling : {
#                 '20210324-165609': {
#                     'V' : config.dictVersion,
#                     'I' : self.d,
#                     'CI': self.do,
#                     'DP': {
#                         'dfS' : pd.DataFrame with initial data as float and
#                                 after discarding values by score.
#                         'dfT' : pd.DataFrame with transformed data.
#                         'dfN' : pd.DataFrame with normalized data.
#                         'dfIm': pd.DataFrame with imputed data.
#                     }
#                     'R' : pd.DataFrame (dict) with the calculation results.
#                 }
#             }
#         }
        
#         The result data frame has the following structure:
        
#         Gene Protein Score C1 ..... CN
#         Gene Protein Score RP1 ..... RPN
#         Gene Protein Score aveC stdC ave std P Pc FC CI FCz
        
#         where all FC related values are for log2FC
#     """
#     #region -----------------------------------------------------> Class setup
#     cName = config.npProtProf
#     #endregion --------------------------------------------------> Class setup

#     #region --------------------------------------------------> Instance setup
#     def __init__(self, cParent, cDataI: Optional[dict]):
#         """ """
#         #region -------------------------------------------------> Check Input
        
#         #endregion ----------------------------------------------> Check Input

#         #region -----------------------------------------------> Initial Setup
#         #------------------------------> Needed by BaseConfPanel
#         self.cURL         = config.urlProtProf
#         self.cSection     = config.nmProtProf
#         self.cTitlePD     = f"Running {config.nmProtProf} Analysis"
#         self.cGaugePD     = 36
#         self.rLLenLongest = len(config.lStResultCtrl)
#         #------------------------------> Optional configuration
#         self.cTTHelp = config.ttBtnHelp.format(config.urlProtProf)
#         #------------------------------> Base attributes and setup
#         super().__init__(cParent)
#         #------------------------------> Needed to Run
#         self.rMainData  = config.fnMainDataProtProf
#         #------------------------------> Dict with methods
#         # self.cColCtrlData = {
#         #     config.oControlTypeProtProf['OC']   : self.ColCtrlData_OC,
#         #     config.oControlTypeProtProf['OCC']  : self.ColCtrlData_OCC,
#         #     config.oControlTypeProtProf['OCR']  : self.ColCtrlData_OCR,
#         #     config.oControlTypeProtProf['Ratio']: self.ColCtrlData_Ratio,
#         # }
#         #endregion --------------------------------------------> Initial Setup

#         #region --------------------------------------------------------> Menu
        
#         #endregion -----------------------------------------------------> Menu

#         #region -----------------------------------------------------> Widgets
#         #------------------------------> Values
#         self.wCorrectP = dtsWidget.StaticTextComboBox(
#             self.sbValue,
#             label     = config.lCbCorrectP,
#             choices   = list(config.oCorrectP.keys()),
#             tooltip   = config.ttStPCorrection,
#             validator = dtsValidator.IsNotEmpty(),
#         )
        
#         self.wSample = dtsWidget.StaticTextComboBox(
#             self.sbValue,
#             label     = config.lCbSample,
#             choices   = list(config.oSamples.keys()),
#             tooltip   = config.ttStSample,
#             validator = dtsValidator.IsNotEmpty(),
#         )
        
#         self.wRawI = dtsWidget.StaticTextComboBox(
#             self.sbValue,
#             label     = config.lCbIntensity,
#             choices   = list(config.oIntensities.values()),
#             tooltip   = config.ttStRawI,
#             validator = dtsValidator.IsNotEmpty(),
#         )
#         #------------------------------> Columns
#         self.wGeneName = dtsWidget.StaticTextCtrl(
#             self.sbColumn,
#             stLabel   = config.lStGeneName,
#             stTooltip = config.ttStGenName,
#             tcSize    = self.cSTc,
#             tcHint    = 'e.g. 6',
#             validator = dtsValidator.NumberList(numType='int', nN=1, vMin=0),
#         )
        
#         self.wExcludeProt = dtsWidget.StaticTextCtrl(
#             self.sbColumn,
#             stLabel   = config.lStExcludeProt,
#             stTooltip = config.ttStExcludeProt,
#             tcSize    = self.cSTc,
#             tcHint    = 'e.g. 171-173',
#             validator = dtsValidator.NumberList(
#                 numType='int', sep=' ', vMin=0, opt=True),
#         )
#         #endregion --------------------------------------------------> Widgets

#         #region ----------------------------------------------> checkUserInput
#         self.checkUserInput = {
#             self.cLuFile       : [self.wUFile.tc,           config.mFileBad],
#             self.cLiFile       : [self.wIFile.tc,           config.mFileBad],
#             self.cLTransMethod : [self.wTransMethod.cb,     config.mOptionBad],
#             self.cLNormMethod  : [self.wNormMethod.cb,      config.mOptionBad],
#             self.cLImputation  : [self.wImputationMethod.cb,config.mOptionBad],
#             self.cLScoreVal    : [self.wScoreVal.tc,        config.mOneRealNum],
#             config.lCbSample   : [self.wSample.cb,          config.mOptionBad],
#             config.lCbIntensity: [self.wRawI.cb,            config.mOptionBad],
#             self.cLAlpha       : [self.wAlpha.tc,           config.mOne01Num],
#             config.lCbCorrectP : [self.wCorrectP.cb,        config.mOptionBad],
#             self.cLDetectedProt: [self.wDetectedProt.tc,   config.mOneZPlusNum],
#             config.lStGeneName : [self.wGeneName.tc,       config.mOneZPlusNum],
#             self.cLScoreCol    : [self.wScore.tc,          config.mOneZPlusNum],
#             config.lStExcludeProt: [self.wExcludeProt.tc,  config.mNZPlusNum],
#             self.cLResControl  : [self.wTcResults,         config.mResCtrl]
#         }        
#         #endregion -------------------------------------------> checkUserInput

#         #region -----------------------------------------------------> Tooltip
        
#         #endregion --------------------------------------------------> Tooltip
        
#         #region ------------------------------------------------------> Sizers
#         #------------------------------> Sizer Values
#         self.sizersbValueWid.Add(
#             1, 1,
#             pos    = (0,0),
#             flag   = wx.EXPAND|wx.ALL,
#             border = 5,
#             span   = (2, 0),
#         )
#         self.sizersbValueWid.Add(
#             self.wScoreVal.st,
#             pos    = (0,1),
#             flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
#             border = 5,
#         )
#         self.sizersbValueWid.Add(
#             self.wScoreVal.tc,
#             pos    = (0,2),
#             flag   = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL,
#             border = 5,
#         )
#         self.sizersbValueWid.Add(
#             self.wAlpha.st,
#             pos    = (0,3),
#             flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
#             border = 5,
#         )
#         self.sizersbValueWid.Add(
#             self.wAlpha.tc,
#             pos    = (0,4),
#             flag   = wx.EXPAND|wx.ALL,
#             border = 5,
#         )
#         self.sizersbValueWid.Add(
#             self.wSample.st,
#             pos    = (1,1),
#             flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
#             border = 5,
#         )
#         self.sizersbValueWid.Add(
#             self.wSample.cb,
#             pos    = (1,2),
#             flag   = wx.EXPAND|wx.ALL,
#             border = 5,
#         )
#         self.sizersbValueWid.Add(
#             self.wCorrectP.st,
#             pos    = (1,3),
#             flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
#             border = 5,
#         )
#         self.sizersbValueWid.Add(
#             self.wCorrectP.cb,
#             pos    = (1,4),
#             flag   = wx.EXPAND|wx.ALL,
#             border = 5,
#         )
#         self.sizersbValueWid.Add(
#             self.wRawI.st,
#             pos    = (2,1),
#             flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
#             border = 5,
#         )
#         self.sizersbValueWid.Add(
#             self.wRawI.cb,
#             pos    = (2,2),
#             flag   = wx.EXPAND|wx.ALL,
#             border = 5,
#         )
#         self.sizersbValueWid.Add(
#             1, 1,
#             pos    = (0,5),
#             flag   = wx.EXPAND|wx.ALL,
#             border = 5,
#             span   = (2, 0),
#         )
#         self.sizersbValueWid.AddGrowableCol(0, 1)
#         self.sizersbValueWid.AddGrowableCol(5, 1)
#         #------------------------------> Sizer Columns
#         self.sizersbColumnWid.Add(
#             self.wDetectedProt.st,
#             pos    = (0,0),
#             flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
#             border = 5,
#         )
#         self.sizersbColumnWid.Add(
#             self.wDetectedProt.tc,
#             pos    = (0,1),
#             flag   = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL,
#             border = 5,
#         )
#         self.sizersbColumnWid.Add(
#             self.wGeneName.st,
#             pos    = (0,2),
#             flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
#             border = 5,
#         )
#         self.sizersbColumnWid.Add(
#             self.wGeneName.tc,
#             pos    = (0,3),
#             flag   = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL,
#             border = 5,
#         )
#         self.sizersbColumnWid.Add(
#             self.wScore.st,
#             pos    = (0,4),
#             flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
#             border = 5,
#         )
#         self.sizersbColumnWid.Add(
#             self.wScore.tc,
#             pos    = (0,5),
#             flag   = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL,
#             border = 5,
#         )
#         self.sizersbColumnWid.Add(
#             self.wExcludeProt.st,
#             pos    = (1,0),
#             flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
#             border = 5,
#         )
#         self.sizersbColumnWid.Add(
#             self.wExcludeProt.tc,
#             pos    = (1,1),
#             flag   = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL,
#             border = 5,
#             span   = (0, 5),
#         )
#         self.sizersbColumnWid.Add(
#             self.sRes,
#             pos    = (2,0),
#             flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND,
#             border = 0,
#             span   = (0,6),
#         )
#         self.sizersbColumnWid.AddGrowableCol(1,1)
#         self.sizersbColumnWid.AddGrowableCol(3,1)
#         self.sizersbColumnWid.AddGrowableCol(5,1)
#         #------------------------------> Main Sizer
#         self.SetSizer(self.sSizer)
#         self.sSizer.Fit(self)
#         self.SetupScrolling()
#         #endregion ---------------------------------------------------> Sizers

#         #region --------------------------------------------------------> Bind
        
#         #endregion -----------------------------------------------------> Bind

#         #region --------------------------------------------------------> Test
#         if config.development:
#             import getpass
#             user = getpass.getuser()
#             if config.os == "Darwin":
#                 self.wUFile.tc.SetValue("/Users/" + str(user) + "/TEMP-GUI/BORRAR-UMSAP/umsap-dev.umsap")
#                 self.wIFile.tc.SetValue("/Users/" + str(user) + "/Dropbox/SOFTWARE-DEVELOPMENT/APPS/UMSAP/LOCAL/DATA/UMSAP-TEST-DATA/PROTPROF/protprof-data-file.txt")
#             elif config.os == 'Windows':
#                 from pathlib import Path
#                 # self.iFile.tc.SetValue(str(Path('C:/Users/bravo/Desktop/SharedFolders/BORRAR-UMSAP/PlayDATA/TARPROT/Mod-Enz-Dig-data-ms.txt')))
#                 # self.oFile.tc.SetValue(str(Path('C:/Users/bravo/Desktop/SharedFolders/BORRAR-UMSAP/PlayDATA/TARPROT')))
#             else:
#                 pass
#             self.wScoreVal.tc.SetValue('320')
#             self.wId.tc.SetValue('Beta Test Dev')
#             self.wTransMethod.cb.SetValue('Log2')
#             self.wNormMethod.cb.SetValue('Median')
#             self.wImputationMethod.cb.SetValue('Normal Distribution')
#             self.wAlpha.tc.SetValue('0.05')
#             self.wSample.cb.SetValue('Independent Samples')
#             self.wRawI.cb.SetValue('Raw Intensities')
#             self.wCorrectP.cb.SetValue('Benjamini - Hochberg')
#             self.wDetectedProt.tc.SetValue('0')
#             self.wGeneName.tc.SetValue('6')   
#             self.wScore.tc.SetValue('39')
#             self.wExcludeProt.tc.SetValue('171 172 173')
#             #------------------------------> 
#             #--> One Control per Column, 2 Cond and 2 TP
#             # self.wTcResults.SetValue('105 115 125, 130 131 132; 106 116 126, 101 111 121; 108 118 128, 103 113 123')
#             # self.rLbDict = {
#             #     1            : ['C1', 'C2'],
#             #     2            : ['RP1', 'RP2'],
#             #     'Control'    : ['TheControl'],
#             #     'ControlType': 'One Control per Column',
#             # }
#             #--> One Control per Row, 1 Cond and 2 TP
#             self.wTcResults.SetValue('105 115 125, 106 116 126, 101 111 121')
#             self.rLbDict = {
#                 1            : ['DMSO'],
#                 2            : ['30min', '60min'],
#                 'Control'    : ['MyControl'],
#                 'ControlType': 'One Control per Row',
#             }
#             #--> One Control 2 Cond and 2 TP
#             # self.wTcResults.SetValue('105 115 125; 106 116 126, 101 111 121; 108 118 128, 103 113 123')
#             # self.rLbDict = {
#             #     1            : ['C1', 'C2'],
#             #     2            : ['RP1', 'RP2'],
#             #     'Control'    : ['1Control'],
#             #     'ControlType': 'One Control',
#             # }
#             #--> Ratio 2 Cond and 2 TP
#             # self.wTcResults.SetValue('106 116 126, 101 111 121; 108 118 128, 103 113 123')
#             # self.rLbDict = {
#             #     1            : ['C1', 'C2'],
#             #     2            : ['RP1', 'RP2'],
#             #     'Control'    : ['1Control'],
#             #     'ControlType': 'Ratio of Intensities',
#             # }
#         else:
#             pass
#         #endregion -----------------------------------------------------> Test
        
#         #region -------------------------------------------------------> DataI
#         self.SetInitialData(cDataI)
#         #endregion ----------------------------------------------------> DataI
#     #---
#     #endregion -----------------------------------------------> Instance setup

#     #region ---------------------------------------------------> Manage methods
#     def SetInitialData(self, dataI: Optional[dict]=None) -> bool:
#         """Set initial data
    
#             Parameters
#             ----------
#             dataI : dict or None
#                 Data to fill all fields and repeat an analysis. See Notes.
    
#             Returns
#             -------
#             True
#         """
#         #region -------------------------------------------------> Fill Fields
#         if dataI is not None:
#             #------------------------------> Files
#             self.wUFile.tc.SetValue(dataI['CI']['uFile'])
#             self.wIFile.tc.SetValue(dataI['I'][self.cLiFile])
#             self.wId.tc.SetValue(dataI['CI']['ID'])
#             #------------------------------> Data Preparation
#             self.wCeroB.SetValue(dataI['I'][self.cLCeroTreatD])
#             self.wTransMethod.cb.SetValue(dataI['I'][self.cLTransMethod])
#             self.wNormMethod.cb.SetValue(dataI['I'][self.cLNormMethod])
#             self.wImputationMethod.cb.SetValue(dataI['I'][self.cLImputation])
#             #------------------------------> Values
#             self.wScoreVal.tc.SetValue(dataI['I'][self.cLScoreVal])
#             self.wSample.cb.SetValue(dataI['I'][config.lCbSample])
#             self.wRawI.cb.SetValue(dataI['I'][config.lCbIntensity])
#             self.wAlpha.tc.SetValue(dataI['I'][self.cLAlpha])
#             self.wCorrectP.cb.SetValue(dataI['I'][config.lCbCorrectP])
#             #------------------------------> Columns
#             self.wDetectedProt.tc.SetValue(dataI['I'][self.cLDetectedProt])
#             self.wGeneName.tc.SetValue(dataI['I'][config.lStGeneName])
#             self.wScore.tc.SetValue(dataI['I'][self.cLScoreCol])
#             self.wExcludeProt.tc.SetValue(dataI['I'][config.lStExcludeProt])
#             self.wTcResults.SetValue(dataI['I'][self.cLResControl])
#             self.lbDict[1] = dataI['I'][config.lStProtProfCond]
#             self.lbDict[2] = dataI['I'][config.lStProtProfRP]
#             self.lbDict['ControlType'] = dataI['I'][f'Control {config.lStCtrlType}']
#             self.lbDict['Control'] = dataI['I'][f"Control {config.lStCtrlName}"]
#         else:
#             pass
#         #endregion ----------------------------------------------> Fill Fields
        
#         return True
#     #---
#     #endregion ------------------------------------------------> Manage methods


#     #region ---------------------------------------------------> Run methods
#     # def CheckInput(self) -> bool:
#     #     """Check user input

#     #         Returns
#     #         -------
#     #         bool
#     #     """
#     #     #region -------------------------------------------------------> Super
#     #     if super().CheckInput():
#     #         pass
#     #     else:
#     #         return False
#     #     #endregion ----------------------------------------------------> Super
        
#     #     #region ---------------------------------------------------------> Msg
#     #     msgPrefix = config.lPdCheck
#     #     #endregion ------------------------------------------------------> Msg
        
#     #     #region -------------------------------------------> Individual Fields
        
#     #     #endregion ----------------------------------------> Individual Fields
        
#     #     #region ------------------------------------------------> Mixed Fields
#     #     #region --------------------------------> Raw or Ration of Intensities
#     #     msgStep = msgPrefix + 'Intensity Options'
#     #     wx.CallAfter(self.rDlg.UpdateStG, msgStep)
#     #     #------------------------------> 
#     #     a = self.wRawI.cb.GetValue()
#     #     b = self.lbDict['ControlType']
#     #     if a == b == config.oIntensities['RatioI']:
#     #         pass
#     #     elif a != config.oIntensities['RatioI'] and b != config.oIntensities['RatioI']:
#     #         pass
#     #     else:
#     #         self.msgError = (
#     #             f'The values for {self.cLRawI} ({self.rawI.cb.GetValue()}) '
#     #             f'and Control Type ({self.lbDict["ControlType"]}) are '
#     #             f'incompatible with each other.'
#     #         )
#     #         return False
#     #     #endregion -----------------------------> Raw or Ration of Intensities
        
#     #     #region ---------------------------------------> Unique Column Numbers
#     #     msgStep = msgPrefix + 'Unique Column Numbers'
#     #     wx.CallAfter(self.dlg.UpdateStG, msgStep)
#     #     #------------------------------> 
#     #     l = [self.detectedProt.tc, self.geneName.tc, self.score.tc, 
#     #         self.excludeProt.tc, self.tcResults]
#     #     #------------------------------> 
#     #     if self.UniqueColumnNumber(l):
#     #         pass
#     #     else:
#     #         return False
#     #     #endregion ------------------------------------> Unique Column Numbers
#     #     #endregion ---------------------------------------------> Mixed Fields
        
#     #     return True
#     # #---
    
# #     def PrepareRun(self) -> bool:
# #         """Set variable and prepare data for analysis.
        
# #             Returns
# #             -------
# #             bool
# #         """
# #         #region ---------------------------------------------------------> Msg
# #         msgPrefix = config.lPdPrepare
# #         #endregion ------------------------------------------------------> Msg

# #         #region -------------------------------------------------------> Input
# #         msgStep = msgPrefix + 'User input, reading'
# #         wx.CallAfter(self.dlg.UpdateStG, msgStep)
# #         #------------------------------> As given
# #         self.d = {
# #             self.EqualLenLabel(self.cLiFile) : (
# #                 self.iFile.tc.GetValue()),
# #             self.EqualLenLabel(self.cLuFile) : (
# #                 self.uFile.tc.GetValue()),
# #             self.EqualLenLabel(self.cLId) : (
# #                 self.id.tc.GetValue()),
# #             self.EqualLenLabel(self.cLCeroTreatD) : (
# #                 self.ceroB.IsChecked()),
# #             self.EqualLenLabel(self.cLScoreVal) : (
# #                 self.scoreVal.tc.GetValue()),
# #             self.EqualLenLabel(self.cLSample) : (
# #                 self.sample.cb.GetValue()),
# #             self.EqualLenLabel(self.cLRawI) : (
# #                 self.rawI.cb.GetValue()),
# #             self.EqualLenLabel(self.cLTransMethod) : (
# #                 self.transMethod.cb.GetValue()),
# #             self.EqualLenLabel(self.cLNormMethod) : (
# #                 self.normMethod.cb.GetValue()),
# #             self.EqualLenLabel(self.cLImputation) : (
# #                 self.imputationMethod.cb.GetValue()),
# #             self.EqualLenLabel(self.cLAlpha) : (
# #                 self.alpha.tc.GetValue()),
# #             self.EqualLenLabel(self.cLCorrectP) : (
# #                 self.correctP.cb.GetValue()),
# #             self.EqualLenLabel(self.cLDetectedProt) : (
# #                 self.detectedProt.tc.GetValue()),
# #             self.EqualLenLabel(self.cLGeneName) : (
# #                 self.geneName.tc.GetValue()),
# #             self.EqualLenLabel(self.cLScoreCol) : (
# #                 self.score.tc.GetValue()),
# #             self.EqualLenLabel(self.cLExcludeProt) : (
# #                 self.excludeProt.tc.GetValue()),
# #             self.EqualLenLabel(config.lStProtProfCond) : (
# #                 self.lbDict[1]),
# #             self.EqualLenLabel(config.lStProtProfRP) : (
# #                 self.lbDict[2]),
# #             self.EqualLenLabel(f"Control {config.lStCtrlType}") : (
# #                 self.lbDict['ControlType']),
# #             self.EqualLenLabel(f"Control {config.lStCtrlName}") : (
# #                 self.lbDict['Control']),
# #             self.EqualLenLabel(self.cLResControl): (
# #                 self.tcResults.GetValue()),
# #         }
# #         #------------------------------> Dict with all values
# #         #--------------> 
# #         msgStep = msgPrefix + 'User input, processing'
# #         wx.CallAfter(self.dlg.UpdateStG, msgStep)
# #         #--------------> 
# #         detectedProt = int(self.detectedProt.tc.GetValue())
# #         geneName     = int(self.geneName.tc.GetValue())
# #         scoreCol     = int(self.score.tc.GetValue())
# #         excludeProt  = dtsMethod.Str2ListNumber(
# #             self.excludeProt.tc.GetValue(), sep=' ',
# #         )
# #         resctrl       = dmethod.ResControl2ListNumber(self.tcResults.GetValue())
# #         resctrlFlat   = dmethod.ResControl2Flat(resctrl)
# #         resctrlDF     = dmethod.ResControl2DF(resctrl, 2+len(excludeProt)+1)
# #         resctrlDFFlat = dmethod.ResControl2Flat(resctrlDF)
# #         #--------------> 
# #         self.do  = {
# #             'iFile'      : Path(self.iFile.tc.GetValue()),
# #             'uFile'      : Path(self.uFile.tc.GetValue()),
# #             'ID'         : self.id.tc.GetValue(),
# #             'ScoreVal'   : float(self.scoreVal.tc.GetValue()),
# #             'RawI'       : True if self.rawI.cb.GetValue() == config.oIntensities['RawI'] else False,
# #             'IndS'       : True if self.sample.cb.GetValue() == config.oSamples['Independent Samples'] else False,
# #             'Cero'       : self.ceroB.IsChecked(),
# #             'NormMethod' : self.normMethod.cb.GetValue(),
# #             'TransMethod': self.transMethod.cb.GetValue(),
# #             'ImpMethod'  : self.imputationMethod.cb.GetValue(),
# #             'Alpha'      : float(self.alpha.tc.GetValue()),
# #             'CorrectP'   : self.correctP.cb.GetValue(),
# #             'Cond'       : self.lbDict[1],
# #             'RP'         : self.lbDict[2],
# #             'ControlT'   : self.lbDict['ControlType'],
# #             'ControlL'   : self.lbDict['Control'],
# #             'oc'         : {
# #                 'DetectedP' : detectedProt,
# #                 'GeneName'  : geneName,
# #                 'ScoreCol'  : scoreCol,
# #                 'ExcludeP'  : excludeProt,
# #                 'ResCtrl'   : resctrl,
# #                 'Column'    : (
# #                     [geneName, detectedProt, scoreCol] 
# #                     + excludeProt 
# #                     + resctrlFlat
# #                 ),
# #             },
# #             'df' : {
# #                 'DetectedP'  : 0,
# #                 'GeneName'   : 1,
# #                 'ScoreCol'   : 2,
# #                 'ExcludeP'   : [2+x for x in range(1, len(excludeProt)+1)],
# #                 'ResCtrl'    : resctrlDF,
# #                 'ResCtrlFlat': resctrlDFFlat,
# #                 'ColumnR'    : resctrlDFFlat,
# #                 'ColumnF'    : [2] + resctrlDFFlat,
# #             },
# #         }
# #         #------------------------------> File base name
# #         self.oFolder = self.do['uFile'].parent
# #         #------------------------------> Date
# #         self.date = dtsMethod.StrNow()
# #         #------------------------------> DateID
# #         self.dateID = f'{self.date} - {self.do["ID"]}'
# #         #endregion ----------------------------------------------------> Input

# #         #region -------------------------------------------------> Print d, do
# #         if config.development:
# #             print('')
# #             print('self.d:')
# #             for k,v in self.d.items():
# #                 print(str(k)+': '+str(v))
# #             print('')
# #             print('self.do')
# #             for k,v in self.do.items():
# #                 if k in ['oc', 'df']:
# #                     print(k)
# #                     for j,w in self.do[k].items():
# #                         print(f'\t{j}: {w}')
# #                 else:
# #                     print(str(k)+': '+str(v))
# #             print('')
# #         else:
# #             pass
# #         #endregion ----------------------------------------------> Print d, do
        
# #         return True
# #     #---
    
# #     def RunAnalysis(self) -> bool:
# #         """Calculate proteome profiling data
        
# #             Returns
# #             -------
# #             bool
# #         """
# #         #region ---------------------------------------------------------> Msg
# #         msgPrefix = config.lPdRun
# #         #endregion ------------------------------------------------------> Msg
        
# #          #region --------------------------------------------> Data Preparation
# #         if self.DataPreparation():
# #             pass
# #         else:
# #             return False
# #         #endregion -----------------------------------------> Data Preparation
        
# #         #region --------------------------------------------------------> Sort
# #         self.dfIm.sort_values(
# #             by=list(self.dfIm.columns[0:2]), inplace=True, ignore_index=True,
# #         )
# #         #endregion -----------------------------------------------------> Sort
        
# #         #region ----------------------------------------------------> Empty DF
# #         #------------------------------> Msg
# #         msgStep = (
# #             f'{msgPrefix}'
# #             f'Calculating output data - Creating empty dataframe'
# #         )  
# #         wx.CallAfter(self.dlg.UpdateStG, msgStep)
# #         #------------------------------> 
# #         self.dfR = self.EmptyDFR()
        
# #         if config.development:
# #             print('self.dfR.shape: ', self.dfR.shape)
# #             print(self.dfR.head())
# #             print('')
# #         #endregion -------------------------------------------------> Empty DF
        
# #         #region --------------------------------------------> Calculate values
# #         #------------------------------> Msg
# #         msgStep = (
# #             f'{msgPrefix}'
# #             f'Calculating output data'
# #         )  
# #         wx.CallAfter(self.dlg.UpdateStG, msgStep)
# #         #------------------------------> Calculate data
# #         for c, cN in enumerate(self.do['Cond']):
# #             for t, tN in enumerate(self.do['RP']):
# #                 #------------------------------> Message
# #                 msgStep = (
# #                     f'{msgPrefix}'
# #                     f'Calculating output data for {cN} - {tN}'
# #                 )  
# #                 wx.CallAfter(self.dlg.UpdateSt, msgStep)
# #                 #------------------------------> Control & Data Column
# #                 colC, colD = self.cColCtrlData[self.do['ControlT']](c, t)
# #                 #------------------------------> Calculate data
# #                 try:
# #                     self.CalcOutData(cN, tN, colC, colD)
# #                 except Exception as e:
# #                     self.msgError = (
# #                         f'Calculation of the Proteome Profiling data for '
# #                         f'point {cN} - {tN} failed.'
# #                     )
# #                     self.tException = e
# #                     return False
                
# #         if config.development:
# #             print('self.dfR.shape: ', self.dfR.shape)
# #             print(self.dfR.head())
# #             print('')
# #         #endregion -----------------------------------------> Calculate values
        
# #         return True
# #     #---

# #     def EmptyDFR(self) -> 'pd.DataFrame':
# #         """Creates the empty data frame for the output. This data frame contains
# #             the values for Gene, Protein and Score
    
# #             Returns
# #             -------
# #             pd.DataFrame
# #         """
# #         #region -------------------------------------------------------> Index
# #         #------------------------------> First Three Columns
# #         aL = config.dfcolProtprofFirstThree
# #         bL = config.dfcolProtprofFirstThree
# #         cL = config.dfcolProtprofFirstThree
# #         #------------------------------> Columns per Point
# #         n = len(config.dfcolProtprofCLevel)
# #         #------------------------------> Other columns
# #         for c in self.do['Cond']:
# #             for t in self.do['RP']:
# #                 aL = aL + n*[c]
# #                 bL = bL + n*[t]
# #                 cL = cL + config.dfcolProtprofCLevel
# #         #------------------------------> 
# #         idx = pd.MultiIndex.from_arrays([aL[:], bL[:], cL[:]])
# #         #endregion ----------------------------------------------------> Index
        
# #         #region ----------------------------------------------------> Empty DF
# #         df = pd.DataFrame(
# #             np.nan, columns=idx, index=range(self.dfIm.shape[0]),
# #         )
# #         #endregion -------------------------------------------------> Empty DF
        
# #         #region -----------------------------------------> First Three Columns
# #         df[(aL[0], bL[0], cL[0])] = self.dfIm.iloc[:,0]
# #         df[(aL[1], bL[1], cL[1])] = self.dfIm.iloc[:,1]
# #         df[(aL[2], bL[2], cL[2])] = self.dfIm.iloc[:,2]
# #         #endregion --------------------------------------> First Three Columns
        
# #         return df
# #     #---
    
# #     def ColCtrlData_OC(self, c:int, t:int) -> list[list[int]]:
# #         """Get the Ctrl and Data columns for the given condition and relevant
# #             point when Control Type is: One Control
    
# #             Parameters
# #             ----------
# #             c: int
# #                 Condition index in self.do['df']['ResCtrl]
# #             t: int
# #                 Relevant point index in self.do['df']['ResCtrl]
    
# #             Returns
# #             -------
# #             list[list[int]]
# #         """
# #         #region ---------------------------------------------------> List
# #         #------------------------------> 
# #         colC = self.do['df']['ResCtrl'][0][0]
# #         #------------------------------> 
# #         colD = self.do['df']['ResCtrl'][c+1][t]
# #         #endregion ------------------------------------------------> List
        
# #         return [colC, colD]
# #     #---
    
# #     def ColCtrlData_OCC(self, c:int, t:int) -> list[list[int]]:
# #         """Get the Ctrl and Data columns for the given condition and relevant
# #             point when Control Type is: One Control per Column
    
# #             Parameters
# #             ----------
# #             c: int
# #                 Condition index in self.do['df']['ResCtrl]
# #             t: int
# #                 Relevant point index in self.do['df']['ResCtrl]
    
# #             Returns
# #             -------
# #             list[list[int]]
# #         """
# #         #region ---------------------------------------------------> List
# #         #------------------------------> 
# #         colC = self.do['df']['ResCtrl'][0][t]
# #         #------------------------------> 
# #         colD = self.do['df']['ResCtrl'][c+1][t]
# #         #endregion ------------------------------------------------> List
        
# #         return [colC, colD]
# #     #---
    
# #     def ColCtrlData_OCR(self, c:int, t:int) -> list[list[int]]:
# #         """Get the Ctrl and Data columns for the given condition and relevant
# #             point when Control Type is: One Control per Row
    
# #             Parameters
# #             ----------
# #             c: int
# #                 Condition index in self.do['df']['ResCtrl]
# #             t: int
# #                 Relevant point index in self.do['df']['ResCtrl]
    
# #             Returns
# #             -------
# #             list[list[int]]
# #         """
# #         #region ---------------------------------------------------> List
# #         #------------------------------> 
# #         colC = self.do['df']['ResCtrl'][c][0]
# #         #------------------------------> 
# #         colD = self.do['df']['ResCtrl'][c][t+1]
# #         #endregion ------------------------------------------------> List
        
# #         return [colC, colD]
# #     #---
    
# #     def ColCtrlData_Ratio(self, c:int, t:int) -> list[Optional[list[int]]]:
# #         """Get the Ctrl and Data columns for the given condition and relevant
# #             point when Control Type is: Data as Ratios
    
# #             Parameters
# #             ----------
# #             c: int
# #                 Condition index in self.do['df']['ResCtrl]
# #             t: int
# #                 Relevant point index in self.do['df']['ResCtrl]
    
# #             Returns
# #             -------
# #             list[list[int]]
# #         """
# #         #region ---------------------------------------------------> List
# #         #------------------------------> 
# #         colC = None
# #         #------------------------------> 
# #         colD = self.do['df']['ResCtrl'][c][t]
# #         #endregion ------------------------------------------------> List
        
# #         return [colC, colD]
# #     #---
    
# #     def CalcOutData(
# #         self, cN: str, tN: str, colC: Optional[list[int]], colD: list[int]) -> bool:
# #         """Calculate the data for the main output dataframe
    
# #             Parameters
# #             ----------
            
    
# #             Returns
# #             -------
# #             bool
    
# #             Raise
# #             -----
# #             ExecutionError:
# #                 - When the calculation fails
# #         """
# #         if config.development:
# #             print(cN, tN, colC, colD)
# #         #------------------------------> Ave & Std
# #         if colC is not None:
# #             self.dfR.loc[:,(cN, tN, 'aveC')] = self.dfIm.iloc[:,colC].mean(
# #                 axis=1, skipna=True).to_numpy()
# #             self.dfR.loc[:,(cN, tN, 'stdC')] = self.dfIm.iloc[:,colC].std(
# #                 axis=1, skipna=True).to_numpy()
# #         else:
# #             self.dfR.loc[:,(cN, tN, 'aveC')] = np.nan
# #             self.dfR.loc[:,(cN, tN, 'stdC')] = np.nan
        
# #         self.dfR.loc[:,(cN, tN, 'ave')] = self.dfIm.iloc[:,colD].mean(
# #             axis=1, skipna=True).to_numpy()
# #         self.dfR.loc[:,(cN, tN, 'std')] = self.dfIm.iloc[:,colD].std(
# #             axis=1, skipna=True).to_numpy()
# #         #------------------------------> Intensities as log2 Intensities
# #         dfLogI = self.dfIm.copy() 
# #         if self.do['TransMethod'] == 'Log2':
# #             pass
# #         else:
# #             if colC is not None:
# #                 dfLogI.iloc[:,colC+colD] = np.log2(dfLogI.iloc[:,colC+colD])
# #             else:
# #                 dfLogI.iloc[:,colD] = np.log2(dfLogI.iloc[:,colD])
# #         #------------------------------> log2(FC)
# #         if colC is not None:
# #             FC = (
# #                 dfLogI.iloc[:,colD].mean(axis=1, skipna=True)
# #                 - dfLogI.iloc[:,colC].mean(axis=1, skipna=True)
# #             )
# #         else:
# #             FC = dfLogI.iloc[:,colD].mean(axis=1, skipna=True)
        
# #         self.dfR.loc[:, (cN, tN, 'FC')] = FC.to_numpy()
# #         #------------------------------> FCz
# #         self.dfR.loc[:,(cN, tN, 'FCz')] = (FC - FC.mean()).div(FC.std()).to_numpy()
# #         #------------------------------> FCci
# #         if self.do['RawI']:
# #             self.dfR.loc[:,(cN, tN, 'CI')] = dtsStatistic.CI_Mean_Diff_DF(
# #                 dfLogI, 
# #                 colC, 
# #                 colD, 
# #                 self.do['Alpha'], 
# #                 self.do['IndS'],
# #                 fullCI=False,
# #             ).to_numpy()
# #         else:
# #             self.dfR.loc[:,(cN, tN, 'CI')] = dtsStatistic.CI_Mean_DF(
# #                 dfLogI.iloc[:,colD], self.do['Alpha'], fullCI=False,
# #             ).to_numpy()
# #         #------------------------------> P
# #         if self.do['RawI']:
# #             if self.do['IndS']:
# #                 self.dfR.loc[:,(cN,tN,'P')] = dtsStatistic.ttest_IS_DF(
# #                     dfLogI, colC, colD,
# #                 )['P'].to_numpy()        
# #             else:
# #                 self.dfR.loc[:,(cN,tN,'P')] = dtsStatistic.ttest_PS_DF(
# #                     dfLogI, colC, colD,
# #                 )['P'].to_numpy()
# #         else:
# #             #------------------------------> Dummy 0 columns
# #             dfLogI['TEMP_Col_Full_00'] = 0
# #             dfLogI['TEMP_Col_Full_01'] = 0
# #             colCF = []
# #             colCF.append(dfLogI.columns.get_loc('TEMP_Col_Full_00'))
# #             colCF.append(dfLogI.columns.get_loc('TEMP_Col_Full_01'))
# #             #------------------------------> 
# #             self.dfR.loc[:,(cN,tN,'P')] = dtsStatistic.ttest_IS_DF(
# #                 dfLogI, colCF, colD, f=True,
# #             )['P'].to_numpy()
# #         #------------------------------> Pc
# #         if self.do['CorrectP'] != 'None':
# #             self.dfR.loc[:,(cN,tN,'Pc')] = multipletests(
# #                 self.dfR.loc[:,(cN,tN,'P')], 
# #                 self.do['Alpha'], 
# #                 config.oCorrectP[self.do['CorrectP']]
# #             )[1]
# #         else:
# #             pass
# #         #------------------------------> Round to .XX
# #         self.dfR.loc[:,(cN,tN,config.dfcolProtprofCLevel)] = (
# #             self.dfR.loc[:,(cN,tN,config.dfcolProtprofCLevel)].round(2)
# #         )
        
# #         return True
# #     #---
    
# #     def WriteOutput(self) -> bool:
# #         """Write output 
        
# #             Returns
# #             -------
# #             bool
# #         """
# #         #region --------------------------------------------------> Data Steps
# #         stepDict = {
# #             config.fnInitial.format('01', self.date): self.dfI,
# #             config.fnFloat.format('02', self.date)  : self.dfF,
# #             config.fnExclude.format('03', self.date): self.dfEx,
# #             config.fnScore.format('04', self.date)  : self.dfS,
# #             config.fnTrans.format('05', self.date)  : self.dfT,
# #             config.fnNorm.format('06', self.date)   : self.dfN,
# #             config.fnImp.format('07', self.date)    : self.dfIm,
# #             self.cMainData.format('08', self.date)  : self.dfR,
# #         }
# #         #endregion -----------------------------------------------> Data Steps

# #         return self.WriteOutputData(stepDict)
# #     #---
#     #endregion ------------------------------------------------> Run methods
# #---


# # class LimProt(BaseConfModPanel2):
# #     """Configuration Pane for the Limited Proteolysis module.

# #         Parameters
# #         ----------
# #         parent: wx.Widget
# #             Parent of the pane
# #         dataI : dict or None
# #             Initial data provided by the user in a previous analysis.
# #             This contains both I and CI dicts e.g. {'I': I, 'CI': CI}.

# #         Attributes
# #         ----------
# #         name : str
# #             Name of the pane. Default to config.npLimProt.
# #         cURL : str
# #             URL for the online help.
# #         #------------------------------> Configuration
# #         cLBeta: str
# #             Label for the Beta value
# #         cLGamma: str
# #             Label for the Gamma value
# #         cLSample: str
# #             Label for the Samples
# #         cLTheta: str
# #             Label for the Theta value
# #         cLThetaMax: str
# #             Label for the Theta Max value
# #         cOSample: list of str
# #             Options for the Samples
# #         cTTSample: str
# #             Tooltip for the Samples  
# #         #------------------------------> To Run Analysis
# #         changeKey: list of str
# #             Keys in self.do that must be turned to str.
# #         checkUserInput : dict
# #             To check the user input in the right order. 
# #             See pane.BaseConfPanel.CheckInput for a description of the dict.
# #         cColCtrlData : dict
# #             Keys are control type and values methods to get the Ctrl and 
# #             Data columns for the given condition and relevant point.
# #         cGaugePD : int
# #             Number of steps for the Progress Dialog.
# #         cLLenLongest : int
# #             Length of the longest label in the panel.
# #         cMainData : str
# #             Name of file containing the results in Steps_Data_File.
# #         cSection : str
# #             Name of the section. Default to config.nmLimProt.
# #         cTitlePD : str
# #             Name of the Progress Dialog window.
# #         do: dict
# #             Dictionary with checked user input. Keys are:
# #             {
# #                 "iFile"      : "Path to input data file",
# #                 "uFile"      : "Path to umsap file.",
# #                 'seqFile'    : "Path to the sequence file",
# #                 'ID'         : 'Analysis ID',
# #                 "Cero"       : Boolean, how to treat cero values,
# #                 "TransMethod": "Transformation method",
# #                 "NormMethod" : "Normalization method",
# #                 "ImpMethod"  : "Imputation method",
# #                 "TargetProt" : 'Target Protein',
# #                 "ScoreVal"   : "Score value threshold",
# #                 'SeqLength'  : "Sequence length",
# #                 'Sample'     : 'Independent or dependent samples',
# #                 "Alpha"      : "Significance level",
# #                 "Beta"       : "Beta level',
# #                 'Gamma'      : "Gamma level",
# #                 'Theta'      : Theta value or None,
# #                 'Theta Max'  : Theta maximum,
# #                 "Lane"       : [List of lanes],
# #                 "Band"       : [List of bands],
# #                 "ControlL"   : "Control label",
# #                 "oc": {
# #                     'SeqCol'   : Column of Sequences,
# #                     "TargetProtCol" : Column of Proteins,
# #                     "ScoreCol" : Score column,
# #                     "ResCtrl": [List of columns containing the control and 
# #                                 experiments column numbers],
# #                     "Column": [Flat list of all column numbers with the 
# #                               following order: SeqCol, TargetProtCol, 
# #                               ScoreColRes & Control]
# #                 },
# #                 "df": { Column numbers in the pd.df created from the input file.
# #                     "SeqCol" : 0,
# #                     "TargetProtCol": 1,
# #                     "ScoreCol" : 2,
# #                     "ResCtrl": [],
# #                     "ResCtrlFlat": [ResCtrl as a flat list],
# #                     "ColumnR : [Columns with the results] 
# #                     "ColumnF": [Columns that must contain only float numbers]
# #                 },
# #                 "dfo" : {
# #                     'NC' : [Columns for the N and C residue numbers in the 
# #                         output df],
# #                     'NCF' : [Columns for the Nnat and Cnat residue numbers in 
# #                         the output df],
# #                 },
# #             },    
# #         d: dict
# #             Dictionary with the user input. Keys are labels in the panel plus:
# #             {
# #                 config.lStLimProtLane           : [list of lanes],
# #                 config.lStLimProtBand           : [list of bands],
# #                 f"Control {config.lStCtrlName}" : "Control Name",
# #             }
            
# #         See Parent classes for more aatributes.
        
# #         Notes
# #         -----
# #         Running the analysis results in the creation of:
        
# #         - Parent Folder/
# #             - Input_Data_Files/
# #             - Steps_Data_Files/20220104-214055_Limited Proteolysis/
# #             - output-file.umsap
        
# #         The Input_Data_Files folder contains the original data files. These are 
# #         needed for data visualization, running analysis again with different 
# #         parameters, etc.
# #         The Steps_Data_Files/Date-Section folder contains regular csv files with 
# #         the step by step data.
    
# #         The Limited Proteolysis section in output-file.umsap conteins the 
# #         information about the calculations, e.g

# #         {
# #             'Limited Proteolysis : {
# #                 '20210324-165609': {
# #                     'V' : config.dictVersion,
# #                     'I' : self.d,
# #                     'CI': self.do,
# #                     'DP': {
# #                         'dfS' : pd.DataFrame with initial data as float and
# #                                 after discarding values by score.
# #                         'dfT' : pd.DataFrame with transformed data.
# #                         'dfN' : pd.DataFrame with normalized data.
# #                         'dfIm': pd.DataFrame with imputed data.
# #                     }
# #                     'R' : pd.DataFrame (dict) with the calculation results.
# #                 }
# #             }
# #         }
        
# #         The result data frame has the following structure:
        
# #         Sequence Score Nterm Cterm NtermF CtermF Delta Band1 ... BandN
# #         Sequence Score Nterm Cterm NtermF CtermF Delta Lane1 ... LaneN
# #         Sequence Score Nterm Cterm NtermF CtermF Delta Ptost ... Ptost
# #     """
# #     #region -----------------------------------------------------> Class setup
# #     name = config.npLimProt
# #     #endregion --------------------------------------------------> Class setup

# #     #region --------------------------------------------------> Instance setup
# #     def __init__(self, parent, dataI: Optional[dict]):
# #         """ """
# #         #region -------------------------------------------------> Check Input
        
# #         #endregion ----------------------------------------------> Check Input

# #         #region -----------------------------------------------> Initial Setup
# #         #------------------------------> Configuration
# #         self.cLBeta     = "β value"
# #         self.cLGamma    = "γ value"
# #         self.cLTheta    = "Θ value"
# #         self.cLThetaMax = "Θmax value"
# #         self.cLSample   = 'Samples'
# #         #------------------------------> Choices
# #         self.cOSample = list(config.oSamples.keys())
# #         #------------------------------> Tooltips
# #         self.cTTSample = config.ttStSample
# #         #------------------------------> Needed by BaseConfPanel
# #         self.cURL         = config.urlLimProt
# #         self.cSection     = config.nmLimProt
# #         self.cLLenLongest = len(config.lStResultCtrl)
# #         self.cTitlePD     = f"Running {config.nmLimProt} Analysis"
# #         self.cGaugePD     = 50
# #         #------------------------------> Needed to Run
# #         self.cMainData    = '{}-LimitedProteolysis-Data-{}.txt'
# #         self.changeKey = ['iFile', 'uFile', 'seqFile']
# #         #------------------------------> 
# #         super().__init__(parent)
# #         #endregion --------------------------------------------> Initial Setup

# #         #region -----------------------------------------------------> Widgets
# #         #------------------------------> Values
# #         self.beta = dtsWidget.StaticTextCtrl(
# #             self.sbValue,
# #             stLabel   = self.cLBeta,
# #             tcSize    = self.cSTc,
# #             validator = dtsValidator.NumberList(
# #                 numType = 'float',
# #                 nN      = 1,
# #                 vMin    = 0,
# #                 vMax    = 1,
# #             )
# #         )
# #         self.gamma = dtsWidget.StaticTextCtrl(
# #             self.sbValue,
# #             stLabel   = self.cLGamma,
# #             tcSize    = self.cSTc,
# #             validator = dtsValidator.NumberList(
# #                 numType = 'float',
# #                 nN      = 1,
# #                 vMin    = 0,
# #                 vMax    = 1,
# #             )
# #         )
# #         self.theta = dtsWidget.StaticTextCtrl(
# #             self.sbValue,
# #             stLabel   = self.cLTheta,
# #             tcSize    = self.cSTc,
# #             validator = dtsValidator.NumberList(
# #                 numType = 'float',
# #                 nN      = 1,
# #                 vMin    = 0,
# #                 opt     = True,
# #             )
# #         )
# #         self.thetaMax = dtsWidget.StaticTextCtrl(
# #             self.sbValue,
# #             stLabel   = self.cLThetaMax,
# #             tcSize    = self.cSTc,
# #             validator = dtsValidator.NumberList(
# #                 numType = 'float',
# #                 nN      = 1,
# #                 vMin    = 0,
# #             )
# #         )
# #         self.sample = dtsWidget.StaticTextComboBox(
# #             self.sbValue,
# #             label     = self.cLSample,
# #             choices   = self.cOSample,
# #             tooltip   = self.cTTSample,
# #             validator = dtsValidator.IsNotEmpty(),
# #         )
# #         #endregion --------------------------------------------------> Widgets
        
# #         #region ----------------------------------------------> checkUserInput
# #         self.checkUserInput = {
# #             self.cLuFile       : [self.uFile.tc,           config.mFileBad],
# #             self.cLiFile       : [self.iFile.tc,           config.mFileBad],
# #             self.cLSeqFile     : [self.seqFile.tc,         config.mFileBad],
# #             self.cLTransMethod : [self.transMethod.cb,     config.mOptionBad],
# #             self.cLNormMethod  : [self.normMethod.cb,      config.mOptionBad],
# #             self.cLImputation  : [self.imputationMethod.cb,config.mOptionBad],
# #             self.cLTargetProt  : [self.targetProt.tc,      config.mValueBad],
# #             self.cLScoreVal    : [self.scoreVal.tc,        config.mOneRealNum],
# #             self.cLSeqLength   : [self.seqLength.tc,       config.mOneZPlusNum],
# #             self.cLSample      : [self.sample.cb,          config.mOptionBad],
# #             self.cLAlpha       : [self.alpha.tc,           config.mOne01Num],
# #             self.cLBeta        : [self.beta.tc,            config.mOne01Num],
# #             self.cLGamma       : [self.gamma.tc,           config.mOne01Num],
# #             self.cLTheta       : [self.theta.tc,           config.mOneZPlusNum],
# #             self.cLThetaMax    : [self.thetaMax.tc,        config.mOneZPlusNum],
# #             self.cLSeqCol      : [self.seqCol.tc,          config.mOneZPlusNum],
# #             self.cLDetectedProt: [self.detectedProt.tc,    config.mOneZPlusNum],
# #             self.cLScoreCol    : [self.score.tc,           config.mOneZPlusNum],
# #             self.cLResControl  : [self.tcResults,          config.mResCtrl]
# #         }        
# #         #endregion -------------------------------------------> checkUserInput

# #         #region ------------------------------------------------------> Sizers
# #         #------------------------------> Sizer Values
# #         self.sizersbValueWid.Add(
# #             1, 1,
# #             pos    = (0,0),
# #             flag   = wx.EXPAND|wx.ALL,
# #             border = 5,
# #             span   = (2, 0),
# #         )
# #         self.sizersbValueWid.Add(
# #             self.targetProt.st,
# #             pos    = (0,1),
# #             flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
# #             border = 5,
# #         )
# #         self.sizersbValueWid.Add(
# #             self.targetProt.tc,
# #             pos    = (0,2),
# #             flag   = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL,
# #             border = 5,
# #         )
# #         self.sizersbValueWid.Add(
# #             self.scoreVal.st,
# #             pos    = (1,1),
# #             flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
# #             border = 5,
# #         )
# #         self.sizersbValueWid.Add(
# #             self.scoreVal.tc,
# #             pos    = (1,2),
# #             flag   = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL,
# #             border = 5,
# #         )
# #         self.sizersbValueWid.Add(
# #             self.seqLength.st,
# #             pos    = (2,1),
# #             flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
# #             border = 5,
# #         )
# #         self.sizersbValueWid.Add(
# #             self.seqLength.tc,
# #             pos    = (2,2),
# #             flag   = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL,
# #             border = 5,
# #         )
# #         self.sizersbValueWid.Add(
# #             self.alpha.st,
# #             pos    = (3,1),
# #             flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
# #             border = 5,
# #         )
# #         self.sizersbValueWid.Add(
# #             self.alpha.tc,
# #             pos    = (3,2),
# #             flag   = wx.EXPAND|wx.ALL,
# #             border = 5,
# #         )
# #         self.sizersbValueWid.Add(
# #             self.beta.st,
# #             pos    = (0,3),
# #             flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
# #             border = 5,
# #         )
# #         self.sizersbValueWid.Add(
# #             self.beta.tc,
# #             pos    = (0,4),
# #             flag   = wx.EXPAND|wx.ALL,
# #             border = 5,
# #         )
# #         self.sizersbValueWid.Add(
# #             self.gamma.st,
# #             pos    = (1,3),
# #             flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
# #             border = 5,
# #         )
# #         self.sizersbValueWid.Add(
# #             self.gamma.tc,
# #             pos    = (1,4),
# #             flag   = wx.EXPAND|wx.ALL,
# #             border = 5,
# #         )
# #         self.sizersbValueWid.Add(
# #             self.theta.st,
# #             pos    = (2,3),
# #             flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
# #             border = 5,
# #         )
# #         self.sizersbValueWid.Add(
# #             self.theta.tc,
# #             pos    = (2,4),
# #             flag   = wx.EXPAND|wx.ALL,
# #             border = 5,
# #         )
# #         self.sizersbValueWid.Add(
# #             self.thetaMax.st,
# #             pos    = (3,3),
# #             flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
# #             border = 5,
# #         )
# #         self.sizersbValueWid.Add(
# #             self.thetaMax.tc,
# #             pos    = (3,4),
# #             flag   = wx.EXPAND|wx.ALL,
# #             border = 5,
# #         )
# #         self.sizersbValueWid.Add(
# #             self.sample.st,
# #             pos    = (4,1),
# #             flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
# #             border = 5,
# #         )
# #         self.sizersbValueWid.Add(
# #             self.sample.cb,
# #             pos    = (4,2),
# #             flag   = wx.EXPAND|wx.ALL,
# #             border = 5,
# #         )
# #         self.sizersbValueWid.Add(
# #             1, 1,
# #             pos    = (0,5),
# #             flag   = wx.EXPAND|wx.ALL,
# #             border = 5,
# #             span   = (2, 0),
# #         )
        
# #         self.sizersbValueWid.AddGrowableCol(0, 1)
# #         self.sizersbValueWid.AddGrowableCol(2, 1)
# #         self.sizersbValueWid.AddGrowableCol(4, 1)
# #         self.sizersbValueWid.AddGrowableCol(5, 1)
# #         #------------------------------> Main Sizer
# #         self.SetSizer(self.Sizer)
# #         self.Sizer.Fit(self)
# #         self.SetupScrolling()
# #         #endregion ---------------------------------------------------> Sizers

# #         #region --------------------------------------------------------> Bind
        
# #         #endregion -----------------------------------------------------> Bind

# #         #region ---------------------------------------------> Window position
        
# #         #endregion ------------------------------------------> Window position
        
# #         #region --------------------------------------------------------> Test
# #         if config.development:
# #             import getpass
# #             user = getpass.getuser()
# #             if config.cOS == "Darwin":
# #                 self.uFile.tc.SetValue("/Users/" + str(user) + "/TEMP-GUI/BORRAR-UMSAP/umsap-dev.umsap")
# #                 self.iFile.tc.SetValue("/Users/" + str(user) + "/Dropbox/SOFTWARE-DEVELOPMENT/APPS/UMSAP/LOCAL/DATA/UMSAP-TEST-DATA/LIMPROT/limprot-data-file.txt")
# #                 self.seqFile.tc.SetValue("/Users/" + str(user) + "/Dropbox/SOFTWARE-DEVELOPMENT/APPS/UMSAP/LOCAL/DATA/UMSAP-TEST-DATA/LIMPROT/limprot-seq-both.txt")
# #             else:
# #                 pass
# #             self.id.tc.SetValue('Beta Test Dev')
# #             self.transMethod.cb.SetValue('Log2')
# #             self.normMethod.cb.SetValue('Median')
# #             self.imputationMethod.cb.SetValue('Normal Distribution')
# #             self.targetProt.tc.SetValue('Mis18alpha')
# #             self.scoreVal.tc.SetValue('10')
# #             self.seqLength.tc.SetValue('100')
# #             self.alpha.tc.SetValue('0.05')
# #             self.beta.tc.SetValue('0.05')
# #             self.gamma.tc.SetValue('0.8')
# #             self.theta.tc.SetValue('')
# #             self.thetaMax.tc.SetValue('8')
# #             self.sample.cb.SetValue('Independent Samples')
# #             self.seqCol.tc.SetValue('0')
# #             self.detectedProt.tc.SetValue('34')
# #             self.score.tc.SetValue('42')
# #             self.tcResults.SetValue('69-71; 81-83, 78-80, 75-77, 72-74, ; , , , 66-68, ; 63-65, 105-107, 102-104, 99-101, ; 93-95, 90-92, 87-89, 84-86, 60-62')
# #             self.lbDict = {
# #                 1        : ['Lane1', 'Lane2', 'Lane3', 'Lane4', 'Lane5'],
# #                 2        : ['Band1', 'Band2', 'Band3', 'Band4'],
# #                 'Control': ['Ctrl'],
# #             }
# #         else:
# #             pass
# #         #endregion -----------------------------------------------------> Test
        
# #         #region -------------------------------------------------------> DataI
# #         self.SetInitialData(dataI)
# #         #endregion ----------------------------------------------------> DataI
# #     #---
# #     #endregion -----------------------------------------------> Instance setup

# #     #region ---------------------------------------------------> Class methods
# #     def SetInitialData(self, dataI: Optional[dict]=None) -> Literal[True]:
# #         """Set initial data
    
# #             Parameters
# #             ----------
# #             dataI : dict or None
# #                 Data to fill all fields and repeat an analysis. See Notes.
    
# #             Returns
# #             -------
# #             True
# #         """
# #         #region -------------------------------------------------> Fill Fields
# #         if dataI is not None:
# #             #------------------------------> Files
# #             self.uFile.tc.SetValue(dataI['CI']['uFile'])
# #             self.iFile.tc.SetValue(dataI['I'][self.cLiFile])
# #             self.seqFile.tc.SetValue(dataI['I'][f'{self.cLSeqFile} File'])
# #             self.id.tc.SetValue(dataI['CI']['ID'])
# #             # #------------------------------> Data Preparation
# #             self.ceroB.SetValue(dataI['I'][self.cLCeroTreatD])
# #             self.transMethod.cb.SetValue(dataI['I'][self.cLTransMethod])
# #             self.normMethod.cb.SetValue(dataI['I'][self.cLNormMethod])
# #             self.imputationMethod.cb.SetValue(dataI['I'][self.cLImputation])
# #             # #------------------------------> Values
# #             self.targetProt.tc.SetValue(dataI['I'][self.cLTargetProt])
# #             self.scoreVal.tc.SetValue(dataI['I'][self.cLScoreVal])
# #             self.seqLength.tc.SetValue(dataI['I'][self.cLSeqLength])
# #             self.alpha.tc.SetValue(dataI['I'][self.cLAlpha])
# #             self.sample.cb.SetValue(dataI['I'][self.cLSample])
# #             self.beta.tc.SetValue(dataI['I'][self.cLBeta])
# #             self.gamma.tc.SetValue(dataI['I'][self.cLGamma])
# #             self.theta.tc.SetValue(dataI['I'][self.cLTheta])
# #             self.thetaMax.tc.SetValue(dataI['I'][self.cLThetaMax])
# #             # #------------------------------> Columns
# #             self.seqCol.tc.SetValue(dataI['I'][f'{self.cLSeqCol} Column'])
# #             self.detectedProt.tc.SetValue(dataI['I'][self.cLDetectedProt])
# #             self.score.tc.SetValue(dataI['I'][self.cLScoreCol])
# #             self.tcResults.SetValue(dataI['I'][self.cLResControl])
# #             self.lbDict[1] = dataI['I'][config.lStLimProtLane]
# #             self.lbDict[2] = dataI['I'][config.lStLimProtBand]
# #             self.lbDict['Control'] = dataI['I'][f"Control {config.lStCtrlName}"]
# #         else:
# #             pass
# #         #endregion ----------------------------------------------> Fill Fields
        
# #         return True
# #     #---
    
# #     #------------------------------> Run Methods
# #     def CheckInput(self) -> bool:
# #         """Check user input
        
# #             Returns
# #             -------
# #             bool
# #         """
# #         #region -------------------------------------------------------> Super
# #         if super().CheckInput():
# #             pass
# #         else:
# #             return False
# #         #endregion ----------------------------------------------------> Super
        
# #         #region ---------------------------------------------------------> Msg
# #         msgPrefix = config.lPdCheck
# #         #endregion ------------------------------------------------------> Msg
        
# #         #region -------------------------------------------> Individual Fields

# #         #endregion ----------------------------------------> Individual Fields
        
# #         #region ------------------------------------------------> Mixed Fields
# #         #region ---------------------------------------> Unique Column Numbers
# #         msgStep = msgPrefix + 'Unique Column Numbers'
# #         wx.CallAfter(self.dlg.UpdateStG, msgStep)
# #         #------------------------------> 
# #         l = [self.seqCol.tc, self.detectedProt.tc, self.score.tc, 
# #             self.tcResults]
# #         #------------------------------> 
# #         if self.UniqueColumnNumber(l):
# #             pass
# #         else:
# #             return False
# #         #endregion ------------------------------------> Unique Column Numbers
# #         #endregion ---------------------------------------------> Mixed Fields
        
# #         return True
# #     #---
    
# #     def PrepareRun(self) -> bool:
# #         """Set variable and prepare data for analysis.
        
# #             Returns
# #             -------
# #             bool
# #         """
        
# #         #region ---------------------------------------------------------> Msg
# #         msgPrefix = config.lPdPrepare
# #         #endregion ------------------------------------------------------> Msg

# #         #region -----------------------------------------------------------> d
# #         msgStep = msgPrefix + 'User input, reading'
# #         wx.CallAfter(self.dlg.UpdateStG, msgStep)
# #         #------------------------------> As given
# #         self.d = {
# #             self.EqualLenLabel(self.cLiFile) : (
# #                 self.iFile.tc.GetValue()),
# #             self.EqualLenLabel(self.cLuFile) : (
# #                 self.uFile.tc.GetValue()),
# #             self.EqualLenLabel(f'{self.cLSeqFile} File') : (
# #                 self.seqFile.tc.GetValue()),
# #             self.EqualLenLabel(self.cLId) : (
# #                 self.id.tc.GetValue()),
# #             self.EqualLenLabel(self.cLCeroTreatD) : (
# #                 self.ceroB.IsChecked()),
# #             self.EqualLenLabel(self.cLTransMethod) : (
# #                 self.transMethod.cb.GetValue()),
# #             self.EqualLenLabel(self.cLNormMethod) : (
# #                 self.normMethod.cb.GetValue()),
# #             self.EqualLenLabel(self.cLImputation) : (
# #                 self.imputationMethod.cb.GetValue()),
# #             self.EqualLenLabel(self.cLTargetProt) : (
# #                 self.targetProt.tc.GetValue()),
# #             self.EqualLenLabel(self.cLScoreVal) : (
# #                 self.scoreVal.tc.GetValue()),
# #             self.EqualLenLabel(self.cLSeqLength) : (
# #                 self.seqLength.tc.GetValue()),
# #             self.EqualLenLabel(self.cLSample) : (
# #                 self.sample.cb.GetValue()),
# #             self.EqualLenLabel(self.cLAlpha) : (
# #                 self.alpha.tc.GetValue()),
# #             self.EqualLenLabel(self.cLBeta) : (
# #                 self.beta.tc.GetValue()),
# #             self.EqualLenLabel(self.cLGamma) : (
# #                 self.gamma.tc.GetValue()),
# #             self.EqualLenLabel(self.cLTheta) : (
# #                 self.theta.tc.GetValue()),
# #             self.EqualLenLabel(self.cLThetaMax) : (
# #                 self.thetaMax.tc.GetValue()),
# #             self.EqualLenLabel(f'{self.cLSeqCol} Column') : (
# #                 self.seqCol.tc.GetValue()),
# #             self.EqualLenLabel(self.cLDetectedProt) : (
# #                 self.detectedProt.tc.GetValue()),
# #             self.EqualLenLabel(self.cLScoreCol) : (
# #                 self.score.tc.GetValue()),
# #             self.EqualLenLabel(self.cLResControl): (
# #                 self.tcResults.GetValue()),
# #             self.EqualLenLabel(config.lStLimProtLane) : (
# #                 self.lbDict[1]),
# #             self.EqualLenLabel(config.lStLimProtBand) : (
# #                 self.lbDict[2]),
# #             self.EqualLenLabel(f"Control {config.lStCtrlName}") : (
# #                 self.lbDict['Control']),
# #         }
# #         #endregion --------------------------------------------------------> d
        
# #         #region ----------------------------------------------------------> do
# #         #------------------------------> Dict with all values
# #         #--------------> Step
# #         msgStep = msgPrefix + 'User input, processing'
# #         wx.CallAfter(self.dlg.UpdateStG, msgStep)
# #         #--------------> SeqLength
# #         seqLengthVal = self.seqLength.tc.GetValue()
# #         seqLength = float(seqLengthVal) if seqLengthVal != '' else None
# #         #--------------> Theta
# #         thetaVal = self.theta.tc.GetValue()
# #         theta = float(thetaVal) if thetaVal != '' else None
# #         #--------------> Columns
# #         seqCol       = int(self.seqCol.tc.GetValue())
# #         detectedProt = int(self.detectedProt.tc.GetValue())
# #         scoreCol     = int(self.score.tc.GetValue())
# #         resctrl       = dmethod.ResControl2ListNumber(self.tcResults.GetValue())
# #         resctrlFlat   = dmethod.ResControl2Flat(resctrl)
# #         resctrlDF     = dmethod.ResControl2DF(resctrl, 3)
# #         resctrlDFFlat = dmethod.ResControl2Flat(resctrlDF)
# #         #--------------> 
# #         self.do  = {
# #             'iFile'      : Path(self.iFile.tc.GetValue()),
# #             'uFile'      : Path(self.uFile.tc.GetValue()),
# #             'seqFile'    : Path(self.seqFile.tc.GetValue()),
# #             'ID'         : self.id.tc.GetValue(),
# #             'Cero'       : self.ceroB.IsChecked(),
# #             'TransMethod': self.transMethod.cb.GetValue(),
# #             'NormMethod' : self.normMethod.cb.GetValue(),
# #             'ImpMethod'  : self.imputationMethod.cb.GetValue(),
# #             'TargetProt' : self.targetProt.tc.GetValue(),
# #             'ScoreVal'   : float(self.scoreVal.tc.GetValue()),
# #             'SeqLength'  : seqLength,
# #             'Sample'     : config.oSamples[self.sample.cb.GetValue()],
# #             'Alpha'      : float(self.alpha.tc.GetValue()),
# #             'Beta'       : float(self.beta.tc.GetValue()),
# #             'Gamma'      : float(self.gamma.tc.GetValue()),
# #             'Theta'      : theta,
# #             'ThetaMax'   : float(self.thetaMax.tc.GetValue()),
# #             'Lane'       : self.lbDict[1],
# #             'Band'       : self.lbDict[2],
# #             'ControlL'   : self.lbDict['Control'],
# #             'oc'         : { # Column numbers in the initial dataframe
# #                 'SeqCol'       : seqCol,
# #                 'TargetProtCol': detectedProt,
# #                 'ScoreCol'     : scoreCol,
# #                 'ResCtrl'      : resctrl,
# #                 'Column'       : (
# #                     [seqCol, detectedProt, scoreCol] + resctrlFlat),
# #             },
# #             'df' : { # Column numbers in the selected data dataframe
# #                 'SeqCol'       : 0,
# #                 'TargetProtCol': 1,
# #                 'ScoreCol'     : 2,
# #                 'ResCtrl'      : resctrlDF,
# #                 'ResCtrlFlat'  : resctrlDFFlat,
# #                 'ColumnR'      : resctrlDFFlat,
# #                 'ColumnF'      : [2] + resctrlDFFlat,
# #             },
# #             'dfo' : { # Column numbers in the output dataframe
# #                 'NC' : [2,3], # N and C Term Res Numbers in the Rec Seq
# #                 'NCF': [4,5], # N and C Term Res Numbers in the Nat Seq
# #             }
# #         }
# #         #------------------------------> File base name
# #         self.oFolder = self.do['uFile'].parent
# #         #------------------------------> Date
# #         self.date = dtsMethod.StrNow()
# #         #------------------------------> DateID
# #         self.dateID = f'{self.date} - {self.do["ID"]}'
# #         #endregion -------------------------------------------------------> do

# #         #region -------------------------------------------------> Print d, do
# #         if config.development:
# #             print('')
# #             print('self.d:')
# #             for k,v in self.d.items():
# #                 print(str(k)+': '+str(v))
# #             print('')
# #             print('self.do')
# #             for k,v in self.do.items():
# #                 if k in ['oc', 'df', 'dfo']:
# #                     print(k)
# #                     for j,w in self.do[k].items():
# #                         print(f'\t{j}: {w}')
# #                 else:
# #                     print(str(k)+': '+str(v))
# #             print('')
# #         else:
# #             pass
# #         #endregion ----------------------------------------------> Print d, do
        
# #         return True
# #     #---
    
# #     def ReadInputFiles(self) -> bool:
# #         """Read the input files.
        
# #             Returns
# #             -------
# #             bool
# #         """
# #         #region ---------------------------------------------------> Super
# #         if super().ReadInputFiles():
# #             pass
# #         else:
# #             return False
# #         #endregion ------------------------------------------------> Super

# #         #region ---------------------------------------------------> 
# #         try:
# #             ProtLoc = self.seqFileObj.GetNatProtLoc()
# #         except Exception:
# #             ProtLoc = (None, None)
        
# #         self.do['ProtLength'] = self.seqFileObj.seqLengthRec
# #         self.do['ProtLoc'] = ProtLoc
# #         #endregion ------------------------------------------------> 
        
# #         #region ---------------------------------------------------> 
# #         try:
# #             ProtDelta = self.seqFileObj.GetSelfDelta()
# #         except Exception:
# #             ProtDelta = (None, None)
        
# #         self.do['ProtDelta'] = ProtDelta
# #         #endregion ------------------------------------------------> 
        
# #         return True
# #     #---
    
# #     def RunAnalysis(self) -> bool:
# #         """ Perform the equivalence tests 

# #             Returns
# #             -------
# #             bool
# #         """
# #         #region ---------------------------------------------------------> Msg
# #         msgPrefix = config.lPdRun
# #         #endregion ------------------------------------------------------> Msg
        
# #         #region --------------------------------------------> Data Preparation
# #         if self.DataPreparation():
# #             pass
# #         else:
# #             return False
# #         #endregion -----------------------------------------> Data Preparation
        
# #         #region ----------------------------------------------------> Empty DF
# #         #------------------------------> Msg
# #         msgStep = f'{msgPrefix} Creating empty dataframe'
# #         wx.CallAfter(self.dlg.UpdateStG, msgStep)
# #         #------------------------------> 
# #         self.dfR = self.EmptyDFR()
# #         #endregion -------------------------------------------------> Empty DF
        
# #         #region ------------------------------------------------> N, C Res Num
# #         if self.NCResNumbers(seqNat=False):
# #             pass
# #         else:
# #             return False
# #         #endregion ---------------------------------------------> N, C Res Num
        
# #         #region -------------------------------------------------------> Delta
# #         #------------------------------> Msg
# #         msgStep = f'{msgPrefix} Delta values'
# #         wx.CallAfter(self.dlg.UpdateStG, msgStep)
# #         #------------------------------> 
# #         colC = self.do['df']['ResCtrl'][0][0]
# #         #------------------------------> 
# #         if self.do['Theta'] is not None:
# #             delta = self.do['Theta']
# #         else:
# #             delta = dtsStatistic.tost_delta(
# #                 self.dfIm.iloc[:,colC], 
# #                 self.do['Alpha'],
# #                 self.do['Beta'],
# #                 self.do['Gamma'], 
# #                 deltaMax=self.do['ThetaMax'],
# #             )
# #         #------------------------------>         
# #         self.dfR[('Delta', 'Delta', 'Delta')] = delta
# #         #endregion ----------------------------------------------------> Delta
        
# #         #region ---------------------------------------------------> Calculate
# #         for b, bN in enumerate(self.do['Band']):
# #             for l, lN in enumerate(self.do['Lane']):
# #                 #------------------------------> Message
# #                 msgStep = (
# #                     f'{msgPrefix}'
# #                     f'Gel spot {bN} - {lN}'
# #                 )  
# #                 wx.CallAfter(self.dlg.UpdateSt, msgStep)
# #                 #------------------------------> Control & Data Column
# #                 colD = self.do['df']['ResCtrl'][b+1][l]
# #                 #------------------------------> Calculate data
# #                 if colD:
# #                     try:
# #                         self.CalcOutData(bN, lN, colC, colD)
# #                     except Exception as e:
# #                         self.msgError = (
# #                             f'Calculation of the Limited Proteolysis data for '
# #                             f'point {bN} - {lN} failed.'
# #                         )
# #                         self.tException = e
# #                         return False
# #                 else:
# #                     pass
# #         #endregion ------------------------------------------------> Calculate
        
# #         #region --------------------------------------------------------> Sort
# #         self.dfR = self.dfR.sort_values(
# #             by=[('Nterm', 'Nterm', 'Nterm'),('Cterm', 'Cterm', 'Cterm')]
# #         )
# #         self.dfR = self.dfR.reset_index(drop=True)
# #         #endregion -----------------------------------------------------> Sort
        
# #         if config.development:
# #             print('self.dfR.shape: ', self.dfR.shape)
# #             print('')
# #             print(self.dfR)
# #             print('')
        
# #         return True
# #     #---
    
# #     def WriteOutput(self) -> bool:
# #         """Write output 
        
# #             Returns
# #             -------
# #             bool
# #         """
# #         #region --------------------------------------------------> Data Steps
# #         stepDict = {
# #             config.fnInitial.format('01', self.date)    : self.dfI,
# #             config.fnFloat.format('02', self.date)      : self.dfF,
# #             config.fnTargetProt.format('03', self.date) : self.dfTP,
# #             config.fnScore.format('04', self.date)      : self.dfS,
# #             config.fnTrans.format('05', self.date)      : self.dfT,
# #             config.fnNorm.format('06', self.date)       : self.dfN,
# #             config.fnImp.format('07', self.date)        : self.dfIm,
# #             self.cMainData.format('08', self.date)      : self.dfR,
# #         }
# #         #endregion -----------------------------------------------> Data Steps
        
# #         return self.WriteOutputData(stepDict)
# #     #---
    
# #     def EmptyDFR(self) -> 'pd.DataFrame':
# #         """Creates the empty df for the results
        
# #             Returns
# #             -------
# #             pd.DataFrame
# #         """
# #         #region -------------------------------------------------------> Index
# #         #------------------------------> 
# #         aL = config.dfcolLimProtFirstPart
# #         bL = config.dfcolLimProtFirstPart
# #         cL = config.dfcolLimProtFirstPart
# #         #------------------------------> 
# #         n = len(config.dfcolLimProtCLevel)
# #         #------------------------------> 
# #         for b in self.do['Band']:
# #             for l in self.do['Lane']:
# #                 aL = aL + n*[b]
# #                 bL = bL + n*[l]
# #                 cL = cL + config.dfcolLimProtCLevel
# #         #------------------------------> 
# #         idx = pd.MultiIndex.from_arrays([aL[:], bL[:], cL[:]])
# #         #endregion ----------------------------------------------------> Index
        
# #         #region ----------------------------------------------------> Empty DF
# #         df = pd.DataFrame(
# #             np.nan, columns=idx, index=range(self.dfIm.shape[0]),
# #         )
# #         #endregion -------------------------------------------------> Empty DF
        
# #         #region -------------------------------------------------> Seq & Score
# #         df[(aL[0], bL[0], cL[0])] = self.dfIm.iloc[:,0]
# #         df[(aL[1], bL[1], cL[1])] = self.dfIm.iloc[:,2]
# #         #endregion ----------------------------------------------> Seq & Score
        
# #         return df
# #     #---
    
# #     def CalcOutData(
# #         self, bN: str,  lN: str, colC: list[int], colD: list[int],
# #         ) -> bool:
# #         """Performed the tost test
    
# #             Parameters
# #             ----------
# #             bN: str
# #                 Band name
# #             lN : str
# #                 Lane name
# #             colC : list int
# #                 Column numbers of the control
# #             colD : list int
# #                 Column numbers of the gel spot
    
# #             Returns
# #             -------
# #             bool
# #         """
# #         #region ----------------------------------------------> Delta and TOST
# #         a = dtsStatistic.tost(
# #             self.dfIm, colC, colD, sample=self.do['Sample'], 
# #             delta=self.dfR[('Delta', 'Delta', 'Delta')], alpha=self.do['Alpha'],
# #         ) 
# #         self.dfR[(bN, lN, 'Ptost')] = a['P'].to_numpy()
# #         #endregion -------------------------------------------> Delta and TOST
        
# #         return True
# #     #---
    
# #     def RunEnd(self):
# #         """Restart GUI and needed variables"""
# #         #region ---------------------------------------> Dlg progress dialogue
# #         if self.msgError is None:
# #             #--> 
# #             self.dlg.SuccessMessage(
# #                 config.lPdDone,
# #                 eTime=f"{config.lPdEllapsed}  {self.deltaT}",
# #             )
# #         else:
# #             self.dlg.ErrorMessage(
# #                 config.lPdError, 
# #                 error      = self.msgError,
# #                 tException = self.tException
# #             )
# #         #endregion ------------------------------------> Dlg progress dialogue

# #         #region -------------------------------------------------------> Reset
# #         self.msgError   = None # Error msg to show in self.RunEnd
# #         self.tException = None # Exception
# #         self.d          = {} # Dict with the user input as given
# #         self.do         = {} # Dict with the processed user input
# #         self.dfI        = None # pd.DataFrame for initial, normalized and
# #         self.dfF        = None
# #         self.dfTP       = None
# #         self.dfEx       = None
# #         self.dfS        = None
# #         self.dfT        = None
# #         self.dfN        = None
# #         self.dfIm       = None
# #         self.dfR        = None
# #         self.date       = None # date for corr file
# #         self.dateID     = None
# #         self.oFolder    = None # folder for output
# #         self.iFileObj   = None
# #         self.seqFileObj = None
# #         self.deltaT     = None
        
# #         if self.dFile is not None:
# #             self.iFile.tc.SetValue(str(self.dFile))
# #         else:
# #             pass
# #         self.dFile = None # Data File copied to Data-Initial
# #         #endregion ----------------------------------------------------> Reset
# #     #---
# #     #endregion ------------------------------------------------> Class methods
# # #---


# #------------------------------> Panes for Type Results - Control Epxeriments
# class ProtProfResControlExp(ResControlExpConfBase):
#     """Creates the configuration panel for the Results - Control Experiments
#         dialog when called from the ProtProf Tab

#         Parameters
#         ----------
#         cParent : wx.Widget
#             Parent of the panel
#         cTopParent : wx.Widget
#             Top parent window
#         cNColF : int
#             Total number of columns present in the Data File

#         Attributes
#         ----------
#         cN: int
#             Number of Labels. 
#         cName : str
#             Unique name of the panel
#         cStLabel: dict
#             Full name for the Labels. Keys are 1 to N values the text for 
#             the labels e.g. {1: 'Conditions', 2: 'Relevant Points'}
#         cTTTotalFields: str
#             Tooltip for the Total Fields.
#         dAddWidgets: dict
#             Methods to add the widgets depending on the control type.
#         mNoCondRP: str
#             Error message
#         mNoControl: str
#             Error message
#         rControlVal : str
#             Value of Control Type in the previous Create Field event.
#     """
#     #region -----------------------------------------------------> Class setup
#     cName = config.npResControlExpProtProf
#     #endregion --------------------------------------------------> Class setup

#     #region --------------------------------------------------> Instance setup
#     def __init__(
#         self, cParent: wx.Window, cTopParent: wx.Window, cNColF: int
#         ) -> None:
#         """ """
#         #region -------------------------------------------------> Check Input
        
#         #endregion ----------------------------------------------> Check Input

#         #region -----------------------------------------------> Initial Setup
#         #------------------------------> Needed by ResControlExpConfBase
#         self.cN = 2
#         self.cStLabel = { # Keys runs in range(1, N+1)
#             1 : f"{config.lStProtProfCond}:",
#             2 : f"{config.lStProtProfRP}:",
#         }
#         self.cLabelText = { # Keys runs in range(1, N+1)
#             1 : 'C',
#             2 : 'RP',
#         }
#         #------------------------------> 
#         self.dAddWidget = {
#             config.oControlTypeProtProf['OC']   : self.AddWidget_OC,
#             config.oControlTypeProtProf['OCC']  : self.AddWidget_OCC,
#             config.oControlTypeProtProf['OCR']  : self.AddWidget_OCR,
#             config.oControlTypeProtProf['Ratio']: self.AddWidget_Ratio,
#         }
#         #------------------------------> Tooltips
#         self.cTTTotalField = [
#             f'Set the number of {self.cStLabel[1][0:-2]}.',
#             f'Set the number of {self.cStLabel[2][0:-2]}.',
#         ]
#         #--------------> Control type from previous call to Setup Fields
#         self.rControlVal = ''
#         #------------------------------> Error messages
#         self.mNoCondRP = (
#             f"Both {self.cStLabel[1][:-1]} and {self.cStLabel[2][:-1]} must be "
#             f"defined."
#         )
#         self.mNoControl = (f"The Control Type must defined.")
#         #------------------------------> Super init
#         super().__init__(cParent, self.cName, cTopParent, cNColF)
#         #------------------------------> Choices
#         self.cControlTypeO = [x for x in config.oControlTypeProtProf.values()]
#         #endregion --------------------------------------------> Initial Setup

#         #region --------------------------------------------------------> Menu
        
#         #endregion -----------------------------------------------------> Menu

#         #region -----------------------------------------------------> Widgets
#         #------------------------------> wx.StaticText
#         self.wStControl = wx.StaticText(
#             self.wSwLabel, label='Control Experiment:')
#         self.wStControlT = wx.StaticText(
#             self.wSwLabel, label=config.lStCtrlType)
#         #------------------------------> wx.ComboBox
#         self.wCbControl = wx.ComboBox(
#             self.wSwLabel, 
#             style     = wx.CB_READONLY,
#             choices   = self.cControlTypeO,
#             validator = dtsValidator.IsNotEmpty(),
#         )
#         #endregion --------------------------------------------------> Widgets

#         #region -----------------------------------------------------> Tooltip
#         self.wStControl.SetToolTip(
#             'Set the Type and Name of the control experiment.')
#         self.wStControlT.SetToolTip('Set the Type of the control experiment.')
#         #endregion --------------------------------------------------> Tooltip
        
#         #region ------------------------------------------------------> Sizers
#         #------------------------------> 
#         self.sSWLabelControl = wx.BoxSizer(wx.HORIZONTAL)
#         self.sSWLabelControl.Add(
#             self.wStControl, 
#             0, 
#             wx.ALIGN_CENTER_VERTICAL|wx.ALL, 
#             5,
#         )
#         self.sSWLabelControl.Add(
#             self.wStControlT, 
#             0, 
#             wx.ALIGN_CENTER_VERTICAL|wx.ALL, 
#             5,
#         )
#         self.sSWLabelControl.Add(
#             self.wCbControl, 
#             0, 
#             wx.EXPAND|wx.ALL, 
#             5,
#         )
#         self.sSWLabelControl.Add(
#             self.wControlN.st, 
#             0, 
#             wx.ALIGN_CENTER_VERTICAL|wx.ALL, 
#             5,
#         )
#         self.sSWLabelControl.Add(
#             self.wControlN.tc, 
#             1, 
#             wx.EXPAND|wx.ALL,
#             5,
#         )
#         #------------------------------> 
#         self.sSWLabelMain.Add(
#             self.sSWLabelControl, 
#             0, 
#             wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 
#             5,
#         )
#         #------------------------------> 
#         self.sSizer.Fit(self)
#         #endregion ---------------------------------------------------> Sizers

#         #region --------------------------------------------------------> Bind
#         self.wCbControl.Bind(wx.EVT_COMBOBOX, self.OnControl)
#         #endregion -----------------------------------------------------> Bind

#         #region ---------------------------------------------> Window position
        
#         #endregion ------------------------------------------> Window position
        
#         #region -----------------------------------------------> Initial State
#         self.SetInitialState()
#         #endregion --------------------------------------------> Initial State
        
#     #---
#     #endregion -----------------------------------------------> Instance setup

#     #region ---------------------------------------------------> Event methods
#     def OnControl(self, event: wx.CommandEvent) -> bool:
#         """Enable/Disable the Control name when selecting control type
    
#             Parameters
#             ----------
#             event:wx.Event
#                 Information about the event
            
    
#             Returns
#             -------
#             True
#         """
#         #region ---------------------------------------------------> Get value
#         control = self.wCbControl.GetValue()
#         #endregion ------------------------------------------------> Get value
        
#         #region ------------------------------------------------------> Action
#         if control == config.oControlTypeProtProf['Ratio']:
#             self.wControlN.tc.SetValue('None')
#             self.wControlN.tc.SetEditable(False)
#         else:
#             self.wControlN.tc.SetEditable(True)
#         #endregion ---------------------------------------------------> Action
        
#         return True
#     #---
    
#     def OnCreate(self, event: wx.CommandEvent) -> bool:
#         """Create the widgets in the white panel
    
#             Parameters
#             ----------
#             event:wx.Event
#                 Information about the event
            
    
#             Returns
#             -------
#             True
#         """
#         #region -------------------------------------------------> Check input
#         #------------------------------> Labels
#         n = []
#         for k in range(1, self.cN+1):
#             n.append(len(self.rTcDict[k]))
#         if all(n):
#             pass
#         else:
#             dtscore.Notification('errorF', msg=self.mNoCondRP, parent=self)
#             return False
#         #------------------------------> Control
#         if self.wCbControl.GetValidator().Validate()[0]:
#             pass
#         else:
#             dtscore.Notification('errorF', msg=self.mNoControl, parent=self)
#             return False
#         #endregion ----------------------------------------------> Check input
        
#         #region ---------------------------------------------------> Variables
#         control = self.wCbControl.GetValue()
        
#         if control == config.oControlTypeProtProf['OCR']:
#             Nc   = n[0]     # Number of rows of tc needed
#             Nr   = n[1] + 1 # Number of tc needed for each row
#             NCol = n[1] + 2 # Number of columns in the sizer
#             NRow = n[0] + 1 # Number of rows in the sizer
#         elif control == config.oControlTypeProtProf['Ratio']:
#             Nc   = n[0]     
#             Nr   = n[1]     
#             NCol = n[1] + 1 
#             NRow = n[0] + 1 
#         else:
#             Nc   = n[0] + 1
#             Nr   = n[1]
#             NCol = n[1] + 1
#             NRow = n[0] + 2
#         #endregion ------------------------------------------------> Variables
        
#         #region -------------------------------------------> Remove from sizer
#         self.sSWMatrix.Clear(delete_windows=False)
#         #endregion ----------------------------------------> Remove from sizer
        
#         #region --------------------------------> Create/Destroy wx.StaticText
#         #------------------------------> Destroy
#         for k, v in self.rLbDict.items():
#             for j in range(0, len(v)):
#                 v[-1].Destroy()
#                 v.pop()
#         #------------------------------> Create
#         #--------------> Labels
#         for k, v in self.rTcDict.items():
#             #--------------> New row
#             row = []
#             #--------------> Fill row
#             for j in v:
#                 row.append(
#                     wx.StaticText(
#                         self.wSwMatrix,
#                         label = j.GetValue(),
#                     )
#                 )
#             #--------------> Assign
#             self.rLbDict[k] = row
#         #--------------> Control
#         self.rLbDict['Control'] = [
#             wx.StaticText(
#                 self.wSwMatrix,
#                 label = self.wControlN.tc.GetValue(),
#             )
#         ]
#         if control == config.oControlTypeProtProf['Ratio']:
#             self.rLbDict['Control'][0].Hide()
#         else:
#             pass
#         #endregion -----------------------------> Create/Destroy wx.StaticText
        
#         #region ----------------------------------> Create/Destroy wx.TextCtrl
#         #------------------------------> Widgets
#         for k in range(1, Nc+1):
#             #------------------------------> Get row
#             row = self.rTcDictF.get(k, [])
#             lrow = len(row)
#             #------------------------------> First row is especial
#             if k == 1 and control == config.oControlTypeProtProf['OC']:
#                 if control == self.rControlVal:
#                     continue
#                 else:
#                     #--------------> Destroy old widgets
#                     for j in row:
#                         j.Destroy()
#                     #--------------> New Row and wx.TextCtrl
#                     row = []
#                     row.append(
#                         wx.TextCtrl(
#                             self.wSwMatrix,
#                             size      = self.cSLabel,
#                             validator = self.cVColNumList,
#                         )
#                     )
#                     #--------------> Assign & Continue to next for step
#                     self.rTcDictF[k] = row
#                     continue
#             else:
#                 pass
#             #------------------------------> Create destroy
#             if Nr > lrow:
#                 #-------------->  Create
#                 for j in range(lrow, Nr):
#                     row.append(
#                         wx.TextCtrl(
#                             self.wSwMatrix,
#                             size      = self.cSLabel,
#                             validator = self.cVColNumList,
#                         )
#                     )
#                 #-------------->  Add to dict
#                 self.rTcDictF[k] = row
#             else:
#                 for j in range(Nr, lrow):
#                     #-------------->  Destroy
#                     row[-1].Destroy()
#                     #--------------> Remove from list
#                     row.pop()
#         #------------------------------> Drop keys and destroy from dict
#         dK = [x for x in self.rTcDictF.keys()]
#         for k in dK:
#             if k > Nc:
#                 #--------------> Destroy this widget
#                 for j in self.rTcDictF[k]:
#                     j.Destroy()
#                 #--------------> Remove key
#                 del(self.rTcDictF[k])
#             else:
#                 pass      
#         #------------------------------> Clear value if needed
#         if control != self.rControlVal:
#             for v in self.rTcDictF.values():
#                 for j in v:
#                     j.SetValue('')
#         else:
#             pass      
#         #endregion -------------------------------> Create/Destroy wx.TextCtrl
        
#         #region ------------------------------------------------> Setup Sizers
#         #------------------------------> Adjust size
#         self.sSWMatrix.SetCols(NCol)
#         self.sSWMatrix.SetRows(NRow)
#         #------------------------------> Add widgets
#         self.dAddWidget[control](NCol, NRow)
#         #------------------------------> Grow Columns
#         for k in range(1, NCol):
#             if not self.sSWMatrix.IsColGrowable(k):
#                 self.sSWMatrix.AddGrowableCol(k, 1)
#             else:
#                 pass
#         #------------------------------> Update sizer
#         self.sSWMatrix.Layout()
#         #endregion ---------------------------------------------> Setup Sizers
        
#         #region --------------------------------------------------> Set scroll
#         self.wSwMatrix.SetupScrolling()
#         #endregion -----------------------------------------------> Set scroll
        
#         #region -------------------------------------------> Update controlVal
#         self.rControlVal = control
#         #endregion ----------------------------------------> Update controlVal
        
#         return True
#     #---
#     #endregion ------------------------------------------------> Event Methods
    
#     #region --------------------------------------------------> Manage Methods
#     def AddWidget_OC(self, NCol: int, NRow: int) -> bool:
#         """Add the widget when Control Type is One Control. It is assumed 
#             everything is ready to add the widgets
            
#             Parameters
#             ----------
#             NCol : int
#                 Number of columns in the sizer
#             NRow : int
#                 Number of rows in the sizer 
#         """
#         #region -------------------------------------------------> Control Row
#         self.sSWMatrix.Add(
#             self.rLbDict['Control'][0],
#             0,
#             wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL,
#             5
#         )
#         self.sSWMatrix.Add(
#             self.rTcDictF[1][0],
#             0,
#             wx.EXPAND|wx.ALL,
#             5
#         )
#         for k in range(2, NCol):
#             self.sSWMatrix.AddSpacer(1)
#         #endregion ----------------------------------------------> Control Row
        
#         #region ---------------------------------------------------> RP Labels
#         #--------------> Empty space
#         self.sSWMatrix.AddSpacer(1)
#         #--------------> Labels
#         for k in self.rLbDict[2]:
#             self.sSWMatrix.Add(
#                 k,
#                 0,
#                 wx.ALIGN_CENTER|wx.ALL,
#                 5
#             )
#         #endregion ------------------------------------------------> RP Labels
        
#         #region ------------------------------------------------> Other fields
#         K = 2
#         for k in self.rLbDict[1]:
#             #--------------> Add Label
#             self.sSWMatrix.Add(
#                 k,
#                 0,
#                 wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL|wx.ALL,
#                 5
#             )
#             #--------------> Add tc
#             for j in self.rTcDictF[K]:
#                 self.sSWMatrix.Add(
#                     j,
#                     0,
#                     wx.EXPAND|wx.ALL,
#                     5
#                 )
#             K += 1
#         #endregion ---------------------------------------------> Other fields
        
#         return True
#     #---
    
#     def AddWidget_OCC(self, NCol: int, NRow: int) -> bool:
#         """Add the widget when Control Type is One Control. It is assumed 
#             everything is ready to add the widgets"""
#         #region ---------------------------------------------------> RP Labels
#         self.sSWMatrix.AddSpacer(1)
        
#         for k in self.rLbDict[2]:
#             self.sSWMatrix.Add(
#                 k,
#                 0,
#                 wx.ALIGN_CENTER|wx.ALL,
#                 5
#             )
#         #endregion ------------------------------------------------> RP Labels
        
#         #region -------------------------------------------------> Control Row
#         self.sSWMatrix.Add(
#             self.rLbDict['Control'][0],
#             0,
#             wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL|wx.ALL,
#             5
#         )
        
#         for k in self.rTcDictF[1]:
#             self.sSWMatrix.Add(
#                 k,
#                 0,
#                 wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL,
#                 5
#             )    
#         #endregion ----------------------------------------------> Control Row
        
#         #region --------------------------------------------------> Other Rows
#         for k, v in self.rTcDictF.items():
#             K = k - 2
#             #------------------------------> Skip control row
#             if k == 1:
#                 continue
#             else:
#                 pass
#             #------------------------------> Add Label
#             self.sSWMatrix.Add(
#                 self.rLbDict[1][K],
#                 0,
#                 wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL|wx.ALL,
#                 5
#             )
#             #------------------------------> Add wx.TextCtrl
#             for j in v:
#                 self.sSWMatrix.Add(
#                 j,
#                 0,
#                 wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL,
#                 5
#             ) 
#         #endregion -----------------------------------------------> Other Rows
        
#         return True
#     #---
    
#     def AddWidget_OCR(self, NCol: int, NRow: int) -> bool:
#         """Add the widget when Control Type is One Control. It is assumed 
#             everything is ready to add the widgets"""
#         #region ---------------------------------------------------> RP Labels
#         self.sSWMatrix.AddSpacer(1)
        
#         self.sSWMatrix.Add(
#             self.rLbDict['Control'][0],
#             0,
#             wx.ALIGN_CENTER|wx.ALL,
#             5
#         )
        
#         for k in self.rLbDict[2]:
#             self.sSWMatrix.Add(
#                 k,
#                 0,
#                 wx.ALIGN_CENTER|wx.ALL,
#                 5
#             )
#         #endregion ------------------------------------------------> RP Labels
        
#         #region --------------------------------------------------> Other rows
#         for k, v in self.rTcDictF.items():
#             #--------------> 
#             K = int(k) - 1
#             #--------------> 
#             self.sSWMatrix.Add(
#                 self.rLbDict[1][K],
#                 0,
#                 wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL|wx.ALL,
#                 5
#             )
#             #-------------->
#             for j in v:
#                 self.sSWMatrix.Add(
#                     j,
#                     0,
#                     wx.EXPAND|wx.ALL,
#                     5
#                 )
#         #endregion -----------------------------------------------> Other rows
        
#         return True
#     #---
    
#     def AddWidget_Ratio(self, NCol: int, NRow: int) -> bool:
#         """Add the widget when Control Type is Data as Ratios. It is assumed 
#             everything is ready to add the widgets"""
#         #region ---------------------------------------------------> RP Labels
#         self.sSWMatrix.AddSpacer(1)
        
#         for k in self.rLbDict[2]:
#             self.sSWMatrix.Add(
#                 k,
#                 0,
#                 wx.ALIGN_CENTER|wx.ALL,
#                 5
#             )
#         #endregion ------------------------------------------------> RP Labels
        
#         #region --------------------------------------------------> Other rows
#         for k, v in self.rTcDictF.items():
#             #--------------> 
#             K = int(k) - 1
#             #--------------> 
#             self.sSWMatrix.Add(
#                 self.rLbDict[1][K],
#                 0,
#                 wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL|wx.ALL,
#                 5
#             )
#             #-------------->
#             for j in v:
#                 self.sSWMatrix.Add(
#                     j,
#                     0,
#                     wx.EXPAND|wx.ALL,
#                     5
#                 )
#         #endregion -----------------------------------------------> Other rows
        
#         return True
#     #---    
#     #endregion -----------------------------------------------> Manage Methods
# #---


# # class LimProtResControlExp(ResControlExpConfBase):
# #     """Creates the configuration panel for the Results - Control Experiments
# #         dialog when called from the LimProt Tab.

# #         Parameters
# #         ----------
# #         parent : wx.Widget
# #             Parent of the panel
# #         topParent : wx.Widget
# #             Top parent window
# #         NColF : int
# #             Total number of columns present in the Data File

# #         Attributes
# #         ----------
# #         cLabelText : dict
# #             Keys are 1 to cN and values the prefix for the label values. e.g. C  
# #         cN : int
# #             Number of labels excluding control labels.
# #         cStLabel : dict
# #             Keys are 1 to cN and values the text of the labels. e.g. Condition.
# #         cTTTotalField : str
# #             Tooltip for the labels in the top region
# #         mNoBL : str
# #             Error message when the number of bands and/or lanes is not given.
# #         name : str
# #             Name of the panel
# #     """
# #     #region -----------------------------------------------------> Class setup
# #     name = config.npResControlExpLimProt
# #     #endregion --------------------------------------------------> Class setup

# #     #region --------------------------------------------------> Instance setup
# #     def __init__(self, parent, topParent, NColF):
# #         """ """
# #         #region -------------------------------------------------> Check Input
        
# #         #endregion ----------------------------------------------> Check Input

# #         #region -----------------------------------------------> Initial Setup
# #         #------------------------------> Needed by ResControlExpConfBase
# #         self.cN = 2
# #         self.cStLabel = { # Keys runs in range(1, N+1)
# #             1 : f"{config.lStLimProtLane}:",
# #             2 : f"{config.lStLimProtBand}:",
# #         }
# #         self.cLabelText = { # Keys runs in range(1, N+1)
# #             1 : 'L',
# #             2 : 'B',
# #         }
# #         #------------------------------> Tooltips
# #         self.cTTTotalField = [
# #             f'Set the number of {self.cStLabel[1]}.',
# #             f'Set the number of {self.cStLabel[2]}.',
# #         ]  
# #         #------------------------------> Error messages
# #         self.mNoBL = (
# #             f"Both {self.cStLabel[1][:-1]} and {self.cStLabel[2][:-1]} must be "
# #             f"defined."
# #         )
# #         #------------------------------> 
# #         super().__init__(parent, self.name, topParent, NColF)
# #         #endregion --------------------------------------------> Initial Setup

# #         #region --------------------------------------------------------> Menu
        
# #         #endregion -----------------------------------------------------> Menu

# #         #region -----------------------------------------------------> Widgets
        
# #         #endregion --------------------------------------------------> Widgets

# #         #region ------------------------------------------------------> Sizers
# #         #------------------------------> 
# #         self.sizerSWLabelControl = wx.BoxSizer(wx.HORIZONTAL)    
# #         self.sizerSWLabelControl.Add(
# #             self.controlN.st, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5,
# #         )
# #         self.sizerSWLabelControl.Add(
# #             self.controlN.tc, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5,
# #         )
# #         #------------------------------> 
# #         self.sizerSWLabelMain.Add(
# #             self.sizerSWLabelControl, 
# #             0, 
# #             wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 
# #             5,
# #         )
# #         #endregion ---------------------------------------------------> Sizers

# #         #region --------------------------------------------------------> Bind
        
# #         #endregion -----------------------------------------------------> Bind

# #         #region ---------------------------------------------> Window position
        
# #         #endregion ------------------------------------------> Window position
        
# #         #region -----------------------------------------------> Initial State
# #         self.SetInitialState()
# #         #endregion --------------------------------------------> Initial State
# #     #---
# #     #endregion -----------------------------------------------> Instance setup

# #     #region ---------------------------------------------------> Class methods
# #     def OnCreate(self, event: wx.CommandEvent) -> bool:
# #         """Create the fields in the white panel. Override as needed.
        
# #             Parameters
# #             ----------
# #             event : wx.Event
# #                 Information about the event.
                
# #             Return
# #             ------
# #             bool
# #         """
# #         #region -------------------------------------------------> Check Input
# #         n = []
# #         #------------------------------> 
# #         for k in range(1, self.cN+1):
# #             n.append(len(self.tcDict[k]))
# #         #------------------------------> 
# #         if all(n):
# #             #------------------------------> Set default value if empty
# #             for k in range(1, self.cN+1):
# #                 for j, tc in enumerate(self.tcDict[k], 1):
# #                     if tc.GetValue().strip() == '':
# #                         tc.SetValue(f'{self.cLabelText[k]}{j}')
# #                     else:
# #                         pass
# #         else:
# #             dtscore.Notification(
# #                 'errorF', msg=self.mNoBL, parent=self,
# #             )
# #             return False
# #         #------------------------------> Control
# #         if self.controlN.tc.GetValue().strip() == '':
# #             self.controlN.tc.SetValue(self.cHControlN)
# #         else:
# #             pass
# #         #endregion ----------------------------------------------> Check Input
        
# #         #region ---------------------------------------------------> Variables
# #         Nl = n[0]
# #         NCol = n[0]+1
# #         Nb = n[1]
# #         NRow = n[1]+2
# #         #endregion ------------------------------------------------> Variables
        
# #         #region -------------------------------------------> Remove from sizer
# #         self.sizerSWMatrix.Clear(delete_windows=False)
# #         #endregion ----------------------------------------> Remove from sizer
        
# #         #region --------------------------------> Create/Destroy wx.StaticText
# #         #------------------------------> Destroy
# #         for k, v in self.lbDict.items():
# #             for j in range(0, len(v)):
# #                 v[-1].Destroy()
# #                 v.pop()
# #         #------------------------------> Create
# #         #--------------> Labels
# #         for k, v in self.tcDict.items():
# #             #--------------> New row
# #             row = []
# #             #--------------> Fill row
# #             for j in v:
# #                 row.append(
# #                     wx.StaticText(
# #                         self.swMatrix,
# #                         label = j.GetValue(),
# #                     )
# #                 )
# #             #--------------> Assign
# #             self.lbDict[k] = row
# #         #--------------> Control
# #         self.lbDict['Control'] = [
# #             wx.StaticText(
# #                 self.swMatrix,
# #                 label = self.controlN.tc.GetValue(),
# #             )
# #         ]
# #         #endregion -----------------------------> Create/Destroy wx.StaticText
        
# #         #region ----------------------------------> Create/Destroy wx.TextCtrl
# #         #------------------------------> Add/Destroy new/old fields
# #         for k in range(1, Nb+2):
# #             #------------------------------> 
# #             row = self.tcDictF.get(k, [])
# #             lrow = len(row)
# #             #------------------------------> Control
# #             if k == 1:
# #                 if lrow:
# #                     continue
# #                 else:
# #                     #------------------------------> 
# #                     row.append(wx.TextCtrl(
# #                         self.swMatrix, 
# #                         size      = self.cSLabel,
# #                         validator = self.cVColNumList,
# #                     ))
# #                     #------------------------------> 
# #                     self.tcDictF[k] = row
# #                     #------------------------------> 
# #                     continue
# #             else:
# #                 pass
# #             #------------------------------> One row for each band
# #             if Nl >= lrow:
# #                 #------------------------------> Create new fields
# #                 for j in range(lrow, Nl):
# #                     #------------------------------> 
# #                     row.append(wx.TextCtrl(
# #                         self.swMatrix, 
# #                         size      = self.cSLabel,
# #                         validator = self.cVColNumList,
# #                     ))
# #                     #------------------------------> 
# #                     self.tcDictF[k] = row
# #             else:
# #                 #------------------------------> Destroy old fields
# #                 for j in range(Nl, lrow):
# #                     row[-1].Destroy()
# #                     row.pop()
# #         #------------------------------> Remove old bands not needed anymore
# #         # Get keys because you cannot iterate and delete keys
# #         dK = [x for x in self.tcDictF.keys()]
# #         #------------------------------> 
# #         for k in dK:
# #             if k > Nb+1:
# #                 #------------------------------> 
# #                 for j in self.tcDictF[k]:
# #                     j.Destroy()
# #                 #------------------------------> 
# #                 del(self.tcDictF[k])
# #             else:
# #                 pass
# #         #endregion -------------------------------> Create/Destroy wx.TextCtrl
        
# #         #region ------------------------------------------------> Setup Sizers
# #         #------------------------------> Adjust size
# #         self.sizerSWMatrix.SetCols(NCol)
# #         self.sizerSWMatrix.SetRows(NRow)
# #         #------------------------------> Add widgets
# #         #--------------> Control row
# #         self.sizerSWMatrix.Add(
# #             self.lbDict['Control'][0],
# #             0,
# #             wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL,
# #             5
# #         )
# #         self.sizerSWMatrix.Add(
# #             self.tcDictF[1][0],
# #             0,
# #             wx.EXPAND|wx.ALL,
# #             5
# #         )
# #         for k in range(2, NCol):
# #             self.sizerSWMatrix.AddSpacer(1)
# #         #--------------> Lane Labels
# #         self.sizerSWMatrix.AddSpacer(1)
# #         for l in self.lbDict[1]:
# #             self.sizerSWMatrix.Add(
# #                 l,
# #                 0,
# #                 wx.ALIGN_CENTER|wx.ALL,
# #                 5
# #             )
# #         #--------------> Bands
# #         for r, l in enumerate(self.lbDict[2], 1):
# #             #--------------> 
# #             self.sizerSWMatrix.Add(
# #                 l,
# #                 0,
# #                 wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL,
# #                 5
# #             )
# #             #--------------> 
# #             for btc in self.tcDictF[r+1]:
# #                 self.sizerSWMatrix.Add(
# #                     btc,
# #                     0,
# #                     wx.EXPAND|wx.ALL,
# #                     5
# #                 )
# #         #------------------------------> Grow Columns
# #         for k in range(1, NCol):
# #             if not self.sizerSWMatrix.IsColGrowable(k):
# #                 self.sizerSWMatrix.AddGrowableCol(k, 1)
# #             else:
# #                 pass
# #         #------------------------------> Update sizer
# #         self.sizerSWMatrix.Layout()
# #         #endregion ---------------------------------------------> Setup Sizers
        
# #         #region --------------------------------------------------> Set scroll
# #         self.swMatrix.SetupScrolling()
# #         #endregion -----------------------------------------------> Set scroll
        
# #         return True
# #     #---
# #     #endregion ------------------------------------------------> Class methods
# # #---
#endregion ----------------------------------------------------------> Classes


