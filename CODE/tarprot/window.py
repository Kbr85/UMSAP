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


"""Windows for the tarprot module of the app"""


#region -------------------------------------------------------------> Imports
import _thread
from pathlib import Path
from typing  import Optional, TYPE_CHECKING

import pandas as pd

import matplotlib.patches as mpatches

from Bio       import pairwise2
from Bio.Align import substitution_matrices

import wx

from config.config import config as mConfig
from core    import file      as cFile
from core    import method    as cMethod
from core    import validator as cValidator
from core    import window    as cWindow
from main    import menu      as mMenu
from tarprot import method    as tarpMethod

if TYPE_CHECKING:
    from result import window as resWindow
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Classes
class ResTarProt(cWindow.BaseWindowResultListText2PlotFragments):
    """Plot the results of a Targeted Proteolysis analysis.

        Parameters
        ----------
        parent: wx.Window
            Parent of the window.

        Attributes
        ----------
        rCorrP: bool
            Show P corrected values (True) or regular values (False).
        rData: cMethod.BaseAnalysis
            For each Targeted Proteolysis analysis a new attribute 'Date-ID' is
            added with value tarpMethod.TarpAnalysis.
        rDate: list[str]
            Dates for the analysis
        rDateC: str
            Current Date.
        rDf: pd.DataFrame
            Copy of the data used to plot
        rFragments: cMethod.Fragment
            Class with the info for the fragments. See cMethod.Fragment.
        rFragSelC: list[band, lane, fragment]
            Coordinates for the currently selected fragment. 0 based.
        rFragSelLine: matplotlib line
            Line to highlight the currently selected fragment.
        rIdxP: pd.IndexSlice
            To access the P columns in the data frame.
        rLCIdx: int
            Row selected in the wx.ListCtrl.
        rNatSeqC: str
            Sequence of the current native protein.
        rObj: UMSAPFile
            Reference to the UMSAP file in the parent UMSAPCtrl window.
        rPeptide: str
            Sequence of the selected peptide in the wx.ListCtrl.
        rPStr: str
            Name of the P column in the dataframe.
        rRecSeq: dict
            Keys are date and values a list with the sequence of the recombinant
            and native protein.
        rRecSeqC: list[str]
            Sequence of the recombinant and native protein for the current date.
     """
    #region -----------------------------------------------------> Class setup
    cName    = mConfig.tarp.nwRes
    cSection = mConfig.tarp.tMod
    #------------------------------> Label
    cLPaneSec = 'Intensity'
    #------------------------------>
    cSWindow = (1100, 800)
    #------------------------------>
    cImgName   = {
        mConfig.core.kwMain: '{}-Protein-Fragments.{}',
        mConfig.core.kwSec : '{}-Intensity-Representation.{}',
    }
    #------------------------------>
    cFragment = mConfig.core.cFragment
    cCtrl     = mConfig.tarp.cCtrl
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent:'resWindow.UMSAPControl') -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.cTitle = f'{parent.cTitle} - {self.cSection}'
        self.rObj   = parent.rObj
        self.rData:cMethod.BaseAnalysis = self.rObj.dConfigure[self.cSection]()
        self.rDate, menuData = self.SetDateMenuDate()
        self.rCorrP = False
        self.rCCtrl = mConfig.tarp.cCtrl
        self.rCAve  = mConfig.tarp.cAve
        self.rCAveL = mConfig.tarp.cAveL
        #------------------------------>
        self.ReportPlotDataError()
        #------------------------------>
        self.rDateC  = self.rDate[0]
        self.rDataC:tarpMethod.TarpAnalysis = getattr(self.rData, self.rDateC)
        self.rRecSeq = {}
        #------------------------------>
        super().__init__(parent)
        #------------------------------>
        dKeyMethod = {
            mConfig.tarp.kwClearPeptide : self.ClearPept,
            mConfig.tarp.kwClearFragment: self.ClearFrag,
            mConfig.tarp.kwClearAll     : self.ClearAll,
            #------------------------------>
            'AA-Item'                      : self.AASelect,
            'AA-New'                       : self.AANew,
            'Hist-Item'                    : self.HistSelect,
            'Hist-New'                     : self.HistNew,
            mConfig.tarp.kwFACleavageEvol  : self.CEvol,
            mConfig.tarp.kwFACleavagePerRes: self.CpR,
            mConfig.tarp.kwFAPDBMap        : self.PDBMap,
        }
        self.dKeyMethod = self.dKeyMethod | dKeyMethod
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------------> Menu
        self.mBar = mMenu.MenuBarTool(self.cName, menuData=menuData)
        self.SetMenuBar(self.mBar)
        #endregion -----------------------------------------------------> Menu

        #region ---------------------------------------------> Window position
        self.UpdateResultWindow()
        self.WinPos()
        self.Show()
        #endregion ------------------------------------------> Window position
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class Methods
    def PickFragment(self, event) -> bool:
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
        tKey = f'{self.rDataC.labelA[fragC[0]]}-{self.rPStr}'
        #------------------------------>
        x1, x2 = getattr(self.rFragments, tKey).coord[fragC[1]]
        #endregion ------------------------------------------------> Variables

        #region ------------------------------------------> Highlight Fragment
        if self.rFragSelLine is not None:
            self.rFragSelLine[0].remove()
        #------------------------------
        self.rFragSelLine = self.wPlot['Main'].rAxes.plot(
            [x1+2, x2-2], [y,y], color='black', linewidth=4)
        #------------------------------>
        self.wPlot['Main'].rCanvas.draw()
        #endregion ---------------------------------------> Highlight Fragment

        #region -------------------------------------------------------> Print
        self.PrintFragmentText(tKey, fragC)
        #endregion ----------------------------------------------------> Print

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
        info = super().WinPos()                                                 # pylint: disable=unused-variable
        #endregion ------------------------------------------------> Variables

        #region ------------------------------------------------> Set Position
        # x = info['D']['xo'] + info['W']['N']*config.deltaWin
        # y = (
        #     ((info['D']['h']/2) - (info['W']['h']/2))
        #     + info['W']['N']*config.deltaWin
        # )
        # self.SetPosition(pt=(x,y))
        #endregion ---------------------------------------------> Set Position

        return True
    #---

    def SetDateMenuDate(self) -> tuple[list, dict]:
        """Set the self.rDate list and the menuData dict needed to build the
            Tool menu.

            Returns
            -------
            tuple of list and dict
            The list is a list of str with the dates in the analysis.
            The dict has the following structure:
                {
                    'MenuDate' : [List of dates],
                }
        """
        #region ---------------------------------------------------> Fill dict
        #------------------------------> Variables
        date = self.rData.date
        menuData = {
            'MenuDate': [],
            'FA'      : {},
        }
        #------------------------------> Fill
        for k in self.rData.date:
            data = getattr(self.rData, k)
            aa   = data.AA
            hist = data.Hist
            menuData['FA'][k] = {}
            menuData['FA'][k]['AA']   = list(aa.keys())
            menuData['FA'][k]['Hist'] = list(hist.keys())
        #------------------------------>
        menuData['MenuDate'] = date
        #endregion ------------------------------------------------> Fill dict

        return (date, menuData)
    #---

    def UpdateResultWindow(                                                     # pylint: disable=arguments-differ
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
        self.rDateC       = tDate if tDate else self.rDateC
        self.rDataC       = getattr(self.rData, self.rDateC)
        self.rDf          = self.rDataC.df.copy()
        self.rFragSelLine = None
        self.rFragSelC    = [None, None, None]
        self.rCorrP       = corrP if corrP is not None else self.rCorrP
        self.rPStr        = 'Pc' if self.rCorrP else 'P'
        self.rIdxP        = pd.IndexSlice[self.rDataC.labelA,'Pc'] if self.rCorrP else pd.IndexSlice[self.rDataC.labelA,'P']
        self.rPeptide     = None
        self.rRecSeqC, self.rNatSeqC = (
            self.rRecSeq.get(self.rDateC)
            or
            self.rObj.GetSeq(self.cSection, self.rDateC)
        )
        self.rRecSeq[self.rDateC] = (self.rRecSeqC, self.rNatSeqC)
        #endregion ------------------------------------------------> Variables

        #region --------------------------------------------------->
        self.wText.Clear()
        #endregion ------------------------------------------------>

        #region ---------------------------------------------------> Fragments
        try:                                                                    # Keep backward compatibility
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
                raise Exception from e
            #------------------------------> Reset attributes
            self.rCorrP = False
            self.rPStr  = 'P'
            self.rIdxP  = pd.IndexSlice[self.rDataC.labelA,'P']
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
            self.rDataC.protLoc,
        )
        #------------------------------>
        self.DrawFragments()
        #endregion ------------------------------------------------> Fragments

        #region -------------------------------------------------> wx.ListCtrl
        self.FillListCtrl()
        #endregion ----------------------------------------------> wx.ListCtrl

        #region -----------------------------------------------------> Peptide
        self.SetAxisInt()
        self.wPlot['Sec'].rCanvas.draw()
        self.wPlot['Sec'].ZoomResetSetValues()
        #endregion --------------------------------------------------> Peptide

        #region ---------------------------------------------------> Win Title
        self.PlotTitle()
        #endregion ------------------------------------------------> Win Title

        return True
    #---

    def DrawFragments(self) -> bool:                                            # pylint: disable=arguments-differ
        """Draw the fragments associated with the date.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        tKeyLabel = {}
        #endregion ------------------------------------------------> Variables

        #region --------------------------------------------------------> Keys
        for k,v in enumerate(self.rDataC.labelA):
            tKeyLabel[f'{v}-{self.rPStr}'] = f'{k}'
        #endregion -----------------------------------------------------> Keys

        #region -------------------------------------------------------> Super
        super().DrawFragments(tKeyLabel)
        #endregion ----------------------------------------------------> Super

        return True
    #---

    def SetFragmentAxis(self) -> bool:                                          # pylint: disable=arguments-differ
        """Set the axis for the plot showing the fragments.

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
        self.wPlot['Main'].rAxes.set_yticks(range(1, len(self.rDataC.labelA)+2))
        self.wPlot['Main'].rAxes.set_yticklabels(self.rDataC.labelA+['Protein'])
        self.wPlot['Main'].rAxes.set_ylim(0.5, len(self.rDataC.labelA)+1.5)
        #------------------------------>
        ymax = len(self.rDataC.labelA)+0.8
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

    def ShowPeptideLoc(self) -> bool:
        """Show the location of the selected peptide.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Fragments
        #------------------------------> Remove old
        for k in self.rRectsFrag:
            k.set_linewidth(self.cGelLineWidth)
        #------------------------------> Get Keys
        fKeys = [f'{x}-{self.rPStr}' for x in self.rDataC.labelA]
        #------------------------------> Highlight
        j = 0
        for k in fKeys:
            frag = getattr(self.rFragments, k)
            for p in frag.seqL:
                if self.rPeptide in p:
                    self.rRectsFrag[j].set_linewidth(2.0)
                else:
                    pass
                j = j + 1
        #------------------------------> Show
        self.wPlot['Main'].rCanvas.draw()
        #endregion ------------------------------------------------> Fragments

        #region ---------------------------------------------------> Intensity
        #------------------------------> Variables
        nc = len(self.cFragment)                                                # type: ignore
        #------------------------------> Clear Plot
        self.wPlot['Sec'].rAxes.clear()
        #------------------------------> Axis
        self.SetAxisInt()
        #------------------------------> Row
        row = self.rDf.loc[self.rDf[('Sequence', 'Sequence')] == self.rPeptide]
        row =row.loc[:,pd.IndexSlice[:,('Int','P')]]                            # type: ignore
        #------------------------------> Values
        x = []
        y = []
        for k,c in enumerate(self.rDataC.ctrlName+self.rDataC.labelA, start=1):
            #------------------------------> Variables
            intL, P = row[c].values.tolist()[0]
            intL = list(map(float, intL[1:-1].split(',')))
            P = float(P)
            intN = len(intL)
            #------------------------------> Color, x & y
            if k == 1:
                color = self.rCCtrl                                             # type: ignore
                x = [1]
                y = [sum(intL)/intN]
            else:
                color = self.cFragment[(k-2)%nc]                                # type: ignore
            #------------------------------> Ave
            if P <= self.rDataC.alpha:
                x.append(k)
                y.append(sum(intL)/intN)
            else:
                pass
            #------------------------------> Plot
            self.wPlot['Sec'].rAxes.scatter(
                intN*[k], intL, color=color, edgecolor='black', zorder=3)
        #------------------------------>
        self.wPlot['Sec'].rAxes.scatter(
            x,
            y,
            edgecolor = 'black',
            marker    = 'D',
            color     = self.rCAve,
            s         = 120,
            zorder    = 2,
        )
        self.wPlot['Sec'].rAxes.plot(x,y, zorder=1, color=self.rCAveL)
        #------------------------------> Show
        self.wPlot['Sec'].ZoomResetSetValues()
        self.wPlot['Sec'].rCanvas.draw()
        #endregion ------------------------------------------------> Intensity

        return True
    #---

    def SetAxisInt(self) -> bool:
        """Set the axis of the Intensity plot.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        nExp = len(self.rDataC.labelA)
        #endregion ------------------------------------------------> Variables

        #region ------------------------------------------------------> Values
        self.wPlot['Sec'].rAxes.clear()
        self.wPlot['Sec'].rAxes.set_xticks(range(1,nExp+2))
        self.wPlot['Sec'].rAxes.set_xticklabels(self.rDataC.ctrlName+self.rDataC.labelA)
        #------------------------------>
        self.wPlot['Sec'].rAxes.set_xlim(0.5, nExp+1.5)
        #------------------------------>
        self.wPlot['Sec'].rAxes.set_ylabel('Intensity (after DP)')
        #endregion ---------------------------------------------------> Values

        return True
    #---

    def PrintFragmentText(self, tKey:str, fragC:list[int]) -> bool:
        """Print information about a selected Fragment.

            Parameters
            ----------
            tKey: tuple(str, str)
                Tuple with the column name in the pd.DataFrame with the results.
            fragC: list[int]
                Fragment coordinates.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Info
        fragData = getattr(self.rFragments, tKey)
        #------------------------------> Fragments
        frag =  f'{fragData.nFrag[0]}({fragData.nFrag[1]})'
        clSiteExp = (f'{fragData.nCT[0]}({fragData.nCT[1]})')
        seqExp = (f'{sum(fragData.np)}({sum(fragData.npNat)})')
        #------------------------------> Res Numbers
        n, c = fragData.coord[fragC[1]]
        nf, cf = fragData.coordN[fragC[1]]
        #------------------------------> Sequences
        tNP = (f'{fragData.np[fragC[1]]}({fragData.npNat[fragC[1]]})')
        #------------------------------> Cleavages
        clSite = (f'{fragData.nc[fragC[1]]}({fragData.ncNat[fragC[1]]})')
        #------------------------------> Labels
        expL, fragL = cMethod.StrEqualLength(                                   # pylint: disable=unbalanced-tuple-unpacking
            [self.rDataC.labelA[fragC[0]], f'Fragment {fragC[1]+1}'])
        emptySpace = (2+ len(expL))*' '
        #endregion ------------------------------------------------> Info

        #region --------------------------------------------------->
        self.wText.Clear()
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        self.wText.AppendText(
            f'Details for {self.rDataC.labelA[fragC[0]]} - Fragment {fragC[1]+1}\n\n')
        self.wText.AppendText(f'{expL}: Fragments {frag}, Cleavage sites {clSiteExp}\n')
        self.wText.AppendText(f'{emptySpace}Peptides {seqExp}\n\n')
        self.wText.AppendText(f'{fragL}: Nterm {n}({nf}), Cterm {c}({cf})\n')
        self.wText.AppendText(f'{emptySpace}Peptides {tNP}, Cleavage sites {clSite}\n\n')
        self.wText.AppendText('Sequences in the fragment:\n\n')
        self.wText.AppendText(f'{fragData.seq[fragC[1]]}')
        self.wText.SetInsertionPoint(0)
        #endregion ------------------------------------------------>

        return True
    #---

    def SeqExport(self) -> bool:
        """Export the sequence alignment.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> dlg
        dlg = cWindow.FABtnText(
            'File',
            'Path to the output file',
            mConfig.core.elPDF,
            cValidator.OutputFF('file'),
            'Length',
            'Residues per line in the output file, e.g. 100',
            cValidator.NumberList('int', vMin=1, vMax=100, nN=1),
            parent = self,
        )
        #endregion ------------------------------------------------> dlg

        #region ---------------------------------------------------> Get Pos
        if dlg.ShowModal():
            fileP  = dlg.wBtnTc.wTc.GetValue()
            length = int(dlg.wLength.wTc.GetValue())
        else:
            dlg.Destroy()
            return False
        #endregion ------------------------------------------------> Get Pos

        #region ---------------------------------------------------> Run
        tarpMethod.R2SeqAlignment(
            self.rDf,
            self.rDataC.alpha,
            self.rRecSeqC,
            fileP,
            length,
            self.rNatSeqC,
        )
        #endregion ------------------------------------------------> Run

        dlg.Destroy()
        return True
    #---

    def ClearPept(self, plot:bool=True) -> bool:
        """Clear the Peptide selection. Method called from menu.

            Parameters
            ----------
            plot: bool
                Redraw the canvas.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        if (rID := self.wLC.wLCS.wLC.GetFirstSelected()):
            self.wLC.wLCS.wLC.Select(rID, on=0)
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        for r in self.rRectsFrag:
            r.set_linewidth(self.cGelLineWidth)
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        if plot:
            self.wPlot['Main'].rCanvas.draw()
            self.SetAxisInt()
            self.wPlot['Sec'].rCanvas.draw()
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        self.rPeptide = None
        self.rLCIdx = None
        #endregion ------------------------------------------------>

        return True
    #---

    def ClearFrag(self, plot=True) -> bool:
        """Clear the Fragment selection. Method called from Menu.

            Parameters
            ----------
            plot: bool
                Redraw the canvas.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        if self.rFragSelLine is not None:
            self.rFragSelLine[0].remove()
            self.rFragSelLine = None
            if plot:
                self.wPlot['Main'].rCanvas.draw()
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        self.wText.Clear()
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        self.rFragSelC = [None, None]
        #endregion ------------------------------------------------>

        return True
    #---

    def ClearAll(self) -> bool:
        """Clear all selections. Method called from menu.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        self.ClearPept(plot=False)
        self.ClearFrag(plot=False)
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        self.wPlot['Main'].rCanvas.draw()
        self.SetAxisInt()
        self.wPlot['Sec'].rCanvas.draw()
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        self.wText.Clear()
        #endregion ------------------------------------------------>

        return True
    #---

    def AANew(self) -> bool:
        """Perform a new AA analysis. Method called from Menu.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> dlg
        dlg = cWindow.UserInputText(
            'New AA Distribution Analysis',
            ['Positions'],
            ['Number of residues around the cleavage site to consider, e.g. 5'],
            parent    = self,
            validator = [cValidator.NumberList('int', vMin=1, nN=1)],
        )
        #endregion ------------------------------------------------> dlg

        #region ---------------------------------------------------> Get Pos
        if dlg.ShowModal():
            pos = int(dlg.rInput[0].wTc.GetValue())
            dateC = cMethod.StrNow()
        else:
            dlg.Destroy()
            return False
        #endregion ------------------------------------------------> Get Pos

        #region ---------------------------------------------------> Run
        dfI = self.rDataC.df
        idx = pd.IndexSlice
        dfI = dfI.loc[:,idx[['Sequence']+self.rDataC.labelA,['Sequence', 'P']]] # type: ignore
        dfO = tarpMethod.R2AA(
            dfI, self.rRecSeqC, self.rDataC.alpha, self.rDataC.protLength[0], pos=pos)
        #endregion ------------------------------------------------> Run

        #region -----------------------------------------------> Save & Update
        #------------------------------> File
        date    = f'{self.rDateC.split(" - ")[0]}'
        section = f'{self.cSection.replace(" ", "-")}'
        folder  = f'{date}_{section}'
        fileN   = f'{dateC}_AA-{pos}.txt'
        fileP   = self.rObj.rStepDataP/folder/fileN
        cFile.WriteDF2CSV(fileP, dfO)
        #------------------------------> Umsap
        self.rObj.rData[self.cSection][self.rDateC]['AA'][f'{date}_{pos}'] = fileN
        self.rObj.Save()
        #------------------------------> Refresh
        #--------------> UMSAPControl
        self.cParent.UpdateFileContent()                                        # type: ignore
        #--------------> TarProt
        self.rObj = self.cParent.rObj                                           # type: ignore
        self.rData = self.rObj.dConfigure[self.cSection]()
        self.rDataC = getattr(self.rData, self.rDateC)
        #--------------> Menu
        _, menuData = self.SetDateMenuDate()
        self.mBar.mTool.mFurtherA.UpdateFurtherAnalysis(
            self.rDateC, menuData['FA'])
        #--------------> GUI
        self.AASelect(f'{date}_{pos}')
        #endregion --------------------------------------------> Save & Update

        dlg.Destroy()
        return True
    #---

    def AASelect(self, aa:str) -> bool:
        """Show an AA analysis. Method called from Menu.

            Parameters
            ----------
            aa: str
                Date for the analysis

            Returns
            -------
            bool
        """
        self.cParent.rWindow[self.cSection]['FA'].append(                       # type: ignore
            ResAA(self, self.rDateC, aa, self.rDataC.AA[aa]))
        return True
    #---

    def HistSelect(self, hist:str) -> bool:
        """Show a Histogram. Method called from Menu.

            Parameters
            ----------
            hist: str
                Selected date.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        self.cParent.rWindow[self.cSection]['FA'].append(                       # type: ignore
            ResHist(
                self, self.rDateC, hist, self.rDataC.Hist[hist]))
        #endregion ------------------------------------------------>

        return True
    #---

    def HistNew(self) -> bool:
        """Create a new histogram. Method called from Menu.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> dlg
        dlg = cWindow.UserInputText(
            'New Histogram Analysis',
            ['Histograms Windows'],
            ['Size of the histogram windows, e.g. 50 or 50 100 200'],
            parent    = self,
            validator = [cValidator.NumberList(numType='int', vMin=0, sep=' ')],
        )
        #endregion ------------------------------------------------> dlg

        #region ---------------------------------------------------> Get Pos
        if dlg.ShowModal():
            win   = [int(x) for x in dlg.rInput[0].wTc.GetValue().split()]
            dateC = cMethod.StrNow()
        else:
            dlg.Destroy()
            return False
        #endregion ------------------------------------------------> Get Pos

        #region ---------------------------------------------------> Run
        dfI = self.rDataC.df
        idx = pd.IndexSlice
        a   = mConfig.tarp.dfcolFirstPart[2:]+self.rDataC.labelA
        b   = mConfig.tarp.dfcolFirstPart[2:]+len(self.rDataC.labelA)*['P']
        dfI = dfI.loc[:,idx[a,b]]                                               # type: ignore
        dfO = tarpMethod.R2Hist(
            dfI, self.rDataC.alpha, win, self.rDataC.protLength)
        #endregion ------------------------------------------------> Run

        #region -----------------------------------------------> Save & Update
        #------------------------------> File
        date    = f'{self.rDateC.split(" - ")[0]}'
        section = f'{self.cSection.replace(" ", "-")}'
        folder  = f'{date}_{section}'
        fileN   = f'{dateC}_Hist-{win}.txt'
        fileP   = self.rObj.rStepDataP/folder/fileN
        cFile.WriteDF2CSV(fileP, dfO)
        #------------------------------> Umsap
        self.rObj.rData[self.cSection][self.rDateC]['Hist'][f'{date}_{win}'] = fileN
        self.rObj.Save()
        #------------------------------> Refresh
        #--------------> UMSAPControl
        self.cParent.UpdateFileContent()                                        # type: ignore
        #--------------> TarProt
        self.rObj   = self.cParent.rObj                                         # type: ignore
        self.rData  = self.rObj.dConfigure[self.cSection]()
        self.rDataC = getattr(self.rData, self.rDateC)
        #--------------> Menu
        _, menuData = self.SetDateMenuDate()
        self.mBar.mTool.mFurtherA.UpdateFurtherAnalysis(
            self.rDateC, menuData['FA'])
        #--------------> GUI
        self.HistSelect(f'{date}_{win}')
        #endregion --------------------------------------------> Save & Update

        dlg.Destroy()
        return True
    #---

    def CpR(self) -> bool:
        """Show the Cleavage per Residue results. Method called from Menu.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        self.cParent.rWindow[self.cSection]['FA'].append(                       # type: ignore
            ResCpR(self, self.rDateC, self.rDataC.CpR))
        #endregion ------------------------------------------------>

        return True
    #---

    def PDBMap(self) -> bool:
        """Map results to a PDB. Method called from Menu.

            Returns
            -------
            bool
        """
        #region ------------------------------------------------------> Helper
        def _steps(*args) -> bool:                                              # pylint: disable=unused-argument
            """Perform the pdb mapping in a different thread."""
            #region -----------------------------------------------> Variables
            msgStep = 'Preparing PDB mapping'
            wx.CallAfter(dlp.UpdateStG, msgStep)
            #------------------------------>
            pdbObj   = cFile.PDBFile(pdbI)
            pdbSeq   = pdbObj.GetSequence(pdbObj.rChain[0])
            cut      = self.rObj.GetCleavagePerResidue(self.cSection, self.rDateC)
            cEvol    = self.rObj.GetCleavageEvolution(self.cSection, self.rDateC)
            blosum62 = substitution_matrices.load("BLOSUM62")
            #endregion --------------------------------------------> Variables

            #region -----------------------------------------------------> Run
            msgStep = 'Performing sequence alignments'
            wx.CallAfter(dlp.UpdateStG, msgStep)
            #------------------------------>
            align = pairwise2.align.globalds(                                       # type: ignore
                pdbSeq, self.rRecSeqC, blosum62, -10, -0.5)
            #------------------------------>
            msgStep = 'Creating PDB files'
            wx.CallAfter(dlp.UpdateStG, msgStep)
            #------------------------------>
            _helper(pdbObj, self.rDataC.labelA, align, cut, (self.rDateC, 'CpR'))
            _helper(pdbObj, self.rDataC.labelA, align, cEvol, (self.rDateC, 'CEvol'))
            #------------------------------>
            msgStep = mConfig.core.lPdDone
            wx.CallAfter(dlp.UpdateG)
            wx.CallAfter(dlp.SuccessMessage, msgStep)
            #endregion -------------------------------------------------> Run

            return True
        #---

        def _helper(pdbObj, tExp, tAlign, tDF, name):
            """Writes to file

                Parameters
                ----------
                pdbObj: mFile.PDBFile
                    PDB Object
                tExp: str
                    Current experiment
                tAlign: BioPython alignment
                    Sequence alignment
                tDF: pd.DataFrame
                    To get the beta values
                name: str
                    Part of the file name

                Returns
                -------
                bool
            """
            #region -------------------------------------------------------->
            pdbRes = pdbObj.GetResNum(pdbObj.rChain[0])
            idx    = pd.IndexSlice
            #------------------------------>
            for e in tExp:
                #------------------------------>
                betaDict = {}
                p = 0
                s = 0
                #------------------------------>
                for j,r in enumerate(tAlign[0].seqB):
                    if r != '-':
                        #------------------------------>
                        if tAlign[0].seqA[j] != '-':
                            betaDict[pdbRes[p]] = tDF.iat[s, tDF.columns.get_loc(idx['Rec',e])]
                            p = p + 1
                        #------------------------------>
                        s = s + 1
                #------------------------------>
                pdbObj.SetBeta(pdbObj.rChain[0], betaDict)
                pdbObj.WritePDB(
                    pdbO/f'{name[0]} - {e} - {name[1]}.pdb', pdbObj.rChain[0])
            #endregion ----------------------------------------------------->

            return True
        #---
        #endregion ---------------------------------------------------> Helper

        #region ---------------------------------------------------------> dlg
        dlg = cWindow.FA2Btn(
            ['PDB', 'Output'],
            ['Path to the PDB file', 'Path to the output folder'],
            [mConfig.core.elPDB, mConfig.core.elPDB],
            [cValidator.InputFF('file'), cValidator.OutputFF('folder')],
            parent = self
        )
        #endregion ------------------------------------------------------> dlg

        #region ---------------------------------------------------> Get Path
        if dlg.ShowModal():
            pdbI = dlg.wBtnI.wTc.GetValue()
            pdbO = Path(dlg.wBtnO.wTc.GetValue())
        else:
            dlg.Destroy()
            return False
        #endregion ------------------------------------------------> Get Path

        #region -------------------------------------------------------->
        dlp = cWindow.Progress(self, 'Creating PDB files', 4)
        #endregion ----------------------------------------------------->

        #region -------------------------------------------------------->
        _thread.start_new_thread(_steps, ('test',))
        #------------------------------>
        dlp.ShowModal()
        #endregion ----------------------------------------------------->

        dlg.Destroy()
        dlp.Destroy()
        return True
    #---

    def CEvol(self) -> bool:
        """Show the Cleavage Evolution results. Method called from Menu.

            Returns
            -------
            bool
        """
        self.cParent.rWindow[self.cSection]['FA'].append(                       # type: ignore
            ResCEvol(self, self.rDateC, self.rDataC.CEvol))
        return True
    #---
    #endregion ------------------------------------------------> Class Methods
#---


class ResAA(cWindow.BaseWindowResultOnePlotFA):
    """Show the results of an AA analysis.

        Parameters
        ----------
        parent: ResTarProt
            Parent of the window.
        dateC: str
            Current date
        key: str
        fileN: str
            Name of the file with the analysis result.

        Attributes
        ----------
        rBandStart: float
            Start x coordinates for the bands.
        rBandWidth: float
            Width of the bands.
        rData: pd.DataFrame
            Data with the results.
        rDataC.labelA: bool
            Show experiments (True) or Positions (False).
        rLabel: list[str]
            Experiment names.
        rLabelC: str
            Currently selected experiment.
        rObj: UMSAPFile
            Reference to the UMSAP file in the parent UMSAPCtrl window.
        rPos: list[str]
            Positions in the results.
        rRecSeq: str
            Sequence of the recombinant protein.
        rUMSAP: UMSAPCtrl
            Pointer to the UMSAPCtrl window.
    """
    #region -----------------------------------------------------> Class setup
    cName     = mConfig.tarp.nwAAPlot
    cSection  = mConfig.tarp.tuAA
    cFragment = mConfig.core.cFragment
    cCtrl     = mConfig.tarp.cCtrl
    cBarColor = mConfig.core.cBarColor
    cXaa      = mConfig.tarp.cXaa
    cChi      = mConfig.core.cChi
    #------------------------------>
    rBandWidth = 0.8
    rBandStart = 0.4
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self,
        parent:ResTarProt,
        dateC:str,
        key:str,
        fileN:str,
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.cTitle  = f"{parent.cTitle} - {dateC} - {self.cSection} - {key}"
        self.cDateC  = dateC
        self.cKey    = key
        self.cFileN  = fileN
        self.rUMSAP  = parent.cParent
        self.rObj    = parent.rObj
        self.rData   = self.rObj.GetFAData(
            parent.cSection, self.cDateC, fileN, [0,1])
        self.rRecSeq = self.rObj.GetRecSeq(parent.cSection, dateC)
        menuData     = self.SetMenuDate()
        self.rPos    = menuData['Pos']
        self.rLabel  = menuData['Label']
        self.rExp    = True
        self.rLabelC = ''
        #------------------------------>
        super().__init__(parent)
        #------------------------------>
        dKeyMethod = {
            mConfig.tarp.kwAAExp : self.PlotExp,
            mConfig.tarp.kwAAPos : self.PlotPos,
        }
        self.dKeyMethod = self.dKeyMethod | dKeyMethod
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------------> Menu
        self.mBar = mMenu.MenuBarTool(self.cName, menuData=menuData)
        self.SetMenuBar(self.mBar)
        #endregion -----------------------------------------------------> Menu

        #region ---------------------------------------------------> Plot
        self.PlotExp(menuData['Label'][0])
        #endregion ------------------------------------------------> Plot

        #region ---------------------------------------------> Window position
        self.WinPos()
        self.Show()
        #endregion ------------------------------------------> Window position
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def SetMenuDate(self) -> dict:
        """Set the menu data.

            Returns
            -------
            dict
        """
        menuData = {}
        menuData['Label'] = list(self.rData.columns.unique(level=0)[1:-1])
        menuData['Pos'] = list(self.rData[menuData['Label'][0]].columns.unique(level=0))

        return menuData
    #---

    def SetAxisExp(self) -> bool:
        """General details of the plot area.

            Returns
            -------
            bool
        """
        #region -------------------------------------------------------> Clear
        self.wPlot[0].rFigure.clear()
        self.wPlot[0].rAxes = self.wPlot[0].rFigure.add_subplot(111)
        #endregion ----------------------------------------------------> Clear

        #region ---------------------------------------------------> Set ticks
        self.wPlot[0].rAxes.set_ylabel('AA distribution (%)')
        self.wPlot[0].rAxes.set_xlabel('Positions')
        self.wPlot[0].rAxes.set_xticks(range(1,len(self.rPos)+1,1))
        self.wPlot[0].rAxes.set_xticklabels(self.rPos)
        self.wPlot[0].rAxes.set_xlim(0,len(self.rPos)+1)
        #endregion ------------------------------------------------> Set ticks

        return True
    #---

    def PlotExp(self, label:str) -> bool:
        """Plot the results for the selected experiment.

            Parameters
            ----------
            label: str
                Name of the experiment.

            Returns
            -------
            bool
        """
        #region -------------------------------------------------------->
        self.rExp    = True
        self.rLabelC = label
        #endregion ----------------------------------------------------->

        #region --------------------------------------------------->
        self.SetAxisExp()
        #endregion ------------------------------------------------>

        #region ---------------------------------------------------> Data
        idx = pd.IndexSlice
        df  = self.rData.loc[:,idx[('AA', label),:]].iloc[0:-1,:]               # type: ignore
        df.iloc[:,1:] = 100*(df.iloc[:,1:]/df.iloc[:,1:].sum(axis=0))
        #endregion ------------------------------------------------> Data

        #region ---------------------------------------------------> Bar
        col = df.loc[:,idx[label,:]].columns.unique(level=1)                    # type: ignore
        for k,c in enumerate(col, start=1):
            #------------------------------> Prepare DF
            dfB = df.loc[:,idx[('AA',label),('AA',c)]]                          # type: ignore
            dfB = dfB[dfB[(label,c)] != 0]
            dfB = dfB.sort_values(by=[(label,c),('AA','AA')], ascending=False)  # type: ignore
            #------------------------------> Supp Data
            cumS = [0]+dfB[(label,c)].cumsum().values.tolist()[:-1]
            #-------------->
            color = []
            text  = []
            r     = 0
            for row in dfB.itertuples(index=False):
                #-------------->
                color.append(self.cBarColor[row[0]]
                     if row[0] in mConfig.core.lAA1 else self.cXaa)
                #-------------->
                if row[1] >= 10.0:
                    s = f'{row[0]}\n{row[1]:.1f}'
                    y = (2*cumS[r]+row[1])/2
                    text.append([k,y,s])
                r = r + 1
            #------------------------------> Bar
            self.wPlot[0].rAxes.bar(
                k,
                dfB[(label,c)].values.tolist(),
                bottom    = cumS,
                color     = color,
                edgecolor = 'black',
            )
            #------------------------------> Text
            for x,y,t in text:
                self.wPlot[0].rAxes.text(
                    x,y,t,
                    fontsize            = 9,
                    horizontalalignment = 'center',
                    verticalalignment   = 'center',
                )
        #endregion ------------------------------------------------> Bar

        #region --------------------------------------------------> Tick Color
        chi = self.rData.loc[:,idx[('AA', label),:]].iloc[-1,1:].values         # type: ignore
        self.wPlot[0].rAxes.set_title(label)
        for k,v in enumerate(chi):
            color = self.cChi[v]
            self.wPlot[0].rAxes.get_xticklabels()[k].set_color(color)
        #endregion -----------------------------------------------> Tick Color

        #region --------------------------------------------------->
        self.wPlot[0].ZoomResetSetValues()
        self.wPlot[0].rCanvas.draw()
        #endregion ------------------------------------------------>

        return True
    #---

    def SetAxisPos(self) -> bool:
        """General details of the plot area.

            Returns
            -------
            bool
        """
        #region -------------------------------------------------------> Clear
        self.wPlot[0].rFigure.clear()
        self.wPlot[0].rAxes = self.wPlot[0].rFigure.add_subplot(111)
        #endregion ----------------------------------------------------> Clear

        #region ---------------------------------------------------> Set ticks
        self.wPlot[0].rAxes.set_ylabel('AA distribution (%)')
        self.wPlot[0].rAxes.set_xlabel('Amino acids')
        self.wPlot[0].rAxes.set_xticks(range(1,len(mConfig.core.lAA1)+1,1))
        self.wPlot[0].rAxes.set_xticklabels(mConfig.core.lAA1)
        self.wPlot[0].rAxes.set_xlim(0,len(mConfig.core.lAA1)+1)
        #endregion ------------------------------------------------> Set ticks

        return True
    #---

    def PlotPos(self, label:str) -> bool:
        """Plot the results for a position.

            Parameters
            ----------
            label: str
                Name of the position.

            Returns
            -------
            bool
        """
        #region -------------------------------------------------------->
        self.rExp    = False
        self.rLabelC = label
        #endregion ----------------------------------------------------->

        #region --------------------------------------------------->
        self.SetAxisPos()
        #endregion ------------------------------------------------>

        #region ---------------------------------------------------> Data
        idx = pd.IndexSlice
        df  = self.rData.loc[:,idx[:,label]].iloc[0:-1,0:-1]                    # type: ignore
        df  = 100*(df/df.sum(axis=0))
        #endregion ------------------------------------------------> Data

        #region ---------------------------------------------------> Bar
        n = len(self.rLabel)
        for row in df.itertuples():
            s = row[0]+1-self.rBandStart
            w = self.rBandWidth/n
            for x in range(0,n,1):
                self.wPlot[0].rAxes.bar(
                    s+x*w,
                    row[x+1],
                    width     = w,
                    align     = 'edge',
                    color     = self.cFragment[x%len(self.cFragment)],
                    edgecolor = 'black',
                )
        #endregion ------------------------------------------------> Bar

        #region ------------------------------------------------------> Legend
        leg = []
        legLabel = self.rData.columns.unique(level=0)[1:-1]
        for i in range(0, n, 1):
            leg.append(mpatches.Patch(
                color = self.cFragment[i],
                label = legLabel[i],
            ))
        leg = self.wPlot[0].rAxes.legend(
            handles        = leg,
            loc            = 'upper left',
            bbox_to_anchor = (1, 1)
        )
        leg.get_frame().set_edgecolor('k')
        #endregion ---------------------------------------------------> Legend

        #region --------------------------------------------------->
        self.wPlot[0].ZoomResetSetValues()
        self.wPlot[0].rAxes.set_title(label)
        self.wPlot[0].rCanvas.draw()
        #endregion ------------------------------------------------>

        return True
    #---

    def UpdateStatusBar(self, event) -> bool:
        """Update the statusbar info.

            Parameters
            ----------
            event: matplotlib event
                Information about the event.

            Returns
            -------
            bool
        """
        #region ----------------------------------------------> Statusbar Text
        if event.inaxes:
            #------------------------------>
            x, y = event.xdata, event.ydata
            #------------------------------>
            if self.rExp:
                return self.UpdateStatusBarExp(x,y)
            #------------------------------> Position
            return self.UpdateStatusBarPos(x,y)
        else:
            self.wStatBar.SetStatusText('')
        #endregion -------------------------------------------> Statusbar Text

        return True
    #---

    def UpdateStatusBarExp(self, x:float, y:float) -> bool:
        """Update the wx.StatusBar text when plotting an experiment.

            Parameters
            ----------
            x: float
                Mouse x coordinate.
            y: float
                Mouse y coordinate.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        if not 1 <= (xf := round(x)) <= len(self.rPos):
            self.wStatBar.SetStatusText('')
            return False
        #------------------------------>
        pos = self.rPos[xf-1]
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        df = self.rData.loc[:,[('AA', 'AA'),(self.rLabelC, pos)]].iloc[0:-1,:]
        df['Pc'] = 100*(df.iloc[:,1]/df.iloc[:,1].sum(axis=0))
        df = df.sort_values(
            by=[(self.rLabelC, pos),('AA','AA')], ascending=False)              # type: ignore
        df['Sum'] = df['Pc'].cumsum()
        df = df.reset_index(drop=True)
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        try:
            row = df[df['Sum'].gt(y)].index[0]
        except Exception:
            self.wStatBar.SetStatusText('')
            return False
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        aa    = df.iat[row,0]
        pc    = f'{df.iat[row,-2]:.1f}'
        absV  = f'{df.iat[row,1]:.0f}'
        inSeq = self.rRecSeq.count(aa)
        text  = (f'Pos={pos}  AA={aa}  {pc}%  Abs={absV}  InSeq={inSeq}')
        #endregion ------------------------------------------------>

        self.wStatBar.SetStatusText(text)
        return True
    #---

    def UpdateStatusBarPos(self, x:float, y:float) -> bool:                     # pylint: disable=unused-argument
        """Update the wx.StatusBar text when plotting a positions.

            Parameters
            ----------
            x: float
                Mouse x coordinate.
            y: float
                Mouse y coordinate.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        if not 1 <= (xf := round(x)) <= len(mConfig.core.lAA1):
            self.wStatBar.SetStatusText('')
            return False
        aa = mConfig.core.lAA1[xf-1]
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        n = len(self.rLabel)
        w = self.rBandWidth / n
        e = xf - self.rBandStart + (self.rBandWidth / n)
        k = 0
        for k in range(0, n, 1):
            if e < x:
                e = e + w
            else:
                break
        exp = self.rLabel[k]
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        df = self.rData.loc[:,[('AA', 'AA'),(exp, self.rLabelC)]].iloc[0:-1,:]
        df['Pc'] = 100*(df.iloc[:,1]/df.iloc[:,1].sum(axis=0))
        df = df.sort_values(
            by=[(exp, self.rLabelC),('AA','AA')], ascending=False)              # type: ignore
        df['Sum'] = df['Pc'].cumsum()
        df = df.reset_index(drop=True)
        row = df.loc[df[('AA', 'AA')] == aa].index[0]
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        pc    = f'{df.iat[row, 2]:.1f}'
        absV  = f'{df.iat[row, 1]:.0f}'
        inSeq = self.rRecSeq.count(aa)
        text  = (f'AA={aa}  Exp={exp}  {pc}%  Abs={absV}  InSeq={inSeq}')
        #endregion ------------------------------------------------>

        self.wStatBar.SetStatusText(text)
        return True
    #---

    def DupWin(self) -> bool:
        """Export data to a csv file.

            Returns
            -------
            bool
        """
        #------------------------------>
        self.rUMSAP.rWindow[self.cParent.cSection]['FA'].append(                # type: ignore
            ResAA(self.cParent, self.cDateC, self.cKey, self.cFileN)            # type: ignore
        )
        #------------------------------>
        return True
    #---
    #endregion ------------------------------------------------> Class methods
#---


class ResHist(cWindow.BaseWindowResultOnePlotFA):
    """Plot the results for a cleavage histogram.

        Parameters
        ----------
        parent: ResTarProt
            Parent of the window.
        dateC: str
            Current date
        key: str
        fileN: str
            Name of the file with the analysis result.

        Attributes
        ----------
        rAllC: str
            Show all cleavage or not.
        rBandStart: float
            Start x coordinates for the bands.
        rBandWidth: float
            Width of the bands.
        rData: pd.DataFrame
            Data with the results.
        rLabel: list[str]
            List of experiment labels.
        rNat: str
            Plot recombinant or native sequence.
        rObj: UMSAPFile
            Reference to the UMSAP file in the parent UMSAPCtrl window.
        rDataC.protLength[0]: list[int]
            Length of the recombinant and native protein.
        rUMSAP: UMSAPCtrl
            Pointer to the UMSAPCtrl window.
    """
    #region -----------------------------------------------------> Class setup
    cName     = mConfig.tarp.nwHistPlot
    cSection  = mConfig.tarp.tuHist
    cFragment = mConfig.core.cFragment
    cRec = {
        True : 'Nat',
        False: 'Rec',
        'Rec': 'Recombinant Sequence',
        'Nat': 'Native Sequence',
    }
    cAll = {
        True    : 'Unique',
        False   : 'All',
        'All'   : 'All Cleavages',
        'Unique': 'Unique Cleavages',
    }
    #------------------------------>
    rBandWidth = 0.8
    rBandStart = 0.4
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self,
        parent:ResTarProt,
        dateC:str,
        key:str,
        fileN:str,
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.cTitle = f"{parent.cTitle} - {dateC} - {self.cSection} - {key}"
        self.cDateC = dateC
        self.cKey   = key
        self.cFileN = fileN
        self.rUMSAP = parent.cParent
        self.rObj   = parent.rObj
        self.rData  = self.rObj.GetFAData(
            parent.cSection, self.cDateC, fileN, [0,1,2])
        self.rLabel      = self.rData.columns.unique(level=2).tolist()[1:]
        data = getattr(parent.rData, self.cDateC)
        self.rProtLength = data.protLength
        menuData         = self.SetMenuDate()
        self.rNat = 'Rec'
        self.rAllC = 'All'
        #------------------------------>
        super().__init__(parent)
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------------> Plot
        self.UpdateResultWindow()
        #endregion -----------------------------------------------------> Plot

        #region --------------------------------------------------------> Menu
        self.mBar = mMenu.MenuBarTool(self.cName, menuData=menuData)
        self.SetMenuBar(self.mBar)
        #endregion -----------------------------------------------------> Menu

        #region ---------------------------------------------> Window position
        self.WinPos()
        self.Show()
        #endregion ------------------------------------------> Window position
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def SetMenuDate(self) -> dict:
        """Set the data for the menu.

            Returns
            -------
            dict
        """
        #region --------------------------------------------------->
        menuData = {}
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        menuData['Label'] = [k for k in self.rLabel]
        #------------------------------>
        if self.rProtLength[1]:
            menuData['Nat'] = True
        else:
            menuData['Nat'] = False
        #endregion ------------------------------------------------>

        return menuData
    #---

    def UpdateResultWindow(                                                     # pylint: disable=arguments-differ
        self,
        nat:Optional[bool]  = None,
        allC:Optional[bool] = None,
        ) -> bool:
        """Update the window.

            Parameters
            ----------
            nat: bool or None
                Show native or recombinant sequence.
            allC: bool or None
                Show all cleavages or not.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        self.rNat  = self.cRec[nat] if nat is not None else self.rNat
        self.rAllC = self.cAll[allC] if allC is not None else self.rAllC
        #------------------------------>
        idx = pd.IndexSlice
        df  = self.rData.loc[:,idx[self.rNat,['Win',self.rAllC],:]]             # type: ignore
        #endregion ------------------------------------------------> Variables

        #region --------------------------------------------------->
        self.SetAxis(df.loc[:,idx[:,:,'Win']])                                  # type: ignore
        #endregion ------------------------------------------------>

        #region ---------------------------------------------------> Plot
        n = len(self.rLabel)
        w = self.rBandWidth / n
        df = df.iloc[:,range(1,n+1,1)]
        df = df[(df.notna()).all(axis=1)]                                       # type: ignore
        for row in df.itertuples():
            s = row[0]+1-self.rBandStart
            for x in range(0,n,1):
                self.wPlot[0].rAxes.bar(
                    s+x*w,
                    row[x+1],
                    width     = w,
                    align     = 'edge',
                    color     = self.cFragment[x%len(self.cFragment)],
                    edgecolor = 'black',
                )
        #endregion ------------------------------------------------> Plot

        #region ------------------------------------------------------> Legend
        leg = []
        for i in range(0, n, 1):
            leg.append(mpatches.Patch(
                color = self.cFragment[i],
                label = self.rLabel[i],
            ))
        leg = self.wPlot[0].rAxes.legend(
            handles        = leg,
            loc            = 'upper left',
            bbox_to_anchor = (1, 1)
        )
        leg.get_frame().set_edgecolor('k')
        #endregion ---------------------------------------------------> Legend

        #region --------------------------------------------------->
        self.wPlot[0].ZoomResetSetValues()
        self.wPlot[0].rAxes.set_title(
            f'{self.cRec[self.rNat]} - {self.cAll[self.rAllC]}')
        self.wPlot[0].rCanvas.draw()
        #endregion ------------------------------------------------>

        return True
    #---

    def SetAxis(self, win:pd.Series) -> bool:
        """Set the axis of the plot.

            Parameters
            ----------
            win: pd.Series
                Windows of the histograms.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        self.wPlot[0].rAxes.clear()
        #endregion ------------------------------------------------>

        #region ---------------------------------------------------> Label
        #------------------------------>
        win = win.dropna().astype('int').to_numpy().flatten()                   # type: ignore
        label = []
        for k,w in enumerate(win[1:]):
            label.append(f'{win[k]}-{w}')
        #------------------------------>
        self.wPlot[0].rAxes.set_xticks(range(1,len(label)+1,1))
        self.wPlot[0].rAxes.set_xticklabels(label)
        self.wPlot[0].rAxes.set_xlim(0, len(label)+1)
        self.wPlot[0].rAxes.tick_params(axis='x', labelrotation=45)
        self.wPlot[0].rAxes.yaxis.get_major_locator().set_params(integer=True)
        self.wPlot[0].rAxes.set_xlabel('Windows')
        self.wPlot[0].rAxes.set_ylabel('Number of Cleavages')
        #endregion ------------------------------------------------> Label

        return True
    #---

    def DupWin(self) -> bool:
        """ Export data to a csv file.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        self.rUMSAP.rWindow[self.cParent.cSection]['FA'].append(                # type: ignore
            ResHist(self.cParent, self.cDateC, self.cKey, self.cFileN))         # type: ignore
        #endregion ------------------------------------------------>

        return True
    #---

    def UpdateStatusBar(self, event) -> bool:
        """Update the statusbar info.

            Parameters
            ----------
            event: matplotlib event
                Information about the event.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        if event.inaxes:
            x, _ = event.xdata, event.ydata
            xf = round(x)
        else:
            self.wStatBar.SetStatusText('')
            return True
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        idx = pd.IndexSlice
        df = self.rData.loc[:,idx[self.rNat,['Win',self.rAllC],:]]              # type: ignore
        df = df.dropna(how='all')
        if not 0 <= xf < df.shape[0]:
            self.wStatBar.SetStatusText('')
            return False
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        n = len(self.rLabel)
        w = self.rBandWidth / n
        e = xf - self.rBandStart + (self.rBandWidth / n)
        k = 0
        for k in range(0, n, 1):
            if e < x:
                e = e + w
            else:
                break
        exp = self.rLabel[k]
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        win = f'{df.iat[xf-1, 0]:.0f}-{df.iat[xf, 0]:.0f}'
        clv = f'{df.iat[xf-1,df.columns.get_loc(idx[self.rNat,self.rAllC,exp])]:.0f}'
        text = (f'Win={win}  Exp={exp}  Cleavages={clv}')
        #------------------------------>
        self.wStatBar.SetStatusText(text)
        #endregion ------------------------------------------------>

        return True
    #---
    #endregion ------------------------------------------------> Class methods
#---


class ResCpR(cWindow.BaseWindowResultOnePlotFA):
    """Plot the Cleavage per Residue for an analysis.

        Parameters
        ----------
        parent: ResTarProt
            Parent of the window.
        dateC: str
            Current date.
        fileN: str
            Name of the file with the analysis result.

        Attributes
        ----------
        rData: dict
            Keys are dates and values is the data to create the plot.
        rLabel: list[str]
            Label of the experiment.
        rLabelC: str
            Currently selected label.
        rNat: str
            Plot results for the native or recombinant protein.
        rObj: UMSAPFile
            Reference to the UMSAP file in the parent UMSAPCtrl window.
        rDataC.protLength[0]: list[int]
            Length of the recombinant and native protein.
        rDataC.protLoc: list[int]
            Location of the native protein in the sequence of the recombinant
            protein.
        rUMSAP: UMSAPCtrl
            Pointer to the UMSAPCtrl window.
    """
    #region -----------------------------------------------------> Class setup
    cName     = mConfig.tarp.nwCpRPlot
    cSection  = mConfig.tarp.tuCpR
    cFragment = mConfig.core.cFragment
    #------------------------------>
    cNat = {
        True : 'Nat',
        False: 'Rec',
        'Rec': 'Recombinant Sequence',
        'Nat': 'Native Sequence',
    }
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent:ResTarProt, dateC:str, fileN:str) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.cTitle = f"{parent.cTitle} - {dateC} - {self.cSection}"
        self.cDateC = dateC
        self.cFileN = fileN
        self.rUMSAP = parent.cParent
        self.rObj   = parent.rObj
        self.rData  = self.rObj.GetFAData(
            parent.cSection, self.cDateC, fileN, [0,1])
        self.rLabel = self.rData.columns.unique(level=1).tolist()
        data = getattr(parent.rData, self.cDateC)
        self.rProtLength = data.protLength
        self.rProtLoc    = data.protLoc
        menuData         = self.SetMenuDate()
        #------------------------------>
        super().__init__(parent)
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------------> Menu
        self.mBar = mMenu.MenuBarTool(self.cName, menuData=menuData)
        self.SetMenuBar(self.mBar)
        #endregion -----------------------------------------------------> Menu

        #region ---------------------------------------------------> Plot
        self.UpdateResultWindow(nat=False, label=[menuData['Label'][0]])        # type: ignore
        #endregion ------------------------------------------------> Plot

        #region ---------------------------------------------> Window position
        self.WinPos()
        self.Show()
        #endregion ------------------------------------------> Window position
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def SetMenuDate(self) -> dict:
        """Set the data to build the Tool menu.

            Returns
            -------
            dict
        """
        #region --------------------------------------------------->
        menuData = {}
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        menuData['Label'] = [k for k in self.rLabel]
        #------------------------------>
        if self.rProtLength[1]:
            menuData['Nat'] = True
        else:
            menuData['Nat'] = False
        #endregion ------------------------------------------------>

        return menuData
    #---

    def UpdateResultWindow(                                                     # pylint: disable=arguments-differ
        self,
        nat:bool,
        label:str,
        protLoc:bool = True
        ) -> bool:
        """Update the results shown in the window.

            Parameters
            ----------
            nat: bool
                Plot results for the native (True) or recombinant (False)
                protein.
            label: str
                Plot results for this experiment.
            protLoc: bool
                Show native protein location (True) or not (False).

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        self.rNat    = self.cNat[nat]
        self.rLabelC = label
        #------------------------------>
        idx = pd.IndexSlice
        #------------------------------>
        if nat:
            tXIdx = range(0, self.rProtLength[1])
        else:
            tXIdx = range(0, self.rProtLength[0])
        x = [x+1 for x in tXIdx]
        #------------------------------>
        color = []
        #------------------------------>
        yMax = self.rData.loc[:,idx[self.rNat,label]].max().max()               # type: ignore
        #endregion ------------------------------------------------> Variables

        #region --------------------------------------------------->
        self.SetAxis()
        #endregion ------------------------------------------------>

        #region ---------------------------------------------------> Plot
        for e in label:
            #------------------------------>
            y = self.rData.iloc[tXIdx, self.rData.columns.get_loc(idx[self.rNat,e])]                # type: ignore
            tColor = self.cFragment[
                self.rLabel.index(e)%len(self.cFragment)]
            color.append(tColor)
            #------------------------------>
            self.wPlot[0].rAxes.plot(x,y, color=tColor)
        #------------------------------>
        if self.rNat == self.cNat[False] and protLoc:
            if self.rProtLoc[0] > -1:
                self.wPlot[0].rAxes.vlines(
                    self.rProtLoc[0],0,yMax,linestyles='dashed',color='black',zorder=1)
                self.wPlot[0].rAxes.vlines(
                    self.rProtLoc[1],0,yMax,linestyles='dashed',color='black',zorder=1)
        #endregion ------------------------------------------------> Plot

        #region ----------------------------------------------------> Legend
        leg = []
        for i in range(0, len(label), 1):
            leg.append(mpatches.Patch(
                color = color[i],
                label = label[i],
            ))
        leg = self.wPlot[0].rAxes.legend(
            handles        = leg,
            loc            = 'upper left',
            bbox_to_anchor = (1, 1)
        )
        leg.get_frame().set_edgecolor('k')
        #endregion -------------------------------------------------> Legend

        #region ---------------------------------------------------> Zoom
        self.wPlot[0].ZoomResetSetValues()
        self.wPlot[0].rAxes.set_title(f'{self.cNat[self.rNat]}')
        self.wPlot[0].rCanvas.draw()
        #endregion ------------------------------------------------> Zoom

        return True
    #---

    def SetAxis(self) -> bool:
        """Set the axis of the plot.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        self.wPlot[0].rAxes.clear()
        #endregion ------------------------------------------------>

        #region ---------------------------------------------------> Label
        self.wPlot[0].rAxes.yaxis.get_major_locator().set_params(integer=True)
        self.wPlot[0].rAxes.set_xlabel('Residue Number')
        self.wPlot[0].rAxes.set_ylabel('Number of Cleavages')
        #endregion ------------------------------------------------> Label

        return True
    #---

    def DupWin(self) -> bool:
        """Export data to a csv file.

            Returns
            -------
            bool
        """
        #------------------------------>
        self.rUMSAP.rWindow[self.cParent.cSection]['FA'].append(                # type: ignore
            ResCpR(self.cParent, self.cDateC, self.cFileN))                     # type: ignore
        #------------------------------>
        return True
    #---

    def UpdateStatusBar(self, event) -> bool:
        """Update the statusbar info

            Parameters
            ----------
            event: matplotlib event
                Information about the event.

            Returns
            -------
            bool
        """
        #region ----------------------------------------------> Statusbar Text
        if event.inaxes:
            #------------------------------>
            x = event.xdata
            xf = round(x)
            idx = pd.IndexSlice
            #------------------------------>
            y = []
            try:
                for l in self.rLabelC:
                    col = self.rData.columns.get_loc(idx[self.rNat,l])
                    y.append(self.rData.iat[xf-1,col])
            except IndexError:
                self.wStatBar.SetStatusText('')
                return False
            #------------------------------>
            s = ''
            for k,l in enumerate(self.rLabelC):
                s = f'{s}{l}={y[k]}   '
            self.wStatBar.SetStatusText(f'Res={xf}   {s}')

        else:
            self.wStatBar.SetStatusText('')
        #endregion -------------------------------------------> Statusbar Text

        return True
    #---
    #endregion ------------------------------------------------> Class methods
#---


class ResCEvol(cWindow.BaseWindowResultListTextNPlot):
    """Show the results for a Cleavage Evolution analysis.

        Parameters
        ----------
        parent: ResTarProt
            Parent of the window.
        dateC: str
            Current date
        fileN: str
            Name of the file with the analysis result.

        Attributes
        ----------
        rData: dict
            Keys are dates and values is the data to create the plot.
        rDf: pd.DataFrame
            Results for the current selected options.
        rIdx: dict
            Information about selected rows in the wx.ListCtrl.
        rLabel: list[str]
            Experiment names.
        rMon: bool
            Plot monotonic results (True) or all results (False)
        rObj: UMSAPFile
            Reference to the UMSAP file in the parent UMSAPCtrl window.
        rDataC.protLength[0]: list[int]
            Length of the recombinant and native protein.
        rRec: bool
            Plot data for recombinant or native sequence.
        rUMSAP: UMSAPCtrl
            Pointer to the UMSAPCtrl window.
    """
    #region -----------------------------------------------------> Class setup
    cName    = mConfig.tarp.nwCEvolPlot
    cSection = mConfig.tarp.tuCEvol
    #------------------------------>
    cTList   = 'Residue Numbers'
    cTPlot   = 'Plot'
    cLNPlot  = ['M']
    cLCol    = ['Residue']
    #------------------------------>
    cHSearch = 'Residue Number'
    #------------------------------>
    cRec = {
        True : 'Nat',
        False: 'Rec',
        'Rec': 'Recombinant Sequence',
        'Nat': 'Native Sequence',
    }
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, parent:ResTarProt, dateC:str, fileN:str) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.cTitle = f"{parent.cTitle} - {dateC} - {self.cSection}"
        self.cDateC = dateC
        self.cFileN = fileN
        self.rUMSAP = parent.cParent
        self.rObj   = parent.rObj
        self.rData  = self.rObj.GetFAData(
            parent.cSection, self.cDateC, fileN, [0,1])
        self.rLabel = self.rData.columns.unique(level=1).tolist()
        self.rIdx   = {}
        data = getattr(parent.rData, self.cDateC)
        self.rProtLength = data.protLength
        menuData = self.SetMenuDate()
        #------------------------------>
        super().__init__(parent)
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------->
        self._mgr.DetachPane(self.wText)
        self._mgr.Update()
        self.wText.Destroy()
        #endregion ------------------------------------------------>

        #region --------------------------------------------------------> Menu
        self.mBar = mMenu.MenuBarTool(self.cName, menuData=menuData)
        self.SetMenuBar(self.mBar)
        #endregion -----------------------------------------------------> Menu

        #region --------------------------------------------------------> Plot
        self.UpdateResultWindow(False, False)
        #endregion -----------------------------------------------------> Plot

        #region ---------------------------------------------> Window position
        self.WinPos()
        self.Show()
        #endregion ------------------------------------------> Window position
    #---
    #endregion -----------------------------------------------> Instance setup

    #region --------------------------------------------------> Manage Methods
    def SetMenuDate(self) -> dict:
        """Set the menu data.

            Returns
            -------
            dict
        """
        #region --------------------------------------------------->
        menuData = {}
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        menuData['Label'] = [k for k in self.rLabel]
        #------------------------------>
        if self.rProtLength[1]:
            menuData['Nat'] = True
        else:
            menuData['Nat'] = False
        #endregion ------------------------------------------------>

        return menuData
    #---

    def UpdateResultWindow(                                                     # pylint: disable=arguments-differ
        self,
        nat:Optional[bool] = None,
        mon:Optional[bool] = None,
        ) -> bool:
        """Update the plot.

            Parameters
            ----------
            nat: bool or None
                Plot results for the recombinant or native protein.
            mon: bool or None
                Plot monotonic or all results.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        #------------------------------>
        if nat is not None:
            self.rRec = self.cRec[nat]
        #------------------------------>
        self.rMon = mon if mon is not None else self.rMon
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        idx = pd.IndexSlice
        if self.rRec:
            self.rDF = self.rData.loc[:,idx[self.rRec,:]]                       # type: ignore
        else:
            self.rDF = self.rData.loc[:,idx[self.rRec,:]]                       # type: ignore
        #------------------------------>
        self.rDF = self.rDF[self.rDF.any(axis=1)]
        #------------------------------>
        if self.rMon:
            self.rDF = self.rDF[self.rDF.apply(
                lambda x: x.is_monotonic_increasing or x.is_monotonic_decreasing,
                axis=1
            )]
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        self.FillListCtrl(self.rDF.index.tolist())
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        self.SetAxis()
        self.wPlot.dPlot['M'].ZoomResetSetValues()
        self.wPlot.dPlot['M'].rCanvas.draw()
        #endregion ------------------------------------------------>

        return True
    #---

    def FillListCtrl(self, tRes:list[int]) -> bool:
        """Fill the wx.ListCtrl.

            Parameters
            ----------
            tRes: list[int]
                List of residue numbers.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        self.wLC.wLCS.wLC.DeleteAllItems()
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        data = []
        for k in tRes:
            data.append([str(k+1)])
        self.wLC.wLCS.wLC.SetNewData(data)
        #endregion ------------------------------------------------>

        #region ----------------------------------------------> Update Row Num
        self._mgr.GetPane(self.wLC).Caption(f'{self.cTList} ({len(data)})')
        self._mgr.Update()
        #endregion -------------------------------------------> Update Row Num

        return True
    #---

    def SetAxis(self) -> bool:
        """Set the axis.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        self.wPlot.dPlot['M'].rAxes.clear()
        #endregion ------------------------------------------------>

        #region ---------------------------------------------------> Label
        self.wPlot.dPlot['M'].rAxes.set_xticks(range(1,len(self.rLabel)+1))
        self.wPlot.dPlot['M'].rAxes.set_xticklabels(self.rLabel)
        self.wPlot.dPlot['M'].rAxes.set_xlim(0, len(self.rLabel)+1)
        self.wPlot.dPlot['M'].rAxes.set_xlabel('Experiment Label')
        self.wPlot.dPlot['M'].rAxes.set_ylabel('Relative Cleavage Rate')
        #------------------------------>
        self.wPlot.dPlot['M'].rAxes.set_title(self.cRec[self.rRec])
        #endregion ------------------------------------------------> Label

        return True
    #---

    def Plot(self) -> bool:
        """Plot the data.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        self.SetAxis()
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        for idx,v in self.rIdx.items():
            x = range(1,len(self.rLabel)+1)
            y = self.rDF.iloc[idx,:]
            self.wPlot.dPlot['M'].rAxes.plot(x,y, label=f'{v[0]}')
        #------------------------------>
        if len(self.rIdx) > 1:
            self.wPlot.dPlot['M'].rAxes.legend()
        #------------------------------>
        self.wPlot.dPlot['M'].ZoomResetSetValues()
        self.wPlot.dPlot['M'].rCanvas.draw()
        #endregion ------------------------------------------------>

        return True
    #---

    def DupWin(self) -> bool:
        """Export data to a csv file.

            Returns
            -------
            bool
        """
        #------------------------------>
        self.rUMSAP.rWindow[self.cParent.cSection]['FA'].append(                # type: ignore
            ResCEvol(self.cParent, self.cDateC, self.cFileN))                   # type: ignore
        #------------------------------>
        return True
    #---

    def ExportData(self) -> bool:                                               # pylint: disable=arguments-differ
        """Export data to a csv file.

            Returns
            -------
            bool
        """
        return super().ExportData(df=self.rData)
    #---

    def ExportImgAll(self) -> bool:
        """Save an image of the plot.

            Returns
            -------
            bool
        """
        return self.wPlot.dPlot['M'].SaveImage(
            mConfig.core.elMatPlotSaveI, parent=self)
    #---

    def Close(self) -> bool:
        """Close window and uncheck section in UMSAPFile window. Assumes
            self.parent is an instance of UMSAPControl.

            Parameters
            ----------
            event: wx.CloseEvent
                Information about the event.

            Returns
            -------
            bool
        """
        #region -----------------------------------------------> Update parent
        self.rUMSAP.rWindow[self.cParent.cSection]['FA'].remove(self)           # type: ignore
        #endregion --------------------------------------------> Update parent

        #region ------------------------------------> Reduce number of windows
        mConfig.core.winNumber[self.cName] -= 1
        #endregion ---------------------------------> Reduce number of windows

        #region -----------------------------------------------------> Destroy
        self.Destroy()
        #endregion --------------------------------------------------> Destroy

        return True
    #---

    def ListSelect(self) -> bool:
        """What to do after selecting a row in the wx.ListCtrl.

            Parameters
            ----------
            event : wx.Event
                Information about the event.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        super().ListSelect()
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        self.rIdx = self.wLC.wLCS.wLC.GetSelectedRows(True)
        self.Plot()
        #endregion ------------------------------------------------>

        return True
    #---
    #endregion -----------------------------------------------> Manage Methods
#---
#endregion ----------------------------------------------------------> Classes
