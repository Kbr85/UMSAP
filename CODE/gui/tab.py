# # ------------------------------------------------------------------------------
# # Copyright (C) 2017 Kenny Bravo Rodriguez <www.umsap.nl>
# #
# # Author: Kenny Bravo Rodriguez (kenny.bravorodriguez@mpi-dortmund.mpg.de)
# #
# # This program is distributed for free in the hope that it will be useful,
# # but WITHOUT ANY WARRANTY; without even the implied warranty of
# # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# #
# # See the accompaning licence for more details.
# # ------------------------------------------------------------------------------


# """ Tabs of the application"""


# #region -------------------------------------------------------------> Imports
# from typing import Optional

# import wx
# import wx.lib.agw.aui as aui

# import dat4s_core.data.method as dtsMethod

# import config.config as config
# import gui.dtscore as dtscore
# import gui.pane as pane

# if config.typeCheck:
#     from pathlib import Path
# #endregion ----------------------------------------------------------> Imports


# #region -------------------------------------------------------------> Methods

# #endregion ----------------------------------------------------------> Methods


# #region --------------------------------------------------------> Base Classes
# class BaseConfTab(wx.Panel):
#     """Base class for a Tab containing only a configuration panel. 

#         Parameters
#         ----------
#         parent : wx.Window
#             Parent of the tab
#         name : str or None
#             Unique name of the tab. Default is None. In this case the child 
#             class is expected to define a name
#         dataI : dict or None
#             Initial data provided by the user to performed a previous analysis.

#         Attributes
#         ----------
#         cConfPanel : dict
#             Classes to create the configuration panel in the Tab. Keys are
#             config.ntNAMES and values the corresponding method.
#         cnPaneConf : str
#             Title for the configuration panel. 
#             Default is config.lnPaneConf.
#         conf : pane.X
#             Configuration panel to show in the tab.
#         name : str
#             Name of the tab
#         parent : wx.Window
#             Parent of the tab
#     """
#     #region -----------------------------------------------------> Class setup
#     cConfPanel = {
#         config.ntCorrA   : pane.CorrA,
#         config.ntDataPrep: pane.DataPrep,
#         config.ntLimProt : pane.LimProt,
#         config.ntProtProf: pane.ProtProf,
#     }
#     #endregion --------------------------------------------------> Class setup

#     #region --------------------------------------------------> Instance setup
#     def __init__(
#         self, parent: wx.Window, name: Optional[str]=None, 
#         dataI: Optional[dict]=None) -> None:
#         """ """
#         #region -----------------------------------------------> Initial Setup
#         self.parent = parent
#         self.name = name if name is not None else self.name
        
#         self.cnPaneConf = getattr(self, 'cnPaneConf', config.lnPaneConf)
        
#         super().__init__(parent, name=self.name)
#         #endregion --------------------------------------------> Initial Setup

#         #region -----------------------------------------------------> Widgets
#         self.conf = self.cConfPanel[self.name](self, dataI)
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
#                     self.cnPaneConf
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
#         #------------------------------> 
#         self._mgr.Update()
#         #endregion ----------------------------------------------> Aui control
#     #---
#     #endregion -----------------------------------------------> Instance setup

#     #region ---------------------------------------------------> Class methods
    
#     #endregion ------------------------------------------------> Class methods
# #---


# class BaseConfListTab(BaseConfTab):
#     """Base class for a Tab containing a configuration panel and a right list
#         panel. 

#         Parameters
#         ----------
#         parent : wx.Window
#             Parent of the tab 
#         name : str or None
#             Unique name of the tab.
#         dataI : dict or None
#             Initial data provided by the user to performed a previous analysis

#         Attributes
#         ----------
#         cLCColLabel : list of str
#             Labels for the columns in the wx.ListCtrl.
#             Default is config.lLCtrlColNameI.
#         cLCColSize : list of int
#             Size of the columns in the wx.ListCtrl. It should match cLCColLabel
#             Default is config.sLCtrlColI.
#         cLCPaneTitle : str
#             Title of the pane containing the wx.ListCtrl.
#             Default is config.lnListPane.
#     """
#     #region -----------------------------------------------------> Class setup
#     #endregion --------------------------------------------------> Class setup

#     #region --------------------------------------------------> Instance setup
#     def __init__(
#         self, parent: wx.Window, name: Optional[str]=None,
#         dataI : Optional[dict]=None) -> None:
#         """ """
#         #region -----------------------------------------------> Initial Setup
#         self.cLCColLabel = getattr(self, 'cLCColLabel', config.lLCtrlColNameI)
#         self.cLCColSize = getattr(self, 'cLCColSize', config.sLCtrlColI)
#         self.cLCPaneTitle = getattr(self, 'cLCPaneTitle', config.lnListPane)
        
#         super().__init__(parent, name=name, dataI=dataI)
#         #endregion --------------------------------------------> Initial Setup

#         #region -----------------------------------------------------> Widgets
#         self.lc = dtscore.ListZebraMaxWidth(
#             self, colLabel=self.cLCColLabel, colSize=self.cLCColSize,
#         )
#         #----------------------------> Pointer to lc to load data file content
#         self.conf.lbI = self.lc
#         self.conf.lbL = [self.lc]
#         #endregion --------------------------------------------------> Widgets
        
#         #region -------------------------------------------------> Aui control
#         self._mgr.AddPane(
#             self.lc, 
#             aui.AuiPaneInfo(
#                 ).Right(
#                 ).Caption(
#                     self.cLCPaneTitle
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
#         #------------------------------> 
#         self._mgr.Update()
#         #endregion ----------------------------------------------> Aui control
#     #---
#     #endregion -----------------------------------------------> Instance setup

#     #region ---------------------------------------------------> Class methods
    
#     #endregion ------------------------------------------------> Class methods
# #---


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
# #endregion -----------------------------------------------------> Base Classes


# #region -------------------------------------------------------------> Classes
# class Start(wx.Panel):
#     """Start tab
    
#         Parameters
#         ----------
#         parent : wx.Window
#             Direct parent of the widgets in the tab.
#         statusbar : wx.SatusBar
#             Statusbar to display info
#         args : extra arguments

#         Attributes
#         ----------
#         parent : wx widget
#             Parent of the tab. 
#         name : str
#             Name of the tab. Unique name for the application
#         btnDataPrep : wx.Button
#             Launch the Data Preparation utility.
#         btnCorrA : wx.Button
#             Launch the Correlation Analysis utility.
#         btnLimProt : wx.Button
#             Launch the Limited Proteolysis module.
#         btnProtProf : wx.Button
#             Launch the Proteome profiling module.
#         btnTarProt : wx.Button
#             Launch the Targeted Proteolysis module.
#         Sizer : wx.BoxSizer
#             Main sizer of the app
#         SizerGrid : wx.GridBagSizer
#             Sizer to hold the widgets
#         Sizerbtn : wx.BoxSizer
#             Sizer for the buttons
#     """
#     #region -----------------------------------------------------> Class setup
#     name = config.ntStart
#     #------------------------------> Tooltips
#     cTTBtnDataPrep = f"Start the utility {config.nuDataPrep}"
#     cTTBtnCorrA    = f"Start the utility {config.nuCorrA}"
#     cTTBtnLimProt  = f"Start the module {config.nmLimProt}"
#     cTTBtnTarProt  = f"Start the module {config.nmTarProt}"
#     cTTBtnProtProf = f"Start the module {config.nmProtProf}"
#     #------------------------------> Files
#     cImg = config.fImgStart
#     #endregion --------------------------------------------------> Class setup

#     #region --------------------------------------------------> Instance setup
#     def __init__(self, parent: wx.Window, *args, **kwargs) -> None:
#         """"""
#         #region -----------------------------------------------> Initial setup
#         self.parent = parent
        
#         super().__init__(parent=parent, name=self.name)
#         #endregion --------------------------------------------> Initial setup
        
#         #region -----------------------------------------------------> Widgets
#         #--> Images
#         self.img = wx.StaticBitmap(
#             self, 
#             bitmap=wx.Bitmap(str(self.cImg), wx.BITMAP_TYPE_ANY),
#         )
#         #---
#         #--> Buttons
#         self.btnCorrA    = wx.Button(self, label=config.nuCorrA)
#         self.btnDataPrep = wx.Button(self, label=config.nuDataPrep)
#         self.btnLimProt  = wx.Button(self, label=config.nmLimProt)
#         self.btnProtProf = wx.Button(self, label=config.nmProtProf)
#         self.btnTarProt  = wx.Button(self, label=config.nmTarProt)
#         #endregion --------------------------------------------------> Widgets

#         #region ----------------------------------------------------> Tooltips
#         self.btnDataPrep.SetToolTip(self.cTTBtnDataPrep)
#         self.btnCorrA.SetToolTip(self.cTTBtnCorrA)
#         self.btnLimProt.SetToolTip(self.cTTBtnLimProt)
#         self.btnProtProf.SetToolTip(self.cTTBtnProtProf)
#         self.btnTarProt.SetToolTip(self.cTTBtnTarProt)
#         #endregion -------------------------------------------------> Tooltips
        
#         #region ------------------------------------------------------> Sizers
#         #--> Sizers
#         self.Sizer	 = wx.BoxSizer(wx.VERTICAL)
#         self.SizerGrid = wx.GridBagSizer(1,1)
#         self.SizerBtn  = wx.BoxSizer(wx.VERTICAL)
#         #--> Add widgets
#         self.SizerBtn.Add(
#             self.btnCorrA, 0, wx.EXPAND|wx.ALL, 5
#         )
#         self.SizerBtn.Add(
#             self.btnDataPrep, 0, wx.EXPAND|wx.ALL, 5
#         )
#         self.SizerBtn.Add(
#             self.btnLimProt, 0, wx.EXPAND|wx.ALL, 5
#         )
#         self.SizerBtn.Add(
#             self.btnProtProf, 0, wx.EXPAND|wx.ALL, 5
#         )
#         self.SizerBtn.Add(
#             self.btnTarProt, 0, wx.EXPAND|wx.ALL, 5
#         )

#         self.SizerGrid.Add(
#             self.img, 
#             pos	= (0,0),
#             flag   = wx.EXPAND|wx.RIGHT,
#             border = 25,
#         )
#         self.SizerGrid.Add(
#             self.SizerBtn, 
#             pos	= (0,1),
#             flag   = wx.ALIGN_CENTRE_VERTICAL|wx.LEFT,
#             border = 25,
#         )

#         self.Sizer.AddStretchSpacer(1)
#         self.Sizer.Add(
#             self.SizerGrid, 0, wx.CENTER|wx.ALL, 5
#         )
#         self.Sizer.AddStretchSpacer(1)

#         self.SetSizer(self.Sizer)
#         self.Sizer.Fit(self)
#         #endregion ---------------------------------------------------> Sizers

#         #region --------------------------------------------------------> Bind
#         self.btnDataPrep.Bind(
#             wx.EVT_BUTTON, 
#             lambda event: config.winMain.CreateTab(config.ntDataPrep)
#         )
#         self.btnCorrA.Bind(
#             wx.EVT_BUTTON, 
#             lambda event: config.winMain.CreateTab(config.ntCorrA)
#         )
#         self.btnLimProt.Bind(
#             wx.EVT_BUTTON, 
#             lambda event: config.winMain.CreateTab(config.ntLimProt)
#         )
#         self.btnProtProf.Bind(
#             wx.EVT_BUTTON, 
#             lambda event: config.winMain.CreateTab(config.ntProtProf)
#         )
#         #endregion -----------------------------------------------------> Bind
#     #endregion -----------------------------------------------> Instance setup
# #---
# #endregion ----------------------------------------------------------> Classes
