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


"""Methods to handle files in the result module of the app"""


#region -------------------------------------------------------------> Imports
import shutil
from pathlib import Path
from typing  import Union

import pandas as pd

from config.config import config as mConfig
from core     import check  as cCheck
from core     import file   as cFile
from core     import method as cMethod
from corr     import method as corrMethod
from dataprep import method as dataMethod
from limprot  import method as limpMethod
from protprof import method as protMethod
from tarprot  import method as tarpMethod
#endregion ----------------------------------------------------------> Imports


#region -------------------------------------------------------------> Classes
class UMSAPFile():
    """Load an UMSAP file.

        Parameters
        ----------
        rFileP: Path
            Path to the UMSAP file

        Attributes
        ----------
        dConfigure: dict
            Configure methods. Keys are the section names as read from the file
        rData: dict
            Data read from json formatted file.
        rFileP: Path
            Path to the UMSAP file.
        rInputFileP: Path
            Path to the input files.
        rStepDataP: Path
            Path to the step data files.
        SeqF: list[str]
            Sections with a sequence file.
    """
    # No Test
    #region -----------------------------------------------------> Class setup
    SeqF = [mConfig.tarp.tMod, mConfig.limp.tMod]
    #------------------------------>
    rUserDataClass = {
        mConfig.corr.tUtil : corrMethod.UserData,
        mConfig.data.tUtil : dataMethod.UserData,
        mConfig.prot.tMod  : protMethod.UserData,
        mConfig.tarp.tMod  : tarpMethod.UserData,
        mConfig.limp.tMod  : limpMethod.UserData,
    }
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(self, fileP:Path) -> None:
        """ """
        #region ---------------------------------------------------> Read File
        data = cFile.ReadJSON(fileP)
        #------------------------------> Sort Keys
        dataKey = sorted(list(data.keys()))
        #------------------------------>
        self.rData = {k:data[k] for k in dataKey}
        #endregion ------------------------------------------------> Read File

        #region ---------------------------------------------------> Variables
        self.rFileP = fileP
        self.rStepDataP  = self.rFileP.parent / mConfig.core.fnDataSteps
        self.rInputFileP = self.rFileP.parent / mConfig.core.fnDataInit
        #------------------------------>
        self.dConfigure = {                                                     # Configure methods. Keys are section names.
            mConfig.corr.tUtil: self.ConfigureDataCorrA,
            mConfig.data.tUtil: self.ConfigureDataDataPrep,
            mConfig.prot.tMod : self.ConfigureDataProtProf,
            mConfig.limp.tMod : self.ConfigureDataLimProt,
            mConfig.tarp.tMod : self.ConfigureDataTarProt,
        }
        #endregion ------------------------------------------------> Variables
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ----------------------------------------------------> Class Method
    def Save(self, tPath:Union[None, str, Path]=None) -> bool:
        """Save the file content.

            Parameters
            ----------
            tPath: Path, str or None

            Returns
            -------
            bool
        """
        #region -----------------------------------------------> Security Copy
        tempF = self.rFileP.with_name('.kbr-temp.umsap')
        shutil.copy(self.rFileP, tempF)
        #endregion --------------------------------------------> Security Copy

        #region --------------------------------------------------->
        oPath = tPath if tPath is not None else self.rFileP
        #------------------------------>
        try:
            cFile.WriteJSON(oPath, self.rData)
        except Exception as e:
            shutil.copy(tempF, self.rFileP)
            tempF.unlink()
            raise e
        #endregion ------------------------------------------------>

        tempF.unlink()
        return True
    #---
    #endregion -------------------------------------------------> Class Method

    #region -------------------------------------------------------> Configure
    def ConfigureDataCorrA(self) -> cMethod.BaseAnalysis:
        """Configure a Correlation Analysis section.

            Returns
            ------
            cMethod.BaseAnalysis
                For each CorrA a new attribute 'Date' is added with value
                corrMethod.CorrAnalysis.
        """
        #region ---------------------------------------------------> Variables
        data  = cMethod.BaseAnalysis()
        pathB = mConfig.corr.tUtil.replace(" ", "-")
        #endregion ------------------------------------------------> Variables

        #region -------------------------------------------------> Plot & Menu
        #------------------------------> Fill
        for k, v in self.rData[mConfig.corr.tUtil].items():
            #------------------------------>
            pathA = k.split(" - ")[0]
            tPath = self.rStepDataP / f'{pathA}_{pathB}'
            #------------------------------> Read data
            try:
                df = cFile.ReadCSV2DF(tPath/v['R'])
            except Exception:
                data.error.append(k)
                continue
            #------------------------------> Check Columns
            try:
                numColList = v['CI']['oc']['Column']                            # Keep support for previous versions
            except KeyError:
                numColList = v['CI']['ocResCtrlFlat']
            numCol = len(numColList)
            #------------------------------>
            if numCol != df.shape[0]:
                data.error.append(k)
                continue
            #------------------------------> Add to dict if no error
            setattr(data, k, corrMethod.CorrAnalysis(
                df         = df,
                numCol     = numCol,
                numColList = numColList
            ))
            data.date.append(k)
        #endregion ----------------------------------------------> Plot & Menu

        return data
    #---

    def ConfigureDataDataPrep(
        self,
        tSection:str = '',
        tDate:str    = '',
        ) -> cMethod.BaseAnalysis:
        """Configure a Data Preparation Check section.

            Parameters
            ----------
            tSection: str
                Section name. Default is ''.
            tDate: str
                Date and comment. Default is ''.

            Returns
            -------
            cMethod.BaseAnalysis
                For each DataPrep a new attribute 'Date' is added with value
                dataMethod.DataPrepAnalysis.
        """
        #------------------------------> Data Prep From Plot
        if tSection and tDate:
            return self.ConfigureDataDataPrepFromPlot(tSection, tDate)
        #------------------------------> Data Prep From UMSAP
        if not tSection and not tDate:
            return self.ConfigureDataDataPrepFromUMSAP()
        #------------------------------> Error
        msg = (f'Both tSection ({tSection}) and tDate ({tDate}) must be '
               f"defined or ''.")
        raise ValueError(msg)
    #---

    def ConfigureDataDataPrepFromPlot(
        self,
        tSection:str,
        tDate:str,
        ) -> cMethod.BaseAnalysis:
        """Configure a Data Preparation Check section.

            Parameters
            ----------
            tSection: str
                Section name.
            tDate: str
                Date and comment.

            Returns
            -------
            cMethod.BaseAnalysis
                For each DataPrep a new attribute 'Date' is added with value
                dataMethod.DataPrepAnalysis.
        """
        #region ---------------------------------------------------> Variables
        data  = cMethod.BaseAnalysis()
        pathA = tDate.split(" - ")[0]
        pathB = tSection.replace(" ", "-")
        tPath = self.rStepDataP / f'{pathA}_{pathB}'
        #endregion ------------------------------------------------> Variables

        #region --------------------------------------------------------> Data
        dp = {j:cFile.ReadCSV2DF(tPath/w) for j,w in self.rData[tSection][tDate]['DP'].items()}
        #------------------------------>
        try:
            numColList = self.rData[tSection][tDate]['CI']['oc']['Column']      # Keep support for previous versions
        except KeyError:
            numColList = self.rData[tSection][tDate]['CI']['ocColumn']
        #------------------------------>
        setattr(data, tDate, dataMethod.DataAnalysis(
            dp         = dataMethod.DataSteps(**dp),
            numColList = numColList,
        ))
        data.date.append(tDate)
        #endregion -----------------------------------------------------> Data

        return data
    #---

    def ConfigureDataDataPrepFromUMSAP(self) -> cMethod.BaseAnalysis:
        """Configure a Data Preparation Check section.

            Returns
            -------
            cMethod.BaseAnalysis
                For each DataPrep a new attribute 'Date' is added with value
                dataMethod.DataPrepAnalysis.
        """
        #region ---------------------------------------------------> Variables
        data  = cMethod.BaseAnalysis()
        pathB = mConfig.data.tUtil.replace(" ", "-")
        #endregion ------------------------------------------------> Variables

        #region -------------------------------------------------> Plot & Menu
        for k,v in self.rData[mConfig.data.tUtil].items():
            #------------------------------> Read and type
            pathA = k.split(" - ")[0]
            tPath = self.rStepDataP / f'{pathA}_{pathB}'
            #------------------------------> Read data frames
            try:
                dp = {j:cFile.ReadCSV2DF(tPath/w) for j,w in v['DP'].items()}
            except Exception:
                data.error.append(k)
                continue
            #------------------------------>
            try:
                numColList = v['CI']['oc']['Column']                            # Keep support for older versions
            except KeyError:
                numColList = v['CI']['ocColumn']
            #------------------------------>
            setattr(data, k, dataMethod.DataAnalysis(
                dp         = dataMethod.DataSteps(**dp),
                numColList = numColList,
            ))
            data.date.append(k)
        #endregion ----------------------------------------------> Plot & Menu

        return data
    #---

    def ConfigureDataProtProf(self) -> cMethod.BaseAnalysis:
        """Configure a Proteome Profiling section.

            Returns
            ------
            cMethod.BaseAnalysis
                For each Proteome Profiling a new attribute 'Date' is added with
                value protMethod.ProtProfAnalysis.
        """
        #region ---------------------------------------------------> Variables
        data   = cMethod.BaseAnalysis()
        colStr = [('Gene','Gene','Gene'),('Protein','Protein','Protein')]
        pathB  = mConfig.prot.tMod.replace(" ", "-")
        #endregion ------------------------------------------------> Variables

        #region -------------------------------------------------> Plot & Menu
        for k,v in self.rData[mConfig.prot.tMod].items():
            #------------------------------> Path
            pathA = k.split(" - ")[0]
            tPath = self.rStepDataP / f'{pathA}_{pathB}'
            #------------------------------> Read and type
            try:
                df = cFile.ReadCSV2DF(tPath/v['R'], header=[0,1,2])
                df.loc[:,colStr] = df.loc[:,colStr].astype('str')               # type: ignore
            except Exception:
                data.error.append(k)
                continue
            #------------------------------> Alpha
            try:
                alpha    = v['CI']['Alpha']                                     # Keep support for older versions
                labelA   = v['CI']['Cond']
                labelB   = v['CI']['RP']
                ctrlType = v['CI']['ControlT']
                ctrlName = v['CI']['ControlL'][0]
            except KeyError:
                alpha    = v['CI']['alpha']
                labelA   = v['CI']['labelA']
                labelB   = v['CI']['labelB']
                ctrlType = v['CI']['ctrlType']
                ctrlName = v['CI']['ctrlName'][0]
            #------------------------------> Add to class
            setattr(data, k, protMethod.ProtAnalysis(
                df       = df,
                filterS  = v['F'],
                alpha    = alpha,
                labelA   = labelA,
                labelB   = labelB,
                ctrlName = ctrlName,
                ctrlType = ctrlType,
            ))
            data.date.append(k)
        #endregion ----------------------------------------------> Plot & Menu

        return data
    #---

    def ConfigureDataLimProt(self) -> cMethod.BaseAnalysis:
        """Configure a Limited Proteolysis section.

            Returns
            -------
            cMethod.BaseAnalysis
                For each Limited Proteolysis a new attribute 'Date' is added
                with value limpMethod.LimpAnalysis.
        """
        #region ---------------------------------------------------> Variables
        plotData = cMethod.BaseAnalysis()
        pathB    = mConfig.limp.tMod.replace(" ", "-")
        #endregion ------------------------------------------------> Variables

        #region -------------------------------------------------> Plot & Menu
        for k,v in self.rData[mConfig.limp.tMod].items():
            #------------------------------>
            pathA = k.split(" - ")[0]
            tPath = self.rStepDataP / f'{pathA}_{pathB}'
            #------------------------------>
            try:
                df = cFile.ReadCSV2DF(tPath/v['R'], header=[0,1,2])
            except Exception:
                plotData.error.append(k)
                continue
            #------------------------------>
            try:
                labelB     = v['CI']['Band']                                     # Keep support for older versions
                labelA     = v['CI']['Lane']
                alpha      = v['CI']['Alpha']
                protLength = v['CI']['ProtLength']
                protLoc    = v['CI']['ProtLoc']
                protDelta  = v['CI']['ProtDelta']
                prot       = v['CI']['TargetProt']
            except KeyError:
                labelB     = v['CI']['labelB']
                labelA     = v['CI']['labelA']
                alpha      = v['CI']['alpha']
                protLength = v['CI']['protLength']
                protLoc    = v['CI']['protLoc']
                protDelta  = v['CI']['protDelta']
                prot       = v['CI']['targetProt']
            #------------------------------>
            setattr(plotData, k, limpMethod.LimpAnalysis(
                df         = df,
                labelA     = labelA,
                labelB     = labelB,
                alpha      = alpha,
                protLength = protLength,
                protLoc    = protLoc,
                protDelta  = protDelta,
                targetProt = prot,
            ))
            plotData.date.append(k)
        #endregion ----------------------------------------------> Plot & Menu

        return plotData
    #---

    def ConfigureDataTarProt(self) -> cMethod.BaseAnalysis:
        """Configure a Targeted Proteolysis section.

            Returns
            ------
            cMethod.BaseAnalysis
                For each Targeted Proteolysis a new attribute 'Date' is added
                with value tarpMethod.TarpAnalysis.
        """
        #region ---------------------------------------------------> Variables
        data  = cMethod.BaseAnalysis()
        pathB = mConfig.tarp.tMod.replace(" ", "-")
        #endregion ------------------------------------------------> Variables

        #region -------------------------------------------------> Plot & Menu
        for k,v in self.rData[mConfig.tarp.tMod].items():
            #------------------------------>
            pathA = k.split(" - ")[0]
            tPath = self.rStepDataP / f'{pathA}_{pathB}'
            #------------------------------>
            try:
                df  = cFile.ReadCSV2DF(tPath/v['R'], header=[0,1])
            except Exception:
                data.error.append(k)
                continue
            #------------------------------>
            try:
                exp        = v['CI']['Exp']                                     # Keep support for older versions
                ctrl       = v['CI']['ControlL']
                alpha      = v['CI']['Alpha']
                protLength = v['CI']['ProtLength']
                protLoc    = v['CI']['ProtLoc']
                protDelta  = v['CI']['ProtDelta']
                prot       = v['CI']['TargetProt']
            except KeyError:
                exp        = v['CI']['labelA']
                ctrl       = v['CI']['ctrlName']
                alpha      = v['CI']['alpha']
                protLength = v['CI']['protLength']
                protLoc    = v['CI']['protLoc']
                protDelta  = v['CI']['protDelta']
                prot       = v['CI']['targetProt']
            #------------------------------> Add to dict if no error
            setattr(data, k, tarpMethod.TarpAnalysis(
                df         = df,
                labelA     = exp,
                ctrlName   = [ctrl],
                alpha      = alpha,
                protLength = protLength,
                protLoc    = protLoc,
                protDelta  = protDelta,
                targetProt = prot,
                CpR        = v['CpR'],
                CEvol      = v['CEvol'],
                AA         = v.get('AA', {}),
                Hist       = v.get('Hist', {})
            ))
            data.date.append(k)
        #endregion ----------------------------------------------> Plot & Menu

        return data
    #---
    #endregion ----------------------------------------------------> Configure

    #region -----------------------------------------------------> Get Methods
    def GetDataUser(self, tSection:str, tDate:str) -> cMethod.BaseUserData:
        """Get both initial and curated data from the user for the analysis.

            Parameters
            ----------
            tSection: str
                Analysis performed, e.g. 'Correlation Analysis'
            tDate: str
                The date plus user-given Analysis ID
                e.g. '20210325-112056 - bla'

            Returns
            -------
            cMethod.BaseUserData
                An instance according to tSection.
        """
        #region ---------------------------------------------> Helper Function
        def OldVersion():
            """"""
            #region ------------------------------------------> Key Translator
            kTranslator = {
                'uFile'  : 'uFile',
                'ID'     : 'ID',
                #------------------------------>
                'Cero'       : 'cero',
                'TransMethod': 'tran',
                'NormMethod' : 'norm',
                'ImpMethod'  : 'imp',
                'Shift'      : 'shift',
                'Width'      : 'width',
                #------------------------------>
                'CorrMethod': 'corr',
                'ScoreVal'  : 'scoreVal',
                'RawI'      : 'rawInt',
                'IndS'      : 'indSample',
                'Alpha'     : 'alpha',
                'Beta'      : 'beta',
                'Gamma'     : 'gamma',
                'Theta'     : 'theta',
                'ThetaMax'  : 'thetaM',
                'CorrectP'  : 'correctedP',
                'TargetProt': 'targetProt',
                'AA'        : 'posAA',
                'Hist'      : 'winHist',
                #------------------------------>
                'Cond'    : 'labelA',
                'Lane'    : 'labelA',
                'RP'      : 'labelB',
                'Band'    : 'labelB',
                'Exp'     : 'labelA',
                'ControlT': 'ctrlType',
                'ControlL': 'ctrlName',
                'oc'      : {
                    'SeqCol'       : 'ocSeq',
                    'TargetProtCol': 'ocTargetProt',
                    'DetectedP'    : 'ocTargetProt',
                    'GeneName'     : 'ocGene',
                    'ScoreCol'     : 'ocScore',
                    'ExcludeR'     : 'ocExcludeR',
                    'ResCtrl'      : 'ocResCtrl',
                    'Column'       : 'ocColumn',
                },
                'df' : {
                    'SeqCol'       : 'dfSeq',
                    'TargetProtCol': 'dfTargetProt',
                    'DetectedP'    : 'dfTargetProt',
                    'GeneName'     : 'dfGene',
                    'ScoreCol'     : 'dfScore',
                    'ExcludeR'     : 'dfExcludeR',
                    'ResCtrl'      : 'dfResCtrl',
                    'ColumnR'      : 'dfColumnR',
                    'ColumnF'      : 'dfColumnF',
                    'ResCtrlFlat'  : 'dfResCtrlFlat',
                },
                'dfo': {
                    'NC' : 'dfNC',
                    'NCF': 'dfNCF',
                },
                'ProtLength': 'protLength',
                'ProtLoc'   : 'protLoc',
                'ProtDelta' : 'protDelta',
            }
            #endregion ---------------------------------------> Key Translator

            #region ----------------------------------------------------> Data
            data = {}
            #------------------------------>
            for k,v in self.rData[tSection][tDate]['CI'].items():
                if isinstance(v, dict):
                    for j,w in v.items():
                        try:
                            data[kTranslator[k][j]] = w
                        except KeyError:
                            pass
                else:
                    try:
                        data[kTranslator[k]] = v
                    except KeyError:
                        pass
            #------------------------------> Files
            for k in self.rData[tSection][tDate]['I'].keys():
                if 'Data' in k:
                    fileN = self.rData[tSection][tDate]['I'][k]
                    data['iFile'] = self.rInputFileP / fileN
                #------------------------------>
                if 'Sequences File' in k:
                    fileN = self.rData[tSection][tDate]['I'][k]
                    data['seqFile'] = self.rInputFileP / fileN
                #------------------------------>
                if 'Results - Control' in k:
                    data['resCtrl'] = self.rData[tSection][tDate]['I'][k]
            #------------------------------> Independent Samples
            if data.get('indSample', None) is not None:
                if data['indSample']:
                    data['indSample'] = 'i'
                else:
                    data['indSample'] = 'p'
            #endregion -------------------------------------------------> Data

            return data
        #---
        #endregion ------------------------------------------> Helper Function

        #region --------------------------------------------------------> Data
        fileV = self.rData[tSection][tDate]['V']['Version']
        #------------------------------>
        if cCheck.VersionCompare('2.2.1', fileV)[0]:
            data = OldVersion()                                                 # Old Files <= 2.2.0 with json format
        else:
            data          = self.rData[tSection][tDate]['CI']                   # > 2.2.0
            data['uFile'] = self.rFileP
            data['iFile'] = self.rInputFileP / data['iFileN']
            try:
                data['seqFile'] = self.rInputFileP / data['seqFileN']
            except KeyError:
                pass
        #------------------------------>
        if data.get('method') is None and tSection == mConfig.tarp.tMod:
            data['method']    = 'slope'
            data['indSample'] = 'i'
        #endregion -----------------------------------------------------> Data

        #region ---------------------------------------------------> DataClass
        userData = self.rUserDataClass[tSection]()                              # Default Values
        userData.FromDict(data)                                                 # Values for Analysis
        #endregion ------------------------------------------------> DataClass

        return userData
    #---

    def GetSeq(self, tSection:str, tDate:str) -> tuple[str, str]:
        """Get the sequences used in an analysis.

            Parameters
            ----------
            tSection: str
                Analysis performed, e.g. 'Correlation Analysis'
            tDate: str
                The date plus user-given Analysis ID
                e.g. '20210325-112056 - bla'

            Returns
            -------
            tuple[RecSeq, NatSeq]
        """
        #region ------------------------------------------------> Path
        fileN = ''
        #------------------------------>
        try:
            fileN = self.rData[tSection][tDate]['CI']['seqFileN']
        except KeyError:                                                        # Keep backward compatibility
            for k,v in self.rData[tSection][tDate]['I'].items():
                if 'Sequences File' in k:
                    fileN = v
                    break
        #endregion ---------------------------------------------> Path

        #region --------------------------------------------------->
        seqObj = cFile.FastaFile(self.rInputFileP/fileN)
        #endregion ------------------------------------------------>

        return (seqObj.rSeqRec, seqObj.rSeqNat)
    #---

    def GetRecSeq(self, tSection:str, tDate:str) -> str:
        """Get the recombinant sequence used in an analysis.

            Parameters
            ----------
            tSection: str
                Analysis performed, e.g. 'Correlation Analysis'
            tDate: str
                The date plus user-given Analysis ID
                e.g. '20210325-112056 - bla'

            Returns
            -------
            str
        """
        #region --------------------------------------------------->
        seqs = self.GetSeq(tSection, tDate)
        #endregion ------------------------------------------------>

        return seqs[0]
    #---

    def GetFAData(
        self,
        tSection:str,
        tDate:str,
        fileN:str,
        header:list[int],
        ) -> pd.DataFrame:
        """Get the data for a Further Analysis section.

            Parameters
            ----------
            tSection: str
                Analysis performed, e.g. 'Correlation Analysis'.
            tDate: str
                The date e.g. '20210325-112056 - bla'.
            fileN: str
                File name with the data.
            header: list[int]
                Header rows in the file.

            Returns
            -------
            pd.DataFrame
        """
        #region --------------------------------------------------->
        pathA = tDate.split(" - ")[0]
        pathB = tSection.replace(" ", "-")
        tPath = self.rStepDataP/f'{pathA}_{pathB}'/fileN
        #endregion ------------------------------------------------>

        return cFile.ReadCSV2DF(tPath, header=header)
    #---

    def GetCleavagePerResidue(self, tSection:str, tDate:str) -> 'pd.DataFrame':
        """Get the Cleavage per residue data.

            Parameters
            ----------
            tSection: str
                Analysis performed, e.g. 'Correlation Analysis'.
            tDate: str
                The date e.g. '20210325-112056 - bla'.

            Returns
            -------
            pd.DataFrame
        """
        #region ---------------------------------------------------> Path
        folder = f'{tDate.split(" - ")[0]}_{tSection.replace(" ", "-")}'
        fileN  = self.rData[tSection][tDate]['CpR']
        fileP  = self.rStepDataP/folder/fileN
        #endregion ------------------------------------------------> Path

        return cFile.ReadCSV2DF(fileP, header=[0,1])
    #---

    def GetCleavageEvolution(self, tSection:str, tDate:str) -> 'pd.DataFrame':
        """Get the Cleavage evolution information.

            Parameters
            ----------
            tSection: str
                Analysis performed, e.g. 'Correlation Analysis'.
            tDate: str
                The date e.g. '20210325-112056 - bla'.

            Returns
            -------
            pd.DataFrame
        """
        #region ---------------------------------------------------> Path
        folder = f'{tDate.split(" - ")[0]}_{tSection.replace(" ", "-")}'
        fileN  = self.rData[tSection][tDate]['CEvol']
        fileP  = self.rStepDataP/folder/fileN
        #endregion ------------------------------------------------> Path

        return cFile.ReadCSV2DF(fileP, header=[0,1])
    #---

    def GetInputFiles(self) -> list[str]:
        """Get a flat list of all input files in self.rData.

            Returns
            -------
            list[str]
                List of full file paths.

            Notes
            -----
            This assumes files are added to I as the first and second items.
            Full path to the files are returned.
        """
        #region --------------------------------------------------->
        inputF = []
        #------------------------------>
        for k,v in self.rData.items():
            for w in v.values():
                iVal   = iter(w['I'].values())
                inputF.append(self.rInputFileP/next(iVal))
                if k in self.SeqF:
                    inputF.append(self.rInputFileP/next(iVal))
        #endregion ------------------------------------------------>

        return inputF
    #---
    #endregion --------------------------------------------------> Get Methods
#---
#endregion ----------------------------------------------------------> Classes
