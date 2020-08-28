# ------------------------------------------------------------------------------
#	Copyright (C) 2017 Kenny Bravo Rodriguez <www.umsap.nl>
	
#	This program is distributed for free in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
	
#	See the accompaning licence for more details.
# ------------------------------------------------------------------------------


""" This module contains the main configuration parameters of the app """


#region -------------------------------------------------------------- Imports
import json
import os
import platform
from pathlib import Path

import wx
#endregion ----------------------------------------------------------- Imports


# ------------------------------------------------------------------------------
# NON-CONFIGURABLE PARAMETERS
# ------------------------------------------------------------------------------


#region --------------------------------------------------- General parameters
development = True # To control variables with different values in dev or prod

version         = '2.1.0 (beta)' # String to write in the output files
versionUpdate   = [2, 0, 1]      # List to match against the version online
versionInternet = None           # To hold the version found in the Internet
dictVersion     = { # dict for directly write into output files
	'version': version,
}

cOS = platform.system() # Current operating system
cwd = Path(os.path.abspath(os.path.dirname(__file__))) # Current working directory
#endregion ------------------------------------------------ General parameters

#region ---------------------------------------- PLATFORM DEPENDENT PARAMETERS
if cOS == 'Darwin':
	#--> Fix cwd and set the location of the Resources folder
	cwd = cwd.parent
	cwd = cwd.parent
	if development:
		res = cwd / 'BORRAR-UMSAP/RESOURCES'
	else:
		res = cwd / 'Resources'	
	
	#--> Set top left coordinate
	topLeftCoord = (0, 21)
	#--> Height of the panels I and T corrected by windows addition, like separators blabla
	tarprotPanelBelow = 640
	#--> x, y coordinates for the first window at the top so they are top align
	topXY = (0, 41)
	#--- Height to add to the y coordinate due to the taskbar
	TaskBarHeight = 0

	##### Correct minimum size difference in TarprotRes due to different windows top bar and menu
	#self.tarprotMSH = 21
	##### Correct virtual size of scroll window in TarprotRes. To make the scrolled region more tight
	#self.tarprotSWVH = 0

elif cOS == 'Windows':
	#--> Fix cwd and set the location of the Resources folder
	cwd = cwd.parent
	res = cwd / 'RESOURCES'
	#--> Set top left coordinate
	topLeftCoord = (0, 0)
	#--> Height of the panels I and T corrected by windows addition, like separators blabla
	tarprotPanelBelow    = 680
	#--> x, y coordinates for the first window at the top so they are top align
	topXY = (0, 41)
	#--> Height to add to the y coordinate due to the taskbar
	TaskBarHeight = -50

	##### Correct minimum size difference in TarprotRes due to different windows top bar and menu
	#self.tarprotMSH = 57
	##### Correct virtual size of scroll window in TarprotRes. To make the scrolled region more tight
	#self.tarprotSWVH = 25

elif cOS == 'Linux':
	#--> Fix cwd and set the location of the Resources folder
	res = cwd / 'RESOURCES'	
	#--> Set top left coordinate
	topLeftCoord = (20, 20)
	#---> Height of the panels I and T corrected by windows addition, like separators blabla
	tarprotPanelBelow    = 680
	#--- x, y coordinates for the first window at the top so they are top align
	topXY = (0, 41)
	#--- Height to add to the y coordinate due to the taskbar
	TaskBarHeight = -50

	##### Correct minimum size difference in TarprotRes due to different windows top bar and menu
	#self.tarprotMSH = 57
	##### Correct virtual size of scroll window in TarprotRes. To make the scrolled region more tight
	#self.tarprotSWVH = 25	
	
else:
	pass
#endregion ------------------------------------- PLATFORM DEPENDENT PARAMETERS

#region ----------------------------------------------------- Names and titles
name = { # Unique names to identify windows/objects through the config file
	#--> Main like windows
	'Main'        : 'Main',
	'About'       : 'About',
	'Preference'  : 'Preference',
	'UpdateNotice': 'UpdateNotice',
	#--> Utilities
	'Util'    : 'Util',
	'CorrA'   : 'Correlation Analysis',
	'CorrARes': 'Correlation Analysis Results',
	'MergeAA' : 'MergeAA',
	'TypeRes' : 'TypeRes',
	#--> Targeted Proteolysis module
	'TarProt'   : 'TarProt',
	'TarProtRes': 'TarProtRes',
	'CutPropRes': 'Cleavage propensity',
	'AAdist'    : 'AA Distribution',
	'AAdistR'   : 'AA Distribution Results',
	'Histo'     : 'Histograms',
	'HistoRes'  : 'Histograms Results',
	'SeqAlign'  : 'Sequence Alignment',
	'ShortDFile': 'ShortDFile',
	'Cuts2PDB'  : 'Cuts2PDB',
	#--> Proteome Profiling module
	'ProtProf'   : 'ProtProf',
	'ProtProfRes': 'ProtProfRes',
	#--> Limited Proteolysis module
	'LimProt'   : 'LimProt',
	'LimProtRes': 'LimProtRes',
	'SeqH'      : 'SeqH',
	#--> Data File Objects
	'DataObj'    : 'DataObj',
	'SeqObj'     : 'SeqObj',
	'PdbObj'     : 'PdbObj',
	'CorrObj'    : 'CorrObj',
	'CutPropObj' : 'CutPropObj',
	'HistoObj'   : 'HistoObj',
	'TarProtObj' : 'TarProtObj',
	'AAdistObj'  : 'AAdistObj',
	'ScriptObj'  : 'ScriptObj',
	'ProtProfObj': 'ProtProffObj',
	'LimProtObj' : 'LimProtObj',
	#--> Windows shown as Modal windows
	'CorrAExp'  : 'Correlation Analysis Export',
}

title = { # Title of the windows
	#--> Main like windows
	name['Main'] : ("Utilities for Mass Spectrometry Analysis of Proteins"
					" " + version),
	name['About']       : 'About UMSAP',
	name['Preference']  : 'Preferences',
	name['UpdateNotice']: 'UMSAP Updates',
	#--> Utilities
	name['Util']    : 'UMSAP - Utilities',
	name['CorrA']   : 'UMSAP - Util - Correlation Analysis',
	name['CorrARes']: 'UMSAP - Util - Correlation Analysis',
	name['MergeAA'] : 'UMSAP - Util - Merge aadist Files',
	name['TypeRes'] : 'UMSAP - Column Numbers for the Field Results - Control Experiment',
	#--> Targeted Proteolysis module
	name['TarProt']   : 'UMSAP - Targeted Proteolysis',
	name['TarProtRes']: 'UMSAP - TarProt - Fragments',
	name['CutPropRes']: 'UMSAP - Util - Cleavages per Residue',
	name['AAdist']    : 'UMSAP - Util - AA Distribution',
	name['AAdistR']   : 'UMSAP - Util - AA Distribution',
	name['Histo']     : 'UMSAP - Util - Histograms',
	name['HistoRes']  : 'UMSAP - Util - Histograms',
	name['SeqAlign']  : 'UMSAP - Util - Sequence Alignment',
	name['ShortDFile']: 'UMSAP - Util - Short Data Files',
	name['Cuts2PDB']  : 'UMSAP - Util - Cleavages to PDB Files',
	#--> Limited Proteolysis module
	name['LimProt']   : 'UMSAP - Limited Proteolysis',
	name['LimProtRes']: 'UMSAP - LimProt - Gel Analysis',
	name['SeqH']      : 'UMSAP - Util - Sequence Highlight',
	#--> Proteome Profiling module
	name['ProtProf']   : 'UMSAP - Proteome Profiling',
	name['ProtProfRes']: 'UMSAP - ProtProf - Results',
	#--> Windows shown as modal
	name['CorrAExp']  : 'Export column numbers',
}
#endregion -------------------------------------------------- Names and titles

#region ------------------------------------------------------ Windows options
win = { # To track the existence and number of certain windows. 
		# None values change to a reference to the open window.
	'Open'  : [], # List of all open windows in the program
	#--> Main like windows
	name['Main']        : None,
	name['About']       : None,
	name['Preference']  : None,
	name['UpdateNotice']: None,
	#--> Utilities 
	name['Util']      : None,
	name['CorrA']     : None,
	     'CorrAResNum': 0,
	name['MergeAA']   : None,
	name['TypeRes']   : {}, # keys will be the name of the module and values references to the associated TypeResults window
	#--> Targeted Proteolysis module
	name['TarProt']     : None,
	     'TarProtResNum': 0,
	name['Histo']       : None,
	     'HistoResNum'  : 0,
	name['AAdist']      : None,
	     'AAdistResNum' : 0,		 
	name['SeqAlign']    : None,
	name['ShortDFile']  : None,
	name['Cuts2PDB']    : None,
	     'CutpropResNum': 0,	
	#--> Limited Proteolysis module
	name['LimProt']     : None,
	     'LimProtResNum': 0,
	name['SeqH']        : None,
	#--> Proteome Profiling module
	name['ProtProf']     : None,
	     'ProtProfResNum': 0,
	'DeltaNewWin'   : 15,
}
#endregion --------------------------------------------------- Windows options

#region ------------------------------------------------ Modules and Utilities
mod = { # Modules in the program including the Utilities window
	name['TarProt'] : 'Targeted Proteolysis',
	name['LimProt'] : 'Limited Proteolysis',
	name['ProtProf']: 'Proteome Profiling',
	name['Util']    : 'Utilities',
	'Targeted Proteolysis': name['TarProt'],
	'Limited Proteolysis' : name['LimProt'],
	'Proteome Profiling'  : name['ProtProf'],
	'Utilities'           : name['Util'],
}
#endregion --------------------------------------------- Modules and Utilities

#region ---------------------------------------------------------------- Paths
path = { # Path to folders containing UMSAP files independently of the OS
	'CWD'      : cwd,            # Root of the folders containing UMSAP files
	'Resources': res,            # Resources folder
	'Images'   : res / 'IMAGES', # Images folder
	'Config'   : res / 'CONFIG', # Configuration folder
}
#endregion ------------------------------------------------------------- Paths

#region ---------------------------------------------------------------- Files
file = { # Path to critical files
	'Config'   : path['Config'] / 'config.json',     # User config file
	'ConfigDef': path['Config'] / 'config_def.json', # Default config file
	'Manual'   : path['Resources'] / 'MANUAL/manual.pdf', # UMSAP Manual
}
#endregion ------------------------------------------------------------- Files

#region----------------------------------------------------------------- Sizes
size = { # Size for different widgets in the GUI
	'Screen'       : None,          # Size of the user screen
	'TaskBarHeight': TaskBarHeight, # Height of the task bar for the current OS
	'GraphPanel'   : { # Size of the matplotlib panel in windows like tarprotRes
		name['TarProtRes'] : (560, 560),
		name['LimProtRes'] : (560, 560),
		name['ProtProfRes']: (560, 560),
	},
	'Panel' : { # Size for wx.Panels
		name['LimProtRes'] : {
			'PanelGel': (560, 560)
		},
	},
	'TextCtrl' : { # Size for wx.TextCtrl
		'DataFile'         : (495, 22), # Data file in a File section
		'OutputFF'         : (495, 22), # Output file/folder in a File section
		'ValuesSect'       : (180, 22), # For the Values section of module
		'ColumnsSect'      : (470, 22), # For the Columns section of module
		'ExpColNumCorrARes': (600, 22), # Export columns for correlation utility
		'MergeOut'         : (515, 22), # Output file for the merge utility		
		name['TarProt'] : {
			'tcResults': (380, 22),
		},
		name['LimProt'] : {
			'tcResults': (380, 22),
		},
		name['ProtProf'] : {
			'tcResults': (380, 22),			
		},
		name['ProtProfRes']: {
			'TextPanel' : (560, 280),
		},
		name['TarProtRes'] : {
			'TextPanel': (560, 560),
		},
		name['LimProtRes'] : {
			'TextPanel': (560, 560),
		},
		name['TypeRes'] : {
			'Rows' : (70, 22),
			'Flex' : (100, 22),
			'Names': (200, 22),
		},				
	},
	'ListBox' : { # Size for wx.ListCtrl
		name['TarProtRes' ]: (250, 200),
		name['TarProt']    : (250, 200),
		name['LimProt']    : (250, 200),
		name['LimProtRes' ]: (250, 200),
		name['ProtProfRes']: (275, 200),
		name['ProtProf']   : (250, 200),
		name['TypeRes']    : (250, 200),
		name['MergeAA']    : (600, 200),
	},
	'SearchCtrl' : { # Size for wx.SearchCtrl
		name['TarProtRes'] : (250,-1),
		name['LimProtRes'] : (250,-1),
		name['ProtProfRes']: (250,-1),
	},
	'Drawings' : { # General size settings to make all drawings the same
		'RectH'     : 20, # Height of a rectangle representing a fragment
		'RectBetw'  : 15, # Vertical space between fragments
		'RectT'     : 35, # RectH + RectBetw
		'PanelBelow': { # Corrected size of the panel in the second row of results windows for:
			'TarProt' : tarprotPanelBelow,
			'LimProt' : tarprotPanelBelow,
		},
	},
	'ScrolledW' : { # Size for ScrolledWindows
		name['TypeRes'] : (500, 500),
	},
}
#endregion ------------------------------------------------------------- Sizes

#region ---------------------------------------- Information about UMSAP Files
protprof = { # Information about the protprof file
	'SColNorm': 3, # Columns to be normalized in protprof.dataV starts in this index
	'SColNumRow': 3,   # Index where experiments starts
	'ColNames': [ # Col names in the data frame excluding experiments
		'Gene',
		'Protein',
		'Score',
	],
	'ColDS' : [ # Col names for descriptive statistic in each tp/c
		'ave',
		'sd',
	],
	'ColOut' : [ # Col names to add for each experiment in the protprof data frame
		'P',
		'pP',
		'Pc',
		'pPc', 
		'FC',
		'log2FC', 
		'zFC',
	],
	'ColTPp' : [ # Col names for the Time analysis setion of the df in protprof
		'P',
		'Pc',
	],
	'SortBy' : ( # The data frame wll be sorted using this columns
		'Gene', 
		'Gene', 
		'Gene',
		'Gene',
	),
	'StringKeys' : [ # Fields that need to be converted to string before saving as json
		"Datafile", 
		"Outputfolder"
	],
	'Join'      : ',', # To make the tuples for a multiindex data frame
	'ExtraX_V'  : 40,  # Extra x for the positioning of the protprofRes window
}

limprot = { # Information about the limprot file
	'SColNorm' : 3, # Columns to be normalized in limprot.dataV start in this index.
	'ColNames': [ # Name of the columns in the limprot data frame. Experiments columns are not included. 
		'Nterm', 
		'Cterm', 
		'Fixed Nterm', 
		'Fixed Cterm',
		'Control Exp', 
		'Sequence', 
		'Score'
	],
	'SortBy' : [ # Data frame in the limprot file will be sort using these columns
		('Nterm', 'Nterm', 'Nterm'), 
		('Cterm', 'Cterm', 'Cterm')
	],	
	'ColOut' : [ # This are the columns that will be added in the limprot data frame for each experiment
		'ttest', 
		'delta', 
		'tost', 
		'I'
	],
	'StringKeys' : [ # Fields that need to be converted to string before saving as json
		"Datafile", 
		"Seq_rec", 
		"Seq_nat", 
		"Outputfolder"
	],
	'ColNamFrags' : [ # Columns name in the limprot data frame needed to create the fragment data frame 
		'Nterm', 
		'Cterm', 
		'Fixed Nterm', 
		'Fixed Cterm',
		'Sequence'
	],
	'ColNamFragsOut' : [ # Columns name in the fragments data frame
		'TCuts', 
		'TCutsNat', 
		'Nterm',
		'Fixed Nterm', 
		'Cterm', 
		'Fixed Cterm', 
		'SeqN', 
		'SeqNNat', 
		'Cuts', 
		'CutsNat', 
		'SeqSpace', 
		'Sequence', 
		'Bit'
	], 
	'SeqColInd' : -2, # Index of the Sequence column in the limprot data frame	
	#--> Coord and sizes for Gel Draw
	'LabelW'       : 50,   # width of the label area for the protein residue number in the fragment region
	'LabelpLocY'   : 40,   # y value for the residue numbers of the native sequence in the fragment region
	'LabelFirstExp': 55,   # y value for the first experiment/lane/band label in the fragment region
	'LBLineW'      : 3,    # line width to highlight listbox selection in frgment and gel regions
	'TextRectH'    : 4,    # space to adjust the height of the rectangle for the text selection inside a fragment
	'TextRectWLat' : 1,    # space to adjust the width of the rectangle for the text selection inside a fragment
	'LBTopGap'     : 3,    # space to adjust the rectangle for the list selection inside a fragment/band
	'ImageH'       : 20,   # Extra space to save the image of the fragments/gels
	'RectSx'       : 100,  # Start drawing in x = RectSx
	'RectSxg'      : 50,   # Space around the Gel bands
	'RectEx'       : 30,   # End drawings with 30 pixel space to the right
	'RectHRatio'   : 0.5,  # For the ratio of Height/Space Below
	'RectWRatio'   : 0.66, # For the ration of width/Space to --->
	'RectH'        : size['Drawings']['RectH'], # See size['Drawnings]
	'RectT'        : size['Drawings']['RectT'],	# See size['Drawnings]
	'PanelBelow'   : size['Drawings']['PanelBelow']['LimProt'], # dimensions of the gel/text panels in limprotRes
}

tarprot = { # Information about the tarprot file
	'SColNorm' : 3, # Columns to be normalized in tarprot.dataV start in this index.
	'ColNames': [ # Name of the columns in the tarprot data frame. Experiments columns are not included. 
		'Nterm', 
		'Cterm', 
		'Fixed Nterm', 
		'Fixed Cterm',
		'Control Exp', 
		'Sequence', 
		'Score'
	],
	'InsertPoint' : 5, # List index in config.tarprot[ColNames] to insert Exp# label
	'SortBy' : [ # Columns that will be used to sort the tarprot data frame.
		'Nterm', 
		'Cterm'
	],
	'StringKeys' : [ # This fields need to be converted into a string before saving to the json.
		"Datafile", 
		"Seq_rec", 
		"Seq_nat", 
		"PDBfile",
		"Outputfolder", 
		"PDBID"
	],		
	'ColNamFrags' : [ # Col names needed to build the fragments data frame
		'Nterm', 
		'Cterm', 
		'Fixed Nterm', 
		'Fixed Cterm',
		'Sequence'
	],
	'ColNamFragsOut' : [ # Col names in the fragment data frame
		'TCuts', 
		'TCutsNat', 
		'Nterm',
		'Fixed Nterm', 
		'Cterm', 
		'Fixed Cterm', 
		'SeqN', 
		'SeqNNat', 
		'Cuts', 
		'CutsNat', 
		'SeqSpace', 
		'Sequence', 
		'Bit'
	],
	'NumColsHeader': 7,          # Number of columns in the data frame without the experiments. = len('ColNames')
	'SeqColInd'    : -2,         # Index of the Sequence column in the tarprot data frame
	'SeqColName'   : 'Sequence', # Name of the Sequence column in the tarprot data frame
	#--> Coord and sizes for tarprotR
	'RectSx'       : 100, # Starting x for the fragments in tarprotRes
	'RectEx'       : 30,  # Ending x (width - RectEx) for the fragments in the tarprotRes
	'LabelW'       : 50,  # width of the label box
	'LabelpLocY'   : 40,  # 2 * RectH
	'LabelFirstExp': 55,  # 2 * RectH + RectB
	'TextRectW'    : 3,   # width of the Rect for the text selection
	'TextRectH'    : 4,   # height of the Rect for the text selection
	'TextRectWLat' : 1,   # space around the Rect for the text selection
	'LBTopGap'     : 3,   # space around the Rect for list box selection
	'LBLineW'      : 3,   # line width for hte Rect for list box selection
	'ImageH'       : 20,  # Extra space needed to save the image of the fragments
	'RectH'        : size['Drawings']['RectH'], # See size['Drawings']
	'RectB'        : size['Drawings']['RectBetw'], # See size['Drawings']
	'RectT'        : size['Drawings']['RectT'], # See size['Drawings']
	'PanelBelow'   : size['Drawings']['PanelBelow']['TarProt'], # dimensions of the intensity/text panels in tarprotRes
}

lpprot = { # Dict for ElementFragPanel and to allow having different setting for tarprotR and limprotR
	name['LimProtRes'] : { # See limprot dict for the menaning of the terms
		'RectH'         : limprot['RectH'], 
		'RectT'         : limprot['RectT'],
		'RectSx'        : limprot['RectSx'],
		'RectEx'        : limprot['RectEx'],
		'PanelBelow'    : limprot['PanelBelow'],
		'LabelW'        : limprot['LabelW'],
		'LabelpLocY'    : limprot['LabelpLocY'],
		'LabelFirstExp' : limprot['LabelFirstExp'],
		'LBTopGap'      : limprot['LBTopGap'], 
		'LBLineW'       : limprot['LBLineW'],    
		'TextRectH'     : limprot['TextRectH'], 
		'TextRectWLat'  : limprot['TextRectWLat'],
		'ImageH'        : limprot['ImageH'],
	},
	name['TarProtRes'] : { # See the tarprot dict for the meaning of the terms
		'RectH'         : tarprot['RectH'],
		'RectT'         : tarprot['RectT'],
		'RectSx'        : tarprot['RectSx'],
		'RectEx'        : tarprot['RectEx'],
		'PanelBelow'    : tarprot['PanelBelow'],
		'LabelW'        : tarprot['LabelW'],
		'LabelpLocY'    : tarprot['LabelpLocY'],
		'LabelFirstExp' : tarprot['LabelFirstExp'],
		'LBTopGap'      : tarprot['LBTopGap'],
		'LBLineW'       : tarprot['LBLineW'],
		'TextRectH'     : tarprot['TextRectH'],
		'TextRectWLat'  : tarprot['TextRectWLat'],
		'ImageH'        : tarprot['ImageH'],
	},
}

cutprop = { # Information about the cutprop file
	'ColNames' : [ # Col names in the cutprop data frame
		'Residue Number', 
		'Fixed Residue Number', 
		'FP Cleavages Rec', 
		'FP Cleavages Rec Norm', 
		'FP Cleavages Nat',
		'FP Cleavages Nat Norm'
	],
	'SortBy' : [ # Col names to sort the data frame
		'Residue Number'
	],
	'NumColsHeader':  6, # Number of columns in the data frame excluding the experiments
	'NColExpStart' :  2, # Index of the column in the data frame where experiments beging
	'NColFPStart'  : -4, # Index of the column in the data frame where the FP results starts
	'DistBetExp'   :  4, # Number of columns for each experiment
}

aadist = { # Information about the aadist file
	'FillChar'  : '-',   # Character used by BioPython to fill sequence gaps
	'FP'        : 'FP',  # Name for the Filtered Peptide key
	'RD'        : 'RD',  # Name for the Random Cleavages key
	'NumKeys'   : 2,     # Number of keys excluding experiments
	'Poskey'    : 'Pos', # Name of the position key holding the chi square results
	'Twidth'    : 0.8,   # Total width for a position or an experiment in the bar plot
	'StartLoc'  : 0.4, # To have some space between positions or experiments
}

hist = { # Information about the hist files 
	'DictKeys': [ 
		'Rec-all', 
		'Rec-uni', 
		'Nat-all', 
		'Nat-uni'
	],
	'Twidth'  : 0.8, # Total width for a position/experiment in the bar plot
	'StartLoc': 0.4  # To have some space between positon/experiment in the bar plot
}

typeRes = { # Information about the typeRes window
	'labelRow' : {
		name['LimProt']  : 'Bands:',
		name['ProtProf'] : 'Conditions:', 
		name['TarProt']  : 'Experiments:',
	},
	'labelCol' : {
		name['LimProt']  : 'Lanes:',
		name['ProtProf'] : 'Relevant points:', 
		name['TarProt']  : 'NA',		
	},
	'minValRow' : {
		name['LimProt']  : 1,
		name['ProtProf'] : 1, 
		name['TarProt']  : 1,
	},
	'minValCol' : {
		name['LimProt']  : 1,
		name['ProtProf'] : 2, 
		name['TarProt']  : 1,
	},
	'ModList' : [ # Modules that modify one row for control experiments
		name['TarProt'], 
		name['LimProt'],
	],
}
#endregion ------------------------------------- Information about UMSAP Files

#region ---------------------------------------- Information about other Files
pdbFile = { # Information about pdb files
	'Coord records' : { # Details about the pdb records containing atomic coordinates
		'ATOM'      : [(1, 4)  , 'ATOM'      , 'string'],
		'HETATM'    : [(1, 6)  , 'HETATM'    , 'string'],
		'ANumber'   : [(7, 11) , 'ANumber'   ,    'int'],
		'AName'     : [(13, 16), 'AName'     , 'string'],
		'AltLoc'    : [(17, )  , 'AltLoc'    , 'string'],
		'ResName'   : [(18, 20), 'ResName'   , 'string'],
		'Chain'     : [(22, )  , 'Chain'     , 'string'],
		'ResNum'    : [(23, 26), 'ResNum'    ,    'int'],
		'CodeResIns': [(27, )  , 'CodeResIns', 'string'],
		'X'         : [(31, 38), 'X'         ,  'float'],
		'Y'         : [(39, 46), 'Y'         ,  'float'],
		'Z'         : [(47, 54), 'Z'         ,  'float'],
		'Occupancy' : [(55, 60), 'Occupancy' ,  'float'],
		'Beta'      : [(61, 66), 'beta'      ,  'float'],
		'Segment'   : [(73, 76), 'Segment'   , 'string'],
		'Element'   : [(77, 78), 'Element'   , 'string'],
		'DFHeader'  : [ # Col names for hte data frame containing the information about the pdb file
			'ATOM', 
			'ANumber', 
			'AName', 
			'AltLoc', 
			'ResName', 
			'Chain',
			'ResNum', 
			'CodeResIns', 
			'X', 
			'Y', 
			'Z', 
			'Occupancy', 
			'beta', 
			'Segment', 
			'Element'
		],
	},
}
#endregion ------------------------------------- Information about other Files

#region ----------------------------------------------------------- Extensions
extLong = { # string for the dlg windows representing the extension of the files
	'Data'    : 'txt files (*.txt)|*.txt',
	'Seq'     : 'txt fasta files (*.txt; *.fasta)|*.txt;*.fasta',
	'PDB'     : 'pdb files (*.pdb)|*.pdb',
	'PDF'     : 'pdf files (*.pdf)|*.pdf',
	'TarProt' : 'tarprot files (*.tarprot)|*.tarprot',
	'LimProt' : 'limprot files (*.limprot)|*.limprot',
	'Protprof': 'protprof files (*.protprof)|*.protprof',
	'AAdist'  : 'aadist files (*.aadist)|*.aadist',
	'Histo'   : 'hist files (*.hist)|*.hist',
	'CorrA'   : 'corr files (*.corr)|*.corr',
	'Uscr'    : 'uscr files (*.uscr)|*.uscr',
	'CutProp' : 'cutprop files (*.cutprop)|*.cutprop',
	'UmsapM'  : ("UMSAP main output files (*.tarprot; *.limprot; *.protprof)"
		"|*.tarprot;*.limprot;*.protprof"),
	'UmsapR'  : ("UMSAP files (*.tarprot; *.cutprop; *.aadist; *.hist; "
		"*.corr; *.limprot; *.protprof)|*.tarprot;*.cutprop;*.aadist;*.hist;"
		"*.corr;*.limprot;*.protprof"),
	'MatplotSaveImage' : ("Portable Document File (*.pdf)|*.pdf|Portable "
		"Network Graphic (*.png)|*.png|Scalable Vector Graphic (*.svg)|*.svg|"
		"Tagged Image File (*.tif)|*.tif"),
	'FragImage' : 'Image files (*.png; *.tiff)|*.png;*.tiff'
}

extShort = { # extension of selected files to get default values. When more than one element, the first elemeent will be the default value
	'Data'    : ['.txt'],
	'Seq'     : ['.txt', '.fasta'],
	'PDB'     : ['.pdb'],
	'PDF'     : ['.pdf'],
	'TarProt' : ['.tarprot'],
	'LimProt' : ['.limprot'],
	'ProtProf': ['.protprof'],
	'AAdist'  : ['.aadist'],
	'Histo'   : ['.hist'],
	'CorrA'   : ['.corr'],
	'Uscr'    : ['.uscr'],
	'CutProp' : ['.cutprop'],
	'UmsapM'  : ['.tarprot', '.limprot', '.protprof'],
	'UmsapR'  : ['.tarprot', '.cutprop', '.aadist', '.hist', '.corr', 
		'.limprot', '.uscr', '.protprof'],
}

extName = { # Link the file extension to name dict
	'.limprot' : name['LimProt'],
	'.tarprot' : name['TarProt'],
	'.protprof': name['ProtProf'],
}
#endregion -------------------------------------------------------- Extensions

#region --------------------------------------------------------------- Images
image = { # Information regarding images
	#--> paths to images in:
	'icon' : path['Images'] / 'icon2.ico',
	'Main' : path['Images'] / 'MAIN-WINDOW/p97-2.png',
	'Util' : path['Images'] / 'MAIN-WINDOW/p97-2.png',
	'About': path['Images'] / 'ABOUT/p97-2-about.png',
	#--> 
	'DPI'  : 300, # dpi resolution for the matplotlib images
}
#endregion ------------------------------------------------------------ Images

#region ------------------------------------------------------------------ URL
url_home = 'https://www.umsap.nl'
url_tutorial = f"{url_home}/tutorial/2-1-0"

url = { # Selected URL needed by umsap.
 #--> Third party sites
	'Uniprot'  : 'https://www.uniprot.org/uniprot/',
	'Pdb'      : 'http://www.rcsb.org/pdb/files/',
 #--> www.umsap.nl
	'Home'            : url_home,
	'Update'          : f"{url_home}/page/release-notes",
	'Tutorial'        : f"{url_tutorial}/start",
	name['CorrA']     : f"{url_tutorial}/correlation-analysis",
	name['MergeAA']   : f"{url_tutorial}/merge-aadist-files",
	name['ShortDFile']: f"{url_tutorial}/short-data-files",
	name['TarProt']   : f"{url_tutorial}/targeted-proteolysis",
	name['AAdist']    : f"{url_tutorial}/aa-distribution",
	name['Cuts2PDB']  : f"{url_tutorial}/cleavages-pdb-files",
	name['Histo']     : f"{url_tutorial}/histograms",
	name['SeqAlign']  : f"{url_tutorial}/sequence-alignment",
	name['LimProt']   : f"{url_tutorial}/limited-proteolysis",
	name['SeqH']      : f"{url_tutorial}/sequence-highlight",
	name['ProtProf']  : f"{url_tutorial}/proteome-profiling",
}
#endregion --------------------------------------------------------------- URL

#region ------------------------------------------------------------- ListCtrl
listctrl = { # Information regarding the col width and header of list boxes
	'Widths' : { # width for each column
		name['TarProt']      : (40, 200),
		name['LimProt']      : (40, 200),
		name['ProtProf']     : (40, 200),
		name['TypeRes']      : (40, 200),
		name['TarProtRes']   : (40, 200),
		name['LimProtRes']   : (40, 200),
		name['ProtProfRes']  : (45, 75, 140),
		name['MergeAA']      : (40, 560),
		name['CorrA']        : (40, 200),
		'CorrA2'             : (40, 200)
	},
	'Header' : { # Name of each column
		name['TarProt']     : ['#', 'Columns in the Data File'],
		name['LimProt']     : ['#', 'Columns in the Data File'],
		name['ProtProf']    : ['#', 'Columns in the Data File'],
		name['TypeRes']     : ['#', 'Columns in the Data File'],
		name['ProtProfRes'] : ['#', 'Gene names', 'Protein IDs'],
		name['CorrA']       : ['#', 'Columns in the Data File'],
		'CorrA2'            : ['#', 'Selected columns'],
		name['TarProtRes']  : ['#', 'Sequences in the FP list'],
		name['LimProtRes']  : ['#', 'Sequences in the FP list'],
		name['MergeAA']     : ['#', 'Files to merge']		
	},
}
#endregion ---------------------------------------------------------- ListCtrl

#region ------------------------------------------------ ComboBox and RadioBox
combobox = { # Information for combo boxes
	'NormValues': [
		'None', 
		'Log2',
	],
	'Avalues': [
		'0.100', 
		'0.050', 
		'0.025', 
		'0.010', 
		'0.001',
	],
	'CorrAMethod': [
		'Pearson', 
		'Kendall', 
		'Spearman',
	],
	'ModValues': [
		'Targeted proteolysis', 
		'Limited proteolysis',
	],
	'Bvalues': [
		'Equal alpha', 
		'0.100', 
		'0.050', 
		'0.025', 
		'0.010', 
		'0.001',
	],
	'Yvalues': [
		'1.0', '0.9', '0.8', '0.7', '0.6', '0.5', '0.4', '0.3', 
		'0.2', '0.1', '0.0'
	],
	'CorrectP': [
		'None',
		'Benjamini - Hochberg',  
		'Benjamini - Yekutieli',
		'Bonferroni',            
		'Holm',                  
		'Holm - Sidak',          
		'Hommel',        
		'Sidak',                 
		'Simes-Hochberg',
	],
	'ControlType' : [
		'One Control', 'One Control per Column', 'One Control per Row',
	],
}

radiobox = { # Information for radio boxes
	'CheckUpdate' : ['Automatically', 'Never']
}
#endregion --------------------------------------------- ComboBox and RadioBox

#region ------------------------------------------------------------- Messages
msg = { # Text messages used in the programm
	'StaticBoxNames' : { # Name of the StaticBoxes
		'Files'  : 'Files',
		'Values' : 'Values',
		'Columns': 'Column numbers', 
	},
	'TextInput' : { # For text in input dialog
		'msg': {
			'aVal'           : "α value:",
			'ZScoreThreshold': "Z score threshold value (%):",
			'Filter_ZScore'  : "Threshold value: (%):",
			'Filter_Log2FC'  : 'Threshold value (absolute value):',
			'Filter_P'       : 'Threshold value:',
			'Filter_OneP'    : 'Threshold value:',
		},
		'caption' : {
			'aVal'           : 'α value for the Volcano plot',
			'ZScoreThreshold': "Z score threshold for the Volcano plot",
			'Filter_ZScore'  : "Filter results by Z score",
			'Filter_Log2FC'  : 'Filter results by Log2FC value',
			'Filter_P'       : 'Filter results by P value',
			'Filter_Remove'  : 'Remove filters',
			'Filter_OneP'    : 'Filter relevant points by α value',
		}
	},
	'Open' : { # For open file dialogues
		'DataFile'   : 'Select the data file',
		'TarProtFile': 'Select the tarprot file',
		'LimProtFile': 'Select the limprot file',
		'SeqRecFile' : 'Select the recombinant sequence file',
		'SeqNatFile' : 'Select the native sequence file',
		'PDBFile'    : 'Select the PDB file',
		'UMSAPFile'  : 'Select the UMSAP file',
		'UMSAPMFile' : 'Select the UMSAP main output file',
		'InputF'     : 'Select the .uscr file',
		'AAdistFile' : 'Select the .aadist files',
		'ResultLFile': 'Select the file with the data'
	},
	'Save' : { # For save file dialogues
		'OutFile'        : 'Select the output file',
		'PlotImage'      : 'Save plot image',
		'ExportData'     : 'Save data as',
		'TarProtFragImg' : 'Save image of the fragments',
		'LimProtGelImg'  : 'Save image of the gel',
	},
	'UErrors' : { # For unexpected errors
		'OS' : ("This operating system is not supported. Proceed at your own "
			"risk."),
		'Unknown' : ("An unexpected error just happened.")
	},
	'Errors' : { # For errors details
		'Nothing' : '\nNothing will be done.',
	 #--> File path related
		'Datafile' : ("Data file points to a file that cannot be read."),
		'Datafile2': ("Select a Data file first."),
		'Seq_rec' : ("Sequence (Rec) must hold the path to a local file or a "
			"valid UNIPROT code."),
		'Seq_nat' : ("Sequence (Nat) must hold the path to a local file, a "
			"valid UNIPROT code or the value NA."),
		'PDBfile' : ("PDB file must hold the path to a local file or the value"
			" NA."),
		'PDBfile2' : ("PDB file points to a file that cannot be read."),
		'OutputFile' : ("Output file points to a file that cannot be used."),
		'TarProtFile' : ("Tarprot file points to a file that cannot be read."),
		'UMSAPFile' : ("UMSAP file points to a file that cannot be read."), 
		'LimProtFile' : ("Limprot file points to a file that cannot be read."),
		'ConfigUserFile': ("It was not possible to save the user configuration"
			" file."),
		'ConfigDefFile' : ("It was not possible to read the file with the "
			"default option values."),
	 #--> File content related
		'BadCsvFile' : ("The given Data file could not be loaded. A plain text "
			"file with tab separated columns and column names in the first line"
			" is expected here."),
		'chainSInFile' : ("The chain/segment in PDB ID was not found in the "
			"given PDB file."),
		'NoPeptInRecSeq' : ("The sequence of the recombinant protein does not "
			"include one of the peptides reported in the Data file."),
		'NoNatSeq' : ("The native sequence was not specified when creating the "
			"tarprot file"),
		'TarProtFileFormat': ("The given .tarprot file appears to be damaged."),
		'ProtProfFileFormat' : ("The given .protprof file appears to be "
			"damaged."),
		'LimProtFileFormat' : ("The given .limprot file appears to be "
			"damaged."),
		'CorrFileFormat' : ("The given .corr file appears to be damaged."),
		'CutPropFileFormat': ("The given .cutprop file appears to be damaged."),
		'HistoFileFormat' : ("The given .hist file apperrs to be damaged."),
		'AAdistFileFormat' : ("The given .aadist file appears to be damaged."),
		'UscrFileNoModule' : ("The given .uscr file does not contain the "
			"keyword: Module."),
		'UscrFileUnknownModule' : ("The Module in the given .uscr file is "
			"unknown."),
		'UscrFileNoKeywords' : ("There are no valid keywords in the given "
			".uscr file."),
	 #--> Folder path related
		'Outputfolder' : ("Output folder points to a folder that cannot be "
			"used."),
		'Outputname' : ("Output name cannot be empty."),	
	 #--> Value related
		'NoFloatInColumns' : ("There is at least one non numeric value in the "
			"selected columns."),
		'FiltPept' : ("The current settings do not allow to include any peptide"
			" in the Filtered Peptide list."),
		'FiltPept2' : ("The filtered peptide list in the selected tarprot file "
			"is empty."),
		'FiltPept2LP' : ("The filtered peptide list in the selected limprot "
			"file is empty."),
		'NoResults_PP' : ("The current settings results in the exclution of all"
			" proteins in the data file."),			
		'Targetprotein' : ("Target protein cannot be empty."),
		'Scorevalue' : ("Score value must hold a decimal number equal or "
			"greater than 0."),
		'duVal' : ("Delta value must hold a decimal number equal or "
			"greater than 0."),
		'dmVal' : ("Delta max value must hold a decimal number equal or "
			"greater than 0."),		
		'Positions' : ("Positions must hold an integer number greater than 0"
			" or the value NA."),
		'Positions2' : ("Positions must hold an integer number greater than 0."
			""),
		'Sequencelength' : ("Sequence length must hold an integer number "
			"greater than 0 or the value NA."),
		'Sequencelength2' : ("Sequence length must hold an integer number "
			"greater than 0."),
		'Histogramwindows' : ("Histogram windows must hold an integer number "
			"greater than 0, a list of ordered positive integer numbers or the "
			"value NA."),
		'Histogramwindows2' : ("Histogram windows must hold an integer number "
			"greater than 0 or a list of ordered positive integer numbers."),
		'PDBID' : ("PDB ID must hold two values separated by a semicolon (;). "
			"The values must be:\n 1.- a valid PDB code\n 2.- a chain/segment "
			"identifier.\nThe maximum length of each value is 4 characters. "
			"\nThe value NA means no analysis." ),
		'PDBID2' : ("PDB ID must hold two values separated by a semicolon (;). "
			"The values must be a valid PDB code and a chain/segment "
			"identifier. The maximum length of each value is 4 characters."),		
		'SeqCol' : ("Sequences must hold an integer number greater or equal to "
			"0."),
		'DetectProtCol' : ("Detected proteins must hold an integer number "
			"greater or equal to 0."),
		'ScoreCol' : ("Score must hold an integer number greater or equal to "
			"0."),
		'GeneNCol' : ("Gene names must hold an integer number greater or equal "
			"to 0."),
		'ExcludeCol' : ("Exclude proteins must hold a list of positive "
			"integer numbers or the value NA."),						
		'ColExtract' : ("Columns to extract must hold a list of positive "
			"integer numbers or the value NA."),
		'ColExtract2' : ("Columns to extract must hold a list of positive "
			"integer numbers."),
		'ControlNA' : ("Control experiments in Results - Control experiments"
			" cannot be empty or NA."),		
		'Results' : ("Results - Control experiments must hold a list of unique "
			"positive integer numbers.\nSemicolons (;) are used to separate "
			"replicates of different experiments."),
		'ResultsPP' : ("Results - Control experiments must hold a list of "
			"positive integer numbers.\nCommas (,) are used to separate "
			"replicates of different experiments. Semicolons (;) are used to "
			"separate relevant points or conditions.\nSee the manual for more "
			"details."),	
		'ResultsLP' : ("Results - Control experiments must hold a list of "
			"unique positive integer numbers.\nCommas (,) are used to separate "
			"replicates of different bands. Semicolons (;) are used to separate"
			" lanes.\nSee the manual for more details."),	
		'ResultsShape' : ("Results - Control experiments must hold the same "
			"number of elements in each defined level."),				
		'ListCtrlRightEmpty' : ("The list below Columns to analyze must contain"
			" at least two items."),
		'NoDataSelected' : ("Please select a Data file and some columns."),
		'NoAAdistFiles' : ("Please select more than one .aadist file."),
		'Character' : ("Character cannot be empty."),
		'EqualNElem' : ("Results and control experiments must have the same "
			"number of replicates."),
		'LTimeP_PP' : ("A minimum of one time point per condition is needed."),
		'NElemPLevel_LP' : ("Results - Control experiments must contain the "
			"same number of bands per lane in the gel."),
		'NTPperCond_PP' : ("Results - Control experiments must contain the same"
			" number of relevant points for each condition."),
		'TyepResRowCol': ("must contain a positive integer number."),
		'NConds_PP' : ("The number of conditions in Conditions and Results are "
			"different."),
		'NTimeP_PP' : ("The number of relevant points in Relevant points and "
			"Results are different."),
		'TimePoint_Number' : ("More than one relevant point is needed for this"
			"filter."),
		'Conditions_Number' : ("More than one conditions is needed for this"
			"filter."),
		'No_Filters' : ("There are no applied filters."),
		'NoExport' : ("There is nothing to export."),
		'FailExport' : ("It was not possible to export the data in the "
			"selected file."),
	 #--> Image related
		'ImgNotSaved' : ("The image could not be saved."),
	 #--> Option related
		'FileExt' : ("The extension of the given file is not valid in this "
			"context."),
		'NormMethod' : ("The given normalization method is unknown."),
		'UniqueTP' : ("The values for Sequences, Detected proteins, Score," 
			" and Results must be unique."),
		'UniquePP' : ("The values for Detected proteins, Gene names, Score," 
			" Exclude proteins and Results must be unique."),
		'ColNumber' : ("The given data file contains less columns than "
			"requested."),
		'UOption' : ("Received and unknown option."),
		'Filter_ZScore' : ("Please provide a valid value to filter the "
			"results by Z score. \ne.g. < 10 or > 25"),
		'Filter_Log2FC' : ("Please provide a valid value to filter the "
			"results by Log2FC. \ne.g. < 1.5 or > 2"),
		'Filter_P' : ("Please provide a valid value to filter the "
			"results by P values.\ne.g. < 0.01 or p > 0.005"),
		'Filter_OneP' : ("Please provide a valid value to filter the "
			"Relevant points by α threshold.\ne.g. 0.01"),
	 #--> class related
		'NoSeq' : ("It is not possible to create an instance of "
			"DataObjSequenceFile with no sequence."),
		'NoAlign' : ("The sequence alignment algorithm failed."),
		'NoOverlap' : ("There is no overlap between the two sequences."),
	 #--> TypeRes
		'MixNA' : ("Mixing NA with column numbers will result in an error when"
			" running the analysis."),
		'CType' : ("Options for Results - Control experiments are not properly"
			" configured. Use the Type values button to check the options."),
		'ResMatrixShape' : ("Values in Results - Control experiments are not "
			"properly organized. Use the Type values button to organize the "
			"values."),
	 #--> Internet related
		'UMSAPSite' : ("Check for updates failed.\nIt was not possible to "
			"contact umsap.nl.\nCheck your Internet connection."),
	},
	'StaticText' : { # For tooltips regarding static text widgets
	 #--> Used in TarProt Module
		'TarProt' : ("A unique protein identifier present in the data file."
			"\ne.g. efeB"),
		'ScoreVal' : ("Detected sequences will be considered relevant if their"
			" score values are higher than the Score value defined here.\n"
			"e.g. 50.7"),
		'DataNorm' : ("Normalization procedure to be applied to the data."),
		'aVal' : ("Significance level for the ANCOVA test."),
		'Positions' : ("Number of positions to consider during the amino acids "
			"distribution analysis.\ne.g. 5"),
		'SeqLength' : ("Number of residues per line in the sequence alignment "
			"files.\ne.g. 100"),	
		'HistWin' : ("Histogram window sizes.\nOne number will result in "
			"multiple windows with the same width. Multiple numbers will "
			"define custom sized windows.\nSee the manual for more details."
			"\ne.g. 50 or 0 50 100 200 400"),
		'PDBID' : ("The PDB code and the chain/segment that will be used to map"
			" the detected cleavages.\nIf a local file has being specified only"
			" the chain/segment is needed here.\ne.g. A or SEGA or 2Y4F;A or "
			"2Y4F;SEGA"),
		'Sequence' : ("Column number in the data file containing the detected "
			"sequences.\ne.g. 0"),
		'DetProt' : ("Column number in the data file containing the unique "
			"protein identifiers.\ne.g. 38"),
		'Score' : ("Column number in the data file containing the Score values."
			"\ne.g. 44"),
		'ColExt' : ("Column number(s) in the data file to be written to the "
			"short data output files.\ne.g. 0-2 35 40-50 51"),
		'Results' : ("Column number(s) in the data file containing the "
			"Results and Control experiments.\nReplicates from different "
			"experiments are separated by semicolons (;).\nThe first values are"
			" for the Control experiments. \ne.g. Control experiments plus "
			"three different experiments:\n98-105; 109-111; 112 113 114; "
			"115-117 120"),
		'ResultsPP' : ("Column number(s) in the data file containing the "
			"Results and Control experiments.\nIn this case the values cannot "
			"be directly typed.\nPlease use the Type value or Load values."),
		'ResultsLP' : ("Column number(s) in the data file containing the "
			"Results and Control experiment.\nReplicates from different lanes" 
			" are comma (,) separated. Different bands are separated by a "
			"semicolon (;).\nThe first values are for the Control experiments.\n"
			"e.g. Control experiments plus three lanes with two bands and "
			"two replicates per gel: \n69-71; 105 125, 106 126, 107 127; "
			"101 121, 130 132, 141 142"),
	  #--> Used in ProtProf
		'ScoreValPP' : ("Detected proteins will be considered relevant if their"
			" score values are higher than the Score value defined here.\n"
			"e.g. 50.7"),
		'CharacterPP' : ("Character used to separate protein names in the data"
			" file.\ne.g. ;"),		
		'MedianCorrection' : ("Apply median correction to Results columns after"
			" normalization."),
		'TimeP' : ("Name of the relevant points tested.\ne.g. 0H, 1H, 24H"),
		'CorrP' : ("Method to correct the calculated p values"),
		'GeneN' : ("Column number with the gene names of the identified "
			"proteins.\ne.g. 6"),			
	 #--> Used in LimProt
		'aValLP' : ("Significance level for the statistical tests."),
		'bValLP' : ("Beta level for the statistical tests."),
		'yValLP' : ("Confidence limit level for estimating the measuring "
			"precision."),
		'dValLP' : ("User provided confidence interval. The value depends on "
			"the normalization procedure used. NA means estimate the confidence"
			" interval for each peptide.\ne.g. 3"),
		'dmaxValLP' : ("Maximum value for the calculated confidence interval."
			"\ne.g. 8"),
		'SeqLength_LP' : ("Number of residues per line in the sequence file.\n"
			"The recommended higher number is 100.\ne.g. 85"),
	 #--> Used in CorrA
		'CorrelationM' : ("Select the method used to calculate the correlation"
			" coeficients."),
	 #--> Used in AAdist U
		'Positions2' : ("Number of positions to consider during the amino acids"
			" distribution analysis.\ne.g. 5"),
	 #--> Used in Histo U
		'HistWin2' : ("Histograms window size.\nOne number will result in "
			"multiple windows with the same width. Multiple numbers will "
			"define custom sized windows.\nSee the manual for more details."
			"\ne.g. 50"),
	 #--> Used in mergeAA
		'OutputFile' : ("The path to the selected output file."),
	 #--> Used in TypeR
		'Experiments' : ("Number of experiments to analyze."),
		'Bands' : ("Number of bands to analyze."),
		'Lanes' : ("Number of lanes to analyze."),
		'Conditions' : ("Information regarding the conditions to analyze."),
		'ConditionsNu' : ("Number of conditions to analyze.\ne.g. 4"),
		'ConditionsNa' : ("Name of the conditions to analyze.\ne.g. A, B, C"),
		'RP' : ("Information regarding the relevant points to analyze."),
		'RPNu' : ("Number of relevant points to analyze.\ne.g. 3"),
		'RPNa' : ("Name of the relevant points to analyse.\ne.g. 1H, 12H, 1D"),
		'Control' : ("Information regarding the control experiments."),
		'ControlNa' : ("Name of the control experiment.\ne.g DMSO"),
		'ControlType' : ("Control experiment design."),
	 #--> Used in ProtProf
		'Exclude' : ("Proteins found in these columns will be excluded from" 
			" the analysis.\ne.g. 45 67 109"),
	},
	'Button' : { # For tooltips regarding button widgets
	 #--> Used in Main
		'LimProt'  : ("Start the " + mod[name['LimProt']] + " module."),
		'ProtProf' : ("Start the " + mod[name['ProtProf']] + " module."),
		'TarProt'  : ("Start the " + mod[name['TarProt']] + " module."),
		'Util'     : ("Show the built-in " + mod[name['Util']] + "."),
	 #--> Used in Update Notice
		'UpdateOk' : ("Close the window."),
		'UpdateRead' : ("Read the release notes in umsap.nl."),
	 #--> Used in Util
		'AAdist' : ("Generate an amino acid distribution based on a .tarprot"
			" file."),
		'CutPerRes' : ("Count the number of cleavages per residue found in a "
			".tarprot file."),
		'Cuts2PDB' : ("Map the number of cleavages found in a .tarprot file to"
			" a protein structure."),
		'CInputFile' : ("Create an input file from a main UMSAP output file."),
		'Export' : ("Export selected data to a file with CSV format."),
		'CHist' : ("Generate histograms of the detected cleavage sites "
			"found in a .tarprot file."),
		'SeqAlign' : ("Generate sequence alignments based on the peptides found"
			" in a .tarprot file."),
		'ShortFile' : ("Generate short versions of a data file based on a "
			"main UMSAP output file."),
		'CorrA' : ("Perform a correlation analysis of the data in a data "
			"file."),
		'AAdistM' : ("Merge several .aadist files."),
		'ReadOut' : ("Read an UMSAP file and generates a graphical "
			"representation of the results in it."),
		'UpdateTP' : ("Read a .tarprot file from a previous version of UMSAP "
			"and generate UMSAP result files compatible with the current "
			"version of UMSAP."),
		'ReadTP' : ("Read a .tarprot file from a previous version of UMSAP and "
			"load the Targeted Proteolysis module with the data in the "
			".tarprot file."),
		'RunScript' : ("Read an input file and configure the window of the "
			"corresponding module."),
		'SeqH' : ("Highlight the detected fragments in the sequence of the "
			"protein."),
	 #--> Used in Tarprot Mod
		'DataFile' : ("Browse the file system to select a data file.\nOnly "
			"plain text files with tab delimited columns are supported here."),
		'SeqRec' : ("Browse the file system to select the file with the "
			"sequence of the Recombinant protein.\nFASTA or plain text files "
			"containing only one aa sequence are supported.\nAlternatively, a "
			"UNIPROT ID can be given here.\ne.g.P31545"),
		'SeqNat' : ("Browse the file system to select the file with the "
			"sequence of the Native protein.\nFASTA or plain text files "
			"containing only one aa sequence are supported.\nAlternatively, a "
			"UNIPROT ID can be given here.\ne.g.P31545"),
		'PDBFile' : ("Browse the file system to select the file with the "
			"structure of the Target protein.\nOnly .pdb files are supported "
			"here."),
		'OutputFolderDataFile' : ("Browse the file system to select the "
			"folder that will contain the output files.\nNA means the"
			" output folder will be created in the same directory as the "
			"data file, with a default name."),
		'OutputFolderTarProtFile' : ("Browse the file system to select the "
			"folder that will contain the output files.\nNA means the "
			"output folder will be created in the same directory as the "
			".tarprot file, with a default name."),
		'OutputFolderUMSAPFile' : ("Browse the file system to select the "
			"folder that will contain the output files.\nNA means the "
			"output folder will be created in the same directory as the "
			"UMSAP file, with a default name."),			
		'OutputFileDataFile' : ("Browse the file system to select the location"
			" of the output file.\nNA means the output file will be "
			"created in the same directory as the data file, with a default "
			"name."),
		'OutputFileTarProtFile' : ("Browse the file system to select the "
			"location of the output file.\nNA means the output file will "
			"be created in the same directory as the .tarprot file, with a "
			"default name."),
		'OutputFileUMSAPFile' : ("Browse the file system to select the "
			"location of the output file.\nNA means the output file will "
			"be created in the same directory as the UMSAP file, with a "
			"default name."),			
		'OutputFileLimProtFile' : ("Browse the file system to select the "
			"location of the output file.\nNA means the output file will "
			"be created in the same directory as the .limprot file, with a "
			"default name."),
		'OutputFile' : ("Browse the file system to select the location"
			" of the output file."),
		'OutName' : ("This button does nothing but the text box to the right "
			"allows to type the name of the files that will be created.\nNA "
			"means the files will have a default name.\ne.g. myAnalysis"),
	 #--> Used in ProtProf
		'OutNamePP' : ("This button does nothing but the text box to the right "
			"allows to type the name of the files that will be created.\nNA "
			"means the name will be set to protprof.\ne.g. myAnalysis"),
		'ResultsW' : ("Type the column numbers containing the replicates of the"
			" results and control experiments.\nSee the manual for more "
			"details."),
		'ResultsL' : ("Load the column numbers containing the replicates of the"
			" results and control experiments.\nSee the manual for more "
			"details."),
	 #--> Used in LimProt
		'OutNameLP' : ("This button does nothing but the text box to the right "
			"allows to type the name of the files that will be created.\nNA "
			"means the name will be set to limprot.\ne.g. myAnalysis"),
	 #--> Used in Utils Windows
		'LimProtFile' : ("Browse the file system to select a .limprot file.\n"
			"Only .limprot files are supported here."),
		'TarProtFile' : ("Browse the file system to select a .tarprot file.\n"
			"Only .tarprot files are supported here."),
		'DataFile2' : ("Browse the file system to select a data file. Only "
			"plain text files with tab delimited columns are supported here. "
			"NA means the location of the data file will be read from the "
			"given .tarprot file"),
		'aadistFile' : ("Browse the file system to select the .aadist files."),
	 #--> Used in CorrA
		'AddColCorrA' : ("Add selected columns in the left list to the list on "
			"the right."),
	 #--> Short data file
		'UMSAPMFile' : ("Browse the file system to select the main output file"
			" from a module."),
	 #--> Help Run
		'Help' : ("Show the online tutorials at www.umsap.nl."),
		'Run' : ("Start the analysis."),
	 #--> Clear buttons
		'All' : ("Clear the content of all user provided input."),
		'Files' : ("Clear the content of section Files."),
		'Values' : ("Clear the content of section Values."),
		'Cols' : ("Clear the content of section Column numbers."),
	 #--> Used in TypeRes
		'Create' : ("Create the matrix of text fields to write the column "
			"numbers."),
		'Ok' : ("Export column numbers to the Result - Control experiments "
			"field in the window of the module."),
		'Cancel' :	("Close this window."),	
	 #--> Used in Preferences
		'SavePref' : ("Save the configuration options."),
		'CancelPref' : ("Close the Preference window without saving."),
		'LoadDef' : ("Load default values."),						
	},
	'FilteredValues' : { # Filtered values in ProtProf
		'Examples' : {
			'Filter_ZScore': 'e.g. < 10 or > 20',
			'Filter_Log2FC': 'e.g. < 2 or > 1.4',
			'Filter_P'     : 'e.g. < 0.05 or > 0.001',
			'Filter_OneP'  : 'e.g. 0.01',
		},
		'StatusBar' : {
			'Filter_ZScore': 'Zscore',
			'Filter_Log2FC': 'Log2FC',
			'Filter_P'     : 'P',
			'Filter_OneP'  : 'α',
		},
	},		
	'OptVal' : ("\n---\nThis field is optional (NA)."),	
}
#endregion ---------------------------------------------------------- Messages

#region ------------------------------------------------------------- Tooltips
tooltip = { # This dict makes it easier to set the tooltips based on the name of the window
	name['Main'] : { # Main Window
		'LimProt'  : msg['Button']['LimProt'],
		'ProtProf' : msg['Button']['ProtProf'],
		'TarProt'  : msg['Button']['TarProt'],
		'Util'     : msg['Button']['Util']
	},
	name['UpdateNotice'] : { # Update notice window
		'Ok'   : msg['Button']['UpdateOk'],
		'Read' : msg['Button']['UpdateRead'],
	},
	name['Util'] : { # Utilities Window
	    'AAdist'    : msg['Button']['AAdist'],
	    'CutPerRes' : msg['Button']['CutPerRes'],
	    'Cuts2PDB'  : msg['Button'][ 'Cuts2PDB'],
	    'CInputFile': msg['Button']['CInputFile'],
	    'Export'    : msg['Button']['Export'],
	    'CHist'     : msg['Button']['CHist'],
	    'SeqAlign'  : msg['Button']['SeqAlign'],
	    'ShortFile' : msg['Button']['ShortFile'],
	    'CorrA'     : msg['Button']['CorrA'],
	    'AAdistM'   : msg['Button']['AAdistM'],
	    'ReadOut'   : msg['Button']['ReadOut'],
	    'UpdateTP'  : msg['Button']['UpdateTP'],
	    'ReadTP'    : msg['Button']['ReadTP'],
	    'RunScript' : msg['Button']['RunScript'],
	    'SeqH'      : msg['Button']['SeqH']
	},
	name['ProtProf'] : { # Proteome Profiling module
		'DataFile'            : msg['Button']['DataFile'],
		'OutputFolderDataFile': msg['Button']['OutputFolderDataFile'],
		'OutName'             : msg['Button']['OutNamePP'],
		'ResultsW'            : msg['Button']['ResultsW'],
		'ResultsL'            : msg['Button']['ResultsL'],
		'ScoreVal'            : msg['StaticText']['ScoreValPP'],
		'MedianCorrection'    : msg['StaticText']['MedianCorrection'],
		'Character'           : msg['StaticText']['CharacterPP'],
		'Results'             : msg['StaticText']['ResultsPP'],
		'Conditions'          : msg['StaticText']['Conditions'],
		'TimeP'               : msg['StaticText']['TimeP'],
		'CorrP'               : msg['StaticText']['CorrP'],
		'GeneN'               : msg['StaticText']['GeneN'],
		'Exclude'             : msg['StaticText']['Exclude'],
	},
	name['LimProt'] : { # Limited Proteolysis module
		'DataFile'            : msg['Button']['DataFile'],		
		'OutputFolderDataFile': msg['Button']['OutputFolderDataFile'],
		'OutName'             : msg['Button']['OutNameLP'],
		'ResultsW'            : msg['Button']['ResultsW'],
		'ResultsL'            : msg['Button']['ResultsL'],
		'aVal'                : msg['StaticText']['aValLP'],
		'bVal'                : msg['StaticText']['bValLP'],
		'yVal'                : msg['StaticText']['yValLP'],
		'dVal'                : msg['StaticText']['dValLP'],
		'dmaxVal'             : msg['StaticText']['dmaxValLP'], 
		'Results'             : msg['StaticText']['ResultsLP'],		
		'SeqLength'		      : msg['StaticText']['SeqLength_LP']
	},
	name['TarProt'] : { # Targeted Proteolysis module. Other tooltips are set in WinModule below
		'DataFile'            : msg['Button']['DataFile'],
		'OutputFolderDataFile': msg['Button']['OutputFolderDataFile'],
		'Results'             : msg['StaticText']['Results'],
		'ResultsW'            : msg['Button']['ResultsW'],
		'ResultsL'            : msg['Button']['ResultsL'],			
	},
	name['CorrA'] : { # Correlation Analysis Util
		'DataFile'          : msg['Button']['DataFile'],
		'OutputFileDataFile': msg['Button']['OutputFileDataFile'],
		'AddCol'            : msg['Button']['AddColCorrA'],
		'ValueFieldTooltip' : msg['StaticText']['DataNorm'],
		'CorrelationM'      : msg['StaticText']['CorrelationM']
	},
	name['AAdist'] : { # AA Distribution Util
		'TarProtFile'          : msg['Button']['TarProtFile'],
		'OutputFileTarProtFile': msg['Button']['OutputFileTarProtFile'],
		'ValueFieldTooltip'    : msg['StaticText']['Positions2'],
	},
	name['Histo'] : { # Histogram Util
		'TarProtFile'          : msg['Button']['TarProtFile'],
		'OutputFileTarProtFile': msg['Button']['OutputFileTarProtFile'],
		'ValueFieldTooltip'    : msg['StaticText']['HistWin2']
	},
	name['SeqH']: { # Sequence Highlight Util
		'LimProtFile'       : msg['Button']['LimProtFile'],
		'OutputFile'        : msg['Button']['OutputFileLimProtFile'],
		'ValueFieldTooltip' : msg['StaticText']['SeqLength_LP']
	},
	name['SeqAlign'] : { # Sequence Aligments Util
		'TarProtFile'            : msg['Button']['TarProtFile'],
		'OutputFolderTarProtFile': msg['Button']['OutputFolderTarProtFile'],
		'ValueFieldTooltip'      : msg['StaticText']['SeqLength']
	},
	name['ShortDFile'] : { # Short Data File Util
		'UMSAPMFile'             : msg['Button']['UMSAPMFile'],
		'OutputFolderUMSAPFile': msg['Button']['OutputFolderUMSAPFile'],
		'DataFile'               : msg['Button']['DataFile2'],
		'ValueFieldTooltip'      : msg['StaticText']['ColExt'],
	},
	name['Cuts2PDB'] : { # Cleavages to PDB Util
		'TarProtFile'            : msg['Button']['TarProtFile'],
		'OutputFolderTarProtFile': msg['Button']['OutputFolderTarProtFile'],
		'PDBFile'                : msg['Button']['PDBFile'],
		'ValueFieldTooltip'      : msg['StaticText']['PDBID'],
	},
	name['MergeAA'] : { # Merge aadist Files Util
		'aadistFile'  : msg['Button']['aadistFile'],
		'OutputFileB' : msg['Button']['OutputFile'],
		'OutputFileT' : msg['StaticText']['OutputFile']
	},
	name['TypeRes'] : { # TypeRes window
		'Cancel': msg['Button']['Cancel'], 
		'Ok'    : msg['Button']['Ok'],
		'Create': msg['Button']['Create'],
		name['TarProt'] : {
			'Experiments' : msg['StaticText']['Experiments'],
		},
		name['LimProt'] : {
			'Bands' : msg['StaticText']['Bands'],
			'Lanes' : msg['StaticText']['Lanes'],
		},
		name['ProtProf'] : {
			'Conditions'  : msg['StaticText']['Conditions'],
			'ConditionsNu': msg['StaticText']['ConditionsNu'],
			'ConditionsNa': msg['StaticText']['ConditionsNa'],
			'RP'          : msg['StaticText']['RP'],
			'RPNu'        : msg['StaticText']['RPNu'],
			'RPNa'        : msg['StaticText']['RPNa'],
			'ControlType' : msg['StaticText']['ControlType'],
			'ControlNa'   : msg['StaticText']['ControlNa'],
			'Control'     : msg['StaticText']['Control'],
		},
	},
	name['Preference'] : { # Preference window
		'Save' : msg['Button']['SavePref'],
		'Cancel': msg['Button']['CancelPref'],
		'Load' : msg['Button']['LoadDef'],
	},
	'WinModule' : { # Tooltips for gclasses.WinModule class
		'SeqRec'   : msg['Button']['SeqRec'],
		'SeqNat'   : msg['Button']['SeqNat'],
		'PDBFile'  : msg['Button']['PDBFile'],
		'OutName'  : msg['Button']['OutName'],
		'TarProt'  : msg['StaticText']['TarProt'],
		'ScoreVal' : msg['StaticText']['ScoreVal'],
		'DataNorm' : msg['StaticText']['DataNorm'],
		'aVal'     : msg['StaticText']['aVal'],
		'Sequence' : msg['StaticText']['Sequence'],
		'DetProt'  : msg['StaticText']['DetProt'],
		'Score'    : msg['StaticText']['Score'],
		'ColExt'   : msg['StaticText']['ColExt'],
		'Positions': msg['StaticText']['Positions'],
		'SeqLength': msg['StaticText']['SeqLength'],
		'HistWin'  : msg['StaticText']['HistWin'],
		'PDBID'    : msg['StaticText']['PDBID']
	},
	'HelpRun' : { # Tooltips for the gclasses.ElementHelpRun class
		'Run' : msg['Button']['Run'],
		'Help': msg['Button']['Help']
	},
	'Clear' : { # Tooltips for the gclasses.ElementClearAFVC
		'All'   : msg['Button']['All'],
		'Files' : msg['Button']['Files'],
		'Values': msg['Button']['Values'],
		'Cols'  : msg['Button']['Cols']
	},
}
#endregion ---------------------------------------------------------- Tooltips

#region ----------------------------------------------------------- Menu items
addColumnsTo = {
	name['TarProt'] : ['Sequences', 'Detected proteins', 'Score', 
			'Columns to extract'],
	name['LimProt'] : ['Sequences', 'Detected proteins', 'Score', 
			'Columns to extract'],
	name['ProtProf'] : ['Detected proteins', 'Gene names', 'Score', 
			'Exclude proteins', 'Columns to extract'],
}

modules = {
	1: 'Limited Proteolysis',
	2: 'Proteome Profiling',
	3: 'Targeted Proteolysis',
}
#endregion -------------------------------------------------------- Menu items

#-------------------------------------------------------- GUI dictionaries
#--- The name of the dict is the class where the dict is used or
#--- the GUI element for which the dict is intended to be used 

dictElemHelpRun = { # Label for the help run buttons
	'Help' : 'Help',
	'Run'  : 'Start analysis',
}

#region --------------------------------------------------------- File section
dictWinUtilUno = { # Label for the text control in the values section (aadist util)
	name['AAdist'] : {
		'StaticLabel' : 'Positions'
	},
	name['Histo'] : {
		'StaticLabel' : 'Windows'
	},
	name['SeqAlign'] : {
		'StaticLabel' : 'Sequence length'
	},
	name['SeqH'] : {
		'StaticLabel' : 'Sequence length'
	},	
	name['CorrA'] : {
		'StaticLabel' : 'Data normalization'
	},
	name['ShortDFile'] : {
		'StaticLabel' : 'Columns to extract'	
	},
	name['Cuts2PDB'] : {
		'StaticLabel' : 'PDB ID'	
	},
}

dictElemDataFile = { # To create a data file element in the File section 
	name['TypeRes'] : {
		'MsgOpenFile': msg['Open']['DataFile'],
		'ExtLong'    : extLong['Data'],
		'ExtShort'   : extShort['Data'],
	},
	name['ProtProf'] : {
		'ButtonLabel'        : 'Data file',
		'ButtonTooltip'      : tooltip[name['ProtProf']]['DataFile'], 
		'BindEnter'          : True, 
		'MsgOpenFile'        : msg['Open']['DataFile'],
		'ExtLong'            : extLong['Data'], 
		'FillListCtrl'       : True, 
		'ExtShort'           : extShort['Data'], 
		'EmptySecondListCtrl': False		
	},
	name['LimProt'] : {
		'ButtonLabel'        : 'Data file',
		'ButtonTooltip'      : tooltip[name['LimProt']]['DataFile'], 
		'BindEnter'          : True, 
		'MsgOpenFile'        : msg['Open']['DataFile'],
		'ExtLong'            : extLong['Data'], 
		'FillListCtrl'       : True, 
		'ExtShort'           : extShort['Data'], 
		'EmptySecondListCtrl': False		
	},
	name['TarProt'] : {
		'ButtonLabel'        : 'Data file',
		'ButtonTooltip'      : tooltip[name['TarProt']]['DataFile'], 
		'BindEnter'          : True, 
		'MsgOpenFile'        : msg['Open']['DataFile'],
		'ExtLong'            : extLong['Data'], 
		'FillListCtrl'       : True, 
		'ExtShort'           : extShort['Data'], 
		'EmptySecondListCtrl': False
	},
	name['CorrA'] : {  
		'ButtonLabel'        :	'Data file', 
		'ButtonTooltip'      :	tooltip[name['CorrA']]['DataFile'], 
		'BindEnter'          :	True, 
		'MsgOpenFile'        :	msg['Open']['DataFile'],
		'ExtLong'            :	extLong['Data'], 
		'FillListCtrl'       :	True, 
		'ExtShort'           :	extShort['Data'], 
		'EmptySecondListCtrl':	True
	},
	name['AAdist'] : {
		'ButtonLabel'        : 'Tarprot file', 
		'ButtonTooltip'      : tooltip[name['AAdist']]['TarProtFile'], 
		'BindEnter'          : False, 
		'MsgOpenFile'        : msg['Open']['TarProtFile'], 
		'ExtLong'            : extLong['TarProt'], 
		'FillListCtrl'       : False, 
		'ExtShort'           : extShort['TarProt'], 
		'EmptySecondListCtrl': False
	},
	name['Histo'] : {
		'ButtonLabel'        : 'Tarprot file',
		'ButtonTooltip'      : tooltip[name['Histo']]['TarProtFile'], 
		'BindEnter'          : False, 
		'MsgOpenFile'        : msg['Open']['TarProtFile'], 
		'ExtLong'            : extLong['TarProt'], 
		'FillListCtrl'       : False, 
		'ExtShort'           : extShort['TarProt'], 
		'EmptySecondListCtrl': False
	},
	name['SeqH'] : {
		'ButtonLabel'        : 'LimProt file',
		'ButtonTooltip'      : tooltip[name['SeqH']]['LimProtFile'], 
		'BindEnter'          : False, 
		'MsgOpenFile'        : msg['Open']['LimProtFile'],
		'ExtLong'            : extLong['LimProt'], 
		'FillListCtrl'       : False, 
		'ExtShort'           : extShort['LimProt'], 
		'EmptySecondListCtrl': False		
	},	
	name['SeqAlign'] : {
		'ButtonLabel'        : 'Tarprot file', 
		'ButtonTooltip'      : tooltip[name['SeqAlign']]['TarProtFile'], 
		'BindEnter'          : False,
		'MsgOpenFile'        : msg['Open']['TarProtFile'], 
		'ExtLong'            : extLong['TarProt'], 
		'FillListCtrl'       : False, 
		'ExtShort'           : extShort['TarProt'], 
		'EmptySecondListCtrl': False
	},
	name['ShortDFile'] : {
		'ButtonLabel'        : 'UMSAP file', 
		'ButtonTooltip'      : tooltip[name['ShortDFile']]['UMSAPMFile'], 
		'BindEnter'          : False,
		'MsgOpenFile'        : msg['Open']['UMSAPMFile'], 
		'ExtLong'            : extLong['UmsapM'], 
		'FillListCtrl'       : False, 
		'ExtShort'           : extShort['UmsapM'], 
		'EmptySecondListCtrl': False		
	},
	name['Cuts2PDB'] : {
		'ButtonLabel'        : 'Tarprot file', 
		'ButtonTooltip'      : tooltip[name['Cuts2PDB']]['TarProtFile'], 
		'BindEnter'          : False,
		'MsgOpenFile'        : msg['Open']['TarProtFile'], 
		'ExtLong'            : extLong['TarProt'], 
		'FillListCtrl'       : False, 
		'ExtShort'           : extShort['TarProt'], 
		'EmptySecondListCtrl': False		
	},
}

dictElemDataFile2 = { # To create a second data file element in the File section
	name['ShortDFile'] : {
		'MsgOpenFile' : msg['Open']['DataFile'],
		'ExtLong'     : extLong['Data'],
		'ExtShort'    : extShort['Data'],
		'NA'          : True		
	},
	name['Cuts2PDB'] : {
		'MsgOpenFile' : msg['Open']['PDBFile'],
		'ExtLong'     : extLong['PDB'],
		'ExtShort'    : extShort['PDB'],
		'NA'          : True		
	},
	name['MergeAA'] : {
		'MsgOpenFile' : msg['Open']['AAdistFile'],
		'ExtLong'     : extLong['AAdist']
	},
	name['ProtProf'] : {
		'MsgOpenFile' : msg['Open']['ResultLFile'],
		'ExtLong'     : extLong['Data']		
	},
	name['TarProt'] : {
		'MsgOpenFile' : msg['Open']['ResultLFile'],
		'ExtLong'     : extLong['Data']		
	},
	name['LimProt'] : {
		'MsgOpenFile' : msg['Open']['ResultLFile'],
		'ExtLong'     : extLong['Data']		
	},							
}

dictElemSeqRec = { # To create a Recombinant sequence element in the File section
	name['TarProt'] : {
		'ButtonLabel': 'Sequence (Rec)', 
		'ExtShort'   : extShort['Seq'], 
		'NA'         : False
	},
	name['LimProt'] : {
		'ButtonLabel': 'Sequence (Rec)', 
		'ExtShort'   : extShort['Seq'], 
		'NA'         : False
	},
}

dictElemSeqNat = { # To create a Native sequence element in the File section
	name['TarProt'] : {
		'ButtonLabel': 'Sequence (Nat)', 
		'ExtShort'   : extShort['Seq'], 
		'NA'         : True
	},
	name['LimProt'] : {
		'ButtonLabel': 'Sequence (Nat)', 
		'ExtShort'   : extShort['Seq'], 
		'NA'         : True
	},	
}

dictElemPdbFile = { # To create a PDB file element in the File section
	name['TarProt'] : {
		'ButtonLabel': 'PDB file', 
		'ExtShort'   : extShort['PDB'], 
		'NA'         : True
	},
	name['LimProt'] : {
		'ButtonLabel': 'PDB file', 
		'ExtShort'   : extShort['PDB'], 
		'NA'         : True
	},			
}

dictElemOutputFileFolder = { # To create an Output file/folder element in the File section
	name['ProtProf'] : {
		'ButtonLabel'  : 'Output folder', 
		'ButtonTooltip': tooltip[name['ProtProf']]['OutputFolderDataFile'], 
		'FolderOrFile' : True, 
		'ExtLong'      : None,
		'ExtShort'     : None,
		'DefNameFolder': 'ProtProf',
		'DefNameFile'  : 'protprof',
		'NA'           : True
	},
	name['LimProt'] : {
		'ButtonLabel'  : 'Output folder', 
		'ButtonTooltip': tooltip[name['LimProt']]['OutputFolderDataFile'], 
		'FolderOrFile' : True, 
		'ExtLong'      : None,
		'ExtShort'     : None,
		'DefNameFolder': 'LimProt',
		'DefNameFile'  : 'limprot',
		'NA'           : True
	},
	name['TarProt'] : {
		'ButtonLabel'  : 'Output folder', 
		'ButtonTooltip': tooltip[name['TarProt']]['OutputFolderDataFile'], 
		'FolderOrFile' : True, 
		'ExtLong'      : None,
		'ExtShort'     : None,
		'DefNameFolder': 'TarProt',
		'DefNameFile'  : 'tarprot',
		'NA'           : True
	},
	name['SeqH'] : {
		'ButtonLabel'  : 'Output file',
		'ButtonTooltip': tooltip[name['SeqH']]['OutputFile'], 
		'FolderOrFile' : False, 
		'ExtLong'      : extLong['PDF'], 
		'ExtShort'     : extShort['PDF'],
		'DefNameFile'  : 'seqH.seq.pdf',
		'NA'           : True
	},	
	name['SeqAlign'] : {
		'ButtonLabel'  : 'Output folder',
		'ButtonTooltip': tooltip[name['SeqAlign']]['OutputFolderTarProtFile'], 
		'FolderOrFile' : True, 
		'ExtLong'      : extLong['Data'], 
		'ExtShort'     : extShort['Data'],
		'DefNameFolder': 'Sequences',
		'NA'           : True
	},
	name['ShortDFile'] : {
		'ButtonLabel'  : 'Output folder',
		'ButtonTooltip': tooltip[name['ShortDFile']]['OutputFolderUMSAPFile'], 
		'FolderOrFile' : True, 
		'ExtLong'      : extLong['Data'], 
		'ExtShort'     : extShort['Data'],
		'DefNameFolder': 'Data',
		'DefNameFile'  : 'short_data_file',
		'NA'           : True
	},
	name['Cuts2PDB'] : {
		'ButtonLabel'  : 'Output folder',
		'ButtonTooltip': tooltip[name['Cuts2PDB']]['OutputFolderTarProtFile'], 
		'FolderOrFile' : True, 
		'ExtLong'      : extLong['Data'], 
		'ExtShort'     : extShort['Data'],
		'DefNameFolder': 'PDB',
		'NA'           : True
	},	
	name['Histo']    : {
		'ButtonLabel'  : 'Output file', 
		'ButtonTooltip': tooltip[name['Histo']]['OutputFileTarProtFile'], 
		'FolderOrFile' : False, 
		'ExtLong'      : extLong['Histo'], 
		'ExtShort'     : extShort['Histo'],
		'DefNameFile'  : 'histo.hist',
		'NA'           : True
	},
	name['AAdist']   : {
		'ButtonLabel'  : 'Output file', 
		'ButtonTooltip': tooltip[name['AAdist']]['OutputFileTarProtFile'], 
		'FolderOrFile' : False, 
		'ExtLong'      : extLong['AAdist'], 
		'ExtShort'     : extShort['AAdist'],
		'DefNameFile'  : 'aadist.aadist',
		'NA'           : True
	},
	name['CorrA']    : {
		'ButtonLabel'  : 'Output file', 
		'ButtonTooltip': tooltip[name['CorrA']]['OutputFileDataFile'], 
		'FolderOrFile' : False,
		'ExtLong'      : extLong['CorrA'], 
		'ExtShort'     : extShort['CorrA'],
		'DefNameFolder': None,
		'DefNameFile'  : 'corrA.corr',
		'NA'           : True
	},
	name['MergeAA'] : {
		'DefNameFile'  : 'aadist.aadist',
		'ExtLong'      : extLong['AAdist'],
		'ExtShort'     : extShort['AAdist'],
		'NA'           : False
	},
}
#endregion ------------------------------------------------------ File section

#region ------------------------------------------------------- Values Section
dictElemChar = { # To check the user input in a Character element in the Values section
	name['ProtProf'] : {
		'DefNameFile'  : None
	}
}

dictElemSeqLength = { # To check user input in a Sequence Length element in the Values section
	name['TarProt'] : {
		't'   : 'int',
		'comp': 'gt',
		'NA'  : True
	},
	name['SeqAlign'] : {
		't'   : 'int',
		'comp': 'gt',
		'NA'  : False
	},	
	name['LimProt'] : {
		't'   : 'int',
		'comp': 'gt',
		'NA'  : True
	},	
	name['SeqH'] : {
		't'   : 'int',
		'comp': 'gt',
		'NA'  : False
	},						
}

dictElemPositions = { # To check user input in a Positions element in the Values section
	name['TarProt'] : {
		't'   : 'int',
		'comp': 'gt',
		'NA'  : True
	},
	name['AAdist'] : {
		't'   : 'int',
		'comp': 'gt',
		'NA'  : False
	},
}

dictElemHistWin = { # To check user input in a Histogram windos element in the Values section
	name['TarProt'] : {
		't'        : 'int',
		'comp'     : 'egt',
		'val'      : 0,
		'NA'       : True,
		'Order'    : True,
		'Range'    : False,
		'Unique'   : True,
		'DelRepeat': True
	},
	name['Histo'] : {
		't'        : 'int',
		'comp'     : 'egt',
		'val'      : 0,
		'NA'       : False,
		'Order'    : True,
		'Range'    : False,
		'Unique'   : True,
		'DelRepeat': True
	}
}
#endregion ---------------------------------------------------- Values Section

#region ------------------------------------------------------ Columns Section
dictElemSeqCol = { # To check user input in Sequence Col element in the Columns section
	name['TarProt'] : {
		't'   : 'int',
		'comp': 'egt',
		'NA'  : False,
		'val' : 0
	},
	name['LimProt'] : {
		't'   : 'int',
		'comp': 'egt',
		'NA'  : False,
		'val' : 0
	},	
}

dictElemDetectProtCol = { # To check user input in Detected Protein Col in the Columns section
	name['TarProt'] : {
		't'   : 'int',
		'comp': 'egt',
		'NA'  : False,
		'val' : 0
	},
	name['LimProt'] : {
		't'   : 'int',
		'comp': 'egt',
		'NA'  : False,
		'val' : 0
	},	
	name['ProtProf'] : {
		't'   : 'int',
		'comp': 'egt',
		'NA'  : False,
		'val' : 0
	},
}

dictElemScoreCol = { # To check user input in a Score Col in the Columns section
	name['TarProt'] : {
		't'   : 'int',
		'comp': 'egt',
		'NA'  : False,
		'val' : 0
	},
	name['LimProt'] : {
		't'   : 'int',
		'comp': 'egt',
		'NA'  : False,
		'val' : 0
	},	
	name['ProtProf'] : {
		't'   : 'int',
		'comp': 'egt',
		'NA'  : False,
		'val' : 0
	},	
}

dictElemGeneNCol = { # To check user input in a Gene names Col in the Columns section
	name['ProtProf'] : {
		't'   : 'int',
		'comp': 'egt',
		'NA'  : False,
		'val' : 0
	},
}

dictElemColExtract = { # To check user input in a Columns to Extract Col in the Columns section
	name['TarProt'] : {
		't'        : 'int',
		'comp'     : 'egt',
		'val'      : 0,
		'NA'       : True,
		'Order'    : False,
		'Range'    : True,
		'Unique'   : False,
		'DelRepeat': False
	},
	name['LimProt'] : {
		't'        : 'int',
		'comp'     : 'egt',
		'val'      : 0,
		'NA'       : True,
		'Order'    : False,
		'Range'    : True,
		'Unique'   : False,
		'DelRepeat': False
	},	
	name['ProtProf'] : {
		't'        : 'int',
		'comp'     : 'egt',
		'val'      : 0,
		'NA'       : True,
		'Order'    : False,
		'Range'    : True,
		'Unique'   : False,
		'DelRepeat': False
	},	
	name['ShortDFile'] : {
		't'        : 'int',
		'comp'     : 'egt',
		'val'      : 0,
		'NA'       : False,
		'Order'    : False,
		'Range'    : True,
		'Unique'   : False,
		'DelRepeat': False
	},
}

dictElemExclude = { # To check user input in a Exclude proteins Col in the Columns section
	name['ProtProf'] : {
		't'        : 'int',
		'comp'     : 'egt',
		'val'      : 0,
		'NA'       : True,
		'Order'    : False,
		'Range'    : True,
		'Unique'   : True,
		'DelRepeat': False
	},
}

dictElemControl = { # To check user input in a Control Col in the Columns section
	name['TarProt'] : {
		't'        : 'int',
		'comp'     : 'egt',
		'val'      : 0,
		'NA'       : False,
		'Order'    : False,
		'Range'    : True,
		'Unique'   : True,
		'DelRepeat': True
	},
	name['LimProt'] : {
		't'        : 'int',
		'comp'     : 'egt',
		'val'      : 0,
		'NA'       : False,
		'Order'    : False,
		'Range'    : True,
		'Unique'   : True,
		'DelRepeat': True
	},	
}

dictElemResultsTP = { # To check the user input in a Results Col in the Columns section
	name['TarProt'] : {
		't'         : 'int',
		'comp'      : 'egt',
		'val'       : 0,
		'NA'        : False,
		'Order'     : False,
		'Range'     : True,
		'Unique'    : True,
		'DelRepeat' : False,
		'Replicates': False,
	},
	name['ProtProf'] : {
		't'         : 'int',
		'comp'      : 'egt',
		'val'       : 0,
		'NA'        : True,
		'Order'     : False,
		'Range'     : True,
		'Unique'    : True,
		'DelRepeat' : False,
		'Replicates': True,
	},
	name['LimProt'] : {
		't'         : 'int',
		'comp'      : 'egt',
		'val'       : 0,
		'NA'        : True,
		'Order'     : False,
		'Range'     : True,
		'Unique'    : True,
		'DelRepeat' : False,
		'Replicates': False,
	},			
}

dictElemRowsCols = { # To check rows and cols input in TypeRes window
	'Rows' : {
		't'   : 'int',
		'comp': 'egt',
		'NA'  : False
	},	
	'Cols' : {
		't'   : 'int',
		'comp': 'egt',
		'NA'  : False
	},		
}

dictCheckFatalErrorMsg = { ####----> Fatal error messages
	name['TypeRes'] : {
		'DataFile' : msg['Errors']['Datafile2'],
		'RowCol'   : msg['Errors']['TyepResRowCol'],
		'NoExport' : msg['Errors']['NoExport'],	
	},	
	name['CorrA'] : {
		'Datafile'          : msg['Errors']['Datafile'],
		'OutputFile'        : msg['Errors']['OutputFile'],
		'ListCtrlRightEmpty': msg['Errors']['ListCtrlRightEmpty'],
		'NoFloatInColumns'  : msg['Errors']['NoFloatInColumns']
	},
	name['CorrObj'] : {
		'CorrFileFormat' : msg['Errors']['CorrFileFormat']
	},
	name['DataObj'] : {
		'BadCsvFile'      : msg['Errors']['BadCsvFile']
	},
	name['ProtProf'] : {
		'Datafile'        : msg['Errors']['Datafile'],
		'Outputfolder'    : msg['Errors']['Outputfolder'],
		'Outputname'      : msg['Errors']['Outputname'],
		'Scorevalue'      : msg['Errors']['Scorevalue'],
		'DetectProtCol'   : msg['Errors']['DetectProtCol'],
		'GeneNCol'        : msg['Errors']['GeneNCol'],
		'ScoreCol'        : msg['Errors']['ScoreCol'],
		'ExcludeCol'      : msg['Errors']['ExcludeCol'],
		'ColExtract'      : msg['Errors']['ColExtract'],
		'Results'         : msg['Errors']['ResultsPP'],	
		'Unique'          : msg['Errors']['UniquePP'],
		'ColNumber'       : msg['Errors']['ColNumber'],
		'Character'       : msg['Errors']['Character'],
		'EqualNElem'      : msg['Errors']['EqualNElem'],
		'NTimeP'          : msg['Errors']['LTimeP_PP'],
		'ResMatrixShape'  : msg['Errors']['NTPperCond_PP'],
		'NCondsL'         : msg['Errors']['NConds_PP'],
		'NTimePL'         : msg['Errors']['NTimeP_PP'],
		'NoResults'       : msg['Errors']['NoResults_PP'],    			
	},
	name['ProtProfObj'] : {
		'FileFormat' : msg['Errors']['ProtProfFileFormat'],
		'Datafile'   : msg['Errors']['Datafile'],
	},
	name['LimProt'] : {
		'Datafile'        : msg['Errors']['Datafile'],
		'Seq_rec'         : msg['Errors']['Seq_rec'],
		'Seq_nat'         : msg['Errors']['Seq_nat'], 
		'PDBfile'         : msg['Errors']['PDBfile'],		
		'Outputfolder'    : msg['Errors']['Outputfolder'],
		'Outputname'      : msg['Errors']['Outputname'],
		'Targetprotein'   : msg['Errors']['Targetprotein'],
		'Scorevalue'      : msg['Errors']['Scorevalue'],
		'PDBID'           : msg['Errors']['PDBID'],
		'dmVal'           : msg['Errors']['dmVal'],
		'duVal'           : msg['Errors']['duVal'],
		'SeqCol'          : msg['Errors']['SeqCol'],
		'DetectProtCol'   : msg['Errors']['DetectProtCol'],
		'ScoreCol'        : msg['Errors']['ScoreCol'],
		'ColExtract'      : msg['Errors']['ColExtract'],	
		'Results'         : msg['Errors']['ResultsLP'],		
		'Unique'          : msg['Errors']['UniqueTP'],		
		'ColNumber'       : msg['Errors']['ColNumber'],
		'ResMatrixShape'  : msg['Errors']['NElemPLevel_LP'],
		'Sequencelength'  : msg['Errors']['Sequencelength2'],
		'NoPeptInRecSeq'  : msg['Errors']['NoPeptInRecSeq'],
	},	
	name['LimProtRes'] : {
		'FiltPept2'      : msg['Errors']['FiltPept2LP'],
		'FileFormatSort' : msg['Errors']['LimProtFileFormat'],
	},		
	name['LimProtObj'] : {
		'FileFormat'     : msg['Errors']['LimProtFileFormat'],
		'FiltPept2'      : msg['Errors']['FiltPept2LP'],
		'FileFormatSort' : msg['Errors']['LimProtFileFormat'],
		'Datafile'       : msg['Errors']['Datafile'],
	},
	name['TarProt'] : {
		'Datafile'        : msg['Errors']['Datafile'],
		'Seq_rec'         : msg['Errors']['Seq_rec'],
		'Seq_nat'         : msg['Errors']['Seq_nat'], 
		'PDBfile'         : msg['Errors']['PDBfile'],
		'Outputfolder'    : msg['Errors']['Outputfolder'],
		'Outputname'      : msg['Errors']['Outputname'],
		'Targetprotein'   : msg['Errors']['Targetprotein'],
		'Scorevalue'      : msg['Errors']['Scorevalue'],
		'Positions'       : msg['Errors']['Positions'],
		'Sequencelength'  : msg['Errors']['Sequencelength'],
		'Histogramwindows': msg['Errors']['Histogramwindows'],
		'PDBID'           : msg['Errors']['PDBID'],
		'SeqCol'          : msg['Errors']['SeqCol'],
		'DetectProtCol'   : msg['Errors']['DetectProtCol'],
		'ScoreCol'        : msg['Errors']['ScoreCol'],
		'ColExtract'      : msg['Errors']['ColExtract'],
		'Results'         : msg['Errors']['Results'],		
		'chainSInFile'    : msg['Errors']['chainSInFile'],
		'NoPeptInRecSeq'  : msg['Errors']['NoPeptInRecSeq'],
		'Unique'          : msg['Errors']['UniqueTP'],
		'ColNumber'       : msg['Errors']['ColNumber'],
		'NoFloatInColumns': msg['Errors']['NoFloatInColumns'],
	},
	name['TarProtObj'] : {
		'TarProtFileFormat': msg['Errors']['TarProtFileFormat'], 
		'Datafile'         : msg['Errors']['Datafile'],
		'FiltPept2'        : msg['Errors']['FiltPept2'],
		'NoNatSeq'         : msg['Errors']['NoNatSeq']
	},
	name['TarProtRes'] : {
		'FiltPept2'      : msg['Errors']['FiltPept2'],
		'FileFormatSort' : msg['Errors']['TarProtFileFormat']
	},
	name['CutPropObj'] : {
		'CutPropFileFormat' : msg['Errors']['CutPropFileFormat']	
	},
	name['Histo'] : {
		'TarProtFile'      : msg['Errors']['TarProtFile'],
		'OutputFile'       : msg['Errors']['OutputFile'],
		'Histogramwindows2': msg['Errors']['Histogramwindows2'],
		'FiltPept2'        : msg['Errors']['FiltPept2'] 
	},
	name['SeqH'] : {
		'LimProtFile'    : msg['Errors']['LimProtFile'],
		'OutputFile'     : msg['Errors']['OutputFile'],
		'Sequencelength' : msg['Errors']['Sequencelength2'],
		'FiltPept2'      : msg['Errors']['FiltPept2LP'] 
	},
	name['SeqAlign'] : {
		'TarProtFile'    : msg['Errors']['TarProtFile'],
		'Outputfolder'   : msg['Errors']['Outputfolder'],
		'Sequencelength' : msg['Errors']['Sequencelength2'],
		'FiltPept2'      : msg['Errors']['FiltPept2'] 
	},
	name['SeqObj'] : {
		'NoSeq'     : msg['Errors']['NoSeq'],
		'NoAlign'   : msg['Errors']['NoAlign'],
		'NoOverlap' : msg['Errors']['NoOverlap']
	},
	name['HistoObj'] : {
		'HistoFileFormat' : msg['Errors']['HistoFileFormat']
	},
	name['AAdistObj'] : {
		'AAdistFileFormat' : msg['Errors']['AAdistFileFormat']
	},
	name['AAdist'] : {
		'TarProtFile': msg['Errors']['TarProtFile'],
		'OutputFile' : msg['Errors']['OutputFile'],
		'Positions2' : msg['Errors']['Positions2'],
		'FiltPept2'  : msg['Errors']['FiltPept2'] 
	},
	name['MergeAA'] : {
		'NoAAdistFiles' : msg['Errors']['NoAAdistFiles'],
		'OutputFile'    : msg['Errors']['OutputFile']
	},
	name['ShortDFile'] : {
		'TarProtFile' : msg['Errors']['TarProtFile'],
		'DataFile'    : msg['Errors']['Datafile'],
		'Outputfolder': msg['Errors']['Outputfolder'],
		'Outputfile'  : msg['Errors']['OutputFile'],
		'ColExtract'  : msg['Errors']['ColExtract2'],
		'FiltPept2'   : msg['Errors']['FiltPept2'],
		'UMSAPFile'   : msg['Errors']['UMSAPFile'],
	},
	name['Cuts2PDB'] : {
		'TarProtFile' : msg['Errors']['TarProtFile'],
		'PDBfile2'    : msg['Errors']['PDBfile2'],
		'Outputfolder': msg['Errors']['Outputfolder'],
		'PDBID2'      : msg['Errors']['PDBID2'],
		'FiltPept2'   : msg['Errors']['FiltPept2'],
		'chainSInFile': msg['Errors']['chainSInFile']
	},
	name['ScriptObj'] : {
		'NoModule'     : msg['Errors']['UscrFileNoModule'],
		'UnknownModule': msg['Errors']['UscrFileUnknownModule'],
		'NoKeywords'   : msg['Errors']['UscrFileNoKeywords']
	},
	name['Preference']: {
		'Save' : msg['Errors']['ConfigUserFile'],
		'Load' : msg['Errors']['ConfigDefFile'],
	},
	name['UpdateNotice'] : {
		'UMSAPSite' : msg['Errors']['UMSAPSite'],
	},	
}
#endregion --------------------------------------------------- Columns Section

#-------------------------------------------------------- GUI dictionaries (END)

#region ---------------------------------------------------------- Translation
dictComparisonToText = { # Comparison translation
	'gt' : 'greater than',
	'egt': 'equal or greater than',
	'e'  : 'equal than',
	'elt': 'equal or less than',
	'lt' : 'less than'
}

dictNumTypeToText = { # Type translation
	'float': 'a decimal',
	'int'  : 'an integer',
}

dictUserLoadRes = { # To translate the options in the txt file with the results
	name['ProtProf'] : {
		'CType'       : 'Control type',
		'LabelControl': 'Control name',
		'LabelCond'   : 'Condition names',
		'LabelRP'     : 'Relevant point names',
	}
}

dictUserInput2UscrFile = { # Equivalence between the uscr file and the self.do dict
	name['TarProt'] : {
		"Datafile"        : 'Data file',
		"Seq_rec"         : 'Sequence (rec)',
		"Seq_nat"         : 'Sequence (nat)',
		"PDBfile"         : 'PDB file',
		"Outputfolder"    : 'Output folder',
		"Outputname"      : 'Output name',
		"Targetprotein"   : 'Target protein',
		"Scorevalue"      : 'Score value',
		"Datanorm"        : 'Data normalization',
		"aVal"            : 'a-value',
		"Positions"       : 'Positions',
		"Sequencelength"  : 'Sequence length',
		"Histogramwindows": 'Histogram windows',
		"PDBID"           : 'PDB ID',
		"SeqCol"          : 'Sequence',
		"DetectProtCol"   : 'Detected proteins',
		"ScoreCol"        : 'Score',
		"ColExtract"      : 'Columns to extract',
		"Results"         : 'Results',
		"Module"          : 'Module'
	},
	name['ProtProf'] : {
		'Datafile'       : 'Data file',
		'Outputfolder'   : 'Output folder',
		'Outputname'     : 'Output name',
		'Scorevalue'     : 'Score value',
		'Datanorm'       : 'Data normalization',
		'median'         : 'Median correction',
		'CorrP'          : 'P correction',
		'DetectProtCol'  : 'Detected proteins',
		'GeneNCol'       : 'Gene names',
		'ScoreCol'       : 'Score',
		'ExcludeCol'     : 'Exclude proteins',
		'ColExtract'     : 'Columns to extract',
		'Results'        : 'Results',
		'CType'          : 'Control Type',   
		'LabelControl'   : 'Control Label', 
		'LabelCond'      : 'Conditions', 
		'LabelRP'        : 'Relevant Points',
		'Module'         : 'Module'
	},
	name['LimProt'] : {
		'Datafile'      : 'Data file',
		"Seq_rec"       : 'Sequence (rec)',
		"Seq_nat"       : 'Sequence (nat)',
		"Outputfolder"  : 'Output folder',
		"Outputname"    : 'Output name',
		"Targetprotein" : 'Target protein',
		"Scorevalue"    : 'Score value',
		"Datanorm"      : 'Data normalization',
		"Sequencelength": 'Sequence length',
		"aVal"          : 'a-value',
		"bVal"          : 'b-value',
		"yVal"          : 'y-value',
		"duVal"         : 'd-value',
		"dmVal"         : 'dm-value',
		"SeqCol"        : 'Sequence',
		"DetectProtCol" : 'Detected proteins',
		"ScoreCol"      : 'Score',
		"ColExtract"    : 'Columns to extract',
		"Results"       : 'Results',
		"Module"        : 'Module'
	},      
}

dictAA3toAA1 = { # Three to one AA code translation
	'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D', 
	'CYS': 'C', 'GLU': 'E', 'GLN': 'Q', 'GLY': 'G',
	'HIS': 'H', 'ILE': 'I', 'LEU': 'L', 'LYS': 'K', 
	'MET': 'M', 'PHE': 'F', 'PRO': 'P', 'SER': 'S', 
	'THR': 'T', 'TRP': 'W', 'TYR': 'Y', 'VAL': 'V',
}

dictCorrectP = { # Correct P value method name to statsmodels.stats.multitest.multipletests function option
    'Bonferroni'           : 'bonferroni',
    'Sidak'                : 'sidak',
    'Holm - Sidak'         : 'holm-sidak',
    'Holm'                 : 'holm',
    'Simes-Hochberg'       : 'simes-hochberg',
    'Hommel'               : 'hommel',
    'Benjamini - Hochberg' : 'fdr_bh',
    'Benjamini - Yekutieli': 'fdr_by',
}
#endregion ------------------------------------------------------- Translation

#region ---------------------------------------------------------- Coordinates
coord = { # Selected coordinates
	'TopLeft': topLeftCoord,
	'TopXY'  : topXY,
}
#endregion ------------------------------------------------------- Coordinates

#region ---------------------------------------------------------------- Lists
naVals = [ # Possible NA values
	'N', 'n', 'No', 'NO', 'NA', ''
]

aaList1 = [ # AA one letter codes
	'A', 'I', 'L', 'V', 'M', 'F', 'W', 'Y', 'R', 'K', 'D', 'E', 'C', 'Q',
	'H', 'S', 'T', 'N', 'G', 'P'
]

aaList3 = [ # AA three letter codes
	'ALA', 'ARG', 'ASN', 'ASP', 'CYS', 'GLU', 'GLN', 'GLY', 'HIS', 'ILE',
	'LEU', 'LYS', 'MET', 'PHE', 'PRO', 'SER', 'THR', 'TRP', 'TYR', 'VAL'
]

aaGroups = [ # AA groups
	['A', 'I', 'L', 'V', 'M'], 
	['F', 'W', 'Y'], 
	['R', 'K'], 
	['D', 'E'],
	['C', 'Q', 'H', 'S', 'T', 'N'], 
	['G', 'P']
]

winNoMinMainUtil = [ # List of windows that do not minimize Main when opening
	name['Preference'],
	name['UpdateNotice'],
	name['About'],
]
#endregion ------------------------------------------------------------- Lists

#region -------------------------------------------------------------- Strings
PDBformat = ("{:6s}{:5d} {:^4s}{:1s}{:3s} {:1s}{:4d}{:1s}   {:8.3f}{:8.3f}"
	"{:8.3f}{:6.2f}{:6.2f}      {:4s}{:2s}")
#endregion ----------------------------------------------------------- Strings

#region ------------------------------------------------------------ Variables
updateAvail = None # To hold the result of dmethods.VersionCompare
#endregion --------------------------------------------------------- Variables

#region --------- Fonts. Set from Umsap.py because it requires a wx.App object
font = {
}
#endregion ------ Fonts. Set from Umsap.py because it requires a wx.App object

#region ----------- Pointers. Fill in Umsap.py to avoid importing modules here
pointer = { # pointer to methods in different classes to avoid repeating if statements 
	'menu' : {
		'toolmenu' : {}, # Tool menus for main menubar
	},
	'dclasses' : { # pointer to methods in data.data_classes
		'DataObj' : {}, # Classes creating data file objects 
	},
	'dmethods' : {
		'fillListCtrl' : {}, # Methods to get information to fill a ListCtrl
	},
	'gmethods' : { # points to methods in gui.gui_methods module
		'LaunchUscr' : {}, # Launch uscr methods used by dclasses.DataObjScriptFile
		'WinCreate' : {}, # Methods to create a window
	},
}
#endregion -------- Pointers. Fill in Umsap.py to avoid importing modules here


# ------------------------------------------------------------------------------
# CONFIGURABLE PARAMETERS
# ------------------------------------------------------------------------------		


# These dicts are saved/load to/from the configuration file
# The values here are to start the app for the first time
# They must be a dict to save/load with json in/from the configuration file

#region -------------------------------------------- User configurable options
general = { # General options
	'checkUpdate' : 1 # 1 Check, 0 No check 
}

colors = { # Color definition
	'listctrlZebra': '#ffe6e6', # Alternating color for the listboxes
	'cursorColor'  : 'red',     # Cursor color in matplotlib 
	'Fragments'    : [ # Darker colors of the fragments and bands 
		'#a2836e', '#ffef96', '#92a8d1', '#b1cbbb', '#eea29a',
		'#b0aac0', '#f4a688', '#d9ecd0', '#b7d7e8', '#fbefcc'
	],
	'FragmentsLight' : [ # Lighter colors of the fragments and bands 
		'#ECE6E2', '#FFFCEA', '#E9EEF6', '#EFF5F1', '#FCECEB',
		'#EFEEF2', '#FDEDE7', '#F7FBF6', '#F1F7FA', '#FEFCF5'
	],
	name['CutPropRes'] : {
		'vline' : 'GREY'
	},
	name['HistoRes'] : {
		'FPBar' : '#BEBEBE',
		'EdgeC' : 'Black'
	},
	name['AAdistObj'] : {
		'ChiColor1' : 'Green',
		'ChiColor0' : 'Red',
		'ChiColor-' : 'Black',
	},
	name['AAdistR'] : {
		'BarEdge'   : 'Black',
		'BarColors' : { 
			'R': '#0099ff', 'K': '#0099ff', 'D': '#ff4d4d', 'W': '#FF51FD', 
			'E': '#ff4d4d', 'S': '#70db70', 'T': '#70db70', 'H': '#70db70', 
			'N': '#70db70', 'Q': '#70db70', 'C': '#FFFC00', 'G': '#FFFC00', 
			'P': '#FFFC00', 'A': '#BEBEBE', 'V': '#BEBEBE', 'I': '#BEBEBE', 
			'L': '#BEBEBE', 'M': '#BEBEBE', 'F': '#FF51FD', 'Y': '#FF51FD', 
		},
		'Xaa' : 'GREY',
		'FPBar' : '#BEBEBE',
	},
	name['TarProtRes'] : {
		'Nat'      : '#c94c4c',
		'Rec'      : 'GREY',
		'Lines'    : 'BLack',
		'FragLines': 'Black',
		'LBBorder' : 'BLUE'
	},
	name['LimProtRes'] : {
		'Nat'      : '#c94c4c',
		'Rec'      : 'GREY',
		'Lines'    : 'BLack',
		'FragLines': 'Black',
		'LBBorder' : 'BLUE',
		'GBBorder' : 'RED'
	},
	name['LimProtObj'] : {
		'RegColor' : (0, 0 ,0),
		'HColor'   : (255, 0, 0),
	},	
	name['ProtProfRes'] : {
		'Colors' : ['#3333ff', '#d3d3d3', '#ff3333'],
		'Green'  : '#00ff00', #6ac653',
		'Gray'   : '#d3d3d3'
	},
}

cursor = { # Cursor style
	'lineWidth': 1,
	'lineStyle': ':'
}

cutpropU = { # Options for the cleavages per residue plot
	'*Dist'    : 0.01,
	'Threshold': 3,
	'Char'     : '*',
	'CharColor': 'RED'
}
#endregion ----------------------------------------- User configurable options


# ------------------------------------------------------------------------------
# Methods
# ------------------------------------------------------------------------------		


def ConfigLoad(file):
	""" Load a configuration file. """
 #--> Global variables, so the dicts are updated with the user values saved in the configuration file 
	global general
 #--> Read the config file
	try:
		with open(file, 'r') as fileO:
			data = json.load(fileO)
		k = True
	except Exception:
		k = False
 #--> Assing values in file to variables and Return
	if k:
		general = data['general']
		return True
	else:
		return False
#---

def ConfigSave():
	""" Save the configuration file. """
 #--> Variables into data
	data = {}
	data['general']  = general
 #--> Write to file
	try:
		with open(file['Config'], 'w') as fileO:
			json.dump(data, fileO, indent=4)
		k = True
	except Exception:
		k = False
 #--> Return
	if k:
		return True
	else:
		return False	
#---

#--> Try to load user config, if file exists
try:
	ConfigLoad(file['Config'])
except Exception:
	pass
