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
from typing import Union, Optional, Literal

import pandas as pd
from Bio import pairwise2
from Bio.Align import substitution_matrices

import config.config as mConfig
import data.exception as mException
import data.generator as mGenerator
import data.method as mMethod
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Methods
def ReadJSON(fileP: Union[Path, str]) -> dict:
    """Reads a file with a json format.

        Parameters
        ----------
        fileP: Path, str
            Path to the file

        Return
        ------
        dict:
            Data in the file
    """
    #region -------------------------------------------------------> Read file
    with open(fileP, 'r') as file:
        data = json.load(file)
    #endregion ----------------------------------------------------> Read file

    return data
#---


def ReadFileFirstLine(
    fileP: Union[Path, str],
    char: str='\t', 
    empty: bool=False
    ) -> list[str]:
    """Custom method to read the first line in a file.

        Parameters
        ----------
        fileP : path or str
            File path of the file to be read 
        char : str
            each line in the file is splitted using the value of char or not if 
            char is empty.
        empty : boolean
            Return first non-empty line (True) or first line (False).

        Returns
        -------
        list of list
            List of list containing the lines in the read file like:
            [['first', 'line'], ['second', 'line'], ... , ['last', 'line']]

        Notes
        -----
        The method returns a list containing the first line in the file. 
        The line is splitted using char. The first non-empty line is returned if
        empty is False, otherwise the first line is returned. 
        If the file is empty an empty line is returned.
    """
    #region --------------------------------------------> Read and split lines
    with open(fileP, 'r') as file:
        for line in file:
            #--> To remove ' ', \n, \t & \r from start/end of line
            l = line.strip()
            #------------------------------> Return first line
            if l == '' and not empty:
                #------------------------------> Discard empty
                continue
            else:
                #------------------------------> Set data
                if char:
                    return l.split(char)
                else:
                    return [l]
    #------------------------------> If file is empty then return
    return []
    #endregion -----------------------------------------> Read and split lines
#---


def ReadCSV2DF(
    fileP: Union[Path, str],
    sep: str='\t',
    index_col: Optional[int]=None,
    header: Union[int, list[int], None, Literal['infer']]='infer',
    ) -> pd.DataFrame:
    """Reads a csv file and returns a pandas dataframe.

        Parameters
        ----------
        fileP : str or Path
            Path to the file.
        sep : str
            Column separator in the CSV file. Default is tab.
        index_col : int or None
            Index of the column names.
        header : int, list[int], None
            Use list[int] for multi index columns.

        Returns
        -------
        dataframe:
            Pandas dataframe with the data.

        Raise
        -----
        ExecutionError:
            - When the file could not be read.
    """
    #region -------------------------------------------------------> Read file
    return pd.read_csv(
        str(fileP), sep=sep, index_col=index_col, header=header)
    #endregion ----------------------------------------------------> Read file
#---


def WriteJSON(fileP: Union[Path, str], data: dict) -> bool:
    """ Writes a json file.

        Parameters
        ----------
        fileP : str or Path 
            Path to the file.
        data: dict
            Data to be written.

        Return
        ------
        bool

        Raise
        -----
        ExecutionError:
            - When the file could not be written
    """
    #region ---------------------------------------------------> Write to file
    with open(fileP, 'w') as file:
        json.dump(data, file, indent=4)
    #endregion ------------------------------------------------> Write to file

    return True
#---


def WriteDF2CSV(
    fileP: Union[Path, str], 
    df: pd.DataFrame, 
    sep: str='\t', 
    na_rep: str='NA', 
    index: bool=False
    ) -> bool:
    """ Writes a dataframe to csv formatted file .

        Parameters
        ----------
        fileP: str or Path 
            Path to the file
        df: pd.DataFrame
            Data frame to be written
        sep : str
            Character to separate columns in the csv file
        na_rep : str
            Character to represent NA values
        index: boolean 
            Write index columns
    """
    #region ---------------------------------------------------> Write to file
    df.to_csv(str(fileP), sep=sep, na_rep=na_rep, index=index)
    return True
    #endregion ------------------------------------------------> Write to file
#---


def WriteDFs2CSV(
    baseP: Path,
    ncDict: dict[str, pd.DataFrame],
    sep: str='\t',
    na_rep: str='NA',
    index: bool=False
    ) -> bool:
    """Write several pd.DataFrames to baseP as CSV files. 

        Parameters
        ----------
        baseP : Path
            Folder in which all files will be saved.
        ncDict : dict
            Keys are file names and values the pd.DataFrames.
        sep : str
            Character to separate columns in the csv file.
        na_rep : str
            Character to represent NA values.
        index: boolean 
            Write index columns

        Notes
        -----
        Existing files will be overwritten if needed.
    """
    #region ---------------------------------------------------> Write to file
    for k,i in ncDict.items():
        fileP = baseP / k
        WriteDF2CSV(fileP, i, sep=sep, na_rep=na_rep, index=index)
    #endregion ------------------------------------------------> Write to file

    return True
#---
#endregion ----------------------------------------------------------> Methods


#region -------------------------------------------------------------> Classes
class CSVFile():
    """Class to deal with csv formatted input files.

        Parameters
        ----------
        fileP : str or Path
            Path to the input file.
        sep : str
            Column separator character in the csv file.

        Attributes
        ----------
        rDf : pd.DataFrame
            Copy of the df in the file that can be modified.
        rData : pd.DataFrame
            This is the initial data and will not be modified. It is just to 
            read from if needed.
        rFileP : str or Path
            Path to the csv file.
        rHeader : list
            List with the names of the columns in the csv file. It is assumed 
            the names are in the first row of the file.
        rNRow, rNCol : int
            Number of rows and columns in self.rData

        Raises
        ------
        FileIOError:
            - When fileP cannot be read

        Notes
        -----
        It is assumed the csv file has column names in the first row.
        """
    #region --------------------------------------------------> Instance setup
    def __init__(
        self,
        fileP: Union[Path, str],
        sep: str="\t",
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.rFileP = fileP
        #endregion --------------------------------------------> Initial Setup

        #region ---------------------------------------------------> Read File
        self.rData = ReadCSV2DF(self.rFileP, sep=sep)
        #endregion ------------------------------------------------> Read File

        #region ---------------------------------------------------> Variables
        self.SetAttributes()
        #endregion ------------------------------------------------> Variables
        #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def SetAttributes(self) -> bool:
        """ Set other variables needed by the class.

            Returns
            -------
            bool
        """
        #--> list with the name of the columns in the data file
        self.rHeader = list(self.rData.columns)
        #--> copy of self.rData to modify it without altering the original data
        self.rDf = self.rData.copy()
        #--> nRows, nCols
        self.rNRow, self.rNCol = self.rDf.shape

        return True
    #---

    def StrInCol(self, tStr:str, col:int, comp: Literal['e', 'ne']='e') -> bool:
        """Basically check if str is in col.

            Parameters
            ----------
            tStr: str
                String to look for.
            col: int
                Column containing the string.
            comp: str
                One of 'e', 'ne'. Equal or not Equal.

            Returns
            -------
            bool
        """
        df = mMethod.DFFilterByColS(self.rData, col, tStr, comp=comp)
        return not df.empty
    #---
    #endregion ------------------------------------------------> Class methods
#---


class FastaFile():
    """Class to handle fasta files.

        Parameters
        ----------
        fileP: Path or str
            Path to the fasta file.

        Attributes
        ----------
        rAlignment: BioPython alignment or None
            Last calculated alignment.
        rFileP: Path or str
            Path to the fasta file.
        rHeaderNat: str
            Header for the Native sequence.
        rHeaderRec: str
            Header for the Recombinant sequence.
        rSeqLengthNat: int or None
            Length of the Native sequence.
        rSeqLengthRec: int
            Length of the Recombinant sequence.
        rSeqNat: str
            Sequence of the Native sequence.
        rSeqRec: str
            Sequence of the Recombinant sequence.
    """
    #region --------------------------------------------------> Instance setup
    def __init__(self, fileP: Union[Path, str]) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        #------------------------------>
        self.rFileP = fileP
        #------------------------------>
        gen = mGenerator.FastaSequence(fileP)
        #------------------------------>
        self.rHeaderRec, self.rSeqRec = next(gen)
        self.rSeqLengthRec = len(self.rSeqRec)
        #------------------------------>
        try:
            self.rHeaderNat, self.rSeqNat = next(gen)
        except StopIteration:
            self.rHeaderNat, self.rSeqNat, self.rSeqLengthNat = ('', '', None)
        except Exception:
            msg = (f'There was an unexpected error when parsing the fasta '
                f'file.\n{fileP}')
            raise mException.UnexpectedError(msg)
        else:
            self.rSeqLengthNat = len(self.rSeqNat)
        #------------------------------> 
        self.rAlignment = None
        #endregion --------------------------------------------> Initial Setup
        #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def FindSeq(self, seq: str, seqRec: bool=True) -> tuple[int, int]:
        """Find the location of seq in the sequence of the Rec or Nat Protein.

            Parameters
            ----------
            seq : str
                Peptide sequence to find in the Protein sequence
            seqRec: bool
                Search on the recombinant (True) or native sequence (False).

            Returns
            -------
            tuple[int, int]
                The N and C residue numbers of seq in the protein sequence.

            Raises
            ------
            ExecutionError:
                - when seqRec is False but self.seqNat is None.

            Notes
            -----
            [-1, -1] is returned if seq is not found inside the protein 
            sequence.
        """
        #region -------------------------------------------------> Check Input
        if not self.rSeqNat and not seqRec:
            msg = ("The Native sequence of the protein is undefined. The "
                "peptide sequence can only be searched for in the "
                "Recombinant sequence")
            raise mException.ExecutionError(msg)
        else:
            pass
        #endregion ----------------------------------------------> Check Input

        #region ------------------------------------------------------> Find N
        #------------------------------>
        n = self.rSeqRec.find(seq) if seqRec else self.rSeqNat.find(seq)
        #------------------------------>
        if n != -1:
            n = n + 1
        else:
            return (-1, -1)
        #endregion ---------------------------------------------------> Find N

        #region ------------------------------------------------------> Find C
        c = n + len(seq) - 1
        #endregion ---------------------------------------------------> Find C

        return (n, c)
    #---
    
    def CalculateAlignment(self, seqA: str, seqB: str):
        """Calculate the sequence alignment between both sequences.

            Parameters
            ----------
            seqA: str
                Reference sequence.
            seqB: str
                Second sequence.

            Returns
            -------
            BioPython Alignment
        """
        #region -----------------------------------------------> Blosum matrix
        blosum62 = substitution_matrices.load("BLOSUM62")
        #endregion --------------------------------------------> Blosum matrix

        #region ---------------------------------------------------> Alignment
        return pairwise2.align.globalds(seqA, seqB, blosum62, -10, -0.5) # type: ignore
        #endregion ------------------------------------------------> Alignment
    #---

    def SetSelfAlignment(self) -> bool:
        """Calculate the sequence alignment between the Recombinant and Native
            sequences.

            Returns
            -------
            bool

            Raise
            -----
            InputError if self.rSeqNat is empty.
        """
        #region ---------------------------------------------------> 
        if not self.rSeqNat:
            msg = (f'It is not possible to calculate the sequence alignment '
                f'because the Fasta file contains only one sequence.')
            raise mException.ExecutionError(msg)
        else:
            pass
        #endregion ------------------------------------------------> 

        #region ---------------------------------------------------> Alignment
        if getattr(self, 'rAlignment', None) is None:
            self.rAlignment = self.CalculateAlignment(self.rSeqRec,self.rSeqNat)
        else:
            pass
        #endregion ------------------------------------------------> Alignment

        return True
    #---

    def GetSelfAlignment(self):
        """Get the alignment between the Recombinant and Native sequence.

            Returns
            -------
            BioPython alignment.
        """
        #region ---------------------------------------------------> Alignment
        if getattr(self, 'rAlignment', None) is None:
            self.SetSelfAlignment()
        else:
            pass
        #endregion ------------------------------------------------> Alignment

        return self.rAlignment
    #---

    def GetSelfDelta(self) -> int:
        """Get Residue number difference between the Recombinant and Native
            sequence.

            Returns
            -------
            int
        """
        #region ---------------------------------------------------> Alignment
        alignment = self.GetSelfAlignment()
        seqB = alignment[0].seqB # type: ignore
        #endregion ------------------------------------------------> Alignment

        #region ---------------------------------------------------> Get delta
        for k,l in enumerate(seqB):
            if l == '-':
                pass
            else:
                return -1 * k
        #------------------------------>
        return 0 # ProtRec and ProtNat are the same
        #endregion ------------------------------------------------> Get delta
    #---

    def GetNatProtLoc(self) -> tuple[int, int]:
        """Get the location of the Native sequence inside the Recombinant
            sequence.

            Returns
            -------
            tuple
                First and last residue.
        """
        #region ---------------------------------------------------> Alignment
        alignment = self.GetSelfAlignment()
        seqB = alignment[0].seqB # type: ignore
        #endregion ------------------------------------------------> Alignment

        #region -------------------------------------------> Get Left Position
        ll = None
        #------------------------------> 
        for k,l in enumerate(seqB, start=1):
            if l == '-':
                pass
            else:
                ll = k 
                break
        #------------------------------> 
        ll = 1 if ll is None else ll
        #endregion ----------------------------------------> Get Left Position

        #region ------------------------------------------> Get Right Position
        lr = None
        #------------------------------> 
        for k,l in reversed(list(enumerate(seqB, start=1))):
            if l == '-':
                pass
            else:
                lr = k
                break
        #------------------------------> 
        lr = self.rSeqLengthRec if lr is None else lr
        #endregion ---------------------------------------> Get Right Position

        return (ll, lr)
    #---
    #endregion ------------------------------------------------> Class methods
#---


class UMSAPFile():
    """Load an UMSAP file.

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
        self.rData = {}
        for k in dataKey:
            self.rData[k] = data[k]
        #endregion ------------------------------------------------> Read File

        #region ---------------------------------------------------> Variables
        self.rFileP = Path(fileP)
        self.rStepDataP  = self.rFileP.parent / mConfig.fnDataSteps
        self.rInputFileP = self.rFileP.parent / mConfig.fnDataInit

        self.dConfigure = {# Configure methods. Keys are the section names as
                           # read from the file
            # config.nuCorrA   : self.ConfigureDataCorrA,
            # config.nuDataPrep: self.ConfigureDataCheckDataPrep,
            # config.nmProtProf: self.ConfigureDataProtProf,
            # config.nmLimProt : self.ConfigureDataLimProt,
            # config.nmTarProt : self.ConfigureDataTarProt,
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
#     def ConfigureDataCorrA(self) -> dict:
#         """Configure a Correlation Analysis section	
        
#             Returns
#             ------
#             dict
#             {
#                 'DF' : pd.DataFrame with the data to plot,
#                 'NumCol' : number of columns in 'DF',
#                 'NumColList' : List with the number of the columns,
#             }
#         """
#         #region -------------------------------------------------> Plot & Menu
#         #------------------------------> Empty start
#         plotData = {'Error':[]}
#         #------------------------------> Fill
#         for k,v in self.rData[config.nuCorrA].items():
#             #------------------------------> 
#             tPath = self.rStepDataP / f'{k.split(" - ")[0]}_{config.nuCorrA.replace(" ", "-")}'
#             #------------------------------> 
#             try:
#                 #------------------------------> Create data
#                 df = dtsFF.ReadCSV2DF(tPath/v['R'])
                
#                 if (numCol := len(v['CI']['oc']['Column'])) == df.shape[0]:
#                     pass
#                 else:
#                     continue
#                 #------------------------------> Add to dict if no error
#                 plotData[k] = {
#                     'DF'     : df,
#                     'NumCol' : numCol,
#                     'NumColList': v['CI']['oc']['Column'],
#                 }
#             except Exception:
#                 plotData['Error'].append(k)
#         #endregion ----------------------------------------------> Plot & Menu
        
#         return plotData
#     #---
    
#     def ConfigureDataCheckDataPrep(
#         self, tSection: Optional[str]=None, tDate: Optional[str]=None
#         ) -> dict:
#         """Configure a Data Preparation Check section	
        
#             Parameters
#             ----------
#             tSection: str or None
#                 Section name. Default is None
#             tDate : str or None
#                 Date and comment. Default is None
        
#             Returns
#             -------
#             dict
#             {
#                 'DP' : dict with the data preparation steps key are the step's
#                         names and values the pd.DataFrame,
#             }
#         """
#         if tSection is None and tDate is None:
#             return self.ConfigureDataCheckDataPrepFromUMSAP()
#         elif tSection is not None and tDate is not None:
#             return self.ConfigureDataCheckDataPrepFromPlot(tSection, tDate)
#         else:
#             msg = (f'Both tSection ({tSection}) and tDate ({tDate}) must be '
#                    f'None or be defined.')
#             raise dtsException.InputError(msg)
#     #---
    
#     def ConfigureDataCheckDataPrepFromPlot(
#         self, tSection: str, tDate: str,
#         ) -> dict:
#         """Configure a Data Preparation Check section	
        
#             Parameters
#             ----------
#             tSection: str
#                 Section name
#             tDate : str
#                 Date and comment
        
#             Returns
#             -------
#             dict
#             {
#                 'DP' : dict with the data preparation steps key are the step's
#                         names and values the pd.DataFrame,
#             }
#         """
#         #region ---------------------------------------------------> Variables
#         plotData = {}
#         tPath = self.rStepDataP / f'{tDate.split(" - ")[0]}_{tSection.replace(" ", "-")}'
#         #endregion ------------------------------------------------> Variables

#         #region -------------------------------------------------> Plot & Menu
#         try:
#             plotData[tDate] = {
#                 'DP': {j:dtsFF.ReadCSV2DF(tPath/w) for j,w in self.rData[tSection][tDate]['DP'].items()},
#                 'NumColList': self.rData[tSection][tDate]['CI']['oc']['Column'],
#             }
#         except Exception as e:
#             pass        
#         #endregion ----------------------------------------------> Plot & Menu
        
#         return plotData
#     #---
    
#     def ConfigureDataCheckDataPrepFromUMSAP(self) -> dict:
#         """Configure a Data Preparation Check section	
        
#             Returns
#             -------
#             dict
#             {
#                 'DP' : dict with the data preparation steps key are the step's
#                         names and values the pd.DataFrame,
#             }
#         """
#         #region ---------------------------------------------------> Variables
#         plotData = {'Error':[]}
#         #endregion ------------------------------------------------> Variables

#         #region -------------------------------------------------> Plot & Menu        
#         for k,v in self.rData[config.nuDataPrep].items():
#             try:
#                 #------------------------------> 
#                 tPath = self.rStepDataP / f'{k.split(" - ")[0]}_{config.nuDataPrep.replace(" ", "-")}'
#                 #------------------------------> Add to dict
#                 plotData[k] = {
#                     'DP' : {j:dtsFF.ReadCSV2DF(tPath/w) for j,w in v['DP'].items()},
#                     'NumColList': v['CI']['oc']['Column'],
#                 }
#             except Exception:
#                 plotData['Error'].append(k)
#         #endregion ----------------------------------------------> Plot & Menu
        
#         return plotData
#     #---
    
#     def ConfigureDataProtProf(self) -> dict:
#         """Configure a Proteome Profiling section
        
#             Returns
#             ------
#             dict
#             {
#                 'DF' : pd.DataFrame with the data to plot,
#             }
#         """
#         #region -------------------------------------------------> Plot & Menu
#         #------------------------------> Empty start
#         plotData = {'Error':[]}
#         colStr = [('Gene','Gene','Gene'),('Protein','Protein','Protein')]
#         #------------------------------> Fill
#         for k,v in self.rData[config.nmProtProf].items():
#             try:
#                 #------------------------------> 
#                 tPath = self.rStepDataP / f'{k.split(" - ")[0]}_{config.nmProtProf.replace(" ", "-")}'
#                 #------------------------------> Create data
#                 df = dtsFF.ReadCSV2DF(tPath/v['R'], header=[0,1,2])
#                 df.loc[:,colStr] = df.loc[:,colStr].astype('str')
#                 #------------------------------> Add to dict if no error
#                 plotData[k] = {
#                     'DF': df,
#                     'F' : v['F'],
#                     'Alpha': v['CI']['Alpha'],
#                 }
#             except Exception:
#                 plotData['Error'].append(k)
#         #endregion ----------------------------------------------> Plot & Menu
        
#         return plotData
#     #---
    
#     def ConfigureDataLimProt(self) -> dict:
#         """Configure a Limited Proteolysis section
        
#             Returns
#             -------
#             dict
#             {
#                 'DF' : pd.DataFrame with the data to plot,
#                 'PI' : { dict with information for the plotting window
#                     'Bands'     : list with the band's names,
#                     'Lanes'     : list with the lane's names,
#                     'Alpha'     : alpha value,
#                     'ProtLength': length of the recombinant protein,
#                     'ProtLoc'   : list with the location of the native protein,
#                     'ProtDelta' : value to calculate native residue numbers as
#                                     resN_Nat = resN_Rec + ProtDelta,
#                     'Prot'      : name of the Target Protein,
#                 },
#             }
#         """
#         #region -------------------------------------------------> Plot & Menu
#         #------------------------------> Empty start
#         plotData = {'Error':[]}
#         #------------------------------> Fill
#         for k,v in self.rData[config.nmLimProt].items():
#             try:
#                 #------------------------------> 
#                 tPath = self.rStepDataP / f'{k.split(" - ")[0]}_{config.nmLimProt.replace(" ", "-")}'
#                 #------------------------------> Create data
#                 df  = dtsFF.ReadCSV2DF(tPath/v['R'], header=[0,1,2])
#                 #------------------------------> Plot Info
#                 PI = {
#                     'Bands'     : v['CI']['Band'],
#                     'Lanes'     : v['CI']['Lane'],
#                     'Alpha'     : v['CI']['Alpha'],
#                     'ProtLength': v['CI']['ProtLength'],
#                     'ProtLoc'   : v['CI']['ProtLoc'],
#                     'ProtDelta' : v['CI']['ProtDelta'],
#                     'Prot'      : v['CI']['TargetProt'],
#                 }
#                 #------------------------------> Add to dict if no error
#                 plotData[k] = {
#                     'DF': df,
#                     'PI': PI,
#                 }
#             except Exception:
#                 plotData['Error'].append(k)
#         #endregion ----------------------------------------------> Plot & Menu
        
#         return plotData
#     #---
    
#     def ConfigureDataTarProt(self) -> dict:
#         """Configure a Targeted Proteolysis section
        
#             Returns
#             ------
#             dict
#             {
#                 'DF' : pd.DataFrame with the data to plot,
#                 'PI' : { dict with information for the plotting window
#                     'Exp'       : list with the experiment's names,
#                     'Alpha'     : alpha value,
#                     'ProtLength': length of the recombinant protein,
#                     'ProtLoc'   : list with the location of the native protein,
#                     'ProtDelta' : value to calculate native residue numbers as
#                                     resN_Nat = resN_Rec + ProtDelta,
#                     'Prot'      : name of the Target Protein,
#                 },
#             }
#         """
#         #region -------------------------------------------------> Plot & Menu
#         #------------------------------> Empty start
#         plotData = {'Error':[]}
#         #------------------------------> Fill
#         for k,v in self.rData[config.nmTarProt].items():
#             try:
#                 #------------------------------> 
#                 tPath = self.rStepDataP / f'{k.split(" - ")[0]}_{config.nmTarProt.replace(" ", "-")}'
#                 #------------------------------> Create data
#                 df  = dtsFF.ReadCSV2DF(tPath/v['R'], header=[0,1])
#                 #------------------------------> Plot Info
#                 PI = {
#                     'Exp'       : v['CI']['Exp'],
#                     'Ctrl'      : v['CI']['ControlL'],
#                     'Alpha'     : v['CI']['Alpha'],
#                     'ProtLength': v['CI']['ProtLength'],
#                     'ProtLoc'   : v['CI']['ProtLoc'],
#                     'ProtDelta' : v['CI']['ProtDelta'],
#                     'Prot'      : v['CI']['TargetProt'],
#                 }
#                 #------------------------------> Add to dict if no error
#                 plotData[k] = {
#                     'DF'   : df,
#                     'PI'   : PI,
#                     'AA'   : v.get('AA', {}),
#                     'Hist' : v.get('Hist', {}),
#                     'CpR'  : v['CpR'],
#                     'CEvol': v['CEvol'],
#                 }
#             except Exception:
#                 plotData['Error'].append(k)
#         #endregion ----------------------------------------------> Plot & Menu
        
#         return plotData
#     #---
    #endregion ----------------------------------------------------> Configure
    
    #region -----------------------------------------------------> Get Methods
#     def GetSectionCount(self) -> int:
#         """Get the total number of sections in file

#             Returns
#             -------
#             int:
#                 Number of sections in the file	
#         """
#         return len(self.rData.keys())
#     #---

#     def GetSectionData(self, tSection: str) -> dict:
#         """Get the dict with the data for a section
    
#             Parameters
#             ----------
#             tSection : str
#                 Section name like in config.Modules or config.Utilities
    
#             Returns
#             -------
#             dict:
#                 Section data

#             Raise
#             -----
#             ExecutionError
#                 - When the section is not found in the file
#         """
#         if (data := self.rData.get(tSection, {})):
#             return data
#         else:
#             msg = (
#                 f"Section {tSection} was not found in the content of "
#                 f"file:\n{self.rFileP}"
#             )
#             raise dtsException.ExecutionError(msg)
#     #---

#     def GetDataI(self, tSection: str, tDate: str) -> dict:
#         """ Get initial user input for one analysis
    
#             Parameters
#             ----------
#             tSection: str
#                 Analysis performed, e.g. 'Correlation Analysis'
#             tDate : str
#                 The date plus user-given Analysis ID 
#                 e.g. '20210325-112056 - bla'
    
#             Returns
#             -------
#             dict
    
#             Raise
#             -----
#             KeyError:
#                 When tSection or tDate is not found in the file
#         """
#         try:
#             return self.rData[tSection][tDate]['I']
#         except KeyError as e:
#             raise e
#     #---
    
#     def GetDataCI(self, tSection: str, tDate: str) -> dict:
#         """ Get curated user input for one analysis
    
#             Parameters
#             ----------
#             tSection: str
#                 Analysis performed, e.g. 'Correlation Analysis'
#             tDate : str
#                 The date plus user-given Analysis ID 
#                 e.g. '20210325-112056 - bla'
    
#             Returns
#             -------
#             dict
    
#             Raise
#             -----
#             KeyError:
#                 When tSection or tDate is not found in the file
#         """
#         try:
#             return self.rData[tSection][tDate]['CI']
#         except KeyError as e:
#             raise e
#     #---
    
#     def GetDataUser(self, tSection: str, tDate: str) -> dict:
#         """ Get both initial and curated data from the user for the analysis
    
#             Parameters
#             ----------
#             tSection: str
#                 Analysis performed, e.g. 'Correlation Analysis'
#             tDate : str
#                 The date plus user-given Analysis ID 
#                 e.g. '20210325-112056 - bla'
    
#             Returns
#             -------
#             dict:
#                 {
#                     'I' : user input with stripped keys,
#                     'CI': corrected user input,
#                     'rootP' : path to the folder containing the UMSAP file,
#                 }
    
#             Raise
#             -----
#             KeyError:
#                 When tSection or tDate is not found in the file
#         """
#         #region ------------------------------------------------> Strip I keys
#         #------------------------------> 
#         i = {}
#         #------------------------------> 
#         for k,v in self.rData[tSection][tDate]['I'].items():
#             i[k.strip()] = v
#         #endregion ---------------------------------------------> Strip I keys
        
#         try:
#             return {
#                 'I'    : i,
#                 'CI'   : self.rData[tSection][tDate]['CI'],
#                 'uFile': self.rFileP,
#             }
#         except KeyError as e:
#             raise e
#     #---
    
#     def GetRecSeq(self, tSection: str, tDate: str) -> str:
#         """ Get the recombinant sequence used in an analysis.
    
#             Parameters
#             ----------
#             tSection: str
#                 Analysis performed, e.g. 'Correlation Analysis'
#             tDate : str
#                 The date plus user-given Analysis ID 
#                 e.g. '20210325-112056 - bla'
    
#             Returns
#             -------
#             str
    
#             Raise
#             -----
#             KeyError:
#                 When tSection or tDate is not found in the file
#         """
#         #region ------------------------------------------------> Path
#         for k,v in self.rData[tSection][tDate]['I'].items():
#             if 'Sequences File' in k:
#                 fileN = v
#                 break
#             else:
#                 pass
#         #endregion ---------------------------------------------> Path
        
#         #region ---------------------------------------------------> 
#         seqObj = dtsFF.FastaFile(self.rInputFileP/fileN)
        
#         return seqObj.seqRec
#         #endregion ------------------------------------------------> 
#     #---
    
#     def GetNatSeq(self, tSection: str, tDate: str) -> str:
#         """ Get the native sequence used in an analysis.
    
#             Parameters
#             ----------
#             tSection: str
#                 Analysis performed, e.g. 'Correlation Analysis'
#             tDate : str
#                 The date plus user-given Analysis ID 
#                 e.g. '20210325-112056 - bla'
    
#             Returns
#             -------
#             str
    
#             Raise
#             -----
#             KeyError:
#                 When tSection or tDate is not found in the file
#         """
#         #region ------------------------------------------------> Path
#         for k,v in self.rData[tSection][tDate]['I'].items():
#             if 'Sequences File' in k:
#                 fileN = v
#                 break
#             else:
#                 pass
#         #endregion ---------------------------------------------> Path
        
#         #region ---------------------------------------------------> 
#         seqObj = dtsFF.FastaFile(self.rInputFileP/fileN)
        
#         return seqObj.seqNat
#         #endregion ------------------------------------------------> 
#     #---
    
#     def GetSeq(self, tSection: str, tDate: str) -> tuple[str, str]:
#         """Get the sequences used in an analysis.
    
#             Parameters
#             ----------
#             tSection: str
#                 Analysis performed, e.g. 'Correlation Analysis'
#             tDate : str
#                 The date plus user-given Analysis ID 
#                 e.g. '20210325-112056 - bla'
    
#             Returns
#             -------
#             tuple[RecSeq, NatSeq]
    
#             Raise
#             -----
#             KeyError:
#                 When tSection or tDate is not found in the file
#         """
#         #region ------------------------------------------------> Path
#         for k,v in self.rData[tSection][tDate]['I'].items():
#             if 'Sequences File' in k:
#                 fileN = v
#                 break
#             else:
#                 pass
#         #endregion ---------------------------------------------> Path
        
#         #region ---------------------------------------------------> 
#         seqObj = dtsFF.FastaFile(self.rInputFileP/fileN)
        
#         return (seqObj.seqRec, seqObj.seqNat) 
#         #endregion ------------------------------------------------> 
#     #---
    
#     def GetFAData(
#         self, tSection: str, tDate: str, fileN: str, header: list[int]
#         ) -> 'pd.DataFrame':
#         """Get the data for a Further Analysis section
    
#             Parameters
#             ----------
#             tSection: str
#                 Analysis performed, e.g. 'Correlation Analysis'
#             tDate : str
#                 The date plus user-given Analysis ID 
#                 e.g. '20210325-112056 - bla'
#             fileN : str
#                 File name with the data
#             header: list[int]
#                 Header rows in the file
    
#             Returns
#             -------
#             pd.DataFrame
#         """
#         tPath = (
#             self.rStepDataP/f'{tDate.split(" - ")[0]}_{tSection.replace(" ", "-")}'/fileN
#         )
#         return dtsFF.ReadCSV2DF(tPath, header=header)
#     #---
    
#     def GetCleavagePerResidue(self, tSection:str, tDate:str) -> 'pd.DataFrame':
#         """
    
#             Parameters
#             ----------
            
    
#             Returns
#             -------
            
    
#             Raise
#             -----
            
#         """
        
#         #region ---------------------------------------------------> Path
#         folder = f'{tDate.split(" - ")[0]}_{tSection.replace(" ", "-")}'
#         fileN = self.rData[tSection][tDate]['CpR']
#         fileP = self.rStepDataP/folder/fileN
#         #endregion ------------------------------------------------> Path

#         return dtsFF.ReadCSV2DF(fileP, header=[0,1])
#     #---
    
#     def GetCleavageEvolution(self, tSection:str, tDate:str) -> 'pd.DataFrame':
#         """
    
#             Parameters
#             ----------
            
    
#             Returns
#             -------
            
    
#             Raise
#             -----
            
#         """
        
#         #region ---------------------------------------------------> Path
#         folder = f'{tDate.split(" - ")[0]}_{tSection.replace(" ", "-")}'
#         fileN = self.rData[tSection][tDate]['CEvol']
#         fileP = self.rStepDataP/folder/fileN
#         #endregion ------------------------------------------------> Path

#         return dtsFF.ReadCSV2DF(fileP, header=[0,1])
#     #---
    
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
                else:
                    pass
        #endregion ------------------------------------------------> 

        return inputF
    #---
    #endregion --------------------------------------------------> Get Methods
#---
#endregion ----------------------------------------------------------> Classes



