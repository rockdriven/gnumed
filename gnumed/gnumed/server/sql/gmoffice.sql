-- GnuMed office related/administrative tables

-- Copyright 2002 by Dr. Horst Herb
-- This is free software in the sense of the General Public License (GPL)
-- For details regarding GPL licensing see http://gnu.org

-- $Source: /home/ncq/Projekte/cvs2git/vcs-mirror/gnumed/gnumed/server/sql/gmoffice.sql,v $
-- $Revision: 1.5 $ $Date: 2004-03-10 15:45:15 $ $Author: ncq $
-- ===================================================================
-- force terminate + exit(3) on errors if non-interactive
\set ON_ERROR_STOP 1

-- ===================================================================
-- forms handling
-- ===================================================================
-- target classes
create table form_target_classes (
	pk serial primary key,
	name text unique not null
);

-- -------------------------------------------------------------------
-- queue of pending forms
create table form_queue (
	pk serial primary key,
	fk_form_instance integer
		not null
		references form_instances(pk),
	form bytea not null,
	fk_target_class integer
		not null
		references form_target_classes(pk),
	submitted_when timestamp with time zone
		not null
		default CURRENT_TIMESTAMP,
	fk_submitted_by integer not null,
	submitted_from text not null,
	status text not null default 'submitted'
);

-- FIXME: we need a trigger that allows UPDATEs only on "status"
-- FIXME: we also need a notify trigger on insert/update

select add_x_db_fk_def('form_queue', 'fk_submitted_by', 'personalia', 'staff', 'pk');

comment on table form_queue is
	'Queue table for rendered form instances. Note that
	 the rows in this table will get deleted after processing.
	 This is NOT an archive of form jobs.';
comment on column form_queue.fk_form_instance is
	'points to the unrendered source instance of the form,
	 useful for recalling submitted jobs for changing';
comment on column form_queue.form is
	'the rendered form, IOW binary data such as a PDF file';
comment on column form_queue.fk_target_class is
	'points to the target class';
comment on column form_queue.submitted_when is
	'when was this form job submitted';
comment on column form_queue.fk_submitted_by is
	'who of the staff submitted this form job';
comment on column form_queue.submitted_from is
	'the workplace this form job was submitted from';
comment on column form_queue.status is
	'status of the form job:
	 - submitted: ready for processing
	 - in progress: being processed
	 - removable: fit for removal (either cancelled, timed out or done)
	 - halted: do not process';

-- ===================================================================


-- ===================================================================
-- Embryo of billing tables
-- This is a highly classical accounting system, with medical-specific
-- updatable views.

create table schedule (
	id serial,
	code varchar (20),
	name varchar (100),
	min_duration integer,
	description text
);

create table billing_scheme (
	id serial,
	name varchar (100),
	iso_countrycode char (2)
);

create table prices (
	id_consult integer references schedule (id),
	id_scheme integer references billing_scheme (id),
	patient float,
	bulkbill float
);

comment on column prices.patient is
	'the amount of money paid by the patient';
comment on column prices.bulkbill is
	'the amount billed directly (bulk-billed) to the payor';

create table accounts (
	id serial,
	name varchar (50),
	extra integer
);

alter table accounts add column parent integer references accounts (id);

create table ledger (
	stamp timestamp,
	amount float,
	debit integer references accounts (id),
	credit integer references accounts (id)
);

create table consults
(
	start timestamp,
	finish timestamp,
	id_location integer,
	id_doctor integer,
	id_patient integer,
	id_type integer references schedule (id),
	id_scheme integer references billing_scheme (id)
);

-- ===================================================================
-- permissions
-- ===================================================================
GRANT SELECT ON
	form_target_classes
	, form_queue
TO GROUP "gm-public";

GRANT select, insert, delete, update ON
	form_queue
	, form_queue_pk_seq
TO GROUP "_gm-doctors";

-- ===================================================================
-- do simple schema revision tracking
delete from gm_schema_revision where filename='$RCSfile: gmoffice.sql,v $';
INSERT INTO gm_schema_revision (filename, version) VALUES('$RCSfile: gmoffice.sql,v $', '$Revision: 1.5 $');

--=====================================================================
-- $Log: gmoffice.sql,v $
-- Revision 1.5  2004-03-10 15:45:15  ncq
-- - grants on form tables
--
-- Revision 1.4  2004/03/10 00:08:31  ncq
-- - add form queue handling
-- - remove papersizes
-- - cleanup
--
-- Revision 1.3  2002/12/14 08:12:22  ihaywood
-- New prescription tables in gmclinical.sql
--
-- Revision 1.2  2002/12/06 08:50:52  ihaywood
-- SQL internationalisation, gmclinical.sql now internationalised.
--
-- Revision 1.1  2002/12/03 02:50:19  ihaywood
-- new office schema: tables for printing forms
