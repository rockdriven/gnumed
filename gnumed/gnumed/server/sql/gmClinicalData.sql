-- Project: GnuMed
-- ===================================================================
-- $Source: /home/ncq/Projekte/cvs2git/vcs-mirror/gnumed/gnumed/server/sql/gmClinicalData.sql,v $
-- $Id: gmClinicalData.sql,v 1.2 2003-04-09 13:08:21 ncq Exp $
-- license: GPL
-- author: Ian Haywood, Horst Herb

-- ===================================================================
-- This database is internationalised!

-- do fixed string i18n()ing
\i gmI18N.sql

-- ===================================================================
-- force terminate + exit(3) on errors if non-interactive
\set ON_ERROR_STOP 1

-- ===================================================================
INSERT INTO enum_clin_encounters (description) values (i18n('surgery consultation'));
INSERT INTO enum_clin_encounters (description) values (i18n('phone consultation'));
INSERT INTO enum_clin_encounters (description) values (i18n('fax consultation'));
INSERT INTO enum_clin_encounters (description) values (i18n('home visit'));
INSERT INTO enum_clin_encounters (description) values (i18n('nursing home visit'));
INSERT INTO enum_clin_encounters (description) values (i18n('repeat script'));
INSERT INTO enum_clin_encounters (description) values (i18n('hospital visit'));
INSERT INTO enum_clin_encounters (description) values (i18n('video conference'));
INSERT INTO enum_clin_encounters (description) values (i18n('proxy encounter'));
INSERT INTO enum_clin_encounters (description) values (i18n('emergency encounter'));
INSERT INTO enum_clin_encounters (description) values (i18n('other encounter'));

-- ===================================================================
INSERT INTO enum_clin_history (description) values (i18n('past'));
INSERT INTO enum_clin_history (description) values (i18n('presenting complaint'));
INSERT INTO enum_clin_history (description) values (i18n('history of present illness'));
INSERT INTO enum_clin_history (description) values (i18n('social'));
INSERT INTO enum_clin_history (description) values (i18n('family'));
INSERT INTO enum_clin_history (description) values (i18n('immunisation'));
INSERT INTO enum_clin_history (description) values (i18n('requests'));
INSERT INTO enum_clin_history (description) values (i18n('allergy'));
INSERT INTO enum_clin_history (description) values (i18n('drug'));
INSERT INTO enum_clin_history (description) values (i18n('sexual'));
INSERT INTO enum_clin_history (description) values (i18n('psychiatric'));
INSERT INTO enum_clin_history (description) values (i18n('other'));

-- ===================================================================
insert into enum_info_sources (description) values (i18n('patient'));
insert into enum_info_sources (description) values (i18n('clinician'));
insert into enum_info_sources (description) values (i18n('relative'));
insert into enum_info_sources (description) values (i18n('carer'));
insert into enum_info_sources (description) values (i18n('notes'));
insert into enum_info_sources (description) values (i18n('correspondence'));

-- ===================================================================
INSERT INTO enum_coding_systems (description) values (i18n('general'));
INSERT INTO enum_coding_systems (description) values (i18n('clinical'));
INSERT INTO enum_coding_systems (description) values (i18n('diagnosis'));
INSERT INTO enum_coding_systems (description) values (i18n('therapy'));
INSERT INTO enum_coding_systems (description) values (i18n('pathology'));
INSERT INTO enum_coding_systems (description) values (i18n('bureaucratic'));
INSERT INTO enum_coding_systems (description) values (i18n('ean'));
INSERT INTO enum_coding_systems (description) values (i18n('other'));

-- ===================================================================
INSERT INTO enum_confidentiality_level (description) values (i18n('public'));
INSERT INTO enum_confidentiality_level (description) values (i18n('relatives'));
INSERT INTO enum_confidentiality_level (description) values (i18n('receptionist'));
INSERT INTO enum_confidentiality_level (description) values (i18n('clinical staff'));
INSERT INTO enum_confidentiality_level (description) values (i18n('doctors'));
INSERT INTO enum_confidentiality_level (description) values (i18n('doctors of practice only'));
INSERT INTO enum_confidentiality_level (description) values (i18n('treating doctor'));

-- ===================================================================
insert into drug_units(unit) values('ml');
insert into drug_units(unit) values('mg');
insert into drug_units(unit) values('mg/ml');
insert into drug_units(unit) values('mg/g');
insert into drug_units(unit) values('U');
insert into drug_units(unit) values('IU');
insert into drug_units(unit) values('each');
insert into drug_units(unit) values('mcg');
insert into drug_units(unit) values('mcg/ml');
insert into drug_units(unit) values('IU/ml');
insert into drug_units(unit) values('day');

-- ===================================================================
--I18N!
insert into drug_formulations(description) values ('tablet');
insert into drug_formulations(description) values ('capsule');
insert into drug_formulations(description) values ('syrup');
insert into drug_formulations(description) values ('suspension');
insert into drug_formulations(description) values ('powder');
insert into drug_formulations(description) values ('cream');
insert into drug_formulations(description) values ('ointment');
insert into drug_formulations(description) values ('lotion');
insert into drug_formulations(description) values ('suppository');
insert into drug_formulations(description) values ('solution');
insert into drug_formulations(description) values ('dermal patch');
insert into drug_formulations(description) values ('kit');

-- ===================================================================
--I18N!
insert into drug_routes(description, abbreviation) values('oral', 'o.');
insert into drug_routes(description, abbreviation) values('sublingual', 's.l.');
insert into drug_routes(description, abbreviation) values('nasal', 'nas.');
insert into drug_routes(description, abbreviation) values('topical', 'top.');
insert into drug_routes(description, abbreviation) values('rectal', 'rect.');
insert into drug_routes(description, abbreviation) values('intravenous', 'i.v.');
insert into drug_routes(description, abbreviation) values('intramuscular', 'i.m.');
insert into drug_routes(description, abbreviation) values('subcutaneous', 's.c.');
insert into drug_routes(description, abbreviation) values('intraarterial', 'art.');
insert into drug_routes(description, abbreviation) values('intrathecal', 'i.th.');

-- ===================================================================
insert into databases (name, published) values ('MIMS', '1/1/02');
insert into databases (name, published) values ('AMIS', '1/1/02');
insert into databases (name, published) values ('AMH', '1/1/02');

-- ===================================================================
insert into enum_immunities (name) values ('tetanus');

-- ===================================================================
-- do simple schema revision tracking
\i gmSchemaRevision.sql
INSERT INTO gm_schema_revision (filename, version) VALUES('$RCSfile: gmClinicalData.sql,v $', '$Revision: 1.2 $');

-- =============================================
-- $Log: gmClinicalData.sql,v $
-- Revision 1.2  2003-04-09 13:08:21  ncq
-- - _clinical_ -> _clin_
--
-- Revision 1.1  2003/02/14 10:54:19  ncq
-- - breaking out enumerated data
--
