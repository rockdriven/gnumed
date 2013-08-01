
import sys

if __name__ == '__main__':
	sys.path.insert(0, '../../')

from Gnumed.pycommon import gmPG2

print "Please log in as GNUmed database owner:"
gmPG2.get_connection()

print ""
print ""
print "Looking for dangling clin.clin_root_item rows ..."

print ""
print "1) rows with dangling .fk_episode:"
cmd = u"""
	SELECT *, tableoid::regclass AS src_table FROM clin.clin_root_item
	WHERE NOT EXISTS (
		SELECT 1 FROM clin.episode WHERE pk = clin.clin_root_item.fk_episode
	)"""
rows, idx = gmPG2.run_ro_queries(queries = [{u'cmd': cmd}], get_col_idx = False)
for row in rows:
	print "dangling row:", row
	print " Looking for most recent row about episode %s in audit table ..." % row['fk_episode']
	cmd = u"""
		SELECT * FROM audit.log_episode WHERE
			pk = %(pk_epi)s
		ORDER BY row_version DESC
		LIMIT 1
	"""
	args = {'pk_epi': row['fk_episode']}
	audit_rows, idx = gmPG2.run_ro_queries(queries = [{u'cmd': cmd, 'args': args}], get_col_idx = False)
	for audit_row in audit_rows:
		print ' audited row:', audit_row

print ""
print "2) rows with dangling .fk_encounter:"
cmd = u"""
	SELECT *, tableoid::regclass AS src_table FROM clin.clin_root_item
	WHERE NOT EXISTS (
		SELECT 1 FROM clin.encounter WHERE pk = clin.clin_root_item.fk_encounter
	)"""
rows, idx = gmPG2.run_ro_queries(queries = [{u'cmd': cmd}], get_col_idx = False)
for row in rows:
	print "dangling row:", row
	print " Looking for most recent row about encounter %s in audit table ..." % row['fk_encounter']
	cmd = u"""
		SELECT * FROM audit.log_encounter WHERE
			pk = %(pk_enc)s
		ORDER BY row_version DESC
		LIMIT 1
	"""
	args = {'pk_enc': row['fk_encounter']}
	audit_rows, idx = gmPG2.run_ro_queries(queries = [{u'cmd': cmd, 'args': args}], get_col_idx = False)
	for audit_row in audit_rows:
		print ' audited row:', audit_row
