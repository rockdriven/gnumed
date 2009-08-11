#!/usr/bin/env python
# -*- coding: utf8 -*-
# generated by wxGlade 0.6.3 from "/home/ncq/Projekte/gm-cvs/branches/HEAD/gnumed/gnumed/client/wxg/wxgMeasurementTypeEAPnl.wxg"

import wx

# begin wxGlade: extracode
# end wxGlade



class wxgMeasurementTypeEAPnl(wx.ScrolledWindow):
    def __init__(self, *args, **kwds):

        from Gnumed.wxpython import gmPhraseWheel

        # begin wxGlade: wxgMeasurementTypeEAPnl.__init__
        kwds["style"] = wx.NO_BORDER|wx.TAB_TRAVERSAL
        wx.ScrolledWindow.__init__(self, *args, **kwds)
        self._PRW_name = gmPhraseWheel.cPhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._PRW_abbrev = gmPhraseWheel.cPhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._PRW_conversion_unit = gmPhraseWheel.cPhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._PRW_loinc = gmPhraseWheel.cPhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._TCTRL_loinc_info = wx.TextCtrl(self, -1, "", style=wx.TE_READONLY|wx.NO_BORDER)
        self._TCTRL_comment_type = wx.TextCtrl(self, -1, "", style=wx.NO_BORDER)
        self._PRW_test_org = gmPhraseWheel.cPhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._TCTRL_comment_org = wx.TextCtrl(self, -1, "", style=wx.NO_BORDER)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: wxgMeasurementTypeEAPnl.__set_properties
        self.SetScrollRate(10, 10)
        self._PRW_name.SetToolTipString(_("A descriptive name for this test type."))
        self._PRW_name.SetFocus()
        self._PRW_abbrev.SetToolTipString(_("An abbreviation for the name of this test type."))
        self._PRW_conversion_unit.SetToolTipString(_("The base unit to convert results from different labs into when comparing time series."))
        self._PRW_loinc.SetToolTipString(_("The LOINC code corresponding to this test type."))
        self._TCTRL_loinc_info.Enable(False)
        self._TCTRL_comment_type.SetToolTipString(_("A comment on this test type, e.g. pertaining to typical context information."))
        self._PRW_test_org.SetToolTipString(_("The path lab/diagnostic organisation reporting on this test."))
        self._TCTRL_comment_org.SetToolTipString(_("A comment on the organisation performing this measurement."))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: wxgMeasurementTypeEAPnl.__do_layout
        _gszr_main = wx.FlexGridSizer(6, 2, 1, 3)
        __szr_loinc = wx.BoxSizer(wx.HORIZONTAL)
        __szr_abbrev_unit = wx.BoxSizer(wx.HORIZONTAL)
        __lbl_name = wx.StaticText(self, -1, _("Name"))
        _gszr_main.Add(__lbl_name, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(self._PRW_name, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_abbrev = wx.StaticText(self, -1, _("Abbreviation"))
        _gszr_main.Add(__lbl_abbrev, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_abbrev_unit.Add(self._PRW_abbrev, 1, wx.RIGHT|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 10)
        __lbl_unit = wx.StaticText(self, -1, _("Unit"))
        __szr_abbrev_unit.Add(__lbl_unit, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        __szr_abbrev_unit.Add(self._PRW_conversion_unit, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(__szr_abbrev_unit, 1, wx.EXPAND, 0)
        __lbl_loinc = wx.StaticText(self, -1, _("LOINC"))
        _gszr_main.Add(__lbl_loinc, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_loinc.Add(self._PRW_loinc, 0, wx.RIGHT|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 10)
        __szr_loinc.Add(self._TCTRL_loinc_info, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(__szr_loinc, 1, wx.EXPAND, 0)
        __lbl_comment_type = wx.StaticText(self, -1, _("Comment"))
        _gszr_main.Add(__lbl_comment_type, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(self._TCTRL_comment_type, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __lbl_test_org = wx.StaticText(self, -1, _("Lab"))
        _gszr_main.Add(__lbl_test_org, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(self._PRW_test_org, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 10)
        __lbl_comment_org = wx.StaticText(self, -1, _("Comment"))
        _gszr_main.Add(__lbl_comment_org, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(self._TCTRL_comment_org, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        self.SetSizer(_gszr_main)
        _gszr_main.AddGrowableCol(1)
        # end wxGlade

# end of class wxgMeasurementTypeEAPnl


