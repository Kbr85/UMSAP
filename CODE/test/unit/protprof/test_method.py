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


"""Tests for protprof.method"""


#region -------------------------------------------------------------> Imports
import unittest
from pathlib import Path

import pandas as pd

from core     import file   as cFile
from protprof import method as protMethod
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------> File Location
folder = Path(__file__).parent / 'file'
fileA  = folder / 'protprof-data-file.txt'
fileB  = folder / 'res-protprof-1.txt'
#endregion ----------------------------------------------------> File Location


#region -------------------------------------------------------------> Classes
class Test_ProtProf(unittest.TestCase):
    """Test for protprof.method.ProtProf"""
    #region -----------------------------------------------------> Class Setup
    @classmethod
    def setUpClass(cls):
        """Set test"""
        cls.df    = cFile.ReadCSV2DF(fileA)
        cls.dict1 = protMethod.UserData(
            cero          = True,
            norm          = 'Median',
            tran          = 'Log2',
            imp           = 'None',
            shift         = 1.8,
            width         = 0.3,
            scoreVal      = 320.0,
            rawInt        = True,
            indSample     = 'i',
            alpha         = 0.05,
            correctedP    = 'Benjamini - Hochberg',
            ocTargetProt  = 0,
            ocGene        = 6,
            ocScore       = 39,
            ocExcludeR    = [171, 172, 173],
            ocResCtrl     = [[[105, 115, 125]], [[106, 116, 126], [101, 111, 121]], [[108, 118, 128], [103, 113, 123]]],
            ocColumn      = [6, 0, 39, 171, 172, 173, 105, 115, 125, 106, 116, 126, 101, 111, 121, 108, 118, 128, 103, 113, 123],
            labelA        = ['C1', 'C2'],
            labelB        = ['RP1', 'RP2'],
            ctrlType      = 'One Control',
            ctrlName      = '1Control',
            dfTargetProt  = 0,
            dfGene        = 1,
            dfScore       = 2,
            dfExcludeR    = [3, 4, 5],
            dfResCtrl     = [[[6, 7, 8]], [[9, 10, 11], [12, 13, 14]], [[15, 16, 17], [18, 19, 20]]],
            dfResCtrlFlat = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
            dfColumnR     = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
            dfColumnF     = [2, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        )
    #---
    #endregion --------------------------------------------------> Class Setup

    #region -------------------------------------------------> Expected Output
    def test_output(self):
        """Test method output"""
        #------------------------------>
        tInput = [
            (self.df, self.dict1, True, fileB, 'Test - 1'),
        ]
        #------------------------------>
        for a,b,c,d,e in tInput:
            with self.subTest(f"{e}"):
                #------------------------------>
                result = protMethod.ProtProf(
                    df=a, rDO=b, resetIndex=c)[0]['dfR']
                result = result.round(2)
                #------------------------------>
                dfF = pd.read_csv(d, sep='\t', header=[0,1,2]).round(2)
                #------------------------------>
                # pylint: disable=protected-access
                pd._testing.assert_frame_equal(result, dfF)                     # type: ignore
    #---
    #endregion ----------------------------------------------> Expected Output
#---
#endregion ----------------------------------------------------------> Classes
