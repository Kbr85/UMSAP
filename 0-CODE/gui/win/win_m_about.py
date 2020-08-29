# ------------------------------------------------------------------------------
#	Copyright (C) 2017 Kenny Bravo Rodriguez <www.umsap.nl>
	
#	This program is distributed for free in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
	
#	See the accompaning licence for more details.
# ------------------------------------------------------------------------------


""" This module creates the about window of the app """


#region -------------------------------------------------------------- Imports
import wx
import wx.lib.agw.hyperlink as hl

import config.config   as config
import gui.gui_classes as gclasses
#endregion ----------------------------------------------------------- Imports


class WinAbout(gclasses.WinMyFrame):
	""" Creates the about window """

	#region --------------------------------------------------- Instance Setup
	def __init__(self, parent=None, style=None):
		""" parent: parent for the widgets
			style: style of the windows
		"""
	 #--> Initial Setup
		self.name = config.name['About']
		super().__init__(parent=parent, style=style)
	 #---
	 #--> Widgets
	  #--> Images
		self.img = wx.StaticBitmap(self.panel, wx.ID_ANY, 
			wx.Bitmap(str(config.image['About']), wx.BITMAP_TYPE_ANY))
	  #---
	  #--> Lines
		self.lineHI1 = wx.StaticLine(self.panel)
		self.lineHI2 = wx.StaticLine(self.panel)
		self.lineHI3 = wx.StaticLine(self.panel)
	  #---
	  #--> StaticText
		self.text1 = wx.StaticText(self.panel,
			label='Copyright © 2017 Kenny Bravo Rodriguez')
	  #---
	  #--> TextCtrl
		self.MyText = wx.TextCtrl(self.panel, size=(100, 500), 
			style=wx.TE_MULTILINE|wx.TE_WORDWRAP|wx.TE_READONLY)
	  #---
	  #--> Button
		self.buttonOk = wx.Button(self.panel, label='Ok')
	  #---
	  #--> hl
		self.lnk = hl.HyperLinkCtrl(self.panel, -1, config.url['Home'], 
			URL=config.url['Home'])
	  #---
	 #---
	 #--> Sizers
	  #--> Add
		self.sizerIN.Add(self.img,      pos=(0, 0), border=2, span=(0, 2), 
			flag=wx.ALIGN_CENTER|wx.ALL)
		self.sizerIN.Add(self.lineHI1,  pos=(1, 0), border=2, span=(0, 2), 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerIN.Add(self.text1,    pos=(2, 0), border=2, span=(0, 2), 
			flag=wx.ALIGN_CENTER|wx.ALL)
		self.sizerIN.Add(self.lineHI2,  pos=(3, 0), border=2, span=(0, 2), 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerIN.Add(self.MyText,   pos=(4, 0), border=2, span=(0, 2), 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerIN.Add(self.lineHI3,  pos=(5, 0), border=2, span=(0, 2), 
			flag=wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		self.sizerIN.Add(self.lnk,      pos=(6, 0), border=2, 
			flag=wx.ALIGN_LEFT|wx.EXPAND|wx.ALL)
		self.sizerIN.Add(self.buttonOk, pos=(6, 1), border=2, 
			flag=wx.ALIGN_RIGHT|wx.ALL)
	  #---
	  #--> Fit
		self.sizer.Fit(self)
	  #---
	 #---
	 #--> Add Text
		#---# Improve (DOWN) read from file?
		self.MyText.AppendText(myText)
		self.MyText.SetInsertionPoint(0)
		self.buttonOk.SetFocus()
		#---# Improve (UP) read from file?
	 #---
	 #--> Position
		self.Center()
	 #---
	 #--> Binding
		self.buttonOk.Bind(wx.EVT_BUTTON, self.OnButtonClose)
	 #---
	 #--> Show
		self.Show()
	 #---
	#---
	#endregion ------------------------------------------------ Instance Setup
	
	# ------------------------------------------------------------- My Methods
	def OnButtonClose(self, event):
		""" To close the window """
		self.Close()
		return True
	#---
#---

myText = """UMSAP: Fast post-processing of mass spectrometry data 

-- Modules and Python version --

UMSAP 2.1.0 (beta) is written in Python 3.7.1 and uses the following modules:

Biopython 1.73  
pyFPDF 1.7.2 
Python 3.7.1
Matplotlib 3.0.2 
NumPy 1.16.1
Pandas 0.24.2   
PyInstaller 3.4 
Requests 2.21.0 
Scipy 1.2.0 
Statsmodels 0.9.0
wxPython 4.0.4

Copyright notice and License for the modules can be found in the User's manual of UMSAP.

-- Acknowledgments --

I would like to thank all the persons that have contributed to the development 
of UMSAP, either by contributing ideas and suggestions or by testing the code. 
Special thanks go to: Dr. Farnusch Kaschani, Dr. Juliana Rey, Dr. Petra Janning 
and Prof. Dr. Daniel Hoffmann.

In particular, I would like to thank Prof. Dr. Michael Ehrmann for the support and 
useful discussions during my postdoc stay in his group at the University of Duisburg-Essen.

-- License Agreement --

Utilities for Mass Spectrometry Analysis of Proteins and its source code are governed by the following license:

Upon execution of this Agreement by the party identified below (”Licensee”), Kenny Bravo Rodriguez (KBR) will provide the Utilities for Mass Spectrometry Analysis of Proteins software in Executable Code and/or Source Code form (”Software”) to Licensee, subject to the following terms and conditions. For purposes of this Agreement, Executable Code is the compiled code, which is ready to run on Licensee’s computer. Source code consists of a set of files, which contain the actual program commands that are compiled to form the Executable Code.

1. The Software is intellectual property owned by KBR, and all rights, title and interest, including copyright, remain with KBR. KBR grants, and Licensee hereby accepts, a restricted, non-exclusive, non-transferable license to use the Software for academic, research and internal business purposes only, e.g. not for commercial use (see Clause 7 below), without a fee.

2. Licensee may, at its own expense, create and freely distribute complimentary works that inter-operate with the Software, directing others to the Utilities for Mass Spectrometry Analysis of Proteins web page to license and obtain the Software itself. Licensee may, at its own expense, modify the Software to make derivative works. Except as explicitly provided below, this License shall apply to any derivative work as it does to the original Software distributed by KBR. Any derivative work should be clearly marked and renamed to notify users that it is a modified version and not the original Software distributed by KBR. Licensee agrees to reproduce the copyright notice and other proprietary markings on any derivative work and to include in the documentation of such work the acknowledgment: ”This software includes code developed by Kenny Bravo Rodriguez for the Utilities for Mass Spectrometry Analysis of Proteins software”.
Licensee may not sell any derivative work based on the Software under any circumstance. For commercial distribution of the Software or any derivative work based on the Software a separate license is required. Licensee may contact KBR to negotiate an appropriate license for such distribution.

3. Except as expressly set forth in this Agreement, THIS SOFTWARE IS PROVIDED ”AS IS” AND KBR MAKES NO REPRESENTATIONS AND EXTENDS NO WAR- RANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO WARRANTIES OR MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE, OR THAT THE USE OF THE SOFTWARE WILL NOT INFRINGE ANY PATENT, TRADEMARK, OR OTHER RIGHTS. LICENSEE AS- SUMES THE ENTIRE RISK AS TO THE RESULTS AND PERFORMANCE OF THE SOFTWARE AND/OR ASSOCIATED MATERIALS. LICENSEE AGREES THAT KBR SHALL NOT BE HELD LIABLE FOR ANY DIRECT, INDIRECT, CONSE- QUENTIAL, OR INCIDENTAL DAMAGES WITH RESPECT TO ANY CLAIM BY LICENSEE OR ANY THIRD PARTY ON ACCOUNT OF OR ARISING FROM THIS AGREEMENT OR USE OF THE SOFTWARE AND/OR ASSOCIATED MATERIALS.

4. Licensee understands the Software is proprietary to KBR. Licensee agrees to take all reasonable steps to insure that the Software is protected and secured from unauthorized disclosure, use, or release and will treat it with at least the same level of care as Licensee would use to protect and secure its own proprietary computer programs and/or information, but using no less than a reasonable standard of care. Licensee agrees to provide the Software only to any other person or entity who has registered with KBR. If Licensee is not registering as an individual but as an institution or corporation each member of the institution or corporation who has access to or uses Software must agree to and abide by the terms of this license. If Licensee becomes aware of any unauthorized licensing, copying or use of the Software, Licensee shall promptly notify KBR in writing. Licensee expressly agrees to use the Software only in the manner and for the specific uses authorized in this Agreement.

5. KBR shall have the right to terminate this license immediately by written notice upon Licensee’s breach of, or non-compliance with, any terms of the license. Licensee may be held legally responsible for any copyright infringement that is caused or encouraged by its failure to abide by the terms of this license. Upon termination, Licensee agrees to destroy all copies of the Software in its possession and to verify such destruction in writing.

6. Licensee agrees that any reports or published results obtained with the Software will acknowledge its use by the appropriate citation as follows:
”Utilities for Mass Spectrometry Analysis of Proteins was created by Kenny Bravo Rodriguez at the University of Duisburg-Essen and is currently developed at the Max Planck Institute of Molecular Physiology.”
Any published work, which utilizes Utilities for Mass Spectrometry Analysis of Proteins, shall include the following reference:
Kenny Bravo-Rodriguez, Birte Hagemeier, Lea Drescher, Marian Lorenz, Michael Meltzer, Farnusch Kaschani, Markus Kaiser and Michael Ehrmann. (2018). Utilities for Mass Spectrometry Analysis of Proteins (UMSAP): Fast post-processing of mass spectrometry data. Rapid Communications in Mass Spectrometry, 32(19), 1659–1667.
Electronic documents will include a direct link to the official Utilities for Mass Spec- trometry Analysis of Proteins page at: www.umsap.nl

7. Commercial use of the Software, or derivative works based thereon, REQUIRES A COMMERCIAL LICENSE. Should Licensee wish to make commercial use of the Software, Licensee will contact KBR to negotiate an appropriate license for such use. Commercial use includes: (1) integration of all or part of the Software into a product for sale, lease or license by or on behalf of Licensee to third parties, or (2) distribution of the Software to third parties that need it to commercialize product sold or licensed by or on behalf of Licensee.

8. Utilities for Mass Spectrometry Analysis of Proteins is being distributed as a research tool and as such, KBR encourages contributions from users of the code that might, at KBR’s sole discretion, be used or incorporated to make the basic operating framework of the Software a more stable, flexible, and/or useful product. Licensees who contribute their code to become an internal portion of the Software agree that such code may be distributed by KBR under the terms of this License and may be required to sign an ”Agreement Regarding Contributory Code for Utilities for Mass Spectrometry Analysis of Proteins Software” before KBR can accept it (contact umsap@umsap.nl for a copy).

UNDERSTOOD AND AGREED.

Contact Information:

The best contact path for licensing issues is by e-mail to umsap@umsap.nl
"""






