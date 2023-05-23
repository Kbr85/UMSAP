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
from typing  import Optional

import wx

from config.config import config as mConfig
from core import method    as cMethod
from core import pane      as cPane
from core import widget    as cWidget
from core import validator as cValidator
from corr import method    as corrMethod
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Classes
class CorrA(cPane.BaseConfPanel):
    """Creates the configuration tab for Correlation Analysis.

        Parameters
        ----------
        parent: wx.Window
            Parent of the widgets.

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

        The Correlation Analysis section in output-file.umsap contains the
        information about the calculations, e.g

        {
            'Correlation-Analysis : {
                '20210324-165609 - bla': {
                    'V' : config.dictVersion,
                    'I' : Dict with User Input as given. Keys are label like in the Tab GUI,
                    'CI': Dict with Processed User Input. Keys are attributes of UserData,
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
    cSection        = mConfig.corr.tUtil
    cTitlePD        = 'Calculating Correlation Coefficients'
    cGaugePD        = 20
    cTTHelp         = mConfig.core.ttBtnHelp.format(cURL)
    rMainData       = '{}_{}-CorrelationCoefficients-Data.txt'
    rAnalysisMethod = corrMethod.CorrA
    #endregion --------------------------------------------------> Class Setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent:wx.Window) -> None:
        """"""
        #region -----------------------------------------------> Initial setup
        super().__init__(parent, label=mConfig.core.lStResCtrlGroup)
        #endregion --------------------------------------------> Initial setup

        #region -----------------------------------------------------> Widgets
        self.wCorrMethod = cWidget.StaticTextComboBox(self.wSbValue,
            label     = self.cLCorrMethod,
            tooltip   = f'Select the {self.cLCorrMethod}.',
            choices   = mConfig.corr.oCorrMethod,
            validator = cValidator.IsNotEmpty(),
        )
        #endregion --------------------------------------------------> Widgets

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
            self.sRes,
            pos    = (0,0),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND,
            border = 0,
            span   = (0,6),
        )
        self.sSbColumnWid.AddGrowableCol(1,1)
        #------------------------------> Main Sizer
        self.SetSizer(self.sSizer)
        self.sSizer.Fit(self)
        self.SetupScrolling()
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind

        #endregion -----------------------------------------------------> Bind

        #region ----------------------------------------------> checkUserInput
        rCheckUserInput = {
            self.cLCorrMethod : [self.wCorrMethod.wCb, mConfig.core.mOptionBad, False],
            self.cLResControl : [self.wTcResults,      mConfig.core.mResCtrl,   False],
        }
        self.rCheckUserInput = self.rCheckUserInput | rCheckUserInput
        #endregion -------------------------------------------> checkUserInput
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Event Methods

    #endregion ------------------------------------------------> Event Methods

    #region ---------------------------------------------------> Class Methods
    def SetInitialData(self, dataI:Optional[corrMethod.UserData]) -> bool:
        """Set initial data.

            Parameters
            ----------
            dataI: corrMethod.UserData or None
                Data class representation of the already run analysis.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------------> Add
        if dataI is not None:
            self.wUFile.wTc.SetValue(str(dataI.uFile))
            self.wIFile.wTc.SetValue(str(dataI.iFile))
            self.wId.wTc.SetValue(dataI.ID)
            self.wCeroB.wCb.SetValue('Yes' if dataI.cero else 'No')
            self.wTransMethod.wCb.SetValue(dataI.tran)
            self.wNormMethod.wCb.SetValue(dataI.norm)
            self.wImputationMethod.wCb.SetValue(dataI.imp)
            self.wCorrMethod.wCb.SetValue(dataI.corr)
            self.wShift.wTc.SetValue(str(dataI.shift))
            self.wWidth.wTc.SetValue(str(dataI.width))
            self.wTcResults.SetValue(dataI.resCtrl)
            self.rLbDict = {
                0            : dataI.labelA,
                'MinRep'     : dataI.minRep,
                'Control'    : [''],
                'ControlType': '',
            }
            #------------------------------>
            self.OnImpMethod('fEvent')
        else:
            super().SetConfOptions()
            #------------------------------>
            self.wCorrMethod.wCb.SetValue(mConfig.corr.corrMethod)
        #endregion -----------------------------------------------------> Add

        #region --------------------------------------------------------> Test
        if mConfig.core.development and dataI is None:
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
            self.wTcResults.SetValue('98 99 100 101 102; 103 104 105 106 107; 108 109 110 111 112')
            self.rLbDict = {
                0             : ['Group - 1', 'Group - 2', 'Group - 3'],
                'Control'     : [''],
                'ControlType' : '',
                'MinRep'      : '3; 3; 3',
            }
        #endregion -----------------------------------------------------> Test

        return True
    #---
    #endregion ------------------------------------------------> Class Methods

    #region ---------------------------------------------------> Run Analysis
    def CheckInput(self) -> bool:
        """Check user input.

            Returns
            -------
            bool
        """
        #region -------------------------------------------------------> Super
        if not super().CheckInput():
            return False
        #endregion ----------------------------------------------------> Super

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
        #------------------------------> Read
        minRepList    = cMethod.ResControl2ListNumber(self.rLbDict['MinRep'])
        resCtrl       = cMethod.ResControl2ListNumber(self.wTcResults.GetValue())
        resCtrlFlat   = cMethod.ResControl2Flat(resCtrl)
        resCtrlDF     = cMethod.ResControl2DF(resCtrl, 0)
        resCtrlDFFlat = cMethod.ResControl2Flat(resCtrlDF)
        impMethod = self.wImputationMethod.wCb.GetValue()
        dI = {
            'iFileN'       : self.cLiFile,
            'ID'           : self.cLId,
            'cero'         : self.cLCeroTreatD,
            'tran'         : self.cLTransMethod,
            'norm'         : self.cLNormMethod,
            'imp'          : self.cLImputation,
            'shift'        : self.cLShift,
            'width'        : self.cLWidth,
            'corr'         : self.cLCorrMethod,
            'resCtrl'      : mConfig.core.lStResCtrlGroup,
            'minRep'       : 'Valid Replicates',
        }
        if impMethod != mConfig.data.lONormDist:
            dI.pop('shift')
            dI.pop('width')
        #------------------------------>
        msgStep = self.cLPdPrepare + 'User input, processing'
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        #------------------------------> Create DataClass Instance
        self.rDO = corrMethod.UserData(
            uFile         = Path(self.wUFile.wTc.GetValue()),
            iFile         = Path(self.wIFile.wTc.GetValue()),
            ID            = self.wId.wTc.GetValue(),
            cero          = mConfig.core.oYesNo[self.wCeroB.wCb.GetValue()],
            tran          = self.wTransMethod.wCb.GetValue(),
            norm          = self.wNormMethod.wCb.GetValue(),
            imp           = impMethod,
            shift         = float(self.wShift.wTc.GetValue()),
            width         = float(self.wWidth.wTc.GetValue()),
            corr          = self.wCorrMethod.wCb.GetValue(),
            labelA        = self.rLbDict[0],
            minRep        = self.rLbDict['MinRep'],
            minRepList    = minRepList,
            resCtrl       = self.wTcResults.GetValue(),
            ocResCtrl     = resCtrl,
            ocResCtrlFlat = resCtrlFlat,
            ocColumn      = resCtrlFlat,
            dfColumnR     = resCtrlDFFlat,
            dfColumnF     = resCtrlDFFlat,
            dfResCtrl     = resCtrlDF,
            dfResCtrlFlat = resCtrlDFFlat,
            dI            = dI,
        )
        #endregion ----------------------------------------------------> Input

        #region -------------------------------------------------------> Super
        if not super().PrepareRun():
            self.rMsgError = 'Something went wrong when preparing the analysis.'
            return False
        #endregion ----------------------------------------------------> Super

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
            mConfig.core.fnMinRep.format(self.rDate, '03') : self.dfMR,
            mConfig.core.fnTrans.format(self.rDate, '04')  : self.dfT,
            mConfig.core.fnNorm.format(self.rDate, '05')   : self.dfN,
            mConfig.core.fnImp.format(self.rDate, '06')    : self.dfIm,
            self.rMainData.format(self.rDate, '07')        : self.dfR,
        }
        stepDict['R'] = self.rMainData.format(self.rDate, '07')
        #endregion -----------------------------------------------> Data Steps

        return self.WriteOutputData(stepDict)
    #---
    #endregion ------------------------------------------------> Run Analysis
#---
#endregion ----------------------------------------------------------> Classes
