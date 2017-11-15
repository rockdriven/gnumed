#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.7.2
#

import wx

# begin wxGlade: dependencies
import gettext
# end wxGlade

# begin wxGlade: extracode
from Gnumed.wxpython.gmHospitalStayWidgets import cHospitalStayPhraseWheel
# end wxGlade


class wxgReviewDocPartDlg(wx.Dialog):
	def __init__(self, *args, **kwds):

		from Gnumed.wxpython import gmEMRStructWidgets, gmDateTimeInput, gmDocumentWidgets
		from Gnumed.wxpython import gmOrganizationWidgets

		# begin wxGlade: wxgReviewDocPartDlg.__init__
		kwds["style"] = wx.DEFAULT_DIALOG_STYLE | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX | wx.RESIZE_BORDER
		wx.Dialog.__init__(self, *args, **kwds)
		self._PhWheel_episode = gmEMRStructWidgets.cEpisodeSelectionPhraseWheel(self, wx.ID_ANY, style=wx.NO_BORDER)
		self._PhWheel_doc_type = gmDocumentWidgets.cDocumentTypeSelectionPhraseWheel(self, wx.ID_ANY, style=wx.NO_BORDER)
		self._PRW_org = gmOrganizationWidgets.cOrgUnitPhraseWheel(self, wx.ID_ANY, "", style=wx.BORDER_NONE)
		self._RBTN_org_is_source = wx.RadioButton(self, wx.ID_ANY, _("Source"))
		self._RBTN_org_is_receiver = wx.RadioButton(self, wx.ID_ANY, _("Receiver"))
		self._PRW_hospital_stay = cHospitalStayPhraseWheel(self, wx.ID_ANY, "", style=wx.BORDER_NONE)
		self._PRW_doc_comment = gmDocumentWidgets.cDocumentCommentPhraseWheel(self, wx.ID_ANY, "", style=wx.BORDER_NONE)
		self._PhWheel_doc_date = gmDateTimeInput.cFuzzyTimestampInput(self, wx.ID_ANY, style=wx.NO_BORDER)
		self._TCTRL_reference = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.BORDER_NONE)
		self._TCTRL_filename = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.BORDER_NONE)
		self._SPINCTRL_seq_idx = wx.SpinCtrl(self, wx.ID_ANY, "", min=0, max=10000, style=wx.BORDER_NONE | wx.SP_ARROW_KEYS | wx.SP_WRAP | wx.TE_AUTO_URL | wx.TE_NOHIDESEL)
		self._LCTRL_existing_reviews = wx.ListCtrl(self, wx.ID_ANY, style=wx.BORDER_NONE | wx.LC_ALIGN_LEFT | wx.LC_HRULES | wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_VRULES)
		self._TCTRL_responsible = wx.TextCtrl(self, wx.ID_ANY, _("(you are/are not the primary reviewer)"), style=wx.BORDER_NONE | wx.TE_READONLY)
		self._ChBOX_review = wx.CheckBox(self, wx.ID_ANY, _("review document"))
		self._ChBOX_abnormal = wx.CheckBox(self, wx.ID_ANY, _("technically abnormal"))
		self._ChBOX_responsible = wx.CheckBox(self, wx.ID_ANY, _("take over responsibility"))
		self._ChBOX_relevant = wx.CheckBox(self, wx.ID_ANY, _("clinically relevant"))
		self._ChBOX_sign_all_pages = wx.CheckBox(self, wx.ID_ANY, _("sign all pages"))
		self._BTN_save = wx.Button(self, wx.ID_OK, _("Save"))
		self._BTN_cancel = wx.Button(self, wx.ID_CANCEL, _("Cancel"))

		self.__set_properties()
		self.__do_layout()

		self.Bind(wx.EVT_CHECKBOX, self._on_reviewed_box_checked, self._ChBOX_review)
		self.Bind(wx.EVT_BUTTON, self._on_save_button_pressed, id=wx.ID_OK)
		# end wxGlade

	def __set_properties(self):
		# begin wxGlade: wxgReviewDocPartDlg.__set_properties
		self.SetTitle(_("Edit document properties"))
		self._PhWheel_episode.SetToolTipString(_("Shows the episode associated with this document. Select another one or type in a new episode name to associate a different one."))
		self._PRW_org.SetToolTipString(_("The organizational unit this document originates from."))
		self._RBTN_org_is_source.SetToolTipString(_("Select if the organization is the source (sender) of the document."))
		self._RBTN_org_is_source.SetValue(1)
		self._RBTN_org_is_receiver.SetToolTipString(_("Select if the organization is the target (receiver) of the document.\n\nMostly when the document was sent from this praxis."))
		self._PRW_hospital_stay.SetToolTipString(_("Select the hospital stay associated with this document."))
		self._PhWheel_doc_date.SetToolTipString(_("Enter the date of creation of the document."))
		self._TCTRL_reference.SetToolTipString(_("Enter the ID by which this document is referenced externally."))
		self._TCTRL_filename.SetToolTipString(_("An example file name for this document type.\n\nMainly used to derive a file name extension during export for operating systems which need that to guesstimate the viewer."))
		self._SPINCTRL_seq_idx.SetToolTipString(_("The sequence index or page number. If invoked from a document instead of a page always applies to the first page."))
		self._LCTRL_existing_reviews.SetToolTipString(_("Lists previous reviews for this document part.\n\nThe first line (marked with an icon) will show your previous review if there is one.\nThe second line (marked with a blue bar) will display the review of the responsible provider if there is such a review.\n\n You can edit your review below."))
		self._LCTRL_existing_reviews.Enable(False)
		self._TCTRL_responsible.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_BACKGROUND))
		self._ChBOX_review.SetToolTipString(_("Check this if you want to edit your review."))
		self._ChBOX_abnormal.SetToolTipString(_("Does this document inform on a state of the patient's health that is technically abnormal ?"))
		self._ChBOX_abnormal.Enable(False)
		self._ChBOX_responsible.SetToolTipString(_("Check this if you intend to take over responsibility for this document and not just review it."))
		self._ChBOX_responsible.Enable(False)
		self._ChBOX_relevant.SetToolTipString(_("Is this document clinically relevant."))
		self._ChBOX_relevant.Enable(False)
		self._ChBOX_sign_all_pages.SetToolTipString(_("Apply review to entire document rather than just this part or page."))
		self._ChBOX_sign_all_pages.Enable(False)
		self._ChBOX_sign_all_pages.SetValue(1)
		self._BTN_save.SetToolTipString(_("Save your review."))
		self._BTN_cancel.SetToolTipString(_("Cancel this review."))
		self._BTN_cancel.SetFocus()
		self._BTN_cancel.SetDefault()
		# end wxGlade

	def __do_layout(self):
		# begin wxGlade: wxgReviewDocPartDlg.__do_layout
		__szr_main = wx.BoxSizer(wx.VERTICAL)
		__szr_bottom = wx.BoxSizer(wx.HORIZONTAL)
		__szr_box_review = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _("Your review")), wx.VERTICAL)
		__szr_grid_review = wx.FlexGridSizer(4, 2, 0, 0)
		__szr_reviews = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _("Reviews by others")), wx.HORIZONTAL)
		__szr_grid_properties = wx.FlexGridSizer(9, 2, 2, 3)
		__szr_org_details = wx.BoxSizer(wx.HORIZONTAL)
		__lbl_episode_picker = wx.StaticText(self, wx.ID_ANY, _("Episode"))
		__lbl_episode_picker.SetForegroundColour(wx.Colour(255, 0, 0))
		__szr_grid_properties.Add(__lbl_episode_picker, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		__szr_grid_properties.Add(self._PhWheel_episode, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
		__lbl_type = wx.StaticText(self, wx.ID_ANY, _("Type"))
		__lbl_type.SetForegroundColour(wx.Colour(255, 0, 0))
		__szr_grid_properties.Add(__lbl_type, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		__szr_grid_properties.Add(self._PhWheel_doc_type, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
		__lbl_org = wx.StaticText(self, wx.ID_ANY, _("Source"))
		__szr_grid_properties.Add(__lbl_org, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		__szr_org_details.Add(self._PRW_org, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
		__lbl_org_arrow = wx.StaticText(self, wx.ID_ANY, _(u"\u2794"))
		__szr_org_details.Add(__lbl_org_arrow, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 5)
		__szr_org_details.Add(self._RBTN_org_is_source, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.RIGHT, 3)
		__szr_org_details.Add(self._RBTN_org_is_receiver, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 3)
		__szr_grid_properties.Add(__szr_org_details, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
		__lbl_stay = wx.StaticText(self, wx.ID_ANY, _("Hospital Stay"))
		__szr_grid_properties.Add(__lbl_stay, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		__szr_grid_properties.Add(self._PRW_hospital_stay, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
		__lbl_comment = wx.StaticText(self, wx.ID_ANY, _("Comment"))
		__szr_grid_properties.Add(__lbl_comment, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		__szr_grid_properties.Add(self._PRW_doc_comment, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
		__lbl_doc_date = wx.StaticText(self, wx.ID_ANY, _("Date"))
		__lbl_doc_date.SetForegroundColour(wx.Colour(255, 0, 0))
		__szr_grid_properties.Add(__lbl_doc_date, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		__szr_grid_properties.Add(self._PhWheel_doc_date, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
		__lbl_reference = wx.StaticText(self, wx.ID_ANY, _("Reference"))
		__szr_grid_properties.Add(__lbl_reference, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		__szr_grid_properties.Add(self._TCTRL_reference, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
		__lbl_filename = wx.StaticText(self, wx.ID_ANY, _("Filename"))
		__lbl_filename.SetToolTipString(_("The original filename (if any). Only editable if invoked from a single part of the document."))
		__szr_grid_properties.Add(__lbl_filename, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		__szr_grid_properties.Add(self._TCTRL_filename, 1, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)
		__lbl_seq_idx = wx.StaticText(self, wx.ID_ANY, _("Seq #"))
		__lbl_seq_idx.SetToolTipString(_("The sequence index or page number. If invoked from a document instead of a page always applies to the first page."))
		__szr_grid_properties.Add(__lbl_seq_idx, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		__szr_grid_properties.Add(self._SPINCTRL_seq_idx, 1, wx.ALIGN_CENTER_VERTICAL, 0)
		__szr_grid_properties.AddGrowableCol(1)
		__szr_main.Add(__szr_grid_properties, 1, wx.EXPAND, 5)
		__szr_reviews.Add(self._LCTRL_existing_reviews, 1, wx.EXPAND, 0)
		__szr_main.Add(__szr_reviews, 1, wx.EXPAND, 0)
		__szr_box_review.Add(self._TCTRL_responsible, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND, 0)
		__szr_grid_review.Add(self._ChBOX_review, 0, 0, 0)
		__szr_grid_review.Add((5, 5), 1, wx.EXPAND, 0)
		__szr_grid_review.Add(self._ChBOX_abnormal, 0, wx.LEFT, 10)
		__szr_grid_review.Add(self._ChBOX_responsible, 0, wx.LEFT, 10)
		__szr_grid_review.Add(self._ChBOX_relevant, 0, wx.LEFT, 10)
		__szr_grid_review.Add(self._ChBOX_sign_all_pages, 0, wx.LEFT, 10)
		__szr_box_review.Add(__szr_grid_review, 1, wx.EXPAND, 0)
		__szr_main.Add(__szr_box_review, 1, wx.EXPAND, 0)
		__szr_bottom.Add(self._BTN_save, 0, 0, 0)
		__szr_bottom.Add(self._BTN_cancel, 0, 0, 0)
		__szr_main.Add(__szr_bottom, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
		self.SetSizer(__szr_main)
		__szr_main.Fit(self)
		self.Layout()
		self.Centre()
		# end wxGlade

	def _on_reviewed_box_checked(self, event):  # wxGlade: wxgReviewDocPartDlg.<event_handler>
		print "Event handler '_on_reviewed_box_checked' not implemented!"
		event.Skip()

	def _on_save_button_pressed(self, event):  # wxGlade: wxgReviewDocPartDlg.<event_handler>
		print "Event handler '_on_save_button_pressed' not implemented!"
		event.Skip()

# end of class wxgReviewDocPartDlg
