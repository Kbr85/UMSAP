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


"""Classes and methods to handle generators."""


#region -------------------------------------------------------------> Imports
from pathlib import Path
from typing  import Iterator, Union

import wx

import config.config  as mConfig
import data.exception as mException
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Methods
def FastaSequence(fileP: Union[Path, str]) -> Iterator[tuple[str, str]]:
    """Find all sequences in a multi-FASTA file.

        Parameters
        ----------
        fileP : Path
            Location of the fasta file in the file system.

        Yield
        -----
        tuple
            (Fasta header, sequence) or ('', '') if file is empty

        Notes
        -----
        Header line in the multi fasta file is expected to start with >.
    """
    #region -------------------------------------------------------> Variables
    first  = True # To skip yield in the first header of the fasta file
    header = ''
    seq    = []
    #endregion ----------------------------------------------------> Variables

    #region ----------------------------------------------------> Process file
    try:
        with open(fileP, 'r', encoding='utf-8') as file:
            for line in file:
                #-------> Remove empty characters and \n \r \t from line
                sLine = line.strip()
                #------------------------------> Skip empty lines
                if sLine == '':
                    continue
                else:
                    pass
                #------------------------------> Process line
                if sLine[0] == '>':
                    #--------------> No yield if it is the first header
                    if first:
                        first = False
                    else:
                        yield (header, "".join(seq))
                    #--------------> Start a new protein
                    header = sLine
                    seq    = []
                else:
                    #--------------> Append to seq
                    seq.append(sLine)
    except Exception as e:
        raise mException.ExecutionError(mConfig.mFileRead.format(fileP)) from e
    #endregion -------------------------------------------------> Process file

    #region --------------------------------------------> Get the last protein
    yield (header, "".join(seq))
    #endregion -----------------------------------------> Get the last protein
#---

def FindChildren(parent: wx.Window) -> Iterator[wx.Window]:
    """Find all child widgets in parent.

        Parameters
        ----------
        parent : wx.Window
            Parent of the child widgets to search for.

        Yield
        -----
        wx.Window
            Each child in parent.
    """
    #region ---------------------------------------------------------> Iterate
    for child in parent.GetChildren():
        yield child
        yield from FindChildren(child)
    #endregion ------------------------------------------------------> Iterate
#---
#endregion ----------------------------------------------------------> Methods
