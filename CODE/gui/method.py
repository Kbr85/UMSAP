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
import config.config as config
import gui.window as window
import gui.dtscore as dtscore
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
	#region -----------------------------------------------------> File's name
	name  = fileP.name
	#endregion --------------------------------------------------> File's name
	
	#region -------------------------------------------------------> Load file
	if config.umsapW.get(name, '') == '':
		try:
			config.umsapW[name] = window.UMSAPFile(fileP)
		except Exception as e:
			dtscore.Notification(
				mode       = 'errorF',
				msg        = str(e),
				tException = e,
				parent     = parent
			)
			return False
	else:
		config.umsapW[name].Raise()
	#endregion ----------------------------------------------------> Load file
	
	return True
#---