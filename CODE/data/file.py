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
from typing import Optional, Literal

import pandas as pd

import wx

import dat4s_core.data.file as dtsFF
import dat4s_core.exception.exception as dtsException

import config.config as config

if config.typeCheck:
    #------------------------------> 
    from pathlib import Path
    #------------------------------> 
    import gui.dtscore as dtscore
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
        data : dict
            Data read from json formatted file
        confData : dict
            Configured data. Data from the umsap file is checked and converted 
            to the proper python types. See Notes for the structure of the dict.
        confTree : dict
            Nodes to show in the wx.TreeCtrl of the control window. 
            See Notes for the structure of the dict.
        cSection : dict
            Name of the sections in the umsap file
        cConfigure : dict
            Configure methods. Keys are the section names as read from the file

        Raises
        ------
        InputError
            - When fileP cannot be read.
        ExecutionError
            - When a requested section is not found in the file (GetSectionData)

        Methods
        -------

        Notes
        -----
        The general structure of confData is:
        {
            'Correlation Analysis' : {
                'Date' : { # Only valid date sections e.g. 20210325-112056
                    'DF' : pd.DataFrame with Result values,
                },
            },
        }
        - Each Section.Date can have additional information. 
        See the corresponding ConfigureDataSection

        The general structure of confTree is:
        {
            'Sections': { 'A': True, 'B': False},
            'Correlation Analysis' : {'DateA': True, 'DateB': False},
        }
        - Sections with True are shown with a checkbox in the TreeCtrl of the
        UMSAPControl window to signal there is something to plot in the section.
        - Dates with False are shown with a different font in the TreeCtrl of 
        the UMSAPControl window.
    """
    #region -----------------------------------------------------> Class setup
    name = 'UMSAPFile'
    
    cSection = {# Name of the sections in the umsap file
        config.npCorrA   : config.nuCorrA,
        config.npProtProf: config.nmProtProf,
    }
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, fileP: 'Path') -> None:
        """ """
        #region ---------------------------------------------------> Variables
        self.fileP = fileP

        self.cConfigure = {# Configure methods. Keys are the section names as
                           # read from the file
            self.cSection[config.npCorrA]    : self.ConfigureDataCorrA,
            self.cSection[config.npProtProf]: self.ConfigureDataProtProf,
        }
        #------------------------------> See Notes about the structure of dict
        self.confData = {}
        self.confTree = {
            'Sections' : {},
        }
        #endregion ------------------------------------------------> Variables

        #region -------------------------------------------------> Check Input
        try:
            self.data = dtsFF.ReadJSON(fileP)
        except Exception:
            raise dtsException.InputError(config.mFileRead.format(self.fileP))
        #endregion ----------------------------------------------> Check Input
    #---
    #endregion -----------------------------------------------> Instance setup

    #----------------------------------------------------------> Class methods
    #region -------------------------------------------------------> Configure
    def Configure(
        self, dlg: Optional['dtscore.ProgressDialog']=None,
        ) -> Literal[True]:
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
            self.cConfigure[k]()
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

    def ConfigureDataCorrA(self) -> Literal[True]:
        """Configure a Correlation Analysis section	"""
        #region -------------------------------------------------> Plot & Menu
        #------------------------------> Empty start
        plotData = {}
        #------------------------------> Fill
        for k,v in self.data[self.cSection[config.npCorrA]].items():
            try:
                #------------------------------> Create data
                df  = pd.DataFrame(v['R'], dtype='float64')
                if (numCol := len(v['CI']['Column'])) == df.shape[0]:
                    pass
                else:
                    continue
                #------------------------------> Add to dict if no error
                plotData[k] = {
                    'DF'        : df,
                    'NumCol'    : numCol,
                    'NumColList': v['CI']['Column'],
                }
            except Exception:
                pass
        #endregion ----------------------------------------------> Plot & Menu
        
        #region -------------------------------------------> Add/Reset section 
        self.confData[self.cSection[config.npCorrA]] = plotData
        #endregion ----------------------------------------> Add/Reset section 
        
        return True
    #---
    
    def ConfigureDataProtProf(self) -> Literal[True]:
        """Configure a Proteome Profiling section"""
        #region -------------------------------------------------> Plot & Menu
        #------------------------------> Empty start
        plotData = {}
        #------------------------------> Fill
        for k,v in self.data[self.cSection[config.npProtProf]].items():
            try:
                #------------------------------> Create data
                df  = pd.DataFrame(v['R'])
                #------------------------------> Add to dict if no error
                plotData[k] = {
                    'DF': df,
                }
            except Exception:
                pass
        #endregion ----------------------------------------------> Plot & Menu
        
        #region -------------------------------------------> Add/Reset section 
        self.confData[self.cSection[config.npProtProf]] = plotData
        #endregion ----------------------------------------> Add/Reset section 
        
        return True
    #---

    def ConfigureTree(self, tSection: str) -> Literal[True]:
        """Configure a section for the Tree widget.
            This is intended to be used after ConfigureDataX.

            Parameters
            ----------
            tSection : str
                One of config.nameUtilities or config.nameModules
        """
        #region -----------------------------------------> Add Section Boolean
        self.confTree['Sections'][tSection] = (
            any(self.confData[tSection].keys())
        )
        #endregion --------------------------------------> Add Section Boolean
        
        #region ---------------------------------------------------> Add Dates
        #------------------------------> Dicts
        self.confTree[tSection] = {}
        #------------------------------> Date
        for k in self.data[tSection].keys():
            self.confTree[tSection][k] = (
                k in self.confData[tSection]
            )
        #endregion ------------------------------------------------> Add Dates
        
        return True
    #---
    #endregion ----------------------------------------------------> Configure
    
    #region -----------------------------------------------------> Get Methods
    def GetSectionCount(self) -> int:
        """Get the total number of sections in file

            Returns
            -------
            int:
                Number of sections in the file	
        """
        return len(self.data.keys())
    #---

    def GetSectionData(self, tSection: str) -> dict:
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
        if (data := self.data.get(tSection, '')) != '':
            return data
        else:
            msg = (
                f"Section {tSection} was not found in the content of "
                f"file:\n{self.fileP}"
            )
            raise dtsException.ExecutionError(msg)
    #---

    def GetSectionDateDF(self, tSection: str, tDate: str) -> pd.DataFrame:
        """Get the dataframe for the section and date
    
            Parameters
            ----------
            tSection : str
                Section name
            tDate : str
                The date e.g. 20210325-112056
    
            Returns
            -------
            pd.DataFrame
        """
        try:
            return self.confData[tSection][tDate]['DF']
        except Exception as e:
            raise e
    #---

    def GetDataI(self, tSection: str, tDate: str) -> dict:
        """ Get initial user input for one analysis
    
            Parameters
            ----------
            tSection: str
                Analysis performed, e.g. 'Correlation Analysis'
            tDate : str
                Date of the analysis, e.g. '20210630-143556'
    
            Returns
            -------
            dict
    
            Raise
            -----
            KeyError:
                When tSection or tDate is not found in the file
        """
        try:
            return self.data[tSection][tDate]['I']
        except KeyError as e:
            raise e
    #---
    
    def GetDataCI(self, tSection: str, tDate: str) -> dict:
        """ Get curated user input for one analysis
    
            Parameters
            ----------
            tSection: str
                Analysis performed, e.g. 'Correlation Analysis'
            tDate : str
                Date of the analysis, e.g. '20210630-143556'
    
            Returns
            -------
            dict
    
            Raise
            -----
            KeyError:
                When tSection or tDate is not found in the file
        """
        try:
            return self.data[tSection][tDate]['CI']
        except KeyError as e:
            raise e
    #---
    
    def GetDataUser(self, tSection: str, tDate: str) -> dict:
        """ Get both initial and curated data from the user for the analysis
    
            Parameters
            ----------
            tSection: str
                Analysis performed, e.g. 'Correlation Analysis'
            tDate : str
                Date of the analysis, e.g. '20210630-143556'
    
            Returns
            -------
            dict
    
            Raise
            -----
            KeyError:
                When tSection or tDate is not found in the file
        """
        #region ------------------------------------------------> Strip I keys
        #------------------------------> 
        i = {}
        #------------------------------> 
        for k,v in self.data[tSection][tDate]['I'].items():
            i[k.strip()] = v
        #endregion ---------------------------------------------> Strip I keys
        
        try:
            return {
                'I':  i, 
                'CI': self.data[tSection][tDate]['CI'], 
            }
        except KeyError as e:
            raise e
    #---
    #endregion --------------------------------------------------> Get Methods

    #region -----------------------------------------------------> Export data
    def ExportPlotData(self, tSection: str, tDate: str, fileP: 'Path'
                      ) -> Literal[True]:
        """Export the plot data
    
            Parameters
            ----------
            tSection : str
                Section name
            tDate : str
                The date e.g. 20210325-112056
            fileP : Path
                Path to the file
        """
        try:
            dtsFF.WriteDF2CSV(fileP, self.GetSectionDateDF(tSection, tDate))
        except Exception as e:
            raise e
        
        return True
    #---
    #endregion --------------------------------------------------> Export data
#---
#endregion ----------------------------------------------------------> Classes



