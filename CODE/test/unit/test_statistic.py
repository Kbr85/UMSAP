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


"""Tests for data.statistic """


#region -------------------------------------------------------------> Imports
import unittest
from pathlib import Path

import pandas as pd
from numpy import nan, inf

import data.exception as mException
import data.statistic as mStatistic
import data.file      as mFile
#endregion ----------------------------------------------------------> Imports


# Test data lead to long lines, so this check will be disabled for this module
# pylint: disable=line-too-long


#region ---------------------------------------------------------------> Files
folder = Path(__file__).parent / 'test_files'
tarprotData = folder / 'tarprot-data-file.txt'
#endregion ------------------------------------------------------------> Files


#region --------------------------------------------------------> pd.DataFrame
DF_CI_Mean = pd.DataFrame({
    'CI_l' : [-8.17, -1.88, 1.90, -1.30, -2.43, 0.3, -4.74],
    'CI_u' : [16.17, 9.88, 6.10, 5.97, 7.43, 7.37, 12.40]
})

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

DF_CI_DIFF_MEAN_IS = pd.DataFrame({
    'A' : [1.0, 2.0, 3.0, 4.0, 0.0, 5.0, 6.0],
    'B' : [2.0, 3.0, 4.0, 0.0, 5.0, 6.0, 7.0],
    'C' : [7.0, 6.0, 5.0, 4.0, 0.0, 3.0, 2.0],
    'D' : [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 1.0],
    'E' : [6.0, 5.0, 4.0, 3.0, 2.0, 1.0, 6.0],
    'F' : [8.0, 7.0, 6.0, 0.0, 4.0, 3.0, 24.0],
})

DF_CI_Mean_False = pd.DataFrame({
    'CI' : [12.17, 5.88, 2.1, 3.64, 4.93, 3.53, 8.57],
})

DF_CI_Mean_Diff_PS = pd.DataFrame({
    'CI_l' : [-14.40, -5.13, -2.48, -31.30, -38.91, -22.37, -42.91],
    'CI_u' : [17.07, 6.46, 2.48, 29.97, 42.24, 19.03, 38.24],
})

DF_CI_Mean_Diff_IS = pd.DataFrame({
    'CI_l' : [-7.10, -5.26, -3.58, -5.29, -3.32, -5.70, -14.52],
    'CI_u' : [ 9.76,  6.59,  3.58,  3.96,  6.65,  2.37,  25.18],
})

DF_CI_Mean_Diff_IS_False = pd.DataFrame({
    'CI' : [8.43, 5.93, 3.58, 4.63, 4.98, 4.03, 19.85],
})

DF_tTest_PS_In = pd.DataFrame({
    'A' : [1.0, 2.0, 3.0, 4.0, 0.0, 5.0,  1.0],
    'B' : [2.0, 3.0, 4.0, 0.0, 5.0, 6.0,  2.0],
    'C' : [7.0, 6.0, 5.0, 4.0, 0.0, 3.0,  3.0],
    'D' : [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 21.0],
    'E' : [6.0, 5.0, 4.0, 3.0, 2.0, 1.0, 23.0],
    'F' : [8.0, 7.0, 6.0, 0.0, 4.0, 3.0, 24.0],
})

DF_fTest_PS_Out = pd.DataFrame({
    'f' : [1.67742, 2.15385, 4.00000, 1.77778, 6.25000, 1.71429, 2.33333],
    'P' : [0.74699, 0.63415, 0.40000, 0.72000, 0.27586, 0.73684, 0.60000],
    'S' : [  False,   False,   False,   False,   False,   False,   False],
})

DF_chiTest = pd.DataFrame({
    'A' : [ 5, 6, 7, 8, 9],
    'B' : [ 1, 2, 3,30,35],
    'C' : [ 5, 6, 7, 8, 9],
})

DF_tTest_PS_Out = pd.DataFrame({
    't' : [0.91766, 0.75593, 0.00000, -0.32880, 0.71429, -1.00000, 62.00000],
    'P' : [0.45567, 0.52860, 1.00000,  0.77354, 0.54917,  0.42265,  0.00026],
    'S' : [  False,   False,   False,    False,   False,    False,     True],
})

DF_tTest_IS_Out_None_False = pd.DataFrame({
    't' : [0.43906, 0.31235, 0.00000, -0.40000, 0.92848, -1.14708, 19.60612],
    'P' : [0.67895, 0.76738, 1.00000,  0.70567, 0.39577,  0.30326,  0.00001],
    'S' : [  False,   False,   False,    False,   False,    False,     True],
})

DF_tTest_IS_Out_True = pd.DataFrame({
    't' : [0.43906, 0.31235, 0.00000, -0.40000, 0.92848, -1.14708, 19.60612],
    'P' : [0.68467, 0.77235, 1.00000,  0.71111, 0.43042,  0.31938,  0.00012],
    'S' : [  False,   False,   False,    False,   False,    False,     True],
})

DF_tost_delta = pd.DataFrame({
    'A' : [90.8, 86.2],
    'B' : [88.0, 87.4],
    'C' : [90.5, 88.2],
    'D' : [90.0, 89.7],
    'E' : [91.0, 87.3],
    'F' : [86.0, 87.6],
    'G' : [88.3, 88.0],
    'H' : [89.3, 86.5],
    'I' : [88.9, 89.6],
    'J' : [91.1, 89.1],
    'K' : [86.2, 86.1],
    'L' : [91.3, 86.2],
    'M' : [89.3, 87.7],
})

DF_tost = pd.DataFrame({
    'A' : [ 8, 2],
    'B' : [ 7, 4],
    'C' : [ 6, 3],
    'D' : [30, 1],
    'E' : [35, 1],
    'F' : [33, 2]
})

DF_tost_I = pd.DataFrame({
    'P' : [ 0.9999,   0.0001],
    't1': [21.8427,  10.2258],
    'p1': [ 0.0000,   0.0001],
    's1': [   True,     True],
    't2': [10.9902, -15.2258],
    'p2': [ 0.9999,   0.0000],
    's2': [  False,     True],
})

DF_tost_II = pd.DataFrame({
    'P' : [ 0.9985,   0.0008],
    't1': [21.8427,  10.2258],
    'p1': [ 0.0002,   0.0008],
    's1': [   True,     True],
    't2': [10.9902, -15.2258],
    'p2': [ 0.9985,   0.0002],
    's2': [  False,     True],
})

DF_tost_III = pd.DataFrame({
    'P' : [ 0.9999,   0.0001],
    't1': [21.8427,  10.2258],
    'p1': [ 0.0000,   0.0001],
    's1': [   True,     True],
    't2': [10.9902, -15.2258],
    'p2': [ 0.9999,   0.0000],
    's2': [  False,     True],
})

DF_tost_IV = pd.DataFrame({
    'P' : [ 0.9943,   0.0047],
    't1': [18.4008,  10.2258],
    'p1': [ 0.0015,   0.0047],
    's1': [   True,     True],
    't2': [ 9.2584, -15.2258],
    'p2': [ 0.9943,   0.0021],
    's2': [  False,     True],
})

DF_test_slope = pd.DataFrame({
    'Xa': [14,10, 7,18,14,16,13,15, 5,18,16,10, nan],
    'Ya': [29,24,14,27,27,28,27,32,13,35,32,17, nan],
    'Xb': [ 6,16, 9,19,13,14,15,18,17, 8,15,16, nan],
    'Yb': [15,28,13,36,29,27,31,33,32,15,30,26, nan],
    'Xc': [15, 9, 7,12,12, 9,12, 3,13,10,11, 8, nan],
    'Yc': [32,27,15,23,26,17,25,14,29,22,30,25, nan],
    'Xd': [14,10, 7,18,14,16,13,15, 5,18,16,10, nan],
    'Yd': [29,24,14,27,27,28,27,32,13,35,32,17, nan],
    'Xe': [ 6,16, 9,19,13,14,15,18,17, 8,15,16, nan],
    'Ye': [15,28,13,36,29,27,31,33,32,15,30,26, nan],
    'Xf': [15, 9, 7,12,12, 9,12, 3,13,10,11, 8, nan],
    'Yf': [32,27,15,23,26,17,25,14,29,22,30,25, nan],
    'Xg': [ 6,16, 9,19,13,14,15,18,17, 8,15,16, nan],
    'Yg': [15,28,13,36,29,27,31,33,32,15,30,26, nan],
    'Xh': [ 6,16, 9,19,13,14,15,18,17, 8,15,16, nan],
    'Yh': [-10,-20,-15,-40,-25,-21,-34,-30,-38,-19,-24,-21, nan],
})

DF_DataPrep_1 = pd.DataFrame({
    'Intensity 01' : [0.000,16.694,19.152,19.221,17.323,0.000,0.000,16.440,16.691,0.000,0.000,0.000,0.000,0.000,0.000,0.000,16.571,0.000,14.962,0.000],
    'Intensity 02' : [0.000,18.312,19.212,19.240,17.257,17.063,0.000,18.122,17.542,0.000,0.000,0.000,17.390,0.000,16.018,0.000,16.108,0.000,16.291,0.000],
    'Intensity 03' : [0.000,0.000,19.190,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000],
    'Intensity 04' : [0.000,0.000,20.164,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000,0.000],
    'Intensity 05' : [0.000,16.257,19.491,20.658,18.717,17.474,0.000,17.141,17.353,0.000,0.000,0.000,16.615,0.000,0.000,0.000,17.846,0.000,17.671,19.186],
})
#endregion -----------------------------------------------------> pd.DataFrame


#region ---------------------------------------------------------> Class Setup
class Test_DataRange(unittest.TestCase):
    """Test for data.statistic.DataRange"""
    #region -----------------------------------------------------> Class Setup
    @classmethod
    def setUp(cls):                                                             # pylint: disable=arguments-differ
        """Set test"""
        cls.Tlist = [1,2,3,4,5]
    #---
    #endregion --------------------------------------------------> Class Setup

    #region -----------------------------------------------------> Valid Input
    def test_invalid_input(self):
        """Test for invalid input"""
        #------------------------------>
        badInput = [
            (DF_CI_Mean, 0),
            (['a', 'b', 1, 2], 0.04),
            ([], 0.04),
        ]
        #------------------------------>
        for a,b in badInput:
            with self.subTest(f'x={a}, margin={b}'):
                self.assertRaises(
                    mException.InputError,
                    mStatistic.DataRange,
                    a,
                    margin=b,
                )
    #---
    #endregion --------------------------------------------------> Valid Input

    #region -------------------------------------------------> Expected Output
    def test_expected_output(self):
        """Test for expected output"""
        #------------------------------>
        tInput = [
            (self.Tlist,     0, [  1,   5]),
            (self.Tlist,   0.1, [0.6, 5.4]),
            (DF_Log2['A'], 0.5, [-32,  96]),
        ]
        #------------------------------>
        for a,b,c in tInput:
            with self.subTest(f'x={a}, margin={b}'):
                #------------------------------>
                result = mStatistic.DataRange(a,margin=b)
                #------------------------------>
                self.assertEqual(result, c)
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_DataPrep_Float(unittest.TestCase):
    """Test for data.statistic.DataPrep_Float"""
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
                dfI, dfF = mStatistic.DataPrep_Float(a, b, c, d, e)
                #------------------------------>
                # pylint: disable=protected-access
                pd._testing.assert_frame_equal(dfI, f)                          # type: ignore
                pd._testing.assert_frame_equal(dfF, g)                          # type: ignore
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_DataTransformation(unittest.TestCase):
    """Test for data.statistic.DataTransformation"""
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
                result = mStatistic.DataTransformation(
                    a, sel=b, method=c, rep=d)
                #------------------------------>
                # pylint: disable=protected-access
                pd._testing.assert_frame_equal(result, e)                       # type: ignore
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_DataNormalization(unittest.TestCase):
    """Test for data.statistic.DataNormalization"""
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
                result = mStatistic.DataNormalization(
                    a, sel=b, method=c)
                #------------------------------>
                # pylint: disable=protected-access
                pd._testing.assert_frame_equal(result, d)                       # type: ignore
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_DataImputation(unittest.TestCase):
    """Test for data.statistic.DataImputation"""
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
                result = mStatistic.DataImputation(
                    a, sel=b, method=c)
                #------------------------------>
                # pylint: disable=protected-access
                pd._testing.assert_frame_equal(result, d)                       # type: ignore
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_DataPreparation(unittest.TestCase):
    """Test for data.statistic.DataPreparation"""
    #region -----------------------------------------------------> Class Setup
    @classmethod
    def setUp(cls):                                                             # pylint: disable=arguments-differ
        """Set test"""
        cls.df = mFile.ReadCSV2DF(tarprotData)
        cls.dict1 = {
            'Cero' : False,
            'TransMethod' : 'Log2',
            'NormMethod'  : 'Median',
            'ImpMethod'   : 'None',
            'Shift'       : 1.8,
            'Width'       : 0.3,
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
            (self.df, self.dict1, True, DF_DataPrep_1),
        ]
        #------------------------------>
        for a,b,c,d in tInput:
            with self.subTest(f"df={a}, rDO={b}, resetIndex={c}"):
                #------------------------------>
                result = mStatistic.DataPreparation(
                    a, b, resetIndex=c)[0]['dfS']
                result = result.round(3)
                result = result.iloc[range(0,20),:]
                #------------------------------>
                # pylint: disable=protected-access
                pd._testing.assert_frame_equal(result, d)                       # type: ignore
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_CI_Mean_Diff_DF(unittest.TestCase):
    """Test for data.statistic.CI_Mean_Diff_DF"""
    #region -------------------------------------------------> Expected Output
    def test_output(self):
        """Test for method output"""
        #------------------------------>
        tInput = [
            (DF_Log2_Full_0,     [0,1,2], [3,4,5], 0.05, False,  True, 2, DF_CI_Mean_Diff_PS),
            (DF_CI_DIFF_MEAN_IS, [0,1,2], [3,4,5], 0.05,  True,  True, 2, DF_CI_Mean_Diff_IS),
            (DF_CI_DIFF_MEAN_IS, [0,1,2], [3,4,5], 0.05,  True, False, 2, DF_CI_Mean_Diff_IS_False),
        ]
        #------------------------------>
        for a,b,c,d,e,f,g,h in tInput:
            msg = (
                f'df=DF_Log2_Full_0, col1={b}, col2={c}, alpha={d}, ind={e}, '
                f'fullCI={f}, roundN={g}')
            with self.subTest(msg):
                #------------------------------>
                result = mStatistic.CI_Mean_Diff_DF(a,b,c,d,e,fullCI=f,roundN=g)
                #------------------------------>
                # pylint: disable=protected-access
                pd._testing.assert_frame_equal(result, h)                       # type: ignore
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_CI_Mean_DF(unittest.TestCase):
    """Test for data.statistic.CI_Mean_DF"""
    #region -------------------------------------------------> Expected Output
    def test_expected_output(self):
        """Test for expected output"""
        #------------------------------>
        tInput = [
            (DF_Log2_Full_0, '0.05',  True, 2, DF_CI_Mean),
            (DF_Log2_Full_0, '0.05', False, 2, DF_CI_Mean_False),
        ]
        #------------------------------>
        for a,b,c,d,e in tInput:
            msg = f"df=DF_Log2_Full_0, alpha={b}, fullCI={c}, roundN={d}"
            with self.subTest(msg):
                #------------------------------>
                result = mStatistic.CI_Mean_DF(a, b, fullCI=c, roundN=d)
                #------------------------------>
                # pylint: disable=protected-access
                pd._testing.assert_frame_equal(result, e)                       # type: ignore
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_f_DF(unittest.TestCase):
    """Test for data.statistic.Test_f_DF"""
    #region -------------------------------------------------> Expected Output
    def test_expected_output(self):
        """Test for expected output"""
        #------------------------------>
        tInput = [
            (DF_tTest_PS_In, [0,1,2], [3,4,5], 0.05,   5, DF_fTest_PS_Out),
            (DF_tTest_PS_In, [0,1,2], [3,4,5], 0.05, '5', DF_fTest_PS_Out),
        ]
        #------------------------------>
        for a,b,c,d,e,f in tInput:
            msg = (
                f'df={a}, col1={b}, col2={c}, alpha={d}, roundTo={e}'
            )
            with self.subTest(msg):
                #------------------------------>
                result = mStatistic.Test_f_DF(a,b,c,alpha=d,roundTo=e)
                #------------------------------>
                # pylint: disable=protected-access
                pd._testing.assert_frame_equal(result, f)                       # type: ignore
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_chi(unittest.TestCase):
    """Test for data.statistic.Test_chi"""
    #region -------------------------------------------------> Expected Output
    def test_expected_output(self):
        """Test for expected output"""
        #------------------------------>
        tInput = [
            (DF_chiTest.iloc[:,[0,1]], 0.05,  True, -1 ),
            (DF_chiTest.iloc[:,[0,1]], 0.05, False,  1,),
            (DF_chiTest.iloc[:,[0,2]], 0.05,  True,  0,),
            (DF_chiTest.iloc[:,[0,2]], 0.05, False,  0,),
        ]
        #------------------------------>
        for a,b,c,d in tInput:
            msg = (
                f'df={a}, alpha={b}, check5={c}'
            )
            with self.subTest(msg):
                #------------------------------>
                result = mStatistic.Test_chi(a,b,c)[0]
                #------------------------------>
                self.assertEqual(result, d)
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_t_PS_DF(unittest.TestCase):
    """Test for data.statistic.Test_t_PS_DF"""
    #region -------------------------------------------------> Expected Output
    def test_expected_output(self):
        """Test for expected output"""
        #------------------------------>
        tInput = [
            (DF_tTest_PS_In, [0,1,2], [3,4,5], 0.05,   5, DF_tTest_PS_Out),
            (DF_tTest_PS_In, [0,1,2], [3,4,5], 0.05, '5', DF_tTest_PS_Out),
        ]
        #------------------------------>
        for a,b,c,d,e,f in tInput:
            msg = (
                f'df={a}, col1={b}, col2={c}, alpha={d}, roundTo={e}'
            )
            with self.subTest(msg):
                #------------------------------>
                result = mStatistic.Test_t_PS_DF(a,b,c,alpha=d,roundTo=e)
                #------------------------------>
                # pylint: disable=protected-access
                pd._testing.assert_frame_equal(result, f)                       # type: ignore
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_t_IS_DF(unittest.TestCase):
    """Test for data.statistic.Test_t_IS_DF"""
    #region -------------------------------------------------> Expected Output
    def test_expected_output(self):
        """Test for expected output"""
        #------------------------------>
        tInput = [
            (DF_tTest_PS_In, [0,1,2], [3,4,5], 0.05,  None,   5, DF_tTest_IS_Out_None_False),
            (DF_tTest_PS_In, [0,1,2], [3,4,5], 0.05, False,   5, DF_tTest_IS_Out_None_False),
            (DF_tTest_PS_In, [0,1,2], [3,4,5], 0.05,  True, '5', DF_tTest_IS_Out_True),
        ]
        #------------------------------>
        for a,b,c,d,e,f,g in tInput:
            msg = (
                f'df={a}, col1={b}, col2={c}, alpha={d}, f={e}, '
                f'roundTo={f}'
            )
            with self.subTest(msg):
                #------------------------------>
                result = mStatistic.Test_t_IS_DF(a,b,c,alpha=d,f=e,roundTo=f)
                #------------------------------>
                # pylint: disable=protected-access
                pd._testing.assert_frame_equal(result, g)                       # type: ignore
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_tost(unittest.TestCase):
    """Test for data.statistic.Test_tost"""
    #region -------------------------------------------------> Expected Output
    def test_expected_output(self):
        """Test for expected output"""
        #------------------------------>
        tInput = [
            (DF_tost, [0,1,2], [3,4,5], 'i',  None, None, 0.05, 0.05, 0.8, 0, None, DF_tost_I),
            (DF_tost, [0,1,2], [3,4,5], 'i',  True, None, 0.05, 0.05, 0.8, 0, None, DF_tost_II),
            (DF_tost, [0,1,2], [3,4,5], 'i', False, None, 0.05, 0.05, 0.8, 0, None, DF_tost_III),
            (DF_tost, [0,1,2], [3,4,5], 'p',  None, None, 0.05, 0.05, 0.8, 0, None, DF_tost_IV),
        ]
        #------------------------------>
        for a,b,c,d,e,f,g,h,i,j,k,l in tInput:
            msg = (f'df={a}, col1={b}, col2={c}, sample={d}, f={e}, delta={f}, '
                   f'alpha={g}, beta={h}, gamma={i}, d={j}, deltaMax={k}')
            with self.subTest(msg):
                #------------------------------>
                r = mStatistic.Test_tost(a,b,c,d,f=e,delta=f,alpha=g,beta=h,gamma=i,d=j,deltaMax=k)
                r = r.round(4)
                #------------------------------>
                # pylint: disable=protected-access
                pd._testing.assert_frame_equal(r, l)                            # type: ignore
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_tost_delta(unittest.TestCase):
    """Test for data.statistic.Test_tost_delta"""
    #region -------------------------------------------------> Expected Output
    def test_expected_output(self):
        """Test for expected output"""
        #------------------------------>
        tInput = [
            (DF_tost_delta, 0.05, 0.05, 0.8, 0, None, pd.Series([3.25, 2.29])),
        ]
        #------------------------------>
        for a,b,c,d,e,f,g in tInput:
            msg = (f'df={a}, alpha={b}, beta={c}, gamma={d}, d={e}, deltaMax={f}')
            with self.subTest(msg):
                #------------------------------>
                r = mStatistic.Test_tost_delta(a,b,c,d,e,f)
                r = r.round(2)
                #------------------------------>
                # pylint: disable=protected-access
                pd._testing.assert_series_equal(r, g)                           # type: ignore
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_test_slope(unittest.TestCase):
    """Test for data.statistic.Test_slope"""
    #region -------------------------------------------------> Expected Output
    def test_expected_output(self):
        """Test for expected output"""
        #------------------------------>
        tInput = [
            (DF_test_slope, [3,3,2]),
        ]
        #------------------------------>
        for a,b in tInput:
            msg = (f'df=DF_test_slope, nL={b}')
            with self.subTest(msg):
                #------------------------------>
                r = mStatistic.Test_slope(a,b)
                r[0] = int(f'{r[0]*100:.0f}')
                r[1] = int(f'{r[1]*100:.0f}')
                r[2] = int(f'{r[2]*100000000:.0f}')
                #------------------------------>
                self.assertEqual(r, [74, 74, 32])
    #---
    #endregion ----------------------------------------------> Expected Output
#---
#endregion ------------------------------------------------------> Class Setup
