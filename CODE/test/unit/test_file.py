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


"""Tests for data.file """


#region -------------------------------------------------------------> Imports
import unittest
from pathlib import Path

import pandas as pd

import data.file      as mFile
import data.exception as mException
#endregion ----------------------------------------------------------> Imports


# Test data lead to long lines, so this check will be disabled for this module
# pylint: disable=line-too-long


#region -------------------------------------------------------> File Location
folder = Path(__file__).parent / 'test_files'
fasta1Prot = folder / 'tarprot-seq-rec.txt'
fasta2Prot = folder / 'tarprot-seq-both.txt'
fastaNProt = folder / 'tarprot-seq-N.txt'
pdb        = folder / '2y4f.pdb'
csvFile    = folder / 'res-corrA-1.txt'
#endregion ----------------------------------------------------> File Location


#region ---------------------------------------------------------> Class Setup
class Test_ReadFileFirstLine(unittest.TestCase):
    """Test for data.file.ReadFileFirstLine"""
    #region -----------------------------------------------------> Class Setup
    @classmethod
    def setUp(cls):                                                             # pylint: disable=arguments-differ
        """Create class instances"""
        cls.file = fasta1Prot
        cls.firstLine = ['>sp|P31545|EFEB_ECOLI Recombinant']
        cls.firstLineSpace = ['>sp|P31545|EFEB_ECOLI', 'Recombinant']
    #---
    #endregion --------------------------------------------------> Class Setup

    #region -------------------------------------------------> Expected Output
    def test_expected_output(self):
        """Test for expected output"""
        #------------------------------>
        tInput = [
            (self.file, '', False, self.firstLine),
            (self.file, '',  True, self.firstLine),
            (self.file, ' ', False, self.firstLineSpace),
        ]
        #------------------------------>
        for a,b,c,d in tInput:
            msg = f"fileP={a}, char={b}, empty={c}"
            with self.subTest(msg):
                result = mFile.ReadFileFirstLine(a, char=b, empty=c)
                self.assertEqual(result, d)
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_CSVFile(unittest.TestCase):
    """Test for data.file.CSVFile"""
    #region -----------------------------------------------------> Class Setup
    @classmethod
    def setUp(cls):                                                             # pylint: disable=arguments-differ
        """Create class instances"""
        cls.csvFile = mFile.CSVFile(csvFile)
        cls.header = [
            'Unnamed: 0', 'Intensity 01', 'Intensity 02', 'Intensity 03',
            'Intensity 04', 'Intensity 05']
    #---
    #endregion --------------------------------------------------> Class Setup

    #region -------------------------------------------------> Expected Output
    def test_Init(self):
        """Test correct initialization"""
        #------------------------------>
        tInput = [
            (self.csvFile.rFileP,  csvFile,     'File Path'),
            (self.csvFile.rHeader, self.header, 'Data Header'),
            (self.csvFile.rNRow,   5,           'Number of Rows'),
            (self.csvFile.rNCol,   6,           'Number of Columns'),
        ]
        #------------------------------>
        for a,b,c in tInput:
            msg = f"{c}"
            with self.subTest(msg):
                self.assertEqual(a, b)
    #---

    def test_StrInCol(self):
        """Test for StrInCol method"""
        #------------------------------>
        tInput = [
            (self.csvFile, 'Intensity 04', 0, True),
            (self.csvFile, 'Intensity 20', 0, False),
        ]
        #------------------------------>
        for a,b,c,d in tInput:
            msg = f"tStr={b}, col={c}"
            with self.subTest(msg):
                #------------------------------>
                result = a.StrInCol(b, c)
                #------------------------------>
                self.assertEqual(result, d)
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_FastaFile(unittest.TestCase):
    """Test for data.file.FastaFile"""
    #region -----------------------------------------------------> Class Setup
    @classmethod
    def setUp(cls):                                                             # pylint: disable=arguments-differ
        """Create class instances"""
        cls.f1Prot = mFile.FastaFile(fasta1Prot)
        cls.f2Prot = mFile.FastaFile(fasta2Prot)
        cls.fNProt = mFile.FastaFile(fastaNProt)
        cls.seq1 = ('HHHHHHHHHHHHHHMKKTAIAIAVALAGFATVAQAASWSHPQFEKIEGRRDRGQKTQSAP'
                    'FFALPGVKDANDYFGSALLRVMMMMMMMHHHHHHHHHH')
        cls.head1 = '>sp|P31545|EFEB_ECOLI Recombinant'
        cls.seq2 = ('MKKTAIAIAVALAGFATVAQAASWSHPQFEKIEGRRDRGQKTQSAPFFALPGVKDANDYF'
                    'GSALLRVM')
        cls.head2 = '>sp|P31545|EFEB_ECOLI Native'
        cls.seq3  = ('VLLQICANTQDTVIHALRDIIKHTPDLLSVRWKREGFISDHAARSKGKETPINLLGFKDG'
                     'TNSGQLDMGLLFVCYQHDL')
        cls.head3 = '>sp|X|Other protein'
    #---
    #endregion --------------------------------------------------> Class Setup

    #region -------------------------------------------------> Expected Output
    def test_Init(self):
        """Test correct initialization"""
        #------------------------------>
        tInput = [
            (self.f1Prot.rHeaderRec, self.head1,    'Head - Rec - 1'),
            (self.f2Prot.rHeaderRec, self.head1,    'Head - Rec - 2'),
            (self.fNProt.rHeaderRec, self.head1,    'Head - Rec - N'),
            (self.f1Prot.rSeqRec,     self.seq1,     'Seq - Rec - 1'),
            (self.f2Prot.rSeqRec,     self.seq1,     'Seq - Rec - 2'),
            (self.fNProt.rSeqRec,     self.seq1,     'Seq - Rec - N'),
            (self.f1Prot.rHeaderNat,         '',    'Head - Nat - 1'),
            (self.f2Prot.rHeaderNat, self.head2,    'Head - Nat - 2'),
            (self.fNProt.rHeaderNat, self.head2,    'Head - Nat - N'),
            (self.f1Prot.rSeqNat,            '',     'Seq - Nat - 1'),
            (self.f2Prot.rSeqNat,     self.seq2,     'Seq - Nat - 2'),
            (self.fNProt.rSeqNat,     self.seq2,     'Seq - Nat - N'),
            (self.f1Prot.rSeqLengthRec,      98,  'Length - Nat - 1'),
            (self.f2Prot.rSeqLengthRec,      98,  'Length - Nat - 2'),
            (self.fNProt.rSeqLengthRec,      98,  'Length - Nat - N'),
            (self.f1Prot.rSeqLengthNat,    None,  'Length - Nat - 1'),
            (self.f2Prot.rSeqLengthNat,      68,  'Length - Nat - 2'),
            (self.fNProt.rSeqLengthNat,      68,  'Length - Nat - N'),
        ]
        #------------------------------>
        for a,b,c in tInput:
            msg = f"{c}"
            with self.subTest(msg):
                self.assertEqual(a, b)
    #---

    def test_FindSeq_NoExc(self):
        """Test for FindSeq method with no Exception."""
        #------------------------------>
        tInput = [
            (self.f1Prot, 'XXXXX',         True, (-1,-1)),
            (self.f2Prot, 'XXXXX',         True, (-1,-1)),
            (self.f2Prot, 'XXXXX',        False, (-1,-1)),
            (self.f2Prot, 'HHHHHHH',       True,   (1,7)),
            (self.f2Prot, 'QAASWSHPQFEK', False, (20,31)),
            (self.f2Prot, 'GSALLRV'     , False, (61,67)),
        ]
        #------------------------------>
        for a,b,c,d in tInput:
            msg = f"FindSeq: {b}, {c}"
            with self.subTest(msg):
                #------------------------------>
                result = a.FindSeq(b,c)
                #------------------------------>
                self.assertEqual(result, d)
    #---

    def test_FindSeq_Exc(self):
        """Test for FindSeq method with Exception."""
        #------------------------------>
        tInput = [
            (self.f1Prot, 'XXXXX', False),
        ]
        #------------------------------>
        for a,b,c in tInput:
            msg = f"FindSeq: {b}, {c}"
            with self.subTest(msg):
                self.assertRaises(
                    mException.ExecutionError, a.FindSeq, b, c)
    #---

    def test_GetSelfDelta(self):
        """Test for Sequence delta."""
        #------------------------------>
        tInput = [
            (self.f2Prot, -14),
        ]
        #------------------------------>
        for a,b in tInput:
            msg = "GetSelfDelta"
            with self.subTest(msg):
                #------------------------------>
                result = a.GetSelfDelta()
                #------------------------------>
                self.assertEqual(result, b)
    #---

    def test_GetNatProtLoc(self):
        """Test for Sequence delta."""
        #------------------------------>
        tInput = [
            (self.f2Prot, (15,82)),
        ]
        #------------------------------>
        for a,b in tInput:
            msg = "GetNatProtLoc"
            with self.subTest(msg):
                #------------------------------>
                result = a.GetNatProtLoc()
                #------------------------------>
                self.assertEqual(result, b)
    #---

    def test_Exc(self):
        """Test for GetNatProtLoc and GetSelfDelta with only one protein."""
        #------------------------------>
        tInput = [
            (self.f1Prot.GetSelfDelta),
            (self.f1Prot.GetNatProtLoc),
        ]
        #------------------------------>
        for a in tInput:
            msg = "Throw exception."
            with self.subTest(msg):
                self.assertRaises(mException.ExecutionError, a)
    #---
    #endregion ----------------------------------------------> Expected Output
#---


class Test_PDBFile(unittest.TestCase):
    """Test for data.file.PDB"""
    #region -----------------------------------------------------> Class Setup
    @classmethod
    def setUp(cls):                                                             # pylint: disable=arguments-differ
        """Create class instances"""
        cls.pdb = mFile.PDBFile(pdb)
        cls.df = pd.DataFrame({
            'ATOM'      : 44*['ATOM'],
            'ANumber'   : [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,2991,2992,2993,2994,2995,2996,2997,2998,3000,3001,3002,3003,3004,3005,3006,3007,3008,3009,3010,3011,3012,3013,3014,3015,3016,3017],
            'AName'     : ['N','CA','C','O','CB','OG','N','CA','C','O','CB','N','CA','C','O','CB','CG','CD','N','CA','C','O','CB','CG1','CG2','OXT','N','CA','C','O','CB','OG','N','CA','C','O','CB','N','CA','C','O','CB','CG','CD'],
            'AltLoc'    : 44*[''],
            'ResName'   : ['SER','SER','SER','SER','SER','SER','ALA','ALA','ALA','ALA','ALA','PRO','PRO','PRO','PRO','PRO','PRO','PRO','VAL','VAL','VAL','VAL','VAL','VAL','VAL','VAL','SER','SER','SER','SER','SER','SER','ALA','ALA','ALA','ALA','ALA','PRO','PRO','PRO','PRO','PRO','PRO','PRO'],
            'Chain'     : 26*['A'] + 18 * ['B'],
            'ResNum'    : [5,5,5,5,5,5,6,6,6,6,6,7,7,7,7,7,7,7,388,388,388,388,388,388,388,388,5,5,5,5,5,5,6,6,6,6,6,7,7,7,7,7,7,7],
            'CodeResIns': 44*[''],
            'X'         : [-1.303,-0.405,-0.179,-0.215,0.932,1.515,0.062,0.292,1.549,2.571,0.390,1.491,0.370,-0.726,-1.684,1.063,2.186,2.684,6.920,7.601,8.690,8.484,6.628,5.574,5.964,9.773,1.654,0.739,1.329,1.116,-0.629,-1.553,2.060,2.746,3.941,4.617,3.209,4.238,3.634,2.407,1.910,4.762,5.508,5.495],
            'Y'         : [-24.821,-26.001,-26.358,-25.478,-25.731,-24.601,-27.651,-28.233,-27.675,-27.490,-29.758,-27.425,-27.671,-26.597,-26.704,-27.664,-26.716,-26.931,-47.432,-48.740,-48.824,-48.348,-49.971,-50.001,-50.038,-49.365,7.730,7.775,8.411,7.891,8.391,7.388,9.516,10.051,9.162,8.681,11.495,8.959,9.464,8.715,9.024,9.291,8.105,8.237],
            'Z'         : [-18.184,-18.023,-16.556,-15.685,-18.684,-18.092,-16.313,-14.980,-14.308,-14.981,-15.079,-12.971,-12.042,-12.045,-11.271,-10.684,-10.864,-12.252,14.539,14.599,13.542,12.419,14.458,15.592,13.050,13.792,6.721,5.542,4.262,3.170,5.905,6.354,4.363,3.184,2.841,3.750,3.428,1.540,0.288,-0.223,-1.296,-0.727,-0.226, 1.268],
            'Occupancy' : 44*[1.00],
            'Beta'      : [32.14,32.15,32.12,32.54,32.04,31.91,31.65,31.07,30.93,30.94,30.75,30.62,29.96,29.70,29.65,29.97,29.85,30.14,46.92,47.16,47.28,47.44,47.35,47.38,47.39,47.03,28.50,29.18,28.93,29.71,29.72,31.56,28.05,27.51,27.31,27.20,27.61,27.24,27.25,26.99,26.79,27.13,27.48,27.21],
            'Segment'   : 44*[''],
            'Element'   : ['N','C','C','O','C','O','N','C','C','O','C','N','C','C','O','C','C','C','N','C','C','O','C','C','C','O','N','C','C','O','C','O','N','C','C','O','C','N','C','C','O','C','C','C'],
        })
        cls.dfA = pd.DataFrame({
            'ATOM'      : 44*['ATOM'],
            'ANumber'   : [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,2991,2992,2993,2994,2995,2996,2997,2998,3000,3001,3002,3003,3004,3005,3006,3007,3008,3009,3010,3011,3012,3013,3014,3015,3016,3017],
            'AName'     : ['N','CA','C','O','CB','OG','N','CA','C','O','CB','N','CA','C','O','CB','CG','CD','N','CA','C','O','CB','CG1','CG2','OXT','N','CA','C','O','CB','OG','N','CA','C','O','CB','N','CA','C','O','CB','CG','CD'],
            'AltLoc'    : 44*[''],
            'ResName'   : ['SER','SER','SER','SER','SER','SER','ALA','ALA','ALA','ALA','ALA','PRO','PRO','PRO','PRO','PRO','PRO','PRO','VAL','VAL','VAL','VAL','VAL','VAL','VAL','VAL','SER','SER','SER','SER','SER','SER','ALA','ALA','ALA','ALA','ALA','PRO','PRO','PRO','PRO','PRO','PRO','PRO'],
            'Chain'     : 26*['A'] + 18 * ['B'],
            'ResNum'    : [5,5,5,5,5,5,6,6,6,6,6,7,7,7,7,7,7,7,388,388,388,388,388,388,388,388,5,5,5,5,5,5,6,6,6,6,6,7,7,7,7,7,7,7],
            'CodeResIns': 44*[''],
            'X'         : [-1.303,-0.405,-0.179,-0.215,0.932,1.515,0.062,0.292,1.549,2.571,0.390,1.491,0.370,-0.726,-1.684,1.063,2.186,2.684,6.920,7.601,8.690,8.484,6.628,5.574,5.964,9.773,1.654,0.739,1.329,1.116,-0.629,-1.553,2.060,2.746,3.941,4.617,3.209,4.238,3.634,2.407,1.910,4.762,5.508,5.495],
            'Y'         : [-24.821,-26.001,-26.358,-25.478,-25.731,-24.601,-27.651,-28.233,-27.675,-27.490,-29.758,-27.425,-27.671,-26.597,-26.704,-27.664,-26.716,-26.931,-47.432,-48.740,-48.824,-48.348,-49.971,-50.001,-50.038,-49.365,7.730,7.775,8.411,7.891,8.391,7.388,9.516,10.051,9.162,8.681,11.495,8.959,9.464,8.715,9.024,9.291,8.105,8.237],
            'Z'         : [-18.184,-18.023,-16.556,-15.685,-18.684,-18.092,-16.313,-14.980,-14.308,-14.981,-15.079,-12.971,-12.042,-12.045,-11.271,-10.684,-10.864,-12.252,14.539,14.599,13.542,12.419,14.458,15.592,13.050,13.792,6.721,5.542,4.262,3.170,5.905,6.354,4.363,3.184,2.841,3.750,3.428,1.540,0.288,-0.223,-1.296,-0.727,-0.226, 1.268],
            'Occupancy' : 44*[1.00],
            'Beta'      : [5.00,5.00,5.00,5.00,5.00,5.00,6.00,6.00,6.00,6.00,6.00,7.00,7.00,7.00,7.00,7.00,7.00,7.00,388.0,388.0,388.0,388.0,388.0,388.0,388.0,388.0,28.50,29.18,28.93,29.71,29.72,31.56,28.05,27.51,27.31,27.20,27.61,27.24,27.25,26.99,26.79,27.13,27.48,27.21],
            'Segment'   : 44*[''],
            'Element'   : ['N','C','C','O','C','O','N','C','C','O','C','N','C','C','O','C','C','C','N','C','C','O','C','C','C','O','N','C','C','O','C','O','N','C','C','O','C','N','C','C','O','C','C','C'],
        })
        cls.dfB = pd.DataFrame({
            'ATOM'      : 44*['ATOM'],
            'ANumber'   : [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,2991,2992,2993,2994,2995,2996,2997,2998,3000,3001,3002,3003,3004,3005,3006,3007,3008,3009,3010,3011,3012,3013,3014,3015,3016,3017],
            'AName'     : ['N','CA','C','O','CB','OG','N','CA','C','O','CB','N','CA','C','O','CB','CG','CD','N','CA','C','O','CB','CG1','CG2','OXT','N','CA','C','O','CB','OG','N','CA','C','O','CB','N','CA','C','O','CB','CG','CD'],
            'AltLoc'    : 44*[''],
            'ResName'   : ['SER','SER','SER','SER','SER','SER','ALA','ALA','ALA','ALA','ALA','PRO','PRO','PRO','PRO','PRO','PRO','PRO','VAL','VAL','VAL','VAL','VAL','VAL','VAL','VAL','SER','SER','SER','SER','SER','SER','ALA','ALA','ALA','ALA','ALA','PRO','PRO','PRO','PRO','PRO','PRO','PRO'],
            'Chain'     : 26*['A'] + 18 * ['B'],
            'ResNum'    : [5,5,5,5,5,5,6,6,6,6,6,7,7,7,7,7,7,7,388,388,388,388,388,388,388,388,5,5,5,5,5,5,6,6,6,6,6,7,7,7,7,7,7,7],
            'CodeResIns': 44*[''],
            'X'         : [-1.303,-0.405,-0.179,-0.215,0.932,1.515,0.062,0.292,1.549,2.571,0.390,1.491,0.370,-0.726,-1.684,1.063,2.186,2.684,6.920,7.601,8.690,8.484,6.628,5.574,5.964,9.773,1.654,0.739,1.329,1.116,-0.629,-1.553,2.060,2.746,3.941,4.617,3.209,4.238,3.634,2.407,1.910,4.762,5.508,5.495],
            'Y'         : [-24.821,-26.001,-26.358,-25.478,-25.731,-24.601,-27.651,-28.233,-27.675,-27.490,-29.758,-27.425,-27.671,-26.597,-26.704,-27.664,-26.716,-26.931,-47.432,-48.740,-48.824,-48.348,-49.971,-50.001,-50.038,-49.365,7.730,7.775,8.411,7.891,8.391,7.388,9.516,10.051,9.162,8.681,11.495,8.959,9.464,8.715,9.024,9.291,8.105,8.237],
            'Z'         : [-18.184,-18.023,-16.556,-15.685,-18.684,-18.092,-16.313,-14.980,-14.308,-14.981,-15.079,-12.971,-12.042,-12.045,-11.271,-10.684,-10.864,-12.252,14.539,14.599,13.542,12.419,14.458,15.592,13.050,13.792,6.721,5.542,4.262,3.170,5.905,6.354,4.363,3.184,2.841,3.750,3.428,1.540,0.288,-0.223,-1.296,-0.727,-0.226, 1.268],
            'Occupancy' : 44*[1.00],
            'Beta'      : [5.00,5.00,5.00,5.00,5.00,5.00,6.00,6.00,6.00,6.00,6.00,7.00,7.00,7.00,7.00,7.00,7.00,7.00,388.0,388.0,388.0,388.0,388.0,388.0,388.0,388.0,7.00,7.00,7.00,7.00,7.00,7.00,6.00,6.00,6.00,6.00,6.00,5.00,5.00,5.00,5.00,5.00,5.00,5.00],
            'Segment'   : 44*[''],
            'Element'   : ['N','C','C','O','C','O','N','C','C','O','C','N','C','C','O','C','C','C','N','C','C','O','C','C','C','O','N','C','C','O','C','O','N','C','C','O','C','N','C','C','O','C','C','C'],
        })
    #---
    #endregion --------------------------------------------------> Class Setup

    #region -------------------------------------------------> Expected Output
    def test_Init(self):
        """Test correct initialization"""
        #------------------------------>
        tInput = [
            (self.pdb.rChain.tolist(), ['A', 'B'], self.assertEqual,               'Chain'),
            # pylint: disable-next=protected-access
            (self.pdb.rDFAtom,         self.df,    pd._testing.assert_frame_equal, 'DF'),           # type: ignore
        ]
        #------------------------------>
        for a,b,c,d in tInput:
            msg = f"{d}"
            with self.subTest(msg):
                c(a,b)
    #---

    def test_GetSequence(self):
        """Test GetSequence"""
        #------------------------------>
        tInput = [
            ('A', 'SAPV'),
            ('B', 'SAP'),
        ]
        #------------------------------>
        for a,b in tInput:
            msg = "GetSequence"
            with self.subTest(msg):
                #------------------------------>
                result = self.pdb.GetSequence(a)
                #------------------------------>
                self.assertEqual(result, b)
    #---

    def test_GetResNum(self):
        """Test GetResNum"""
        #------------------------------>
        tInput = [
            ('A', [5,6,7,388]),
            ('B', [5,6,7]),
        ]
        #------------------------------>
        for a,b in tInput:
            msg = "GetResNum"
            with self.subTest(msg):
                #------------------------------>
                result = self.pdb.GetResNum(a)
                #------------------------------>
                self.assertEqual(result, b)
    #---

    def test_SetBeta(self):
        """Test SetBeta"""
        #------------------------------>
        tInput = [
            ('A', {5: 5.00, 6: 6.00, 7: 7.00, 388: 388.0}, self.dfA),
            ('B', {5: 7.00, 6: 6.00, 7: 5.00}, self.dfB),
        ]
        #------------------------------>
        for a,b,c in tInput:
            msg = "SetBeta"
            with self.subTest(msg):
                #------------------------------>
                self.pdb.SetBeta(a, b)
                # pylint: disable-next=protected-access
                pd._testing.assert_frame_equal(self.pdb.rDFAtom, c)             # type: ignore
                #------------------------------>

    #---
    #endregion ----------------------------------------------> Expected Output
#---
#endregion ------------------------------------------------------> Class Setup
