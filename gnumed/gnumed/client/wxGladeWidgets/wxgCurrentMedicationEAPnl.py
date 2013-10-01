#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# generated by wxGlade 0.6.8
#

import wx

# begin wxGlade: dependencies
import gettext
# end wxGlade

# begin wxGlade: extracode
from Gnumed.wxpython.gmPhraseWheel import cPhraseWheel
from Gnumed.wxpython.gmEMRStructWidgets import cEpisodeSelectionPhraseWheel
from Gnumed.wxpython.gmDateTimeInput import cDateInputPhraseWheel
from Gnumed.wxpython.gmDateTimeInput import cIntervalPhraseWheel
from Gnumed.wxpython.gmMedicationWidgets import cDrugComponentPhraseWheel
from Gnumed.wxpython.gmMedicationWidgets import cSubstancePhraseWheel
from Gnumed.wxpython.gmMedicationWidgets import cSubstancePreparationPhraseWheel
from Gnumed.wxpython.gmMedicationWidgets import cSubstanceSchedulePhraseWheel
from Gnumed.wxpython.gmMedicationWidgets import cSubstanceAimPhraseWheel
# end wxGlade


class wxgCurrentMedicationEAPnl(wx.ScrolledWindow):
	def __init__(self, *args, **kwds):
		# begin wxGlade: wxgCurrentMedicationEAPnl.__init__
		kwds["style"] = wx.NO_BORDER | wx.TAB_TRAVERSAL
		wx.ScrolledWindow.__init__(self, *args, **kwds)
		self._LBL_allergies = wx.StaticText(self, wx.ID_ANY, "")
		self._LBL_component = wx.StaticText(self, wx.ID_ANY, _("Brand by component"))
		self._PRW_component = cDrugComponentPhraseWheel(self, wx.ID_ANY, "", style=wx.NO_BORDER)
		self._BTN_database_brand = wx.Button(self, wx.ID_ANY, _("Brands"), style=wx.BU_EXACTFIT)
		self._LBL_or = wx.StaticText(self, wx.ID_ANY, _("... or ..."))
		self._TCTRL_brand_ingredients = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_READONLY | wx.NO_BORDER)
		self._BTN_heart = wx.Button(self, wx.ID_ANY, _(u"\u2665"), style=wx.BU_EXACTFIT)
		self._BTN_kidneys = wx.Button(self, wx.ID_ANY, _("Kidneys"), style=wx.BU_EXACTFIT)
		self._LBL_substance = wx.StaticText(self, wx.ID_ANY, _("Unbranded substance"))
		self._PRW_substance = cSubstancePhraseWheel(self, wx.ID_ANY, "", style=wx.NO_BORDER)
		self._BTN_database_substance = wx.Button(self, wx.ID_ANY, _("Manage"), style=wx.BU_EXACTFIT)
		self._LBL_preparation = wx.StaticText(self, wx.ID_ANY, _("Preparation"))
		self._PRW_preparation = cSubstancePreparationPhraseWheel(self, wx.ID_ANY, "", style=wx.NO_BORDER)
		self._DP_started = cDateInputPhraseWheel(self, wx.ID_ANY, "", style=wx.NO_BORDER)
		self._CHBOX_approved = wx.CheckBox(self, wx.ID_ANY, _("Approved of"))
		self._PRW_episode = cEpisodeSelectionPhraseWheel(self, wx.ID_ANY, "", style=wx.NO_BORDER)
		self._PRW_schedule = cSubstanceSchedulePhraseWheel(self, wx.ID_ANY, "", style=wx.NO_BORDER)
		self._PRW_duration = cIntervalPhraseWheel(self, wx.ID_ANY, "", style=wx.NO_BORDER)
		self._CHBOX_long_term = wx.CheckBox(self, wx.ID_ANY, _("Long-term"))
		self._PRW_aim = cSubstanceAimPhraseWheel(self, wx.ID_ANY, "", style=wx.NO_BORDER)
		self._PRW_notes = cPhraseWheel(self, wx.ID_ANY, "", style=wx.NO_BORDER)
		self._DP_discontinued = cDateInputPhraseWheel(self, wx.ID_ANY, "", style=wx.NO_BORDER)
		self._BTN_discontinued_as_planned = wx.Button(self, wx.ID_ANY, _("Per plan"), style=wx.BU_EXACTFIT)
		self._LBL_reason = wx.StaticText(self, wx.ID_ANY, _("... Reason"))
		self._PRW_discontinue_reason = cPhraseWheel(self, wx.ID_ANY, "", style=wx.NO_BORDER)

		self.__set_properties()
		self.__do_layout()

		self.Bind(wx.EVT_BUTTON, self._on_manage_brands_button_pressed, self._BTN_database_brand)
		self.Bind(wx.EVT_BUTTON, self._on_heart_button_pressed, self._BTN_heart)
		self.Bind(wx.EVT_BUTTON, self._on_kidneys_button_pressed, self._BTN_kidneys)
		self.Bind(wx.EVT_BUTTON, self._on_manage_substances_button_pressed, self._BTN_database_substance)
		self.Bind(wx.EVT_CHECKBOX, self._on_chbox_long_term_checked, self._CHBOX_long_term)
		self.Bind(wx.EVT_BUTTON, self._on_discontinued_as_planned_button_pressed, self._BTN_discontinued_as_planned)
		# end wxGlade

	def __set_properties(self):
		# begin wxGlade: wxgCurrentMedicationEAPnl.__set_properties
		self.SetMinSize((660, 400))
		self.SetScrollRate(10, 10)
		self._LBL_component.SetForegroundColour(wx.Colour(255, 0, 0))
		self._PRW_component.SetToolTipString(_("A component of a drug brand the patient is taking.\n\nLookup, and select, a single- (or multi-) component drug brand, by active ingredient name. All components of multi-component drugs will be displayed and automatically added to the patient's list."))
		self._BTN_database_brand.SetToolTipString(_("Manage drug brands.\n\nNote that this will not select a component for you. What it does is to let you manage (add/edit/delete) the drug products/brands known to GNUmed from which you can select a component."))
		self._TCTRL_brand_ingredients.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_BACKGROUND))
		self._TCTRL_brand_ingredients.SetToolTipString(_("The active ingredients of this brand."))
		self._BTN_heart.SetToolTipString(_("Show cardiac information relevant to substance selection."))
		self._BTN_kidneys.SetToolTipString(_("Show renal insufficiency information related to substance selection."))
		self._LBL_substance.SetForegroundColour(wx.Colour(255, 0, 0))
		self._PRW_substance.SetToolTipString(_("The non-branded medication or non-medication substance, with optional strength."))
		self._BTN_database_substance.SetToolTipString(_("Manage consumable substances.\n\nThis will not select a substance for you. It will, however, enable you to manage (add/edit/delete) the consumable substances available for selection."))
		self._PRW_preparation.SetToolTipString(_("The preparation or form of the substance."))
		self._DP_started.SetToolTipString(_("When was this substance started to be consumed or - if not known - the earliest it is known to have been be consumed."))
		self._CHBOX_approved.SetToolTipString(_("Whether this substance is taken by advice."))
		self._CHBOX_approved.SetValue(1)
		self._PRW_episode.SetToolTipString(_("Select, or enter for creation, the episode to which this substance will relate."))
		self._PRW_schedule.SetToolTipString(_("The schedule for taking this substance."))
		self._PRW_duration.SetToolTipString(_("How long is this substance supposed to be taken."))
		self._CHBOX_long_term.SetToolTipString(_("Whether this substance is to be taken for the rest of the patient's life."))
		self._PRW_aim.SetToolTipString(_("The aim of consuming this substance."))
		self._PRW_notes.SetToolTipString(_("Any clinical notes, comments, or instructions on this substance intake."))
		self._DP_discontinued.SetToolTipString(_("When was intake of this substance discontinued ?"))
		self._BTN_discontinued_as_planned.SetToolTipString(_("Press if discontinuation was as planned."))
		self._PRW_discontinue_reason.SetToolTipString(_("Reason for discontinuation."))
		self._PRW_discontinue_reason.Enable(False)
		# end wxGlade

	def __do_layout(self):
		# begin wxGlade: wxgCurrentMedicationEAPnl.__do_layout
		__szr_main = wx.BoxSizer(wx.VERTICAL)
		__gszr_main = wx.FlexGridSizer(13, 2, 1, 3)
		__szr_discontinued_date = wx.BoxSizer(wx.HORIZONTAL)
		__szr_duration = wx.BoxSizer(wx.HORIZONTAL)
		__szr_started = wx.BoxSizer(wx.HORIZONTAL)
		__szr_substance = wx.BoxSizer(wx.HORIZONTAL)
		__szr_ingredient_details = wx.BoxSizer(wx.HORIZONTAL)
		__szr_substance_buttons = wx.BoxSizer(wx.VERTICAL)
		__szr_component = wx.BoxSizer(wx.HORIZONTAL)
		__szr_main.Add(self._LBL_allergies, 0, wx.BOTTOM | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 2)
		__sline_top = wx.StaticLine(self, wx.ID_ANY)
		__szr_main.Add(__sline_top, 0, wx.BOTTOM | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 3)
		__gszr_main.Add(self._LBL_component, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		__szr_component.Add(self._PRW_component, 1, wx.RIGHT | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 5)
		__szr_component.Add(self._BTN_database_brand, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
		__gszr_main.Add(__szr_component, 1, wx.EXPAND, 0)
		__gszr_main.Add(self._LBL_or, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
		__szr_ingredient_details.Add(self._TCTRL_brand_ingredients, 1, wx.RIGHT | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 5)
		__szr_substance_buttons.Add(self._BTN_heart, 0, wx.BOTTOM | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 3)
		__szr_substance_buttons.Add(self._BTN_kidneys, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
		__szr_ingredient_details.Add(__szr_substance_buttons, 0, wx.EXPAND, 0)
		__gszr_main.Add(__szr_ingredient_details, 1, wx.EXPAND, 0)
		__gszr_main.Add(self._LBL_substance, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		__szr_substance.Add(self._PRW_substance, 1, wx.RIGHT | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 5)
		__szr_substance.Add(self._BTN_database_substance, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
		__gszr_main.Add(__szr_substance, 1, wx.EXPAND, 0)
		__gszr_main.Add(self._LBL_preparation, 0, wx.ALIGN_CENTER_VERTICAL, 5)
		__gszr_main.Add(self._PRW_preparation, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 10)
		__gszr_main.Add((20, 20), 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
		__line_top = wx.StaticLine(self, wx.ID_ANY)
		__gszr_main.Add(__line_top, 0, wx.TOP | wx.BOTTOM | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 3)
		__lbl_started = wx.StaticText(self, wx.ID_ANY, _("Started"))
		__lbl_started.SetForegroundColour(wx.Colour(255, 0, 0))
		__gszr_main.Add(__lbl_started, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		__szr_started.Add(self._DP_started, 4, wx.RIGHT | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 10)
		__szr_started.Add(self._CHBOX_approved, 1, wx.ALIGN_CENTER_VERTICAL, 0)
		__szr_started.Add((20, 20), 1, wx.EXPAND, 0)
		__gszr_main.Add(__szr_started, 1, wx.EXPAND, 0)
		__lbl_episode = wx.StaticText(self, wx.ID_ANY, _("Episode"))
		__lbl_episode.SetForegroundColour(wx.Colour(255, 127, 0))
		__gszr_main.Add(__lbl_episode, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		__gszr_main.Add(self._PRW_episode, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
		__lbl_schedule = wx.StaticText(self, wx.ID_ANY, _("Schedule"))
		__gszr_main.Add(__lbl_schedule, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		__gszr_main.Add(self._PRW_schedule, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
		__lbl_duration = wx.StaticText(self, wx.ID_ANY, _("Duration"))
		__gszr_main.Add(__lbl_duration, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		__szr_duration.Add(self._PRW_duration, 1, wx.RIGHT | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 10)
		__szr_duration.Add(self._CHBOX_long_term, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 2)
		__gszr_main.Add(__szr_duration, 1, wx.EXPAND, 0)
		__lbl_aim = wx.StaticText(self, wx.ID_ANY, _("Aim"))
		__gszr_main.Add(__lbl_aim, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		__gszr_main.Add(self._PRW_aim, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
		__lbl_notes = wx.StaticText(self, wx.ID_ANY, _("Advice"))
		__gszr_main.Add(__lbl_notes, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		__gszr_main.Add(self._PRW_notes, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 0)
		__lbl_discontinued = wx.StaticText(self, wx.ID_ANY, _("Discontinued"))
		__gszr_main.Add(__lbl_discontinued, 0, wx.ALIGN_CENTER_VERTICAL, 5)
		__szr_discontinued_date.Add(self._DP_discontinued, 4, wx.RIGHT | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 10)
		__szr_discontinued_date.Add(self._BTN_discontinued_as_planned, 1, wx.ALIGN_CENTER_VERTICAL, 5)
		__szr_discontinued_date.Add((20, 20), 1, wx.EXPAND, 0)
		__gszr_main.Add(__szr_discontinued_date, 1, wx.EXPAND, 0)
		__gszr_main.Add(self._LBL_reason, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)
		__gszr_main.Add(self._PRW_discontinue_reason, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, 5)
		__gszr_main.AddGrowableCol(1)
		__szr_main.Add(__gszr_main, 1, wx.EXPAND, 0)
		self.SetSizer(__szr_main)
		__szr_main.Fit(self)
		# end wxGlade

	def _on_manage_brands_button_pressed(self, event):  # wxGlade: wxgCurrentMedicationEAPnl.<event_handler>
		print "Event handler '_on_manage_brands_button_pressed' not implemented!"
		event.Skip()

	def _on_heart_button_pressed(self, event):  # wxGlade: wxgCurrentMedicationEAPnl.<event_handler>
		print "Event handler '_on_heart_button_pressed' not implemented!"
		event.Skip()

	def _on_kidneys_button_pressed(self, event):  # wxGlade: wxgCurrentMedicationEAPnl.<event_handler>
		print "Event handler '_on_kidneys_button_pressed' not implemented!"
		event.Skip()

	def _on_manage_substances_button_pressed(self, event):  # wxGlade: wxgCurrentMedicationEAPnl.<event_handler>
		print "Event handler '_on_manage_substances_button_pressed' not implemented!"
		event.Skip()

	def _on_chbox_long_term_checked(self, event):  # wxGlade: wxgCurrentMedicationEAPnl.<event_handler>
		print "Event handler '_on_chbox_long_term_checked' not implemented!"
		event.Skip()

	def _on_discontinued_as_planned_button_pressed(self, event):  # wxGlade: wxgCurrentMedicationEAPnl.<event_handler>
		print "Event handler '_on_discontinued_as_planned_button_pressed' not implemented!"
		event.Skip()

# end of class wxgCurrentMedicationEAPnl
