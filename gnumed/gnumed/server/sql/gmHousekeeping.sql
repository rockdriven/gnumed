-- Project: GnuMed - database housekeeping TODO tables
-- ===================================================================
-- $Source: /home/ncq/Projekte/cvs2git/vcs-mirror/gnumed/gnumed/server/sql/gmHousekeeping.sql,v $
-- $Revision: 1.4 $
-- license: GPL
-- author: Karsten Hilbert

-- This script provides tables used in collecting pending
-- housekeeping tasks. Demons, integrity checkers and auto-running
-- workers (say, import scripts) can use this to deliver messages
-- if they cannot count on a human user interacting with them.

-- ===================================================================
-- force terminate + exit(3) on errors if non-interactive
\set ON_ERROR_STOP 1

-- ===================================================================
create table housekeeping_todo (
	pk serial primary key,
	reported_when timestamp with time zone not null default CURRENT_TIMESTAMP,
	reported_by text not null,
	reported_to text
		not null
		default 'admin'
		check (reported_to in ('user', 'admin')),
	problem text not null,
	solution text,
	context text,
	category text not null
);

comment on table housekeeping_todo is
	'this table stores items that originate in headless processes
	 running in the background but need to be brought to the
	 attention of someone, say, errors that an integrity checker
	 may find';
comment on column housekeeping_todo.reported_by is
	'who or what reported this condition, may be a user or software';
comment on column housekeeping_todo.reported_to is
	'who is this condition reported to, user or admin,
	 used for filtering';
comment on column housekeeping_todo.problem is
	'a description of the reported condition';
comment on column housekeeping_todo.solution is
	'a proposed solution to the problem';
comment on column housekeeping_todo.context is
	'specific context for this condition that would
	 make the problem field unnecessary complex and bulky';
comment on column housekeeping_todo.category is
	'a category for the condition, this is used
	 for filtering, too';

-- =============================================
GRANT select, insert ON
	housekeeping_todo
	, housekeeping_todo_pk_seq
TO GROUP "gm-public";

-- should be "admin" ...
GRANT select, insert, update, delete on
	housekeeping_todo
	, housekeeping_todo_pk_seq
TO GROUP "_gm-doctors";

-- =============================================
-- do simple schema revision tracking
delete from gm_schema_revision where filename = '$RCSfile: gmHousekeeping.sql,v $';
INSERT INTO gm_schema_revision (filename, version) VALUES('$RCSfile: gmHousekeeping.sql,v $', '$Revision: 1.4 $');

-- =============================================
-- $Log: gmHousekeeping.sql,v $
-- Revision 1.4  2004-04-26 09:40:11  ncq
-- - add context/category to todo table
--
-- Revision 1.3  2004/04/19 12:47:49  ncq
-- - translate request_status
-- - add housekeeping_todo.reported_to
--
-- Revision 1.2  2004/03/18 09:50:19  ncq
-- - fixed GRANTs
--
-- Revision 1.1  2004/03/16 15:55:42  ncq
-- - use for housekeeping, etc.
--
