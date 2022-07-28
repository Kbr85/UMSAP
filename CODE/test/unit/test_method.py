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

import data.method as mMethod
import data.exception as mException
#endregion ----------------------------------------------------------> Imports

#region ---------------------------------------------------------> Class Setup
class Test_Str2ListNumber(unittest.TestCase):
    """Test for data.method.Str2ListNumber"""
    #region -----------------------------------------------------> Class Setup
    @classmethod
    def setUp(cls):
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
            msg = f"tStr={a}, numType]{b}, sep={c}, unique={d}"
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


class Test_ListRemoveDuplicates(unittest.TestCase):
    """Test for data.method.ListRemoveDuplicates"""
    #region -------------------------------------------------> Expected Output
    def test_expected_output(self):
        """Test for the expected output"""
        #------------------------------> 
        tInput = [
            ([1,2,3,6,4,7,5,6,10,7,8,9], [1,2,3,6,4,7,5,10,8,9]),
            (['q', 'u', 'u', 'z', 'h', 'z'], ['q', 'u', 'z', 'h']),
            ([1, 2, 4, 'q', 'u', 'u', 'z', 6, 2], [1,2,4,'q','u','z',6]),
        ]
        #------------------------------> 
        for a,b in tInput:
            with self.subTest(f"l={a}"):
                #------------------------------> 
                result = mMethod.ListRemoveDuplicates(a)
                #------------------------------> 
                self.assertEqual(result, b) 
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_DictVal2Str(unittest.TestCase):
    """Test for data.method.DictVal2Str"""
    #region -----------------------------------------------------> Class Setup
    @classmethod
    def setUp(cls):
        """"""
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


class Test_ResControl2ListNumber(unittest.TestCase):
    """Test for data.method.ResControl2ListNumber"""
    #region -----------------------------------------------------> Valid Input
    #endregion --------------------------------------------------> Valid Input

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
                result = dmethod.ResControl2ListNumber(a, sep=b, numType=c)
                #------------------------------>
                self.assertEqual(result, d)
    #---
    #endregion ----------------------------------------------> Expected Output
#---

class Test_ResControl2Flat(unittest.TestCase):
    """Test for data.method.ResControl2Flat"""
    #region -----------------------------------------------------> Valid Input
    #endregion --------------------------------------------------> Valid Input

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
                result = dmethod.ResControl2Flat(a)
                #------------------------------>
                self.assertEqual(result, b)
    #---
    #endregion ----------------------------------------------> Expected Output
#---

class Test_ResControl2DF(unittest.TestCase):
    """Test for data.method.ResControl2DF"""
    #region -----------------------------------------------------> Valid Input
    #endregion --------------------------------------------------> Valid Input

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
                result = dmethod.ResControl2DF(a, b)
                #------------------------------>
                self.assertEqual(result, c)
    #---
    #endregion ----------------------------------------------> Expected Output
#---
#endregion ------------------------------------------------------> Class Setup


if __name__ == '__main__':
    unittest.main()
