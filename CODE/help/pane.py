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
from core import widget as cWidget
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Classes
class PrefGeneral(scrolled.ScrolledPanel):
    """Panel for the Preferences window.

        Parameters
        ----------
        parent: wx.Window
            Parent of the pane.
    """
    #region -----------------------------------------------------> Class setup
    cName = mConfig.help.npPrefGeneral
    #------------------------------>
    cLTab = mConfig.help.ntPrefGeneral
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
        self.sSbAA.Add(self.sSbAAW, 0, wx.VERTICAL|wx.ALL, 0)
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
#endregion ----------------------------------------------------------> Classes
