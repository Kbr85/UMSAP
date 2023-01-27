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


"""Panes for the tarprot module of the app"""


#region -------------------------------------------------------------> Imports
from pathlib import Path
from typing  import Optional

import pandas as pd

import wx

from config.config import config as mConfig
from core    import method    as cMethod
from core    import pane      as cPane
from core    import validator as cValidator
from core    import widget    as cWidget
from tarprot import method    as tarpMethod
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Classes
class TarProt(cPane.BaseConfPanelMod2):
    """Configuration Pane for the Targeted Proteolysis module.

        Parameters
        ----------
        parent: wx.Window
            Parent of the pane.
        dataI: tarpMethod.UserData or None
            Initial data provided by the user in a previous analysis.
            Default is None.

        Attributes
        ----------
        rLbDict: dict
            Contains information about the Res - Ctrl e.g.
            {
                0        : ['Exp1', 'Exp1'],
                'Control': ['TheControl'],
            }
        See Parent classes for more attributes.

        Notes
        -----
        Running the analysis results in the creation of:

        - Parent Folder/
            - Input_Data_Files/
            - Steps_Data_Files/20220104-214055_Targeted Proteolysis/
            - output-file.umsap

        The Input_Data_Files folder contains the original data files. These are
        needed for data visualization, running analysis again with different
        parameters, etc.
        The Steps_Data_Files/Date-Section folder contains regular csv files with
        the step by step data.

        The Targeted Proteolysis section in output-file.umsap contains the
        information about the calculations, e.g

        {
            'Targeted Proteolysis : {
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
                    'R' : pd.DataFrame (dict) with the calculation results.
                }
            }
        }

        The result data frame has the following structure:

        Sequence Score Nterm Cterm NtermF CtermF Exp1, Exp1,..., ExpN, ExpN
        Sequence Score Nterm Cterm NtermF CtermF IntL,    P,..., IntL, P
    """
    #region -----------------------------------------------------> Class setup
    cName = mConfig.tarp.nPane
    #------------------------------> Label
    cLAAPos     = 'AA Positions'
    cLHist      = 'Histogram Windows'
    cLExp       = mConfig.tarp.lStExp
    cLCtrlName  = mConfig.core.lStCtrlName
    cLDFFirst   = mConfig.tarp.dfcolFirstPart
    cLDFSecond  = mConfig.tarp.dfcolBLevel
    cLPdRunText = 'Targeted Proteolysis Analysis'
    #------------------------------> Hint
    cHAAPos = 'e.g. 5'
    cHHist  = 'e.g. 50 or 50 100 200'
    #------------------------------> Tooltip
    cTTAAPos = (f'Number of positions around the cleavage sites to consider '
        f'for the AA distribution analysis.\ne.g. 5{mConfig.core.mOptField}')
    cTTHist = (f'Size of the histogram windows. One number will result in '
        f'equally spaced windows. Multiple numbers allow defining custom sized '
        f'windows.\ne.g. 50 or 0 50 100 150 500{mConfig.core.mOptField}')
    #------------------------------> Needed by BaseConfPanel
    cURL      = f"{mConfig.core.urlTutorial}/targeted-proteolysis"
    cSection  = mConfig.tarp.nMod
    cTitlePD  = f"Running {mConfig.tarp.nMod} Analysis"
    cGaugePD  = 34
    rMainData = '{}_{}-TargetedProteolysis-Data.txt'
    rAnalysisMethod = tarpMethod.TarProt
    #------------------------------> Optional configuration
    cTTHelp = mConfig.core.ttBtnHelp.format(cURL)
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self,
        parent,
        dataI:Optional[tarpMethod.UserData]=None,
        ) -> None:                          # pylint: disable=dangerous-default-value
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(parent)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        #------------------------------> Values
        self.wAAPos = cWidget.StaticTextCtrl(
            self.wSbValue,
            stLabel   = self.cLAAPos,
            stTooltip = self.cTTAAPos,
            tcSize    = self.cSTc,
            tcHint    = self.cHAAPos,
            validator = cValidator.NumberList(
                numType='int', nN=1, vMin=0, opt=True)
        )
        self.wHist = cWidget.StaticTextCtrl(
            self.wSbValue,
            stLabel   = self.cLHist,
            stTooltip = self.cTTHist,
            tcSize    = self.cSTc,
            tcHint    = self.cHHist,
            validator = cValidator.NumberList(
                numType='int', vMin=0, sep=' ', opt=True),
        )
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        #------------------------------> Values
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
            self.wAlpha.wSt,
            pos    = (2,1),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sSbValueWid.Add(
            self.wAlpha.wTc,
            pos    = (2,2),
            flag   = wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sSbValueWid.Add(
            self.wAAPos.wSt,
            pos    = (0,3),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sSbValueWid.Add(
            self.wAAPos.wTc,
            pos    = (0,4),
            flag   = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sSbValueWid.Add(
            self.wHist.wSt,
            pos    = (1,3),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sSbValueWid.Add(
            self.wHist.wTc,
            pos    = (1,4),
            flag   = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sSbValueWid.Add(
            1, 1,
            pos    = (0,5),
            flag   = wx.EXPAND|wx.ALL,
            border = 5,
            span   = (2, 0),
        )
        #------------------------------>
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
            self.cLAlpha       : [self.wAlpha.wTc,        mConfig.core.mOne01Num,       False],
            self.cLAAPos       : [self.wAAPos.wTc,        mConfig.core.mOneZPlusNum,    False],
            self.cLHist        : [self.wHist.wTc,         mConfig.core.mValueBad,       False],
            label              : [self.wSeqCol.wTc,       mConfig.core.mOneZPlusNumCol, True ],
            self.cLDetectedProt: [self.wDetectedProt.wTc, mConfig.core.mOneZPlusNumCol, True ],
            self.cLScoreCol    : [self.wScore.wTc,        mConfig.core.mOneZPlusNumCol, True ],
            self.cLResControl  : [self.wTcResults,        mConfig.core.mResCtrl,        False]
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
                self.wIFile.wTc.SetValue("/Users/" + str(user) + "/Dropbox/SOFTWARE-DEVELOPMENT/APPS/UMSAP/LOCAL/DATA/UMSAP-TEST-DATA/TARPROT/tarprot-data-file.txt")
                self.wSeqFile.wTc.SetValue("/Users/" + str(user) + "/Dropbox/SOFTWARE-DEVELOPMENT/APPS/UMSAP/LOCAL/DATA/UMSAP-TEST-DATA/TARPROT/tarprot-seq-both.txt")
                # self.wSeqFile.tc.SetValue("/Users/" + str(user) + "/Dropbox/SOFTWARE-DEVELOPMENT/APPS/UMSAP/LOCAL/DATA/UMSAP-TEST-DATA/TARPROT/tarprot-seq-rec.txt")
            elif mConfig.core.os == 'Windows':
                self.wUFile.wTc.SetValue("C:/Users/" + str(user) + "/Desktop/SharedFolders/BORRAR-UMSAP/umsap-dev.umsap")
                self.wIFile.wTc.SetValue("C:/Users/" + str(user) + "/Dropbox/SOFTWARE-DEVELOPMENT/APPS/UMSAP/LOCAL/DATA/UMSAP-TEST-DATA/TARPROT/tarprot-data-file.txt")
                self.wSeqFile.wTc.SetValue("C:/Users/" + str(user) + "/Dropbox/SOFTWARE-DEVELOPMENT/APPS/UMSAP/LOCAL/DATA/UMSAP-TEST-DATA/TARPROT/tarprot-seq-both.txt")
            else:
                pass
            self.wId.wTc.SetValue('Beta Test Dev')
            self.wCeroB.wCb.SetValue('Yes')
            self.wTransMethod.wCb.SetValue('Log2')
            self.wNormMethod.wCb.SetValue('Median')
            self.wImputationMethod.wCb.SetValue('Normal Distribution')
            self.wTargetProt.wTc.SetValue('efeB')
            self.wScoreVal.wTc.SetValue('200')
            self.wAAPos.wTc.SetValue('5')
            self.wHist.wTc.SetValue('25')
            self.wAlpha.wTc.SetValue('0.05')
            self.wSeqCol.wTc.SetValue('0')
            self.wDetectedProt.wTc.SetValue('38')
            self.wScore.wTc.SetValue('44')
            self.wTcResults.SetValue('98-105; 109-111; 112 113 114; 115-117 120')
            self.rLbDict = {
                0        : ['Exp1', 'Exp2', 'Exp3'],
                'Control': ['Ctrl'],
            }
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

    #region ---------------------------------------------------> Class Event
    def SetInitialData(self, dataI:tarpMethod.UserData) -> bool:                            # pylint: disable=dangerous-default-value
        """Set initial data.

            Parameters
            ----------
            dataI : dict
                Data to fill all fields and repeat an analysis.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        posAA   = str(dataI.posAA) if dataI.posAA is not None else ''
        if dataI.winHist is not None:
            winHist = " ".join(map(str, dataI.winHist))
        else:
            winHist = ''
        #endregion ------------------------------------------------>

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
        self.wAAPos.wTc.SetValue(posAA)
        self.wHist.wTc.SetValue(winHist)
        #------------------------------> Columns
        self.wSeqCol.wTc.SetValue(str(dataI.ocSeq))
        self.wDetectedProt.wTc.SetValue(str(dataI.ocTargetProt))
        self.wScore.wTc.SetValue(str(dataI.ocScore))
        self.wTcResults.SetValue(dataI.resCtrl)
        self.rLbDict[0] = dataI.labelA
        self.rLbDict['Control'] = list(dataI.ctrlName)
        #------------------------------>
        self.OnIFileLoad('fEvent')
        self.OnImpMethod('fEvent')
        #endregion ----------------------------------------------> Fill Fields

        return True
    #---
    #endregion ------------------------------------------------> Class Event

    #region ---------------------------------------------------> Run methods
    def PrepareRun(self) -> bool:
        """Set variable and prepare data for analysis.

            Returns
            -------
            bool
        """
        #region -----------------------------------------------------------> d
        msgStep = self.cLPdPrepare + 'User input, reading'
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        #------------------------------> Read values
        impMethod = self.wImputationMethod.wCb.GetValue()
        #--------------> SeqLength
        aaPosVal = self.wAAPos.wTc.GetValue()
        aaPos    = int(aaPosVal) if aaPosVal != '' else None
        histVal  = self.wHist.wTc.GetValue()
        hist     = [int(x) for x in histVal.split()] if histVal != '' else None
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
            'iFileN'      : self.cLiFile,
            'seqFileN'    : self.cLSeqFile,
            'ID'          : self.cLId,
            'cero'        : self.cLCeroTreatD,
            'tran'        : self.cLTransMethod,
            'norm'        : self.cLNormMethod,
            'imp'         : self.cLImputation,
            'targetProt'  : self.cLTargetProt,
            'scoreVal'    : self.cLScoreVal,
            'alpha'       : self.cLAlpha,
            'posAA'       : self.cLAAPos,
            'winHist'     : self.cLHist,
            'ocSeq'       : f'{self.cLSeqCol} Column',
            'ocTargetProt': self.cLDetectedProt,
            'ocScore'     : self.cLScoreCol,
            'ocResCtrl'   : mConfig.core.lStResCtrlS,
            'labelA'      : self.cLExp,
            'ctrlName'    : f'Control {self.cLCtrlName}',
        }
        if impMethod == mConfig.data.lONormDist:
            dI['shift'] = self.cLShift
            dI['width'] = self.cLWidth
        #endregion --------------------------------------------------------> d

        #region ----------------------------------------------------------> do
        msgStep = self.cLPdPrepare + 'User input, processing'
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        #------------------------------>
        self.rDO = tarpMethod.UserData(
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
            alpha         = float(self.wAlpha.wTc.GetValue()),
            posAA         = aaPos,
            winHist       = hist,
            labelA        = self.rLbDict[0],
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

        #region -------------------------------------------------------> Super
        if not super().PrepareRun():
            self.rMsgError = 'Something went wrong when preparing the analysis.'
            return False
        #endregion ----------------------------------------------------> Super

        return True
    #---

    def RunAnalysis(self) -> bool:
        """Perform the equivalence tests.

            Returns
            -------
            bool
        """
        #region -----------------------------------------------------> Seq Obj
        setattr(self.rDO, 'seqFileObj', self.rSeqFileObj)
        #endregion --------------------------------------------------> Seq Obj

        #region -----------------------------------------------------> TarProt
        if not super().RunAnalysis():
            return False
        #endregion --------------------------------------------------> TarProt

        # Further Analysis
        idx = pd.IndexSlice

        #region ----------------------------------------------------> Cleavage
        msgStep = (f'{self.cLPdRun} Cleavage per Residue')
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        #------------------------------>
        a = self.cLDFFirst[2:] + self.rDO.labelA
        b = self.cLDFFirst[2:] + ['P']
        tIdxH = idx[a,b] # Also used for Hist
        #------------------------------>
        try:
            self.dfCpR = tarpMethod.R2CpR(
                self.dfR.loc[:, tIdxH],                                         # type: ignore
                self.rDO.alpha,
                self.rDO.protLength,
            )
        except Exception as e:
            self.rMsgError = 'The Cleavage per Residue method failed.'
            self.rException = e
            return False
        #endregion -------------------------------------------------> Cleavage

        #region ---------------------------------------------------> CutEvo
        msgStep = (f'{self.cLPdRun} Cleavage Evolution')
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        #------------------------------>
        a    = self.cLDFFirst[2:] + self.rDO.labelA
        b    = self.cLDFFirst[2:] + ['Int', 'P']
        tIdx = idx[a,b]
        #------------------------------>
        try:
            self.dfCEvol = tarpMethod.R2CEvol(
                self.dfR.loc[:, tIdx],                                          # type: ignore
                self.rDO.alpha,
                self.rDO.protLength,
            )
        except Exception as e:
            self.rMsgError = 'The Cleavage Evolution method failed.'
            self.rException = e
            return False
        #endregion ------------------------------------------------> CutEvo

        #region ----------------------------------------------------------> AA
        if self.rDO.posAA is not None:
            #------------------------------>
            msgStep = (f'{self.cLPdRun} AA Distribution')
            wx.CallAfter(self.rDlg.UpdateStG, msgStep)
            #------------------------------>
            tIdx = idx[['Sequence']+self.rDO.labelA,['Sequence', 'P']]
            try:
                self.dfAA = tarpMethod.R2AA(
                    self.dfR.loc[:,tIdx],                                       # type: ignore
                    self.rSeqFileObj.rSeqRec,
                    self.rDO.alpha,
                    self.rDO.protLength[0],
                    pos = self.rDO.posAA,
                )
            except Exception as e:
                self.rMsgError = 'Amino acid distribution calculation failed.'
                self.rException = e
                return False
        #endregion -------------------------------------------------------> AA

        #region --------------------------------------------------------> Hist
        if self.rDO.winHist is not None:
            #------------------------------>
            msgStep = (f'{self.cLPdRun} Histograms')
            wx.CallAfter(self.rDlg.UpdateStG, msgStep)
            #------------------------------>
            try:
                self.dfHist = tarpMethod.R2Hist(
                    self.dfR.loc[:,tIdxH],                                      # type: ignore
                    self.rDO.alpha,
                    self.rDO.winHist,
                    self.rDO.protLength
                )
            except Exception as e:
                self.rMsgError = 'The Histogram generation method failed.'
                self.rException = e
                return False
        #endregion -----------------------------------------------------> Hist

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
            mConfig.core.fnInitial.format(self.rDate, '01')   : self.dfI,
            mConfig.core.fnFloat.format(self.rDate, '02')     : self.dfF,
            mConfig.core.fnTrans.format(self.rDate, '03')     : self.dfT,
            mConfig.core.fnNorm.format(self.rDate, '04')      : self.dfN,
            mConfig.core.fnImp.format(self.rDate, '05')       : self.dfIm,
            mConfig.core.fnTargetProt.format(self.rDate, '06'): self.dfTP,
            mConfig.core.fnScore.format(self.rDate, '07')     : self.dfS,
            self.rMainData.format(self.rDate, '08')     : self.dfR,
        }
        stepDict['R'] = self.rMainData.format(self.rDate, '08')
        #endregion -----------------------------------------------> Data Steps

        #region --------------------------------------------> Further Analysis
        #------------------------------>
        stepDict['CpR']   = f'{self.rDate}_CpR.txt'
        stepDict['CEvol'] = f'{self.rDate}_CEvol.txt'
        #------------------------------>
        if self.rDO.posAA is not None:
            stepDict['AA'] = {
                f'{self.rDate}-{self.rDO.posAA}' : f'{self.rDate}_AA-{self.rDO.posAA}.txt',
            }
        #------------------------------>
        if self.rDO.winHist is not None:
            stepDict['Hist'] = {
                f'{self.rDate}-{self.rDO.winHist}' : f'{self.rDate}_Hist-{self.rDO.winHist}.txt',
            }
        #endregion -----------------------------------------> Further Analysis

        return self.WriteOutputData(stepDict)
    #---

    def RunEnd(self) -> bool:
        """Clean and get """
        #------------------------------>
        if self.rDFile:
            self.wSeqFile.wTc.SetValue(str(self.rDFile[1]))
        #------------------------------>
        self.dfAA    = pd.DataFrame()
        self.dfHist  = pd.DataFrame()
        self.dfCpR   = pd.DataFrame()
        self.dfCEvol = pd.DataFrame()
        #------------------------------>
        return super().RunEnd()
    #---
    #endregion ------------------------------------------------> Run methods
#---


class ResControlExpConf(cPane.BaseResControlExpConf):
    """Creates the configuration panel for the Results - Control Experiments
        dialog when called from the TarProt Tab.

        Parameters
        ----------
        parent: wx.Window
            Parent of the panel
        topParent: wx.Window
            Top parent window
        NColF: int
            Total number of columns present in the Data File
    """
    #region -----------------------------------------------------> Class setup
    cName = mConfig.tarp.npResControlExp
    #------------------------------> Needed by ResControlExpConfBase
    cStLabel   = [f"{mConfig.tarp.lStExp}"]
    cLabelText = ['Exp']
    #------------------------------> Tooltips
    cTTTotalField = [f'Set the number of {mConfig.tarp.lStExp}.']
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
            self.wControlN.wSt, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5,
        )
        self.sSWLabelControl.Add(self.wControlN.wTc, 0, wx.EXPAND|wx.ALL, 5)
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

    #region ---------------------------------------------------> Class methods
    def OnCreate(self, event:wx.CommandEvent) -> bool:
        """Create the fields in the white panel.

            Parameters
            ----------
            event : wx.Event
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
        NCol = 2
        NRow = n[0]+1
        NExp = n[0]
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
        #------------------------------> Add new fields
        for k in range(0, NExp+1):
            #------------------------------>
            row = self.rFSectTcDict.get(k, [])
            lRow = len(row)
            #------------------------------> Control & Exp
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
        #------------------------------> Destroy not needed old field
        for k in range(NExp+1, len(self.rFSectTcDict.keys())+1):
            row = self.rFSectTcDict.get(k, [])
            if len(row):
                row[0].Destroy()
                # row.pop
                self.rFSectTcDict.pop(k)
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
        #--------------> Experiments
        for r, l in enumerate(self.rFSectStDict[0], 1):
            #-------------->
            self.sSWMatrix.Add(
                l, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
            self.sSWMatrix.Add(self.rFSectTcDict[r][0], 0, wx.EXPAND|wx.ALL, 5)
        #------------------------------> Grow Columns
        for k in range(1, NCol):
            if not self.sSWMatrix.IsColGrowable(k):
                self.sSWMatrix.AddGrowableCol(k, 1)
            else:
                pass
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
    #endregion ------------------------------------------------> Class methods
#---
#endregion ----------------------------------------------------------> Classes
