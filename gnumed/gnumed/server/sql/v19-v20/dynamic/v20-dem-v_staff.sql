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
drop view if exists dem.v_staff cascade;


create view dem.v_staff as
select
	vbp.pk_identity as pk_identity,
	s.pk as pk_staff,
	vbp.title as title,
	vbp.firstnames as firstnames,
	vbp.lastnames as lastnames,
	s.short_alias as short_alias,
	case
		when (select exists(select 1 from pg_group where
			groname = 'gm-doctors'
				and
			(select usesysid from pg_user where usename = s.db_user) = any(grolist)
		)) then 'full clinical access'
		when (select exists(select 1 from pg_group where
			groname = 'gm-nurses'
				and
			(select usesysid from pg_user where usename = s.db_user) = any(grolist)
		)) then 'limited clinical access'
		when (select exists(select 1 from pg_group where
			groname = 'gm-staff'
				and
			(select usesysid from pg_user where usename = s.db_user) = any(grolist)
		)) then 'non-clinical access'
		when (select exists(select 1 from pg_group where
			groname = 'gm-public'
				and
			(select usesysid from pg_user where usename = s.db_user) = any(grolist)
		)) then 'public access'
	end as role,
	vbp.dob as dob,
	vbp.gender as gender,
	s.db_user as db_user,
	s.comment as comment,
	s.is_active as is_active,
	(select (
		select exists (
			SELECT 1
			from pg_group
			where
				(SELECT usesysid from pg_user where usename = s.db_user) = any(grolist)
					and
				groname = current_database()
		)
	) AND (
		select exists (
			SELECT 1
			from pg_group
			where
				(SELECT usesysid from pg_user where usename = s.db_user) = any(grolist)
					and
				groname = 'gm-logins'
		)
	)) as can_login,
	s.xmin as xmin_staff
from
	dem.staff s
		join dem.v_basic_person vbp on s.fk_identity = vbp.pk_identity
;


comment on view dem.v_staff is 'Denormalized staff data.';


revoke all on dem.v_staff from public;
grant select on dem.v_staff to group "gm-public";

-- --------------------------------------------------------------
select gm.log_script_insertion('v20-dem-v_staff.sql', '20.0');
