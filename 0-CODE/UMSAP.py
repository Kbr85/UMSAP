# ------------------------------------------------------------------------------
# 	Copyright (C) 2017 Kenny Bravo Rodriguez <www.umsap.nl>

# 	This program is distributed for free in the hope that it will be useful,
# 	but WITHOUT ANY WARRANTY; without even the implied warranty of
# 	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

# 	See the accompaning licence for more details.
# ------------------------------------------------------------------------------


""" This module starts the application """


# ------------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Methods
# ------------------------------------------------------------------------------


# --- Imports
## Standard modules
import wx
import _thread
from pathlib import Path
## My modules
import config.config	 as config
import gui.menu.menu	 as menu
import gui.gui_classes   as gclasses
import gui.gui_methods   as gmethods
import data.data_classes as dclasses
import data.data_methods as dmethods
#--- 
from gui.win.win_m_main		    import WinMain
from gui.win.win_m_about		import WinAbout
from gui.win.win_m_preferences  import WinPreferences
from gui.win.win_m_updateCheck  import WinUpdateNotice
#---
from gui.win.win_ut_util		import WinUtil
from gui.win.win_ut_corra	    import WinCorrA
from gui.win.win_ut_corraR	    import WinCorrARes
from gui.win.win_ut_mergeAA	    import WinMergeAAFiles
from gui.win.win_ut_typeRes	    import WinTypeRes
from gui.win.win_ut_shortdfiles import WinShortDataFiles
#---
from gui.win.win_tp_tarprot	    import WinTarProt
from gui.win.win_tp_histo	    import WinHisto
from gui.win.win_tp_seqalign	import WinSeqAlign
from gui.win.win_tp_aadist	    import WinAAdist
from gui.win.win_tp_cutpropR	import WinCutPropRes
from gui.win.win_tp_histoR	    import WinHistoRes
from gui.win.win_tp_aadistR	    import WinAAdistRes
from gui.win.win_tp_tarprotR	import WinTarProtRes
from gui.win.win_tp_cuts2pdb	import WinCuts2PDB
#---
from gui.win.win_lp_limprot	    import WinLimProt
from gui.win.win_lp_limprotR	import WinLimProtRes
from gui.win.win_lp_seq		    import WinSeqAlignLP
#---
from gui.win.win_pp_protprof	import WinProtProf
from gui.win.win_pp_protprofR   import WinProtProfRes
#---



class UmsapApp(wx.App):
	""" Start the UMSAP app """

	def OnInit(self):
		""" Initialize the app """
	   
	 #--> Set special configuration values that require a running wx.App
		self.AppInit()
	 #--> Check for updates
		self.AppUpdateCheck()
	 #--> Show the main frame & Return
		gmethods.WinMUCreate(config.name["Main"])
		return True
	#---

	####---- Methods of the class
	def AppInit(self):
		""" Define parameters that requires a wx.App to be already running """
	   
	 #--> MenuBar
		if config.cOS == "Darwin":
			wx.MenuBar.MacSetCommonMenuBar(menu.MainMenuBar())
		else:
			pass
	 #--> Configuration options
	  #--> Screen Size
		config.size["Screen"] = wx.GetDisplaySize()
	  #--> Fonts
	   #--> Define Fonts
		if config.cOS == "Darwin":
			config.font[config.name["TarProtRes"]] = wx.Font(
				14,
				wx.FONTFAMILY_ROMAN,
				wx.FONTSTYLE_NORMAL,
				wx.FONTWEIGHT_NORMAL,
				False,
				faceName="Courier",
			)
		elif config.cOS == "Windows":
			config.font[config.name["TarProtRes"]] = wx.Font(
				12,
				wx.FONTFAMILY_ROMAN,
				wx.FONTSTYLE_NORMAL,
				wx.FONTWEIGHT_NORMAL,
				False,
				faceName="Courier",
			)
		elif config.cOS == "Linux":
			config.font[config.name["TarProtRes"]] = wx.Font(
				11,
				wx.FONTFAMILY_ROMAN,
				wx.FONTSTYLE_NORMAL,
				wx.FONTWEIGHT_NORMAL,
				False,
				faceName="Courier",
			)
		else:
			gclasses.DlgUnexpectedErrorMsg(config.msg["UErrors"]["OS"])
			return False
	   #--> Assign fonts
		config.font[config.name["LimProtRes"]] = config.font[config.name["TarProtRes"]]
	  #--> Pointers
		config.pointer['gmethods']['LaunchUscr'] = { # Launch module from uscr file
			config.mod[config.name['TarProt']] : gmethods.LaunchTarProt,
			config.mod[config.name['LimProt']] : gmethods.LaunchLimProt,
			config.mod[config.name['ProtProf']]: gmethods.LaunchProtProf,
		}
		config.pointer['gmethods']['WinCreate'] = { # Modules/util windows
			config.name['Main']        : WinMain,
			config.name['About']       : WinAbout,
			config.name['Preference']  : WinPreferences,
			config.name['UpdateNotice']: WinUpdateNotice,
			#---
			config.name['Util']    : WinUtil,
			config.name['CorrA']   : WinCorrA,
			config.name['CorrARes']: WinCorrARes,
			config.name['TypeRes'] : WinTypeRes,
 			#--- 
 			config.name['TarProt']   : WinTarProt,
 			config.name['Histo']     : WinHisto,
 			config.name['SeqAlign']  : WinSeqAlign,
 			config.name['AAdist']    : WinAAdist,
 			config.name['CutPropRes']: WinCutPropRes,
 			config.name['HistoRes']  : WinHistoRes,
 			config.name['AAdistR']   : WinAAdistRes,
 			config.name['TarProtRes']: WinTarProtRes,
 			config.name['ShortDFile']: WinShortDataFiles,
 			config.name['Cuts2PDB']  : WinCuts2PDB,
 			config.name['MergeAA']   : WinMergeAAFiles,
			#---
			config.name['LimProt']   : WinLimProt,
			config.name['LimProtRes']: WinLimProtRes,
			config.name['SeqH']      : WinSeqAlignLP,
			#---
			config.name['ProtProfRes']: WinProtProfRes,
			config.name['ProtProf']   : WinProtProf,
		}
		config.pointer['menu']['toolmenu'] = { # Tool menu
			#--> Modules
			config.name['TarProt'] : menu.ToolMenuTarProtMod,
			config.name['LimProt'] : menu.ToolMenuLimProtMod,
			config.name['ProtProf']: menu.ToolMenuProtProfMod,
			#--> Utilities
			config.name['MergeAA'] : menu.ToolMenuMergeAA,
			config.name['CorrA']   : menu.ToolMenuCorrAMod,
			config.name['CorrARes']: menu.ToolMenuCorrARes,
			#--> Result windows
			config.name['TarProtRes']: menu.ToolMenuTarProtRes,
			config.name['LimProtRes']: menu.ToolMenuLimProtRes,
			config.name['CutPropRes']: menu.ToolMenuCutPropRes,
			config.name['HistoRes']  : menu.ToolMenuHistoRes,
			config.name['AAdistR']   : menu.ToolMenuAAdistRes,
			#--> Other windows
			config.name['TypeRes']   : menu.ToolMenuTypeResults,
		}
		config.pointer['dclasses']['DataObj'] = { # Data objects with name and file extension
			config.name['TarProtRes']	  : dclasses.DataObjTarProtFile,
			config.extShort['TarProt'][0] : dclasses.DataObjTarProtFile,
			config.name['CorrARes']	      : dclasses.DataObjCorrFile,
			config.name['CutPropRes']	  : dclasses.DataObjCutpropFile,
			config.name['AAdistR']		  : dclasses.DataObjAAdistFile,
			config.name['HistoRes']	      : dclasses.DataObjHistFile,
			config.name['LimProtRes']	  : dclasses.DataObjLimProtFile,
			config.extShort['LimProt'][0] : dclasses.DataObjLimProtFile,
			config.extShort['ProtProf'][0]: dclasses.DataObjProtProfFile,
			config.name['ProtProfRes']	  : dclasses.DataObjProtProfFile,
		}
		config.pointer['dmethods']['fillListCtrl'] = { # Info to fill a ListCtrl
			config.name['TarProtRes']  : dmethods.Get_Data4ListCtrl_TarProtRes,
			config.name['LimProtRes']  : dmethods.Get_Data4ListCtrl_LimProtRes,
			config.name['ProtProfRes'] : dmethods.Get_Data4ListCtrl_ProtProfRes,
		}
	 #--> Return
		return True
	#---

	def AppUpdateCheck(self):
		""" Check for updates from a different thread"""
	 #--> Check if check is on
		if config.general["checkUpdate"] == 1:
	 #--> Check
			_thread.start_new_thread(gmethods.UpdateCheck, ("main",))
		else:
			pass
	 #--> Return
		return True
	#---
#---

if __name__ == "__main__":
	app = UmsapApp()
	app.MainLoop()
else:
	pass

