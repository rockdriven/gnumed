# coding: utf8
#==============================================================
# GNUmed database schema change script
#
# License: GPL v2 or later
# Author: karsten.hilbert@gmx.net
#
#==============================================================
import os

from Gnumed.pycommon import gmPG2

#--------------------------------------------------------------

def run(conn=None):

	# PKV-Rechnung mit USt.
	gmPG2.file2bytea (
		query = u"""
			UPDATE ref.paperwork_templates SET
				data = %(data)s::bytea
			WHERE
				name_long = 'Privatrechnung mit USt. (GNUmed-Vorgabe Deutschland)'""",
		filename = os.path.join('..', 'sql', 'v19-v20', 'data', 'v20-GNUmed-default_invoice_template-de.tex'),
		conn = conn
	)

	# PKV-Rechnung ohne USt.
	gmPG2.file2bytea (
		query = u"""
			UPDATE ref.paperwork_templates SET
				data = %(data)s::bytea
			WHERE
				name_long = 'Privatrechnung ohne USt. (GNUmed-Vorgabe Deutschland)'""",
		filename = os.path.join('..', 'sql', 'v19-v20', 'data', 'v20-GNUmed-default_invoice_template-de_no_vat.tex'),
		conn = conn
	)

	return True

#==============================================================