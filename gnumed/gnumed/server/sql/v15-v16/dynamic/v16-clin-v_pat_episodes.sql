-- ==============================================================
-- GNUmed database schema change script
--
-- License: GPL v2 or later
-- Author: Karsten Hilbert
-- 
-- ==============================================================
\set ON_ERROR_STOP 1

-- --------------------------------------------------------------
\unset ON_ERROR_STOP
drop view clin.v_pat_episodes cascade;
\set ON_ERROR_STOP 1


create view clin.v_pat_episodes as
select
	cenc.fk_patient
		as pk_patient,
	cep.description
		as description,
	cep.summary
		as summary,
	cep.is_open
		as episode_open,
	null
		as health_issue,
	null
		as issue_active,
	null
		as issue_clinically_relevant,
	(select min(started) from clin.encounter cle where cle.pk = cep.fk_encounter limit 1)
		as started_first,
	(select max(started) from clin.encounter cle where cle.pk = cep.fk_encounter limit 1)
		as started_last,
	(select max(last_affirmed) from clin.encounter cle where cle.pk = cep.fk_encounter limit 1)
	 	as last_affirmed,
	cep.pk
		as pk_episode,
	cep.fk_encounter
		as pk_encounter,
	null
		as pk_health_issue,
	cep.modified_when
		as episode_modified_when,
	cep.modified_by
		as episode_modified_by,
	cep.diagnostic_certainty_classification
		as diagnostic_certainty_classification,
	null
		as diagnostic_certainty_classification_issue,
	coalesce (
		(select array_agg(c_lc2e.fk_generic_code) from clin.lnk_code2episode c_lc2e where c_lc2e.fk_item = cep.pk),
		ARRAY[]::integer[]
	)
		as pk_generic_codes,
	cep.xmin
		as xmin_episode
from
	clin.episode cep
		inner join clin.encounter cenc on cep.fk_encounter = cenc.pk
where
	cep.fk_health_issue is null

		UNION ALL

select
	cenc.fk_patient
		as pk_patient,
	cep.description
		as description,
	cep.summary
		as summary,
	cep.is_open
		as episode_open,
	chi.description
		as health_issue,
	chi.is_active
		as issue_active,
	chi.clinically_relevant
		as issue_clinically_relevant,
	(select min(started) from clin.encounter cle where cle.pk = cep.fk_encounter limit 1)
		as started_first,
	(select max(started) from clin.encounter cle where cle.pk = cep.fk_encounter limit 1)
		as started_last,
	(select max(last_affirmed) from clin.encounter cle where cle.pk = cep.fk_encounter limit 1)
		as last_affirmed,
	cep.pk
		as pk_episode,
	cep.fk_encounter
		as pk_encounter,
	cep.fk_health_issue
		as pk_health_issue,
	cep.modified_when
		as episode_modified_when,
	cep.modified_by
		as episode_modified_by,
	cep.diagnostic_certainty_classification
		as diagnostic_certainty_classification,
	chi.diagnostic_certainty_classification
		as diagnostic_certainty_classification_issue,
	coalesce (
		(select array_agg(c_lc2e.fk_generic_code) from clin.lnk_code2episode c_lc2e where c_lc2e.fk_item = cep.pk),
		ARRAY[]::integer[]
	)
		as pk_generic_codes,
	cep.xmin
		as xmin_episode
from
	clin.episode cep
		inner join clin.encounter cenc on cep.fk_encounter = cenc.pk
			-- this should exclude all (cep.fk_health_issue is Null):
			inner join clin.health_issue chi on cep.fk_health_issue = chi.pk
;


grant select on clin.v_pat_episodes TO GROUP "gm-doctors";
-- --------------------------------------------------------------
select gm.log_script_insertion('v16-clin-v_pat_episodes.sql', 'v16');

-- ==============================================================
