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


"""Tests for config.config"""


#region -------------------------------------------------------------> Imports
import unittest
from pathlib import Path

from config.config import Configuration
from core     import config as cConfig
from corr     import config as corrConfig
from dataprep import config as dataConfig
from help     import config as hConfig
from limprot  import config as limpConfig
from main     import config as mConfig
from protprof import config as protConfig
from result   import config as resConfig
from tarprot  import config as tarpConfig
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------> File Location
folder = Path(__file__).parent / 'files'
#endregion ----------------------------------------------------> File Location


#region ---------------------------------------------------------> Class Setup
class Test_Configuration(unittest.TestCase):
    """Test for config.config.Configuration"""
    #region -------------------------------------------------> Expected Output
    def test_expected_output(self):
        """Test for expected output"""
        #------------------------------>
        tInput = [
            #Config File Path,       Return, Attr,  badOpt
            (folder/'no_file.json',  True,   True,  []),                        # File Not Found Error
            (folder/'config_A.json', False,  False, []),                        # File cannot be read
            (folder/'config_B.json', True,   True,  ["BadOption", "BadSection",]),# File with bad options
            ('Users/bravo/umsap_config.json', True, True, [])                   # Real file
        ]
        #------------------------------>
        for a,b,c,d in tInput:
            with self.subTest(f'File:{a}'):
                #------------------------------>
                conf = Configuration(                                           # Create new instance.
                    cConfig.Configuration(),                                    # setUp is not called for
                    corrConfig.Configuration(),                                 # each subTest
                    dataConfig.Configuration(),
                    hConfig.Configuration(),
                    limpConfig.Configuration(),
                    mConfig.Configuration(),
                    protConfig.Configuration(),
                    resConfig.Configuration(),
                    tarpConfig.Configuration(),
                )
                #------------------------------>
                conf.core.fConfig = a
                result = conf.LoadUserConfig()
                #------------------------------>
                self.assertEqual(result, b)
                self.assertEqual(conf.core.confUserFile, c)
                self.assertEqual(conf.core.confUserWrongOptions, d)
    #---
    #endregion ----------------------------------------------> Expected Output
#---
#endregion ------------------------------------------------------> Class Setup
