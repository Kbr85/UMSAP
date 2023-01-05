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
#endregion ----------------------------------------------------------> Classes
