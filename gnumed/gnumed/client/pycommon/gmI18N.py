#===========================================================================
# THIS NEEDS TO BE IMPORTED FIRST IN YOUR MODULES !
#===========================================================================

"""GNUmed client internationalization/localization.

All i18n/l10n issues should be handled through this modules.

Theory of operation:

By importing this module a textdomain providing translations is
automatically installed. The translating method gettext.gettext()
is installed into the global (!) namespace as _(). Your own modules thus
need not do _anything_ (not even import gmI18N) to have _() available
to them for translating strings. You need to make sure, however, that
gmI18N is imported in your main module before any of the modules using
it. In order to resolve circular references involving modules that
absolutely _have_ to be imported before this module you can explicitely
import gmI18N into them at the very beginning.

The text domain (i.e. the name of the message catalog file) is derived
from the name of the main executing script unless explicitely given on
the command line like this:
 --text-domain=<your text domain>

This module searches for message catalog files in 3 main locations:
 - in standard POSIX places (/usr/share/locale/ ...)
 - below $GNUMED_DIR/locale/
 - below (one level above binary directory)/locale/

For DOS/Windows I don't know of standard places so only the last
option will work unless you have CygWin installed. I don't know a
thing about classic Mac behaviour. New Macs are POSIX, of course.

The language you want to see is derived from  environment
variables by the locale system.

@copyright: authors
"""
#===========================================================================
# $Id: gmI18N.py,v 1.7 2005-04-24 15:48:47 ncq Exp $
# $Source: /home/ncq/Projekte/cvs2git/vcs-mirror/gnumed/gnumed/client/pycommon/gmI18N.py,v $
__version__ = "$Revision: 1.7 $"
__author__ = "H. Herb <hherb@gnumed.net>, I. Haywood <i.haywood@ugrad.unimelb.edu.au>, K. Hilbert <Karsten.Hilbert@gmx.net>"
__license__ = "GPL (details at http://www.gnu.org)"

import gettext, sys, os.path, string, os, re
import gmLog, gmCLI

_log = gmLog.gmDefLog
_log.Log(gmLog.lInfo, __version__)
if __name__ == "__main__":
	_log.SetAllLogLevels(gmLog.lData)

system_locale = ''
system_locale_level = {}

# Q: I can't use non-ascii characters in labels and menus.
# A: This can happen if your Python's sytem encoding is ascii and
#    wxPython is non-unicode. Edit/create the file sitecustomize.py
#    (should be somewhere in your PYTHONPATH), and put these magic lines:
#
#	import sys
#	sys.setdefaultencoding('iso8859-1') # replace with encoding you want to be the default one

# default is to not force unicode conversion for gettext
unicode_flag = 0
if gmCLI.has_arg('--unicode-gettext'):
	try:
		unicode_flag = int(gmCLI.arg['--unicode-gettext'])
		if unicode_flag not in [0, 1]:
			unicode_flag = 1
			raise Exception
	except:
		_log.Log(gmLog.lErr, 'cannot use [%s] as value for --unicode-gettext, must use 0 or 1' % gmCLI.arg['--unicode-gettext'])

#===========================================================================
def __split_locale_into_levels():
	"""Split locale into language, country and variant parts.

	- we have observed the following formats in the wild:
	  - de_DE@euro
	  - ec_CA.UTF-8
	  - en_US:en
	"""
	global system_locale_level
	system_locale_level['full'] = system_locale
	# trim '@<variant>' part
	system_locale_level['country'] = re.split('@|:|\.', system_locale, 1)[0]
	# trim '_<COUNTRY>@<variant>' part
	system_locale_level['language'] = system_locale.split('_', 1)[0]
#---------------------------------------------------------------------------
def __get_system_locale():
	"""Get system locale from environment."""
	global system_locale
	global system_locale_level

#	env_key = 'LANGUAGE'
#	if os.environ.has_key(env_key):
#		system_locale = os.environ[env_key]
#		_log.Log(gmLog.lData, '$(%s): "%s"' % (env_key, system_locale))
#	else:
#		_log.Log(gmLog.lData, '$(%s) not set' % (env_key))

#	env_key = 'LC_ALL'
#	if os.environ.has_key(env_key):
#		system_locale = os.environ[env_key]
#		_log.Log(gmLog.lData, '$(%s): "%s"' % (env_key, system_locale))
#	else:
#		_log.Log(gmLog.lData, '$(%s) not set' % (env_key))

#	env_key = 'LC_MESSAGES'
#	if os.environ.has_key(env_key):
#		system_locale = os.environ[env_key]
#		_log.Log(gmLog.lData, '$(%s): "%s"' % (env_key, system_locale))
#	else:
#		_log.Log(gmLog.lData, '$(%s) not set' % (env_key))

#	env_key = 'LANG'
#	if os.environ.has_key(env_key):
#		system_locale = os.environ[env_key]
#		_log.Log(gmLog.lData, '$(%s): "%s"' % (env_key, system_locale))
#	else:
#		_log.Log(gmLog.lData, '$(%s) not set' % (env_key))

	# use locale system
	import locale
	system_locale = locale.setlocale(locale.LC_CTYPE)

	# did we find any locale setting ? assume en_EN if not
	if system_locale in [None, 'C']:
		_log.Log(gmLog.lErr, 'the system locale is not set to anything or is [C], assuming [en_EN]')
		system_locale = "en_EN"

	# generate system locale levels
	__split_locale_into_levels()
#---------------------------------------------------------------------------
def __install_domain():
	"""Install a text domain suitable for the main script.
	"""
	text_domain = ""
	# text domain given on command line ?
	if gmCLI.has_arg('--text-domain'):
		text_domain = gmCLI.arg['--text-domain']
	# else get text domain from name of script 
	else:
		text_domain = os.path.splitext(os.path.basename(sys.argv[0]))[0]

	_log.Log(gmLog.lInfo, 'text domain is "%s"' % text_domain)

	# search for message catalog
	_log.Log(gmLog.lData, 'Searching message catalog file for system locale [%s].' % system_locale)

	# now we can install this text domain
	# 1) try standard places first
	if os.name == 'posix':
		_log.Log(gmLog.lData, 'looking in standard POSIX locations (see Python Manual)')
		try:
			gettext.install(text_domain, unicode=unicode_flag)
			_log.Log(gmLog.lData, 'found msg catalog')
			return 1
		except IOError:
			# most likely we didn't have a .mo file
			_log.LogException('Cannot install textdomain from standard POSIX locations.', sys.exc_info(), verbose=0)
	else:
		_log.Log(gmLog.lData, 'No use looking in standard POSIX locations - not a POSIX system.')

	# 2) $(<script-name>_DIR)/
	env_key = "%s_DIR" % string.upper(os.path.splitext(os.path.basename(sys.argv[0]))[0])
	_log.Log(gmLog.lData, 'looking at $(%s)' % env_key)
	if os.environ.has_key(env_key):
		loc_dir = os.path.abspath(os.path.join(os.environ[env_key], "locale"))
		_log.Log(gmLog.lData, '$(%s) = "%s" -> [%s]' % (env_key, os.environ[env_key], loc_dir))
		if os.path.exists(loc_dir):
			try:
				gettext.install(text_domain, loc_dir, unicode=unicode_flag)
				_log.Log(gmLog.lData, 'found msg catalog')
				return 1
			except IOError:
				# most likely we didn't have a .mo file
				_log.LogException('Cannot install textdomain from custom location [%s].' % (loc_dir), sys.exc_info())
		else:
			_log.Log(gmLog.lWarn, 'Custom location [%s] does not exist. Cannot install textdomain from there.' % (loc_dir))
	else:
		_log.Log(gmLog.lInfo, "$(%s) not set" % env_key)

	# 3) one level below path to binary
	#    last resort for inferior operating systems such as DOS/Windows
	#    strip one directory level
	#    this is a rather neat trick :-)
	loc_dir = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), '..', 'locale'))
	_log.Log(gmLog.lData, 'looking near binary install directory [%s]' % loc_dir)
	#    sanity check (paranoia rulez)
	if os.path.exists(loc_dir):
		try:
			gettext.install(text_domain, loc_dir, unicode=unicode_flag)
			_log.Log(gmLog.lData, 'found msg catalog')
			return 1
		except IOError:
			# most likely we didn't have a .mo file
			_log.LogException('Cannot install textdomain from one level above binary location [%s].' % (loc_dir), sys.exc_info(), 0)
	else:
		_log.Log(gmLog.lWarn, "The application level locale directory [%s] does not exist. Cannot install textdomain from there." % (loc_dir))

	# 4) in path to binary
	loc_dir = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), 'locale' ))
	_log.Log(gmLog.lData, 'looking in binary install directory [%s]' % loc_dir)
	#    sanity check (paranoia rulez)
	if os.path.exists(loc_dir):
		try:
			gettext.install(text_domain, loc_dir, unicode=unicode_flag)
			_log.Log(gmLog.lData, 'found msg catalog')
			return 1
		except IOError:
			# most likely we didn't have a .mo file
			_log.LogException('Cannot install textdomain from within path to binary [%s].' % (loc_dir), sys.exc_info(), 0)
	else:
		_log.Log(gmLog.lWarn, "The application level locale directory [%s] does not exist. Cannot install textdomain from there." % (loc_dir))

	# 5) install a dummy translation class
	_log.Log(gmLog.lWarn, "Giving up and falling back to NullTranslations() class in despair.")
	# this shouldn't fail
	dummy = gettext.NullTranslations()
	dummy.install()
	return 1
#===========================================================================
# Main
#---------------------------------------------------------------------------
__get_system_locale()
__install_domain()

# gmTimeFormat is used to define a standard way of
# displaying a date as a string,
# this is marked for translation by _(),
# this way this variable can be used as a crude
# means of date formatting localization
gmTimeformat = _("%Y-%m-%d  %H:%M:%S")
_log.Log(gmLog.lData, 'local time format set to "%s"' % gmTimeformat)

if __name__ == "__main__":
	print "======================================================================"
	print __doc__
	print "======================================================================"
	print "authors:", __author__
	print "license:", __license__, "; version:", __version__
	print "system locale: ", system_locale, "; levels:", system_locale_level

#=====================================================================
# $Log: gmI18N.py,v $
# Revision 1.7  2005-04-24 15:48:47  ncq
# - change unicode_flag default to 0
# - add comment on proper fix involving sitecustomize.py
#
# Revision 1.6  2005/03/30 22:08:57  ncq
# - properly handle 0/1 in --unicode-gettext
#
# Revision 1.5  2005/03/29 07:25:39  ncq
# - improve docs
# - add unicode CLI switch to toggle unicode gettext use
# - use std lib locale modules to get system locale
#
# Revision 1.4  2004/06/26 23:06:00  ncq
# - cleanup
# - I checked it, no matter where we import (function-/class-/method-
#   local or globally) it will always only be done once so we can
#   get rid of the semaphore
#
# Revision 1.3  2004/06/25 12:29:13  ncq
# - cleanup
#
# Revision 1.2  2004/06/25 07:11:15  ncq
# - make gmI18N self-aware (eg. remember installing _())
#   so we should be able to safely import gmI18N anywhere
#
# Revision 1.1  2004/02/25 09:30:13  ncq
# - moved here from python-common
#
# Revision 1.29  2003/11/17 10:56:36  sjtan
#
# synced and commiting.
#
# Revision 1.1  2003/10/23 06:02:39  sjtan
#
# manual edit areas modelled after r.terry's specs.
#
# Revision 1.28  2003/06/26 21:34:03  ncq
# - fatal->verbose
#
# Revision 1.27  2003/04/25 08:48:47  ncq
# - refactored, now also take into account different delimiters (see __split_locale*)
#
# Revision 1.26  2003/04/18 09:00:02  ncq
# - assume en_EN for locale if none found
#
# Revision 1.25  2003/03/24 16:52:27  ncq
# - calculate system locale levels at startup
#
# Revision 1.24  2003/02/05 21:27:05  ncq
# - more aptly names a variable
#
# Revision 1.23  2003/02/01 02:42:46  ncq
# - log -> _log to prevent namespace pollution on import
#
# Revision 1.22  2003/02/01 02:39:53  ncq
# - get and remember user's locale
#
# Revision 1.21  2002/12/09 23:39:50  ncq
# - only try standard message catalog locations on true POSIX systems
#   as windows will choke on it
#
# Revision 1.20  2002/11/18 09:41:25  ncq
# - removed magic #! interpreter incantation line to make Debian happy
#
# Revision 1.19  2002/11/17 20:09:10  ncq
# - always display __doc__ when called standalone
#
# Revision 1.18  2002/09/26 13:16:52  ncq
# - log version
#
# Revision 1.17  2002/09/23 02:23:16  ncq
# - comment on why it fails on some version of Windows
#
# Revision 1.16  2002/09/22 18:38:58  ncq
# - added big comment on gmTimeFormat
#
# Revision 1.15  2002/09/10 07:52:29  ncq
# - increased log level of gmTimeFormat
#
# Revision 1.14  2002/09/08 15:57:42  ncq
# - added log cvs keyword
#
