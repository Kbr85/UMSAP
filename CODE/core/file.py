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


"""Methods to handle files in the app"""


#region -------------------------------------------------------------> Imports
import json
from pathlib import Path
from typing  import Union, Optional, Literal

import numpy  as np
import pandas as pd

from Bio       import pairwise2
from Bio.Align import substitution_matrices

from config.config import config as mConfig
from core import generator as cGenerator
from core import method    as cMethod
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Methods
def ReadJSON(fileP:Union[Path, str]) -> dict:
    """Reads a file with json format.

        Parameters
        ----------
        fileP: Path, str
            Path to the file.

        Return
        ------
        dict:
            Data in the file.
    """
    # No test
    #region -------------------------------------------------------> Read file
    with open(fileP, 'r', encoding="utf-8") as file:
        data = json.load(file)
    #endregion ----------------------------------------------------> Read file

    return data
#---


def ReadCSV2DF(
    fileP:Union[Path, str],
    sep:str                                              = '\t',
    index_col:Optional[int]                              = None,
    header:Union[int, list[int], None, Literal['infer']] = 'infer',
    ) -> pd.DataFrame:
    """Reads a CSV file and returns a pandas dataframe.

        Parameters
        ----------
        fileP: str or Path
            Path to the file.
        sep: str
            Column separator in the CSV file. Default is tab.
        index_col: int or None
            Index of the column names.
        header: int, list[int], None
            Use list[int] for multi index columns.

        Returns
        -------
        dataframe:
            Pandas dataframe with the data.
    """
    # No test
    #region -------------------------------------------------------> Read file
    return pd.read_csv(
        str(fileP), sep=sep, index_col=index_col, header=header)
    #endregion ----------------------------------------------------> Read file
#---


def ReadFileFirstLine(
    fileP:Union[Path, str],
    char:str   = '\t',
    empty:bool = False,
    ) -> list[str]:
    """Custom method to read the first line in a file.

        Parameters
        ----------
        fileP: path or str
            File path of the file to be read.
        char: str
            each line in the file is splitted using the value of char or not if
            char is empty.
        empty: boolean
            Return first non-empty line (False) or first line (True).

        Returns
        -------
        list of list
            List of list containing the lines in the read file like:
            [['first', 'line'], ['second', 'line'], ... , ['last', 'line']]

        Notes
        -----
        - The method returns a list containing the first line in the file.
        - The line is splitted using char.
        - The first non-empty line is returned if empty is False, otherwise the
          first line is returned independently of the line content.
        - If the file is empty an empty line is returned.
    """
    # Test in test.unit.core.test_file.Test_ReadFileFirstLine
    #region --------------------------------------------> Read and split lines
    with open(fileP, 'r', encoding="utf-8") as file:
        for line in file:
            #------------------------------> # Remove ' ', \n, \t & \r from start/end of line
            l = line.strip()
            #------------------------------> Discard empty lines
            if l == '' and not empty:
                continue
            #------------------------------> Return splitted line
            if char:
                return l.split(char)
            #------------------------------> Return first line
            return [l]
    #endregion -----------------------------------------> Read and split lines

    #------------------------------> If file is empty then return
    return []
#---


def WriteJSON(fileP:Union[Path, str], data:dict) -> bool:
    """Writes a JSON file.

        Parameters
        ----------
        fileP: str or Path
            Path to the file.
        data: dict
            Data to be written.

        Return
        ------
        bool
    """
    # No test
    #region ---------------------------------------------------> Write to file
    with open(fileP, 'w', encoding="utf-8") as file:
        json.dump(data, file, indent=4)
    #endregion ------------------------------------------------> Write to file

    return True
#---


def WriteDF2CSV(
    fileP:Union[Path, str],
    df:pd.DataFrame,
    sep:str    = '\t',
    na_rep:str = 'NA',
    index:bool = False,
    ) -> bool:
    """Writes a dataframe to CSV formatted file.

        Parameters
        ----------
        fileP: str or Path
            Path to the file.
        df: pd.DataFrame
            Data frame to be written.
        sep: str
            Character to separate columns in the CSV file.
        na_rep: str
            Character to represent NA values.
        index: boolean
            Write index columns
    """
    # No Test
    #region ---------------------------------------------------> Write to file
    df.to_csv(str(fileP), sep=sep, na_rep=na_rep, index=index)
    return True
    #endregion ------------------------------------------------> Write to file
#---


def WriteDFs2CSV(
    baseP:Path,
    ncDict:dict[str, pd.DataFrame],
    sep:str    = '\t',
    na_rep:str = 'NA',
    index:bool = False
    ) -> bool:
    """Write several pd.DataFrames to baseP as CSV files.

        Parameters
        ----------
        baseP: Path
            Folder in which all files will be saved.
        ncDict: dict
            Keys are file names and values the pd.DataFrames.
        sep: str
            Character to separate columns in the csv file.
        na_rep: str
            Character to represent NA values.
        index: boolean
            Write index columns.

        Notes
        -----
        Existing files will be overwritten if needed.
    """
    # No test
    #region ---------------------------------------------------> Write to file
    for k,i in ncDict.items():
        fileP = baseP / k
        WriteDF2CSV(fileP, i, sep=sep, na_rep=na_rep, index=index)
    #endregion ------------------------------------------------> Write to file

    return True
#---
#endregion ----------------------------------------------------------> Methods


#region -------------------------------------------------------------> Classes
class FastaFile():
    """Class to handle fasta files.

        Parameters
        ----------
        fileP: Path or str
            Path to the fasta file.

        Attributes
        ----------
        rAlignment: BioPython alignment
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

        Notes
        -----
        It handle the first two sequences in the file. All other sequences
        are discarded. It is assumed that the first sequence is the recombinant
        sequence and the second sequence is the native sequence.
    """
    # Test in test.unit.core.test_file.Test_FastaFile
    #region --------------------------------------------------> Instance setup
    def __init__(self, fileP: Union[Path, str]) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.rFileP = fileP
        #------------------------------>
        gen = cGenerator.FastaSequence(fileP)
        #------------------------------>
        self.rHeaderRec, self.rSeqRec = next(gen)
        self.rSeqLengthRec = len(self.rSeqRec)
        self.rAlignment    = []
        #------------------------------>
        try:
            self.rHeaderNat, self.rSeqNat = next(gen)
            self.rSeqLengthNat = len(self.rSeqNat)
        except StopIteration:
            self.rHeaderNat, self.rSeqNat, self.rSeqLengthNat = ('', '', None)
        except Exception as e:
            msg = (f'There was an unexpected error when parsing the fasta '
                f'file.\n{fileP}')
            raise ValueError(msg) from e
        #endregion --------------------------------------------> Initial Setup
        #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def FindSeq(self, seq:str, seqRec:bool=True) -> tuple[int, int]:
        """Find the location of seq in the sequence of the Rec or Nat Protein.

            Parameters
            ----------
            seq: str
                Peptide sequence to find in the Protein sequence
            seqRec: bool
                Search on the recombinant (True) or native sequence (False).

            Returns
            -------
            tuple[int, int]
                The N and C residue numbers of seq in the protein sequence.

            Raises
            ------
            RuntimeError:
                - When seqRec is False but self.seqNat is None.

            Notes
            -----
            [-1, -1] is returned if seq is not found inside the protein
            sequence.
            - First match is returned if the search sequence is found more than
            once in the protein sequence.
        """
        #region -------------------------------------------------> Check Input
        if not self.rSeqNat and not seqRec:
            msg = ("The Native sequence of the protein is undefined. The "
                "peptide sequence can only be searched for in the "
                "Recombinant sequence")
            raise RuntimeError(msg)
        #endregion ----------------------------------------------> Check Input

        #region ------------------------------------------------------> Find N
        n = self.rSeqRec.find(seq) if seqRec else self.rSeqNat.find(seq)
        #------------------------------>
        if n == -1:
            return (-1, -1)
        #endregion ---------------------------------------------------> Find N

        #region ------------------------------------------------------> Find C
        n = n + 1
        c = n + len(seq) - 1
        #endregion ---------------------------------------------------> Find C

        return (n, c)
    #---

    def CalculateAlignment(self, seqA:str, seqB:str):
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
        return pairwise2.align.globalds(seqA, seqB, blosum62, -10, -0.5)        # type: ignore
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
            ValueError if self.rSeqNat is empty.
        """
        #region --------------------------------------------------->
        if not self.rSeqNat:
            msg = ('It is not possible to calculate the sequence alignment '
                   'because the Fasta file contains only one sequence.')
            raise RuntimeError(msg)
        #endregion ------------------------------------------------>

        #region ---------------------------------------------------> Alignment
        if not getattr(self, 'rAlignment', []):
            self.rAlignment = self.CalculateAlignment(self.rSeqRec,self.rSeqNat)
        #endregion ------------------------------------------------> Alignment

        return True
    #---

    def GetSelfAlignment(self):
        """Get the alignment between the Recombinant and Native sequence.

            Returns
            -------
            BioPython alignment.
        """
        self.SetSelfAlignment()
        return self.rAlignment
    #---

    def GetSelfDelta(self) -> int:
        """Get Residue number difference between the Recombinant and Native
            sequence.

            Returns
            -------
            int

            Notes
            -----
            It is assumed both sequences differ only at the N or C terminal
            region.
        """
        #region ---------------------------------------------------> Alignment
        self.SetSelfAlignment()
        seqB = self.rAlignment[0].seqB
        #endregion ------------------------------------------------> Alignment

        #region ---------------------------------------------------> Get delta
        for k,l in enumerate(seqB):
            if l != '-':
                return -1 * k
        #------------------------------>
        return 0                                                                # ProtRec and ProtNat are the same
        #endregion ------------------------------------------------> Get delta
    #---

    def GetNatProtLoc(self) -> tuple[int, int]:
        """Get the location of the Native sequence inside the Recombinant
            sequence.

            Returns
            -------
            tuple
                First and last residue.

            Notes
            -----
            It is assumes both sequences differ only at the N or C terminal
            region.
        """
        #region ---------------------------------------------------> Alignment
        self.SetSelfAlignment()
        seqB = self.rAlignment[0].seqB
        #endregion ------------------------------------------------> Alignment

        #region -------------------------------------------> Get Left Position
        ll = None
        #------------------------------>
        for k,l in enumerate(seqB, start=1):
            if l != '-':
                ll = k
                break
        #------------------------------>
        ll = 1 if ll is None else ll
        #endregion ----------------------------------------> Get Left Position

        #region ------------------------------------------> Get Right Position
        lr = None
        #------------------------------>
        for k,l in reversed(list(enumerate(seqB, start=1))):
            if l != '-':
                lr = k
                break
        #------------------------------>
        lr = self.rSeqLengthRec if lr is None else lr
        #endregion ---------------------------------------> Get Right Position

        return (ll, lr)
    #---
    #endregion ------------------------------------------------> Class methods
#---


class CSVFile():
    """Class to deal with CSV formatted input files.

        Parameters
        ----------
        fileP: str or Path
            Path to the input file.
        sep: str
            Column separator character in the CSV file.

        Attributes
        ----------
        rData: pd.DataFrame
            This is the initial data and will not be modified. It is just to
            read from if needed.
        rDf: pd.DataFrame
            Copy of the df in the file that can be modified.
        rFileP: str or Path
            Path to the CSV file.
        rHeader: list
            List with the names of the columns in the CSV file. It is assumed
            the names are in the first row of the file.
        rNRow, rNCol: int
            Number of rows and columns in self.rData.

        Notes
        -----
        It is assumed the CSV file has column names in the first row.
        """
    # Test in test.unit.core.test_file.Test_CSVFile
    #region --------------------------------------------------> Instance setup
    def __init__(self, fileP:Union[Path, str], sep:str="\t") -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.rFileP = fileP
        #endregion --------------------------------------------> Initial Setup

        #region ---------------------------------------------------> Read File
        self.rData = ReadCSV2DF(self.rFileP, sep=sep)
        #endregion ------------------------------------------------> Read File

        #region ---------------------------------------------------> Variables
        self.rDf = self.rData.copy()
        self.rHeader = list(self.rData.columns)
        self.rNRow, self.rNCol = self.rDf.shape
        #endregion ------------------------------------------------> Variables
        #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def StrInCol(self, tStr:str, col:int) -> bool:
        """Basically check if str is in col.

            Parameters
            ----------
            tStr: str
                String to look for.
            col: int
                Column containing the string.

            Returns
            -------
            bool
        """
        df = cMethod.DFFilterByColS(self.rData, col, tStr, comp='e')
        return not df.empty
    #---
    #endregion ------------------------------------------------> Class methods
#---


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
    # Test in test.unit.core.test_file.Test_PDBFile
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
    def __init__(self, fileP:Union[Path, str]) -> None:
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

    def WritePDB(self, fileP:Union[Path, str], chain:str) -> bool:
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
        def Line2PDBFormat(row:np.ndarray, buff):
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

    def GetSequence(self, chain:str) -> str:
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
        dfd  = dfd.loc[dfd.loc[:,'ResName'].isin(mConfig.core.oAA3toAA)]
        seq = dfd['ResName'].tolist()
        #endregion ------------------------------------------------>

        return "".join([mConfig.core.oAA3toAA[x] for x in seq])
    #---

    def GetResNum(self, chain:str) -> list:
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

    def SetBeta(self, chain:str, beta:dict) -> bool:
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
#endregion ----------------------------------------------------------> Classes
