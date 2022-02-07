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
from typing import Optional

import pandas as pd
import wx

import dat4s_core.data.file as dtsFF
import dat4s_core.data.method as dtsMethod
import dat4s_core.exception.exception as dtsException

import config.config as config


#endregion ----------------------------------------------------------> Imports

#region -------------------------------------------------------------> Classes
class UMSAPFile():
    """Read and analyse an UMSAP file.

        Parameters
        ----------
        rFileP : Path
            Path to the UMSAP file

        Attributes
        ----------
        cName : str
            Unique name of the class
        dConfigure : dict
            Configure methods. Keys are the section names as read from the file
        rConfData : dict
            Configured data. Data from the umsap file is checked and converted 
            to the proper python types. See Notes for the structure of the dict.
        rConfTree : dict
            Nodes to show in the wx.TreeCtrl of the control window. 
            See Notes for the structure of the dict.    
        rData : dict
            Data read from json formatted file
        rFileP : Path
            Path to the UMSAP file
        
        Raises
        ------
        InputError
            - When fileP cannot be read.
        ExecutionError
            - When a requested section is not found in the file (GetSectionData)

        Notes
        -----
        The general structure of rConfData is:
        {
            'Correlation Analysis' : {
                'Date' : { # Only valid date sections e.g. 20210325-112056
                    'DF' : pd.DataFrame with Result values,
                },
            },
        }
        - Each Section.Date can have additional information. 
        See the corresponding ConfigureDataSection

        The general structure of rConfTree is:
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
    cName = 'UMSAPFile'
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, rFileP: 'Path') -> None:
        """ """
        #region ---------------------------------------------------> Variables
        self.rFileP = rFileP

        self.dConfigure = {# Configure methods. Keys are the section names as
                           # read from the file
            config.nuCorrA   : self.ConfigureDataCorrA,
            config.nuDataPrep: self.ConfigureDataCheckDataPrep,
            config.nmProtProf: self.ConfigureDataProtProf,
            config.nmLimProt : self.ConfigureDataLimProt,
            config.nmTarProt : self.ConfigureDataTarProt,
        }
        #------------------------------> See Notes about the structure of dict
        self.rConfData = {}
        self.rConfTree = {
            'Sections' : {},
        }
        #endregion ------------------------------------------------> Variables

        #region -------------------------------------------------> Check Input
        try:
            #------------------------------> Read File
            data = dtsFF.ReadJSON(rFileP)
            #------------------------------> Sort Keys
            dataKey = sorted([x for x in data.keys()])
            #------------------------------> 
            self.rData = {}
            for k in dataKey:
                self.rData[k] = data[k]
        except Exception:
            raise dtsException.InputError(config.mFileRead.format(self.rFileP))
        #endregion ----------------------------------------------> Check Input
    #---
    #endregion -----------------------------------------------> Instance setup

    #------------------------------>  Class methods
    #region -------------------------------------------------------> Configure
    def Configure(
        self, dlg: Optional['dtscore.ProgressDialog']=None,
        ) -> bool:
        """Prepare data for each section in the file and for the CustomTreeCtrl
            in the control window.
    
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
        for k in self.rData.keys():
            #------------------------------> Configure data to plot
            #--------------> Update dlg
            if dlg is not None:
                wx.CallAfter(dlg.UpdateStG, f"Configuring section: {k}")
            else:
                pass
            #--------------> Configure data to plot
            self.dConfigure[k]()
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

    def ConfigureDataCorrA(self) -> bool:
        """Configure a Correlation Analysis section	
        
            Notes
            -----
            The dictionary with the data to plot contains the following 
            key - value pairs:
            {
                'DF' : pd.DataFrame with the data to plot,
                'DP' : dict with the data preparation steps key are the step's
                        names and values the pd.DataFrame,
                'NumCol' : number of columns in 'DF',
                'NumColList' : List with the colum's names,
            }
        """
        #region -------------------------------------------------> Plot & Menu
        #------------------------------> Empty start
        plotData = {}
        #------------------------------> Fill
        for k,v in self.rData[config.nuCorrA].items():
            try:
                #------------------------------> Create data
                df  = pd.DataFrame(v['R'], dtype='float64')
                if (numCol := len(v['CI']['oc']['Column'])) == df.shape[0]:
                    pass
                else:
                    continue
                #------------------------------> Add to dict if no error
                plotData[k] = {
                    'DF'     : df,
                    'DP'     : {j:pd.DataFrame(w) for j,w in v['DP'].items()},
                    'NumCol' : numCol,
                    'NumColList': v['CI']['oc']['Column'],
                }
            except Exception:
                pass
        #endregion ----------------------------------------------> Plot & Menu
        
        #region -------------------------------------------> Add/Reset section 
        self.rConfData[config.nuCorrA] = plotData
        #endregion ----------------------------------------> Add/Reset section 
        
        return True
    #---
    
    def ConfigureDataCheckDataPrep(self) -> bool:
        """Configure a Data Preparation Check section	
        
            Notes
            -----
            The dictionary with the data to plot contains the following 
            key - value pairs:
            {
                'DP' : dict with the data preparation steps key are the step's
                        names and values the pd.DataFrame,
            }
        """
        #region -------------------------------------------------> Plot & Menu
        #------------------------------> Empty start
        plotData = {}
        #------------------------------> Fill
        for k,v in self.rData[config.nuDataPrep].items():
            try:
                #------------------------------> Add to dict
                plotData[k] = {
                    'DP' : {j:pd.DataFrame(w) for j,w in v['DP'].items()},
                }
            except Exception:
                pass
        #endregion ----------------------------------------------> Plot & Menu
        
        #region -------------------------------------------> Add/Reset section 
        self.rConfData[config.nuDataPrep] = plotData
        #endregion ----------------------------------------> Add/Reset section 
        
        return True
    #---
    
    def ConfigureDataProtProf(self) -> bool:
        """Configure a Proteome Profiling section
        
            Notes
            -----
            The dictionary with the data to plot contains the following 
            key - value pairs:
            {
                'DF' : pd.DataFrame with the data to plot,
                'DP' : dict with the data preparation steps key are the step's
                        names and values the pd.DataFrame,
            }
        """
        #region -------------------------------------------------> Plot & Menu
        #------------------------------> Empty start
        plotData = {}
        #------------------------------> Fill
        for k,v in self.rData[config.nmProtProf].items():
            try:
                #------------------------------> Create data
                df  = pd.DataFrame(dtsMethod.DictStringKey2Tuple(v['R']))
                #------------------------------> Add to dict if no error
                plotData[k] = {
                    'DF': df,
                    'DP': {j: pd.DataFrame(w) for j,w in v['DP'].items()},
                }
            except Exception:
                pass
        #endregion ----------------------------------------------> Plot & Menu
        
        #region -------------------------------------------> Add/Reset section 
        self.rConfData[config.nmProtProf] = plotData
        #endregion ----------------------------------------> Add/Reset section 
        
        return True
    #---
    
    def ConfigureDataLimProt(self) -> bool:
        """Configure a Limited Proteolysis section
        
            Notes
            -----
            The dictionary with the data to plot contains the following 
            key - value pairs:
            {
                'DF' : pd.DataFrame with the data to plot,
                'DP' : dict with the data preparation steps key are the step's
                        names and values the pd.DataFrame,
                'PI' : { dict with information for the plotting window
                    'Bands'     : list with the band's names,
                    'Lanes'     : list with the lane's names,
                    'Alpha'     : alpha value,
                    'ProtLength': length of the recombinant protein,
                    'ProtLoc'   : list with the location of the native protein,
                    'ProtDelta' : value to calculate native residue numbers as
                                    resN_Nat = resN_Rec + ProtDelta,
                    'Prot'      : name of the Target Protein,
                },
            }
        """
        #region -------------------------------------------------> Plot & Menu
        #------------------------------> Empty start
        plotData = {}
        #------------------------------> Fill
        for k,v in self.rData[config.nmLimProt].items():
            try:
                #------------------------------> Create data
                df  = pd.DataFrame(dtsMethod.DictStringKey2Tuple(v['R']))
                #------------------------------> Plot Info
                PI = {
                    'Bands'     : v['CI']['Band'],
                    'Lanes'     : v['CI']['Lane'],
                    'Alpha'     : v['CI']['Alpha'],
                    'ProtLength': v['CI']['ProtLength'],
                    'ProtLoc'   : v['CI']['ProtLoc'],
                    'ProtDelta' : v['CI']['ProtDelta'],
                    'Prot'      : v['CI']['TargetProt'],
                }
                #------------------------------> Add to dict if no error
                plotData[k] = {
                    'DF': df,
                    'DP': {j: pd.DataFrame(w) for j,w in v['DP'].items()},
                    'PI': PI,
                }
            except Exception:
                pass
        #endregion ----------------------------------------------> Plot & Menu
        
        #region -------------------------------------------> Add/Reset section 
        self.rConfData[config.nmLimProt] = plotData
        #endregion ----------------------------------------> Add/Reset section 
        
        return True
    #---
    
    def ConfigureDataTarProt(self) -> bool:
        """Configure a Targeted Proteolysis section
        
            Notes
            -----
            The dictionary with the data to plot contains the following 
            key - value pairs:
            {
                'DF' : pd.DataFrame with the data to plot,
                'DP' : dict with the data preparation steps key are the step's
                        names and values the pd.DataFrame,
                'PI' : { dict with information for the plotting window
                    'Exp'       : list with the experiment's names,
                    'Alpha'     : alpha value,
                    'ProtLength': length of the recombinant protein,
                    'ProtLoc'   : list with the location of the native protein,
                    'ProtDelta' : value to calculate native residue numbers as
                                    resN_Nat = resN_Rec + ProtDelta,
                    'Prot'      : name of the Target Protein,
                },
            }
        """
        #region -------------------------------------------------> Plot & Menu
        #------------------------------> Empty start
        plotData = {}
        #------------------------------> Fill
        for k,v in self.rData[config.nmTarProt].items():
            try:
                #------------------------------> Create data
                df  = pd.DataFrame(dtsMethod.DictStringKey2Tuple(v['R']))
                #------------------------------> Plot Info
                PI = {
                    'Exp'       : v['CI']['Exp'],
                    'Ctrl'      : v['CI']['ControlL'],
                    'Alpha'     : v['CI']['Alpha'],
                    'ProtLength': v['CI']['ProtLength'],
                    'ProtLoc'   : v['CI']['ProtLoc'],
                    'ProtDelta' : v['CI']['ProtDelta'],
                    'Prot'      : v['CI']['TargetProt'],
                }
                #------------------------------> Add to dict if no error
                plotData[k] = {
                    'DF': df,
                    'DP': {j: pd.DataFrame(w) for j,w in v['DP'].items()},
                    'PI': PI,
                }
            except Exception:
                pass
        #endregion ----------------------------------------------> Plot & Menu
        
        #region -------------------------------------------> Add/Reset section 
        self.rConfData[config.nmTarProt] = plotData
        #endregion ----------------------------------------> Add/Reset section 
        
        return True
    #---

    def ConfigureTree(self, tSection: str) -> bool:
        """Configure a section for the Tree widget.
            This is intended to be used after ConfigureDataX.

            Parameters
            ----------
            tSection : str
                One of config.nameUtilities or config.nameModules
        """
        #region -----------------------------------------> Add Section Boolean
        self.rConfTree['Sections'][tSection] = (
            any(self.rConfData[tSection].keys())
        )
        #endregion --------------------------------------> Add Section Boolean
        
        #region ---------------------------------------------------> Add Dates
        #------------------------------> Dicts
        self.rConfTree[tSection] = {}
        #------------------------------> Date
        for k in self.rData[tSection].keys():
            self.rConfTree[tSection][k] = (
                k in self.rConfData[tSection]
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
        return len(self.rData.keys())
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
        if (data := self.rData.get(tSection, {})):
            return data
        else:
            msg = (
                f"Section {tSection} was not found in the content of "
                f"file:\n{self.rFileP}"
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
                The date plus user-given Analysis ID 
                e.g. '20210325-112056 - bla'
    
            Returns
            -------
            pd.DataFrame
        """
        try:
            return self.rConfData[tSection][tDate]['DF']
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
                The date plus user-given Analysis ID 
                e.g. '20210325-112056 - bla'
    
            Returns
            -------
            dict
    
            Raise
            -----
            KeyError:
                When tSection or tDate is not found in the file
        """
        try:
            return self.rData[tSection][tDate]['I']
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
                The date plus user-given Analysis ID 
                e.g. '20210325-112056 - bla'
    
            Returns
            -------
            dict
    
            Raise
            -----
            KeyError:
                When tSection or tDate is not found in the file
        """
        try:
            return self.rData[tSection][tDate]['CI']
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
                The date plus user-given Analysis ID 
                e.g. '20210325-112056 - bla'
    
            Returns
            -------
            dict:
                {
                    'I' : user input with stripped keys,
                    'CI': corrected user input,
                }
    
            Raise
            -----
            KeyError:
                When tSection or tDate is not found in the file
        """
        #region ------------------------------------------------> Strip I keys
        #------------------------------> 
        i = {}
        #------------------------------> 
        for k,v in self.rData[tSection][tDate]['I'].items():
            i[k.strip()] = v
        #endregion ---------------------------------------------> Strip I keys
        
        try:
            return {
                'I':  i, 
                'CI': self.rData[tSection][tDate]['CI'], 
            }
        except KeyError as e:
            raise e
    #---
    #endregion --------------------------------------------------> Get Methods

    #region --------------------------------------------------> Export Methods
    def ExportPlotData(self, tSection: str, tDate: str, fileP: 'Path') -> bool:
        """Export the plot data
    
            Parameters
            ----------
            tSection : str
                Section name
            tDate : str
                The date plus user-given Analysis ID 
                e.g. '20210325-112056 - bla'
            fileP : Path
                Path to the file
        """
        try:
            dtsFF.WriteDF2CSV(fileP, self.GetSectionDateDF(tSection, tDate))
        except Exception as e:
            raise e
        
        return True
    #---
    #endregion -----------------------------------------------> Export Methods
#---
#endregion ----------------------------------------------------------> Classes



