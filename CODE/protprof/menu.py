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


"""Menu for the main module of the app"""


#region -------------------------------------------------------------> Imports
import wx

from config.config import config as mConfig
from core import menu as cMenu
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Classes
class ToolProtProfFCEvolution(cMenu.BaseMenu):
    """Menu for a log2FC evolution along relevant points."""
    #region -----------------------------------------------------> Class Setup
    cLShowAll   = mConfig.prot.lmFCEvolShowAll
    cLExpImg    = mConfig.prot.lmFCEvolExpImg
    cLZoomReset = mConfig.prot.lmFCEvolZoomReset
    #------------------------------>
    cVExpImg    = mConfig.core.kwExpImg
    cVZoomReset = mConfig.core.kwZoomReset
    cVFCShowAll = mConfig.prot.kwFCShowAll
    #------------------------------>
    cVFC = mConfig.prot.kwFC
    #endregion --------------------------------------------------> Class Setup

    #region --------------------------------------------------> Instance setup
    def __init__(self) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__()
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        self.miShowAll = self.Append(-1, self.cLShowAll, kind=wx.ITEM_CHECK)
        self.Check(self.miShowAll.GetId(), True)
        self.AppendSeparator()
        self.miSaveI = self.Append(-1, f'{self.cLExpImg}\tAlt+I')
        self.AppendSeparator()
        self.miZoomR = self.Append(-1, f'{self.cLZoomReset}\tAlt+Z')
        #endregion -----------------------------------------------> Menu Items

        #region ---------------------------------------------------> rKeyID
        rIDMap = {
            self.miSaveI.GetId()  : self.cVExpImg,
            self.miZoomR.GetId()  : self.cVZoomReset,
            self.miShowAll.GetId(): self.cVFCShowAll,
        }
        self.rIDMap = self.rIDMap | rIDMap
        #------------------------------>
        rKeyMap = {
            self.miSaveI.GetId()  : self.cVFC,
            self.miZoomR.GetId()  : self.cVFC,
        }
        self.rKeyMap = self.rKeyMap | rKeyMap
        #endregion ------------------------------------------------> rKeyID

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnMethodLabelBool, source=self.miShowAll)
        self.Bind(wx.EVT_MENU, self.OnMethodLabelKey,  source=self.miSaveI)
        self.Bind(wx.EVT_MENU, self.OnMethodLabelKey,  source=self.miZoomR)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup
#---


class ToolProtProfFilters(cMenu.BaseMenu):
    """Menu for the ProtProfPlot Filters"""
    #region -----------------------------------------------------> Class Setup
    cLFCEvol    = mConfig.prot.lmFilterFcEvol
    cLHypCurve  = mConfig.prot.lmFilterHypCurve
    cLLog2FC    = mConfig.prot.lmFilterLog2FC
    cLPVal      = mConfig.prot.lmFilterPVal
    cLZScore    = mConfig.prot.lmFilterZScore
    cLApplyAll  = mConfig.prot.lmFilterApplyAll
    cLAutoApply = mConfig.prot.lmFilterApplyAuto
    cLRemove    = mConfig.prot.lmFilterRemove
    cLRemoveL   = mConfig.prot.lmFilterRemoveLast
    cLRemoveA   = mConfig.prot.lmFilterRemoveAll
    cLCopy      = mConfig.prot.lmFilterCopy
    cLPaste     = mConfig.prot.lmFilterPaste
    cLSave      = mConfig.prot.lmFilterSave
    cLLoad      = mConfig.prot.lmFilterLoad
    #------------------------------>
    cVFCEvol    = mConfig.prot.kwFilterFCEvol
    cVHypCurve  = mConfig.prot.kwFilterHypCurve
    cVFCLog     = mConfig.prot.kwFilterFCLog
    cVPVal      = mConfig.prot.kwFilterPVal
    cVZScore    = mConfig.prot.kwFilterZScore
    cVApplyAll  = mConfig.prot.kwFilterApplyAll
    cVApplyAuto = mConfig.prot.kwFilterApplyAuto
    cVRemL      = mConfig.prot.kwFilterRemoveLast
    cVRemAny    = mConfig.prot.kwFilterRemoveAny
    cVRemAll    = mConfig.prot.kwFilterRemoveAll
    cVCopy      = mConfig.prot.kwFilterCopy
    cVPaste     = mConfig.prot.kwFilterPaste
    cVSave      = mConfig.prot.kwFilterSave
    cVLoad      = mConfig.prot.kwFilterLoad
    #endregion --------------------------------------------------> Class Setup

    #region --------------------------------------------------> Instance setup
    def __init__(self) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__()
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        self.miFcChange = self.Append(-1, self.cLFCEvol)
        self.miHypCurve = self.Append(-1, self.cLHypCurve)
        self.miLog2FC   = self.Append(-1, self.cLLog2FC)
        self.miPValue   = self.Append(-1, self.cLPVal)
        self.miZScore   = self.Append(-1, self.cLZScore)
        self.AppendSeparator()
        self.miApply = self.Append(-1, f'{self.cLApplyAll}\tCtrl+Shift+A')
        self.miUpdate = self.Append(
            -1, f'{self.cLAutoApply}\tCtrl-Shift+F', kind=wx.ITEM_CHECK)
        self.AppendSeparator()
        self.miRemoveAny  = self.Append(-1, f'{self.cLRemove}\tCtrl+Shift+R')
        self.miRemoveLast = self.Append(-1, f'{self.cLRemoveL}\tCtrl+Shift+Z')
        self.miRemoveAll  = self.Append(-1, f'{self.cLRemoveA}\tCtrl+Shift+X')
        self.AppendSeparator()
        self.miCopy = self.Append(-1,  f'{self.cLCopy}\tCtrl+Shift+C')
        self.miPaste = self.Append(-1, f'{self.cLPaste}\tCtrl+Shift+V')
        self.AppendSeparator()
        self.miSave = self.Append(-1, f'{self.cLSave}\tCtrl+Shift+S')
        self.miLoad = self.Append(-1, f'{self.cLLoad}\tCtrl+Shift+L')
        #endregion -----------------------------------------------> Menu Items

        #region ---------------------------------------------------> rKeyID
        rIDMap = {
            self.miFcChange.GetId()  : self.cVFCEvol,
            self.miHypCurve.GetId()  : self.cVHypCurve,
            self.miLog2FC.GetId()    : self.cVFCLog,
            self.miPValue.GetId()    : self.cVPVal,
            self.miZScore.GetId()    : self.cVZScore,
            self.miApply.GetId()     : self.cVApplyAll,
            self.miRemoveLast.GetId(): self.cVRemL,
            self.miRemoveAny.GetId() : self.cVRemAny,
            self.miRemoveAll.GetId() : self.cVRemAll,
            self.miCopy.GetId()      : self.cVCopy,
            self.miPaste.GetId()     : self.cVPaste,
            self.miSave.GetId()      : self.cVSave,
            self.miLoad.GetId()      : self.cVLoad,
            self.miUpdate.GetId()    : self.cVApplyAuto,
        }
        self.rIDMap = self.rIDMap | rIDMap
        #endregion ------------------------------------------------> rKeyID

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnMethod,          source=self.miFcChange)
        self.Bind(wx.EVT_MENU, self.OnMethod,          source=self.miHypCurve)
        self.Bind(wx.EVT_MENU, self.OnMethod,          source=self.miLog2FC)
        self.Bind(wx.EVT_MENU, self.OnMethod,          source=self.miPValue)
        self.Bind(wx.EVT_MENU, self.OnMethod,          source=self.miZScore)
        self.Bind(wx.EVT_MENU, self.OnMethod,          source=self.miApply)
        self.Bind(wx.EVT_MENU, self.OnMethod,          source=self.miRemoveLast)
        self.Bind(wx.EVT_MENU, self.OnMethod,          source=self.miRemoveAny)
        self.Bind(wx.EVT_MENU, self.OnMethod,          source=self.miRemoveAll)
        self.Bind(wx.EVT_MENU, self.OnMethod,          source=self.miCopy)
        self.Bind(wx.EVT_MENU, self.OnMethod,          source=self.miPaste)
        self.Bind(wx.EVT_MENU, self.OnMethod,          source=self.miSave)
        self.Bind(wx.EVT_MENU, self.OnMethod,          source=self.miLoad)
        self.Bind(wx.EVT_MENU, self.OnMethodLabelBool, source=self.miUpdate)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup
#---


class ToolProtProfLockPlotScale(cMenu.BaseMenu):
    """Lock the plots scale to the selected option."""
    #region -----------------------------------------------------> Class Setup
    cLNo       = mConfig.prot.lmScaleNo
    cLAnalysis = mConfig.prot.lmScaleAnalysis
    cLProject  = mConfig.prot.lmScaleProject
    #------------------------------>
    cVMode     = mConfig.prot.kwScaleMode
    cVNo       = mConfig.prot.kwScaleNo
    cVAnalysis = mConfig.prot.kwScaleAnalysis
    cVProject  = mConfig.prot.kwScaleProject
    cVMode     = mConfig.prot.kwMode
    #endregion --------------------------------------------------> Class Setup

    #region --------------------------------------------------> Instance setup
    def __init__(self) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__()
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        self.miNo      = self.Append(-1, self.cLNo,       kind=wx.ITEM_RADIO)
        self.miDate    = self.Append(-1, self.cLAnalysis, kind=wx.ITEM_RADIO)
        self.miProject = self.Append(-1, self.cLProject,  kind=wx.ITEM_RADIO)
        self.miDate.Check()
        #endregion -----------------------------------------------> Menu Items

        #region ------------------------------------------------------> nameID
        rIDMap = {
            self.miNo.GetId()     : self.cVNo,
            self.miDate.GetId()   : self.cVAnalysis,
            self.miProject.GetId(): self.cVProject,
        }
        self.rIDMap = self.rIDMap | rIDMap
        #------------------------------>
        rKeyMap = {
            self.miNo.GetId()     : self.cVMode,
            self.miDate.GetId()   : self.cVMode,
            self.miProject.GetId(): self.cVMode,
        }
        self.rKeyMap = self.rKeyMap | rKeyMap
        #endregion ---------------------------------------------------> nameID

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnMethodKey, source=self.miNo)
        self.Bind(wx.EVT_MENU, self.OnMethodKey, source=self.miDate)
        self.Bind(wx.EVT_MENU, self.OnMethodKey, source=self.miProject)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup
#---


class ToolProtProfClearSel(cMenu.BaseMenu):
    """Clear the selection in a ProtProf Res Window."""
    #region -----------------------------------------------------> Class Setup
    cLLabel = mConfig.prot.lmClearSelLabel
    cLSel   = mConfig.prot.lmClearSelSel
    cLAll   = mConfig.prot.lmClearSelAll
    #------------------------------>
    cVLabel = mConfig.prot.kwClearSelLabel
    cVSel   = mConfig.prot.kwClearSelSel
    cVAll   = mConfig.prot.kwClearSelAll
    #endregion --------------------------------------------------> Class Setup

    #region --------------------------------------------------> Instance setup
    def __init__(self) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__()
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        self.miLabel = self.Append(-1, self.cLLabel)
        self.miSel   = self.Append(-1, self.cLSel)
        self.AppendSeparator()
        self.miNoSel  = self.Append(-1, f'{self.cLAll}\tCtrl+K')
        #endregion -----------------------------------------------> Menu Items

        #region --------------------------------------------------->
        rIDMap = {
            self.miLabel.GetId(): self.cVLabel,
            self.miSel.GetId()  : self.cVSel,
            self.miNoSel.GetId(): self.cVAll,
        }
        self.rIDMap = self.rIDMap | rIDMap
        #endregion ------------------------------------------------>

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnMethod, source=self.miLabel)
        self.Bind(wx.EVT_MENU, self.OnMethod, source=self.miSel)
        self.Bind(wx.EVT_MENU, self.OnMethod, source=self.miNoSel)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup
#---


class ToolProtProfVolcanoPlotColorScheme(cMenu.BaseMenu):
    """Menu for Color Scheme in the Volcano Plot menu of ProtProf result window.
    """
    #region -----------------------------------------------------> Class Setup
    cLHypCurve = mConfig.prot.lmFilterHypCurve
    cLPLog2FC  = mConfig.prot.lmColorSchemePLog2
    cLZScore   = mConfig.prot.lmFilterZScore
    cLConf     = mConfig.prot.lmColorSchemeConf
    #------------------------------>
    cVHypCurve = mConfig.prot.kwVolPlotColorScheme
    cVPLog2FC  = mConfig.prot.kwVolPlotColorScheme
    cVZScore   = mConfig.prot.kwVolPlotColorScheme
    cVConf     = mConfig.prot.kwVolPlotColorConf
    #endregion --------------------------------------------------> Class Setup

    #region --------------------------------------------------> Instance setup
    def __init__(self):
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__()
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        self.miHypCurve = self.Append(
            -1, self.cLHypCurve, kind=wx.ITEM_RADIO)
        self.miPLogFC   = self.Append(
            -1, self.cLPLog2FC, kind=wx.ITEM_RADIO)
        self.miZScore   = self.Append(
            -1, self.cLZScore, kind=wx.ITEM_RADIO)
        self.AppendSeparator()
        self.miConfigure= self.Append(-1, self.cLConf)
        #endregion -----------------------------------------------> Menu Items

        #region ------------------------------------------------------> rKeyID
        rIDMap = {
            self.miHypCurve.GetId() : self.cVHypCurve,
            self.miPLogFC.GetId  () : self.cVPLog2FC,
            self.miZScore.GetId  () : self.cVZScore,
            self.miConfigure.GetId(): self.cVConf,
        }
        self.rIDMap = self.rIDMap | rIDMap
        #endregion ---------------------------------------------------> rKeyID

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnMethodLabel, source=self.miHypCurve)
        self.Bind(wx.EVT_MENU, self.OnMethodLabel, source=self.miPLogFC)
        self.Bind(wx.EVT_MENU, self.OnMethodLabel, source=self.miZScore)
        self.Bind(wx.EVT_MENU, self.OnMethod,      source=self.miConfigure)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup
#---


class ToolProtProfVolcanoPlot(cMenu.BaseMenu):
    """Menu for a Volcano Plot.

        Parameters
        ----------
        menuData: dict
            Available conditions and relevant point for the analysis.
            See Notes for more details.
        ciDate: str
            Initially selected date

        Attributes
        ----------
        rCond: list of wx.MenuItems
            Available conditions as wx.MenuItems for the current date.
        rCrp: dict
            Available conditions and relevant point for the analysis.
            See Notes for more details.
        rRp: list of wx.MenuItems
            Available relevant points as wx.MenuItems for the current date.
        rSep: wx.MenuItem
            Separator between conditions and relevant points.

        Notes
        -----
        rCrp has the following structure:
            {
                    'date1' : {
                        'C' : [List of conditions as str],
                        'RP': [List of relevant points as str],
                    }
                    .......
                    'dateN' : {}
            }
    """
    #region -----------------------------------------------------> Class Setup
    cLAddLabel    = mConfig.prot.lmVolLabelAdd
    cLPickLabel   = mConfig.prot.lmVolLabelPick
    cLColorScheme = mConfig.prot.lmVolColor
    cLCorrP       = mConfig.core.lmPCorrected
    cLExpImg      = mConfig.prot.lmVolExpImg
    cLZoomReset   = mConfig.prot.lmVolZoomReset
    #------------------------------>
    cVWinUpdate = mConfig.core.kwWinUpdate
    cVLabelPick = mConfig.prot.kwVolPlotLabelPick
    cVLabelProt = mConfig.prot.kwVolPlotLabelProt
    cVPCorr     = mConfig.core.kwWinUpdate
    cVExpImg    = mConfig.core.kwExpImg
    cVZoomReset = mConfig.core.kwZoomReset
    #------------------------------>
    cVPCorrKey = mConfig.core.kwPCorrected
    cVMenuKey  = mConfig.prot.kwVolMenuVol
    cVCond     = mConfig.prot.kwVolMenuCond
    cVRP       = mConfig.prot.kwVolMenuRP
    #endregion --------------------------------------------------> Class Setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, menuData:dict, ciDate:str) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.rCrp = menuData
        #------------------------------> Cond - RP separator. To remove/create.
        self.rSep = None
        #------------------------------>
        super().__init__()
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        self.rCond, self.rRp = self.SetCondRPMenuItems(ciDate)
        self.AppendSeparator()
        self.miLabelProt = self.Append(-1, f'{self.cLAddLabel}\tShift+A')
        self.miLabelPick = self.Append(
            -1, f'{self.cLPickLabel}\tShift+P', kind=wx.ITEM_CHECK)
        self.AppendSeparator()
        self.mColor = ToolProtProfVolcanoPlotColorScheme()
        self.AppendSubMenu(self.mColor, self.cLColorScheme)
        self.AppendSeparator()
        self.miPCorr = self.Append(-1, self.cLCorrP, kind=wx.ITEM_CHECK)
        self.AppendSeparator()
        self.miSaveI = self.Append(-1, f'{self.cLExpImg}\tShift+I')
        self.AppendSeparator()
        self.miZoomR = self.Append(-1, f'{self.cLZoomReset}\tShift+Z')
        #endregion -----------------------------------------------> Menu Items

        #region ---------------------------------------------------> rKeyID
        rIDMap = {
            self.miLabelPick.GetId(): self.cVLabelPick,
            self.miLabelProt.GetId(): self.cVLabelProt,
            self.miPCorr.GetId()    : self.cVPCorr,
            self.miSaveI.GetId()    : self.cVExpImg,
            self.miZoomR.GetId()    : self.cVZoomReset,
        }
        self.rIDMap = self.rIDMap | rIDMap
        #------------------------------>
        rKeyMap = {
            self.miPCorr.GetId() : self.cVPCorrKey,
            self.miSaveI.GetId() : self.cVMenuKey,
            self.miZoomR.GetId() : self.cVMenuKey,
        }
        self.rKeyMap = self.rKeyMap | rKeyMap
        #endregion ------------------------------------------------> rKeyID

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnMethod,         source=self.miLabelProt)
        self.Bind(wx.EVT_MENU, self.OnMethod,         source=self.miLabelPick)
        self.Bind(wx.EVT_MENU, self.OnMethodKeyBool,  source=self.miPCorr)
        self.Bind(wx.EVT_MENU, self.OnMethodLabelKey, source=self.miSaveI)
        self.Bind(wx.EVT_MENU, self.OnMethodLabelKey, source=self.miZoomR)
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #region --------------------------------------------------> Manage methods
    def SetCondRPMenuItems(
        self,
        tDate:str,
        ) -> tuple[list[wx.MenuItem], list[wx.MenuItem]]:
        """Set the menu items for conditions and relevant points as defined for
            the current analysis date.

            Parameters
            ----------
            tDate: str
                Currently selected date.

            Returns
            -------
            tuple:
                First element is the condition menu items and second relevant
                point menu items.
        """
        #region -------------------------------------------------> Empty lists
        cond = []
        rp   = []
        #endregion ----------------------------------------------> Empty lists

        #region ------------------------------------------------> Add elements
        #------------------------------> Conditions
        k = 0
        for c in self.rCrp[tDate]['C']:
            #------------------------------>
            cond.append(self.Insert(k, -1, item=c, kind=wx.ITEM_RADIO))
            #------------------------------>
            self.Bind(wx.EVT_MENU, self.OnMethodKey, source=cond[-1])
            #------------------------------>
            self.rIDMap[cond[-1].GetId()]  = self.cVWinUpdate
            self.rKeyMap[cond[-1].GetId()] = self.cVCond
            #------------------------------>
            k = k + 1
        #------------------------------>
        self.rSep = self.Insert(k, -1, kind=wx.ITEM_SEPARATOR)
        k = k + 1
        #------------------------------> Relevant Points
        for t in self.rCrp[tDate]['RP']:
            #------------------------------>
            rp.append(self.Insert(k, -1, item=t, kind=wx.ITEM_RADIO))
            #------------------------------>
            self.Bind(wx.EVT_MENU, self.OnMethodKey, source=rp[-1])
            #------------------------------>
            self.rIDMap[rp[-1].GetId()]  = self.cVWinUpdate
            self.rKeyMap[rp[-1].GetId()] = self.cVRP
            #------------------------------>
            k = k + 1
        #endregion ---------------------------------------------> Add elements

        return (cond, rp)
    #---

    def UpdateCondRP(self, tDate:str, menuData:dict={}) -> bool:                # pylint: disable=dangerous-default-value
        """Update the conditions and relevant points when date changes.

            Parameters
            ----------
            tDate: str
                Selected date
            menuData: dict
                Information for the menu item.

            Returns
            -------
            bool

            Notes
            -----
            Date changes in ProtProfToolMenu
        """
        #region --------------------------------------------------->
        self.rCrp = menuData if menuData else self.rCrp
        #endregion ------------------------------------------------>

        #region ---------------------------------------------> Delete Elements
        #------------------------------> Conditions
        for c in self.rCond:
            self.Delete(c)
        #------------------------------> Separators
        self.Delete(self.rSep)
        #------------------------------> RP
        for rp in self.rRp:
            self.Delete(rp)
        #endregion ------------------------------------------> Delete Elements

        #region -----------------------------------> Create & Add New Elements
        self.rCond, self.rRp = self.SetCondRPMenuItems(tDate)
        #endregion --------------------------------> Create & Add New Elements

        return True
    #---
    #endregion -----------------------------------------------> Manage methods
#---


class ToolProtProf(cMenu.BaseMenuMainResult):
    """Tool menu for the Proteome Profiling Plot window.

        Parameters
        ----------
        menuData: dict
            Data needed to build the menu.
            {
                'MenuDate' : [List of dates as str],
                'crp' : {
                    'date1' : {
                        'C' : [List of conditions as str],
                        'RP': [List of relevant points as str],
                    }
                    .......
                    'dateN'
                }
            }
    """
    #region -----------------------------------------------------> Class Setup
    cLVol           = mConfig.prot.lmToolVolPlot
    cLFC            = mConfig.prot.lmToolFCEvol
    cLFilter        = mConfig.prot.lmToolFilter
    cLLock          = mConfig.prot.lmToolLockScale
    cLCLear         = mConfig.prot.lmToolClearSel
    cLExpDataFilter = mConfig.prot.lmToolExpFilterData
    #------------------------------>
    cVExpDataFilter = mConfig.prot.kwExportDataFiltered
    #endregion --------------------------------------------------> Class Setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, menuData:dict) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(menuData)
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------> Menu Items
        self.mVolcano =  ToolProtProfVolcanoPlot(
                self.rMenuData['crp'], self.rPlotDate[0].GetItemLabelText()
        )
        self.AppendSubMenu(self.mVolcano, self.cLVol)
        self.AppendSeparator()
        #------------------------------> Relevant Points
        self.mFc = ToolProtProfFCEvolution()
        self.AppendSubMenu(self.mFc, self.cLFC)
        self.AppendSeparator()
        #------------------------------> Filter
        self.mFilter = ToolProtProfFilters()
        self.AppendSubMenu(self.mFilter, self.cLFilter)
        self.AppendSeparator()
        #------------------------------> Lock scale
        self.mLockScale = ToolProtProfLockPlotScale()
        self.AppendSubMenu(self.mLockScale, self.cLLock)
        self.AppendSeparator()
        #------------------------------> Clear Selection
        self.mClearSel = ToolProtProfClearSel()
        self.AppendSubMenu(self.mClearSel, self.cLCLear)
        self.AppendSeparator()
        #------------------------------>
        self.AddLastItems(False)
        pos = self.FindChildItem(self.miSaveD.GetId())[1]
        self.miSaveDataFiltered = self.Insert(
            pos+1, -1, f'{self.cLExpDataFilter}\tShift+Ctrl+E')
        #endregion -----------------------------------------------> Menu Items

        #region ---------------------------------------------------> rKeyID
        rIDMap = {
            self.miSaveDataFiltered.GetId() : self.cVExpDataFilter,
        }
        self.rIDMap = self.rIDMap | rIDMap
        #endregion ------------------------------------------------> rKeyID

        #region ---------------------------------------------------> Bind
        self.Bind(wx.EVT_MENU, self.OnMethod, source=self.miSaveDataFiltered)
        #endregion ------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class Methods
    def OnMethodKey(self, event:wx.MenuEvent):
        """Call the corresponding method in the window.

            Parameters
            ----------
            event: wx.CommandEvent
                Information about the event.

            Returns
            -------
            bool
        """
        #region -------------------------------------------------------->
        tID      = event.GetId()
        menuItem = self.FindItem(tID)[0]
        label    = self.GetLabelText(tID)
        #endregion ----------------------------------------------------->

        #region --------------------------------------------------->
        if menuItem in self.rPlotDate:
            #------------------------------> Update Menu
            self.mVolcano.UpdateCondRP(label)
            #------------------------------> Update Plot
            win = self.GetWindow()
            win.UpdateResultWindow(
                tDate = label,
                cond  = self.mVolcano.rCond[0].GetItemLabelText(),
                rp    = self.mVolcano.rRp[0].GetItemLabelText(),
            )
        else:
            super().OnMethodKey(event)
        #endregion ------------------------------------------------>

        return True
    #---

    def UpdateOtherItems(self, menuData:dict, tDate:wx.MenuItem) -> bool:
        """Update Further Analysis.

            Parameters
            ----------
            menuData: dict
                Updated menu content.
            tDate: wx.MenuItem
                Currently selected Analysis ID

            Returns
            -------
            bool
        """
        return self.mVolcano.UpdateCondRP(
            tDate.GetItemLabelText(), menuData=menuData['crp'])
    #---
    #endregion ------------------------------------------------> Class Methods
#---
#endregion ----------------------------------------------------------> Classes
