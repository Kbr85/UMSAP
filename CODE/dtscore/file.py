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
def ReadFile(
    fileP: Union[Path, str], char: Optional[str]='\t', empty: bool=False
    ) -> list[list[str]]:
    """Custom method to read in a file.

        See Notes below for more details.

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
        The method returns a list of list containing the lines in the files. 
        Each line is splitted using char. Empty lines can be discarded.
        This will read the entire file and return a list of list with the 
        content of the entire file or an empty list if the file is empty.
    """
    #region -------------------------------------------------------> Variables
    data = []
    #endregion ----------------------------------------------------> Variables
    
    #region --------------------------------------------> Read and split lines
    try:
        #------------------------------> Read file
        with open(fileP, 'r') as file:
            for line in file:
                #--> To remove ' ', \n, \t & \r from start/end of line
                l = line.strip()
                #------------------------------> Add to data
                if l == '' and not empty:
                    #------------------------------> Discard empty
                    pass
                else:
                    #------------------------------> Add to data
                    if char is None:
                        data.append([l])
                    else:
                        ll = l.split(char)
                        data.append(ll)
        #------------------------------> Return list
        return data
    except Exception:
        raise dtsException.ExecutionError(config.mReadErrorIO.format(fileP))
    #endregion -----------------------------------------> Read and split lines
#---
#endregion ---------------------------------------------------> File/Folder IO


#region -------------------------------------------------------------> Methods
def OutputPath(
    baseP: Union[Path, str], outP: Union[Path, str], defVal: str, 
    unique: bool=True, returnTimeStamp: bool=True
    ) -> Union[Path, tuple[Path, str]]:
    """Creates the path to the output file or folder. 
    
        See Notes below for more deails.

        Parameters
        ----------
        baseP : str
            Path to a file or folder used as the base to construct the 
            output
        outP: str
            If empty string '' then uses baseP and defVal to build the path to 
            the output file. Full path is expected if not empty.
        defVal : str
            Default name for the output file or folder
        unique : boolean
            Check file or folder does not exist. If it does add the datetime
            to the name to make it unique.
        returnTimeStamp : boolean
            If True the value of dtsFF.NowFormat() used to build the output
            path is also returned

        Returns
        -------
        str:
            Path to the output file or folder
        tupple:
            (Path to the output file or folder, dtsFF.NowFormat())

        Raise
        -----
        InputError:
            - When baseP is ''.
            - When out and defVal are ''

        Notes
        -----
        If unique is True and file/folder exists, then add dtsFF.NowFormat() to 
        the name to make it unique.

        Examples
        --------
        >>> OutputPath('/Users/john/file.txt', '/Users/john/Desktop/b.zip', 'test.corr', unique=False)
        ('/Users/john/Desktop/b.zip', '20120423-102354')
        
        >>> OutputPath('/Users/john/file.txt', '', 'test.corr', unique=False, returnTimeStamp=False)
        'Users/john/test.corr'

        >>> OutputPath('/Users/john/file.txt', '', 'test.corr', unique=True)
        ('Users/john/test_20210107-101256.corr', '20210107-101256') # If 'Users/john/test.corr' already exists
    """
    #region -------------------------------------------------------> Variables
    date = dtsMethod.StrNow()
    #endregion ----------------------------------------------------> Variables
    
    #region ------------------------------------------------------> Build path
    if outP != '':
        oPath = Path(outP)
    else:
        #------------------------------> 
        iPath = Path(baseP).parent
        oPath = iPath / defVal
        #------------------------------> 
        if unique:
            if oPath.exists():
                defPath = Path(defVal)
                name = (
                    defPath.stem
                    + '_'
                    + date
                    + defPath.suffix
                )
                oPath = oPath.with_name(name)
            else:
                pass
        else:
            pass
    #endregion ---------------------------------------------------> Build path
    
    #region ----------------------------------------------------------> Return
    if returnTimeStamp:
        return (oPath, date)
    else:
        return oPath
    #endregion -------------------------------------------------------> Return
#---
#endregion ----------------------------------------------------------> Methods


#region -----------------------------------------------> File content classess
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

