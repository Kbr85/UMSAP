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
import _thread
import json
import webbrowser
from datetime import datetime
from pathlib import Path
from typing import Literal, Optional, Union, Callable

import matplotlib as mpl
import matplotlib.patches as patches
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

import wx
import wx.lib.mixins.listctrl as listmix

import config.config as config
import dtscore.check as dtsCheck
import dtscore.exception as dtsException
import dtscore.file as dtsFF
import dtscore.generator as dtsGenerator
import dtscore.window as dtsWindow
#endregion ----------------------------------------------------------> Imports


#region ------------------------------------------------------> Single widgets
class MatPlotPanel(wx.Panel):
    """Panel with a matplotlib plot.

        Parameters
        ----------
        parent : wx widget or none
            Parent of the panel
        dpi : int
            DPI for the plot. Default is 300
        statusbar : wx.StatusBar
            wx.StatusBar to display information about the graph
        statusMethod: callable or None
            Method to print information to the statusbar. The method should 
            accept only one parameter, the matplotlib event. Default is None.

        Attributes
        ----------
        axes: 
            Axes in the canvas.
        canvas : FigureCanvas
            Canvas in the panel.
        dpi : int
            DPI for the plot. Default is 300
        figure: mpl.Figure
            Figure in the panel
        statusbar : wx.StatusBar
            wx.StatusBar to display information about the graph
        finalX : float
            x coordinate in the plot scale when drag is over
        finalY : float
            y coordinate in the plot scale when drag is over
        initX : float
            x coordinate in the plot scale when left click is pressed
        initY : float
            y coordinate in the plot scale when left click is pressed
        zoomRect : mpl.patches.Rectangle or None
            Rectangle to show the zoom in area
        zoomReset : dict
            Cero zoom axes configuration. This will be used to reset the zoom 
            level. {'x' : (xmin, xmax), 'y': (ymin, ymax)}
        statusMethod: callable or None
            Method to print information to the statusbar. The method should 
            accept only one parameter, the matplotlib event. Default is None
    """
    #region -----------------------------------------------------> Class setup
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self, parent: wx.Window, dpi: Optional[int]=None, 
        statusbar: Optional[wx.StatusBar]=None, 
        statusMethod: Optional[Callable]=None
        ) -> None:
        """ """
        #region -----------------------------------------------> Initial Setup
        self.dpi          = 100 if dpi is None else dpi
        self.statusbar    = statusbar
        self.statusMethod = statusMethod
        self.initY        = None
        self.initX        = None
        self.finalX       = None
        self.finalY       = None
        self.zoomRect     = None
        self.zoomReset    = None
        self.cid          = []
        super().__init__(parent)
        #endregion --------------------------------------------> Initial Setup

        #region -----------------------------------------------------> Widgets
        self.figure  = mpl.figure.Figure(
            dpi          = self.dpi,
            figsize      = (2, 2),
            tight_layout = True,
        )
        self.axes    = self.figure.add_subplot(111)
        self.canvas  = FigureCanvas(self, -1, self.figure)
        self.axes.set_axisbelow(True)
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        self.sizerPlot = wx.BoxSizer(wx.HORIZONTAL)
        self.sizerPlot.Add(self.canvas, 1, wx.EXPAND|wx.ALL, 5)

        self.SetSizer(self.sizerPlot)
        self.sizerPlot.Fit(self)
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind
        self.ConnectEvent()
        #------------------------------> Keyboard shortcut
        #--------------> Accelerator entries
        accel = {
            'Zoom' : wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('Z'), wx.NewId()),
            'Img'  : wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('I'), wx.NewId()),
        }
        #--------------> Bind
        self.Bind(
            wx.EVT_MENU, self.ZoomResetPlot, id=accel['Zoom'].GetCommand())
        self.Bind(
            wx.EVT_MENU, self.OnSaveImage, id=accel['Img'].GetCommand())
        #--------------> Add 
        self.SetAcceleratorTable(
            wx.AcceleratorTable([x for x in accel.values()])
        )
        #endregion -----------------------------------------------------> Bind
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods
    def ConnectEvent(self) -> bool:
        """Connect or Disconnect all event handlers.
    
            Returns
            -------
            bool
        """
        #region -----------------------------------------------> Connect events
        self.cid.append(
            self.canvas.mpl_connect('motion_notify_event', self.OnMotionMouse)
        )
        self.cid.append(
            self.canvas.mpl_connect('button_press_event', self.OnPressMouse)
        )
        self.cid.append(
            self.canvas.mpl_connect('button_release_event', self.OnReleaseMouse)
        )
        self.cid.append(
            self.canvas.mpl_connect('key_press_event', self.OnKeyPress)
        )
        #endregion --------------------------------------------> Connect events
        
        return True
    #---
    
    def DisconnectEvent(self) -> bool:
        """Disconnect the event defined in ConnectEvent.
    
            Returns
            -------
            bool
        """
        #region --------------------------------------------------> Disconnect
        for k in self.cid:
            self.canvas.mpl_disconnect(k)
        #endregion -----------------------------------------------> Disconnect
        
        #region --------------------------------------------------> Reset list
        self.cid = []
        #endregion -----------------------------------------------> Reset list
        
        return True
    #---
    
    def GetAxesXY(self, event) -> tuple[float, float]:
        """"""
        x = event.xdata
        if getattr(self, 'axes2', None) is not None:
            _, y = self.axes.transData.inverted().transform((event.x,event.y))
        else:
            y = event.ydata
        
        return (x,y)
    #---
    
    #--------------------------------------------------------> Key press event
    def OnKeyPress(self, event) -> Literal[True]:
        """Process a key press event
    
            Parameter
            ---------
            event: mpl.KeyEvent
                Information about the mpl event
        """
        #region -------------------------------------------------------> Event
        if (tKey:= event.key) == 'escape':
            self.ZoomInAbort(event) 
        else:
            pass
        #endregion ----------------------------------------------------> Event

        return True
    #---

    #-----------------------------------------------------> Press mouse button
    def OnPressMouse(self, event) -> Literal[True]:
        """Process press mouse event
        
            Parameter
            ---------
            event: mpl.MouseEvent
                Information about the mpl event
        """
        #region -------------------------------------------------------> Event
        if event.inaxes:
            if event.button == 1:
                self.OnLeftClick(event)
            elif event.button == 3:
                self.OnRightClick(event)
            else:
                pass
        else:
            pass
        #endregion ----------------------------------------------------> Event
        
        return True
    #---

    def OnLeftClick(self, event) -> Literal[True]:
        """Process left click event. Override as needed.
            
            Parameters
            ----------
            event: mpl.MouseEvent
                Information about the mpl event
        """
        #region -------------------------------------------------------> Event
        self.initX, self.initY = self.GetAxesXY(event)
        #endregion ----------------------------------------------------> Event

        return True
    #---

    def OnRightClick(self, event) -> Literal[True]:
        """Process right click event. Override as needed
            
            Parameters
            ----------
            event: mpl.MouseEvent
                Information about the mpl event
        """
        return True
    #---

    #------------------------------------------------------> Move mouse button
    def OnMotionMouse(self, event) -> Literal[True]:
        """Handle move mouse event

            Parameters
            ----------
            event: mpl.MouseEvent
                Information about the mpl event
        """
        #region -------------------------------------------------------> Event
        if event.button == 1:
            self.DrawZoomRect(event)
        else:
            if self.statusbar is not None:
                self.UpdateStatusBar(event)
            else:
                pass        
        #endregion ----------------------------------------------------> Event
        
        return True
    #---

    def DrawZoomRect(self, event) -> bool:
        """Draw a rectangle to highlight area that will be zoomed in
    
            Parameters
            ----------
            event: mpl.MouseEvent
                Information about the mpl event
    
        """
        #region -----------------------------------------> Check event in axes
        if event.inaxes:
            pass
        else:
            return False
        #endregion --------------------------------------> Check event in axes

        #region -----------------------------------------> Initial coordinates
        if self.initX is None:
            self.initX, self.initY = self.GetAxesXY(event)
        else:
            pass
        #endregion --------------------------------------> Initial coordinates
        
        #region -------------------------------------------> Final coordinates
        self.finalX, self.finalY = self.GetAxesXY(event)
        #endregion ----------------------------------------> Final coordinates

        #region ------------------------------------> Delete & Create zoomRect
        #------------------------------> 
        if self.zoomRect is not None:
            self.zoomRect.remove()
        else:
            pass
        #------------------------------> 
        self.zoomRect = patches.Rectangle(
            (min(self.initX, self.finalX), min(self.initY, self.finalY)),
            abs(self.initX - self.finalX),
            abs(self.initY - self.finalY),
            fill      = False,
            linestyle = '--',
            linewidth = '0.5'
        )
        #endregion ---------------------------------> Delete & Create zoomRect

        #region --------------------------------------------------> Add & Draw
        self.axes.add_patch(
            self.zoomRect
        )
        self.canvas.draw()
        #endregion -----------------------------------------------> Add & Draw

        return True
    #---

    def UpdateStatusBar(self, event):
        """To update status bar. Basic functionality. Override as needed 
        
            Parameters
            ----------
            event: mpl.MouseEvent
                Information about the mpl event
        """
        #region -------------------------------------------------------> Event
        if event.inaxes:
            if self.statusMethod is not None:
                self.statusMethod(event)
            else:
                x,y = self.GetAxesXY(event)
                self.statusbar.SetStatusText(
                    f"x={x:.2f} y={y:.2f}"
                )
        else:
            self.statusbar.SetStatusText('') 
        #endregion ----------------------------------------------------> Event
        
        return True
    #---

    #---------------------------------------------------> Release mouse button
    def OnReleaseMouse(self, event) -> Literal[True]:
        """Process a release mouse event 
    
            Parameters
            ----------
            event: mpl.MouseEvent
                Information about the mpl event
        """
        #region ---------------------------------------------------> Event
        if event.button == 1:
            self.OnLeftRelease(event)
        elif event.button == 3:
            self.OnRightRelease(event)
        else:
            pass
        #endregion ------------------------------------------------> Event
        
        return True
    #---

    def OnLeftRelease(self, event) -> Literal[True]:
        """Process a left button release event
    
            Parameters
            ----------
            event: mpl.MouseEvent
                Information about the mpl event
        """
        #region -----------------------------------------------------> Zoom in
        if self.finalX is not None:
            self.axes.set_xlim(
                min(self.initX, self.finalX), 
                max(self.initX, self.finalX),
            )
            self.axes.set_ylim(
                min(self.initY, self.finalY), 
                max(self.initY, self.finalY),
            )
        else:
            return True
        #endregion --------------------------------------------------> Zoom in
        
        #region -----------------------------------> Reset initial coordinates
        self.initY  = None
        self.initX  = None
        self.finalX = None
        self.finalY = None
        #endregion --------------------------------> Reset initial coordinates
        
        #region --------------------------------------------> Delete zoom rect
        self.ZoomRectDelete()
        #endregion -----------------------------------------> Delete zoom rect
        
        return True
    #---

    def OnRightRelease(self, event) -> Literal[True]:
        """Process a right button release event. Override as needed.
    
            Parameters
            ----------
            event: mpl.MouseEvent
                Information about the mpl event
        """
        return True
    #---
    
    def OnSaveImage(self, event) -> bool:
        """
    
            Parameters
            ----------
            
    
            Returns
            -------
            
    
            Raise
            -----
            
        """
        return self.SaveImage(config.elMatPlotSaveI, parent=self, message=None)
    #---

    #---------------------------------------------------> Zoom related methods
    def ZoomResetSetValues(self) -> Literal[True]:
        """Set the axis limit in the cero zoom state. Should be called after all 
            initial plotting and axis configuration is done.
        
            Returns
            -------
            dict:
                {'x' : (xmin, xmax), 'y': (ymin, ymax)}
        """
        self.zoomReset = {'x': self.axes.get_xlim(), 'y': self.axes.get_ylim()}

        return True
    #---

    def ZoomResetPlot(
        self, event:Optional[wx.CommandEvent]=None) -> Literal[True]:
        """Reset the zoom level of the plot 
        
            Parameters
            ----------
            event: wx.Event or None
                To call from keyboard shortcut or as regular function
                
            Return
            ------
            True
        """
        #------------------------------> 
        self.axes.set_xlim(self.zoomReset['x'])
        self.axes.set_ylim(self.zoomReset['y'])
        self.canvas.draw()
        
        return True
    #---

    def ZoomInAbort(self, event) -> Literal[True]:
        """Abort a zoom in operation when Esc is pressed 
        
            Parameters
            ----------
            event: mpl.MouseEvent
                Information about the mpl event
        """
        #------------------------------> 
        self.initX  = None
        self.initY  = None
        self.finalX = None
        self.finalY = None
        #------------------------------> 
        self.ZoomRectDelete()
        #------------------------------> 
        self.UpdateStatusBar(event)
        
        return True
    #---

    def ZoomRectDelete(self) -> Literal[True]:
        """Delete the zoom in rectangle"""
        #region --------------------------------------------------------> Rect
        if self.zoomRect is not None:
            self.zoomRect.remove()
            self.canvas.draw()
            self.zoomRect = None
        else:
            pass        
        #endregion -----------------------------------------------------> Rect
        
        return True
    #---
    
    def SaveImage(
        self, ext: str, parent: Optional[wx.Window]=None, 
        message: Optional[str]=None
        ) -> Literal[True]:
        """Save image of the plot
    
            Parameters
            ----------
            ext : file extension
                wxPython extension spec
            parent : wx.Widget or None
                To center the save dialog. Default is None
            message : str or None
                Title for the save file window. Default is None
        """
        #region ------------------------------------------------------> Dialog
        dlg = dtsWindow.FileSelectDialog(
            'save',
            ext,
            parent  = parent,
            message = message,
        )
        #endregion ---------------------------------------------------> Dialog
        
        #region ----------------------------------------------------> Get Path
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            try:
                self.figure.savefig(path, dpi=self.dpi)
            except Exception:
                raise dtsException.ExecutionError(
                    f"The image of the plot could not be saved to file:\n"
                    f"{path}"
                )
        else:
            pass
        #endregion -------------------------------------------------> Get Path
        
        #region ---------------------------------------------------> Destroy
        dlg.Destroy()
        #endregion ------------------------------------------------> Destroy
        
        return True	
    #---
    #endregion ------------------------------------------------> Class methods
#---
#endregion ---------------------------------------------------> Single widgets


#region ---------------------------------------------------------> Mix widgets
class ListCtrlSearch():
    """Creates a wx.ListCtrl with a wx.SearchCtrl beneath it.
    
        See Notes below for more details

        Parameters
        ----------
        parent : wx widget or None
            Parent of the wx.ListCtrl
        listT : 0, 1 or 2
            Type of wx.ListCtrl. 
        setSizer : bool
            Arrange widgets in self.Sizer. Default is True.
        colLabel : list of str or None
            Label for the columns in the wx.ListCtrl
        colSize : list of int or None
            Width of the columns in the wx.ListCtrl
        canCopy : Boolean
            Row content can be copied. Default is True
        canCut : Boolean
            Row content can be copied and the selected rows deleted. 
            Default is False  
        canPaste : Boolean
            New rows can be added at the end of the list or after the last 
            selected row if nothing is selected.
        copyFullContent : Boolean
            Copy full rows's content or just rows's numbers. Default is False
        sep : str
            String used to join column numbers. Default is ','
        pasteUnique : Boolean
            Paste only new rows (True) silently discarding duplicate rows.
            Default is True
        selAll : Boolean
            Allow Ctr/Cmd+A to select all rows (True) or not (False). 
            For performance reasons this should not be used if 
            wx.EVT_LIST_ITEM_SELECTED is bound. Default is True.
        style : wx style specification
            Style of the wx.ListCtrl. Default is wx.LC_REPORT.
        data : list of list of str
            Data for the wx.ListCtrl when in virtual mode.
        color : str
            Row color for zebra style when wx.ListCtrl is in virtual mode.
        tcHint : str
            Hint for the wx.TextCtrl

        Attributes
        ----------
        listTDict: dict
            Keys are 0,1,2 and methods the class for the wx.ListCtrl.
        lc : wx.ListCtrl
        search : wx.SearchCtrl
    """
    #region -----------------------------------------------------> Class setup
    listTDict = {
        0: MyListCtrl,
        1: ListZebra,
        2: ListZebraMaxWidth,
    }
    #endregion --------------------------------------------------> Class setup

    #region --------------------------------------------------> Instance setup
    def __init__(
        self, parent: wx.Window, listT: int=1, setSizer=True, 
        color: str=config.color['Zebra'], colLabel: Optional[list[str]]=None, 
        colSize: Optional[list[int]]=None, canCopy: bool=True, 
        canCut: bool=False, canPaste: bool=False, copyFullContent: bool=False, 
        sep: str=' ', pasteUnique: bool=True, selAll: bool=True, 
        style=wx.LC_REPORT, data: list[list]=[], tcHint: str='',
        ) -> None:
        """ """
        #region -------------------------------------------------> Check Input
            
        #endregion ----------------------------------------------> Check Input

        #region -----------------------------------------------> Initial Setup
        
        #endregion --------------------------------------------> Initial Setup

        #region --------------------------------------------------------> Menu
        
        #endregion -----------------------------------------------------> Menu

        #region -----------------------------------------------------> Widgets
        #------------------------------> wx.ListCtrl
        self.lc = self.listTDict[listT](
            parent,
            color           = color,
            colLabel        = colLabel,
            colSize         = colSize,
            canCopy         = canCopy,
            canCut          = canCut,
            canPaste        = canPaste,
            copyFullContent = copyFullContent,
            sep             = sep,
            pasteUnique     = pasteUnique,
            selAll          = selAll,
            style           = style,
            data            = data,
        )
        #------------------------------> wx.SearchCtrl
        self.search = wx.SearchCtrl(parent)
        self.search.SetHint(tcHint) if tcHint != '' else ''
        #endregion --------------------------------------------------> Widgets

        #region ------------------------------------------------------> Sizers
        if setSizer:
            #------------------------------> 
            self.Sizer = wx.BoxSizer(orient=wx.VERTICAL)
            #------------------------------> 
            self.Sizer.Add(self.lc, 1, wx.EXPAND|wx.ALL, 5)
            self.Sizer.Add(self.search, 0, wx.EXPAND|wx.ALL, 5)
        else:
            pass
        #endregion ---------------------------------------------------> Sizers

        #region --------------------------------------------------------> Bind
        
        #endregion -----------------------------------------------------> Bind

        #region ---------------------------------------------> Window position
        
        #endregion ------------------------------------------> Window position
    #---
    #endregion -----------------------------------------------> Instance setup

    #region ---------------------------------------------------> Class methods

    #endregion ------------------------------------------------> Class methods
#---
#endregion ------------------------------------------------------> Mix widgets



