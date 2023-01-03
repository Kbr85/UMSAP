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


"""Pane for the corr module of the app"""


#region -------------------------------------------------------------> Imports
from pathlib import Path
from typing  import Union

import wx

from config.config import config as mConfig
from core import pane   as cPane
from core import widget as cWidget
from core import validator as cValidator
from corr import method as corrMethod
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Classes
class CorrA(cPane.BaseConfPanel):
    """Creates the configuration tab for Correlation Analysis.

        Parameters
        ----------
        parent: wx.Window
            Parent of the widgets.
        dataI: dict
            Initial data provided by the user in a previous analysis.
            This contains both I and CI dicts e.g. {'I': I, 'CI': CI}

        Notes
        -----
        The structures of self.rDO and self.rDI are:
        rDO: dict
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
        rDI: dict
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
                        'dfF' : Name of file with initial data as float
                        'dfT' : Name of file with transformed data.
                        'dfN' : Name of file with normalized data.
                        'dfIm': Name of file with imputed data.
                    }
                    'R' : Name of result file
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
    cLCorrMethod  = 'Correlation Method'
    cLColAnalysis = mConfig.core.lStColAnalysis
    cLNumName     = mConfig.core.lLCtrlColNameI
    cSNumName     = mConfig.core.sLCtrlColI
    cLPdRunText   = 'Calculating Correlation Coefficients'
    #------------------------------> Needed by BaseConfPanel
    cName           = mConfig.corr.nPane
    cURL            = f'{mConfig.core.urlTutorial}/correlation-analysis'
    cSection        = mConfig.corr.nUtil
    cTitlePD        = 'Calculating Correlation Coefficients'
    cGaugePD        = 21
    cTTHelp         = mConfig.core.ttBtnHelp.format(cURL)
    rLLenLongest    = len(cLCorrMethod)
    rMainData       = '{}_{}-CorrelationCoefficients-Data.txt'
    rAnalysisMethod = corrMethod.CorrA
    #endregion --------------------------------------------------> Class Setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent:wx.Window, dataI:dict={}):                        # pylint: disable=dangerous-default-value
        """"""
        #region -----------------------------------------------> Initial setup
        super().__init__(parent)
        #endregion --------------------------------------------> Initial setup

        #region -----------------------------------------------------> Widgets
        self.wCorrMethod = cWidget.StaticTextComboBox(self.wSbValue,
            label     = self.cLCorrMethod,
            tooltip   = f'Select the {self.cLCorrMethod}.',
            choices   = list(mConfig.corr.oCorrMethod.values()),
            validator = cValidator.IsNotEmpty(),
        )
        self.wStListI = wx.StaticText(
            self.wSbColumn, label=f'Columns in the {self.cLiFile}')
        self.wStListO = wx.StaticText(
            self.wSbColumn, label=f'{self.cLColAnalysis}')
        self.wLCtrlI = cWidget.MyListCtrlZebra(self.wSbColumn,
            colLabel        = self.cLNumName,
            colSize         = self.cSNumName,
            copyFullContent = True,
        )
        self.wLCtrlO = cWidget.MyListCtrlZebra(self.wSbColumn,
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
        self.wStListI.SetToolTip(mConfig.core.ttLCtrlCopyNoMod)
        self.wStListO.SetToolTip(mConfig.core.ttLCtrlPasteMod)
        self.wAddCol.SetToolTip(
            'Add selected Columns in the Data File to '
            'the table of Columns to Analyze. New columns will be added after '
            'the last selected element in Columns to Analyze. Duplicate '
            'columns are discarded.')
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
            self.cLCorrMethod : [self.wCorrMethod.wCb, mConfig.core.mOptionBad, False],
        }
        self.rCheckUserInput = self.rCheckUserInput | rCheckUserInput
        #endregion -------------------------------------------> checkUserInput

        #region --------------------------------------------------------> Test
        if mConfig.core.development:
            import getpass                                                      # pylint: disable=import-outside-toplevel
            user = getpass.getuser()
            if mConfig.core.os == "Darwin":
                self.wUFile.wTc.SetValue("/Users/" + str(user) + "/TEMP-GUI/BORRAR-UMSAP/umsap-dev.umsap")
                fDataTemp = "/Users/" + str(user) + "/Dropbox/SOFTWARE-DEVELOPMENT/APPS/UMSAP/LOCAL/DATA/UMSAP-TEST-DATA/TARPROT/tarprot-data-file.txt"
                self.wIFile.wTc.SetValue(fDataTemp)
                self.IFileEnter(fDataTemp)
            elif mConfig.core.os == 'Windows':
                self.wUFile.wTc.SetValue(str(Path('C:/Users/bravo/Desktop/SharedFolders/BORRAR-UMSAP/umsap-dev.umsap')))
                self.wIFile.wTc.SetValue(str(Path(f'C:/Users/{user}/Dropbox/SOFTWARE-DEVELOPMENT/APPS/UMSAP/LOCAL/DATA/UMSAP-TEST-DATA/TARPROT/tarprot-data-file.txt')))
            self.wId.wTc.SetValue("Beta Version Dev")
            self.wCeroB.wCb.SetValue("Yes")
            self.wTransMethod.wCb.SetValue("Log2")
            self.wNormMethod.wCb.SetValue("Median")
            self.wImputationMethod.wCb.SetValue("Normal Distribution")
            self.OnImpMethod('fEvent')
            self.wShift.wTc.SetValue('1.8')
            self.wWidth.wTc.SetValue('0.3')
            self.wCorrMethod.wCb.SetValue("Pearson")
        #endregion -----------------------------------------------------> Test

        #region -------------------------------------------------------> DataI
        self.SetInitialData(dataI)
        #endregion ----------------------------------------------------> DataI
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Event Methods
    def OnAdd(self, event:Union[wx.Event, str]) -> bool:                        # pylint: disable=unused-argument
        """Add columns to analyze using the button.

            Parameters
            ----------
            event: wx.Event
                Event information.

            Returns
            -------
            bool
        """
        self.wLCtrlI.OnCopy('fEvent')
        self.wLCtrlO.OnPaste('fEvent')
        return True
    #---
    #endregion ------------------------------------------------> Event Methods

    #region ---------------------------------------------------> Class Methods
    def SetInitialData(self, dataI:dict={}) -> bool:                            # pylint: disable=dangerous-default-value
        """Set initial data.

            Parameters
            ----------
            dataI: dict
                Data to fill all fields and repeat an analysis. See Notes.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------------> Add
        if dataI:
            #------------------------------>
            dataInit = dataI['uFile'].parent / mConfig.core.fnDataInit
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
                        l.append(k)
                        continue
                    #------------------------------>
                    if k > l[-1]:
                        l.append(k)
                        continue
                    #------------------------------>
                    self.wLCtrlI.SelectList(l)
                    self.OnAdd('fEvent')
                    #------------------------------>
                    l = [k]
                #------------------------------> Last past
                self.wLCtrlI.SelectList(l)
                self.OnAdd('fEvent')
            #------------------------------>
            self.OnImpMethod('fEvent')
        #endregion -----------------------------------------------------> Add

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
        if not super().CheckInput():
            return False
        #endregion ----------------------------------------------------> Super

        #region -------------------------------------------> Individual Fields
        #region -------------------------------------------> ListCtrl
        msgStep = self.cLPdCheck +  self.cLColAnalysis
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        if not self.wLCtrlO.GetItemCount() > 1:
            self.rMsgError = mConfig.core.mRowsInLCtrl.format(2, self.cLColAnalysis)
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
        colF = list(range(0, len(col)))
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
            'Cero'       : mConfig.core.oYesNo[self.wCeroB.wCb.GetValue()],
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
        if not super().PrepareRun():
            self.rMsgError = 'Something went wrong when preparing the analysis.'
            return False
        #endregion ------------------------------------------------> Super

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
            mConfig.core.fnInitial.format(self.rDate, '01'): self.dfI,
            mConfig.core.fnFloat.format(self.rDate, '02')  : self.dfF,
            mConfig.core.fnTrans.format(self.rDate, '03')  : self.dfT,
            mConfig.core.fnNorm.format(self.rDate, '04')   : self.dfN,
            mConfig.core.fnImp.format(self.rDate, '05')    : self.dfIm,
            self.rMainData.format(self.rDate, '06')   : self.dfR,
        }
        stepDict['R'] = self.rMainData.format(self.rDate, '06')
        #endregion -----------------------------------------------> Data Steps

        return self.WriteOutputData(stepDict)
    #---
    #endregion ------------------------------------------------> Run Analysis
#---
#endregion ----------------------------------------------------------> Classes
