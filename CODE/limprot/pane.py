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
from pathlib import Path

import wx

from config.config import config as mConfig
from core    import pane      as cPane
from core    import widget    as cWidget
from core    import validator as cValidator
from core    import method    as cMethod
from limprot import method    as limpMethod
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Classes
class LimProt(cPane.BaseConfPanelMod2):
    """Configuration Pane for the Limited Proteolysis module.

        Parameters
        ----------
        parent: wx.Window
            Parent of the pane.
        dataI: dict
            Initial data provided by the user in a previous analysis.
            This contains both I and CI dicts e.g. {'I': I, 'CI': CI}.

        Attributes
        ----------
        rDI: dict
            Dictionary with the user input. Keys are labels in the panel plus:
            {
                config.lStLimProtLane           : [list of lanes],
                config.lStLimProtBand           : [list of bands],
                f"Control {config.lStCtrlName}" : "Control Name",
            }
        rDO: dict
            Dictionary with checked user input. Keys are:
            {
                "iFile"      : "Path to input data file",
                "uFile"      : "Path to umsap file.",
                'seqFile'    : "Path to the sequence file",
                'ID'         : "Analysis ID",
                "Cero"       : "Boolean, how to treat cero values",
                "TransMethod": "Transformation method",
                "NormMethod" : "Normalization method",
                "ImpMethod"  : "Imputation method",
                "Shift"      : float,
                "Width"      : float,
                "TargetProt" : "Target Protein",
                "ScoreVal"   : "Score value threshold",
                'Sample'     : 'Independent or dependent samples',
                "Alpha"      : "Significance level",
                "Beta"       : "Beta level',
                'Gamma'      : "Gamma level",
                'Theta'      : Theta value or None,
                'Theta Max'  : Theta maximum,
                "Lane"       : [List of lanes],
                "Band"       : [List of bands],
                "ControlL"   : "Control label",
                "oc": {
                    "SeqCol"       : Column of Sequences,
                    "TargetProtCol": Column of Proteins,
                    "ScoreCol"     : Score column,
                    "ResCtrl"      : [List of columns containing the control and
                        experiments column numbers],
                    "ColumnF" : [Flat list of all columns containing floats],
                    "Column": [Flat list of all column numbers with the
                              following order: SeqCol, TargetProtCol,
                              ScoreColRes & Control]
                },
                "df": { Column numbers in the pd.df created from the input file.
                    "SeqCol"       : 0,
                    "TargetProtCol": 1,
                    "ScoreCol"     : 2,
                    "ResCtrl"      : [[[]], [[]],...,[[]]],
                    "ResCtrlFlat"  : [ResCtrl as a flat list],
                    "ColumnR"      : [Columns with the results],
                    "ColumnF"      : [Columns that must contain only floats],
                },
                "dfo" : {
                    "NC" : [Columns for the N and C residue numbers in the
                        output df],
                    "NCF" : [Columns for the nNat and cNat residue numbers in
                        the output df],
                },
                "ProtLength": "Length of the Recombinant protein",
                "ProtLoc"   : "Location of the Nat Seq in the Rec Seq",
                "ProtDelta" : "To adjust Res Number. Nat = Res + Delta",
            },
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
                    'I' : self.d,
                    'CI': self.do,
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
    cHBeta = 'e.g. 0.05'
    cHGamma = 'e.g. 0.8'
    cHTheta = 'e.g. 4.5'
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
    cURL         = f"{mConfig.core.urlTutorial}/limited-proteolysis"
    cSection     = mConfig.limp.nMod
    cTitlePD     = f"Running {mConfig.limp.nMod} Analysis"
    cGaugePD     = 35
    rMainData    = '{}_{}-LimitedProteolysis-Data.txt'
    rDExtra: dict = {
        'cLDFFirstThree' : cLDFFirstThree,
        'cLDFThirdLevel' : cLDFThirdLevel,
    }
    rAnalysisMethod = limpMethod.LimProt
    #------------------------------> Optional configuration
    cTTHelp = mConfig.core.ttBtnHelp.format(cURL)
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent, dataI: dict={}) -> None:                         # pylint: disable=dangerous-default-value
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
        self.SetInitialData(dataI)
        #endregion ----------------------------------------------------> DataI

        #region --------------------------------------------------------> Test
        if mConfig.core.development:
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
                0        : ['Lane1', 'Lane2', 'Lane3', 'Lane4', 'Lane5'],
                1        : ['Band1', 'Band2', 'Band3', 'Band4'],
                'Control': ['Ctrl'],
            }
            self.OnImpMethod('fEvent')
            self.wShift.wTc.SetValue('1.8')
            self.wWidth.wTc.SetValue('0.3')
        else:
            pass
        #endregion -----------------------------------------------------> Test
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class Event
    def SetInitialData(self, dataI: dict={}) -> bool:                           # pylint: disable=dangerous-default-value
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
        if dataI:
            #------------------------------>
            dataInit = dataI['uFile'].parent / mConfig.core.fnDataInit
            iFile = dataInit / dataI['I'][self.cLiFile]
            seqFile = dataInit / dataI['I'][f'{self.cLSeqFile} File']
            #------------------------------> Files
            self.wUFile.wTc.SetValue(str(dataI['uFile']))
            self.wIFile.wTc.SetValue(str(iFile))
            self.wSeqFile.wTc.SetValue(str(seqFile))
            self.wId.wTc.SetValue(dataI['CI']['ID'])
            #------------------------------> Data Preparation
            self.wCeroB.wCb.SetValue(dataI['I'][self.cLCeroTreatD])
            self.wTransMethod.wCb.SetValue(dataI['I'][self.cLTransMethod])
            self.wNormMethod.wCb.SetValue(dataI['I'][self.cLNormMethod])
            self.wImputationMethod.wCb.SetValue(dataI['I'][self.cLImputation])
            self.wShift.wTc.SetValue(dataI['I'].get(self.cLShift, self.cValShift))
            self.wWidth.wTc.SetValue(dataI['I'].get(self.cLWidth, self.cValWidth))
            #------------------------------> Values
            self.wTargetProt.wTc.SetValue(dataI['I'][self.cLTargetProt])
            self.wScoreVal.wTc.SetValue(dataI['I'][self.cLScoreVal])
            self.wAlpha.wTc.SetValue(dataI['I'][self.cLAlpha])
            self.wSample.wCb.SetValue(dataI['I'][self.cLSample])
            self.wBeta.wTc.SetValue(dataI['I'][self.cLBeta])
            self.wGamma.wTc.SetValue(dataI['I'][self.cLGamma])
            self.wTheta.wTc.SetValue(dataI['I'][self.cLTheta])
            self.wThetaMax.wTc.SetValue(dataI['I'][self.cLThetaMax])
            #------------------------------> Columns
            self.wSeqCol.wTc.SetValue(dataI['I'][f'{self.cLSeqCol} Column'])
            self.wDetectedProt.wTc.SetValue(dataI['I'][self.cLDetectedProt])
            self.wScore.wTc.SetValue(dataI['I'][self.cLScoreCol])
            self.wTcResults.SetValue(dataI['I'][mConfig.core.lStResCtrlS])
            self.rLbDict[0] = dataI['I'][self.cLLane]
            self.rLbDict[1] = dataI['I'][self.cLBand]
            self.rLbDict['Control'] = dataI['I'][f"Control {self.cLCtrlName}"]
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
        #------------------------------> As given
        self.rDI = {
            self.EqualLenLabel(self.cLiFile) : (
                self.wIFile.wTc.GetValue()),
            self.EqualLenLabel(f'{self.cLSeqFile} File') : (
                self.wSeqFile.wTc.GetValue()),
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
            self.EqualLenLabel(self.cLTargetProt) : (
                self.wTargetProt.wTc.GetValue()),
            self.EqualLenLabel(self.cLScoreVal) : (
                self.wScoreVal.wTc.GetValue()),
            self.EqualLenLabel(self.cLSample) : (
                self.wSample.wCb.GetValue()),
            self.EqualLenLabel(self.cLAlpha) : (
                self.wAlpha.wTc.GetValue()),
            self.EqualLenLabel(self.cLBeta) : (
                self.wBeta.wTc.GetValue()),
            self.EqualLenLabel(self.cLGamma) : (
                self.wGamma.wTc.GetValue()),
            self.EqualLenLabel(self.cLTheta) : (
                self.wTheta.wTc.GetValue()),
            self.EqualLenLabel(self.cLThetaMax) : (
                self.wThetaMax.wTc.GetValue()),
            self.EqualLenLabel(f'{self.cLSeqCol} Column') : (
                self.wSeqCol.wTc.GetValue()),
            self.EqualLenLabel(self.cLDetectedProt) : (
                self.wDetectedProt.wTc.GetValue()),
            self.EqualLenLabel(self.cLScoreCol) : (
                self.wScore.wTc.GetValue()),
            self.EqualLenLabel(mConfig.core.lStResCtrlS): (
                self.wTcResults.GetValue()),
            self.EqualLenLabel(self.cLLane) : (
                self.rLbDict[0]),
            self.EqualLenLabel(self.cLBand) : (
                self.rLbDict[1]),
            self.EqualLenLabel(f"Control {self.cLCtrlName}") : (
                self.rLbDict['Control']),
        }
        #endregion --------------------------------------------------------> d

        #region ----------------------------------------------------------> do
        #------------------------------> Dict with all values
        #--------------> Step
        msgStep = self.cLPdPrepare + 'User input, processing'
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        #--------------> Theta
        thetaVal = self.wTheta.wTc.GetValue()
        theta = float(thetaVal) if thetaVal != '' else None
        thetaMaxVal = self.wThetaMax.wTc.GetValue()
        thetaMax = float(thetaMaxVal) if thetaMaxVal != '' else None
        #--------------> Columns
        seqCol       = int(self.wSeqCol.wTc.GetValue())
        detectedProt = int(self.wDetectedProt.wTc.GetValue())
        scoreCol     = int(self.wScore.wTc.GetValue())
        resCtrl       = cMethod.ResControl2ListNumber(self.wTcResults.GetValue())
        resCtrlFlat   = cMethod.ResControl2Flat(resCtrl)
        resCtrlDF     = cMethod.ResControl2DF(resCtrl, 3)
        resCtrlDFFlat = cMethod.ResControl2Flat(resCtrlDF)
        #-------------->
        self.rDO  = {
            'iFile'      : Path(self.wIFile.wTc.GetValue()),
            'uFile'      : Path(self.wUFile.wTc.GetValue()),
            'seqFile'    : Path(self.wSeqFile.wTc.GetValue()),
            'ID'         : self.wId.wTc.GetValue(),
            'Cero'       : mConfig.core.oYesNo[self.wCeroB.wCb.GetValue()],
            'TransMethod': self.wTransMethod.wCb.GetValue(),
            'NormMethod' : self.wNormMethod.wCb.GetValue(),
            'ImpMethod'  : impMethod,
            'Shift'      : float(self.wShift.wTc.GetValue()),
            'Width'      : float(self.wWidth.wTc.GetValue()),
            'TargetProt' : self.wTargetProt.wTc.GetValue(),
            'ScoreVal'   : float(self.wScoreVal.wTc.GetValue()),
            'Sample'     : self.cOSample[self.wSample.wCb.GetValue()],
            'Alpha'      : float(self.wAlpha.wTc.GetValue()),
            'Beta'       : float(self.wBeta.wTc.GetValue()),
            'Gamma'      : float(self.wGamma.wTc.GetValue()),
            'Theta'      : theta,
            'ThetaMax'   : thetaMax,
            'Lane'       : self.rLbDict[0],
            'Band'       : self.rLbDict[1],
            'ControlL'   : self.rLbDict['Control'],
            'oc'         : { # Column numbers in the initial dataframe
                'SeqCol'       : seqCol,
                'TargetProtCol': detectedProt,
                'ScoreCol'     : scoreCol,
                'ResCtrl'      : resCtrl,
                'ColumnF'      : [scoreCol] + resCtrlFlat,
                'Column'       : (
                    [seqCol, detectedProt, scoreCol] + resCtrlFlat),
            },
            'df' : { # Column numbers in the selected data dataframe
                'SeqCol'       : 0,
                'TargetProtCol': 1,
                'ScoreCol'     : 2,
                'ResCtrl'      : resCtrlDF,
                'ResCtrlFlat'  : resCtrlDFFlat,
                'ColumnR'      : resCtrlDFFlat,
                'ColumnF'      : [2] + resCtrlDFFlat,
            },
            'dfo' : { # Column numbers in the output dataframe
                'NC' : [2,3], # N and C Term Res Numbers in the Rec Seq
                'NCF': [4,5], # N and C Term Res Numbers in the Nat Seq
            }
        }
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
        #region -----------------------------------------------------> rDExtra
        self.rDExtra['rSeqFileObj'] = self.rSeqFileObj
        #endregion --------------------------------------------------> rDExtra

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
            self.rMainData.format(self.rDate, '08')     : self.dfR,
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
        parent : wx.Widget
            Parent of the panel
        topParent : wx.Widget
            Top parent window
        NColF : int
            Total number of columns present in the Data File
    """
    #region -----------------------------------------------------> Class setup
    cName = mConfig.limp.npResControlExp
    #------------------------------> Needed by ResControlExpConfBase
    cStLabel   = [f"{mConfig.limp.lStLane}:", f"{mConfig.limp.lStBand}:"]
    cLabelText = ['L','B']
    #------------------------------> Tooltips
    cTTTotalField = [
        f'Set the number of {cStLabel[0]}.',
        f'Set the number of {cStLabel[1]}.',
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
    def OnCreate(self, event: wx.CommandEvent) -> bool:
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

    def OnOK(self, export: bool=True) -> bool:
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
