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
#endregion -----------------------------------------------------> pd.DataFrame


#region ---------------------------------------------------------> Class Setup
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
#endregion ------------------------------------------------------> Class Setup
