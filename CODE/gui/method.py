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


""" GUI common methods """


#region -------------------------------------------------------------> Imports
import _thread
from pathlib import Path
from typing import Optional

import wx

import dat4s_core.gui.wx.method as dtsGwxMethod

import config.config as config
import data.file as file
import gui.dtscore as dtscore
import gui.window as window
#endregion ----------------------------------------------------------> Imports


def LoadUMSAPFile(
    fileP: Optional[Path]=None, win: Optional[wx.Window]=None, 
    shownSection: Optional[list[str]]=None
    ) -> bool:
    """Load an UMSAP File either from Read UMSAP File menu, LoadResults
        method in Tab or Update File Content menu.

        Parameters
        ----------
        fileP : Path or None
            If None, it is assumed the method is called from Read UMSAP File
            menu. Default is None.
        win : wx.Window or None
            If called from menu it is used to center the Select file dialog.
            Default is None.
        shownSection : list of str or None
            List with the name of all checked sections in File Control window.
            
        Return
        ------
        bool
    """   
    #region --------------------------------------------> Get file from Dialog
    if fileP is None:
        try:
            #------------------------------> Get File
            filePdlg = dtsGwxMethod.GetFilePath(
                'openO', ext=config.elUMSAP, parent=win, msg=config.mUMSAPFile,
            )
            #------------------------------> Set Path
            if filePdlg is None:
                return False
            else:
                tFileP = Path(filePdlg[0])
        except Exception as e:      
            dtscore.Notification(
                'errorF', 
                msg        = config.mFileSelector,
                tException = e,
                parent     = win,
            )
            return False
    else:
        tFileP = fileP
    #endregion -----------------------------------------> Get file from Dialog
    
    #region ----------------------------> Raise window if file is already open
    if shownSection is None:
        #------------------------------> Check file is opened & Raise it
        if config.winUMSAP.get(tFileP, '') != '':
            config.winUMSAP[tFileP].UpdateFileContent()
            return True
        else:
            pass		
    else:
        #------------------------------> Check file is opened & Close window
        if config.winUMSAP.get(tFileP, '') != '':
            config.winUMSAP[tFileP].Close()
        else:
            pass
    #endregion -------------------------> Raise window if file is already open

    #region ---------------------------------------------> Progress Dialog
    dlg = dtscore.ProgressDialog(None, f"Analysing file {tFileP.name}", 100)
    #endregion ------------------------------------------> Progress Dialog

    #region -----------------------------------------------> Configure obj
    #------------------------------> UMSAPFile obj is placed in config.obj
    _thread.start_new_thread(_LoadUMSAPFile, (tFileP, dlg))
    #endregion --------------------------------------------> Configure obj

    #region --------------------------------------------------> Show modal
    if dlg.ShowModal() == 1:
        config.winUMSAP[tFileP] = window.UMSAPControl(
            config.obj, 
            shownSection = shownSection,
        )
    else:
        pass

    dlg.Destroy()
    #endregion -----------------------------------------------> Show modal

    return True
#---

def _LoadUMSAPFile(fileP: Path, dlg: dtscore.ProgressDialog) -> bool:
    """Load an UMSAP file

        Parameters
        ----------
        fileP : Path
            Path to the UMSAP file
        parent : wx.Window or None
            To center notification alert

        Returns
        -------
        Boolean
    """	
    #region -------------------------------------------------------> Variables
    N = 1 # Extra steps for the gauge in the Progress Dialog
    #endregion ----------------------------------------------------> Variables
    
    #region -------------------------------------------------------> Read file
    wx.CallAfter(dlg.UpdateStG, f"Reading file: {fileP.name}")
    try:
        config.obj = file.UMSAPFile(fileP)
    except Exception as e:
        wx.CallAfter(dlg.ErrorMessage,
            label = config.lPdError,
            error        = str(e),
            tException = e,
        )
    #endregion ----------------------------------------------------> Read file

    #region --------------------------------------------------> Configure file
    dlg.g.SetRange((2*config.obj.GetSectionCount())+N)
    config.obj.Configure(dlg)
    #endregion -----------------------------------------------> Configure file
    
    return True
#---

def GetDisplayInfo(win: wx.Frame) -> dict[str, dict[str, int]]:
    """This will get the information needed to set the position of a window.
        Should be called after Fitting sizers for accurate window size 
        information

        Parameters
        ----------
        win : wx.Frame
            Window to be positioned

        Returns
        -------
        dict
            {
                'D' : {'xo':X, 'yo':Y, 'w':W, 'h':h}, Info about display
                'W' : {'N': N, 'w':W, 'h', H},        Info about win
            }
    """
    
    #region ----------------------------------------------------> Display info
    d = wx.Display(win)
    xd, yd, wd, hd = d.GetClientArea()
    #endregion -------------------------------------------------> Display info
    
    #region -----------------------------------------------------> Window info
    nw = config.winNumber.get(win.name, 0)
    ww, hw = win.GetSize()
    #endregion --------------------------------------------------> Window info
    
    #region ------------------------------------------------------------> Dict
    data = {
        'D' : {
            'xo' : xd,
            'yo' : yd,
            'w'  : wd,
            'h'  : hd,
        },
        'W' : {
            'N' : nw,
            'w' : ww,
            'h' : hw,
        },
    }
    #endregion ---------------------------------------------------------> Dict
    
    return data
#---