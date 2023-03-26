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


"""Tests for data.method"""


#region -------------------------------------------------------------> Imports
import unittest
from pathlib import Path

import pandas as pd
from numpy  import nan, inf

from core     import file   as cFile
from dataprep import method as dataMethod
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------> File Location
folder = Path(__file__).parent / 'file'
fileA  = folder / 'dataprep-tarprot-data-file.txt'
#endregion ----------------------------------------------------> File Location


#region --------------------------------------------------------> pd.DataFrame
DF_DataPrep_Float = pd.DataFrame({
    'A' : [  2,  '',  8, 16,  0, 32,  64],
    'B' : [  4,   8, 16,  0, 32, 64, 128],
    'C' : ['a', 'b','c','d','e','f', 'g'],
    'D' : [  0,   2,  4,  8, 16, 32,  64],
    'E' : [ 64,  32, 16, "",  4,  2,   0],
    'F' : [ "", 128, 64,  0, 16,  8,   4],
})

DF_DataPrep_Float_True = pd.DataFrame({
    'A' : [  2, nan,  8,  16, nan, 32,  64],
    'B' : [  4,   8, 16, nan,  32, 64, 128],
    'C' : ['a', 'b','c', 'd', 'e','f', 'g'],
    'F' : [nan, 128, 64, nan,  16,  8,   4],
})

DF_DataPrep_Float_False = pd.DataFrame({
    'A' : [  2, nan,  8,  16,   0, 32,  64],
    'B' : [  4,   8, 16,   0,  32, 64, 128],
    'C' : ['a', 'b','c', 'd', 'e','f', 'g'],
    'F' : [nan, 128, 64,  0,  16,  8,   4],
})

DF_Log2 = pd.DataFrame({
    'A' : [  2,   4,  8, 16,  0, 32,  64],
    'B' : [  4,   8, 16,  0, 32, 64, 128],
    'C' : [128,  64, 32, 16,  0,  8,   4],
    'D' : [  0,   2,  4,  8, 16, 32,  64],
    'E' : [ 64,  32, 16,  8,  4,  2,   0],
    'F' : [256, 128, 64,  0, 16,  8,   4],
})

DF_Log2_Full_None = pd.DataFrame({
    'A' : [          1.0, 2.0, 3.0,           4.0, -inf, 5.0,           6.0],
    'B' : [          2.0, 3.0, 4.0, -inf,           5.0, 6.0,           7.0],
    'C' : [          7.0, 6.0, 5.0,           4.0, -inf, 3.0,           2.0],
    'D' : [-inf, 1.0, 2.0,           3.0,           4.0, 5.0,           6.0],
    'E' : [          6.0, 5.0, 4.0,           3.0,           2.0, 1.0, -inf],
    'F' : [          8.0, 7.0, 6.0, -inf,           4.0, 3.0,           2.0],
})

DF_Log2_Full_0 = pd.DataFrame({
    'A' : [1.0, 2.0, 3.0, 4.0, 0.0, 5.0, 6.0],
    'B' : [2.0, 3.0, 4.0, 0.0, 5.0, 6.0, 7.0],
    'C' : [7.0, 6.0, 5.0, 4.0, 0.0, 3.0, 2.0],
    'D' : [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
    'E' : [6.0, 5.0, 4.0, 3.0, 2.0, 1.0, 0.0],
    'F' : [8.0, 7.0, 6.0, 0.0, 4.0, 3.0, 2.0],
})

DF_Log2_0_2_4_0 = pd.DataFrame({
    'A' : [1.0, 2.0, 3.0, 4.0, 0.0, 5.0, 6.0],
    'B' : [  4,   8,  16,   0,  32,  64, 128],
    'C' : [7.0, 6.0, 5.0, 4.0, 0.0, 3.0, 2.0],
    'D' : [  0,   2,   4,   8,  16,  32,  64],
    'E' : [6.0, 5.0, 4.0, 3.0, 2.0, 1.0, 0.0],
    'F' : [256, 128,  64,   0,  16,   8,   4],
})

DF_Log2_0_1_2_NA = pd.DataFrame({
    'A' : [1.0, 2.0, 3.0,          4.0, nan, 5.0, 6.0],
    'B' : [2.0, 3.0, 4.0, nan,          5.0, 6.0, 7.0],
    'C' : [7.0, 6.0, 5.0,          4.0, nan, 3.0, 2.0],
    'D' : [  0,   2,   4,            8,           16,  32,  64],
    'E' : [ 64,  32,  16,            8,            4,   2,   0],
    'F' : [256, 128,  64,            0,           16,   8,   4],
})

DF_Median = pd.DataFrame({
    'A' : [  2,   4,  8],
    'B' : [  4, nan, 16],
    'C' : [128,  64, 32],
    'D' : [  0,   2,  4],
    'E' : [ 64,  32, 16],
    'F' : [256, 128, 64],
})

DF_Median_Full = pd.DataFrame({
    'A' : [ -2.0, 0.0,   4.0],
    'B' : [ -6.0, nan,   6.0],
    'C' : [ 64.0, 0.0, -32.0],
    'D' : [ -2.0, 0.0,   2.0],
    'E' : [ 32.0, 0.0, -16.0],
    'F' : [128.0, 0.0, -64.0],
})

DF_Median_0_2_4 = pd.DataFrame({
    'A' : [ -2.0, 0.0,   4.0],
    'B' : [    4, nan,  16],
    'C' : [ 64.0, 0.0, -32.0],
    'D' : [    0,   2,   4],
    'E' : [ 32.0, 0.0, -16.0],
    'F' : [  256, 128,  64],
})

DF_DataPrep_1 = pd.DataFrame({
    'Intensity 01' : [0.000,16.694,19.152,19.221,17.323,0.000,0.000,16.440,16.691,0.000,0.000,0.000,0.000,0.000,0.000,0.000,16.571,0.000,14.962,0.000],
    'Intensity 02' : [0.000,18.312,19.212,19.240,17.257,17.063,0.000,18.122,17.542,0.000,0.000,0.000,17.390,0.000,16.018,0.000,16.108,0.000,16.291,0.000],
    'Intensity 03' : [0.000,0.000,19.190,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000],
    'Intensity 04' : [0.000,0.000,20.164,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000],
    'Intensity 05' : [0.000,16.257,19.491,20.658,18.717,17.474,0.000,17.141,17.353,0.000,0.000,0.000,16.615,0.000,0.000,0.000,17.846,0.000,17.671,19.186],
})
#endregion -----------------------------------------------------> pd.DataFrame



#region -------------------------------------------------------------> Classes
class Test_DataPrep_Float(unittest.TestCase):
    """Test for dataprep.method.DataPrep_Float"""
    #region -------------------------------------------------> Expected Output
    def test_expected_output(self):
        """Test for expected output"""
        #------------------------------>
        tInput = [
            (DF_DataPrep_Float,  True, [0,1,2,5], [0,1,3], [0,1,3], DF_DataPrep_Float.iloc[:,[0,1,2,5]], DF_DataPrep_Float_True),
            (DF_DataPrep_Float, False, [0,1,2,5], [0,1,3],   [0,3], DF_DataPrep_Float.iloc[:,[0,1,2,5]], DF_DataPrep_Float_False),
        ]
        #------------------------------>
        for a,b,c,d,e,f,g in tInput:
            with self.subTest(
                f'df={a}, cero={b}, col={c}, colCero={d}, colFloat={e}'):
                #------------------------------>
                dfI, dfF = dataMethod.DataPrep_Float(a, b, c, d, e)
                #------------------------------>
                # pylint: disable=protected-access
                pd._testing.assert_frame_equal(dfI, f)                          # type: ignore
                pd._testing.assert_frame_equal(dfF, g)                          # type: ignore
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_DataTransformation(unittest.TestCase):
    """Test for dataprep.method.DataTransformation"""
    #region -------------------------------------------------> Expected Output
    #------------------------------> Log2
    def test_output(self):
        """Test method output"""
        #------------------------------>
        tInput = [
            (DF_Log2,      [], 'None', None, DF_Log2),
            (DF_Log2,      [], 'Log2', None, DF_Log2_Full_None),
            (DF_Log2,      [], 'Log2',    0, DF_Log2_Full_0),
            (DF_Log2, [0,2,4], 'Log2',    0, DF_Log2_0_2_4_0),
            (DF_Log2, [0,1,2], 'Log2',  nan, DF_Log2_0_1_2_NA),
        ]
        #------------------------------>
        for a,b,c,d,e in tInput:
            with self.subTest(f"df=DF_Log2, sel={b}, method={c}, rep={d}"):
                #------------------------------>
                result = dataMethod.DataTransformation(
                    a, sel=b, method=c, rep=d)
                #------------------------------>
                # pylint: disable=protected-access
                pd._testing.assert_frame_equal(result, e)                       # type: ignore
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_DataNormalization(unittest.TestCase):
    """Test for dataprep.method.DataNormalization"""
    #region -------------------------------------------------> Expected Output
    #------------------------------> Log2
    def test_output(self):
        """Test method output"""
        #------------------------------>
        tInput = [
            (DF_Median,      [],   'None', DF_Median),
            (DF_Median,      [], 'Median', DF_Median_Full),
            (DF_Median, [0,2,4], 'Median', DF_Median_0_2_4),
        ]
        #------------------------------>
        for a,b,c,d in tInput:
            with self.subTest(f"df={a}, sel={b}, method={c}"):
                #------------------------------>
                result = dataMethod.DataNormalization(
                    a, sel=b, method=c)
                #------------------------------>
                # pylint: disable=protected-access
                pd._testing.assert_frame_equal(result, d)                       # type: ignore
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_DataImputation(unittest.TestCase):
    """Test for dataprep.method.DataImputation"""
    #region -------------------------------------------------> Expected Output
    def test_output(self):
        """Test method output"""
        #------------------------------>
        tInput = [
            (DF_Median, [], 'None', DF_Median),
        ]
        #------------------------------>
        for a,b,c,d in tInput:
            with self.subTest(f"df={a}, sel={b}, method={c}"):
                #------------------------------>
                result = dataMethod.DataImputation(
                    a, sel=b, method=c)
                #------------------------------>
                # pylint: disable=protected-access
                pd._testing.assert_frame_equal(result, d)                       # type: ignore
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_DataPreparation(unittest.TestCase):
    """Test for dataprep.method.DataPreparation"""
    #region -----------------------------------------------------> Class Setup
    @classmethod
    def setUpClass(cls):                                                        # pylint: disable=arguments-differ
        """Set test"""
        cls.df    = cFile.ReadCSV2DF(fileA)
        cls.dict1 = dataMethod.UserData(
            cero          = False,
            tran          = 'Log2',
            norm          = 'Median',
            imp           = 'None',
            shift         = 1.8,
            width         = 0.3,
            ocColumn      = [98,99,100,101,102],
            ocResCtrlFlat = [0,1,2,3,4],
        )
    #---
    #endregion --------------------------------------------------> Class Setup

    #region -------------------------------------------------> Expected Output
    def test_output(self):
        """Test method output"""
        #------------------------------>
        tInput = [
            (self.df, self.dict1, True, DF_DataPrep_1),
        ]
        #------------------------------>
        for a,b,c,d in tInput:
            with self.subTest(f"df={a}, rDO={b}, resetIndex={c}"):
                #------------------------------>
                result = dataMethod.RunDataPreparation(
                    df=a, rDO=b, resetIndex=c)[0]['dfS']
                result = result.round(3)
                result = result.iloc[range(0,20),:]
                #------------------------------>
                # pylint: disable=protected-access
                pd._testing.assert_frame_equal(result, d)                       # type: ignore
    #---
    #endregion ----------------------------------------------> Expected Output
#---
#endregion ----------------------------------------------------------> Classes
