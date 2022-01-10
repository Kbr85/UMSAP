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


# """ Widgets of the application"""


# #region -------------------------------------------------------------> Imports
# import wx

# import dat4s_core.gui.wx.validator as dtsValidator

# import config.config as config
# import gui.window as window
# #endregion ----------------------------------------------------------> Imports


# class ResControl():
#     """Creates the Results - Control experiment widgets.

#         Parameters
#         ----------
#         cParent : wx widget
#             Parent of the widgets
#     """
#     #region -----------------------------------------------------> Class setup
#     cLResControl = config.lStResultCtrl
#     #endregion --------------------------------------------------> Class setup

#     #region --------------------------------------------------> Instance setup
#     def __init__(self, cParent: wx.Window) -> None:
#         """ """
#         #region -----------------------------------------------------> Widgets
#         self.wTcResults = wx.TextCtrl(
#             parent    = cParent,
#             style     = wx.TE_READONLY,
#             value     = "",
#             size      = config.sTc,
#             validator = dtsValidator.IsNotEmpty(),
#         )

#         self.wStResults = wx.StaticText(
#             parent = cParent,
#             label  = config.lStResultCtrl,
#             style  = wx.ALIGN_RIGHT
#         )

#         self.wBtnResultsW = wx.Button(
#             parent = cParent,
#             label  = config.lBtnTypeResCtrl,
#         )
#         #endregion --------------------------------------------------> Widgets

#         #region ------------------------------------------------------> Sizers
#         #------------------------------> 
#         self.sRes = wx.GridBagSizer(1,1)
#         #------------------------------> 
#         self.sRes.Add(
#             self.wStResults,
#             pos    = (0,0),
#             flag   = wx.ALIGN_LEFT|wx.ALL,
#             border = 5,
#             span   = (0,2),
#         )
#         self.sRes.Add(
#             self.wBtnResultsW,
#             pos    = (1,0),
#             flag   = wx.ALIGN_CENTER_VERTICAL|wx.ALL,
#             border = 5
#         )
#         self.sRes.Add(
#             self.wTcResults,
#             pos    = (1,1),
#             flag   = wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL,
#             border = 5,
#         )
#         #------------------------------> 
#         self.sRes.AddGrowableCol(1,1)
#         #endregion ---------------------------------------------------> Sizers
        
#         #region -----------------------------------------------------> Tooltip
#         self.wBtnResultsW.SetToolTip(config.ttBtnTypeRes)
#         self.wStResults.SetToolTip(config.ttStResult)
#         #endregion --------------------------------------------------> Tooltip
        
#         #region --------------------------------------------------------> Bind
#         self.wBtnResultsW.Bind(wx.EVT_BUTTON, self.OnResW)
#         #endregion -----------------------------------------------------> Bind
#     #---
#     #endregion -----------------------------------------------> Instance setup

#     #region ---------------------------------------------------> Class methods
#     #------------------------------> Event Methods
#     def OnResW(self, event: wx.CommandEvent) -> bool:
#         """ Open the window to write the results columns. 
        
#             Parameters
#             ----------
#             event: wx.Event
#                 Information about the event
            
#             Returns
#             -------
#             bool
#         """
#         #------------------------------> 
#         with window.ResControlExp(self) as dlg:
#             dlg.ShowModal()
#         #------------------------------> 
#         return True
#     #---
#     #endregion ------------------------------------------------> Class methods
# #---


