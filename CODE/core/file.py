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
from typing  import Union
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Methods
def ReadJSON(fileP: Union[Path, str]) -> dict:
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
#endregion ----------------------------------------------------------> Methods
