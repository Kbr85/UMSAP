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


"""Panes for the limprot module of the app"""


#region -------------------------------------------------------------> Imports
from typing  import Optional
from pathlib import Path

import wx

from config.config import config as mConfig
from core    import method    as cMethod
from core    import pane      as cPane
from core    import validator as cValidator
from core    import widget    as cWidget
from limprot import method    as limpMethod
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Classes
class LimProt(cPane.BaseConfPanelMod2):
    """Configuration Pane for the Limited Proteolysis module.

        Parameters
        ----------
        parent: wx.Window
            Parent of the pane.
        dataI: limpMethod.UserData or None
            Initial data provided by the user in a previous analysis.
            Default is None.

        Attributes
        ----------
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
                    'I' : Dict with User Input as given. Keys are label like in the Tab GUI,
                    'CI': Dict with Processed User Input. Keys are attributes of UserData,
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
    cName = mConfig.limp.nPane
    #------------------------------> Label
    cLBeta         = "β level"
    cLGamma        = "γ level"
    cLTheta        = "Θ value"
    cLThetaMax     = "Θmax value"
    cLSample       = 'Samples'
    cLLane         = mConfig.limp.lStLane
    cLBand         = mConfig.limp.lStBand
    cLCtrlName     = mConfig.core.lStCtrlName
    cLDFFirstThree = mConfig.limp.dfcolFirstPart
    cLDFThirdLevel = mConfig.limp.dfcolCLevel
    cLPdRunText    = 'Performing Limited Proteolysis analysis'
    #------------------------------> Choices
    cOSample = mConfig.core.oSamples
    #------------------------------> Hints
    cHBeta     = 'e.g. 0.05'
    cHGamma    = 'e.g. 0.8'
    cHTheta    = 'e.g. 4.5'
    cHThetaMax = 'e.g. 8'
    #------------------------------> Tooltips
    cTTSample = mConfig.core.ttStSample
    cTTBeta = ('Beta level for the analysis.\ne.g. 0.05')
    cTTGamma = ('Confidence limit level for estimating the measuring '
                'precision.\ne.g. 0.80')
    cTTTheta = ('Confidence interval used in the analysis. The value depends '
        'on the Data Preparation selected. An empty values means that the '
        'confidence interval will be calculated for each peptide.\ne.g. 3')
    cTTThetaMax = (f'Maximum value for the calculated Confidence interval. It '
        f'is only used if {cLTheta} is left empty.\ne.g. 8')
    #------------------------------> Needed by BaseConfPanel
    cURL            = f"{mConfig.core.urlTutorial}/limited-proteolysis"
    cSection        = mConfig.limp.nMod
    cTitlePD        = f"Running {mConfig.limp.nMod} Analysis"
    cGaugePD        = 34
    rMainData       = '{}_{}-LimitedProteolysis-Data.txt'
    rAnalysisMethod = limpMethod.LimProt
    #------------------------------> Optional configuration
    cTTHelp = mConfig.core.ttBtnHelp.format(cURL)
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self,
        parent,
        dataI:Optional[limpMethod.UserData]=None,
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(parent)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        #------------------------------> Values
        self.wBeta = cWidget.StaticTextCtrl(
            self.wSbValue,
            stLabel   = self.cLBeta,
            stTooltip = self.cTTBeta,
            tcSize    = self.cSTc,
            tcHint    = self.cHBeta,
            validator = cValidator.NumberList(
                numType='float', nN=1, vMin=0, vMax=1),
        )
        self.wGamma = cWidget.StaticTextCtrl(
            self.wSbValue,
            stLabel   = self.cLGamma,
            stTooltip = self.cTTGamma,
            tcSize    = self.cSTc,
            tcHint    = self.cHGamma,
            validator = cValidator.NumberList(
                numType='float', nN=1, vMin=0, vMax=1),
        )
        self.wTheta = cWidget.StaticTextCtrl(
            self.wSbValue,
            stLabel   = self.cLTheta,
            stTooltip = self.cTTTheta,
            tcSize    = self.cSTc,
            tcHint    = self.cHTheta,
            validator = cValidator.NumberList(
                numType='float', nN=1, vMin=0.01, opt=True),
        )
        self.wThetaMax = cWidget.StaticTextCtrl(
            self.wSbValue,
            stLabel   = self.cLThetaMax,
            stTooltip = self.cTTThetaMax,
            tcSize    = self.cSTc,
            tcHint    = self.cHThetaMax,
            validator = cValidator.NumberList(
                numType='float', nN=1, vMin=0.01),
        )
        self.wSample = cWidget.StaticTextComboBox(
            self.wSbValue,
            label     = self.cLSample,
            choices   = list(self.cOSample.keys()),
            tooltip   = self.cTTSample,
            validator = cValidator.IsNotEmpty(),
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
        label = f'{self.cLSeqCol} column'
        rCheckUserInput = {
            self.cLSample       : [ self.wSample.wCb,       mConfig.core.mOptionBad,      False],
            self.cLAlpha        : [ self.wAlpha.wTc,        mConfig.core.mOne01Num,       False],
            self.cLBeta         : [ self.wBeta.wTc,         mConfig.core.mOne01Num,       False],
            self.cLGamma        : [ self.wGamma.wTc,        mConfig.core.mOne01Num,       False],
            self.cLTheta        : [ self.wTheta.wTc,        mConfig.core.mOneZPlusNumCol, False],
            label               : [ self.wSeqCol.wTc,       mConfig.core.mOneZPlusNumCol, True ],
            self.cLDetectedProt : [ self.wDetectedProt.wTc, mConfig.core.mOneZPlusNumCol, True ],
            self.cLScoreCol     : [ self.wScore.wTc,        mConfig.core.mOneZPlusNumCol, True ],
            self.cLResControl   : [ self.wTcResults,        mConfig.core.mResCtrl       , False],
        }
        self.rCheckUserInput = self.rCheckUserInput | rCheckUserInput
        #endregion -------------------------------------------> checkUserInput

        #region -------------------------------------------------------> DataI
        if dataI is not None:
            self.SetInitialData(dataI)
        #endregion ----------------------------------------------------> DataI
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class Event
    def SetInitialData(self, dataI:limpMethod.UserData) -> bool:
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
        #------------------------------> Files
        self.wUFile.wTc.SetValue(str(dataI.uFile))
        self.wIFile.wTc.SetValue(str(dataI.iFile))
        self.wSeqFile.wTc.SetValue(str(dataI.seqFile))
        self.wId.wTc.SetValue(dataI.ID)
        #------------------------------> Data Preparation
        self.wCeroB.wCb.SetValue('Yes' if dataI.cero else 'No')
        self.wTransMethod.wCb.SetValue(dataI.tran)
        self.wNormMethod.wCb.SetValue(dataI.norm)
        self.wImputationMethod.wCb.SetValue(dataI.imp)
        self.wShift.wTc.SetValue(str(dataI.shift))
        self.wWidth.wTc.SetValue(str(dataI.width))
        #------------------------------> Values
        self.wTargetProt.wTc.SetValue(dataI.targetProt)
        self.wScoreVal.wTc.SetValue(str(dataI.scoreVal))
        self.wAlpha.wTc.SetValue(str(dataI.alpha))
        self.wSample.wCb.SetValue(mConfig.core.oSamplesP[dataI.indSample])
        self.wBeta.wTc.SetValue(str(dataI.beta))
        self.wGamma.wTc.SetValue(str(dataI.gamma))
        theta = str(dataI.theta) if dataI.theta is not None else ''
        self.wTheta.wTc.SetValue(theta)
        thetaM = str(dataI.thetaM) if dataI.thetaM is not None else ''
        self.wThetaMax.wTc.SetValue(thetaM)
        #------------------------------> Columns
        self.wSeqCol.wTc.SetValue(str(dataI.ocSeq))
        self.wDetectedProt.wTc.SetValue(str(dataI.ocTargetProt))
        self.wScore.wTc.SetValue(str(dataI.ocScore))
        self.wTcResults.SetValue(dataI.resCtrl)
        self.rLbDict[0] = dataI.labelA
        self.rLbDict[1] = dataI.labelB
        self.rLbDict['Control'] = [dataI.ctrlName]
        #------------------------------>
        self.OnIFileLoad('fEvent')
        self.OnImpMethod('fEvent')
        #endregion ----------------------------------------------> Fill Fields

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
        if not super().CheckInput():
            return False
        #endregion ----------------------------------------------------> Super

        #region ------------------------------------------------> Mixed Fields
        #region -------------------------------------------------------> Theta
        msgStep = self.cLPdCheck + f'{self.cLThetaMax}'
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        #------------------------------>
        if self.wTheta.wTc.GetValue() == '':
            a, b = self.wThetaMax.wTc.GetValidator().Validate()
            if not a:
                self.rMsgError = cMethod.StrSetMessage(
                    mConfig.core.mOneZPlusNum.format(b[1], self.cLThetaMax), b[2])
                return False
        #endregion ----------------------------------------------------> Theta

        #region ----------------------------------------------> Paired Samples
        msgStep = self.cLPdCheck + f'{self.cLSample}'
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        #------------------------------>
        if self.wSample.wCb.GetValue() == 'Paired Samples':
            resCtrl = cMethod.ResControl2ListNumber(self.wTcResults.GetValue())
            n = [len(x) for y in resCtrl for x in y if len(x) != 0]
            if len(set(n)) != 1:
                self.rMsgError = (
                    'The Pair Samples analysis requires all gel '
                    'spots and control to have the same number of replicates.')
                return False
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
        #--------------> Theta
        thetaVal    = self.wTheta.wTc.GetValue()
        theta       = float(thetaVal) if thetaVal != '' else None
        thetaMaxVal = self.wThetaMax.wTc.GetValue()
        thetaMax    = float(thetaMaxVal) if thetaMaxVal != '' else None
        #--------------> Columns
        seqCol        = int(self.wSeqCol.wTc.GetValue())
        detectedProt  = int(self.wDetectedProt.wTc.GetValue())
        scoreCol      = int(self.wScore.wTc.GetValue())
        resCtrl       = cMethod.ResControl2ListNumber(self.wTcResults.GetValue())
        resCtrlFlat   = cMethod.ResControl2Flat(resCtrl)
        resCtrlDF     = cMethod.ResControl2DF(resCtrl, 3)
        resCtrlDFFlat = cMethod.ResControl2Flat(resCtrlDF)
        #--------------> dI
        dI = {
            'iFileN'       : self.cLiFile,
            'seqFileN'     : self.cLSeqFile,
            'ID'           : self.cLId,
            'cero'         : self.cLCeroTreatD,
            'tran'         : self.cLTransMethod,
            'norm'         : self.cLNormMethod,
            'imp'          : self.cLImputation,
            'shift'        : self.cLShift,
            'width'        : self.cLWidth,
            'targetProt'   : self.cLTargetProt,
            'scoreVal'     : self.cLScoreVal,
            'alpha'        : self.cLAlpha,
            'indSample'    : self.cLSample,
            'beta'         : self.cLBeta,
            'gamma'        : self.cLGamma,
            'theta'        : self.cLTheta,
            'thetaM'       : self.cLThetaMax,
            'ocSeq'        : f'{self.cLSeqCol} Column',
            'ocTargetProt' : self.cLDetectedProt,
            'ocScore'      : self.cLScoreCol,
            'resCtrl'      : mConfig.core.lStResCtrlS,
            'labelA'       : self.cLLane,
            'labelB'       : self.cLBand,
            'ctrlName'     : f'Control {self.cLCtrlName}',
        }
        if impMethod != mConfig.data.lONormDist:
            dI.pop('shift')
            dI.pop('width')
        #endregion --------------------------------------------------------> d

        #region ----------------------------------------------------------> do
        msgStep = self.cLPdPrepare + 'User input, processing'
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        #------------------------------>
        self.rDO = limpMethod.UserData(
            uFile         = Path(self.wUFile.wTc.GetValue()),
            iFile         = Path(self.wIFile.wTc.GetValue()),
            seqFile       = Path(self.wSeqFile.wTc.GetValue()),
            ID            = self.wId.wTc.GetValue(),
            cero          = mConfig.core.oYesNo[self.wCeroB.wCb.GetValue()],
            tran          = self.wTransMethod.wCb.GetValue(),
            norm          = self.wNormMethod.wCb.GetValue(),
            imp           = impMethod,
            shift         = float(self.wShift.wTc.GetValue()),
            width         = float(self.wWidth.wTc.GetValue()),
            targetProt    = self.wTargetProt.wTc.GetValue(),
            scoreVal      = float(self.wScore.wTc.GetValue()),
            indSample     = self.cOSample[self.wSample.wCb.GetValue()],
            alpha         = float(self.wAlpha.wTc.GetValue()),
            beta          = float(self.wBeta.wTc.GetValue()),
            gamma         = float(self.wGamma.wTc.GetValue()),
            theta         = theta,
            thetaM        = thetaMax,
            labelA        = self.rLbDict[0],
            labelB        = self.rLbDict[1],
            ctrlName      = self.rLbDict['Control'][0],
            ocSeq         = seqCol,
            ocTargetProt  = detectedProt,
            ocScore       = scoreCol,
            resCtrl       = self.wTcResults.GetValue(),
            ocResCtrl     = resCtrl,
            ocColumn      = [seqCol, detectedProt, scoreCol] + resCtrlFlat,
            dfSeq         = 0,
            dfTargetProt  = 1,
            dfScore       = 2,
            dfResCtrl     = resCtrlDF,
            dfResCtrlFlat = resCtrlDFFlat,
            dfColumnR     = resCtrlDFFlat,
            dfColumnF     = [2] + resCtrlDFFlat,
            dI            = dI,
        )
        #endregion -------------------------------------------------------> do

        #region ---------------------------------------------------> Super
        if not super().PrepareRun():
            self.rMsgError = 'Something went wrong when preparing the analysis.'
            return False
        #endregion ------------------------------------------------> Super

        return True
    #---

    def RunAnalysis(self) -> bool:
        """Run the analysis.

            Returns
            -------
            bool
        """
        #region -----------------------------------------------------> Seq Obj
        setattr(self.rDO, 'seqFileObj', self.rSeqFileObj)
        #endregion --------------------------------------------------> Seq Obj

        #region ---------------------------------------------------> Run Super
        return super().RunAnalysis()
        #endregion ------------------------------------------------> Run Super
    #---

    def WriteOutput(self):
        """Write output. Override as needed"""
        #region --------------------------------------------------> Data Steps
        stepDict = self.SetStepDictDP()
        stepDict['Files'] = {
            mConfig.core.fnInitial.format(self.rDate, '01')   : self.dfI,
            mConfig.core.fnFloat.format(self.rDate, '02')     : self.dfF,
            mConfig.core.fnTrans.format(self.rDate, '03')     : self.dfT,
            mConfig.core.fnNorm.format(self.rDate, '04')      : self.dfN,
            mConfig.core.fnImp.format(self.rDate, '05')       : self.dfIm,
            mConfig.core.fnTargetProt.format(self.rDate, '06'): self.dfTP,
            mConfig.core.fnScore.format(self.rDate, '07')     : self.dfS,
            self.rMainData.format(self.rDate, '08')           : self.dfR,
        }
        stepDict['R'] = self.rMainData.format(self.rDate, '08')
        #endregion -----------------------------------------------> Data Steps

        return self.WriteOutputData(stepDict)
    #---

    def RunEnd(self) -> bool:
        """Finish analysis"""
        #------------------------------>
        if self.rDFile:
            self.wSeqFile.wTc.SetValue(str(self.rDFile[1]))
        #------------------------------>
        return super().RunEnd()
    #---
    #endregion ------------------------------------------------> Run Method
#---


class ResControlExpConf(cPane.BaseResControlExpConf):
    """Creates the configuration panel for the Results - Control Experiments
        dialog when called from the LimProt Tab.

        Parameters
        ----------
        parent: wx.Widget
            Parent of the panel
        topParent: wx.Widget
            Top parent window
        NColF: int
            Total number of columns present in the Data File
    """
    #region -----------------------------------------------------> Class setup
    cName = mConfig.limp.npResControlExp
    #------------------------------> Needed by ResControlExpConfBase
    cStLabel   = [f"{mConfig.limp.lStLane}", f"{mConfig.limp.lStBand}"]
    cLabelText = ['L','B']
    #------------------------------> Tooltips
    cTTTotalField = [
        f'Set the number of {mConfig.limp.lStLane}.',
        f'Set the number of {mConfig.limp.lStBand}.',
    ]
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
    def OnCreate(self, event:wx.CommandEvent) -> bool:
        """Create the fields in the white panel.

            Parameters
            ----------
            event: wx.Event
                Information about the event.

            Return
            ------
            bool
        """
        #region -------------------------------------------------> Check input
        if not (n := self.CheckLabel(False)):
            return False
        #endregion ----------------------------------------------> Check input

        #region ---------------------------------------------------> Variables
        Nl   = n[0]
        NCol = n[0]+1
        Nb   = n[1]
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
        dK = list(self.rFSectTcDict)
        #------------------------------>
        for k in dK:
            if k > Nb:
                #------------------------------>
                for j in self.rFSectTcDict[k]:
                    j.Destroy()
                #------------------------------>
                del self.rFSectTcDict[k]
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
        #------------------------------> Update sizer
        self.sSWMatrix.Layout()
        #endregion ---------------------------------------------> Setup Sizers

        #region --------------------------------------------------> Set scroll
        self.wSwMatrix.SetupScrolling()
        #endregion -----------------------------------------------> Set scroll

        return True
    #---

    def OnOK(self, export:bool=True) -> bool:
        """Check wx.Dialog content and send values to topParent.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Super
        if super().OnOK()[0]:
            return True
        #------------------------------>
        return False
        #endregion ------------------------------------------------> Super
    #---
    #endregion ------------------------------------------------> Event Methods
#---
#endregion ----------------------------------------------------------> Classes