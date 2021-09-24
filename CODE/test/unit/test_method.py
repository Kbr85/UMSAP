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


"""tests for data.method """


#region -------------------------------------------------------------> Imports
import unittest

import data.method as dmethod
#endregion ----------------------------------------------------------> Imports

#region ---------------------------------------------------------> Class Setup
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
