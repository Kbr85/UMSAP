# ------------------------------------------------------------------------------
# Copyright (C) 2017 Kenny Bravo Rodriguez <www.umsap.nl>
#
# Author: Kenny Bravo Rodriguez (kenny.bravorodriguez@mpi-dortmund.mpg.de)
#
# This program is distributed for free in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See the accompaning licence for more details.
# ------------------------------------------------------------------------------


"""tests for data.check """


#region -------------------------------------------------------------> Imports
import unittest

import data.check as dcheck
import dtscore.exception as dtsException
#endregion ----------------------------------------------------------> Imports

#region ---------------------------------------------------------> Class Setup
class Test_UniqueColNumbers(unittest.TestCase):
    """Test for data.check.UniqueColNumbers"""
    #region -----------------------------------------------------> Class Setup
    @classmethod
    def setUp(cls):
        """"""
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

    #region -----------------------------------------------------> Valid Input
    def test_invalid_input(self):
        """Test for invalid input"""
        #------------------------------>
        badInput = [
            (self.a, self.sepListA),
            (self.b, self.sepListC),
            (self.b, self.sepListD),
            (self.e, self.sepListA),   
        ]
        #------------------------------>
        for a,b in badInput:
            with self.subTest(f'value={a}, sepList={b}'):
                self.assertRaises(
                    dtsException.InputError,
                    dcheck.UniqueColNumbers,
                    a, sepList=b,
                )
    #---
    #endregion --------------------------------------------------> Valid Input

    #region -------------------------------------------------> Expected Output
    def test_expected_output(self):
        """Test for expected output"""
        #------------------------------>
        tInput = [
            (self.b, self.sepListA,  True),    
            (self.c, self.sepListA,  True),    
            (self.d, self.sepListA, False), 
            (self.f, self.sepListA, False), 
        ]
        #------------------------------>
        for a,b,c in tInput:
            with self.subTest(f'value={a}, sepList={b}'):
                #------------------------------>
                result = dcheck.UniqueColNumbers(a, sepList=b)[0]
                #------------------------------>
                self.assertIs(result, c)
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_TcUniqueColNumbers(unittest.TestCase):
    """Test for data.check.TcUniqueColNumbers"""
    #region -----------------------------------------------------> Valid Input
    def test_invalid_input(self):
        """Test for invalid input"""
        #------------------------------>
        badInput = [
            (1, [' ', ',', ';']),
        ]
        #------------------------------>
        for a,b in badInput:
            with self.subTest(f'tcList={a}, sepList={b}'):
                self.assertRaises(
                    dtsException.InputError,
                    dcheck.TcUniqueColNumbers,
                    a, sepList=b,
                )
    #---
    #endregion --------------------------------------------------> Valid Input

    #region -------------------------------------------------> Expected Output
    
    #endregion ----------------------------------------------> Expected Output
#---
#endregion ------------------------------------------------------> Class Setup




if __name__ == '__main__':
    unittest.main()
