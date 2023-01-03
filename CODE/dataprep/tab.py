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


"""Tabs for the dataprep module of the app"""


#region -------------------------------------------------------------> Imports
from config.config import config as mConfig
from core import tab as cTab
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Classes
class DataPrep(cTab.BaseConfListTab):
    """Creates the Tab to setup a Correlation Analysis"""
    #region -----------------------------------------------------> Class Setup
    cName  = mConfig.data.ntDataPrep
    cTitle = mConfig.data.ttDataPrep
    #endregion --------------------------------------------------> Class Setup
#---
#endregion ----------------------------------------------------------> Classes
