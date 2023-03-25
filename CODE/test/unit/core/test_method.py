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


"""Tests for core.method"""


#region -------------------------------------------------------------> Imports
import unittest
from pathlib import Path

import pandas as pd
from numpy  import nan
from pandas import NA

from core    import method as cMethod
from core    import file   as cFile
from limprot import method as limpMethod
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------> File Location
folder = Path(__file__).parent / 'file'
fileA  = folder / 'fasta-tarprot-seq-both.txt'                                  # Fasta File with two seq
#endregion ----------------------------------------------------> File Location


#region --------------------------------------------> pd.DataFrame for Testing
DF_DFFilterByColS = pd.DataFrame({
    'A' : [1,2,3,4,5],
    'B' : ['1','2','1','2','1'],
})


DF_DFExclude = pd.DataFrame({
    'A' : [  1,   2,   3,   4,     5],
    'B' : [  1,   2,   3,   4,     5],
    'C' : [  1,   2,   3,   4,     5],
    'D' : [nan, nan, nan, nan, 'nan'],
    'E' : [  3, nan, nan, nan,   nan],
    'F' : [nan, nan,  '', nan,   nan],
    'G' : [ '',  '',  '',  '',    ''],
    'H' : [  1,   2,   3,   4,     5],
})


DF_DFFilterByColN = pd.DataFrame({
    'A' : [1,2,3,4,5],
    'B' : [1,2,3,4,5],
})


DF_DFReplace = pd.DataFrame({
    'A' : [  2,  '',  8, 16,  0, 32,  64],
    'B' : [  4,   8, 16,  0, 32, 64, 128],
    'C' : [128,  64, 32, 16,  0,  8,   4],
    'D' : [  0,   2,  4,  8, 16, 32,  64],
    'E' : [ 64,  32, 16, "",  4,  2,   0],
    'F' : [ "", 128, 64,  0, 16,  8,   4],
})


DF_DFReplace_0_NaN = pd.DataFrame({
    'A' : [  2,  '',  8, 16,  nan, 32,  64],
    'B' : [  4,   8, 16,  nan, 32, 64, 128],
    'C' : [128,  64, 32, 16,  nan,  8,   4],
    'D' : [  nan,   2,  4,  8, 16, 32,  64],
    'E' : [ 64,  32, 16, "",  4,  2,   nan],
    'F' : [ "", 128, 64,  nan, 16,  8,   4],
})


DF_DFReplace_0_empty_NaN = pd.DataFrame({
    'A' : [  2, nan,  8,  16, nan, 32,  64],
    'B' : [  4,   8, 16, nan,  32, 64, 128],
    'C' : [128,  64, 32,  16, nan,  8,   4],
    'D' : [nan,   2,  4,   8,  16, 32,  64],
    'E' : [ 64,  32, 16, nan,   4,  2, nan],
    'F' : [nan, 128, 64, nan,  16,  8,   4],
})


DF_DFReplace_0_empty_C_E = pd.DataFrame({
    'A' : [  2, 'E',  8,  16, 'C', 32,  64],
    'B' : [  4,   8, 16, 'C',  32, 64, 128],
    'C' : [128,  64, 32,  16, 'C',  8,   4],
    'D' : [ 'C',  2,  4,   8,  16, 32,  64],
    'E' : [ 64,  32, 16, "E",   4,  2, 'C'],
    'F' : ["E", 128, 64, 'C',  16,  8,   4],
})


DF_DFReplace_0_empty_NaN_0_1 = pd.DataFrame({
    'A' : [  2, nan,  8,  16, nan, 32,  64],
    'B' : [  4,   8, 16, nan,  32, 64, 128],
    'C' : [128,  64, 32,  16,   0,  8,   4],
    'D' : [  0,   2,  4,   8,  16, 32,  64],
    'E' : [ 64,  32, 16,  "",   4,  2,   0],
    'F' : [ "", 128, 64,   0,  16,  8,   4],
})

#endregion -----------------------------------------> pd.DataFrame for Testing


#region --------------------------------------------------------------> String
class Test_Str2ListNumber(unittest.TestCase):
    """Test for core.method.Str2ListNumber"""
    #region -----------------------------------------------------> Class Setup
    @classmethod
    def setUpClass(cls):
        """Set the line used by the test """
        cls.tStrC  = "1, 2, 3,  4  ,  5, 6  , 7, 6-10"
        cls.tStrCO = "  1, 2, 3, 6-10,  4  ,  5, 6  , 7   "
        cls.tStrS  = "   1 2 3  4    5 6   7 6-10  "
    #---
    #endregion --------------------------------------------------> Class Setup

    #region -----------------------------------------------------> Valid Input
    def test_invalid_input(self):
        """Test for invalid input"""
        #------------------------------>
        badInput = [
            (self.tStrC, 'badNumType', ',', False, KeyError),
            ('1, 2, 4b',        'int', ',', False, ValueError),
            ('50-10, 4, 7',     'int', ',', False, ValueError),
            ('1,2,3,4-',        'int', ',', False, ValueError),
        ]
        #------------------------------>
        for a,b,c,d, e in badInput:
            msg = f"tStr={a}, numType={b}, sep={c}, unique={d}"
            with self.subTest(msg):
                self.assertRaises(
                    e,
                    cMethod.Str2ListNumber,
                    a, numType=b, sep=c, unique=d,
                )
    #---
    #endregion --------------------------------------------------> Valid Input

    #region -------------------------------------------------> Expected Output
    def test_expected_output(self):
        """Expected output"""
        #------------------------------>
        tInput = [
            ( self.tStrC,    'int', ',', False, [1, 2, 3, 4, 5, 6, 7, 6, 7, 8, 9, 10]),
            ( self.tStrC,    'int', ',',  True, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
            ( self.tStrC,  'float', ',',  True, [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8, 9, 10]),
            (self.tStrCO,    'int', ',', False, [1, 2, 3, 6, 7, 8, 9, 10, 4, 5, 6, 7]),
            (self.tStrCO,    'int', ',',  True, [1, 2, 3, 6, 7, 8, 9, 10, 4, 5]),
            ( self.tStrS,    'int', ' ', False, [1, 2, 3, 4, 5, 6, 7, 6, 7, 8, 9, 10]),
        ]
        #------------------------------>
        for a,b,c,d,e in tInput:
            msg = f"tStr={a}, numType={b}, sep={c}, unique={d}"
            with self.subTest(msg):
                #------------------------------>
                result = cMethod.Str2ListNumber(a, numType=b, sep=c, unique=d)
                #------------------------------>
                self.assertEqual(result, e)
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_StrEqualLength(unittest.TestCase):
    """Test for core.method.StrEqualLength"""
    #region -------------------------------------------------> Expected Output
    def test_expected_output(self):
        """Test for expected output"""
        #------------------------------>
        tInput = [
            (['A', 'AA', 'AAA'], ' ', 'end',   ['A  ', 'AA ', 'AAA']),
            (['A', 'AA', 'AAA'], ' ', 'start', ['  A', ' AA', 'AAA']),
            (['A', 'AA', 'AAA'], ' ', 'bad',   ['  A', ' AA', 'AAA']),
        ]
        #------------------------------>
        for a,b,c,d in tInput:
            with self.subTest(f"strL={a}, char={b}, loc={c}"):
                #------------------------------>
                result = cMethod.StrEqualLength(a, char=b,loc=c)
                #------------------------------>
                self.assertEqual(result, d)
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_ResControl2ListNumber(unittest.TestCase):
    """Test for core.method.ResControl2ListNumber"""
    #region -------------------------------------------------> Expected Output
    def test_expected_output(self):
        """Test for expected output"""
        #------------------------------>
        tInput = [
            (',;,',                               [' ', ',', ';'], 'int', [[[], []], [[], []]]),
            ('0 1 2, 3 4 5; 6 7 8, 9 10 11',      [' ', ',', ';'], 'int', [[[0,1,2], [3,4,5]], [[6,7,8], [9,10,11]]]),
            ('0 1 2,; 6 7 8,',                    [' ', ',', ';'], 'int', [[[0,1,2], []], [[6,7,8], []]]),
            ('0-2, 3-5; 6-8, 9-11',               [' ', ',', ';'], 'int', [[[0,1,2], [3,4,5]], [[6,7,8], [9,10,11]]]),
            ('0-2, 3 4 5; 6-8, 9-11',             [' ', ',', ';'], 'int', [[[0,1,2], [3,4,5]], [[6,7,8], [9,10,11]]]),
            ('0-2 20, 3 4 5 21; 6-8 22, 23 9-11', [' ', ',', ';'], 'int', [[[0,1,2,20], [3,4,5, 21]], [[6,7,8, 22], [23,9,10,11]]]),
        ]
        #------------------------------>
        for a,b,c,d in tInput:
            with self.subTest(f"val={a}, sep={b}, numType={c}"):
                #------------------------------>
                result = cMethod.ResControl2ListNumber(a, sep=b, numType=c)
                #------------------------------>
                self.assertEqual(result, d)
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_ResControl2Flat(unittest.TestCase):
    """Test for core.method.ResControl2Flat"""
    #region -------------------------------------------------> Expected Output
    def test_expected_output(self):
        """Test for expected output"""
        #------------------------------>
        tInput = [
            ([[[], []], [[], []]], []),
            ([[[0,1,2], [3,4,5]], [[6,7,8], [9,10,11]]], [0,1,2,3,4,5,6,7,8,9,10,11]),
            ([[[0,1,2], []], [[6,7,8], []]], [0,1,2,6,7,8]),
            ([[[0,1,2], [3,4,5]], [[6,7,8], [9,10,11]]], [0,1,2,3,4,5,6,7,8,9,10,11]),
            ([[[0,1,2,20], [3,4,5, 21]], [[6,7,8, 22], [23,9,10,11]]], [0,1,2,20,3,4,5,21,6,7,8,22,23,9,10,11]),
        ]
        #------------------------------>
        for a,b in tInput:
            with self.subTest(f"val={a}"):
                #------------------------------>
                result = cMethod.ResControl2Flat(a)
                #------------------------------>
                self.assertEqual(result, b)
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_ResControl2DF(unittest.TestCase):
    """Test for core.method.ResControl2DF"""
    #region -------------------------------------------------> Expected Output
    def test_expected_output(self):
        """Test for expected output"""
        #------------------------------>
        tInput = [
            ([[[], []], [[], []]], 0, [[[], []], [[], []]]),
            ([[[0,1,2], [3,4,5]], [[6,7,8], [9,10,11]]], 0, [[[0,1,2],[3,4,5]],[[6,7,8],[9,10,11]]]),
            ([[[0,1,2], []], [[6,7,8], []]], 1, [[[1,2,3],[]], [[4,5,6],[]]]),
            ([[[0,1,2], [3,4,5]], [[6,7,8], [9,10,11]]], 2, [[[2,3,4],[5,6,7]],[[8,9,10],[11,12,13]]]),
            ([[[0,1,2,20], [3,4,5,21]], [[6,7,8,22], [23,9,10,11]]], 4, [[[4,5,6,7], [8,9,10,11]], [[12,13,14,15],[16,17,18,19]]]),
        ]
        #------------------------------>
        for a,b,c in tInput:
            with self.subTest(f"val={a}, start={b}"):
                #------------------------------>
                result = cMethod.ResControl2DF(a, b)
                #------------------------------>
                self.assertEqual(result, c)
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_ExpandRange(unittest.TestCase):
    """Test for core.method.ExpandRange"""
    #region -----------------------------------------------------> Valid Input
    def test_invalid_input(self):
        """Test for invalid input"""
        #------------------------------>
        badInput = [
            ('4-',  'int', ValueError),
            ('4-1', 'int', ValueError),
        ]
        #------------------------------>
        for a,b,c in badInput:
            msg = f"r={a}, numType={b}"
            with self.subTest(msg):
                self.assertRaises(
                    c,
                    cMethod.ExpandRange,
                    a, numType=b
                )
    #---
    #endregion --------------------------------------------------> Valid Input

    #region -------------------------------------------------> Expected Output
    def test_expected_output(self):
        """Expected output"""
        #------------------------------>
        tInput = [
            (   '4',   'int',           [4]),
            ( '4.9', 'float',         [4.9]),
            ('-5.4', 'float',        [-5.4]),
            ( '0-5',   'int', [0,1,2,3,4,5]),
        ]
        #------------------------------>
        for a,b,c in tInput:
            with self.subTest(f"r={a}, numType={b}"):
                #------------------------------>
                result = cMethod.ExpandRange(a, numType=b)
                #------------------------------>
                self.assertEqual(result, c)
    #---
    #endregion ----------------------------------------------> Expected Output
#---
#endregion -----------------------------------------------------------> String


#region --------------------------------------------------------> pd.DataFrame
class Test_DFFilterByColS(unittest.TestCase):
    """Test for core.method.DFFilterByColS"""
    #region -----------------------------------------------------> Class Setup
    @classmethod
    def setUpClass(cls):
        """Set test"""
        cls.a = DF_DFFilterByColS.iloc[[1,3],:]
        cls.b = DF_DFFilterByColS.iloc[[0,2,4],:]
    #---
    #endregion --------------------------------------------------> Class Setup

    #region -------------------------------------------------> Expected Output
    def test_expected_output(self):
        """Test for expected output"""
        #------------------------------>
        tInput = [
            (DF_DFFilterByColS, 1,   '2',  'e',  self.a),
            (DF_DFFilterByColS, 1,   '2', 'ne',  self.b),
            (DF_DFFilterByColS, 1,   '2', 'bad', self.b),
        ]
        #------------------------------>
        for a,b,c,d,e in tInput:
            with self.subTest(f'df={a}, col={b}, refVal={c}, comp={d}'):
                #------------------------------>
                result = cMethod.DFFilterByColS(a, b, c, d)
                #------------------------------>
                # pylint: disable=protected-access
                pd._testing.assert_frame_equal(result, e)                       # type: ignore
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_DFExclude(unittest.TestCase):
    """Test for core.method.DFExclude"""
    #region -----------------------------------------------------> Class Setup
    @classmethod
    def setUpClass(cls):
        """Set test"""
        cls.a = DF_DFExclude.iloc[0:4,:]
        cls.b = DF_DFExclude.iloc[1:4,:]
        cls.c = DF_DFExclude.iloc[[1,3],:]
        cls.d = DF_DFExclude.drop(index=DF_DFExclude.index)                     # type: ignore
    #---
    #endregion --------------------------------------------------> Class Setup

    #region -------------------------------------------------> Expected Output
    def test_expected_output(self):
        """Test for expected output"""
        #------------------------------>
        tInput = [
            (DF_DFExclude,       [3], self.a),
            (DF_DFExclude,     [3,4], self.b),
            (DF_DFExclude,   [3,4,5], self.c),
            (DF_DFExclude, [3,4,5,6], self.d),
        ]
        #------------------------------>
        for a,b,c in tInput:
            with self.subTest(f"df={a}, col={b}"):
                #------------------------------>
                result = cMethod.DFExclude(a,b)
                #------------------------------>
                # pylint: disable=protected-access
                pd._testing.assert_frame_equal(result, c)                       # type: ignore
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_DFFilterByColN(unittest.TestCase):
    """Test for core.method.DFFilterByColN"""
    #region -----------------------------------------------------> Class Setup
    @classmethod
    def setUpClass(cls):
        """Set test"""
        cls.a = DF_DFFilterByColN.iloc[2:5,:]
        cls.b = DF_DFFilterByColN.iloc[0,:].to_frame().transpose()
        cls.c = DF_DFFilterByColN.iloc[[0,1],:]
    #---
    #endregion --------------------------------------------------> Class Setup

    #region -------------------------------------------------> Expected Output
    def test_expected_output(self):
        """Test for expected output"""
        #------------------------------>
        tInput = [
            (DF_DFFilterByColN, [1],   2, 'gt', self.a),
            (DF_DFFilterByColN, [1],   2, 'lt', self.b),
            (DF_DFFilterByColN, [1], 2.0, 'le', self.c),
        ]
        #------------------------------>
        for a,b,c,d,e in tInput:
            with self.subTest(f'df={a}, col={b}, refVal={c}, comp={d}'):
                #------------------------------>
                result = cMethod.DFFilterByColN(a, b, c, d)
                #------------------------------>
                # pylint: disable=protected-access
                pd._testing.assert_frame_equal(result, e)                       # type: ignore
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_DFReplace(unittest.TestCase):
    """Test for core.method.DFReplace"""
    #region -------------------------------------------------> Expected Output
    def test_expected_output(self):
        """Test for expected output"""
        #------------------------------>
        tInput = [
            (DF_DFReplace, [0],          [nan],  None, DF_DFReplace_0_NaN),
            (DF_DFReplace, [0, ""], [nan, nan],  None, DF_DFReplace_0_empty_NaN),
            (DF_DFReplace, [0, ""],        nan,  None, DF_DFReplace_0_empty_NaN),
            (DF_DFReplace, [0, ""], [nan, nan], [0,1], DF_DFReplace_0_empty_NaN_0_1),
            (DF_DFReplace, [0, ""],        nan, [0,1], DF_DFReplace_0_empty_NaN_0_1),
            (DF_DFReplace, [0, ""], ['C', 'E'],  None, DF_DFReplace_0_empty_C_E),
        ]
        #------------------------------>
        for a,b,c,d,e in tInput:
            with self.subTest(f"df={a}, oriVal={b}, repVal={c}, sel={d}"):
                #------------------------------>
                result = cMethod.DFReplace(a, b, c, sel=d)
                #------------------------------>
                # pylint: disable=protected-access
                pd._testing.assert_frame_equal(result, e)                       # type: ignore
    #---
    #endregion ----------------------------------------------> Expected Output
#---
#endregion -----------------------------------------------------> pd.DataFrame


#region --------------------------------------------------------------> Others
class Test_NCResNumbers(unittest.TestCase):
    """Test for core.method.NCResNumbers"""
    #region -----------------------------------------------------> Class Setup
    @classmethod
    def setUpClass(cls):
        """Set test"""
        cls.df = pd.DataFrame({
            'Seq': ['HMKKTA', 'VALAG', 'SALLR', 'LRVMM'],
            'N'  : [nan, nan, nan, nan,],
            'C'  : [nan, nan, nan, nan,],
            'NF' : [nan, nan, nan, nan,],
            'CF' : [nan, nan, nan, nan,],
        })
        cls.do = limpMethod.UserData(
            dfSeq      = 0,
            seqFileObj = cFile.FastaFile(fileA),
            dfNC       = [1,2],
            dfNCF      = [3,4],
        )
        cls.dfRes = pd.DataFrame({
            'Seq': ['HMKKTA', 'VALAG', 'SALLR', 'LRVMM'],
            'N'  : [14, 24, 76, 79,],
            'C'  : [19, 28, 80, 83,],
            'NF' : [NA, 10, 62, 65,],
            'CF' : [5,  14, 66, NA,],
        })
        cls.dfRes.iloc[:,3:5] = cls.dfRes.iloc[:,3:5].astype('Int64')
    #---
    #endregion --------------------------------------------------> Class Setup

    #region -------------------------------------------------> Expected Output
    def test_output(self):
        """Test method output"""
        #------------------------------>
        tInput = [
            (self.df, self.do, True, self.dfRes),
        ]
        #------------------------------>
        for a,b,c,d in tInput:
            with self.subTest(f"dfR={a}, rDO={b}, seqNat={c}"):
                #------------------------------>
                result = cMethod.NCResNumbers(a,b,seqNat=c)[0]
                # pylint: disable=protected-access
                pd._testing.assert_frame_equal(result, d)                     # type: ignore
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_Fragments(unittest.TestCase):
    """Test for core.method.Fragments"""
    #region -----------------------------------------------------> Class Setup
    @classmethod
    def setUpClass(cls):
        """Set test"""
        cls.a = pd.DataFrame({
            ('Seq','Seq')     :  [  'A',  'Q',  'A',  'N',  'P',  'V',  'V',  'A',  'I',  'Q',  'E',  'A',  'Y',  'L',  'L',  'N',  'D'],
            ('N', 'N')        :  [    1,   50,  201,  247,  258,  270,  270,  274,  311,  325,  327,  343,  368,  372,  372,  376,  432],
            ('C', 'C')        :  [   42,   62,  211,  263,  269,  283,  290,  293,  324,  342,  342,  351,  377,  385,  387,  387,  441],
            ('Nn', 'Nn')      :  [   NA,   NA,  187,  233,  244,  256,  256,  260,  297,  311,  313,  329,   NA,   NA,   NA,   NA,   NA],
            ('Cn', 'Cn')      :  [   NA,   48,  197,  249,  255,  269,  276,  279,  310,  328,  328,   NA,   NA,   NA,   NA,   NA,   NA],
            ('Exp1', 'P')     :  [0.001,0.904,0.001,0.012,0.869,0.819,0.504,0.919,0.380,0.915,0.713,0.104,0.012,0.904,0.001,0.190,0.808],
            ('Exp2', 'P')     :  [0.963,0.001,0.001,0.001,0.001,0.112,0.058,0.060,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.472],
            ('Exp3', 'P')     :  [0.732,0.335,0.605,0.164,0.650,0.230,0.034,0.655,0.002,0.008,0.243,0.307,0.240,0.666,0.663,0.189,0.001],
        })
        exp1 = cMethod.LabelDetail(
            coord  = [(1,  42), (201, 211), (247, 263), (368, 387)],
            coordN = [(NA, NA), (187, 197), (233, 249), ( NA,  NA)],
            seq    = [     'A',        'A',        'N', 'Y\n    L'],
            seqL   = [   ['A'],      ['A'],      ['N'], ['Y', 'L']],
            np     = [       1,          1,         1,           2],
            npNat  = [       0,          1,         1,           0],
            nc     = [       1,          2,         2,           4],
            ncNat  = [       0,          2,         2,           0],
            nFrag  = (9, 4),
            nCT    = (4, 2),
        )
        exp2 = cMethod.LabelDetail(
            coord  = [(50, 62), (201, 211),        (247, 269), (311, 324), (325, 342), (343, 351),                   (368, 387)],
            coordN = [(NA, 48), (187, 197),        (233, 255), (297, 310), (311, 328), (329,  NA),                   (NA,   NA)],
            seq    = [     'Q',        'A', 'N\n           P',        'I',   'Q\n  E',        'A', 'Y\n    L\n    L\n        N'],
            seqL   = [   ['Q'],      ['A'],        ['N', 'P'],      ['I'], ['Q', 'E'],      ['A'],         ['Y', 'L', 'L', 'N']],
            np     = [       1,          1,                 2,          1,          2,          1,                            4],
            npNat  = [       1,          1,                 2,          1,          2,          1,                            0],
            nc     = [       2,          2,                 4,          2,          3,          2,                            6],
            ncNat  = [       1,          2,                 4,          2,          3,          1,                            0],
            nFrag  = (19, 11),
            nCT    = (7, 6),
        )
        exp3 = cMethod.LabelDetail(
            coord  = [(270, 290), (311, 324), (325, 342), (432, 441)],
            coordN = [(256, 276), (297, 310), (311, 328), ( NA,  NA)],
            seq    = [        'V',       'I',        'Q',        'D'],
            seqL   = [      ['V'],     ['I'],      ['Q'],      ['D']],
            np     = [1, 1, 1, 1],
            npNat  = [1, 1, 1, 0],
            nc     = [2, 2, 2, 1],
            ncNat  = [2, 2, 2, 0],
            nFrag  = (6, 5),
            nCT    = (4,3),
        )
        cls.b = cMethod.Fragment(
            label = ['Exp1-P', 'Exp2-P', 'Exp3-P'],
        )
        setattr(cls.b, 'Exp1-P', exp1)
        setattr(cls.b, 'Exp2-P', exp2)
        setattr(cls.b, 'Exp3-P', exp3)
    #---
    #endregion --------------------------------------------------> Class Setup

    #region -------------------------------------------------> Expected Output
    def test_expected_output(self):
        """Test for expected output"""
        #------------------------------>
        tInput = [
            (self.a, 0.05, 'le', 441, (55, 350), self.b),
        ]
        #------------------------------>
        for a,b,c,d,e,f in tInput:
            with self.subTest(
                f'df={a}, val={b}, comp={c}, protL={d}, protLoc={e}'):
                #------------------------------>
                result = cMethod.Fragments(a, b, c, d, e)
                #------------------------------>
                self.assertEqual(result, f)
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_Rec2NatCoord(unittest.TestCase):
    """Test for core.method.Rec2NatCoord"""
    #region -----------------------------------------------------> Class Setup
    @classmethod
    def setUpClass(cls):
        """Set test"""
        cls.a = [(1,42), (38, 50), (201, 211), (247, 263)]
        cls.b = [(48, 60), (211, 221), (257, 273)]
        cls.c = [(211, 221)]
    #---
    #endregion --------------------------------------------------> Class Setup

    #region -------------------------------------------------> Expected Output
    def test_expected_output(self):
        """Test for expected output"""
        #------------------------------>
        tInput = [
            (self.a,  (10, 300), 10, self.b),
            (self.a, (100, 230), 10, self.c),
            (self.a, (100, 230), None, ['NA']),
        ]
        #------------------------------>
        for a,b,c,d in tInput:
            with self.subTest(f'coord={a}, protLoc={b}, delta={c}'):
                #------------------------------>
                result = cMethod.Rec2NatCoord(a, b, c)
                #------------------------------>
                self.assertEqual(result, d)
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_MergeOverlappingFragments(unittest.TestCase):
    """Test for core.method.MergeOverlappingFragments"""
    #region -----------------------------------------------------> Class Setup
    @classmethod
    def setUpClass(cls):
        """Set test"""
        cls.a = [(1,42), (201, 211), (247, 263), (38, 50), (212, 230)]
        cls.b = [(1,50), (201, 211), (212, 230), (247, 263)]
        cls.c = [(1,50), (201, 230), (247, 263)]
    #---
    #endregion --------------------------------------------------> Class Setup

    #region -------------------------------------------------> Expected Output
    def test_expected_output(self):
        """Test for expected output"""
        #------------------------------>
        tInput = [
            (self.a, 0, self.b),
            (self.a, 1, self.c),
            (self.a, 5, self.c),
        ]
        #------------------------------>
        for a,b,c,in tInput:
            with self.subTest(f'coord={a}, delta={b}'):
                #------------------------------>
                result = cMethod.MergeOverlappingFragments(a, b)
                #------------------------------>
                self.assertEqual(result, c)
    #---
    #endregion ----------------------------------------------> Expected Output
#---
#endregion -----------------------------------------------------------> Others
