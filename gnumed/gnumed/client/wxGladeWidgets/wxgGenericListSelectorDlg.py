#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.5 on Tue Jun 12 19:31:26 2007 from /home/ncq/Projekte/gm-cvs/branches/HEAD/gnumed/gnumed/client/wxg/wxgGenericListSelectorDlg.wxg

import wx

class wxgGenericListSelectorDlg(wx.Dialog):
    def __init__(self, *args, **kwds):

        from Gnumed.wxpython import gmListWidgets

        # begin wxGlade: wxgGenericListSelectorDlg.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX|wx.THICK_FRAME
        wx.Dialog.__init__(self, *args, **kwds)
        self._LBL_message = wx.StaticText(self, -1, "")
        self._LCTRL_items = gmListWidgets.cReportListCtrl(self, -1, style=wx.LC_REPORT|wx.NO_BORDER)
        self._BTN_ok = wx.Button(self, wx.ID_OK, "")
        self._BTN_cancel = wx.Button(self, wx.ID_CANCEL, "")
        self._BTN_edit = wx.Button(self, -1, _("Edit"))

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self._on_list_item_deselected, self._LCTRL_items)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self._on_list_item_selected, self._LCTRL_items)
        self.Bind(wx.EVT_BUTTON, self._on_edit_button_pressed, self._BTN_edit)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: wxgGenericListSelectorDlg.__set_properties
        self.SetSize((400, 500))
        self._LCTRL_items.SetToolTipString(_("Mark the items you want to work on with <SPACE>."))
        self._LCTRL_items.SetFocus()
        self._BTN_ok.SetToolTipString(_("Act on the items selected in the above list."))
        self._BTN_ok.Enable(False)
        self._BTN_cancel.SetToolTipString(_("Cancel this dialog."))
        self._BTN_cancel.SetDefault()
        self._BTN_edit.SetToolTipString(_("Edit the (first or only) item selected in the list above."))
        self._BTN_edit.Enable(False)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: wxgGenericListSelectorDlg.__do_layout
        __szr_main = wx.BoxSizer(wx.VERTICAL)
        __szr_buttons = wx.BoxSizer(wx.HORIZONTAL)
        __szr_main.Add(self._LBL_message, 0, wx.LEFT|wx.RIGHT|wx.TOP|wx.EXPAND, 3)
        __szr_main.Add(self._LCTRL_items, 1, wx.ALL|wx.EXPAND, 3)
        __szr_buttons.Add((20, 20), 1, wx.EXPAND|wx.ADJUST_MINSIZE, 0)
        __szr_buttons.Add(self._BTN_ok, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
        __szr_buttons.Add((20, 20), 1, wx.EXPAND|wx.ADJUST_MINSIZE, 0)
        __szr_buttons.Add(self._BTN_cancel, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
        __szr_buttons.Add((20, 20), 2, wx.EXPAND|wx.ADJUST_MINSIZE, 0)
        __szr_buttons.Add(self._BTN_edit, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_buttons.Add((20, 20), 1, wx.EXPAND|wx.ADJUST_MINSIZE, 0)
        __szr_main.Add(__szr_buttons, 0, wx.ALL|wx.EXPAND, 3)
        self.SetSizer(__szr_main)
        self.Layout()
        self.Centre()
        # end wxGlade

    def _on_list_item_deselected(self, event): # wxGlade: wxgGenericListSelectorDlg.<event_handler>
        print "Event handler `_on_list_item_deselected' not implemented!"
        event.Skip()

    def _on_list_item_selected(self, event): # wxGlade: wxgGenericListSelectorDlg.<event_handler>
        print "Event handler `_on_list_item_selected' not implemented!"
        event.Skip()

    def _on_ok_button_pressed(self, event): # wxGlade: wxgGenericListSelectorDlg.<event_handler>
        print "Event handler `_on_ok_button_pressed' not implemented!"
        event.Skip()

    def _on_edit_button_pressed(self, event): # wxGlade: wxgGenericListSelectorDlg.<event_handler>
        print "Event handler `_on_edit_button_pressed' not implemented"
        event.Skip()

# end of class wxgGenericListSelectorDlg


if __name__ == "__main__":
    import gettext
    gettext.install("app") # replace with the appropriate catalog name

    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    dialog_1 = wxgGenericListSelectorDlg(None, -1, "")
    app.SetTopWindow(dialog_1)
    dialog_1.Show()
    app.MainLoop()
