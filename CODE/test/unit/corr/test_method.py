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


"""Tests for corr.method"""


#region -------------------------------------------------------------> Imports
import unittest
from pathlib import Path

import pandas as pd

from core import file   as cFile
from corr import method as corrMethod
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------> File Location
folder = Path(__file__).parent / 'file'
fileA  = folder / 'corrA-tarprot-data-file.txt'
corrA_1 = folder / 'res-corrA-1.txt'
corrA_2 = folder / 'res-corrA-2.txt'
corrA_3 = folder / 'res-corrA-3.txt'
corrA_4 = folder / 'res-corrA-4.txt'
#endregion ----------------------------------------------------> File Location


#region -------------------------------------------------------------> Classes
class Test_CorrA(unittest.TestCase):
    """Test for corr.method.CorrA"""
    #region -----------------------------------------------------> Class Setup
    @classmethod
    def setUpClass(cls):
        """Set test"""
        cls.df = cFile.ReadCSV2DF(fileA)
        cls.test1 = corrMethod.UserData(
            cero          = False,
            tran          = 'Log2',
            norm          = 'Median',
            imp           = 'None',
            shift         = 1.8,
            width         = 0.3,
            corr          = 'Pearson',
            ocColumn      = [98,99,100,101,102],
            ocResCtrlFlat = [98,99,100,101,102],
            dfColumnF     = [0,1,2,3,4],
            dfColumnR     = [0,1,2,3,4],
            dfResCtrlFlat = [0,1,2,3,4],
        )
        cls.test2 = corrMethod.UserData(
            cero          = False,
            tran          = 'None',
            norm          = 'None',
            imp           = 'None',
            shift         = 1.8,
            width         = 0.3,
            corr          = 'Pearson',
            ocColumn      = [98,99,100,101,102],
            ocResCtrlFlat = [98,99,100,101,102],
            dfColumnF     = [0,1,2,3,4],
            dfColumnR     = [0,1,2,3,4],
            dfResCtrlFlat = [0,1,2,3,4],
        )
        cls.test3 = corrMethod.UserData(
            cero          = True,
            tran          = 'Log2',
            norm          = 'Median',
            imp           = 'None',
            shift         = 1.8,
            width         = 0.3,
            corr          = 'Pearson',
            ocColumn      = [98,99,100,101,102],
            ocResCtrlFlat = [98,99,100,101,102],
            dfColumnF     = [0,1,2,3,4],
            dfColumnR     = [0,1,2,3,4],
            dfResCtrlFlat = [0,1,2,3,4],
        )
        cls.test4 = corrMethod.UserData(
            cero          = True,
            tran          = 'Log2',
            norm          = 'Median',
            imp           = 'None',
            shift         = 1.8,
            width         = 0.3,
            corr          = 'Kendall',
            ocColumn      = [98,99,100,101,102],
            ocResCtrlFlat = [98,99,100,101,102],
            dfColumnF     = [0,1,2,3,4],
            dfColumnR     = [0,1,2,3,4],
            dfResCtrlFlat = [0,1,2,3,4],
        )
    #---
    #endregion --------------------------------------------------> Class Setup

    #region -------------------------------------------------> Expected Output
    def test_output(self):
        """Test method output"""
        #------------------------------>
        tInput = [
            (self.df, self.test1, True, corrA_1, 'Test - 1'),
            (self.df, self.test2, True, corrA_2, 'Test - 2'),
            (self.df, self.test3, True, corrA_3, 'Test - 3'),
            (self.df, self.test4, True, corrA_4, 'Test - 4'),
        ]
        #------------------------------>
        for a,b,c,d,g in tInput:
            with self.subTest(f"{g}"):
                #------------------------------>
                result = corrMethod.CorrA(
                    df=a, rDO=b, resetIndex=c)[0]['dfR']
                result = result.round(3)
                #------------------------------>
                dfF = pd.read_csv(d, sep='\t',index_col=0).round(3)
                #------------------------------>
                # pylint: disable=protected-access
                pd._testing.assert_frame_equal(result, dfF)                     # type: ignore
    #---
    #endregion ----------------------------------------------> Expected Output
#---
#endregion ----------------------------------------------------------> Classes
