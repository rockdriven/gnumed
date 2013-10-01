#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 from "/home/ncq/Projekte/gm-cvs/branches/HEAD/gnumed/gnumed/client/wxg/wxgProviderInboxPnl.wxg"

import wx

# begin wxGlade: extracode
# end wxGlade



class wxgProviderInboxPnl(wx.ScrolledWindow):
    def __init__(self, *args, **kwds):

        from Gnumed.wxpython import gmListWidgets

        # begin wxGlade: wxgProviderInboxPnl.__init__
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.ScrolledWindow.__init__(self, *args, **kwds)
        self._msg_welcome = wx.StaticText(self, -1, _("Programmer must override this text."))
        self._RBTN_all_messages = wx.RadioButton(self, -1, _("A&ll"), style=wx.RB_GROUP)
        self._RBTN_overdue_messages = wx.RadioButton(self, -1, _("&Overdue"))
        self._RBTN_scheduled_messages = wx.RadioButton(self, -1, _("&Scheduled"))
        self._RBTN_unscheduled_messages = wx.RadioButton(self, -1, _("&Unscheduled"))
        self._RBTN_expired_messages = wx.RadioButton(self, -1, _("&Expired"))
        self._CHBOX_active_patient = wx.CheckBox(self, -1, _("Active patient"))
        self._CHBOX_active_provider = wx.CheckBox(self, -1, _("Yours"))
        self._BTN_add = wx.Button(self, -1, _("&Add"), style=wx.BU_EXACTFIT)
        self._LCTRL_provider_inbox = gmListWidgets.cReportListCtrl(self, -1, style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.SIMPLE_BORDER)
        self._TXT_inbox_item_comment = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL | wx.TE_LINEWRAP | wx.TE_WORDWRAP)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_RADIOBUTTON, self._on_message_range_radiobutton_selected, self._RBTN_all_messages)
        self.Bind(wx.EVT_RADIOBUTTON, self._on_message_range_radiobutton_selected, self._RBTN_overdue_messages)
        self.Bind(wx.EVT_RADIOBUTTON, self._on_message_range_radiobutton_selected, self._RBTN_scheduled_messages)
        self.Bind(wx.EVT_RADIOBUTTON, self._on_message_range_radiobutton_selected, self._RBTN_unscheduled_messages)
        self.Bind(wx.EVT_RADIOBUTTON, self._on_message_range_radiobutton_selected, self._RBTN_expired_messages)
        self.Bind(wx.EVT_CHECKBOX, self._on_active_patient_checkbox_ticked, self._CHBOX_active_patient)
        self.Bind(wx.EVT_CHECKBOX, self._on_active_provider_checkbox_ticked, self._CHBOX_active_provider)
        self.Bind(wx.EVT_BUTTON, self._on_add_button_pressed, self._BTN_add)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self._lst_item_selected, self._LCTRL_provider_inbox)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self._lst_item_activated, self._LCTRL_provider_inbox)
        self.Bind(wx.EVT_LIST_ITEM_FOCUSED, self._lst_item_focused, self._LCTRL_provider_inbox)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self._lst_item_right_clicked, self._LCTRL_provider_inbox)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: wxgProviderInboxPnl.__set_properties
        self.SetScrollRate(10, 10)
        self._msg_welcome.SetFont(wx.Font(11, wx.DEFAULT, wx.ITALIC, wx.BOLD, 0, ""))
        self._RBTN_all_messages.SetToolTipString(_("Show all (but expired) messages."))
        self._RBTN_all_messages.SetValue(1)
        self._RBTN_overdue_messages.SetToolTipString(_("Show overdue messages only."))
        self._RBTN_scheduled_messages.SetToolTipString(_("Show scheduled (future-due) messages only."))
        self._RBTN_unscheduled_messages.SetToolTipString(_("Show unscheduled (no due date) messages only."))
        self._RBTN_expired_messages.SetToolTipString(_("Show expired (expiry date has passed) messages only."))
        self._CHBOX_active_patient.SetToolTipString(_("Include only messages about the active patient."))
        self._CHBOX_active_patient.Enable(False)
        self._CHBOX_active_provider.SetToolTipString(_("Include only messages explicitely for you (rather than also to all providers)."))
        self._CHBOX_active_provider.SetValue(1)
        self._BTN_add.SetToolTipString(_("Add a new message."))
        self._LCTRL_provider_inbox.SetFocus()
        self._TXT_inbox_item_comment.SetToolTipString(_("This shows the entirety of the selected message in your Inbox."))
        self._TXT_inbox_item_comment.Enable(False)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: wxgProviderInboxPnl.__do_layout
        __szr_main = wx.BoxSizer(wx.VERTICAL)
        __szr_items = wx.BoxSizer(wx.HORIZONTAL)
        __szr_main.Add(self._msg_welcome, 0, 0, 0)
        __line_top = wx.StaticLine(self, -1)
        __szr_main.Add(__line_top, 0, wx.TOP | wx.BOTTOM | wx.EXPAND, 5)
        __lbl_items = wx.StaticText(self, -1, _("Messages:"))
        __szr_items.Add(__lbl_items, 0, wx.LEFT | wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 3)
        __szr_items.Add(self._RBTN_all_messages, 0, wx.RIGHT | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 5)
        __szr_items.Add(self._RBTN_overdue_messages, 0, wx.RIGHT | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 5)
        __szr_items.Add(self._RBTN_scheduled_messages, 0, wx.RIGHT | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 5)
        __szr_items.Add(self._RBTN_unscheduled_messages, 0, wx.RIGHT | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 5)
        __szr_items.Add(self._RBTN_expired_messages, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 5)
        __vline1_options = wx.StaticLine(self, -1, style=wx.LI_VERTICAL)
        __szr_items.Add(__vline1_options, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, 3)
        __lbl_audience = wx.StaticText(self, -1, _("Only:"))
        __szr_items.Add(__lbl_audience, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 3)
        __szr_items.Add(self._CHBOX_active_patient, 0, wx.RIGHT | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 5)
        __szr_items.Add(self._CHBOX_active_provider, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 3)
        __vline2_options = wx.StaticLine(self, -1, style=wx.LI_VERTICAL)
        __szr_items.Add(__vline2_options, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, 3)
        __szr_items.Add((20, 20), 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
        __szr_items.Add(self._BTN_add, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 3)
        __szr_main.Add(__szr_items, 0, wx.BOTTOM | wx.EXPAND, 5)
        __szr_main.Add(self._LCTRL_provider_inbox, 3, wx.EXPAND, 0)
        __szr_main.Add(self._TXT_inbox_item_comment, 1, wx.EXPAND, 0)
        self.SetSizer(__szr_main)
        __szr_main.Fit(self)
        # end wxGlade

    def _lst_item_activated(self, event): # wxGlade: wxgProviderInboxPnl.<event_handler>
        print "Event handler `_lst_item_activated' not implemented!"
        event.Skip()

    def _lst_item_focused(self, event): # wxGlade: wxgProviderInboxPnl.<event_handler>
        print "Event handler `_lst_item_focused' not implemented!"
        event.Skip()

    def _lst_item_right_clicked(self, event): # wxGlade: wxgProviderInboxPnl.<event_handler>
        print "Event handler `_lst_item_right_clicked' not implemented!"
        event.Skip()

    def _lst_item_selected(self, event): # wxGlade: wxgProviderInboxPnl.<event_handler>
        print "Event handler `_lst_item_selected' not implemented"
        event.Skip()

    def _on_add_button_pressed(self, event): # wxGlade: wxgProviderInboxPnl.<event_handler>
        print "Event handler `_on_add_button_pressed' not implemented"
        event.Skip()

    def _on_active_patient_checkbox_ticked(self, event):  # wxGlade: wxgProviderInboxPnl.<event_handler>
        print "Event handler `_on_active_patient_checkbox_ticked' not implemented"
        event.Skip()

    def _on_active_provider_checkbox_ticked(self, event):  # wxGlade: wxgProviderInboxPnl.<event_handler>
        print "Event handler `_on_active_provider_checkbox_ticked' not implemented"
        event.Skip()

    def _on_message_range_radiobutton_selected(self, event):  # wxGlade: wxgProviderInboxPnl.<event_handler>
        print "Event handler `_on_message_range_radiobutton_selected' not implemented"
        event.Skip()

# end of class wxgProviderInboxPnl


