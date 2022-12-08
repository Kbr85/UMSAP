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


"""Tests for data.method """


#region -------------------------------------------------------------> Imports
import unittest
from pathlib import Path

import pandas as pd
from numpy  import nan
from pandas import NA

import config.config  as mConfig
import data.method    as mMethod
import data.exception as mException
import data.file      as mFile
#endregion ----------------------------------------------------------> Imports


# Test data lead to long lines, so this check will be disabled for this module
# pylint: disable=line-too-long


#region ---------------------------------------------------------------> Files
folder      = Path(__file__).parent / 'test_files'
#------------------------------> Input Files
tarprotData  = folder / 'tarprot-data-file.txt'  # For TarProt and CorrA
protprofData = folder / 'protprof-data-file.txt' # For ProtProf
#------------------------------> Result Files
#-------------->
corrA_1 = folder / 'res-corrA-1.txt'
corrA_2 = folder / 'res-corrA-2.txt'
corrA_3 = folder / 'res-corrA-3.txt'
corrA_4 = folder / 'res-corrA-4.txt'
#-------------->
protprof_1 = folder / 'res-protprof-1.txt'
#endregion ------------------------------------------------------------> Files


#region -------------------------------------------------------> pd.DataFrames
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


DF_DFFilterByColN = pd.DataFrame({
    'A' : [1,2,3,4,5],
    'B' : [1,2,3,4,5],
})


DF_DFFilterByColS = pd.DataFrame({
    'A' : [1,2,3,4,5],
    'B' : ['1','2','1','2','1'],
})
#endregion ----------------------------------------------------> pd.DataFrames


#region ---------------------------------------------------------> Class Setup
class Test_Str2ListNumber(unittest.TestCase):
    """Test for data.method.Str2ListNumber"""
    #region -----------------------------------------------------> Class Setup
    @classmethod
    def setUp(cls):                                                             # pylint: disable=arguments-differ
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
            ('50-10, 4, 7',     'int', ',', False, mException.InputError),
            ('1,2,3,4-',        'int', ',', False, mException.InputError),
        ]
        #------------------------------>
        for a,b,c,d, e in badInput:
            msg = f"tStr={a}, numType={b}, sep={c}, unique={d}"
            with self.subTest(msg):
                self.assertRaises(
                    e,
                    mMethod.Str2ListNumber,
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
                result = mMethod.Str2ListNumber(a, numType=b, sep=c, unique=d)
                #------------------------------>
                self.assertEqual(result, e)
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_StrEqualLength(unittest.TestCase):
    """Test for data.method.StrEqualLength"""
    #region -----------------------------------------------------> Valid Input
    def test_invalid_input(self):
        """Test for invalid input"""
        #------------------------------>
        badInput = [
            (['1, 2, 4b'], ' ', 'Bad Input', mException.InputError),
        ]
        #------------------------------>
        for a,b,c,d in badInput:
            msg = f"tStr={a}, char={b}, loc={c}"
            with self.subTest(msg):
                self.assertRaises(
                    d,
                    mMethod.StrEqualLength,
                    a, char=b, loc=c
                )
    #---
    #endregion --------------------------------------------------> Valid Input

    #region -------------------------------------------------> Expected Output
    def test_expected_output(self):
        """Test for expected output"""
        #------------------------------>
        tInput = [
            (['A', 'AA', 'AAA'], ' ', 'end', ['A  ', 'AA ', 'AAA']),
            (['A', 'AA', 'AAA'], ' ', 'start', ['  A', ' AA', 'AAA']),
        ]
        #------------------------------>
        for a,b,c,d in tInput:
            with self.subTest(f"strL={a}, char={b}, loc={c}"):
                #------------------------------>
                result = mMethod.StrEqualLength(a, char=b,loc=c)
                #------------------------------>
                self.assertEqual(result, d)
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_ResControl2ListNumber(unittest.TestCase):
    """Test for data.method.ResControl2ListNumber"""
    #region -------------------------------------------------> Expected Output
    def test_expected_output(self):
        """Test for expected output"""
        #------------------------------>
        tInput = [
            (',;,', [' ', ',', ';'], 'int', [[[], []], [[], []]]),
            ('0 1 2, 3 4 5; 6 7 8, 9 10 11', [' ', ',', ';'], 'int', [[[0,1,2], [3,4,5]], [[6,7,8], [9,10,11]]]),
            ('0 1 2,; 6 7 8,', [' ', ',', ';'], 'int', [[[0,1,2], []], [[6,7,8], []]]),
            ('0-2, 3-5; 6-8, 9-11', [' ', ',', ';'], 'int', [[[0,1,2], [3,4,5]], [[6,7,8], [9,10,11]]]),
            ('0-2, 3 4 5; 6-8, 9-11', [' ', ',', ';'], 'int', [[[0,1,2], [3,4,5]], [[6,7,8], [9,10,11]]]),
            ('0-2 20, 3 4 5 21; 6-8 22, 23 9-11', [' ', ',', ';'], 'int', [[[0,1,2,20], [3,4,5, 21]], [[6,7,8, 22], [23,9,10,11]]]),
        ]
        #------------------------------>
        for a,b,c,d in tInput:
            with self.subTest(f"val={a}, sep={b}, numType={c}"):
                #------------------------------>
                result = mMethod.ResControl2ListNumber(a, sep=b, numType=c)
                #------------------------------>
                self.assertEqual(result, d)
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_ResControl2Flat(unittest.TestCase):
    """Test for data.method.ResControl2Flat"""
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
                result = mMethod.ResControl2Flat(a)
                #------------------------------>
                self.assertEqual(result, b)
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_ResControl2DF(unittest.TestCase):
    """Test for data.method.ResControl2DF"""
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
                result = mMethod.ResControl2DF(a, b)
                #------------------------------>
                self.assertEqual(result, c)
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_ExpandRange(unittest.TestCase):
    """Test for data.method.ExpandRange"""
    #region -----------------------------------------------------> Valid Input
    def test_invalid_input(self):
        """Test for invalid input"""
        #------------------------------>
        badInput = [
            ('4-',  'int', mException.InputError),
            ('4-1', 'int', mException.InputError),
        ]
        #------------------------------>
        for a,b,c in badInput:
            msg = f"r={a}, numType={b}"
            with self.subTest(msg):
                self.assertRaises(
                    c,
                    mMethod.ExpandRange,
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
                result = mMethod.ExpandRange(a, numType=b)
                #------------------------------>
                self.assertEqual(result, c)
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_DictVal2Str(unittest.TestCase):
    """Test for data.method.DictVal2Str"""
    #region -----------------------------------------------------> Class Setup
    @classmethod
    def setUp(cls):                                                             # pylint: disable=arguments-differ
        """Set test"""
        cls.iDict = {
            1    : Path('/k/d/c'),
            'B'  : 3,
            '2'  : [1,2,3,4,5],
            'All': 'This is already a str',
        }

        cls.allDict = {
            1    : str(Path('/k/d/c')),
            'B'  : str(3),
            '2'  : str([1,2,3,4,5]),
            'All': str('This is already a str'),
        }

        cls.pathDict = {
            1    : str(Path('/k/d/c')),
            'B'  : 3,
            '2'  : [1,2,3,4,5],
            'All': 'This is already a str',
        }
    #---
    #endregion --------------------------------------------------> Class Setup

    #region -------------------------------------------------> Expected Output
    def test_expected_output(self):
        """Test for the expected output"""
        #------------------------------>
        tInput = [
            (self.iDict,                [], True, self.iDict),
            (self.iDict,               [1], True, self.pathDict),
            (self.iDict, [1,'B','2','All'], True, self.allDict),
        ]
        #------------------------------>
        for a,b,c,d in tInput:
            with self.subTest(f"iDict={a}, changeKey={b}, new={c}"):
                #------------------------------>
                result = mMethod.DictVal2Str(a, changeKey=b, new=c)
                #------------------------------>
                self.assertEqual(result, d)
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_DFReplace(unittest.TestCase):
    """Test for data.method.DFReplace"""
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
                result = mMethod.DFReplace(a, b, c, sel=d)
                #------------------------------>
                # pylint: disable=protected-access
                pd._testing.assert_frame_equal(result, e)                       # type: ignore
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_DFExclude(unittest.TestCase):
    """Test for data.method.DFExclude"""
    #region -----------------------------------------------------> Class Setup
    @classmethod
    def setUp(cls):                                                             # pylint: disable=arguments-differ
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
                result = mMethod.DFExclude(a,b)
                #------------------------------>
                # pylint: disable=protected-access
                pd._testing.assert_frame_equal(result, c)                       # type: ignore
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_DFFilterByColN(unittest.TestCase):
    """Test for data.method.DFFilterByColN"""
    #region -----------------------------------------------------> Class Setup
    @classmethod
    def setUp(cls):                                                             # pylint: disable=arguments-differ
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
                result = mMethod.DFFilterByColN(a, b, c, d)
                #------------------------------>
                # pylint: disable=protected-access
                pd._testing.assert_frame_equal(result, e)                       # type: ignore
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_DFFilterByColS(unittest.TestCase):
    """Test for data.method.DFFilterByColS"""
    #region -----------------------------------------------------> Class Setup
    @classmethod
    def setUp(cls):                                                             # pylint: disable=arguments-differ
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
            (DF_DFFilterByColS, 1,   '2',  'e', self.a),
            (DF_DFFilterByColS, 1,   '2', 'ne', self.b),
        ]
        #------------------------------>
        for a,b,c,d,e in tInput:
            with self.subTest(f'df={a}, col={b}, refVal={c}, comp={d}'):
                #------------------------------>
                result = mMethod.DFFilterByColS(a, b, c, d)
                #------------------------------>
                # pylint: disable=protected-access
                pd._testing.assert_frame_equal(result, e)                       # type: ignore
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_LoadUserConfig(unittest.TestCase):
    """Test for data.method.LoadUserConfig"""
    #region -----------------------------------------------------> Class Setup
    @classmethod
    def setUp(cls):                                                             # pylint: disable=arguments-differ
        """Set test"""
        #------------------------------> File Path
        cls.okFile = Path('/Users/bravo/Dropbox/SOFTWARE-DEVELOPMENT/APPS/UMSAP/GIT/CODE/test/unit/test_files/umsap_conf.json')
        cls.badFile = Path('/Users/bravo/Dropbox/SOFTWARE-DEVELOPMENT/APPS/UMSAP/GIT/CODE/test/unit/test_files/umsap_confBAD.json')
        cls.noFile = Path('/Users/bravo/Dropbox/SOFTWARE-DEVELOPMENT/APPS/UMSAP/GIT/CODE/test/unit/test_files/umsap_confNOFILE.json')
        #------------------------------> Dict In
        cls.genDict = {
            "checkUpdate": True,
            "DPI": 100,
            "MatPlotMargin": 0.025
        }
        #------------------------------> Dict Out
        cls.genDictOutOk = {
            'confUserFile'         : True,
            'confUserFileException': None,
            'confUserWrongOptions' : [],
            'confGeneral'          : {
                "checkUpdate"  : False,
                "DPI"          : 100,
                "MatPlotMargin": 0.025
            },
        }
        cls.genDictOutBad = {
            'confUserFile'         : True,
            'confUserFileException': None,
            'confUserWrongOptions' : [],
            'confGeneral'          : {
                "checkUpdate"  : True,
                "DPI"          : 100,
                "MatPlotMargin": 0.025
            },
        }
        cls.genDictOutNoFile = {
            'confUserFile'         : True,
            'confUserFileException': None,
            'confUserWrongOptions' : [],
            'confGeneral'          : {
                "checkUpdate"  : True,
                "DPI"          : 100,
                "MatPlotMargin": 0.025
            },
        }
    #---
    #endregion --------------------------------------------------> Class Setup

    #region -------------------------------------------------> Expected Output
    def test_expected_output(self):
        """Test for expected output"""
        #------------------------------>
        tInput = [
            (self.okFile,  self.genDict, self.genDictOutOk),
            (self.badFile, self.genDict, self.genDictOutBad),
            (self.noFile,  self.genDict, self.genDictOutNoFile),
        ]
        #------------------------------>
        for a,b,c in tInput:
            with self.subTest(f'fileP={a}, confGen={b}'):
                #------------------------------>
                result = mMethod.LoadUserConfig(a, b)
                #------------------------------>
                self.assertEqual(result, c)
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_Fragments(unittest.TestCase):
    """Test for data.method.Fragments"""
    #region -----------------------------------------------------> Class Setup
    @classmethod
    def setUp(cls):                                                             # pylint: disable=arguments-differ
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
        cls.b = {
            str(('Exp1', 'P')): {
                'Coord' : [(1,  42), (201, 211), (247, 263), (368, 387)],
                'CoordN': [(NA, NA), (187, 197), (233, 249), ( NA,  NA)],
                'Seq'   : [     'A',        'A',        'N', 'Y\n    L'],
                'SeqL'  : [   ['A'],      ['A'],      ['N'], ['Y', 'L']],
                'Np'    : [       1,          1,         1,           2],
                'NpNat' : [       0,          1,         1,           0],
                'Nc'    : [       1,          2,         2,           4],
                'NcNat' : [       0,          2,         2,           0],
                'NcT'   : [       9,          4],
                'NFrag' : [       4,          2],
            },
            str(('Exp2', 'P')): {
                'Coord' : [(50, 62), (201, 211),        (247, 269), (311, 324), (325, 342), (343, 351),                   (368, 387)],
                'CoordN': [(NA, 48), (187, 197),        (233, 255), (297, 310), (311, 328), (329,  NA),                   (NA,   NA)],
                'Seq'   : [     'Q',        'A', 'N\n           P',        'I',   'Q\n  E',        'A', 'Y\n    L\n    L\n        N'],
                'SeqL'  : [   ['Q'],      ['A'],        ['N', 'P'],      ['I'], ['Q', 'E'],      ['A'],         ['Y', 'L', 'L', 'N']],
                'Np'    : [       1,          1,                 2,          1,          2,          1,                            4],
                'NpNat' : [       1,          1,                 2,          1,          2,          1,                            0],
                'Nc'    : [       2,          2,                 4,          2,          3,          2,                            6],
                'NcNat' : [       1,          2,                 4,          2,          3,          1,                            0],
                'NcT'   : [19, 11],
                'NFrag' : [7, 6],
            },
            str(('Exp3', 'P')): {
                'Coord' : [(270, 290), (311, 324), (325, 342), (432, 441)],
                'CoordN': [(256, 276), (297, 310), (311, 328), ( NA,  NA)],
                'Seq'   : [        'V',       'I',        'Q',        'D'],
                'SeqL'  : [      ['V'],     ['I'],      ['Q'],      ['D']],
                'Np'    : [1, 1, 1, 1],
                'NpNat' : [1, 1, 1, 0],
                'Nc'    : [2, 2, 2, 1],
                'NcNat' : [2, 2, 2, 0],
                'NcT'   : [6, 5],
                'NFrag' : [4,3],
            }
        }
    #---
    #endregion --------------------------------------------------> Class Setup

    #region -------------------------------------------------> Expected Output
    def test_expected_output(self):
        """Test for expected output"""
        #------------------------------>
        tInput = [
            (self.a, 0.05, 'le', 441, [55, 350], self.b),
        ]
        #------------------------------>
        for a,b,c,d,e,f in tInput:
            with self.subTest(
                f'df={a}, val={b}, comp={c}, protL={d}, protLoc={e}'):
                #------------------------------>
                result = mMethod.Fragments(a, b, c, d, e)
                #------------------------------>
                self.assertEqual(result, f)
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_MergeOverlappingFragments(unittest.TestCase):
    """Test for data.method.MergeOverlappingFragments"""
    #region -----------------------------------------------------> Class Setup
    @classmethod
    def setUp(cls):                                                             # pylint: disable=arguments-differ
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
                result = mMethod.MergeOverlappingFragments(a, b)
                #------------------------------>
                self.assertEqual(result, c)
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_CorrA(unittest.TestCase):
    """Test for data.method.CorrA"""
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
        cls.dict2 = {
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
        cls.dict3 = {
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
        cls.dict4 = {
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
                result = mMethod.CorrA(
                    a, b, resetIndex=c)[0]['dfR']
                result = result.round(3)
                #------------------------------>
                dfF = pd.read_csv(d, sep='\t',index_col=0).round(3)
                #------------------------------>
                # pylint: disable=protected-access
                pd._testing.assert_frame_equal(result, dfF)                     # type: ignore
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_ProtProf(unittest.TestCase):
    """Test for data.method.ProtProf"""
    #region -----------------------------------------------------> Class Setup
    @classmethod
    def setUp(cls):                                                             # pylint: disable=arguments-differ
        """Set test"""
        cls.df = mFile.ReadCSV2DF(protprofData)
        cls.dExtra  = {
            'cLDFThreeCol'  : mConfig.dfcolProtprofFirstThree,
            'cLDFThirdLevel': mConfig.dfcolProtprofCLevel,
        }
        cls.dict1 = {
            'ScoreVal': 320.0,
            'RawI': True,
            'IndS': True,
            'Cero': True,
            'NormMethod': 'Median',
            'TransMethod': 'Log2',
            'ImpMethod': 'None',
            'Shift': 1.8,
            'Width': 0.3,
            'Alpha': 0.05,
            'CorrectP': 'Benjamini - Hochberg',
            'Cond': ['C1', 'C2'],
            'RP': ['RP1', 'RP2'],
            'ControlT': 'One Control',
            'ControlL': ['1Control'],
            'oc': {
                'DetectedP': 0,
                'GeneName': 6,
                'ScoreCol': 39,
                'ExcludeP': [171, 172, 173],
                'ResCtrl': [[[105, 115, 125]], [[106, 116, 126], [101, 111, 121]], [[108, 118, 128], [103, 113, 123]]],
                'ColumnF': [39, 105, 115, 125, 106, 116, 126, 101, 111, 121, 108, 118, 128, 103, 113, 123],
                'Column': [6, 0, 39, 171, 172, 173, 105, 115, 125, 106, 116, 126, 101, 111, 121, 108, 118, 128, 103, 113, 123],
            },
            'df' : {
                'DetectedP': 0,
                'GeneName': 1,
                'ScoreCol': 2,
                'ExcludeP': [3, 4, 5],
                'ResCtrl': [[[6, 7, 8]], [[9, 10, 11], [12, 13, 14]], [[15, 16, 17], [18, 19, 20]]],
                'ResCtrlFlat': [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
                'ColumnR': [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
                'ColumnF': [2, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
            },
        }
    #---
    #endregion --------------------------------------------------> Class Setup

    #region -------------------------------------------------> Expected Output
    # def test_output(self):
    #     """Test method output"""
    #     #------------------------------>
    #     tInput = [
    #         (self.df, self.dict1, self.dExtra, True, protprof_1),
    #     ]
    #     #------------------------------>
    #     for a,b,c,d,e in tInput:
    #         with self.subTest(f"df={a}, rDO={b}, dExtra={c}, resetIndex={d}"):
    #             #------------------------------>
    #             result = mMethod.ProtProf(
    #                 a, b, c, resetIndex=d)[0]['dfR']
    #             result = result.round(3)
    #             #------------------------------>
    #             dfF = pd.read_csv(e, sep='\t', header=[0,1,2]).round(3)
    #             #------------------------------>
    #             # pylint: disable=protected-access
    #             pd._testing.assert_frame_equal(result, dfF)                     # type: ignore
    # #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_Rec2NatCoord(unittest.TestCase):
    """Test for data.method.Rec2NatCoord"""
    #region -----------------------------------------------------> Class Setup
    @classmethod
    def setUp(cls):                                                             # pylint: disable=arguments-differ
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
                result = mMethod.Rec2NatCoord(a, b, c)
                #------------------------------>
                self.assertEqual(result, d)
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_R2AA(unittest.TestCase):
    """Test for data.method.R2AA

        Notes
        -----
        Last row with the chi2 results is not tested here.
    """
    #region -----------------------------------------------------> Class Setup
    @classmethod
    def setUp(cls):                                                             # pylint: disable=arguments-differ
        """Set test"""
        cls.a = pd.DataFrame({
            ('Seq','Seq') : ['TVAQA', 'MLVAF', 'TITLS', 'LRDII', 'WVTAD', 'PDYAS', 'HDLEK', 'MKHHH', 'HHHLM'],
            ('Exp1', 'P') : [  0.001,   0.904,   0.001,   0.012,   0.869,   0.001,   0.504,   0.176,   0.010],
            ('Exp2', 'P') : [  0.963,   0.001,   0.001,   0.001,   0.001,   0.112,   0.058,   0.001,   0.690],
            ('Exp3', 'P') : [  0.732,   0.001,   0.605,   0.164,   0.650,   0.230,   0.001,   0.001,   0.001],
        })
        cls.seq = (
            'MKHHHHHHHHHHHHMKKTAIAIAVALAGFATVAQAASWSHPQFEKIEGRRDRGQKTQSAP'
            'GTLSPDARNEKQPFYGEHQAGILTPQQAAMMLVAFDVLASDKADLERLFRLLTQRFAFLT'
            'QGGAAPETPNPRLPPLDSGILGGYIAPDNLTITLSVGHSLFDERFGLAPQMPKKLQKMTR'
            'FPNDSLDAALCHGDVLLQICANTQDTVIHALRDIIKHTPDLLSVRWKREGFISDHAARSK'
            'GKETPINLLGFKDGTANPDSQNDKLMQKVVWVTADQQEPAWTIGGSYQAVRLIQFRVEFW'
            'DRTPLKEQQTIFGRDKQTGAPLGMQHEHDVPDYASDPEGKVIALDSHIRLANPRTAESES'
            'SLMLRRGYSYSLGVTNSGQLDMGLLFVCYQHDLEKGFLTVQKRLNGEALEEYVKPIGGGY'
            'FFALPGVKDANDYFGSALLRVMMMMMMMHHHHHHHHHLM')
        cls.b = pd.DataFrame(
            {
                ('AA', 'AA')    : ['A','I','L','V','M','F','W','Y','R','K','D','E','C','Q','H','S','T','N','G','P'],
                ('Exp1', 'P2')  : [  1,  1,  1,  0,  0,  1,  0,  0,  0,  0,  1,  0,  0,  1,  2,  0,  0,  1,  0, 0,],
                ('Exp1', 'P1')  : [  3,  1,  1,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  2,  0,  0,  0, 0,],
                ('Exp1', "P1'") : [  1,  0,  1,  1,  0,  0,  0,  0,  0,  1,  1,  0,  0,  0,  1,  0,  2,  0,  0, 1,],
                ('Exp1', "P2'") : [  0,  1,  0,  1,  0,  0,  0,  0,  1,  0,  1,  0,  0,  0,  2,  1,  0,  0,  1, 1,],
                ('Exp2', 'P2')  : [  3,  1,  1,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  2,  0,  0,  1,  0, 0,],
                ('Exp2', 'P1')  : [  1,  1,  1,  1,  1,  1,  0,  0,  0,  0,  1,  0,  0,  0,  1,  1,  0,  0,  0, 0,],
                ('Exp2', "P1'") : [  0,  0,  1,  1,  1,  0,  1,  0,  0,  1,  1,  0,  0,  1,  1,  0,  1,  0,  0, 0,],
                ('Exp2', "P2'") : [  0,  1,  1,  2,  0,  0,  0,  0,  1,  0,  0,  0,  0,  1,  2,  0,  0,  0,  1, 0,],
                ('Exp3', 'P2')  : [  2,  0,  0,  0,  0,  0,  0,  1,  0,  0,  0,  1,  0,  0,  2,  0,  0,  0,  0, 0,],
                ('Exp3', 'P1')  : [  0,  0,  0,  0,  1,  1,  0,  0,  0,  1,  0,  0,  0,  1,  2,  0,  0,  0,  0, 0,],
                ('Exp3', "P1'") : [  0,  0,  0,  0,  1,  0,  0,  0,  0,  0,  1,  0,  0,  0,  3,  0,  0,  0,  1, 0,],
                ('Exp3', "P2'") : [  0,  0,  1,  1,  0,  1,  0,  0,  0,  0,  1,  0,  0,  0,  2,  0,  0,  0,  0, 0,],
                ('ALL_CLEAVAGES_UMSAP', 'P2')  : [41, 19, 46, 21, 17, 20,  5, 10, 24, 24, 29, 20,  3, 27, 31, 23, 24, 12, 35, 25],
                ('ALL_CLEAVAGES_UMSAP', 'P1')  : [41, 19, 46, 21, 17, 20,  5, 10, 24, 24, 29, 20,  3, 27, 32, 23, 24, 12, 35, 25],
                ('ALL_CLEAVAGES_UMSAP', "P1'") : [41, 19, 47, 21, 16, 20,  5, 10, 24, 24, 29, 20,  3, 27, 32, 23, 24, 12, 35, 25],
                ('ALL_CLEAVAGES_UMSAP', "P2'") : [41, 19, 47, 21, 17, 20,  5, 10, 24, 23, 29, 20,  3, 27, 32, 23, 24, 12, 35, 25],
            },
            index=['A','I','L','V','M','F','W','Y','R','K','D','E','C','Q','H','S','T','N','G','P']
        )
    #---
    #endregion --------------------------------------------------> Class Setup

    #region -------------------------------------------------> Expected Output
    def test_expected_output(self):
        """Test for expected output"""
        #------------------------------>
        tInput = [
            (self.a, self.seq, 0.05, len(self.seq), 2, self.b),
        ]
        #------------------------------>
        for a,b,c,d,e,f in tInput:
            with self.subTest(
                f'df={a}, seq={b}, alpha={c}, protL={d}, pos={e}'):
                #------------------------------>
                result = mMethod.R2AA(a, b, c, d, e)
                result = result.iloc[0:-1,:] # Exclude chi2 test row
                #------------------------------>
                # pylint: disable=protected-access
                pd._testing.assert_frame_equal(result, f)                       # type: ignore
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_R2Hist(unittest.TestCase):
    """Test for data.method.R2Hist"""
    #region -----------------------------------------------------> Class Setup
    @classmethod
    def setUp(cls):                                                             # pylint: disable=arguments-differ
        """Set test"""
        cls.a = pd.DataFrame({
            ('Nterm',   'Nterm') : [    1,   50,  201,  247,  258,  270,  270,  274,  311,  325,  327,  343,  368,  372,  372,  376,  432],
            ('Cterm',   'Cterm') : [   42,   62,  211,  263,  269,  283,  290,  293,  324,  342,  342,  351,  377,  385,  387,  387,  441],
            ('NtermF', 'NtermF') : [   NA,   NA,  187,  233,  244,  256,  256,  260,  297,  311,  313,  329,   NA,   NA,   NA,   NA,   NA],
            ('CtermF', 'CtermF') : [   NA,   48,  197,  249,  255,  269,  276,  279,  310,  328,  328,   NA,   NA,   NA,   NA,   NA,   NA],
            ('Exp1',        'P') : [0.001,0.904,0.001,0.012,0.869,0.819,0.504,0.919,0.380,0.915,0.713,0.104,0.012,0.904,0.001,0.190,0.808],
            ('Exp2',        'P') : [0.963,0.001,0.001,0.001,0.001,0.112,0.058,0.060,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.472],
            ('Exp3',        'P') : [0.732,0.335,0.605,0.164,0.650,0.230,0.034,0.655,0.002,0.008,0.243,0.307,0.240,0.666,0.663,0.189,0.001],
        })

        cls.b = pd.DataFrame({
            ('Rec',    'Win',  'Win') : [0.0, 50.0, 100.0, 150.0, 200.0, 250.0, 300.0, 350.0, 400.0, 450.0],
            ('Rec',    'All', 'Exp1') : [1.0,    0,     0,     0,   3.0,   1.0,     0,   4.0,     0,   nan],
            ('Rec',    'All', 'Exp2') : [1.0,  1.0,     0,     0,   3.0,   3.0,   7.0,   9.0,     0,   nan],
            ('Rec',    'All', 'Exp3') : [  0,    0,     0,     0,     0,   2.0,   4.0,     0,   1.0,   nan],
            ('Rec', 'Unique', 'Exp1') : [1.0,    0,     0,     0,   3.0,   1.0,     0,   4.0,     0,   nan],
            ('Rec', 'Unique', 'Exp2') : [1.0,  1.0,     0,     0,   3.0,   3.0,   4.0,   7.0,     0,   nan],
            ('Rec', 'Unique', 'Exp3') : [  0,    0,     0,     0,     0,   2.0,   3.0,     0,   1.0,   nan],
            ('Nat',    'Win',  'Win') : [0.0, 50.0, 100.0, 150.0, 200.0, 250.0, 300.0, 350.0, 400.0, 450.0],
            ('Nat',    'All', 'Exp1') : [  0,    0,     0,   2.0,   2.0,     0,     0,     0,     0,   nan],
            ('Nat',    'All', 'Exp2') : [1.0,    0,     0,   2.0,   3.0,   2.0,   6.0,     0,     0,   nan],
            ('Nat',    'All', 'Exp3') : [  0,    0,     0,     0,     0,   3.0,   3.0,     0,     0,   nan],
            ('Nat', 'Unique', 'Exp1') : [  0,    0,     0,   2.0,   2.0,     0,     0,     0,     0,   nan],
            ('Nat', 'Unique', 'Exp2') : [1.0,    0,     0,   2.0,   3.0,   2.0,   3.0,     0,     0,   nan],
            ('Nat', 'Unique', 'Exp3') : [  0,    0,     0,     0,     0,   3.0,   2.0,     0,     0,   nan],
        })

        cls.c = pd.DataFrame({
            ('Rec',    'Win',  'Win') : [200.0, 250.0, 300.0],
            ('Rec',    'All', 'Exp1') : [  3.0,   1.0,   nan],
            ('Rec',    'All', 'Exp2') : [  3.0,   3.0,   nan],
            ('Rec',    'All', 'Exp3') : [    0,   2.0,   nan],
            ('Rec', 'Unique', 'Exp1') : [  3.0,   1.0,   nan],
            ('Rec', 'Unique', 'Exp2') : [  3.0,   3.0,   nan],
            ('Rec', 'Unique', 'Exp3') : [    0,   2.0,   nan],
            ('Nat',    'Win',  'Win') : [200.0, 250.0, 300.0],
            ('Nat',    'All', 'Exp1') : [  2.0,     0,   nan],
            ('Nat',    'All', 'Exp2') : [  3.0,   2.0,   nan],
            ('Nat',    'All', 'Exp3') : [    0,   3.0,   nan],
            ('Nat', 'Unique', 'Exp1') : [  2.0,     0,   nan],
            ('Nat', 'Unique', 'Exp2') : [  3.0,   2.0,   nan],
            ('Nat', 'Unique', 'Exp3') : [    0,   3.0,   nan],
        })
    #---
    #endregion --------------------------------------------------> Class Setup

    #region -------------------------------------------------> Expected Output
    def test_expected_output(self):
        """Test for expected output"""
        #------------------------------>
        tInput = [
            (self.a, 0.05, [50], [441, 441], self.b),
            (self.a, 0.05, [200, 250, 300], [441, 441], self.c),
        ]
        #------------------------------>
        for a,b,c,d,e in tInput:
            with self.subTest(
                f'df={a}, alpha={b}, win={c}, maxL={d}'):
                #------------------------------>
                result = mMethod.R2Hist(a, b, c, d)
                #------------------------------>
                # pylint: disable=protected-access
                pd._testing.assert_frame_equal(result, e)                       # type: ignore
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_R2CpR(unittest.TestCase):
    """Test for data.method.R2CpR"""
    #region -----------------------------------------------------> Class Setup
    @classmethod
    def setUp(cls):                                                             # pylint: disable=arguments-differ
        """Set test"""
        cls.a = pd.DataFrame({
            ('Nterm',   'Nterm') : [    1,   5,  20,  24,  25,  27,  27,  27,  31,  32,  32,  34,  36,  37,  37,  37,  43],
            ('Cterm',   'Cterm') : [    4,   6,  21,  26,  26,  28,  29,  30,  32,  34,  35,  36,  38,  39,  40,  41,  45],
            ('NtermF', 'NtermF') : [   NA,   NA, 16,  20,  21,  23,  23,  23,  27,  28,  28,  30,  NA,  NA,  NA,  NA,  NA],
            ('CtermF', 'CtermF') : [   NA,    2, 17,  22,  22,  24,  25,  26,  28,  30,  31,  NA,  NA,  NA,  NA,  NA,  NA],
            ('Exp1',        'P') : [0.001,0.904,0.001,0.012,0.869,0.819,0.504,0.919,0.380,0.915,0.713,0.104,0.012,0.904,0.001,0.190,0.808],
            ('Exp2',        'P') : [0.963,0.001,0.001,0.001,0.001,0.112,0.058,0.060,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.472],
            ('Exp3',        'P') : [0.732,0.335,0.605,0.164,0.650,0.230,0.034,0.655,0.002,0.008,0.243,0.307,0.240,0.666,0.663,0.189,0.001],
        })

        cls.b = pd.DataFrame({
                            #  1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45
            ('Rec', 'Exp1') : [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0],
            ('Rec', 'Exp2') : [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 2, 0, 0, 0, 1, 2, 1, 1, 1, 2, 4, 0, 1, 1, 1, 1, 0, 0, 0, 0],
            ('Rec', 'Exp3') : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            ('Nat', 'Exp1') : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ('Nat', 'Exp2') : [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 2, 0, 0, 0, 1, 2, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ('Nat', 'Exp3') : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        })
    #---
    #endregion --------------------------------------------------> Class Setup

    #region -------------------------------------------------> Expected Output
    def test_expected_output(self):
        """Test for expected output"""
        #------------------------------>
        tInput = [
            (self.a, 0.05, [45, 45], self.b),
        ]
        #------------------------------>
        for a,b,c,d in tInput:
            with self.subTest(
                f'df={a}, alpha={b}, protL={c}'):
                #------------------------------>
                result = mMethod.R2CpR(a, b, c)
                #------------------------------>
                # pylint: disable=protected-access
                pd._testing.assert_frame_equal(result, d)                       # type: ignore
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_R2CEvol(unittest.TestCase):
    """Test for data.method.R2CEvol"""
    #region -----------------------------------------------------> Class Setup
    @classmethod
    def setUp(cls):                                                             # pylint: disable=arguments-differ
        """Set test"""
        cls.a = pd.DataFrame({
            ('Nterm',   'Nterm') : [        1,         5,        20,        24,        25,        27,        27,        27,        31,        32,        32,        34,        36,        37,        37,        37,        43],
            ('Cterm',   'Cterm') : [        4,         6,        21,        26,        26,        28,        29,        30,        32,        34,        35,        36,        38,        39,        40,        41,        45],
            ('NtermF', 'NtermF') : [       NA,        NA,        16,        20,        21,        23,        23,        23,        27,        28,        28,        30,        NA,        NA,        NA,        NA,        NA],
            ('CtermF', 'CtermF') : [       NA,         2,        17,        22,        22,        24,        25,        26,        28,        30,        31,        NA,        NA,        NA,        NA,        NA,        NA],
            ('Exp1',      'Int') : ['[1,2,3]', '[0,0,0]', '[1,2,3]', '[1,2,3]', '[0,0,0]', '[0,0,0]', '[0,0,0]', '[0,0,0]', '[7,8,9]', '[0,0,0]', '[0,0,0]', '[0,0,0]', '[2,4,5]', '[0,0,0]', '[7,8,9]', '[0,0,0]', '[0,0,0]'],
            ('Exp1',        'P') : [    0.001,     0.904,     0.001,     0.012,     0.869,     0.819,     0.504,     0.919,     0.001,     0.915,     0.713,     0.104,     0.012,     0.904,     0.001,     0.190,     0.808],
            ('Exp2',      'Int') : ['[0,0,0]', '[1,2,3]', '[3,4,5]', '[5,6,7]', '[7,8,9]', '[0,0,0]', '[0,0,0]', '[1,2,3]', '[3,4,5]', '[1,2,3]', '[4,5,6]', '[1,2,3]', '[2,4,5]', '[4,6,8]', '[7,8,9]', '[1,3,5]', '[0,0,0]'],
            ('Exp2',        'P') : [    0.963,     0.001,     0.001,     0.001,     0.001,     0.112,     0.058,     0.040,     0.001,     0.001,     0.001,     0.001,     0.001,     0.001,     0.001,     0.001,     0.472],
            ('Exp3',      'Int') : ['[0,0,0]', '[4,6,8]', '[7,8,9]', '[0,0,0]', '[0,0,0]', '[1,2,3]', '[3,4,5]', '[0,0,0]', '[1,2,3]', '[7,8,9]', '[0,0,0]', '[0,0,0]', '[2,4,5]', '[0,0,0]', '[0,0,0]', '[0,0,0]', '[3,4,5]'],
            ('Exp3',        'P') : [    0.732,     0.001,     0.001,     0.164,     0.650,     0.001,     0.034,     0.655,     0.002,     0.008,     0.243,     0.307,     0.010,     0.666,     0.663,     0.189,     0.001],
        })

        cls.b = pd.DataFrame({
                            #  1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25, 26,27, 28,29, 30,31,  32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47
            ('Rec', 'Exp1') : [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0,  1, 0,  0, 0,  1, 0,   1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            ('Rec', 'Exp2') : [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 4, 0, 7, 1, 0,  9, 0,  0, 0,1.4, 2, 0.4, 1, 1, 2, 4, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            ('Rec', 'Exp3') : [0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,10, 0,10, 0, 0, 0, 0,  2, 0,  1, 1,0.1,10, 0.1, 0,10, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            ('Nat', 'Exp1') : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0,  1, 0,  1, 0,  0, 0,   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ('Nat', 'Exp2') : [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 4, 0, 7, 1, 0, 9, 0, 0, 0,1.4, 2,0.4, 1,  1, 1,   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ('Nat', 'Exp3') : [0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,10, 0,10, 0, 0, 0, 0, 2, 0, 1, 1,0.1,10,0.1, 0, 10, 0,   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        })
    #---
    #endregion --------------------------------------------------> Class Setup

    #region -------------------------------------------------> Expected Output
    def test_expected_output(self):
        """Test for expected output"""
        #------------------------------>
        tInput = [
            (self.a, 0.05, [45, 47], self.b),
        ]
        #------------------------------>
        for a,b,c,d in tInput:
            with self.subTest(
                f'df={a}, alpha={b}, protL={c}'):
                #------------------------------>
                result = mMethod.R2CEvol(a, b, c)
                #------------------------------>
                # pylint: disable=protected-access
                pd._testing.assert_frame_equal(result, d)                       # type: ignore
    #---
    #endregion ----------------------------------------------> Expected Output
#---
#endregion ------------------------------------------------------> Class Setup


if __name__ == '__main__':
    unittest.main()
