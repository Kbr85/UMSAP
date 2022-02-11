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
from pathlib import Path
from typing import Optional

import dat4s_core.data.file as dtsFF
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
    """
    #region -----------------------------------------------------> Class setup
    cName = 'UMSAPFile'
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, rFileP: Path) -> None:
        """ """
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
        
        #region ---------------------------------------------------> Variables
        self.rFileP = Path(rFileP)
        self.rStepDataP = self.rFileP.parent / config.fnDataSteps

        self.dConfigure = {# Configure methods. Keys are the section names as
                           # read from the file
            config.nuCorrA   : self.ConfigureDataCorrA,
            config.nuDataPrep: self.ConfigureDataCheckDataPrep,
            config.nmProtProf: self.ConfigureDataProtProf,
            config.nmLimProt : self.ConfigureDataLimProt,
            config.nmTarProt : self.ConfigureDataTarProt,
        }
        #endregion ------------------------------------------------> Variables
    #---
    #endregion -----------------------------------------------> Instance setup

    #------------------------------>  Class methods
    #region -------------------------------------------------------> Configure
    def ConfigureDataCorrA(self) -> dict:
        """Configure a Correlation Analysis section	
        
            Returns
            ------
            dict
            {
                'DF' : pd.DataFrame with the data to plot,
                'NumCol' : number of columns in 'DF',
                'NumColList' : List with the number of the columns,
            }
        """
        #region -------------------------------------------------> Plot & Menu
        #------------------------------> Empty start
        plotData = {}
        #------------------------------> Fill
        for k,v in self.rData[config.nuCorrA].items():
            #------------------------------> 
            tPath = self.rStepDataP / f'{k.split(" - ")[0]}_{config.nuCorrA.replace(" ", "-")}'
            #------------------------------> 
            try:
                #------------------------------> Create data
                df = dtsFF.ReadCSV2DF(tPath/v['R'])
                
                if (numCol := len(v['CI']['oc']['Column'])) == df.shape[0]:
                    pass
                else:
                    continue
                #------------------------------> Add to dict if no error
                plotData[k] = {
                    'DF'     : df,
                    'NumCol' : numCol,
                    'NumColList': v['CI']['oc']['Column'],
                }
            except Exception:
                pass
        #endregion ----------------------------------------------> Plot & Menu
        
        return plotData
    #---
    
    def ConfigureDataCheckDataPrep(
        self, tSection: Optional[str]=None, tDate: Optional[str]=None
        ) -> dict:
        """Configure a Data Preparation Check section	
        
            Parameters
            ----------
            tSection: str or None
                Section name. Default is None
            tDate : str or None
                Date and comment. Default is None
        
            Returns
            -------
            dict
            {
                'DP' : dict with the data preparation steps key are the step's
                        names and values the pd.DataFrame,
            }
        """
        if tSection is None and tDate is None:
            return self.ConfigureDataCheckDataPrepFromUMSAP()
        elif tSection is not None and tDate is not None:
            return self.ConfigureDataCheckDataPrepFromPlot(tSection, tDate)
        else:
            msg = (f'Both tSection ({tSection}) and tDate ({tDate}) must be '
                   f'None or be defined.')
            raise dtsException.InputError(msg)
    #---
    
    def ConfigureDataCheckDataPrepFromPlot(
        self, tSection: str, tDate: str,
        ) -> dict:
        """Configure a Data Preparation Check section	
        
            Parameters
            ----------
            tSection: str
                Section name
            tDate : str
                Date and comment
        
            Returns
            -------
            dict
            {
                'DP' : dict with the data preparation steps key are the step's
                        names and values the pd.DataFrame,
            }
        """
        #region ---------------------------------------------------> Variables
        plotData = {}
        tPath = self.rStepDataP / f'{tDate.split(" - ")[0]}_{tSection.replace(" ", "-")}'
        #endregion ------------------------------------------------> Variables

        #region -------------------------------------------------> Plot & Menu
        try:
            plotData[tDate] = {
                'DP': {j:dtsFF.ReadCSV2DF(tPath/w) for j,w in self.rData[tSection][tDate]['DP'].items()},
            }
        except Exception as e:
            pass        
        #endregion ----------------------------------------------> Plot & Menu
        
        return plotData
    #---
    
    def ConfigureDataCheckDataPrepFromUMSAP(self) -> dict:
        """Configure a Data Preparation Check section	
        
            Returns
            -------
            dict
            {
                'DP' : dict with the data preparation steps key are the step's
                        names and values the pd.DataFrame,
            }
        """
        #region ---------------------------------------------------> Variables
        plotData = {}
        #endregion ------------------------------------------------> Variables

        #region -------------------------------------------------> Plot & Menu        
        for k,v in self.rData[config.nuDataPrep].items():
            try:
                #------------------------------> 
                tPath = self.rStepDataP / f'{k.split(" - ")[0]}_{config.nuDataPrep.replace(" ", "-")}'
                #------------------------------> Add to dict
                plotData[k] = {
                    'DP' : {j:dtsFF.ReadCSV2DF(tPath/w) for j,w in v['DP'].items()},
                }
            except Exception:
                pass
        #endregion ----------------------------------------------> Plot & Menu
        
        return plotData
    #---
    
    def ConfigureDataProtProf(self) -> dict:
        """Configure a Proteome Profiling section
        
            Returns
            ------
            dict
            {
                'DF' : pd.DataFrame with the data to plot,
            }
        """
        #region -------------------------------------------------> Plot & Menu
        #------------------------------> Empty start
        plotData = {}
        #------------------------------> Fill
        for k,v in self.rData[config.nmProtProf].items():
            try:
                #------------------------------> 
                tPath = self.rStepDataP / f'{k.split(" - ")[0]}_{config.nmProtProf.replace(" ", "-")}'
                #------------------------------> Create data
                df  = dtsFF.ReadCSV2DF(tPath/v['R'], header=[0,1,2])
                #------------------------------> Add to dict if no error
                plotData[k] = {
                    'DF': df,
                }
            except Exception:
                pass
        #endregion ----------------------------------------------> Plot & Menu
        
        return plotData
    #---
    
    def ConfigureDataLimProt(self) -> dict:
        """Configure a Limited Proteolysis section
        
            Returns
            -------
            dict
            {
                'DF' : pd.DataFrame with the data to plot,
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
                #------------------------------> 
                tPath = self.rStepDataP / f'{k.split(" - ")[0]}_{config.nmLimProt.replace(" ", "-")}'
                #------------------------------> Create data
                df  = dtsFF.ReadCSV2DF(tPath/v['R'], header=[0,1,2])
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
                    'PI': PI,
                }
            except Exception:
                pass
        #endregion ----------------------------------------------> Plot & Menu
        
        return plotData
    #---
    
    def ConfigureDataTarProt(self) -> dict:
        """Configure a Targeted Proteolysis section
        
            Returns
            ------
            dict
            {
                'DF' : pd.DataFrame with the data to plot,
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
                #------------------------------> 
                tPath = self.rStepDataP / f'{k.split(" - ")[0]}_{config.nmTarProt.replace(" ", "-")}'
                #------------------------------> Create data
                df  = dtsFF.ReadCSV2DF(tPath/v['R'], header=[0,1])
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
                    'PI': PI,
                }
            except Exception:
                pass
        #endregion ----------------------------------------------> Plot & Menu
        
        return plotData
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
                    'rootP' : path to the folder containing the UMSAP file,
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
                'I'    : i,
                'CI'   : self.rData[tSection][tDate]['CI'],
                'uFile': self.rFileP,
            }
        except KeyError as e:
            raise e
    #---
    #endregion --------------------------------------------------> Get Methods
#---
#endregion ----------------------------------------------------------> Classes



