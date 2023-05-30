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
from dataprep import method    as dataMethod
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Classes
class DataPrep(cPane.BaseConfPanel):
    """Data Preparation utility.

        Parameters
        ----------
        parent: wx.Window
            Parent of the pane.

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
                        'dfF' : Name of file with initial data as float
                        'dfMP': Name of file with minimum valid replicate filter
                        'dfT' : Name of file with transformed data.
                        'dfN' : Name of file with normalized data.
                        'dfIm': Name of file with imputed data.
                    },
                }
            }
        }
        Each pd.DataFrame in DP contains a header with the column name and values
        are the data processed values.
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
    cSection        = mConfig.data.tUtil
    cTitlePD        = f"Running {mConfig.data.tUtil} Analysis"
    cGaugePD        = 19
    rAnalysisMethod = dataMethod.RunDataPreparation
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent:wx.Window) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(parent, label=mConfig.core.lStResCtrlGroup)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wSbValue.Hide()
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        #------------------------------> Sizer Columns
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

        #region ----------------------------------------------> checkUserInput
        rCheckUserInput = {
            self.cLResControl : [self.wTcResults, mConfig.core.mResCtrl, False],
        }
        self.rCheckUserInput = self.rCheckUserInput | rCheckUserInput
        #endregion -------------------------------------------> checkUserInput
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class Methods
    def SetInitialData(self, dataI:Optional[dataMethod.UserData]) -> bool:
        """Set initial data.

            Parameters
            ----------
            dataI: dataMethod.UserData or None
                Data to fill all fields and repeat an analysis.

            Returns
            -------
            True
        """
        #region -------------------------------------------------> Fill Fields
        if dataI is not None:
            self.wUFile.wTc.SetValue(str(dataI.uFile))
            self.wIFile.wTc.SetValue(str(dataI.iFile))
            self.wId.wTc.SetValue(dataI.ID)
            self.wCeroB.wCb.SetValue('Yes' if dataI.cero else 'No')
            self.wTransMethod.wCb.SetValue(dataI.tran)
            self.wNormMethod.wCb.SetValue(dataI.norm)
            self.wImputationMethod.wCb.SetValue(dataI.imp)
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
        #endregion ----------------------------------------------> Fill Fields

        #region --------------------------------------------------------> Test
        if mConfig.core.development and dataI is None:
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
            self.OnImpMethod('fEvent')
            self.wShift.wTc.SetValue('1.8')
            self.wWidth.wTc.SetValue('0.3')
            self.wTcResults.SetValue('130 131 132 133 134; 135 136 137 138 139; 140 141 142 143 144')
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
        impMethod     = self.wImputationMethod.wCb.GetValue()
        minRepList    = cMethod.ResControl2ListNumber(self.rLbDict['MinRep'])
        resCtrl       = cMethod.ResControl2ListNumber(self.wTcResults.GetValue())
        resCtrlFlat   = cMethod.ResControl2Flat(resCtrl)
        resCtrlDF     = cMethod.ResControl2DF(resCtrl, 0)
        resCtrlDFFlat = cMethod.ResControl2Flat(resCtrlDF)
        dI            = {
            'iFileN'       : self.cLiFile,
            'ID'           : self.cLId,
            'cero'         : self.cLCeroTreatD,
            'tran'         : self.cLTransMethod,
            'norm'         : self.cLNormMethod,
            'imp'          : self.cLImputation,
            'shift'        : self.cLShift,
            'width'        : self.cLWidth,
            'resCtrl'      : mConfig.core.lStResCtrlGroup,
            'minRep'       : mConfig.core.lStValRep,
        }
        if impMethod != mConfig.data.lONormDist:
            dI.pop('shift')
            dI.pop('width')
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
            mConfig.core.fnInitial.format(self.rDate, '01') : self.dfI,
            mConfig.core.fnFloat.format(self.rDate,   '02') : self.dfF,
            mConfig.core.fnMinRep.format(self.rDate,  '03') : self.dfMR,
            mConfig.core.fnTrans.format(self.rDate,   '04') : self.dfT,
            mConfig.core.fnNorm.format(self.rDate,    '05') : self.dfN,
            mConfig.core.fnImp.format(self.rDate,     '06') : self.dfIm,
        }
        #endregion -----------------------------------------------> Data Steps

        return self.WriteOutputData(stepDict)
    #---
    #endregion ------------------------------------------------> Run methods
#---
#endregion ----------------------------------------------------------> Classes
