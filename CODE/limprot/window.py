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


"""Windows for the limprot module of the app"""


#region -------------------------------------------------------------> Imports
from itertools import zip_longest
from pathlib   import Path
from typing    import Optional, Union, TYPE_CHECKING

import pandas             as pd
import matplotlib.patches as mpatches

from reportlab.lib.pagesizes      import A4
from reportlab.platypus           import SimpleDocTemplate, Paragraph, Spacer
from reportlab.platypus.flowables import KeepTogether
from reportlab.lib.styles         import getSampleStyleSheet, ParagraphStyle

import wx
import wx.richtext
from wx import aui

from config.config import config as mConfig
from core    import method as cMethod
from core    import window as cWindow
from main    import menu   as mMenu
from limprot import method as limpMethod

if TYPE_CHECKING:
    from result import window as resWindow
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Classes
class ResLimProt(cWindow.BaseWindowResultListText2PlotFragments):
    """Plot the results of a Limited Proteolysis analysis.

        Parameters
        ----------
        parent: wx.Window
            Parent of the window.

        Attributes
        ----------
        dClearMethod: dict
            Methods to clear the selections in the window.
        rBlSelC: list[int, int]
            Coordinates for the Band/Lane selected from 1 to N
        rBlSelRect: mpatch
            Rectangle used to highlight the selected Band/Lane.
        rCorrP: bool
            Show P corrected values (True) or regular values (False).
        rData: dict
            Data for the Limited Proteolysis section of the UMSAP File.
        rDate: list[str]
            Available dates.
        rDateC: str
            Currently selected date.
        rDf: pd.DataFrame
            Copy of the data used to plot
        rFragments: cMethod.Fragment
            Class with the info for the fragments. See cMethod.Fragment.
        rFragSelC: list[band, lane, fragment]
            Coordinates for the currently selected fragment. 0 based.
        rFragSelLine: matplotlib line
            Line to highlight the currently selected fragment.
        rGelSelC: list[band, lane]
            Coordinated for the currently selected gel spot. 1 based.
        rGelSpotPicked: bool
            Gel spot was selected (True) or not (False).
        rLCIdx: int
            Row selected in the wx.ListCtrl.
        rObj: UMSAPFile
            Reference to the UMSAP file in the parent UMSAPCtrl window.
        rPeptide: str
            Sequence of the selected peptide in the wx.ListCtrl.
        rPStr: str
            Name of the P column in the dataframe.
        rRecSeq: dict
            Keys are date and values the sequence of the recombinant protein.
        rRecSeqC: str
            Sequence of the recombinant protein for the current date.
        rReqSeqColor: dict
            Keys are color and values are sequences to highlight in the given
            color.
        rRectsFrag: list[mpatches]
            Rectangles used in the Fragment plot.
        rRectsGel: list[mpatches]
            Rectangles used in the Gel spot.
        rSelBands: bool
            Select Bands (True) or Lanes (False).
        rSpotSelLine: line
            Line to highlight the selected Gel spot.
        rTextStyleDef: wx.TextAttr
            Text Style for Sequence Highlight.
        rUpdateColors: bool
            Update Gel colors (True) or not (False).
    """
    #region -----------------------------------------------------> Class setup
    cName    = mConfig.limp.nwRes
    cSection = mConfig.limp.nMod
    #------------------------------>
    cSWindow = (1100, 900)
    #------------------------------>
    cImgName   = {
        mConfig.core.kwMain: '{}-Protein-Fragments.tiff',
        mConfig.core.kwSec : '{}-Gel-Representation.tiff',
    }
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent:'resWindow.UMSAPControl') -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.cTitle          = f'{parent.cTitle} - {self.cSection}'
        self.rObj            = parent.rObj
        self.rData:limpMethod.LimpAnalysis = self.rObj.dConfigure[self.cSection]()
        self.rDate, menuData = self.SetDateMenuDate()
        #------------------------------>
        self.ReportPlotDataError()
        #------------------------------>
        self.rDateC         = self.rDate[0]
        self.rDataC         = getattr(self.rData, self.rDateC)
        self.rCorrP         = False
        self.rPStr          = 'Ptost'
        self.rIdxP          = pd.IndexSlice[:,:,'Ptost']
        self.rSelBands      = True
        self.rBlSelRect     = None
        self.rSpotSelLine   = None
        self.rBlSelC        = [None, None]
        self.rGelSpotPicked = False
        self.rUpdateColors  = False
        self.rRecSeq        = {}
        self.rTextStyleDef  = wx.TextAttr(
            'Black', 'White', mConfig.core.fSeqAlign)
        self.rGelSelC       = [None, None]
        #------------------------------>
        super().__init__(parent)
        #------------------------------>
        dKeyMethod = {
            mConfig.limp.kwClearPeptide : self.ClearPept,
            mConfig.limp.kwClearFragment: self.ClearFrag,
            mConfig.limp.kwClearGelSpot : self.ClearGel,
            mConfig.limp.kwClearBandLane: self.ClearBL,
            mConfig.limp.kwClearAll     : self.ClearAll,
            #------------------------------>
            mConfig.limp.kwBandLane : self.LaneBandSel,
            mConfig.limp.kwShowAll  : self.ShowAll,
        }
        self.dKeyMethod = self.dKeyMethod | dKeyMethod
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wTextSeq = wx.richtext.RichTextCtrl(
            self, size=(100,100), style=wx.TE_READONLY|wx.TE_MULTILINE)
        self.wTextSeq.SetFont(mConfig.core.fSeqAlign)
        #endregion --------------------------------------------------> Widgets

        #region ---------------------------------------------------------> AUI
        self._mgr.AddPane(
            self.wTextSeq,
            aui.AuiPaneInfo(
                ).Bottom(
                ).Layer(
                    1
                ).Caption(
                    'Sequence Alignment'
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
        #endregion ------------------------------------------------------> AUI

        #region --------------------------------------------------------> Menu
        self.mBar = mMenu.MenuBarTool(self.cName, menuData=menuData)
        self.SetMenuBar(self.mBar)
        #endregion -----------------------------------------------------> Menu

        #region --------------------------------------------------------> Bind
        self.wPlot['Sec'].rCanvas.mpl_connect('pick_event', self.OnPickGel)
        self.wPlot['Sec'].rCanvas.mpl_connect(
            'button_press_event', self.OnPressMouse)
        #endregion -----------------------------------------------------> Bind

        #region ---------------------------------------------> Window position
        self.UpdateResultWindow()
        self.WinPos()
        self.Show()
        #endregion ------------------------------------------> Window position
    #---
    #endregion -----------------------------------------------> Instance setup

    #region --------------------------------------------------> Manage Methods
    def LaneBandSel(self, state:bool) -> bool:
        """Change Band/Lane selection mode.

            Parameters
            ----------
            state: bool

            Returns
            -------
            bool
        """
        self.rSelBands     = not state
        self.rUpdateColors = True
        #------------------------------>
        return True
    #---

    def ShowAll(self) -> bool:
        """Show all Fragments.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        idx = self.rLCIdx
        self.ClearAll()
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        self.UpdateGelColor(showAll=True)
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        self.rBlSelRect = mpatches.Rectangle(
            (0.55, 0.55),
            len(self.rDataC.labelA)-0.1,
            len(self.rDataC.labelB)-0.1,
            linewidth = 1.5,
            edgecolor = 'red',
            fill      = False,
        )
        #------------------------------>
        self.wPlot['Sec'].rAxes.add_patch(self.rBlSelRect)
        #------------------------------>
        self.wPlot['Sec'].rCanvas.draw()
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        #------------------------------>
        tKeys   = []
        tLabel  = []
        tColor  = []
        tYLabel = []
        self.rRectsFrag = []
        #------------------------------>
        if self.rSelBands:
            for bk, b in enumerate(self.rDataC.labelB):
                for lk, l in enumerate(self.rDataC.labelA):
                    tKeys.append(f'{b}-{l}-{self.rPStr}')
                    tYLabel.append(f'{b}-{l}')
                    tColor.append(bk)
                    tLabel.append(f'{bk}.{lk}')
        else:
            for lk, l in enumerate(self.rDataC.labelA):
                for bk, b in enumerate(self.rDataC.labelB):
                    tKeys.append(f'{b}-{l}-{self.rPStr}')
                    tYLabel.append(f'{l}-{b}')
                    tColor.append(lk)
                    tLabel.append(f'{bk}.{lk}')
        #------------------------------>
        self.SetFragmentAxis(showAll=tYLabel)
        #------------------------------>
        nc = len(self.cSpot)                                                    # type: ignore
        #------------------------------>
        k = 1
        for k,v in enumerate(tKeys, start=1):
            frag = getattr(self.rFragments, v)
            for j,f in enumerate(frag.coord):
                self.rRectsFrag.append(mpatches.Rectangle(
                    (f[0], k-0.2),
                    (f[1]-f[0]),
                    0.4,
                    picker    = True,
                    linewidth = self.cGelLineWidth,
                    facecolor = self.cSpot[(tColor[k-1])%nc],                   # type: ignore
                    edgecolor = 'black',
                    label     = f'{tLabel[k-1]}.{j}',
                ))
                self.wPlot['Main'].rAxes.add_patch(self.rRectsFrag[-1])
        #------------------------------>
        self.DrawProtein(k+1)                                                   # type: ignore
        #------------------------------>
        self.wPlot['Main'].ZoomResetSetValues()
        self.wPlot['Main'].rCanvas.draw()
        #endregion ------------------------------------------------>

        #region --------------------------------------------> Reselect peptide
        if idx is not None:
            self.wLC.wLCS.wLC.Select(idx, on=1)
        #endregion -----------------------------------------> Reselect peptide

        #region ---------------------------------------------------> Show Text
        self.PrintAllText()
        #endregion ------------------------------------------------> Show Text

        #region ---------------------------------------------------> Rec Sec
        self.rRecSeqColor['Red'] = self.SeqHighAll()
        self.RecSeqHighlight()
        #endregion ------------------------------------------------> Rec Sec

        return True
    #---

    def WinPos(self) -> bool:
        """Set the position on the screen and adjust the total number of
            shown windows.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        info = super().WinPos()
        #endregion ------------------------------------------------> Variables

        #region ------------------------------------------------> Set Position
        x = info['D']['xo'] + info['W']['N']*mConfig.core.deltaWin
        y = (
            ((info['D']['h']/2) - (info['W']['h']/2))
            + info['W']['N']*mConfig.core.deltaWin
        )
        self.SetPosition(pt=(x,y))
        #endregion ---------------------------------------------> Set Position

        return True
    #---

    def UpdateResultWindow(
        self,
        tDate:str            ='',
        corrP:Optional[bool] = None,
        ) -> bool:
        """Update the GUI and attributes when a new date is selected.

            Parameters
            ----------
            date: str
                Selected date.
            corrP: bool or None
                Sow corrected P values (True) or regular P values (False, None).
                Default is None.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        self.rDateC = tDate if tDate else self.rDateC
        self.rDataC:limpMethod.LimpAnalysis = getattr(self.rData, self.rDateC)
        #------------------------------>
        self.rDf          = self.rDataC.df.copy()
        self.rRectsGel    = []
        self.rRectsFrag   = []
        self.rBlSelC      = [None, None]
        self.rGelSelC     = [None, None]
        self.rFragSelC    = [None, None, None]
        self.rPeptide     = None
        self.rLCIdx       = None
        self.rCorrP       = corrP if corrP is not None else self.rCorrP
        self.rPStr        = 'Pc' if self.rCorrP else 'Ptost'
        self.rIdxP = pd.IndexSlice[:,:,'Pc'] if self.rCorrP else pd.IndexSlice[:,:,'Ptost']

        self.rRecSeqColor = {'Red':[],'Blue':{'Pept':[],'Spot':[],'Frag':[]}}
        self.rRecSeqC     = (
            self.rRecSeq.get(self.rDateC)
            or
            self.rObj.GetRecSeq(self.cSection, self.rDateC)
        )
        self.rRecSeq[self.rDateC] = self.rRecSeqC
        #endregion ------------------------------------------------> Variables

        #region ---------------------------------------------------> Fragments
        try:
            df = self.GetDF4FragmentSearch()
        except KeyError as e:
            #------------------------------> Notification
            if 'Pc' in str(e):
                cWindow.Notification(
                    'warning',
                    msg        = mConfig.core.mNoPCorr,
                    tException = e,
                    parent     = self,
                )
            else:
                cWindow.Notification(
                    'errorU',
                    msg        = mConfig.core.mUnexpectedError,
                    tException = e,
                    parent     = self,
                )
            #------------------------------> Reset attributes
            self.rCorrP = False
            self.rPStr  = 'Ptost'
            self.rIdxP  = pd.IndexSlice[:,:,'Ptost']
            #------------------------------> Reset Menu
            menu = self.mBar.GetMenu(self.mBar.FindMenu(mConfig.core.lmTools))
            item = menu.FindChildItem(menu.FindItem(mConfig.core.lmPCorrected))[0]
            item.Check(check=False)
            #------------------------------> df
            df = self.GetDF4FragmentSearch()
        #------------------------------>
        self.rFragments = cMethod.Fragments(
            df,
            self.rDataC.alpha,
            'le',
            self.rDataC.protLength[0],
            self.rDataC.protLoc
        )
        #------------------------------>
        self.SetEmptyFragmentAxis()
        #endregion ------------------------------------------------> Fragments

        #region --------------------------------------------------->
        self.wText.Clear()
        self.wTextSeq.Clear()
        self.wTextSeq.AppendText(self.rRecSeqC)
        self.wTextSeq.SetInsertionPoint(0)
        #endregion ------------------------------------------------>

        #region -------------------------------------------------> wx.ListCtrl
        self.FillListCtrl()
        #endregion ----------------------------------------------> wx.ListCtrl

        #region ----------------------------------------------------> Gel Plot
        self.DrawGel()
        #endregion -------------------------------------------------> Gel Plot

        #region ---------------------------------------------------> Win Title
        self.PlotTitle()
        #endregion ------------------------------------------------> Win Title

        return True
    #---

    def DrawGel(self) -> bool:
        """Draw the Gel representation on the window.

            Returns
            -------
            bool
        """
        #region ---------------------------------------> Remove Old Selections
        #------------------------------> Select Gel Spot
        if self.rSpotSelLine is not None:
            self.rSpotSelLine[0].remove()
            self.rSpotSelLine = None
        #------------------------------>
        if self.rBlSelRect is not None:
            self.rBlSelRect.remove()
            self.rBlSelRect = None
        #endregion ------------------------------------> Remove Old Selections

        #region --------------------------------------------------------> Axis
        self.SetGelAxis()
        #endregion -----------------------------------------------------> Axis

        #region ---------------------------------------------------> Draw Rect
        for nb,_ in enumerate(self.rDataC.labelB, start=1):
            for nl,_ in enumerate(self.rDataC.labelA, start=1):
                self.rRectsGel.append(mpatches.Rectangle(
                    ((nl-0.4),(nb-0.4)),
                    0.8,
                    0.8,
                    edgecolor = 'black',
                    linewidth = self.cGelLineWidth,
                    facecolor = self.SetGelSpotColor(nb-1,nl-1),
                    picker    = True,
                ))
                self.wPlot['Sec'].rAxes.add_patch(self.rRectsGel[-1])
        #endregion ------------------------------------------------> Draw Rect

        #region --------------------------------------------------> Zoom Reset
        self.wPlot['Sec'].ZoomResetSetValues()
        #endregion -----------------------------------------------> Zoom Reset

        #region --------------------------------------------------------> Draw
        self.wPlot['Sec'].rCanvas.draw()
        #endregion -----------------------------------------------------> Draw

        return True
    #---

    def SetGelAxis(self) -> bool:
        """Configure the axis for the Gel representation.

            Returns
            -------
            bool
        """
        #region ----------------------------------------------------> Variables
        nLanes = len(self.rDataC.labelA)
        nBands = len(self.rDataC.labelB)
        #endregion -------------------------------------------------> Variables

        #region --------------------------------------------------->
        self.wPlot['Sec'].rAxes.clear()
        self.wPlot['Sec'].rAxes.set_xticks(range(1, nLanes+1))
        self.wPlot['Sec'].rAxes.set_xticklabels(self.rDataC.labelA)
        self.wPlot['Sec'].rAxes.set_yticks(range(1, nBands+1))
        self.wPlot['Sec'].rAxes.set_yticklabels(self.rDataC.labelB)
        self.wPlot['Sec'].rAxes.tick_params(length=0)
        #------------------------------>
        self.wPlot['Sec'].rAxes.set_xlim(0.5, nLanes+0.5)
        self.wPlot['Sec'].rAxes.set_ylim(0.5, nBands+0.5)
        #endregion ------------------------------------------------>

        #region ------------------------------------------------> Remove Frame
        self.wPlot['Sec'].rAxes.spines['top'].set_visible(False)
        self.wPlot['Sec'].rAxes.spines['right'].set_visible(False)
        self.wPlot['Sec'].rAxes.spines['bottom'].set_visible(False)
        self.wPlot['Sec'].rAxes.spines['left'].set_visible(False)
        #endregion ---------------------------------------------> Remove Frame

        return True
    #---

    def SetGelSpotColor(
        self,
        nb:int,
        nl:int,
        showAll:bool=False,
        ) -> str:
        """Get the color for each gel spot.

            Parameters
            ----------
            nb: int
                Number of bands in the gel.
            nl: int
                Number of lanes in the gel.
            showAll: bool
                Show all fragments in the gel or not.

            Returns
            -------
            str
                Gel spot color
        """
        #region ---------------------------------------------------> Variables
        b = self.rDataC.labelB[nb]
        l = self.rDataC.labelA[nl]
        c = (self.rDf.loc[:,(b,l,self.rPStr)].isna().all() or                   # type: ignore
            not getattr(self.rFragments, f'{b}-{l}-{self.rPStr}').coord
        )
        nc = len(self.cSpot)                                                    # type: ignore
        #endregion ------------------------------------------------> Variables

        #region -------------------------------------------------------> Color
        if c:
            return 'white'
        #------------------------------>
        if showAll:
            if self.rSelBands:
                return self.cSpot[nb%nc]                                        # type: ignore
            #------------------------------>
            return self.cSpot[nl%nc]                                            # type: ignore
        #------------------------------>
        if self.rSelBands:
            return self.cSpot[nl%nc]                                            # type: ignore
            #------------------------------>
        return self.cSpot[nb%nc]                                                # type: ignore
        #endregion ----------------------------------------------------> Color
    #---

    def DrawBLRect(self, x:int, y:int) -> bool:
        """Draw the red rectangle to highlight the selected band/lane.

            Parameters
            ----------
            x: int
                X coordinate of the band/lane
            y: int
                Y coordinate of the band/lane

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        self.UpdateGelColor()
        #endregion ------------------------------------------------>

        #region ---------------------------------------------------> Variables
        if self.rSelBands:
            xy = (0.55, y-0.45)
            w = len(self.rDataC.labelA) - 0.1
            h = 0.9
        else:
            xy = (x-0.45, 0.55)
            w = 0.9
            h = len(self.rDataC.labelB) - 0.1
        #endregion ------------------------------------------------> Variables

        #region ---------------------------------------------> Remove Old Rect
        if self.rBlSelRect is not None:
            self.rBlSelRect.remove()
        #endregion ------------------------------------------> Remove Old Rect

        #region -----------------------------------------------> Draw New Rect
        self.rBlSelRect = mpatches.Rectangle(
            xy, w, h,
            linewidth = 1.5,
            edgecolor = 'red',
            fill      = False,
        )
        self.wPlot['Sec'].rAxes.add_patch(self.rBlSelRect)
        self.wPlot['Sec'].rCanvas.draw()
        #endregion --------------------------------------------> Draw New Rect

        return True
    #---

    def DrawFragments(self, x:int, y:int) -> bool:                              # pylint: disable=arguments-differ
        """Draw the fragments associated with the selected band/lane.

            Parameters
            ----------
            x: int
                X coordinate of the band/lane.
            y: int
                Y coordinate of the band/lane.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        b = self.rDataC.labelB[y-1]
        l = self.rDataC.labelA[x-1]
        tKeyLabel = {}
        #endregion ------------------------------------------------> Variables

        #region --------------------------------------------------------> Keys
        if self.rSelBands:
            for k,tL in enumerate(self.rDataC.labelA):
                tKeyLabel[f'{b}-{tL}-{self.rPStr}'] = f'{y-1}.{k}'
        else:
            for k,tB in enumerate(self.rDataC.labelB):
                tKeyLabel[f'{tB}-{l}-{self.rPStr}'] = f'{k}.{x-1}'
        #endregion -----------------------------------------------------> Keys

        #region -------------------------------------------------------> Super
        super().DrawFragments(tKeyLabel)
        #endregion ----------------------------------------------------> Super

        return True
    #---

    def SetFragmentAxis(self, showAll:list[str]=[]) -> bool:                    # pylint: disable=dangerous-default-value
        """Set the axis for the plot showing the fragments.

            Parameters
            ----------
            showAll: bool
                Show all fragments or not. Default is False.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        self.wPlot['Main'].rAxes.clear()
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        #------------------------------>
        if self.rDataC.protLoc[0] > -1:
            xtick = [1] + list(self.rDataC.protLoc) + [self.rDataC.protLength[0]]
        else:
            xtick = [1] + [self.rDataC.protLength[0]]
        self.wPlot['Main'].rAxes.set_xticks(xtick)
        self.wPlot['Main'].rAxes.set_xticklabels(xtick)
        #------------------------------>
        if showAll:
            self.wPlot['Main'].rAxes.set_yticks(range(1, len(showAll)+2))
            self.wPlot['Main'].rAxes.set_yticklabels(showAll+['Protein'])
            self.wPlot['Main'].rAxes.set_ylim(0.5, len(showAll)+1.5)
            #------------------------------>
            ymax = len(showAll)+0.8
        else:
            if self.rSelBands:
                #------------------------------>
                self.wPlot['Main'].rAxes.set_yticks(range(1, len(self.rDataC.labelA)+2))
                self.wPlot['Main'].rAxes.set_yticklabels(self.rDataC.labelA+['Protein'])
                self.wPlot['Main'].rAxes.set_ylim(0.5, len(self.rDataC.labelA)+1.5)
                #------------------------------>
                ymax = len(self.rDataC.labelA)+0.8
            else:
                #------------------------------>
                self.wPlot['Main'].rAxes.set_yticks(range(1, len(self.rDataC.labelB)+2))
                self.wPlot['Main'].rAxes.set_yticklabels(self.rDataC.labelB+['Protein'])
                self.wPlot['Main'].rAxes.set_ylim(0.5, len(self.rDataC.labelB)+1.5)
                #------------------------------>
                ymax = len(self.rDataC.labelB)+0.8
        #------------------------------>
        self.wPlot['Main'].rAxes.tick_params(length=0)
        #------------------------------>
        self.wPlot['Main'].rAxes.set_xlim(0, self.rDataC.protLength[0]+1)
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        self.wPlot['Main'].rAxes.vlines(
            xtick, 0, ymax, linestyles='dashed', linewidth=0.5, color='black')
        #endregion ------------------------------------------------>

        #region ------------------------------------------------> Remove Frame
        self.wPlot['Main'].rAxes.spines['top'].set_visible(False)
        self.wPlot['Main'].rAxes.spines['right'].set_visible(False)
        self.wPlot['Main'].rAxes.spines['bottom'].set_visible(False)
        self.wPlot['Main'].rAxes.spines['left'].set_visible(False)
        #endregion ---------------------------------------------> Remove Frame

        return True
    #---

    def PrintBLText(self, x:int, y:int) -> bool:
        """Print the text for selected band/lane.

            Parameters
            ----------
            x: int
                X coordinates of the selected band/lane.
            y: int
                Y coordinates of the selected band/lane.

            Returns
            -------
            bool
        """
        if self.rSelBands:
            return self.PrintBText(y)
        #------------------------------>
        return self.PrintLText(x)
    #---

    def PrintLBGetInfo(self, tKeys:list[str]) -> dict:
        """Helper method to get information about the selected Band/Lane.

            Parameters
            ----------
            tKeys: str
                List of keys for the information.

            Returns
            -------
            dict:
                {
                    'LanesWithFP': ,
                    'Fragments': ,
                    'FP': ,
                    'NCO': ,
                    'NCONat': ,
                }
        """
        #region --------------------------------------------------->
        dictO = {}
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        lanesWithFP = []
        fragments   = []
        fP          = []
        ncL         = []
        ncO         = []
        #------------------------------>
        for tKey in tKeys:
            x = f'{tKey}'
            frag = getattr(self.rFragments, x)
            nF = len(frag.coord)
            #-------------->
            if nF:
                if self.rSelBands:
                    lanesWithFP.append(tKey.split('-')[1])
                else:
                    lanesWithFP.append(tKey.split('-')[0])
                fragments.append(nF)
                fP.append(sum(frag.np))
            #------------------------------>
            ncL = ncL + frag.coord
        #------------------------------>
        dictO['LanesWithFP'] = (
            f'{len(lanesWithFP)} (' + f'{lanesWithFP}'[1:-1] + ')')
        dictO['Fragments'] = (
            f'{sum(fragments)} (' + f'{fragments}'[1:-1] + ')')
        dictO['FP'] = (
            f'{sum(fP)} (' +f'{fP}'[1:-1] + ')')
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        ncL.sort()
        #------------------------------>
        if not ncL:
            return {}
        #------------------------------>
        n,c = ncL[0]
        for nc,cc in ncL[1:]:
            if nc <= c:
                if cc <= c:
                    pass
                else:
                    c = cc
            else:
                ncO.append((n,c))
                n = nc
                c = cc
        ncO.append((n,c))
        #------------------------------>
        if self.rDataC.protDelta is not None:
            ncONat = []
            for a,b in ncO:
                aX = a+self.rDataC.protDelta
                bX = b+self.rDataC.protDelta
                ncONat.append((aX,bX))
        else:
            ncONat = 'NA'
        #------------------------------>
        dictO['NCO'] = ncO
        dictO['NCONat'] = ncONat
        #endregion ------------------------------------------------>

        return dictO
    #---

    def PrintBText(self, band:int) -> bool:
        """Print information about a Band.

            Parameters
            ----------
            band: int
                Index of the selected band in self.rDataC.labelB.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------> Get Values
        #------------------------------> Keys
        tKeys = [f'{self.rDataC.labelB[band]}-{x}-{self.rPStr}' for x in self.rDataC.labelA]
        #------------------------------> Info
        infoDict = self.PrintLBGetInfo(tKeys)                                   # type: ignore
        #endregion -----------------------------------------------> Get Values

        #region -------------------------------------------------------> Clear
        self.wText.Clear()
        #endregion ----------------------------------------------------> Clear

        #region ----------------------------------------------------> New Text
        if infoDict:
            self.wText.AppendText(f'Details for {self.rDataC.labelB[band]}\n\n')
            self.wText.AppendText('--> Analyzed Lanes\n\n')
            self.wText.AppendText(f'Total Lanes  : {len(self.rDataC.labelA)}\n')
            self.wText.AppendText(f'Lanes with FP: {infoDict["LanesWithFP"]}\n')
            self.wText.AppendText(f'Fragments    : {infoDict["Fragments"]}\n')
            self.wText.AppendText(f'Number of FP : {infoDict["FP"]}\n\n')
            self.wText.AppendText('--> Detected Protein Regions:\n\n')
            self.wText.AppendText('Recombinant Sequence:\n')
            self.wText.AppendText(f'{infoDict["NCO"]}'[1:-1]+'\n\n')
            self.wText.AppendText('Native Sequence:\n')
            self.wText.AppendText(f'{infoDict["NCONat"]}'[1:-1])
        else:
            self.wText.AppendText(f'There were no peptides from '
                f'{self.rDataC.targetProt} detected here.')

        self.wText.SetInsertionPoint(0)
        #endregion -------------------------------------------------> New Text

        return True
    #---

    def PrintLText(self, lane:int) -> bool:
        """Print information about a Lane.

            Parameters
            ----------
            lane: int
                Index of the selected lane in self.rDataC.labelA.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------> Get Values
        #------------------------------> Keys
        tKeys = [f'{x}-{self.rDataC.labelA[lane]}-{self.rPStr}' for x in self.rDataC.labelB]
        #------------------------------> Info
        infoDict = self.PrintLBGetInfo(tKeys)                                   # type: ignore
        #endregion -----------------------------------------------> Get Values

        #region -------------------------------------------------------> Clear
        self.wText.Clear()
        #endregion ----------------------------------------------------> Clear

        #region ----------------------------------------------------> New Text
        if infoDict:
            self.wText.AppendText(f'Details for {self.rDataC.labelA[lane]}\n\n')
            self.wText.AppendText('--> Analyzed Bands\n\n')
            self.wText.AppendText(f'Total Bands  : {len(self.rDataC.labelB)}\n')
            self.wText.AppendText(f'Bands with FP: {infoDict["LanesWithFP"]}\n')
            self.wText.AppendText(f'Fragments    : {infoDict["Fragments"]}\n')
            self.wText.AppendText(f'Number of FP : {infoDict["FP"]}\n\n')
            self.wText.AppendText('--> Detected Protein Regions:\n\n')
            self.wText.AppendText('Recombinant Sequence:\n')
            self.wText.AppendText(f'{infoDict["NCO"]}'[1:-1]+'\n\n')
            self.wText.AppendText('Native Sequence:\n')
            self.wText.AppendText(f'{infoDict["NCONat"]}'[1:-1])
        else:
            self.wText.AppendText(f'There were no peptides from '
                f'{self.rDataC.targetProt} detected here.')

        self.wText.SetInsertionPoint(0)
        #endregion -------------------------------------------------> New Text

        return True
    #---

    def PrintGelSpotText(self, x:int, y:int) -> bool:
        """Print information about a selected Gel spot.

            Parameters
            ----------
            x: int
                X coordinate of the selected Gel spot.
            y: int
                Y coordinate od the selected Gel spot

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        tKey = f'{self.rDataC.labelB[y]}-{self.rDataC.labelA[x]}-{self.rPStr}'
        frag = getattr(self.rFragments, tKey)
        #------------------------------>
        fragments = len(frag.coord)
        if fragments == 0:
            self.wText.Clear()
            self.wText.AppendText(
                f'Details for {self.rDataC.labelA[x]} - {self.rDataC.labelB[y]}\n\n')
            self.wText.AppendText(
                f'There were no peptides from {self.rDataC.targetProt} detected here.')
            return True
        #------------------------------>
        fp = (f'{sum(frag.np)} (' + f'{frag.np}'[1:-1] + ')')
        #------------------------------>
        if self.rDataC.protDelta is not None:
            ncONat = []
            for a,b in frag.coord:
                aX = a+self.rDataC.protDelta
                bX = b+self.rDataC.protDelta
                ncONat.append((aX,bX))
        else:
            ncONat = 'NA'
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        self.wText.Clear()
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        self.wText.AppendText(
            f'Details for {self.rDataC.labelA[x]} - {self.rDataC.labelB[y]}\n\n')
        self.wText.AppendText(f'--> Fragments: {fragments}\n\n')
        self.wText.AppendText(f'--> Number of FP: {fp}\n\n')
        self.wText.AppendText('--> Detected Protein Regions:\n\n')
        self.wText.AppendText('Recombinant Protein:\n')
        self.wText.AppendText(f'{frag.coord}'[1:-1]+'\n\n')
        self.wText.AppendText('Native Protein:\n')
        self.wText.AppendText(f'{ncONat}'[1:-1])

        self.wText.SetInsertionPoint(0)
        #endregion ------------------------------------------------>

        return True
    #---

    def PrintFragmentText(self, tKey:str, fragC:list[int]) -> bool:
        """Print information about a selected Fragment.

            Parameters
            ----------
            tKey: str
                String with the column name in the pd.DataFrame with the
                results.
            fragC: list[int]
                Fragment coordinates.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Info
        frag = getattr(self.rFragments, tKey)
        n, c = frag.coord[fragC[2]]
        #------------------------------>
        if self.rDataC.protLoc[0] > -1:
            if self.rDataC.protLoc[0] <= n <= self.rDataC.protLoc[1]:
                nnat = n + self.rDataC.protDelta
            else:
                nnat = 'NA'
        #------------------------------>
            if self.rDataC.protLoc[0] <= c <= self.rDataC.protLoc[1]:
                cnat = c + self.rDataC.protDelta
            else:
                cnat = 'NA'
        else:
            nnat = 'NA'
            cnat = 'NA'
        resNum = f'Nterm {n}({nnat}) - Cterm {c}({cnat})'
        #------------------------------>
        tNP    = (f'{frag.np[fragC[2]]} ({frag.npNat[fragC[2]]})')
        clSite = (f'{frag.nc[fragC[2]]} ({frag.ncNat[fragC[2]]})')
        #endregion ------------------------------------------------> Info

        #region --------------------------------------------------->
        self.wText.Clear()
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        self.wText.AppendText(
            f'Details for {self.rDataC.labelA[fragC[1]]} - {self.rDataC.labelB[fragC[0]]} - Fragment {fragC[2]+1}\n\n')
        self.wText.AppendText(f'Residue Numbers: {resNum}\n')
        self.wText.AppendText(f'Sequences: {tNP}\n')
        self.wText.AppendText(f'Cleavage Sites: {clSite}\n\n')
        self.wText.AppendText('Sequences in the fragment:\n\n')
        self.wText.AppendText(f'{frag.seq[fragC[2]]}')
        self.wText.SetInsertionPoint(0)
        #endregion ------------------------------------------------>

        return True
    #---

    def PrintAllText(self) -> bool:
        """Print text when the entire gel is selected.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        aSpot = len(self.rDataC.labelB)*len(self.rDataC.labelA)
        eSpot = self.rFragments.NumEmptyFrag()
        nPept = self.wLC.wLCS.wLC.GetItemCount()
        coord = self.SeqHighAll()
        coordN = cMethod.Rec2NatCoord(coord, self.rDataC.protLoc, self.rDataC.protDelta)
        if coordN[0] == 'NA':
            coordN = coordN[0]
        else:
            coordN = ', '.join(map(str,coordN))
        #endregion ------------------------------------------------> Variables

        #region --------------------------------------------------->
        self.wText.Clear()
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        self.wText.AppendText('Details for Gel\n\n')
        self.wText.AppendText('--> Analyzed Spots:\n\n')
        self.wText.AppendText(f'Analyzed Spots: {aSpot}\n')
        self.wText.AppendText(f'Empty Spots: {eSpot}\n')
        self.wText.AppendText(f'Detected Peptides: {nPept}\n\n')
        self.wText.AppendText('--> Detected Protein Regions:\n\n')
        self.wText.AppendText('Recombinant Sequence:\n')
        self.wText.AppendText(f'{", ".join(map(str,coord))}\n\n')
        self.wText.AppendText('Native Sequence:\n')
        self.wText.AppendText(f'{coordN}')
        self.wText.SetInsertionPoint(0)
        #endregion ------------------------------------------------>

        return True
    #---

    def PrintSeqPDF(self, fileP:Path) -> bool:
        """Print sequences to a PDF.

            Parameters
            ----------
            fileP: Path
                Path to the PDF file.

            Returns
            -------
            bool
        """
        def _helper(coord, label, style):
            """"""
            #------------------------------>
            head = Paragraph(label)
            #------------------------------>
            if coord:
                seq = self.GetPDFPrintSeq(coord)
                coordN = cMethod.Rec2NatCoord(coord, self.rDataC.protLoc, self.rDataC.protDelta)
                coord = Paragraph(
                    f"Recombinant protein: {', '.join(map(str,coord))}", style)
                coordN = Paragraph(
                    f"Native protein: {', '.join(map(str,coordN))}", style)
                tSeq = Paragraph(seq, style)
                return KeepTogether([head, Spacer(1,6), coord, coordN, tSeq])
            #------------------------------>
            empty = Paragraph('No peptides detected here.', style)
            return KeepTogether([head, Spacer(1,6), empty])
        #---
        #region ---------------------------------------------------> Variables
        doc = SimpleDocTemplate(fileP, pagesize=A4, rightMargin=25,
            leftMargin=25, topMargin=25, bottomMargin=25)
        Story  = []
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Seq', fontName='Courier', fontSize=8.5))
        #endregion ------------------------------------------------> Variables

        #region ---------------------------------------------------> Gel
        coord = self.SeqHighAll()
        Story.append(_helper(coord, 'Gel', styles['Seq']))
        Story.append(Spacer(1, 18))
        #endregion ------------------------------------------------> All

        #region ---------------------------------------------------> B/L
        for k,l in enumerate(self.rDataC.labelA):
            coord = self.SeqHighBL(bl=k)
            Story.append(_helper(coord, l, styles['Seq']))
            Story.append(Spacer(1, 18))
        #------------------------------>
        for k,b in enumerate(self.rDataC.labelB):
            coord = self.SeqHighBL(bb=k)
            Story.append(_helper(coord, b, styles['Seq']))
            Story.append(Spacer(1, 18))
        #endregion ------------------------------------------------> B/L

        #region ----------------------------------------------------> Gel Spot
        for j,l in enumerate(self.rDataC.labelA):
            for k,b in enumerate(self.rDataC.labelB):
                coord = self.SeqHighSpot(spot=[k,j])
                Story.append(_helper(coord,f'{l} - {b}', styles['Seq']))
                Story.append(Spacer(1, 18))
        #endregion -------------------------------------------------> Gel Spot

        doc.build(Story)
        return True
    #---

    def ShowPeptideLoc(self) -> bool:
        """Show the location of the selected peptide.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        for k in self.rRectsGel:
            k.set_linewidth(self.cGelLineWidth)
        #------------------------------>
        for k in self.rRectsFrag:
            k.set_linewidth(self.cGelLineWidth)
        #endregion ------------------------------------------------>

        #region ---------------------------------------------------> Gel
        j = 0
        for b in self.rDataC.labelB:
            for l in self.rDataC.labelA:
                frag = getattr(self.rFragments, f'{b}-{l}-{self.rPStr}')
                for p in frag.seqL:
                    if self.rPeptide in p:
                        self.rRectsGel[j].set_linewidth(2.0)
                        break
                j = j + 1
        #endregion ------------------------------------------------> Gel

        #region ---------------------------------------------------> Fragments
        fKeys = []
        #------------------------------>
        if self.rBlSelC != [None, None]:
            if self.rSelBands:
                for l in self.rDataC.labelA:
                    fKeys.append(f'{self.rDataC.labelB[self.rBlSelC[0]]}-{l}-{self.rPStr}')   # type: ignore
            else:
                for b in self.rDataC.labelB:
                    fKeys.append(f'{b}-{self.rDataC.labelA[self.rBlSelC[1]]}-{self.rPStr}')   # type: ignore
        else:
            for b in self.rDataC.labelB:
                for l in self.rDataC.labelA:
                    fKeys.append(f'{b}-{l}-{self.rPStr}')
        #------------------------------>
        if self.rRectsFrag:
            j = 0
            for k in fKeys:
                frag = getattr(self.rFragments, k)
                for p in frag.seqL:
                    if self.rPeptide in p:
                        self.rRectsFrag[j].set_linewidth(2.0)
                    j = j + 1
        #endregion ------------------------------------------------> Fragments

        #region --------------------------------------------------->
        self.wPlot['Sec'].rCanvas.draw()
        self.wPlot['Main'].rCanvas.draw()
        #endregion ------------------------------------------------>

        return True
    #---

    def UpdateGelColor(self, showAll=False) -> bool:
        """Update the Gel colors.

            Parameters
            ----------
            showAll: bool
                Show all fragments or not. Default is False.

            Returns
            -------
            bool
        """
        #------------------------------>
        j = 0
        #------------------------------>
        for nb,_ in enumerate(self.rDataC.labelB):
            for nl,_ in enumerate(self.rDataC.labelA):
                self.rRectsGel[j].set_facecolor(
                    self.SetGelSpotColor(nb,nl, showAll=showAll)
                )
                j = j + 1
        #------------------------------>
        self.wPlot['Sec'].rCanvas.draw()

        return True
    #---

    def SeqHighPept(self) -> bool:
        """Highlight the selected sequence in the wx.ListCtrl

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        seq = self.wLC.wLCS.wLC.GetItemText(
            self.wLC.wLCS.wLC.GetFirstSelected(), col=1)
        s = self.rRecSeqC.find(seq)
        self.rRecSeqColor['Blue']['Pept'] = [(s+1, s+len(seq))]
        #endregion ------------------------------------------------> Variables

        #region -------------------------------------------------------> Color
        self.RecSeqHighlight()
        #endregion ----------------------------------------------------> Color

        return True
    #---

    def SeqHighSpot(
        self,
        spot:Optional[list[int]]=None,
        ) -> list[tuple[int, int]]:
        """Highlight the sequences in the selected Gel spot.

            Returns
            -------
            list[tuple[int, int]]
        """
        #region ---------------------------------------------------> Variables
        self.rRecSeqColor['Blue']['Frag'] = []
        #------------------------------>
        if spot is None:
            b,l = self.rGelSelC
        else:
            b,l = spot
        tKey = f'{self.rDataC.labelB[b]}-{self.rDataC.labelA[l]}-{self.rPStr}'                # type: ignore
        #endregion ------------------------------------------------> Variables

        return cMethod.MergeOverlappingFragments(
            getattr(self.rFragments, tKey).coord)
    #---

    def SeqHighFrag(
        self,
        frag:Optional[list[int]]=None,
        ) -> list[tuple[int, int]]:
        """Highlight the sequences in the selected Fragment.

            Returns
            -------
            list[tuple[int, int]]
        """
        #region ---------------------------------------------------> Variables
        self.rRecSeqColor['Blue']['Spot'] = []
        #------------------------------>
        if frag is None:
            b,l,j = self.rFragSelC
        else:
            b,l,j = frag
        tKey = f'{self.rDataC.labelB[b]}-{self.rDataC.labelA[l]}-{self.rPStr}'                       # type: ignore
        #endregion ------------------------------------------------> Variables

        return cMethod.MergeOverlappingFragments(
            [getattr(self.rFragments, tKey).coord[j]])
    #---

    def SeqHighBL(
        self,
        bb:Optional[int]=None,
        bl:Optional[int]=None,
        ) -> list[tuple[int, int]]:
        """Highlight the sequences in the selected Band/Lane.

            Returns
            -------
            list[tuple[int, int]]
        """
        #region ---------------------------------------------------> Variables
        if bb is None and bl is None:
            b, l = self.rBlSelC
        else:
            b, l = bb, bl
        #------------------------------>
        if b is not None:
            bN = self.rDataC.labelB[b]
            tKey = [f'{bN}-{l}-{self.rPStr}' for l in self.rDataC.labelA]
        else:
            lN = self.rDataC.labelA[l]                                                 # type: ignore
            tKey = [f'{b}-{lN}-{self.rPStr}' for b in self.rDataC.labelB]
        #endregion ------------------------------------------------> Variables

        #region ---------------------------------------------------> Seqs
        self.rRecSeqColor['Red'] = []
        #------------------------------>
        seqL = []
        for k in tKey:
            frag = getattr(self.rFragments, k)
            seqL = seqL + frag.coord
        #endregion ------------------------------------------------> Seqs

        return cMethod.MergeOverlappingFragments(list(set(seqL)))
    #---

    def SeqHighAll(self) -> list[tuple[int, int]]:
        """Highlight the sequences in all Bands/Lanes

            Returns
            -------
            list(tuple(int, int))
                All detected fragments in the gel
        """
        #region ---------------------------------------------------> Seqs
        self.rRecSeqColor['Red'] = []
        #------------------------------>
        pept = self.wLC.wLCS.wLC.GetColContent(1)
        #------------------------------>
        resN = []
        for p in pept:
            s = self.rRecSeqC.find(p)
            resN.append((s+1, s+len(p)))
        #endregion ------------------------------------------------> Seqs

        return cMethod.MergeOverlappingFragments(resN, 1)
    #---

    def RecSeqHighlight(self) -> bool:
        """Apply the colors to the recombinant sequence.

            Returns
            -------
            bool
        """
        #region -------------------------------------------------------> Reset
        self.wTextSeq.SetStyle(
            0, self.wTextSeq.GetLastPosition(), self.rTextStyleDef)
        #endregion ----------------------------------------------------> Reset

        #region ---------------------------------------------------> Variables
        styleRed = wx.TextAttr('RED', font=self.rTextStyleDef.GetFont())
        styleRed.SetFontWeight(wx.FONTWEIGHT_BOLD)
        styleBlue = wx.TextAttr('BLUE', font=self.rTextStyleDef.GetFont())
        styleBlue.SetFontWeight(wx.FONTWEIGHT_BOLD)
        #endregion ------------------------------------------------> Variables

        #region -------------------------------------------------------> Color
        for p in self.rRecSeqColor['Red']:
            self.wTextSeq.SetStyle(p[0]-1, p[1], styleRed)
        #------------------------------>
        for _,v in self.rRecSeqColor['Blue'].items():
            for p in v:
                self.wTextSeq.SetStyle(p[0]-1, p[1], styleBlue)
        #endregion ----------------------------------------------------> Color

        return True
    #---

    def SeqExport(self) -> bool:
        """Export the recombinant sequence alignments.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> wx.Dialog
        dlg = cWindow.FileSelect('save', mConfig.core.elPDF, parent=self)
        if dlg.ShowModal():
            self.PrintSeqPDF(dlg.GetPath())
        #endregion ------------------------------------------------> wx.Dialog

        dlg.Destroy()
        return True
    #---

    def GetPDFPrintSeq(self, region:list[tuple[int,int]]) -> str:
        """Get the correct colors for the sequence.

            Parameters
            ----------
            region: list[tuple[int, int]]
                Sequence regions to highlight.

            Returns
            -------
            str
        """
        #region ---------------------------------------------------> Variables
        black = []
        blue  = []
        #endregion ------------------------------------------------> Variables

        #region ---------------------------------------------------> Parts
        try:
            a,b = region[0]
        except IndexError:
            return self.rRecSeqC
        #------------------------------>
        black.append(self.rRecSeqC[0:a-1])
        blue.append(self.rRecSeqC[a-1:b])
        #------------------------------>
        for ac,bc in region[1:]:
            black.append(self.rRecSeqC[b:ac-1])
            blue.append(self.rRecSeqC[ac-1:bc])
            a, b = ac, bc
        #------------------------------>
        black.append(self.rRecSeqC[b:])
        #endregion ------------------------------------------------> Parts

        #region ---------------------------------------------------> Colors
        sO = ''
        for bl,bs in zip_longest(black,blue):
            if bl:
                sO = sO+f'<font color="black">{bl}</font>'
            if bs:
                sO = sO+f'<font color="red">{bs}</font>'
        #endregion ------------------------------------------------> Colors

        return sO
    #---

    def ClearPept(self, plot:bool=True) -> bool:
        """Clear the Peptide selection.

            Parameters
            ----------
            plot: bool
                Redraw the canvas.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        self.rPeptide = None
        self.rLCIdx   = None
        self.rRecSeqColor['Blue']['Pept'] = []
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        if (rID := self.wLC.wLCS.wLC.GetFirstSelected()) > -1:
            self.wLC.wLCS.wLC.Select(rID, on=0)
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        for r in self.rRectsFrag:
            r.set_linewidth(self.cGelLineWidth)

        for r in self.rRectsGel:
            r.set_linewidth(self.cGelLineWidth)
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        if plot:
            self.wPlot['Main'].rCanvas.draw()
            self.wPlot['Sec'].rCanvas.draw()
            self.RecSeqHighlight()
        #endregion ------------------------------------------------>

        return True
    #---

    def ClearFrag(self, plot=True) -> bool:
        """Clear the Fragment selection.

            Parameters
            ----------
            plot: bool
                Redraw the canvas.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        self.rRecSeqColor['Blue']['Frag'] = []
        #------------------------------>
        if self.rFragSelLine is not None:
            self.rFragSelLine[0].remove()
            self.rFragSelLine = None
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        if plot:
            #------------------------------>
            self.wPlot['Main'].rCanvas.draw()
            #------------------------------>
            if self.rFragSelC != [None, None, None]:
                self.wText.Clear()
                #------------------------------> To test for showAll
                if any(self.rGelSelC):
                    if self.rSelBands:
                        self.PrintBText(self.rBlSelC[0])                        # type: ignore
                    else:
                        self.PrintLText(self.rBlSelC[1])                        # type: ignore
            #------------------------------>
            self.RecSeqHighlight()
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        self.rFragSelC = [None, None, None]
        #endregion ------------------------------------------------>

        return True
    #---

    def ClearGel(self, plot=True) -> bool:
        """Clear the Gel spot selection.

            Parameters
            ----------
            plot: bool
                Redraw the canvas.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        self.rRecSeqColor['Blue']['Spot'] = []
        #------------------------------>
        if self.rSpotSelLine is not None:
            self.rSpotSelLine[0].remove()
            self.rSpotSelLine = None
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        if plot:
            #------------------------------>
            self.wPlot['Sec'].rCanvas.draw()
            #------------------------------>
            if self.rGelSelC != [None, None]:
                self.wText.Clear()
                #------------------------------>
                if self.rSelBands:
                    self.PrintBText(self.rBlSelC[0])                            # type: ignore
                else:
                    self.PrintLText(self.rBlSelC[1])                            # type: ignore
            #------------------------------>
            self.RecSeqHighlight()
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        self.rGelSelC = [None, None]
        #endregion ------------------------------------------------>

        return True
    #---

    def ClearBL(self, plot=True) -> bool:
        """Clear the Band/Lane selection.

            Parameters
            ----------
            plot: bool
                Redraw the canvas.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        self.rRecSeqColor['Red'] = []
        self.rRecSeqColor['Blue']['Frag'] = []
        self.SetEmptyFragmentAxis()
        self.ClearGel(plot=False)
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        if self.rBlSelRect is not None:
            self.rBlSelRect.remove()
            self.rBlSelRect = None
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        if plot:
            self.wPlot['Sec'].rCanvas.draw()
            self.wText.Clear()
            self.RecSeqHighlight()
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        self.rBlSelC = [None, None]
        self.rRectsFrag = []
        #endregion ------------------------------------------------>

        return True
    #---

    def ClearAll(self) -> bool:
        """Clear all selections.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        self.ClearPept(plot=False)
        self.ClearFrag(plot=False)
        self.ClearGel(plot=False)
        self.ClearBL(plot=False)
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        self.wPlot['Main'].rCanvas.draw()
        self.wPlot['Sec'].rCanvas.draw()
        self.RecSeqHighlight()
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        self.wText.Clear()
        #endregion ------------------------------------------------>

        return True
    #---
    #endregion -----------------------------------------------> Manage Methods

    #region ---------------------------------------------------> Event Methods
    def OnListSelect(self, event:Union[wx.CommandEvent, str]) -> bool:
        """Process a wx.ListCtrl select event.

            Parameters
            ----------
            event:wx.Event
                Information about the event


            Returns
            -------
            bool
        """
        super().OnListSelect(event)
        self.SeqHighPept()
        return True
    #---

    def OnPickFragment(self, event) -> bool:
        """Display info about the selected fragment.

            Parameters
            ----------
            event: matplotlib pick event.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        art   = event.artist
        fragC = list(map(int, art.get_label().split('.')))
        #------------------------------>
        if self.rFragSelC != fragC:
            self.rFragSelC = fragC
        else:
            return True
        #------------------------------>
        x, y = event.artist.xy
        x = round(x)
        y = round(y)
        #------------------------------>
        tKey = f'{self.rDataC.labelB[fragC[0]]}-{self.rDataC.labelA[fragC[1]]}-{self.rPStr}'
        #------------------------------>
        frag = getattr(self.rFragments, tKey)
        x1, x2 = frag.coord[fragC[2]]
        #endregion ------------------------------------------------> Variables

        #region ------------------------------------------> Highlight Fragment
        if self.rFragSelLine is not None:
            self.rFragSelLine[0].remove()
        #------------------------------>
        self.rFragSelLine = self.wPlot['Main'].rAxes.plot(
            [x1+2, x2-2], [y,y], color='black', linewidth=4)
        #------------------------------>
        self.wPlot['Main'].rCanvas.draw()
        #endregion ---------------------------------------> Highlight Fragment

        #region -------------------------------------------------------> Print
        self.PrintFragmentText(tKey, fragC)
        #endregion ----------------------------------------------------> Print

        #region -------------------------------------------> Remove Sel in Gel
        if self.rSpotSelLine is not None:
            self.rSpotSelLine[0].remove()
            self.rSpotSelLine = None
            self.wPlot['Sec'].rCanvas.draw()
            self.rGelSelC = [None, None]
        #endregion ----------------------------------------> Remove Sel in Gel

        #region -----------------------------------------------------> Rec Seq
        self.rRecSeqColor['Blue']['Frag'] = self.SeqHighFrag()
        self.RecSeqHighlight()
        #endregion --------------------------------------------------> Rec Seq

        return True
    #---

    def OnPickGel(self, event) -> bool:
        """Display info about the selected Gel spot.

            Parameters
            ----------
            event: matplotlib pick event.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        x, y = event.artist.xy
        x = round(x)
        y = round(y)
        #endregion ------------------------------------------------> Variables

        #region -------------------------------------------------> Flag picked
        self.rGelSpotPicked = True
        #endregion ----------------------------------------------> Flag picked

        #region -----------------------------------------------> Spot Selected
        spotC = [y-1, x-1]
        if self.rGelSelC != spotC:
            self.rGelSelC = spotC
        else:
            self.PrintGelSpotText(x-1,y-1)
            return True
        #endregion --------------------------------------------> Spot Selected

        #region ---------------------------------------------> Remove Old Line
        if self.rSpotSelLine is not None:
            self.rSpotSelLine[0].remove()
        #endregion ------------------------------------------> Remove Old Line

        #region -----------------------------------------------> Draw New Line
        self.rSpotSelLine = self.wPlot['Sec'].rAxes.plot(
            [x-0.3, x+0.3], [y,y], color='black', linewidth=4)
        #------------------------------>
        self.wPlot['Sec'].rCanvas.draw()
        #endregion --------------------------------------------> Draw New Line

        #region --------------------------------------------------------> Info
        self.PrintGelSpotText(x-1,y-1)
        #endregion -----------------------------------------------------> Info

        #region ----------------------------------------> Remove Sel from Frag
        if self.rFragSelLine is not None:
            self.rFragSelLine[0].remove()
            self.rFragSelLine = None
            self.wPlot['Main'].rCanvas.draw()
            self.rFragSelC = [None, None, None]
        #endregion -------------------------------------> Remove Sel from Frag

        #region --------------------------------------------------->
        if self.rUpdateColors:
            self.UpdateGelColor()
            self.rUpdateColors = False
        #endregion ------------------------------------------------>

        #region -----------------------------------------------------> Rec Seq
        self.rRecSeqColor['Blue']['Spot'] = self.SeqHighSpot()
        self.RecSeqHighlight()
        #endregion --------------------------------------------------> Rec Seq

        return True
    #---

    def OnPressMouse(self, event) -> bool:
        """Press mouse event in the Gel.

            Parameters
            ----------
            event: wx.Event
                Information about the event.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> In axis
        if not event.inaxes:
            return False
        #endregion ------------------------------------------------> In axis

        #region ---------------------------------------------------> Variables
        x = round(event.xdata)
        y = round(event.ydata)
        #endregion ------------------------------------------------> Variables

        #region -----------------------------------------------> Redraw or Not
        if self.rGelSpotPicked:
            self.rGelSpotPicked = False
            return True
        #------------------------------>
        blSel = [y-1, x-1]
        #------------------------------> Update sel curr or print again
        if self.rSelBands and self.rBlSelC[0] != blSel[0]:
            self.rBlSelC = [blSel[0], None]
        elif not self.rSelBands and self.rBlSelC[1] != blSel[1]:
            self.rBlSelC = [None, blSel[1]]
        else:
            self.PrintBLText(x-1,y-1)
            return True
        #endregion --------------------------------------------> Redraw or Not

        #region -----------------------------------------------> Draw New Rect
        self.DrawBLRect(x,y)
        #endregion --------------------------------------------> Draw New Rect

        #region ----------------------------------------------> Draw Fragments
        self.DrawFragments(x,y)
        #endregion -------------------------------------------> Draw Fragments

        #region ---------------------------------------------------> Print
        self.PrintBLText(x-1,y-1)
        #endregion ------------------------------------------------> Print

        #region --------------------------------------------------->
        if self.rUpdateColors:
            self.UpdateGelColor()
            self.rUpdateColors = False
        #endregion ------------------------------------------------>

        #region ---------------------------------------------------> Rec Seq
        self.rRecSeqColor['Red'] = self.SeqHighBL()
        self.RecSeqHighlight()
        #endregion ------------------------------------------------> Rec Seq

        return True
    #---
    #endregion ------------------------------------------------> Event Methods
#---
#endregion ----------------------------------------------------------> Classes
