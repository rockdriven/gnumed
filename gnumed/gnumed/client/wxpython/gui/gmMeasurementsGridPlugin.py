# -*- coding: utf-8 -*-
#======================================================================
# GNUmed patient measurements plugin
#
# @copyright: author
#======================================================================
__author__ = "Karsten Hilbert"
__license__ = 'GPL v2 or later (details at http://www.gnu.org)'

import logging


from Gnumed.wxpython import gmPlugin, gmMeasurementWidgets
from Gnumed.pycommon import gmI18N
from Gnumed.wxpython import gmAccessPermissionWidgets


_log = logging.getLogger('gm.ui')
#======================================================================
class gmMeasurementsGridPlugin(gmPlugin.cNotebookPlugin):
	"""Plugin to encapsulate patient measurements."""

	tab_name = _('Measurements')
	required_minimum_role = 'full clinical access'

	@gmAccessPermissionWidgets.verify_minimum_required_role (
		required_minimum_role,
		activity = _('loading plugin <%s>') % tab_name,
		return_value_on_failure = False,
		fail_silently = False
	)
	def register(self):
		gmPlugin.cNotebookPlugin.register(self)
	#-------------------------------------------------
	def name (self):
		return gmMeasurementsGridPlugin.tab_name

	def GetWidget (self, parent):
		self._widget = gmMeasurementWidgets.cMeasurementsPnl(parent, -1)
		return self._widget

	def MenuInfo (self):
		return ('emr', _('&Measurements'))

	def can_receive_focus(self):
		if not self._verify_patient_avail():
			return None
		return 1
#======================================================================
# main
#----------------------------------------------------------------------
if __name__ == "__main__":
	print "no test code"

#======================================================================
