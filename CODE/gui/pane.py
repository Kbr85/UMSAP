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


"""Panels of the application"""


#region -------------------------------------------------------------> Imports
import _thread
import shutil
from math    import ceil
from pathlib import Path
from typing  import Union, Optional

import pandas as pd

import wx
import wx.lib.scrolledpanel as scrolled

import config.config  as mConfig
import data.check     as mCheck
import data.method    as mMethod
import data.exception as mException
import data.file      as mFile
import data.statistic as mStatistic
import gui.method     as gMethod
import gui.validator  as mValidator
import gui.widget     as mWidget
import gui.window     as mWindow
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Classes
class PaneListCtrlSearchPlot(wx.Panel):
    """Creates a panel with a wx.ListCtrl and below it a wx.SearchCtrl.

        Parameters
        ----------
        parent: wx.Window
            Parent of the panel
        colLabel : list of str or None
            Name of the columns in the wx.ListCtrl. Default is None
        colSize : list of int or None
            Size of the columns in the wx.ListCtrl. Default is None
        data : list[list]
            Initial Data for the wx.ListCtrl.
        style : wx.Style
            Style of the wx.ListCtrl. Default is wx.LC_REPORT.
        tcHint : str
            Hint for the wx.SearchCtrl. Default is ''.
    """
    #region -----------------------------------------------------> Class setup
    cName = mConfig.npListCtrlSearchPlot
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(                                                               # pylint: disable=dangerous-default-value
        self,
        parent  : wx.Window,
        colLabel: list[str]=[],
        colSize : list[int]=[],
        data    : list[list]=[],
        style   : int=wx.LC_REPORT,
        tcHint  : str='',
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(parent, name=self.cName)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wLCS = mWidget.ListCtrlSearch(
            self,
            listT    = 2,
            colLabel = colLabel,
            colSize  = colSize,
            canCut   = False,
            canPaste = False,
            style    = style,
            data     = data,
            tcHint   = tcHint,
        )
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        self.SetSizer(self.wLCS.sSizer)
        #endregion ---------------------------------------------------> Sizers
    #---
    #endregion -----------------------------------------------> Instance setup
#---


class NPlots(wx.Panel):
    """The panel will contain N plots distributed in a wx.FlexGridSizer.

        Parameters
        ----------
        parent: wx.Window
            Parent of the wx.Panel holding the plots.
        tKeys : list of str
            Keys for a dict holding a reference to the plots
        nCol : int
            Number of columns in the wx.FlexGridSizer holding the plots.
            Number of needed rows will be automatically calculated.
        dpi : int
            DPI value for the Matplot plots.
        statusbar : wx.StatusBar or None
            StatusBar to display information about the plots.

        Attributes
        ----------
        dPlot : dict
            Keys are tKeys and values mWidget.MatPlotPanel
        cName : str
            Name of the panel holding the plots.
        nCol : int
            Number of columns in the sizer
        nRow: int
            Number of rows in the sizer.
    """
    #region -----------------------------------------------------> Class setup
    cName = mConfig.npNPlot
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self,
        parent   : wx.Window,
        tKeys    : list[str],
        nCol     : int,
        dpi      : int=mConfig.confGeneral['DPI'],
        statusbar: Optional[wx.StatusBar]=None,
        ) -> None  :
        """ """
        #region -----------------------------------------------> Initial Setup
        self.nCol = nCol
        self.nRow = ceil(len(tKeys)/nCol)
        #------------------------------>
        super().__init__(parent, name=self.cName)
        #endregion --------------------------------------------> Initial Setup

        #region ------------------------------------------------------> Sizers
        #------------------------------>
        self.sSizer = wx.FlexGridSizer(self.nRow, self.nCol, 1,1)
        #------------------------------>
        for k in range(0, self.nCol):
            self.sSizer.AddGrowableCol(k,1)
        for k in range(0, self.nRow):
            self.sSizer.AddGrowableRow(k,1)
        #------------------------------>
        self.SetSizer(self.sSizer)
        #endregion ---------------------------------------------------> Sizers

        #region -----------------------------------------------------> Widgets
        self.dPlot = {}
        for k in tKeys:
            #------------------------------> Create
            self.dPlot[k] = mWidget.MatPlotPanel(
                self, dpi=dpi, statusbar=statusbar)
            #------------------------------> Add to sizer
            self.sSizer.Add(self.dPlot[k], 1, wx.EXPAND|wx.ALL, 5)
        #endregion --------------------------------------------------> Widgets
    #---
    #endregion -----------------------------------------------> Instance setup
#---


class PaneTarProt(BaseConfPanelMod2):
    """Configuration Pane for the Targeted Proteolysis module.

        Parameters
        ----------
        parent: wx.Widget
            Parent of the pane
        dataI : dict or None
            Initial data provided by the user in a previous analysis.
            This contains both I and CI dicts e.g. {'I': I, 'CI': CI}.

        Attributes
        ----------
        rDI: dict
            Dictionary with the user input. Keys are labels in the panel plus:
            {
                config.lStTarProtExp            : [list of experiments],
                f"Control {config.lStCtrlName}" : "Control Name",
            }
        rDO: dict
            Dictionary with checked user input. Keys are:
            {
                "iFile"      : "Path to input data file",
                "uFile"      : "Path to umsap file.",
                "seqFile"    : "Path to the sequence file",
                "ID"         : "Analysis ID",
                "Cero"       : Boolean, how to treat cero values,
                "TransMethod": "Transformation method",
                "NormMethod" : "Normalization method",
                "ImpMethod"  : "Imputation method",
                "Shift"      : float,
                "Width"      : float,
                "TargetProt" : "Target Protein",
                "ScoreVal"   : "Score value threshold",
                "Alpha"      : "Significance level",
                "SeqLength"  : "Sequence length",
                "AA"         : "Positions to analyze during the AA distribution",
                "Hist"       : "Windows width for the Histograms",
                "Exp"        : "['Exp1', 'Exp2', 'Exp3']",
                "ControlL"   : ['Ctrl']
                "oc" : {
                    "SeqCol"       : Column of Sequences,
                    "TargetProtCol": Column of Proteins,
                    "ScoreCol"     : Score column,
                    "ResCtrl"      : [List of columns containing the control and
                        experiments column numbers],
                    "ColumnF"      : [Flat list with float columns],
                    "Column"       : [Flat list of all column numbers with the
                              following order: SeqCol, TargetProtCol,
                              ScoreColRes & Control]
                },
                "df" : { Colum numbers if the pd.df created from the input file
                    "SeqCol"       : 0,
                    "TargetProtCol": 1,
                    "ScoreCol"     : 2,
                    "ResCtrl"      : [[[]], [[]],...,[[]]],
                    "ResCtrlFlat"  : Flat ResCtrl,
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
            }
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
                    'I' : self.d,
                    'CI': self.do,
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
    cName = mConfig.npTarProt
    #------------------------------> Label
    cLAAPos    = 'AA Positions'
    cLHist     = 'Histogram Windows'
    cLExp      = mConfig.lStTarProtExp
    cLCtrlName = mConfig.lStCtrlName
    cLDFFirst  = mConfig.dfcolTarProtFirstPart
    cLDFSecond = mConfig.dfcolTarProtBLevel
    cLPdRunText = 'Targeted Proteolysis Analysis'
    #------------------------------> Hint
    cHAAPos = 'e.g. 5'
    cHHist  = 'e.g. 50 or 50 100 200'
    #------------------------------> Tooltip
    cTTAAPos = (f'Number of positions around the cleavage sites to consider '
        f'for the AA distribution analysis.\ne.g. 5{mConfig.mOptField}')
    cTTHist = (f'Size of the histogram windows. One number will result in '
        f'equally spaced windows. Multiple numbers allow defining custom sized '
        f'windows.\ne.g. 50 or 0 50 100 150 500{mConfig.mOptField}')
    #------------------------------> Needed by BaseConfPanel
    cURL         = f"{mConfig.urlTutorial}/targeted-proteolysis"
    cSection     = mConfig.nmTarProt
    cTitlePD     = f"Running {mConfig.nmTarProt} Analysis"
    cGaugePD     = 35
    rMainData    = '{}_{}-TargetedProteolysis-Data.txt'
    rDExtra: dict= {
        'cLDFFirst' : cLDFFirst,
        'cLDFSecond': cLDFSecond,
    }
    #------------------------------> Optional configuration
    cTTHelp = mConfig.ttBtnHelp.format(cURL)
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent, dataI: dict={}) -> None:                         # pylint: disable=dangerous-default-value
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(parent)
        #------------------------------>
        self.dfAA    = pd.DataFrame()
        self.dfHist  = pd.DataFrame()
        self.dfCpR   = pd.DataFrame()
        self.dfCEvol = pd.DataFrame()
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        #------------------------------> Values
        self.wAAPos = mWidget.StaticTextCtrl(
            self.wSbValue,
            stLabel   = self.cLAAPos,
            stTooltip = self.cTTAAPos,
            tcSize    = self.cSTc,
            tcHint    = self.cHAAPos,
            validator = mValidator.NumberList(
                numType='int', nN=1, vMin=0, opt=True)
        )
        self.wHist = mWidget.StaticTextCtrl(
            self.wSbValue,
            stLabel   = self.cLHist,
            stTooltip = self.cTTHist,
            tcSize    = self.cSTc,
            tcHint    = self.cHHist,
            validator = mValidator.NumberList(
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
        rCheckUserInput = {
            self.cLAlpha       :[self.wAlpha.wTc,           mConfig.mOne01Num      , False],
            self.cLAAPos       :[self.wAAPos.wTc,           mConfig.mOneZPlusNum   , False],
            self.cLHist        :[self.wHist.wTc,            mConfig.mValueBad      , False],
            f'{self.cLSeqCol} column' :[self.wSeqCol.wTc,   mConfig.mOneZPlusNumCol, True ],
            self.cLDetectedProt:[self.wDetectedProt.wTc,    mConfig.mOneZPlusNumCol, True ],
            self.cLScoreCol    :[self.wScore.wTc,           mConfig.mOneZPlusNumCol, True ],
            self.cLResControl  :[self.wTcResults,          mConfig.mResCtrl       , False]
        }
        self.rCheckUserInput = self.rCheckUserInput | rCheckUserInput
        #endregion -------------------------------------------> checkUserInput

        #region -------------------------------------------------------> DataI
        self.SetInitialData(dataI)
        #endregion ----------------------------------------------------> DataI

        #region --------------------------------------------------------> Test
        if mConfig.development:
            # pylint: disable=line-too-long
            import getpass                                                      # pylint: disable=import-outside-toplevel
            user = getpass.getuser()
            if mConfig.os == "Darwin":
                self.wUFile.wTc.SetValue("/Users/" + str(user) + "/TEMP-GUI/BORRAR-UMSAP/umsap-dev.umsap")
                self.wIFile.wTc.SetValue("/Users/" + str(user) + "/Dropbox/SOFTWARE-DEVELOPMENT/APPS/UMSAP/LOCAL/DATA/UMSAP-TEST-DATA/TARPROT/tarprot-data-file.txt")
                self.wSeqFile.wTc.SetValue("/Users/" + str(user) + "/Dropbox/SOFTWARE-DEVELOPMENT/APPS/UMSAP/LOCAL/DATA/UMSAP-TEST-DATA/TARPROT/tarprot-seq-both.txt")
                # self.wSeqFile.tc.SetValue("/Users/" + str(user) + "/Dropbox/SOFTWARE-DEVELOPMENT/APPS/UMSAP/LOCAL/DATA/UMSAP-TEST-DATA/TARPROT/tarprot-seq-rec.txt")
            elif mConfig.os == 'Windows':
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
        if dataI is not None:
            #------------------------------>
            dataInit = dataI['uFile'].parent / mConfig.fnDataInit
            iFile    = dataInit / dataI['I'][self.cLiFile]
            seqFile  = dataInit / dataI['I'][f'{self.cLSeqFile} File']
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
            self.wAAPos.wTc.SetValue(dataI['I'][self.cLAAPos])
            self.wHist.wTc.SetValue(dataI['I'][self.cLHist])
            #------------------------------> Columns
            self.wSeqCol.wTc.SetValue(dataI['I'][f'{self.cLSeqCol} Column'])
            self.wDetectedProt.wTc.SetValue(dataI['I'][self.cLDetectedProt])
            self.wScore.wTc.SetValue(dataI['I'][self.cLScoreCol])
            self.wTcResults.SetValue(dataI['I'][mConfig.lStResultCtrlS])
            self.rLbDict[0] = dataI['I'][self.cLExp]
            self.rLbDict['Control'] = dataI['I'][f"Control {self.cLCtrlName}"]
            #------------------------------>
            self.OnIFileLoad('fEvent')
            self.OnImpMethod('fEvent')
        else:
            pass
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
                self.wImputationMethod.wCb.GetValue()),
            self.EqualLenLabel(self.cLShift) : (
                self.wShift.wTc.GetValue()),
            self.EqualLenLabel(self.cLWidth) : (
                self.wWidth.wTc.GetValue()),
            self.EqualLenLabel(self.cLTargetProt) : (
                self.wTargetProt.wTc.GetValue()),
            self.EqualLenLabel(self.cLScoreVal) : (
                self.wScoreVal.wTc.GetValue()),
            self.EqualLenLabel(self.cLAlpha) : (
                self.wAlpha.wTc.GetValue()),
            self.EqualLenLabel(self.cLAAPos) : (
                self.wAAPos.wTc.GetValue()),
            self.EqualLenLabel(self.cLHist) : (
                self.wHist.wTc.GetValue()),
            self.EqualLenLabel(f'{self.cLSeqCol} Column') : (
                self.wSeqCol.wTc.GetValue()),
            self.EqualLenLabel(self.cLDetectedProt) : (
                self.wDetectedProt.wTc.GetValue()),
            self.EqualLenLabel(self.cLScoreCol) : (
                self.wScore.wTc.GetValue()),
            self.EqualLenLabel(mConfig.lStResultCtrlS): (
                self.wTcResults.GetValue()),
            self.EqualLenLabel(self.cLExp) : (
                self.rLbDict[0]),
            self.EqualLenLabel(f"Control {self.cLCtrlName}") : (
                self.rLbDict['Control']),
        }
        #endregion --------------------------------------------------------> d

        #region ----------------------------------------------------------> do
        #------------------------------> Dict with all values
        #--------------> Step
        msgStep = self.cLPdPrepare + 'User input, processing'
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        #--------------> SeqLength
        aaPosVal     = self.wAAPos.wTc.GetValue()
        aaPos        = int(aaPosVal) if aaPosVal != '' else None
        histVal      = self.wHist.wTc.GetValue()
        hist         = [int(x) for x in histVal.split()] if histVal != '' else None
        #--------------> Columns
        seqCol        = int(self.wSeqCol.wTc.GetValue())
        detectedProt  = int(self.wDetectedProt.wTc.GetValue())
        scoreCol      = int(self.wScore.wTc.GetValue())
        resCtrl       = mMethod.ResControl2ListNumber(self.wTcResults.GetValue())
        resCtrlFlat   = mMethod.ResControl2Flat(resCtrl)
        resCtrlDF     = mMethod.ResControl2DF(resCtrl, 3)
        resCtrlDFFlat = mMethod.ResControl2Flat(resCtrlDF)
        #-------------->
        self.rDO  = {
            'iFile'      : Path(self.wIFile.wTc.GetValue()),
            'uFile'      : Path(self.wUFile.wTc.GetValue()),
            'seqFile'    : Path(self.wSeqFile.wTc.GetValue()),
            'ID'         : self.wId.wTc.GetValue(),
            'Cero'       : mConfig.oYesNo[self.wCeroB.wCb.GetValue()],
            'TransMethod': self.wTransMethod.wCb.GetValue(),
            'NormMethod' : self.wNormMethod.wCb.GetValue(),
            'ImpMethod'  : self.wImputationMethod.wCb.GetValue(),
            'Shift'      : float(self.wShift.wTc.GetValue()),
            'Width'      : float(self.wWidth.wTc.GetValue()),
            'TargetProt' : self.wTargetProt.wTc.GetValue(),
            'ScoreVal'   : float(self.wScoreVal.wTc.GetValue()),
            'Alpha'      : float(self.wAlpha.wTc.GetValue()),
            'AA'         : aaPos,
            'Hist'       : hist,
            'Exp'        : self.rLbDict[0],
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
        if super().PrepareRun():
            pass
        else:
            self.rMsgError = 'Something went wrong when preparing the analysis.'
            return False
        #endregion ------------------------------------------------> Super

        return True
    #---

    def RunAnalysis(self) -> bool:
        """Perform the equivalence tests.

            Returns
            -------
            bool
        """
        #region -----------------------------------------------------> rDExtra
        self.rDExtra['rSeqFileObj'] = self.rSeqFileObj
        #endregion --------------------------------------------------> rDExtra

        #region -----------------------------------------------------> TarProt
        if super().RunAnalysis():
            pass
        else:
            return False
        #endregion --------------------------------------------------> TarProt

        # Further Analysis
        idx = pd.IndexSlice

        #region ----------------------------------------------------> Cleavage
        msgStep = (f'{self.cLPdRun} Cleavage per Residue')
        wx.CallAfter(self.rDlg.UpdateStG, msgStep)
        #------------------------------>
        a = self.cLDFFirst[2:]+self.rDO['Exp']
        b = self.cLDFFirst[2:]+['P']
        tIdxH = idx[a,b] # Also used for Hist
        #------------------------------>
        try:
            self.dfCpR = mMethod.R2CpR(
                self.dfR.loc[:, tIdxH],                                         # type: ignore
                self.rDO['Alpha'],
                self.rDO['ProtLength'],
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
        a = self.cLDFFirst[2:]+self.rDO['Exp']
        b = self.cLDFFirst[2:]+['Int', 'P']
        tIdx = idx[a,b]
        #------------------------------>
        try:
            self.dfCEvol = mMethod.R2CEvol(
                self.dfR.loc[:, tIdx],                                          # type: ignore
                self.rDO['Alpha'],
                self.rDO['ProtLength'],
            )
        except Exception as e:
            self.rMsgError = 'The Cleavage Evolution method failed.'
            self.rException = e
            return False
        #endregion ------------------------------------------------> CutEvo

        #region ----------------------------------------------------------> AA
        if self.rDO['AA'] is not None:
            #------------------------------>
            msgStep = (f'{self.cLPdRun} AA Distribution')
            wx.CallAfter(self.rDlg.UpdateStG, msgStep)
            #------------------------------>
            tIdx = idx[['Sequence']+self.rDO['Exp'],['Sequence', 'P']]
            try:
                self.dfAA = mMethod.R2AA(
                    self.dfR.loc[:,tIdx],                                       # type: ignore
                    self.rSeqFileObj.rSeqRec, # type: ignore
                    self.rDO['Alpha'],
                    self.rDO['ProtLength'][0],
                    pos=self.rDO['AA'],
                )
            except Exception as e:
                self.rMsgError = 'Amino acid distribution calculation failed.'
                self.rException = e
                return False
        else:
            pass
        #endregion -------------------------------------------------------> AA

        #region --------------------------------------------------------> Hist
        if self.rDO['Hist'] is not None:
            #------------------------------>
            msgStep = (f'{self.cLPdRun} Histograms')
            wx.CallAfter(self.rDlg.UpdateStG, msgStep)
            #------------------------------>
            try:
                self.dfHist = mMethod.R2Hist(
                    self.dfR.loc[:,tIdxH],                                      # type: ignore
                    self.rDO['Alpha'],
                    self.rDO['Hist'],
                    self.rDO['ProtLength']
                )
            except Exception as e:
                self.rMsgError = 'The Histogram generation method failed.'
                self.rException = e
                return False
        else:
            pass
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
            mConfig.fnInitial.format(self.rDate, '01')   : self.dfI,
            mConfig.fnFloat.format(self.rDate, '02')     : self.dfF,
            mConfig.fnTrans.format(self.rDate, '03')     : self.dfT,
            mConfig.fnNorm.format(self.rDate, '04')      : self.dfN,
            mConfig.fnImp.format(self.rDate, '05')       : self.dfIm,
            mConfig.fnTargetProt.format(self.rDate, '06'): self.dfTP,
            mConfig.fnScore.format(self.rDate, '07')     : self.dfS,
            self.rMainData.format(self.rDate, '08')     : self.dfR,
        }
        stepDict['R'] = self.rMainData.format(self.rDate, '08')
        #endregion -----------------------------------------------> Data Steps

        #region --------------------------------------------> Further Analysis
        #------------------------------>
        stepDict['CpR'] = f'{self.rDate}_CpR.txt'
        stepDict['CEvol'] = f'{self.rDate}_CEvol.txt'
        #------------------------------>
        stepDict['AA']= {}
        if self.rDO['AA'] is not None:
            stepDict['AA'][f'{self.rDate}_{self.rDO["AA"]}'] = (
                f'{self.rDate}_AA-{self.rDO["AA"]}.txt')
        else:
            pass
        #------------------------------>
        stepDict['Hist']= {}
        if self.rDO['Hist'] is not None:
            stepDict['Hist'][f'{self.rDate}_{self.rDO["Hist"]}'] = (
                f'{self.rDate}_Hist-{self.rDO["Hist"]}.txt')
        else:
            pass
        #endregion -----------------------------------------> Further Analysis

        return self.WriteOutputData(stepDict)
    #---

    def RunEnd(self) -> bool:
        """Clean and get """
        #------------------------------>
        if self.rDFile:
            self.wSeqFile.wTc.SetValue(str(self.rDFile[1]))
        else:
            pass
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


class PaneResControlExpConfLimProt(BaseResControlExpConf):
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
    cName = mConfig.npResControlExpLimProt
    #------------------------------> Needed by ResControlExpConfBase
    cStLabel   = [f"{mConfig.lStLimProtLane}:", f"{mConfig.lStLimProtBand}:"]
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
        if (n := self.CheckLabel(False)):
            pass
        else:
            return False
        #endregion ----------------------------------------------> Check input

        #region ---------------------------------------------------> Variables
        Nl = n[0]
        NCol = n[0]+1
        Nb = n[1]
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
                else:
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
            else:
                pass
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
        dK = [x for x in self.rFSectTcDict]
        #------------------------------>
        for k in dK:
            if k > Nb:
                #------------------------------>
                for j in self.rFSectTcDict[k]:
                    j.Destroy()
                #------------------------------>
                del self.rFSectTcDict[k]
            else:
                pass
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

    def OnOK(self, export: bool=True) -> bool:
        """Check wx.Dialog content and send values to topParent.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Super
        if super().OnOK()[0]:
            return True
        else:
            return False
        #endregion ------------------------------------------------> Super
    #---
    #endregion ------------------------------------------------> Event Methods
#---


class PaneResControlExpConfTarProt(BaseResControlExpConf):
    """Creates the configuration panel for the Results - Control Experiments
        dialog when called from the TarProt Tab.

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
    cName = mConfig.npResControlExpLimProt
    #------------------------------> Needed by ResControlExpConfBase
    cStLabel = [f"{mConfig.lStTarProtExp}:"]
    cLabelText = ['Exp']
    #------------------------------> Tooltips
    cTTTotalField = [f'Set the number of {cStLabel[0]}.']
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
        if (n := self.CheckLabel(False)):
            pass
        else:
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
            else:
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

    def OnOK(self, export: bool=True) -> bool:
        """Check wx.Dialog content and send values to topParent.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Super
        if super().OnOK()[0]:
            return True
        else:
            return False
        #endregion ------------------------------------------------> Super
    #---
    #endregion ------------------------------------------------> Class methods
#---
#endregion ----------------------------------------------------------> Classes
