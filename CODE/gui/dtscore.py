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
import wx

import dat4s_core.gui.wx.window as dtsWindow

import config.config as config
#endregion ----------------------------------------------------------> Imports


class Notification(dtsWindow.NotificationDialog):
	"""This avoids to type the title and the image of the window every time	"""
	def __init__(self, mode, msg=None, tException=None, parent=None, 
		img=config.file['ImgIcon'], button=1,):
		""" """
		super().__init__(mode, msg=msg, tException=tException, parent=parent,
			button=button, img=img, title='UMSAP - Notification')
	#---
#---

class ProgressDialog(dtsWindow.ProgressDialog):
	"""This avoids to type the icon every time """
	def __init__(self, parent, title, count, img=config.file['ImgIcon'],
		style=wx.CAPTION|wx.CLOSE_BOX|wx.RESIZE_BORDER):	
		""""""
		super().__init__(parent, title, count, img=img, style=style)
	#---
#---