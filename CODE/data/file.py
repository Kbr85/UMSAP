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


"""Classes and methods to handle file/folder input/output operations"""


#region -------------------------------------------------------------> Imports
import json
from pathlib import Path
from typing  import Union, Optional, Literal

import numpy  as np
import pandas as pd
from Bio       import pairwise2
from Bio.Align import substitution_matrices

import config.config  as mConfig
import data.exception as mException
import data.generator as mGenerator
import data.method    as mMethod
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Classes
class PDBFile():
    """Basic class to handle PDB files.

        Parameters
        ----------
        fileP: Path or str
            Path to the PDB file.

        Attributes
        ----------
        cDFAtomCol: list[str]
            Name of the columns in the pd.DataFrame representation of the PDB.
        cPDBformat: str
            Format of the PDB.
        rChain: list[str]
            Chains in the PDB.
        rDFAtom: pd.DataFrame
            DataFrame representation of the PDB. Contains only the ATOM section
            of the PDB.
        rFileP: Path or str
            Path to the PDB file.
    """
    # Test in test.unit.test_file.Test_PDBFile
    #region -----------------------------------------------------> Class setup
    # Col names for the DF with the atom information in the pdb file
    cDFAtomCol = [
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
        'Beta',
        'Segment',
        'Element',
    ]
    #------------------------------>
    cPDBformat = ("{:6s}{:5d} {:^4s}{:1s}{:3s} {:1s}{:4d}{:1s}   {:8.3f}{:8.3f}"
        "{:8.3f}{:6.2f}{:6.2f}      {:4s}{:2s}")
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance Setup
    def __init__(self, fileP: Union[Path, str]) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.rFileP = fileP
        self.ParsePDB()
        #endregion --------------------------------------------> Initial Setup
    #---
    #endregion -----------------------------------------------> Instance Setup

    #region --------------------------------------------------> Manage Methods
    def ParsePDB(self) -> bool:
        """Parse the PDB and create the DataFrame representation.

            Returns
            -------
            bool

            Notes
            -----
            The created DataFrame contains only the ATOM section of the PDB.
        """
        #region --------------------------------------------------->
        ldf = []
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        with open(self.rFileP, 'r', encoding="utf-8") as file:
            for l in file:
                if l[0:4] == 'ATOM':
                    lo = []
                    lo.append(l[ 0: 6].strip())
                    lo.append(int(l[ 6:11].strip()))
                    lo.append(l[12:16].strip())
                    lo.append(l[16].strip())
                    lo.append(l[17:20].strip())
                    lo.append(l[21].strip())
                    lo.append(int(l[22:26].strip()))
                    lo.append(l[26].strip())
                    lo.append(float(l[30:38].strip()))
                    lo.append(float(l[38:46].strip()))
                    lo.append(float(l[46:54].strip()))
                    lo.append(float(l[54:60].strip()))
                    lo.append(float(l[60:66].strip()))
                    lo.append(l[72:76].strip())
                    lo.append(l[76:78].strip())
                    ldf.append(lo)
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        self.rDFAtom = pd.DataFrame(ldf, columns=self.cDFAtomCol)
        self.rChain = self.rDFAtom['Chain'].unique()
        #endregion ------------------------------------------------>

        return True
    #---

    def WritePDB(self, fileP: Union[Path, str], chain: str) -> bool:
        """Write a PDB File.

            Parameters
            ----------
            fileP: Path or str
                Path for the file to be written.
            chain: str
                Chain to write.

            Returns
            -------
            bool
        """
        def Line2PDBFormat(row: np.ndarray, buff):
            """Apply the correct format to the row in the DataFrame and write
                the line to the buffer.

                Parameters
                ----------
                row: np.ndarray
                    Row in the DataFrame as np.ndarray.
                buff:
                    Buffer to write to.

                Returns
                -------
                bool
            """
            buff.write(f'{self.cPDBformat.format(*row)}\n')
        #---
        #region --------------------------------------------------->
        df = self.rDFAtom[self.rDFAtom['Chain'] == chain].copy()
        df = df.replace(np.nan, '')
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        buff = open(fileP, 'w', encoding="utf-8")
        df.apply(Line2PDBFormat, raw=True, axis=1, args=[buff])                 # type: ignore
        buff.write('END')
        buff.close()
        #endregion ------------------------------------------------>

        return True
    #---

    def GetSequence(self, chain: str) -> str:
        """Get the sequence of a chain in the PDB.

            Parameters
            ----------
            chain: str
                Selected chain.

            Returns
            -------
            str
                One letter AA sequence in the selected Chain.
        """
        #region --------------------------------------------------->
        dfd = self.rDFAtom[self.rDFAtom['Chain']==chain]
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        dfd  = dfd.drop_duplicates(subset='ResNum', keep='first', inplace=False)
        dfd  = dfd.loc[dfd.loc[:,'ResName'].isin(mConfig.oAA3toAA)]
        seq = dfd['ResName'].tolist()
        #endregion ------------------------------------------------>

        return "".join([mConfig.oAA3toAA[x] for x in seq])
    #---

    def GetResNum(self, chain: str) -> list:
        """Get the residue number for the selected chain.

            Parameters
            ----------
            chain: str
                Selected chain.

            Returns
            -------
            list
                Residue numbers for the selected chain.
        """
        #region --------------------------------------------------->
        dfd = self.rDFAtom[self.rDFAtom['Chain']==chain]
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        dfd  = dfd.drop_duplicates(subset='ResNum', keep='first', inplace=False)
        #endregion ------------------------------------------------>

        return dfd['ResNum'].tolist()
    #---

    def SetBeta(self, chain: str, beta: dict) -> bool:
        """Set the beta values for the selected chain.

            Parameters
            ----------
            chain: str
                Selected chain.
            beta: dict
                Beta values, keys are residue numbers and values the
                corresponding beta value.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        mask = (
            (self.rDFAtom['Chain']==chain)&(self.rDFAtom['ResNum'].isin(beta)))
        idxR  = self.rDFAtom[mask].index.tolist()
        idxCB = self.rDFAtom.columns.get_loc('Beta')
        idxCR = self.rDFAtom.columns.get_loc('ResNum')
        #endregion ------------------------------------------------>

        #region --------------------------------------------------->
        self.rDFAtom.iloc[idxR, idxCB] = (
            self.rDFAtom.iloc[idxR, idxCR].apply(lambda x: beta[x]))
        #endregion ------------------------------------------------>

        return True
    #---
    #endregion -----------------------------------------------> Manage Methods
#---


class UMSAPFile():
    """Load an UMSAP file.

        Parameters
        ----------
        rFileP : Path
            Path to the UMSAP file

        Attributes
        ----------
        dConfigure : dict
            Configure methods. Keys are the section names as read from the file
        rData : dict
            Data read from json formatted file.
        rFileP : Path
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
    SeqF = [mConfig.nmTarProt, mConfig.nmLimProt]
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, fileP: Path) -> None:
        """ """
        #region ---------------------------------------------------> Read File
        data = ReadJSON(fileP)
        #------------------------------> Sort Keys
        dataKey = sorted([x for x in data.keys()])
        #------------------------------>
        self.rData = {k:data[k] for k in dataKey}
        #endregion ------------------------------------------------> Read File

        #region ---------------------------------------------------> Variables
        self.rFileP = fileP
        self.rStepDataP  = self.rFileP.parent / mConfig.fnDataSteps
        self.rInputFileP = self.rFileP.parent / mConfig.fnDataInit
        #------------------------------>
        self.dConfigure = {# Configure methods. Keys are section names.
            mConfig.nuCorrA   : self.ConfigureDataCorrA,
            mConfig.nuDataPrep: self.ConfigureDataDataPrep,
            mConfig.nmProtProf: self.ConfigureDataProtProf,
            mConfig.nmLimProt : self.ConfigureDataLimProt,
            mConfig.nmTarProt : self.ConfigureDataTarProt,
        }
        #endregion ------------------------------------------------> Variables
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ----------------------------------------------------> Class Method
    def Save(self, tPath: Union[None, str, Path]=None) -> bool:
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
        WriteJSON(oPath, self.rData)
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
        pathB = mConfig.nuCorrA.replace(" ", "-")
        #endregion ------------------------------------------------> Variables

        #region -------------------------------------------------> Plot & Menu
        #------------------------------> Fill
        for k, v in self.rData[mConfig.nuCorrA].items():
            #------------------------------>
            pathA = k.split(" - ")[0]
            tPath = self.rStepDataP / f'{pathA}_{pathB}'
            #------------------------------> Read data
            try:
                df = ReadCSV2DF(tPath/v['R'])
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

    def ConfigureDataDataPrep(self, tSection: str='', tDate: str='') -> dict:
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
        raise mException.InputError(msg)
    #---

    def ConfigureDataDataPrepFromPlot(self, tSection: str, tDate: str) -> dict:
        """Configure a Data Preparation Check section.

            Parameters
            ----------
            tSection: str
                Section name.
            tDate : str
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
        plotData = {}
        plotData['Error'] = []
        pathA = tDate.split(" - ")[0]
        pathB = tSection.replace(" ", "-")
        tPath = self.rStepDataP / f'{pathA}_{pathB}'
        #endregion ------------------------------------------------> Variables

        #region -------------------------------------------------> Plot & Menu
        try:
            plotData[tDate] = {
                'DP': {j:ReadCSV2DF(tPath/w) for j,w in self.rData[tSection][tDate]['DP'].items()},
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
        pathB = mConfig.nuDataPrep.replace(" ", "-")
        #endregion ------------------------------------------------> Variables

        #region -------------------------------------------------> Plot & Menu
        for k,v in self.rData[mConfig.nuDataPrep].items():
            #------------------------------> Read and type
            try:
                pathA = k.split(" - ")[0]
                tPath = self.rStepDataP / f'{pathA}_{pathB}'
            except Exception:
                plotData['Error'].append(k)
                continue
            #------------------------------> Add to dict
            plotData[k] = {
                'DP' : {j:ReadCSV2DF(tPath/w) for j,w in v['DP'].items()},
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
        pathB  = mConfig.nmProtProf.replace(" ", "-")
        #endregion ------------------------------------------------> Variables

        #region -------------------------------------------------> Plot & Menu
        for k,v in self.rData[mConfig.nmProtProf].items():
            #------------------------------> Path
            pathA = k.split(" - ")[0]
            tPath = self.rStepDataP / f'{pathA}_{pathB}'
            #------------------------------> Read and type
            try:
                df = ReadCSV2DF(tPath/v['R'], header=[0,1,2])
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
        pathB = mConfig.nmLimProt.replace(" ", "-")
        #endregion ------------------------------------------------> Variables

        #region -------------------------------------------------> Plot & Menu
        for k,v in self.rData[mConfig.nmLimProt].items():
            #------------------------------>
            pathA = k.split(" - ")[0]
            tPath = self.rStepDataP / f'{pathA}_{pathB}'
            #------------------------------>
            try:
                df = ReadCSV2DF(tPath/v['R'], header=[0,1,2])
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
        pathB = mConfig.nmTarProt.replace(" ", "-")
        #endregion ------------------------------------------------> Variables

        #region -------------------------------------------------> Plot & Menu
        for k,v in self.rData[mConfig.nmTarProt].items():
            #------------------------------>
            pathA = k.split(" - ")[0]
            tPath = self.rStepDataP / f'{pathA}_{pathB}'
            #------------------------------>
            try:
                #------------------------------>
                df  = ReadCSV2DF(tPath/v['R'], header=[0,1])
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
    def GetDataUser(self, tSection: str, tDate: str) -> dict:
        """Get both initial and curated data from the user for the analysis.

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

    def GetRecSeq(self, tSection: str, tDate: str) -> str:
        """Get the recombinant sequence used in an analysis.

            Parameters
            ----------
            tSection: str
                Analysis performed, e.g. 'Correlation Analysis'
            tDate : str
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
        seqObj = FastaFile(self.rInputFileP/fileN)
        #endregion ------------------------------------------------>

        return seqObj.rSeqRec
    #---

    def GetSeq(self, tSection: str, tDate: str) -> tuple[str, str]:
        """Get the sequences used in an analysis.

            Parameters
            ----------
            tSection: str
                Analysis performed, e.g. 'Correlation Analysis'
            tDate : str
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
        seqObj = FastaFile(self.rInputFileP/fileN)
        #endregion ------------------------------------------------>

        return (seqObj.rSeqRec, seqObj.rSeqNat)
    #---

    def GetFAData(
        self,
        tSection: str,
        tDate   : str,
        fileN   : str,
        header  : list[int],
        ) -> 'pd.DataFrame':
        """Get the data for a Further Analysis section.

            Parameters
            ----------
            tSection: str
                Analysis performed, e.g. 'Correlation Analysis'.
            tDate : str
                The date e.g. '20210325-112056 - bla'.
            fileN : str
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

        return ReadCSV2DF(tPath, header=header)
    #---

    def GetCleavagePerResidue(self, tSection:str, tDate:str) -> 'pd.DataFrame':
        """Get the Cleavage per residue data.

            Parameters
            ----------
            tSection: str
                Analysis performed, e.g. 'Correlation Analysis'.
            tDate : str
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

        return ReadCSV2DF(fileP, header=[0,1])
    #---

    def GetCleavageEvolution(self, tSection:str, tDate:str) -> 'pd.DataFrame':
        """Get the Cleavage evolution information.

            Parameters
            ----------
            tSection: str
                Analysis performed, e.g. 'Correlation Analysis'.
            tDate : str
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

        return ReadCSV2DF(fileP, header=[0,1])
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
