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


"""Panes for the help module of the app"""


#region -------------------------------------------------------------> Imports
import wx
import wx.lib.scrolledpanel as scrolled

from config.config import config as mConfig
from core import validator as cValidator
from core import widget    as cWidget
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Classes
class General(scrolled.ScrolledPanel):
    """Panel for the Preferences window.

        Parameters
        ----------
        parent: wx.Window
            Parent of the pane.
    """
    #region -----------------------------------------------------> Class setup
    cName = mConfig.help.npGeneral
    #------------------------------>
    cLTab = mConfig.help.ntGeneral
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent):
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(parent, name=self.cName)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wUpdate = wx.RadioBox(
            self,
            label   = 'Check for Updates',
            choices = ['Never', 'Always'],
        )
        #------------------------------> Images
        self.wSbImg = wx.StaticBox(self, label='Images')
        self.wDPI = cWidget.StaticTextComboBox(
            self.wSbImg,
            label    = 'DPI',
            tooltip  = 'Set dpi value for images.',
            choices  = [str(x) for x in range(100, 550, 50)],
            setSizer = True,
        )
        self.wFormat = cWidget.StaticTextComboBox(
            self.wSbImg,
            label    = 'Format',
            tooltip  = 'Set default format for images.',
            choices  = mConfig.core.esMatPlotSaveI,
            setSizer = True,
        )
        #------------------------------> Color
        self.wSbColor = wx.StaticBox(self, label='Colors')
        self.wZebra = cWidget.StaticTextColor(
            parent    = self.wSbColor,
            stLabel   = 'Row',
            stTooltip = 'Non-white color for the rows in tables.',
            setSizer  = True,
        )
        self.wSbProt  = wx.StaticBox(
            self.wSbColor, label='Protein Representation')
        self.wProtRec = cWidget.StaticTextColor(
            parent    = self.wSbProt,
            stLabel   = 'Recombinant',
            stTooltip = ('Color for the recombinant sequence of a protein in '
                         'the fragments view.'),
            setSizer = True,
        )
        self.wProtNat = cWidget.StaticTextColor(
            parent    = self.wSbProt,
            stLabel   = 'Native',
            stTooltip = ('Color for the native sequence of a protein in '
                         'the fragments view.'),
            setSizer = True,
        )
        self.wSbFragment = wx.StaticBox(
            parent = self.wSbColor,
            label  = 'Experiments and Gel Spot'
        )
        self.wFrag = []
        for k in range(1, len(mConfig.core.cFragment)+1):
            self.wFrag.append(
                cWidget.StaticTextColor(
                    parent   = self.wSbColor,
                    stLabel  = str(k),
                    setSizer = True,
            ))
        self.wSbAA = wx.StaticBox(
            parent = self.wSbColor,
            label  = 'Amino acids groups'
        )
        self.wAA = {}
        for k in mConfig.core.lAAGroups:
            self.wAA[k[0]] = cWidget.StaticTextColor(
                parent   = self.wSbAA,
                stLabel  = ', '.join(k),
                setSizer = True,
            )
        #endregion --------------------------------------------------> Widgets

        #region ----------------------------------------------------> Tooltips
        self.wSbFragment.SetToolTip('These are the color used to color code '
            'fragments, gel spots, bars and lines in the result windows.')
        self.wSbAA.SetToolTip('Color code to group amino acids by type.')
        #endregion -------------------------------------------------> Tooltips

        #region ------------------------------------------------------> Sizers
        #------------------------------> Images
        self.sSbImgW = wx.BoxSizer(wx.HORIZONTAL)
        self.sSbImgW.Add(self.wDPI.Sizer,    0, wx.ALIGN_CENTER|wx.ALL, 5)
        self.sSbImgW.Add(self.wFormat.Sizer, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        #-->
        self.sSbImg = wx.StaticBoxSizer(self.wSbImg, wx.VERTICAL)
        self.sSbImg.Add(self.sSbImgW, 0, wx.ALIGN_CENTER|wx.ALL, 0)
        #------------------------------> Color
        #--> Fragments
        self.sSbFragmentW = wx.FlexGridSizer(5,1,1)
        for k in self.wFrag:
            self.sSbFragmentW.Add(k.Sizer, 0, wx.ALIGN_RIGHT|wx.ALL, 2)
        self.sSbFragment = wx.StaticBoxSizer(self.wSbFragment, wx.VERTICAL)
        self.sSbFragment.Add(self.sSbFragmentW, 0, wx.ALIGN_CENTER|wx.ALL, 0)
        #--> AA Groups
        self.sSbAAW = wx.FlexGridSizer(2,3,1,1)
        for k in self.wAA.values():
            self.sSbAAW.Add(k.Sizer, 0, wx.ALIGN_RIGHT|wx.ALL, 2)
        self.sSbAA = wx.StaticBoxSizer(self.wSbAA, wx.VERTICAL)
        self.sSbAA.Add(self.sSbAAW, 0, wx.ALIGN_CENTER|wx.ALL, 0)
        #--> Protein representation
        self.sSbProtW = wx.BoxSizer(wx.HORIZONTAL)
        self.sSbProtW.Add(self.wProtRec.Sizer, 0, wx.ALIGN_CENTER|wx.ALL, 0)
        self.sSbProtW.Add(self.wProtNat.Sizer, 0, wx.ALIGN_CENTER|wx.ALL, 0)
        self.sSbProt = wx.StaticBoxSizer(self.wSbProt, wx.VERTICAL)
        self.sSbProt.Add(self.sSbProtW, 0, wx.ALIGN_CENTER|wx.ALL, 0)
        #--> Main color wx.GridBagSizer
        self.sSbColorW = wx.BoxSizer(wx.VERTICAL)
        self.sSbColorW.Add(self.wZebra.Sizer, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        self.sSbColorW.Add(self.sSbProt,      0, wx.ALIGN_CENTER|wx.ALL, 5)
        self.sSbColorW.Add(self.sSbFragment,  0, wx.ALIGN_CENTER|wx.ALL, 5)
        self.sSbColorW.Add(self.sSbAA,        0, wx.ALIGN_CENTER|wx.ALL, 5)
        #-->
        self.sSbColor = wx.StaticBoxSizer(self.wSbColor, wx.VERTICAL)
        self.sSbColor.Add(self.sSbColorW, 0, wx.ALIGN_CENTER|wx.ALL, 0)
        #------------------------------>
        self.sSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.sSizer.Add(self.wUpdate,  0, wx.EXPAND|wx.ALL, 5)
        self.sSizer.Add(self.sSbColor, 0, wx.EXPAND|wx.ALL, 5)
        self.sSizer.Add(self.sSbImg,   0, wx.EXPAND|wx.ALL, 5)
        #-->
        self.SetSizer(self.sSizer)
        self.sSizer.Fit(self)
        self.SetupScrolling()
        #endregion ---------------------------------------------------> Sizers
    #---
    #endregion -----------------------------------------------> Instance setup
#---


class CorrA(scrolled.ScrolledPanel):
    """Panel for the CorrA Preferences window.

        Parameters
        ----------
        parent: wx.Window
            Parent of the pane.
    """
    #region -----------------------------------------------------> Class setup
    cName = mConfig.help.npCorrA
    #------------------------------>
    cLTab = mConfig.help.ntCorrA
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent):
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(parent, name=self.cName)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wSbMethod = wx.StaticBox(self, label='Correlation Analysis')
        self.wMethod = cWidget.StaticTextComboBox(
            self,
            label    = 'Default Method',
            tooltip  = 'Select the Correlation Method to use as default.',
            choices  = mConfig.corr.oCorrMethod,
            setSizer = True,
        )
        #------------------------------> Plot
        self.wSbRes = wx.StaticBox(self, label='Result Plot')
        self.wCol = cWidget.StaticTextComboBox(
            self.wSbRes,
            label   = 'Axis Label',
            choices = ['Names', 'Numbers'],
            tooltip = ('Use Column Names or Column Numbers for the labels '
                       'in the axis.'),
            setSizer = True,
        )
        self.wBar = cWidget.StaticTextComboBox(
            self.wSbRes,
            label    = 'Show Color Bar',
            choices  = ['False', 'True'],
            tooltip  = 'Show the color bar by default or hide it.',
            setSizer = True,
        )
        #------------------------------> Color
        self.wSbColor    = wx.StaticBox(self, label='Colors')
        self.wSbGradient = wx.StaticBox(self.wSbColor, label='Gradient')
        self.wC = []
        for x in ['-1', '0', '1']:
            self.wC.append(
                cWidget.StaticTextColor(
                    parent   = self.wSbGradient,
                    setSizer = True,
                    stLabel  = x,
            ))
        self.wC.append(
            cWidget.StaticTextColor(
                    parent   = self.wSbGradient,
                    setSizer = True,
                    stLabel  = 'NA',
        ))
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        self.sSbMethodW = wx.BoxSizer(wx.HORIZONTAL)
        self.sSbMethodW.Add(self.wMethod.Sizer, 0, wx.ALIGN_CENTER|wx.ALL, 0)
        #-->
        self.sSbMethod = wx.StaticBoxSizer(self.wSbMethod, wx.VERTICAL)
        self.sSbMethod.Add(self.sSbMethodW, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        #------------------------------>
        self.sSbGradientW = wx.BoxSizer(wx.HORIZONTAL)
        for k in self.wC:
            self.sSbGradientW.Add(k.Sizer, 0, wx.ALIGN_CENTER|wx.ALL, 0)
        self.sSbGradient = wx.StaticBoxSizer(self.wSbGradient, wx.VERTICAL)
        self.sSbGradient.Add(self.sSbGradientW, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        #-->
        self.sSbColor = wx.StaticBoxSizer(self.wSbColor, wx.VERTICAL)
        self.sSbColor.Add(self.sSbGradient, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        #------------------------------>
        self.sSbResW = wx.BoxSizer(wx.HORIZONTAL)
        self.sSbResW.Add(self.wCol.Sizer, 0, wx.ALIGN_CENTER|wx.ALL, 0)
        self.sSbResW.Add(self.wBar.Sizer, 0, wx.ALIGN_CENTER|wx.ALL, 0)
        #-->
        self.sSbRes = wx.StaticBoxSizer(self.wSbRes, wx.VERTICAL)
        self.sSbRes.Add(self.sSbResW, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        #------------------------------>
        self.sSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.sSizer.Add(self.sSbMethod, 0, wx.EXPAND|wx.ALL, 5)
        self.sSizer.Add(self.sSbColor,  0, wx.EXPAND|wx.ALL, 5)
        self.sSizer.Add(self.sSbRes,    0, wx.EXPAND|wx.ALL, 5)
        #-->
        self.SetSizer(self.sSizer)
        self.sSizer.Fit(self)
        self.SetupScrolling()
        #endregion ---------------------------------------------------> Sizers
    #---
    #endregion -----------------------------------------------> Instance setup
#---


class Data(scrolled.ScrolledPanel):
    """Panel for the Data Preferences window.

        Parameters
        ----------
        parent: wx.Window
            Parent of the pane.
    """
    #region -----------------------------------------------------> Class setup
    cName = mConfig.help.npData
    #------------------------------>
    cLTab = mConfig.help.ntData
    cLCeroTreat   = 'Treat 0s as Missing Values'
    cLNormMethod  = 'Normalization'
    cLTransMethod = 'Transformation'
    cLImputation  = 'Imputation'
    cLShift       = 'Shift'
    cLWidth       = 'Width'
    #------------------------------>
    cOCero       = list(mConfig.core.oYesNo.keys())
    cONorm       = list(mConfig.data.oNormMethod.keys())
    cOTrans      = list(mConfig.data.oTransMethod.keys())
    cOImputation = list(mConfig.data.oImputation.keys())
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent):
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(parent, name=self.cName)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wSbData = wx.StaticBox(
            self, label='Data Preparation Default Methods')
        self.wCeroB = cWidget.StaticTextComboBox(
            self.wSbData,
            label    = self.cLCeroTreat,
            choices  = self.cOCero,
            setSizer = True,
        )
        self.wNormMethod = cWidget.StaticTextComboBox(
            self.wSbData,
            label    = self.cLNormMethod,
            choices  = self.cONorm,
            setSizer = True,
        )
        self.wTransMethod = cWidget.StaticTextComboBox(
            self.wSbData,
            label    = self.cLTransMethod,
            choices  = self.cOTrans,
            setSizer = True,
        )
        self.wImpMethod = cWidget.StaticTextComboBox(
            self.wSbData,
            label    = self.cLImputation,
            choices  = self.cOImputation,
            setSizer = True,
        )
        #-->
        self.wSbImpOpt = wx.StaticBox(
            self.wSbData, label='Normal Distribution Imputation Options')
        self.wShift = cWidget.StaticTextCtrl(
            self.wSbImpOpt,
            stLabel   = self.cLShift,
            tcSize    = (60,22),
            tcHint    = 'e.g. 1.8',
            validator = cValidator.NumberList('float', nN=1, vMin=0),
            setSizer  = True,
        )
        self.wWidth = cWidget.StaticTextCtrl(
            self.wSbImpOpt,
            stLabel   = self.cLWidth,
            tcSize    = (60,22),
            validator = cValidator.NumberList('float', nN=1, vMin=0),
            tcHint    = 'e.g. 0.3',
            setSizer  = True,
        )
        #------------------------------> Color
        self.wSbColor    = wx.StaticBox(self, label='Colors')
        self.wPDF = cWidget.StaticTextColor(
            parent   = self.wSbColor,
            stLabel  = 'PDF',
            setSizer = True,
        )
        self.wBar = cWidget.StaticTextColor(
            parent   = self.wSbColor,
            stLabel  = 'Bars',
            setSizer = True,
        )
        self.wBarI = cWidget.StaticTextColor(
            parent   = self.wSbColor,
            stLabel  = 'Imputed Bars',
            setSizer = True,
        )
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        self.sSbMethodW = wx.BoxSizer(wx.HORIZONTAL)
        self.sSbMethodW.Add(self.wTransMethod.Sizer, 0, wx.ALIGN_CENTER|wx.ALL, 0)
        self.sSbMethodW.Add(self.wNormMethod.Sizer,  0, wx.ALIGN_CENTER|wx.ALL, 0)
        self.sSbMethodW.Add(self.wImpMethod.Sizer,   0, wx.ALIGN_CENTER|wx.ALL, 0)
        #-->
        self.sSbImpOptW = wx.BoxSizer(wx.HORIZONTAL)
        self.sSbImpOptW.Add(self.wShift.Sizer, 0, wx.ALIGN_CENTER|wx.ALL, 0)
        self.sSbImpOptW.Add(self.wWidth.Sizer, 0, wx.ALIGN_CENTER|wx.ALL, 0)
        self.sSbImpOpt = wx.StaticBoxSizer(self.wSbImpOpt, wx.VERTICAL)
        self.sSbImpOpt.Add(self.sSbImpOptW, 0, wx.ALIGN_CENTER|wx.ALL, 0)
        #-->
        self.sSbDataW = wx.BoxSizer(wx.VERTICAL)
        self.sSbDataW.Add(self.wCeroB.Sizer, 0, wx.ALIGN_CENTER|wx.ALL, 0)
        self.sSbDataW.Add(self.sSbMethodW,   0, wx.ALIGN_CENTER|wx.ALL, 0)
        self.sSbDataW.Add(self.sSbImpOpt,    0, wx.ALIGN_CENTER|wx.TOP, 10)
        #-->
        self.sSbData = wx.StaticBoxSizer(self.wSbData, wx.VERTICAL)
        self.sSbData.Add(self.sSbDataW, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        #------------------------------>
        self.sSbColorW = wx.BoxSizer(wx.HORIZONTAL)
        self.sSbColorW.Add(self.wBar.Sizer,  0, wx.ALIGN_CENTER|wx.ALL, 0)
        self.sSbColorW.Add(self.wBarI.Sizer, 0, wx.ALIGN_CENTER|wx.ALL, 0)
        self.sSbColorW.Add(self.wPDF.Sizer,  0, wx.ALIGN_CENTER|wx.ALL, 0)
        #-->
        self.sSbColor = wx.StaticBoxSizer(self.wSbColor, wx.VERTICAL)
        self.sSbColor.Add(self.sSbColorW, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        #------------------------------>
        self.sSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.sSizer.Add(self.sSbData,   0, wx.EXPAND|wx.ALL, 5)
        self.sSizer.Add(self.sSbColor,  0, wx.EXPAND|wx.ALL, 5)
        #-->
        self.SetSizer(self.sSizer)
        self.sSizer.Fit(self)
        self.SetupScrolling()
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------> Check Input Data
        self.rCheckUserInput = {
            f'{self.cLTab} - {self.cLShift}' : [self.wShift.wTc, mConfig.core.mOneRPlusNum],
            f'{self.cLTab} - {self.cLWidth}' : [self.wWidth.wTc, mConfig.core.mOneRPlusNum],
        }
        #endregion -----------------------------------------> Check Input Data
    #---
    #endregion -----------------------------------------------> Instance setup
#---


class LimProt(scrolled.ScrolledPanel):
    """Panel for the Limited Proteolysis window.

        Parameters
        ----------
        parent: wx.Window
            Parent of the pane.
    """
    #region -----------------------------------------------------> Class setup
    cName = mConfig.help.npLimProt
    #------------------------------> Labels
    cLTab      = mConfig.help.ntLimProt
    cLAlpha    = mConfig.core.lStAlpha
    cLBeta     = mConfig.core.lStBeta
    cLGamma    = mConfig.core.lStGamma
    cLTheta    = mConfig.core.lStTheta
    cLThetaMax = mConfig.core.lStThetaMax
    cLScoreVal = mConfig.core.lStScoreVal
    cLCorrectP = mConfig.core.lCbCorrectP
    #------------------------------> Hint
    cHBeta     = mConfig.limp.hBeta
    cHGamma    = mConfig.limp.hGamma
    cHTheta    = mConfig.limp.hTheta
    cHThetaMax = mConfig.limp.hThetaMax
    #------------------------------> Tooltips
    cTTScoreVal = mConfig.core.ttStScoreVal
    cTTAlpha    = 'Significance level for the statistical analysis.\ne.g. 0.05'
    cTTCorrectP = mConfig.core.ttStCorrectP
    cTTBeta     = mConfig.limp.ttBeta
    cTTGamma    = mConfig.limp.ttGamma
    cTTTheta    = mConfig.limp.ttTheta
    cTTThetaMax = mConfig.limp.ttThetaMax
    #------------------------------>
    cSTc = mConfig.core.sTcS
    #------------------------------>
    cOCorrectP = mConfig.core.oCorrectP
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent):
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(parent, name=self.cName)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wSbData = wx.StaticBox(
            self, label='Limited Proteolysis Analysis')
        self.wScoreVal = cWidget.StaticTextCtrl(
            self.wSbData,
            stLabel   = self.cLScoreVal,
            stTooltip = self.cTTScoreVal,
            tcSize    = self.cSTc,
            tcHint    = 'e.g. 320',
            setSizer  = True,
            validator = cValidator.NumberList(opt=True, numType='float', nN=1),
        )
        self.wCorrectP = cWidget.StaticTextComboBox(
            self.wSbData,
            label    = self.cLCorrectP,
            choices  = list(self.cOCorrectP.keys()),
            tooltip  = self.cTTCorrectP,
            setSizer = True,
        )
        self.wAlpha = cWidget.StaticTextCtrl(
            self.wSbData,
            stLabel   = self.cLAlpha,
            stTooltip = self.cTTAlpha,
            tcSize    = self.cSTc,
            tcHint    = 'e.g. 0.05',
            setSizer  = True,
            validator = cValidator.NumberList(
                opt=True, numType='float', nN=1, vMin=0, vMax=1),
        )
        self.wBeta = cWidget.StaticTextCtrl(
            self.wSbData,
            stLabel   = self.cLBeta,
            stTooltip = self.cTTBeta,
            tcSize    = self.cSTc,
            tcHint    = self.cHBeta,
            setSizer  = True,
            validator = cValidator.NumberList(
                opt=True, numType='float', nN=1, vMin=0, vMax=1),
        )
        self.wGamma = cWidget.StaticTextCtrl(
            self.wSbData,
            stLabel   = self.cLGamma,
            stTooltip = self.cTTGamma,
            tcSize    = self.cSTc,
            tcHint    = self.cHGamma,
            setSizer  = True,
            validator = cValidator.NumberList(
                opt=True, numType='float', nN=1, vMin=0, vMax=1),
        )
        self.wTheta = cWidget.StaticTextCtrl(
            self.wSbData,
            stLabel   = self.cLTheta,
            stTooltip = self.cTTTheta,
            tcSize    = self.cSTc,
            tcHint    = self.cHTheta,
            setSizer  = True,
            validator = cValidator.NumberList(
                opt=True, numType='float', nN=1, vMin=0, vMax=1),
        )
        self.wThetaMax = cWidget.StaticTextCtrl(
            self.wSbData,
            stLabel   = self.cLThetaMax,
            stTooltip = self.cTTThetaMax,
            tcSize    = self.cSTc,
            tcHint    = self.cHThetaMax,
            setSizer  = True,
            validator = cValidator.NumberList(
                opt=True, numType='float', nN=1, vMin=0, vMax=1),
        )
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        self.sSbDataW = wx.GridBagSizer(1,1)
        self.sSbDataW.Add(
            self.wScoreVal.Sizer,
            pos    = (0,0),
            flag   = wx.ALIGN_RIGHT|wx.ALL,
            border = 0,
        )
        self.sSbDataW.Add(
            self.wAlpha.Sizer,
            pos    = (1,0),
            flag   = wx.ALIGN_RIGHT|wx.ALL,
            border = 0,
        )
        self.sSbDataW.Add(
            self.wBeta.Sizer,
            pos    = (0,1),
            flag   = wx.ALIGN_RIGHT|wx.ALL,
            border = 0,
        )
        self.sSbDataW.Add(
            self.wGamma.Sizer,
            pos    = (1,1),
            flag   = wx.ALIGN_RIGHT|wx.ALL,
            border = 0,
        )
        self.sSbDataW.Add(
            self.wTheta.Sizer,
            pos    = (0,2),
            flag   = wx.ALIGN_RIGHT|wx.ALL,
            border = 0,
        )
        self.sSbDataW.Add(
            self.wThetaMax.Sizer,
            pos    = (1,2),
            flag   = wx.ALIGN_RIGHT|wx.ALL,
            border = 0,
        )
        self.sSbDataW.Add(
            self.wCorrectP.Sizer,
            pos    = (2,0),
            flag   = wx.ALIGN_CENTER|wx.ALL,
            border = 0,
            span   = (0, 3),
        )
        #-->
        self.sSbData = wx.StaticBoxSizer(self.wSbData, wx.VERTICAL)
        self.sSbData.Add(self.sSbDataW, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        #------------------------------>
        self.sSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.sSizer.Add(self.sSbData,  0, wx.EXPAND|wx.ALL, 5)
        #-->
        self.SetSizer(self.sSizer)
        self.sSizer.Fit(self)
        self.SetupScrolling()
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------> Check User Input
        self.rCheckUserInput = {
            f'{self.cLTab} - {self.cLScoreVal}': [self.wScoreVal.wTc, mConfig.core.mOneRealNum],
            f'{self.cLTab} - {self.cLAlpha}'   : [self.wAlpha.wTc,    mConfig.core.mOne01Num],
            f'{self.cLTab} - {self.cLBeta}'    : [self.wBeta.wTc,     mConfig.core.mOne01Num],
            f'{self.cLTab} - {self.cLGamma}'   : [self.wGamma.wTc,    mConfig.core.mOne01Num],
            f'{self.cLTab} - {self.cLTheta}'   : [self.wTheta.wTc,    mConfig.core.mOneRPlusNum],
            f'{self.cLTab} - {self.cLThetaMax}': [self.wThetaMax.wTc, mConfig.core.mOneRPlusNum],
        }
        #endregion -----------------------------------------> Check User Input

    #---
    #endregion -----------------------------------------------> Instance setup
#---


class ProtProf(scrolled.ScrolledPanel):
    """Panel for the Proteome Profile window.

        Parameters
        ----------
        parent: wx.Window
            Parent of the pane.
    """
    #region -----------------------------------------------------> Class setup
    cName      = mConfig.help.npProtProf
    cNLineNone = f'{mConfig.prot.lmFilterZScore} Line'
    cNLineHyp  = f'{mConfig.prot.lmFilterHypCurve} Line'
    cNLinePLog = f'{mConfig.prot.lmColorSchemePLog2} Line'
    #------------------------------>
    cLTab      = mConfig.help.ntProtProf
    cLAlpha    = mConfig.core.lStAlpha
    cLScoreVal = mConfig.core.lStScoreVal
    cLCorrectP = mConfig.core.lCbCorrectP
    cLT0       = mConfig.core.lStT0
    cLS0       = mConfig.core.lStS0
    cLP        = mConfig.core.lStP
    cLLog2FC   = mConfig.core.lStLog2FC
    cLZ        = mConfig.core.lStZScore
    #------------------------------>
    cTTScoreVal = mConfig.core.ttStScoreVal
    cTTAlpha    = 'Significance level for the statistical analysis.\ne.g. 0.05'
    cTTCorrectP = mConfig.core.ttStCorrectP
    #------------------------------>
    cSTc = mConfig.core.sTcS
    #------------------------------>
    cOCorrectP = mConfig.core.oCorrectP
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent):
        """ """
        #region -----------------------------------------------> Initial Setup
        self.rCheck = mConfig.prot.zShow
        #------------------------------>
        super().__init__(parent, name=self.cName)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wSbData = wx.StaticBox(
            self, label='Proteome Profiling Analysis')
        self.wAlpha = cWidget.StaticTextCtrl(
            self.wSbData,
            stLabel   = self.cLAlpha,
            stTooltip = self.cTTAlpha,
            tcSize    = self.cSTc,
            tcHint    = 'e.g. 0.05',
            setSizer  = True,
            validator = cValidator.NumberList(
                opt=True, numType='float', nN=1, vMin=0, vMax=1),
        )
        self.wCorrectP = cWidget.StaticTextComboBox(
            self.wSbData,
            label    = self.cLCorrectP,
            choices  = list(self.cOCorrectP.keys()),
            tooltip  = self.cTTCorrectP,
            setSizer = True,
        )
        self.wScoreVal = cWidget.StaticTextCtrl(
            self.wSbData,
            stLabel   = self.cLScoreVal,
            stTooltip = self.cTTScoreVal,
            tcSize    = self.cSTc,
            tcHint    = 'e.g. 320',
            setSizer  = True,
            validator = cValidator.NumberList(opt=True, numType='float', nN=1),
        )
        #------------------------------> Color
        self.wSbColor = wx.StaticBox(self,          label='Colors')
        self.wSbVol   = wx.StaticBox(self.wSbColor, label='Volcano Plot Data')
        self.wVolD = cWidget.StaticTextColor(
            self.wSbVol,
            stLabel  = 'Downregulated',
            setSizer = True,
        )
        self.wVolU = cWidget.StaticTextColor(
            self.wSbVol,
            stLabel  = 'Upregulated',
            setSizer = True,
        )
        self.wVolN = cWidget.StaticTextColor(
            self.wSbVol,
            stLabel  = 'Non Relevant',
            setSizer = True,
        )
        self.wVolS = cWidget.StaticTextColor(
            self.wSbVol,
            stLabel  = 'Selected',
            setSizer = True,
        )
        self.wVolT = cWidget.StaticTextColor(
            self.wSbVol,
            stLabel  = 'Thresholds',
            setSizer = True,
        )
        #------------------------------> Result Plot
        self.wSbRes = wx.StaticBox(self, label='Result Plots')
        self.wLock = cWidget.StaticTextComboBox(
            self.wSbRes,
            label    = 'Lock Plot Scale',
            choices  = [mConfig.prot.lmScaleNo,
                        mConfig.prot.lmScaleAnalysis,
                        mConfig.prot.lmScaleProject],
            setSizer = True,
        )
        self.wFilterA = cWidget.StaticTextComboBox(
            self.wSbRes,
            label    = 'Auto Apply Filters',
            choices  = list(mConfig.core.oYesNo.keys())[1:],
            setSizer = True,
        )
        self.wShowAll = cWidget.StaticTextComboBox(
            self.wSbRes,
            label    = 'Show Value Range',
            choices  = list(mConfig.core.oYesNo.keys())[1:],
            setSizer = True,
        )
        self.wPick = cWidget.StaticTextComboBox(
            self.wSbRes,
            label    = 'Left Click Action',
            choices  = ['Label', 'Select'],
            setSizer = True,
        )
        #-->
        self.wSbThreshold = wx.StaticBox(self.wSbRes, label='Threshold Parameters')
        self.wsbHC = wx.StaticBox(self.wSbThreshold, label='Hyperbolic Curve')
        self.wT0 = cWidget.StaticTextCtrl(
            self.wsbHC,
            stLabel   = self.cLT0,
            tcHint    = 'e.g. 1.0',
            tcSize    = self.cSTc,
            validator = cValidator.NumberList('float', vMin=0, nN=1),
            setSizer  = True,
        )
        self.wS0 = cWidget.StaticTextCtrl(
            self.wsbHC,
            stLabel   = self.cLS0,
            tcHint    = 'e.g. 0.1',
            tcSize    = self.cSTc,
            validator = cValidator.NumberList('float', vMin=0, nN=1),
            setSizer  = True,
        )
        self.wSbPFC = wx.StaticBox(self.wSbThreshold, label='P - Log2[FC]')
        self.wP = cWidget.StaticTextCtrl(
            self.wSbPFC,
            stLabel   = self.cLP,
            tcHint    = 'e.g. 0.05',
            tcSize    = self.cSTc,
            validator = cValidator.NumberList('float', vMin=0, nN=1),
            setSizer  = True,
        )
        self.wFC = cWidget.StaticTextCtrl(
            self.wSbPFC,
            stLabel   = self.cLLog2FC,
            tcHint    = 'e.g. 0.1',
            tcSize    = self.cSTc,
            validator = cValidator.NumberList('float', vMin=0, nN=1),
            setSizer  = True,
        )
        self.wSbZ = wx.StaticBox(self.wSbThreshold, label='Z Score')
        self.wZ = cWidget.StaticTextCtrl(
            self.wSbZ,
            stLabel   = self.cLZ,
            tcHint    = 'e.g. 10.0',
            tcSize    = self.cSTc,
            validator = cValidator.NumberList(
                    numType='float', vMin=0, vMax=100, nN=1),
        )
        self.wStShow = wx.StaticText(self.wSbZ, label='Show')
        self.wCbNone = wx.RadioButton(
            self.wSbZ, label='None', name=self.cNLineNone)
        self.wCbHyp  = wx.RadioButton(
            self.wSbZ, label='Hyperbolic Curve', name=self.cNLineHyp)
        self.wCbPLog = wx.RadioButton(
            self.wSbZ, label='P - Log2[FC] Lines', name=self.cNLinePLog)
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        self.sSbDataW = wx.BoxSizer(wx.HORIZONTAL)
        self.sSbDataW.Add(self.wScoreVal.Sizer, 0, wx.ALIGN_CENTER|wx.ALL, 0)
        self.sSbDataW.Add(self.wAlpha.Sizer,    0, wx.ALIGN_CENTER|wx.ALL, 0)
        self.sSbDataW.Add(self.wCorrectP.Sizer, 0, wx.ALIGN_CENTER|wx.ALL, 0)
        #-->
        self.sSbData = wx.StaticBoxSizer(self.wSbData, wx.VERTICAL)
        self.sSbData.Add(self.sSbDataW, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        #------------------------------>
        self.sSbVolW = wx.BoxSizer(wx.HORIZONTAL)
        self.sSbVolW.Add(self.wVolD.Sizer, 0, wx.ALIGN_CENTER|wx.ALL, 0)
        self.sSbVolW.Add(self.wVolN.Sizer, 0, wx.ALIGN_CENTER|wx.ALL, 0)
        self.sSbVolW.Add(self.wVolU.Sizer, 0, wx.ALIGN_CENTER|wx.ALL, 0)
        self.sSbVolW.Add(self.wVolS.Sizer, 0, wx.ALIGN_CENTER|wx.ALL, 0)
        self.sSbVolW.Add(self.wVolT.Sizer, 0, wx.ALIGN_CENTER|wx.ALL, 0)
        self.sSbVol = wx.StaticBoxSizer(self.wSbVol, wx.VERTICAL)
        self.sSbVol.Add(self.sSbVolW, 0, wx.ALIGN_CENTER|wx.ALL, 0)
        #-->
        self.sSbColor = wx.StaticBoxSizer(self.wSbColor, wx.VERTICAL)
        self.sSbColor.Add(self.sSbVol, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        #------------------------------>
        self.sGen = wx.FlexGridSizer(2,1,1)
        self.sGen.Add(self.wLock.Sizer,    0, wx.ALIGN_CENTER|wx.ALL, 0)
        self.sGen.Add(self.wShowAll.Sizer, 0, wx.ALIGN_CENTER|wx.ALL, 0)
        self.sGen.Add(self.wPick.Sizer,    0, wx.ALIGN_CENTER|wx.ALL, 0)
        self.sGen.Add(self.wFilterA.Sizer, 0, wx.ALIGN_CENTER|wx.ALL, 0)
        #-------------->
        self.sHC = wx.BoxSizer(wx.VERTICAL)
        self.sHC.Add(self.wT0.Sizer, 0, wx.ALIGN_RIGHT|wx.ALL, 0)
        self.sHC.Add(self.wS0.Sizer, 0, wx.ALIGN_RIGHT|wx.ALL, 0)
        self.sSbHC = wx.StaticBoxSizer(self.wsbHC, wx.VERTICAL)
        self.sSbHC.Add(self.sHC, 0, wx.ALIGN_CENTER|wx.ALL, 0)
        #-------------->
        self.sPFC = wx.BoxSizer(wx.VERTICAL)
        self.sPFC.Add(self.wP.Sizer,  0, wx.ALIGN_RIGHT|wx.ALL, 0)
        self.sPFC.Add(self.wFC.Sizer, 0, wx.ALIGN_RIGHT|wx.ALL, 0)
        self.sSbPFC = wx.StaticBoxSizer(self.wSbPFC, wx.VERTICAL)
        self.sSbPFC.Add(self.sPFC, 0, wx.ALIGN_CENTER|wx.ALL, 0)
        #-------------->
        self.sZ = wx.FlexGridSizer(4,2,1,1)
        self.sZ.Add(self.wZ.wSt,  0, wx.ALIGN_LEFT|wx.ALIGN_CENTER_HORIZONTAL|wx.TOP|wx.LEFT|wx.RIGHT, 5)
        self.sZ.Add(self.wZ.wTc,  0, wx.EXPAND|wx.BOTTOM|wx.LEFT|wx.RIGHT, 5)
        self.sZ.Add(self.wStShow, 0, wx.ALIGN_LEFT|wx.TOP|wx.LEFT|wx.RIGHT, 5)
        self.sZ.Add(self.wCbNone, 0, wx.ALIGN_LEFT|wx.TOP|wx.LEFT|wx.RIGHT, 5)
        self.sZ.AddSpacer(0)
        self.sZ.Add(self.wCbHyp, 0, wx.ALIGN_LEFT|wx.TOP|wx.LEFT|wx.RIGHT, 5)
        self.sZ.AddSpacer(0)
        self.sZ.Add(self.wCbPLog, 0, wx.ALIGN_LEFT|wx.TOP|wx.LEFT|wx.RIGHT, 5)
        self.sSbZ = wx.StaticBoxSizer(self.wSbZ, wx.VERTICAL)
        self.sSbZ.Add(self.sZ, 0, wx.ALIGN_CENTER|wx.ALL, 0)
        #-------------->
        self.sThreshold = wx.BoxSizer(wx.HORIZONTAL)
        self.sThreshold.Add(self.sSbHC,  0, wx.ALIGN_TOP|wx.RIGHT, 10)
        self.sThreshold.Add(self.sSbPFC, 0, wx.ALIGN_TOP|wx.RIGHT, 10)
        self.sThreshold.Add(self.sSbZ,   0, wx.ALIGN_TOP|wx.RIGHT, 0)
        self.sSbThreshold = wx.StaticBoxSizer(self.wSbThreshold, wx.VERTICAL)
        self.sSbThreshold.Add(self.sThreshold, 0, wx.ALIGN_CENTER|wx.ALL, 0)
        #-------------->
        self.sSbRes = wx.StaticBoxSizer(self.wSbRes, wx.VERTICAL)
        self.sSbRes.Add(self.sGen,         0, wx.ALIGN_CENTER|wx.ALL, 0)
        self.sSbRes.Add(self.sSbThreshold, 0, wx.ALIGN_CENTER|wx.ALL, 10)
        #------------------------------>
        self.sSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.sSizer.Add(self.sSbData,  0, wx.EXPAND|wx.ALL, 5)
        self.sSizer.Add(self.sSbColor, 0, wx.EXPAND|wx.ALL, 5)
        self.sSizer.Add(self.sSbRes,   0, wx.EXPAND|wx.ALL, 5)
        #-->
        self.SetSizer(self.sSizer)
        self.sSizer.Fit(self)
        self.SetupScrolling()
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_RADIOBUTTON, self.OnCheckChange)
        #endregion -----------------------------------------------------> Bind

        #region --------------------------------------------> Check User Input
        self.rCheckUserInput = {
            f'{self.cLTab} - {self.cLAlpha}'    : [self.wAlpha.wTc,    mConfig.core.mOne01Num],
            f'{self.cLTab} - {self.cLScoreVal}' : [self.wScoreVal.wTc, mConfig.core.mOneRealNum],
            f'{self.cLTab} - {self.cLT0}'       : [self.wT0.wTc,       mConfig.core.mOneRPlusNum],
            f'{self.cLTab} - {self.cLS0}'       : [self.wS0.wTc,       mConfig.core.mOneRPlusNum],
            f'{self.cLTab} - {self.cLP}'        : [self.wP.wTc ,       mConfig.core.mOne01Num],
            f'{self.cLTab} - {self.cLLog2FC}'   : [self.wFC.wTc,       mConfig.core.mOneRPlusNum],
            f'{self.cLTab} - {self.cLZ}'        : [self.wZ.wTc ,       mConfig.core.mOne0100Num],
        }
        #endregion -----------------------------------------> Check User Input

    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Event Methods
    def OnCheckChange(self, event:wx.CommandEvent) -> bool:
        """Update Selected Radio Button

            Parameters
            ----------
            event: wx.Event
                Information about the event.

            Returns
            -------
            bool
        """
        self.rCheck = event.GetEventObject().GetName()
        return True
    #---
    #endregion ------------------------------------------------> Event Methods
#---


class TarProt(scrolled.ScrolledPanel):
    """Panel for the Targeted Proteolysis Preferences window.

        Parameters
        ----------
        parent: wx.Window
            Parent of the pane.
    """
    #region -----------------------------------------------------> Class setup
    cName = mConfig.help.npTarProt
    #------------------------------>
    cLTab      = mConfig.help.ntTarProt
    cLAlpha    = mConfig.core.lStAlpha
    cLScoreVal = mConfig.core.lStScoreVal
    cLAA       = mConfig.core.lStAAPos
    cLHist     = mConfig.core.lStHistWind
    cLCorrectP = mConfig.core.lCbCorrectP
    #------------------------------>
    cTTScoreVal = mConfig.core.ttStScoreVal
    cTTAlpha    = 'Significance level for the statistical analysis.\ne.g. 0.05'
    cTTCorrectP = mConfig.core.ttStCorrectP
    cTTAA       = mConfig.core.ttAAPos
    cTTHist     = mConfig.core.ttHist
    #------------------------------>
    cSTc = mConfig.core.sTcS
    #------------------------------>
    cOCorrectP = mConfig.core.oCorrectP
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent):
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(parent, name=self.cName)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wSbData = wx.StaticBox(
            self, label='Targeted Proteolysis Analysis')
        self.wScoreVal = cWidget.StaticTextCtrl(
            self.wSbData,
            stLabel   = self.cLScoreVal,
            stTooltip = self.cTTScoreVal,
            tcSize    = self.cSTc,
            tcHint    = 'e.g. 320',
            setSizer  = True,
            validator = cValidator.NumberList(opt=True, numType='float', nN=1),
        )
        self.wCorrectP = cWidget.StaticTextComboBox(
            self.wSbData,
            label    = self.cLCorrectP,
            choices  = list(self.cOCorrectP.keys()),
            tooltip  = self.cTTCorrectP,
            setSizer = True,
        )
        self.wAlpha = cWidget.StaticTextCtrl(
            self.wSbData,
            stLabel   = self.cLAlpha,
            stTooltip = self.cTTAlpha,
            tcSize    = self.cSTc,
            tcHint    = 'e.g. 0.05',
            setSizer  = True,
            validator = cValidator.NumberList(
                opt=True, numType='float', nN=1, vMin=0, vMax=1),
        )
        self.wAA = cWidget.StaticTextCtrl(
            self.wSbData,
            stLabel   = self.cLAA,
            stTooltip = self.cTTAA,
            tcSize    = self.cSTc,
            tcHint    = 'e.g. 5',
            setSizer  = True,
            validator = cValidator.NumberList(
                numType='int', nN=1, vMin=0, opt=True),
        )
        self.wHist = cWidget.StaticTextCtrl(
            self.wSbData,
            stLabel   = self.cLHist,
            stTooltip = self.cTTHist,
            tcSize    = self.cSTc,
            tcHint    = 'e.g. 50',
            setSizer  = True,
            validator = cValidator.NumberList(
                numType='int', vMin=0, sep=' ', opt=True),
        )
        #------------------------------> Color
        self.wSbColor = wx.StaticBox(self, label='Colors')
        self.wCtrl = cWidget.StaticTextColor(
            self.wSbColor,
            stLabel  = 'Control Points',
            setSizer = True,
        )
        self.wAve = cWidget.StaticTextColor(
            self.wSbColor,
            stLabel  = 'Average Intensity',
            setSizer = True,
        )
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        self.sSbDataW = wx.GridBagSizer(1,1)
        self.sSbDataW.Add(
            self.wScoreVal.Sizer,
            pos    = (0,0),
            flag   = wx.ALIGN_RIGHT|wx.ALL,
            border = 0,
        )
        self.sSbDataW.Add(
            self.wAlpha.Sizer,
            pos    = (1,0),
            flag   = wx.ALIGN_RIGHT|wx.ALL,
            border = 0,
        )
        self.sSbDataW.Add(
            self.wAA.Sizer,
            pos    = (0,1),
            flag   = wx.ALIGN_RIGHT|wx.ALL,
            border = 0,
        )
        self.sSbDataW.Add(
            self.wHist.Sizer,
            pos    = (1,1),
            flag   = wx.ALIGN_RIGHT|wx.ALL,
            border = 0,
        )
        self.sSbDataW.Add(
            self.wCorrectP.Sizer,
            pos    = (2,0),
            flag   = wx.ALIGN_CENTER|wx.ALL,
            border = 0,
            span   = (0, 2),
        )
        #-->
        self.sSbData = wx.StaticBoxSizer(self.wSbData, wx.VERTICAL)
        self.sSbData.Add(self.sSbDataW, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        #------------------------------>
        self.sSbColorW = wx.BoxSizer(wx.HORIZONTAL)
        self.sSbColorW.Add(self.wCtrl.Sizer, 0, wx.ALIGN_CENTER|wx.ALL, 0)
        self.sSbColorW.Add(self.wAve.Sizer,  0, wx.ALIGN_CENTER|wx.ALL, 0)
        #-->
        self.sSbColor = wx.StaticBoxSizer(self.wSbColor, wx.VERTICAL)
        self.sSbColor.Add(self.sSbColorW, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        #------------------------------>
        self.sSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.sSizer.Add(self.sSbData,   0, wx.EXPAND|wx.ALL, 5)
        self.sSizer.Add(self.sSbColor,  0, wx.EXPAND|wx.ALL, 5)
        #-->
        self.SetSizer(self.sSizer)
        self.sSizer.Fit(self)
        self.SetupScrolling()
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------> Check Input Data
        self.rCheckUserInput = {
            f'{self.cLTab} - {self.cLScoreVal}': [self.wScoreVal.wTc, mConfig.core.mOneRealNum],
            f'{self.cLTab} - {self.cLAlpha}'   : [self.wAlpha.wTc,    mConfig.core.mOne01Num],
            f'{self.cLTab} - {self.cLAA}'      : [self.wAA.wTc,       mConfig.core.mOneZPlusNum],
            f'{self.cLTab} - {self.cLHist}'    : [self.wHist.wTc,     mConfig.core.mValueBad],
        }
        #endregion -----------------------------------------> Check Input Data
    #---
    #endregion -----------------------------------------------> Instance setup
#---
#endregion ----------------------------------------------------------> Classes
