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

#endregion --------------------------------------------> File content classess

