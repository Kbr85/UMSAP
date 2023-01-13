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


"""Tests for core.generator """


#region -------------------------------------------------------------> Imports
import unittest
from pathlib import Path

from core import generator as cGenerator
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------> File Location
folder = Path(__file__).parent / 'files'
fileA  = folder / 'fasta-tarprot-seq-both.txt'
#endregion ----------------------------------------------------> File Location


#region ---------------------------------------------------------> Class Setup
class Test_FastaSequence(unittest.TestCase):
    """Test for core.generator.FastaSequence"""
    #region -----------------------------------------------------> Class Setup
    def setUp(self):
        """Create class instances"""
        self.file    = fileA
        self.header1 = '>sp|P31545|EFEB_ECOLI Recombinant'
        self.seq1    = ('HHHHHHHHHHHHHHMKKTAIAIAVALAGFATVAQAASWSHPQFEKIEGRRDRG'
                       'QKTQSAPFFALPGVKDANDYFGSALLRVMMMMMMMHHHHHHHHHH')
        self.header2 = '>sp|P31545|EFEB_ECOLI Native'
        self.seq2    = ('MKKTAIAIAVALAGFATVAQAASWSHPQFEKIEGRRDRGQKTQSAPFFALPGV'
                       'KDANDYFGSALLRVM')
    #---
    #endregion --------------------------------------------------> Class Setup

    #region -------------------------------------------------> Expected Output
    def test_expected_output(self):
        """Test for expected output"""
        #------------------------------>
        gen = cGenerator.FastaSequence(self.file)
        #------------------------------>
        self.assertEqual(next(gen), (self.header1, self.seq1))
        self.assertEqual(next(gen), (self.header2, self.seq2))
    #---
    #endregion ----------------------------------------------> Expected Output
#---
#endregion ------------------------------------------------------> Class Setup
