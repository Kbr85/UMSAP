# ------------------------------------------------------------------------------
# Copyright (C) 2017 Kenny Bravo Rodriguez <www.umsap.nl>
#
# Author: Kenny Bravo Rodriguez (kenny.bravorodriguez@mpi-dortmund.mpg.de)
#
# This program is distributed for free in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See the accompaning licence for more details.
# ------------------------------------------------------------------------------


""" Tabs of the application"""


#region -------------------------------------------------------------> Imports
from typing import Optional

import wx
import wx.lib.agw.aui as aui

# import dat4s_core.data.method as dtsMethod

import config.config as config
import gui.dtscore as dtscore
import gui.pane as pane

# if config.typeCheck:
#     from pathlib import Path
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Methods

#endregion ----------------------------------------------------------> Methods


#region --------------------------------------------------------> Base Classes
class BaseConfTab(wx.Panel):
    """Base class for a Tab containing only a configuration panel. 

        Parameters
        ----------
        cParent : wx.Window
            Parent of the tab
        cName : str or None
            Unique name of the tab. Default is None. In this case the child 
            class is expected to define a name
        cDataI : dict or None
            Initial data provided by the user to performed a previous analysis.

        Attributes
        ----------
        clPaneConf : str
            Title for the configuration panel. Default is config.lnPaneConf.
        cName : str
            Name of the tab
        cParent : wx.Window
            Parent of the tab
        dConfPanel : dict
            Classes to create the configuration panel in the Tab. Keys are
            config.ntNAMES and values the corresponding method.
        wConf : pane.X
            Configuration panel to show in the tab.
    """
    #region -----------------------------------------------------> Class setup
    dConfPanel = {
        config.ntCorrA   : pane.CorrA,
        config.ntDataPrep: pane.DataPrep,
        # config.ntLimProt : pane.LimProt,
        config.ntProtProf: pane.ProtProf,
    }
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self, cParent: wx.Window, cName: Optional[str]=None, 
        cDataI: Optional[dict]=None) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.cParent = cParent
        self.cName = cName if cName is not None else self.cName
        self.clPaneConf = getattr(self, 'clPaneConf', config.lnPaneConf)
        #------------------------------> 
        super().__init__(cParent, name=self.cName)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wConf = self.dConfPanel[self.cName](self, cDataI)
        #endregion --------------------------------------------------> Widgets
        
        #region -------------------------------------------------> Aui control
        #------------------------------> AUI control
        self._mgr = aui.AuiManager()
        #------------------------------> AUI which frame to use
        self._mgr.SetManagedWindow(self)
        #------------------------------> Add Configuration panel
        self._mgr.AddPane( 
            self.wConf, 
            aui.AuiPaneInfo(
                ).Center(
                ).Caption(
                    self.clPaneConf
                ).Floatable(
                    b=False
                ).CloseButton(
                    visible=False
                ).Movable(
                    b=False
                ).PaneBorder(
                    visible=True,
            ),
        )
        #------------------------------> 
        self._mgr.Update()
        #endregion ----------------------------------------------> Aui control
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    
    #endregion ------------------------------------------------> Class methods
#---


class BaseConfListTab(BaseConfTab):
    """Base class for a Tab containing a configuration panel and a right list
        panel. 

        Parameters
        ----------
        cParent : wx.Window
            Parent of the tab 
        cName : str or None
            Unique name of the tab.
        cDataI : dict or None
            Initial data provided by the user to performed a previous analysis

        Attributes
        ----------
        cLCColLabel : list of str
            Labels for the columns in the wx.ListCtrl.
            Default is config.lLCtrlColNameI.
        cLCColSize : list of int
            Size of the columns in the wx.ListCtrl. It should match cLCColLabel
            Default is config.sLCtrlColI.
        cLCPaneTitle : str
            Title of the pane containing the wx.ListCtrl.
            Default is config.lnListPane.
    """
    #region -----------------------------------------------------> Class setup
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self, cParent: wx.Window, cName: Optional[str]=None,
        cDataI : Optional[dict]=None) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.cLCColLabel  = getattr(self, 'cLCColLabel',  config.lLCtrlColNameI)
        self.cLCColSize   = getattr(self, 'cLCColSize',   config.sLCtrlColI)
        self.cLCPaneTitle = getattr(self, 'cLCPaneTitle', config.lnListPane)
        
        super().__init__(cParent, cName=cName, cDataI=cDataI)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wLCtrl = dtscore.ListZebraMaxWidth(
            self, colLabel=self.cLCColLabel, colSize=self.cLCColSize)
        #----------------------------> Pointer to lc to load data file content
        self.wConf.wLCtrlI = self.wLCtrl
        self.wConf.rLCtrlL = [self.wLCtrl]
        #endregion --------------------------------------------------> Widgets
        
        #region -------------------------------------------------> Aui control
        self._mgr.AddPane(
            self.wLCtrl, 
            aui.AuiPaneInfo(
                ).Right(
                ).Caption(
                    self.cLCPaneTitle
                ).Floatable(
                    b=False
                ).CloseButton(
                    visible=False
                ).Movable(
                    b=False
                ).PaneBorder(
                    visible=True,
            ),
        )
        #------------------------------> 
        self._mgr.Update()
        #endregion ----------------------------------------------> Aui control
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    
    #endregion ------------------------------------------------> Class methods
#---


# class ResControlExp(wx.Panel):
#     """Creates the panel containig the panes for the dialog Results - Control
#         Experiments

#         Parameters
#         ----------
#         parent : wx.Widget
#             Parent of the panel
#         iFile : Path
#             Path to the Data File already selected in the parent window
#         topParent : wx.Widget
#             Window calling the dialog.

#         Attributes
#         ----------
#         name : str
#             Unique name of the panel
#         widget : ditc of methods
#             Methods to create the configuration panel
#         conf : pane
#             Configuration panel to show in the window.
#         lc : wx.ListCtrl
#             List with the column numbers in iFile.
#     """
#     #region -----------------------------------------------------> Class setup
#     name = 'ResControlExpPane'

#     widget = {
#         config.npProtProf : pane.ProtProfResControlExp,
#         config.npLimProt  : pane.LimProtResControlExp,
#     }
#     #endregion --------------------------------------------------> Class setup

#     #region --------------------------------------------------> Instance setup
#     def __init__(
#         self, parent: 'wx.Window', iFile: 'Path', topParent: 'wx.Window',
#         ) -> None:
#         """ """
#         #region -------------------------------------------------> Check Input
        
#         #endregion ----------------------------------------------> Check Input

#         #region -----------------------------------------------> Initial Setup
#         super().__init__(parent, name=self.name)
#         #endregion --------------------------------------------> Initial Setup

#         #region --------------------------------------------------------> Menu
        
#         #endregion -----------------------------------------------------> Menu

#         #region -----------------------------------------------------> Widgets
#         #------------------------------> ListCtrl and fill it
#         self.lc = dtscore.ListZebraMaxWidth(
#             self, 
#             colLabel = config.lLCtrlColNameI,
#             colSize  = config.sLCtrlColI,
#         )
#         dtsMethod.LCtrlFillColNames(self.lc, iFile)
#         #------------------------------> Conf panel here to read NRow in lc
#         self.conf = self.widget[topParent.name](
#             self, topParent, self.lc.GetItemCount(),
#         )
#         #endregion --------------------------------------------------> Widgets

#         #region -------------------------------------------------> Aui control
#         #------------------------------> AUI control
#         self._mgr = aui.AuiManager()
#         #------------------------------> AUI which frame to use
#         self._mgr.SetManagedWindow(self)
#         #------------------------------> Add Configuration panel
#         self._mgr.AddPane( 
#             self.conf, 
#             aui.AuiPaneInfo(
#                 ).Center(
#                 ).Caption(
#                     config.lnPaneConf
#                 ).Floatable(
#                     b=False
#                 ).CloseButton(
#                     visible=False
#                 ).Movable(
#                     b=False
#                 ).PaneBorder(
#                     visible=True,
#             ),
#         )

#         self._mgr.AddPane(
#             self.lc, 
#             aui.AuiPaneInfo(
#                 ).Right(
#                 ).Caption(
#                     config.lnListPane
#                 ).Floatable(
#                     b=False
#                 ).CloseButton(
#                     visible=False
#                 ).Movable(
#                     b=False
#                 ).PaneBorder(
#                     visible=True,
#             ),
#         )

#         self._mgr.Update()
#         #endregion ----------------------------------------------> Aui control

#         #region --------------------------------------------------------> Bind
        
#         #endregion -----------------------------------------------------> Bind

#         #region ---------------------------------------------> Window position
        
#         #endregion ------------------------------------------> Window position
#     #---
#     #endregion -----------------------------------------------> Instance setup

#     #region ---------------------------------------------------> Class methods
    
#     #endregion ------------------------------------------------> Class methods
# #---
#endregion -----------------------------------------------------> Base Classes


#region -------------------------------------------------------------> Classes
class Start(wx.Panel):
    """Start tab
    
        Parameters
        ----------
        cParent : wx.Window
            Direct parent of the widgets in the tab.
        args : extra arguments

        Attributes
        ----------
        cImg: str
            Path to the image.
        cName: str
            Name of the tab. Unique name for the application
        cParent: wx.Window
            Parent of the tab.
    """
    #region -----------------------------------------------------> Class setup
    cName = config.ntStart
    #------------------------------> Files
    cImg = config.fImgStart
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, cParent: wx.Window, *args, **kwargs) -> None:
        """"""
        #region -----------------------------------------------> Initial setup
        self.cParent = cParent
        
        super().__init__(parent=cParent, name=self.cName)
        #endregion --------------------------------------------> Initial setup
        
        #region -----------------------------------------------------> Widgets
        #------------------------------>  Images
        self.wImg = wx.StaticBitmap(
            self,bitmap=wx.Bitmap(str(self.cImg), wx.BITMAP_TYPE_ANY))
        #------------------------------> Buttons
        self.wBtnCorrA    = wx.Button(self, label=config.nuCorrA)
        self.wBtnDataPrep = wx.Button(self, label=config.nuDataPrep)
        self.wBtnLimProt  = wx.Button(self, label=config.nmLimProt)
        self.wBtnProtProf = wx.Button(self, label=config.nmProtProf)
        self.wBtnTarProt  = wx.Button(self, label=config.nmTarProt)
        #endregion --------------------------------------------------> Widgets

        #region ----------------------------------------------------> Tooltips
        self.wBtnDataPrep.SetToolTip(config.ttBtnDataPrep)
        self.wBtnCorrA.SetToolTip   (config.ttBtnCorrA)
        self.wBtnLimProt.SetToolTip (config.ttBtnLimProt)
        self.wBtnProtProf.SetToolTip(config.ttBtnProtProf)
        self.wBtnTarProt.SetToolTip (config.ttBtnTarProt)
        #endregion -------------------------------------------------> Tooltips
        
        #region ------------------------------------------------------> Sizers
        #------------------------------> Sizers
        self.sSizer	 = wx.BoxSizer(wx.VERTICAL)
        self.sGrid = wx.GridBagSizer(1,1)
        self.sBtn  = wx.BoxSizer(wx.VERTICAL)
        #------------------------------>  Add widgets
        #--------------> Buttons
        self.sBtn.Add(self.wBtnCorrA, 0, wx.EXPAND|wx.ALL, 5)
        self.sBtn.Add(self.wBtnDataPrep, 0, wx.EXPAND|wx.ALL, 5)
        self.sBtn.Add(self.wBtnLimProt, 0, wx.EXPAND|wx.ALL, 5)
        self.sBtn.Add(self.wBtnProtProf, 0, wx.EXPAND|wx.ALL, 5)
        self.sBtn.Add(self.wBtnTarProt, 0, wx.EXPAND|wx.ALL, 5)
        #--------------> GridSizer
        self.sGrid.Add(
            self.wImg, 
            pos	= (0,0),
            flag   = wx.EXPAND|wx.RIGHT,
            border = 25,
        )
        self.sGrid.Add(
            self.sBtn, 
            pos	= (0,1),
            flag   = wx.ALIGN_CENTRE_VERTICAL|wx.LEFT,
            border = 25,
        )
        #--------------> Main Sizer
        self.sSizer.AddStretchSpacer(1)
        self.sSizer.Add(self.sGrid, 0, wx.CENTER|wx.ALL, 5)
        self.sSizer.AddStretchSpacer(1)
        self.SetSizer(self.sSizer)
        self.sSizer.Fit(self)
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind
        self.wBtnCorrA.Bind(
            wx.EVT_BUTTON, 
            lambda event: config.winMain.OnCreateTab(config.ntCorrA)
        )
        self.wBtnDataPrep.Bind(
            wx.EVT_BUTTON, 
            lambda event: config.winMain.OnCreateTab(config.ntDataPrep)
        )
#         self.btnLimProt.Bind(
#             wx.EVT_BUTTON, 
#             lambda event: config.winMain.CreateTab(config.ntLimProt)
#         )
        self.wBtnProtProf.Bind(
            wx.EVT_BUTTON, 
            lambda event: config.winMain.OnCreateTab(config.ntProtProf)
        )
        #endregion -----------------------------------------------------> Bind
    #endregion -----------------------------------------------> Instance setup
#---
#endregion ----------------------------------------------------------> Classes
