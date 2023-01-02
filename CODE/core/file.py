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

import pandas as pd

from Bio       import pairwise2
from Bio.Align import substitution_matrices

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
    # Test in test.unit.test_file.Test_ReadFileFirstLine
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


def WriteJSON(fileP: Union[Path, str], data: dict) -> bool:
    """ Writes a JSON file.

        Parameters
        ----------
        fileP : str or Path
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
    # Test in test.unit.test_file.Test_FastaFile
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
            raise RuntimeError(msg) from e
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
            raise ValueError(msg)
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
    # Test in test.unit.test_file.Test_CSVFile
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
#endregion ----------------------------------------------------------> Classes
