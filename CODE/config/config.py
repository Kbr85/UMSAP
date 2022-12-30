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


"""Configuration of the app"""


#region -------------------------------------------------------------> Imports
import json
from dataclasses import dataclass

from core     import config as cConfig
from corr     import config as corrConfig
from dataprep import config as dataConfig
from help     import config as hConfig
from limprot  import config as limpConfig
from main     import config as mConfig
from protprof import config as protConfig
from tarprot  import config as tarpConfig
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------> Configuration
@dataclass
class Configuration():
    """Configuration of the app

        Notes
        -----
        Each configuration section must define a converter dict to properly
        assign the correct type for each attribute that can be defined in a
        user configuration file, e.g.:
        converter = {'DPI' : int, 'checkForUpdates':bool}
    """
    #region ---------------------------------------------------------> Options
    core:cConfig.Configuration
    corr:corrConfig.Configuration
    data:dataConfig.Configuration
    help:hConfig.Configuration
    limp:limpConfig.Configuration
    main:mConfig.Configuration
    prot:protConfig.Configuration
    tarp:tarpConfig.Configuration
    #endregion ------------------------------------------------------> Options

    #region ---------------------------------------------------> Class Methods
    def LoadUserConfig(self) -> bool:
        """Load and validate user configuration file.

            Returns
            -------
            bool

            Notes
            -----
            Method handles any exception raise since this will be reported by
            mWindow.MainWindow
        """
        # Test in test.unit.test_method.Test_LoadUserConfig
        #region ---------------------------------------------------> Read File
        try:
            with open(self.core.fConfig, 'r', encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            #--> Config file has not been created or was deleted by user
            return True
        except Exception as e:
            #--> Config file exists but cannot be read
            self.core.confUserFile          = False
            self.core.confUserFileException = e
            return False
        #endregion ------------------------------------------------> Read File

        #region ---------------------------------------------------> Variables
        badOpt = []
        #endregion ------------------------------------------------> Variables

        #region -------------------------------------------------> Load Config
        for k in data:
            #------------------------------> Check config section exists
            if (sec := getattr(self, k, None)) is None:
                badOpt.append(sec)
                continue
            #------------------------------>
            for j,v in data[k].items():
                #------------------------------>
                if getattr(sec, j, None) is None:
                    badOpt.append(j)
                    continue
                #------------------------------>
                conv = sec.converter.get(j, str)
                setattr(sec, j, conv(v))
        #------------------------------>
        self.core.confUserWrongOptions = badOpt
        #endregion ----------------------------------------------> Load Config

        return True
    #---
    #endregion ------------------------------------------------> Class Methods
#---

config = Configuration(
    cConfig.Configuration(),
    corrConfig.Configuration(),
    dataConfig.Configuration(),
    hConfig.Configuration(),
    limpConfig.Configuration(),
    mConfig.Configuration(),
    protConfig.Configuration(),
    tarpConfig.Configuration(),
)
#endregion ----------------------------------------------------> Configuration
