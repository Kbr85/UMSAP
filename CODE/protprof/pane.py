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


"""Panes for the protprof module of the app"""


#region -------------------------------------------------------------> Imports
from pathlib import Path
from typing  import Optional

import wx

from config.config import config as mConfig
from core     import method    as cMethod
from core     import pane      as cPane
from core     import validator as cValidator
from core     import widget    as cWidget
from core     import window    as cWindow
from protprof import method    as protMethod
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Classes
class ProtProf(cPane.BaseConfPanelMod):
    """Creates the Proteome Profiling configuration tab.

        Parameters
        ----------
        parent: wx.Widget
            Parent of the pane

        Attributes
        ----------
        dCheckRepNum: dict
            Methods to check the replicate numbers.
        dColCtrlData: dict
            Methods to get the Columns for Control Experiments.
        rDO: protMethod.UserData
            DataClass with user input.
        rLbDict: dict
            Contains information about the Res - Ctrl e.g.
            {
                0            : ['C1', 'C2'],
                1            : ['RP1', 'RP2'],
                'Control'    : ['TheControl'],
                'ControlType': 'One Control per Column',
            }
        See Parent classes for more attributes.

        Notes
        -----
        Running the analysis results in the creation of:

        - Parent Folder/
            - Input_Data_Files/
            - Steps_Data_Files/20210324-165609-Proteome-Profiling/
            - output-file.umsap

        The Input_Data_Files folder contains the original data files. These are
        needed for data visualization, running analysis again with different
        parameters, etc.
        The Steps_Data_Files/Date-Section folder contains regular csv files with
        the step by step data.

        The Proteome Profiling section in output-file.umsap contains the
        information about the calculations, e.g

        {
            'Proteome-Profiling : {
                '20210324-165609': {
                    'V' : config.dictVersion,
                    'I' : Dict with User Input as given. Keys are label like in the Tab GUI,
                    'CI': Dict with Processed User Input. Keys are attributes of UserData,
                    'DP': {
                        'dfI' : Name of the file with initial data as float.
                        'dfT' : Name of the file with transformed data.
                        'dfN' : Name of the file with normalized data.
                        'dfIm': Name of the file with imputed data.
                    }
                    'R' : Path to the file with the calculation results.
                    'F' : Dict for Filters.
                }
            }
        }

        The result data frame has the following structure:

        Gene Protein Score C1 .....  CN
        Gene Protein Score RP1 ..... RPN
        Gene Protein Score aveC stdC ave std P Pc FC CI FCz

        where all FC related values are for log2FC
    """
    #region -----------------------------------------------------> Class setup
    cName = mConfig.prot.nPane
    #------------------------------> Label
    cLGene         = mConfig.core.lStGeneName
    cLExcludeProt  = mConfig.core.lStExcludeProt
    cLDetectedProt = 'Detected Proteins'
    cLCond         = mConfig.prot.lStCond
    cLRP           = mConfig.prot.lStRP
    cLCtrlType     = mConfig.core.lStCtrlType
    cLCtrlName     = mConfig.core.lStCtrlName
    cLPdRunText    = 'Performing Proteome Profiling'
    #------------------------------> Tooltip
    cTTGene        = mConfig.core.ttStGenName
    cTTExcludeProt = f'{mConfig.core.ttStExcludeProt}{mConfig.core.mOptField}'
    #------------------------------> Control Type
    cDCtrlType = mConfig.prot.oControlType
    #------------------------------> Needed by BaseConfPanel
    cURL         = f'{mConfig.core.urlTutorial}/proteome-profiling'
    cSection     = mConfig.prot.nMod
    cTitlePD     = f"Running {mConfig.prot.nMod} Analysis"
    cGaugePD     = 29
    rMainData    = '{}_{}-ProteomeProfiling-Data.txt'
    rAnalysisMethod = protMethod.ProtProf
    #------------------------------> Optional configuration
    cTTHelp = mConfig.core.ttBtnHelp.format(cURL)
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        #------------------------------> Base attributes and setup
        super().__init__(parent)
        #------------------------------> Dict with methods
        self.dCheckRepNum = {
            self.cDCtrlType['OC']   : self.CheckRepNum_OC,
            self.cDCtrlType['OCC']  : self.CheckRepNum_OCC,
            self.cDCtrlType['OCR']  : self.CheckRepNum_OCR,
            self.cDCtrlType['Ratio']: self.CheckRepNum_Ratio,
        }
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        #------------------------------> Columns
        self.wGeneName = cWidget.StaticTextCtrl(
            self.wSbColumn,
            stLabel   = self.cLGene,
            stTooltip = self.cTTGene,
            tcSize    = self.cSTc,
            tcHint    = 'e.g. 6',
            validator = cValidator.NumberList(numType='int', nN=1, vMin=0),
        )
        self.wExcludeProt = cWidget.StaticTextCtrl(
            self.wSbColumn,
            stLabel   = self.cLExcludeProt,
            stTooltip = self.cTTExcludeProt,
            tcSize    = self.cSTc,
            tcHint    = 'e.g. 171-173',
            validator = cValidator.NumberList(
                numType='int', sep=' ', vMin=0, opt=True),
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
            self.wScoreVal.wSt,
            pos    = (0,1),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sSbValueWid.Add(
            self.wScoreVal.wTc,
            pos    = (0,2),
            flag   = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sSbValueWid.Add(
            self.wSample.wSt,
            pos    = (1,1),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sSbValueWid.Add(
            self.wSample.wCb,
            pos    = (1,2),
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
            self.wCorrectP.wSt,
            pos    = (1,3),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sSbValueWid.Add(
            self.wCorrectP.wCb,
            pos    = (1,4),
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
        self.sSbValueWid.AddGrowableCol(5, 1)
        #------------------------------> Sizer Columns
        self.sSbColumnWid.Add(
            self.wDetectedProt.wSt,
            pos    = (0,0),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sSbColumnWid.Add(
            self.wDetectedProt.wTc,
            pos    = (0,1),
            flag   = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sSbColumnWid.Add(
            self.wGeneName.wSt,
            pos    = (0,2),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sSbColumnWid.Add(
            self.wGeneName.wTc,
            pos    = (0,3),
            flag   = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sSbColumnWid.Add(
            self.wScore.wSt,
            pos    = (0,4),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sSbColumnWid.Add(
            self.wScore.wTc,
            pos    = (0,5),
            flag   = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL,
            border = 5,
        )
        self.sSbColumnWid.Add(
            self.wExcludeProt.wSt,
            pos    = (1,0),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT,
            border = 5,
        )
        self.sSbColumnWid.Add(
            self.wExcludeProt.wTc,
            pos    = (1,1),
            flag   = wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.ALL,
            border = 5,
            span   = (0, 5),
        )
        self.sSbColumnWid.Add(
            self.sRes,
            pos    = (2,0),
            flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND,
            border = 0,
            span   = (0,6),
        )
        self.sSbColumnWid.AddGrowableCol(1,1)
        self.sSbColumnWid.AddGrowableCol(3,1)
        self.sSbColumnWid.AddGrowableCol(5,1)
        #------------------------------> Main Sizer
        self.SetSizer(self.sSizer)
        self.sSizer.Fit(self)
        self.SetupScrolling()
        #endregion ---------------------------------------------------> Sizers

        #region ----------------------------------------------> checkUserInput
        rCheckUserInput = {
            self.cLScoreVal     : [self.wScoreVal.wTc,     mConfig.core.mOneRealNum,     False],
            self.cLSample       : [self.wSample.wCb,       mConfig.core.mOptionBad,      False],
            self.cLAlpha        : [self.wAlpha.wTc,        mConfig.core.mOne01Num,       False],
            self.cLCorrectP     : [self.wCorrectP.wCb,     mConfig.core.mOptionBad,      False],
            self.cLDetectedProt : [self.wDetectedProt.wTc, mConfig.core.mOneZPlusNumCol, True ],
            self.cLGene         : [self.wGeneName.wTc,     mConfig.core.mOneZPlusNumCol, True ],
            self.cLScoreCol     : [self.wScore.wTc,        mConfig.core.mOneZPlusNumCol, True ],
            self.cLExcludeProt  : [self.wExcludeProt.wTc,  mConfig.core.mNZPlusNumCol,   True ],
            self.cLResControl   : [self.wTcResults,        mConfig.core.mResCtrl,        False]
        }
        self.rCheckUserInput = self.rCheckUserInput | rCheckUserInput
        #------------------------------>
        self.rCheckUnique = [self.wDetectedProt.wTc, self.wGeneName.wTc,
            self.wScore.wTc, self.wExcludeProt.wTc, self.wTcResults]
        #endregion -------------------------------------------> checkUserInput

        #region --------------------------------------------------------> Test
        # if mConfig.core.development:
        #     # pylint: disable=line-too-long
        #     import getpass                                                      # pylint: disable=import-outside-toplevel
        #     user = getpass.getuser()
        #     if mConfig.core.os == "Darwin":
        #         self.wUFile.wTc.SetValue("/Users/" + str(user) + "/TEMP-GUI/BORRAR-UMSAP/umsap-dev.umsap")
        #         self.wIFile.wTc.SetValue("/Users/" + str(user) + "/Dropbox/SOFTWARE-DEVELOPMENT/APPS/UMSAP/LOCAL/DATA/UMSAP-TEST-DATA/PROTPROF/protprof-data-file.txt")
        #     elif mConfig.core.os == 'Windows':
        #         self.wUFile.wTc.SetValue(str(Path('C:/Users/bravo/Desktop/SharedFolders/BORRAR-UMSAP/umsap-dev.umsap')))
        #         self.wIFile.wTc.SetValue(str(Path('C:/Users/bravo/Dropbox/SOFTWARE-DEVELOPMENT/APPS/UMSAP/LOCAL/DATA/UMSAP-TEST-DATA/PROTPROF/protprof-data-file.txt')))
        #     else:
        #         pass
        #     self.wScoreVal.wTc.SetValue('320')
        #     self.wId.wTc.SetValue('Beta Test Dev')
        #     self.wCeroB.wCb.SetValue('Yes')
        #     self.wTransMethod.wCb.SetValue('Log2')
        #     self.wNormMethod.wCb.SetValue('Median')
        #     self.wImputationMethod.wCb.SetValue('Normal Distribution')
        #     self.wAlpha.wTc.SetValue('0.05')
        #     self.wSample.wCb.SetValue('Independent Samples')
        #     self.wCorrectP.wCb.SetValue('Benjamini - Hochberg')
        #     self.wDetectedProt.wTc.SetValue('0')
        #     self.wGeneName.wTc.SetValue('6')
        #     self.wScore.wTc.SetValue('39')
        #     self.wExcludeProt.wTc.SetValue('171 172 173')
        #     #------------------------------>
        #     #--> One Control per Column, 2 Cond and 2 TP
        #     # self.wTcResults.SetValue('105 115 125, 130 131 132; 106 116 126, 101 111 121; 108 118 128, 103 113 123')
        #     # self.rLbDict = {
        #     #     0            : ['C1', 'C2'],
        #     #     1            : ['RP1', 'RP2'],
        #     #     'Control'    : ['TheControl'],
        #     #     'ControlType': 'One Control per Column',
        #     # }
        #     #--> One Control per Row, 1 Cond and 2 TP
        #     # self.wTcResults.SetValue('105 115 125, 106 116 126, 101 111 121')
        #     # self.rLbDict = {
        #     #     0            : ['DMSO'],
        #     #     1            : ['30min', '60min'],
        #     #     'Control'    : ['MyControl'],
        #     #     'ControlType': 'One Control per Row',
        #     # }
        #     #--> One Control 2 Cond and 2 TP
        #     self.wTcResults.SetValue('105 115 125; 106 116 126, 101 111 121; 108 118 128, 103 113 123')
        #     self.rLbDict = {
        #         0            : ['C1', 'C2'],
        #         1            : ['RP1', 'RP2'],
        #         'Control'    : ['1Control'],
        #         'ControlType': 'One Control',
        #     }
        #     #--> Ratio 2 Cond and 2 TP
        #     # self.wTcResults.SetValue('106 116 126, 101 111 121; 108 118 128, 103 113 123')
        #     # self.rLbDict = {
        #     #     0            : ['C1', 'C2'],
        #     #     1            : ['RP1', 'RP2'],
        #     #     'Control'    : ['1Control'],
        #     #     'ControlType': 'Ratio of Intensities',
        #     # }
        #     self.OnImpMethod('fEvent')
        #     self.wShift.wTc.SetValue('1.8')
        #     self.wWidth.wTc.SetValue('0.3')
        #endregion -----------------------------------------------------> Test
    #---
    #endregion -----------------------------------------------> Instance setup

    #region --------------------------------------------------> Class Methods
    def SetInitialData(self, dataI:Optional[protMethod.UserData]) -> bool:
        """Set initial data.

            Parameters
            ----------
            dataI : protMethod.UserData or None
                Data to fill all fields and repeat an analysis. See Notes.

            Returns
            -------
            True
        """
        #region -------------------------------------------------> Fill Fields
        if dataI is not None:
            self.wUFile.wTc.SetValue(str(dataI.uFile))
            self.wIFile.wTc.SetValue(str(dataI.iFile))
            self.wId.wTc.SetValue(dataI.ID)
            #------------------------------>
            self.wCeroB.wCb.SetValue('Yes' if dataI.cero else 'No')
            self.wTransMethod.wCb.SetValue(dataI.tran)
            self.wNormMethod.wCb.SetValue(dataI.norm)
            self.wImputationMethod.wCb.SetValue(dataI.imp)
            self.wShift.wTc.SetValue(str(dataI.shift))
            self.wWidth.wTc.SetValue(str(dataI.width))
            #------------------------------> Values
            self.wScoreVal.wTc.SetValue(str(dataI.scoreVal))
            self.wSample.wCb.SetValue(mConfig.core.oSamplesP[dataI.indSample])
            self.wAlpha.wTc.SetValue(str(dataI.alpha))
            self.wCorrectP.wCb.SetValue(dataI.correctedP)
            #------------------------------> Columns
            self.wDetectedProt.wTc.SetValue(str(dataI.ocTargetProt))
            self.wGeneName.wTc.SetValue(str(dataI.ocGene))
            self.wScore.wTc.SetValue(str(dataI.ocScore))
            self.wExcludeProt.wTc.SetValue(" ".join(map(str, dataI.ocExcludeR)))
            self.wTcResults.SetValue(dataI.resCtrl)
            self.rLbDict[0] = dataI.labelA
            self.rLbDict[1] = dataI.labelB
            self.rLbDict['ControlType'] = dataI.ctrlType
            self.rLbDict['Control'] = dataI.ctrlName
            #------------------------------>
            self.IFileEnter(dataI.iFile)
            self.OnImpMethod('fEvent')
        else:
            super().SetConfOptions()
            #------------------------------>
            self.wAlpha.wTc.SetValue(mConfig.prot.alpha)
            self.wScoreVal.wTc.SetValue(mConfig.prot.scoreVal)
            self.wCorrectP.wCb.SetValue(mConfig.prot.correctP)
        #endregion ----------------------------------------------> Fill Fields

        return True
    #---

    def CheckNumberReplicates(self) -> bool:
        """Check the number of replicates when samples are paired and raw
            intensities are used.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> ResCtrl
        resCtrl = cMethod.ResControl2ListNumber(self.wTcResults.GetValue())
        #endregion ------------------------------------------------> ResCtrl

        #region ---------------------------------------------------> Check
        if self.dCheckRepNum[self.rLbDict["ControlType"]](resCtrl):
            return True
        #------------------------------>
        return False
        #endregion ------------------------------------------------> Check
    #---

    def CheckRepNum_OC(self, resCtrl:list[list[list[int]]]) -> bool:
        """Check equal number of replicas.

            Parameters
            ----------
            resCtrl: list[list[list[int]]]
                Result and Control as a list of list of list of int.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        badRep = []
        #endregion ------------------------------------------------> Variables

        #region ---------------------------------------------------> Check
        #------------------------------>
        ctrlL = len(resCtrl[0][0])
        #------------------------------>
        for row in resCtrl:
            for col in row:
                if len(col) != ctrlL:
                    badRep.append(col)
        #endregion ------------------------------------------------> Check

        #region ---------------------------------------------------> Return
        if not badRep:
            return True
        #------------------------------>
        self.rMsgError  = mConfig.core.mRepNum
        self.rException = ValueError(mConfig.prot.mRepNum.format(badRep))
        return False
        #endregion ------------------------------------------------> Return
    #---

    def CheckRepNum_Ratio(self, resCtrl:list[list[list[int]]]) -> bool:         # pylint: disable=unused-argument
        """Check equal number of replicas. Only needed for completion.

            Parameters
            ----------
            resCtrl: list[list[list[int]]]
                Result and Control as a list of list of list of int.

            Returns
            -------
            bool
        """
        return True
    #---

    def CheckRepNum_OCC(self, resCtrl:list[list[list[int]]]) -> bool:
        """Check equal number of replicas.

            Parameters
            ----------
            resCtrl: list[list[list[int]]]
                Result and Control as a list of list of list of int.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        badRep = []
        rowL   = len(resCtrl)
        colL   = len(resCtrl[0])
        #endregion ------------------------------------------------> Variables

        #region ---------------------------------------------------> Check
        for colI in range(0, colL):
            ctrlL = len(resCtrl[0][colI])
            for rowI in range(1,rowL):
                if len(resCtrl[rowI][colI]) != ctrlL:
                    badRep.append(resCtrl[rowI][colI])
        #endregion ------------------------------------------------> Check

        #region ---------------------------------------------------> Return
        if not badRep:
            return True
        #------------------------------>
        self.rMsgError  = mConfig.core.mRepNum
        self.rException = ValueError(mConfig.prot.mRepNum.format(badRep))
        return False
        #endregion ------------------------------------------------> Return
    #---

    def CheckRepNum_OCR(self, resCtrl:list[list[list[int]]]) -> bool:
        """Check equal number of replicas.

            Parameters
            ----------
            resCtrl: list[list[list[int]]]
                Result and Control as a list of list of list of int.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        badRep = []
        #endregion ------------------------------------------------> Variables

        #region ---------------------------------------------------> Check
        for row in resCtrl:
            #------------------------------>
            ctrlL = len(row[0])
            #------------------------------>
            for col in row[1:]:
                if len(col) != ctrlL:
                    badRep.append(col)
        #endregion ------------------------------------------------> Check

        #region ---------------------------------------------------> Return
        if not badRep:
            return True
        #------------------------------>
        self.rMsgError = mConfig.core.mRepNum
        self.rException = ValueError(mConfig.prot.mRepNum.format(badRep))
        return False
        #endregion ------------------------------------------------> Return
    #---
    #endregion ----------------------------------------------> Class Methods

    #region -----------------------------------------------------> Run Methods
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

        #region ------------------------------------------------> Mixed Fields
        #region ---------------------------------------------> # of Replicates
        msgStep = self.cLPdCheck + 'Number of Replicates'
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        #------------------------------>
        a = self.wSample.wCb.GetValue() == 'Paired Samples'
        b = self.rLbDict['Control'] == mConfig.prot.oControlType['Ratio']
        if a and not b:
            if not self.CheckNumberReplicates():
                return False
        #endregion ------------------------------------------> # of Replicates
        #endregion ---------------------------------------------> Mixed Fields

        return True
    #---

    def PrepareRun(self) -> bool:
        """Set variables and prepare data for analysis.

            Returns
            -------
            bool
        """
        #region -------------------------------------------------------> Input
        msgStep = self.cLPdPrepare + 'User input, reading'
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        #------------------------------> Read values
        impMethod     = self.wImputationMethod.wCb.GetValue()
        a = self.rLbDict['ControlType'] == mConfig.prot.oControlType['Ratio']
        rawI          = False if a else True
        detectedProt  = int(self.wDetectedProt.wTc.GetValue())
        geneName      = int(self.wGeneName.wTc.GetValue())
        scoreCol      = int(self.wScore.wTc.GetValue())
        excludeProt   = cMethod.Str2ListNumber(
            self.wExcludeProt.wTc.GetValue(), numType='int', sep=' ')
        resCtrl       = cMethod.ResControl2ListNumber(self.wTcResults.GetValue())
        resCtrlFlat   = cMethod.ResControl2Flat(resCtrl)
        resCtrlDF     = cMethod.ResControl2DF(resCtrl, 2+len(excludeProt)+1)
        resCtrlDFFlat = cMethod.ResControl2Flat(resCtrlDF)
        ocColumn      = [geneName, detectedProt, scoreCol] + excludeProt + resCtrlFlat
        dI = {
            'iFileN'      : self.cLiFile,
            'ID'          : self.cLId,
            'cero'        : self.cLCeroTreatD,
            'tran'        : self.cLTransMethod,
            'norm'        : self.cLNormMethod,
            'imp'         : self.cLImputation,
            'shift'       : self.cLShift,
            'width'       : self.cLWidth,
            'scoreVal'    : self.cLScoreVal,
            'indSample'   : self.cLSample,
            'alpha'       : self.cLAlpha,
            'correctedP'  : self.cLCorrectP,
            'ocTargetProt': self.cLDetectedProt,
            'ocGene'      : self.cLGene,
            'ocScore'     : self.cLScoreCol,
            'ocExcludeR'  : self.cLExcludeProt,
            'labelA'      : self.cLCond,
            'labelB'      : self.cLRP,
            'ctrlType'    : f"Control {self.cLCtrlType}",
            'ctrlName'    : f"Control {self.cLCtrlName}",
            'resCtrl'     : mConfig.core.lStResCtrlS,
        }
        if impMethod != mConfig.data.lONormDist:
            dI.pop('shift')
            dI.pop('width')
        #------------------------------> Create dataclass
        msgStep = self.cLPdPrepare + 'User input, processing'
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        #-------------->
        self.rDO = protMethod.UserData(
            uFile         = Path(self.wUFile.wTc.GetValue()),
            iFile         = Path(self.wIFile.wTc.GetValue()),
            ID            = self.wId.wTc.GetValue(),
            cero          = mConfig.core.oYesNo[self.wCeroB.wCb.GetValue()],
            norm          = self.wNormMethod.wCb.GetValue(),
            tran          = self.wTransMethod.wCb.GetValue(),
            imp           = self.wImputationMethod.wCb.GetValue(),
            shift         = float(self.wShift.wTc.GetValue()),
            width         = float(self.wWidth.wTc.GetValue()),
            scoreVal      = float(self.wScoreVal.wTc.GetValue()),
            rawInt        = rawI,
            indSample     = self.cOSample[self.wSample.wCb.GetValue()],
            alpha         = float(self.wAlpha.wTc.GetValue()),
            correctedP    = self.wCorrectP.wCb.GetValue(),
            ocTargetProt  = detectedProt,
            ocGene        = geneName,
            ocScore       = scoreCol,
            ocExcludeR    = excludeProt,                                         # type: ignore
            ocColumn      = ocColumn,                                            # type: ignore
            ocResCtrl     = resCtrl,
            resCtrl       = self.wTcResults.GetValue(),
            labelA        = self.rLbDict[0],
            labelB        = self.rLbDict[1],
            ctrlType      = self.rLbDict['ControlType'],
            ctrlName      = self.rLbDict['Control'][0],
            dfGene        = 0,
            dfTargetProt  = 1,
            dfScore       = 2,
            dfExcludeR    = [2+x for x in range(1, len(excludeProt)+1)],
            dfResCtrl     = resCtrlDF,
            dfResCtrlFlat = resCtrlDFFlat,
            dfColumnR     = resCtrlDFFlat,
            dfColumnF     = [2] + resCtrlDFFlat,
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
    #endregion --------------------------------------------------> Run Methods
#---


class ResControlExpConf(cPane.BaseResControlExpConf):
    """Creates the configuration panel for the Results - Control Experiments
        dialog when called from the ProtProf Tab

        Parameters
        ----------
        parent: wx.Widget
            Parent of the panel
        topParent: wx.Widget
            Top parent window
        NColF: int
            Total number of columns present in the Data File

        Attributes
        ----------
        dAddWidgets: dict
            Methods to add the widgets depending on the control type.
    """
    #region -----------------------------------------------------> Class setup
    cName = mConfig.prot.npResControlExp
    #------------------------------>
    cCtrlType = mConfig.prot.oControlType
    #------------------------------> Needed by ResControlExpConfBase
    cStLabel   = [f"{mConfig.prot.lStCond}", f"{mConfig.prot.lStRP}"]
    cLabelText = ['C', 'RP']
    #------------------------------>
    cTTTotalField = [
        f'Set the number of {mConfig.prot.lStCond}.',
        f'Set the number of {mConfig.prot.lStRP}.',
    ]
    #------------------------------>
    cLCtrlType = mConfig.core.lStCtrlType
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent:wx.Window, topParent:wx.Window, NColF:int)->None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.dAddWidget = {
            self.cCtrlType['OC']   : self.AddWidget_OC,
            self.cCtrlType['OCC']  : self.AddWidget_OCC,
            self.cCtrlType['OCR']  : self.AddWidget_OCR,
            self.cCtrlType['Ratio']: self.AddWidget_Ratio,
        }
        #--------------> Control type from previous call to Setup Fields
        self.rControlVal = ''
        #------------------------------> Super init
        super().__init__(parent, self.cName, topParent, NColF)
        #------------------------------> Choices
        self.cControlTypeO = [x for x in self.cCtrlType.values()]
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        #------------------------------> wx.StaticText
        self.wStControl = wx.StaticText(
            self.wSwLabel, label='Control Experiment:')
        self.wStControlT = wx.StaticText(
            self.wSwLabel, label=self.cLCtrlType)
        #------------------------------> wx.ComboBox
        self.wCbControl = wx.ComboBox(
            self.wSwLabel,
            style     = wx.CB_READONLY,
            choices   = self.cControlTypeO,
            validator = cValidator.IsNotEmpty(),
        )
        #endregion --------------------------------------------------> Widgets

        #region -----------------------------------------------------> Tooltip
        self.wStControl.SetToolTip(
            'Set the Type and Name of the control experiment.')
        self.wStControlT.SetToolTip('Set the Type of the control experiment.')
        #endregion --------------------------------------------------> Tooltip

        #region ------------------------------------------------------> Sizers
        #------------------------------>
        self.sSWLabelControl = wx.BoxSizer(wx.HORIZONTAL)
        self.sSWLabelControl.Add(
            self.wStControl, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.sSWLabelControl.Add(
            self.wStControlT, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.sSWLabelControl.Add(self.wCbControl, 0, wx.EXPAND|wx.ALL, 5)
        self.sSWLabelControl.Add(
            self.wControlN.wSt, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.sSWLabelControl.Add(self.wControlN.wTc, 1, wx.EXPAND|wx.ALL, 5)
        #------------------------------>
        self.sSWLabelMain.Add(
            self.sSWLabelControl, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        #------------------------------>
        self.sSizer.Fit(self)
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind
        self.wCbControl.Bind(wx.EVT_COMBOBOX, self.OnControl)
        #endregion -----------------------------------------------------> Bind

        #region -----------------------------------------------> Initial State
        self.SetInitialState()
        #endregion --------------------------------------------> Initial State
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Event methods
    def OnControl(self, event:wx.CommandEvent) -> bool:                         # pylint: disable=unused-argument
        """Enable/Disable the Control name when selecting control type.

            Parameters
            ----------
            event:wx.Event
                Information about the event.

            Returns
            -------
            True
        """
        #region ---------------------------------------------------> Get value
        control = self.wCbControl.GetValue()
        #endregion ------------------------------------------------> Get value

        #region ------------------------------------------------------> Action
        if control == self.cCtrlType['Ratio']:
            self.wControlN.wTc.SetValue('None')
            self.wControlN.wTc.SetEditable(False)
        else:
            self.wControlN.wTc.SetEditable(True)
        #endregion ---------------------------------------------------> Action

        return True
    #---

    def OnCreate(self, event:wx.CommandEvent) -> bool:
        """Create the widgets in the white panel.

            Parameters
            ----------
            event: wx.Event
                Information about the event.

            Returns
            -------
            bool
        """
        #region -------------------------------------------------> Check input
        if not (n := self.CheckLabel(True)):
            return False
        #endregion ----------------------------------------------> Check input

        #region ---------------------------------------------------> Variables
        control = self.wCbControl.GetValue()
        #------------------------------>
        if control == self.cCtrlType['OCR']:
            Nc   = n[0]                                                         # Number of rows of tc needed
            Nr   = n[1] + 1                                                     # Number of tc needed for each row
            NCol = n[1] + 2                                                     # Number of columns in the sizer
            NRow = n[0] + 1                                                     # Number of rows in the sizer
        elif control == self.cCtrlType['Ratio']:
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
        if control == self.cCtrlType['Ratio']:
            self.rFSectStDict['Control'][0].Hide()
        #endregion -----------------------------> Create/Destroy wx.StaticText

        #region ----------------------------------> Create/Destroy wx.TextCtrl
        #------------------------------> Widgets
        for k in range(0, Nc):
            #------------------------------> Get row
            row = self.rFSectTcDict.get(k, [])
            lRow = len(row)
            #------------------------------> First row is especial
            if k == 0 and control == self.cCtrlType['OC']:
                if control == self.rControlVal:
                    continue
                #--------------> Destroy old widgets
                for j in row:
                    j.Destroy()
                #--------------> New Row and wx.TextCtrl
                row = []
                row.append(
                    wx.TextCtrl(
                        self.wSwMatrix,
                        size      = self.cSLabel,
                        validator = self.cVColNumList,
                    )
                )
                #--------------> Assign & Continue to next for step
                self.rFSectTcDict[k] = row
                continue
            #------------------------------> Create destroy
            if Nr > lRow:
                #-------------->  Create
                for j in range(lRow, Nr):
                    row.append(
                        wx.TextCtrl(
                            self.wSwMatrix,
                            size      = self.cSLabel,
                            validator = self.cVColNumList,
                        )
                    )
                #-------------->  Add to dict
                self.rFSectTcDict[k] = row
            else:
                for j in range(Nr, lRow):
                    #-------------->  Destroy
                    row[-1].Destroy()
                    #--------------> Remove from list
                    row.pop()
        #------------------------------> Drop keys and destroy from dict
        dK = [x for x in self.rFSectTcDict]
        for k in dK:
            if k+1 > Nc:
                #--------------> Destroy this widget
                for j in self.rFSectTcDict[k]:
                    j.Destroy()
                #--------------> Remove key
                del self.rFSectTcDict[k]
        #------------------------------> Clear value if needed
        if control != self.rControlVal:
            for v in self.rFSectTcDict.values():
                for j in v:
                    j.SetValue('')
        #endregion -------------------------------> Create/Destroy wx.TextCtrl

        #region ------------------------------------------------> Setup Sizers
        #------------------------------> Adjust size
        self.sSWMatrix.SetCols(NCol)
        self.sSWMatrix.SetRows(NRow)
        #------------------------------> Add widgets
        self.dAddWidget[control](NCol, NRow)
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

        #region -------------------------------------------> Update controlVal
        self.rControlVal = control
        #endregion ----------------------------------------> Update controlVal

        return True
    #---

    def OnOK(self, export:bool=True) -> bool:
        """Check wx.Dialog content and send values to topParent.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        ctrlType = self.wCbControl.GetValue()
        ctrl     = True
        #endregion ------------------------------------------------> Variables

        #region ---------------------------------------------------> Super
        a, oText = super().OnOK(export=False)
        if not a:
            return False
        #endregion ------------------------------------------------> Super

        #region --------------------------------------------------> Check Ctrl
        if ctrlType  == self.cCtrlType['OC']:
            if self.rFSectTcDict[0][0].GetValue().strip() == '':
                ctrl = False
        elif ctrlType == self.cCtrlType['OCC']:
            for w in self.rFSectTcDict[0]:
                if w.GetValue().strip() == '':
                    ctrl = False
                    break
        else:
            for w in self.rFSectTcDict.values():
                if w[0].GetValue().strip() == '':
                    ctrl = False
                    break
        #------------------------------>
        if not ctrl:
            cWindow.Notification(
                'errorF', msg=mConfig.core.mCtrlEmpty, parent=self)
            return False
        #endregion -----------------------------------------------> Check Ctrl

        #region --------------------------------------------------->
        self.Export2TopParent(oText)
        #endregion ------------------------------------------------>

        return True
    #---
    #endregion ------------------------------------------------> Event Methods

    #region --------------------------------------------------> Class Methods
    def AddWidget_OC(self, NCol:int, NRow:int) -> bool:                         # pylint: disable=unused-argument
        """Add the widget when Control Type is One Control.

            Parameters
            ----------
            NCol: int
                Number of columns in the sizer.
            NRow: int
                Number of rows in the sizer.

            Returns
            -------
            bool
        """
        #region -------------------------------------------------> Control Row
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
        #endregion ----------------------------------------------> Control Row

        #region ---------------------------------------------------> RP Labels
        #--------------> Empty space
        self.sSWMatrix.AddSpacer(1)
        #--------------> Labels
        for k in self.rFSectStDict[1]:
            self.sSWMatrix.Add(k, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        #endregion ------------------------------------------------> RP Labels

        #region ------------------------------------------------> Other fields
        K = 1
        for k in self.rFSectStDict[0]:
            #--------------> Add Label
            self.sSWMatrix.Add(
                k,
                0,
                wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL|wx.ALL,
                5
            )
            #--------------> Add tc
            for j in self.rFSectTcDict[K]:
                self.sSWMatrix.Add(j, 0, wx.EXPAND|wx.ALL, 5)
            K += 1
        #endregion ---------------------------------------------> Other fields

        return True
    #---

    def AddWidget_OCC(self, NCol:int, NRow:int) -> bool:                        # pylint: disable=unused-argument
        """Add the widget when Control Type is One Control.

            Parameters
            ----------
            NCol: int
                Number of columns in the sizer.
            NRow: int
                Number of rows in the sizer.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> RP Labels
        self.sSWMatrix.AddSpacer(1)
        #------------------------------>
        for k in self.rFSectStDict[1]:
            self.sSWMatrix.Add(k, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        #endregion ------------------------------------------------> RP Labels

        #region -------------------------------------------------> Control Row
        self.sSWMatrix.Add(
            self.rFSectStDict['Control'][0],
            0,
            wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL|wx.ALL,
            5
        )
        #------------------------------>
        for k in self.rFSectTcDict[0]:
            self.sSWMatrix.Add(
                k,
                0,
                wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL,
                5
            )
        #endregion ----------------------------------------------> Control Row

        #region --------------------------------------------------> Other Rows
        for k, v in self.rFSectTcDict.items():
            #------------------------------> Skip control row
            if k == 0:
                continue
            #------------------------------> Add Label
            self.sSWMatrix.Add(
                self.rFSectStDict[0][k-1],
                0,
                wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL|wx.ALL,
                5
            )
            #------------------------------> Add wx.TextCtrl
            for j in v:
                self.sSWMatrix.Add(
                    j, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL,5)
        #endregion -----------------------------------------------> Other Rows

        return True
    #---

    def AddWidget_OCR(self, NCol:int, NRow:int) -> bool:                        # pylint: disable=unused-argument
        """Add the widget when Control Type is One Control.

            Parameters
            ----------
            NCol: int
                Number of columns in the sizer.
            NRow: int
                Number of rows in the sizer.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> RP Labels
        self.sSWMatrix.AddSpacer(1)
        #------------------------------>
        self.sSWMatrix.Add(
            self.rFSectStDict['Control'][0], 0, wx.ALIGN_CENTER|wx.ALL, 5)
        #------------------------------>
        for k in self.rFSectStDict[1]:
            self.sSWMatrix.Add(k, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        #endregion ------------------------------------------------> RP Labels

        #region --------------------------------------------------> Other rows
        for k, v in self.rFSectTcDict.items():
            #------------------------------>
            self.sSWMatrix.Add(
                self.rFSectStDict[0][k],
                0,
                wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL|wx.ALL,
                5
            )
            #------------------------------>
            for j in v:
                self.sSWMatrix.Add(j, 0, wx.EXPAND|wx.ALL, 5)
        #endregion -----------------------------------------------> Other rows

        return True
    #---

    def AddWidget_Ratio(self, NCol:int, NRow:int) -> bool:                      # pylint: disable=unused-argument
        """Add the widget when Control Type is Data as Ratios.

            Parameters
            ----------
            NCol: int
                Number of columns in the sizer.
            NRow: int
                Number of rows in the sizer.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> RP Labels
        self.sSWMatrix.AddSpacer(1)
        #------------------------------>
        for k in self.rFSectStDict[1]:
            self.sSWMatrix.Add(k, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        #endregion ------------------------------------------------> RP Labels

        #region --------------------------------------------------> Other rows
        for k, v in self.rFSectTcDict.items():
            #------------------------------>
            self.sSWMatrix.Add(
                self.rFSectStDict[0][k],
                0,
                wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL|wx.ALL,
                5
            )
            #------------------------------>
            for j in v:
                self.sSWMatrix.Add(j, 0, wx.EXPAND|wx.ALL, 5)
        #endregion -----------------------------------------------> Other rows

        return True
    #---
    #endregion -----------------------------------------------> Class Methods
#---
#endregion ----------------------------------------------------------> Classes
