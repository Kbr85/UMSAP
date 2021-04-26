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


"""Derived classes from DAT4S - Core"""


#region -------------------------------------------------------------> Imports
from pathlib import Path
from typing import Optional

import wx

import dat4s_core.gui.wx.window as dtsWindow
# import dat4s_core.gui.wx.widget as dtsWidget

import config.config as config
#endregion ----------------------------------------------------------> Imports


class Notification(dtsWindow.NotificationDialog):
    """This avoids to type the title and the image of the window every time    """
    def __init__(self, mode: str, msg: Optional[str]=None, 
        tException: Optional[Exception]=None, parent: Optional[wx.Window]=None, 
        img: Path=config.fImgIcon, button: int=1,) -> None:
        """ """
        super().__init__(mode, msg=msg, tException=tException, parent=parent,
            button=button, img=img, title='UMSAP - Notification')
    #---
#---

# class ProgressDialog(dtsWindow.ProgressDialog):
#     """This avoids to type the icon every time """
#     def __init__(self, parent: Optional[wx.Window], title: str, count: int, 
#         img: Path=config.fImgIcon, 
#         style=wx.CAPTION|wx.CLOSE_BOX|wx.RESIZE_BORDER) -> None:    
#         """"""
#         super().__init__(parent, title, count, img=img, style=style)
#     #---
# #---

# class ListZebra(dtsWidget.ListZebra):
#     """ This avoids defining the color for the zebra style every time """
#     def __init__(self, parent:wx.Window, color: str=config.color['Zebra'], 
#         colLabel: Optional[list[str]]=None, colSize: Optional[list[int]]=None, 
#         canCopy: bool=True, canCut: bool=False, canPaste: bool=False, 
#         copyFullContent: bool=False, pasteUnique: bool=True, selAll:bool=True, 
#         style=wx.LC_REPORT) -> None:
#         """"""
#         super().__init__(
#             parent, color=color, colLabel=colLabel, colSize=colSize, 
#             canCopy=canCopy, canCut=canCut, canPaste=canPaste, 
#             copyFullContent=copyFullContent, pasteUnique=pasteUnique, 
#             selAll=selAll, style=style)
#     #---
# #---

# class ListZebraMaxWidth(dtsWidget.ListZebraMaxWidth):
#     """This avoids defining the color for the zebra style every time """
#     def __init__(self, parent: wx.Window, color: str=config.color['Zebra'], 
#         colLabel: Optional[list[str]]=None, colSize: Optional[list[int]]=None, 
#         canCopy: bool=True, canCut:bool=False, canPaste: bool=False, 
#         copyFullContent: bool=False, pasteUnique: bool=True, selAll: bool=True, 
#         style=wx.LC_REPORT):
#         """"""
#         super().__init__(
#             parent, color=color, colLabel=colLabel, colSize=colSize, 
#             canCopy=canCopy, canCut=canCut, canPaste=canPaste, 
#             copyFullContent=copyFullContent, pasteUnique=pasteUnique, 
#             selAll=selAll, style=style)
#     #---    
    
    
