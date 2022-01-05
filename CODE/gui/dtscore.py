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


# """Derived classes from DAT4S - Core"""


# #region -------------------------------------------------------------> Imports
# from pathlib import Path
# from typing import Optional, Literal

# import wx

# import dat4s_core.data.method as dtsMethod
# import dat4s_core.gui.wx.widget as dtsWidget
# import dat4s_core.gui.wx.window as dtsWindow

# import config.config as config
# #endregion ----------------------------------------------------------> Imports


# #region -------------------------------------------------------------> Methods
# def StrSetMessage(
#     start: str, end: str, link: str='\n\nFurther details:\n'
#     )-> str:
#     """Default link for message in Progress Dialog.

#         Parameters
#         ----------
#         start: str
#             Start of the message
#         end: str
#             End of the message
#         link : str
#             Link between strat and end. Default is '\n\nFurther details:\n'


#         Returns
#         -------
#         str:
#             The full message
#     """
#     return dtsMethod.StrSetMessage(start, end, link=link)
# #---
# #endregion ----------------------------------------------------------> Methods


# #region -------------------------------------------------------------> Classes
# class Notification(dtsWindow.NotificationDialog):
#     """This avoids to type the title and the image of the window every time """
#     def __init__(
#         self, 
#         mode: Literal['errorF', 'errorU', 'warning', 'success', 'question'], 
#         msg: Optional[str]=None, tException: Optional[Exception]=None, 
#         parent: Optional[wx.Window]=None, img: Path=config.fImgIcon, 
#         button: int=1, setText=False
#         ) -> None:
#         """ """
#         super().__init__(mode, msg=msg, tException=tException, parent=parent,
#             button=button, img=img, title='UMSAP - Notification', 
#             setText=setText)
#     #---
# #---

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
#         copyFullContent: bool=False, sep: str=' ', pasteUnique: bool=True, 
#         selAll:bool=True, style=wx.LC_REPORT) -> None:
#         """"""
#         super().__init__(
#             parent, color=color, colLabel=colLabel, colSize=colSize, 
#             canCopy=canCopy, canCut=canCut, canPaste=canPaste, 
#             copyFullContent=copyFullContent, sep=sep, pasteUnique=pasteUnique, 
#             selAll=selAll, style=style)
#     #---
# #---

# class ListZebraMaxWidth(dtsWidget.ListZebraMaxWidth):
#     """This avoids defining the color for the zebra style every time """
#     def __init__(self, parent: wx.Window, color: str=config.color['Zebra'], 
#         colLabel: Optional[list[str]]=None, colSize: Optional[list[int]]=None, 
#         canCopy: bool=True, canCut:bool=False, canPaste: bool=False, 
#         copyFullContent: bool=False, sep: str=' ', pasteUnique: bool=True, 
#         selAll: bool=True, style=wx.LC_REPORT):
#         """"""
#         super().__init__(
#             parent, color=color, colLabel=colLabel, colSize=colSize, 
#             canCopy=canCopy, canCut=canCut, canPaste=canPaste, 
#             copyFullContent=copyFullContent, sep=sep, pasteUnique=pasteUnique, 
#             selAll=selAll, style=style)
#     #---    
# #---
# #endregion ----------------------------------------------------------> Classes


    
    
