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
import wx

import config.config as config
import data.file as file
#endregion ----------------------------------------------------------> Imports


def LoadUMSAPFile(fileP, dlg):
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
	confOpt = {
		'N' : 1
	}
	#endregion ----------------------------------------------------> Variables
	
	#region -------------------------------------------------------> Read file
	wx.CallAfter(dlg.UpdateStG, f"Reading file: {fileP.name}")
	try:
		config.obj = file.UMSAPFile(fileP)
	except Exception as e:
		wx.CallAfter(dlg.ErrorMessage,
			label = config.label['PdError'],
			error        = str(e),
			tException = e,
		)
	#endregion ----------------------------------------------------> Read file

	#region --------------------------------------------------> Configure file
	dlg.g.SetRange((2*config.obj.GetSectionCount())+confOpt['N'])
	config.obj.Configure(dlg)
	#endregion -----------------------------------------------> Configure file
	
	return True
#---

def GetDisplayInfo(win):
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
				'D' : {'xo':X, 'yo':Y, 'w':W, 'h':h},
				'W' : {'N': N, 'w':W, 'h', H}
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