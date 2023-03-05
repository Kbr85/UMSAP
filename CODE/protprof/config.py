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
    #------------------------------> Names & Titles
    nMod:str              = 'Proteome Profiling'                                # Name of the Module
    nwRes:str             = 'Window Result ProtProf Plot'                       # Name of the Result window
    ndFilterRemoveAny:str = 'Remove Filters'
    nTab:str              = 'Tab Proteome Profiling'                            # Name of Conf Tab
    nPane:str             = 'Pane ProtProf'                                     # Name of Conf Pane
    npResControlExp:str   = 'ResControlExpPaneProtProf'
    tTab:str              = 'ProtProf'                                          # Title of Conf Tab
    #------------------------------> Labels
    lStCond:str             = 'Conditions'                                      # lSt: Label for wx.StaticText
    lStRP:str               = 'Relevant Points'
    lmClearSelAll:str       = 'All'
    lmClearSelLabel:str     = 'Labels'
    lmClearSelSel:str       = 'Selection'
    lmColorSchemeConf:str   = 'Configure'
    lmColorSchemePLog2:str  = 'P - Log2FC'
    lmFCEvolExpImg:str      = 'Export Image'
    lmFCEvolShowAll:str     = 'Show All'                                        # lm: Label for wx.MenuItem
    lmFCEvolZoomReset:str   = 'Reset Zoom'
    lmFilterApplyAll:str    = 'Apply All'
    lmFilterApplyAuto:str   = 'Auto Apply'
    lmFilterCopy:str        = 'Copy'
    lmFilterFcEvol:str      = 'FC Evolution'
    lmFilterHypCurve:str    = 'Hyperbolic Curve'
    lmFilterLoad:str        = 'Load'
    lmFilterLog2FC:str      = 'Log2(FC)'
    lmFilterPaste:str       = 'Paste'
    lmFilterPVal:str        = 'P Value'
    lmFilterRemove:str      = 'Remove'
    lmFilterRemoveAll:str   = 'Remove All'
    lmFilterRemoveLast:str  = 'Remove Last'
    lmFilterSave:str        = 'Save'
    lmFilterZScore:str      = 'Z Score'
    lmScaleAnalysis:str     = 'Analysis'
    lmScaleNo:str           = 'No'
    lmScaleProject:str      = 'Project'
    lmToolClearSel:str      = 'Clear Selection'
    lmToolExpFilterData:str = 'Export Filtered Data'
    lmToolFCEvol:str        = 'FC Evolution'
    lmToolFilter:str        = 'Filters'
    lmToolLockScale:str     = 'Lock Plot Scale'
    lmToolVolPlot:str       = 'Volcano Plot'
    lmVolColor:str          = 'Color Scheme'
    lmVolExpImg:str         = 'Export Image'
    lmVolLabelAdd:str       = 'Add Label'
    lmVolLabelPick:str      = 'Pick Label'
    lmVolZoomReset:str      = 'Reset Zoom'
    #------------------------------> Keyword for wx.MenuItem
    kwClearSelAll:str        = 'Clear Selection All'
    kwClearSelLabel:str      = 'Clear Selection Labels'
    kwClearSelSel:str        = 'Clear Selection Selection'
    kwExportDataFiltered:str = 'Tool Export Filtered Data'
    kwFCShowAll:str          = 'FC Plot Show All'
    kwFilterApplyAll:str     = 'Filter Apply All'
    kwFilterApplyAuto:str    = 'Filter AutoApplyFilter'
    kwFilterCopy:str         = 'Filter Copy'
    kwFilterFCEvol:str       = 'Filter FC Evolution'
    kwFilterFCLog:str        = 'Filter Log2FC'
    kwFilterHypCurve:str     = 'Filter Hyp Curve'
    kwFilterLoad:str         = 'Filter Load Filter'
    kwFilterPaste:str        = 'Filter Paste'
    kwFilterPVal:str         = 'Filter P Val'
    kwFilterRemoveAll:str    = 'Filter Remove All'
    kwFilterRemoveAny:str    = 'Filter Remove Any'
    kwFilterRemoveLast:str   = 'Filter Remove Last'
    kwFilterSave:str         = 'Filter Save Filter'
    kwFilterZScore:str       = 'Filter Z Score'
    kwScaleAnalysis:str      = 'Lock Scale Analysis'
    kwScaleMode:str          = 'Lock Scale Mode'
    kwScaleNo:str            = 'Lock Scale No'
    kwScaleProject:str       = 'Lock Scale Project'
    kwVolMenuCond:str        = 'cond'
    kwVolMenuRP:str          = 'rp'
    kwVolMenuVol:str         = 'Vol'
    kwVolPlot:str            = 'Vol Plot CRP'
    kwVolPlotColorConf:str   = 'Vol Plot Color Configure'
    kwVolPlotColorScheme:str = 'Vol Plot Color Scheme'
    kwVolPlotLabelPick:str   = 'Vol Plot Pick Label'
    kwVolPlotLabelProt:str   = 'Vol Plot Add Label'
    kwFC:str                 = 'FC'                                             # Methods keyword
    kwVol:str                = 'Vol'
    kwMode:str               = 'mode'
    #------------------------------> List
    lFilter:list = field(default_factory=list)
    #------------------------------> DataFrame Columns
    dfColGene = ('Gene', 'Gene', 'Gene')
    dfColProt = ('Protein', 'Protein', 'Protein')
    dfcolFirstPart:list[str] = field(default_factory=lambda:
        ['Gene', 'Protein', 'Score'])
    dfcolCLevel:list[str] = field(default_factory=lambda:
        ['aveC', 'stdC', 'ave', 'std', 'FC', 'CI', 'FCz', 'P', 'Pc'])
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
    cFCAll:str  = '#d3d3d3'
    #------------------------------> User defined options
    alpha:str      = '0.05'
    correctP:str   = ''
    scoreVal:str   = '0'
    lock:str       = 'Analysis'
    filterA:str    = 'No'
    showAll:str    = ''
    pickP:str      = 'Select'
    t0:str         = '1.0'
    s0:str         = '0.1'
    p:str          = '0.05'
    fc:str         = '0.1'
    z:str          = '10.0'
    zShow:str      = 'Z Score Line'
    #-->
    cCV:str        = 'gray'
    cVolSel:str    = '#6ac653'
    cVol:list[str] = field(default_factory=lambda:
        ['#ff3333', '#d3d3d3', '#3333ff'])

    #endregion ------------------------------------------------------> Options
#---
#endregion ----------------------------------------------------> Configuration
