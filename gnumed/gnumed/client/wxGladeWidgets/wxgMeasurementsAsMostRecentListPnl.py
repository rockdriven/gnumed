# -*- coding: UTF-8 -*-
#
# generated by wxGlade
#

import wx

# begin wxGlade: dependencies
import gettext
# end wxGlade

# begin wxGlade: extracode
from Gnumed.wxpython.gmListWidgets import cReportListCtrl
# end wxGlade


class wxgMeasurementsAsMostRecentListPnl(wx.Panel):
	def __init__(self, *args, **kwds):
		# begin wxGlade: wxgMeasurementsAsMostRecentListPnl.__init__
		kwds["style"] = kwds.get("style", 0) | wx.BORDER_NONE | wx.TAB_TRAVERSAL
		wx.Panel.__init__(self, *args, **kwds)
		from Gnumed.wxpython.gmMeasurementWidgets import cTestPanelPRW
		self._PRW_panel = cTestPanelPRW(self, wx.ID_ANY, "")
		self._TCTRL_panel_comment = wx.TextCtrl(self, wx.ID_ANY, "")
		self._BTN_manage_panels = wx.Button(self, wx.ID_ANY, _("Manage"), style=wx.BU_EXACTFIT)
		self._LCTRL_results = cReportListCtrl(self, wx.ID_ANY, style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES)
		self._TCTRL_details = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_BESTWRAP | wx.TE_MULTILINE | wx.TE_READONLY)

		self.__set_properties()
		self.__do_layout()

		self.Bind(wx.EVT_BUTTON, self._on_manage_panels_button_pressed, self._BTN_manage_panels)
		# end wxGlade

	def __set_properties(self):
		# begin wxGlade: wxgMeasurementsAsMostRecentListPnl.__set_properties
		self._TCTRL_panel_comment.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BACKGROUND))
		self._TCTRL_panel_comment.Enable(False)
		self._BTN_manage_panels.SetToolTip(_("Manage test panels."))
		# end wxGlade

	def __do_layout(self):
		# begin wxGlade: wxgMeasurementsAsMostRecentListPnl.__do_layout
		__szr_main = wx.BoxSizer(wx.VERTICAL)
		__szr_bottom = wx.BoxSizer(wx.HORIZONTAL)
		__szr_panel_options = wx.BoxSizer(wx.HORIZONTAL)
		__lbl_display = wx.StaticText(self, wx.ID_ANY, _("&Panel:"))
		__szr_panel_options.Add(__lbl_display, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
		__szr_panel_options.Add(self._PRW_panel, 2, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
		__szr_panel_options.Add(self._TCTRL_panel_comment, 3, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
		__szr_panel_options.Add(self._BTN_manage_panels, 0, wx.ALIGN_CENTER_VERTICAL, 5)
		__szr_main.Add(__szr_panel_options, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 5)
		__szr_bottom.Add(self._LCTRL_results, 5, wx.EXPAND | wx.RIGHT, 3)
		__szr_bottom.Add(self._TCTRL_details, 4, wx.EXPAND, 0)
		__szr_main.Add(__szr_bottom, 1, wx.ALL | wx.EXPAND, 5)
		self.SetSizer(__szr_main)
		__szr_main.Fit(self)
		self.Layout()
		# end wxGlade

	def _on_manage_panels_button_pressed(self, event):  # wxGlade: wxgMeasurementsAsMostRecentListPnl.<event_handler>
		print("Event handler '_on_manage_panels_button_pressed' not implemented!")
		event.Skip()

# end of class wxgMeasurementsAsMostRecentListPnl
