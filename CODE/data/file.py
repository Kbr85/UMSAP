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


"""Classes and methods to handle file/folder input/output operations"""


#region -------------------------------------------------------------> Imports
import json
import pandas as pd
# from pathlib import Path

import dat4s_core.data.file as dtsFF
import dat4s_core.data.method as dtsMethod
import dat4s_core.exception.exception as dtsException

import config.config as config
#endregion ----------------------------------------------------------> Imports


class UMSAPFile():
	"""Read and analyse an umsap file

		Parameters
		----------
		fileP : Path
			Path to the UMSAP file

		Attributes
		----------
		name : str
			Unique name of the class
		fileP : Path
			Path to the UMSAP file
		data : dict
			Data read from json formatted file

		Raises
		------
		ExecutionError
			- When a requested section is not found in the file (GetSectionData)

		Methods
		-------
		
	"""
	#region -----------------------------------------------------> Class setup
	name = 'UMSAPFile'
	#endregion --------------------------------------------------> Class setup

	#region --------------------------------------------------> Instance setup
	def __init__(self, fileP):
		""" """
		#region ---------------------------------------------------> Variables
		self.fileP = fileP
		#endregion ------------------------------------------------> Variables

		#region -------------------------------------------------> Check Input
		self.data = dtsFF.ReadJSON(fileP)
		#endregion ----------------------------------------------> Check Input

		#region -----------------------------------------------> Initial Setup
		
		#endregion --------------------------------------------> Initial Setup
	#---
	#endregion -----------------------------------------------> Instance setup

	#region ---------------------------------------------------> Class methods
	def GetSectionData(self, sectionName):
		"""Get the dict with the data for a section
	
			Parameters
			----------
			sectionName : str
				Section name like in config.Modules or config.Utilities
	
			Returns
			-------
			dict:
				Section data

			Raise
			-----
			ExecutionError
				- When the section is not found in the file
		"""
		#region ---------------------------------------------------> Variables
		confMsg = {
			'NoSection' : (
				f"Section {sectionName} was not found in the content of "
				f"file:\n{self.fileP}"),
		}
		#endregion ------------------------------------------------> Variables
		
		if (data := self.data.get(sectionName, '')) != '':
			return data
		else:
			raise dtsException.ExecutionError(confMsg['NoSection'])
	#---
	#endregion ------------------------------------------------> Class methods
#---


class CorrAFile():
	"""Read and analyse a correlation analysis file or a correlation analysis
		section of a file.

		Parameters
		----------
		data : dict
			Correlation-Analysis section from an UMSAP File.
		fileP : Path
			For error printing only

		Attributes
		----------
		name : str
			Unique name for the class
		data : dict
			Correlation-Analysis section from an UMSAP File.
		plotData : dict
			{'Date' : {'DF': df, 'Column' : list}, } One for each valid date
		menuEntry : 

		Raises
		------
		InputError:
			- When file content is missing critical keys

		Notes
		-----
		See UTIL/DETAILS/details.py -> Correlation Analysis file for a 
		description of the file/section content
		
	"""
	#region -----------------------------------------------------> Class setup
	name   = 'CorrAFile'
	#endregion --------------------------------------------------> Class setup

	#region --------------------------------------------------> Instance setup
	def __init__(self, data):
		""" """
		#region ---------------------------------------------------> Variables
		self.data = data
		self.confMSg = {
			'NoDateSection' : (
				f"The {config.nameUtilities['CorrA']} section of the UMSAP "
				f"file is corrupted."),
		}
		#endregion ------------------------------------------------> Variables
		
		#region -------------------------------------------------> Check Input
		
		#endregion ----------------------------------------------> Check Input

		#region -----------------------------------------------> Initial Setup
		if self.SetVariables():
			pass
		else:
			raise dtsException.InputError(self.confMSg['NoDateSection'])
		#endregion --------------------------------------------> Initial Setup
		#---
	#endregion -----------------------------------------------> Instance setup

	#region ---------------------------------------------------> Class methods
	def SetVariables(self):
		"""Set instance variables needed for file visualization"""
		#region -------------------------------------------------> Plot & Menu
		#------------------------------> Dicts
		self.plotData = {}
		self.menuEntry = {}
		#------------------------------> Fill
		for k,v in self.data.items():
			self.plotData[k] = {}
			try:
				self.plotData[k]['DF'] = pd.DataFrame(v['R'], dtype='float64')
				self.plotData[k]['Col'] = v['CI']['Column']
				self.menuEntry[k] = True
			except Exception:
				self.menuEntry[k] = False
		#endregion ----------------------------------------------> Plot & Menu
		
		#region ---------------------------> Check there is somenthing to plot
		if not any(self.menuEntry.values()):
			return False
		else:
			return True
		#endregion ------------------------> Check there is somenthing to plot
		
	#---
	#endregion ------------------------------------------------> Class methods
#---