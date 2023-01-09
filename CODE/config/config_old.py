# ------------------------------------------------------------------------------
# Copyright (C) 2017 Kenny Bravo Rodriguez <www.umsap.nl>
#
# Author: Kenny Bravo Rodriguez (kenny.bravorodriguez@mpi-dortmund.mpg.de)
#
# This program is distributed for free in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See the accompanying license for more details.
# ------------------------------------------------------------------------------


"""Configuration parameters of the app"""


#region -------------------------------------------------------------> Imports
import platform
from pathlib import Path
from typing  import Literal
#endregion ----------------------------------------------------------> Imports


#region -----------------------------------------> NON-CONFIGURABLE PARAMETERS
#region ---------------------------------------------------------------> Names
#------------------------------> Windows
nwProtProf  = 'ProtProfPlot'
#------------------------------> Dialogs
ndFilterRemoveAny = 'Remove Filters'
#endregion ------------------------------------------------------------> Names


#region ------------------------------------> Keywords for Menu - Method Links
#------------------------------> Tool Menu for Plot Window. General Items
kwToolExportDataFiltered = 'GeneralTool Export Filtered Data'
#------------------------------> Volcano Plot
kwToolVolPlot            = 'ToolVol Plot CRP'
kwToolVolPlotLabelPick   = 'ToolVol Plot Pick Label'
kwToolVolPlotLabelProt   = 'ToolVol Plot Add Label'
kwToolVolPlotColorScheme = 'ToolVol Plot Color Scheme'
kwToolVolPlotColorConf   = 'ToolVol Plot Color Configure'
#------------------------------> Fold Change Evolution
kwToolFCShowAll = 'FC Plot Show All'
#endregion ---------------------------------> Keywords for Menu - Method Links


#region --------------------------------------------------------------> Labels
#------------------------------> Filters
lFilFCEvol   = 'FC Evolution'
lFilHypCurve = 'Hyp Curve'
lFilFCLog    = 'Log2FC'
lFilPVal     = 'P Val'
lFilZScore   = 'Z Score'
#endregion -----------------------------------------------------------> Labels


#region -------------------------------------------------------------> Options
oIntensities = {
    'Empty' : '',
    'RawI'  : 'Raw Intensities',
    'RatioI': 'Ratio of Intensities',
}
#endregion ----------------------------------------------------------> Options


#region --------------------------------------------------------> Literal
litTestSide     = Literal['ts', 's', 'l']
#endregion -----------------------------------------------------> Literal


#region ------------------------------------------------------------> Messages
#region -------------------------------------------------------------> Other
#------------------------------> Check for Update
mCheckUpdate     = 'Check for Updates failed. Check again later.'
#endregion ----------------------------------------------------------> Other

#region ---------------------------------------------------------------> Files
mFileSelector = 'It was not possible to show the file selecting dialog.'
#endregion ------------------------------------------------------------> Files

#region ------------------------------------------------------------> Pandas
mPDGetInitCol     = ('It was not possible to extract the selected columns ({}) '
                     'from the selected {} file:\n{}')
mPDDataTypeCol    = 'The {} contains unexpected data type in columns {}.'
#endregion ---------------------------------------------------------> Pandas

#------------------------------>
mCompNYI            = "Comparison method is not yet implemented: {}."
mPDFilterByCol      = "Filtering process failed."
mNotImplemented     = 'Option {} is not yet implemented.'
mNotSupported       = "{} value '{}' is not supported."
#endregion ---------------------------------------------------------> Messages


#region ---------------------------------------------------------------> Sizes
#------------------------------> Plot Window
sWinModPlot = (1100, 625)
#endregion ------------------------------------------------------------> Sizes
#endregion --------------------------------------> NON-CONFIGURABLE PARAMETERS


#region ---------------------------------------------> CONFIGURABLE PARAMETERS
#region --------------------------------------------------------------> Colors


confColor = { # Colors for the app
    nwProtProf : {
        'Vol'    : ['#ff3333', '#d3d3d3', '#3333ff'],
        'VolSel' : '#6ac653',
        'FCAll'  : '#d3d3d3',
        'FCLines': ['#ff5ce9', '#5047ff', '#ffa859', '#85ff8c', '#78dbff'],
        'CV'     : 'gray',
    }
}
#endregion -----------------------------------------------------------> Colors
#endregion ------------------------------------------> CONFIGURABLE PARAMETERS
