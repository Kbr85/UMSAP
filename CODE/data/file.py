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

import wx

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
		confOpt : dict
			Configuration options
		data : dict
			Data read from json formatted file
		confData : dict
			Configured data. See Notes

		Raises
		------
		ExecutionError
			- When a requested section is not found in the file (GetSectionData)

		Methods
		-------

		Notes
		-----
		The general structure of confData is
		{
			'Correlation Analysis' : {
				'PlotData' : { # Only valid date sections
					'Date' : { 
						'DF' : pd.DataFrame with Result values,
						'Col' : list of columns,
					},
				},
				'MenuItem : { # All date sections
					'Date' : Boolean, DateSection is corrupted or not
				},
			},
		}
		
	"""
	#region -----------------------------------------------------> Class setup
	name = 'UMSAPFile'
	#endregion --------------------------------------------------> Class setup

	#region --------------------------------------------------> Instance setup
	def __init__(self, fileP):
		""" """
		#region ---------------------------------------------------> Variables
		self.fileP = fileP

		self.confOpt = {
			#------------------------------> Names of the sections
			'CorrA' : config.nameUtilities['CorrA'],
			#------------------------------> Configure section methods
			'Configure' : { 
				config.nameUtilities['CorrA'] : self.ConfigureCorrA,
			}
		}
		#------------------------------> See Notes about the structure of dict
		self.confData = {}
		#endregion ------------------------------------------------> Variables

		#region -------------------------------------------------> Check Input
		self.data = dtsFF.ReadJSON(fileP)
		#endregion ----------------------------------------------> Check Input
	#---
	#endregion -----------------------------------------------> Instance setup

	#region ---------------------------------------------------> Class methods
	def Configure(self, dlg=None):
		"""Prepare data for each section in the file and for the CustomTreeCtrl
			in the control window. See Notes.
	
			Parameters
			----------
			dlg : wx.Dialog or None
				To show configuration progress.
	
			Notes
			-----
			If dlg is provided, then it is assumed the configuration is done 
			from another thread and calls to dlg methods should be made with
			wx.CallAfter()
		"""
		#region ------------------------------------------> Configure sections
		for k in self.data.keys():
			#------------------------------> Update dlg
			if dlg is not None:
				wx.CallAfter(dlg.UpdateStG, f"Configuring section: {k}")
			else:
				pass
			#------------------------------> Configure
			self.confOpt['Configure'][k]()
		#endregion ---------------------------------------> Configure sections
		
		#region ----------------------------------------------> Configure tree
		wx.CallAfter(dlg.UpdateStG, f"Configuring tree data")
		
		#endregion -------------------------------------------> Configure tree
		
		#region -------------------------------------------------> Destroy dlg
		if dlg is not None:
			wx.CallAfter(dlg.EndModal, 1)
			wx.CallAfter(dlg.Destroy)
		else:
			pass		
		#endregion ----------------------------------------------> Destroy dlg
	
		return True
	#---

	def ConfigureCorrA(self):
		"""Configure a Correlation Analysis section	"""
		#region -------------------------------------------------> Plot & Menu
		#------------------------------> Empty start
		plotData = {}
		menuItem = {}
		#------------------------------> Fill
		for k,v in self.data[self.confOpt['CorrA']].items():
			try:
				#------------------------------> Create data
				df  = pd.DataFrame(v['R'], dtype='float64')
				col = v['CI']['Column']
				#------------------------------> Add to dict if no error
				plotData[k] = {
					'DF' : df,
					'Col' : col,
				}
				menuItem[k] = True
			except Exception:
				menuItem[k] = False
		#endregion ----------------------------------------------> Plot & Menu
		
		#region -------------------------------------------> Add/Reset section 
		self.confData[self.confOpt['CorrA']] = {
			'PlotData' : plotData,
			'MenuItem' : menuItem,
		}
		#endregion ----------------------------------------> Add/Reset section 
		
		return True
	#---


	def GetSectionCount(self):
		"""Get the total number of sections in file

			Returns
			-------
			int:
				Number of sections in the file	
		"""
		return len(self.data.keys())
	#---

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


