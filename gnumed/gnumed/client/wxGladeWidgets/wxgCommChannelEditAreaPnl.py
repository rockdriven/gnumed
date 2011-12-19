#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.5 on Sun Dec  2 21:43:06 2007 from /home/ncq/Projekte/gm-cvs/branches/HEAD/gnumed/gnumed/client/wxg/wxgCommChannelEditAreaPnl.wxg

import wx

class wxgCommChannelEditAreaPnl(wx.ScrolledWindow):
    def __init__(self, *args, **kwds):

        from Gnumed.wxpython import gmAddressWidgets
        from Gnumed.wxpython import gmContactWidgets

        # begin wxGlade: wxgCommChannelEditAreaPnl.__init__
        kwds["style"] = wx.NO_BORDER|wx.TAB_TRAVERSAL
        wx.ScrolledWindow.__init__(self, *args, **kwds)
        self._PRW_type = gmContactWidgets.cCommChannelTypePhraseWheel(self, -1, "", style=wx.NO_BORDER)
        self._TCTRL_url = wx.TextCtrl(self, -1, "", style=wx.NO_BORDER)
        self._TCTRL_comment = wx.TextCtrl(self, -1, "", style=wx.NO_BORDER)
        self._CHBOX_confidential = wx.CheckBox(self, -1, _("Confidential"))

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: wxgCommChannelEditAreaPnl.__set_properties
        self.SetScrollRate(10, 10)
        self._TCTRL_url.SetToolTipString(_("Enter the address or number for this communications channel here."))
        self._TCTRL_comment.SetToolTipString(_("A comment on this communications channel."))
        self._CHBOX_confidential.SetToolTipString(_("Check this if the communications channel is to be treated confidentially."))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: wxgCommChannelEditAreaPnl.__do_layout
        _gszr_main = wx.FlexGridSizer(4, 2, 3, 5)
        __LBL_type = wx.StaticText(self, -1, _("Channel"))
        _gszr_main.Add(__LBL_type, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(self._PRW_type, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __LBL_url = wx.StaticText(self, -1, _("Value"))
        _gszr_main.Add(__LBL_url, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(self._TCTRL_url, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __LBL_comment = wx.StaticText(self, -1, _("Comment"))
        _gszr_main.Add(__LBL_comment, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(self._TCTRL_comment, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __LBL_options = wx.StaticText(self, -1, "")
        _gszr_main.Add(__LBL_options, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        _gszr_main.Add(self._CHBOX_confidential, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        self.SetSizer(_gszr_main)
        _gszr_main.Fit(self)
        _gszr_main.AddGrowableCol(1)
        # end wxGlade

# end of class wxgCommChannelEditAreaPnl


