-- ==============================================================
-- GNUmed database schema change script
--
-- License: GPL v2 or later
-- Author: karsten.hilbert@gmx.net
--
-- ==============================================================
\set ON_ERROR_STOP 1
--set default_transaction_read_only to off;

-- --------------------------------------------------------------
-- table
comment on table ref.substance is 'Holds consumable substances.';

select audit.register_table_for_auditing('ref', 'substance');
select gm.register_notifying_table('ref', 'substance');

-- grants
grant select on ref.substance to "gm-public";
grant insert, update, delete on ref.substance to "gm-doctors";
grant usage on ref.substance_pk_seq to "gm-public" ;

-- --------------------------------------------------------------
-- .description
comment on column ref.substance.description is 'the name of the substance';

alter table ref.substance drop constraint if exists ref_substance_sane_desc cascade;

alter table ref.substance
	add constraint ref_substance_sane_desc check (
		gm.is_null_or_non_empty_string(description) is True
	);

drop index if exists ref.idx_substance_desc cascade;
create unique index idx_substance_desc on ref.substance(description);

-- --------------------------------------------------------------
-- .atc
comment on column ref.substance.atc is 'the ATC of the substance';

-- needs FK trigger
-- not possible because ref.atc.atc is only unique on (code, system)
--alter table ref.substance drop constraint if exists ref_substance_fk_atc cascade;
--alter table ref.substance
--	add constraint ref_substance_fk_atc
--		foreign key (atc) references ref.atc(code)
--;

drop index if exists ref.idx_substance_atc cascade;
create index idx_substance_atc on ref.substance(atc);

-- --------------------------------------------------------------
-- .intake_instructions
comment on column ref.substance.intake_instructions is 'any intake instructions for the substance';

alter table ref.substance drop constraint if exists ref_substance_sane_instructions cascade;

alter table ref.substance
	add constraint ref_substance_sane_instructions check (
		gm.is_null_or_non_empty_string(intake_instructions) is True
	);

-- --------------------------------------------------------------
-- populate
insert into ref.substance (description, atc)
	select distinct on (r_cs.description)
		r_cs.description,
		r_cs.atc_code
	from
		ref.consumable_substance r_cs
	where
		not exists (
			select 1 from ref.substance r_s
			where
				r_s.description = r_cs.description
		)
;

-- --------------------------------------------------------------
drop view if exists ref.v_substances cascade;

create view ref.v_substances as
select
	r_s.pk
		as pk_substance,
	r_s.description
		as substance,
	r_s.intake_instructions,
	r_s.atc,
	ARRAY (
		select row_to_json(loinc_row) from (
			select r_ll2s.loinc, r_ll2s.comment, r_ll2s.max_age
			from ref.lnk_loinc2substance r_ll2s
			where r_ll2s.fk_substance = r_s.pk
		) as loinc_row
	)	as loincs,

	r_s.xmin as xmin_substance
from
	ref.substance r_s
;

grant select on ref.v_substances to "gm-public";

-- --------------------------------------------------------------
select gm.log_script_insertion('v22-ref-substance-dynamic.sql', '22.0');
