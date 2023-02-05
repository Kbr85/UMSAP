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


"""Tests for core.statistic"""


#region -------------------------------------------------------------> Imports
import unittest
from pathlib import Path

import pandas as pd
from numpy import nan

from core import statistic as cStatistic
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------> File Location
folder  = Path(__file__).parent / 'files'

#endregion ----------------------------------------------------> File Location


#region --------------------------------------------------------> pd.DataFrame
DF_CI_Mean = pd.DataFrame({
    'CI_l' : [-8.17, -1.88, 1.90, -1.30, -2.43, 0.3, -4.74],
    'CI_u' : [16.17, 9.88, 6.10, 5.97, 7.43, 7.37, 12.40]
})


DF_Log2 = pd.DataFrame({
    'A' : [  2,   4,  8, 16,  0, 32,  64],
    'B' : [  4,   8, 16,  0, 32, 64, 128],
    'C' : [128,  64, 32, 16,  0,  8,   4],
    'D' : [  0,   2,  4,  8, 16, 32,  64],
    'E' : [ 64,  32, 16,  8,  4,  2,   0],
    'F' : [256, 128, 64,  0, 16,  8,   4],
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


DF_chiTest = pd.DataFrame({
    'A' : [ 5, 6, 7, 8, 9],
    'B' : [ 1, 2, 3,30,35],
    'C' : [ 5, 6, 7, 8, 9],
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

#endregion -----------------------------------------------------> pd.DataFrame


#region ---------------------------------------------------------> Class Setup
class Test_DataRange(unittest.TestCase):
    """Test for core.statistic.DataRange"""
    #region -----------------------------------------------------> Class Setup
    def setUp(self):
        """Set test"""
        self.Tlist = [1,2,3,4,5]
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
                    ValueError,
                    cStatistic.DataRange,
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
                result = cStatistic.DataRange(a,margin=b)
                #------------------------------>
                self.assertEqual(result, c)
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_CI_Sample(unittest.TestCase):
    """Test for core.statistic.CI_Sample"""
    #region -----------------------------------------------------> Class Setup
    def setUp(self):
        """Set test"""
        self.dfA = pd.DataFrame({
            'CI' : [179.2944069, 83.3328547, 30.35666427, 22.94748123, 45.89496245, 69.79203948, 154.043247],
            'LL' : [-134.6277402, -57.99952137, -11.6899976, -12.28081456, -35.22829578, -35.12537281, -88.70991364],
            'UL' : [223.9610735, 108.666188, 49.02333094, 33.61414789, 56.56162912, 104.4587061, 219.3765803],
        })
        self.dfB = pd.DataFrame({
            'CI' : [21.33168297, 42.66336593, 42.66336593],
            'LL' : [-3.331682966, -6.663365932, -6.663365932],
            'UL' : [39.33168297, 78.66336593, 78.66336593],
        })
    #---
    #endregion --------------------------------------------------> Class Setup

    #region -------------------------------------------------> Expected Output
    def test_expected_output(self):
        """Test for expected output"""
        #------------------------------>
        tInput = [
            (DF_Log2.iloc[:,[0,1,2]], 0.05, 1, None, self.dfA),
            (DF_Log2.iloc[:,[0,1,2]], 0.05, 0, None, self.dfB),
            (DF_Log2.iloc[:,[0,1,2]], 0.05, 0, 2,    self.dfB.round(2)),
        ]
        #------------------------------>
        for a,b,c,d,e in tInput:
            with self.subTest(f"df={a}, alpha={b}, axis={c}, roundN={d}"):
                #------------------------------>
                result = cStatistic.CI_Sample(a, b, axis=c, roundN=d)
                #------------------------------>
                # pylint: disable=protected-access
                pd._testing.assert_frame_equal(result, e)                       # type: ignore
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_CI_Mean_Diff(unittest.TestCase):
    """Test for core.statistic.CI_Mean_Diff"""
    #region -----------------------------------------------------> Class Setup
    def setUp(self):
        """Set test"""
        self.dfA = pd.DataFrame({
            'CI' : [242.8856155, 118.4182679, 54.53278713, 16.55551998, 31.6292765, 51.7277215, 114.819424],
            'LL' : [-304.8856155, -147.0849346, -63.86612046, -11.22218664, -32.96260984, -31.06105484, -72.15275732],
            'UL' : [180.8856155, 89.75160125, 45.1994538, 21.88885331, 30.29594317, 72.39438817, 157.4860907],
        })
        self.dfB = pd.DataFrame({
            'CI' : [26.86220863, 42.47288113, 86.86151901],
            'LL' : [-26.86220863, -24.47288113, -118.861519],
            'UL' : [26.86220863, 60.47288113, 54.86151901],
        })
        self.dfC = pd.DataFrame({
            'CI' : [274.3139, 136.4241, 68.6797, 19.193, 40.1394, 57.6398, 127.0213],
            'LL' : [-336.3139,-165.0908, -78.013, -13.8596, -41.4727, -36.9731, -84.3547],
            'UL' : [212.3139,107.7575, 59.3464, 24.5263, 38.806, 78.3064, 169.688],
        })
        self.dfD = pd.DataFrame({
            'CI' : [26.8622, 44.2324, 90.6806],
            'LL' : [-26.8622, -26.2324, -122.6806],
            'UL' : [26.8622, 62.2324, 58.6806],
        })
    #---
    #endregion --------------------------------------------------> Class Setup

    #region -------------------------------------------------> Expected Output
    def test_expected_output(self):
        """Test for expected output"""
        #------------------------------>
        tInput = [
            (DF_Log2.iloc[:,[0,1,2]], DF_Log2.iloc[:,[3,4,5]], 0.05, True,  1, None, self.dfA),
            (DF_Log2.iloc[:,[0,1,2]], DF_Log2.iloc[:,[3,4,5]], 0.05, True,  0, None, self.dfB),
            (DF_Log2.iloc[:,[0,1,2]], DF_Log2.iloc[:,[3,4,5]], 0.05, False, 1, None, self.dfC),
            (DF_Log2.iloc[:,[0,1,2]], DF_Log2.iloc[:,[3,4,5]], 0.05, False, 0, None, self.dfD),
            (DF_Log2.iloc[:,[0,1,2]], DF_Log2.iloc[:,[3,4,5]], 0.05, False, 0, 2, self.dfD.round(2)),
        ]
        #------------------------------>
        for a,b,c,d,e,f,g in tInput:
            with self.subTest(f"dfA={a}, dfB={b}, alpha={c}, equal_var={d}, axis={e}, roundN={f}"):
                #------------------------------>
                result = cStatistic.CI_Mean_Diff(a, b, c, equal_var=d, axis=e, roundN=f)
                #------------------------------>
                # pylint: disable=protected-access
                pd._testing.assert_frame_equal(result, g)                       # type: ignore
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_Tost_delta(unittest.TestCase):
    """Test for core.statistic.Test_tost_delta"""
    #region -------------------------------------------------> Expected Output
    def test_expected_output(self):
        """Test for expected output"""
        #------------------------------>
        tInput = [
            (DF_tost_delta, 0.05, 0.05, 0.8, 1, 0, None, pd.Series([3.25, 2.29])),
            (DF_tost_delta, 0.05, 0.05, 0.8, 1, 0, 3,    pd.Series([3, 2.29])),
        ]
        #------------------------------>
        for a,b,c,d,e,f,g,h in tInput:
            msg = (f'df={a}, alpha={b}, beta={c}, gamma={d}, axis={e}, d={f}, deltaMax={g}')
            with self.subTest(msg):
                #------------------------------>
                r = cStatistic.Tost_delta(a,b,c,d,axis=e, d=f, deltaMax=g)
                r = r.round(2)
                #------------------------------>
                # pylint: disable=protected-access
                pd._testing.assert_series_equal(r, h)                           # type: ignore
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
                result = cStatistic.Test_chi(a,b,c)[0]
                #------------------------------>
                self.assertEqual(result, d)
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_slope(unittest.TestCase):
    """Test for core.statistic.Test_slope"""
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
                r = cStatistic.Test_slope(a,b)
                r[0] = int(f'{r[0]*100:.0f}')
                r[1] = int(f'{r[1]*100:.0f}')
                r[2] = int(f'{r[2]*100000000:.0f}')
                #------------------------------>
                self.assertEqual(r, [74, 74, 32])
    #---
    #endregion ----------------------------------------------> Expected Output
#---
#endregion ------------------------------------------------------> Class Setup
