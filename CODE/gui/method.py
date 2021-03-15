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

import config.config as config
import gui.window as window
import gui.dtscore as dtscore
import data.file as file
#endregion ----------------------------------------------------------> Imports


def LoadUMSAPFile(fileP, parent=None):
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
		'ExtraConfStep' : 1,
	}
	name  = fileP.name
	#endregion ----------------------------------------------------> Variables
	
	#region ----------------------------> Raise window if file is already open
	if config.umsapW.get(name, '') != '':
		config.umsapW[name].Raise()
		return True
	else:
		pass		
	#endregion -------------------------> Raise window if file is already open

	#region -------------------------------------------------------> Read file
	try:
		obj = file.UMSAPFile(fileP)
	except Exception as e:
		dtscore.Notification(
			mode       = 'errorF',
			msg        = str(e),
			tException = e,
			parent     = parent
		)
		return False
	#endregion ----------------------------------------------------> Read file
	
	#region -------------------------------------------------> Progress Dialog
	dlg = dtscore.ProgressDialog(
		None, 
		obj.fileP.name, 
		obj.GetSectionCount()+confOpt['ExtraConfStep'],
	)
	#endregion ----------------------------------------------> Progress Dialog
	
	#region ---------------------------------------------------> Configure obj
	_thread.start_new_thread(obj.Configure, (dlg,))
	#endregion ------------------------------------------------> Configure obj
	
	#region ------------------------------------------------------> Show modal
	#------------------------------> This will be destroy by obj.Configure()
	dlg.ShowModal()
	#endregion ---------------------------------------------------> Show modal
	
	#region -----------------------------------------------------> Show window
	config.umsapW[name] = window.UMSAPControl(obj)
	#endregion --------------------------------------------------> Show window

	return True
#---