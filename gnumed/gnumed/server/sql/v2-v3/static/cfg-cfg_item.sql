-- ==============================================================
-- GNUmed database schema change script
--
-- Source database version: v2
-- Target database version: v3
--
-- What it does:
-- - upgrade cfg.cfg_item
--
-- License: GPL
-- Author: 
-- 
-- ==============================================================
-- $Id: cfg-cfg_item.sql,v 1.1 2006-09-26 14:47:53 ncq Exp $
-- $Revision: 1.1 $

-- --------------------------------------------------------------
\set ON_ERROR_STOP 1

-- --------------------------------------------------------------
begin;

-- --------------------------------------------------------------
alter table cfg.cfg_item
	alter column workplace
		drop not null;

alter table cfg.cfg_item
	alter column workplace
		set default null;


alter table cfg.cfg_item
	alter column cookie
		drop not null;

alter table cfg.cfg_item
	alter column cookie
		set default null;


alter table cfg.cfg_item
	drop constraint "$1";

alter table cfg.cfg_item
	add foreign key (fk_template)
		references cfg.cfg_template(pk)
		on update cascade
		on delete cascade;

-- --------------------------------------------------------------
select public.log_script_insertion('$RCSfile: cfg-cfg_item.sql,v $', '$Revision: 1.1 $');

-- --------------------------------------------------------------
commit;

-- ==============================================================
-- $Log: cfg-cfg_item.sql,v $
-- Revision 1.1  2006-09-26 14:47:53  ncq
-- - those live here now
--
-- Revision 1.2  2006/09/21 19:50:08  ncq
-- - adjust defaults, constraints and foreign keys
--
-- Revision 1.1  2006/09/19 18:27:47  ncq
-- - add cfg.set_option()
-- - drop NOT NULL on cfg.cfg_item.cookie
--
-- Revision 1.3  2006/09/18 17:32:53  ncq
-- - make more fool-proof
--
-- Revision 1.2  2006/09/16 21:47:37  ncq
-- - improvements
--
-- Revision 1.1  2006/09/16 14:02:36  ncq
-- - use this as a template for change scripts
--
--
