-- ==============================================================
-- GNUmed database schema change script
--
-- License: GPL
-- Author: karsten.hilbert@gmx.net
-- 
-- ==============================================================
\set ON_ERROR_STOP 1

set check_function_bodies to on;

-- --------------------------------------------------------------
-- .narrative
comment on column clin.vaccination.narrative is
	'Used to record a comment on this vaccination.';

\unset ON_ERROR_STOP
alter table clin.vaccination drop constraint vaccination_sane_narrative cascade;
\set ON_ERROR_STOP 1

alter table clin.vaccination
	add constraint vaccination_sane_narrative check (
		gm.is_null_or_non_empty_string(narrative) is true
	);


-- .reaction
comment on column clin.vaccination.reaction is
	'Used to record reactions to this vaccination.';

\unset ON_ERROR_STOP
alter table clin.vaccination drop constraint vaccination_sane_reaction cascade;
\set ON_ERROR_STOP 1

alter table clin.vaccination
	add constraint vaccination_sane_reaction check (
		gm.is_null_or_non_empty_string(reaction) is true
	);


-- .site
comment on column clin.vaccination.site is
	'The site of injection used in this vaccination.';

\unset ON_ERROR_STOP
alter table clin.vaccination drop constraint vaccination_sane_site cascade;
\set ON_ERROR_STOP 1

alter table clin.vaccination
	add constraint vaccination_sane_site check (
		gm.is_null_or_non_empty_string(site) is true
	);

alter table clin.vaccination
	alter column site
		set default null;


-- .batch_no
comment on column clin.vaccination.batch_no is
	'The batch/lot number of the vaccine given.';

alter table clin.vaccination
	alter column batch_no
		drop default;



-- .fk_provider
comment on column clin.vaccination.fk_provider is
	'Who administered this vaccination.';

alter table clin.vaccination
	alter column fk_provider
		drop not null;

alter table clin.vaccination
	add foreign key (fk_provider)
		references dem.staff(pk)
		on update cascade
		on delete restrict;

-- --------------------------------------------------------------
-- this was shot down on the list because documenting clinical
-- reality (at least of previous previous, perhaps faulty,
-- vaccinations) is more important than making it impossible
-- to record reality at all

-- trigger to ensure that UNIQUE(clin_when, pk_patient, fk_vaccine) holds

--\unset ON_ERROR_STOP
--drop function clin.trf_sanity_check_no_duplicate_vaccinations() cascade;
--\set ON_ERROR_STOP 1

--create function clin.trf_sanity_check_no_duplicate_vaccinations()
--	returns trigger
--	language 'plpgsql'
--	as '
--DECLARE
--	_NEW_pk_patient integer;
--	_row record;
--	_indication_collision integer;
--BEGIN
--	select fk_patient into _NEW_pk_patient from clin.encounter where pk = NEW.fk_encounter;
--
--	-- loop over ...
--	for _row in
--		-- ... vaccinations ...
--		SELECT * FROM clin.vaccination
--		WHERE
--			-- ... of this patient ...
--			NEW.fk_encounter in (select pk from clin.encounter where fk_patient = _NEW_pk_patient)
--				and
--			-- ... within 2 days of the vaccination date
--			clin_when BETWEEN (NEW.clin_when - ''2 days''::interval) AND (NEW.clin_when + ''2 days''::interval)
--	loop
--
--		select (
--			select fk_indication from clin.lnk_vaccine2inds where fk_vaccine = NEW.fk_vaccine
--		) INTERSECT (
--			select fk_indication from clin.lnk_vaccine2inds where fk_vaccine = _row.fk_vaccine
--		) into _indication_collision;
--
--		if FOUND then
--			raise exception ''[clin.vaccination]: INSERT/UPDATE failed: vaccinations [%] and [%] share the indication [%] within 2 days of each other'', NEW.pk, _row.pk, _indication_collision;
--			return NEW;
--		end if;
--
--	end loop;
--
--	return NEW;
--END;';


--create trigger tr_sanity_check_no_duplicate_vaccinations
--	before insert or update on clin.vaccination
--		for each row execute procedure clin.trf_sanity_check_no_duplicate_vaccinations()
--;

-- --------------------------------------------------------------
\unset ON_ERROR_STOP
drop view clin.v_pat_vaccinations cascade;
\set ON_ERROR_STOP 1

create view clin.v_pat_vaccinations as

select
	cenc.fk_patient
		as pk_patient,
	clv.pk
		as pk_vaccination,
	clv.clin_when
		as date_given,
	rbd.description
		as vaccine,
	(select array_agg(description)
	 from
		clin.lnk_vaccine2inds clvi
			join clin.vacc_indication cvi on (clvi.fk_indication = cvi.id)
	 where
		clvi.fk_vaccine = clv.fk_vaccine
	) as indications,
	(select array_agg(_(description))
	 from
		clin.lnk_vaccine2inds clvi
			join clin.vacc_indication cvi on (clvi.fk_indication = cvi.id)
	 where
		clvi.fk_vaccine = clv.fk_vaccine
	) as l10n_indications,
	clv.site
		as site,
	clv.batch_no
		as batch_no,
	clv.reaction
		as reaction,
	clv.narrative
		as comment,
	clv.soap_cat
		as soap_cat,

	clv.modified_when
		as modified_when,
	clv.modified_by
		as modified_by,
	clv.row_version
		as row_version,

	(select array_agg(clvi.fk_indication)
	 from
		clin.lnk_vaccine2inds clvi
			join clin.vacc_indication cvi on (clvi.fk_indication = cvi.id)
	 where
		clvi.fk_vaccine = clv.pk
	) as pk_indications,
	clv.fk_vaccine
		as pk_vaccine,
	clv.fk_provider
		as pk_provider,
	clv.fk_encounter
		as pk_encounter,
	clv.fk_episode
		as pk_episode,

	clv.xmin
		as xmin_vaccination
from
	clin.vaccination clv
		join clin.encounter cenc on (cenc.pk = clv.fk_encounter)
			join clin.vaccine on (clin.vaccine.pk = clv.fk_vaccine)
				join ref.branded_drug rbd on (clin.vaccine.fk_brand = rbd.pk)

;

comment on view clin.v_pat_vaccinations is
	'Lists vaccinations for patients';

grant select on clin.v_pat_vaccinations to group "gm-doctors";

-- --------------------------------------------------------------
\unset ON_ERROR_STOP
drop view clin.v_pat_vaccs4indication cascade;
\set ON_ERROR_STOP 1

create view clin.v_pat_vaccs4indication as

select
	cenc.fk_patient
		as pk_patient,
	cv.pk
		as pk_vaccination,
	cv.clin_when
		as date_given,
	cvi4v.vaccine
		as vaccine,
	cvi4v.indication
		as indication,
	cvi4v.l10n_indication
		as l10n_indication,
	cv.site
		as site,
	cv.batch_no
		as batch_no,
	cv.reaction
		as reaction,
	cv.narrative
		as comment,
	cv.soap_cat
		as soap_cat,

	cv.modified_when
		as modified_when,
	cv.modified_by
		as modified_by,
	cv.row_version
		as row_version,

	cv.fk_vaccine
		as pk_vaccine,
	cvi4v.pk_indication
		as pk_indication,
	cv.fk_provider
		as pk_provider,
	cv.fk_encounter
		as pk_encounter,
	cv.fk_episode
		as pk_episode,

	cv.xmin
		as xmin_vaccination
from
	clin.vaccination cv
		join clin.encounter cenc on (cenc.pk = cv.fk_encounter)
			join clin.v_indications4vaccine cvi4v on (cvi4v.pk_vaccine = cv.fk_vaccine)

;

comment on view clin.v_pat_vaccs4indication is
	'Lists vaccinations per indication for patients';

grant select on clin.v_pat_vaccs4indication to group "gm-doctors";

-- --------------------------------------------------------------
\unset ON_ERROR_STOP
drop view clin.v_pat_last_vacc4indication cascade;
\set ON_ERROR_STOP 1

create view clin.v_pat_last_vacc4indication as

select
	cvpv4i1.*,
	cpi.indication_count
from
	clin.v_pat_vaccs4indication cvpv4i1
		join (
			SELECT
				COUNT(1) AS indication_count,
				pk_patient,
				pk_indication
			FROM clin.v_pat_vaccs4indication
			GROUP BY
				pk_patient,
				pk_indication
		) AS cpi ON (cvpv4i1.pk_patient = cpi.pk_patient AND cvpv4i1.pk_indication = cpi.pk_indication)
where
	cvpv4i1.date_given = (
		select
			max(cvpv4i2.date_given)
		from
			clin.v_pat_vaccs4indication cvpv4i2
		where
			cvpv4i1.pk_patient = cvpv4i2.pk_patient
				and
			cvpv4i1.pk_indication = cvpv4i2.pk_indication
	)
;

comment on view clin.v_pat_last_vacc4indication is
	'Lists *latest* vaccinations with total count per indication.';

grant select on clin.v_pat_last_vacc4indication to group "gm-doctors";

-- --------------------------------------------------------------
\unset ON_ERROR_STOP
drop view clin.v_pat_vaccinations_journal cascade;
\set ON_ERROR_STOP 1

create view clin.v_pat_vaccinations_journal as

select
	cenc.fk_patient
		as pk_patient,
	cv.modified_when
		as modified_when,
	cv.clin_when
		as clin_when,
	coalesce (
		(select short_alias from dem.staff where db_user = cv.modified_by),
		'<' || cv.modified_by || '>'
	)
		as modified_by,
	cv.soap_cat
		as soap_cat,

	(_('Vaccination') || ': '
		|| rbd.description || ' '
		|| '[' || cv.batch_no || ']'
		|| coalesce(' (' || cv.site || ')', '')
		|| coalesce(E'\n' || _('Reaction') || ': ' || cv.reaction, '')
		|| coalesce(E'\n' || _('Comment') || ': ' || cv.narrative, '')
		|| coalesce (
			(
				E'\n' || _('Indications') || ': '
				|| array_to_string ((
					select
						array_agg(_(description))
		 			from
						clin.lnk_vaccine2inds clvi
							join clin.vacc_indication cvi on (clvi.fk_indication = cvi.id)
					where
						clvi.fk_vaccine = cv.fk_vaccine
					),
					' / '
				)
			),
			''
		)
	)
		as narrative,

	cv.fk_encounter
		as pk_encounter,
	cv.fk_episode
		as pk_episode,
	(select fk_health_issue from clin.episode where pk = cv.fk_episode)
		as pk_health_issue,
	cv.pk
		as src_pk,
	'clin.vaccination'::text
		as src_table,
	cv.row_version
		as row_version
from
	clin.vaccination cv
		join clin.encounter cenc on (cenc.pk = cv.fk_encounter)
			join clin.vaccine on (clin.vaccine.pk = cv.fk_vaccine)
				join ref.branded_drug rbd on (clin.vaccine.fk_brand = rbd.pk)
;

select i18n.upd_tx('de_DE', 'Vaccination', 'Impfung');
select i18n.upd_tx('de_DE', 'Reaction', 'Reaktion');
select i18n.upd_tx('de_DE', 'Comment', 'Kommentar');
select i18n.upd_tx('de_DE', 'Indications', 'Indikationen');


comment on view clin.v_pat_vaccinations_journal is
	'Vaccination data denormalized for the EMR journal.';

grant select on clin.v_pat_vaccinations_journal to group "gm-doctors";


-- --------------------------------------------------------------
select gm.log_script_insertion('v14-clin-vaccination-dynamic.sql', 'Revision: 1.1');