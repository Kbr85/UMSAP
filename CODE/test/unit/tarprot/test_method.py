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


"""Tests for tarprot.method"""


#region -------------------------------------------------------------> Imports
import unittest
from pathlib import Path

import pandas as pd
from numpy import nan
from pandas import NA

from core    import file   as cFile
from tarprot import method as tarpMethod
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------> File Location
folder = Path(__file__).parent / 'file'
fileA  = folder / 'tarprot-data-file-1.txt'
fileB  = folder / 'tarprot-seq-both-1.txt'
fileC  = folder / 'res-tarprot-1.txt'
fileD  = folder / 'res-tarprot-2.txt'
#endregion ----------------------------------------------------> File Location


#region -------------------------------------------------------------> Classes
class Test_TarProt(unittest.TestCase):
    """Test for tarprot.method.TarProt"""
    #region -----------------------------------------------------> Class Setup
    @classmethod
    def setUpClass(cls):
        """Set test"""
        cls.df    = cFile.ReadCSV2DF(fileA)
        cls.dict1 = tarpMethod.UserData(
            seqFileObj    = cFile.FastaFile(fileB),
            cero          = True,
            tran          = 'Log2',
            norm          = 'Median',
            imp           = 'None',
            shift         = 1.8,
            width         = 0.3,
            method        = 'slope',
            targetProt    = 'efeB',
            scoreVal      = 100.0,
            correctedP    = 'Bonferroni',
            alpha         = 0.05,
            labelA        = ['Exp1', 'Exp2'],
            ctrlName      = 'Ctrl',
            ocSeq         = 0,
            ocTargetProt  = 38,
            ocScore       = 44,
            ocResCtrl     = [[[98, 99, 100, 101, 102, 103, 104, 105]], [[109, 110, 111]], [[112, 113, 114]]],
            ocColumn      = [0, 38, 44, 98, 99, 100, 101, 102, 103, 104, 105, 109, 110, 111, 112, 113, 114],
            dfSeq         = 0,
            dfTargetProt  = 1,
            dfScore       = 2,
            dfResCtrl     = [[[3, 4, 5, 6, 7, 8, 9, 10]], [[11, 12, 13]], [[14, 15, 16]]],
            dfResCtrlFlat = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
            dfColumnR     = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
            dfColumnF     = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
        )
        cls.dict2 = tarpMethod.UserData(
            seqFileObj    = cFile.FastaFile(fileB),
            cero          = True,
            tran          = 'Log2',
            norm          = 'Median',
            imp           = 'None',
            shift         = 1.8,
            width         = 0.3,
            method        = 'ttest',
            indSample     = 'i',
            targetProt    = 'efeB',
            scoreVal      = 0,
            alpha         = 0.05,
            correctedP    = 'None',
            labelA        = ['Exp1', 'Exp2', 'Exp3'],
            ctrlName      = 'Ctrl',
            ocSeq         = 0,
            ocTargetProt  = 38,
            ocScore       = 44,
            ocResCtrl     = [[[98, 99, 100, 101, 102, 103, 104, 105]], [[109, 110, 111]], [[112, 113, 114]], [[115, 116, 117, 120]]],
            ocColumn      = [0, 38, 44, 98, 99, 100, 101, 102, 103, 104, 105, 109, 110, 111, 112, 113, 114, 115, 116, 117, 120],
            dfSeq         = 0,
            dfTargetProt  = 1,
            dfScore       = 2,
            dfResCtrl     = [[[3, 4, 5, 6, 7, 8, 9, 10]], [[11, 12, 13]], [[14, 15, 16]], [[17, 18, 19, 20]]],
            dfResCtrlFlat = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
            dfColumnR     = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
            dfColumnF     = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        )
    #---
    #endregion --------------------------------------------------> Class Setup

    #region -------------------------------------------------> Expected Output
    def test_output(self):
        """Test method output"""
        #------------------------------>
        tInput = [
            (self.df, self.dict1, True, fileC, 'Test - 1'),
            (self.df, self.dict2, True, fileD, 'Test - 2'),
        ]
        #------------------------------>
        for a,b,c,d,e in tInput:
            with self.subTest(f"{e}"):
                #------------------------------>
                result = tarpMethod.TarProt(
                    df=a, rDO=b, resetIndex=c)[0]['dfR']
                # result = result.round(2)
                #------------------------------>
                dfF = pd.read_csv(d, sep='\t', header=[0,1])#.round(2)
                dfF.iloc[:,4:6] = dfF.iloc[:,4:6].astype('Int64')
                #------------------------------>
                # pylint: disable=protected-access
                pd._testing.assert_frame_equal(result, dfF)                     # type: ignore
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_R2AA(unittest.TestCase):
    """Test for tarprot.method.R2AA

        Notes
        -----
        Last row with the chi2 results is not tested here.
    """
    #region -----------------------------------------------------> Class Setup
    def setUp(self):
        """Set test"""
        self.a = pd.DataFrame({
            ('Seq','Seq') : ['TVAQA', 'MLVAF', 'TITLS', 'LRDII', 'WVTAD', 'PDYAS', 'HDLEK', 'MKHHH', 'HHHLM'],
            ('Exp1', 'P') : [  0.001,   0.904,   0.001,   0.012,   0.869,   0.001,   0.504,   0.176,   0.010],
            ('Exp2', 'P') : [  0.963,   0.001,   0.001,   0.001,   0.001,   0.112,   0.058,   0.001,   0.690],
            ('Exp3', 'P') : [  0.732,   0.001,   0.605,   0.164,   0.650,   0.230,   0.001,   0.001,   0.001],
        })
        self.seq = (
            'MKHHHHHHHHHHHHMKKTAIAIAVALAGFATVAQAASWSHPQFEKIEGRRDRGQKTQSAP'
            'GTLSPDARNEKQPFYGEHQAGILTPQQAAMMLVAFDVLASDKADLERLFRLLTQRFAFLT'
            'QGGAAPETPNPRLPPLDSGILGGYIAPDNLTITLSVGHSLFDERFGLAPQMPKKLQKMTR'
            'FPNDSLDAALCHGDVLLQICANTQDTVIHALRDIIKHTPDLLSVRWKREGFISDHAARSK'
            'GKETPINLLGFKDGTANPDSQNDKLMQKVVWVTADQQEPAWTIGGSYQAVRLIQFRVEFW'
            'DRTPLKEQQTIFGRDKQTGAPLGMQHEHDVPDYASDPEGKVIALDSHIRLANPRTAESES'
            'SLMLRRGYSYSLGVTNSGQLDMGLLFVCYQHDLEKGFLTVQKRLNGEALEEYVKPIGGGY'
            'FFALPGVKDANDYFGSALLRVMMMMMMMHHHHHHHHHLM')
        self.b = pd.DataFrame(
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
                result = tarpMethod.R2AA(a, b, c, d, e)
                result = result.iloc[0:-1,:] # Exclude chi2 test row
                #------------------------------>
                # pylint: disable=protected-access
                pd._testing.assert_frame_equal(result, f)                       # type: ignore
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_R2Hist(unittest.TestCase):
    """Test for tarprot.method.R2Hist"""
    #region -----------------------------------------------------> Class Setup
    def setUp(self):
        """Set test"""
        self.a = pd.DataFrame({
            ('Nterm',   'Nterm') : [    1,   50,  201,  247,  258,  270,  270,  274,  311,  325,  327,  343,  368,  372,  372,  376,  432],
            ('Cterm',   'Cterm') : [   42,   62,  211,  263,  269,  283,  290,  293,  324,  342,  342,  351,  377,  385,  387,  387,  441],
            ('NtermF', 'NtermF') : [   NA,   NA,  187,  233,  244,  256,  256,  260,  297,  311,  313,  329,   NA,   NA,   NA,   NA,   NA],
            ('CtermF', 'CtermF') : [   NA,   48,  197,  249,  255,  269,  276,  279,  310,  328,  328,   NA,   NA,   NA,   NA,   NA,   NA],
            ('Exp1',        'P') : [0.001,0.904,0.001,0.012,0.869,0.819,0.504,0.919,0.380,0.915,0.713,0.104,0.012,0.904,0.001,0.190,0.808],
            ('Exp2',        'P') : [0.963,0.001,0.001,0.001,0.001,0.112,0.058,0.060,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.472],
            ('Exp3',        'P') : [0.732,0.335,0.605,0.164,0.650,0.230,0.034,0.655,0.002,0.008,0.243,0.307,0.240,0.666,0.663,0.189,0.001],
        })

        self.b = pd.DataFrame({
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

        self.c = pd.DataFrame({
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
            (self.a, 0.05, [50], (441, 441), self.b),
            (self.a, 0.05, [200, 250, 300], (441, 441), self.c),
        ]
        #------------------------------>
        for a,b,c,d,e in tInput:
            with self.subTest(
                f'df={a}, alpha={b}, win={c}, maxL={d}'):
                #------------------------------>
                result = tarpMethod.R2Hist(a, b, c, d)
                #------------------------------>
                # pylint: disable=protected-access
                pd._testing.assert_frame_equal(result, e)                       # type: ignore
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_R2CpR(unittest.TestCase):
    """Test for tarprot.method.R2CpR"""
    #region -----------------------------------------------------> Class Setup
    def setUp(self):
        """Set test"""
        self.a = pd.DataFrame({
            ('Nterm',   'Nterm') : [    1,   5,  20,  24,  25,  27,  27,  27,  31,  32,  32,  34,  36,  37,  37,  37,  43],
            ('Cterm',   'Cterm') : [    4,   6,  21,  26,  26,  28,  29,  30,  32,  34,  35,  36,  38,  39,  40,  41,  45],
            ('NtermF', 'NtermF') : [   NA,   NA, 16,  20,  21,  23,  23,  23,  27,  28,  28,  30,  NA,  NA,  NA,  NA,  NA],
            ('CtermF', 'CtermF') : [   NA,    2, 17,  22,  22,  24,  25,  26,  28,  30,  31,  NA,  NA,  NA,  NA,  NA,  NA],
            ('Exp1',        'P') : [0.001,0.904,0.001,0.012,0.869,0.819,0.504,0.919,0.380,0.915,0.713,0.104,0.012,0.904,0.001,0.190,0.808],
            ('Exp2',        'P') : [0.963,0.001,0.001,0.001,0.001,0.112,0.058,0.060,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.472],
            ('Exp3',        'P') : [0.732,0.335,0.605,0.164,0.650,0.230,0.034,0.655,0.002,0.008,0.243,0.307,0.240,0.666,0.663,0.189,0.001],
        })

        self.b = pd.DataFrame({
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
            (self.a, 0.05, (45, 45), self.b),
        ]
        #------------------------------>
        for a,b,c,d in tInput:
            with self.subTest(
                f'df={a}, alpha={b}, protL={c}'):
                #------------------------------>
                result = tarpMethod.R2CpR(a, b, c)
                #------------------------------>
                # pylint: disable=protected-access
                pd._testing.assert_frame_equal(result, d)                       # type: ignore
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_R2CEvol(unittest.TestCase):
    """Test for tarprot.method.R2CEvol"""
    #region -----------------------------------------------------> Class Setup
    def setUp(self):
        """Set test"""
        self.a = pd.DataFrame({
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

        self.b = pd.DataFrame({
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
            (self.a, 0.05, (45, 47), self.b),
        ]
        #------------------------------>
        for a,b,c,d in tInput:
            with self.subTest(
                f'df={a}, alpha={b}, protL={c}'):
                #------------------------------>
                result = tarpMethod.R2CEvol(a, b, c)
                #------------------------------>
                # pylint: disable=protected-access
                pd._testing.assert_frame_equal(result, d)                       # type: ignore
    #---
    #endregion ----------------------------------------------> Expected Output
#---
#endregion ----------------------------------------------------------> Classes
