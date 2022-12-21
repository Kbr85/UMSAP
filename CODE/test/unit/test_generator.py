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


"""Tests for data.generator """


#region -------------------------------------------------------------> Imports
import unittest
from pathlib import Path

import data.generator as mGenerator
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------> File Location
folder = Path(__file__).parent / 'test_files'
fasta2Prot = folder / 'tarprot-seq-both.txt'
#endregion ----------------------------------------------------> File Location


#region ---------------------------------------------------------> Class Setup
class Test_FastaSequence(unittest.TestCase):
    """Test for data.generator.FastaSequence"""
    #region -----------------------------------------------------> Class Setup
    @classmethod
    def setUp(cls):                                                             # pylint: disable=arguments-differ
        """Create class instances"""
        cls.file    = fasta2Prot
        cls.header1 = '>sp|P31545|EFEB_ECOLI Recombinant'
        cls.seq1    = ('HHHHHHHHHHHHHHMKKTAIAIAVALAGFATVAQAASWSHPQFEKIEGRRDRG'
                      'QKTQSAPFFALPGVKDANDYFGSALLRVMMMMMMMHHHHHHHHHH')
        cls.header2 = '>sp|P31545|EFEB_ECOLI Native'
        cls.seq2    = ('MKKTAIAIAVALAGFATVAQAASWSHPQFEKIEGRRDRGQKTQSAPFFALPGV'
                       'KDANDYFGSALLRVM')
    #---
    #endregion --------------------------------------------------> Class Setup

    #region -------------------------------------------------> Expected Output
    def test_expected_output(self):
        """Test for expected output"""
        #------------------------------>
        gen = mGenerator.FastaSequence(self.file)
        #------------------------------>
        self.assertEqual(next(gen), (self.header1, self.seq1))
        self.assertEqual(next(gen), (self.header2, self.seq2))
    #---
    #endregion ----------------------------------------------> Expected Output
#---
#endregion ------------------------------------------------------> Class Setup
