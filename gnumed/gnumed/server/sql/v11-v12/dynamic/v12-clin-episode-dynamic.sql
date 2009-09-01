-- ==============================================================
-- GNUmed database schema change script
--
-- License: GPL
-- Author: karsten.hilbert@gmx.net
--
-- ==============================================================
-- $Id: v12-clin-episode-dynamic.sql,v 1.1 2009-08-28 12:45:26 ncq Exp $
-- $Revision: 1.1 $

-- --------------------------------------------------------------
--set default_transaction_read_only to off;
\set ON_ERROR_STOP 1

-- --------------------------------------------------------------
comment on column clin.episode.diagnostic_certainty is
'The certainty at which this problem is believed to be a diagnosis:

A: sign (Symptom)
B: cluster of signs (Symptomkomplex)
C: syndromic diagnosis (Bild einer Diagnose)
D: proven diagnosis (diagnostisch gesichert)'
;


alter table clin.episode
	add constraint valid_diagnostic_certainty
		check (diagnostic_certainty in ('A', 'B', 'C', 'D', NULL));

-- --------------------------------------------------------------
select gm.log_script_insertion('$RCSfile: v12-clin-episode-dynamic.sql,v $', '$Revision: 1.1 $');

-- ==============================================================
-- $Log: v12-clin-episode-dynamic.sql,v $
-- Revision 1.1  2009-08-28 12:45:26  ncq
-- - add diagnostic certainty
--
--