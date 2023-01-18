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

from config.config import config as mConfig
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
        self.df = cFile.ReadCSV2DF(fileA)
        self.dExtra  = {
            'cLDFFirstThree' : mConfig.limp.dfcolFirstPart,
            'cLDFThirdLevel' : mConfig.limp.dfcolCLevel,
            'rSeqFileObj'    : cFile.FastaFile(fileB),
        }
        self.dict1 = {
            'Cero': True,
            'TransMethod': 'Log2',
            'NormMethod': 'Median',
            'ImpMethod': 'None',
            'Shift': 1.8,
            'Width': 0.3,
            'TargetProt': 'Mis18alpha',
            'ScoreVal': 25.0,
            'Sample': 'i',
            'Alpha': 0.05,
            'Beta': 0.05,
            'Gamma': 0.8,
            'Theta': None,
            'ThetaMax': 8.0,
            'Lane': ['Lane1', 'Lane2'],
            'Band': ['Band1', 'Band2'],
            'ControlL': ['Ctrl'],
            'oc': {
                'SeqCol': 0,
                'TargetProtCol': 34,
                'ScoreCol': 42,
                'ResCtrl': [[[69, 70, 71]], [[81, 82, 83], [78, 79, 80]], [[], [66, 67, 68]]],
                'ColumnF': [42, 69, 70, 71, 81, 82, 83, 78, 79, 80, 66, 67, 68],
                'Column': [0, 34, 42, 69, 70, 71, 81, 82, 83, 78, 79, 80, 66, 67, 68],
            },
            'df': {
                'SeqCol': 0,
                'TargetProtCol': 1,
                'ScoreCol': 2,
                'ResCtrl': [[[3, 4, 5]], [[6, 7, 8], [9, 10, 11]], [[], [12, 13, 14]]],
                'ResCtrlFlat': [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
                'ColumnR': [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
                'ColumnF': [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
            },
            'dfo' : {
                    'NC': [2, 3],
                    'NCF': [4, 5],
            },
        }
    #---
    #endregion --------------------------------------------------> Class Setup

    #region -------------------------------------------------> Expected Output
    def test_output(self):
        """Test method output"""
        #------------------------------>
        tInput = [
            (self.df, self.dict1, self.dExtra, True, fileC),
        ]
        #------------------------------>
        for a,b,c,d,e in tInput:
            with self.subTest(f"df={a}, rDO={b}, dExtra={c}, resetIndex={d}"):
                #------------------------------>
                result = limpMethod.LimProt(
                    df=a, rDO=b, rDExtra=c, resetIndex=d)[0]['dfR']
                # result = result.round(2)
                #------------------------------>
                dfF = pd.read_csv(e, sep='\t', header=[0,1,2])#.round(2)
                dfF.iloc[:,4:6] = dfF.iloc[:,4:6].astype('Int64')
                #------------------------------>
                # pylint: disable=protected-access
                pd._testing.assert_frame_equal(result, dfF)                     # type: ignore
    #---
    #endregion ----------------------------------------------> Expected Output
#---
#endregion ----------------------------------------------------------> Classes
