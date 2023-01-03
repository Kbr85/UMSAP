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


"""Panes for the dataprep module of the app"""


#region -------------------------------------------------------------> Imports
from pathlib import Path

import wx

from config.config import config as mConfig
from core     import method    as cMethod
from core     import pane      as cPane
from core     import validator as cValidator
from core     import widget    as cWidget
from dataprep import method    as dataMethod
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Classes
class DataPrep(cPane.BaseConfPanel):
    """Data Preparation utility.

        Parameters
        ----------
        parent: wx.Window
            Parent of the pane.
        dataI: dict or None
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
                        'dfF' : Name of the file with initial data as float,
                        'dfT' : Name of the file with transformed data,
                        'dfN' : Name of the file with normalized data,
                        'dfIm': Name of the file with imputed data,
                    },
                }
            }
        }
    """
    #region -----------------------------------------------------> Class setup
    #------------------------------> Label
    cLColAnalysis = mConfig.core.lStColAnalysis
    cLPdRunText   = 'Performing Data Preparation Steps'
    #------------------------------> Tooltips
    cTTColAnalysis = ('Columns on which to perform the Data Preparation.\ne.g. '
                      '8 10-12')
    #------------------------------> Needed to Run
    cName           = mConfig.data.npDataPrep
    cURL            = f'{mConfig.core.urlTutorial}/data-preparation'
    cTTHelp         = mConfig.core.ttBtnHelp.format(cURL)
    cSection        = mConfig.data.nUtil
    cTitlePD        = f"Running {mConfig.data.nUtil} Analysis"
    cGaugePD        = 20
    rLLenLongest    = len(cLColAnalysis)
    rAnalysisMethod = dataMethod.DataPreparation
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent:wx.Window, dataI:dict={}) -> None:                # pylint: disable=dangerous-default-value
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(parent)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wSbValue.Hide()

        self.wColAnalysis = cWidget.StaticTextCtrl(
            self.wSbColumn,
            stLabel   = self.cLColAnalysis,
            stTooltip = self.cTTColAnalysis,
            tcSize    = self.cSTc,
            tcHint    = 'e.g. 130-135',
            validator = cValidator.NumberList(numType='int', sep=' ', vMin=0),
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
            self.cLColAnalysis: [self.wColAnalysis.wTc, mConfig.core.mNZPlusNumCol, True ],
        }
        self.rCheckUserInput = self.rCheckUserInput | rCheckUserInput
        #endregion -------------------------------------------> checkUserInput

        #region --------------------------------------------------------> Test
        if mConfig.core.development:
            # pylint: disable=line-too-long
            import getpass                                                      # pylint: disable=import-outside-toplevel
            user = getpass.getuser()
            if mConfig.core.os == "Darwin":
                self.wUFile.wTc.SetValue("/Users/" + str(user) + "/TEMP-GUI/BORRAR-UMSAP/umsap-dev.umsap")
                self.wIFile.wTc.SetValue("/Users/" + str(user) + "/Dropbox/SOFTWARE-DEVELOPMENT/APPS/UMSAP/LOCAL/DATA/UMSAP-TEST-DATA/PROTPROF/protprof-data-file.txt")
            elif mConfig.core.os == 'Windows':
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
    def SetInitialData(self, dataI: dict={}) -> bool:                           # pylint: disable=dangerous-default-value
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
            dataInit = dataI['uFile'].parent / mConfig.core.fnDataInit
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
        colAnalysis = cMethod.Str2ListNumber(
            self.wColAnalysis.wTc.GetValue(), sep=' ',
        )
        resCtrlFlat = [x for x in range(0, len(colAnalysis))]
        #-------------->
        self.rDO  = {
            'iFile'      : Path(self.wIFile.wTc.GetValue()),
            'uFile'      : Path(self.wUFile.wTc.GetValue()),
            'ID'         : self.wId.wTc.GetValue(),
            'Cero'       : mConfig.core.oYesNo[self.wCeroB.wCb.GetValue()],
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
        }
        #endregion -----------------------------------------------> Data Steps

        return self.WriteOutputData(stepDict)
    #---
    #endregion ------------------------------------------------> Run methods
#---
#endregion ----------------------------------------------------------> Classes
