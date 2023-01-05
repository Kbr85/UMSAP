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


"""Methods to handle files in the result module of the app"""


#region -------------------------------------------------------------> Imports
from pathlib import Path
from typing  import Union

import pandas as pd

from config.config import config as mConfig
from core import file as cFile
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Classes
class UMSAPFile():
    """Load an UMSAP file.

        Parameters
        ----------
        rFileP: Path
            Path to the UMSAP file

        Attributes
        ----------
        dConfigure: dict
            Configure methods. Keys are the section names as read from the file
        rData: dict
            Data read from json formatted file.
        rFileP: Path
            Path to the UMSAP file.
        rInputFileP: Path
            Path to the input files.
        rStepDataP: Path
            Path to the step data files.
        SeqF: list[str]
            Sections with a sequence file.
    """
    # No Test
    #region -----------------------------------------------------> Class setup
    SeqF = [mConfig.tarp.nMod, mConfig.limp.nMod]
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, fileP:Path) -> None:
        """ """
        #region ---------------------------------------------------> Read File
        data = cFile.ReadJSON(fileP)
        #------------------------------> Sort Keys
        dataKey = sorted(list(data.keys()))
        #------------------------------>
        self.rData = {k:data[k] for k in dataKey}
        #endregion ------------------------------------------------> Read File

        #region ---------------------------------------------------> Variables
        self.rFileP = fileP
        self.rStepDataP  = self.rFileP.parent / mConfig.core.fnDataSteps
        self.rInputFileP = self.rFileP.parent / mConfig.core.fnDataInit
        #------------------------------>
        self.dConfigure = {# Configure methods. Keys are section names.
            mConfig.corr.nUtil: self.ConfigureDataCorrA,
            mConfig.data.nUtil: self.ConfigureDataDataPrep,
            mConfig.prot.nMod : self.ConfigureDataProtProf,
            mConfig.limp.nMod : self.ConfigureDataLimProt,
            mConfig.tarp.nMod : self.ConfigureDataTarProt,
        }
        #endregion ------------------------------------------------> Variables
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ----------------------------------------------------> Class Method
    def Save(self, tPath:Union[None, str, Path]=None) -> bool:
        """Save the file content.

            Parameters
            ----------
            tPath: Path, str or None

            Returns
            -------
            bool
        """
        #region ---------------------------------------------------> Variables
        oPath = tPath if tPath is not None else self.rFileP
        #endregion ------------------------------------------------> Variables

        #region ---------------------------------------------------> Write
        cFile.WriteJSON(oPath, self.rData)
        #endregion ------------------------------------------------> Write

        return True
    #---
    #endregion -------------------------------------------------> Class Method

    #region -------------------------------------------------------> Configure
    def ConfigureDataCorrA(self) -> dict:
        """Configure a Correlation Analysis section.

            Returns
            ------
            dict
            {
                'Error': ['Date1',...], # Analysis containing errors.
                'Date1': {
                    'DF'         : pd.DataFrame with the data to plot,
                    'NumCol'     : number of columns in 'DF',
                    'NumColList' : List with the number of the columns,
                },
                'DateN' : {}
            }
        """
        #region ---------------------------------------------------> Variables
        plotData = {}
        plotData['Error'] = []
        pathB = mConfig.corr.nUtil.replace(" ", "-")
        #endregion ------------------------------------------------> Variables

        #region -------------------------------------------------> Plot & Menu
        #------------------------------> Fill
        for k, v in self.rData[mConfig.corr.nUtil].items():
            #------------------------------>
            pathA = k.split(" - ")[0]
            tPath = self.rStepDataP / f'{pathA}_{pathB}'
            #------------------------------> Read data
            try:
                df = cFile.ReadCSV2DF(tPath/v['R'])
            except Exception:
                plotData['Error'].append(k)
                continue
            #------------------------------> Check Columns
            if not (numCol := len(v['CI']['oc']['Column'])) == df.shape[0]:
                plotData['Error'].append(k)
                continue
            #------------------------------> Add to dict if no error
            plotData[k] = { # type: ignore
                'DF'        : df,
                'NumCol'    : numCol,
                'NumColList': v['CI']['oc']['Column'],
            }
        #endregion ----------------------------------------------> Plot & Menu

        return plotData
    #---

    def ConfigureDataDataPrep(self, tSection:str='', tDate:str='') -> dict:
        """Configure a Data Preparation Check section.

            Parameters
            ----------
            tSection: str
                Section name. Default is ''.
            tDate : str
                Date and comment. Default is ''.

            Returns
            -------
            dict
            {
                'Error': ['Date1',...], # Analysis containing errors.
                'Date1': {
                    'DP' : dict with the data preparation steps key are the
                        step's names and values the pd.DataFrame,
                },
                'DateN': {},
            }
        """
        #------------------------------> Data Prep From Plot
        if tSection and tDate:
            return self.ConfigureDataDataPrepFromPlot(tSection, tDate)
        #------------------------------> Data Prep From UMSAP
        if not tSection and not tDate:
            return self.ConfigureDataDataPrepFromUMSAP()
        #------------------------------> Error
        msg = (f'Both tSection ({tSection}) and tDate ({tDate}) must be '
               f"defined or ''.")
        raise ValueError(msg)
    #---

    def ConfigureDataDataPrepFromPlot(self, tSection:str, tDate:str) -> dict:
        """Configure a Data Preparation Check section.

            Parameters
            ----------
            tSection: str
                Section name.
            tDate: str
                Date and comment.

            Returns
            -------
            dict
            {
                'Error': ['Date1',...], # Analysis containing errors.
                'Date1': {
                    'DP' : dict with the data preparation steps key are the
                        step's names and values the pd.DataFrame,
                }
            }
        """
        #region ---------------------------------------------------> Variables
        plotData          = {}
        plotData['Error'] = []
        pathA = tDate.split(" - ")[0]
        pathB = tSection.replace(" ", "-")
        tPath = self.rStepDataP / f'{pathA}_{pathB}'
        #endregion ------------------------------------------------> Variables

        #region -------------------------------------------------> Plot & Menu
        try:
            plotData[tDate] = {
                'DP': {j:cFile.ReadCSV2DF(tPath/w) for j,w in self.rData[tSection][tDate]['DP'].items()},
                'NumColList': self.rData[tSection][tDate]['CI']['oc']['Column'],
            }
        except Exception:
            pass
        #endregion ----------------------------------------------> Plot & Menu

        return plotData
    #---

    def ConfigureDataDataPrepFromUMSAP(self) -> dict:
        """Configure a Data Preparation Check section.

            Returns
            -------
            dict
            {
                'Error': ['Date1',...], # Analysis containing errors.
                'Date1': {
                    'DP' : dict with the data preparation steps key are the
                        step's names and values the pd.DataFrame,
                },
                'DateN': {},
            }
        """
        #region ---------------------------------------------------> Variables
        plotData = {}
        plotData['Error'] = []
        pathB = mConfig.data.nUtil.replace(" ", "-")
        #endregion ------------------------------------------------> Variables

        #region -------------------------------------------------> Plot & Menu
        for k,v in self.rData[mConfig.data.nUtil].items():
            #------------------------------> Read and type
            try:
                pathA = k.split(" - ")[0]
                tPath = self.rStepDataP / f'{pathA}_{pathB}'
            except Exception:
                plotData['Error'].append(k)
                continue
            #------------------------------> Add to dict
            plotData[k] = {
                'DP' : {j:cFile.ReadCSV2DF(tPath/w) for j,w in v['DP'].items()},
                'NumColList': v['CI']['oc']['Column'],
            }
        #endregion ----------------------------------------------> Plot & Menu

        return plotData
    #---

    def ConfigureDataProtProf(self) -> dict:
        """Configure a Proteome Profiling section.

            Returns
            ------
            dict
            {
                'Error': ['Date1',...], # Analysis containing errors.
                'Date1': {
                    'DF'   : pd.DataFrame with the data to plot,
                    'F'    : dict with filters,
                    'Alpha': Alpha value used in the analysis,
                },
                'DateN': {},
            }
        """
        #region ---------------------------------------------------> Variables
        plotData = {}
        plotData['Error'] = []
        colStr = [('Gene','Gene','Gene'),('Protein','Protein','Protein')]
        pathB  = mConfig.prot.nMod.replace(" ", "-")
        #endregion ------------------------------------------------> Variables

        #region -------------------------------------------------> Plot & Menu
        for k,v in self.rData[mConfig.prot.nMod].items():
            #------------------------------> Path
            pathA = k.split(" - ")[0]
            tPath = self.rStepDataP / f'{pathA}_{pathB}'
            #------------------------------> Read and type
            try:
                df = cFile.ReadCSV2DF(tPath/v['R'], header=[0,1,2])
                df.loc[:,colStr] = df.loc[:,colStr].astype('str')               # type: ignore
            except Exception:
                plotData['Error'].append(k)
                continue
            #------------------------------> Add to dict
            plotData[k] = {
                'DF'   : df,
                'F'    : v['F'],
                'Alpha': v['CI']['Alpha'],
            }
        #endregion ----------------------------------------------> Plot & Menu

        return plotData
    #---

    def ConfigureDataLimProt(self) -> dict:
        """Configure a Limited Proteolysis section.

            Returns
            -------
            dict
            {
                'Error': ['Date1',...], # Analysis containing errors.
                'Date1': {
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
                },
                'DateN': {},
            }
        """
        #region ---------------------------------------------------> Variables
        plotData = {}
        plotData['Error'] = []
        pathB = mConfig.limp.nMod.replace(" ", "-")
        #endregion ------------------------------------------------> Variables

        #region -------------------------------------------------> Plot & Menu
        for k,v in self.rData[mConfig.limp.nMod].items():
            #------------------------------>
            pathA = k.split(" - ")[0]
            tPath = self.rStepDataP / f'{pathA}_{pathB}'
            #------------------------------>
            try:
                df = cFile.ReadCSV2DF(tPath/v['R'], header=[0,1,2])
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
            except Exception:
                plotData['Error'].append(k)
                continue
            #------------------------------>
            plotData[k] = {
                'DF': df,
                'PI': PI,
            }
        #endregion ----------------------------------------------> Plot & Menu

        return plotData
    #---

    def ConfigureDataTarProt(self) -> dict:
        """Configure a Targeted Proteolysis section.

            Returns
            ------
            dict
            {
                'Error': ['Date1',...], # Analysis containing errors.
                'Date1': {
                    'DF' : pd.DataFrame with the data to plot,
                    'PI' : { dict with information for the plotting window
                        'Exp'       : list with the experiment's names,
                        'Ctrl'      : name of the control,
                        'Alpha'     : alpha value,
                        'ProtLength': length of the recombinant protein,
                        'ProtLoc'   : list with the location of the native protein,
                        'ProtDelta' : value to calculate native residue numbers as
                                        resN_Nat = resN_Rec + ProtDelta,
                        'Prot'      : name of the Target Protein,
                    },
                    'Cpr': 'File name',
                    'CEvol: 'File name',
                    'AA': {
                        'Date': 'File name',
                        'DateN': 'File name',
                    },
                    'Hist' : {
                        'Date': 'File name',
                        'DateN': 'File name',
                    },
                },
                'DateN': {},
            }
        """
        #region ---------------------------------------------------> Variables
        plotData = {}
        plotData['Error']=[]
        pathB = mConfig.tarp.nMod.replace(" ", "-")
        #endregion ------------------------------------------------> Variables

        #region -------------------------------------------------> Plot & Menu
        for k,v in self.rData[mConfig.tarp.nMod].items():
            #------------------------------>
            pathA = k.split(" - ")[0]
            tPath = self.rStepDataP / f'{pathA}_{pathB}'
            #------------------------------>
            try:
                #------------------------------>
                df  = cFile.ReadCSV2DF(tPath/v['R'], header=[0,1])
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
            except Exception:
                plotData['Error'].append(k)
                continue
            #------------------------------> Add to dict if no error
            plotData[k] = {
                'DF'   : df,
                'PI'   : PI,
                'AA'   : v.get('AA', {}),
                'Hist' : v.get('Hist', {}),
                'CpR'  : v['CpR'],
                'CEvol': v['CEvol'],
            }
        #endregion ----------------------------------------------> Plot & Menu

        return plotData
    #---
    #endregion ----------------------------------------------------> Configure

    #region -----------------------------------------------------> Get Methods
    def GetDataUser(self, tSection:str, tDate:str) -> dict:
        """Get both initial and curated data from the user for the analysis.

            Parameters
            ----------
            tSection: str
                Analysis performed, e.g. 'Correlation Analysis'
            tDate: str
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
        """
        #region ------------------------------------------------> Strip I keys
        i = {k.strip():v
             for k,v in self.rData[tSection][tDate]['I'].items()}
        #endregion ---------------------------------------------> Strip I keys

        return {
            'I'    : i,
            'CI'   : self.rData[tSection][tDate]['CI'],
            'uFile': self.rFileP,
        }
    #---

    def GetRecSeq(self, tSection:str, tDate:str) -> str:
        """Get the recombinant sequence used in an analysis.

            Parameters
            ----------
            tSection: str
                Analysis performed, e.g. 'Correlation Analysis'
            tDate: str
                The date plus user-given Analysis ID
                e.g. '20210325-112056 - bla'

            Returns
            -------
            str
        """
        #region ------------------------------------------------> Path
        fileN = ''
        #------------------------------>
        for k,v in self.rData[tSection][tDate]['I'].items():
            if 'Sequences File' in k:
                fileN = v
                break
        #endregion ---------------------------------------------> Path

        #region --------------------------------------------------->
        seqObj = cFile.FastaFile(self.rInputFileP/fileN)
        #endregion ------------------------------------------------>

        return seqObj.rSeqRec
    #---

    def GetSeq(self, tSection:str, tDate:str) -> tuple[str, str]:
        """Get the sequences used in an analysis.

            Parameters
            ----------
            tSection: str
                Analysis performed, e.g. 'Correlation Analysis'
            tDate: str
                The date plus user-given Analysis ID
                e.g. '20210325-112056 - bla'

            Returns
            -------
            tuple[RecSeq, NatSeq]
        """
        #region ------------------------------------------------> Path
        fileN = ''
        #------------------------------>
        for k,v in self.rData[tSection][tDate]['I'].items():
            if 'Sequences File' in k:
                fileN = v
                break
        #endregion ---------------------------------------------> Path

        #region --------------------------------------------------->
        seqObj = cFile.FastaFile(self.rInputFileP/fileN)
        #endregion ------------------------------------------------>

        return (seqObj.rSeqRec, seqObj.rSeqNat)
    #---

    def GetFAData(
        self,
        tSection:str,
        tDate:str,
        fileN:str,
        header:list[int],
        ) -> pd.DataFrame:
        """Get the data for a Further Analysis section.

            Parameters
            ----------
            tSection: str
                Analysis performed, e.g. 'Correlation Analysis'.
            tDate: str
                The date e.g. '20210325-112056 - bla'.
            fileN: str
                File name with the data.
            header: list[int]
                Header rows in the file.

            Returns
            -------
            pd.DataFrame
        """
        #region --------------------------------------------------->
        pathA = tDate.split(" - ")[0]
        pathB = tSection.replace(" ", "-")
        tPath = self.rStepDataP/f'{pathA}_{pathB}'/fileN
        #endregion ------------------------------------------------>

        return cFile.ReadCSV2DF(tPath, header=header)
    #---

    def GetCleavagePerResidue(self, tSection:str, tDate:str) -> 'pd.DataFrame':
        """Get the Cleavage per residue data.

            Parameters
            ----------
            tSection: str
                Analysis performed, e.g. 'Correlation Analysis'.
            tDate: str
                The date e.g. '20210325-112056 - bla'.

            Returns
            -------
            pd.DataFrame
        """
        #region ---------------------------------------------------> Path
        folder = f'{tDate.split(" - ")[0]}_{tSection.replace(" ", "-")}'
        fileN  = self.rData[tSection][tDate]['CpR']
        fileP  = self.rStepDataP/folder/fileN
        #endregion ------------------------------------------------> Path

        return cFile.ReadCSV2DF(fileP, header=[0,1])
    #---

    def GetCleavageEvolution(self, tSection:str, tDate:str) -> 'pd.DataFrame':
        """Get the Cleavage evolution information.

            Parameters
            ----------
            tSection: str
                Analysis performed, e.g. 'Correlation Analysis'.
            tDate: str
                The date e.g. '20210325-112056 - bla'.

            Returns
            -------
            pd.DataFrame
        """
        #region ---------------------------------------------------> Path
        folder = f'{tDate.split(" - ")[0]}_{tSection.replace(" ", "-")}'
        fileN  = self.rData[tSection][tDate]['CEvol']
        fileP  = self.rStepDataP/folder/fileN
        #endregion ------------------------------------------------> Path

        return cFile.ReadCSV2DF(fileP, header=[0,1])
    #---

    def GetInputFiles(self) -> list[str]:
        """Get a flat list of all input files in self.rData.

            Returns
            -------
            list[str]
                List of the files

            Notes
            -----
            This assumes files are added to I as the first and second items
        """
        #region --------------------------------------------------->
        inputF = []
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        for k,v in self.rData.items():
            for w in v.values():
                iVal = iter(w['I'].values())
                inputF.append(next(iVal))
                if k in self.SeqF:
                    inputF.append(next(iVal))
        #endregion ------------------------------------------------>

        return inputF
    #---
    #endregion --------------------------------------------------> Get Methods
#---
#endregion ----------------------------------------------------------> Classes
