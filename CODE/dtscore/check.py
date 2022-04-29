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


#region -------------------------------------------------------------> Imports
from typing import Union, Optional
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Methods
def AInRange(
    a: Union[str, int, float], refMin: Union[str, int, float, None]=None,
    refMax: Union[str, int, float, None]=None,
    ) -> tuple[bool, Optional[tuple[str, Optional[str], str]]]:
    """Check if refMin <= a <= refMax.

        Parameters
        ----------
        a: str, int or float
            Number to check if it is within the given range
        refMin: str, int, float or None
            Lower end of range
        refMax: str, int, float or None
            Upper end of range

        Returns
        -------
        tuple
            - (True, None)
            - (False, (code, val, msg))
                code, val are:
                    - ('AInRange', a) : a is the given value to check
                
        Notes
        -----
        Leaving one range limit as None allows to check for open intervals.
        If both refMin and refMax are None it returns True
            
        Examples
        --------
        >>> AInRange(6, refMin=None, refMax=None)
        >>> (True, None)
        >>> AInRange(6, refMin='3', refMax=10)
        >>> (True, None)
        >>> AInRange('0', refMin='3', refMax=10)
        >>> (False, ('AInRange), '0', '0 is not in the range: [3, 10].')
        >>> AInRange(6, refMin='3')
        >>> (True, None)
        >>> AInRange(-1, refMax='-3.9')
        >>> (False, ('AInRange', '-1', '-1 is not in the range: [None, -3.9].'))
        >>> AInRange('3', refMin=-10, refN=3, refMax=0)
        >>> (True, None)
    """
    #region -------------------------------------------------------> Variables
    a = float(a)
    b = float(refMin) if refMin is not None else float('-inf')
    c = float(refMax) if refMax is not None else float('inf')
    #endregion ----------------------------------------------------> Variables
    
    #region ---------------------------------------------------------> Compare
    if b <= a <= c:
        return (True, None)
    else:
        msg = (f'{a} is not in the range: [{refMin}, {refMax}].')
        return (False, ('AInRange', str(a), msg))
    #endregion ------------------------------------------------------> Compare
#---

#endregion ----------------------------------------------------------> Methods
