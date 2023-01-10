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


"""Configuration parameters of the app"""


#region -------------------------------------------------------------> Imports
import platform
from pathlib import Path
from typing  import Literal
#endregion ----------------------------------------------------------> Imports


#region -----------------------------------------> NON-CONFIGURABLE PARAMETERS

#region -------------------------------------------------------------> Options
oIntensities = {
    'Empty' : '',
    'RawI'  : 'Raw Intensities',
    'RatioI': 'Ratio of Intensities',
}
#endregion ----------------------------------------------------------> Options


#region --------------------------------------------------------> Literal
litTestSide     = Literal['ts', 's', 'l']
#endregion -----------------------------------------------------> Literal


#region ------------------------------------------------------------> Messages
#region -------------------------------------------------------------> Other
#------------------------------> Check for Update
mCheckUpdate     = 'Check for Updates failed. Check again later.'
#endregion ----------------------------------------------------------> Other

#region ---------------------------------------------------------------> Files
mFileSelector = 'It was not possible to show the file selecting dialog.'
#endregion ------------------------------------------------------------> Files

#region ------------------------------------------------------------> Pandas
mPDGetInitCol     = ('It was not possible to extract the selected columns ({}) '
                     'from the selected {} file:\n{}')
mPDDataTypeCol    = 'The {} contains unexpected data type in columns {}.'
#endregion ---------------------------------------------------------> Pandas

#------------------------------>
mCompNYI            = "Comparison method is not yet implemented: {}."
mPDFilterByCol      = "Filtering process failed."
mNotImplemented     = 'Option {} is not yet implemented.'
mNotSupported       = "{} value '{}' is not supported."
#endregion ---------------------------------------------------------> Messages
#endregion --------------------------------------> NON-CONFIGURABLE PARAMETERS