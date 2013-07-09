"""GNUmed measurement widgets."""
#================================================================
__author__ = "Karsten Hilbert <Karsten.Hilbert@gmx.net>"
__license__ = "GPL"


import sys, logging, datetime as pyDT, decimal, os, subprocess, codecs
import os.path


import wx, wx.grid, wx.lib.hyperlink


if __name__ == '__main__':
	sys.path.insert(0, '../../')
from Gnumed.pycommon import gmTools
from Gnumed.pycommon import gmNetworkTools
from Gnumed.pycommon import gmI18N
from Gnumed.pycommon import gmShellAPI
from Gnumed.pycommon import gmCfg
from Gnumed.pycommon import gmDateTime
from Gnumed.pycommon import gmMatchProvider
from Gnumed.pycommon import gmDispatcher
from Gnumed.pycommon import gmMimeLib

from Gnumed.business import gmPerson
from Gnumed.business import gmStaff
from Gnumed.business import gmPathLab
from Gnumed.business import gmPraxis
from Gnumed.business import gmLOINC
from Gnumed.business import gmForms
from Gnumed.business import gmPersonSearch
from Gnumed.business import gmOrganization

from Gnumed.wxpython import gmRegetMixin
from Gnumed.wxpython import gmEditArea
from Gnumed.wxpython import gmPhraseWheel
from Gnumed.wxpython import gmListWidgets
from Gnumed.wxpython import gmGuiHelpers
from Gnumed.wxpython import gmAuthWidgets
from Gnumed.wxpython import gmOrganizationWidgets


_log = logging.getLogger('gm.ui')

#================================================================
# HL7 related widgets
#================================================================
def import_Excelleris_HL7(parent=None):

	if parent is None:
		parent = wx.GetApp().GetTopWindow()

	# select file
	dlg = wx.FileDialog (
		parent = parent,
		message = 'Import Excelleris HL7 from XML file:',
#		defaultDir = aDefDir,
#		defaultFile = fname,
		wildcard = "xml files|*.xml|XML files|*.XML|all files|*",
		style = wx.OPEN | wx.FILE_MUST_EXIST
	)
	choice = dlg.ShowModal()
	xml_name = dlg.GetPath()
	dlg.Destroy()
	if choice != wx.ID_OK:
		return False

	# for now, localize gmHL7 import
	from Gnumed.business import gmHL7

	hl7 = gmHL7.extract_HL7_from_CDATA(xml_name, u'.//Message')
	if hl7 is None:
		gmGuiHelpers.gm_show_info (
			u'File [%s]\ndoes not seem to contain HL7 wrapped in XML.' % xml_name,
			u'Extracting HL7 from XML'
		)
		return False
	fixed_hl7 = gmHL7.fix_HL7_stupidities(hl7)
	PID_names = gmHL7.split_HL7_by_PID(fixed_hl7)
	for name in PID_names:
		gmHL7.stage_MSH_as_incoming_data(name, source = u'Excelleris')

#================================================================
def import_HL7(parent=None):

	if parent is None:
		parent = wx.GetApp().GetTopWindow()

	# select file
	dlg = wx.FileDialog (
		parent = parent,
		message = 'Import HL7 from file:',
#		defaultDir = aDefDir,
#		defaultFile = fname,
		wildcard = "*.hl7|*.hl7|*.HL7|*.HL7|all files|*",
		style = wx.OPEN | wx.FILE_MUST_EXIST
	)
	choice = dlg.ShowModal()
	hl7_name = dlg.GetPath()
	dlg.Destroy()
	if choice != wx.ID_OK:
		return False

	# for now, localize gmHL7 import
	from Gnumed.business import gmHL7

	fixed_hl7 = gmHL7.fix_HL7_stupidities(hl7_name)
	PID_names = gmHL7.split_HL7_by_PID(fixed_hl7)
	for name in PID_names:
		gmHL7.stage_MSH_as_incoming_data(name, source = u'generic')

#================================================================
def browse_incoming_unmatched(parent=None):

	# for now, localize gmHL7 import
	from Gnumed.business import gmHL7

	if parent is None:
		parent = wx.GetApp().GetTopWindow()
	#------------------------------------------------------------
	def show_hl7(data=None):
		if data is None:
			return False
		filename = data.export_to_file()
		if filename is None:
			return False
		formatted_hl7 = gmHL7.format_hl7_file(filename, return_filename = True)
		gmMimeLib.call_viewer_on_file(aFile = formatted_hl7, block = False)

		return False
	#------------------------------------------------------------
	def refresh(lctrl):
		incoming = gmHL7.get_incoming_data()
		items = [ [
			i['data_type'],
			u'%s, %s (%s) %s' % (
				i['lastnames'],
				i['firstnames'],
				i['dob'],
				i['gender']
			),
			i['external_data_id'],
			i['pk_incoming_data_unmatched']
		] for i in incoming ]
		lctrl.set_string_items(items)
		lctrl.set_data(incoming)
	#------------------------------------------------------------
	gmListWidgets.get_choices_from_list (
		parent = parent,
		msg = None,
		caption = _('Showing unmatched incoming data'),
		columns = [ _('Type'), _('Patient'), _('Data ID'), '#' ],
		single_selection = True,
		can_return_empty = False,
		ignore_OK_button = True,
		refresh_callback = refresh,
#		edit_callback=None,
#		new_callback=None,
#		delete_callback=None,
		left_extra_button = [_('Show'), _('Show formatted HL7'), show_hl7]
#		middle_extra_button=None,
#		right_extra_button=None
	)

#================================================================
# LOINC related widgets
#================================================================
def update_loinc_reference_data():

	wx.BeginBusyCursor()

	gmDispatcher.send(signal = 'statustext', msg = _('Updating LOINC data can take quite a while...'), beep = True)

	# download
	loinc_zip = gmNetworkTools.download_file(url = 'http://www.gnumed.de/downloads/data/loinc/loinctab.zip', suffix = '.zip')
	if loinc_zip is None:
		wx.EndBusyCursor()
		gmGuiHelpers.gm_show_warning (
			aTitle = _('Downloading LOINC'),
			aMessage = _('Error downloading the latest LOINC data.\n')
		)
		return False

	_log.debug('downloaded zipped LOINC data into [%s]', loinc_zip)

	loinc_dir = gmNetworkTools.unzip_data_pack(filename = loinc_zip)

	# split master data file
	data_fname, license_fname = gmLOINC.split_LOINCDBTXT(input_fname = os.path.join(loinc_dir, 'LOINCDB.TXT'))

	wx.EndBusyCursor()

	conn = gmAuthWidgets.get_dbowner_connection(procedure = _('importing LOINC reference data'))
	if conn is None:
		return False

	wx.BeginBusyCursor()

	# import data
	if gmLOINC.loinc_import(data_fname = data_fname, license_fname = license_fname, conn = conn):
		gmDispatcher.send(signal = 'statustext', msg = _('Successfully imported LOINC reference data.'))
	else:
		gmDispatcher.send(signal = 'statustext', msg = _('Importing LOINC reference data failed.'), beep = True)

	wx.EndBusyCursor()
	return True
#================================================================
# convenience functions
#================================================================
def call_browser_on_measurement_type(measurement_type=None):

	dbcfg = gmCfg.cCfgSQL()

	url = dbcfg.get (
		option = u'external.urls.measurements_search',
		workplace = gmPraxis.gmCurrentPraxisBranch().active_workplace,
		bias = 'user',
		default = u"http://www.google.de/search?as_oq=%(search_term)s&num=10&as_sitesearch=laborlexikon.de"
	)

	base_url = dbcfg.get2 (
		option = u'external.urls.measurements_encyclopedia',
		workplace = gmPraxis.gmCurrentPraxisBranch().active_workplace,
		bias = 'user',
		default = u'http://www.laborlexikon.de'
	)

	if measurement_type is None:
		url = base_url

	measurement_type = measurement_type.strip()

	if measurement_type == u'':
		url = base_url

	url = url % {'search_term': measurement_type}

	gmNetworkTools.open_url_in_browser(url = url)

#----------------------------------------------------------------
def edit_measurement(parent=None, measurement=None, single_entry=False):
	ea = cMeasurementEditAreaPnl(parent = parent, id = -1)
	ea.data = measurement
	ea.mode = gmTools.coalesce(measurement, 'new', 'edit')
	dlg = gmEditArea.cGenericEditAreaDlg2(parent = parent, id = -1, edit_area = ea, single_entry = single_entry)
	dlg.SetTitle(gmTools.coalesce(measurement, _('Adding new measurement'), _('Editing measurement')))
	if dlg.ShowModal() == wx.ID_OK:
		dlg.Destroy()
		return True
	dlg.Destroy()
	return False

#----------------------------------------------------------------
def manage_measurements(parent=None, single_selection=False, emr=None):

	if parent is None:
		parent = wx.GetApp().GetTopWindow()

	if emr is None:
		emr = gmPerson.gmCurrentPatient().emr

	#------------------------------------------------------------
	def edit(measurement=None):
		return edit_measurement(parent = parent, measurement = measurement, single_entry = True)
	#------------------------------------------------------------
	def delete(measurement):
		gmPathLab.delete_test_result(result = measurement)
		return True
	#------------------------------------------------------------
	def get_tooltip(measurement):
		return measurement.format(with_review=True, with_evaluation=True, with_ranges=True)
	#------------------------------------------------------------
	def refresh(lctrl):
		results = emr.get_test_results(order_by = 'clin_when DESC, unified_abbrev, unified_name')
		items = [ [
			gmDateTime.pydt_strftime (
				r['clin_when'],
				'%Y %b %d %H:%M',
				accuracy = gmDateTime.acc_minutes
			),
			r['unified_abbrev'],
			u'%s%s%s' % (
				r['unified_val'],
				gmTools.coalesce(r['val_unit'], u'', u' %s'),
				gmTools.coalesce(r['abnormality_indicator'], u'', u' %s')
			),
			r['unified_name'],
			gmTools.coalesce(r['comment'], u''),
			r['pk_test_result']
		] for r in results ]
		lctrl.set_string_items(items)
		lctrl.set_data(results)
	#------------------------------------------------------------
	msg = _('Test results (ordered reverse-chronologically)')

	return gmListWidgets.get_choices_from_list (
		parent = parent,
		msg = msg,
		caption = _('Showing test results.'),
		columns = [ _('When'), _('Abbrev'), _('Value'), _('Name'), _('Comment'), u'#' ],
		single_selection = single_selection,
		can_return_empty = False,
		refresh_callback = refresh,
		edit_callback = edit,
		new_callback = edit,
		delete_callback = delete,
		list_tooltip_callback = get_tooltip
	)

#================================================================
def configure_default_gnuplot_template(parent=None):

	from Gnumed.wxpython import gmFormWidgets

	if parent is None:
		parent = wx.GetApp().GetTopWindow()

	template = gmFormWidgets.manage_form_templates (
		parent = parent,
		active_only = True,
		template_types = [u'gnuplot script']
	)

	option = u'form_templates.default_gnuplot_template'

	if template is None:
		gmDispatcher.send(signal = 'statustext', msg = _('No default Gnuplot script template selected.'), beep = True)
		return None

	if template['engine'] != u'G':
		gmDispatcher.send(signal = 'statustext', msg = _('No default Gnuplot script template selected.'), beep = True)
		return None

	dbcfg = gmCfg.cCfgSQL()
	dbcfg.set (
		workplace = gmPraxis.gmCurrentPraxisBranch().active_workplace,
		option = option,
		value = u'%s - %s' % (template['name_long'], template['external_version'])
	)
	return template

#============================================================
def get_default_gnuplot_template(parent = None):

	option = u'form_templates.default_gnuplot_template'

	dbcfg = gmCfg.cCfgSQL()

	# load from option
	default_template_name = dbcfg.get2 (
		option = option,
		workplace = gmPraxis.gmCurrentPraxisBranch().active_workplace,
		bias = 'user'
	)

	# not configured -> try to configure
	if default_template_name is None:
		gmDispatcher.send('statustext', msg = _('No default Gnuplot template configured.'), beep = False)
		default_template = configure_default_gnuplot_template(parent = parent)
		# still not configured -> return
		if default_template is None:
			gmGuiHelpers.gm_show_error (
				aMessage = _('There is no default Gnuplot one-type script template configured.'),
				aTitle = _('Plotting test results')
			)
			return None
		return default_template

	# now it MUST be configured (either newly or previously)
	# but also *validly* ?
	try:
		name, ver = default_template_name.split(u' - ')
	except:
		# not valid
		_log.exception('problem splitting Gnuplot script template name [%s]', default_template_name)
		gmDispatcher.send(signal = 'statustext', msg = _('Problem loading Gnuplot script template.'), beep = True)
		return None

	default_template = gmForms.get_form_template(name_long = name, external_version = ver)
	if default_template is None:
		default_template = configure_default_gnuplot_template(parent = parent)
		# still not configured -> return
		if default_template is None:
			gmGuiHelpers.gm_show_error (
				aMessage = _('Cannot load default Gnuplot script template [%s - %s]') % (name, ver),
				aTitle = _('Plotting test results')
			)
			return None

	return default_template

#----------------------------------------------------------------
def plot_measurements(parent=None, tests=None, format=None, show_year = True, use_default_template=False):

	from Gnumed.wxpython import gmFormWidgets

	# only valid for one-type plotting
	if use_default_template:
		template = get_default_gnuplot_template()
	else:
		template = gmFormWidgets.manage_form_templates (
			parent = parent,
			active_only = True,
			template_types = [u'gnuplot script']
		)

	if template is None:
		gmGuiHelpers.gm_show_error (
			aMessage = _('Cannot plot without a plot script.'),
			aTitle = _('Plotting test results')
		)
		return False

	fname_data = gmPathLab.export_results_for_gnuplot(results = tests, show_year = show_year)

	script = template.instantiate()
	script.data_filename = fname_data
	script.generate_output(format = format) 		# Gnuplot output terminal, wxt = wxWidgets window

#----------------------------------------------------------------
def plot_adjacent_measurements(parent=None, test=None, format=None, show_year=True, plot_singular_result=True, use_default_template=False):

	earlier, later = test.get_adjacent_results(desired_earlier_results = 2, desired_later_results = 2)
	results2plot = []
	if earlier is not None:
		results2plot.extend(earlier)
	results2plot.append(test)
	if later is not None:
		results2plot.extend(later)
	if len(results2plot) == 1:
		if not plot_singular_result:
			return
	plot_measurements (
		parent = parent,
		tests = results2plot,
		format = format,
		show_year = show_year,
		use_default_template = use_default_template
	)
#================================================================
#from Gnumed.wxGladeWidgets import wxgPrimaryCareVitalsInputPnl

# Taillenumfang: Mitte zwischen unterster Rippe und
# hoechstem Teil des Beckenkamms
# Maenner: maessig: 94-102, deutlich: > 102  .. erhoeht
# Frauen:  maessig: 80-88,  deutlich: > 88   .. erhoeht

#================================================================
# display widgets
#================================================================
class cMeasurementsGrid(wx.grid.Grid):
	"""A grid class for displaying measurment results.

	- does NOT listen to the currently active patient
	- thereby it can display any patient at any time
	"""
	# FIXME: sort-by-battery
	# FIXME: filter-by-battery
	# FIXME: filter out empty
	# FIXME: filter by tests of a selected date
	# FIXME: dates DESC/ASC by cfg
	# FIXME: mouse over column header: display date info
	def __init__(self, *args, **kwargs):

		wx.grid.Grid.__init__(self, *args, **kwargs)

		self.__patient = None
		self.__panel_to_show = None
		self.__show_by_panel = False
		self.__cell_data = {}
		self.__row_label_data = []

		self.__prev_row = None
		self.__prev_col = None
		self.__prev_label_row = None
		self.__date_format = str((_('lab_grid_date_format::%Y\n%b %d')).lstrip('lab_grid_date_format::'))

		self.__init_ui()
		self.__register_events()
	#------------------------------------------------------------
	# external API
	#------------------------------------------------------------
	def delete_current_selection(self):
		if not self.IsSelection():
			gmDispatcher.send(signal = u'statustext', msg = _('No results selected for deletion.'))
			return True

		selected_cells = self.get_selected_cells()
		if len(selected_cells) > 20:
			results = None
			msg = _(
				'There are %s results marked for deletion.\n'
				'\n'
				'Are you sure you want to delete these results ?'
			) % len(selected_cells)
		else:
			results = self.__cells_to_data(cells = selected_cells, exclude_multi_cells = False)
			txt = u'\n'.join([ u'%s %s (%s): %s %s%s' % (
					r['clin_when'].strftime('%x %H:%M').decode(gmI18N.get_encoding()),
					r['unified_abbrev'],
					r['unified_name'],
					r['unified_val'],
					r['val_unit'],
					gmTools.coalesce(r['abnormality_indicator'], u'', u' (%s)')
				) for r in results
			])
			msg = _(
				'The following results are marked for deletion:\n'
				'\n'
				'%s\n'
				'\n'
				'Are you sure you want to delete these results ?'
			) % txt

		dlg = gmGuiHelpers.c2ButtonQuestionDlg (
			self,
			-1,
			caption = _('Deleting test results'),
			question = msg,
			button_defs = [
				{'label': _('Delete'), 'tooltip': _('Yes, delete all the results.'), 'default': False},
				{'label': _('Cancel'), 'tooltip': _('No, do NOT delete any results.'), 'default': True}
			]
		)
		decision = dlg.ShowModal()

		if decision == wx.ID_YES:
			if results is None:
				results = self.__cells_to_data(cells = selected_cells, exclude_multi_cells = False)
			for result in results:
				gmPathLab.delete_test_result(result)
	#------------------------------------------------------------
	def sign_current_selection(self):
		if not self.IsSelection():
			gmDispatcher.send(signal = u'statustext', msg = _('Cannot sign results. No results selected.'))
			return True

		selected_cells = self.get_selected_cells()
		if len(selected_cells) > 10:
			test_count = len(selected_cells)
			tests = None
		else:
			test_count = None
			tests = self.__cells_to_data(cells = selected_cells, exclude_multi_cells = False)
			if len(tests) == 0:
				return True

		dlg = cMeasurementsReviewDlg (
			self,
			-1,
			tests = tests,
			test_count = test_count
		)
		decision = dlg.ShowModal()

		if decision == wx.ID_APPLY:
			wx.BeginBusyCursor()

			if dlg._RBTN_confirm_abnormal.GetValue():
				abnormal = None
			elif dlg._RBTN_results_normal.GetValue():
				abnormal = False
			else:
				abnormal = True

			if dlg._RBTN_confirm_relevance.GetValue():
				relevant = None
			elif dlg._RBTN_results_not_relevant.GetValue():
				relevant = False
			else:
				relevant = True

			if tests is None:
				tests = self.__cells_to_data(cells = selected_cells, exclude_multi_cells = False)

			comment = None
			if len(tests) == 1:
				comment = dlg._TCTRL_comment.GetValue()

			for test in tests:
				test.set_review (
					technically_abnormal = abnormal,
					clinically_relevant = relevant,
					comment = comment,
					make_me_responsible = dlg._CHBOX_responsible.IsChecked()
				)

			wx.EndBusyCursor()

		dlg.Destroy()
	#------------------------------------------------------------
	def plot_current_selection(self):

		if not self.IsSelection():
			gmDispatcher.send(signal = u'statustext', msg = _('Cannot plot results. No results selected.'))
			return True

		tests = self.__cells_to_data (
			cells = self.get_selected_cells(),
			exclude_multi_cells = False,
			auto_include_multi_cells = True
		)

		plot_measurements(parent = self, tests = tests)
	#------------------------------------------------------------
	def get_selected_cells(self):

		sel_block_top_left = self.GetSelectionBlockTopLeft()
		sel_block_bottom_right = self.GetSelectionBlockBottomRight()
		sel_cols = self.GetSelectedCols()
		sel_rows = self.GetSelectedRows()

		selected_cells = []

		# individually selected cells (ctrl-click)
		selected_cells += self.GetSelectedCells()

		# selected rows
		selected_cells += list (
			(row, col)
				for row in sel_rows
				for col in xrange(self.GetNumberCols())
		)

		# selected columns
		selected_cells += list (
			(row, col)
				for row in xrange(self.GetNumberRows())
				for col in sel_cols
		)

		# selection blocks
		for top_left, bottom_right in zip(self.GetSelectionBlockTopLeft(), self.GetSelectionBlockBottomRight()):
			selected_cells += [
				(row, col)
					for row in xrange(top_left[0], bottom_right[0] + 1)
					for col in xrange(top_left[1], bottom_right[1] + 1)
			]

		return set(selected_cells)
	#------------------------------------------------------------
	def select_cells(self, unsigned_only=False, accountables_only=False, keep_preselections=False):
		"""Select a range of cells according to criteria.

		unsigned_only: include only those which are not signed at all yet
		accountable_only: include only those for which the current user is responsible
		keep_preselections: broaden (rather than replace) the range of selected cells

		Combinations are powerful !
		"""
		wx.BeginBusyCursor()
		self.BeginBatch()

		if not keep_preselections:
			self.ClearSelection()

		for col_idx in self.__cell_data.keys():
			for row_idx in self.__cell_data[col_idx].keys():
				# loop over results in cell and only include
				# those multi-value cells that are not ambiguous
				do_not_include = False
				for result in self.__cell_data[col_idx][row_idx]:
					if unsigned_only:
						if result['reviewed']:
							do_not_include = True
							break
					if accountables_only:
						if not result['you_are_responsible']:
							do_not_include = True
							break
				if do_not_include:
					continue

				self.SelectBlock(row_idx, col_idx, row_idx, col_idx, addToSelected = True)

		self.EndBatch()
		wx.EndBusyCursor()
	#------------------------------------------------------------
	def repopulate_grid(self):
		self.empty_grid()
		if self.__patient is None:
			return

		if self.__show_by_panel:
			self.__repopulate_grid_by_panel()
			return

		self.__repopulate_grid_all_results()
	#------------------------------------------------------------
	def __repopulate_grid_by_panel(self):

		if self.__panel_to_show is None:
			return

		emr = self.__patient.get_emr()

		# rows
		self.__row_label_data = self.__panel_to_show.test_types
		row_labels = [ u'%s%s' % (
				gmTools.bool2subst(test['is_fake_meta_type'], u'', gmTools.u_sum, u''),
				test['unified_abbrev']
			) for test in self.__row_label_data
		]
		if len(row_labels) == 0:
			return

		# columns
		column_labels = [
			date[0].strftime(self.__date_format) for date in emr.get_dates_for_results (
				tests = self.__panel_to_show['pk_test_types'],
				# FIXME: make configurable
				reverse_chronological = True
			)
		]
		results = emr.get_test_results_by_date (
			tests = self.__panel_to_show['pk_test_types'],
			# FIXME: make configurable
			reverse_chronological = True
		)

		self.BeginBatch()

		# rows
		self.AppendRows(numRows = len(row_labels))
		for row_idx in range(len(row_labels)):
			self.SetRowLabelValue(row_idx, row_labels[row_idx])

		# columns
		self.AppendCols(numCols = len(column_labels))
		for date_idx in range(len(column_labels)):
			self.SetColLabelValue(date_idx, column_labels[date_idx])

		# cell values (list of test results)
		for result in results:
			row = row_labels.index(u'%s%s' % (
				gmTools.bool2subst(result['is_fake_meta_type'], u'', gmTools.u_sum, u''),
				result['unified_abbrev']
			))
			col = column_labels.index(result['clin_when'].strftime(self.__date_format))

			try:
				self.__cell_data[col]
			except KeyError:
				self.__cell_data[col] = {}

			# the tooltip always shows the youngest sub result details
			if self.__cell_data[col].has_key(row):
				self.__cell_data[col][row].append(result)
				self.__cell_data[col][row].sort(key = lambda x: x['clin_when'], reverse = True)
			else:
				self.__cell_data[col][row] = [result]

			# rebuild cell display string
			vals2display = []
			for sub_result in self.__cell_data[col][row]:

				# is the sub_result technically abnormal ?
				ind = gmTools.coalesce(sub_result['abnormality_indicator'], u'').strip()
				if ind != u'':
					lab_abnormality_indicator = u' (%s)' % ind[:3]
				else:
					lab_abnormality_indicator = u''
				# - if noone reviewed - use what the lab thinks
				if sub_result['is_technically_abnormal'] is None:
					abnormality_indicator = lab_abnormality_indicator
				# - if someone reviewed and decreed normality - use that
				elif sub_result['is_technically_abnormal'] is False:
					abnormality_indicator = u''
				# - if someone reviewed and decreed abnormality ...
				else:
					# ... invent indicator if the lab did't use one
					if lab_abnormality_indicator == u'':
						# FIXME: calculate from min/max/range
						abnormality_indicator = u' (%s)' % gmTools.u_plus_minus
					# ... else use indicator the lab used
					else:
						abnormality_indicator = lab_abnormality_indicator

				# is the sub_result relevant clinically ?
				# FIXME: take into account primary_GP once we support that
				sub_result_relevant = sub_result['is_clinically_relevant']
				if sub_result_relevant is None:
					# FIXME: calculate from clinical range
					sub_result_relevant = False

				missing_review = False
				# warn on missing review if
				# a) no review at all exists or
				if not sub_result['reviewed']:
					missing_review = True
				# b) there is a review but
				else:
					# current user is reviewer and hasn't reviewed
					if sub_result['you_are_responsible'] and not sub_result['review_by_you']:
						missing_review = True

				# can we display the full sub_result length ?
				if len(sub_result['unified_val']) > 8:
					tmp = u'%.7s%s' % (sub_result['unified_val'][:7], gmTools.u_ellipsis)
				else:
					tmp = u'%.8s' % sub_result['unified_val'][:8]

				# abnormal ?
				tmp = u'%s%.6s' % (tmp, abnormality_indicator)

				# is there a comment ?
				has_sub_result_comment = gmTools.coalesce (
					gmTools.coalesce(sub_result['note_test_org'], sub_result['comment']),
					u''
				).strip() != u''
				if has_sub_result_comment:
					tmp = u'%s %s' % (tmp, gmTools.u_ellipsis)

				# lacking a review ?
				if missing_review:
					tmp = u'%s %s' % (tmp, gmTools.u_writing_hand)

				# part of a multi-result cell ?
				if len(self.__cell_data[col][row]) > 1:
					tmp = u'%s %s' % (sub_result['clin_when'].strftime('%H:%M'), tmp)

				vals2display.append(tmp)

			self.SetCellValue(row, col, u'\n'.join(vals2display))
			self.SetCellAlignment(row, col, horiz = wx.ALIGN_RIGHT, vert = wx.ALIGN_CENTRE)
#			font = self.GetCellFont(row, col)
#			if not font.IsFixedWidth():
#				font.SetFamily(family = wx.FONTFAMILY_MODERN)
			# FIXME: what about partial sub results being relevant ??
			if sub_result_relevant:
				font = self.GetCellFont(row, col)
				self.SetCellTextColour(row, col, 'firebrick')
				font.SetWeight(wx.FONTWEIGHT_BOLD)
				self.SetCellFont(row, col, font)
#			self.SetCellFont(row, col, font)

		self.AutoSize()
		self.EndBatch()
		return
	#------------------------------------------------------------
	def __repopulate_grid_all_results(self):
		emr = self.__patient.get_emr()

		self.__row_label_data = emr.get_test_types_for_results()
		test_type_labels = [ u'%s%s' % (
				gmTools.bool2subst(test['is_fake_meta_type'], u'', gmTools.u_sum, u''),
				test['unified_abbrev']
			) for test in self.__row_label_data
		]
		if len(test_type_labels) == 0:
			return

		test_date_labels = [ date[0].strftime(self.__date_format) for date in emr.get_dates_for_results() ]
		results = emr.get_test_results_by_date()

		self.BeginBatch()

		# rows
		self.AppendRows(numRows = len(test_type_labels))
		for row_idx in range(len(test_type_labels)):
			self.SetRowLabelValue(row_idx, test_type_labels[row_idx])

		# columns
		self.AppendCols(numCols = len(test_date_labels))
		for date_idx in range(len(test_date_labels)):
			self.SetColLabelValue(date_idx, test_date_labels[date_idx])

		# cell values (list of test results)
		for result in results:
			row = test_type_labels.index(u'%s%s' % (
				gmTools.bool2subst(result['is_fake_meta_type'], u'', gmTools.u_sum, u''),
				result['unified_abbrev']
			))
			col = test_date_labels.index(result['clin_when'].strftime(self.__date_format))

			try:
				self.__cell_data[col]
			except KeyError:
				self.__cell_data[col] = {}

			# the tooltip always shows the youngest sub result details
			if self.__cell_data[col].has_key(row):
				self.__cell_data[col][row].append(result)
				self.__cell_data[col][row].sort(key = lambda x: x['clin_when'], reverse = True)
			else:
				self.__cell_data[col][row] = [result]

			# rebuild cell display string
			vals2display = []
			for sub_result in self.__cell_data[col][row]:

				# is the sub_result technically abnormal ?
				ind = gmTools.coalesce(sub_result['abnormality_indicator'], u'').strip()
				if ind != u'':
					lab_abnormality_indicator = u' (%s)' % ind[:3]
				else:
					lab_abnormality_indicator = u''
				# - if noone reviewed - use what the lab thinks
				if sub_result['is_technically_abnormal'] is None:
					abnormality_indicator = lab_abnormality_indicator
				# - if someone reviewed and decreed normality - use that
				elif sub_result['is_technically_abnormal'] is False:
					abnormality_indicator = u''
				# - if someone reviewed and decreed abnormality ...
				else:
					# ... invent indicator if the lab did't use one
					if lab_abnormality_indicator == u'':
						# FIXME: calculate from min/max/range
						abnormality_indicator = u' (%s)' % gmTools.u_plus_minus
					# ... else use indicator the lab used
					else:
						abnormality_indicator = lab_abnormality_indicator

				# is the sub_result relevant clinically ?
				# FIXME: take into account primary_GP once we support that
				sub_result_relevant = sub_result['is_clinically_relevant']
				if sub_result_relevant is None:
					# FIXME: calculate from clinical range
					sub_result_relevant = False

				missing_review = False
				# warn on missing review if
				# a) no review at all exists or
				if not sub_result['reviewed']:
					missing_review = True
				# b) there is a review but
				else:
					# current user is reviewer and hasn't reviewed
					if sub_result['you_are_responsible'] and not sub_result['review_by_you']:
						missing_review = True

				# can we display the full sub_result length ?
				if len(sub_result['unified_val']) > 8:
					tmp = u'%.7s%s' % (sub_result['unified_val'][:7], gmTools.u_ellipsis)
				else:
					tmp = u'%.8s' % sub_result['unified_val'][:8]

				# abnormal ?
				tmp = u'%s%.6s' % (tmp, abnormality_indicator)

				# is there a comment ?
				has_sub_result_comment = gmTools.coalesce (
					gmTools.coalesce(sub_result['note_test_org'], sub_result['comment']),
					u''
				).strip() != u''
				if has_sub_result_comment:
					tmp = u'%s %s' % (tmp, gmTools.u_ellipsis)

				# lacking a review ?
				if missing_review:
					tmp = u'%s %s' % (tmp, gmTools.u_writing_hand)

				# part of a multi-result cell ?
				if len(self.__cell_data[col][row]) > 1:
					tmp = u'%s %s' % (sub_result['clin_when'].strftime('%H:%M'), tmp)

				vals2display.append(tmp)

			self.SetCellValue(row, col, u'\n'.join(vals2display))
			self.SetCellAlignment(row, col, horiz = wx.ALIGN_RIGHT, vert = wx.ALIGN_CENTRE)
#			font = self.GetCellFont(row, col)
#			if not font.IsFixedWidth():
#				font.SetFamily(family = wx.FONTFAMILY_MODERN)
			# FIXME: what about partial sub results being relevant ??
			if sub_result_relevant:
				font = self.GetCellFont(row, col)
				self.SetCellTextColour(row, col, 'firebrick')
				font.SetWeight(wx.FONTWEIGHT_BOLD)
				self.SetCellFont(row, col, font)
#			self.SetCellFont(row, col, font)

		self.AutoSize()
		self.EndBatch()
		return
	#------------------------------------------------------------
	def empty_grid(self):
		self.BeginBatch()
		self.ClearGrid()
		# Windows cannot do nothing, it rather decides to assert()
		# on thinking it is supposed to do nothing
		if self.GetNumberRows() > 0:
			self.DeleteRows(pos = 0, numRows = self.GetNumberRows())
		if self.GetNumberCols() > 0:
			self.DeleteCols(pos = 0, numCols = self.GetNumberCols())
		self.EndBatch()
		self.__cell_data = {}
		self.__row_label_data = []
	#------------------------------------------------------------
	def get_row_tooltip(self, row=None):
		# display test info (unified, which tests are grouped, which panels
		# they belong to include details about test types included,

		# sometimes, for some reason, there is no row and
		# wxPython still tries to find a tooltip for it
		try:
			tt = self.__row_label_data[row]
		except IndexError:
			return u' '

		return tt.format(patient = self.__patient.ID)
	#------------------------------------------------------------
	def get_cell_tooltip(self, col=None, row=None):
		try:
			d = self.__cell_data[col][row]
		except KeyError:
			# FIXME: maybe display the most recent or when the most recent was ?
			d = None

		if d is None:
			return u' '

		is_multi_cell = False
		if len(d) > 1:
			is_multi_cell = True
		d = d[0]

		tt = u''
		# header
		if is_multi_cell:
			tt += _(u'Details of most recent (topmost) result !               \n')
		tt += d.format(with_review = True, with_evaluation = True, with_ranges = True)
		return tt
	#------------------------------------------------------------
	# internal helpers
	#------------------------------------------------------------
	def __init_ui(self):
		self.CreateGrid(0, 1)
		self.EnableEditing(0)
		self.EnableDragGridSize(1)
		self.SetMinSize(wx.DefaultSize)

		# setting this screws up the labels: they are cut off and displaced
		#self.SetColLabelAlignment(wx.ALIGN_CENTER, wx.ALIGN_BOTTOM)

		self.SetRowLabelSize(wx.grid.GRID_AUTOSIZE)		# starting with 2.8.8
		#self.SetRowLabelSize(150)
		self.SetRowLabelAlignment(horiz = wx.ALIGN_LEFT, vert = wx.ALIGN_CENTRE)

		# add link to left upper corner
		dbcfg = gmCfg.cCfgSQL()
		url = dbcfg.get2 (
			option = u'external.urls.measurements_encyclopedia',
			workplace = gmPraxis.gmCurrentPraxisBranch().active_workplace,
			bias = 'user',
			default = u'http://www.laborlexikon.de'
		)

		self.__WIN_corner = self.GetGridCornerLabelWindow()		# a wx.Window instance

		LNK_lab = wx.lib.hyperlink.HyperLinkCtrl (
			self.__WIN_corner,
			-1,
			label = _('Tests'),
			style = wx.HL_DEFAULT_STYLE			# wx.TE_READONLY|wx.TE_CENTRE| wx.NO_BORDER |
		)
		LNK_lab.SetURL(url)
		LNK_lab.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_BACKGROUND))
		LNK_lab.SetToolTipString(_(
			'Navigate to an encyclopedia of measurements\n'
			'and test methods on the web.\n'
			'\n'
			' <%s>'
		) % url)

		SZR_inner = wx.BoxSizer(wx.HORIZONTAL)
		SZR_inner.Add((20, 20), 1, wx.EXPAND, 0)		# spacer
		SZR_inner.Add(LNK_lab, 0, wx.ALIGN_CENTER_VERTICAL, 0)		#wx.ALIGN_CENTER wx.EXPAND
		SZR_inner.Add((20, 20), 1, wx.EXPAND, 0)		# spacer

		SZR_corner = wx.BoxSizer(wx.VERTICAL)
		SZR_corner.Add((20, 20), 1, wx.EXPAND, 0)		# spacer
		SZR_corner.AddWindow(SZR_inner, 0, wx.EXPAND)	# inner sizer with centered hyperlink
		SZR_corner.Add((20, 20), 1, wx.EXPAND, 0)		# spacer

		self.__WIN_corner.SetSizer(SZR_corner)
		SZR_corner.Fit(self.__WIN_corner)
	#------------------------------------------------------------
	def __resize_corner_window(self, evt):
		self.__WIN_corner.Layout()
	#------------------------------------------------------------
	def __cells_to_data(self, cells=None, exclude_multi_cells=False, auto_include_multi_cells=False):
		"""List of <cells> must be in row / col order."""
		data = []
		for row, col in cells:
			try:
				# cell data is stored col / row
				data_list = self.__cell_data[col][row]
			except KeyError:
				continue

			if len(data_list) == 1:
				data.append(data_list[0])
				continue

			if exclude_multi_cells:
				gmDispatcher.send(signal = u'statustext', msg = _('Excluding multi-result field from further processing.'))
				continue

			if auto_include_multi_cells:
				data.extend(data_list)
				continue

			data_to_include = self.__get_choices_from_multi_cell(cell_data = data_list)
			if data_to_include is None:
				continue
			data.extend(data_to_include)

		return data
	#------------------------------------------------------------
	def __get_choices_from_multi_cell(self, cell_data=None, single_selection=False):
		data = gmListWidgets.get_choices_from_list (
			parent = self,
			msg = _(
				'Your selection includes a field with multiple results.\n'
				'\n'
				'Please select the individual results you want to work on:'
			),
			caption = _('Selecting test results'),
			choices = [ [d['clin_when'], u'%s: %s' % (d['abbrev_tt'], d['name_tt']), d['unified_val']] for d in cell_data ],
			columns = [ _('Date / Time'), _('Test'), _('Result') ],
			data = cell_data,
			single_selection = single_selection
		)
		return data
	#------------------------------------------------------------
	# event handling
	#------------------------------------------------------------
	def __register_events(self):
		# dynamic tooltips: GridWindow, GridRowLabelWindow, GridColLabelWindow, GridCornerLabelWindow
		self.GetGridWindow().Bind(wx.EVT_MOTION, self.__on_mouse_over_cells)
		self.GetGridRowLabelWindow().Bind(wx.EVT_MOTION, self.__on_mouse_over_row_labels)
		#self.GetGridColLabelWindow().Bind(wx.EVT_MOTION, self.__on_mouse_over_col_labels)

		# sizing left upper corner window
		self.Bind(wx.EVT_SIZE, self.__resize_corner_window)

		# editing cells
		self.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK, self.__on_cell_left_dclicked)
	#------------------------------------------------------------
	def __on_cell_left_dclicked(self, evt):
		col = evt.GetCol()
		row = evt.GetRow()

		# empty cell, perhaps ?
		try:
			self.__cell_data[col][row]
		except KeyError:
			# FIXME: invoke editor for adding value for day of that column
			# FIMXE: and test of that row
			return

		if len(self.__cell_data[col][row]) > 1:
			data = self.__get_choices_from_multi_cell(cell_data = self.__cell_data[col][row], single_selection = True)
		else:
			data = self.__cell_data[col][row][0]

		if data is None:
			return

		edit_measurement(parent = self, measurement = data, single_entry = True)
	#------------------------------------------------------------
#     def OnMouseMotionRowLabel(self, evt):
#         x, y = self.CalcUnscrolledPosition(evt.GetPosition())
#         row = self.YToRow(y)
#         label = self.table().GetRowHelpValue(row)
#         self.GetGridRowLabelWindow().SetToolTipString(label or "")
#         evt.Skip()
	def __on_mouse_over_row_labels(self, evt):

		# Use CalcUnscrolledPosition() to get the mouse position within the
		# entire grid including what's offscreen
		x, y = self.CalcUnscrolledPosition(evt.GetX(), evt.GetY())

		row = self.YToRow(y)

		if self.__prev_label_row == row:
			return

		self.__prev_label_row == row

		evt.GetEventObject().SetToolTipString(self.get_row_tooltip(row = row))
	#------------------------------------------------------------
#     def OnMouseMotionColLabel(self, evt):
#         x, y = self.CalcUnscrolledPosition(evt.GetPosition())
#         col = self.XToCol(x)
#         label = self.table().GetColHelpValue(col)
#         self.GetGridColLabelWindow().SetToolTipString(label or "")
#         evt.Skip()
	#------------------------------------------------------------
	def __on_mouse_over_cells(self, evt):
		"""Calculate where the mouse is and set the tooltip dynamically."""

		# Use CalcUnscrolledPosition() to get the mouse position within the
		# entire grid including what's offscreen
		x, y = self.CalcUnscrolledPosition(evt.GetX(), evt.GetY())

		# use this logic to prevent tooltips outside the actual cells
		# apply to GetRowSize, too
#        tot = 0
#        for col in xrange(self.NumberCols):
#            tot += self.GetColSize(col)
#            if xpos <= tot:
#                self.tool_tip.Tip = 'Tool tip for Column %s' % (
#                    self.GetColLabelValue(col))
#                break
#            else:  # mouse is in label area beyond the right-most column
#            self.tool_tip.Tip = ''

		row, col = self.XYToCell(x, y)

		if (row == self.__prev_row) and (col == self.__prev_col):
			return

		self.__prev_row = row
		self.__prev_col = col

		evt.GetEventObject().SetToolTipString(self.get_cell_tooltip(col=col, row=row))
	#------------------------------------------------------------
	# properties
	#------------------------------------------------------------
	def _set_patient(self, patient):
		self.__patient = patient
		self.repopulate_grid()

	patient = property(lambda x:x, _set_patient)
	#------------------------------------------------------------
	def _set_panel_to_show(self, panel):
		self.__panel_to_show = panel
		self.repopulate_grid()

	panel_to_show = property(lambda x:x, _set_panel_to_show)
	#------------------------------------------------------------
	def _set_show_by_panel(self, show_by_panel):
		self.__show_by_panel = show_by_panel
		self.repopulate_grid()

	show_by_panel = property(lambda x:x, _set_show_by_panel)
#================================================================
from Gnumed.wxGladeWidgets import wxgMeasurementsPnl

class cMeasurementsPnl(wxgMeasurementsPnl.wxgMeasurementsPnl, gmRegetMixin.cRegetOnPaintMixin):
	"""Panel holding a grid with lab data. Used as notebook page."""

	def __init__(self, *args, **kwargs):

		wxgMeasurementsPnl.wxgMeasurementsPnl.__init__(self, *args, **kwargs)
		gmRegetMixin.cRegetOnPaintMixin.__init__(self)
		self.__init_ui()
		self.__register_interests()
	#--------------------------------------------------------
	# event handling
	#--------------------------------------------------------
	def __register_interests(self):
		gmDispatcher.connect(signal = u'pre_patient_selection', receiver = self._on_pre_patient_selection)
		gmDispatcher.connect(signal = u'post_patient_selection', receiver = self._on_post_patient_selection)
		gmDispatcher.connect(signal = u'test_result_mod_db', receiver = self._schedule_data_reget)
		gmDispatcher.connect(signal = u'reviewed_test_results_mod_db', receiver = self._schedule_data_reget)
	#--------------------------------------------------------
	def _on_post_patient_selection(self):
		wx.CallAfter(self.__on_post_patient_selection)
	#--------------------------------------------------------
	def __on_post_patient_selection(self):
		self._schedule_data_reget()
	#--------------------------------------------------------
	def _on_pre_patient_selection(self):
		wx.CallAfter(self.__on_pre_patient_selection)
	#--------------------------------------------------------
	def __on_pre_patient_selection(self):
		self.data_grid.patient = None
		self.panel_data_grid.patient = None
	#--------------------------------------------------------
	def _on_add_button_pressed(self, event):
		edit_measurement(parent = self, measurement = None)
	#--------------------------------------------------------
	def _on_review_button_pressed(self, evt):
		self.PopupMenu(self.__action_button_popup)
	#--------------------------------------------------------
	def _on_select_button_pressed(self, evt):
		if self._RBTN_my_unsigned.GetValue() is True:
			self.data_grid.select_cells(unsigned_only = True, accountables_only = True, keep_preselections = False)
		elif self._RBTN_all_unsigned.GetValue() is True:
			self.data_grid.select_cells(unsigned_only = True, accountables_only = False, keep_preselections = False)
	#--------------------------------------------------------
	def _on_manage_panels_button_pressed(self, event):
		manage_test_panels(parent = self)
	#--------------------------------------------------------
	def __on_sign_current_selection(self, evt):
		self.data_grid.sign_current_selection()
	#--------------------------------------------------------
	def __on_plot_current_selection(self, evt):
		self.data_grid.plot_current_selection()
	#--------------------------------------------------------
	def __on_delete_current_selection(self, evt):
		self.data_grid.delete_current_selection()
	#--------------------------------------------------------
	def _on_panel_selected(self, panel):
		wx.CallAfter(self.__on_panel_selected, panel=panel)
	#--------------------------------------------------------
	def __on_panel_selected(self, panel):
		if panel is None:
			self._TCTRL_panel_comment.SetValue(u'')
			self.panel_data_grid.panel_to_show = None
			self.panel_data_grid.Hide()
		else:
			pnl = self._PRW_panel.GetData(as_instance = True)
			self._TCTRL_panel_comment.SetValue(gmTools.coalesce (
				pnl['comment'],
				u''
			))
			self.panel_data_grid.panel_to_show = pnl
			self.panel_data_grid.Show()
		self.Layout()
		#self.Refresh()
	#--------------------------------------------------------
	def _on_panel_selection_modified(self):
		wx.CallAfter(self.__on_panel_selection_modified)
	#--------------------------------------------------------
	def __on_panel_selection_modified(self):
		self._TCTRL_panel_comment.SetValue(u'')
		if self._PRW_panel.GetValue().strip() == u'':
			self.panel_data_grid.panel_to_show = None
			self.panel_data_grid.Hide()
			self.Layout()
	#--------------------------------------------------------
	# internal API
	#--------------------------------------------------------
	def __init_ui(self):
		self.__action_button_popup = wx.Menu(title = _('Perform on selected results:'))

		menu_id = wx.NewId()
		self.__action_button_popup.AppendItem(wx.MenuItem(self.__action_button_popup, menu_id, _('Review and &sign')))
		wx.EVT_MENU(self.__action_button_popup, menu_id, self.__on_sign_current_selection)

		menu_id = wx.NewId()
		self.__action_button_popup.AppendItem(wx.MenuItem(self.__action_button_popup, menu_id, _('Plot')))
		wx.EVT_MENU(self.__action_button_popup, menu_id, self.__on_plot_current_selection)

		menu_id = wx.NewId()
		self.__action_button_popup.AppendItem(wx.MenuItem(self.__action_button_popup, menu_id, _('Export to &file')))
		#wx.EVT_MENU(self.__action_button_popup, menu_id, self.data_grid.current_selection_to_file)
		self.__action_button_popup.Enable(id = menu_id, enable = False)

		menu_id = wx.NewId()
		self.__action_button_popup.AppendItem(wx.MenuItem(self.__action_button_popup, menu_id, _('Export to &clipboard')))
		#wx.EVT_MENU(self.__action_button_popup, menu_id, self.data_grid.current_selection_to_clipboard)
		self.__action_button_popup.Enable(id = menu_id, enable = False)

		menu_id = wx.NewId()
		self.__action_button_popup.AppendItem(wx.MenuItem(self.__action_button_popup, menu_id, _('&Delete')))
		wx.EVT_MENU(self.__action_button_popup, menu_id, self.__on_delete_current_selection)

		# FIXME: create inbox message to staff to phone patient to come in
		# FIXME: generate and let edit a SOAP narrative and include the values

		self._PRW_panel.add_callback_on_selection(callback = self._on_panel_selected)
		self._PRW_panel.add_callback_on_modified(callback = self._on_panel_selection_modified)

		self.panel_data_grid.show_by_panel = True
		self.panel_data_grid.panel_to_show = None
		self.panel_data_grid.Hide()
		self.Layout()

		self._PRW_panel.SetFocus()
	#--------------------------------------------------------
	# reget mixin API
	#--------------------------------------------------------
	def _populate_with_data(self):
		"""Populate fields in pages with data from model."""
		pat = gmPerson.gmCurrentPatient()
		if pat.connected:
			self.data_grid.patient = pat
			self.panel_data_grid.patient = pat
		else:
			self.data_grid.patient = None
			self.panel_data_grid.patient = None
		return True

#================================================================
# editing widgets
#================================================================
from Gnumed.wxGladeWidgets import wxgMeasurementsReviewDlg

class cMeasurementsReviewDlg(wxgMeasurementsReviewDlg.wxgMeasurementsReviewDlg):

	def __init__(self, *args, **kwargs):

		try:
			tests = kwargs['tests']
			del kwargs['tests']
			test_count = len(tests)
			try: del kwargs['test_count']
			except KeyError: pass
		except KeyError:
			tests = None
			test_count = kwargs['test_count']
			del kwargs['test_count']

		wxgMeasurementsReviewDlg.wxgMeasurementsReviewDlg.__init__(self, *args, **kwargs)

		if tests is None:
			msg = _('%s results selected. Too many to list individually.') % test_count
		else:
			msg = ' // '.join (
				[	u'%s: %s %s (%s)' % (
						t['unified_abbrev'],
						t['unified_val'],
						t['val_unit'],
						gmDateTime.pydt_strftime(t['clin_when'], '%Y %b %d')
					) for t in tests
				]
			)

		self._LBL_tests.SetLabel(msg)

		if test_count == 1:
			self._TCTRL_comment.Enable(True)
			self._TCTRL_comment.SetValue(gmTools.coalesce(tests[0]['review_comment'], u''))
			if tests[0]['you_are_responsible']:
				self._CHBOX_responsible.Enable(False)

		self.Fit()
	#--------------------------------------------------------
	# event handling
	#--------------------------------------------------------
	def _on_signoff_button_pressed(self, evt):
		if self.IsModal():
			self.EndModal(wx.ID_APPLY)
		else:
			self.Close()
#================================================================
from Gnumed.wxGladeWidgets import wxgMeasurementEditAreaPnl

class cMeasurementEditAreaPnl(wxgMeasurementEditAreaPnl.wxgMeasurementEditAreaPnl, gmEditArea.cGenericEditAreaMixin):
	"""This edit area saves *new* measurements into the active patient only."""

	def __init__(self, *args, **kwargs):

		try:
			self.__default_date = kwargs['date']
			del kwargs['date']
		except KeyError:
			self.__default_date = None

		wxgMeasurementEditAreaPnl.wxgMeasurementEditAreaPnl.__init__(self, *args, **kwargs)
		gmEditArea.cGenericEditAreaMixin.__init__(self)

		self.__register_interests()

		self.successful_save_msg = _('Successfully saved measurement.')

		self._DPRW_evaluated.display_accuracy = gmDateTime.acc_minutes
	#--------------------------------------------------------
	# generic edit area mixin API
	#--------------------------------------------------------
	def _refresh_as_new(self):
		self._PRW_test.SetText(u'', None, True)
		self.__refresh_loinc_info()
		self.__refresh_previous_value()
		self.__update_units_context()
		self._TCTRL_result.SetValue(u'')
		self._PRW_units.SetText(u'', None, True)
		self._PRW_abnormality_indicator.SetText(u'', None, True)
		if self.__default_date is None:
			self._DPRW_evaluated.SetData(data = pyDT.datetime.now(tz = gmDateTime.gmCurrentLocalTimezone))
		else:
			self._DPRW_evaluated.SetData(data =	None)
		self._TCTRL_note_test_org.SetValue(u'')
		self._PRW_intended_reviewer.SetData(gmStaff.gmCurrentProvider()['pk_staff'])
		self._PRW_problem.SetData()
		self._TCTRL_narrative.SetValue(u'')
		self._CHBOX_review.SetValue(False)
		self._CHBOX_abnormal.SetValue(False)
		self._CHBOX_relevant.SetValue(False)
		self._CHBOX_abnormal.Enable(False)
		self._CHBOX_relevant.Enable(False)
		self._TCTRL_review_comment.SetValue(u'')
		self._TCTRL_normal_min.SetValue(u'')
		self._TCTRL_normal_max.SetValue(u'')
		self._TCTRL_normal_range.SetValue(u'')
		self._TCTRL_target_min.SetValue(u'')
		self._TCTRL_target_max.SetValue(u'')
		self._TCTRL_target_range.SetValue(u'')
		self._TCTRL_norm_ref_group.SetValue(u'')

		self._PRW_test.SetFocus()
	#--------------------------------------------------------
	def _refresh_from_existing(self):
		self._PRW_test.SetData(data = self.data['pk_test_type'])
		self.__refresh_loinc_info()
		self.__refresh_previous_value()
		self.__update_units_context()
		self._TCTRL_result.SetValue(self.data['unified_val'])
		self._PRW_units.SetText(self.data['val_unit'], self.data['val_unit'], True)
		self._PRW_abnormality_indicator.SetText (
			gmTools.coalesce(self.data['abnormality_indicator'], u''),
			gmTools.coalesce(self.data['abnormality_indicator'], u''),
			True
		)
		self._DPRW_evaluated.SetData(data = self.data['clin_when'])
		self._TCTRL_note_test_org.SetValue(gmTools.coalesce(self.data['note_test_org'], u''))
		self._PRW_intended_reviewer.SetData(self.data['pk_intended_reviewer'])
		self._PRW_problem.SetData(self.data['pk_episode'])
		self._TCTRL_narrative.SetValue(gmTools.coalesce(self.data['comment'], u''))
		self._CHBOX_review.SetValue(False)
		self._CHBOX_abnormal.SetValue(gmTools.coalesce(self.data['is_technically_abnormal'], False))
		self._CHBOX_relevant.SetValue(gmTools.coalesce(self.data['is_clinically_relevant'], False))
		self._CHBOX_abnormal.Enable(False)
		self._CHBOX_relevant.Enable(False)
		self._TCTRL_review_comment.SetValue(gmTools.coalesce(self.data['review_comment'], u''))
		self._TCTRL_normal_min.SetValue(unicode(gmTools.coalesce(self.data['val_normal_min'], u'')))
		self._TCTRL_normal_max.SetValue(unicode(gmTools.coalesce(self.data['val_normal_max'], u'')))
		self._TCTRL_normal_range.SetValue(gmTools.coalesce(self.data['val_normal_range'], u''))
		self._TCTRL_target_min.SetValue(unicode(gmTools.coalesce(self.data['val_target_min'], u'')))
		self._TCTRL_target_max.SetValue(unicode(gmTools.coalesce(self.data['val_target_max'], u'')))
		self._TCTRL_target_range.SetValue(gmTools.coalesce(self.data['val_target_range'], u''))
		self._TCTRL_norm_ref_group.SetValue(gmTools.coalesce(self.data['norm_ref_group'], u''))

		self._TCTRL_result.SetFocus()
	#--------------------------------------------------------
	def _refresh_as_new_from_existing(self):
		self._refresh_from_existing()

		self._PRW_test.SetText(u'', None, True)
		self.__refresh_loinc_info()
		self.__refresh_previous_value()
		self.__update_units_context()
		self._TCTRL_result.SetValue(u'')
		self._PRW_units.SetText(u'', None, True)
		self._PRW_abnormality_indicator.SetText(u'', None, True)
		# self._DPRW_evaluated
		self._TCTRL_note_test_org.SetValue(u'')
		self._TCTRL_narrative.SetValue(u'')
		self._CHBOX_review.SetValue(False)
		self._CHBOX_abnormal.SetValue(False)
		self._CHBOX_relevant.SetValue(False)
		self._CHBOX_abnormal.Enable(False)
		self._CHBOX_relevant.Enable(False)
		self._TCTRL_review_comment.SetValue(u'')
		self._TCTRL_normal_min.SetValue(u'')
		self._TCTRL_normal_max.SetValue(u'')
		self._TCTRL_normal_range.SetValue(u'')
		self._TCTRL_target_min.SetValue(u'')
		self._TCTRL_target_max.SetValue(u'')
		self._TCTRL_target_range.SetValue(u'')
		self._TCTRL_norm_ref_group.SetValue(u'')

		self._PRW_test.SetFocus()
	#--------------------------------------------------------
	def _valid_for_save(self):

		validity = True

		if not self._DPRW_evaluated.is_valid_timestamp():
			self._DPRW_evaluated.display_as_valid(False)
			validity = False
		else:
			self._DPRW_evaluated.display_as_valid(True)

		if self._TCTRL_result.GetValue().strip() == u'':
			validity = False
			self.display_ctrl_as_valid(self._TCTRL_result, False)
		else:
			self.display_ctrl_as_valid(self._TCTRL_result, True)

		if self._PRW_problem.GetValue().strip() == u'':
			self._PRW_problem.display_as_valid(False)
			validity = False
		else:
			self._PRW_problem.display_as_valid(True)

		if self._PRW_test.GetValue().strip() == u'':
			self._PRW_test.display_as_valid(False)
			validity = False
		else:
			self._PRW_test.display_as_valid(True)

		if self._PRW_intended_reviewer.GetData() is None:
			self._PRW_intended_reviewer.display_as_valid(False)
			validity = False
		else:
			self._PRW_intended_reviewer.display_as_valid(True)

		if self._PRW_units.GetValue().strip() == u'':
			self._PRW_units.display_as_valid(False)
			validity = False
		else:
			self._PRW_units.display_as_valid(True)

		ctrls = [self._TCTRL_normal_min, self._TCTRL_normal_max, self._TCTRL_target_min, self._TCTRL_target_max]
		for widget in ctrls:
			val = widget.GetValue().strip()
			if val == u'':
				continue
			try:
				decimal.Decimal(val.replace(',', u'.', 1))
				self.display_ctrl_as_valid(widget, True)
			except:
				validity = False
				self.display_ctrl_as_valid(widget, False)

		if validity is False:
			gmDispatcher.send(signal = 'statustext', msg = _('Cannot save result. Invalid or missing essential input.'))

		return validity
	#--------------------------------------------------------
	def _save_as_new(self):

		emr = gmPerson.gmCurrentPatient().get_emr()

		success, result = gmTools.input2decimal(self._TCTRL_result.GetValue())
		if success:
			v_num = result
			v_al = None
		else:
			v_al = self._TCTRL_result.GetValue().strip()
			v_num = None

		pk_type = self._PRW_test.GetData()
		if pk_type is None:
			tt = gmPathLab.create_measurement_type (
				lab = None,
				abbrev = self._PRW_test.GetValue().strip(),
				name = self._PRW_test.GetValue().strip(),
				unit = gmTools.coalesce(self._PRW_units.GetData(), self._PRW_units.GetValue()).strip()
			)
			pk_type = tt['pk_test_type']

		tr = emr.add_test_result (
			episode = self._PRW_problem.GetData(can_create=True, is_open=False),
			type = pk_type,
			intended_reviewer = self._PRW_intended_reviewer.GetData(),
			val_num = v_num,
			val_alpha = v_al,
			unit = self._PRW_units.GetValue()
		)

		tr['clin_when'] = self._DPRW_evaluated.GetData().get_pydt()

		ctrls = [
			('abnormality_indicator', self._PRW_abnormality_indicator),
			('note_test_org', self._TCTRL_note_test_org),
			('comment', self._TCTRL_narrative),
			('val_normal_range', self._TCTRL_normal_range),
			('val_target_range', self._TCTRL_target_range),
			('norm_ref_group', self._TCTRL_norm_ref_group)
		]
		for field, widget in ctrls:
			tr[field] = widget.GetValue().strip()

		ctrls = [
			('val_normal_min', self._TCTRL_normal_min),
			('val_normal_max', self._TCTRL_normal_max),
			('val_target_min', self._TCTRL_target_min),
			('val_target_max', self._TCTRL_target_max)
		]
		for field, widget in ctrls:
			val = widget.GetValue().strip()
			if val == u'':
				tr[field] = None
			else:
				tr[field] = decimal.Decimal(val.replace(',', u'.', 1))

		tr.save_payload()

		if self._CHBOX_review.GetValue() is True:
			tr.set_review (
				technically_abnormal = self._CHBOX_abnormal.GetValue(),
				clinically_relevant = self._CHBOX_relevant.GetValue(),
				comment = gmTools.none_if(self._TCTRL_review_comment.GetValue().strip(), u''),
				make_me_responsible = False
			)

		self.data = tr

		wx.CallAfter (
			plot_adjacent_measurements,
			test = self.data,
			plot_singular_result = False,
			use_default_template = True
		)

		return True
	#--------------------------------------------------------
	def _save_as_update(self):

		success, result = gmTools.input2decimal(self._TCTRL_result.GetValue())
		if success:
			v_num = result
			v_al = None
		else:
			v_num = None
			v_al = self._TCTRL_result.GetValue().strip()

		pk_type = self._PRW_test.GetData()
		if pk_type is None:
			tt = gmPathLab.create_measurement_type (
				lab = None,
				abbrev = self._PRW_test.GetValue().strip(),
				name = self._PRW_test.GetValue().strip(),
				unit = gmTools.none_if(self._PRW_units.GetValue().strip(), u'')
			)
			pk_type = tt['pk_test_type']

		tr = self.data

		tr['pk_episode'] = self._PRW_problem.GetData(can_create=True, is_open=False)
		tr['pk_test_type'] = pk_type
		tr['pk_intended_reviewer'] = self._PRW_intended_reviewer.GetData()
		tr['val_num'] = v_num
		tr['val_alpha'] = v_al
		tr['val_unit'] = gmTools.coalesce(self._PRW_units.GetData(), self._PRW_units.GetValue()).strip()
		tr['clin_when'] = self._DPRW_evaluated.GetData().get_pydt()

		ctrls = [
			('abnormality_indicator', self._PRW_abnormality_indicator),
			('note_test_org', self._TCTRL_note_test_org),
			('comment', self._TCTRL_narrative),
			('val_normal_range', self._TCTRL_normal_range),
			('val_target_range', self._TCTRL_target_range),
			('norm_ref_group', self._TCTRL_norm_ref_group)
		]
		for field, widget in ctrls:
			tr[field] = widget.GetValue().strip()

		ctrls = [
			('val_normal_min', self._TCTRL_normal_min),
			('val_normal_max', self._TCTRL_normal_max),
			('val_target_min', self._TCTRL_target_min),
			('val_target_max', self._TCTRL_target_max)
		]
		for field, widget in ctrls:
			val = widget.GetValue().strip()
			if val == u'':
				tr[field] = None
			else:
				tr[field] = decimal.Decimal(val.replace(',', u'.', 1))

		tr.save_payload()

		if self._CHBOX_review.GetValue() is True:
			tr.set_review (
				technically_abnormal = self._CHBOX_abnormal.GetValue(),
				clinically_relevant = self._CHBOX_relevant.GetValue(),
				comment = gmTools.none_if(self._TCTRL_review_comment.GetValue().strip(), u''),
				make_me_responsible = False
			)

		wx.CallAfter (
			plot_adjacent_measurements,
			test = self.data,
			plot_singular_result = False,
			use_default_template = True
		)

		return True
	#--------------------------------------------------------
	# event handling
	#--------------------------------------------------------
	def __register_interests(self):
		self._PRW_test.add_callback_on_lose_focus(self._on_leave_test_prw)
		self._PRW_abnormality_indicator.add_callback_on_lose_focus(self._on_leave_indicator_prw)
	#--------------------------------------------------------
	def _on_leave_test_prw(self):
		self.__refresh_loinc_info()
		self.__refresh_previous_value()
		self.__update_units_context()
	#--------------------------------------------------------
	def _on_leave_indicator_prw(self):
		# if the user hasn't explicitly enabled reviewing
		if not self._CHBOX_review.GetValue():
			self._CHBOX_abnormal.SetValue(self._PRW_abnormality_indicator.GetValue().strip() != u'')
	#--------------------------------------------------------
	def _on_review_box_checked(self, evt):
		self._CHBOX_abnormal.Enable(self._CHBOX_review.GetValue())
		self._CHBOX_relevant.Enable(self._CHBOX_review.GetValue())
		self._TCTRL_review_comment.Enable(self._CHBOX_review.GetValue())
	#--------------------------------------------------------
	def _on_test_info_button_pressed(self, event):

		pk = self._PRW_test.GetData()
		if pk is not None:
			tt = gmPathLab.cMeasurementType(aPK_obj = pk)
			search_term = u'%s %s %s' % (
				tt['name'],
				tt['abbrev'],
				gmTools.coalesce(tt['loinc'], u'')
			)
		else:
			search_term = self._PRW_test.GetValue()

		search_term = search_term.replace(' ', u'+')

		call_browser_on_measurement_type(measurement_type = search_term)
	#--------------------------------------------------------
	# internal helpers
	#--------------------------------------------------------
	def __update_units_context(self):

		self._PRW_units.unset_context(context = u'loinc')

		tt = self._PRW_test.GetData(as_instance = True)

		if tt is None:
			self._PRW_units.unset_context(context = u'pk_type')
			if self._PRW_test.GetValue().strip() == u'':
				self._PRW_units.unset_context(context = u'test_name')
			else:
				self._PRW_units.set_context(context = u'test_name', val = self._PRW_test.GetValue().strip())
			return

		self._PRW_units.set_context(context = u'pk_type', val = tt['pk_test_type'])
		self._PRW_units.set_context(context = u'test_name', val = tt['name'])

		if tt['loinc'] is None:
			return

		self._PRW_units.set_context(context = u'loinc', val = tt['loinc'])
	#--------------------------------------------------------
	def __refresh_loinc_info(self):

		self._TCTRL_loinc.SetValue(u'')

		if self._PRW_test.GetData() is None:
			return

		tt = self._PRW_test.GetData(as_instance = True)

		if tt['loinc'] is None:
			return

		info = gmLOINC.loinc2term(loinc = tt['loinc'])
		if len(info) == 0:
			self._TCTRL_loinc.SetValue(u'')
			return

		self._TCTRL_loinc.SetValue(u'%s: %s' % (tt['loinc'], info[0]))
	#--------------------------------------------------------
	def __refresh_previous_value(self):
		self._TCTRL_previous_value.SetValue(u'')
		# it doesn't make much sense to show the most
		# recent value when editing an existing one
		if self.data is not None:
			return
		if self._PRW_test.GetData() is None:
			return
		tt = self._PRW_test.GetData(as_instance = True)
		most_recent = tt.get_most_recent_results (
			no_of_results = 1,
			patient = gmPerson.gmCurrentPatient().ID
		)
		if most_recent is None:
			return
		self._TCTRL_previous_value.SetValue(_('%s ago: %s%s%s - %s') % (
			gmDateTime.format_interval_medically(gmDateTime.pydt_now_here() - most_recent['clin_when']),
			most_recent['unified_val'],
			most_recent['val_unit'],
			gmTools.coalesce(most_recent['abnormality_indicator'], u'', u' (%s)'),
			most_recent['name_tt']
		))

#================================================================
# measurement type handling
#================================================================
def pick_measurement_types(parent=None, msg=None, right_column=None, picks=None):

	if parent is None:
		parent = wx.GetApp().GetTopWindow()

	if msg is None:
		msg = _('Pick the relevant measurement types.')

	if right_column is None:
		right_columns = [_('Picked')]
	else:
		right_columns = [right_column]

	picker = gmListWidgets.cItemPickerDlg(parent, -1, msg = msg)
	picker.set_columns(columns = [_('Known measurement types')], columns_right = right_columns)
	types = gmPathLab.get_measurement_types(order_by = 'unified_abbrev')
	picker.set_choices (
		choices = [
			u'%s: %s%s' % (
				t['unified_abbrev'],
				t['unified_name'],
				gmTools.coalesce(t['name_org'], u'', u' (%s)')
			)
			for t in types
		],
		data = types
	)
	if picks is not None:
		picker.set_picks (
			picks = [
				u'%s: %s%s' % (
					p['unified_abbrev'],
					p['unified_name'],
					gmTools.coalesce(p['name_org'], u'', u' (%s)')
				)
				for p in picks
			],
			data = picks
		)
	result = picker.ShowModal()

	if result == wx.ID_CANCEL:
		picker.Destroy()
		return None

	picks = picker.picks
	picker.Destroy()
	return picks

#----------------------------------------------------------------
def manage_measurement_types(parent=None):

	if parent is None:
		parent = wx.GetApp().GetTopWindow()

	#------------------------------------------------------------
	def edit(test_type=None):
		ea = cMeasurementTypeEAPnl(parent = parent, id = -1, type = test_type)
		dlg = gmEditArea.cGenericEditAreaDlg2 (
			parent = parent,
			id = -1,
			edit_area = ea,
			single_entry = gmTools.bool2subst((test_type is None), False, True)
		)
		dlg.SetTitle(gmTools.coalesce(test_type, _('Adding measurement type'), _('Editing measurement type')))

		if dlg.ShowModal() == wx.ID_OK:
			dlg.Destroy()
			return True

		dlg.Destroy()
		return False
	#------------------------------------------------------------
	def delete(measurement_type):
		if measurement_type.in_use:
			gmDispatcher.send (
				signal = 'statustext',
				beep = True,
				msg = _('Cannot delete measurement type [%s (%s)] because it is in use.') % (measurement_type['name'], measurement_type['abbrev'])
			)
			return False
		gmPathLab.delete_measurement_type(measurement_type = measurement_type['pk_test_type'])
		return True
	#------------------------------------------------------------
	def get_tooltip(test_type):
		return test_type.format()
	#------------------------------------------------------------
	def refresh(lctrl):
		mtypes = gmPathLab.get_measurement_types(order_by = 'name, abbrev')
		items = [ [
			m['abbrev'],
			m['name'],
			gmTools.coalesce(m['conversion_unit'], u''),
			gmTools.coalesce(m['loinc'], u''),
			gmTools.coalesce(m['comment_type'], u''),
			gmTools.coalesce(m['name_org'], u'?'),
			gmTools.coalesce(m['comment_org'], u''),
			m['pk_test_type']
		] for m in mtypes ]
		lctrl.set_string_items(items)
		lctrl.set_data(mtypes)
	#------------------------------------------------------------
	msg = _(
		'\n'
		'These are the measurement types currently defined in GNUmed.\n'
		'\n'
	)

	gmListWidgets.get_choices_from_list (
		parent = parent,
		msg = msg,
		caption = _('Showing measurement types.'),
		columns = [ _('Abbrev'), _('Name'), _('Unit'), _('LOINC'), _('Comment'), _('Org'), _('Comment'), u'#' ],
		single_selection = True,
		refresh_callback = refresh,
		edit_callback = edit,
		new_callback = edit,
		delete_callback = delete,
		list_tooltip_callback = get_tooltip
	)
#----------------------------------------------------------------
class cMeasurementTypePhraseWheel(gmPhraseWheel.cPhraseWheel):

	def __init__(self, *args, **kwargs):

		query = u"""
SELECT DISTINCT ON (field_label)
	pk_test_type AS data,
	name
		|| ' ('
		|| coalesce (
			(SELECT unit || ' @ ' || organization FROM clin.v_test_orgs c_vto WHERE c_vto.pk_test_org = c_vtt.pk_test_org),
			'%(in_house)s'
			)
		|| ')'
	AS field_label,
	name
		|| ' ('
		|| abbrev || ', '
		|| coalesce(abbrev_meta || ': ' || name_meta || ', ', '')
		|| coalesce (
			(SELECT unit || ' @ ' || organization FROM clin.v_test_orgs c_vto WHERE c_vto.pk_test_org = c_vtt.pk_test_org),
			'%(in_house)s'
			)
		|| ')'
	AS list_label
FROM
	clin.v_test_types c_vtt
WHERE
	abbrev_meta %%(fragment_condition)s
		OR
	name_meta %%(fragment_condition)s
		OR
	abbrev %%(fragment_condition)s
		OR
	name %%(fragment_condition)s
ORDER BY field_label
LIMIT 50""" % {'in_house': _('generic / in house lab')}

		mp = gmMatchProvider.cMatchProvider_SQL2(queries=query)
		mp.setThresholds(1, 2, 4)
		mp.word_separators = '[ \t:@]+'
		gmPhraseWheel.cPhraseWheel.__init__(self, *args, **kwargs)
		self.matcher = mp
		self.SetToolTipString(_('Select the type of measurement.'))
		self.selection_only = False
	#------------------------------------------------------------
	def _data2instance(self):
		if self.GetData() is None:
			return None

		return gmPathLab.cMeasurementType(aPK_obj = self.GetData())
#----------------------------------------------------------------
from Gnumed.wxGladeWidgets import wxgMeasurementTypeEAPnl

class cMeasurementTypeEAPnl(wxgMeasurementTypeEAPnl.wxgMeasurementTypeEAPnl, gmEditArea.cGenericEditAreaMixin):

	def __init__(self, *args, **kwargs):

		try:
			data = kwargs['type']
			del kwargs['type']
		except KeyError:
			data = None

		wxgMeasurementTypeEAPnl.wxgMeasurementTypeEAPnl.__init__(self, *args, **kwargs)
		gmEditArea.cGenericEditAreaMixin.__init__(self)
		self.mode = 'new'
		self.data = data
		if data is not None:
			self.mode = 'edit'

		self.__init_ui()

	#----------------------------------------------------------------
	def __init_ui(self):

		# name phraseweel
		query = u"""
select distinct on (name)
	pk,
	name
from clin.test_type
where
	name %(fragment_condition)s
order by name
limit 50"""
		mp = gmMatchProvider.cMatchProvider_SQL2(queries=query)
		mp.setThresholds(1, 2, 4)
		self._PRW_name.matcher = mp
		self._PRW_name.selection_only = False
		self._PRW_name.add_callback_on_lose_focus(callback = self._on_name_lost_focus)

		# abbreviation
		query = u"""
select distinct on (abbrev)
	pk,
	abbrev
from clin.test_type
where
	abbrev %(fragment_condition)s
order by abbrev
limit 50"""
		mp = gmMatchProvider.cMatchProvider_SQL2(queries=query)
		mp.setThresholds(1, 2, 3)
		self._PRW_abbrev.matcher = mp
		self._PRW_abbrev.selection_only = False

		# unit
		self._PRW_conversion_unit.selection_only = False

		# loinc
		query = u"""
SELECT DISTINCT ON (list_label)
	data,
	field_label,
	list_label
FROM ((

		SELECT
			loinc AS data,
			loinc AS field_label,
			(loinc || ': ' || abbrev || ' (' || name || ')') AS list_label
		FROM clin.test_type
		WHERE loinc %(fragment_condition)s
		LIMIT 50

	) UNION ALL (

		SELECT
			code AS data,
			code AS field_label,
			(code || ': ' || term) AS list_label
		FROM ref.v_coded_terms
		WHERE
			coding_system = 'LOINC'
				AND
			lang = i18n.get_curr_lang()
				AND
			(code %(fragment_condition)s
				OR
			term %(fragment_condition)s)
		LIMIT 50

	) UNION ALL (

		SELECT
			code AS data,
			code AS field_label,
			(code || ': ' || term) AS list_label
		FROM ref.v_coded_terms
		WHERE
			coding_system = 'LOINC'
				AND
			lang = 'en_EN'
				AND
			(code %(fragment_condition)s
				OR
			term %(fragment_condition)s)
		LIMIT 50

	) UNION ALL (

		SELECT
			code AS data,
			code AS field_label,
			(code || ': ' || term) AS list_label
		FROM ref.v_coded_terms
		WHERE
			coding_system = 'LOINC'
				AND
			(code %(fragment_condition)s
				OR
			term %(fragment_condition)s)
		LIMIT 50
	)
) AS all_known_loinc

ORDER BY list_label
LIMIT 50"""
		mp = gmMatchProvider.cMatchProvider_SQL2(queries = query)
		mp.setThresholds(1, 2, 4)
		self._PRW_loinc.matcher = mp
		self._PRW_loinc.selection_only = False
		self._PRW_loinc.add_callback_on_lose_focus(callback = self._on_loinc_lost_focus)
	#----------------------------------------------------------------
	def _on_name_lost_focus(self):

		test = self._PRW_name.GetValue().strip()

		if test == u'':
			self._PRW_conversion_unit.unset_context(context = u'test_name')
			return

		self._PRW_conversion_unit.set_context(context = u'test_name', val = test)
	#----------------------------------------------------------------
	def _on_loinc_lost_focus(self):
		loinc = self._PRW_loinc.GetData()

		if loinc is None:
			self._TCTRL_loinc_info.SetValue(u'')
			self._PRW_conversion_unit.unset_context(context = u'loinc')
			return

		self._PRW_conversion_unit.set_context(context = u'loinc', val = loinc)

		info = gmLOINC.loinc2term(loinc = loinc)
		if len(info) == 0:
			self._TCTRL_loinc_info.SetValue(u'')
			return

		self._TCTRL_loinc_info.SetValue(info[0])
	#----------------------------------------------------------------
	# generic Edit Area mixin API
	#----------------------------------------------------------------
	def _valid_for_save(self):

		has_errors = False
		for field in [self._PRW_name, self._PRW_abbrev, self._PRW_conversion_unit]:
			if field.GetValue().strip() in [u'', None]:
				has_errors = True
				field.display_as_valid(valid = False)
			else:
				field.display_as_valid(valid = True)
			field.Refresh()

		return (not has_errors)
	#----------------------------------------------------------------
	def _save_as_new(self):

		pk_org = self._PRW_test_org.GetData()
		if pk_org is None:
			pk_org = gmPathLab.create_test_org (
				name = gmTools.none_if(self._PRW_test_org.GetValue().strip(), u''),
				comment = gmTools.none_if(self._TCTRL_comment_org.GetValue().strip(), u'')
			)['pk_test_org']

		tt = gmPathLab.create_measurement_type (
			lab = pk_org,
			abbrev = self._PRW_abbrev.GetValue().strip(),
			name = self._PRW_name.GetValue().strip(),
			unit = gmTools.coalesce (
				self._PRW_conversion_unit.GetData(),
				self._PRW_conversion_unit.GetValue()
			).strip()
		)
		if self._PRW_loinc.GetData() is not None:
			tt['loinc'] = gmTools.none_if(self._PRW_loinc.GetData().strip(), u'')
		else:
			tt['loinc'] = gmTools.none_if(self._PRW_loinc.GetValue().strip(), u'')
		tt['comment_type'] = gmTools.none_if(self._TCTRL_comment_type.GetValue().strip(), u'')
		tt['pk_meta_test_type'] = self._PRW_meta_type.GetData()

		tt.save()

		self.data = tt

		return True
	#----------------------------------------------------------------
	def _save_as_update(self):

		pk_org = self._PRW_test_org.GetData()
		if pk_org is None:
			pk_org = gmPathLab.create_test_org (
				name = gmTools.none_if(self._PRW_test_org.GetValue().strip(), u''),
				comment = gmTools.none_if(self._TCTRL_comment_org.GetValue().strip(), u'')
			)['pk_test_org']

		self.data['pk_test_org'] = pk_org
		self.data['abbrev'] = self._PRW_abbrev.GetValue().strip()
		self.data['name'] = self._PRW_name.GetValue().strip()
		self.data['conversion_unit'] = gmTools.coalesce (
			self._PRW_conversion_unit.GetData(),
			self._PRW_conversion_unit.GetValue()
		).strip()
		if self._PRW_loinc.GetData() is not None:
			self.data['loinc'] = gmTools.none_if(self._PRW_loinc.GetData().strip(), u'')
		if self._PRW_loinc.GetData() is not None:
			self.data['loinc'] = gmTools.none_if(self._PRW_loinc.GetData().strip(), u'')
		else:
			self.data['loinc'] = gmTools.none_if(self._PRW_loinc.GetValue().strip(), u'')
		self.data['comment_type'] = gmTools.none_if(self._TCTRL_comment_type.GetValue().strip(), u'')
		self.data['pk_meta_test_type'] = self._PRW_meta_type.GetData()
		self.data.save()

		return True
	#----------------------------------------------------------------
	def _refresh_as_new(self):
		self._PRW_name.SetText(u'', None, True)
		self._on_name_lost_focus()
		self._PRW_abbrev.SetText(u'', None, True)
		self._PRW_conversion_unit.SetText(u'', None, True)
		self._PRW_loinc.SetText(u'', None, True)
		self._on_loinc_lost_focus()
		self._TCTRL_comment_type.SetValue(u'')
		self._PRW_test_org.SetText(u'', None, True)
		self._TCTRL_comment_org.SetValue(u'')
		self._PRW_meta_type.SetText(u'', None, True)

		self._PRW_name.SetFocus()
	#----------------------------------------------------------------
	def _refresh_from_existing(self):
		self._PRW_name.SetText(self.data['name'], self.data['name'], True)
		self._on_name_lost_focus()
		self._PRW_abbrev.SetText(self.data['abbrev'], self.data['abbrev'], True)
		self._PRW_conversion_unit.SetText (
			gmTools.coalesce(self.data['conversion_unit'], u''),
			self.data['conversion_unit'],
			True
		)
		self._PRW_loinc.SetText (
			gmTools.coalesce(self.data['loinc'], u''),
			self.data['loinc'],
			True
		)
		self._on_loinc_lost_focus()
		self._TCTRL_comment_type.SetValue(gmTools.coalesce(self.data['comment_type'], u''))
		self._PRW_test_org.SetText (
			gmTools.coalesce(self.data['pk_test_org'], u'', self.data['name_org']),
			self.data['pk_test_org'],
			True
		)
		self._TCTRL_comment_org.SetValue(gmTools.coalesce(self.data['comment_org'], u''))
		if self.data['pk_meta_test_type'] is None:
			self._PRW_meta_type.SetText(u'', None, True)
		else:
			self._PRW_meta_type.SetText(u'%s: %s' % (self.data['abbrev_meta'], self.data['name_meta']), self.data['pk_meta_test_type'], True)

		self._PRW_name.SetFocus()
	#----------------------------------------------------------------
	def _refresh_as_new_from_existing(self):
		self._refresh_as_new()
		self._PRW_test_org.SetText (
			gmTools.coalesce(self.data['pk_test_org'], u'', self.data['name_org']),
			self.data['pk_test_org'],
			True
		)
		self._TCTRL_comment_org.SetValue(gmTools.coalesce(self.data['comment_org'], u''))

		self._PRW_name.SetFocus()

#================================================================
_SQL_units_from_test_results = u"""
	-- via clin.v_test_results.pk_type (for types already used in results)
	SELECT
		val_unit AS data,
		val_unit AS field_label,
		val_unit || ' (' || name_tt || ')' AS list_label,
		1 AS rank
	FROM
		clin.v_test_results
	WHERE
		(
			val_unit %(fragment_condition)s
				OR
			conversion_unit %(fragment_condition)s
		)
		%(ctxt_type_pk)s
		%(ctxt_test_name)s
"""

_SQL_units_from_test_types = u"""
	-- via clin.test_type (for types not yet used in results)
	SELECT
		conversion_unit AS data,
		conversion_unit AS field_label,
		conversion_unit || ' (' || name || ')' AS list_label,
		2 AS rank
	FROM
		clin.test_type
	WHERE
		conversion_unit %(fragment_condition)s
		%(ctxt_ctt)s
"""

_SQL_units_from_loinc_ipcc = u"""
	-- via ref.loinc.ipcc_units
	SELECT
		ipcc_units AS data,
		ipcc_units AS field_label,
		ipcc_units || ' (LOINC.ipcc: ' || term || ')' AS list_label,
		3 AS rank
	FROM
		ref.loinc
	WHERE
		ipcc_units %(fragment_condition)s
		%(ctxt_loinc)s
		%(ctxt_loinc_term)s
"""

_SQL_units_from_loinc_submitted = u"""
	-- via ref.loinc.submitted_units
	SELECT
		submitted_units AS data,
		submitted_units AS field_label,
		submitted_units || ' (LOINC.submitted:' || term || ')' AS list_label,
		3 AS rank
	FROM
		ref.loinc
	WHERE
		submitted_units %(fragment_condition)s
		%(ctxt_loinc)s
		%(ctxt_loinc_term)s
"""

_SQL_units_from_loinc_example = u"""
	-- via ref.loinc.example_units
	SELECT
		example_units AS data,
		example_units AS field_label,
		example_units || ' (LOINC.example: ' || term || ')' AS list_label,
		3 AS rank
	FROM
		ref.loinc
	WHERE
		example_units %(fragment_condition)s
		%(ctxt_loinc)s
		%(ctxt_loinc_term)s
"""

_SQL_units_from_atc = u"""
	-- via ref.atc.unit
	SELECT
		unit AS data,
		unit AS field_label,
		unit || ' (ATC: ' || term || ')' AS list_label,
		2 AS rank
	FROM
		ref.atc
	WHERE
		unit IS NOT NULL
			AND
		unit %(fragment_condition)s
"""

_SQL_units_from_consumable_substance = u"""
	-- via ref.consumable_substance.unit
	SELECT
		unit AS data,
		unit AS field_label,
		unit || ' (' || description || ')' AS list_label,
		2 AS rank
	FROM
		ref.consumable_substance
	WHERE
		unit %(fragment_condition)s
		%(ctxt_substance)s
"""

#----------------------------------------------------------------
class cUnitPhraseWheel(gmPhraseWheel.cPhraseWheel):

	def __init__(self, *args, **kwargs):

		query = u"""
SELECT DISTINCT ON (data)
	data,
	field_label,
	list_label
FROM (

	SELECT
		data,
		field_label,
		list_label,
		rank
	FROM (
		(%s) UNION ALL
		(%s) UNION ALL
		(%s) UNION ALL
		(%s) UNION ALL
		(%s) UNION ALL
		(%s) UNION ALL
		(%s)
	) AS all_matching_units
	WHERE data IS NOT NULL
	ORDER BY rank

) AS ranked_matching_units
LIMIT 50""" % (
			_SQL_units_from_test_results,
			_SQL_units_from_test_types,
			_SQL_units_from_loinc_ipcc,
			_SQL_units_from_loinc_submitted,
			_SQL_units_from_loinc_example,
			_SQL_units_from_atc,
			_SQL_units_from_consumable_substance
		)

		ctxt = {
			'ctxt_type_pk': {
				'where_part': u'AND pk_test_type = %(pk_type)s',
				'placeholder': u'pk_type'
			},
			'ctxt_test_name': {
				'where_part': u'AND %(test_name)s IN (name_tt, name_meta, abbrev_meta)',
				'placeholder': u'test_name'
			},
			'ctxt_ctt': {
				'where_part': u'AND %(test_name)s IN (name, abbrev)',
				'placeholder': u'test_name'
			},
			'ctxt_loinc': {
				'where_part': u'AND code = %(loinc)s',
				'placeholder': u'loinc'
			},
			'ctxt_loinc_term': {
				'where_part': u'AND term ~* %(test_name)s',
				'placeholder': u'test_name'
			},
			'ctxt_substance': {
				'where_part': u'AND description ~* %(substance)s',
				'placeholder': u'substance'
			}
		}

		mp = gmMatchProvider.cMatchProvider_SQL2(queries = query, context = ctxt)
		mp.setThresholds(1, 2, 4)
		#mp.print_queries = True
		gmPhraseWheel.cPhraseWheel.__init__(self, *args, **kwargs)
		self.matcher = mp
		self.SetToolTipString(_('Select the desired unit for the amount or measurement.'))
		self.selection_only = False
		self.phrase_separators = u'[;|]+'
#================================================================

#================================================================
class cTestResultIndicatorPhraseWheel(gmPhraseWheel.cPhraseWheel):

	def __init__(self, *args, **kwargs):

		query = u"""
select distinct abnormality_indicator,
	abnormality_indicator, abnormality_indicator
from clin.v_test_results
where
	abnormality_indicator %(fragment_condition)s
order by abnormality_indicator
limit 25"""

		mp = gmMatchProvider.cMatchProvider_SQL2(queries=query)
		mp.setThresholds(1, 1, 2)
		mp.ignored_chars = "[.'\\\[\]#$%_]+" + '"'
		mp.word_separators = '[ \t&:]+'
		gmPhraseWheel.cPhraseWheel.__init__ (
			self,
			*args,
			**kwargs
		)
		self.matcher = mp
		self.SetToolTipString(_('Select an indicator for the level of abnormality.'))
		self.selection_only = False

#================================================================
# measurement org widgets / functions
#----------------------------------------------------------------
def edit_measurement_org(parent=None, org=None):
	ea = cMeasurementOrgEAPnl(parent = parent, id = -1)
	ea.data = org
	ea.mode = gmTools.coalesce(org, 'new', 'edit')
	dlg = gmEditArea.cGenericEditAreaDlg2(parent = parent, id = -1, edit_area = ea)
	dlg.SetTitle(gmTools.coalesce(org, _('Adding new diagnostic org'), _('Editing diagnostic org')))
	if dlg.ShowModal() == wx.ID_OK:
		dlg.Destroy()
		return True
	dlg.Destroy()
	return False
#----------------------------------------------------------------
def manage_measurement_orgs(parent=None):

	if parent is None:
		parent = wx.GetApp().GetTopWindow()

	#------------------------------------------------------------
	def edit(org=None):
		return edit_measurement_org(parent = parent, org = org)
	#------------------------------------------------------------
	def refresh(lctrl):
		orgs = gmPathLab.get_test_orgs()
		lctrl.set_string_items ([
			(o['unit'], o['organization'], gmTools.coalesce(o['test_org_contact'], u''), gmTools.coalesce(o['comment'], u''), o['pk_test_org'])
			for o in orgs
		])
		lctrl.set_data(orgs)
	#------------------------------------------------------------
	def delete(test_org):
		gmPathLab.delete_test_org(test_org = test_org['pk_test_org'])
		return True
	#------------------------------------------------------------
	gmListWidgets.get_choices_from_list (
		parent = parent,
		msg = _('\nThese are the diagnostic orgs (path labs etc) currently defined in GNUmed.\n\n'),
		caption = _('Showing diagnostic orgs.'),
		columns = [_('Name'), _('Organization'), _('Contact'), _('Comment'), u'#'],
		single_selection = True,
		refresh_callback = refresh,
		edit_callback = edit,
		new_callback = edit,
		delete_callback = delete
	)

#----------------------------------------------------------------
from Gnumed.wxGladeWidgets import wxgMeasurementOrgEAPnl

class cMeasurementOrgEAPnl(wxgMeasurementOrgEAPnl.wxgMeasurementOrgEAPnl, gmEditArea.cGenericEditAreaMixin):

	def __init__(self, *args, **kwargs):

		try:
			data = kwargs['org']
			del kwargs['org']
		except KeyError:
			data = None

		wxgMeasurementOrgEAPnl.wxgMeasurementOrgEAPnl.__init__(self, *args, **kwargs)
		gmEditArea.cGenericEditAreaMixin.__init__(self)

		self.mode = 'new'
		self.data = data
		if data is not None:
			self.mode = 'edit'

		#self.__init_ui()
	#----------------------------------------------------------------
#	def __init_ui(self):
#		# adjust phrasewheels etc
	#----------------------------------------------------------------
	# generic Edit Area mixin API
	#----------------------------------------------------------------
	def _valid_for_save(self):
		has_errors = False
		if self._PRW_org_unit.GetData() is None:
			if self._PRW_org_unit.GetValue().strip() == u'':
				has_errors = True
				self._PRW_org_unit.display_as_valid(valid = False)
			else:
				self._PRW_org_unit.display_as_valid(valid = True)
		else:
			self._PRW_org_unit.display_as_valid(valid = True)

		return (not has_errors)
	#----------------------------------------------------------------
	def _save_as_new(self):
		data = gmPathLab.create_test_org (
			name = self._PRW_org_unit.GetValue().strip(),
			comment = self._TCTRL_comment.GetValue().strip(),
			pk_org_unit = self._PRW_org_unit.GetData()
		)
		data['test_org_contact'] = self._TCTRL_contact.GetValue().strip()
		data.save()
		self.data = data
		return True
	#----------------------------------------------------------------
	def _save_as_update(self):
		# get or create the org unit
		name = self._PRW_org_unit.GetValue().strip()
		org = gmOrganization.org_exists(organization = name)
		if org is None:
			org = gmOrganization.create_org (
				organization = name,
				category = u'Laboratory'
			)
		org_unit = gmOrganization.create_org_unit (
			pk_organization = org['pk_org'],
			unit = name
		)
		# update test_org fields
		self.data['pk_org_unit'] = org_unit['pk_org_unit']
		self.data['test_org_contact'] = self._TCTRL_contact.GetValue().strip()
		self.data['comment'] = self._TCTRL_comment.GetValue().strip()
		self.data.save()
		return True
	#----------------------------------------------------------------
	def _refresh_as_new(self):
		self._PRW_org_unit.SetText(value = u'', data = None)
		self._TCTRL_contact.SetValue(u'')
		self._TCTRL_comment.SetValue(u'')
	#----------------------------------------------------------------
	def _refresh_from_existing(self):
		self._PRW_org_unit.SetText(value = self.data['unit'], data = self.data['pk_org_unit'])
		self._TCTRL_contact.SetValue(gmTools.coalesce(self.data['test_org_contact'], u''))
		self._TCTRL_comment.SetValue(gmTools.coalesce(self.data['comment'], u''))
	#----------------------------------------------------------------
	def _refresh_as_new_from_existing(self):
		self._refresh_as_new()
	#----------------------------------------------------------------
	def _on_manage_orgs_button_pressed(self, event):
		gmOrganizationWidgets.manage_orgs(parent = self)

#----------------------------------------------------------------
class cMeasurementOrgPhraseWheel(gmPhraseWheel.cPhraseWheel):

	def __init__(self, *args, **kwargs):

		query = u"""
SELECT DISTINCT ON (list_label)
	pk_test_org AS data,
	unit || ' (' || organization || ')' AS field_label,
	unit || ' @ ' || organization AS list_label
FROM clin.v_test_orgs
WHERE
	unit %(fragment_condition)s
		OR
	organization %(fragment_condition)s
ORDER BY list_label
LIMIT 50"""
		mp = gmMatchProvider.cMatchProvider_SQL2(queries=query)
		mp.setThresholds(1, 2, 4)
		#mp.word_separators = '[ \t:@]+'
		gmPhraseWheel.cPhraseWheel.__init__(self, *args, **kwargs)
		self.matcher = mp
		self.SetToolTipString(_('The name of the path lab/diagnostic organisation.'))
		self.selection_only = False
	#------------------------------------------------------------
	def _create_data(self):
		if self.GetData() is not None:
			_log.debug('data already set, not creating')
			return

		if self.GetValue().strip() == u'':
			_log.debug('cannot create new lab, missing name')
			return

		lab = gmPathLab.create_test_org(name = self.GetValue().strip())
		self.SetText(value = lab['unit'], data = lab['pk_test_org'])
		return
	#------------------------------------------------------------
	def _data2instance(self):
		return gmPathLab.cTestOrg(aPK_obj = self.GetData())

#================================================================
def manage_meta_test_types(parent=None):

	if parent is None:
		parent = wx.GetApp().GetTopWindow()

	msg = _(
		'\n'
		'These are the meta test types currently defined in GNUmed.\n'
		'\n'
		'Meta test types allow you to aggregate several actual test types used\n'
		'by pathology labs into one logical type.\n'
		'\n'
		'This is useful for grouping together results of tests which come under\n'
		'different names but really are the same thing. This often happens when\n'
		'you switch labs or the lab starts using another test method.\n'
	)

	mtts = gmPathLab.get_meta_test_types()

	gmListWidgets.get_choices_from_list (
		parent = parent,
		msg = msg,
		caption = _('Showing meta test types.'),
		columns = [_('Abbrev'), _('Name'), _('LOINC'), _('Comment'), u'#'],
		choices = [ [
			m['abbrev'],
			m['name'],
			gmTools.coalesce(m['loinc'], u''),
			gmTools.coalesce(m['comment'], u''),
			m['pk']
		] for m in mtts ],
		data = mtts,
		single_selection = True,
		#edit_callback = edit,
		#new_callback = edit,
		#delete_callback = delete,
		#refresh_callback = refresh
	)
#----------------------------------------------------------------
class cMetaTestTypePRW(gmPhraseWheel.cPhraseWheel):

	def __init__(self, *args, **kwargs):

		query = u"""
SELECT DISTINCT ON (field_label)
	c_mtt.pk
		AS data,
	c_mtt.abbrev || ': ' || name
		AS field_label,
	c_mtt.abbrev || ': ' || name
		||	coalesce (
				' (' || c_mtt.comment || ')',
				''
			)
		||	coalesce (
				', LOINC: ' || c_mtt.loinc,
				''
			)
	AS list_label
FROM
	clin.meta_test_type c_mtt
WHERE
	abbrev %(fragment_condition)s
		OR
	name %(fragment_condition)s
		OR
	loinc %(fragment_condition)s
ORDER BY field_label
LIMIT 50"""

		mp = gmMatchProvider.cMatchProvider_SQL2(queries=query)
		mp.setThresholds(1, 2, 4)
		mp.word_separators = '[ \t:@]+'
		gmPhraseWheel.cPhraseWheel.__init__(self, *args, **kwargs)
		self.matcher = mp
		self.SetToolTipString(_('Select the meta test type.'))
		self.selection_only = True
	#------------------------------------------------------------
	def _data2instance(self):
		if self.GetData() is None:
			return None

		return gmPathLab.cMetaTestType(aPK_obj = self.GetData())

#================================================================
# test panel handling
#================================================================
def edit_test_panel(parent=None, test_panel=None):
	ea = cTestPanelEAPnl(parent = parent, id = -1)
	ea.data = test_panel
	ea.mode = gmTools.coalesce(test_panel, 'new', 'edit')
	dlg = gmEditArea.cGenericEditAreaDlg2 (
		parent = parent,
		id = -1,
		edit_area = ea,
		single_entry = gmTools.bool2subst((test_panel is None), False, True)
	)
	dlg.SetTitle(gmTools.coalesce(test_panel, _('Adding new test panel'), _('Editing test panel')))
	if dlg.ShowModal() == wx.ID_OK:
		dlg.Destroy()
		return True
	dlg.Destroy()
	return False

#----------------------------------------------------------------
def manage_test_panels(parent=None):

	if parent is None:
		parent = wx.GetApp().GetTopWindow()

	#------------------------------------------------------------
	def edit(test_panel=None):
		return edit_test_panel(parent = parent, test_panel = test_panel)
	#------------------------------------------------------------
	def delete(test_panel):
		gmPathLab.delete_test_panel(pk = test_panel['pk_test_panel'])
		return True
	#------------------------------------------------------------
	def get_tooltip(test_panel):
		return test_panel.format()
	#------------------------------------------------------------
	def refresh(lctrl):
		panels = gmPathLab.get_test_panels(order_by = 'description')
		items = [ [
			p['description'],
			gmTools.coalesce(p['comment'], u''),
			p['pk_test_panel']
		] for p in panels ]
		lctrl.set_string_items(items)
		lctrl.set_data(panels)
	#------------------------------------------------------------
	msg = _(
		'\n'
		'Test panels as defined in GNUmed.\n'
	)

	gmListWidgets.get_choices_from_list (
		parent = parent,
		msg = msg,
		caption = _('Showing test panels.'),
		columns = [ _('Name'), _('Comment'), u'#' ],
		single_selection = True,
		refresh_callback = refresh,
		edit_callback = edit,
		new_callback = edit,
		delete_callback = delete,
		list_tooltip_callback = get_tooltip
	)

#----------------------------------------------------------------
class cTestPanelPRW(gmPhraseWheel.cPhraseWheel):

	def __init__(self, *args, **kwargs):
		query = u"""
SELECT
	pk_test_panel
		AS data,
	description
		AS field_label,
	description
		AS list_label
FROM
	clin.v_test_panels
WHERE
	description %(fragment_condition)s
ORDER BY field_label
LIMIT 30"""
		mp = gmMatchProvider.cMatchProvider_SQL2(queries=query)
		mp.setThresholds(1, 2, 4)
		#mp.word_separators = '[ \t:@]+'
		gmPhraseWheel.cPhraseWheel.__init__(self, *args, **kwargs)
		self.matcher = mp
		self.SetToolTipString(_('Select a test panel.'))
		self.selection_only = True
	#------------------------------------------------------------
	def _data2instance(self):
		if self.GetData() is None:
			return None
		return gmPathLab.cTestPanel(aPK_obj = self.GetData())
	#------------------------------------------------------------
	def _get_data_tooltip(self):
		if self.GetData() is None:
			return None
		return gmPathLab.cTestPanel(aPK_obj = self.GetData()).format()

#====================================================================
from Gnumed.wxGladeWidgets import wxgTestPanelEAPnl

class cTestPanelEAPnl(wxgTestPanelEAPnl.wxgTestPanelEAPnl, gmEditArea.cGenericEditAreaMixin):

	def __init__(self, *args, **kwargs):

		try:
			data = kwargs['panel']
			del kwargs['panel']
		except KeyError:
			data = None

		wxgTestPanelEAPnl.wxgTestPanelEAPnl.__init__(self, *args, **kwargs)
		gmEditArea.cGenericEditAreaMixin.__init__(self)

		self._test_types = None

		self.mode = 'new'
		self.data = data
		if data is not None:
			self.mode = 'edit'

		#self.__init_ui()
	#----------------------------------------------------------------
#	def __init_ui(self):
#		# adjust phrasewheels etc
	#----------------------------------------------------------------
	# generic Edit Area mixin API
	#----------------------------------------------------------------
	def _valid_for_save(self):
		validity = True

		if self._test_types is None:
			validity = False
			gmDispatcher.send(signal = 'statustext', msg = _('No test types selected.'))
			self._BTN_select_tests.SetFocus()

		if self._TCTRL_description.GetValue().strip() == u'':
			validity = False
			self.display_tctrl_as_valid(tctrl = self._TCTRL_description, valid = False)
			self._TCTRL_description.SetFocus()
		else:
			self.display_tctrl_as_valid(tctrl = self._TCTRL_description, valid = True)

		return validity
	#----------------------------------------------------------------
	def _save_as_new(self):
		data = gmPathLab.create_test_panel(description = self._TCTRL_description.GetValue().strip())
		data['comment'] = self._TCTRL_comment.GetValue().strip()
		data['pk_test_types'] = [ tt['pk_test_type'] for tt in self._test_types ]
		data.save()
		data.generic_codes = [ c['data'] for c in self._PRW_codes.GetData() ]
		self.data = data
		return True
	#----------------------------------------------------------------
	def _save_as_update(self):
		self.data['description'] = self._TCTRL_description.GetValue().strip()
		self.data['comment'] = self._TCTRL_comment.GetValue().strip()
		self.data['pk_test_types'] = [ tt['pk_test_type'] for tt in self._test_types ]
		self.data.save()
		self.data.generic_codes = [ c['data'] for c in self._PRW_codes.GetData() ]
		return True
	#----------------------------------------------------------------
	def __refresh_test_types_field(self, test_types=None):
		self._TCTRL_tests.SetValue(u'')
		self._test_types = test_types
		if self._test_types is None:
			return
		tmp = u';\n'.join ([
			u'%s: %s%s' % (
				t['unified_abbrev'],
				t['unified_name'],
				gmTools.coalesce(t['name_org'], u'', u' (%s)')
			)
			for t in self._test_types
		])
		self._TCTRL_tests.SetValue(tmp)
	#----------------------------------------------------------------
	def _refresh_as_new(self):
		self._TCTRL_description.SetValue(u'')
		self._TCTRL_comment.SetValue(u'')
		self.__refresh_test_types_field()
		self._PRW_codes.SetText()

		self._TCTRL_description.SetFocus()
	#----------------------------------------------------------------
	def _refresh_as_new_from_existing(self):
		self._refresh_as_new()
		self.__refresh_test_types_field(test_types = self.data.test_types)
	#----------------------------------------------------------------
	def _refresh_from_existing(self):
		self._TCTRL_description.SetValue(self.data['description'])
		self._TCTRL_comment.SetValue(gmTools.coalesce(self.data['comment'], u''))
		self.__refresh_test_types_field(test_types = self.data.test_types)
		val, data = self._PRW_codes.generic_linked_codes2item_dict(self.data.generic_codes)
		self._PRW_codes.SetText(val, data)

		self._BTN_select_tests.SetFocus()
	#----------------------------------------------------------------
	def _on_select_tests_button_pressed(self, event):
		desc = self._TCTRL_description.GetValue().strip()
		if desc == u'':
			desc = None
		picked = pick_measurement_types (
			parent = self,
			msg = _('Pick the measurement types for this panel.'),
			right_column = desc,
			picks = self._test_types
		)
		if picked is None:
			return
		if len(picked) == 0:
			picked = None
		self.__refresh_test_types_field(test_types = picked)

#================================================================
# main
#----------------------------------------------------------------
if __name__ == '__main__':

	from Gnumed.pycommon import gmLog2
	from Gnumed.wxpython import gmPatSearchWidgets

	gmI18N.activate_locale()
	gmI18N.install_domain()
	gmDateTime.init()

	#------------------------------------------------------------
	def test_grid():
		pat = gmPersonSearch.ask_for_patient()
		app = wx.PyWidgetTester(size = (500, 300))
		lab_grid = cMeasurementsGrid(parent = app.frame, id = -1)
		lab_grid.patient = pat
		app.frame.Show()
		app.MainLoop()
	#------------------------------------------------------------
	def test_test_ea_pnl():
		pat = gmPersonSearch.ask_for_patient()
		gmPatSearchWidgets.set_active_patient(patient=pat)
		app = wx.PyWidgetTester(size = (500, 300))
		ea = cMeasurementEditAreaPnl(parent = app.frame, id = -1)
		app.frame.Show()
		app.MainLoop()
	#------------------------------------------------------------
#	def test_primary_care_vitals_pnl():
#		app = wx.PyWidgetTester(size = (500, 300))
#		pnl = wxgPrimaryCareVitalsInputPnl.wxgPrimaryCareVitalsInputPnl(parent = app.frame, id = -1)
#		app.frame.Show()
#		app.MainLoop()
	#------------------------------------------------------------
	if (len(sys.argv) > 1) and (sys.argv[1] == 'test'):
		#test_grid()
		test_test_ea_pnl()
		#test_primary_care_vitals_pnl()

#================================================================
