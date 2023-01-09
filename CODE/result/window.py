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


"""Windows for the result module of the app"""


#region -------------------------------------------------------------> Imports
import shutil
from pathlib import Path
from typing  import Optional, Union

import wx
import wx.lib.agw.customtreectrl as wxCT

from config.config import config as mConfig
from core     import file   as cFile
from core     import method as cMethod
from core     import window as cWindow
from main     import menu   as mMenu
from main     import window as mWindow
from result   import file   as resFile
from corr     import window as corrWindow
from dataprep import window as dataWindow
from limprot  import window as limpWindow
from tarprot  import window as tarpWindow
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Classes
#------------------------------> wx.Frame
class UMSAPControl(cWindow.BaseWindow):
    """Window to show and control the content of an umsap file.

        Parameters
        ----------
        fileP: Path
            Path to the UMSAP file
        parent: wx.Window or None
            Parent of the window.

        Attributes
        ----------
        dPlotMethod: dict
            Keys are section names and values the Window to plot the results
        dSectionTab: dict
            Keys are section names and values the corresponding config.name
        rCopiedFilter: list
            Copy of the List of applied filters in a ProtProfPlot Window
        rDataInitPath: Path
            Path to the folder with the Initial files.
        rDataStepPath: Path
            Path to the folder with the step by step results.
        rObj: file.UMSAPFile
            Object to handle UMSAP files
        rSection: dict
            Keys are section names and values a reference to the object in the
            tree control.
        rWindow: list[wx.Window]
            List of plot windows associated with this window.

    """
    #region -----------------------------------------------------> Class setup
    cName = mConfig.res.nwUMSAPControl
    #------------------------------>
    cSWindow = (400, 700)
    #------------------------------>
    cFileLabelCheck = ['Data']
    #------------------------------>
    dPlotMethod = { # Methods to create plot windows
        mConfig.corr.nUtil : corrWindow.ResCorrA,
        mConfig.data.nUtil : dataWindow.ResDataPrep,
        # mConfig.nmProtProf: WindowResProtProf,
        mConfig.limp.nMod : limpWindow.ResLimProt,
        mConfig.tarp.nMod : tarpWindow.ResTarProt,
    }
    # #------------------------------>
    dSectionTab = { # Section name and Tab name correlation
        mConfig.corr.nUtil: mConfig.corr.nTab,
        mConfig.data.nUtil: mConfig.data.nTab,
        mConfig.prot.nMod : mConfig.prot.nTab,
        mConfig.limp.nMod : mConfig.limp.nTab,
        mConfig.tarp.nMod : mConfig.tarp.nTab,
    }
    #------------------------------>
    cLSecSeqF = [mConfig.limp.nMod, mConfig.tarp.nMod]
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, fileP:Path, parent:Optional[wx.Window]=None) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.rObj = resFile.UMSAPFile(fileP)
        #------------------------------>
        self.cTitle        = self.rObj.rFileP.name
        self.rDataInitPath = self.rObj.rInputFileP
        self.rDataStepPath = self.rObj.rStepDataP
        #-------------->  Reference to section items in wxCT.CustomTreeCtrl
        self.rSection = {}
        #------------------------------> Reference to plot windows
        self.rWindow = {}
        #------------------------------> Copied Filters
        self.rCopiedFilters = []
        #------------------------------>
        super().__init__(parent=parent)
        #------------------------------>
        dKeyMethod = {
            mConfig.res.kwToolUMSAPCtrlAddDelExp: self.AddDelExport,
            mConfig.res.kwToolUMSAPCtrlReload   : self.UpdateFileContent,
            mConfig.res.lmToolUMSAPCtrlAdd      : self.AddAnalysis,             # Methods used directly
            mConfig.res.lmToolUMSAPCtrlDel      : self.DeleteAnalysis,          # here in the window class
            mConfig.res.lmToolUMSAPCtrlExp      : self.ExportAnalysis,          # and not in the menu.
        }
        self.dKeyMethod = self.dKeyMethod | dKeyMethod
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wTrc = wxCT.CustomTreeCtrl(self)
        self.wTrc.SetFont(mConfig.core.fTreeItem)
        self.SetTree()
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        self.Sizer.Add(self.wTrc, 1, wx.EXPAND|wx.ALL, 5)                       # pylint: disable=no-member
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Menu
        self.mBar = mMenu.MenuBarTool(self.cName)
        self.SetMenuBar(self.mBar)
        #endregion -----------------------------------------------------> Menu

        #region --------------------------------------------------------> Bind
        self.wTrc.Bind(wxCT.EVT_TREE_ITEM_CHECKING, self.OnCheckItem)
        self.wTrc.Bind(wxCT.EVT_TREE_ITEM_HYPERLINK, self.OnHyperLink)
        #endregion -----------------------------------------------------> Bind

        #region ---------------------------------------------> Window position
        self.WinPos()
        self.Show()
        #endregion ------------------------------------------> Window position
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Event Methods
    def OnHyperLink(self, event:wxCT.TreeEvent) -> bool:
        """Setup analysis.

            Parameters
            ----------
            event: wxCT.TreeEvent
                Information about the event.

            Returns
            -------
            bool
        """
        #region -------------------------------------------------------> DateI
        dateI   = event.GetItem()
        section = dateI.GetParent().GetText()                                   # type: ignore
        #endregion ----------------------------------------------------> DateI

        #region -------------------------------------------------------> DataI
        dataI = self.rObj.GetDataUser(section, dateI.GetText())                 # type: ignore
        #endregion ----------------------------------------------------> DataI

        #region --------------------------------------------------> Create Tab
        #------------------------------>
        if mConfig.main.mainWin is None:
            mConfig.main.mainWin = mWindow.WindowMain()
        #------------------------------>
        mConfig.main.mainWin.CreateTab(self.dSectionTab[section], dataI)
        #endregion -----------------------------------------------> Create Tab

        return True
    #---

    def OnCheckItem(self, event:wxCT.TreeEvent) -> bool:
        """Show window when section is checked.

            Parameters
            ----------
            event: wxCT.TreeEvent
                Information about the event.

            Returns
            -------
            bool
        """
        #region ------------------------------------------> Get Item & Section
        item    = event.GetItem()
        section = self.wTrc.GetItemText(item)
        #endregion ---------------------------------------> Get Item & Section

        #region ----------------------------------------------> Destroy window
        #------------------------------> Event triggers before checkbox changes
        if self.wTrc.IsItemChecked(item):
            #------------------------------>
            for v in self.rWindow[section].values():
                for x in v:
                    mConfig.core.winNumber[x.cName] -= 1
                    x.Destroy()
            #------------------------------>
            event.Skip()
            return True
        #endregion -------------------------------------------> Destroy window

        #region -----------------------------------------------> Create window
        try:
            self.rWindow[section] = {'Main':[], 'FA':[]}
            self.rWindow[section]['Main'].append(
                self.dPlotMethod[section](self))
        except Exception as e:
            cWindow.Notification('errorU', msg=str(e), tException=e)
            return False
        #endregion --------------------------------------------> Create window

        event.Skip()
        return True
    #---

    def OnClose(self, event:Union[wx.CloseEvent, str]) -> bool:
        """Destroy window and remove reference from config.umsapW.

            Parameters
            ----------
            event: wx.Event
                Information about the event.

            Returns
            -------
            bool
        """
        #region -----------------------------------> Update list of open files
        del mConfig.res.winUMSAP[self.rObj.rFileP]
        #endregion --------------------------------> Update list of open files

        #region ------------------------------------> Reduce number of windows
        mConfig.core.winNumber[self.cName] -= 1
        #endregion ---------------------------------> Reduce number of windows

        #region -----------------------------------------------------> Destroy
        self.Destroy()
        #endregion --------------------------------------------------> Destroy

        return True
    #---
    #endregion ------------------------------------------------> Event Methods

    #region ---------------------------------------------------> Class Methods
    def AddDelExport(self, mode:str) -> bool:
        """Set variables to start the Add/Del/Export method.

            Parameters
            ----------
            mode: str
                Label of the selected Tool menu item.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------> Set Object
        if mode == mConfig.res.lmToolUMSAPCtrlAdd:
            #------------------------------>
            dlg = cWindow.FileSelect(
                'openO',
                mConfig.core.elUMSAP,
                parent = self,
                msg    = mConfig.core.mFileSelUMSAP,
            )
            #------------------------------>
            if dlg.ShowModal() == wx.ID_OK:
                #------------------------------>
                fileP = Path(dlg.GetPath())
                dlg.Destroy()
                #------------------------------>
                if fileP == self.rObj.rFileP:
                    msg = ('New Analysis cannot be added from the same UMSAP '
                        'file.\nPlease choose a different UMSAP file.')
                    cWindow.Notification('warning', msg=msg)
                    return False
                #------------------------------>
                try:
                    objAdd = resFile.UMSAPFile(fileP)
                except Exception as e:
                    cWindow.Notification('errorF', tException=e)
                    return False
            else:
                dlg.Destroy()
                return False
        else:
            objAdd = self.rObj
        #endregion -----------------------------------------------> Set Object

        #region ------------------------------------------> Get User Selection
        dlg = UMSAPAddDelExport(objAdd, mode)
        #------------------------------>
        if dlg.ShowModal():
            selItem = dlg.rSelItems
            dlg.Destroy()
        else:
            dlg.Destroy()
            return True
        #endregion ---------------------------------------> Get User Selection

        #region --------------------------------------------------->
        return self.dKeyMethod[mode](selItem, objAdd)                           # type: ignore
        #endregion ------------------------------------------------>
    #---

    def AddAnalysis(self, selItems:dict, objAdd:resFile.UMSAPFile) -> bool:
        """Add analysis from objAdd to the file on the window.

            Parameters
            ----------
            selItems: dict
                Keys are Section names and values selected items.
            objAdd: mFile.UMSAPFile
                File from where new analysis will be added.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        folderData = self.rObj.rStepDataP
        folderInit = self.rObj.rInputFileP
        #------------------------------>
        dataStep = objAdd.rStepDataP
        initStep = objAdd.rInputFileP
        folderD  = {}
        fileD    = {}
        #endregion ------------------------------------------------> Variables

        #region --------------------------------------------------->
        for k, d in selItems.items():
            sec = k.replace(" ","-")
            #------------------------------> Make sure section exist
            self.rObj.rData[k] = self.rObj.rData.get(k, {})
            #------------------------------>
            for run in d:
                temp = run.split(" - ")
                date = temp[0]
                tID = " - ".join(temp[1:])
                #------------------------------>
                folderN = f'{date}_{sec}'
                #------------------------------>
                a = (folderData/folderN).exists()
                b = self.rObj.rData[k].get(run, False)
                if a or b:
                    #------------------------------>
                    n = 1
                    dateF = f'{date}M{n}'
                    c = dateF in self.rObj.rData[k].keys()
                    d = (folderData/f"{dateF}_{sec}").exists()
                    while(c or d):
                        n = n + 1
                        dateF = f'{date}M{n}'
                        c = dateF in self.rObj.rData[k].keys()
                        d = (folderData/f"{dateF}_{sec}").exists()
                    #------------------------------>
                    runN    = f'{dateF} - {tID}'
                    folderT = f'{dateF}_{sec}'
                else:
                    runN    = run
                    folderT = folderN
                #------------------------------> Data
                self.rObj.rData[k][runN] = objAdd.rData[k][run]
                #------------------------------> Folder
                folderD[dataStep/folderN] = folderData/folderT
                #------------------------------> Files
                valI = iter(objAdd.rData[k][run]['I'].values())
                keyI = iter(objAdd.rData[k][run]['I'].keys())
                dataFile = next(valI)
                if (folderInit/dataFile).exists():
                    #------------------------------>
                    n = 1
                    dateFile, nameFile = dataFile.split('_')
                    nameF = f"{dateFile}M{n}_{nameFile}"
                    while (folderInit/nameF).exists():
                        n = n + 1
                        nameF = f"{dateFile}M{n}_{nameFile}"
                    #------------------------------>
                    fileD[initStep/dataFile] = folderInit/nameF
                    #------------------------------>
                    self.rObj.rData[k][runN]['I'][next(keyI)] = nameF
                else:
                    fileD[initStep/dataFile] = folderInit/dataFile
                if k in self.cLSecSeqF:
                    dataFile = next(valI)
                    if (folderInit/dataFile).exists():
                        #------------------------------>
                        n = 1
                        dateFile, nameFile = dataFile.split('_')
                        nameF = f"{dateFile}M{n}_{nameFile}"
                        while (folderInit/nameF).exists():
                            n = n + 1
                            nameF = f"{dateFile}M{n}_{nameFile}"
                        #------------------------------>
                        fileD[initStep/dataFile] = folderInit/nameF
                        #------------------------------>
                        self.rObj.rData[k][runN]['I'][next(keyI)] = nameF
                    else:
                        fileD[initStep/dataFile] = folderInit/dataFile
                else:
                    pass
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        for k,v in folderD.items():
            shutil.copytree(k,v)
        #------------------------------>
        for k,v in fileD.items():
            shutil.copyfile(k,v)
        #------------------------------>
        self.rObj.Save()
        #------------------------------>
        self.UpdateFileContent()
        #endregion ------------------------------------------------>

        return True
    #---

    def ExportAnalysis(self, selItems:dict, *args) -> bool:                     # pylint: disable=unused-argument
        """Export analysis to a new UMSAP file.

            Parameters
            ----------
            selItems: dict
                Keys are Section names and values selected items.
            *args
                For compatibility. They are ignore.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        dlg = cWindow.FileSelect(
            'save', mConfig.core.elUMSAP, parent=self, msg='Select file')
        if dlg.ShowModal() == wx.ID_OK:
            fileP = Path(dlg.GetPath())
            name = fileP.name
            dlg.Destroy()
        else:
            dlg.Destroy()
            return True
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        step = fileP.parent/mConfig.core.fnDataSteps
        init = fileP.parent/mConfig.core.fnDataInit
        if step.exists() or init.exists():
            folderN = f'{cMethod.StrNow()}_UMSAP_Export'
            fileP = fileP.parent / folderN / name
        #------------------------------>
        folder = fileP.parent
        folderData = folder/mConfig.core.fnDataSteps
        folderInit = folder/mConfig.core.fnDataInit
        #------------------------------>
        dataStep = self.rObj.rStepDataP
        initStep = self.rObj.rInputFileP
        folderD  = {}
        fileD    = {}
        data     = {}
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        for k,d in selItems.items():
            #------------------------------>
            data[k] = data.get(k, {})
            #------------------------------>
            for run in d:
                #------------------------------>
                data[k][run] = self.rObj.rData[k][run]
                #------------------------------>
                folderD, fileD = self.GetFolderFile(
                    k, run, data[k][run]['I'], folderD, fileD, dataStep,
                    folderData, initStep, folderInit)
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        folder.mkdir(parents=True, exist_ok=True)
        #------------------------------>
        folderData.mkdir()
        for k,v in folderD.items():
            shutil.copytree(k,v)
        #------------------------------>
        folderInit.mkdir()
        for k,v in fileD.items():
            shutil.copyfile(k,v)
        #------------------------------>
        cFile.WriteJSON(fileP, data)
        #endregion ------------------------------------------------>

        return True
    #---

    def DeleteAnalysis(self, selItems:dict, *args) -> bool:                    # pylint: disable=unused-argument
        """Delete selected analysis.

            Parameters
            ----------
            selItems: dict
                Keys are Section names and values selected items.
            *args
                For compatibility. They are ignore.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        inputF = []
        folder = []
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        for k,v in selItems.items():
            #------------------------------> Analysis
            for item in v:
                #------------------------------> Folder
                folder.append(
                    self.rObj.rStepDataP/f"{item.split(' - ')[0]}_{k.replace(' ', '-')}")
                #------------------------------> Files
                iVal = iter(self.rObj.rData[k][item]['I'].values())
                inputF.append(next(iVal))
                if k in self.cLSecSeqF:
                    inputF.append(next(iVal))
                #------------------------------> Delete Analysis
                self.rObj.rData[k].pop(item)
            #------------------------------> Section
            if not self.rObj.rData[k]:
                self.rObj.rData.pop(k)
        #------------------------------> Full file
        if not self.rObj.rData:
            shutil.rmtree(self.rObj.rStepDataP)
            shutil.rmtree(self.rObj.rInputFileP)
            self.rObj.rFileP.unlink()
            if mConfig.core.os == 'Darwin':
                (self.rObj.rFileP.parent/'.DS_Store').unlink(missing_ok=True)
            #------------------------------>
            try:
                self.rObj.rFileP.parent.rmdir()
            except OSError:
                pass
            #------------------------------>
            self.OnClose('fEvent')
            return True
        #endregion ------------------------------------------------>

        #region -------------------------------------------------------->
        folder = list(set(folder))
        [shutil.rmtree(x) for x in folder]                                      # pylint: disable=expression-not-assigned
        #------------------------------>
        inputF = list(set(inputF))
        inputNeeded = self.rObj.GetInputFiles()
        for iFile in inputF:
            if iFile not in inputNeeded:
                (self.rObj.rInputFileP/iFile).unlink()
        #endregion ----------------------------------------------------->

        #region --------------------------------------------------->
        self.rObj.Save()
        self.UpdateFileContent()
        #endregion ------------------------------------------------>

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
        self.SetPosition(pt=(
            info['D']['xo'] + info['W']['N']*self.cSDeltaWin,
            info['D']['yo'] + info['W']['N']*self.cSDeltaWin,
        ))
        #endregion ---------------------------------------------> Set Position

        return True
    #---

    def SetTree(self) -> bool:
        """Set the elements of the wx.TreeCtrl.

            Returns
            -------
            bool

            Notes
            -----
            See data.file.UMSAPFile for the structure of obj.confTree.
        """
        #region ----------------------------------------------------> Add root
        root = self.wTrc.AddRoot(self.cTitle)
        #endregion -------------------------------------------------> Add root

        #region ------------------------------------------------> Add elements
        for a, b in self.rObj.rData.items():
            #------------------------------> Add section node
            childa = self.wTrc.AppendItem(root, a, ct_type=1)
            #------------------------------> Keep reference
            self.rSection[a] = childa
            #------------------------------>
            for c, d in b.items():
                #------------------------------> Add date node
                childb = self.wTrc.AppendItem(childa, c)
                self.wTrc.SetItemHyperText(childb, True)
                #------------------------------>
                for e, f in d['I'].items():
                    #------------------------------> Add date items
                    childc = self.wTrc.AppendItem(childb, f"{e}: {f}")
                    #------------------------------> Set font
                    if e.strip() in self.cFileLabelCheck:
                        fileP = self.rDataInitPath/f
                        if fileP.exists():
                            self.wTrc.SetItemFont(
                                childc, mConfig.core.fTreeItemDataFile)
                        else:
                            self.wTrc.SetItemFont(
                                childc, mConfig.core.fTreeItemDataFileFalse)
                    else:
                        self.wTrc.SetItemFont(
                            childc, mConfig.core.fTreeItemDataFile)
        #endregion ---------------------------------------------> Add elements

        #region -------------------------------------------------> Expand root
        self.wTrc.Expand(root)
        #endregion ----------------------------------------------> Expand root

        return True
    #---

    def UnCheckSection(self, sectionName:str, win:wx.Window) -> bool:
        """Method to uncheck a section when the plot window is closed by the
            user.

            Parameters
            ----------
            sectionName: str
                Section name like in config.nameModules config.nameUtilities
            win: wx.Window
                Window that was closed

            Returns
            -------
            bool
        """
        #region --------------------------------------------> Remove from list
        self.rWindow[sectionName]['Main'].remove(win)
        #endregion -----------------------------------------> Remove from list

        #region --------------------------------------------------> Update GUI
        if len(self.rWindow[sectionName]['Main']) > 0:
            return True
        #------------------------------> Remove check
        self.wTrc.SetItem3StateValue(
            self.rSection[sectionName], wx.CHK_UNCHECKED)
        #------------------------------> Repaint
        self.Update()
        self.Refresh()
        #------------------------------>
        return True
        #endregion -----------------------------------------------> Update GUI
    #---

    def UpdateFileContent(self) -> bool:
        """Update the content of the file.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        tSectionChecked = self.GetCheckedSection()
        #endregion ------------------------------------------------>

        #region ---------------------------------------------------> Read file
        try:
            self.rObj = resFile.UMSAPFile(self.rObj.rFileP)
        except Exception as e:
            raise e
        #endregion ------------------------------------------------> Read file

        #region --------------------------------------------------->
        self.rSection = {}
        #------------------------------>
        self.wTrc.DeleteAllItems()
        #------------------------------>
        self.SetTree()
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        for s in tSectionChecked:
            if self.rSection.get(s, False):
                #------------------------------> Check
                self.wTrc.SetItem3StateValue(
                    self.rSection[s], wx.CHK_CHECKED)
                #------------------------------> Win Menu
                if (win := self.rWindow[s].get('Main', False)):
                    for w in win:
                        w.UpdateUMSAPData()
            else:
                [x.Destroy() for v in self.rWindow[s].values() for x in v]      # pylint: disable=expression-not-assigned
        #endregion ------------------------------------------------>

        return True
    #---
    #endregion -----------------------------------------------> Manage Methods

    #region -----------------------------------------------------> Get Methods
    def GetCheckedSection(self) -> list[str]:
        """Get a list with the name of all checked sections.

            Returns
            -------
            bool
        """
        return [k for k, v in self.rSection.items() if v.IsChecked()]
    #---

    def GetFolderFile(
        self,
        sec:str,
        run:str,
        valI:dict,
        folderD:dict,
        fileD:dict,
        dataStep:Path,
        folderData:Path,
        initStep:Path,
        folderInit:Path,
        ) -> tuple[dict, dict]:
        """Get path to folders and files.

            Parameters
            ----------
            sec: str
                Analysis name.
            run: str
                Analysis ID.
            valI: dict
                Initial Data for the analysis.
            folderD: dict
                Folder paths.
            fileD: dict
                File paths.
            dataStep: Path
                Data Steps path
            folderData: Path
                Folder Path
            initStep: Path
                Path to the Initial files.
            folderInit: Path
                Path to the Initial files.
            Returns
            -------
            bool
        """
        #------------------------------>
        secN = sec.replace(' ', '-')
        secF = f"{run.split(' - ')[0]}_{secN}"
        folderD[dataStep/secF] = folderData/secF
        #------------------------------>
        val = iter(valI.values())
        dataFI = next(val)
        fileD[initStep/dataFI] = folderInit/dataFI
        if sec in self.cLSecSeqF:
            dataFI = next(val)
            fileD[initStep/dataFI] = folderInit/dataFI
        #------------------------------>
        return (folderD, fileD)
    #---
    #endregion --------------------------------------------------> Get Methods
#---


#------------------------------> wx.Dialog
class UMSAPAddDelExport(cWindow.BaseDialogOkCancel):
    """Dialog to select items from an UMSAP file in order to Add/Del/Export
        the selected items.

        Parameters
        ----------
        obj: mFile.UMSAPFile
            UMSAP File object.
        mode: str
            Add/Del/Export

        Attributes
        ----------
        rSelItem: dict
            Key are sections and values selected items.
    """
    #region -----------------------------------------------------> Class setup
    cSize = (400, 700)
    cLBtnOpt = {
        mConfig.res.lmToolUMSAPCtrlAdd: 'Add',
        mConfig.res.lmToolUMSAPCtrlDel: 'Delete',
        mConfig.res.lmToolUMSAPCtrlExp: 'Export',
    }
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, obj:resFile.UMSAPFile, mode:str) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.rObj = obj
        self.mode = mode
        #------------------------------>
        self.cLBtn = self.cLBtnOpt[mode]
        self.cTitle = f'{self.cLBtn} data from: {self.rObj.rFileP.name}'
        #------------------------------>
        super().__init__(title=self.cTitle, parent=None)
        self.FindWindowById(wx.ID_OK).SetLabel(self.cLBtn)
        #------------------------------>
        self.rSelItems = {}
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wTrc = wxCT.CustomTreeCtrl(self)
        self.wTrc.SetFont(mConfig.core.fTreeItem)
        self.SetTree()
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        self.sSizer.Add(self.wTrc, 1, wx.EXPAND|wx.ALL, 5)
        self.sSizer.Add(self.sBtn, 0, wx.ALIGN_RIGHT|wx.ALL, 5)
        #------------------------------>
        self.SetSizer(self.sSizer)
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind
        self.wTrc.Bind(wxCT.EVT_TREE_ITEM_CHECKED, self.OnCheckItem)
        #endregion -----------------------------------------------------> Bind

        #region ---------------------------------------------> Window position
        self.Center()
        #endregion ------------------------------------------> Window position
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Event Methods
    def OnCheckItem(self, event:wx.Event) -> bool:
        """Adjust checked items.

            Parameters
            ----------
            event: wx.Event
                Information about the event.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        item     = event.GetItem()                                              # type: ignore
        checked  = self.wTrc.IsItemChecked(item)
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        if checked:
            #------------------------------> Check all children
            for child in item.GetChildren():
                child.Set3StateValue(wx.CHK_CHECKED)
                for gchild in child.GetChildren():
                    gchild.Set3StateValue(wx.CHK_CHECKED)
            #------------------------------> Check parent or not
            parent = item.GetParent()
            if parent is not None:
                if all([x.IsChecked() for x in parent.GetChildren()]):
                    parent.Set3StateValue(wx.CHK_CHECKED)
                    gparent = parent.GetParent()
                    if gparent is not None:
                        if all([x.IsChecked() for x in gparent.GetChildren()]):
                            gparent.Set3StateValue(wx.CHK_CHECKED)
        else:
            #------------------------------> Uncheck all children
            for child in item.GetChildren():
                child.Set3StateValue(wx.CHK_UNCHECKED)
                for gchild in child.GetChildren():
                    gchild.Set3StateValue(wx.CHK_UNCHECKED)
            #------------------------------> Unchecked all parent
            parent = item.GetParent()
            if parent is not None:
                parent.Set3StateValue(wx.CHK_UNCHECKED)
                gparent = parent.GetParent()
                if gparent is not None:
                    gparent.Set3StateValue(wx.CHK_UNCHECKED)
        #------------------------------>
        self.Update()
        self.Refresh()
        #endregion ------------------------------------------------>

        event.Skip()
        return True
    #---

    def OnOK(self, event: wx.CommandEvent) -> bool:
        """Check Dialog input.

            Parameters
            ----------
            event: wx.Event
                Information about the event.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        root = self.wTrc.GetRootItem()
        self.rSelItems = {}
        checked = []
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        for child in root.GetChildren():                                        # type: ignore
            #------------------------------>
            childN = child.GetText()
            gchildL = child.GetChildren()
            #------------------------------>
            for gchild in gchildL:
                if gchild.IsChecked():
                    self.rSelItems[childN] = self.rSelItems.get(childN, [])
                    self.rSelItems[childN].append(gchild.GetText())
                    checked.append(True)
        #------------------------------>
        if not checked:
            msg = ('There are no analysis selected. Please select something '
                   'first.')
            cWindow.Notification('warning', msg=msg)
            return False
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        self.EndModal(1)
        self.Close()
        #endregion ------------------------------------------------>

        return True
    #---
    #endregion ------------------------------------------------> Event Methods

    #region ---------------------------------------------------> Class Methods
    def SetTree(self) -> bool:
        """Set the elements of the wx.TreeCtrl.

            Returns
            -------
            bool

            Notes
            -----
            See data.file.UMSAPFile for the structure of obj.confTree.
        """
        #region ----------------------------------------------------> Add root
        root = self.wTrc.AddRoot(self.rObj.rFileP.name, ct_type=1)
        #endregion -------------------------------------------------> Add root

        #region ------------------------------------------------> Add elements
        for a, b in self.rObj.rData.items():
            #------------------------------> Add section node
            childa = self.wTrc.AppendItem(root, a, ct_type=1)
            for c, d in b.items():
                #------------------------------> Add date node
                childb = self.wTrc.AppendItem(childa, c, ct_type=1)
                for e, f in d['I'].items():
                    #------------------------------> Add date items
                    childc = self.wTrc.AppendItem(childb, f"{e}: {f}")
                    self.wTrc.SetItemFont(
                        childc, mConfig.core.fTreeItemDataFile)
        #endregion ---------------------------------------------> Add elements

        #region -------------------------------------------------> Expand root
        self.wTrc.Expand(root)
        [child.Expand() for child in root.GetChildren()]                        # pylint: disable=expression-not-assigned
        #endregion ----------------------------------------------> Expand root

        return True
    #---
    #endregion ------------------------------------------------> Class Methods
#---
#endregion ----------------------------------------------------------> Classes
