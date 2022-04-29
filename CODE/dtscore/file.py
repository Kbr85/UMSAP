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

from Bio import pairwise2
from Bio.Align import substitution_matrices
import pandas as pd
import numpy as np

import config.config as config
import dtscore.data_method as dtsMethod
import dtscore.exception as dtsException
import dtscore.generator as dtsGenerator
#endregion ----------------------------------------------------------> Imports



#region ------------------------------------------------------> File/Folder IO
#------------------------------> Read
def ReadJSON(fileP: Union[Path, str]) -> dict:
    """Reads a file with a json format 
        
        Parameters
        ----------
        fileP: Path 
            Path to the file

        Return
        ------
        dict:
            With the data in the file

        Raise
        -----
        ExecutionError:
            - When the file could not be read
    """
    #region -------------------------------------------------------> Read file
    try:
        #------------------------------> Read file
        with open(fileP, 'r') as file:
            data = json.load(file)
        #------------------------------> Return
        return data
    except FileNotFoundError as e:
        raise e
    except Exception:
        raise dtsException.ExecutionError(config.mReadErrorIO.format(fileP))
    #endregion ----------------------------------------------------> Read file	
#---

def ReadCSV2DF(
    fileP: Union[Path, str], sep: str='\t', index_col: Optional[int]=None,
    header: Union[int, list[int], None, str]='infer') -> pd.DataFrame:
    """ Reads a csv file and returns a pandas dataframe 
        
        Parameters
        ----------
        fileP : str or Path
            Path to the file
        sep : str
            Column separator in the CSV file. Default is tab
        index_col : int or None
            Index of the column names
        header : int, list[int], None
            Use list[int] for multiindex columns

        Returns
        -------
        dataframe:
            Pandas dataframe with the data

        Raise
        -----
        ExecutionError:
            - When the file could not be read
    """   
    #region -------------------------------------------------------> Read file
    try:
        return pd.read_csv(
            str(fileP), sep=sep, index_col=index_col, header=header)
    except Exception:
        raise dtsException.ExecutionError(config.mReadErrorIO.format(fileP))
    #endregion ----------------------------------------------------> Read file
#---

def ReadFileFirstLine(
    fileP: Union[Path, str], char: Optional[str]='\t', empty: bool=False
    ) -> list[str]:
    """Custom method to read the first line in a file.

        See Notes below for more details

        Parameters
        ----------
        fileP : path or str
            File path of the file to be read 
        char : str or None
            each line in the file is splitted using the value of char or not if 
            char is None
        empty : boolean
            Keep (True) or discard (False) empty lines in the file

        Returns
        -------
        list of list
            List of list containing the lines in the read file like:
            [['first', 'line'], ['second', 'line'], ... , ['last', 'line']]

        Raises
        ------
        ExecutionError:
            - When the file cannot be read
            
        Notes
        -----
        The method returns a list containing the first line in the file. 
        The line is splitted using char. The first non-empty line is returned if
        empty is False, otherwise the first line is returned. 
        If the file is empty an empty line is returned.
    """
    #region --------------------------------------------> Read and split lines
    try:
        #------------------------------> Read file
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
                    if char is None:
                        return [l]
                    else:
                        return l.split(char)
        #------------------------------> If file is empty then return
        return []
    except Exception:
        raise dtsException.ExecutionError(config.mReadErrorIO.format(fileP))
    #endregion -----------------------------------------> Read and split lines
#---

#------------------------------> Write
def WriteJSON(fileP: Union[Path, str], data: dict) -> bool:
    """ Writes a json file

        Parameters
        ----------
        fileP : str or Path 
            Path to the file
        data: dict
            Data to be written
            
        Return
        ------
        bool
        
        Raise
        -----
        ExecutionError:
            - When the file could not be written
    """
    #region ---------------------------------------------------> Write to file
    try:
        with open(fileP, 'w') as filew:
            json.dump(data, filew, indent=4)
    except Exception:
        raise dtsException.ExecutionError(config.mWriteErrorIO.format(fileP))
    #endregion ------------------------------------------------> Write to file
    
    return True
#---

def WriteDF2CSV(
    fileP: Union[Path, str], df: pd.DataFrame, sep: str='\t', na_rep: str='NA', 
    index: bool=False) -> bool:
    """ Writes a dataframe to csv formatted file 

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
    try:
        df.to_csv(str(fileP), sep=sep, na_rep=na_rep, index=index)
        return True
    except Exception:
        raise dtsException.ExecutionError(config.mWriteErrorIO.format(fileP))
    #endregion ------------------------------------------------> Write to file
#---


def WriteDFs2CSV(
    baseP: Path, ncDict: dict[str, pd.DataFrame], sep: str='\t', 
    na_rep: str='NA', index: bool=False) -> bool:
    """Write several pd.DataFrames to baseP as CSV files. 

        Existing files will be overwritten if needed. 
    
        Parameters
        ----------
        baseP : Path
            Folder in which all files will be saved
        ncDict : dict
            Keys are file names and values the pd.DataFrames
        sep : str
            Character to separate columns in the csv file
        na_rep : str
            Character to represent NA values
        index: boolean 
            Write index columns
    """
    #region ---------------------------------------------------> Write to file
    for k,i in ncDict.items():
        try:
            fileP = baseP / k
            WriteDF2CSV(fileP, i, sep=sep, na_rep=na_rep, index=index)
        except Exception:
            msg = config.mWriteFilesIO.format(baseP)
            raise dtsException.ExecutionError(msg)
    #endregion ------------------------------------------------> Write to file
    
    return True
#---
#endregion ---------------------------------------------------> File/Folder IO


#region -----------------------------------------------> File content classess
class FastaFile():
    """Class to handle fasta files.
    
        See Notes below for more details.

        Parameters
        ----------
        

        Attributes
        ----------
        

        Raises
        ------
        

        Methods
        -------
        
    """
    #region -----------------------------------------------------> Class setup
    
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, fileP: Union[Path, str]):
        """ """
        #region -----------------------------------------------> Initial Setup
        #------------------------------> 
        self.fileP = fileP
        #------------------------------> 
        gen = dtsGenerator.FastaSequence(fileP)
        #------------------------------> 
        self.headerRec, self.seqRec = next(gen)
        self.seqLengthRec = len(self.seqRec)
        #------------------------------> 
        try:
            self.headerNat, self.seqNat = next(gen)
        except StopIteration:
            self.headerNat, self.seqNat, self.seqLengthNat = (None, None, None)
        except Exception as e:
            msg = (f'There was an unexpected error when parsing the fasta '
                f'file.\n{fileP}')
            raise dtsException.UnexpectedError(msg)
        else:
            self.seqLengthNat = len(self.seqNat)
        #------------------------------> 
        self.alignment = None
        #endregion --------------------------------------------> Initial Setup
        #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def FindSeq(self, seq: str, seqRec: bool=True) -> tuple[int, int]:
        """Find the location of seq in the sequence of the Rec or Nat Protein
        
            See Notes below for more details
    
            Parameters
            ----------
            seq : str
                Peptide sequence to find in the Protein sequence
    
            Returns
            -------
            tuple[int, int]
                The N and C residue numbers of seq in the protein sequence.
                
            Raises
            ------
            ExecutionError:
                - when seqRec is False but self.seqNat is None
    
            Notes
            -----
            [-1, -1] is returned if seq is not found inside the protein 
            sequence.
        """
        #region -------------------------------------------------> Check Input
        if seqRec:
            pass
        else:
            if self.seqNat is not None:
                pass
            else:
                msg = ("The Native sequence of the protein is undefined. The "
                    "peptide sequence can only be searched for in the "
                    "Recombinant sequence")
                raise dtsException.ExecutionError(msg)
        #endregion ----------------------------------------------> Check Input
        
        #region ------------------------------------------------------> Find N
        #------------------------------> 
        n = self.seqRec.find(seq) if seqRec else self.seqNat.find(seq)
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
        """
    
            Parameters
            ----------
            
    
            Returns
            -------
            
    
            Raise
            -----
        
        """
        #region -----------------------------------------------> Blosum matrix
        blosum62 = substitution_matrices.load("BLOSUM62")
        #endregion --------------------------------------------> Blosum matrix
        
        #region ---------------------------------------------------> Alignment
        try:
            return pairwise2.align.globalds(seqA, seqB, blosum62, -10, -0.5)
        except Exception:
            msg = (f'Sequence alignment failed.\nseqA: {seqA}\nseqB: {seqB}')
            raise dtsException.ExecutionError(msg)
        #endregion ------------------------------------------------> Alignment
    #---
    
    def SetSelfAlignment(self) -> bool:
        """
    
            Parameters
            ----------
            
    
            Returns
            -------
            
    
            Raise
            -----
        
        """
        #region ---------------------------------------------------> Alignment
        if getattr(self, 'alignment', None) is None:
            try:
                self.alignment = self.CalculateAlignment(
                    self.seqRec, self.seqNat)
            except Exception as e:
                raise e
            else:
                return True
        else:
            return True
        #endregion ------------------------------------------------> Alignment
    #---
    
    def GetSelfAlignment(self):
        """
    
            Parameters
            ----------
            
    
            Returns
            -------
            
    
            Raise
            -----
        
        """
        #region ---------------------------------------------------> Alignment
        if getattr(self, 'alignment', None) is None:
            try:
                self.SetSelfAlignment()
            except Exception as e:
                raise e
            else:
                return self.alignment
        else:
            return self.alignment
        #endregion ------------------------------------------------> Alignment
    #---
    
    def GetSelfDelta(self) -> int:
        """
    
            Parameters
            ----------
            
    
            Returns
            -------
            
    
            Raise
            -----
        
        """
        #region ---------------------------------------------------> Alignment
        try:
            alignment = self.GetSelfAlignment()
            seqB = alignment[0].seqB
        except Exception as e:
            raise e
        #endregion ------------------------------------------------> Alignment
        
        #region ---------------------------------------------------> Get delta
        for k,l in enumerate(seqB):
            if l == '-':
                pass
            else:
                return -1 * k
            
        return 0 # ProtRec and ProtNat are the same
        #endregion ------------------------------------------------> Get delta
    #---
    
    def GetNatProtLoc(self):
        """

            Parameters
            ----------


            Returns
            -------


            Raise
            -----

        """
        #region ---------------------------------------------------> Alignment
        try:
            alignment = self.GetSelfAlignment()
            seqB = alignment[0].seqB
        except Exception as e:
            raise e
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
        lr = self.seqLengthRec if lr is None else lr
        #endregion ---------------------------------------> Get Right Position
        
        return (ll, lr)
    #---
    #endregion ------------------------------------------------> Class methods
#---


class CSVFile():
    """Class to deal with csv formatted input files

        Parameters
        ----------
        fileP : str or Path
            Path to the input file
        sep : str
            Column separator character in the csv file

        Attributes
        ----------
        df : pd.DataFrame
            Copy of the df in the file that can be modified
        Fdata : pd.DataFrame
            This is the initial data and will not be modified. It is just to 
            read from if needed.
        fileP : str or Path
            Path to the csv file
        header : list
            List with the names of the columns in the csv file. It is assumed 
            the names are in the first row of the file.
        nRow, nCol : int
            Number of rows and columns in self.Fdata

        Raises
        ------
        FileIOError:
            - When fileP cannot be read
            
        Notes
        -----
        It is assumed the csv file has column names in the first row.
        """
    #region -----------------------------------------------------> Class setup
    
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self, fileP: Union[Path, str], sep: str="\t",
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.fileP = fileP
        #endregion --------------------------------------------> Initial Setup

        #region ---------------------------------------------------> Read File
        try:
            self.Fdata = ReadCSV2DF(self.fileP, sep=sep)
        except Exception:
            raise dtsException.FileIOError(config.mReadErrorIO.format(fileP))
        #endregion ------------------------------------------------> Read File

        #region ---------------------------------------------------> Variables
        self.SetAttributes()
        #endregion ------------------------------------------------> Variables
        #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def SetAttributes(self) -> bool:
        """ Set other variables needed by the class """
        #--> list with the name of the columns in the data file
        self.header = list(self.Fdata.columns)
        #--> copy of self.Fdata to modify it without altering the original data
        self.df = self.Fdata.copy()
        #--> nRows, nCols
        self.nRow, self.nCol = self.df.shape

        return True
    #---
    
    def StrInCol(self, tStr:str, col:int, comp: Literal['e', 'ne']='e') -> bool:
        """Basically check if str is in col.
    
            Parameters
            ----------
            tStr: str
                String to look for
            col: int
                Column containing the string
            comp: str
                One of 'e', 'ne'. Equal or not Equal
    
            Returns
            -------
            bool
        """
        df = dtsMethod.DFFilterByColS(self.Fdata, col, tStr, comp=comp)
        return not df.empty
    #---
    #endregion ------------------------------------------------> Class methods
#---


class PDBFile():
    """Basic class to handle PDB files 
    
        Parameters
        ----------
        
        
        Attributes
        ----------
    
    """
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
        """
    
            Parameters
            ----------
            
    
            Returns
            -------
            
    
            Raise
            -----
            
        """
        #region ---------------------------------------------------> 
        ldf = []
        #endregion ------------------------------------------------> 

        #region ---------------------------------------------------> 
        with open(self.rFileP, 'r') as file:
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
        """
    
            Parameters
            ----------
            
    
            Returns
            -------
            
    
            Raise
            -----
            
        """
        def Line2PDBFormat(row, buff):
            """
        
                Parameters
                ----------
                
        
                Returns
                -------
                
        
                Raise
                -----
                
            """
            buff.write(f'{self.cPDBformat.format(*row)}\n')
        #---
        #region ---------------------------------------------------> 
        df = self.rDFAtom[self.rDFAtom['Chain'] == chain].copy()
        df = df.replace(np.nan, '')
        #endregion ------------------------------------------------> 

        #region ---------------------------------------------------> 
        buff = open(fileP, 'w')
        df.apply(Line2PDBFormat, raw=True, axis=1, args=[buff])
        buff.write('END')
        buff.close()
        #endregion ------------------------------------------------> 

        return True
    #---
    
    def GetSequence(self, chain: str) -> str:
        """
    
            Parameters
            ----------
            
    
            Returns
            -------
            
    
            Raise
            -----
            
        """
        #region ---------------------------------------------------> 
        dfd = self.rDFAtom[self.rDFAtom['Chain']==chain]
        #endregion ------------------------------------------------> 

        #region ---------------------------------------------------> 
        dfd  = dfd.drop_duplicates(subset='ResNum', keep='first', inplace=False)
        dfd  = dfd.loc[dfd.loc[:,'ResName'].isin(config.oAA3toAA)]
        seq = dfd['ResName'].tolist()
        #endregion ------------------------------------------------> 
                
        return "".join([config.oAA3toAA[x] for x in seq])
    #---
    
    def GetResNum(self, chain: str) -> str:
        """
    
            Parameters
            ----------
            
    
            Returns
            -------
            
    
            Raise
            -----
            
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
        """
    
            Parameters
            ----------
            
    
            Returns
            -------
            
    
            Raise
            -----
            
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
#endregion --------------------------------------------> File content classess

