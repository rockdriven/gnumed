# -*- coding: UTF-8 -*-
#
# generated by wxGlade
#

import wx

# begin wxGlade: dependencies
import gettext
# end wxGlade

# begin wxGlade: extracode
from Gnumed.wxpython.gmCodingWidgets import cDataSourcePhraseWheel
# end wxGlade


class wxgBillableEAPnl(wx.ScrolledWindow):
	def __init__(self, *args, **kwds):
		# begin wxGlade: wxgBillableEAPnl.__init__
		kwds["style"] = kwds.get("style", 0) | wx.BORDER_NONE | wx.TAB_TRAVERSAL
		wx.ScrolledWindow.__init__(self, *args, **kwds)
		self._TCTRL_code = wx.TextCtrl(self, wx.ID_ANY, "")
		self._PRW_coding_system = cDataSourcePhraseWheel(self, wx.ID_ANY, "")
		self._TCTRL_description = wx.TextCtrl(self, wx.ID_ANY, "")
		self._TCTRL_amount = wx.TextCtrl(self, wx.ID_ANY, "")
		self._TCTRL_currency = wx.TextCtrl(self, wx.ID_ANY, "")
		self._TCTRL_vat = wx.TextCtrl(self, wx.ID_ANY, "")
		self._TCTRL_comment = wx.TextCtrl(self, wx.ID_ANY, "")
		self._CHBOX_active = wx.CheckBox(self, wx.ID_ANY, _("&Active"))

		self.__set_properties()
		self.__do_layout()
		# end wxGlade

	def __set_properties(self):
		# begin wxGlade: wxgBillableEAPnl.__set_properties
		self.SetScrollRate(10, 10)
		self._TCTRL_code.SetToolTip(_("Mandatory: A code for this billable."))
		self._PRW_coding_system.SetToolTip(_("Mandatory: The system of billing codes this billable comes from."))
		self._TCTRL_description.SetToolTip(_("Mandatory: A description of this billable."))
		self._TCTRL_amount.SetToolTip(_("The payable amount associated with this billable.\nDefaults to 0."))
		self._TCTRL_currency.SetToolTip(_(u"The currency to apply to this billable.\nDefaults to \u20ac."))
		self._TCTRL_vat.SetToolTip(_("Value Added Tax (VAT) in percent to apply to this billable.\nDefaults to 0 meaning \"no VAT\"."))
		self._TCTRL_comment.SetToolTip(_("Optional: A comment on this billable."))
		self._CHBOX_active.SetToolTip(_("Check here if this billable is active."))
		self._CHBOX_active.SetValue(1)
		# end wxGlade

	def __do_layout(self):
		# begin wxGlade: wxgBillableEAPnl.__do_layout
		_gszr_main = wx.FlexGridSizer(5, 2, 1, 3)
		__szr_amount_details = wx.BoxSizer(wx.HORIZONTAL)
		__szr_code_details = wx.BoxSizer(wx.HORIZONTAL)
		__lbl_code = wx.StaticText(self, wx.ID_ANY, _("Code"))
		__lbl_code.SetForegroundColour(wx.Colour(255, 0, 0))
		_gszr_main.Add(__lbl_code, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		__szr_code_details.Add(self._TCTRL_code, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.RIGHT, 5)
		__lbl_system = wx.StaticText(self, wx.ID_ANY, _("System"))
		__lbl_system.SetForegroundColour(wx.Colour(255, 0, 0))
		__szr_code_details.Add(__lbl_system, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 3)
		__szr_code_details.Add(self._PRW_coding_system, 2, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
		_gszr_main.Add(__szr_code_details, 1, wx.EXPAND, 0)
		__lbl_description = wx.StaticText(self, wx.ID_ANY, _("Description"))
		__lbl_description.SetForegroundColour(wx.Colour(255, 0, 0))
		_gszr_main.Add(__lbl_description, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		_gszr_main.Add(self._TCTRL_description, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
		__lbl_value = wx.StaticText(self, wx.ID_ANY, _("Value"))
		__lbl_value.SetForegroundColour(wx.Colour(255, 127, 0))
		_gszr_main.Add(__lbl_value, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		__szr_amount_details.Add(self._TCTRL_amount, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.RIGHT, 5)
		__lbl_currency = wx.StaticText(self, wx.ID_ANY, _("Currency"))
		__lbl_currency.SetForegroundColour(wx.Colour(255, 127, 0))
		__szr_amount_details.Add(__lbl_currency, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 3)
		__szr_amount_details.Add(self._TCTRL_currency, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.RIGHT, 5)
		__lbl_vat = wx.StaticText(self, wx.ID_ANY, _("VAT"))
		__lbl_vat.SetForegroundColour(wx.Colour(255, 127, 0))
		__szr_amount_details.Add(__lbl_vat, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 3)
		__szr_amount_details.Add(self._TCTRL_vat, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.RIGHT, 3)
		__lbl_percent = wx.StaticText(self, wx.ID_ANY, _("%"))
		__szr_amount_details.Add(__lbl_percent, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		_gszr_main.Add(__szr_amount_details, 1, wx.EXPAND, 0)
		__lbl_comment = wx.StaticText(self, wx.ID_ANY, _("Comment"))
		_gszr_main.Add(__lbl_comment, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		_gszr_main.Add(self._TCTRL_comment, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
		__lbl_status = wx.StaticText(self, wx.ID_ANY, _("Status"))
		_gszr_main.Add(__lbl_status, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		_gszr_main.Add(self._CHBOX_active, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		self.SetSizer(_gszr_main)
		_gszr_main.Fit(self)
		_gszr_main.AddGrowableCol(1)
		self.Layout()
		# end wxGlade

# end of class wxgBillableEAPnl
