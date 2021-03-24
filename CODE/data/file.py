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
import pandas as pd

import wx

import dat4s_core.data.file as dtsFF
import dat4s_core.exception.exception as dtsException

import config.config as config
#endregion ----------------------------------------------------------> Imports

#region -------------------------------------------------------------> Classes
class UMSAPFile():
    """Read and analyse an umsap file.

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
        The general structure of confData is:
        {
            'Correlation Analysis' : {
                'Date' : { # Only valid date sections
                    'DF' : pd.DataFrame with Result values,
                },
            },
        }

        The general structure of confTree is:
        {
            'Sections': { 'A': True, 'B': False},
            'Correlation Analysis' : {DateA': True, 'DateB': False},
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
            #------------------------------> Configure data to plot
            'Configure' : { 
                config.nameUtilities['CorrA'] : self.ConfigureDataCorrA,
            },
        }
        #------------------------------> See Notes about the structure of dict
        self.confData = {}
        self.confTree = {
            'Sections' : {},
        }
        #endregion ------------------------------------------------> Variables

        #region -------------------------------------------------> Check Input
        self.data = dtsFF.ReadJSON(fileP)
        #endregion ----------------------------------------------> Check Input
    #---
    #endregion -----------------------------------------------> Instance setup

    #----------------------------------------------------------> Class methods
    #region -------------------------------------------------------> Configure
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
            #------------------------------> Configure data to plot
            #--------------> Update dlg
            if dlg is not None:
                wx.CallAfter(dlg.UpdateStG, f"Configuring section: {k}")
            else:
                pass
            #--------------> Configure data to plot
            self.confOpt['Configure'][k]()
            #------------------------------> Configure tree
            #--------------> Update dlg
            if dlg is not None:
                wx.CallAfter(dlg.UpdateG)
            else:
                pass
            #--------------> Configure tree
            self.ConfigureTree(k)
        #endregion ---------------------------------------> Configure sections
        
        #region -------------------------------------------------> Destroy dlg
        if dlg is not None:
            wx.CallAfter(dlg.EndModal, 1)
        else:
            pass		
        #endregion ----------------------------------------------> Destroy dlg
    
        return True
    #---

    def ConfigureDataCorrA(self):
        """Configure a Correlation Analysis section	"""
        #region -------------------------------------------------> Plot & Menu
        #------------------------------> Empty start
        plotData = {}
        #------------------------------> Fill
        for k,v in self.data[self.confOpt['CorrA']].items():
            try:
                #------------------------------> Create data
                df  = pd.DataFrame(v['R'], dtype='float64')
                if (numCol := len(v['CI']['Column'])) == df.shape[0]:
                    pass
                else:
                    raise Exception
                #------------------------------> Add to dict if no error
                plotData[k] = {
                    'DF'    : df,
                    'NumCol': numCol,
                }
            except Exception:
                pass

        #endregion ----------------------------------------------> Plot & Menu
        
        #region -------------------------------------------> Add/Reset section 
        self.confData[self.confOpt['CorrA']] = plotData
        #endregion ----------------------------------------> Add/Reset section 
        
        return True
    #---

    def ConfigureTree(self, section):
        """Configure a section for the Tree widget.
            This is intended to be used after ConfigureDataX

            Parameters
            ----------
            section : str
                One of config.nameUtilities or config.nameModules
        """
        #region -----------------------------------------> Add Section Boolean
        self.confTree['Sections'][section] = (
            any(self.confData[section].keys())
        )
        #endregion --------------------------------------> Add Section Boolean
        
        #region ---------------------------------------------------> Add Dates
        #------------------------------> Dicts
        self.confTree[section] = {}
        #------------------------------> Date
        for k in self.data[section].keys():
            self.confTree[section][k] = (
                k in self.confData[section]
            )
        #endregion ------------------------------------------------> Add Dates
    #---
    #endregion ----------------------------------------------------> Configure
    
    #region -----------------------------------------------------> Get Methods
    def GetSectionCount(self):
        """Get the total number of sections in file

            Returns
            -------
            int:
                Number of sections in the file	
        """
        return len(self.data.keys())
    #---

    def GetSectionData(self, tSection):
        """Get the dict with the data for a section
    
            Parameters
            ----------
            tSection : str
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
                f"Section {tSection} was not found in the content of "
                f"file:\n{self.fileP}"),
        }
        #endregion ------------------------------------------------> Variables
        
        if (data := self.data.get(tSection, '')) != '':
            return data
        else:
            raise dtsException.ExecutionError(confMsg['NoSection'])
    #---

    def GetSectionDateDF(self, tSection, tDate):
        """Get the dataframe for the section and date
    
            Parameters
            ----------
            tSection : str
                Section name
            tDate : str
                The date
    
            Returns
            -------
            pd.DataFrame
        """
        try:
            return self.confData[tSection][tDate]['DF']
        except Exception as e:
            raise e
    #---

    #region -----------------------------------------------------> Export data
    def ExportPlotData(self, tSection, tDate, fileP):
        """Export the plot data
    
            Parameters
            ----------
            tSection : str
                Section name
            tDate : str
                The date
            fileP : Path
                Path to the file
        """
        try:
            dtsFF.WriteDF2CSV(fileP, self.GetSectionDateDF(tSection, tDate))
        except Exception as e:
            raise e
    #---
    #endregion --------------------------------------------------> Export data
    
    #endregion --------------------------------------------------> Get Methods
#---

#endregion ----------------------------------------------------------> Classes



