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

import config.config as config
import gui.pane as pane
import gui.dtscore as dtscore
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Methods

#endregion ----------------------------------------------------------> Methods


#region --------------------------------------------------------> Base Classes
class BaseConfTab(wx.Panel):
    """Base class for a Tab containing only a configuration panel. 

        Parameters
        ----------
        parent : wx.Window
            Parent of the tab
        name : str or None
            Unique name of the tab. Default is None. In this case the child 
            class is expected to define a name

        Attributes
        ----------
        parent : wx.Window
            Parent of the tab
        cConfPanel : dict
            Classes to create the configuration panel in tha Tab
        cConfPaneTitle : str
            Title for the configuration panel. 
            Default is config.label['TP_ConfPane'].

        Raises
        ------
        

        Methods
        -------
        
    """
    #region -----------------------------------------------------> Class setup
    cmConfPanel = {
        'CorrATab'   : pane.CorrA,
        'ProtProfTab': pane.ProtProf,
    }
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self, parent: wx.Window, name: Optional[str]=None, 
        dataI: Optional[dict]=None) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.parent = parent
        self.name   = name if name is not None else self.name
        
        self.cnPaneConf = getattr(self, 'cnPaneConf', config.lnPaneConf)
        
        super().__init__(parent, name=self.name)
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------------> Menu
        
        #endregion -----------------------------------------------------> Menu

        #region -----------------------------------------------------> Widgets
        self.conf = self.cmConfPanel[self.name](self, dataI)
        #endregion --------------------------------------------------> Widgets
        
        #region -------------------------------------------------> Aui control
        #------------------------------> AUI control
        self._mgr = aui.AuiManager()
        #------------------------------> AUI which frame to use
        self._mgr.SetManagedWindow(self)
        #------------------------------> Add Configuration panel
        self._mgr.AddPane( 
            self.conf, 
            aui.AuiPaneInfo(
                ).Center(
                ).Caption(
                    self.cnPaneConf
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
        parent : wx.Window
            Parent of the tab 
        name : str or None
            Unique name of the tab. Default is None. In this case the child 
            class is expected to define a name

        Attributes
        ----------
        cLCColLabel : list of str
            Labels for the columns in the wx.ListCtrl.
            Default is config.label['LCtrlColName_I']
        cLCColSize : list of int
            Size of the columns in the wx.ListCtrl. It should match cLCColLabel
            Default is config.size['LCtrl#Name']
        cLCPaneTitle : str
            Title of the pane containing the wx.ListCtrl.
            Default is config.label['TP_ListPane']
            
        Raises
        ------
        

        Methods
        -------
        
    """
    #region -----------------------------------------------------> Class setup
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent: wx.Window, name: Optional[str]=None) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.cLCColLabel = getattr(self, 'cLCColLabel', config.lLCtrlColNameI)
        self.cLCColSize = getattr(self, 'cLCColSize', config.sLCtrlColI)
        self.cLCPaneTitle = getattr(self, 'cLCPaneTitle', config.lnListPane)
        
        super().__init__(parent, name=name)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.lc = dtscore.ListZebraMaxWidth(
            self, colLabel=self.cLCColLabel, colSize=self.cLCColSize,
        )
        #----------------------------> Pointer to lc to load data file content
        self.conf.lbI = self.lc
        self.conf.lbL = [self.lc]
        #endregion --------------------------------------------------> Widgets
        
        #region -------------------------------------------------> Aui control
        self._mgr.AddPane(
            self.lc, 
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
#endregion -----------------------------------------------------> Base Classes


#region -------------------------------------------------------------> Classes
class Start(wx.Panel):
    """Start tab
    
        Parameters
        ----------
        parent : wx.Window
            Direct parent of the widgets in the tab.
        statusbar : wx.SatusBar
            Statusbar to display info
        args : extra arguments

        Attributes
        ----------
        parent : wx widget
            Parent of the tab. 
        name : str
            Name of the tab. Unique name for the application
        statusbar : wx.SatusBar
            Statusbar to display info
        btnLimProt : wx.Button
            Launch the Limited Proteolysis module
        btnProtProf : wx.Button
            Launch the Proteome profiling module
        btnTarProt : wx.Button
            Launch the Targeted Proteolysis module
        Sizer : wx.BoxSizer
            Main sizer of the app
        SizerGrid : wx.GridBagSizer
            Sizer to hold the widgets
        Sizerbtn : wx.BoxSizer
            Sizer for the buttons
    """
    #region -----------------------------------------------------> Class setup
    name = 'StartTab'
    #------------------------------> Tooltips
    cBtnCorrATT = f"Start the utility {config.nUCorrA}"
    cBtnLimProtTT = f"Start the module {config.nMLimProt}"
    cBtnTarProtTT = f"Start the module {config.nMTarProt}"
    cBtnProtProfTT = f"Start the module {config.nMProtProf}"
    #------------------------------> Files
    cImg = config.fImgStart
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent: wx.Window, *args, **kwargs) -> None:
        """"""
        #region -----------------------------------------------> Initial setup
        self.parent = parent
        
        super().__init__(parent=parent, name=self.name)
        #endregion --------------------------------------------> Initial setup
        
        #region -----------------------------------------------------> Widgets
        #--> Images
        self.img = wx.StaticBitmap(
            self, 
            bitmap=wx.Bitmap(str(self.cImg), wx.BITMAP_TYPE_ANY),
        )
        #---
        #--> Buttons
        self.btnCorrA    = wx.Button(self, label=config.nUCorrA)
        self.btnLimProt  = wx.Button(self, label=config.nMLimProt)
        self.btnProtProf = wx.Button(self, label=config.nMProtProf)
        self.btnTarProt  = wx.Button(self, label=config.nMTarProt)
        #endregion --------------------------------------------------> Widgets

        #region ----------------------------------------------------> Tooltips
        self.btnCorrA.SetToolTip(self.cBtnCorrATT)
        self.btnLimProt.SetToolTip(self.cBtnLimProtTT)
        self.btnProtProf.SetToolTip(self.cBtnProtProfTT)
        self.btnTarProt.SetToolTip(self.cBtnTarProtTT)
        #endregion -------------------------------------------------> Tooltips
        
        #region ------------------------------------------------------> Sizers
        #--> Sizers
        self.Sizer	 = wx.BoxSizer(wx.VERTICAL)
        self.SizerGrid = wx.GridBagSizer(1,1)
        self.SizerBtn  = wx.BoxSizer(wx.VERTICAL)
        #--> Add widgets
        self.SizerBtn.Add(
            self.btnCorrA, 0, wx.EXPAND|wx.ALL, 5
        )
        self.SizerBtn.Add(
            self.btnLimProt, 0, wx.EXPAND|wx.ALL, 5
        )
        self.SizerBtn.Add(
            self.btnProtProf, 0, wx.EXPAND|wx.ALL, 5
        )
        self.SizerBtn.Add(
            self.btnTarProt, 0, wx.EXPAND|wx.ALL, 5
        )

        self.SizerGrid.Add(
            self.img, 
            pos	= (0,0),
            flag   = wx.EXPAND|wx.RIGHT,
            border = 25,
        )
        self.SizerGrid.Add(
            self.SizerBtn, 
            pos	= (0,1),
            flag   = wx.ALIGN_CENTRE_VERTICAL|wx.LEFT,
            border = 25,
        )

        self.Sizer.AddStretchSpacer(1)
        self.Sizer.Add(
            self.SizerGrid, 0, wx.CENTER|wx.ALL, 5
        )
        self.Sizer.AddStretchSpacer(1)

        self.SetSizer(self.Sizer)
        self.Sizer.Fit(self)
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind
        self.btnCorrA.Bind(
            wx.EVT_BUTTON, 
            lambda event: config.winMain.CreateTab('CorrATab')
        )
        self.btnProtProf.Bind(
            wx.EVT_BUTTON, 
            lambda event: config.winMain.CreateTab('ProtProfTab')
        )
        #endregion -----------------------------------------------------> Bind
    #endregion -----------------------------------------------> Instance setup
#---
#endregion ----------------------------------------------------------> Classes
