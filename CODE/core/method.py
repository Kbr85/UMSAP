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


"""Methods for the app"""


#region -------------------------------------------------------------> Imports
import itertools
import traceback
from dataclasses import dataclass, field
from datetime    import datetime
from operator    import itemgetter
from pathlib     import Path
from typing      import Literal, Union, Optional, Any, TYPE_CHECKING

import matplotlib as mpl
import numpy      as np
import pandas     as pd

import wx

from config.config import config as mConfig
from core import file as cFile

if TYPE_CHECKING:
    from core import window as cWindow
#endregion ----------------------------------------------------------> Imports


LIT_Comp       = Literal['lt', 'le', 'e', 'ge', 'gt']
LIT_CompEq     = Literal['e', 'ne']
LIT_NumType    = Literal['int', 'float']
LIT_IndSample  = Literal['i', 'p']
LIT_Region     = Literal['start', 'end']
LIT_Tran       = Literal['', 'None', 'Log2']
LIT_Norm       = Literal['', 'None', 'Median']
LIT_Imp        = Literal['', 'None', 'Normal Distribution']
LIT_Corr       = Literal['', 'Pearson', 'Kendall', 'Spearman']
LIT_CorrectedP = Literal['', 'None', 'Bonferroni', 'Sidak', 'Holm - Sidak',
                         'Holm', 'Simes - Hochberg', 'Hommel',
                         'Benjamini - Hochberg', 'Benjamini - Yekutieli']


#region -------------------------------------------------------------> Classes
@dataclass
class BaseUserData():
    """Base class for the representation of the user input data"""
    #region ---------------------------------------------------------> Options
    #------------------------------> Files & ID
    uFile:Path    = Path()                                                      # UMSAP File
    iFile:Path    = Path()                                                      # Data File
    seqFile:Path  = Path()                                                      # Sequence File
    ID:str        = ''                                                          # ID for Analysis
    iFileN:str    = ''                                                          # Name of Data File after copied to output folder
    seqFileN:str  = ''                                                          # Name of Sequence File after copied to output folder
    copyFile:dict = field(default_factory=lambda: {                             # Copy these files to result folders
        'iFile'  : 'iFileN',
        'seqFile': 'seqFileN',})
    seqFileObj:Optional['cFile.FastaFile'] = None                                 # Sequence File Object
    #------------------------------> Data Preparation
    cero:bool      = False                                                      # Treatment of 0 in data
    tran:LIT_Tran  = ''                                                         # Transformation method
    norm:LIT_Norm  = ''                                                         # Normalization method
    imp:LIT_Imp    = ''                                                         # Imputation Method
    shift:float    = float(mConfig.data.Shift)                                  # Center shift
    width:float    = float(mConfig.data.Width)                                  # Stdev value
    targetProt:str = ''                                                         # Target Protein
    scoreVal:float = 0                                                          # Minimum Score value
    #------------------------------> Statistic options
    rawInt:bool               = False                                           # Raw intensity or ration of intensity
    indSample:LIT_IndSample   = 'i'                                             # Samples are independent or not
    alpha:float               = 0                                               # Significance level
    beta:float                = 0                                               # Beta level
    gamma:float               = 0                                               # Chi squared test level
    thetaM:Optional[float]    = None                                            # Equivalence Test maximum possible difference
    theta:Optional[float]     = None                                            # Equivalence Test threshold. None implies calculate a value based on Control experiments
    correctedP:LIT_CorrectedP = ''                                              # Method to correct P values for multiple test
    #------------------------------> Result - Control
    labelA:list[str] = field(default_factory=list)
    labelB:list[str] = field(default_factory=list)
    ctrlType:str     = ''
    ctrlName:str     = ''
    #------------------------------> Correlation Analysis
    corr:LIT_Corr = ''                                                         # Correlation method
    #------------------------------> Further Analysis
    posAA:Optional[int]         = None                                          # Position number for AA analysis
    winHist:Optional[list[int]] = None                                          # Windows for Histograms
    #------------------------------> Column numbers in the original (oc) and short (df) dataframe
    resCtrl:str             = ''                                                # ResCtrl in str form
    ocSeq:int               = -1                                                # Search here for Peptides.
    ocTargetProt:int        = -1                                                # Search here for targetProt
    ocGene:int              = -1                                                # Search here for Gene names
    ocScore:int             = -1                                                # Search here for Score values
    ocExcludeR:list[int]    = field(default_factory=list)                       # Search here for values to exclude rows in data from analysis
    ocColumn:list[int]      = field(default_factory=list)                       # All columns that will be extracted from original data
    ocResCtrl:list          = field(default_factory=list)                       # ResCtrl column as nested list of int
    ocResCtrlFlat:list[int] = field(default_factory=list)                       # ResCtrl columns as flat list
    dfSeq:int               = -1                                                # Search here for Peptides.
    dfTargetProt:int        = -1                                                # Search here for targetProt
    dfGene:int              = -1                                                # Search here for Gene names
    dfScore:int             = -1                                                # Search here for Score values
    dfExcludeR:list[int]    = field(default_factory=list)                       # Search here for values to exclude rows in data from analysis
    dfColumnR:list[int]     = field(default_factory=list)                       # Columns in which 0 and/or '' will be replaced with NA
    dfColumnF:list[int]     = field(default_factory=list)                       # Columns with only Float values
    dfResCtrl:list          = field(default_factory=list)                       # ResCtrl columns as nested list of int
    dfResCtrlFlat:list[int] = field(default_factory=list)                       # ResCtrl columns as flat list
    dfNC:list[int]          = field(default_factory=lambda: [2,3])              # Location of N, C residue numbers in Recombinant Protein
    dfNCF:list[int]         = field(default_factory=lambda: [4,5])              # Location of N, C residue numbers in Native Protein
    #------------------------------>
    protLoc:tuple[int, int]    = (-1, -1)                                       # Location of the Native Sequence in the Recombinant Sequence
    protLength:tuple[int, int] = (1, 0)                                         # Length of Recombinant and Natural Protein
    protDelta:Optional[int]    = None                                           # To calculate Native residue number from Recombinant residue number
    converterRead:dict         = field(default_factory=lambda:{                 # Set proper type when reading from file
        'uFile'  : Path,
        'iFile'  : Path,
        'seqFile': Path,
    })
    converterPrint:dict     = field(default_factory=lambda:{                    # Set proper type when printing to file
        'uFile'  : str,
        'iFile'  : str,
        'seqFile': str,
    })
    dI:dict                 = field(default_factory=dict)                       # Keys are class attributes and values string for pretty print
    #------------------------------> Child class should give default values for the following attributes
    dO:list        = field(default_factory=list)                                # Attributes written to umsap file
    longestKey:int = 0                                                          # Length of the longest Key in dI
    #endregion ------------------------------------------------------> Options

    #region ---------------------------------------------------------> Methods
    def PrintDI(self) -> dict:
        """Creates the dictionary needed to pretty print the user input.

            Returns
            -------
            dict
        """
        #region --------------------------------------------------->
        dictO = {}
        #------------------------------>
        for k,v in self.dI.items():
            label = f"{v}{(self.longestKey - len(v))*' '}"
            val   = getattr(self, k)
            #------------------------------>
            if isinstance(val, (list, tuple)):
                val = ', '.join(map(str, val))
            #------------------------------>
            if k == 'indSample':
                val = PrintIndSample(val)
            #------------------------------>
            if k == 'method':
                val = PrintMethod(val)
            #------------------------------>
            dictO[label] = str(val)
        #endregion ------------------------------------------------>

        return dictO
    #---

    def PrintDO(self) -> dict:
        """Creates the dictionary needed to print the processed user input

            Return
            ------
            dict
        """
        #region -------------------------------------------------------->
        dictO = {}
        #------------------------------>
        for k in self.dO:
            if (conv := self.converterPrint.get(k)) is not None:
                dictO[k] = conv(getattr(self, k))
            else:
                dictO[k] = getattr(self, k)
        #endregion ----------------------------------------------------->

        return dictO
    #---

    def FromDict(self, data:dict) -> bool:
        """Update class attributes based on data

            Parameters
            ----------
            data: dict
                Keys are class attributes and values the corresponding values.

            Returns
            -------
            bool
        """
        #region --------------------------------------------------->
        for k,v in data.items():
            if (conv := self.converterRead.get(k)) is not None:
                setattr(self, k, conv(v))
            else:
                setattr(self, k, v)
        #endregion ------------------------------------------------>

        return True
    #---
    #endregion ------------------------------------------------------> Methods
#---


@dataclass
class BaseAnalysis():
    """Base class to hold information about an analysis in an UMSAP file."""
    #region --------------------------------------------------->
    error:list[str] = field(default_factory=list)                               # List of analysis with errors.
    date:list[str]  = field(default_factory=list)                               # List of analysis with no error.
    #endregion ------------------------------------------------>
#---


@dataclass
class LabelDetail():
    """Details about each protein fragment for the given experimental label.

        Attributes
        ----------
        coord : [(x1, x2),...., (xN, xM)]
            First and last residue number of the fragment in Recombinant Protein
            sequence.
        coordN: [(x1, x2),.(NaN, NaN)..., (xN, xM)]
            First and last residue number of the fragment in Native Protein
            sequence.
        seq   : [Aligned Seq1, ...., Aligned SeqN]
            Sequence alignment within the fragment as a str.
        seqL  : [Flat List with Seqs1, ...., Flat List with SeqsN]
            Flat list of peptide sequences withing the fragment.
        np    : [Number of peptides1, ...., NpN]
            Number of peptides in each fragment.
        npNat : [Number of native peptides1, ...., NpNatN]
            Number of native peptides in each fragment.
        nc    : [Number of cleavages1, ...., NcN]
            Number of unique cleavages in each fragment.
        ncNat : [Number of native cleavages1, ....., NcNatN]
            Number of unique cleavages in each fragment for the Native sequence.
        nFrag : (Number of fragments, Number of fragments Nat)
            Total number of fragments for the experiment in the Recombinant and
            Native sequence.
        ncT   : (Number of cleavages for the Exp as a whole, Nat),
            Total number of cleavages for the experiment in the Recombinant and
            Native sequence.

        Notes
        -----
        - All list have the same length.
        - nFrag and nCT are tuples with two values each.
    """
    #region ---------------------------------------------------------> Options
    coord:list[tuple[int,int]]                        = field(default_factory=list)
    coordN:list[tuple[Union[int,Any],Union[int,Any]]] = field(default_factory=list)
    seq:list[str]                                     = field(default_factory=list)
    seqL:list[list[str]]                              = field(default_factory=list)
    np:list[int]                                      = field(default_factory=list)
    npNat:list[int]                                   = field(default_factory=list)
    nc:list[int]                                      = field(default_factory=list)
    ncNat:list[int]                                   = field(default_factory=list)
    nFrag:tuple[int,int]                              = (0,0)
    nCT:tuple[int,int]                                = (0,0)
    #endregion ------------------------------------------------------> Options
#---


@dataclass
class Fragment():
    """Information about protein fragments.

        Notes
        -----
        For each label there will be an attribute with an instance of
        LabelDetail as value.
    """
    #region ---------------------------------------------------------> Options
    label:list[str] = field(default_factory=list)                               # List of labels
    #endregion ------------------------------------------------------> Options

    #region ---------------------------------------------------> Class Methods
    def NumEmptyFrag(self) -> int:
        """Get the total number of empty frag.

            Return
            ------
            int
        """
        #region -------------------------------------------------------->
        total = 0
        #------------------------------>
        for k in self.label:
            frag = getattr(self, k)
            #------------------------------>
            if not frag.coord:
                total += 1
        #endregion ----------------------------------------------------->

        return total
    #---
    #endregion ------------------------------------------------> Class Methods
#---
#endregion ----------------------------------------------------------> Classes


#region ------------------------------------------------------> String Methods
def StrNow(dtFormat:str=mConfig.core.dtFormat) -> str:
    """Get a formatted datetime.now() string.

        Parameters
        ----------
        dtFormat: str
            Format specification.

        Returns
        -------
        str:
            The now date time as 20210112-140137.

        Example
        -------
        >>> StrNow()
        >>> '20210112-140137'
    """
    # No test
    return datetime.now().strftime(dtFormat)
#---


def StrException(
    tException: Exception,
    tStr:bool  = True,
    tRepr:bool = True,
    trace:bool = True
    ) -> str:
    """Get a string to print information about tException.

        Parameters
        ----------
        tException: Exception
            Exception to print.
        tStr: boolean
            Include error message as return by str(tException). Default is True.
        tRepr: boolean
            Include error message as return by repr(tException).
            Default is True.
        trace: boolean
            Include the traceback. Default is True.

        Returns
        -------
        str
            Error message
    """
    # No test
    #region -------------------------------------------------------> Variables
    msg = ''
    #endregion ----------------------------------------------------> Variables

    #region ---------------------------------------------------------> Message
    #------------------------------> str(e)
    if tStr:
        msg = f"{msg}{str(tException)}\n\n"
    #------------------------------> repr(e)
    if tRepr:
        msg = f"{msg}{repr(tException)}\n\n"
    #------------------------------> traceback
    if trace:
        tTrace = "".join(
            traceback.format_exception(
                type(tException),
                tException,
                tException.__traceback__,
            )
        )
        msg = f"{msg}{tTrace}"
    #endregion ------------------------------------------------------> Message

    return msg
#---


def Str2ListNumber(
    tStr:str,
    numType:LIT_NumType = 'int',
    sep:str             = ',',
    unique:bool         = False
    ) -> Union[list[int], list[float]]:
    """Turn a string into a list of numbers. Ranges are expanded as integers.

        Parameters
        ----------
        tStr: str
            The string containing the numbers and/or range of numbers (4-8)
        numType: str
            One of int, float
        sep: str
            The character to separate numbers in the string
        unique: boolean
            Return only unique values. Order is kept. Default is False.

        Returns
        -------
        list of numbers.

        Examples
        --------
        >>> Str2ListNumber('1, 2, 3, 6-10,  4  ,  5, 6  , 7', sep=',')
        >>> [1, 2, 3, 6, 7, 8, 9, 10, 4, 5, 6, 7]
        >>> Str2ListNumber('1, 2, 3, 6-10,  4  ,  5, 6  , 7', sep=',', unique=True)
        >>> [1, 2, 3, 6, 7, 8, 9, 10, 4, 5]
    """
    # Test in test.unit.core.test_method.Test_Str2ListNumber
    #region -------------------------------------------------------> Variables
    lN = []
    values = tStr.strip().split(sep)
    #endregion ----------------------------------------------------> Variables

    #region -----------------------------------------------------> Get numbers
    for k in values:
        if k.strip() != '':
            #------------------------------> Expand ranges
            lK = ExpandRange(k, numType)
            #------------------------------> Get list of numbers
            lN = lN + lK
    #endregion --------------------------------------------------> Get numbers

    #region ----------------------------------------------------------> Unique
    if unique:
        lo = list(dict.fromkeys(lN))
    else:
        lo = lN
    #endregion -------------------------------------------------------> Unique

    return lo
#---


def StrSetMessage(start:str, end:str, link:str='\n\nFurther details:\n') -> str:
    """Creates a message by concatenating start and end with link.

        Parameters
        ----------
        start: str
            Start of the message.
        end: str
            End of the message.
        link: str
            Link between start and end.

        Returns
        -------
        str:
            Full message

        Examples
        --------
        >>> StrSetMessage('Start', 'End', link=' - ')
        >>> 'Start - End'
    """
    # No test
    if link:
        return f"{start}{link}{end}"
    #------------------------------>
    return f"{start} {end}"
#---


def StrEqualLength(
    strL:list[str],
    char:str       = ' ',
    loc:LIT_Region = 'end',
    ) -> list[str]:
    """Return a list in which every string element has the same length.

        Parameters
        ----------
        strL: list[str]
            String with different length.
        char: str
            Fill character. Default is empty space ' '.
        loc: str
            Add filling character to start or end of the strings.

        Returns
        -------
        list[str]
            String with the same length with the same original order.

        Notes
        -----
        Filling characters are added at the end or start of each str.
    """
    # Test in test.unit.core.test_method.Test_StrEqualLength
    #region ---------------------------------------------------> Variables
    long = len(max(strL, key=len))
    lOut = []
    #endregion ------------------------------------------------> Variables

    #region ---------------------------------------------------> Fill lOut
    if loc == 'end':
        for x in strL:
            space = (long-len(x))*char
            lOut.append(f'{x}{space}')
    elif loc == 'start':
        for x in strL:
            space = (long-len(x))*char
            lOut.append(f'{space}{x}')
    else:
        msg = mConfig.core.mNotImplementedFull.format(
            loc, 'loc', LIT_Region)
        raise ValueError(msg)
    #endregion ------------------------------------------------> Fill lOut

    return lOut
#---


def ResControl2ListNumber(                                                      # pylint: disable=dangerous-default-value
    val:str,
    sep:list[str]       = [' ', ',', ';'],
    numType:LIT_NumType = 'int',
    ) -> list[list[list[int]]]:
    """Return a list from a Result - Control string.

        Parameters
        ----------
        val: str
            String with the numbers. e.g. '0-4 6, 7 8 9; 10 13-15, ""; ...'.
        sep: list of str
            Separators used in the string e.g. [' ', ',', ';'].
        numType: str
            To convert to numbers.

        Returns
        -------
        list of list of list of str
        [[[0 1 2 3 4], [7 8 9]], [[10 13 14 15], []], ...]

        Examples
        --------
        >>> ResControl2ListNumber(
            '0 1 2, 3 4 5; 6 7 8, 9 10 11', sep=[' ', ',', ';'], numType='int')
        >>> [[[0,1,2], [3,4,5]], [[6,7,8], [9,10,11]]]
    """
    # Test in test.unit.core.test_method.Test_ResControl2ListNumber
    #region -------------------------------------------------------> Variables
    l = []
    #endregion ----------------------------------------------------> Variables

    #region -------------------------------------------------------> Form list
    for k in val.split(sep[2]):
        #------------------------------>
        lRow = []
        #------------------------------>
        for j in k.split(sep[1]):
            colVal = Str2ListNumber(j, numType=numType, sep=sep[0])
            lRow.append(colVal)
        #------------------------------>
        l.append(lRow)
    #endregion ----------------------------------------------------> Form list

    return l
#---


def ResControl2Flat(val:list[list[list[int]]]) -> list[int]:
    """Result - Control list as a flat list.

        Parameters
        ----------
        val: list of list of list of int
            Result - Control as a list of list of list of int.

        Returns
        -------
        list of int
            Flat Result - Control list

        Examples
        --------
        >>> ResControl2Flat([[[0,1,2], [3,4,5]], [[6,7,8], [9,10,11]]])
        >>> [0,1,2,3,4,5,6,7,8,9,10,11])
    """
    # Test in test.unit.core.test_method.Test_ResControl2Flat
    return list(itertools.chain(*(itertools.chain(*val))))
#---


def ResControl2DF(
    val:list[list[list[int]]],
    start:int,
    ) -> list[list[list[int]]]:
    """Convert the Result - Control column numbers in the original file to the
        column numbers of the initial dataframe used in the analysis.

        Parameters
        ----------
        val: list of list of list of int
            Result - Control as a list of list of list of int
        start: int
            Column index start of the Result - Control columns in the initial
            dataframe

        Returns
        -------
        list[list[list[int]]]
            The list has the same order as the input val but the column index
            are adjusted.

        Notes
        -----
        It is assumed columns in the DF have the same order as in val.
        Empty list are possible to mimic empty conditions in an experiment.

        Examples
        --------
        >>> ResControl2DF([[[0,1,2], []], [[6,7,8], []]], 1)
        >>> [[[1,2,3],[]], [[4,5,6],[]]]
    """
    # Test in test.unit.core.test_method.Test_ResControl2DF
    #region -------------------------------------------------------> Variables
    idx  = start
    outL = []
    #endregion ----------------------------------------------------> Variables

    #region --------------------------------------------------> Adjust col idx
    for row in val:
        outR = []
        #------------------------------>
        for col in row:
            outC = []
            #------------------------------>
            for _ in col:
                outC.append(idx)
                idx += 1
            #------------------------------>
            outR.append(outC)
        #------------------------------>
        outL.append(outR)
    #endregion -----------------------------------------------> Adjust col idx

    return outL
#---
#endregion ---------------------------------------------------> String Methods


#region ------------------------------------------------------> Number methods
def ExpandRange(
    r:str,
    numType:LIT_NumType = 'int',
    ) -> Union[list[int], list[float]]:
    """Expand a range of numbers: '4-7' --> [4,5,6,7]. Only positive integers
        are supported.

        Parameters
        ----------
        r: str
            String containing the range.
        numType: str
            One of 'int', 'float'. For the case where r is not a range.

        Returns
        -------
        list of int

        Notes
        -----
        Ranges are interpreted as closed ranges.

        Examples
        --------
        >>> ExpandRange('0-15', 'int')
        >>> [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        >>> ExpandRange('-5.4', 'float')
        >>> [-5.4]
    """
    # Test in test.unit.core.test_method.Test_ExpandRange
    #region -------------------------------------------------> Expand & Return
    tr = r.strip()
    #------------------------------> Expand
    if '-' in tr:
        #------------------------------> Catch more than one - in range by raising ValueError
        a,b = tr.split('-')
        #------------------------------> Negative value
        if a == '':
            return [mConfig.core.oNumType[numType](tr)]
        #------------------------------> Range like 4-
        if b == '':
            raise ValueError(mConfig.core.mRangeNumIE.format(r))
        #------------------------------> Expand range
        a = int(a)
        b = int(b)
        if a < b:
            return list(range(a, b+1, 1))
        #------------------------------> Bad Input
        raise ValueError(mConfig.core.mRangeNumIE.format(r))
    #------------------------------> Positive number
    return [mConfig.core.oNumType[numType](tr)]
    #endregion ----------------------------------------------> Expand & Return
#---
#endregion ---------------------------------------------------> Number methods


#region --------------------------------------------------------> pd.DataFrame
def DFFilterByColS(
    df:pd.DataFrame,
    col:int,
    refStr:str,
    comp:LIT_CompEq,
    ) -> 'pd.DataFrame':
    """Filter rows in the pd.DataFrame based on the string values present in
        col.

        Parameters
        ----------
        df: pd.DataFrame
        col: int
            The column index used to filter rows.
        refStr: string
            Reference string.
        comp: str
            Numeric comparison to use in the filter. One of: 'e', 'ne.

        Returns
        -------
        pd.DataFrame

        Notes
        -----
        - Rows with values in col that do not comply with c[x] comp refStr are
        discarded, e.g. c[x] == 'refString'
        - Assumes all values in col are strings.
    """
    # Test in test.unit.core.test_method.Test_DFFilterByColS
    #region ----------------------------------------------------------> Filter
    #------------------------------>  Copy
    dfo = df.copy()
    #------------------------------> Filter
    if comp == 'e':
        dfo = dfo.loc[dfo.iloc[:,col] == refStr]
    elif comp == 'ne':
        dfo = dfo.loc[dfo.iloc[:,col] != refStr]
    else:
        msg = mConfig.core.mNotImplementedFull.format(
            comp, 'comp', LIT_CompEq)
        raise ValueError(msg)
    #endregion -------------------------------------------------------> Filter

    return dfo
#---


def DFExclude(df:pd.DataFrame, col:list[int]) -> 'pd.DataFrame':
    """Exclude rows in the pd.DataFrame based on the values present in col.

        Parameters
        ----------
        df: pd.DataFrame
            DataFrame with the data.
        col: list[int]
            Column numbers to look for rows to exclude.

        Returns
        -------
        pd.DataFrame

        Notes
        -----
        Rows with at least one value other than NA in the given columns are
        discarded.
    """
    # Test in test.unit.core.test_method.Test_DFExclude
    #region ----------------------------------------------------------> Exclude
    #------------------------------>  Copy
    dfo = df.copy()
    #------------------------------> Exclude
    a = dfo.iloc[:,col].notna()
    a = a.loc[(a==True).any(axis=1)]                                            # pylint: disable=singleton-comparison
    idx = a.index
    dfo = dfo.drop(index=idx)                                                   # type: ignore
    #endregion -------------------------------------------------------> Exclude

    return dfo
#---


def DFFilterByColN(
    df:pd.DataFrame,
    col:list[int],
    refVal:float,
    comp:LIT_Comp,
    ) -> pd.DataFrame:
    """Filter rows in the pd.DataFrame based on the numeric values present in
        col.

        Parameters
        ----------
        df: pd.DataFrame
            DataFrame with the data.
        col: list of int
            The column indexes used to filter rows.
        refVal: float
            Reference value.
        comp: str
            Numeric comparison to use in the filter. One of:
            'lt', 'le', 'e', 'ge', 'gt'

        Returns
        -------
        pd.DataFrame

        Notes
        -----
        Rows with values in col that do not comply with c[x] comp refVal are
        discarded, e.g. c[x] > 3,45

        Assumes all values in col are numbers.
    """
    # Test in test.unit.core.test_method.Test_DFFilterByColN
    #region ----------------------------------------------------------> Filter
    #------------------------------>  Copy
    dfo = df.copy()
    #------------------------------> Filter
    if comp == 'lt':
        dfo = dfo.loc[(dfo.iloc[:,col] < refVal).any(axis=1)]                     # type: ignore
    elif comp == 'le':
        dfo = dfo.loc[(dfo.iloc[:,col] <= refVal).any(axis=1)]                    # type: ignore
    elif comp == 'e':
        dfo = dfo.loc[(dfo.iloc[:,col] == refVal).any(axis=1)]                    # type: ignore
    elif comp == 'ge':
        dfo = dfo.loc[(dfo.iloc[:,col] >= refVal).any(axis=1)]                    # type: ignore
    elif comp == 'gt':
        dfo = dfo.loc[(dfo.iloc[:,col] > refVal).any(axis=1)]                     # type: ignore
    else:
        msg = mConfig.core.mNotImplementedFull.format(comp, 'comp', LIT_Comp)
        raise ValueError(msg)
    #endregion -------------------------------------------------------> Filter

    return dfo
#---


def DFReplace(                                                                  # pylint: disable=dangerous-default-value
    df:Union[pd.DataFrame, pd.Series],
    oriVal:list,
    repVal:Union[list, tuple, str, float, int],
    sel:list[int] = [],
    ) -> Union[pd.DataFrame, pd.Series]:
    """Replace values in the dataframe.

        Parameters
        ----------
        df: pd.DataFrame or pd.Series
            Dataframe with the data.
        oriVal: list
            List of values to search and replace.
        repVal: list or single value
            List of values to use as replacement. When only one value is given
            all oriVal are replace with the given value.
        sel: list of int
            Column indexes.

        Returns
        -------
        pd.DataFrame or pd.Series
            With replaced values

        Raise
        -----
        ValueError:
            - When selection is not found in df
            - When oriVal and repVal have different length
        RuntimeError :
            - When the replacement procedure does not finish correctly

        Notes
        -----
        Column selection in the df is done by column number.
    """
    # Test in test.unit.core.test_method.Test_DFReplace
    #region ---------------------------------------------------------> Replace
    #------------------------------> Copy
    dfo = df.copy()
    #------------------------------> Replace
    if sel:
        dfo.iloc[:,sel] = dfo.iloc[:,sel].replace(oriVal, repVal)               # type: ignore
    else:
        dfo = dfo.replace(oriVal, repVal)                                       # type: ignore
    #endregion ------------------------------------------------------> Replace

    return dfo
#---
#endregion -----------------------------------------------------> pd.DataFrame


#region ---------------------------------------------------------> GUI Methods
def GetDisplayInfo(win:'cWindow.BaseWindow') -> dict[str, dict[str, int]]:
    """This will get the information needed to set the position of a window.
        Should be called after Fitting sizers for accurate window size
        information.

        Parameters
        ----------
        win: wx.Frame
            Window to be positioned

        Returns
        -------
        dict
            {
                'D' : {'xo':X, 'yo':Y, 'w':W, 'h':h}, Info about display
                'W' : {'N': N, 'w':W, 'h', H},        Info about win
            }
    """
    # No test
    #region ----------------------------------------------------> Display info
    xd, yd, wd, hd =  wx.Display(win).GetClientArea()
    #endregion -------------------------------------------------> Display info

    #region -----------------------------------------------------> Window info
    nw = mConfig.core.winNumber.get(win.cName, 0)
    ww, hw = win.GetSize()
    #endregion --------------------------------------------------> Window info

    #region ------------------------------------------------------------> Dict
    data = {
        'D' : {
            'xo' : xd,
            'yo' : yd,
            'w'  : wd,
            'h'  : hd,
        },
        'W' : {
            'N' : nw,
            'w' : ww,
            'h' : hw,
        },
    }
    #endregion ---------------------------------------------------------> Dict

    return data
#---


def LCtrlFillColNames(lc:wx.ListCtrl, fileP:Union[Path, str]) -> bool:
    """Fill the wx.ListCtrl with the name of the columns in fileP.

        Parameters
        ----------
        lc: wx.ListCtrl
            wx.ListCtrl to fill info into.
        fileP: Path
            Path to the file from which to read the column names.

        Notes
        -----
        This will delete the wx.ListCtrl before adding the new names.
        wx.ListCtrl is assumed to have at least two columns [#, Name,]
    """
    # No test
    #region -------------------------------------------------------> Read file
    colNames = cFile.ReadFileFirstLine(fileP)
    #endregion ----------------------------------------------------> Read file

    #region -------------------------------------------------------> Fill List
    lc.DeleteAllItems()
    #------------------------------> Fill
    for k, v in enumerate(colNames):
        index = lc.InsertItem(k, " " + str(k))
        lc.SetItem(index, 1, v)
    #endregion ----------------------------------------------------> Fill List

    return True
#---
#endregion ------------------------------------------------------> GUI Methods


#region --------------------------------------------------------------> Others
def PrintIndSample(val:LIT_IndSample) -> str:
    """Pretty Print Independent Sample choice to UMSAP File.

        Parameters
        ----------
        val: str
            One of the 'i' or 'p'.

        Returns
        -------
        str
            Value to print in the UMSAP File
    """
    #region -------------------------------------------------------->
    try:
        valO = mConfig.core.oSamplesP[val]
    except KeyError:
        valO = ''
    #endregion ----------------------------------------------------->

    return valO
#---


def PrintMethod(val) -> str:
    """Pretty Print Method choice to UMSAP File.

        Parameters
        ----------
        val: str
            One of the 'slope' or 'ttest'.

        Returns
        -------
        str
            Value to print in the UMSAP File
    """
    #region -------------------------------------------------------->
    try:
        valO = mConfig.tarp.oMethodP[val]
    except KeyError:
        valO = ''
    #endregion ----------------------------------------------------->

    return valO
#---


def NCResNumbers(
    dfR:pd.DataFrame,
    rDO:BaseUserData,
    seqNat:bool = True
    ) -> tuple[pd.DataFrame, str, Optional[Exception]]:
    """Find the residue numbers for the peptides in the sequence of the
        Recombinant and Native protein.

        Parameters
        ----------
        dfR: pd.DataFrame
            DataFrame with the data.
        rDO: BaseUserData
            Dataclass with user input.
        rSeqFileObj: cFile.FastaFile
            Fasta file object with the protein sequence.
        seqNat: bool
            Calculate N and C residue numbers also for the Native protein.

        Returns
        -------
        bool
    """
    # Test in test.unit.core.test_method.Test_NCResNumbers
    #region --------------------------------------------> Helper Functions
    def _ncTerm(
        row:list[str],
        seqObj:cFile.FastaFile,
        seqType:str,
        ) -> tuple[int, int]:
        """Get the N and C terminal residue numbers for a given peptide.

            Parameters
            ----------
            row: list[str]
                List with two elements. The Sequence is in index 0.
            seqObj: mFile.FastaFile
                Object with the protein sequence and the method to search
                the peptide sequence.
            seqType: str
                For the error message.
            Returns
            -------
            (Nterm, Cterm)
        """
        #region -----------------------------------------------> Find pept
        nc = seqObj.FindSeq(row[0])
        #endregion --------------------------------------------> Find pept

        #region ------------------------------------------------> Check ok
        if nc[0] != -1:
            return nc
        #------------------------------>
        msg = mConfig.core.mSeqPeptNotFound.format(row[0], seqType)
        raise RuntimeError(msg)
        #endregion ---------------------------------------------> Check ok
    #---
    #endregion -----------------------------------------> Helper Functions

    #region -----------------------------------------------------> Rec Seq
    try:
        dfR.iloc[:,rDO.dfNC] = dfR.iloc[
            :,[rDO.dfSeq, 1]].apply(
                _ncTerm,                                                        # type: ignore
                axis        = 1,
                raw         = True,
                result_type = 'expand',                                         # type: ignore
                args        = (rDO.seqFileObj, 'Recombinant'),
            )
    except RuntimeError as e:
        return (pd.DataFrame(), str(e), e)
    except Exception as e:
        return (pd.DataFrame(), mConfig.core.mUnexpectedError, e)
    #endregion --------------------------------------------------> Rec Seq

    #region -----------------------------------------------------> Nat Seq
    #------------------------------>
    if seqNat and rDO.seqFileObj.rSeqNat:
        #------------------------------>
        delta   = rDO.seqFileObj.GetSelfDelta()
        protLoc = rDO.seqFileObj.GetNatProtLoc()
        #------------------------------>
        a = dfR.iloc[:,rDO.dfNC] + delta
        dfR.iloc[:,rDO.dfNCF] = a
        #------------------------------> Remove Numbers not in the Native Protein
        m = ((dfR.iloc[:,rDO.dfNC] >= protLoc[0]) &
            (dfR.iloc[:,rDO.dfNC] <= protLoc[1])).to_numpy()
        a = dfR.iloc[:,rDO.dfNCF].where(m, np.nan)
        a = a.astype('Int64')
        dfR.iloc[:,rDO.dfNCF] = a
    #endregion --------------------------------------------------> Nat Seq

    return (dfR, '', None)
#---


def MatplotLibCmap(
    N:int                                      = 128,
    c1:tuple[int, int, int]                    = (255, 0, 0),
    c2:tuple[int, int, int]                    = (255, 255, 255),
    c3:tuple[int, int, int]                    = (0, 0, 255),
    bad:Union[tuple[float, float, float], str] = '',
    ):
    """Generate custom matplotlib cmap c1->c2->c3.

        Parameters
        ----------
        c1: list of int
            Color for lowest value. Default is red [255, 0, 0]
        c2: list of int
            Color for the middle value. Default is white [255, 255, 255]
        c3: list of int
            Color of the biggest value. Default is blue [0, 0, 255]
        bad: list of int, list of float, str or None
            Color for bad values. Default is None.

        Return
        ------
        Matplotlib color map.
    """
    # No test
    #region ----------------------------------------------------------> Colors
    #------------------------------>  c1 -> c2
    try:
        vals1 = np.ones((N, 4))
        vals1[:, 0] = np.linspace(c1[0]/255, c2[0]/255, N)
        vals1[:, 1] = np.linspace(c1[1]/255, c2[1]/255, N)
        vals1[:, 2] = np.linspace(c1[2]/255, c2[2]/255, N)
    except Exception as e:
        raise ValueError(str(e)) from e
    #------------------------------>  c2 -> c3
    try:
        vals2 = np.ones((N, 4))
        vals2[:, 0] = np.linspace(c2[0]/255, c3[0]/255, N)
        vals2[:, 1] = np.linspace(c2[1]/255, c3[1]/255, N)
        vals2[:, 2] = np.linspace(c2[2]/255, c3[2]/255, N)
    except Exception as e:
        raise ValueError(str(e)) from e
    #endregion -------------------------------------------------------> Colors

    #region ------------------------------------------------------------> CMAP
    #------------------------------>
    vals   = np.vstack((vals1, vals2))
    newMap = mpl.colors.ListedColormap(vals)                                    # type: ignore
    #------------------------------>
    if bad is not None:
        newMap.set_bad(color=bad)
    #endregion ---------------------------------------------------------> CMAP

    return newMap
#---


def Fragments(
    df:'pd.DataFrame',
    val:float,
    comp:LIT_Comp,
    protL:int,
    protLoc:tuple[int,int],
    ) -> Fragment:
    """Creates the dict holding the fragments identified in the analysis.

        Parameters
        ----------
        df: pd.DataFrame with the data from the analysis. The columns in df are
            expected to be:
            Seq Nrec Crec Nnat Cnat Exp1 Exp2 ...... ExpN
            Seq Nrec Crec Nnat Cnat    P    P           P
        val: float
            Threshold value to filter df and identify relevant peptides
        comp: str
            One of 'lt', 'le', 'e', 'ge', 'gt'
        protL: int
            Length of recombinant protein.
        protLoc: tuple[int, int]
            Location of the native protein in the recombinant sequence

        Returns
        -------
        Fragment instance.
    """
    # Test in test.unit.core.test_method.Test_Fragments
    #region -------------------------------------------------------> Variables
    fragment = Fragment()
    #endregion ----------------------------------------------------> Variables

    #region --------------------------------------------------->
    for c in range(5, df.shape[1]):
        colK = '-'.join(map(str, df.columns.values[c]))
        fragment.label.append(colK)
        labelDetail = LabelDetail()
        #------------------------------> Filter df
        dfE = DFFilterByColN(df, [c], val, comp)
        #------------------------------> Total cleavages for the experiment
        nctL    = []
        nctLNat = []
        #------------------------------> First row
        if dfE.shape[0] > 0:
            #------------------------------> Values from dfE
            seq    = dfE.iat[0,0]
            n      = dfE.iat[0,1]
            c      = dfE.iat[0,2]
            nf     = dfE.iat[0,3]
            cf     = dfE.iat[0,4]
            ncL    = []
            ncLNat = []
            #------------------------------>
            seqL = [seq]
            #------------------------------> Number of peptides
            nP = 1
            if pd.isna(nf) and pd.isna(cf):
                npNat = 0
            else:
                npNat = 1
            #------------------------------> Cleavages Rec
            if n != 1:
                ncL.append(n-1)
                nctL.append(n-1)
            if c != protL:
                ncL.append(c)
                nctL.append(c)
            #------------------------------> Cleavages Nat
            if not pd.isna(nf):
                if nf != 1:
                    ncLNat.append(nf-1)
                    nctLNat.append(nf-1)
            if not pd.isna(cf):
                if cf != protL != protLoc[1]:
                    ncLNat.append(cf)
                    nctLNat.append(cf)
        else:
            setattr(fragment, colK, labelDetail)
            continue
        #------------------------------> Other rows
        for r in range(1, dfE.shape[0]):
            #------------------------------> Values from dfE
            seqC = dfE.iat[r,0]
            nc   = dfE.iat[r,1]
            cc   = dfE.iat[r,2]
            ncf  = dfE.iat[r,3]
            ccf  = dfE.iat[r,4]
            if nc <= c:
                #------------------------------>
                seq = f'{seq}\n{(nc-n)*" "}{seqC}'
                seqL.append(seqC)
                #------------------------------> Number of peptides
                nP = nP + 1
                if not pd.isna(ncf) and not pd.isna(ccf):
                    npNat = npNat + 1
                #------------------------------> Cleavages Rec
                if nc != 1:
                    ncL.append(nc-1)
                    nctL.append(nc-1)
                if cc != protL:
                    ncL.append(cc)
                    nctL.append(cc)
                #------------------------------> Cleavages Nat
                if not pd.isna(ncf):
                    if ncf != 1:
                        ncLNat.append(nc-1)
                        nctLNat.append(nc-1)
                if not pd.isna(ccf):
                    if ccf != protL != protLoc[1]:
                        ncLNat.append(ccf)
                        nctLNat.append(ccf)
                #------------------------------> Update c residue
                if cc > c:
                    c = cc
                    cf = ccf
            else:
                #------------------------------> Add Fragment
                labelDetail.coord.append((n,c))
                labelDetail.coordN.append((nf,cf))
                labelDetail.seq.append(seq)
                labelDetail.seqL.append(seqL)
                labelDetail.np.append(nP)
                labelDetail.npNat.append(npNat)
                labelDetail.nc.append(len(set(ncL)))
                labelDetail.ncNat.append(len(set(ncLNat)))
                #------------------------------> Start new Fragment
                seq    = seqC
                n      = nc
                c      = cc
                nf     = ncf
                cf     = ccf
                ncL    = []
                ncLNat = []
                #------------------------------>
                seqL = [seqC]
                #------------------------------> Number of peptides
                nP   = 1
                if pd.isna(nf) and pd.isna(cf):
                    npNat = 0
                else:
                    npNat = 1
                #------------------------------> Cleavages Rec
                if n != 1:
                    ncL.append(n-1)
                    nctL.append(n-1)
                if c != protL:
                    ncL.append(c)
                    nctL.append(c)
                #------------------------------> Cleavages Nat
                if not pd.isna(nf):
                    if nf != 1:
                        ncLNat.append(nf-1)
                        nctLNat.append(nf-1)
                if not pd.isna(cf):
                    if cf != protL != protLoc[1]:
                        ncLNat.append(cf)
                        nctLNat.append(cf)
        #------------------------------> Catch the last line
        labelDetail.coord.append((n,c))
        labelDetail.coordN.append((nf,cf))
        labelDetail.seq.append(seq)
        labelDetail.seqL.append(seqL)
        labelDetail.np.append(nP)
        labelDetail.npNat.append(npNat)
        labelDetail.nc.append(len(set(ncL)))
        labelDetail.ncNat.append(len(set(ncLNat)))
        #------------------------------>
        labelDetail.nCT = (len(set(nctL)), len(set(nctLNat)))
        #------------------------------>
        nFragN = [x for x in labelDetail.coordN if not pd.isna(x[0]) or not pd.isna(x[1])]
        labelDetail.nFrag = (len(labelDetail.coord), len(nFragN))
        #------------------------------>
        setattr(fragment, colK, labelDetail)
    #endregion ------------------------------------------------>

    return fragment
#---


def Rec2NatCoord(
    coord:list[tuple[int,int]],
    protLoc:tuple[int,int],
    delta:Optional[int],
    ) -> Union[list[tuple[int,int]], list[str]]:
    """Translate residue numbers from the recombinant sequence to the native
        sequence.

        Parameters
        ----------
        coord: list of tuples(int, int)
            Residue numbers in the recombinant sequence.
        protLoc: tuple(int, int)
            Location of the native protein in the recombinant sequence.
        delta: int or None
            Difference in residue numbers.

        Returns
        -------
        list of tuples(int. int)
            Residue number in the native sequence.

        Notes
        -----
        Returns ['NA'] if delta is None or any of the protLoc items is None.

        Examples
        --------
        >>> Rec2NatCoord([(1,42), (38, 50), (201, 211), (247, 263)], (10, 300)), 10)
        >>> [(48, 60), (211, 221), (257, 273)]
        >>> Rec2NatCoord([(1,42), (38, 50), (201, 211), (247, 263)], (100, 230)), 10)
        >>> [(211, 221)]
    """
    # Test in test.unit.core.test_method.Test_Rec2NatCoord
    #region ---------------------------------------------------> Return NA
    if delta is None or protLoc[0] is None or protLoc[1] is None:
        return ['NA']
    #endregion ------------------------------------------------> Return NA

    #region ---------------------------------------------------> Calc
    listO = []
    for a,b in coord:
        if protLoc[0] <= a <= protLoc[1] and protLoc[0] <= b <= protLoc[1]:
            listO.append((a+delta, b+delta))
    #endregion ------------------------------------------------> Calc

    return listO
#---


def MergeOverlappingFragments(
    coord:list[tuple[int, int]],
    delta:int=0,
    ) -> list[tuple[int, int]]:
    """Merge overlapping fragments in a list of fragments coordinates.

        Parameters
        ----------
        coord: list[tuple[int, int]]
            Fragment coordinates lists.
        delta: int
            To adjust the merging of adjacent fragments.

        Returns
        -------
        list[tuple[int, int]]

        Notes
        -----
        An empty list is returned if coord is empty.
    """
    # Test in test.unit.core.test_method.Test_MergeOverlappingFragments
    #region ---------------------------------------------------> Variables
    coordO = []
    #endregion ------------------------------------------------> Variables

    #region ------------------------------------------------------> Sort & Dup
    coordS = sorted(list(set(coord)), key=itemgetter(0,1))
    #endregion ---------------------------------------------------> Sort & Dup

    #region -------------------------------------> Merge Overlapping Intervals
    try:
        a,b = coordS[0]
    except IndexError:
        return []
    for ac,bc in coordS[1:]:
        if ac <= b+delta:
            if bc > b:
                b = bc
        else:
            coordO.append((a,b))
            a = ac
            b = bc
    #------------------------------> Catch the last one
    coordO.append((a,b))
    #endregion ----------------------------------> Merge Overlapping Intervals

    return coordO
#---
#endregion -----------------------------------------------------------> Others
