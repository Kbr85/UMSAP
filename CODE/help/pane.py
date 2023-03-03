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
            'fragments, gel spots and bars in the result windows.')
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
        self.wSbImpOpt = wx.StaticBox(self.wSbData, label='Imputation Options')
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
    #---
    #endregion -----------------------------------------------> Instance setup
#---
#endregion ----------------------------------------------------------> Classes
