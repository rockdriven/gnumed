#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 from "/home/ncq/Projekte/gm-cvs/branches/HEAD/gnumed/gnumed/client/wxg/wxgMeasurementOrgEAPnl.wxg"

import wx

# begin wxGlade: extracode
# end wxGlade



class wxgMeasurementOrgEAPnl(wx.ScrolledWindow):
    def __init__(self, *args, **kwds):

        from Gnumed.wxpython import gmMeasurementWidgets
        from Gnumed.wxpython.gmOrganizationWidgets import cOrgUnitPhraseWheel

        # begin wxGlade: wxgMeasurementOrgEAPnl.__init__
        kwds["style"] = wx.NO_BORDER|wx.TAB_TRAVERSAL
        wx.ScrolledWindow.__init__(self, *args, **kwds)
        self._PRW_org_unit = cOrgUnitPhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._BTN_manage_orgs = wx.Button(self, -1, _("&Manage orgs"), style=wx.BU_EXACTFIT)
        self._TCTRL_contact = wx.TextCtrl(self, -1, "", style=wx.NO_BORDER)
        self._TCTRL_comment = wx.TextCtrl(self, -1, "", style=wx.NO_BORDER)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self._on_manage_orgs_button_pressed, self._BTN_manage_orgs)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: wxgMeasurementOrgEAPnl.__set_properties
        self.SetScrollRate(10, 10)
        self._BTN_manage_orgs.SetToolTipString(_("Manage all organizations."))
        self._TCTRL_contact.SetToolTipString(_("A way of contacting this lab, ideally a direct clinical contact.\n\nThis will be shown in the tooltip of test results originating from this lab."))
        self._TCTRL_comment.SetToolTipString(_("A comment on this lab."))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: wxgMeasurementOrgEAPnl.__do_layout
        _gszr_main = wx.FlexGridSizer(3, 2, 1, 3)
        __szr_org_details = wx.BoxSizer(wx.HORIZONTAL)
        __lbl_org = wx.StaticText(self, -1, _("Org.Unit"))
        __lbl_org.SetForegroundColour(wx.Colour(255, 0, 0))
        _gszr_main.Add(__lbl_org, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_org_details.Add(self._PRW_org_unit, 1, wx.RIGHT|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5)
        __szr_org_details.Add(self._BTN_manage_orgs, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(__szr_org_details, 1, wx.EXPAND, 0)
        __lbl_contact = wx.StaticText(self, -1, _("Contact"))
        _gszr_main.Add(__lbl_contact, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(self._TCTRL_contact, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_comment = wx.StaticText(self, -1, _("Comment"))
        _gszr_main.Add(__lbl_comment, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(self._TCTRL_comment, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        self.SetSizer(_gszr_main)
        _gszr_main.Fit(self)
        _gszr_main.AddGrowableCol(1)
        # end wxGlade

    def _on_manage_orgs_button_pressed(self, event): # wxGlade: wxgMeasurementOrgEAPnl.<event_handler>
        print "Event handler `_on_manage_orgs_button_pressed' not implemented"
        event.Skip()

# end of class wxgMeasurementOrgEAPnl


