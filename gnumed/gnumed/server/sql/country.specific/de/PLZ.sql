-- GnuMed

-- author: Karsten Hilbert <Karsten.Hilbert@gmx.net>
-- license: GPL
-- $Source: /home/ncq/Projekte/cvs2git/vcs-mirror/gnumed/gnumed/server/sql/country.specific/de/PLZ.sql,v $
-- $Revision: 1.11 $

-- ===================================================================
-- force terminate + exit(3) on errors if non-interactive
\set ON_ERROR_STOP 1

set client_encoding to 'LATIN1';
-- ===================================================================
delete from urb where id_state = (select id from state where code='SN' and country='DE');
delete from state where country='DE';

-- Deutschland (Bundesl�nder)
insert into state (code, country, name) values ('BW', 'DE', 'Baden-W�rttemberg');
insert into state (code, country, name) values ('BY', 'DE', 'Bayern');
insert into state (code, country, name) values ('BE', 'DE', 'Berlin');
insert into state (code, country, name) values ('BB', 'DE', 'Brandenburg');
insert into state (code, country, name) values ('HB', 'DE', 'Bremen');
insert into state (code, country, name) values ('HH', 'DE', 'Hamburg');
insert into state (code, country, name) values ('HE', 'DE', 'Hessen');
insert into state (code, country, name) values ('MV', 'DE', 'Mecklenburg-Vorpommern');
insert into state (code, country, name) values ('NI', 'DE', 'Niedersachsen');
insert into state (code, country, name) values ('NW', 'DE', 'Nordrhein-Westfalen');
insert into state (code, country, name) values ('RP', 'DE', 'Rheinland-Pfalz');
insert into state (code, country, name) values ('SL', 'DE', 'Saarland');
insert into state (code, country, name) values ('SN', 'DE', 'Sachsen');
insert into state (code, country, name) values ('ST', 'DE', 'Sachsen-Anhalt');
insert into state (code, country, name) values ('SH', 'DE', 'Schleswig-Holstein');
insert into state (code, country, name) values ('TH', 'DE', 'Th�ringen');

-- �sterreich (Bundesl�nder)
insert into state (code, country, name) values ('Wien', 'AT', 'Wien');				-- Vienna
insert into state (code, country, name) values ('Tirol', 'AT', 'Tirol');			-- the Tyrol
insert into state (code, country, name) values ('O�', 'AT', 'Ober�sterreich');		-- Upper Austria
insert into state (code, country, name) values ('N�', 'AT', 'Nieder�sterreich');	-- Lower Austria
insert into state (code, country, name) values ('Stmk', 'AT', 'Steiermark');		-- Styria
insert into state (code, country, name) values ('Sbg', 'AT', 'Salzburg');
insert into state (code, country, name) values ('Vlbg', 'AT', 'Vorarlberg');
insert into state (code, country, name) values ('Bgld', 'AT', 'Burgenland');
insert into state (code, country, name) values ('Ktn', 'AT', 'K�rnten');			-- Carinthia

-- jo, wos is jetz d�s ?
--INSERT INTO state(code, country, name) VALUES ('BU','AT',i18n('Burgenland'));
--INSERT INTO state(code, country, name) VALUES ('CA','AT',i18n('Carinthia'));
--INSERT INTO state(code, country, name) VALUES ('NI','AT',i18n('Niederoesterreich'));
--INSERT INTO state(code, country, name) VALUES ('OB','AT',i18n('Oberoesterreich'));
--INSERT INTO state(code, country, name) VALUES ('SA','AT',i18n('Salzburg'));
--INSERT INTO state(code, country, name) VALUES ('ST','AT',i18n('Steiermark'));
--INSERT INTO state(code, country, name) VALUES ('TI','AT',i18n('Tirol'));
--INSERT INTO state(code, country, name) VALUES ('VO','AT',i18n('Vorarlberg'));
--INSERT INTO state(code, country, name) VALUES ('WI','AT',i18n('Wien'));

select gm_upd_default_states();

------------------
-- Gro� S�rchen --
------------------
insert into urb (id_state, name, postcode) values (
	(select id from state where code = 'SN' and country='DE'),
	'Gro� S�rchen',
	'02999'
);

-------------
-- Leipzig --
-------------
-- no street
insert into urb (id_state, postcode, name) values (
	(select id from state where code = 'SN' and country = 'DE'),
	'04318',
	'Leipzig'
);

insert into urb (id_state, postcode, name) values (
	(select id from state where code = 'SN' and country = 'DE'),
	'04317',
	'Leipzig'
);

-- streets
insert into street (
	id_urb,
	name,
	suburb,
	postcode
) values (
	(select id from urb where name='Leipzig' limit 1),
	'Zum Kleingartenpark',
	'Sellerhausen',
	'04318'
);

insert into street (id_urb, name, postcode) values (
	(select id from urb where name='Leipzig' limit 1),
	'Riebeckstra�e',
	'04317'
);

insert into street (id_urb, name, postcode) values (
	(select id from urb where name='Leipzig' limit 1),
	'Lange Reihe',
	'04299'
);

insert into street (id_urb, name, postcode) values (
	(select id from urb where name='Leipzig' limit 1),
	'Ferdinand-Jost-Stra�e',
	'04299'
);

insert into street (
	id_urb,
	name,
	suburb,
	postcode
) values (
	(select id from urb where name='Leipzig' limit 1),
	'Schildberger Weg',
	'Mockau',
	'04357'
);

insert into street (id_urb, name, postcode) values (
	(select id from urb where name='Leipzig' limit 1),
	'Wurzener Stra�e',
	'04315'
);

insert into street (
	id_urb,
	name,
	suburb,
	postcode
) values (
	(select id from urb where name='Leipzig' limit 1),
	'Wurzener Stra�e',
	'Sellerhausen',
	'04318'
);

insert into street (id_urb, name, postcode) values (
	(select id from urb where name='Leipzig' limit 1),
	'Eilenburger Stra�e',
	'04317'
);

insert into street (
	id_urb,
	name,
	suburb,
	postcode
) values (
	(select id from urb where name='Leipzig' limit 1),
	'Cunnersdorfer Stra�e',
	'Sellerhausen',
	'04318'
);

-- ===================================================================
-- do simple revision tracking
delete from gm_schema_revision where filename = '$RCSfile: PLZ.sql,v $';
INSERT INTO gm_schema_revision (filename, version) VALUES('$RCSfile: PLZ.sql,v $', '$Revision: 1.11 $');

-- =============================================
-- $Log: PLZ.sql,v $
-- Revision 1.11  2005-10-19 11:29:09  ncq
-- - when selecting state pks must give country, too, or else duplicates exist
--
-- Revision 1.10  2005/09/25 17:52:09  ncq
-- - add commented out alternative state information for AT
--
-- Revision 1.9  2005/09/19 16:26:07  ncq
-- - update default states
--
-- Revision 1.8  2005/07/14 21:31:43  ncq
-- - partially use improved schema revision tracking
--
-- Revision 1.7  2005/06/10 07:21:35  ncq
-- - better docs
--
-- Revision 1.6  2005/06/07 20:59:18  ncq
-- - Austrian states
--
-- Revision 1.5  2005/05/24 19:44:31  ncq
-- - use proper state abbreviations
--
-- Revision 1.4  2005/05/17 08:17:53  ncq
-- - Bundesl�nder
--
-- Revision 1.3  2004/09/20 21:17:39  ncq
-- - add a few suburbs
--
-- Revision 1.2  2004/04/07 18:16:06  ncq
-- - move grants into re-runnable scripts
-- - update *.conf accordingly
--
-- Revision 1.1  2003/12/29 15:15:01  uid66147
-- - a few German post codes
--
