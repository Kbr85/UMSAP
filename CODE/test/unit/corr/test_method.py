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
    def setUp(self):
        """Set test"""
        self.df = cFile.ReadCSV2DF(fileA)
        self.dict1 = {
            'Cero' : False,
            'TransMethod' : 'Log2',
            'NormMethod'  : 'Median',
            'ImpMethod'   : 'None',
            'Shift'       : 1.8,
            'Width'       : 0.3,
            'CorrMethod'  : 'Pearson',
            'oc' : {
                'Column' : [98,99,100,101,102],
            },
            'df' : {
                'ColumnR'     : [0,1,2,3,4],
                'ColumnF'     : [0,1,2,3,4],
                'ResCtrlFlat' : [0,1,2,3,4],
            }
        }
        self.dict2 = {
            'Cero' : False,
            'TransMethod' : 'None',
            'NormMethod'  : 'None',
            'ImpMethod'   : 'None',
            'Shift'       : 1.8,
            'Width'       : 0.3,
            'CorrMethod'  : 'Pearson',
            'oc' : {
                'Column' : [98,99,100,101,102],
            },
            'df' : {
                'ColumnR'     : [0,1,2,3,4],
                'ColumnF'     : [0,1,2,3,4],
                'ResCtrlFlat' : [0,1,2,3,4],
            }
        }
        self.dict3 = {
            'Cero' : True,
            'TransMethod' : 'Log2',
            'NormMethod'  : 'Median',
            'ImpMethod'   : 'None',
            'Shift'       : 1.8,
            'Width'       : 0.3,
            'CorrMethod'  : 'Pearson',
            'oc' : {
                'Column' : [98,99,100,101,102],
            },
            'df' : {
                'ColumnR'     : [0,1,2,3,4],
                'ColumnF'     : [0,1,2,3,4],
                'ResCtrlFlat' : [0,1,2,3,4],
            }
        }
        self.dict4 = {
            'Cero' : True,
            'TransMethod' : 'Log2',
            'NormMethod'  : 'Median',
            'ImpMethod'   : 'None',
            'Shift'       : 1.8,
            'Width'       : 0.3,
            'CorrMethod'  : 'Kendall',
            'oc' : {
                'Column' : [98,99,100,101,102],
            },
            'df' : {
                'ColumnR'     : [0,1,2,3,4],
                'ColumnF'     : [0,1,2,3,4],
                'ResCtrlFlat' : [0,1,2,3,4],
            }
        }
    #---
    #endregion --------------------------------------------------> Class Setup

    #region -------------------------------------------------> Expected Output
    def test_output(self):
        """Test method output"""
        #------------------------------>
        tInput = [
            (self.df, self.dict1, True, corrA_1),
            (self.df, self.dict2, True, corrA_2),
            (self.df, self.dict3, True, corrA_3),
            (self.df, self.dict4, True, corrA_4),
        ]
        #------------------------------>
        for a,b,c,d in tInput:
            with self.subTest(f"df={a}, rDO={b}, resetIndex={c}"):
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
