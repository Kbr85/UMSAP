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

import wx

import dat4s_core.gui.wx.menu as dtsMenu

import config.config as config
import data.file as file
import gui.dtscore as dtscore
import gui.window as window
#endregion ----------------------------------------------------------> Imports


def LoadUMSAPFile(fileP=None, win=None, shownSection=None):
	"""Load an UMSAP File either from Read UMSAP File menu, LoadResults
		method in Tab or Update File Content menu

		Parameters
		----------
		fileP : Path or None
			If None, it is assumed the method is called from Read UMSAP File
			menu. Default is None.
		win : wx.Window or None
			If called from menu it is used to center the Select file dialog.
			Default is None.
		shownSection : list of str
			List with the name of all checked sections in File Control window

	"""
	#region -------------------------------------------------------> Variables
	confMsg = {
		'Selector': config.msg['FileSelector'],
	}
	#endregion ----------------------------------------------------> Variables
	
	#region --------------------------------------------> Get file from Dialog
	if fileP is None:
		try:
			#------------------------------> Get File
			fileP = dtsMenu.GetFilePath('openO', config.extLong['UMSAP'])
			#------------------------------> Set Path
			if fileP is None:
				#------------------------------> No file selected
				return False
			else:
				#------------------------------> Set Path
				fileP = Path(fileP[0])
		except Exception as e:
			dtscore.Notification(
				'errorF', 
				msg        = confMsg['Selector'],
				tException = e,
				parent     = win,
			)
			return False
	else:
		pass
	#endregion -----------------------------------------> Get file from Dialog
	
	#region ----------------------------> Raise window if file is already open
	if shownSection is None:
		#------------------------------> Check file is opened & Raise it
		if config.umsapW.get(fileP, '') != '':
			config.umsapW[fileP].Raise()
			return True
		else:
			pass		
	else:
		#------------------------------> Check file is opened & Close window
		if config.umsapW.get(fileP, '') != '':
			config.umsapW[fileP].Close()
		else:
			pass
	#endregion -------------------------> Raise window if file is already open

	#region ---------------------------------------------> Progress Dialog
	dlg = dtscore.ProgressDialog(None, f"Analysing file {fileP.name}", 100)
	#endregion ------------------------------------------> Progress Dialog

	#region -----------------------------------------------> Configure obj
	#------------------------------> UMSAPFile obj is placed in config.obj
	_thread.start_new_thread(_LoadUMSAPFile, (fileP, dlg))
	#endregion --------------------------------------------> Configure obj

	#region --------------------------------------------------> Show modal
	if dlg.ShowModal() == 1:
		config.umsapW[fileP] = window.UMSAPControl(
			config.obj, 
			shownSection = shownSection,
		)
	else:
		pass

	dlg.Destroy()
	#endregion -----------------------------------------------> Show modal

	return True
#---

def _LoadUMSAPFile(fileP, dlg):
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