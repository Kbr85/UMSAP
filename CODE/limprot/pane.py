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

        Attributes
        ----------
        rLbDict: dict
            Contains information about the Res - Ctrl e.g.
            {
                0            : ['L1', 'L2'],
                1            : ['B1', 'B2'],
                'Control'    : ['TheControl'],
                'ControlType': '',
                'MinRep'     : String like ResCtrl,
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
                        'dfF' : Name of file with initial data as float
                        'dfMP': Name of file with minimum valid replicate filter
                        'dfT' : Name of file with transformed data.
                        'dfN' : Name of file with normalized data.
                        'dfIm': Name of file with imputed data.
                    }
                    'R' : Path to file with the analysis results.
                }
            }
        }

        The result data frame has the following structure:

        Sequence Score Nterm Cterm NtermF CtermF Delta Band1, Band1, ... BandN, BandN
        Sequence Score Nterm Cterm NtermF CtermF Delta Lane1, Lane1, ... LaneN, LaneN
        Sequence Score Nterm Cterm NtermF CtermF Delta Ptost,    Pc, ... Ptost,    Pc
    """
    #region -----------------------------------------------------> Class setup
    cName = mConfig.limp.nPane
    #------------------------------> Label
    cLBeta         = mConfig.core.lStBeta
    cLGamma        = mConfig.core.lStGamma
    cLTheta        = mConfig.core.lStTheta
    cLThetaMax     = mConfig.core.lStThetaMax
    cLLane         = mConfig.limp.lStLane
    cLBand         = mConfig.limp.lStBand
    cLCtrlName     = mConfig.core.lStCtrlName
    cLDFFirstThree = mConfig.limp.dfcolFirstPart
    cLDFThirdLevel = mConfig.limp.dfcolCLevel
    cLPdRunText    = 'Performing Limited Proteolysis analysis'
    #------------------------------> Hints
    cHBeta     = mConfig.limp.hBeta
    cHGamma    = mConfig.limp.hGamma
    cHTheta    = mConfig.limp.hTheta
    cHThetaMax = mConfig.limp.hThetaMax
    #------------------------------> Tooltips
    cTTBeta     = mConfig.limp.ttBeta
    cTTGamma    = mConfig.limp.ttGamma
    cTTTheta    = mConfig.limp.ttTheta
    cTTThetaMax = mConfig.limp.ttThetaMax
    #------------------------------> Needed by BaseConfPanel
    cURL            = f"{mConfig.core.urlTutorial}/limited-proteolysis"
    cSection        = mConfig.limp.tMod
    cTitlePD        = f"Running {mConfig.limp.tMod} Analysis"
    cGaugePD        = 34
    rMainData       = '{}_{}-LimitedProteolysis-Data.txt'
    rAnalysisMethod = limpMethod.LimProt
    #------------------------------> Optional configuration
    cTTHelp = mConfig.core.ttBtnHelp.format(cURL)
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent) -> None:
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
            self.wCorrectP.wSt,
            pos    = (3,1),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sSbValueWid.Add(
            self.wCorrectP.wCb,
            pos    = (3,2),
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
            self.wBeta.wSt,
            pos    = (1,3),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sSbValueWid.Add(
            self.wBeta.wTc,
            pos    = (1,4),
            flag   = wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sSbValueWid.Add(
            self.wGamma.wSt,
            pos    = (2,3),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sSbValueWid.Add(
            self.wGamma.wTc,
            pos    = (2,4),
            flag   = wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sSbValueWid.Add(
            self.wTheta.wSt,
            pos    = (3,3),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sSbValueWid.Add(
            self.wTheta.wTc,
            pos    = (3,4),
            flag   = wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sSbValueWid.Add(
            self.wThetaMax.wSt,
            pos    = (4,3),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sSbValueWid.Add(
            self.wThetaMax.wTc,
            pos    = (4,4),
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
            self.cLTargetProt   : [self.wTargetProt.wTc,   mConfig.core.mValueBad,       False],
            self.cLScoreVal     : [self.wScoreVal.wTc,     mConfig.core.mOneRealNum,     False],
            self.cLSample       : [self.wSample.wCb,       mConfig.core.mOptionBad,      False],
            self.cLCorrectP     : [self.wCorrectP.wCb,     mConfig.core.mOptionBad,      False],
            self.cLAlpha        : [self.wAlpha.wTc,        mConfig.core.mOne01Num,       False],
            self.cLBeta         : [self.wBeta.wTc,         mConfig.core.mOne01Num,       False],
            self.cLGamma        : [self.wGamma.wTc,        mConfig.core.mOne01Num,       False],
            self.cLTheta        : [self.wTheta.wTc,        mConfig.core.mOneRPlusNum,    False],
            label               : [self.wSeqCol.wTc,       mConfig.core.mOneRPlusNum,    True ],
            self.cLDetectedProt : [self.wDetectedProt.wTc, mConfig.core.mOneZPlusNumCol, True ],
            self.cLScoreCol     : [self.wScore.wTc,        mConfig.core.mOneZPlusNumCol, True ],
            self.cLResControl   : [self.wTcResults,        mConfig.core.mResCtrl,        False],
        }
        self.rCheckUserInput = self.rCheckUserInput | rCheckUserInput
        #endregion -------------------------------------------> checkUserInput
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class Event
    def SetInitialData(self, dataI:Optional[limpMethod.UserData]) -> bool:
        """Set initial data.

            Parameters
            ----------
            dataI : limpMethod.UserData or None
                Data to fill all fields and repeat an analysis.

            Returns
            -------
            bool
        """
        #region -------------------------------------------------> Fill Fields
        if dataI is not None:
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
            self.wCorrectP.wCb.SetValue(dataI.correctedP)
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
            self.IFileEnter(dataI.iFile)
            self.OnImpMethod('fEvent')
        else:
            super().SetConfOptions()
            #------------------------------>
            self.wScoreVal.wTc.SetValue(mConfig.limp.scoreVal)
            self.wAlpha.wTc.SetValue(mConfig.limp.alpha)
            self.wBeta.wTc.SetValue(mConfig.limp.beta)
            self.wGamma.wTc.SetValue(mConfig.limp.gamma)
            self.wTheta.wTc.SetValue(mConfig.limp.theta)
            self.wThetaMax.wTc.SetValue(mConfig.limp.thetaMax)
            self.wCorrectP.wCb.SetValue(mConfig.limp.correctP)
        #endregion ----------------------------------------------> Fill Fields

        #region --------------------------------------------------------> Test
        if mConfig.core.development and dataI is None:
            # pylint: disable=line-too-long
            import getpass                                                      # pylint: disable=import-outside-toplevel
            user = getpass.getuser()
            if mConfig.core.os == "Darwin":
                self.wUFile.wTc.SetValue("/Users/" + str(user) + "/TEMP-GUI/BORRAR-UMSAP/umsap-dev.umsap")
                self.wIFile.wTc.SetValue("/Users/" + str(user) + "/Dropbox/SOFTWARE-DEVELOPMENT/APPS/UMSAP/LOCAL/DATA/UMSAP-TEST-DATA/LIMPROT/limprot-data-file.txt")
                self.wSeqFile.wTc.SetValue("/Users/" + str(user) + "/Dropbox/SOFTWARE-DEVELOPMENT/APPS/UMSAP/LOCAL/DATA/UMSAP-TEST-DATA/LIMPROT/limprot-seq-both.txt")
            elif mConfig.core.os == 'Windows':
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
            self.wCorrectP.wCb.SetValue('Bonferroni')
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
                0            : ['Lane1', 'Lane2', 'Lane3', 'Lane4', 'Lane5'],
                1            : ['Band1', 'Band2', 'Band3', 'Band4'],
                'Control'    : ['Ctrl'],
                'ControlType': '',
                'MinRep'     : '; , , , , ; , , , , ; , , , , ; , , , , 2'
            }
            self.OnImpMethod('fEvent')
            self.wShift.wTc.SetValue('1.8')
            self.wWidth.wTc.SetValue('0.3')
        #endregion -----------------------------------------------------> Test

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
        minRepList    = cMethod.ResControl2ListNumber(self.rLbDict['MinRep'])
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
            'indSample'    : self.cLSample,
            'correctedP'   : self.cLCorrectP,
            'alpha'        : self.cLAlpha,
            'beta'         : self.cLBeta,
            'gamma'        : self.cLGamma,
            'theta'        : self.cLTheta,
            'thetaM'       : self.cLThetaMax,
            'ocSeq'        : f'{self.cLSeqCol} Column',
            'ocTargetProt' : self.cLDetectedProt,
            'ocScore'      : self.cLScoreCol,
            'resCtrl'      : mConfig.core.lStResCtrlS,
            'minRep'       : mConfig.core.lStValRep,
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
            scoreVal      = float(self.wScoreVal.wTc.GetValue()),
            indSample     = self.cOSample[self.wSample.wCb.GetValue()],
            correctedP    = self.wCorrectP.wCb.GetValue(),
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
            minRep        = self.rLbDict['MinRep'],
            minRepList    = minRepList,
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
            mConfig.core.fnInitial.format(self.rDate,    '01') : self.dfI,
            mConfig.core.fnFloat.format(self.rDate,      '02') : self.dfF,
            mConfig.core.fnMinRep.format(self.rDate,     '03') : self.dfMR,
            mConfig.core.fnTrans.format(self.rDate,      '04') : self.dfT,
            mConfig.core.fnNorm.format(self.rDate,       '05') : self.dfN,
            mConfig.core.fnImp.format(self.rDate,        '06') : self.dfIm,
            mConfig.core.fnTargetProt.format(self.rDate, '07') : self.dfTP,
            mConfig.core.fnScore.format(self.rDate,      '08') : self.dfS,
            self.rMainData.format(self.rDate,            '09') : self.dfR,
        }
        stepDict['R'] = self.rMainData.format(self.rDate, '09')
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
        self.sSWLabelControl.Add(self.wControlN.wTc, 0, wx.EXPAND|wx.ALL, 5)
        self.sSWLabelControl.AddGrowableCol(1,1)
        #------------------------------>
        self.sSWLabelMain.Add(
            self.sSWLabelControl, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
        #endregion ---------------------------------------------------> Sizers

        #region -----------------------------------------------> Initial State
        self.AddWidgetValidReplicates()
        self.SetInitialState()
        #endregion --------------------------------------------> Initial State
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Event Methods
    def Create(self) -> bool:
        """Create the fields in the white panel.

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
                row.append(cWidget.TextCtrlMinRep(
                    self.wSwMatrix, self.cVColNumList, self.cColNumSep,
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
                    row.append(cWidget.TextCtrlMinRep(
                        self.wSwMatrix, self.cVColNumList, self.cColNumSep,
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
        w = self.rFSectTcDict[0][0]
        w.SetSizer()
        self.sSWMatrix.Add(w.sSizer, 0, wx.EXPAND|wx.ALL, 5)
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
                btc.SetSizer()                                                    # wx. Destroy child sizers
                self.sSWMatrix.Add(btc.sSizer, 0, wx.EXPAND|wx.ALL, 5)
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
    #endregion ------------------------------------------------> Event Methods
#---
#endregion ----------------------------------------------------------> Classes
