#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 from "/home/ncq/Projekte/gm-cvs/branches/HEAD/gnumed/gnumed/client/wxg/wxgWaitingListEntryEditAreaPnl.wxg"

import wx

# begin wxGlade: extracode
# end wxGlade



class wxgWaitingListEntryEditAreaPnl(wx.ScrolledWindow):
    def __init__(self, *args, **kwds):

        from Gnumed.wxpython import gmPatSearchWidgets, gmWaitingListWidgets

        # begin wxGlade: wxgWaitingListEntryEditAreaPnl.__init__
        kwds["style"] = wx.NO_BORDER|wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self._PRW_patient = gmPatSearchWidgets.cPersonSearchCtrl(self, -1, "", style=wx.NO_BORDER)
        self._TCTRL_comment = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE|wx.TE_WORDWRAP|wx.NO_BORDER)
        self._PRW_zone = gmWaitingListWidgets.cWaitingZonePhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._SPCTRL_urgency = wx.SpinCtrl(self, -1, "0", min=0, max=10, style=wx.NO_BORDER)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: wxgWaitingListEntryEditAreaPnl.__set_properties
        self._PRW_patient.SetToolTipString(_("Waiting list details for this patient."))
        self._TCTRL_comment.SetToolTipString(_("What is the patient here for. Could be the Reason for Encounter."))
        self._TCTRL_comment.SetFocus()
        self._PRW_zone.SetToolTipString(_("Select or enter the zone the patient is waiting in."))
        self._SPCTRL_urgency.SetToolTipString(_("Select the urgency for this patient.\n\nDefault is 0. Range is 0-10.\nHigher values mean higher urgency."))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: wxgWaitingListEntryEditAreaPnl.__do_layout
        _gszr_main = wx.FlexGridSizer(3, 2, 3, 5)
        __szr_options = wx.BoxSizer(wx.HORIZONTAL)
        __lbl_patient = wx.StaticText(self, -1, _("Patient"))
        _gszr_main.Add(__lbl_patient, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(self._PRW_patient, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_comment = wx.StaticText(self, -1, _("Comment"))
        _gszr_main.Add(__lbl_comment, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(self._TCTRL_comment, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_options = wx.StaticText(self, -1, "")
        _gszr_main.Add(__lbl_options, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_zone = wx.StaticText(self, -1, _("&Zone:"))
        __szr_options.Add(__lbl_zone, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        __szr_options.Add(self._PRW_zone, 1, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 10)
        __lbl_urgency = wx.StaticText(self, -1, _("&Urgency:"))
        __szr_options.Add(__lbl_urgency, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        __szr_options.Add(self._SPCTRL_urgency, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_options.Add((20, 20), 1, wx.EXPAND, 0)
        _gszr_main.Add(__szr_options, 1, wx.EXPAND, 0)
        self.SetSizer(_gszr_main)
        _gszr_main.Fit(self)
        _gszr_main.AddGrowableRow(1)
        _gszr_main.AddGrowableCol(1)
        # end wxGlade

# end of class wxgWaitingListEntryEditAreaPnl


