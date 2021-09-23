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


""" Panels of the application"""


#region -------------------------------------------------------------> Imports
import _thread 
import shutil
from pathlib import Path
from typing import Optional, Literal

import pandas as pd
import numpy as np
from statsmodels.stats.multitest import multipletests

import wx
import wx.lib.scrolledpanel as scrolled

import dat4s_core.data.file as dtsFF
import dat4s_core.data.method as dtsMethod
import dat4s_core.exception.exception as dtsException
import dat4s_core.gui.wx.validator as dtsValidator
import dat4s_core.gui.wx.widget as dtsWidget
import dat4s_core.data.statistic as dtsStatistic
import dat4s_core.data.check as dtsCheck

import config.config as config
import gui.dtscore as dtscore
import gui.method as gmethod
import gui.widget as widget
import data.check as check
import data.method as dmethod

if config.typeCheck:
    import pandas as pd
#endregion ----------------------------------------------------------> Imports


#region --------------------------------------------------------> Base Classes
class BaseConfPanel(
    wx.Panel,
    dtsWidget.StaticBoxes, 
    dtsWidget.ButtonOnlineHelpClearAllRun
    ):
    """Creates the skeleton of a configuration panel. This includes the 
        wx.StaticBox, the bottom Buttons, the statusbar and some widgets.
        
        See Notes below for more details.

        Parameters
        ----------
        parent : wx Widget
            Parent of the widgets
        rightDelete : Boolean
            Enables clearing wx.StaticBox input with right click

        Attributes
        ----------
        parent : wx Widget
            Parent of the widgets
        #------------------------------> Configuration
        cEiFile : wxPython extension list
            Extensions for the main input file. Default is config.elData.
        cHiFile : str
            Hint for the main input wx.TextCtrl. Default is config.hTcDataFile.
        cHuFile : str
            Hint for the umpsap file wx.TextCtrl. Default is config.hTcUFile.
        cLColumnBox : str
            Label for the wx.StaticBox in section Columns.
            Default is config.lSbColumn.
        cLDataBox : str
            Label for the wx.StaticBox in section Data preparation.
            Default is config.lSbData.
        cLFileBox : str
            Label for the wx.StaticBox in section Files & Folders
            Default is config.lSBFile.
        cLiFile : str
            Label for the main input data wx.Button. 
            Default is config.lBtnDataFile.
        cLRunBtn : str
            Label for the run wx.Button. Default is config.lBtnRun.
        cLuFile : str
            Label for the output wx.Button. Default is config.lBtnOutFile.
        cLValueBox : str
            Label for the wx.StaticBox in section User-defined values
            Default is config.lSBValue.
        cLImputation : str
            Label for Imputation method. Default is config.lCbImputation.
        cLNormMethod : str
            Data normalization label. Default is config.lCbNormMethod.
        cLTransMethod : str
            Data transformation label. Default is config.lCbTransMethod.
        cMiFile : str
            Mode for selecting the main input file. Default is 'openO'.
        cMuFile : str
            Mode for selecting the umpsap file. Default is 'save'.
        cOImputation : list of str
            Choices for imputation method. Default is config.oImputation.
        cONorm : list of str
            Choice for normalization method. Default is config.oNormMethod.
        cOTrans : list of str
            Choice for transformation method. Default is config.oTransMethod.
        cTTClearAll : str
            Tooltip for the Clear All button. Default is config.ttBtnClearAll.
        cTTHelp : str
            Tooltip for the Help button. Default is config.ttBtnHelpDef.
        cTTiFile : str
            Tooltip for the input file button. Default is config.ttTcDataFile.
        cTTRun : str
            Tooltip for the run button. Default is config.ttBtnRun.
        cTTuFile : str
            Tooltip for the umsap file button. Default is config.ttBtnUFile.
        cTTImputation : str
            Tooltip for Imputation method. Default is config.lCbImputation.
        cTTNormMethod : str
            Tooltip for Normalization method. Default is config.lCbNormMethod.
        cTTTransMethod : str
            Tooltip for Transformation method. Default is config.ttStTrans.
        cViFile : wx.Validator
            Validator for the main input file. 
            Default is dtsValidator.InputFF(fof='file', ext=config.esData)
        cVuFile : wx.Validator
            Validator for the main input file. 
            Default is dtsValidator.OutputFF(fof='file', ext=config.esUMSAP[0])
        #------------------------------> To run the analysis
        changeKey : list of str
            Keys in do whose values will be turned into a str. Default to
            ['iFile', 'uFile].
        d : dict
            Dict with user input. See keys in Child class.
        date : str or None
            Date for the new section in the umsap file.
        dFile : Path
            Full path to copy the given input file if not in Data-Files.
        dfI : pd.DataFrame
            DataFrame for the initial values.
        dfF : pd.DataFrame
            DataFrame as float values and 0 and '' as np.nan
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
        dlg : dtscore.ProgressDialog
            Progress dialog.
        do : dict
            Dict with processed user input. See keys in Child class.
        msgError : Str or None
            Error message to show when analysis fails
        NCol : int
            Number of columns in the main input file - 1. Set when the file is
            read.
        oFolder : Path or None
            Folder to contain the output. Set based on the umsap file path.
        iFileObj : dtsFF.CSVFile or none
            Input Data File Object
        tException : Exception or None
            Exception raised during analysis   
        #------------------------------> Widgets
        iFile : dtsWidget.ButtonTextCtrlFF
            Attributes: btn, tc
        lbI : wx.ListCtrl or None
            Pointer to the default wx.ListCtrl to load Data File content to. 
        lbL : list of wx.ListCtrl
            To clear all wx.ListCtrl in the Tab.
        uFile : dtsWidget.ButtonTextCtrlFF
            Attributes: btn, tc.
        
        Methods
        -------
        CheckInput:
            Check the user input in the widgets created in __init__
        ReadInputFiles:
            Read the input file and create the corresponding file object.
        LoadResults:
            Load the created umsap file. This will reload the opened umsap file 
            if the new information was added to it or load the new umsap file
            just created.
            
        Notes
        -----
        The following attributes must be set in the child class
        name : str
            Unique name of the pane
        cURL : str 
            URL for the Help wx.Button
        cSection : str 
            Section in the UMSAP file. One of the values in config.nameModules 
            or config.nameUtilities
        cLLenLongest : int 
            Length of the longest label in output dict
        cTitlePD : str
            Title for the Progress Dialog shown when running analysis
        cGaugePD : int 
            Number of steps for the wx.Gauge in the Progress Dialog shown when 
            running analysis
    """
    #region -----------------------------------------------------> Class setup
    
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent: wx.Window, rightDelete: bool=True) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.parent = parent
        #------------------------------> Labels
        self.cLRunBtn      = getattr(self, 'cLRunBtn', config.lBtnRun)
        self.cLuFile       = getattr(self, 'cLuFile', config.lBtnUFile)
        self.cLiFile       = getattr(self, 'cLiFile', config.lBtnDataFile)
        self.cLFileBox     = getattr(self, 'cLFileBox', config.lSbFile)
        self.cLDataBox     = getattr(self, 'cLDataBox', config.lSbData)
        self.cLValueBox    = getattr(self, 'cLValueBox', config.lSbValue)
        self.cLColumnBox   = getattr(self, 'cLColumnBox', config.lSbColumn)
        self.cLNormMethod  = getattr(self, 'cLNormMethod', config.lCbNormMethod)
        self.cLTransMethod = getattr(
            self, 'cLTransMethod', config.lCbTransMethod)
        self.cLImputation = getattr(self, 'cLImputation', config.lCbImputation)
        #------------------------------> Choices
        self.cONorm = getattr(self, 'cONorm', list(config.oNormMethod.values()))
        self.cOTrans = getattr(
            self, 'cOTrans', list(config.oTransMethod.values()),
        )
        self.cOImputation = getattr(
            self, 'cOImputation', list(config.oImputation.values()),
        )
        #------------------------------> Hints
        self.cHuFile = getattr(self, 'cHuFile', config.hTcUFile)
        self.cHiFile = getattr(self, 'cHiFile', config.hTcDataFile)
        #------------------------------> Tooltips
        self.cTTuFile       = getattr(self, 'cTTuFile', config.ttBtnUFile)
        self.cTTiFile       = getattr(self, 'cTTiFile', config.ttBtnDataFile)
        self.cTTHelp        = getattr(self, 'cTTHelp', config.ttBtnHelpDef)
        self.cTTClearAll    = getattr(self, 'cTTClearAll', config.ttBtnClearAll)
        self.cTTRun         = getattr(self, 'cTTRun', config.ttBtnRun)
        self.cTTNormMethod  = getattr(self, 'cTTNormMethod', config.ttStNorm)
        self.cTTTransMethod = getattr(self, 'cTTTransMethod', config.ttStTrans)
        self.cTTImputation  = getattr(
            self, 'cTTImputation', config.ttStImputation,)
        #------------------------------> Extensions
        self.cEiFile = getattr(self, 'ciFileE', config.elData)
        #------------------------------> Mode
        self.cMiFile = getattr(self, 'cMiFile', 'openO')
        self.cMuFile = getattr(self, 'cMuFile', 'save')
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
        #------------------------------> This is needed to handle Data File 
        # content load to the wx.ListCtrl in Tabs with multiple panels
        #--------------> Default wx.ListCtrl to load data file content
        self.lbI = None 
        #--------------> List to use just in case there are more than 1 
        self.lbL = [self.lbI]
        #------------------------------> Needed to Run the analysis
        #--------------> Dict with the user input as given
        self.d = {}
        #--------------> Dict with the processed user input
        self.do = {} 
        #--------------> Error message and exception to show in self.RunEnd
        self.msgError   = None 
        self.tException = None
        #--------------> pd.DataFrames for:
        self.dfI  = None # Initial and
        self.dfF  = None # Data as float and 0 and '' values as np.nan
        self.dfE  = None # Exclude entries by some parameter
        self.dfS  = None # Exclude entries by Score value
        self.dfT  = None # Transformed values
        self.dfN  = None # Normalized Values
        self.dfIm = None # Imputed values
        self.dfR  = None # Results values
        #--------------> date for umsap file
        self.date = None
        #--------------> folder for output
        self.oFolder = None
        #--------------> input file for directing repeating analysis from
        # file copied to oFolder
        self.dFile   = None
        #--------------> Obj for the input data file
        self.iFileObj = None
        #------------------------------> 
        self.changeKey = getattr(self, 'changeKey', ['iFile', 'uFile'])
        #------------------------------> Parent init
        wx.Panel.__init__(self, parent, name=self.name)

        dtsWidget.ButtonOnlineHelpClearAllRun.__init__(
            self, self, self.cURL, labelR = self.cLRunBtn,
        )

        dtsWidget.StaticBoxes.__init__(self, self, 
            labelF      = self.cLFileBox,
            labelD      = self.cLDataBox,
            labelV      = self.cLValueBox,
            labelC      = self.cLColumnBox,
            rightDelete = rightDelete,
        )
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.uFile = dtsWidget.ButtonTextCtrlFF(self.sbFile,
            btnLabel   = self.cLuFile,
            tcHint     = self.cHuFile,
            mode       = self.cMuFile,
            ext        = config.elUMSAP,
            tcStyle    = wx.TE_READONLY,
            validator  = self.cVuFile,
            ownCopyCut = True,
        )
        self.uFile.btn.SetToolTip(self.cTTuFile)
        
        self.iFile = dtsWidget.ButtonTextCtrlFF(self.sbFile,
            btnLabel   = self.cLiFile,
            tcHint     = self.cHiFile,
            ext        = self.cEiFile,
            mode       = self.cMiFile,
            tcStyle    = wx.TE_READONLY|wx.TE_PROCESS_ENTER,
            validator  = self.cViFile,
            ownCopyCut = True,
        )
        self.iFile.btn.SetToolTip(self.cTTiFile)
        
        self.normMethod = dtsWidget.StaticTextComboBox(
            self.sbData, 
            label     = self.cLNormMethod,
            choices   = self.cONorm,
            validator = dtsValidator.IsNotEmpty(),
        )
        
        self.transMethod = dtsWidget.StaticTextComboBox(
            self.sbData, 
            label     = self.cLTransMethod,
            choices   = self.cOTrans,
            validator = dtsValidator.IsNotEmpty(),
        )
        
        self.imputationMethod = dtsWidget.StaticTextComboBox(
            self.sbData, 
            label     = self.cLImputation,
            choices   = self.cOImputation,
            validator = dtsValidator.IsNotEmpty(),
        )
        #endregion --------------------------------------------------> Widgets
        
        #region -----------------------------------------------------> Tooltip
        self.btnHelp.SetToolTip(self.cTTHelp)
        self.btnClearAll.SetToolTip(self.cTTClearAll)
        self.btnRun.SetToolTip(self.cTTRun)
        self.normMethod.st.SetToolTip(self.cTTNormMethod)
        self.transMethod.st.SetToolTip(self.cTTTransMethod)
        self.imputationMethod.st.SetToolTip(self.cTTImputation)
        #endregion --------------------------------------------------> Tooltip
        
        #region ------------------------------------------------------> Sizers
        self.sizersbFileWid.Add(
            self.uFile.btn,
            pos    = (0,0),
            flag   = wx.EXPAND|wx.ALL,
            border = 5
        )
        self.sizersbFileWid.Add(
            self.uFile.tc,
            pos    = (0,1),
            flag   = wx.EXPAND|wx.ALL,
            border = 5
        )
        self.sizersbFileWid.Add(
            self.iFile.btn,
            pos    = (1,0),
            flag   = wx.EXPAND|wx.ALL,
            border = 5
        )
        self.sizersbFileWid.Add(
            self.iFile.tc,
            pos    = (1,1),
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
            self.transMethod.st,
            pos    = (0,1),
            flag   = wx.ALL|wx.ALIGN_CENTER,
            border = 5,
        )
        self.sizersbDataWid.Add(
            self.transMethod.cb,
            pos    = (0,2),
            flag   = wx.ALL|wx.EXPAND,
            border = 5,
        )
        self.sizersbDataWid.Add(
            self.normMethod.st,
            pos    = (0,3),
            flag   = wx.ALL|wx.ALIGN_CENTER,
            border = 5,
        )
        self.sizersbDataWid.Add(
            self.normMethod.cb,
            pos    = (0,4),
            flag   = wx.ALL|wx.EXPAND,
            border = 5,
        )
        self.sizersbDataWid.Add(
            self.imputationMethod.st,
            pos    = (0,5),
            flag   = wx.ALL|wx.ALIGN_CENTER,
            border = 5,
        )
        self.sizersbDataWid.Add(
            self.imputationMethod.cb,
            pos    = (0,6),
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

        self.Sizer = wx.BoxSizer(wx.VERTICAL)

        self.Sizer.Add(self.sizersbFile,   0, wx.EXPAND|wx.ALL,       5)
        self.Sizer.Add(self.sizersbData,   0, wx.EXPAND|wx.ALL,       5)
        self.Sizer.Add(self.sizersbValue,  0, wx.EXPAND|wx.ALL,       5)
        self.Sizer.Add(self.sizersbColumn, 0, wx.EXPAND|wx.ALL,       5)
        self.Sizer.Add(self.btnSizer,      0, wx.ALIGN_CENTER|wx.ALL, 5)
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind
        self.iFile.tc.Bind(wx.EVT_TEXT, self.OnIFileLoad)
        self.iFile.tc.Bind(wx.EVT_TEXT_ENTER, self.OnIFileLoad)
        self.uFile.tc.Bind(wx.EVT_TEXT, self.OnUFileChange)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def OnUFileChange(self, event: wx.CommandEvent) -> Literal[True]:
        """Adjust default Path for UMSAP File when an UMSAP file is selected.
    
            Parameters
            ----------
            event: wx.Event
                Information about the event		
        """
        #region -------------------------------------------------> Set defPath
        if (fileP := self.uFile.tc.GetValue()) == '':
            self.iFile.defPath = None
        else:
            #------------------------------> 
            p = Path(fileP).parent / config.fnDataInit
            #------------------------------> 
            if p.exists():
                self.iFile.defPath = p
            else:
                self.iFile.defPath = None
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
        if (fileP := self.iFile.tc.GetValue()) == '':
            return self.LCtrlEmpty()
        else:
            return self.OnIFileEnter('fEvent', fileP)
    #---
    
    def OnIFileEnter(self, event: wx.CommandEvent, fileP: Path) -> bool:
        """Fill the wx.ListCtrl after selecting path to the folder. This is
            called from within self.iFile
    
            Parameters
            ----------
            fileP : Path
                Folder path
                
            Notes
            -----
            Silently ignores the absence of a wx.ListCtrl as self.lbI
        """
        #region -----------------------------------------------> Check for lbI
        if self.lbI is None:
            return True
        else:
            pass
        #endregion --------------------------------------------> Check for lbI
        
        #region ----------------------------------------------------> Del list
        self.LCtrlEmpty()
        #endregion -------------------------------------------------> Del list
        
        #region ---------------------------------------------------> Fill list
        try:
            dtsMethod.LCtrlFillColNames(self.lbI, fileP)
        except Exception as e:
            dtscore.Notification('errorF', msg=str(e), tException=e)
            return False
        #endregion ------------------------------------------------> Fill list
        
        #region -----------------------------------------> Columns in the file
        self.NCol = self.lbI.GetItemCount() - 1
        #endregion --------------------------------------> Columns in the file

        return True
    #---	

    def LCtrlEmpty(self) -> Literal[True]:
        """Clear wx.ListCtrl and NCol 
        
            Notes
            -----
            Helper function to accomodate several wx.ListCtrl in the panel.
        """
        #region -------------------------------------------------> Delete list
        for l in self.lbL:
            l.DeleteAllItems()
        #endregion ----------------------------------------------> Delete list
        
        #region ---------------------------------------------------> Set NCol
        self.NCol = None
        #endregion ------------------------------------------------> Set NCol

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
            existing data.
        """
        #region ---------------------------------------------------> Read File
        if self.do['uFile'].exists():
            try:
                outData = dtsFF.ReadJSON(self.do['uFile'])
            except Exception as e:
                msg = (
                    "It was not possible to read the existing UMSAP file:\n"
                    f'{self.do["uFile"]}')
                raise dtsException.ExecutionError(msg)
        else:
            outData = {}
        #endregion ------------------------------------------------> Read File
        
        #region ------------------------------------------------> Add new data
        if outData.get(self.cSection, False):
                outData[self.cSection][self.date] = dateDict[self.date]
        else:
            outData[self.cSection] = dateDict
        #endregion ---------------------------------------------> Add new data

        return outData
    #---

    def EqualLenLabel(self, label: str) -> str:
        """Add empty space to the end of label to match the length of
            self.cLLenLongest
    
            Parameters
            ----------
            label : str
                Original label
    
            Returns
            -------
            str
                Label with added empty strings at the end to match the length of
                self.cLLenLongest
        """
        return f"{label}{(self.cLLenLongest - len(label))*' '}" 
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
        #region ---------------------------------------------------------> Msg
        msgPrefix = config.lPdWrite
        #endregion ------------------------------------------------------> Msg
        
        #region -----------------------------------------------> Create folder
        #------------------------------> 
        msgStep = msgPrefix + 'Creating needed folders, Data-Steps folder'
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        dataFolder = f"{self.date}_{self.cSection}"
        dataFolder = self.oFolder / config.fnDataSteps / dataFolder
        dataFolder.mkdir(parents=True, exist_ok=True)
        #------------------------------> 
        msgStep = msgPrefix + 'Creating needed folders, Data-Initial folder'
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        dataInit = self.oFolder / config.fnDataInit
        dataInit.mkdir(parents=True, exist_ok=True)
        #endregion --------------------------------------------> Create folder
        
        #region ------------------------------------------------> Data Initial
        msgStep = msgPrefix + 'Data files, Data file'
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        #------------------------------> 
        piFolder = self.do['iFile'].parent
        puFolder = self.do['uFile'].parent / config.fnDataInit
        #------------------------------>
        if not piFolder == puFolder:
            #------------------------------> 
            name = (
                f"{self.date}-{self.do['iFile'].stem}{self.do['iFile'].suffix}")
            self.dFile = puFolder/name
            #------------------------------> 
            shutil.copy(self.do['iFile'], self.dFile)
            #------------------------------> 
            self.d[self.EqualLenLabel(self.cLiFile)] = str(self.dFile)
        else:
            self.dFile = None
        #endregion ---------------------------------------------> Data Initial
        
        #region --------------------------------------------------> Data Steps
        msgStep = msgPrefix + 'Data files, Step by Step Data files'
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        try:
            dtsFF.WriteDFs2CSV(dataFolder, stepDict)
        except Exception as e:
            self.msgError = (
                "It was not possible to create the files with the data for the "
                "intermediate steps of the analysis.")
            self.tException = e
            return False
        #endregion -----------------------------------------------> Data Steps
        
        #region --------------------------------------------------> UMSAP File
        msgStep = msgPrefix + 'Main file'
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        #------------------------------> Create output dict
        dateDict = {
            self.date : {
                'V' : config.dictVersion,
                'I' : self.d,
                'CI': dtsMethod.DictVal2Str(self.do, self.changeKey, new=True),
                'DP': {
                    'dfS' : self.dfS.to_dict(),
                    'dfT' : self.dfT.to_dict(),
                    'dfN' : self.dfN.to_dict(),
                    'dfIm': self.dfIm.to_dict(),
                },
                'R' : dtsMethod.DictTuplesKey2StringKey(self.dfR.to_dict()),
            }
        }
        #------------------------------> Append or not
        try:
            outData = self.SetOutputDict(dateDict)
        except Exception as e:
            self.msgError = ("It was not possible ")
            self.tException = e
            return False
        #------------------------------> Write
        try:
            dtsFF.WriteJSON(self.do['uFile'], outData)
        except Exception as e:
            self.msgError = (
                "It was not possible to write the results of the analysis to "
                "the selected UMSAP file.")
            self.tException = e
            return False
        #endregion -----------------------------------------------> UMSAP File

        return True
    #---
    
    def OnRun(self, event: wx.CommandEvent) -> Literal[True]:
        """ Start analysis of the module/utility

            Parameter
            ---------
            event : wx.Event
                Event information
        """
        #region --------------------------------------------------> Dlg window
        self.dlg = dtscore.ProgressDialog(
            config.winMain, self.cTitlePD, self.cGaugePD,
        )
        #endregion -----------------------------------------------> Dlg window

        #region ------------------------------------------------------> Thread
        _thread.start_new_thread(self.Run, ('test',))
        #endregion ---------------------------------------------------> Thread

        #region ----------------------------------------> Show progress dialog
        self.dlg.ShowModal()
        self.dlg.Destroy()
        #endregion -------------------------------------> Show progress dialog

        return True
    #---
    
    def CheckInput(self) -> bool:
        """Check user input"""
        #region ---------------------------------------------------------> Msg
        msgPrefix = config.lPdCheck
        #endregion ------------------------------------------------------> Msg
        
        #region --------------------------------------------------> UMSAP File
        msgStep = msgPrefix + self.cLuFile
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        a, b = self.uFile.tc.GetValidator().Validate()
        if a:
            pass
        else:
            self.msgError = dtscore.StrSetMessage(
                config.mFileBad.format(b[1], self.cLuFile), b[2],
            )
            return False
        #endregion -----------------------------------------------> UMSAP File
        
        #region --------------------------------------------------> Input File
        msgStep = msgPrefix + self.cLiFile
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        a, b = self.iFile.tc.GetValidator().Validate()
        if a:
            pass
        else:
            self.msgError = dtscore.StrSetMessage(
                config.mFileBad.format(b[1], self.cLiFile), b[2],
            )
            return False
        #endregion -----------------------------------------------> Input File
        
        #region ----------------------------------------------> Transformation
        msgStep = msgPrefix + self.cLTransMethod
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        if self.transMethod.cb.GetValidator().Validate()[0]:
            pass
        else:
            self.msgError = config.mNotEmpty.format(self.cLTransMethod)
            return False
        #endregion -------------------------------------------> Transformation
        
        #region -----------------------------------------------> Normalization
        msgStep = msgPrefix + self.cLNormMethod
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        if self.normMethod.cb.GetValidator().Validate()[0]:
            pass
        else:
            self.msgError = config.mNotEmpty.format(self.cLNormMethod)
            return False
        #endregion --------------------------------------------> Normalization
        
        #region --------------------------------------------------> Imputation
        msgStep = msgPrefix + self.cLImputation
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        if self.imputationMethod.cb.GetValidator().Validate()[0]:
            pass
        else:
            self.msgError = config.mNotEmpty.format(self.cLImputation)
            return False
        #endregion -----------------------------------------------> Imputation
        
        return True
    #---
    
    def ReadInputFiles(self):
        """Read input file and check data"""
        #region ---------------------------------------------------------> Msg
        msgPrefix = config.lPdReadFile
        #endregion ------------------------------------------------------> Msg

        #region ---------------------------------------------------> Data file
        #------------------------------> 
        msgStep = msgPrefix + f"{self.cLiFile}, reading"
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        #------------------------------> 
        try:
            self.iFileObj = dtsFF.CSVFile(self.do['iFile'])
        except dtsException.FileIOError as e:
            self.msgError = str(e)
            self.tException = e
            return False
        #endregion ------------------------------------------------> Data file

        return True
    #---
    
    def LoadResults(self):
        """Load output file"""
        #region ---------------------------------------------------------> Msg
        msgPrefix = config.lPdLoad
        #endregion ------------------------------------------------------> Msg

        #region --------------------------------------------------------> Load
        wx.CallAfter(self.dlg.UpdateStG, msgPrefix)
        
        wx.CallAfter(gmethod.LoadUMSAPFile, fileP=self.do['uFile'])
        #endregion -----------------------------------------------------> Load

        return True
    #---
    #endregion ------------------------------------------------> Class methods
#---


class BaseConfModPanel(BaseConfPanel, widget.ResControl):
    """Base configuration for a panel of a module.

        Parameters
        ----------
        parent : wx Widget
            Parent of the widgets
        rightDelete : Boolean
            Enables clearing wx.StaticBox input with right click

        Attributes
        ----------
        #------------------------------> Configuration
        cLAlpha : str
            Label for the alpha level. Default is config.lStAlpha.
        cLColExtract : str
            Label for Columns to Exctract. Default is config.lStColExtract.
        cLDetectedProt : str
            Label for Detected Proteins. Default is config.lStDetectedProt.
        cLScoreCol : str
            Score column. Default is config.lStScoreCol.
        cLScoreVal : str
            Score value label. Default is config.lStScoreVal.
        cSTc : wx.Size
            Size for the wx.TextCtrl in the panel
        cTTAlpha : str
            Tooltip for alpha level. Default is config.ttStAlpha.
        cTTColExtract : str
            Tooltip for Columns to Extract. Default is config.lStColExtract.
        cTTDetectedProt : str
            Tooltip for Detected Proteins. Default is config.lStDetectedProt.
        cTTScore : str
            Tooltip for Score columns. Default is config.lStScoreCol.
        cTTScoreVal : str
            Tooltip for Score value. Default is config.lStScoreVal.
        #------------------------------> Widgets
        alpha : dtsWidget.StaticTextCtrl
            Attributes: st, tc
        colExtract : dtsWidget.StaticTextCtrl
            Attributes: st, tc.   
        detectedProt : : dtsWidget.StaticTextCtrl
            Attributes: st, tc     
        imputationMethos: dtsWidget.StaticTextComboBox
            Attributes: st, cb
        normMethod : dtsWidget.StaticTextComboBox
            Attributes: st, cb
        score : : dtsWidget.StaticTextCtrl
            Attributes: st, tc
        scoreVal : dtsWidget.StaticTextCtrl
            Attributes: st, tc
        transMethod : dtsWidget.StaticTextComboBox
            Attributes: st, cb   
        - See also widget.ResControl
        
        Methods
        -------
        CheckInput:
            Check the user input in the widgets created in super().__ini__ and 
            in __init__()
    """
    #region -----------------------------------------------------> Class setup
    
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent: wx.Window, rightDelete: bool=True) -> None:
        """ """
        #region -------------------------------------------------> Check Input
        
        #endregion ----------------------------------------------> Check Input

        #region -----------------------------------------------> Initial Setup
        #------------------------------> Label
        self.cLScoreVal = getattr(self, 'cLScoreVal', config.lStScoreVal)
        self.cLAlpha = getattr(self, 'cLAlpha', config.lStAlpha)
        self.cLDetectedProt = getattr(
            self, 'cLDetectedProt', config.lStDetectedProt,
        )
        self.cLScoreCol = getattr(self, 'cLScoreCol', config.lStScoreCol)
        self.cLColExtract = getattr(self, 'cLColExtract', config.lStColExtract)
        #------------------------------> Size
        self.cSTc = getattr(self, 'cSTc', config.sTc)
        #------------------------------> Tooltips
        self.cTTAlpha = getattr(self, 'cTTAlpha', config.ttStAlpha)
        self.cTTScoreVal = getattr(self, 'cTTScoreVal', config.ttStScoreVal)
        self.cTTDetectedProt = getattr(
            self, 'cTTDetectedProtL', config.ttStDetectedProtL,
        )
        self.cTTScore = getattr(self, 'cTTScore', config.ttStScore)
        #------------------------------> __init__
        BaseConfPanel.__init__(self, parent, rightDelete=rightDelete)

        widget.ResControl.__init__(self, self.sbColumn)
        
        #------------------------------> Here because it needs iFile
        self.cTTColExtract = getattr(
            self, 'cTTColExtract', config.ttStColExtract.format(self.cLiFile),
        )
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------------> Menu
        
        #endregion -----------------------------------------------------> Menu

        #region -----------------------------------------------------> Widgets
        self.alpha = dtsWidget.StaticTextCtrl(
            self.sbValue,
            stLabel   = self.cLAlpha,
            tcSize    = self.cSTc,
            validator = dtsValidator.NumberList(
                numType = 'float',
                nN      = 1,
                vMin    = 0,
                vMax    = 1,
            )
        )

        self.scoreVal = dtsWidget.StaticTextCtrl(
            self.sbValue,
            stLabel   = self.cLScoreVal,
            tcSize    = self.cSTc,
            validator = dtsValidator.NumberList(
                numType = 'float',
                nN      = 1,
            )
        )

        self.detectedProt = dtsWidget.StaticTextCtrl(
            self.sbColumn,
            stLabel   = self.cLDetectedProt,
            tcSize    = self.cSTc,
            validator = dtsValidator.NumberList(
                numType = 'int',
                nN      = 1,
                vMin    = 0,
            )
        )

        self.score = dtsWidget.StaticTextCtrl(
            self.sbColumn,
            stLabel   = self.cLScoreCol,
            tcSize    = self.cSTc,
            validator = dtsValidator.NumberList(
                numType = 'int',
                nN      = 1,
                vMin    = 0,
            )
        )

        self.colExtract = dtsWidget.StaticTextCtrl(
            self.sbColumn,
            stLabel   = self.cLColExtract,
            tcSize    = self.cSTc,
            validator = dtsValidator.NumberList(
                numType = 'int',
                vMin    = 0,
                sep     = ' ',
                unique  = False,
                opt     = True,
            )
        )
        #endregion --------------------------------------------------> Widgets

        #region -----------------------------------------------------> Tooltip
        self.alpha.st.SetToolTip(self.cTTAlpha)
        self.scoreVal.st.SetToolTip(self.cTTScoreVal)
        self.detectedProt.st.SetToolTip(self.cTTDetectedProt)
        self.score.st.SetToolTip(self.cTTScore)
        self.colExtract.st.SetToolTip(self.cTTColExtract)
        #endregion --------------------------------------------------> Tooltip
        
        #region ------------------------------------------------------> Sizers
        
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind
        
        #endregion -----------------------------------------------------> Bind

        #region ---------------------------------------------> Window position
        
        #endregion ------------------------------------------> Window position
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def CheckInput(self) -> bool:
        """Check user input"""
        #region -------------------------------------------------------> Super
        if super().CheckInput():
            pass
        else:
            return False
        #endregion ----------------------------------------------------> Super
        
        #region ---------------------------------------------------------> Msg
        msgPrefix = config.lPdCheck
        #endregion ------------------------------------------------------> Msg
        
        #region -------------------------------------------------> Score Value
        msgStep = msgPrefix + self.cLScoreVal
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        a, b = self.scoreVal.tc.GetValidator().Validate()
        if a:
            pass
        else:
            self.msgError = dtscore.StrSetMessage(
                config.mNumROne.format(self.cLScoreVal), b[2],
            )
            return False
        #endregion ----------------------------------------------> Score Value
        
        #region -------------------------------------------------------> Alpha
        msgStep = msgPrefix + self.cLAlpha
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        a, b = self.alpha.tc.GetValidator().Validate()
        if a:
            pass
        else:
            self.msgError = config.mAlphaRange.format(self.cLAlpha)
            return False
        #endregion ----------------------------------------------------> Alpha
        
        #region -------------------------------------------> Detected Proteins
        msgStep = msgPrefix + self.cLDetectedProt
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        a, b = self.detectedProt.tc.GetValidator().Validate(vMax=self.NCol)
        if a:
            pass
        else:
            msg = f"{config.mNumZPlusOne}\n{config.mFileColNum}".format(
                self.cLDetectedProt, self.cLiFile,
            )
            self.msgError = dtscore.StrSetMessage(msg, b[2])
            return False
        #endregion ----------------------------------------> Detected Proteins
        
        #region ------------------------------------------------> Score Column
        msgStep = msgPrefix + self.cLScoreCol
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        a, b = self.score.tc.GetValidator().Validate(vMax=self.NCol)
        if a:
            pass
        else:
            msg = f"{config.mNumZPlusOne}\n{config.mFileColNum}".format(
                self.cLScoreCol, self.cLiFile,
            )
            self.msgError = dtscore.StrSetMessage(msg, b[2])
            return False
        #endregion ---------------------------------------------> Score Column
        
        #region ------------------------------------------> Columns to Extract
        msgStep = msgPrefix + self.cLColExtract
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        a, b = self.colExtract.tc.GetValidator().Validate(vMax=self.NCol)
        if a:
            pass
        else:
            msg = f"{config.mNumZPlusOne}\n{config.mFileColNum}".format(
                self.cLColExtract, self.cLiFile,
            )
            self.msgError = dtscore.StrSetMessage(msg, b[2])
            return False
        #endregion ---------------------------------------> Columns to Extract
        
        #region -----------------------------------------------> Res - Control
        msgStep = msgPrefix + self.cLResControl
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        a, b = self.tcResults.GetValidator().Validate()
        if a:
            pass
        else:
            self.msgError = config.mNotEmpty.format(self.cLResControl)
            return False
        #endregion --------------------------------------------> Res - Control
        
        return True
    #---
    
    def UniqueColumnNumber(self, l: list[wx.TextCtrl]) -> bool:
        """Check l and self.tcResults contains unique numbers. 
        
            See Notes below for more details.
    
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
        msgStep = config.lPdCheck + 'Unique column numbers'
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        #endregion --------------------------------------------------> Message
        
        #region -------------------------------------------------------> Check
        a, b = check.TcUniqueColNumbers(l, self.tcResults)
        if a:
            pass
        else:
            msg = config.mColNumbers.format(config.mColNumbersNoColExtract)
            self.msgError = dtscore.StrSetMessage(msg, b[2])
            return False
        #endregion ----------------------------------------------------> Check
        
        return True
    #---
    #endregion ------------------------------------------------> Class methods
#---


class ResControlExpConfBase(wx.Panel):
    """Parent class for the configuration panel in the dialog Results - Control
        Experiments
        
        See Notes below for more details.

        Parameters
        ----------
        parent : wx.Widget
            Parent of the widgets
        name : str	
            Unique name of the panel
        topParent : wx.Widget
            Top parent window
        NColF : int
            Number of columns in the input file.

        Attributes
        ----------
        topParent : wx.Widget
            Top parent window
        NcolF: int
            Number of columns in the input file minus 1.
        pName: str
            Name of the parent window.
        #------------------------------> Configuration
        cHTotalField : str
            Hint for the total number of required labels. It must be set in the
            child class. Default is '#'.
        cLSetup : str
            Label for the wx.Button in top region. Default is 'Setup Fields'.
        cSSWLabel : wx.Size
            Size for the ScrolledPanel with the label. Default is (670,135).
        cSSWMatrix : wx.Size
            Size for the ScrolledPanel with the fields. Default is (670,670).
        cSTotalField : wx.Size
            Size for the total wx.TextCtrl in top region. Default is (35,22).
        cSLabel : wx.Size
            Size for the labels wx.TextCtrl in top region. Default is (35,22).
        #------------------------------> To manage window
        lbDict : dict of lists of wx.StaticText for user-given labels
            Keys are 1 to N plus 'Control' and values are the lists.
            List of wx.StaticText to show the given user labels in the Field
            region.
        stLabel : list of wx.StaticText
            List of wx.StaticText with the label names. e.g. Conditions
        tcDict : dict of lists of wx.TextCtrl for labels
            Keys are 1 to N and values are lists of wx.TextCtrl for the user 
            given label.
            List of wx.TextCtrl to input the number of labels.
        tcDictF : dict of lists of wx.TextCtrl for fields
            Keys are 1 to NRow and values are lists of wx.TextCtrl for the user
            given column numbers. 
        tcLabel : list of wx.TextCtrl
            To give the number of user defined labels. e.g. 2 Conditions.
        
        Notes
        -----
        The panel is divided in two sections. 
        - Section Label holds information about the label for the experiments 
        and control.
            The number of labels and the name are set in the child class with 
            cStLabel and cN.
            This information is converted to stLabel (name of the label e.g 
            Condition), tcLabel (input of number of each labels) and tcDict 
            (name of the experiment points e.g. Cond1).
        - Section Fields that holds the information about the column numbers
            The name of the experiments is shown with lbDict that is populated 
            from tcDict
            The column numbers are stored in tcDictF.
        #------------------------------> Attributes that must be set on child
        cN : int
            Number of labels excluding control labels.
        cHTotalField : str
            Hint for the total number of required labels.
        cTTTotalField : str
            Tooltip for the labels in the top region
        cStLabel : dict
            Keys are 1 to cN and values the text of the labels. e.g. Condition.
        cLabelText : dict
            Keys are 1 to cN and values the prefix for the label values. e.g. C  
        
        See OnOk method for information about how the column numbers are
        exported to the parent panel.
    """
    #region -----------------------------------------------------> Class setup
    
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent: wx.Window, name: str, topParent: wx.Window, 
        NColF: int) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup        
        self.topParent = topParent
        self.pName     = self.topParent.name
        #------------------------------> 
        self.tcDictF   = {}
        #------------------------------> User given labels
        self.lbDict    = {}
        self.NColF     = NColF - 1
        #------------------------------> Label
        self.cLSetup = getattr(self, 'cLSetup', 'Setup Fields')
        #------------------------------> Hint
        self.cHTotalField = getattr(self, 'cHTotalField', '#')
        #------------------------------> Size
        self.cSSWLabel    = getattr(self, 'cSSWLabel', (670,135))
        self.cSSWMatrix   = getattr(self, 'cSSWMatrix', (670,670))
        self.cSTotalField = getattr(self, 'cSTotalField', (35,22))
        self.cSLabel      = getattr(self, 'cSLabel', (60,22))
        #------------------------------> super()
        super().__init__(parent, name=name)
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------------> Menu
        
        #endregion -----------------------------------------------------> Menu

        #region -----------------------------------------------------> Widgets
        #------------------------------> wx.ScrolledWindow
        self.swLabel  = scrolled.ScrolledPanel(self, size=self.cSSWLabel)
        
        self.swMatrix = scrolled.ScrolledPanel(self, size=self.cSSWMatrix)
        self.swMatrix.SetBackgroundColour('WHITE')
        #------------------------------> wx.StaticText & wx.TextCtrl
        #--------------> Experiment design
        self.stLabel = []
        self.tcLabel = []
        self.tcDict = {}
        for k in range(1, self.cN+1):
            #------------------------------> tcDict key
            self.tcDict[k] = []
            #------------------------------> wx.StaticText
            a = wx.StaticText(self.swLabel, label=self.cStLabel[k])
            a.SetToolTip(self.cTTTotalField[k-1])
            self.stLabel.append(a)
            #------------------------------> wx.TextCtrl for the label
            a = wx.TextCtrl(
                    self.swLabel,
                    size      = self.cSTotalField,
                    name      = str(k),
                    validator = dtsValidator.NumberList(vMin=1, nN=1),
                )
            a.SetHint(self.cHTotalField)
            self.tcLabel.append(a)
        #------------------------------> wx.Button
        self.btnCreate = wx.Button(self, label=self.cLSetup)
        #endregion --------------------------------------------------> Widgets

        #region -----------------------------------------------------> Tooltip
        self.btnCreate.SetToolTip(
            'Create the fields to type the column numbers.'
        )
        #endregion --------------------------------------------------> Tooltip
        
        #region ------------------------------------------------------> Sizers
        #------------------------------> Main Sizer
        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        #------------------------------> Sizers for self.swLabel
        self.sizerSWLabelMain = wx.BoxSizer(wx.VERTICAL)
        self.sizerSWLabel = wx.FlexGridSizer(self.cN,2,1,1)

        self.Add2SWLabel()

        self.sizerSWLabelMain.Add(self.sizerSWLabel, 0, wx.EXPAND|wx.ALL, 5)

        self.swLabel.SetSizer(self.sizerSWLabelMain)
        #------------------------------> Sizer with setup btn
        self.sizerSetup = wx.BoxSizer(wx.VERTICAL)
        self.sizerSetup.Add(self.btnCreate, 0, wx.ALIGN_RIGHT|wx.ALL, 5)
        #------------------------------> Sizer for swMatrix
        self.sizerSWMatrix = wx.FlexGridSizer(1,1,1,1)
        self.swMatrix.SetSizer(self.sizerSWMatrix)
        #------------------------------> All in Sizer
        self.Sizer.Add(self.swLabel,    0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, 5)
        self.Sizer.Add(self.sizerSetup, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
        self.Sizer.Add(self.swMatrix,   1, wx.EXPAND|wx.ALL, 5)
        self.SetSizer(self.Sizer)
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind
        for k in range(0, self.cN):
            self.tcLabel[k].Bind(wx.EVT_KILL_FOCUS, self.OnLabelNumber)

        self.btnCreate.Bind(wx.EVT_BUTTON, self.OnCreate)
        #endregion -----------------------------------------------------> Bind

        #region ---------------------------------------------> Window position
        
        #endregion ------------------------------------------> Window position
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def OnCreate(self, event: wx.CommandEvent) -> Literal[True]:
        """Create the fields in the white panel. Override as needed."""
        return True
    #---

    def OnLabelNumber(self, event: wx.Event) -> bool:
        """Creates fields for names when the total wx.TextCtrl loose focus
    
            Parameters
            ----------
            event : wx.Event
                Information about the event
            
    
            Returns
            -------
            True
        """
        #region -------------------------------------------------> Check input
        for k in range(0, self.cN):
            if self.tcLabel[k].GetValidator().Validate()[0]:
                pass
            else:
                self.tcLabel[k].SetValue("")
                return False
        #endregion ----------------------------------------------> Check input
        
        #region ---------------------------------------------------> Variables
        vals = []
        for k in self.tcLabel:
            vals.append(0 if (x:=k.GetValue()) == '' else int(x))
        vals.sort(reverse=True)
        n = vals[0]
        #endregion ------------------------------------------------> Variables
        
        #region ------------------------------------------------> Modify sizer
        if (N := n + 2) != self.sizerSWLabel.GetCols():
            self.sizerSWLabel.SetCols(N)
        else:
            pass
        #endregion ---------------------------------------------> Modify sizer
        
        #region --------------------------------------> Create/Destroy widgets
        for k in range(0, self.cN):
            K = k + 1
            tN = int(self.tcLabel[k].GetValue())
            lN = len(self.tcDict[k+1])
            if tN > lN:
                #------------------------------> Create new widgets
                for knew in range(lN, tN):
                    KNEW = knew + 1
                    self.tcDict[K].append(
                        wx.TextCtrl(
                            self.swLabel,
                            size  = self.cSLabel,
                            value = f"{self.cLabelText[K]}{KNEW}"
                        )
                    )
            else:
                #------------------------------> Destroy widget
                for knew in range(tN, lN):
                    #------------------------------> Detach
                    self.sizerSWLabel.Detach(self.tcDict[K][-1])
                    #------------------------------> Destroy
                    self.tcDict[K][-1].Destroy()
                    #------------------------------> Remove from list
                    self.tcDict[K].pop()
        #endregion -----------------------------------> Create/Destroy widgets

        #region ------------------------------------------------> Add to sizer
        self.Add2SWLabel()
        #endregion ---------------------------------------------> Add to sizer
        
        #region --------------------------------------------------> Event Skip
        if isinstance(event, str):
            pass
        else:
            event.Skip()
        #endregion -----------------------------------------------> Event Skip
        
        return True
    #---

    def Add2SWLabel(self):
        """Add the widgets to self.sizerSWLabel. It assumes sizer already has 
            the right number of columns and rows. """
        #region ------------------------------------------------------> Remove
        self.sizerSWLabel.Clear(delete_windows=False)
        #endregion ---------------------------------------------------> Remove
        
        #region ---------------------------------------------------------> Add
        for k in range(0, self.cN):
            #------------------------------> 
            K = k + 1
            #------------------------------> Add conf fields
            self.sizerSWLabel.Add(
                self.stLabel[k], 
                0, 
                wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 
                5
            )
            self.sizerSWLabel.Add(
                self.tcLabel[k], 
                0, 
                wx.ALIGN_RIGHT|wx.EXPAND|wx.ALL, 
                5
            )
            #------------------------------> Add user fields
            for tc in self.tcDict[K]:
                self.sizerSWLabel.Add(
                    tc, 
                    0, 
                    wx.EXPAND|wx.ALL, 
                    5
            )
            #------------------------------> Add empty space
            n = self.sizerSWLabel.GetCols()
            l = len(self.tcDict[K]) + 2
            
            if n > l:
                for c in range(l, n):
                    self.sizerSWLabel.AddSpacer(1)
            else:
                pass
        #endregion ------------------------------------------------------> Add

        #region ------------------------------------------------> Setup Sizers
        #------------------------------> Grow Columns
        for k in range(2, n):
            if not self.sizerSWLabel.IsColGrowable(k):
                self.sizerSWLabel.AddGrowableCol(k, 1)
            else:
                pass
        #------------------------------> Update sizer
        self.sizerSWLabel.Layout()
        #endregion ---------------------------------------------> Setup Sizers
        
        #region --------------------------------------------------> Set scroll
        self.swLabel.SetupScrolling()
        #endregion -----------------------------------------------> Set scroll
        
        return True
    #---
    
    def OnOK(self) -> bool:
        """Validate and set the Results - Control Experiments text 
        
            Notes
            -----
            This will set the tcResult in the topParent window to a string like:
            1 2 3, 4 5 6; '', 7-10; 11-14, '' where commas separate tcfields
            in the same row and ; separate rows.
            The following dict will be set in topParent.lbDict
            {
                1             : [values], # First row of labels
                N             : [values], # N row of labels
                'Control'     : 'Name',
                'ControlType' : Control type,
            }
            And topParent.controlType will be also set to the corresponding 
            value
        """
        #region -------------------------------------------------> Check input
        #------------------------------> Variables
        tcList = []
        oText  = ''
        #------------------------------> Individual fields and list of tc
        for v in self.tcDictF.values():
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
                    msg = f"{config.mListNumN0L}\n{config.mFileColNum}".format(
                            'the text fields', 
                            self.topParent.ciFileL,
                        )
                    e = dtsException.ExecutionError(b[2])
                    dtscore.Notification(
                        'errorF', msg=msg, parent=self, tException=e,
                    )
                    j.SetFocus(),
                    return False
            #--------------> Add row delimiter
            oText = f"{oText[0:-2]}; "
        #------------------------------> All cannot be empty
        a, b = dtsCheck.AllTcEmpty(tcList)
        if not a:
            pass
        else:
            msg = "All text fields are empty. Nothing will be done."
            dtscore.Notification('errorF', msg=msg, parent=self)
            return False
        #------------------------------> All unique
        a, b = dtsCheck.UniqueNumbers(tcList, sep=' ')
        if a:
            pass
        else:
            msg = 'There are repeated column numbers in the text fields.'
            e = dtsException.InputError(b[2])
            dtscore.Notification('errorF', msg=msg, parent=self, tException=e)
            return False
        #endregion ----------------------------------------------> Check input
        
        #region -----------------------------------------------> Set tcResults
        self.topParent.tcResults.SetValue(f"{oText[0:-2]}")
        #endregion --------------------------------------------> Set tcResults
        
        #region ----------------------------------------> Set parent variables
        #------------------------------> Labels        
        self.topParent.lbDict = {}
        for k, v in self.lbDict.items():
            self.topParent.lbDict[k] = []
            for j in v:
                self.topParent.lbDict[k].append(j.GetLabel())
                
        #------------------------------> Control type if needed
        if self.pName == 'ProtProfPane' :
            self.topParent.lbDict['ControlType'] = self.controlVal
        else:
            pass
        #endregion -------------------------------------> Set parent variables
        return True
    #---
    
    def SetInitialState(self) -> bool:
        """Set the initial state of the panel. This assumes that the needed
            values in topParent are properly configured.
        """
        #region -------------------------------------------------> Check input
        if (tcFieldsVal := self.topParent.tcResults.GetValue()) != '':
            pass
        else:
            return False
        #endregion ----------------------------------------------> Check input

        #region --------------------------------------------------> Add Labels
        if config.development:
            for k,v in self.topParent.lbDict.items():
                print(str(k)+': '+str(v))
        else:
            pass
        #------------------------------> Set the label numbers
        for k, v in self.topParent.lbDict.items():
            if k != 'Control' and k != 'ControlType':
                self.tcLabel[k-1].SetValue(str(len(v)))
            else:
                pass
        #------------------------------> Create labels fields
        self.OnLabelNumber('test')
        #------------------------------> Fill. 2 iterations needed. Improve
        for k, v in self.topParent.lbDict.items():
            if k != 'Control' and k != 'ControlType':
                for j, t in enumerate(v):
                    self.tcDict[k][j].SetValue(t)
            elif k == 'Control':
                self.tcControl.SetValue(v[0])
            else:
                pass
        #endregion -----------------------------------------------> Add Labels
        
        #region -------------------------------------------------> Set Control
        if self.pName == 'ProtProfPane':
            #------------------------------> 
            cT = self.topParent.lbDict['ControlType']
            self.cbControl.SetValue(cT)
            #------------------------------> 
            if cT == config.oControlTypeProtProf['Ratio']:
                self.tcControl.SetEditable(False)
            else:
                pass
        else:
            pass
        #endregion ----------------------------------------------> Set Control
        
        #region ---------------------------------------------> Create tcFields
        self.OnCreate('test')
        #endregion ------------------------------------------> Create tcFields
        
        #region --------------------------------------------> Add Field Values
        row = tcFieldsVal.split(";")
        for k, r in enumerate(row, start=1):
            fields = r.split(",")
            for j, f in enumerate(fields):
                self.tcDictF[k][j].SetValue(f)
        #endregion -----------------------------------------> Add Field Values
        
        return True
    #---
    #endregion ------------------------------------------------> Class methods
#---
#endregion -----------------------------------------------------> Base Classes


#region -------------------------------------------------------------> Classes
#------------------------------> Panes
class ListCtrlSearchPlot(wx.Panel):
    """Creates a panel with a wx.ListCtrl and below it a wx.SearchCtrl.

        Parameters
        ----------
        parent: wx.Window
            Parent of the panel
        colLabel : list of str or None
            Name of the columns in the wx.ListCtrl. Default is None
        colSize : list of int or None
            Size of the columns in the wx.ListCtlr. Default is None
        data : list of list
            Data for the wx.ListCtrl when in virtual mode. Default is []. 
        style : wx.Style
            Style of the wx.ListCtrl. Default is wx.LC_REPORT.
        tcHint : str
            Hint for the wx.SearchCtrl. Default is ''.

        Attributes
        ----------
        name : str
            Name of the panel. Default is config.npListCtrlSearchPlot.
        lcs : dtsWidget.ListCtrlSearch
    """
    #region -----------------------------------------------------> Class setup
    name = config.npListCtrlSearchPlot
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self, parent: wx.Window, colLabel: Optional[list[str]]=None, 
        colSize: Optional[list[int]]=None, data: list[list]=[],
        style = wx.LC_REPORT, tcHint: str = ''
        ) -> None:
        """ """
        #region -------------------------------------------------> Check Input
        
        #endregion ----------------------------------------------> Check Input

        #region -----------------------------------------------> Initial Setup
        super().__init__(parent, name=self.name)
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------------> Menu
        
        #endregion -----------------------------------------------------> Menu

        #region -----------------------------------------------------> Widgets
        #------------------------------> 
        self.lcs = dtsWidget.ListCtrlSearch(
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
        self.SetSizer(self.lcs.Sizer)
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind
        
        #endregion -----------------------------------------------------> Bind

        #region ---------------------------------------------> Window position
        
        #endregion ------------------------------------------> Window position
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    
    #endregion ------------------------------------------------> Class methods
#---


#------------------------------> Utils
class CorrA(BaseConfPanel):
    """Creates the configuration tab for Correlation Analysis
    
        Parameters
        ----------
        parent : wx Widget
            Parent of the widgets
        dataI : dict or None
            Initial data provided by the user in a previous analysis.
            This contains both I and CI dicts e.g. {'I': I, 'CI': CI}

        Attributes
        ----------
        name : str
            Unique id of the pane in the app
        #------------------------------> Configuration
        cGaugePD : int
            Number of steps needed in hte Progress Dialog.
        cLCorr : str
            Label for the Correlation Method widget. 
            Default is config.lCbCorrMethod.
        cLiListCtrl : str
            Label for the wx.ListCtrl showing the column names in the in the 
            input file. Default is config.lStColIFile.format(self.cLiFile).
        cLoListCtrl : str
            Label for the wx.ListCtrl showing the selected column.
        cOCorrMethod : list of str
            Options for the Correlation Methods. Default is config.oCorrMethod.
        cSection : str
            Section for the output file in the UMSAP file.
        cTitlePD : str
            Title for the progress dialog. Default is config.lnPDCorrA.
        cTTCorr : str
            Tooltip for the Correlation Method. Default is config.ttStTrans.
        cTTHelp : str 
            Tooltip for the Help button. 
            Default is config.ttBtnHelp.format(config.urlCorrA).
        cURL : str
            URL for the Help button.
        #------------------------------> For Analysis
        cLLenLongest : int
            Length of the longest label. 
        cMainData : str
            Name of the file with the correlation coefficient values.
        do : dict
            Dict with the processed user input
            {
                'uFile'      : 'umsap file path',
                'iFile'      : 'data file path',
                'TransMethod': 'transformation method',
                'NormMethod' : 'normalization method',
                'ImpMethod'  : 'imputation method',
                'CorrMethod' : 'correlation method',
                'Column'     : [selected columns as integers],
                'df'         : {
                  'Column' : [cero based list of selected columns],  
                },
            }
        d : dict
            Similar to 'do' but: 
                - No uFile and no df dict
                - With the values given by the user
                - Keys as in the GUI of the tab.
        
        See parent class for more attributes.

        Notes
        -----
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
    
        The Correlation Analysis section in output-file.umsap conteins the 
        information about the calculations, e.g

        {
            'Correlation-Analysis : {
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
    #endregion --------------------------------------------------> Class Setup
    
    #region --------------------------------------------------> Instance setup
    def __init__(self, parent: wx.Window, dataI: Optional[dict]):
        """"""
        #region -----------------------------------------------> Initial setup
        #------------------------------> Needed by BaseConfPanel
        self.name         = 'CorrAPane'
        self.cURL         = config.urlCorrA
        self.cSection     = config.nuCorrA
        self.cLLenLongest = len(config.lCbCorrMethod)
        self.cTitlePD     = config.lnPDCorrA
        self.cGaugePD     = 17
        #------------------------------> Optional configuration
        self.cTTHelp = config.ttBtnHelp.format(config.urlCorrA)
        #------------------------------> Setup attributes in base class 
        super().__init__(parent)
        #------------------------------> Needed to Run
        self.cMainData  = '{}-CorrelationCoefficients-Data.txt'
        #------------------------------> Label
        self.cLCorr      = config.lCbCorrMethod
        self.cLiListCtrl = config.lStColIFile.format(self.cLiFile)
        self.cLoListCtrl = 'Columns to Analyse'
        #------------------------------> Options
        self.cOCorrMethod = list(config.oCorrMethod.values())
        #------------------------------> Tooltips
        self.cTTCorr  = config.ttStCorr
        #endregion --------------------------------------------> Initial setup
        
        #region -----------------------------------------------------> Widgets
        #------------------------------> Values
        self.corrMethod = dtsWidget.StaticTextComboBox(self.sbValue, 
            label     = self.cLCorr,
            choices   = self.cOCorrMethod,
            validator = dtsValidator.IsNotEmpty(),
        )
        self.corrMethod.st.SetToolTip(self.cTTCorr)
        #------------------------------> Columns
        self.stListI = wx.StaticText(
            self.sbColumn, 
            label = self.cLiListCtrl,
        )
        self.stListO = wx.StaticText(
            self.sbColumn, 
            label = self.cLoListCtrl,
        )
        self.lbI = dtscore.ListZebra(self.sbColumn, 
            colLabel        = config.lLCtrlColNameI,
            colSize         = config.sLCtrlColI,
            copyFullContent = True,
        )
        self.lbO = dtscore.ListZebra(self.sbColumn, 
            colLabel        = config.lLCtrlColNameI,
            colSize         = config.sLCtrlColI,
            canPaste        = True,
            canCut          = True,
            copyFullContent = True,
        )
        self.lbL = [
            self.lbI, self.lbO
        ]
        self.addCol = wx.Button(
            self.sbColumn, 
            label = 'Add columns'
        )
        self.addCol.SetBitmap(
            wx.ArtProvider.GetBitmap(wx.ART_GO_FORWARD), 
            dir = wx.RIGHT,
        )
        #endregion --------------------------------------------------> Widgets

        #region -----------------------------------------------------> Tooltip
        self.stListI.SetToolTip(config.ttLCtrlCopyNoMod)
        self.stListO.SetToolTip(config.ttLCtrlPasteMod)
        self.addCol.SetToolTip(
            f"Add selected Columns in the Data File to the list of Columns "
            f"to Analyse. New columns will be added after the last "
            f"selected element in Columns to analyse. Duplicate columns "
            f"are discarded."
        )
        #endregion --------------------------------------------------> Tooltip

        #region ------------------------------------------------------> Sizers
        #------------------------------> Expand Column section
        item = self.Sizer.GetItem(self.sizersbColumn)
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
            self.corrMethod.st,
            pos    = (0,1),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL,
            border = 5,
        )
        self.sizersbValueWid.Add(
            self.corrMethod.cb,
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
            self.stListI,
            pos    = (0,0),
            flag   = wx.ALIGN_CENTRE|wx.ALL,
            border = 5
        )
        self.sizersbColumnWid.Add(
            self.stListO,
            pos    = (0,2),
            flag   = wx.ALIGN_CENTRE|wx.ALL,
            border = 5
        )
        self.sizersbColumnWid.Add(
            self.lbI,
            pos    = (1,0),
            flag   = wx.EXPAND|wx.ALL,
            border = 20
        )
        self.sizersbColumnWid.Add(
            self.addCol,
            pos    = (1,1),
            flag   = wx.ALIGN_CENTER|wx.ALL,
            border = 20
        )
        self.sizersbColumnWid.Add(
            self.lbO,
            pos    = (1,2),
            flag   = wx.EXPAND|wx.ALL,
            border = 20
        )
        self.sizersbColumnWid.AddGrowableCol(0, 1)
        self.sizersbColumnWid.AddGrowableCol(2, 1)
        self.sizersbColumnWid.AddGrowableRow(1, 1)
        #------------------------------> Main Sizer
        self.SetSizer(self.Sizer)
        self.Sizer.Fit(self)
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind
        self.addCol.Bind(wx.EVT_BUTTON, self.OnAdd)
        #endregion -----------------------------------------------------> Bind
    
        #region --------------------------------------------------------> Test
        if config.development:
            import getpass
            user = getpass.getuser()
            if config.cOS == "Darwin":
                self.uFile.tc.SetValue("/Users/" + str(user) + "/TEMP-GUI/BORRAR-UMSAP/umsap-dev.umsap")
                self.iFile.tc.SetValue("/Users/" + str(user) + "/Dropbox/SOFTWARE-DEVELOPMENT/APPS/UMSAP/LOCAL/DATA/UMSAP-TEST-DATA/TARPROT/tarprot-data-file.txt")
            elif config.cOS == 'Windows':
                from pathlib import Path
                self.uFile.tc.SetValue(str(Path('C:/Users/bravo/Desktop/SharedFolders/BORRAR-UMSAP/umsap-dev.umsap')))
                self.iFile.tc.SetValue(str(Path(f'C:/Users/{user}/Dropbox/SOFTWARE-DEVELOPMENT/APPS/UMSAP/LOCAL/DATA/UMSAP-TEST-DATA/TARPROT/tarprot-data-file.txt')))
            else:
                pass
            self.transMethod.cb.SetValue("Log2")
            self.normMethod.cb.SetValue("Median")
            self.imputationMethod.cb.SetValue("Normal Distribution")
            self.corrMethod.cb.SetValue("Pearson")
        else:
            pass
        #endregion -----------------------------------------------------> Test
        
        #region -------------------------------------------------------> DataI
        self.SetInitialData(dataI)
        #endregion ----------------------------------------------------> DataI
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class Methods
    def OnAdd(self, event: 'wx.Event') -> Literal[True]:
        """Add columns to analyse using the button.
    
            Parameters
            ----------
            event : wx.Event
                Event information
        """
        self.lbI.OnCopy('')
        self.lbO.OnPaste('')
        
        return True
    #---

    def SetInitialData(self, dataI: Optional[dict]=None) -> Literal[True]:
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
            self.uFile.tc.SetValue(dataI['CI']['uFile'])
            self.iFile.tc.SetValue(dataI['I']['Data File'])
            #------------------------------> 
            self.transMethod.cb.SetValue(dataI['CI']['TransMethod'])
            self.normMethod.cb.SetValue(dataI['CI']['NormMethod'])
            self.imputationMethod.cb.SetValue(dataI['CI']['ImpMethod'])
            self.corrMethod.cb.SetValue(dataI['CI']['CorrMethod'])
            #------------------------------> 
            if Path(self.iFile.tc.GetValue()).exists:
                #------------------------------> Add columns with the same order
                l = []
                for k in dataI['CI']['Column']:
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
                            self.lbI.SelectList(l)
                            self.OnAdd('')            
                            #------------------------------> 
                            l = [k]
                #------------------------------> Last past
                self.lbI.SelectList(l)
                self.OnAdd('')    
            else:
                pass
        else:
            pass
        
        return True
    #---
    
    #-------------------------------------> Run analysis methods
    def CheckInput(self):
        """Check user input"""
        #region -------------------------------------------------------> Super
        if super().CheckInput():
            pass
        else:
            return False
        #endregion ----------------------------------------------------> Super
        
        #region ---------------------------------------------------------> Msg
        msgPrefix = config.lPdCheck
        #endregion ------------------------------------------------------> Msg
        
        #region -------------------------------------------> Individual Fields        
        #region -------------------------------------------> Correlation
        msgStep = msgPrefix + self.cLCorr
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        if self.corrMethod.cb.GetValidator().Validate()[0]:
            pass
        else:
            self.msgError = config.mNotEmpty.format(self.cLCorr)
            return False
        #endregion ----------------------------------------> Correlation
        
        #region -------------------------------------------> ListCtrl
        msgStep = msgPrefix + self.cLoListCtrl
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        if self.lbO.GetItemCount() > 1:
            pass
        else:
            self.msgError = (
                f"There must be at least two items in {self.cLoListCtrl}."
            )
            return False
        #endregion ----------------------------------------> ListCtrl
        #endregion ----------------------------------------> Individual Fields

        return True
    #---

    def PrepareRun(self):
        """Set variable and prepare data for analysis."""
        
        #region ---------------------------------------------------------> Msg
        msgPrefix = config.lPdPrepare
        #endregion ------------------------------------------------------> Msg

        #region -------------------------------------------------------> Input
        msgStep = msgPrefix + 'User input, reading'
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        
        col = [int(x) for x in self.lbO.GetColContent(0)]
        
        #------------------------------> As given
        self.d = {
            self.EqualLenLabel(self.cLiFile) : (
                self.iFile.tc.GetValue()),
            self.EqualLenLabel(self.cLuFile) : (
                self.uFile.tc.GetValue()),
            self.EqualLenLabel(self.cLTransMethod) : (
                self.transMethod.cb.GetValue()),
            self.EqualLenLabel(self.cLNormMethod) : (
                self.normMethod.cb.GetValue()),
            self.EqualLenLabel(self.cLImputation) : (
                self.imputationMethod.cb.GetValue()),
            self.EqualLenLabel(self.cLCorr) : (
                self.corrMethod.cb.GetValue()),
            self.EqualLenLabel('Selected Columns') : col,
        }

        msgStep = msgPrefix + 'User input, processing'
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        #------------------------------> Dict with all values
        self.do = {
            'uFile'      : Path(self.uFile.tc.GetValue()),
            'iFile'      : Path(self.iFile.tc.GetValue()),
            'TransMethod': self.transMethod.cb.GetValue(),
            'NormMethod' : self.normMethod.cb.GetValue(),
            'ImpMethod'  : self.imputationMethod.cb.GetValue(),
            'CorrMethod' : self.corrMethod.cb.GetValue(),
            'Column'     : col,
            'df'         : {
                'Column' : [x for x in range(0, len(col))]
            }
        }
        #------------------------------> File base name
        self.oFolder = self.do['uFile'].parent
        #------------------------------> Date
        self.date = dtsMethod.StrNow()
        #endregion ----------------------------------------------------> Input
        
        #region -------------------------------------------------------> Print
        if config.development:
            print('d:')
            for k,v in self.d.items():
                print(str(k)+': '+str(v))
            print('')  
            print('do:')
            for k,v in self.do.items():
                if k != 'df':
                    print(str(k)+': '+str(v))
                else:
                    print('df')
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
        #region ---------------------------------------------------------> Msg
        msgPrefix = config.lPdRun
        #endregion ------------------------------------------------------> Msg
        
        #region ------------------------------------------------------> Column
        msgStep = msgPrefix + f"{self.cLiFile}, data type"
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        #------------------------------> 
        self.dfI = self.iFileObj.df.iloc[:,self.do['Column']]
        try:
            #------------------------------> Replace 0 and ''
            self.dfS = dtsMethod.DFReplace(
                self.dfI, [0, ''], np.nan, sel=self.do['df']['Column'],
            )
            #------------------------------> Float
            self.dfS = self.dfS.astype('float')
        except Exception as e:
            self.msgError  = config.mPDDataTypeCol.format(
                self.cLiFile,
                ", ".join(map(str, self.do['df']['Column'])),
            )
            self.tException = e
            return False
        #endregion ---------------------------------------------------> Column
        
        #region ---------------------------------------------> Transaformation
        #------------------------------> Msg
        msgStep = msgPrefix + f"Data transformation"
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        #------------------------------> 
        try:
            self.dfT = dtsStatistic.DataTransformation(
                self.dfS, sel=None, method=self.do['TransMethod'], rep=np.nan,
            )
        except Exception as e:
            self.msgError = str(e)
            self.tException = e
            return False
        #endregion ------------------------------------------> Transaformation
        
        #region -----------------------------------------------> Normalization
        #------------------------------> Msg
        msgStep = msgPrefix + f"Data normalization"
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        #------------------------------> 
        try:
            self.dfN = dtsStatistic.DataNormalization(
                self.dfT, sel=None, method=self.do['NormMethod'],
            )
        except Exception as e:
            self.msgError = str(e)
            self.tException = e
            return False
        #endregion --------------------------------------------> Normalization
        
        #region --------------------------------------------------> Imputation
        #------------------------------> Msg
        msgStep = msgPrefix + f"Data imputation"
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        #------------------------------> 
        try:
            self.dfIm = dtsStatistic.DataImputation(
                self.dfN, sel=None, method=self.do['ImpMethod'],
            )
        except Exception as e:
            self.msgError = str(e)
            self.tException = e
            return False
        #endregion -----------------------------------------------> Imputation

        #region ------------------------------------> Correlation coefficients
        #------------------------------> Msg
        msgStep = msgPrefix + f"Correlation coefficients calculation"
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        #------------------------------> 
        try:
            self.dfR = self.dfIm.corr(method=self.do['CorrMethod'].lower())
        except Exception as e:
            self.msgError = str(e)
            self.tException = e
            return False
        #endregion ---------------------------------> Correlation coefficients

        return True
    #---

    def WriteOutput(self):
        """Write output. Override as needed """
        #region --------------------------------------------------> Data Steps
        stepDict = {
            config.fnInitial.format('01'): self.dfI,
            config.fnFloat.format('02')  : self.dfS,
            config.fnTrans.format('03')  : self.dfT,
            config.fnNorm.format('04')   : self.dfN,
            config.fnImp.format('05')    : self.dfI,
            self.cMainData.format('06')  : self.dfR,
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

    def RunEnd(self):
        """Restart GUI and needed variables"""
        #region ---------------------------------------> Dlg progress dialogue
        if self.msgError is None:
            #--> 
            self.dlg.SuccessMessage(
                config.lPdDone, eTime=f"{config.lPdEllapsed} {self.deltaT}",
            )
        else:
            self.dlg.ErrorMessage(
                config.lPdError,  
                error      = self.msgError,
                tException = self.tException
            )
        #endregion ------------------------------------> Dlg progress dialogue

        #region -------------------------------------------------------> Reset
        self.msgError   = None # Error msg to show in self.RunEnd
        self.tException = None
        self.d          = {} # Dict with the user input as given
        self.do         = {} # Dict with the processed user input
        self.dfI        = None # pd.DataFrames
        self.dfS        = None
        self.dfT        = None
        self.dfN        = None
        self.dfIm       = None
        self.dfR        = None
        self.date       = None # date for corr file
        self.oFolder    = None # folder for output
        self.iFileObj   = None # input file object
        self.corrP      = None # path to the corr file that will be created
        self.deltaT     = None
        #------------------------------> 
        if self.dFile is not None:
            self.iFile.tc.SetValue(str(self.dFile))
        else:
            pass
        #------------------------------> 
        self.dFile = None # Data File copied to Data-Initial
        #endregion ----------------------------------------------------> Reset
    #---
    #endregion ------------------------------------------------> Class Methods
#---


#------------------------------> Modules
class ProtProf(BaseConfModPanel):
    """Creates the Proteome Profiling configuration tab.
    
        See Notes below for more details.

        Parameters
        ----------
        parent: wx.Widget
            Parent of the pane
        dataI : dict or None
            Initial data provided by the user in a previous analysis.
            This contains both I and CI dicts e.g. {'I': I, 'CI': CI}.

        Attributes
        ----------
        name : str
            Name of the pane. Default to config.npProtProf.
        cURL : str
            URL for the online help.
        #------------------------------> Configuration
        cLCorrectP : str
            Label for the P correction field.
        cLExcludeProt : str
            Label for the Exclude Protein field.
        cLGeneName : str
            Label for the Gene Name field.
        cLLenLongest : int
            Length of the longest label in the panel.
        cLRawI : str
            Label for the Intensity field.
        cLSample : str
            Label for Sample field.
        cOCorrectP : list of str
            Options to correct P values.
        cORawI : list of str
            Options for intensity values
        cOSample : list of str
            Options for sample relationship.
        cTTCorrectP : str
            Tooltip for the correction of P values field.
        cTTExcludeProt : str
            Tooltip for the exclude protein field.
        cTTGeneName : str
            Tooltip for the Gene name field.
        cTTHelp : str
            Tooltip for the help button.
        cTTRawI : str
            Tooltip for the intensity field.
        cTTSample : str
            Tooltip for the sample field.
        
        #------------------------------> To Run Analysis
        cColCtrlData : dict
            Keys are control type and values methods to get the Ctrl and 
            Data columns for the given condition and relevant point.
        cGaugePD : int
            Number of steps for the Progress Dialog.
        cMainData : str
            Name of file containing the results in Steps_Data_File.
        cSection : str
            Name of the section. Default to config.nmProtProf.
        cTitlePD : str
            Name of the Progress Dialog window.
        do: dict
            Dictionary with checked user input. Keys are:
            {
                "iFile"      : "Path to input data file",
                "uFile"      : "Path to umsap file.",
                "ScoreVal"   : "Score value threshold",
                "RawI"       : "Raw intensity or not. Boolean",
                "IndS"       : "Independent sampels or not. Boolean,
                "TransMethod": "Transformation method",
                "NormMethod" : "Normalization method",
                "ImpMethod"  : "Imputation method",
                "Alpha"      : "Significance level",
                "CorrectP"   : "Method to correct P values",
                "Cond"       : [List of conditions],
                "RP"         : [List of relevent points],
                "ControlT"   : "Control type",
                "ControlL"   : "Control label",
                "oc": {
                    "DetectedP": "Detected Proteins column. Int",
                    "GeneName" : "Gene name column. Int",
                    "ScoreCol" : "Score column. Int",
                    "ExcludeP" : [List of columns to search for proteins to 
                                exclude. List of int],
                    "ColExtract": [List of columns to extract],
                    "ResCtrl": [List of columns containing the control and 
                                experiments column numbers],
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
                    "ColumnF": [Columns that must contain only float numbers]
                }
            },    
        d: dict
            Dictionary with the user input. Keys are labels in the panel plus:
            {
                config.lStProtProfCond          : [list of conditions],
                config.lStProtProfRP            : [list of relevant points],
                f"Control {config.lStCtrlType}" : "Control Type",
                f"Control {config.lStCtrlName}" : "Control Name",
            }
            
        See Parent classes for more aatributes.
        
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
    
        The Proteome Profiling section in output-file.umsap conteins the 
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
                    'R' : pd.DataFrame (dict) with the calculation results.
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
    name = config.npProtProf
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent, dataI: Optional[dict]):
        """ """
        #region -------------------------------------------------> Check Input
        
        #endregion ----------------------------------------------> Check Input

        #region -----------------------------------------------> Initial Setup
        #------------------------------> Needed by BaseConfPanel
        self.cURL         = config.urlProtProf
        self.cSection     = config.nmProtProf
        self.cLLenLongest = len(config.lStResultCtrl)
        self.cTitlePD     = f"Running {config.nmProtProf} Analysis"
        self.cGaugePD     = 30
        #------------------------------> Optional configuration
        self.cTTHelp = config.ttBtnHelp.format(config.urlProtProf)
        #------------------------------> Base attributes and setup
        super().__init__(parent)
        #------------------------------> Needed to Run
        self.cMainData  = '{}-ProteomeProfiling-Data.txt'
        #------------------------------> Labels
        self.cLCorrectP    = 'P Correction'
        self.cLGeneName    = 'Gene Names'
        self.cLExcludeProt = 'Exclude Proteins'
        self.cLSample      = 'Samples'
        self.cLRawI        = 'Intensities'
        #------------------------------> Choices
        self.cOSample   = list(config.oSamples.values())
        self.cORawI     = list(config.oIntensities.values())
        self.cOCorrectP = list(config.oCorrectP.keys())
        #------------------------------> Tooltips
        self.cTTCorrectP    = config.ttStPCorrection
        self.cTTGeneName    = config.ttStGenName
        self.cTTExcludeProt = config.ttStExcludeProt
        self.cTTSample      = (
            f"Specify if samples are independent or paired.\n"
            f"For example, samples are paired when the same Petri dish is "
            f"used for the control and experiment.")
        self.cTTRawI = (
            f"Specify if intensities are raw intensity values or are already "
            f"expressed as a ratio (SILAC, TMT/iTRAQ).")
        #------------------------------> Dict with methods
        self.cColCtrlData = {
            config.oControlTypeProtProf['OC']   : self.ColCtrlData_OC,
            config.oControlTypeProtProf['OCC']  : self.ColCtrlData_OCC,
            config.oControlTypeProtProf['OCR']  : self.ColCtrlData_OCR,
            config.oControlTypeProtProf['Ratio']: self.ColCtrlData_Ratio,
        }
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------------> Menu
        
        #endregion -----------------------------------------------------> Menu

        #region -----------------------------------------------------> Widgets
        #------------------------------> Values
        self.correctP = dtsWidget.StaticTextComboBox(
            self.sbValue,
            self.cLCorrectP,
            self.cOCorrectP,
            validator = dtsValidator.IsNotEmpty(),
        )
        
        self.sample = dtsWidget.StaticTextComboBox(
            self.sbValue,
            self.cLSample,
            self.cOSample,
            validator = dtsValidator.IsNotEmpty(),
        )
        
        self.rawI = dtsWidget.StaticTextComboBox(
            self.sbValue,
            self.cLRawI,
            self.cORawI,
            validator = dtsValidator.IsNotEmpty(),
        )
        #------------------------------> Columns
        self.geneName = dtsWidget.StaticTextCtrl(
            self.sbColumn,
            stLabel   = self.cLGeneName,
            tcSize    = self.cSTc,
            validator = dtsValidator.NumberList(
                numType = 'int',
                nN      = 1,
                vMin    = 0,
            )
        )
        self.excludeProt = dtsWidget.StaticTextCtrl(
            self.sbColumn,
            stLabel   = self.cLExcludeProt,
            tcSize    = self.cSTc,
            validator = dtsValidator.NumberList(
                numType = 'int',
                sep     = ' ',
                vMin    = 0,
                opt     = True,
            )
        )
        #endregion --------------------------------------------------> Widgets

        #region -----------------------------------------------------> Tooltip
        self.correctP.st.SetToolTip(self.cTTCorrectP)
        self.geneName.st.SetToolTip(self.cTTGeneName)
        self.excludeProt.st.SetToolTip(self.cTTExcludeProt)
        self.sample.st.SetToolTip(self.cTTSample)
        self.rawI.st.SetToolTip(self.cTTRawI)
        #endregion --------------------------------------------------> Tooltip
        
        #region ------------------------------------------------------> Sizers
        #------------------------------> Sizer Values
        self.sizersbValueWid.Add(
            1, 1,
            pos    = (0,0),
            flag   = wx.EXPAND|wx.ALL,
            border = 5,
            span   = (2, 0),
        )
        self.sizersbValueWid.Add(
            self.scoreVal.st,
            pos    = (0,1),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sizersbValueWid.Add(
            self.scoreVal.tc,
            pos    = (0,2),
            flag   = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sizersbValueWid.Add(
            self.alpha.st,
            pos    = (0,3),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sizersbValueWid.Add(
            self.alpha.tc,
            pos    = (0,4),
            flag   = wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sizersbValueWid.Add(
            self.sample.st,
            pos    = (1,1),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sizersbValueWid.Add(
            self.sample.cb,
            pos    = (1,2),
            flag   = wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sizersbValueWid.Add(
            self.correctP.st,
            pos    = (1,3),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sizersbValueWid.Add(
            self.correctP.cb,
            pos    = (1,4),
            flag   = wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sizersbValueWid.Add(
            self.rawI.st,
            pos    = (2,1),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sizersbValueWid.Add(
            self.rawI.cb,
            pos    = (2,2),
            flag   = wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sizersbValueWid.Add(
            1, 1,
            pos    = (0,5),
            flag   = wx.EXPAND|wx.ALL,
            border = 5,
            span   = (2, 0),
        )
        self.sizersbValueWid.AddGrowableCol(0, 1)
        self.sizersbValueWid.AddGrowableCol(5, 1)
        #------------------------------> Sizer Columns
        self.sizersbColumnWid.Add(
            self.detectedProt.st,
            pos    = (0,0),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sizersbColumnWid.Add(
            self.detectedProt.tc,
            pos    = (0,1),
            flag   = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sizersbColumnWid.Add(
            self.geneName.st,
            pos    = (0,2),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sizersbColumnWid.Add(
            self.geneName.tc,
            pos    = (0,3),
            flag   = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sizersbColumnWid.Add(
            self.score.st,
            pos    = (0,4),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sizersbColumnWid.Add(
            self.score.tc,
            pos    = (0,5),
            flag   = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sizersbColumnWid.Add(
            self.excludeProt.st,
            pos    = (1,0),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sizersbColumnWid.Add(
            self.excludeProt.tc,
            pos    = (1,1),
            flag   = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL,
            border = 5,
            span   = (0, 5),
        )
        self.sizersbColumnWid.Add(
            self.colExtract.st,
            pos    = (2,0),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sizersbColumnWid.Add(
            self.colExtract.tc,
            pos    = (2,1),
            flag   = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL,
            border = 5,
            span   = (0, 5),
        )
        self.sizersbColumnWid.Add(
            self.sizerRes,
            pos    = (3,0),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND,
            border = 0,
            span   = (0,6),
        )
        self.sizersbColumnWid.AddGrowableCol(1,1)
        self.sizersbColumnWid.AddGrowableCol(3,1)
        self.sizersbColumnWid.AddGrowableCol(5,1)
        #------------------------------> Main Sizer
        self.SetSizer(self.Sizer)
        self.Sizer.Fit(self)
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind
        
        #endregion -----------------------------------------------------> Bind

        #region --------------------------------------------------------> Test
        if config.development:
            import getpass
            user = getpass.getuser()
            if config.cOS == "Darwin":
                self.uFile.tc.SetValue("/Users/" + str(user) + "/TEMP-GUI/BORRAR-UMSAP/umsap-dev.umsap")
                self.iFile.tc.SetValue("/Users/" + str(user) + "/Dropbox/SOFTWARE-DEVELOPMENT/APPS/UMSAP/LOCAL/DATA/UMSAP-TEST-DATA/PROTPROF/protprof-data-file.txt")
            elif config.cOS == 'Windows':
                from pathlib import Path
                # self.iFile.tc.SetValue(str(Path('C:/Users/bravo/Desktop/SharedFolders/BORRAR-UMSAP/PlayDATA/TARPROT/Mod-Enz-Dig-data-ms.txt')))
                # self.oFile.tc.SetValue(str(Path('C:/Users/bravo/Desktop/SharedFolders/BORRAR-UMSAP/PlayDATA/TARPROT')))
            else:
                pass
            self.scoreVal.tc.SetValue('320')
            self.transMethod.cb.SetValue('Log2')
            self.normMethod.cb.SetValue('Median')
            self.imputationMethod.cb.SetValue('Normal Distribution')
            self.alpha.tc.SetValue('0.05')
            self.sample.cb.SetValue('Independent Samples')
            self.rawI.cb.SetValue('Raw Intensities')
            self.correctP.cb.SetValue('Benjamini - Hochberg')
            self.detectedProt.tc.SetValue('0')
            self.geneName.tc.SetValue('6')   
            self.score.tc.SetValue('39')     
            self.colExtract.tc.SetValue('0 1 2 3 4-10')
            self.excludeProt.tc.SetValue('171 172 173')
            #------------------------------> 
            #--> One Control per Column, 2 Cond and 2 TP
            # self.tcResults.SetValue('105 115 125, 130 131 132; 106 116 126, 101 111 121; 108 118 128, 103 113 123')
            # self.lbDict = {
            #     1            : ['C1', 'C2'],
            #     2            : ['RP1', 'RP2'],
            #     'Control'    : ['TheControl'],
            #     'ControlType': 'One Control per Column',
            # }
            #--> One Control per Row, 1 Cond and 2 TP
            # self.tcResults.SetValue('105 115 125, 106 116 126, 101 111 121')
            # self.lbDict = {
            #     1            : ['DMSO'],
            #     2            : ['30min', '60min'],
            #     'Control'    : ['MyControl'],
            #     'ControlType': 'One Control per Row',
            # }
            #--> One Control 2 Cond and 2 TP
            self.tcResults.SetValue('105 115 125; 106 116 126, 101 111 121; 108 118 128, 103 113 123')
            self.lbDict = {
                1            : ['C1', 'C2'],
                2            : ['RP1', 'RP2'],
                'Control'    : ['1Control'],
                'ControlType': 'One Control',
            }
            #--> Ratio 2 Cond and 2 TP
            self.tcResults.SetValue('106 116 126, 101 111 121; 108 118 128, 103 113 123')
            self.lbDict = {
                1            : ['C1', 'C2'],
                2            : ['RP1', 'RP2'],
                'Control'    : ['1Control'],
                'ControlType': 'Ratio of Intensities',
            }
        else:
            pass
        #endregion -----------------------------------------------------> Test
        
        #region -------------------------------------------------------> DataI
        self.SetInitialData(dataI)
        #endregion ----------------------------------------------------> DataI
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def SetInitialData(self, dataI: Optional[dict]=None) -> Literal[True]:
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
            self.uFile.tc.SetValue(dataI['CI']['uFile'])
            self.iFile.tc.SetValue(dataI['I'][self.cLiFile])
            #------------------------------> Data Preparation
            self.transMethod.cb.SetValue(dataI['I'][self.cLTransMethod])
            self.normMethod.cb.SetValue(dataI['I'][self.cLNormMethod])
            self.imputationMethod.cb.SetValue(dataI['I'][self.cLImputation])
            #------------------------------> Values
            self.scoreVal.tc.SetValue(dataI['I'][self.cLScoreVal])
            self.sample.cb.SetValue(dataI['I'][self.cLSample])
            self.rawI.cb.SetValue(dataI['I'][self.cLRawI])
            self.alpha.tc.SetValue(dataI['I'][self.cLAlpha])
            self.correctP.cb.SetValue(dataI['I'][self.cLCorrectP])
            #------------------------------> Columns
            self.detectedProt.tc.SetValue(dataI['I'][self.cLDetectedProt])
            self.geneName.tc.SetValue(dataI['I'][self.cLGeneName])
            self.score.tc.SetValue(dataI['I'][self.cLScoreCol])
            self.excludeProt.tc.SetValue(dataI['I'][self.cLExcludeProt])
            self.colExtract.tc.SetValue(dataI['I'][self.cLColExtract])
            self.tcResults.SetValue(dataI['I'][self.cLResControl])
            self.lbDict[1] = dataI['I'][config.lStProtProfCond]
            self.lbDict[2] = dataI['I'][config.lStProtProfRP]
            self.lbDict['ControlType'] = dataI['I'][f'Control {config.lStCtrlType}']
            self.lbDict['Control'] = dataI['I'][f"Control {config.lStCtrlName}"]
        else:
            pass
        #endregion ----------------------------------------------> Fill Fields
        
        return True
    #---
    
    #------------------------------> Run methods
    def CheckInput(self):
        """Check user input"""
        #region -------------------------------------------------------> Super
        if super().CheckInput():
            pass
        else:
            return False
        #endregion ----------------------------------------------------> Super
        
        #region ---------------------------------------------------------> Msg
        msgPrefix = config.lPdCheck
        #endregion ------------------------------------------------------> Msg
        
        #region -------------------------------------------> Individual Fields
        #region ------------------------------------------------------> Sample
        msgStep = msgPrefix + self.cLSample
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        if self.sample.cb.GetValidator().Validate()[0]:
            pass
        else:
            self.msgError = config.mNotEmpty.format(self.cLSample)
            return False
        #endregion ---------------------------------------------------> Sample
        
        #region ---------------------------------------------------> Intensity
        msgStep = msgPrefix + self.cLRawI
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        if self.rawI.cb.GetValidator().Validate()[0]:
            pass
        else:
            self.msgError = config.mNotEmpty.format(self.cLRawI)
            return False
        #endregion ------------------------------------------------> Intensity
        
        #region ------------------------------------------------> P Correction
        msgStep = msgPrefix + self.cLCorrectP
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        if self.correctP.cb.GetValidator().Validate()[0]:
            pass
        else:
            self.msgError = config.mNotEmpty.format(self.cLCorrectP)
            return False
        #endregion ---------------------------------------------> P Correction
        
        #region --------------------------------------------------> Gene Names
        msgStep = msgPrefix + self.cLGeneName
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        a, b = self.geneName.tc.GetValidator().Validate(vMax=self.NCol)
        if a:
            pass
        else:
            msg = f"{config.mNumZPlusOne}\n{config.mFileColNum}".format(
                self.cLGeneName, self.cLiFile,
            )
            self.msgError = dtscore.StrSetMessage(msg, b[2])
            return False
        #endregion -----------------------------------------------> Gene Names
        
        #region --------------------------------------------> Exclude Proteins
        msgStep = msgPrefix + self.cLExcludeProt
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        a, b = self.excludeProt.tc.GetValidator().Validate(vMax=self.NCol)
        if a:
            pass
        else:
            msg = f"{config.mNumZPlusOne}\n{config.mFileColNum}".format(
                self.cLExcludeProt, self.cLiFile,
            )
            self.msgError = dtscore.StrSetMessage(msg, b[2])
            return False
        #endregion -----------------------------------------> Exclude Proteins
        #endregion ----------------------------------------> Individual Fields
        
        #region ------------------------------------------------> Mixed Fields
        #region --------------------------------> Raw or Ration of Intensities
        a = self.rawI.cb.GetValue()
        b = self.lbDict['ControlType']
        if a == b == config.oIntensities['RatioI']:
            pass
        elif a != config.oIntensities['RatioI'] and b != config.oIntensities['RatioI']:
            pass
        else:
            self.msgError = (
                f'The values for {self.cLRawI} ({self.rawI.cb.GetValue()}) '
                f'and Control Type ({self.lbDict["ControlType"]}) are '
                f'incompatible with each other.'
            )
            return False
        #endregion -----------------------------> Raw or Ration of Intensities
        
        #region ---------------------------------------> Unique Column Numbers
        #------------------------------> 
        l = [self.detectedProt.tc, self.geneName.tc, self.score.tc, 
            self.excludeProt.tc]
        #------------------------------> 
        if self.UniqueColumnNumber(l):
            pass
        else:
            return False
        #endregion ------------------------------------> Unique Column Numbers
        #endregion ---------------------------------------------> Mixed Fields
        
        return True
    #---
    
    def PrepareRun(self):
        """Set variable and prepare data for analysis."""
        
        #region ---------------------------------------------------------> Msg
        msgPrefix = config.lPdPrepare
        #endregion ------------------------------------------------------> Msg

        #region -------------------------------------------------------> Input
        msgStep = msgPrefix + 'User input, reading'
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        #------------------------------> As given
        self.d = {
            self.EqualLenLabel(self.cLiFile) : (
                self.iFile.tc.GetValue()),
            self.EqualLenLabel(self.cLuFile) : (
                self.uFile.tc.GetValue()),
            self.EqualLenLabel(self.cLScoreVal) : (
                self.scoreVal.tc.GetValue()),
            self.EqualLenLabel(self.cLSample) : (
                self.sample.cb.GetValue()),
            self.EqualLenLabel(self.cLRawI) : (
                self.rawI.cb.GetValue()),
            self.EqualLenLabel(self.cLTransMethod) : (
                self.transMethod.cb.GetValue()),
            self.EqualLenLabel(self.cLNormMethod) : (
                self.normMethod.cb.GetValue()),
            self.EqualLenLabel(self.cLImputation) : (
                self.imputationMethod.cb.GetValue()),
            self.EqualLenLabel(self.cLAlpha) : (
                self.alpha.tc.GetValue()),
            self.EqualLenLabel(self.cLCorrectP) : (
                self.correctP.cb.GetValue()),
            self.EqualLenLabel(self.cLDetectedProt) : (
                self.detectedProt.tc.GetValue()),
            self.EqualLenLabel(self.cLGeneName) : (
                self.geneName.tc.GetValue()),
            self.EqualLenLabel(self.cLScoreCol) : (
                self.score.tc.GetValue()),
            self.EqualLenLabel(self.cLExcludeProt) : (
                self.excludeProt.tc.GetValue()),
            self.EqualLenLabel(self.cLColExtract) : (
                self.colExtract.tc.GetValue()),
            self.EqualLenLabel(config.lStProtProfCond) : (
                self.lbDict[1]),
            self.EqualLenLabel(config.lStProtProfRP) : (
                self.lbDict[2]),
            self.EqualLenLabel(f"Control {config.lStCtrlType}") : (
                self.lbDict['ControlType']),
            self.EqualLenLabel(f"Control {config.lStCtrlName}") : (
                self.lbDict['Control']),
            self.EqualLenLabel(self.cLResControl): (
                self.tcResults.GetValue()),
        }
        #------------------------------> Dict with all values
        #--------------> 
        msgStep = msgPrefix + 'User input, processing'
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        #--------------> 
        detectedProt = int(self.detectedProt.tc.GetValue())
        geneName     = int(self.geneName.tc.GetValue())
        scoreCol     = int(self.score.tc.GetValue())
        excludeProt  = dtsMethod.Str2ListNumber(
            self.excludeProt.tc.GetValue(), sep=' ',
        )
        colExtract = dtsMethod.Str2ListNumber(
            self.colExtract.tc.GetValue(), sep=' ',
        )
        resctrl       = dmethod.ResControl2ListNumber(self.tcResults.GetValue())
        resctrlFlat   = dmethod.ResControl2Flat(resctrl)
        resctrlDF     = dmethod.ResControl2DF(resctrl, 2+len(excludeProt)+1)
        resctrlDFFlat = dmethod.ResControl2Flat(resctrlDF)
        #--------------> 
        self.do  = {
            'iFile'      : Path(self.iFile.tc.GetValue()),
            'uFile'      : Path(self.uFile.tc.GetValue()),
            'ScoreVal'   : float(self.scoreVal.tc.GetValue()),
            'RawI'       : True if self.rawI.cb.GetValue() == config.oIntensities['RawI'] else False,
            'IndS'       : True if self.sample.cb.GetValue() == config.oSamples['IS'] else False,
            'NormMethod' : self.normMethod.cb.GetValue(),
            'TransMethod': self.transMethod.cb.GetValue(),
            'ImpMethod'  : self.imputationMethod.cb.GetValue(),
            'Alpha'      : float(self.alpha.tc.GetValue()),
            'CorrectP'   : self.correctP.cb.GetValue(),
            'Cond'       : self.lbDict[1],
            'RP'         : self.lbDict[2],
            'ControlT'   : self.lbDict['ControlType'],
            'ControlL'   : self.lbDict['Control'],
            'oc'         : {
                'DetectedP' : detectedProt,
                'GeneName'  : geneName,
                'ScoreCol'  : scoreCol,
                'ExcludeP'  : excludeProt,
                'ColExtract': colExtract,
                'ResCtrl'   : resctrl,
                'Column'    : (
                    [geneName, detectedProt, scoreCol] 
                    + excludeProt 
                    + resctrlFlat
                ),
            },
            'df' : {
                'DetectedP'  : 0,
                'GeneName'   : 1,
                'ScoreCol'   : 2,
                'ExcludeP'   : [2+x for x in range(1, len(excludeProt)+1)],
                'ResCtrl'    : resctrlDF,
                'ResCtrlFlat': resctrlDFFlat,
                'ColumnF'    : [2] + resctrlDFFlat,
            },
        }
        #------------------------------> File base name
        self.oFolder = self.do['uFile'].parent
        #------------------------------> Date
        self.date = dtsMethod.StrNow()
        #endregion ----------------------------------------------------> Input

        #region -------------------------------------------------> Print d, do
        if config.development:
            print('')
            print('self.d:')
            for k,v in self.d.items():
                print(str(k)+': '+str(v))
            print('')
            print('self.do')
            for k,v in self.do.items():
                if k in ['oc', 'df']:
                    print(k)
                    for j,w in self.do[k].items():
                        print(f'\t{j}: {w}')
                else:
                    print(str(k)+': '+str(v))
            print('')
        else:
            pass
        #endregion ----------------------------------------------> Print d, do
        
        return True
    #---
    
    def RunAnalysis(self):
        """Calculate proteome profiling data"""
        #region ---------------------------------------------------------> Msg
        msgPrefix = config.lPdRun
        #endregion ------------------------------------------------------> Msg
        
        #region -------------------------------------------------------> Float
        #------------------------------> 
        msgStep = msgPrefix + "Data type"
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        #------------------------------> 
        self.dfI = self.iFileObj.df.iloc[:,self.do['oc']['Column']]
        #------------------------------> 
        try:
            self.dfF = dtsMethod.DFReplace(
                self.dfI, [0, ''], np.nan, sel=self.do['df']['ColumnF'],
            )
            self.dfF.iloc[:,self.do['df']['ColumnF']] = (
                self.dfF.iloc[:,self.do['df']['ColumnF']].astype('float')
            )
        except Exception as e:
            self.msgError  = config.mPDDataTypeCol.format(
                self.cLiFile,
                ", ".join(map(str, self.do['oc']['Column'])),
            )
            self.tException = e
            return False
        
        if config.development:
            print("self.dfI.shape: ", self.dfI.shape)
            print("self.dfF.shape: ", self.dfF.shape)
        #endregion ----------------------------------------------------> Float
        
        #region ---------------------------------------------> Exclude Protein
        #------------------------------> Msg
        msgStep = msgPrefix + 'Excluding proteins by Exclude Proteins values'
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        #------------------------------> Exclude
        if self.do['df']['ExcludeP']:
            a = self.dfF.iloc[:,self.do['df']['ExcludeP']].notna()
            a = a.loc[(a==True).any(axis=1)]
            idx = a.index
            self.dfEx = self.dfF.drop(index=idx)
        else:
            self.dfEx = self.dfF.copy()
            
        if config.development:
            print('self.dfEx.shape: ', self.dfEx.shape)
        #endregion ------------------------------------------> Exclude Protein
        
        #region -------------------------------------------------------> Score
        #------------------------------> Msg
        msgStep = msgPrefix + 'Excluding proteins by Score value'
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        #------------------------------> Exclude
        self.dfS = self.dfEx.loc[self.dfEx.iloc[:,2] >= self.do['ScoreVal']]
        #------------------------------> Sort
        self.dfS.sort_values(by = list(self.dfS.columns[0:2]), inplace=True)
        #------------------------------> Reset index
        self.dfS.reset_index(drop=True, inplace=True)
        
        if config.development:
            print('self.dfS.shape: ', self.dfS.shape)
        #endregion ----------------------------------------------------> Score
        
        #region ----------------------------------------------> Transformation
        #------------------------------> Msg
        msgStep = (
            f'{msgPrefix}'
            f'Performing data transformation - {self.do["TransMethod"]}'
        )  
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        #------------------------------> Transformed
        try:
            self.dfT = dtsStatistic.DataTransformation(
                self.dfS, 
                self.do['df']['ResCtrlFlat'], 
                method = self.do['TransMethod'],
                rep    = np.nan,
            )
        except Exception as e:
            self.msgError   = config.mPDDataTran
            self.tException = e
            return False                
        
        if config.development:
            print('self.dfT.shape: ', self.dfT.shape)
        #endregion -------------------------------------------> Transformation
        
        #region -----------------------------------------------> Normalization
        #------------------------------> Msg
        msgStep = (
            f'{msgPrefix}'
            f'Performing data normalization - {self.do["NormMethod"]}'
        )  
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        #------------------------------> Normalization
        try:
            self.dfN = dtsStatistic.DataNormalization(
                self.dfT, 
                self.do['df']['ResCtrlFlat'], 
                method = self.do['NormMethod'],
            )
        except Exception as e:
            self.msgError   = config.mPDDataNorm
            self.tException = e
        
        if config.development:
            print('self.dfN.shape: ', self.dfN.shape)
        #endregion --------------------------------------------> Normalization

        #region --------------------------------------------------> Imputation
        #------------------------------> Msg
        msgStep = (
            f'{msgPrefix}'
            f'Performing data imputation - {self.do["ImpMethod"]}'
        )  
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        #------------------------------> Imputation
        try:
            self.dfIm = dtsStatistic.DataImputation(
                self.dfN, 
                self.do['df']['ResCtrlFlat'], 
                method = self.do['ImpMethod'],
            )
        except Exception as e:
            self.msgError   = config.mPDDataImputation
            self.tException = e
        
        if config.development:
            print('self.dfIm.shape: ', self.dfIm.shape)
            print(self.dfIm.head())
        #endregion -----------------------------------------------> Imputation
        
        #region ----------------------------------------------------> Empty DF
        #------------------------------> Msg
        msgStep = (
            f'{msgPrefix}'
            f'Calculating output data - Creating empty dataframe'
        )  
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        #------------------------------> 
        self.dfR = self.EmptyDFR()
        
        if config.development:
            print('self.dfR.shape: ', self.dfR.shape)
            print(self.dfR.head())
            print('')
        #endregion -------------------------------------------------> Empty DF
        
        #region --------------------------------------------> Calculate values
        #------------------------------> Msg
        msgStep = (
            f'{msgPrefix}'
            f'Calculating output data'
        )  
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        #------------------------------> 
        for c, cN in enumerate(self.do['Cond']):
            for t, tN in enumerate(self.do['RP']):
                #------------------------------> Message
                msgStep = (
                    f'{msgPrefix}'
                    f'Calculating output data for {cN} - {tN}'
                )  
                wx.CallAfter(self.dlg.UpdateSt, msgStep)
                #------------------------------> Control & Data Column
                colC, colD = self.cColCtrlData[self.do['ControlT']](c, t)
                #------------------------------> Calculate data
                try:
                    self.CalcOutData(cN, tN, colC, colD)
                except Exception as e:
                    self.msgError = (
                        f'Calculation of the Proteome Profiling data for '
                        f'point {cN} - {tN} failed.'
                    )
                    self.tException = e
                    return False
                
        if config.development:
            print('self.dfR.shape: ', self.dfR.shape)
            print(self.dfR.head())
            print('')
        #endregion -----------------------------------------> Calculate values
        
        return True
    #---
    
    def WriteOutput(self) -> bool:
        """Write output """
        #region --------------------------------------------------> Data Steps
        stepDict = {
            config.fnInitial.format('01'): self.dfI,
            config.fnFloat.format('02')  : self.dfF,
            config.fnExclude.format('03'): self.dfEx,
            config.fnScore.format('04')  : self.dfS,
            config.fnTrans.format('05')  : self.dfT,
            config.fnNorm.format('06')   : self.dfN,
            config.fnImp.format('07')    : self.dfIm,
            self.cMainData.format('08')  : self.dfR,
        }
        #endregion -----------------------------------------------> Data Steps

        return self.WriteOutputData(stepDict)
    #---

    def RunEnd(self):
        """Restart GUI and needed variables"""
        #region ---------------------------------------> Dlg progress dialogue
        if self.msgError is None:
            #--> 
            self.dlg.SuccessMessage(
                config.lPdDone,
                eTime=f"{config.lPdEllapsed}  {self.deltaT}",
            )
        else:
            self.dlg.ErrorMessage(
                config.lPdError, 
                error      = self.msgError,
                tException = self.tException
            )
        #endregion ------------------------------------> Dlg progress dialogue

        #region -------------------------------------------------------> Reset
        self.msgError   = None # Error msg to show in self.RunEnd
        self.tException = None # Exception
        self.d          = {} # Dict with the user input as given
        self.do         = {} # Dict with the processed user input
        self.dfI        = None # pd.DataFrame for initial, normalized and
        self.dfF        = None
        self.dfEx       = None
        self.dfS        = None
        self.dfT        = None
        self.dfN        = None
        self.dfIm       = None
        self.dfR        = None
        self.date       = None # date for corr file
        self.oFolder    = None # folder for output
        self.iFileObj   = None
        self.deltaT     = None
        
        if self.dFile is not None:
            self.iFile.tc.SetValue(str(self.dFile))
        else:
            pass
        self.dFile = None # Data File copied to Data-Initial
        #endregion ----------------------------------------------------> Reset
    #---
    
    def EmptyDFR(self) -> 'pd.DataFrame':
        """Creates the empty data frame for the output. This data frame contains
            the values for Gene, Protein and Score
    
            Returns
            -------
            pd.DataFrame
        """
        #region -------------------------------------------------------> Index
        #------------------------------> First Three Columns
        aL = config.protprofFirstThree
        bL = config.protprofFirstThree
        cL = config.protprofFirstThree
        #------------------------------> Columns per Point
        n = len(config.protprofCLevel)
        #------------------------------> Other columns
        for c in self.do['Cond']:
            for t in self.do['RP']:
                aL = aL + n*[c]
                bL = bL + n*[t]
                cL = cL + config.protprofCLevel
        idx = pd.MultiIndex.from_arrays([aL[:], bL[:], cL[:]])
        #endregion ----------------------------------------------------> Index
        
        #region ----------------------------------------------------> Empty DF
        df = pd.DataFrame(
            np.nan, columns=idx, index=range(self.dfIm.shape[0]),
        )
        #endregion -------------------------------------------------> Empty DF
        
        #region -----------------------------------------> First Three Columns
        df[(aL[0], bL[0], cL[0])] = self.dfIm.iloc[:,0]
        df[(aL[1], bL[1], cL[1])] = self.dfIm.iloc[:,1]
        df[(aL[2], bL[2], cL[2])] = self.dfIm.iloc[:,2]
        #endregion --------------------------------------> First Three Columns
        
        return df
    #---
    
    def ColCtrlData_OC(self, c:int, t:int) -> list[list[int]]:
        """Get the Ctrl and Data columns for the given condition and relevant
            point when Control Type is: One Control
    
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
        colC = self.do['df']['ResCtrl'][0][0]
        #------------------------------> 
        colD = self.do['df']['ResCtrl'][c+1][t]
        #endregion ------------------------------------------------> List
        
        return [colC, colD]
    #---
    
    def ColCtrlData_OCC(self, c:int, t:int) -> list[list[int]]:
        """Get the Ctrl and Data columns for the given condition and relevant
            point when Control Type is: One Control per Column
    
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
        colC = self.do['df']['ResCtrl'][0][t]
        #------------------------------> 
        colD = self.do['df']['ResCtrl'][c+1][t]
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
        colC = self.do['df']['ResCtrl'][c][0]
        #------------------------------> 
        colD = self.do['df']['ResCtrl'][c][t+1]
        #endregion ------------------------------------------------> List
        
        return [colC, colD]
    #---
    
    def ColCtrlData_Ratio(self, c:int, t:int) -> list[Optional[list[int]]]:
        """Get the Ctrl and Data columns for the given condition and relevant
            point when Control Type is: Data as Ratios
    
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
        colC = None
        #------------------------------> 
        colD = self.do['df']['ResCtrl'][c][t]
        #endregion ------------------------------------------------> List
        
        return [colC, colD]
    #---
    
    def CalcOutData(
        self, cN: str, tN: str, colC: Optional[list[int]], colD: list[int]) -> bool:
        """Calculate the data for the main output dataframe
    
            Parameters
            ----------
            
    
            Returns
            -------
            bool
    
            Raise
            -----
            ExecutionError:
                - When the calculation fails
        """
        if config.development:
            print(cN, tN, colC, colD)
        #------------------------------> Ave & Std
        if colC is not None:
            self.dfR.loc[:,(cN, tN, 'aveC')] = self.dfIm.iloc[:,colC].mean(
                axis=1, skipna=True).to_numpy()
            self.dfR.loc[:,(cN, tN, 'stdC')] = self.dfIm.iloc[:,colC].std(
                axis=1, skipna=True).to_numpy()
        else:
            self.dfR.loc[:,(cN, tN, 'aveC')] = np.nan
            self.dfR.loc[:,(cN, tN, 'stdC')] = np.nan
        
        self.dfR.loc[:,(cN, tN, 'ave')] = self.dfIm.iloc[:,colD].mean(
            axis=1, skipna=True).to_numpy()
        self.dfR.loc[:,(cN, tN, 'std')] = self.dfIm.iloc[:,colD].std(
            axis=1, skipna=True).to_numpy()
        #------------------------------> Intensities as log2 Intensities
        dfLogI = self.dfIm.copy() 
        if self.do['TransMethod'] == 'Log2':
            pass
        else:
            if colC is not None:
                dfLogI.iloc[:,colC+colD] = np.log2(dfLogI.iloc[:,colC+colD])
            else:
                dfLogI.iloc[:,colD] = np.log2(dfLogI.iloc[:,colD])
        #------------------------------> log2(FC)
        if colC is not None:
            FC = (
                dfLogI.iloc[:,colD].mean(axis=1, skipna=True)
                - dfLogI.iloc[:,colC].mean(axis=1, skipna=True)
            )
        else:
            FC = dfLogI.iloc[:,colD].mean(axis=1, skipna=True)
        
        self.dfR.loc[:, (cN, tN, 'FC')] = FC.to_numpy()
        #------------------------------> FCz
        self.dfR.loc[:,(cN, tN, 'FCz')] = (FC - FC.mean()).div(FC.std()).to_numpy()
        #------------------------------> FCci
        if self.do['RawI']:
            self.dfR.loc[:,(cN, tN, 'CI')] = dtsStatistic.CI_Mean_Diff_DF(
                dfLogI, 
                colC, 
                colD, 
                self.do['Alpha'], 
                self.do['IndS'],
                fullCI=False,
            ).to_numpy()
        else:
            self.dfR.loc[:,(cN, tN, 'CI')] = dtsStatistic.CI_Mean_DF(
                dfLogI.iloc[:,colD], self.do['Alpha'], fullCI=False,
            ).to_numpy()
        #------------------------------> P
        if self.do['RawI']:
            if self.do['IndS']:
                self.dfR.loc[:,(cN,tN,'P')] = dtsStatistic.ttest_IS_DF(
                    dfLogI, colC, colD,
                )['P'].to_numpy()        
            else:
                self.dfR.loc[:,(cN,tN,'P')] = dtsStatistic.ttest_PS_DF(
                    dfLogI, colC, colD,
                )['P'].to_numpy()
        else:
            #------------------------------> Dummy 0 columns
            dfLogI['TEMP_Col_Full_00'] = 0
            dfLogI['TEMP_Col_Full_01'] = 0
            colCF = []
            colCF.append(dfLogI.columns.get_loc('TEMP_Col_Full_00'))
            colCF.append(dfLogI.columns.get_loc('TEMP_Col_Full_01'))
            #------------------------------> 
            self.dfR.loc[:,(cN,tN,'P')] = dtsStatistic.ttest_IS_DF(
                dfLogI, colCF, colD, f=True,
            )['P'].to_numpy()
        #------------------------------> Pc
        if self.do['CorrectP'] != 'None':
            self.dfR.loc[:,(cN,tN,'Pc')] = multipletests(
                self.dfR.loc[:,(cN,tN,'P')], 
                self.do['Alpha'], 
                config.oCorrectP[self.do['CorrectP']]
            )[1]
        else:
            pass
        #------------------------------> Round to .XX
        self.dfR.loc[:,(cN,tN,config.protprofCLevel)] = (
            self.dfR.loc[:,(cN,tN,config.protprofCLevel)].round(2)
        )
        
        return True
    #---
    #endregion ------------------------------------------------> Class methods
#---


#------------------------------> Panes for Type Results - Control Epxeriments
class ProtProfResControlExp(ResControlExpConfBase):
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
        name : str
            Unique name of the panel
        controlVal : str
            Value of Control Type in the previous Create Field event

        Raises
        ------
        

        Methods
        -------
        
    """
    #region -----------------------------------------------------> Class setup
    name = config.npResControlExpProtProf
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent, topParent, NColF):
        """ """
        #region -------------------------------------------------> Check Input
        
        #endregion ----------------------------------------------> Check Input

        #region -----------------------------------------------> Initial Setup
        #------------------------------> Needed by ResControlExpConfBase
        self.cN = 2
        self.cStLabel = { # Keys runs in range(1, N+1)
            1 : f"{config.lStProtProfCond}:",
            2 : f"{config.lStProtProfRP}:",
        }
        self.cLabelText = { # Keys runs in range(1, N+1)
            1 : 'C',
            2 : 'RP',
        }
        #------------------------------> 
        self.cAddWidget = {
            config.oControlTypeProtProf['OC']   : self.AddWidget_OC,
            config.oControlTypeProtProf['OCC']  : self.AddWidget_OCC,
            config.oControlTypeProtProf['OCR']  : self.AddWidget_OCR,
            config.oControlTypeProtProf['Ratio']: self.AddWidget_Ratio,
        }
        #------------------------------> Tooltips
        self.cTTTotalField = [
            f'Set the number of {self.cStLabel[1]}.',
            f'Set the number of {self.cStLabel[2]}.',
        ]
        #--------------> Control type from previous call to Setup Fields
        self.controlVal = ''
        #------------------------------> Error messages
        self.mNoCondRP = (
            f"Both {self.cStLabel[1]} and {self.cStLabel[2]} must be defined."
        )
        self.mNoControl = (f"The Control Type must defined.")
        #------------------------------> Super init
        super().__init__(parent, self.name, topParent, NColF)
        #------------------------------> Choices
        self.cControlTypeO = [x for x in config.oControlTypeProtProf.values()]
        
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------------> Menu
        
        #endregion -----------------------------------------------------> Menu

        #region -----------------------------------------------------> Widgets
        #------------------------------> wx.StaticText
        self.stControl = wx.StaticText(
            self.swLabel, 
            label = 'Control Experiment:'
        )
        self.stControlT = wx.StaticText(
            self.swLabel, 
            label = config.lStCtrlType
        )
        self.stControlN = wx.StaticText(
            self.swLabel, 
            label = config.lStCtrlName
        )
        #------------------------------> Text
        self.tcControl = wx.TextCtrl(
            self.swLabel, 
            size  = (125, 22),
            value = 'Control',
        )
        self.tcControl.SetHint('Name')
        #------------------------------> wx.ComboBox
        self.cbControl = wx.ComboBox(
            self.swLabel, 
            style     = wx.CB_READONLY,
            choices   = self.cControlTypeO,
            validator = dtsValidator.IsNotEmpty(),
        )
        #endregion --------------------------------------------------> Widgets

        #region -----------------------------------------------------> Tooltip
        self.stControl.SetToolTip(
            'Set the Type and Name of the control experiment.'
        )
        self.stControlT.SetToolTip('Set the Type of the control experiment.')
        self.stControlN.SetToolTip('Set the Name of the control experiment.')
        #endregion --------------------------------------------------> Tooltip
        

        #region ------------------------------------------------------> Sizers
        self.sizerSWLabelControl = wx.BoxSizer(wx.HORIZONTAL)
            
        self.sizerSWLabelControl.Add(
            self.stControl, 
            0, 
            wx.ALIGN_CENTER_VERTICAL|wx.ALL, 
            5,
        )
        self.sizerSWLabelControl.Add(
            self.stControlT, 
            0, 
            wx.ALIGN_CENTER_VERTICAL|wx.ALL, 
            5,
        )
        self.sizerSWLabelControl.Add(
            self.cbControl, 
            0, 
            wx.EXPAND|wx.ALL, 
            5,
        )
        self.sizerSWLabelControl.Add(
            self.stControlN, 
            0, 
            wx.ALIGN_CENTER_VERTICAL|wx.ALL, 
            5,
        )
        self.sizerSWLabelControl.Add(
            self.tcControl, 
            1, 
            wx.EXPAND|wx.ALL,
            5,
        )
        
        self.sizerSWLabelMain.Add(
            self.sizerSWLabelControl, 
            0, 
            wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 
            5,
        )
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind
        self.cbControl.Bind(wx.EVT_COMBOBOX, self.OnControl)
        #endregion -----------------------------------------------------> Bind

        #region ---------------------------------------------> Window position
        
        #endregion ------------------------------------------> Window position
        
        #region -----------------------------------------------> Initial State
        self.SetInitialState()
        #endregion --------------------------------------------> Initial State
        
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def OnControl(self, event) -> Literal[True]:
        """Enable/Disable the Control name when selecting control type
    
            Parameters
            ----------
            event:wx.Event
                Information about the event
            
    
            Returns
            -------
            True
        """
        #region ---------------------------------------------------> Get value
        control = self.cbControl.GetValue()
        #endregion ------------------------------------------------> Get value
        
        #region ------------------------------------------------------> Action
        if control == config.oControlTypeProtProf['Ratio']:
            self.tcControl.SetValue('None')
            self.tcControl.SetEditable(False)
        else:
            self.tcControl.SetEditable(True)
        #endregion ---------------------------------------------------> Action
        
        return True
    #---
    
    def OnCreate(self, event) -> bool:
        """Create the widgets in the white panel
    
            Parameters
            ----------
            event:wx.Event
                Information about the event
            
    
            Returns
            -------
            True
        """
        #region -------------------------------------------------> Check input
        #------------------------------> Labels
        n = []
        for k in range(1, self.cN+1):
            n.append(len(self.tcDict[k]))
        if all(n):
            pass
        else:
            dtscore.Notification(
                'errorF', msg=self.mNoCondRP, parent=self,
            )
            return False
        #------------------------------> Control
        if self.cbControl.GetValidator().Validate()[0]:
            pass
        else:
            dtscore.Notification(
                'errorF', msg=self.mNoControl, parent=self,
            )
            return False
        #endregion ----------------------------------------------> Check input
        
        #region ---------------------------------------------------> Variables
        control = self.cbControl.GetValue()
        
        if control == config.oControlTypeProtProf['OCR']:
            Nc   = n[0]     # Number of rows of tc needed
            Nr   = n[1] + 1 # Number of tc needed for each row
            NCol = n[1] + 2 # Number of columns in the sizer
            NRow = n[0] + 1 # Number of rows in the sizer
        elif control == config.oControlTypeProtProf['Ratio']:
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
        self.sizerSWMatrix.Clear(delete_windows=False)
        #endregion ----------------------------------------> Remove from sizer
        
        #region --------------------------------> Create/Destroy wx.StaticText
        #------------------------------> Destroy
        for k, v in self.lbDict.items():
            for j in range(0, len(v)):
                v[-1].Destroy()
                v.pop()
        #------------------------------> Create
        #--------------> Labels
        for k, v in self.tcDict.items():
            #--------------> New row
            row = []
            #--------------> Fill row
            for j in v:
                row.append(
                    wx.StaticText(
                        self.swMatrix,
                        label = j.GetValue(),
                    )
                )
            #--------------> Assign
            self.lbDict[k] = row
        #--------------> Control
        self.lbDict['Control'] = [
            wx.StaticText(
                self.swMatrix,
                label = self.tcControl.GetValue(),
            )
        ]
        if control == config.oControlTypeProtProf['Ratio']:
            self.lbDict['Control'][0].Hide()
        else:
            pass
        #endregion -----------------------------> Create/Destroy wx.StaticText
        
        #region ----------------------------------> Create/Destroy wx.TextCtrl
        #------------------------------> Widgets
        for k in range(1, Nc+1):
            #------------------------------> Get row
            row = self.tcDictF.get(k, [])
            lrow = len(row)
            #------------------------------> First row is especial
            if k == 1 and control == config.oControlTypeProtProf['OC']:
                if control == self.controlVal:
                    continue
                else:
                    #--------------> Destroy old widgets
                    for j in row:
                        j.Destroy()
                    #--------------> New Row and wx.TextCtrl
                    row = []
                    row.append(
                        wx.TextCtrl(
                            self.swMatrix,
                            size      = self.cSLabel,
                            validator = dtsValidator.NumberList(
                                sep = ' ',
                                opt  = True,
                                vMin = 0,
                                vMax = self.NColF,
                            )
                        )
                    )
                    #--------------> Assign & Continue to next for step
                    self.tcDictF[k] = row
                    continue
            else:
                pass
            #------------------------------> Create destroy
            if Nr > lrow:
                #-------------->  Create
                for j in range(lrow, Nr):
                    row.append(
                        wx.TextCtrl(
                            self.swMatrix,
                            size      = self.cSLabel,
                            validator = dtsValidator.NumberList(
                                opt  = True,
                                sep = ' ',
                                vMin = 0,
                                vMax = self.NColF,
                            )
                        )
                    )
                #-------------->  Add to dict
                self.tcDictF[k] = row
            else:
                for j in range(Nr, lrow):
                    #-------------->  Destroy
                    row[-1].Destroy()
                    #--------------> Remove from list
                    row.pop()
        #------------------------------> Drop keys and destroy from dict
        dK = [x for x in self.tcDictF.keys()]
        for k in dK:
            if k > Nc:
                #--------------> Destroy this widget
                for j in self.tcDictF[k]:
                    j.Destroy()
                #--------------> Remove key
                del(self.tcDictF[k])
            else:
                pass      
        #------------------------------> Clear value if needed
        if control != self.controlVal:
            for v in self.tcDictF.values():
                for j in v:
                    j.SetValue('')
        else:
            pass      
        #endregion -------------------------------> Create/Destroy wx.TextCtrl
        
        #region ------------------------------------------------> Setup Sizers
        #------------------------------> Adjust size
        self.sizerSWMatrix.SetCols(NCol)
        self.sizerSWMatrix.SetRows(NRow)
        #------------------------------> Add widgets
        self.cAddWidget[control](NCol, NRow)
        #------------------------------> Grow Columns
        for k in range(1, NCol):
            if not self.sizerSWMatrix.IsColGrowable(k):
                self.sizerSWMatrix.AddGrowableCol(k, 1)
            else:
                pass
        #------------------------------> Update sizer
        self.sizerSWMatrix.Layout()
        #endregion ---------------------------------------------> Setup Sizers
        
        #region --------------------------------------------------> Set scroll
        self.swMatrix.SetupScrolling()
        #endregion -----------------------------------------------> Set scroll
        
        #region -------------------------------------------> Update controlVal
        self.controlVal = control
        #endregion ----------------------------------------> Update controlVal
        
        
        return True
    #---
    
    def AddWidget_OC(self, NCol: int, NRow: int) -> bool:
        """Add the widget when Control Type is One Control. It is assumed 
            everything is ready to add the widgets
            
            Parameters
            ----------
            NCol : int
                Number of columns in the sizer
            NRow : int
                Number of rows in the sizer 
        """
        #region -------------------------------------------------> Control Row
        self.sizerSWMatrix.Add(
            self.lbDict['Control'][0],
            0,
            wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL,
            5
        )
        self.sizerSWMatrix.Add(
            self.tcDictF[1][0],
            0,
            wx.EXPAND|wx.ALL,
            5
        )
        for k in range(2, NCol):
            self.sizerSWMatrix.AddSpacer(1)
        #endregion ----------------------------------------------> Control Row
        
        #region ---------------------------------------------------> RP Labels
        #--------------> Empty space
        self.sizerSWMatrix.AddSpacer(1)
        #--------------> Labels
        for k in self.lbDict[2]:
            self.sizerSWMatrix.Add(
                k,
                0,
                wx.ALIGN_CENTER|wx.ALL,
                5
            )
        #endregion ------------------------------------------------> RP Labels
        
        #region ------------------------------------------------> Other fields
        K = 2
        for k in self.lbDict[1]:
            #--------------> Add Label
            self.sizerSWMatrix.Add(
                k,
                0,
                wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL|wx.ALL,
                5
            )
            #--------------> Add tc
            for j in self.tcDictF[K]:
                self.sizerSWMatrix.Add(
                    j,
                    0,
                    wx.EXPAND|wx.ALL,
                    5
                )
            K += 1
        #endregion ---------------------------------------------> Other fields
        
        return True
    #---
    
    def AddWidget_OCC(self, NCol: int, NRow: int) -> bool:
        """Add the widget when Control Type is One Control. It is assumed 
            everything is ready to add the widgets"""
        #region ---------------------------------------------------> RP Labels
        self.sizerSWMatrix.AddSpacer(1)
        
        for k in self.lbDict[2]:
            self.sizerSWMatrix.Add(
                k,
                0,
                wx.ALIGN_CENTER|wx.ALL,
                5
            )
        #endregion ------------------------------------------------> RP Labels
        
        #region -------------------------------------------------> Control Row
        self.sizerSWMatrix.Add(
            self.lbDict['Control'][0],
            0,
            wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL|wx.ALL,
            5
        )
        
        for k in self.tcDictF[1]:
            self.sizerSWMatrix.Add(
                k,
                0,
                wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL,
                5
            )    
        #endregion ----------------------------------------------> Control Row
        
        #region --------------------------------------------------> Other Rows
        for k, v in self.tcDictF.items():
            K = k - 2
            #------------------------------> Skip control row
            if k == 1:
                continue
            else:
                pass
            #------------------------------> Add Label
            self.sizerSWMatrix.Add(
                self.lbDict[1][K],
                0,
                wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL|wx.ALL,
                5
            )
            #------------------------------> Add wx.TextCtrl
            for j in v:
                self.sizerSWMatrix.Add(
                j,
                0,
                wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL,
                5
            ) 
        #endregion -----------------------------------------------> Other Rows
        
        return True
    #---
    
    def AddWidget_OCR(self, NCol: int, NRow: int) -> bool:
        """Add the widget when Control Type is One Control. It is assumed 
            everything is ready to add the widgets"""
        #region ---------------------------------------------------> RP Labels
        self.sizerSWMatrix.AddSpacer(1)
        
        self.sizerSWMatrix.Add(
            self.lbDict['Control'][0],
            0,
            wx.ALIGN_CENTER|wx.ALL,
            5
        )
        
        for k in self.lbDict[2]:
            self.sizerSWMatrix.Add(
                k,
                0,
                wx.ALIGN_CENTER|wx.ALL,
                5
            )
        #endregion ------------------------------------------------> RP Labels
        
        #region --------------------------------------------------> Other rows
        for k, v in self.tcDictF.items():
            #--------------> 
            K = int(k) - 1
            #--------------> 
            self.sizerSWMatrix.Add(
                self.lbDict[1][K],
                0,
                wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL|wx.ALL,
                5
            )
            #-------------->
            for j in v:
                self.sizerSWMatrix.Add(
                    j,
                    0,
                    wx.EXPAND|wx.ALL,
                    5
                )
        #endregion -----------------------------------------------> Other rows
        
        return True
    #---
    
    def AddWidget_Ratio(self, NCol: int, NRow: int) -> bool:
        """Add the widget when Control Type is Data as Ratios. It is assumed 
            everything is ready to add the widgets"""
        #region ---------------------------------------------------> RP Labels
        self.sizerSWMatrix.AddSpacer(1)
        
        for k in self.lbDict[2]:
            self.sizerSWMatrix.Add(
                k,
                0,
                wx.ALIGN_CENTER|wx.ALL,
                5
            )
        #endregion ------------------------------------------------> RP Labels
        
        #region --------------------------------------------------> Other rows
        for k, v in self.tcDictF.items():
            #--------------> 
            K = int(k) - 1
            #--------------> 
            self.sizerSWMatrix.Add(
                self.lbDict[1][K],
                0,
                wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL|wx.ALL,
                5
            )
            #-------------->
            for j in v:
                self.sizerSWMatrix.Add(
                    j,
                    0,
                    wx.EXPAND|wx.ALL,
                    5
                )
        #endregion -----------------------------------------------> Other rows
        
        return True
    #---
    #endregion ------------------------------------------------> Class methods
#---
#endregion ----------------------------------------------------------> Classes


