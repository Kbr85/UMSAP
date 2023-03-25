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


"""Tests for core.check"""


#region -------------------------------------------------------------> Imports
import unittest
from pathlib import Path

from core import check as cCheck
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------> File Location
folder = Path(__file__).parent / 'file'
#endregion ----------------------------------------------------> File Location


#region ---------------------------------------------------------> Class Setup
class Test_VersionCompare(unittest.TestCase):
    """Test for core.check.VersionCompare"""
    #region -------------------------------------------------> Expected Output
    def test_expected_output(self):
        """Test for the first element of the expected output"""
        #------------------------------>
        tInput = [
            (   'badVersion',       '2.4.6', False),
            ('2.44.9 (beta)',  'badVersion', False),
            (       '2.4.7',        '2.4.7', False),
            (  '2.4.7 beta',        '2.4.7', False),
            (       '2.4.7', '2.4.7 (beta)', False),
            (       '2.4.7',        '2.4.9', False),
            (       '2.5.7',        '2.6.1', False),
            (       '3.4.7',        '5.4.1', False),
            (  '3.4.7 beta',        '5.4.1', False),
            (       '3.4.7', '5.4.1 (beta)', False),
            (       '2.4.7',        '2.4.1',  True),
            (       '2.5.7',        '2.4.1',  True),
            (       '3.4.7',        '2.4.1',  True),
            ('3.4.7 (beta)',        '2.4.1',  True),
            (       '3.4.7',   '2.4.1 beta',  True),
        ]
        #------------------------------>
        for a,b,c in tInput:
            with self.subTest(f"strA={a}, strB={b}"):
                #------------------------------>
                result = cCheck.VersionCompare(a, b)[0]
                #------------------------------>
                self.assertIs(result, c)
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_Path2FFOutput(unittest.TestCase):
    """Test for core.check.Path2FFOutput"""
    #region -----------------------------------------------------> Class Setup
    @classmethod
    def setUpClass(cls):
        """Set test"""
        cls.file   = Path(__file__)
        cls.folder = cls.file.parent
        cls.noPerm = Path('/etc/')
    #---
    #endregion --------------------------------------------------> Class Setup

    #region -------------------------------------------------> Expected Output
    def test_expected_output(self):
        """Test for the first element of the expected output"""
        #------------------------------>
        tInput = [
            (self.file,  'baInput',  True, False),                              # Bad Input
            ('',            'file',  True,  True),                              # Optional
            ('',            'file', False, False),                              #
            ('',          'folder',  True,  True),                              #
            ('',          'folder', False, False),                              #
            (list(),        'file', False, False),                              # Path() fails
            (self.file,     'file', False,  True),                              # File
            (self.folder, 'folder', False,  True),                              # Folder
            (self.noPerm, 'folder', False, False),                              # No Write Permission
        ]
        #------------------------------>
        for a,b,c,d in tInput:
            with self.subTest(f"value={a}, fof={b}, opt={c}"):
                #------------------------------>
                result = cCheck.Path2FFOutput(a, fof=b, opt=c)[0]
                #------------------------------>
                self.assertIs(result, d)
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_Path2FFInput(unittest.TestCase):
    """Test for core.check.Path2FFInput"""
    #region -----------------------------------------------------> Class Setup
    @classmethod
    def setUpClass(cls):
        """Set test"""
        cls.file   = Path(__file__)
        cls.folder = cls.file.parent
        cls.noPerm = Path('/etc/kbr-delete.delete')
    #---
    #endregion --------------------------------------------------> Class Setup

    #region -------------------------------------------------> Expected Output
    def test_expected_output(self):
        """Test for the first element of the expected output"""
        #------------------------------>
        tInput = [
            (self.file,  'baInput',  True, False),                              # Bad Input
            ('',            'file',  True,  True),                              # Optional
            ('',            'file', False, False),                              #
            ('',          'folder',  True,  True),                              #
            ('',          'folder', False, False),                              #
            (list(),        'file', False, False),                              # Path() fails
            (self.file,     'file', False,  True),                              # File
            (self.file,   'folder', False, False),                              #
            (self.folder, 'folder', False,  True),                              # Folder
            (self.folder,   'file', False, False),                              #
            (self.noPerm,   'file', False, False),                              # No Read Permission
        ]
        #------------------------------>
        for a,b,c,d in tInput:
            with self.subTest(f"value={a}, fof={b}, opt={c}"):
                #------------------------------>
                result = cCheck.Path2FFInput(a, fof=b, opt=c)[0]
                #------------------------------>
                self.assertIs(result, d)
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_NumberList(unittest.TestCase):
    """Test for core.check.NumberList"""
    #region -----------------------------------------------------> Class Setup
    @classmethod
    def setUpClass(cls):
        """Set test"""
        cls.a = '1 2 3 4'
        cls.b = '1 2 3 4.0'
        cls.c = '1 2 3 4-10'
        cls.d = '1 2 3 4-10 5.4'
        cls.e = '1 2 3 4-10 11a'
        cls.f = '1 2 3 4-10 6'
        cls.g = '4-10 11'
        cls.h = '1,2,3, 4-10'
    #---
    #endregion --------------------------------------------------> Class Setup

    #region -------------------------------------------------> Expected Output
    def test_expected_output(self):
        """Test for the first element of the expected output"""
        #------------------------------>
        tInput = [
            ('',       'int', False, ' ',  True, None, None, None, None, None,  True), # Optional
            ('',       'int', False, ' ', False, None, None, None, None, None, False), #
            (self.a,   'int', False, ' ', False, None, None, None, None, None,  True), # NumType
            (self.b,   'int', False, ' ', False, None, None, None, None, None, False), #
            (self.c,   'int', False, ' ', False, None, None, None, None, None,  True), #
            (self.d,   'int', False, ' ', False, None, None, None, None, None, False), #
            (self.d, 'float', False, ' ', False, None, None, None, None, None,  True), #
            (self.e,   'int', False, ' ', False, None, None, None, None, None, False), #
            (self.f,   'int', False, ' ', False, None, None, None, None, None,  True), # Unique
            (self.f,   'int',  True, ' ', False, None, None, None, None, None, False), #
            (self.a,   'int',  True, ' ', False,    3, None, None, None, None, False), # vMin
            (self.g,   'int',  True, ' ', False, None,   10, None, None, None, False), # vMax
            (self.c,   'int',  True, ' ', False,    0,   10, None, None, None,  True), #
            (self.a,   'int',  True, ' ', False,    0,   10, None,    3, None, False), # Length
            (self.a,   'int',  True, ' ', False,    0,   10,    0,    3,    5, False), #
            (self.a,   'int',  True, ' ', False,    0,   10,    0,    4,    1,  True), #
            (self.a,   'int',  True, ' ', False,    0,   10,    0, None,    5,  True), #
            (self.f,   'int', False, ' ', False,    0,   10,    0, None,    5, False), #
            (self.h,   'int',  True, ',', False, None, None, None, None, None,  True),
        ]
        #------------------------------>
        for a,b,c,d,e,f,g,h,i,j,k in tInput:
            msg = (
                f"tStr={a}, numType={b}, unique={c}, sep={d}, opt={e}, "
                f"vMin={f}, vMax={g}, nMin={h}, nN={i}, nMax={j}"
            )
            with self.subTest(msg):
                #------------------------------>
                result = cCheck.NumberList(
                    a,
                    numType = b,
                    unique  = c,
                    sep     = d,
                    opt     = e,
                    vMin    = f,
                    vMax    = g,
                    nMin    = h,
                    nN      = i,
                    nMax    = j,
                )[0]
                #------------------------------>
                self.assertIs(result, k)
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_AInRange(unittest.TestCase):
    """Test for core.check.AInRange"""
    #region -------------------------------------------------> Expected output
    def test_expected_output(self):
        """Test for first element in expected result"""
        #------------------------------>
        tInput = [
            (     6,  None,   None,  True),                                     # Nothing to compare is True
            (     6,   '3',     10,  True),                                     #   3 <=    6 <=   10 is True
            (  '-2',  '-4',      0,  True),                                     #  -4 <=   -2 <=    0 is True
            (   '3',   '3',     10,  True),                                     #   3 <=    3 <=   10 is True
            (  '10',   '3',   '10',  True),                                     #   3 <=   10 <=   10 is True
            (   '0',   '3',     10, False),                                     #   3 <=    0 <=   10 is False
            ('30.3', '3.5', '10.9', False),                                     # 3.5 <= 30.3 <= 10.9 is False
            (     6,   '3',   None,  True),                                     #   3 <=    6         is True
            (    '3',  '3',   None,  True),                                     #   3 <=    3         is True
            (     -3,  '3',   None, False),                                     #   3 <=   -3         is False
            (      3, None,    '6',  True),                                     #   3 <=    6         is True
            (    '3', None,    '3',  True),                                     #           3 <=    3 is True
            (     -1, None, '-3.9', False),                                     #          -1 <= -3.9 is False
        ]
        #------------------------------>
        for a,b,c,d in tInput:
            with self.subTest(f"a={a}, refMin={b}, refMax={c}"):
                #------------------------------>
                result = cCheck.AInRange(a, refMin=b, refMax=c)[0]
                #------------------------------>
                self.assertIs(result, d)
    #---
    #endregion ----------------------------------------------> Expected output
#---


class Test_ListUnique(unittest.TestCase):
    """Test for core.check.ListUnique"""
    #region -------------------------------------------------> Expected Output
    def test_expected_output(self):
        """Test for first element in expected result"""
        #------------------------------>
        tInput = [
            (                               [], False, False),
            (                               [],  True,  True),
            (                        [1,2,3,4], False,  True),
            (  [1,2,3,4,5,6,7,8,9,'A','B','C'], False,  True),
            (            [1,2,3,'1','2','3',2], False, False),
            (['A',1,2,3,'1','2','3',2,'3','A'], False, False),
        ]
        #------------------------------>
        for a,b,c in tInput:
            with self.subTest(f"tList={a}, opt={b}"):
                #------------------------------>
                result = cCheck.ListUnique(a, opt=b)[0]
                #------------------------------>
                self.assertIs(result, c)
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_UniqueColNumbers(unittest.TestCase):
    """Test for core.check.UniqueColNumbers"""
    #region -----------------------------------------------------> Class Setup
    @classmethod
    def setUpClass(cls):                                                        # pylint: disable=arguments-differ
        """Set test"""
        cls.a = [1, 2, 3, 4]
        cls.b = ['1 2 3 4', '5-7, 8-10; 11-13, 14-16', '17-20']
        cls.c = [' 1 2 3 4 ', '5-7  ,  8-10 ; 11-13  , 14-16', '  17-20  ']
        cls.d = [' 1 2 12 4 ', '5-7  ,  8-10 ; 11-13  , 14-16', '  17-20  ']
        cls.e = [' 1 2 1.2 4 ', '5-7  ,  8-10 ; 11-13  , 14-16', '  17-20  ']
        cls.f = ['1 2 3', '3-5']
        cls.sepListA = [' ', ',', ';']
        cls.sepListB = [1, 2, 3]
        cls.sepListC = [' ', ',', ';', '\t']
        cls.sepListD = [' ', ',']
    #---
    #endregion --------------------------------------------------> Class Setup

    #region -------------------------------------------------> Expected Output
    def test_expected_output(self):
        """Test for expected output"""
        #------------------------------>
        tInput = [
            (self.b, self.sepListC, False),                                     # Bad Input
            (self.b, self.sepListD, False),
            (self.e, self.sepListA, False),                                     # Non-Integer
            (self.b, self.sepListA,  True),
            (self.c, self.sepListA,  True),
            (self.d, self.sepListA, False),                                     # Not Unique
            (self.f, self.sepListA, False),
        ]
        #------------------------------>
        for a,b,c in tInput:
            with self.subTest(f'value={a}, sepList={b}'):
                #------------------------------>
                result = cCheck.UniqueColNumbers(a, sepList=b)[0]
                #------------------------------>
                self.assertIs(result, c)
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_Comparison(unittest.TestCase):
    """Test for core.check.Comparison"""
    #region -----------------------------------------------------> Class Setup
    @classmethod
    def setUpClass(cls):                                                        # pylint: disable=arguments-differ
        """Set test"""
        cls.op1 = ['<', '>', '<=', '>=']
        cls.op2 = ['>', '<=', '>=']
    #---
    #endregion --------------------------------------------------> Class Setup

    #region -------------------------------------------------> Expected Output
    def test_expected_output(self):
        """Test for expected output"""
        #------------------------------>
        tInput = [
            ('    ',  'float',  True,   0,   100, self.op2,  True),
            ('< 1.4', 'float', False,    0,  100, self.op1,  True),
            (  '1.4', 'float', False,    0,  100, self.op1, False),
            ('< 1.4',   'int', False,    0,  100, self.op2, False),
            ('< 1.4',   'int', False,    0,  100, self.op1, False),
            ('< 1.4',   'int', False,   20,  100, self.op1, False),
            ('< 204',   'int', False,   20,  100, self.op1, False),
            ('< 204',   'int', False, None, None, self.op1,  True),
            ('> 204',   'int', False,   20,  300, self.op1,  True),
        ]
        #------------------------------>
        for a,b,c,d,e,f,g in tInput:
            msg = (
                f'tStr={a}, numType={b}, opt={c}, vMin={d}, vMax={e}, op={f}')
            with self.subTest(msg):
                #------------------------------>
                result = cCheck.Comparison(
                    a, numType=b, opt=c, vMin=d, vMax=e, op=f)[0]
                #------------------------------>
                self.assertIs(result, g)
    #---
    #endregion ----------------------------------------------> Expected Output
#---
#endregion ------------------------------------------------------> Class Setup
