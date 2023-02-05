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


"""Windows for the help module of the app"""


#region -------------------------------------------------------------> Imports
from typing import Optional, Union

import wx
import wx.lib.agw.hyperlink as hl
from wx import adv

from config.config import config as mConfig
from core import file   as cFile
from core import window as cWindow
from help import pane   as hPane
from main import menu   as mMenu
#endregion ----------------------------------------------------------> Imports


#region --------------------------------------------------------------> Frames
class WindowAbout(cWindow.BaseWindow):
    """About UMSAP window."""
    #region -----------------------------------------------------> Class setup
    cName  = mConfig.help.nwAbout
    cTitle = mConfig.help.twAbout
    #------------------------------>
    cSWindow = (600, 775)
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self):
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__()
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.SetBackgroundColour('white')
        #------------------------------>
        self.wImg = wx.StaticBitmap(self, wx.ID_ANY,
            wx.Bitmap(str(mConfig.core.fImgAbout), wx.BITMAP_TYPE_PNG))
        self.wCopyRight = wx.StaticText(
            self, label='Copyright © 2017 Kenny Bravo Rodriguez')
        #------------------------------>
        self.wText = wx.TextCtrl(
            self,
            size  = (100, 500),
            style = wx.TE_MULTILINE|wx.TE_WORDWRAP|wx.TE_READONLY
        )
        self.wText.AppendText(myText)
        self.wText.SetInsertionPoint(0)
        #------------------------------>
        self.wLink = hl.HyperLinkCtrl(
            self,
            -1,
            mConfig.core.urlHome,
            URL=mConfig.core.urlHome,
        )
        #------------------------------>
        self.wBtn = wx.Button(self, id=wx.ID_OK, label='OK')
        self.wBtn.SetFocus()
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        self.sBtn = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.sBtn.Add(self.wLink, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.sBtn.AddStretchSpacer()
        self.sBtn.Add(self.wBtn, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        #------------------------------>
        self.sSizer.Add(self.wImg,       0, wx.ALIGN_CENTER|wx.ALL, 5)
        self.sSizer.Add(self.wCopyRight, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        self.sSizer.Add(self.wText,      1, wx.EXPAND|wx.ALL, 5)
        self.sSizer.Add(self.sBtn,       0, wx.EXPAND|wx.ALL, 5)
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Menu
        self.mBar = mMenu.MenuBarTool(self.cName)
        self.SetMenuBar(self.mBar)
        #endregion -----------------------------------------------------> Menu

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_BUTTON, self.OnButtonClose, source=self.wBtn)
        #endregion -----------------------------------------------------> Bind

        #region ---------------------------------------------> Window position
        self.Center()
        self.Show()
        #endregion ------------------------------------------> Window position
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Event Methods
    def OnButtonClose(self, event:wx.CommandEvent) -> bool:                     # pylint: disable=unused-argument
        """Close the window

            Parameters
            ----------
            event: wx.CommandEvent
                Information about the event.

            Returns
            -------
            bool
        """
        self.Close()
        return True
    #---
    #endregion ------------------------------------------------> Event Methods
#---
#endregion -----------------------------------------------------------> Frames


#region -------------------------------------------------------------> Dialogs
class Preference(wx.Dialog):
    """Set the UMSAP preferences."""
    #region -----------------------------------------------------> Class setup
    cName = mConfig.help.ndPreferences
    cTitle = mConfig.help.tdPrefUpdate
    #------------------------------>
    cStyle = wx.CAPTION|wx.CLOSE_BOX|wx.RESIZE_BORDER
    #------------------------------>
    cSize = (340,200)
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self):
        """ """
        #region -----------------------------------------------> Initial Setup
        super().__init__(
            None,
            title = self.cTitle,
            style = self.cStyle,
            size  = self.cSize,
            name  = self.cName,
        )
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.wNoteBook = wx.Notebook(self, style=wx.NB_TOP)
        #------------------------------>
        self.wUpdate = hPane.PrefUpdate(self.wNoteBook)
        self.wNoteBook.AddPage(self.wUpdate, self.wUpdate.cLTab)
        #------------------------------>
        self.sBtn = self.CreateButtonSizer(wx.OK|wx.CANCEL|wx.NO)
        self.FindWindowById(wx.ID_OK).SetLabel('Save')
        self.FindWindowById(wx.ID_CANCEL).SetLabel('Cancel')
        self.FindWindowById(wx.ID_NO).SetLabel('Load Defaults')
        #------------------------------>
        self.OnDefault('fEvent')
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        self.sSizer = wx.BoxSizer(orient=wx.VERTICAL)
        #------------------------------>
        self.sSizer.Add(self.wNoteBook, 1, wx.EXPAND|wx.ALL, 5)
        self.sSizer.Add(self.sBtn, 0, wx.ALIGN_RIGHT|wx.ALL, 5)
        #------------------------------>
        self.SetSizer(self.sSizer)
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind
        self.Bind(wx.EVT_BUTTON, self.OnSave,    id=wx.ID_OK)
        self.Bind(wx.EVT_BUTTON, self.OnCancel,  id=wx.ID_CANCEL)
        self.Bind(wx.EVT_BUTTON, self.OnDefault, id=wx.ID_NO)
        #endregion -----------------------------------------------------> Bind

        #region ---------------------------------------------> Window position
        self.Center()
        self.ShowModal()
        self.Destroy()
        #endregion ------------------------------------------> Window position
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def OnSave(self, event:wx.CommandEvent) -> bool:                            # pylint: disable=unused-argument
        """Save the preferences.

            Parameters
            ----------
            event: wx.CommandEvent
                Information about the event.

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Set
        #------------------------------> Update
        mConfig.core.checkUpdate = not bool(
            self.wUpdate.wRBox.GetSelection())
        #endregion ------------------------------------------------>

        #region ---------------------------------------------------> Save
        data = {}
        #------------------------------>
        for secStr in mConfig.core.confList:
            #------------------------------>
            sec = getattr(mConfig, secStr, None)
            #------------------------------>
            if sec is None:
                continue
            #------------------------------>
            secDict = {}
            for k in sec.converter:
                secDict[k] = getattr(sec, k)
            #------------------------------>
            data[secStr] = secDict
        #------------------------------>
        try:
            cFile.WriteJSON(mConfig.core.fConfig, data)
        except Exception as e:
            msg = 'Configuration options could not be saved.'
            cWindow.Notification('errorF', msg=msg, tException=e)
            return False
        #endregion ------------------------------------------------>

        self.EndModal(1)
        return True
    #---

    def OnCancel(self, event:wx.CommandEvent) -> bool:                          # pylint: disable=unused-argument
        """Close the window.

            Parameters
            ----------
             event: wx.CommandEvent
                Information about the event.

            Returns
            -------
            bool
        """
        self.EndModal(0)
        return True
    #---

    def OnDefault(self, event:Union[wx.CommandEvent, str]) -> bool:
        """Set default options.

            Parameters
            ----------
             event: wx.CommandEvent
                Information about the event.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        if isinstance(event, str):
            data = self.GetConfConf()
        else:
            data = self.GetConfFile()
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        if data:
            return self.SetConfValues(data)
        #endregion ------------------------------------------------>

        return False
    #---

    def GetConfFile(self) -> dict:
        """Get default data from file.

            Parameters
            ----------
             event : wx.CommandEvent
                Information about the event.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        try:
            data = cFile.ReadJSON(mConfig.core.fConfigDef)
        except Exception as e:
            msg = 'It was not possible to read the default configuration file.'
            cWindow.Notification('errorF', msg=msg, tException=e)
            return {}
        #endregion ------------------------------------------------>

        return data
    #---

    def GetConfConf(self) -> dict:
        """Get default options from current options.

            Parameters
            ----------
             event : wx.CommandEvent
                Information about the event.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        data = {}
        #------------------------------>
        for secStr in mConfig.core.confList:
            #------------------------------>
            sec = getattr(mConfig, secStr, None)
            #------------------------------>
            if sec is None:
                continue
            #------------------------------>
            secDict = {}
            for k in sec.converter:
                secDict[k] = getattr(sec,k)
            #------------------------------>
            data[secStr] = secDict
        #endregion ------------------------------------------------>

        return data
    #---

    def SetConfValues(self, data:dict) -> bool:
        """Set the default values.

            Parameters
            ----------
            data: dict
                Data to be set.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        try:
            #------------------------------> Update
            val = 0 if data['core']['checkUpdate'] else 1
            self.wUpdate.wRBox.SetSelection(val)
        except Exception as e:
            msg = 'Something went wrong when loading the configuration options.'
            cWindow.Notification('errorU', msg=msg, tException=e)
            return False
        #endregion ------------------------------------------------>

        return True
    #---
    #endregion ------------------------------------------------> Class methods
#---


class CheckUpdateResult(wx.Dialog):
    """Show a dialog with the result of the check for update operation.

        Parameters
        ----------
        parent: wx widget or None
            To center the dialog in parent. Default None.
        checkRes: str or None
            Internet latest version. Default None.
    """
    #region -----------------------------------------------------> Class setup
    cName  = mConfig.help.ndCheckUpdateResDialog
    cTitle = mConfig.help.tdCheckUpdate
    #------------------------------> Style
    cStyle = wx.CAPTION|wx.CLOSE_BOX
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self,
        parent:Optional[wx.Window] = None,
        checkRes:str               = '',
        ) -> None:
        """"""
        #region -----------------------------------------------> Initial setup
        super().__init__(
            parent, title=self.cTitle, style=self.cStyle, name=self.cName)
        #endregion --------------------------------------------> Initial setup

        #region -----------------------------------------------------> Widgets
        #------------------------------> Msg
        if checkRes:
            msg = (f'UMSAP {checkRes} is already available.\nYou are '
                f'currently using UMSAP {mConfig.core.version}.')
        else:
            msg = 'You are using the latest version of UMSAP.'
        self.wMsg = wx.StaticText(self, label=msg, style=wx.ALIGN_LEFT)
        #------------------------------> Link
        if checkRes:
            self.wStLink = adv.HyperlinkCtrl(
                self, label='Read the Release Notes.', url=mConfig.core.urlUpdate)
        #------------------------------> Img
        self.wImg = wx.StaticBitmap(
            self, bitmap=wx.Bitmap(str(mConfig.core.fImgIcon), wx.BITMAP_TYPE_PNG))
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        #------------------------------> Button Sizers
        self.sBtn = self.CreateStdDialogButtonSizer(wx.OK)
        #------------------------------> TextSizer
        self.sText = wx.BoxSizer(wx.VERTICAL)
        self.sText.Add(self.wMsg, 0, wx.ALIGN_LEFT|wx.ALL, 10)
        if checkRes:
            self.sText.Add(self.wStLink, 0, wx.ALIGN_CENTER|wx.ALL, 10)
        #------------------------------> Image Sizer
        self.sImg = wx.BoxSizer(wx.HORIZONTAL)
        self.sImg.Add(self.wImg, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.sImg.Add(
            self.sText, 0, wx.ALIGN_LEFT|wx.LEFT|wx.TOP|wx.BOTTOM, 5)
        #------------------------------> Main Sizer
        self.sSizer = wx.BoxSizer(wx.VERTICAL)
        self.sSizer.Add(
            self.sImg, 0, wx.ALIGN_CENTER|wx.TOP|wx.LEFT|wx.RIGHT, 25)
        self.sSizer.Add(
            self.sBtn, 0, wx.ALIGN_RIGHT|wx.RIGHT|wx.BOTTOM, 10)
        #------------------------------>
        self.SetSizer(self.sSizer)
        self.sSizer.Fit(self)
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind
        if checkRes:
            self.wStLink.Bind(adv.EVT_HYPERLINK, self.OnLink)
        #endregion -----------------------------------------------------> Bind

        #region ---------------------------------------------> Position & Show
        self.CentreOnParent()
        self.ShowModal()
        self.Destroy()
        #endregion ------------------------------------------> Position & Show
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Event Methods
    def OnLink(self, event:wx.Event) -> bool:
        """Process the link event.

            Parameters
            ----------
            event: wx.adv.HyperlinkEvent
                Information about the event.

            Returns
            -------
            bool
        """
        #------------------------------>
        event.Skip()
        self.EndModal(1)
        self.Destroy()
        #------------------------------>
        return True
    #endregion ------------------------------------------------> Event Methods
#---
#endregion ----------------------------------------------------------> Dialogs


#region ----------------------------------------------------------> ABOUT TEXT
myText = """UMSAP: Fast post-processing of mass spectrometry data

-- Modules and Python version --

UMSAP 2.2.1 is written in Python 3.9.15 and uses the following modules:

Biopython 1.79
Matplotlib 3.5.1
NumPy 1.23.5
Pandas 1.2.3
PyInstaller 5.7.0
Python 3.9.15
ReportLab 3.6.8
Requests 2.27.0
Scipy 1.9.3
Statsmodels 0.13.5
wxPython 4.1.1

Copyright notice and License for the modules can be found in the User's manual of UMSAP.

-- Acknowledgments --

I would like to thank all the persons that have contributed to the development
of UMSAP, either by contributing ideas and suggestions or by testing the code.
Special thanks go to: Dr. Farnusch Kaschani, Dr. Juliana Rey, Dr. Petra Janning
and Prof. Dr. Daniel Hoffmann.

In particular, I would like to thank Prof. Dr. Michael Ehrmann.

-- License Agreement --

Utilities for Mass Spectrometry Analysis of Proteins and its source code are governed by the following license:

Upon execution of this Agreement by the party identified below (”Licensee”), Kenny Bravo Rodriguez (KBR) will provide the Utilities for Mass Spectrometry Analysis of Proteins software in Executable Code and/or Source Code form (”Software”) to Licensee, subject to the following terms and conditions. For purposes of this Agreement, Executable Code is the compiled code, which is ready to run on Licensee’s computer. Source code consists of a set of files, which contain the actual program commands that are compiled to form the Executable Code.

1. The Software is intellectual property owned by KBR, and all rights, title and interest, including copyright, remain with KBR. KBR grants, and Licensee hereby accepts, a restricted, non-exclusive, non-transferable license to use the Software for academic, research and internal business purposes only, e.g. not for commercial use (see Clause 7 below), without a fee.

2. Licensee may, at its own expense, create and freely distribute complimentary works that inter-operate with the Software, directing others to the Utilities for Mass Spectrometry Analysis of Proteins web page to license and obtain the Software itself. Licensee may, at its own expense, modify the Software to make derivative works. Except as explicitly provided below, this License shall apply to any derivative work as it does to the original Software distributed by KBR. Any derivative work should be clearly marked and renamed to notify users that it is a modified version and not the original Software distributed by KBR. Licensee agrees to reproduce the copyright notice and other proprietary markings on any derivative work and to include in the documentation of such work the acknowledgment: ”This software includes code developed by Kenny Bravo Rodriguez for the Utilities for Mass Spectrometry Analysis of Proteins software”.
Licensee may not sell any derivative work based on the Software under any circumstance. For commercial distribution of the Software or any derivative work based on the Software a separate license is required. Licensee may contact KBR to negotiate an appropriate license for such distribution.

3. Except as expressly set forth in this Agreement, THIS SOFTWARE IS PROVIDED ”AS IS” AND KBR MAKES NO REPRESENTATIONS AND EXTENDS NO WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO WARRANTIES OR MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE, OR THAT THE USE OF THE SOFTWARE WILL NOT INFRINGE ANY PATENT, TRADEMARK, OR OTHER RIGHTS. LICENSEE ASSUMES THE ENTIRE RISK AS TO THE RESULTS AND PERFORMANCE OF THE SOFTWARE AND/OR ASSOCIATED MATERIALS. LICENSEE AGREES THAT KBR SHALL NOT BE HELD LIABLE FOR ANY DIRECT, INDIRECT, CONSEQUENTIAL, OR INCIDENTAL DAMAGES WITH RESPECT TO ANY CLAIM BY LICENSEE OR ANY THIRD PARTY ON ACCOUNT OF OR ARISING FROM THIS AGREEMENT OR USE OF THE SOFTWARE AND/OR ASSOCIATED MATERIALS.

4. Licensee understands the Software is proprietary to KBR. Licensee agrees to take all reasonable steps to insure that the Software is protected and secured from unauthorized disclosure, use, or release and will treat it with at least the same level of care as Licensee would use to protect and secure its own proprietary computer programs and/or information, but using no less than a reasonable standard of care. Licensee agrees to provide the Software only to any other person or entity who has registered with KBR. If Licensee is not registering as an individual but as an institution or corporation each member of the institution or corporation who has access to or uses Software must agree to and abide by the terms of this license. If Licensee becomes aware of any unauthorized licensing, copying or use of the Software, Licensee shall promptly notify KBR in writing. Licensee expressly agrees to use the Software only in the manner and for the specific uses authorized in this Agreement.

5. KBR shall have the right to terminate this license immediately by written notice upon Licensee’s breach of, or non-compliance with, any terms of the license. Licensee may be held legally responsible for any copyright infringement that is caused or encouraged by its failure to abide by the terms of this license. Upon termination, Licensee agrees to destroy all copies of the Software in its possession and to verify such destruction in writing.

6. Licensee agrees that any reports or published results obtained with the Software will acknowledge its use by the appropriate citation as follows:
”Utilities for Mass Spectrometry Analysis of Proteins was created by Kenny Bravo Rodriguez at the University of Duisburg-Essen and is currently developed at the Max Planck Institute of Molecular Physiology.”
Any published work, which utilizes Utilities for Mass Spectrometry Analysis of Proteins, shall include the following reference:
Kenny Bravo-Rodriguez, Birte Hagemeier, Lea Drescher, Marian Lorenz, Michael Meltzer, Farnusch Kaschani, Markus Kaiser and Michael Ehrmann. (2018). Utilities for Mass Spectrometry Analysis of Proteins (UMSAP): Fast post-processing of mass spectrometry data. Rapid Communications in Mass Spectrometry, 32(19), 1659–1667.
Electronic documents will include a direct link to the official Utilities for Mass Spectrometry Analysis of Proteins page at: www.umsap.nl

7. Commercial use of the Software, or derivative works based thereon, REQUIRES A COMMERCIAL LICENSE. Should Licensee wish to make commercial use of the Software, Licensee will contact KBR to negotiate an appropriate license for such use. Commercial use includes: (1) integration of all or part of the Software into a product for sale, lease or license by or on behalf of Licensee to third parties, or (2) distribution of the Software to third parties that need it to commercialize product sold or licensed by or on behalf of Licensee.

8. Utilities for Mass Spectrometry Analysis of Proteins is being distributed as a research tool and as such, KBR encourages contributions from users of the code that might, at KBR’s sole discretion, be used or incorporated to make the basic operating framework of the Software a more stable, flexible, and/or useful product. Licensees who contribute their code to become an internal portion of the Software agree that such code may be distributed by KBR under the terms of this License and may be required to sign an ”Agreement Regarding Contributory Code for Utilities for Mass Spectrometry Analysis of Proteins Software” before KBR can accept it (contact umsap@umsap.nl for a copy).

UNDERSTOOD AND AGREED.

Contact Information:

The best contact path for licensing issues is by e-mail to umsap@umsap.nl
"""
#endregion -------------------------------------------------------> ABOUT TEXT
