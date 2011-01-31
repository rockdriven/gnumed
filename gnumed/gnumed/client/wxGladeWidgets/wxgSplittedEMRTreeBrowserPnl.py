#!/usr/bin/env python
# -*- coding: ISO-8859-15 -*-
# generated by wxGlade 0.4cvs on Sun May 28 15:57:29 2006

import wx

class wxgSplittedEMRTreeBrowserPnl(wx.Panel):

    def __init__(self, *args, **kwds):

        from Gnumed.wxpython import gmEMRBrowser
        from Gnumed.wxpython import gmNarrativeWidgets

        # begin wxGlade: wxgSplittedEMRTreeBrowserPnl.__init__
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self._splitter_browser = wx.SplitterWindow(self, -1, style=wx.SP_3D|wx.SP_BORDER)
        self.__pnl_right_side = wx.Panel(self._splitter_browser, -1, style=wx.NO_BORDER)
        self.__pnl_left_side = wx.Panel(self._splitter_browser, -1, style=wx.NO_BORDER|wx.TAB_TRAVERSAL)
        self._pnl_emr_tree = gmEMRBrowser.cScrolledEMRTreePnl(self.__pnl_left_side, -1, style=wx.NO_BORDER|wx.TAB_TRAVERSAL)
        self._RBTN_details = wx.RadioButton(self.__pnl_right_side, -1, _("Details"))
        self._RBTN_journal = wx.RadioButton(self.__pnl_right_side, -1, _("Journal"))
        self._TCTRL_item_details = wx.TextCtrl(self.__pnl_right_side, -1, "", style=wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL|wx.TE_WORDWRAP|wx.NO_BORDER)
        self._PNL_visual_soap = gmNarrativeWidgets.cVisualSoapPresenterPnl(self.__pnl_right_side, -1, style=wx.NO_BORDER)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_RADIOBUTTON, self._on_show_details_selected, self._RBTN_details)
        self.Bind(wx.EVT_RADIOBUTTON, self._on_show_journal_selected, self._RBTN_journal)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: wxgSplittedEMRTreeBrowserPnl.__set_properties
        self._pnl_emr_tree.SetScrollRate(10, 10)
        self._RBTN_details.SetToolTipString(_("Show formatted item details."))
        self._RBTN_details.SetValue(1)
        self._RBTN_journal.SetToolTipString(_("Show item journal."))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: wxgSplittedEMRTreeBrowserPnl.__do_layout
        __szr_main = wx.BoxSizer(wx.HORIZONTAL)
        __szr_right_side = wx.BoxSizer(wx.VERTICAL)
        __szr_item_details_options = wx.BoxSizer(wx.HORIZONTAL)
        __szr_left_side = wx.BoxSizer(wx.VERTICAL)
        __szr_left_side.Add(self._pnl_emr_tree, 1, wx.EXPAND, 0)
        self.__pnl_left_side.SetSizer(__szr_left_side)
        __lbl_show_mode = wx.StaticText(self.__pnl_right_side, -1, _("Show:"))
        __szr_item_details_options.Add(__lbl_show_mode, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        __szr_item_details_options.Add(self._RBTN_details, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        __szr_item_details_options.Add(self._RBTN_journal, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_item_details_options.Add((20, 20), 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_right_side.Add(__szr_item_details_options, 0, wx.EXPAND, 0)
        __szr_right_side.Add(self._TCTRL_item_details, 1, wx.TOP|wx.EXPAND, 3)
        __szr_right_side.Add(self._PNL_visual_soap, 0, wx.EXPAND, 0)
        self.__pnl_right_side.SetSizer(__szr_right_side)
        self._splitter_browser.SplitVertically(self.__pnl_left_side, self.__pnl_right_side)
        __szr_main.Add(self._splitter_browser, 1, wx.EXPAND, 0)
        self.SetSizer(__szr_main)
        __szr_main.Fit(self)
        # end wxGlade

    def _on_show_details_selected(self, event): # wxGlade: wxgSplittedEMRTreeBrowserPnl.<event_handler>
        print "Event handler `_on_show_details_selected' not implemented"
        event.Skip()

    def _on_show_journal_selected(self, event): # wxGlade: wxgSplittedEMRTreeBrowserPnl.<event_handler>
        print "Event handler `_on_show_journal_selected' not implemented"
        event.Skip()

# end of class wxgSplittedEMRTreeBrowserPnl

