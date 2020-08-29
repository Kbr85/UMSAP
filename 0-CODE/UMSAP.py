# ------------------------------------------------------------------------------
# 	Copyright (C) 2017 Kenny Bravo Rodriguez <www.umsap.nl>

# 	This program is distributed for free in the hope that it will be useful,
# 	but WITHOUT ANY WARRANTY; without even the implied warranty of
# 	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

# 	See the accompaning licence for more details.
# ------------------------------------------------------------------------------


""" This module starts the application """


#region -------------------------------------------------------------- Imports
import os
import platform

import wx
import wx.adv
#endregion ----------------------------------------------------------- Imports


DEVELOPMENT = True # # To control variables with different values in dev or prod


class UmsapApp(wx.App):
	""" Start the UMSAP app """

	def OnInit(self):
		""" Initialize the app """

	 #--> Show SplashScreen
		cwd = os.path.abspath(os.path.dirname(__file__))
		cOS = platform.system()

		if cOS == 'Darwin':
			if DEVELOPMENT:
				image_loc = cwd + '/RESOURCES/IMAGES/SPLASHSCREEN/splash.png'
			else:
				image_loc = (
					cwd 
					+ '/UMSAP.app/Contents/Resources/IMAGES/SPLASHSCREEN/splash.png'
				)
		else:
			image_loc = cwd + '/RESOURCES/IMAGES/SPLASHSCREEN/splash.png'
		
		bitmap = wx.Bitmap(image_loc, type=wx.BITMAP_TYPE_PNG)
		
		SplashWindow(bitmap)
	 #---
	 #--> Return
		return True
	 #---
	#---
#---

class SplashWindow(wx.adv.SplashScreen):
	""" Create splash screen """

	def __init__(self, bitmap):
		""""""

		super().__init__(
			bitmap, 
			wx.adv.SPLASH_CENTER_ON_SCREEN|wx.adv.SPLASH_TIMEOUT,
			1000,
			None,	
		)

		self.Bind(wx.EVT_CLOSE, self.OnClose)

		self.Show()
	#---

	def OnClose(self, event):
		""" Finish app configuration """

	 #--> Imports
		import _thread
		from pathlib import Path

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
	 #--> Set special configuration values that require a running wx.App
	  #--> MenuBar
		if config.cOS == "Darwin":
			wx.MenuBar.MacSetCommonMenuBar(menu.MainMenuBar())
		else:
			pass
	  #---
	  #--> Configuration options
	   #--> Screen Size
		config.size["Screen"] = wx.GetDisplaySize()
	   #---
	  #---
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
	   #---
	   #--> Assign fonts
		config.font[config.name["LimProtRes"]] = config.font[config.name["TarProtRes"]]
	   #---
	  #---
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
			config.name['TarProt'] : menu.ToolsModule,
			config.name['LimProt'] : menu.ToolsModule,
			config.name['ProtProf']: menu.ToolsModule,			
			#--> Utilities
			config.name['MergeAA'] : menu.ToolsMergeAA,
			config.name['CorrA']   : menu.ToolsCorrAUtil,
			config.name['CorrARes']: menu.ToolsCorrARes,
			#--> Result windows
			config.name['TarProtRes']: menu.ToolsTarProtRes,
			config.name['LimProtRes']: menu.ToolsLimProtRes,
			config.name['CutPropRes']: menu.ToolsCutRes,
			config.name['HistoRes']  : menu.ToolsHistoRes,
			config.name['AAdistR']   : menu.ToolsAAdistRes,
			#--> Other windows
			config.name['TypeRes']   : menu.ToolsTypeResults,
		}
		config.pointer['dclasses']['DataObj'] = { # Data objects with name and file extension
			config.name['TarProtRes']	  : dclasses.DataObjTarProtFile,
			config.extShort['TarProt'][0] : dclasses.DataObjTarProtFile,
			config.name['CorrARes']	      : dclasses.DataObjCorrFile,
			config.extShort['CorrA'][0]	  : dclasses.DataObjCorrFile,
			config.name['CutPropRes']	  : dclasses.DataObjCutpropFile,
			config.extShort['CutProp'][0] : dclasses.DataObjCutpropFile,
			config.name['AAdistR']		  : dclasses.DataObjAAdistFile,
			config.extShort['AAdist'][0]  : dclasses.DataObjAAdistFile,
			config.name['HistoRes']	      : dclasses.DataObjHistFile,
			config.extShort['Histo'][0]   : dclasses.DataObjHistFile,
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
	  #---
	 #---
	 #--> Check for updates
		if config.general["checkUpdate"] == 1:
			_thread.start_new_thread(gmethods.UpdateCheck, ("main",))
		else:
			pass
	 #---
	 #--> Show the main frame & Return
		gmethods.WinMUCreate(config.name["Main"])
	 #---
	 #--> Destroy Splash Window
		self.Destroy()
	 #---
	 #-->
		return True
	 #---
	#---
#---

if __name__ == "__main__":
	app = UmsapApp()
	app.MainLoop()
else:
	pass

