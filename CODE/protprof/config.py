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


"""Configuration for the protprof module of the app"""


#region -------------------------------------------------------------> Imports
from dataclasses import dataclass, field
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------> Configuration
@dataclass
class Configuration():
    """Configuration for the protprof module"""
    #region ---------------------------------------------------------> Options
    nMod:str              = 'Proteome Profiling'                                # Name of the Module
    nwRes:str             = 'Window Result ProtProf Plot'                       # Name of the Result window
    ndFilterRemoveAny:str = 'Remove Filters'
    nTab:str              = 'Tab Proteome Profiling'                            # Name of Conf Tab
    nPane:str             = 'Pane ProtProf'                                     # Name of Conf Pane
    npResControlExp:str   = 'ResControlExpPaneProtProf'
    tTab:str              = 'ProtProf'                                          # Title of Conf Tab
    #------------------------------> Labels
    lStCond:str      = 'Conditions'                                             # lSt: Label for wx.StaticText
    lStRP:str        = 'Relevant Points'
    lFilFCEvol:str   = 'FC Evolution'                                           # lFil: Label for Filters
    lFilHypCurve:str = 'Hyp Curve'
    lFilFCLog:str    = 'Log2FC'
    lFilPVal:str     = 'P Val'
    lFilZScore:str   = 'Z Score'
    #------------------------------> Keyword for wx.MenuItem
    kwExportDataFiltered:str = 'GeneralTool Export Filtered Data'
    kwFCShowAll:str          = 'FC Plot Show All'
    kwVolPlot:str            = 'ToolVol Plot CRP'
    kwVolPlotColorConf:str   = 'ToolVol Plot Color Configure'
    kwVolPlotColorScheme:str = 'ToolVol Plot Color Scheme'
    kwVolPlotLabelPick:str   = 'ToolVol Plot Pick Label'
    kwVolPlotLabelProt:str   = 'ToolVol Plot Add Label'
    #------------------------------> DataFrame Columns
    dfcolFirstPart:list[str] = field(default_factory=lambda:
        ['Gene', 'Protein', 'Score'])
    dfcolCLevel:list[str] = field(default_factory=lambda:
        ['aveC', 'stdC', 'ave', 'std', 'FC', 'CI', 'FCz'])
    #------------------------------> Options
    oControlType:dict = field(default_factory=lambda: {                         # Control Type for the Res - Ctrl wx.Dialog
        'Empty': '',
        'OC'   : 'One Control',
        'OCC'  : 'One Control per Column',
        'OCR'  : 'One Control per Row',
        'Ratio': 'Ratio of Intensities',
    })
    #------------------------------> Messages
    mRepNum:str = ('To perform a Proteome Profiling analysis using Raw '
                   'Intensities and Paired Samples the number of replicates '
                   'in experiments and the corresponding control must be '
                   'the same.\n\nThe number of replicates in the following '
                   'experiments does not match the number of replicates in '
                   'the corresponding control.\n{}'
    )
    #------------------------------> Colors
    cVol:list[str] = field(default_factory=lambda:
        ['#ff3333', '#d3d3d3', '#3333ff'])
    cFCLines:list[str] = field(default_factory=lambda:
        ['#ff5ce9', '#5047ff', '#ffa859', '#85ff8c', '#78dbff'])
    cVolSel:str = '#6ac653'
    cFCAll:str  = '#d3d3d3'
    cCV:str     = 'gray'
    #------------------------------> Converter for user options
    converter:dict = field(default_factory=lambda: {})
    #endregion ------------------------------------------------------> Options
#---
#endregion ----------------------------------------------------> Configuration
