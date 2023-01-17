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
tarprotData   = folder / 'tarprot-data-file.txt'   # For CorrA
tarprotData1  = folder / 'tarprot-data-file-1.txt' # For TarProt
protprofData  = folder / 'protprof-data-file.txt'  # For ProtProf
limprotData   = folder / 'limprot-data-file.txt'   # For LimProt
seqFileBoth   = folder / 'tarprot-seq-both.txt'    # Fasta File with two seq
seqLimProt    = folder / 'limprot-seq-both.txt'
tarprot_seq_1 = folder / 'tarprot-seq-both-1.txt'
#------------------------------> Result Files
#-------------->
protprof_1 = folder / 'res-protprof-1.txt'
limprot_1  = folder / 'res-limprot-1.txt'
tarprot_1  = folder / 'res-tarprot-1.txt'
#endregion ------------------------------------------------------------> Files


#region -------------------------------------------------------> pd.DataFrames
DF_DFFilterByColN = pd.DataFrame({
    'A' : [1,2,3,4,5],
    'B' : [1,2,3,4,5],
})
#endregion ----------------------------------------------------> pd.DataFrames


#region ---------------------------------------------------------> Class Setup
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
                'ExcludeR': [3, 4, 5],
                'ResCtrl': [[[6, 7, 8]], [[9, 10, 11], [12, 13, 14]], [[15, 16, 17], [18, 19, 20]]],
                'ResCtrlFlat': [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
                'ColumnR': [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
                'ColumnF': [2, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
            },
        }
    #---
    #endregion --------------------------------------------------> Class Setup

    #region -------------------------------------------------> Expected Output
    def test_output(self):
        """Test method output"""
        #------------------------------>
        tInput = [
            (self.df, self.dict1, self.dExtra, True, protprof_1),
        ]
        #------------------------------>
        for a,b,c,d,e in tInput:
            with self.subTest(f"df={a}, rDO={b}, dExtra={c}, resetIndex={d}"):
                #------------------------------>
                result = mMethod.ProtProf(
                    a, b, c, resetIndex=d)[0]['dfR']
                result = result.round(2)
                #------------------------------>
                dfF = pd.read_csv(e, sep='\t', header=[0,1,2]).round(2)
                #------------------------------>
                # pylint: disable=protected-access
                pd._testing.assert_frame_equal(result, dfF)                     # type: ignore
    #---
    #endregion ----------------------------------------------> Expected Output
#---
#endregion ------------------------------------------------------> Class Setup


if __name__ == '__main__':
    unittest.main()
