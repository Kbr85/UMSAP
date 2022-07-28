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


"""Custom exceptions."""


#region -------------------------------------------------------------> Classes
class ExecutionError(Exception):
    """Exception raised for errors when executing a function/process.

        Parameters
        ----------
        message : str
            Explanation of the error.
    """
    #region --------------------------------------------------> Instance setup
    def __init__(self, message: str) -> None:
        """ """
        self.message = message
    #----
    #endregion -----------------------------------------------> Instance setup
#---


class UnexpectedError(Exception):
    """Exception raised for unexpected errors when executing a function/process.

        Parameters
        ----------
        message : str
            Explanation of the error.
    """
    #region --------------------------------------------------> Instance setup
    def __init__(self, message: str) -> None:
        """ """
        self.message = message
    #----
    #endregion -----------------------------------------------> Instance setup
#---


class FileIOError(Exception):
    """Exception raised for errors when reading/writing files.

        Parameters
        ----------
        message : str
            Explanation of the error
    """
    #region --------------------------------------------------> Instance setup
    def __init__(self, message: str) -> None:
        """ """
        self.message = message
    #----
    #endregion -----------------------------------------------> Instance setup
#---


class NotYetImplementedError(Exception):
    """Exception raised when input option is valid but not implemented in 
        method.

        Parameters
        ----------
        message : str
            Explanation of the error
    """
    #region --------------------------------------------------> Instance setup
    def __init__(self, message: str) -> None:
        """ """
        self.message = message
    #----
    #endregion -----------------------------------------------> Instance setup
#---


class InputError(Exception):
    """Exception raised for errors in the input of a method.

        Parameters
        ----------
        message : str
            Explanation of the error
    """
    #region --------------------------------------------------> Instance setup
    def __init__(self, message: str) -> None:
        """ """
        self.message = message
    #----
    #endregion -----------------------------------------------> Instance setup
#---
#endregion ----------------------------------------------------------> Classes