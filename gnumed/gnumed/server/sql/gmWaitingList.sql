-- Project: GNUmed - waiting list tables
-- ===================================================================
-- $Source: /home/ncq/Projekte/cvs2git/vcs-mirror/gnumed/gnumed/server/sql/gmWaitingList.sql,v $
-- $Revision: 1.1 $
-- license: GPL
-- author: Karsten Hilbert

-- ===================================================================
-- force terminate + exit(3) on errors if non-interactive
\set ON_ERROR_STOP 1

create table waiting_list (
	pk serial primary key,
	fk_patient integer
		not null
		references xlnk_identity(xfk_identity)
		on update cascade
		on delete cascade,
	registered timestamp with time zone
		not null
		default CURRENT_TIMESTAMP,
	urgency integer
		not null
		default 0,
	list_position integer
		unique
		not null
		check (list_position > 0),
	comment text
) inherits (audit_fields);

select add_table_for_audit('waiting_list');

comment on table waiting_list is
	'aggregates all the patients currently waiting for an encounter';

comment on column waiting_list.fk_patient is
	'the waiting patient';
comment on column waiting_list.registered is
	'when did the patient arrive (enter the waiting list, that is)';
comment on column waiting_list.urgency is
	'relative urgency, used by practices as they see fit,
	   0 - "standard" urgency
	 < 0 - less urgent
	 > 0 - more urgent';
comment on column waiting_list.list_position is
	'the currently assigned position of
	 this patient on the waiting list';
comment on column waiting_list.comment is
	'a free comment regarding this entry,
	 NOT THE RFE !';

-- =============================================
-- do simple schema revision tracking
select log_script_insertion('$RCSfile: gmWaitingList.sql,v $', '$Revision: 1.1 $');

-- =============================================
-- $Log: gmWaitingList.sql,v $
-- Revision 1.1  2005-09-21 10:18:59  ncq
-- - start waiting list
--
--