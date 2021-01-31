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
from pathlib import Path

import dat4s_core.data.file as dtsFF
import dat4s_core.data.method as dtsMethod
import dat4s_core.exception.exception as dtsException

import config.config as config
#endregion ----------------------------------------------------------> Imports

#---------------------------------------------------------------- Base classes
class CommonMethods():
	"""Common methods to all file content classes """
	#region -----------------------------------------------------> Class setup
	gK = config.fileContentCheck['Parts']
	vK = ['Version']
	#endregion --------------------------------------------------> Class setup

	#region --------------------------------------------------> Instance setup
	#endregion -----------------------------------------------> Instance setup

	#region ---------------------------------------------------> Class methods
	def CheckFileContent(self):
		"""Check the content of the file has all necessary information.
			Child class holds the file/data content in self.data
		
			Notes
			-----
			Possible exceptions are raise to the user in the child class
			Child class must have the following attributes: topK, gK, vK, iK, 
			ciK
		"""
		#region -----------------------------------------------> Check top key
		dtStamps = self.data[self.topK]
		#endregion --------------------------------------------> Check top key
		
		#region -----------> Check date-time stamps, general & particular keys
		for k, v in dtStamps.items():
			#------------------------------> Check date-time stamp
			dtsMethod.StrNowCheck(k)
			#------------------------------> Check general keys
			for kg in self.gK:
				#------------------------------> Check dict exists
				s = v[kg]
				#------------------------------> Check it has the needed keys
				#--------------> V
				if kg == 'V':
					for kv in self.vK:
						s[kv]
				#--------------> I
				elif kg == 'I':
					for ki in self.iK:
						s[ki]
				#--------------> CI
				elif kg == 'CI':
					for kci in self.ciK:
						s[kci]
				#--------------> R
				elif kg == 'R':
					self.df = pd.DataFrame(s)
				else:
					pass
		#endregion --------> Check date-time stamps, general & particular keys
	#---	
	#endregion ------------------------------------------------> Class methods
#---

class CorrAFile(CommonMethods):
	"""Read and analyse a correlation analysis file or a correlation analysis
		section of a file.

		Parameters
		----------
		data : Path or dict
			If a path is given then it is the path to an UMSAP output file
			containing a Correlation-Analysis section.
			If a dict is given then it is the Correlation-Analysis section.
		fileP : Path
			For error printing only

		Attributes
		----------
		topK
		iK
		ciK
		name
		data
		df

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
	name = 'CorrAFile'
	topK = config.file['ID']['CorrA']
	iK = ciK = config.fileContentCheck[name]
	#endregion --------------------------------------------------> Class setup

	#region --------------------------------------------------> Instance setup
	def __init__(self, data, fileP=None):
		""" """
		#region -------------------------------------------------> Check Input
		#------------------------------> fileP, needed for error msg here
		self.fileP = fileP if fileP is not None else data
		#------------------------------> Input type
		if isinstance(data, dict):
			self.data = data
		elif isinstance(data, Path):
			self.data = dtsFF.ReadJSON(data)
		else:
			msg = (
				config.msg[self.name]['InputType'] 
				+ f"\nThe given input has type: {type(data)}"
			)
			raise dtsException.InputError(msg)
		#------------------------------> Keys in dict
		try:
			self.CheckFileContent()
		except Exception as e:
			msg = (
				config.msg['Error']['File']['Content']
				+ f"\nSelected file:\n{self.fileP}"
			)
			raise dtsException.InputError(msg)
		#endregion ----------------------------------------------> Check Input

		#region -----------------------------------------------> Initial Setup
		
		#endregion --------------------------------------------> Initial Setup
		#---
	#endregion -----------------------------------------------> Instance setup

	#region ---------------------------------------------------> Class methods

	#endregion ------------------------------------------------> Class methods
#---