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


"""Tests for limprot.method"""


#region -------------------------------------------------------------> Imports
import unittest
from pathlib import Path

import pandas as pd

from core    import file   as cFile
from limprot import method as limpMethod
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------> File Location
folder = Path(__file__).parent / 'file'
fileA  = folder / 'limprot-data-file.txt'
fileB  = folder / 'limprot-seq-both.txt'
fileC  = folder / 'res-limprot-1.txt'
#endregion ----------------------------------------------------> File Location


#region -------------------------------------------------------------> Classes
class Test_LimProt(unittest.TestCase):
    """Test for limprot.method.LimProt"""
    #region -----------------------------------------------------> Class Setup
    def setUp(self):
        """Set test"""
        self.df    = cFile.ReadCSV2DF(fileA)
        self.dict1 = limpMethod.UserData(
            seqFile       = fileB,
            seqFileObj    = cFile.FastaFile(fileB),
            cero          = True,
            tran          = 'Log2',
            norm          = 'Median',
            imp           = 'None',
            shift         = 1.8,
            width         = 0.3,
            targetProt    = 'Mis18alpha',
            scoreVal      = 25.0,
            indSample     = True,
            alpha         = 0.05,
            beta          = 0.05,
            gamma         = 0.8,
            theta         = None,
            thetaM        = 8.0,
            labelA        = ['Lane1', 'Lane2'],
            labelB        = ['Band1', 'Band2'],
            ctrlName      = 'Ctrl',
            ocSeq         = 0,
            ocTargetProt  = 34,
            ocScore       = 42,
            ocResCtrl     = [[[69, 70, 71]], [[81, 82, 83], [78, 79, 80]], [[], [66, 67, 68]]],
            ocColumn      = [0, 34, 42, 69, 70, 71, 81, 82, 83, 78, 79, 80, 66, 67, 68],
            dfSeq         = 0,
            dfTargetProt  = 1,
            dfScore       = 2,
            dfResCtrl     = [[[3, 4, 5]], [[6, 7, 8], [9, 10, 11]], [[], [12, 13, 14]]],
            dfResCtrlFlat = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
            dfColumnR     = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
            dfColumnF     = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
        )
    #---
    #endregion --------------------------------------------------> Class Setup

    #region -------------------------------------------------> Expected Output
    def test_output(self):
        """Test method output"""
        #------------------------------>
        tInput = [
            (self.df, self.dict1, True, fileC, 'Test - 1'),
        ]
        #------------------------------>
        for a,b,c,d,e in tInput:
            with self.subTest(f"{e}"):
                #------------------------------>
                result = limpMethod.LimProt(
                    df=a, rDO=b, resetIndex=c)[0]['dfR']
                # result = result.round(2)
                #------------------------------>
                dfF = pd.read_csv(d, sep='\t', header=[0,1,2])#.round(2)
                dfF.iloc[:,4:6] = dfF.iloc[:,4:6].astype('Int64')
                #------------------------------>
                # pylint: disable=protected-access
                pd._testing.assert_frame_equal(result, dfF)                     # type: ignore
    #---
    #endregion ----------------------------------------------> Expected Output
#---
#endregion ----------------------------------------------------------> Classes
