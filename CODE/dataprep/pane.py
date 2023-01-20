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
from typing  import Optional

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
        dataI: dataMethod.UseData or None
            Initial data provided by the user in a previous analysis.
            Default is None.

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

        The Data Preparation section in output-file.umsap contains the
        information about the calculations, e.g
        {
            'Data Preparation : {
                '20210324-165609': {
                    'V' : config.dictVersion,
                    'I' : Dict with User Input as given. Keys are label like in the Tab GUI,
                    'CI': Dict with Processed User Input. Keys are attributes of UserData,
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
    cName           = mConfig.data.nPane
    cURL            = f'{mConfig.core.urlTutorial}/data-preparation'
    cTTHelp         = mConfig.core.ttBtnHelp.format(cURL)
    cSection        = mConfig.data.nUtil
    cTitlePD        = f"Running {mConfig.data.nUtil} Analysis"
    cGaugePD        = 19
    rAnalysisMethod = dataMethod.DataPreparation
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self,
        parent:wx.Window,
        dataI:Optional[dataMethod.UserData]=None,
        ) -> None:
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

        #region -------------------------------------------------------> DataI
        if dataI is not None:
            self.SetInitialData(dataI)
        #endregion ----------------------------------------------------> DataI
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class Methods
    def SetInitialData(self, dataI:dataMethod.UserData) -> bool:
        """Set initial data.

            Parameters
            ----------
            dataI: dataMethod.UserData
                Data to fill all fields and repeat an analysis.

            Returns
            -------
            True
        """
        #region -------------------------------------------------> Fill Fields
        self.wUFile.wTc.SetValue(str(dataI.uFile))
        self.wIFile.wTc.SetValue(str(dataI.iFile))
        self.wId.wTc.SetValue(dataI.ID)
        self.wCeroB.wCb.SetValue('Yes' if dataI.cero else 'No')
        self.wTransMethod.wCb.SetValue(dataI.tran)
        self.wNormMethod.wCb.SetValue(dataI.norm)
        self.wImputationMethod.wCb.SetValue(dataI.imp)
        self.wShift.wTc.SetValue(str(dataI.shift))
        self.wWidth.wTc.SetValue(str(dataI.width))
        self.wColAnalysis.wTc.SetValue(" ".join(map(str, dataI.ocResCtrlFlat)))
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
        if not super().CheckInput():
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
        impMethod   = self.wImputationMethod.wCb.GetValue()
        colAnalysis = cMethod.Str2ListNumber(
            self.wColAnalysis.wTc.GetValue(), numType='int', sep=' ')
        resCtrlFlat = [x for x in range(0, len(colAnalysis))]
        dI = {
            'iFileN'       : self.cLiFile,
            'ID'           : self.cLId,
            'cero'         : self.cLCeroTreatD,
            'tran'         : self.cLTransMethod,
            'norm'         : self.cLNormMethod,
            'imp'          : self.cLImputation,
            'ocResCtrlFlat': self.cLColAnalysis,
        }
        if impMethod == mConfig.data.lONormDist:
            dI['shift'] = self.cLShift
            dI['width'] = self.cLWidth
        #------------------------------> Dict with all values
        msgStep = self.cLPdPrepare + 'User input, processing'
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        #-------------->
        self.rDO = dataMethod.UserData(
            uFile         = Path(self.wUFile.wTc.GetValue()),
            iFile         = Path(self.wIFile.wTc.GetValue()),
            ID            = self.wId.wTc.GetValue(),
            cero          = mConfig.core.oYesNo[self.wCeroB.wCb.GetValue()],
            norm          = self.wNormMethod.wCb.GetValue(),
            tran          = self.wTransMethod.wCb.GetValue(),
            imp           = impMethod,
            shift         = float(self.wShift.wTc.GetValue()),
            width         = float(self.wWidth.wTc.GetValue()),
            ocColumn      = colAnalysis,                                        # type: ignore
            ocResCtrlFlat = colAnalysis,                                        # type: ignore
            dfColumnR     = resCtrlFlat,
            dfColumnF     = resCtrlFlat,
            dfResCtrlFlat = resCtrlFlat,
            dI            = dI,
        )
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
