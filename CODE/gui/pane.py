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
from typing import Optional, Literal, Type

import pandas as pd
import numpy as np

import wx
import wx.lib.agw.aui as aui
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
        wx.StaticBox, the bottom Buttons and the statusbar.

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
        NCol : int
            Number of columns in the main input file - 1
        #------------------------------> Must be set on child
        name : str
            Unique name of the pane
        cURL : str 
            URL for the Help wx.Button
        cSection : str 
            Section in the UMSAP file. One of the values in config.nameModules 
            or config.nameUtilities
        cLenLongestL : int 
            Length of the longest label in output dict
        cTitlePD : str
            Title for the Progress Dialog shown when running analysis
        cGaugePD : int 
            Number of steps for the wx.Gauge in the Progress Dialog shown when 
            running analysis
        #------------------------------> Configuration
        cRunBtnL : str
            Label for the run wx.Button.
            Default is config.lBtnRun.
        cFileBoxL : str
            Label for the wx.StaticBox in section Files & Folders
            Default is config.lStBoxFile.
        cValueBoxL : str
            Label for the wx.StaticBox in section User-defined values
            Default is config.lStBoxValue
        cColumnBoxL : str
            Label for the wx.StaticBox in section Columns
            Default is config.lStBoxColumn
        ciMode : str
            Mode for selecting the main input file. Default is 'openO'
        coMode : str
            Mode for selecting the output file. Default is 'save'
        ciFileL : str
            Label for the main input data wx.Button
            Default is config.lBtnDataFile
        ciFileH : str
            Hint for the main input wx.TextCtrl
            Default is config.hTcDataFile
        ciFileTT : str
            Tooltip for the main input wx.TextCtrl
            Default is config.ttTcDataFile
        ciFileE : wxPython extension list
            Extensions allowed for the main input file
            Default is config.elData
        coFileL : str
            Label for the output wx.Button
            Default is config.lBtnOutFile
        coFileH : str
            Hint for the output file wx.TextCtrl
            Default is config.hTcOutFile
        coFileTT : str
            Tooltip for the output file wx.TextCtrl
            Default is config.ttTcOutFile
        ciFileValidator : wx.Validator
            Validator for the main input file. 
            Default is dtsValidator.InputFF(
                fof='file', 
                ext = config.esData,
            )
        coFileValidator : wx.Validator
            Validator for the main input file. 
            Default is dtsValidator.OutputFF(
                fof='file', 
                ext = config.esUMSAP[0],
            )
        #------------------------------> Needed to run analysis
        msgError : Str or None
            Error message to show when analysis fails
        d : dict
            Dict with user input. See keys in Child class
        do : dict
            Dict with processed user input. See keys in Child class
        dfI : pdDataFrame or None
            Dataframe with initial values after columns were extracted and type
            assigned.
        dfT : pdDataFrame or None
            Dataframe after data transformation
        date : str or None
            Date time stamp as given by dtsMethod.StrNow()
        oFolder : Path or None
            Folder to contain the output
        tException : Exception or None
            Exception raised during analysis   
        #------------------------------> Widgets
        btnRun : wx.Button
            Run button
        btnHelp : wx.Button
            Help button
        btnClearAll : wx.Button
            Clear All button
        sbFile : wx.StaticBox
            StaticBox to contain the input/output file information
        sbValue : wx.StaticBox
            StaticBox to contain the user-defined values
        sbColumn : wx.StaticBox
            StaticBox to contain the column numbers in the input files
        iFile : dtsWidget.ButtonTextCtrlFF
            Attributes: btn, tc
        oFile : dtsWidget.ButtonTextCtrlFF
            Attributes: btn, tc
        checkB : wx.CheckBox
            Signal whether to add new data to existing file or not
        sizersbFile : wx.StaticBoxSizer
            StaticBoxSizer for sbFile
        sizersbValue : wx.StaticBoxSizer
            StaticBoxSizer for sbValue
        sizersbColumn : wx.StaticBoxSizer
            StaticBoxSizer for sbColumn
        sizersbFileWid : wx.GridBagSizer
            FlexGridSizer for widgets in sbFile
        sizersbValueWid : wx.GridBagSizer
            FlexGridSizer for widgets in sbValue
        sizersbColumnWid : wx.GridBagSizer
            FlexGridSizer for widgets in sbColumn		
        btnSizer : wx.FlexGridSizer
            To align the buttons
        Sizer : wx.BoxSizer
            Main sizer of the tab        
        #------------------------------> Other
        lbI : wx.ListCtrl or None
            Pointer to the default wx.ListCtrl to load Data File content to. 
        lbL : list of wx.ListCtrl
            To clear all wx.ListCtrl in the Tab
                
        Notes
        -----
    """
    #region -----------------------------------------------------> Class setup
    
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent: wx.Window, rightDelete: bool=True) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.parent = parent
        #------------------------------> Labels
        self.cRunBtnL    = getattr(self, 'RunBtnL', config.lBtnRun)
        self.cuFileL     = getattr(self, 'cuFileL', config.lBtnUFile)
        self.ciFileL     = getattr(self, 'ciFileL', config.lBtnDataFile)
        self.cFileBoxL   = getattr(self, 'cFileBoxL', config.lSbFile)
        self.cValueBoxL  = getattr(self, 'cValueBoxL', config.lSbValue)
        self.cColumnBoxL = getattr(self, 'cColumnBoxL', config.lSbColumn)
        self.cCheckL     = getattr(self, 'cCheckL', config.lCbFileAppend)
        #------------------------------> Hints
        self.cuFileH = getattr(self, 'cuFileH', config.hTcUFile)
        self.ciFileH = getattr(self, 'ciFileH', config.hTcDataFile)
        #------------------------------> Tooltips
        self.cuFileTT    = getattr(self, 'cuFileTT', config.ttBtnUFile)
        self.ciFileTT    = getattr(self, 'ciFileTT', config.ttBtnDataFile)
        self.cHelpTT     = getattr(self, 'cHelpTT', config.ttBtnHelpDef)
        self.cClearAllTT = getattr(self, 'cClearAllTT', config.ttBtnClearAll)
        self.cRunTT      = getattr(self, 'cRunTT', config.ttBtnRun)
        #------------------------------> Extensions
        self.ciFileE = getattr(self, 'ciFileE', config.elData)
        #------------------------------> Mode
        self.ciMode = getattr(self, 'ciMode', 'openO')
        self.cuMode = getattr(self, 'coMode', 'save')
        #------------------------------> Validator
        self.cuFileValidator = getattr(
            self, 
            'cuFileValidator',
            dtsValidator.OutputFF(
                fof = 'file',
                ext = config.esUMSAP[0],
                opt = False,
            )
        )
        self.ciFileValidator = getattr(
            self, 
            'ciFileValidator',
            dtsValidator.InputFF(
                fof = 'file',
                ext = config.esData,
            )
        )
        #------------------------------> This is needed to handle Data File 
        # content load to the wx.ListCtrl in Tabs with multiple panels
        #--------------> Default wx.ListCtrl to load data file content
        self.lbI : Optional[Type[wx.ListCtrl]]= None 
        #--------------> List to use just in case there are more than 1 
        self.lbL : list[Optional[Type[wx.ListCtrl]]] = [self.lbI]
        #------------------------------> Needed to Run the analysis
        #--------------> Dict with the user input as given
        self.d = {}
        #--------------> Dict with the processed user input
        self.do = {} 
        #--------------> Error message and exception to show in self.RunEnd
        self.msgError   : Optional[str]       = None 
        self.tException : Optional[Exception] = None
        #--------------> pd.DataFrames for:
        self.dfI : Optional['pd.DataFrame'] = None # Initial and
        self.dfT : Optional['pd.DataFrame'] = None # Transaformed values
        #--------------> date for corr file
        self.date : Optional[str] = None
        #--------------> folder for output
        self.oFolder : Optional[Path] = None
        #------------------------------> Parent init
        wx.Panel.__init__(self, parent, name=self.name)

        dtsWidget.ButtonOnlineHelpClearAllRun.__init__(self, self, 
            self.cURL, 
            labelR = self.cRunBtnL,
        )

        dtsWidget.StaticBoxes.__init__(self, self, 
            labelF      = self.cFileBoxL,
            labelV      = self.cValueBoxL,
            labelC      = self.cColumnBoxL,
            rightDelete = rightDelete,
        )
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.uFile = dtsWidget.ButtonTextCtrlFF(self.sbFile,
            btnLabel   = self.cuFileL,
            tcHint     = self.cuFileH,
            mode       = self.cuMode,
            ext        = config.elUMSAP,
            tcStyle    = wx.TE_READONLY,
            validator  = self.cuFileValidator,
            ownCopyCut = True,
        )
        self.uFile.btn.SetToolTip(self.cuFileTT)
        
        self.iFile = dtsWidget.ButtonTextCtrlFF(self.sbFile,
            btnLabel   = self.ciFileL,
            tcHint     = self.ciFileH,
            ext        = self.ciFileE,
            mode       = self.ciMode,
            tcStyle    = wx.TE_READONLY|wx.TE_PROCESS_ENTER,
            validator  = self.ciFileValidator,
            ownCopyCut = True,
        )
        self.iFile.btn.SetToolTip(self.ciFileTT)
        #endregion --------------------------------------------------> Widgets
        
        #region -----------------------------------------------------> Tooltip
        self.btnHelp.SetToolTip(self.cHelpTT)
        self.btnClearAll.SetToolTip(self.cClearAllTT)
        self.btnRun.SetToolTip(self.cRunTT)
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

        self.Sizer = wx.BoxSizer(wx.VERTICAL)

        self.Sizer.Add(self.sizersbFile, 0, wx.EXPAND|wx.ALL, 5)
        self.Sizer.Add(self.sizersbValue, 0, wx.EXPAND|wx.ALL, 5)
        self.Sizer.Add(self.sizersbColumn, 0, wx.EXPAND|wx.ALL, 5)
        self.Sizer.Add(self.btnSizer, 0, wx.ALIGN_CENTER|wx.ALL, 5)
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
        """Adjust default Path for Data File when an UMSAP file is selected
    
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
    
    def OnIFileLoad(self, event: wx.CommandEvent) -> Literal[True]:
        """Clear GUI elements when Data Folder is ''
    
            Parameters
            ----------
            event: wx.Event
                Information about the event		
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
        """Clear wx.ListCtrl and NCol """
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
                            self.do, 
                            self.cChangeKey,
                            new = True,
                        ),
                        'R' : Results,
                    }
                }
            
            Return
            ------
            dict
                Output data as a dict
        """
        if self.do['uFile'].exists():
            #------------------------------> 
            outData = dtsFF.ReadJSON(self.do['uFile'])
            #------------------------------>
            if outData.get(self.cSection, False):
                outData[self.cSection][self.date] = dateDict[self.date]
            else:
                outData[self.cSection] = dateDict
        else:
            outData = {self.cSection : dateDict}

        return outData
    #---

    def EqualLenLabel(self, label: str) -> str:
        """Add empty space to the end of label to match the length of
            self.cLenLongestL
    
            Parameters
            ----------
            label : str
                Original label
    
            Returns
            -------
            str
                Label with added empty strings at the end to match the length of
                self.cLenLongestL
        """
        return f"{label}{(self.cLenLongestL - len(label))*' '}" 
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
        dataFolder = f"{self.date}-{self.cSection}-{config.fnDataSteps}"
        dataFolder = self.oFolder / dataFolder
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
            self.d[self.EqualLenLabel(self.ciFileL)] = str(self.dFile)
        else:
            self.dFile = None
        #endregion ---------------------------------------------> Data Initial
        
        #region --------------------------------------------------> Data Steps
        msgStep = msgPrefix + 'Data files, Step by Step Data files'
        wx.CallAfter(self.dlg.UpdateStG, msgStep)

        dtsFF.WriteDFs2CSV(dataFolder, stepDict)
        #endregion -----------------------------------------------> Data Steps
        
        #region --------------------------------------------------> UMSAP File
        msgStep = msgPrefix + 'Main file'
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        #------------------------------> Create output dict
        dateDict = {
            self.date : {
                'V' : config.dictVersion,
                'I' : self.d,
                'CI': dtsMethod.DictVal2Str(
                    self.do, 
                    self.cChangeKey,
                    new = True,
                ),
                'R' : self.RDF.to_dict(),
            }
        }
        #------------------------------> Append or not
        outData = self.SetOutputDict(dateDict)
        #------------------------------> Write
        dtsFF.WriteJSON(self.do['uFile'], outData)
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
    #endregion ------------------------------------------------> Class methods
#---


class BaseConfModPanel(BaseConfPanel, widget.ResControl):
    """Base panel for a module

        Parameters
        ----------
        parent : wx Widget
            Parent of the widgets
        oMode : str
            One of 'openO', 'openM', 'save', 'folder'. Default is 'folder'
        statusbar : wx.StatusBar
            Statusbar of the application to display messages
        rightDelete : Boolean
            Enables clearing wx.StaticBox input with right click

        Attributes
        ----------
        #------------------------------> Configuration
        cScoreValL : str
            Score value label. Default is config.lStScoreVal.
        cNormMethodL : str
            Data normalization label. Default is config.lCbNormMethod.
        cTransMethodL : str
            Data transformation label. Default is config.lCbTransMethod.
        cScoreColL : str
            Score column. Default is config.lStScoreCol.
        cNormChoice : list of str
            Choice for normalization method. 
            Default is config.oNormMethod.
        cTransChoice : list of str
            Choice for transformation method. 
            Default is config.oTransMethod.values().
        cTcSize : wx.Size
            Size for the wx.TextCtrl in the panel
        #------------------------------> Widgets
        normMethod : dtsWidget.StaticTextComboBox
            Attributes: st, cb
        scoreVal : dtsWidget.StaticTextCtrl
            Attributes: st, tc
        detectedProt : : dtsWidget.StaticTextCtrl
            Attributes: st, tc 
        score : : dtsWidget.StaticTextCtrl
            Attributes: st, tc
        colExtract : : dtsWidget.StaticTextCtrl
            Attributes: st, tc  
        tcResults : wx.TextCtrl
            For Results - Control Experiments
        stResults : wx.StaticText
            For Results - Control Experiments
        btnResultsW : wx.Button
            For Results - Control Experiments

        Raises
        ------
        

        Methods
        -------
        
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
        self.cScoreValL = getattr(self, 'cScoreValL', config.lStScoreVal)
        self.cNormMethodL = getattr(self, 'cNormMethodL', config.lCbNormMethod)
        self.cTransMethodL = getattr(
            self, 'cTransMethodL', config.lCbTransMethod
        )
        self.cImputationL = getattr(self, 'cImputationL', config.lCbImputation)
        self.cDetectedProtL = getattr(
            self, 'cDetectedProtL', config.lStDetectedProt,
        )
        self.cScoreColL = getattr(self, 'cScoreColL', config.lStScoreCol)
        self.cColExtractL = getattr(self, 'cColExtractL', config.lStColExtract)
        #------------------------------> Choices
        self.cNormO = getattr(
            self, 'cNormO', [x for x in config.oNormMethod.values()]
        )
        self.cTransO = getattr(
            self, 'cTransO', [x for x in config.oTransMethod.values()]
        )
        self.cImputationO = getattr(
            self, 'cImputationO', [x for x in config.oImputation.values()]
        )
        #------------------------------> Size
        self.cTcSize = getattr(self, 'cTcSize', config.sTc)
        #------------------------------> Tooltips
        self.cNormMethodTT = getattr(self, 'cNormMethodTT', config.ttStNorm)
        self.cTransMethodTT = getattr(self, 'cTransMethodTT', config.ttStTrans)
        self.cImputationTT = getattr(
            self, 'cImputationTT', config.ttStImputation,
        )
        self.cScoreValTT = getattr(self, 'cScoreValTT', config.ttStScoreVal)
        self.cDetectedProtTT = getattr(
            self, 'cDetectedProtLTT', config.ttStDetectedProtL,
        )
        self.cScoreTT = getattr(self, 'cScoreTT', config.ttStScore)
        #------------------------------> __init__
        BaseConfPanel.__init__(self, parent, rightDelete=rightDelete)

        widget.ResControl.__init__(self, self.sbColumn)
        
        #------------------------------> Tooltips
        self.cColExtractTT = getattr(
            self, 'cColExtractTT', config.ttStColExtract.format(self.ciFileL),
        )
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------------> Menu
        
        #endregion -----------------------------------------------------> Menu

        #region -----------------------------------------------------> Widgets
        self.normMethod = dtsWidget.StaticTextComboBox(
            self.sbValue, 
            label     = self.cNormMethodL,
            choices   = self.cNormO,
            validator = dtsValidator.IsNotEmpty(),
        )
        
        self.transMethod = dtsWidget.StaticTextComboBox(
            self.sbValue, 
            label     = self.cTransMethodL,
            choices   = self.cTransO,
            validator = dtsValidator.IsNotEmpty(),
        )
        
        self.imputationMethod = dtsWidget.StaticTextComboBox(
            self.sbValue, 
            label     = self.cImputationL,
            choices   = self.cImputationO,
            validator = dtsValidator.IsNotEmpty(),
        )

        self.scoreVal = dtsWidget.StaticTextCtrl(
            self.sbValue,
            stLabel   = self.cScoreValL,
            tcSize    = self.cTcSize,
            validator = dtsValidator.NumberList(
                numType = 'float',
                nN      = 1,
            )
        )

        self.detectedProt = dtsWidget.StaticTextCtrl(
            self.sbColumn,
            stLabel   = self.cDetectedProtL,
            tcSize    = self.cTcSize,
            validator = dtsValidator.NumberList(
                numType = 'int',
                nN      = 1,
                vMin    = 0,
            )
        )

        self.score = dtsWidget.StaticTextCtrl(
            self.sbColumn,
            stLabel   = self.cScoreColL,
            tcSize    = self.cTcSize,
            validator = dtsValidator.NumberList(
                numType = 'int',
                nN      = 1,
                vMin    = 0,
            )
        )

        self.colExtract = dtsWidget.StaticTextCtrl(
            self.sbColumn,
            stLabel   = self.cColExtractL,
            tcSize    = self.cTcSize,
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
        self.normMethod.st.SetToolTip(self.cNormMethodTT)
        self.transMethod.st.SetToolTip(self.cTransMethodTT)
        self.imputationMethod.st.SetToolTip(self.cImputationTT)
        self.scoreVal.st.SetToolTip(self.cScoreValTT)
        self.detectedProt.st.SetToolTip(self.cDetectedProtTT)
        self.score.st.SetToolTip(self.cScoreTT)
        self.colExtract.st.SetToolTip(self.cColExtractTT)
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
    
    #endregion ------------------------------------------------> Class methods
#---


class ResControlExpConfBase(wx.Panel):
    """Parent class for the configuration panel in the dialog Results - Control
        Experiments

        Parameters
        ----------
        parent : wx.Widget
            Parent of the widgets
        name : str	
            Unique name of the panel
        topParent : wx.Widget
            Top parent window

        Attributes
        ----------
        topParent : wx.Widget
            Top parent window
        #------------------------------> Must be set on child
        cN : int
            Number of labels excluding control labels
        cTotalFieldTT : str
            Tooltip for the labels in the top region
        cStLabel : dict
            Keys are 1 to cN and values the text of the labels    
        cLabelText : dict
            Keys are 1 to cN and values the prefix for the label values   
        #------------------------------> Configuration
        cSWLabelS : wx.Size
            Size for the ScrolledPanel with the label. Default is (670,135)
        cSWMatrixS : wx.Size
            Size for the ScrolledPanel with the fields. Default is (670,670)
        cTotalFieldS : wx.Size
            Size for the total wx.TextCtrl in top region. Default is (35,22)
        cSetupL : str
            Label for the wx.Button in top region. Default is 'Setup Fields'
        #------------------------------> Widgets
        #------------------------------> Manage Window
        stLabel : list of wx.StaticText
            List with the labels name
        tcLabel : list of wx.TextCtrl
            To input the number of labels
        tcDict : dict of lists of wx.TextCtrl for labels
            Keys are 1 to N and values are lists of wx.TextCtrl
        tcDictF : dict of lists of wx.TextCtrl for fields
            Keys are 1 to NRow and values are lists of wx.TextCtrl. 
        lbDict : dict of lists of wx.StaticText for user-given labels
            Keys are 1 to N plus 'Control' and values are the the lists. 
        NColF : int
            Number of columns in the file - 1 
            
        Raises
        ------
        
        Methods
        -------
        
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
        self.tcDictF   = {}
        self.lbDict    = {}
        self.NColF     = NColF - 1
        #------------------------------> Label
        self.cSetupL = getattr(self, 'cSetupL', 'Setup Fields')
        #------------------------------> Hint
        self.cTotalFieldH = getattr(self, 'cTotalFieldH', '#')
        #------------------------------> Size
        self.cSWLabelS    = getattr(self, 'cSWLabelS', (670,135))
        self.cSWMatrixS   = getattr(self, 'cSWMatrixS', (670,670))
        self.cTotalFieldS = getattr(self, 'cTotalFieldS', (35,22))
        self.cLabelS      = getattr(self, 'cLabelS', (100, 22))
        #------------------------------> super()
        super().__init__(parent, name=name)
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------------> Menu
        
        #endregion -----------------------------------------------------> Menu

        #region -----------------------------------------------------> Widgets
        #------------------------------> wx.ScrolledWindow
        self.swLabel  = scrolled.ScrolledPanel(self, size=self.cSWLabelS)
        
        self.swMatrix = scrolled.ScrolledPanel(self, size=self.cSWMatrixS)
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
            a.SetToolTip(self.cTotalFieldTT[k-1])
            self.stLabel.append(a)
            #------------------------------> wx.TextCtrl for the label
            a = wx.TextCtrl(
                    self.swLabel,
                    size      = self.cTotalFieldS,
                    name      = str(k),
                    validator = dtsValidator.NumberList(vMin=1, nN=1),
                )
            a.SetHint(self.cTotalFieldH)
            self.tcLabel.append(a)
        #------------------------------> wx.Button
        self.btnCreate = wx.Button(self, label=self.cSetupL)
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
        """Create the fields in the white panel. Override as needed.
    
            Parameters
            ----------
            event:wx.Event
                Information about the event
            
    
            Returns
            -------
            
    
            Raise
            -----
            
        """
        return True
    #---

    def OnLabelNumber(self, event: wx.Event):
        """Creates fields for names when the total wx.TextCtrl loose focus
    
            Parameters
            ----------
            event : wx.Event
                Information about the event
            
    
            Returns
            -------
            
    
            Raise
            -----
            
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
                            size  = self.cLabelS,
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
                1             : [values],
                N             : [values],
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
        #------------------------------> Needed by BaseConfPanel
        cURL : str
            URL for the Help button
        cSection : str
            Section for the output file
        cLenLongestLabel : int
            Length of the longest label
        cTitlePD : str
            Title for hte progress dialog
        cGaugePD : int
        #------------------------------> For Analysis
        cMainData : str
            Name of the file with the correlation coefficient values
        cChangeKey : list of str
        do : dict
            Dict with the processed user input
            {
                'uFile'      : 'umsap file path',
                'iFile'      : 'data file path',
                'TransMethod': 'transformation method',
                'CorrMethod' : 'correlation method',
                'Column'     : [selected columns as integers],
            }
        d : dict
            Similar to 'do' but: 
                - No uFile
                - With the values given by the user
                - Keys as in the GUI of the tab.
        RDF : pdDataFrame
            Dataframe with correlation coefficients
        See parent class for more attributes

        Notes
        -----
        Running the analysis results in the creation of
        - Parent Folder/
            - 20210324-165609-Correlation-Analysis/
            - Data_Files/
            - output-file.umsap
        
        The Data_Files folder contains the original data files. These are needed 
        for data visualization, running analysis again with different 
        parameters, etc.
        The Date-Section folder contains regular csv files with the step by step
        data.
    
        The Correlation Analysis section in output-file.umsap conteins the 
        information about the calculations, e.g

        {
            'Correlation-Analysis : {
                '20210324-165609': {
                    'V' : config.dictVersion,
                    'I' : self.d,
                    'CI': self.do,
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
        self.cSection     = config.nUCorrA
        self.cLenLongestL = len(config.lCbTransMethod)
        self.cTitlePD     = config.lnPDCorrA
        self.cGaugePD     = 17
        #------------------------------> Optional configuration
        self.cHelpTT = config.ttBtnHelp.format(config.urlCorrA)
        #------------------------------> Setup attributes in base class 
        super().__init__(parent)
        #------------------------------> Needed to Run
        self.cMainData  = '{}-CorrelationCoefficients-Data.txt'
        self.cChangeKey = ['uFile', 'iFile']
        self.RDF        = None # correlation coefficients
        self.dFile      = None
        #------------------------------> Label
        self.cTransL    = config.lCbTransMethod
        self.cCorrL     = config.lCbCorrMethod
        self.ciListCtrl = config.lStColIFile.format(self.ciFileL)
        self.coListCtrl = 'Columns to Analyse'
        #------------------------------> Options
        self.cTranMethodO = [x for x in config.oTransMethod.values()]
        self.cCorrMethodO = [x for x in config.oCorrMethod.values()]
        #------------------------------> Tooltips
        self.cTransTT = config.ttStTrans
        self.cCorrTT = config.ttStCorr
        #endregion --------------------------------------------> Initial setup
        
        #region -----------------------------------------------------> Widgets
        #------------------------------> Values
        self.transMethod = dtsWidget.StaticTextComboBox(self.sbValue, 
            label     = self.cTransL,
            choices   = self.cTranMethodO,
            validator = dtsValidator.IsNotEmpty(),
        )
        self.transMethod.st.SetToolTip(self.cTransTT)
        
        self.corrMethod = dtsWidget.StaticTextComboBox(self.sbValue, 
            label     = self.cCorrL,
            choices   = self.cCorrMethodO,
            validator = dtsValidator.IsNotEmpty(),
        )
        self.corrMethod.st.SetToolTip(self.cCorrTT)
        #------------------------------> Columns
        self.stListI = wx.StaticText(
            self.sbColumn, 
            label = self.ciListCtrl,
        )
        self.stListO = wx.StaticText(
            self.sbColumn, 
            label = self.coListCtrl,
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
            self.transMethod.st,
            pos    = (0,1),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL,
            border = 5,
        )
        self.sizersbValueWid.Add(
            self.transMethod.cb,
            pos    = (0,2),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL,
            border = 5,
        )
        self.sizersbValueWid.Add(
            self.corrMethod.st,
            pos    = (0,3),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL,
            border = 5,
        )
        self.sizersbValueWid.Add(
            self.corrMethod.cb,
            pos    = (0,4),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL,
            border = 5,
        )
        self.sizersbValueWid.Add(
            1, 1,
            pos    = (0,5),
            flag   = wx.EXPAND|wx.ALL,
            border = 5
        )
        self.sizersbValueWid.AddGrowableCol(0, 1)
        self.sizersbValueWid.AddGrowableCol(5, 1)
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
    def OnAdd(self, event):
        """Add columns to analyse
    
            Parameters
            ----------
            event : wx.Event
                Event information
        """
        self.lbI.Copy()
        self.lbO.Paste()
    #---

    def SetInitialData(self, dataI: Optional[dict]=None) -> Literal[True]:
        """Set initial data
    
            Parameters
            ----------
            
    
            Returns
            -------
            
    
            Raise
            -----
            
        """
        if dataI is not None:
            #------------------------------> 
            self.uFile.tc.SetValue(dataI['CI']['uFile'])
            self.iFile.tc.SetValue(dataI['I']['Data File          '])
            #------------------------------> 
            self.transMethod.cb.SetValue(dataI['CI']['TransMethod'])
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
        
        #region ---------------------------------------------------------> Msg
        msgPrefix = config.lPdCheck
        #endregion ------------------------------------------------------> Msg
        
        #region -------------------------------------------> Individual Fields
        #------------------------------> Output Folder
        msgStep = msgPrefix + self.cuFileL
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        a, b = self.uFile.tc.GetValidator().Validate()
        if a:
            pass
        else:
            self.msgError = dtscore.StrSetMessage(
                config.mFileBad.format(b[1], self.cuFileL),
                b[2]
            )
            return False
        #------------------------------> Input file
        msgStep = msgPrefix + self.ciFileL
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        a, b = self.iFile.tc.GetValidator().Validate()
        if a:
            pass
        else:
            self.msgError = dtscore.StrSetMessage(
                config.mFileBad.format(b[1], self.ciFileL),
                b[2]
            )
            return False
        #------------------------------> Transformation
        msgStep = msgPrefix + self.cTransL
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        if self.transMethod.cb.GetValidator().Validate()[0]:
            pass
        else:
            self.msgError = config.mNotEmpty.format(self.cTransL)
            return False
        #------------------------------> Corr Method
        msgStep = msgPrefix + self.cCorrL
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        if self.corrMethod.cb.GetValidator().Validate()[0]:
            pass
        else:
            self.msgError = config.mNotEmpty.format(self.cCorrL)
            return False
        #------------------------------> ListCtrl
        msgStep = msgPrefix + self.coListCtrl
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        if self.lbO.GetItemCount() > 1:
            pass
        else:
            self.msgError = (
                f"There must be at least two items in {self.coListCtrl}"
            )
            return False
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
        #------------------------------> As given
        self.d = {
            self.EqualLenLabel(self.ciFileL) : (
                self.iFile.tc.GetValue()),
            self.EqualLenLabel(self.cTransL) : (
                self.transMethod.cb.GetValue()),
            self.EqualLenLabel(self.cCorrL) : (
                self.corrMethod.cb.GetValue()),
            self.EqualLenLabel('Selected Columns') : (
                [int(x) for x in self.lbO.GetColContent(0)]),
        }

        msgStep = msgPrefix + 'User input, processing'
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        #------------------------------> Dict with all values
        self.do = {
            'uFile'      : Path(self.uFile.tc.GetValue()),
            'iFile'      : Path(self.iFile.tc.GetValue()),
            'TransMethod': self.transMethod.cb.GetValue(),
            'CorrMethod' : self.corrMethod.cb.GetValue(),
            'Column'     : [int(x) for x in self.lbO.GetColContent(0)],
        }
        #------------------------------> File base name
        self.oFolder = self.do['uFile'].parent
        #------------------------------> Date
        self.date = dtsMethod.StrNow()
        #endregion ----------------------------------------------------> Input

        return True
    #---

    def ReadInputFiles(self):
        """Read input file and check data"""
        #region ---------------------------------------------------------> Msg
        msgPrefix = config.lPdReadFile
        #endregion ------------------------------------------------------> Msg

        #region ---------------------------------------------------> Data file
        msgStep = msgPrefix + f"{self.ciFileL}, reading"
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        try:
            self.iFileObj = dtsFF.CSVFile(self.do['iFile'])
        except dtsException.FileIOError as e:
            self.msgError = str(e)
            self.tException = e
            return False
        #endregion ------------------------------------------------> Data file

        #region ------------------------------------------------------> Column
        msgStep = msgPrefix + f"{self.ciFileL}, data type"
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        self.df = self.iFileObj.df.iloc[:,self.do['Column']]
        try:
            self.dfI = self.df.astype('float')
        except Exception as e:
            self.msgError  = config.mPDDataTypeCol.format(
                self.ciFileL,
                ", ".join(map(str, self.do['Column'])),
            )
            self.tException = e
            return False
        #endregion ---------------------------------------------------> Column

        return True
    #---

    def RunAnalysis(self):
        """Calculate coefficients"""
        #region ---------------------------------------------------------> Msg
        msgPrefix = config.lPdRun
        #endregion ------------------------------------------------------> Msg

        #region -----------------------------------------------> Normalization
        #------------------------------> Msg
        msgStep = msgPrefix + f"Data normalization"
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        #------------------------------> 
        try:
            self.dfT = dtsStatistic.DataTransformation(
                self.dfI,
                sel = None,
                method = self.do['TransMethod'],
            )
        except Exception as e:
            self.msgError = str(e)
            self.tException = e
            return False
        #endregion --------------------------------------------> Normalization

        #region ------------------------------------> Correlation coefficients
        #------------------------------> Msg
        msgStep = msgPrefix + f"Correlation coefficients calculation"
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        #------------------------------> 
        try:
            self.RDF = self.dfT.corr(method=self.do['CorrMethod'].lower())
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
            config.fnTrans.format('02')   : self.dfT,
            self.cMainData.format('03')  : self.RDF,
        }
        #endregion -----------------------------------------------> Data Steps
        
        #region ---------------------------------------------------> Print
        if config.development:
            print('Input')
            for k,v in self.do.items():
                print(str(k)+': '+str(v))

            print("DataFrames: Initial")
            print(self.dfI)
            print("")
            print("DataFrames: Trans")
            print(self.dfT)
            print("")
            print("DataFrames: CC")
            print(self.RDF)
        else:
            pass
        #endregion ------------------------------------------------> Print

        return self.WriteOutputData(stepDict)
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

    def RunEnd(self):
        """Restart GUI and needed variables"""
        #region ---------------------------------------> Dlg progress dialogue
        if self.msgError is None:
            #--> 
            self.dlg.SuccessMessage(
                config.lPdDone,
                eTime=f"{config.lPdEllapsed} {self.deltaT}",
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
        self.d          = {} # Dict with the user input as given
        self.do         = {} # Dict with the processed user input
        self.dfI        = None # pd.DataFrame for initial, normalized and
        self.dfT        = None # correlation coefficients
        self.RDF        = None
        self.date       = None # date for corr file
        self.oFolder    = None # folder for output
        self.corrP      = None # path to the corr file that will be created
        self.deltaT     = None
        self.tException = None
        if self.dFile is not None:
            self.iFile.tc.SetValue(str(self.dFile))
        else:
            pass
        self.dFile = None # Data File copied to Data-Initial
        #endregion ----------------------------------------------------> Reset
    #---
    #endregion ------------------------------------------------> Class Methods
#---


#------------------------------> Modules
class ProtProf(BaseConfModPanel):
    """Creates the Proteome Profiling configuration tab

        Parameters
        ----------
        parent: wx.Widget
            Parent of the pane

        Attributes
        ----------
        

        Raises
        ------
        

        Methods
        -------
        
    """
    #region -----------------------------------------------------> Class setup
    name = 'ProtProfPane'
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent, dataI: Optional[dict]):
        """ """
        #region -------------------------------------------------> Check Input
        
        #endregion ----------------------------------------------> Check Input

        #region -----------------------------------------------> Initial Setup
        #------------------------------> Needed by BaseConfPanel
        self.cURL         = config.urlProtProf
        self.cSection     = config.nMProtProf
        self.cLenLongestL = len(config.lStResultCtrl)
        self.cTitlePD     = f"Running {config.nMProtProf} Analysis"
        self.cGaugePD     = 30
        #------------------------------> Optional configuration
        self.cHelpTT = config.ttBtnHelp.format(config.urlProtProf)
        #------------------------------> Base attributes and setup
        super().__init__(parent)
        #------------------------------> Needed to Run
        self.cMainData  = '{}-ProteomeProfiling-Data.txt'
        self.cChangeKey = ['iFile', 'uFile']
        self.dFile      = None
        #------------------------------> Labels
        self.cCorrectPL    = 'P Correction'
        self.cGeneNameL    = 'Gene Names'
        self.cExcludeProtL = 'Exclude Proteins'
        self.cSampleL      = 'Samples'
        self.cRawIL        = 'Intensities'
        #------------------------------> Choices
        self.cSampleO   = [x for x in config.oSamples.values()]
        self.cRawIO     = [x for x in config.oIntensities.values()]
        self.cCorrectPO = [x for x in config.oCorrectP.values()]
        #------------------------------> Tooltips
        self.cCorrectPTT    = config.ttStPCorrection
        self.cGeneNameTT    = config.ttStGenName
        self.cExcludeProtTT = config.ttStExcludeProt
        self.cSampleTT      = (
            f"Specify if samples are independent or paired.\n"
            f"For example, samples are paired when the same Petri dish is "
            f"used for the control and experiment.")
        self.cRawITT = (
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
            self.cCorrectPL,
            self.cCorrectPO,
            validator = dtsValidator.IsNotEmpty(),
        )
        
        self.sample = dtsWidget.StaticTextComboBox(
            self.sbValue,
            self.cSampleL,
            self.cSampleO,
            validator = dtsValidator.IsNotEmpty(),
        )
        
        self.rawI = dtsWidget.StaticTextComboBox(
            self.sbValue,
            self.cRawIL,
            self.cRawIO,
            validator = dtsValidator.IsNotEmpty(),
        )
        #------------------------------> Columns
        self.geneName = dtsWidget.StaticTextCtrl(
            self.sbColumn,
            stLabel   = self.cGeneNameL,
            tcSize    = self.cTcSize,
            validator = dtsValidator.NumberList(
                numType = 'int',
                nN      = 1,
                vMin    = 0,
            )
        )
        self.excludeProt = dtsWidget.StaticTextCtrl(
            self.sbColumn,
            stLabel   = self.cExcludeProtL,
            tcSize    = self.cTcSize,
            validator = dtsValidator.NumberList(
                numType = 'int',
                sep     = ' ',
                vMin    = 0,
                opt     = True,
            )
        )
        #endregion --------------------------------------------------> Widgets

        #region -----------------------------------------------------> Tooltip
        self.correctP.st.SetToolTip(self.cCorrectPTT)
        self.geneName.st.SetToolTip(self.cGeneNameTT)
        self.excludeProt.st.SetToolTip(self.cExcludeProtTT)
        self.sample.st.SetToolTip(self.cSampleTT)
        self.rawI.st.SetToolTip(self.cRawITT)
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
            self.transMethod.st,
            pos    = (0,3),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sizersbValueWid.Add(
            self.transMethod.cb,
            pos    = (0,4),
            flag   = wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sizersbValueWid.Add(
            self.normMethod.st,
            pos    = (1,3),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sizersbValueWid.Add(
            self.normMethod.cb,
            pos    = (1,4),
            flag   = wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sizersbValueWid.Add(
            self.imputationMethod.st,
            pos    = (2,3),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sizersbValueWid.Add(
            self.imputationMethod.cb,
            pos    = (2,4),
            flag   = wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sizersbValueWid.Add(
            self.correctP.st,
            pos    = (3,3),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sizersbValueWid.Add(
            self.correctP.cb,
            pos    = (3,4),
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
            #     1            : ['DMSO', 'H2O'],
            #     2            : ['30min', '1D'],
            #     'Control'    : ['MyControl'],
            #     'ControlType': 'One Control per Column',
            # }
            #--> One Control per Column, 1 Cond and 1 TP
            self.tcResults.SetValue('105 115 125, 130 131 132; 106 116 126, 101 111 121')
            self.lbDict = {
                1            : ['DMSO'],
                2            : ['30min', '60min'],
                'Control'    : ['MyControl'],
                'ControlType': 'One Control per Column',
            }
        else:
            pass
        #endregion -----------------------------------------------------> Test
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    #------------------------------> Run methods
    def CheckInput(self):
        """Check user input"""
        
        #region ---------------------------------------------------------> Msg
        msgPrefix = config.lPdCheck
        #endregion ------------------------------------------------------> Msg
        
        #region -------------------------------------------> Individual Fields
        #------------------------------> UMSAP File
        msgStep = msgPrefix + self.cuFileL
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        a, b = self.uFile.tc.GetValidator().Validate()
        if a:
            pass
        else:
            self.msgError = dtscore.StrSetMessage(
                config.mFileBad.format(b[1], self.cuFileL), b[2],
            )
            return False
        #------------------------------> Input file
        msgStep = msgPrefix + self.ciFileL
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        a, b = self.iFile.tc.GetValidator().Validate()
        if a:
            pass
        else:
            self.msgError = dtscore.StrSetMessage(
                config.mFileBad.format(b[1], self.ciFileL), b[2],
            )
            return False
        
        #------------------------------> Score Value
        msgStep = msgPrefix + self.cScoreValL
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        a, b = self.scoreVal.tc.GetValidator().Validate()
        if a:
            pass
        else:
            self.msgError = dtscore.StrSetMessage(
                config.mNumROne.format(self.cScoreValL), b[2],
            )
            return False
        #------------------------------> Sample
        msgStep = msgPrefix + self.cSampleL
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        if self.sample.cb.GetValidator().Validate()[0]:
            pass
        else:
            self.msgError = config.mNotEmpty.format(self.cSampleL)
            return False
        #------------------------------> Intensity
        msgStep = msgPrefix + self.cRawIL
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        if self.rawI.cb.GetValidator().Validate()[0]:
            pass
        else:
            self.msgError = config.mNotEmpty.format(self.cRawIL)
            return False
        #------------------------------> Transformation
        msgStep = msgPrefix + self.cTransMethodL
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        if self.transMethod.cb.GetValidator().Validate()[0]:
            pass
        else:
            self.msgError = config.mNotEmpty.format(self.cTransMethodL)
            return False
        #------------------------------> Normalization
        msgStep = msgPrefix + self.cNormMethodL
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        if self.normMethod.cb.GetValidator().Validate()[0]:
            pass
        else:
            self.msgError = config.mNotEmpty.format(self.cNormMethodL)
            return False
        #------------------------------> Imputation
        msgStep = msgPrefix + self.cImputationL
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        if self.imputationMethod.cb.GetValidator().Validate()[0]:
            pass
        else:
            self.msgError = config.mNotEmpty.format(self.cImputationL)
            return False
        #------------------------------> P Correction
        msgStep = msgPrefix + self.cCorrectPL
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        if self.correctP.cb.GetValidator().Validate()[0]:
            pass
        else:
            self.msgError = config.mNotEmpty.format(self.cCorrectPL)
            return False
        #------------------------------> Detected Proteins
        msgStep = msgPrefix + self.cDetectedProtL
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        a, b = self.detectedProt.tc.GetValidator().Validate(vMax=self.NCol)
        if a:
            pass
        else:
            msg = f"{config.mNumZPlusOne}\n{config.mFileColNum}".format(
                self.cDetectedProtL, self.ciFileL,
            )
            self.msgError = dtscore.StrSetMessage(msg, b[2])
            return False
        #------------------------------> Gene Names
        msgStep = msgPrefix + self.cGeneNameL
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        a, b = self.geneName.tc.GetValidator().Validate(vMax=self.NCol)
        if a:
            pass
        else:
            msg = f"{config.mNumZPlusOne}\n{config.mFileColNum}".format(
                self.cGeneNameL, self.ciFileL,
            )
            self.msgError = dtscore.StrSetMessage(msg, b[2])
            return False
        #------------------------------> Score
        msgStep = msgPrefix + self.cScoreColL
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        a, b = self.score.tc.GetValidator().Validate(vMax=self.NCol)
        if a:
            pass
        else:
            msg = f"{config.mNumZPlusOne}\n{config.mFileColNum}".format(
                self.cScoreColL, self.ciFileL,
            )
            self.msgError = dtscore.StrSetMessage(msg, b[2])
            return False
        #------------------------------> Exclude Proteins
        msgStep = msgPrefix + self.cExcludeProtL
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        a, b = self.excludeProt.tc.GetValidator().Validate(vMax=self.NCol)
        if a:
            pass
        else:
            msg = f"{config.mNumZPlusOne}\n{config.mFileColNum}".format(
                self.cExcludeProtL, self.ciFileL,
            )
            self.msgError = dtscore.StrSetMessage(msg, b[2])
            return False
        #------------------------------> Columns to Extract
        msgStep = msgPrefix + self.cColExtractL
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        a, b = self.colExtract.tc.GetValidator().Validate(vMax=self.NCol)
        if a:
            pass
        else:
            msg = f"{config.mNumZPlusOne}\n{config.mFileColNum}".format(
                self.cColExtractL, self.ciFileL,
            )
            self.msgError = dtscore.StrSetMessage(msg, b[2])
            return False
        #------------------------------> Results - Control Experiment
        msgStep = msgPrefix + self.cResControlL
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        a, b = self.tcResults.GetValidator().Validate()
        if a:
            pass
        else:
            self.msgError = config.mNotEmpty.format(self.cResControlL)
            return False
        #endregion ----------------------------------------> Individual Fields

        #region ------------------------------------------------> Mixed Fields
        #------------------------------> Raw or Ratio of intensities
        a = self.rawI.cb.GetValue()
        b = self.lbDict['ControlType']
        if a == b == config.oIntensities[2]:
            pass
        elif a != config.oIntensities[2] and b != config.oIntensities[2]:
            pass
        else:
            self.msgError = (
                f'The values for {self.cRawIL} ({self.rawI.cb.GetValue()}) '
                f'and Control Type ({self.lbDict["ControlType"]}) are '
                f'incompatible with each other.'
            )
            return False
        #------------------------------> Unique column numbers
        msgStep = msgPrefix + 'Unique column numbers'
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        #--------------> 
        l = [self.detectedProt.tc, self.geneName.tc, self.score.tc, 
            self.excludeProt.tc,
        ]
        #--------------> 
        a, b = check.UniqueColNumbers(l, self.tcResults)
        if a:
            pass
        else:
            msg = config.mColNumbers.format(config.mColNumbersNoColExtract)
            self.msgError = dtscore.StrSetMessage(msg, b[2])
            return False
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
            self.EqualLenLabel(self.ciFileL) : (
                self.iFile.tc.GetValue()),
            self.EqualLenLabel(self.cuFileL) : (
                self.uFile.tc.GetValue()),
            self.EqualLenLabel(self.cScoreValL) : (
                self.scoreVal.tc.GetValue()),
            self.EqualLenLabel(self.cTransMethodL) : (
                self.transMethod.cb.GetValue()),
            self.EqualLenLabel(self.cNormMethodL) : (
                self.normMethod.cb.GetValue()),
            self.EqualLenLabel(self.cImputationL) : (
                self.imputationMethod.cb.GetValue()),
            self.EqualLenLabel(self.cCorrectPL) : (
                self.correctP.cb.GetValue()),
            self.EqualLenLabel(self.cDetectedProtL) : (
                self.detectedProt.tc.GetValue()),
            self.EqualLenLabel(self.cGeneNameL) : (
                self.geneName.tc.GetValue()),
            self.EqualLenLabel(self.cScoreColL) : (
                self.score.tc.GetValue()),
            self.EqualLenLabel(self.cExcludeProtL) : (
                self.excludeProt.tc.GetValue()),
            self.EqualLenLabel(self.cColExtractL) : (
                self.colExtract.tc.GetValue()),
            self.EqualLenLabel(config.lStProtProfCond) : (
                self.lbDict[1]),
            self.EqualLenLabel(config.lStProtProfRP) : (
                self.lbDict[2]),
            self.EqualLenLabel(f"Control {config.lStCtrlType}") : (
                self.lbDict['ControlType']),
            self.EqualLenLabel(f"Control {config.lStCtrlName}") : (
                self.lbDict['Control']),
            self.EqualLenLabel(self.cResControlL): (
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
            'iFile'     : Path(self.iFile.tc.GetValue()),
            'uFile'     : Path(self.uFile.tc.GetValue()),
            'ScoreVal'  : float(self.scoreVal.tc.GetValue()),
            'NormMethod': self.normMethod.cb.GetValue(),
            'TranMethod': self.transMethod.cb.GetValue(),
            'Imputation': self.imputationMethod.cb.GetValue(),
            'CorrectP'  : self.correctP.cb.GetValue(),
            'Cond'      : self.lbDict[1],
            'RP'        : self.lbDict[2],
            'ControlT'  : self.lbDict['ControlType'],
            'oc' : {
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

        if config.development:
            print('self.d:')
            for k,v in self.d.items():
                print(str(k)+': '+str(v))
            print('self.do')
            for k,v in self.do.items():
                print(str(k)+': '+str(v))
        else:
            pass
        
        return True
    #---
    
    def ReadInputFiles(self):
        """Read input file and check data"""
        #region ---------------------------------------------------------> Msg
        msgPrefix = config.lPdReadFile
        #endregion ------------------------------------------------------> Msg

        #region ---------------------------------------------------> Data file
        #------------------------------> 
        msgStep = msgPrefix + f"{self.ciFileL}, reading"
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        #------------------------------> 
        try:
            self.iFileObj = dtsFF.CSVFile(self.do['iFile'])
        except dtsException.FileIOError as e:
            self.msgError = str(e)
            self.tException = e
            return False
        #endregion ------------------------------------------------> Data file

        #region ------------------------------------------------------> Column
        #------------------------------> 
        msgStep = msgPrefix + f"{self.ciFileL}, data type"
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
                self.ciFileL,
                ", ".join(map(str, self.do['oc']['Column'])),
            )
            self.tException = e
            return False
        #endregion ---------------------------------------------------> Column

        if config.development:
            print("self.dfI.shape: ", self.dfI.shape)
            print("self.dfF.shape: ", self.dfF.shape)
        
        return True
    #---
    
    def RunAnalysis(self):
        """Calculate proteome profiling data"""
        #region ---------------------------------------------------------> Msg
        msgPrefix = config.lPdRun
        #endregion ------------------------------------------------------> Msg
        
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
            
        if config.development:
            print('self.dfS.shape: ', self.dfS.shape)
        #endregion ----------------------------------------------------> Score
        
        #region ----------------------------------------------> Transformation
        #------------------------------> Msg
        msgStep = (
            f'{msgPrefix}'
            f'Performing data transformation - {self.do["TranMethod"]}'
        )  
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        #------------------------------> Transformed
        if self.do['TranMethod'] != 'None':
            try:
                self.dfT = dtsStatistic.DataTransformation(
                    self.dfS, 
                    self.do['df']['ResCtrlFlat'], 
                    method = self.do['TranMethod'],
                    rep    = np.nan,
                )
            except Exception as e:
                self.msgError   = config.mPDDataTran
                self.tException = e
                return False                
        else:
            self.dfT = self.dfS.copy()
        
        
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
        if self.do['NormMethod'] != 'None':
            try:
                self.dfN = dtsStatistic.DataNormalization(
                    self.dfT, 
                    self.do['df']['ResCtrlFlat'], 
                    method = self.do['NormMethod'],
                )
            except Exception as e:
                self.msgError   = config.mPDDataNorm
                self.tException = e
        else:
            self.dfN = self.dfT.copy()
        
        if config.development:
            print('self.dfN.shape: ', self.dfN.shape)
        #endregion --------------------------------------------> Normalization

        #region --------------------------------------------------> Imputation
        #------------------------------> Msg
        msgStep = (
            f'{msgPrefix}'
            f'Performing data imputation - {self.do["Imputation"]}'
        )  
        wx.CallAfter(self.dlg.UpdateStG, msgStep)
        #------------------------------> Imputation
        try:
            self.dfIm = dtsStatistic.DataImputation(
                self.dfN, 
                self.do['df']['ResCtrlFlat'], 
                method = self.do['Imputation'],
            )
        except Exception as e:
            self.msgError   = config.mPDDataImputation
            self.tException = e
        #------------------------------> Reset index
        self.dfIm.reset_index(drop=True, inplace=True)
        
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
        #endregion -----------------------------------------> Calculate values
        
        
        if config.development:
            print('self.dfR.shape: ', self.dfR.shape)
            print(self.dfR.head())
            print('')
        
        return False
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
        self.d   = {} # Dict with the user input as given
        self.do  = {} # Dict with the processed user input
        self.dfI = None # pd.DataFrame for initial, normalized and
        # self.dfT       = None # correlation coefficients
        # self.RDF      = None
        self.date      = None # date for corr file
        self.oFolder   = None # folder for output
        # self.corrP     = None # path to the corr file that will be created
        self.deltaT    = None
        
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
            np.nan, 
            columns=idx, 
            index=range(self.dfIm.shape[0]),
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
        if self.do['TranMethod'] == 'Log2':
            pass
        else:
            if colC is not None:
                dfLogI.iloc[:,colC+colD] = np.log2(dfLogI.iloc[:,colC+colD])
            else:
                dfLogI.iloc[:,colD] = np.log2(dfLogI.iloc[:,colD])
        #------------------------------> log2(FC)
        if colC is not None:
            FC = (
                self.dfLogI.iloc[:,colD].mean(axis=1, skipna=True)
                - self.dfLogI.iloc[:,colC].mean(axis=1, skipna=True)
            )
        else:
            FC = self.dfLogI.iloc[:,colD].mean(axis=1, skipna=True)
        
        self.dfR.loc[:, (cN, tN, 'FC')] = FC.to_numpy()
        #------------------------------> FCz
        self.dfR.loc[:,(cN, tN, 'FCz')] = (FC - FC.mean()).div(FC.std()).to_numpy()
        #------------------------------> FCci
        
        #------------------------------> P
        
        #------------------------------> Pc
        
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
    name = 'ResControlExpPaneProtProf'
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
        #------------------------------> 
        self.cTotalFieldTT = [
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
    
    def OnCreate(self, event) -> Literal[True]:
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
                            size      = self.cLabelS,
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
                            size      = self.cLabelS,
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


class ResControlExp(wx.Panel):
    """Creates the panel containig the panes for the dialog Results - Control
        Experiments

        Parameters
        ----------
        parent : wx.Widget
            Parent of the panel
        iFile : Path
            Path to the Data File already selected in the parent window
        topParent : wx.Widget
            Window calling the dialog 

        Attributes
        ----------
        name : str
            Unique name of the panel
        widget : ditc of methods
            Methods to create the configuration panel

        Raises
        ------
        

        Methods
        -------
        
    """
    #region -----------------------------------------------------> Class setup
    name = 'ResControlExpPane'

    widget = {
        'ProtProfPane' : ProtProfResControlExp,
    }
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent, iFile, topParent):
        """ """
        #region -------------------------------------------------> Check Input
        
        #endregion ----------------------------------------------> Check Input

        #region -----------------------------------------------> Initial Setup
        super().__init__(parent, name=self.name)
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------------> Menu
        
        #endregion -----------------------------------------------------> Menu

        #region -----------------------------------------------------> Widgets
        #------------------------------> ListCtrl and fill it
        self.lc = dtscore.ListZebraMaxWidth(
            self, 
            colLabel = config.lLCtrlColNameI,
            colSize  = config.sLCtrlColI,
        )
        dtsMethod.LCtrlFillColNames(self.lc, iFile)
        #------------------------------> Conf panel here to read NRow in lc
        self.conf = self.widget[topParent.name](
            self, topParent, self.lc.GetItemCount(),
        )
        #endregion --------------------------------------------------> Widgets

        #region -------------------------------------------------> Aui control
        #------------------------------> AUI control
        self._mgr = aui.AuiManager()
        #------------------------------> AUI which frame to use
        self._mgr.SetManagedWindow(self)
        #------------------------------> Add Configuration panel
        self._mgr.AddPane( 
            self.conf, 
            aui.AuiPaneInfo(
                ).Center(
                ).Caption(
                    config.lnPaneConf
                ).Floatable(
                    b=False
                ).CloseButton(
                    visible=False
                ).Movable(
                    b=False
                ).PaneBorder(
                    visible=True,
            ),
        )

        self._mgr.AddPane(
            self.lc, 
            aui.AuiPaneInfo(
                ).Right(
                ).Caption(
                    config.lnListPane
                ).Floatable(
                    b=False
                ).CloseButton(
                    visible=False
                ).Movable(
                    b=False
                ).PaneBorder(
                    visible=True,
            ),
        )

        self._mgr.Update()
        #endregion ----------------------------------------------> Aui control

        #region --------------------------------------------------------> Bind
        
        #endregion -----------------------------------------------------> Bind

        #region ---------------------------------------------> Window position
        
        #endregion ------------------------------------------> Window position
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    
    #endregion ------------------------------------------------> Class methods
#---
#endregion ----------------------------------------------------------> Classes


