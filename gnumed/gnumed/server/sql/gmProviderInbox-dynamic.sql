-- =============================================
-- GNUmed - dynamic tables for the provider inbox
-- =============================================
-- $Source: /home/ncq/Projekte/cvs2git/vcs-mirror/gnumed/gnumed/server/sql/gmProviderInbox-dynamic.sql,v $
-- $Id: gmProviderInbox-dynamic.sql,v 1.4 2006-01-09 13:44:02 ncq Exp $
-- license: GPL
-- author: Karsten.Hilbert@gmx.net

-- =============================================
-- force terminate + exit(3) on errors if non-interactive
\set ON_ERROR_STOP 1

-- ---------------------------------------------
comment on table dem.inbox_item_category is
	'Holds the various categories of messages that
	 can show up in the provider inbox.';
comment on column dem.inbox_item_category.description is '
"clinical"\n
"admin"\n
"personal"\n
...';
comment on column dem.inbox_item_category.is_user is
	'whether this category was added locally,
	 as to be left alone by database upgrades';

-- ---------------------------------------------
comment on table dem.inbox_item_type is
	'Holds the various types of messages that can
	 show up in the provider inbox.';
comment on column dem.inbox_item_type.fk_inbox_item_category is
	'The category of this item type.';
comment on column dem.inbox_item_type.description is
	'the various types of inbox items';
comment on column dem.inbox_item_type.is_user is
	'whether this type was added locally,
	 as to be left alone by database upgrades';

-- ---------------------------------------------
comment on table dem.provider_inbox is
	'Holds per-provider messages.';
comment on column dem.provider_inbox.fk_staff is
	'the member of staff this message is addressed to';
comment on column dem.provider_inbox.fk_inbox_item_type is
	'the item (message) type';
comment on column dem.provider_inbox.comment is
	'a free-text comment, may be NULL';
comment on column dem.provider_inbox.ufk_context is
	'an optional, *u*nchecked *f*oreign *k*ey, it is up to
	 the application to know what to do with this, it will
	 have to make sense within the context of the combination
	 of staff ID, item type, and comment';
comment on column dem.provider_inbox.importance is
	'the relative importance of this message:\n
	 -1: lower than most things already in the inbox ("low")\n
	  0: same as most things ("standard")\n
	  1: higher than most things already there ("high")';

-- ---------------------------------------------
\unset ON_ERROR_STOP
drop view dem.v_inbox_item_type cascade;
\set ON_ERROR_STOP 1

create view dem.v_inbox_item_type as
select
	it.description as type,
	_(it.description) as l10n_type,
	ic.description as category,
	_(ic.description) as l10n_category,
	it.is_user as is_user_type,
	ic.is_user as is_user_category,
	it.pk as pk_type,
	it.fk_inbox_item_category as pk_category
from
	dem.inbox_item_type it,
	dem.inbox_item_category ic
where
	it.fk_inbox_item_category = ic.pk
;

-- ---------------------------------------------
\unset ON_ERROR_STOP
drop view dem.v_provider_inbox cascade;
\set ON_ERROR_STOP 1

create view dem.v_provider_inbox as
select
	(select sign from dem.staff where dem.staff.pk = pi.fk_staff) as provider,
	pi.importance,
	vit.category,
	vit.l10n_category,
	vit.type,
	vit.l10n_type,
	pi.comment,
	pi.ufk_context as pk_context,
	pi.pk as pk_provider_inbox,
	pi.fk_staff as pk_staff,
	vit.pk_category,
	pi.fk_inbox_item_type as pk_type
from
	dem.provider_inbox pi,
	dem.v_inbox_item_type vit
where
	pi.fk_inbox_item_type = vit.pk_type
;

-- =============================================
-- do simple schema revision tracking
select log_script_insertion('$RCSfile: gmProviderInbox-dynamic.sql,v $2', '$Revision: 1.4 $');

-- =============================================
-- $Log: gmProviderInbox-dynamic.sql,v $
-- Revision 1.4  2006-01-09 13:44:02  ncq
-- - add inbox item type category and adjust view
--
-- Revision 1.3  2006/01/08 17:40:04  ncq
-- - fixed syntax error with "where" where no where belonged
--
-- Revision 1.2  2006/01/07 17:53:32  ncq
-- - proper grants for provider inbox
-- - dynamic staff re provider inbox added
--
-- Revision 1.1  2006/01/07 15:22:23  ncq
-- - initial attempt at provider inbox tables
--
