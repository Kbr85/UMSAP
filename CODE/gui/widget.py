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


""" Widgets of the application"""


#region -------------------------------------------------------------> Imports
import wx

import dat4s_core.gui.wx.validator as dtsValidator
#endregion ----------------------------------------------------------> Imports


class ResControl():
	"""Creates the Results - Control experiment widgets. Configuration options
		are set in the parent class in self.confOpt

		Parameters
		----------
		parent : wx widget
			Parent of the widgets

		Attributes
		----------
		

		Raises
		------
		

		Methods
		-------
		
	"""


	#region -----------------------------------------------------> Class setup
	
	#endregion --------------------------------------------------> Class setup

	#region --------------------------------------------------> Instance setup
	def __init__(self, parent):
		""" """
		#region -----------------------------------------------------> Widgets
		self.tcResults = wx.TextCtrl(
			parent    = parent,
			style     = wx.TE_READONLY,
			value     = "",
			size      = self.confOpt['TwoInRow'],
			validator = dtsValidator.IsNotEmpty(),
		)

		self.stResults = wx.StaticText(
			parent = parent,
			label  = self.confOpt['ResultL'],
			style  = wx.ALIGN_RIGHT
		)

		self.btnResultsW = wx.Button(
			parent = parent,
			label  = self.confOpt['TypeResL'],
		)
		self.btnResultsL = wx.Button(
			parent = parent,
			label  = self.confOpt['LoadResL'],
		)
		#endregion --------------------------------------------------> Widgets

		#region ------------------------------------------------------> Sizers
		#------------------------------> 
		self.sizerRes = wx.GridBagSizer(1,1)
		#------------------------------> 
		self.sizerRes.Add(
			self.stResults,
			pos    = (0,0),
			flag   = wx.ALIGN_LEFT|wx.ALL,
			border = 5,
			span   = (0,2),
		)
		self.sizerRes.Add(
			self.btnResultsW,
			pos    = (1,0),
			flag   = wx.ALIGN_CENTER_VERTICAL|wx.ALL,
			border = 5
		)
		self.sizerRes.Add(
			self.tcResults,
			pos    = (1,1),
			flag   = wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL,
			border = 5,
		)
		self.sizerRes.Add(
			self.btnResultsL,
			pos    = (1,2),
			flag   = wx.ALL|wx.ALIGN_CENTER_VERTICAL,
			border = 5,
		)
		#------------------------------> 
		self.sizerRes.AddGrowableCol(1,1)
		#endregion ---------------------------------------------------> Sizers

		#region --------------------------------------------------------> Bind
		
		#endregion -----------------------------------------------------> Bind
	#---
	#endregion -----------------------------------------------> Instance setup

	#region ---------------------------------------------------> Class methods
	
	#endregion ------------------------------------------------> Class methods
#---


