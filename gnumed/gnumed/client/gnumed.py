#!/usr/bin/env python3

__doc__ = MANPAGE = """.\\" ========================================================
.\\" SPDX-License-Identifier: GPL-2.0-or-later
.\\" ========================================================

.TH GNUmed 1 "%s" "Manual for GNUmed"

.SH NAME
.B GNUmed
- an electronic MEDICAL record software for GP offices

This is not fully featured yet. Use at your own risk.
You have been warned.

.SH SYNOPSIS
.B gnumed
.RB [--quiet|debug]
.RB [--slave]
.RB [--text-domain=TEXTDOMAIN]
.RB [--log-file=FILE]
.RB [--conf-file=FILE]
.RB [--profile=FILE]
.RB [--lang-gettext=LANGUAGE]
.RB [--tool=TOOL]
.RB [--override-schema-check]
.RB [--skip-update-check]
.RB [--local-import]
.RB [--help]
.RB [--version]
.RB [-V]
.RB [-h|?]


.SH DESCRIPTION
.B GNUmed
is a solution for keeping safe and medically sound electronic
records on a patient's health. It primarily focuses on GP
offices. It is released under the GPL.

GNUmed is written in Python with wxPython/wxWindows. Data is
stored in a PostgreSQL database. Multiple clients can work
with the same database at the same time.

.SH OPTIONS
.PP
.TP
.B \--quiet
Be extra quiet and show only _real_ errors in the log.
.TP
.B \--debug
Pre-set the [debug mode] checkbox in the login dialog
which controls increased verbosity in the log file.

Useful for, well, debugging :-)  Slower, too.
.TP
.B \--slave
Pre-set the [enable remote control] checkbox in the login
dialog to enable the XML-RPC remote control feature.
.TP
.B \--hipaa
Enable HIPAA features with user workflow impact.

Those features which do not affect the workflow of the user
are permanently enabled.
.TP
.B \--log-file=FILE
Use this to change the name of the log file. At startup
GNUmed will tell you the name of the log file in use.
.TP
.B \--conf-file=FILE
Use configuration file FILE instead of searching for it in standard locations.
.TP
.B \--profile=FILE
Activate profiling and write profile data to file FILE.
.TP
.B \--lang-gettext=LANGUAGE
Explicitly set the language to use in gettext translation. The very
same effect can be achieved by setting the environment variable $LANG
from a launcher script.
.TP
.B \--text-domain=TEXTDOMAIN
Set this to change the name of the language file to be loaded.
Note, this does not change the directory the file is searched in,
only the name of the file where messages are loaded from. The
standard textdomain is, of course, "gnumed.mo". You need only
specify the base name of the file without the .mo extension.
.TP
.B \--tool=TOOL
Run the named TOOL instead of a GUI.

Currently implemented tools:

	check_enc_epi_xref: Cross-check that foreign keys values in any given row of any table carrying both of fk_episode and fk_encounter do point to episodes and encounters, respectively, of the very same patient.

	export_pat_emr_structure: Export the EMR structure (issues and episodes) of a patient into a text file.

	check_mimetypes_in_archive: Show mimetypes and related information of all document parts in the archive.

	read_all_rows_of_table: Check readability of all rows of a given table.
.TP
.B \--override-schema-check
Continue loading the client even if the database schema
version and the client software version cannot be verified
to be compatible.
.TP
.B \--skip-update-check
Skip checking for client updates. This is useful during
development or when the update check URL is unavailable.
.TP
.B \--local-import
At startup adjust the PYTHONPATH such that the GNUmed client is
run from a local copy of the source tree (say an unpacked tarball
or a GIT repo) rather than from a proper system-wide installation.
.TP
.B \--version, -V
Show version information about the GNUmed client and the
database it needs.
.TP
.B \--help, -h, or -?
Show this help.


.SH CONFIGURATION
.PP
.TP
.B Client startup and shutdown (OS level)

A shell script /usr/bin/gnumed is used to startup the client.
It checks whether the systemwide configuration file

	/etc/gnumed/gnumed-client.conf

exists. It then executes the following scripts (in that
order) if found:

	/etc/gnumed/gnumed-startup-local.sh

	~/.gnumed/scripts/gnumed-startup-local.sh

When the client terminates it will execute the following
scripts in order if they exist:

	/etc/gnumed/gnumed-shutdown-local.sh

	~/.gnumed/scripts/gnumed-shutdown-local.sh

.PP
.TP
.B wxPython client startup

The gnumed.py script checks for INI style configuration files
and fails if it does not find any. The files are searched for
in the following order and extend/overwrite each others
options:

	in the current working directory (cwd)

		./gumed.conf

	in the systemwide configuration directory

		/etc/gnumed/gnumed-client.conf

	in the home directory

		~/.gnumed/gnumed.conf

	in a local git tree or unpacked tarball

		.../gnumed/client/gnumed.conf

	explicitly given by CLI option

		--conf-file=<CONF FILE>

.PP
.TP
.B client/system interfacing

.B ~/.gnumed/gnumed-xsanerc.conf

(requires XSane > v0.992)

When GNUmed invokes XSane for scanning it passes along this file (via =--xsane-rc=). This way a custom XSane configuration can be used with GNUmed. If the file doesn't exist it will be created from ~/.sane/xsane/xsanerc on the first call to XSane.

When you configure XSane after calling it from GNUmed your changes will be stored in the GNUmed-specific XSane configuration file and will not affect your usual XSane settings.

.B mime_type2file_extension.conf

(searched for in ~/.gnumed/ and /etc/gnumed/, in that order)

GNUmed will use these files to map mime types to file extensions if need be.

The file must contain a group [extensions] under which there can be one option per mime type specifying the extension to use on files of said type. Set the value to the raw extension only, omitting the ".", like so:

.nf
[extensions]
image/x-bmp = bmp


.SH EXIT STATUS
.TP
 > 0: some error occurred while the GUI client was run
.TP
   0: normal termination of the client
.TP
 < 0: some error occurred while trying to run a console tool
.TP
  -1: an unknown console tool was requested
.TP
< -1: an error occurred while a console tool was run
.TP
-999: hard abort of the client


.SH ENVIRONMENT
.TP
.B LANG, LC_MESSAGES, etc.
See gettext(1) for how the various locale related environment variables work.


.SH OTHER FILES AND DIRECTORIES
.PP
.TP
.B ~/.gnumed/gnumed.log
The default log file.
.TP
.B gnumed-client.tmpfiles.d.conf
Integration with systemd-tmpfiles(8).
.TP
.B gnumed-completion.bash
Integration with BASH completions.


.SH SEE ALSO
.PP
.TP
.B https://www.gnumed.[de|org]
Online documenation.
.TP
.B http://savannah.gnu.org/projects/gnumed
Mailing list home
.TP
.B https://github.org/ncqgm/gnumed
Source code repository (Git)
.TP
.B /usr/share/doc/gnumed/
Local documentation
.TP
.B man -k gm-*
List man pages on gm-* commands.
.TP
.B gettext(1)


.SH BUGS

A lot of functionality is still missing. To make up for
that, there's bugs here and there for you to report :-)

Use at your own risk. You have been warned. Take proper backups !
"""

#==========================================================
# SPDX-License-Identifier: GPL-2.0-or-later
__author__ = "H. Herb <hherb@gnumed.net>, K. Hilbert <Karsten.Hilbert@gmx.net>, I. Haywood <i.haywood@ugrad.unimelb.edu.au>"
__license__ = "GPL v2 or later (details at http://www.gnu.org)"


# standard library
import sys
import os
import platform
import tempfile
import faulthandler
import random
import logging
import datetime
import signal
import os.path
import shutil
import stat
import re as regex


# do not run as module
if __name__ != "__main__":
	print("GNUmed startup: This is not intended to be imported as a module !")
	print("-----------------------------------------------------------------")
	sys.exit(1)


# do not run as root
if os.name in ['posix'] and os.geteuid() == 0:
	print("""
GNUmed startup: GNUmed should not be run as root.
-------------------------------------------------

Running GNUmed as <root> can potentially put all
your medical data at risk. It is strongly advised
against. Please run GNUmed as a non-root user.
""")
	sys.exit(1)

#----------------------------------------------------------
#current_client_version = '1.8.0rc3'
#current_client_branch = '1.8'
current_client_version = 'head'
current_client_branch = 'master'


_log = None
_pre_log_buffer = []
_cfg = None
_old_sig_term = None
_known_short_options = 'h?V'
_known_long_options = [
	'debug',
	'slave',
	'skip-update-check',
	'profile=',
	'text-domain=',
	'log-file=',
	'conf-file=',
	'lang-gettext=',
	'override-schema-check',
	'local-import',
	'help',
	'version',
	'hipaa',
	'wxp=',
	'tool=',
	'tui'
]

_known_tools = [
	'check_enc_epi_xref',
	'export_pat_emr_structure',
	'check_mimetypes_in_archive',
	'read_all_rows_of_table',
	'generate_man_page'
]


import_error_sermon = """
GNUmed startup: Cannot load GNUmed Python modules !
---------------------------------------------------
CRITICAL ERROR: Program halted.

Please make sure you have:

 1) the required third-party Python modules installed
 2) the GNUmed Python modules linked or installed into site-packages/
    (if you do not run from a CVS tree the installer should have taken care of that)
 3) your PYTHONPATH environment variable set up correctly

<sys.path> is currently set to:

 %s

If you are running from a copy of the CVS tree make sure you
did run gnumed/check-prerequisites.sh with good results.

If you still encounter errors after checking the above
requirements please ask on the mailing list.
"""


missing_cli_config_file = """
GNUmed startup: Missing configuration file.
-------------------------------------------

You explicitly specified a configuration file
on the command line:

	--conf-file=%s

The file does not exist, however.
"""


no_config_files = """
GNUmed startup: Missing configuration files.
--------------------------------------------

None of the below candidate configuration
files could be found:

 %s

Cannot run GNUmed without any of them.
"""

#==========================================================
# convenience functions
#----------------------------------------------------------
def _symlink_windows(source, link_name):
	import ctypes
	csl = ctypes.windll.kernel32.CreateSymbolicLinkW
	csl.argtypes = (ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint32)
	csl.restype = ctypes.c_ubyte
	if os.path.isdir(source):
		flags = 1
	else:
		flags = 0
	ret_code = csl(link_name, source.replace('/', '\\'), flags)
	if ret_code == 0:
		raise ctypes.WinError()
	return ret_code

#==========================================================
# startup helpers
#----------------------------------------------------------
def setup_fault_handler(target=None):
	if target is None:
		faulthandler.enable()
		_pre_log_buffer.append('<faulthandler> enabled, target = [console]: %s' % faulthandler)
		return
	_pre_log_buffer.append('<faulthandler> enabled, target = [%s]: %s' % (target, faulthandler))
	faulthandler.enable(file = target)

#==========================================================
def setup_console_encoding():
	print_lines = []
	try:
		sys.stdout.reconfigure(errors = 'surrogateescape')
		sys.stderr.reconfigure(errors = 'surrogateescape')
		_pre_log_buffer.append('stdout/stderr reconfigured to use <surrogateescape> for encoding errors')
		return
	except AttributeError:
		line = 'cannot reconfigure sys.stdout/stderr to use <errors="surrogateescape"> (needs Python 3.7+)'
		_pre_log_buffer.append(line)
		print_lines.append(line)
	try:
		_pre_log_buffer.append('sys.stdout/stderr default to "${PYTHONIOENCODING}=%s"' % os.environ['PYTHONIOENCODING'])
		return
	except KeyError:
		lines = [
			'${PYTHONIOENCODING} is not set up, use <PYTHONIOENCODING=utf-8:surrogateescape> in the shell (for Python < 3.7)',
			'console encoding errors may occur'
		]
		for line in lines:
			print_lines.append(line)
			_pre_log_buffer.append(line)
		for line in print_lines:
			print('GNUmed startup:', line)

#==========================================================
def setup_python_path():

	if not '--local-import' in sys.argv:
		_pre_log_buffer.append('running against systemwide install')
		return

	local_python_import_dir = os.path.dirname (
		os.path.abspath(os.path.join(sys.argv[0], '..'))
	)
	print("Running from local source tree (%s) ..." % local_python_import_dir)
	_pre_log_buffer.append("running from local source tree: %s" % local_python_import_dir)

	# does the path exist at all, physically ?
	# (*broken* links are reported as False)
	link_name = os.path.join(local_python_import_dir, 'Gnumed')
	if os.path.exists(link_name):
		_pre_log_buffer.append('local module import dir symlink exists: %s' % link_name)
	else:
		real_dir = os.path.join(local_python_import_dir, 'client')
		print('Creating local module import symlink ...')
		print(' real dir:', real_dir)
		print('     link:', link_name)
		try:
			os.symlink(real_dir, link_name)
		except AttributeError:
			_pre_log_buffer.append('Windows does not have os.symlink(), resorting to ctypes')
			result = _symlink_windows(real_dir, link_name)
			_pre_log_buffer.append('ctypes.windll.kernel32.CreateSymbolicLinkW() exit code: %s', result)
		_pre_log_buffer.append('created local module import dir symlink: link [%s] => dir [%s]' % (link_name, real_dir))

	sys.path.insert(0, local_python_import_dir)
	_pre_log_buffer.append('sys.path with local module import base dir prepended: %s' % sys.path)

#==========================================================
def setup_local_repo_path():

	local_repo_path = os.path.expanduser(os.path.join (
		'~',
		'.gnumed',
		'local_code',
		str(current_client_branch)
	))
	local_wxGladeWidgets_path = os.path.join(local_repo_path, 'Gnumed', 'wxGladeWidgets')

	if not os.path.exists(local_wxGladeWidgets_path):
		_log.debug('[%s] not found', local_wxGladeWidgets_path)
		_log.info('local wxGlade widgets repository not available')
		return

	_log.info('local wxGlade widgets repository found:')
	_log.info(local_wxGladeWidgets_path)

	if not os.access(local_wxGladeWidgets_path, os.R_OK):
		_log.error('invalid repo: no read access')
		return

	all_entries = os.listdir(os.path.join(local_repo_path, 'Gnumed'))
	_log.debug('repo base contains: %s', all_entries)
	all_entries.remove('wxGladeWidgets')
	try:
		all_entries.remove('__init__.py')
	except ValueError:
		_log.error('invalid repo: lacking __init__.py')
		return
	try:
		all_entries.remove('__init__.pyc')
	except ValueError:
		pass

	if len(all_entries) > 0:
		_log.error('insecure repo: additional files or directories found')
		return

	# repo must be 0700 (rwx------)
	stat_val = os.stat(local_wxGladeWidgets_path)
	_log.debug('repo stat(): %s', stat_val)
	perms = stat.S_IMODE(stat_val.st_mode)
	_log.debug('repo permissions: %s (octal: %s)', perms, oct(perms))
	if perms != 448:				# octal 0700
		if os.name in ['nt']:
			_log.warning('this platform does not support os.stat() permission checking')
		else:
			_log.error('insecure repo: permissions not 0600')
			return

	print("Activating local wxGlade widgets repository (%s) ..." % local_wxGladeWidgets_path)
	sys.path.insert(0, local_repo_path)
	_log.debug('sys.path with repo:')
	_log.debug(sys.path)

#==========================================================
def setup_logging():
	try:
		from Gnumed.pycommon import gmLog2 as _gmLog2
	except ImportError:
		print(import_error_sermon % '\n '.join(sys.path))
		sys.exit(1)

	print("Log file:", _gmLog2._logfile.name)
	setup_fault_handler(target = _gmLog2._logfile)

	global gmLog2
	gmLog2 = _gmLog2

	global _log
	_log = logging.getLogger('gm.launcher')

#==========================================================
def log_startup_info():
	global _pre_log_buffer
	if len(_pre_log_buffer) > 0:
		_log.info('early startup log buffer:')
	for line in _pre_log_buffer:
		_log.info(' ' + line)
	del _pre_log_buffer
	_log.info('GNUmed client version [%s] on branch [%s]', current_client_version, current_client_branch)
	_log.info('Platform: %s', platform.uname())
	_log.info(('Python %s on %s (%s)' % (sys.version, sys.platform, os.name)).replace('\n', '<\\n>'))
	try:
		import lsb_release
		_log.info('lsb_release: %s', lsb_release.get_distro_information())
	except ImportError:
		pass
	_log.info('module <sys> info:')
	attrs2skip = ['__doc__', 'copyright', '__name__', '__spec__']
	for attr_name in dir(sys):
		if attr_name in attrs2skip:
			continue
		if attr_name.startswith('set'):
			continue
		attr = getattr(sys, attr_name)
		if not attr_name.startswith('get'):
			_log.info('%s: %s', attr_name.rjust(30), attr)
			continue
		if callable(attr):
			try:
				_log.info('%s: %s', attr_name.rjust(30), attr())
			except Exception:
				_log.exception('%s: <cannot log>', attr_name.rjust(30))
			continue
	_log.info('module <platform> info:')
	attrs2skip = ['__doc__', '__copyright__', '__name__', '__spec__', '__cached__', '__builtins__']
	for attr_name in dir(platform):
		if attr_name in attrs2skip:
			continue
		if attr_name.startswith('set'):
			continue
		attr = getattr(platform, attr_name)
		if callable(attr):
			if attr_name.startswith('_'):
				_log.info('%s: %s', attr_name.rjust(30), attr)
				continue
			try:
				_log.info('%s: %s', attr_name.rjust(30), attr())
			except Exception:
				_log.exception('%s: <cannot log>', attr_name.rjust(30))
			continue
		_log.info('%s: %s', attr_name.rjust(30), attr)
		continue
	_log.info('module <os> info:')
	for n in os.confstr_names:
		_log.info('%s: %s', ('confstr[%s]' % n).rjust(40), os.confstr(n))
	for n in os.sysconf_names:
		try:
			_log.info('%s: %s', ('sysconf[%s]' % n).rjust(40), os.sysconf(n))
		except Exception:
			_log.exception('%s: <invalid> ??', ('sysconf[%s]' % n).rjust(30))
	os_attrs = ['name', 'ctermid', 'getcwd', 'get_exec_path', 'getegid', 'geteuid', 'getgid', 'getgroups', 'getlogin', 'getpgrp', 'getpid', 'getppid', 'getresuid', 'getresgid', 'getuid', 'supports_bytes_environ', 'uname', 'get_terminal_size', 'pathconf_names', 'times', 'cpu_count', 'curdir', 'pardir', 'sep', 'altsep', 'extsep', 'pathsep', 'defpath', 'linesep', 'devnull']
	for attr_name in os_attrs:
		attr = getattr(os, attr_name)
		if callable(attr):
			_log.info('%s: %s', attr_name.rjust(40), attr())
			continue
		_log.info('%s: %s', attr_name.rjust(40), attr)
	_log.info('process environment:')
	for key, val in os.environ.items():
		_log.info(' %s: %s' % (('${%s}' % key).rjust(40),	val))
	import sysconfig
	_log.info('module <sysconfig> info:')
	_log.info(' platform [%s] -- python version [%s]', sysconfig.get_platform(), sysconfig.get_python_version())
	_log.info(' sysconfig.get_paths():')
	paths = sysconfig.get_paths()
	for path in paths:
		_log.info('%s: %s', path.rjust(40), paths[path])
	_log.info(' sysconfig.get_config_vars():')
	conf_vars = sysconfig.get_config_vars()
	for var in conf_vars:
		_log.info('%s: %s', var.rjust(45), conf_vars[var])

#==========================================================
def setup_console_exception_handler():
	from Gnumed.pycommon.gmTools import handle_uncaught_exception_console

	sys.excepthook = handle_uncaught_exception_console

#==========================================================
def setup_cli():
	from Gnumed.pycommon import gmCfg2

	global _cfg
	_cfg = gmCfg2.gmCfgData()
	_cfg.add_cli (
		short_options = _known_short_options,
		long_options = _known_long_options
	)

	val = _cfg.get(option = '--debug', source_order = [('cli', 'return')])
	if val is None:
		val = False
	_cfg.set_option (
		option = 'debug',
		value = val
	)

	val = _cfg.get(option = '--slave', source_order = [('cli', 'return')])
	if val is None:
		val = False
	_cfg.set_option (
		option = 'slave',
		value = val
	)

	val = _cfg.get(option = '--skip-update-check', source_order = [('cli', 'return')])
	if val is None:
		val = False
	_cfg.set_option (
		option = 'skip-update-check',
		value = val
	)

	val = _cfg.get(option = '--hipaa', source_order = [('cli', 'return')])
	if val is None:
		val = False
	_cfg.set_option (
		option = 'hipaa',
		value = val
	)

	val = _cfg.get(option = '--local-import', source_order = [('cli', 'return')])
	if val is None:
		val = False
	_cfg.set_option (
		option = 'local-import',
		value = val
	)

	_cfg.set_option (
		option = 'client_version',
		value = current_client_version
	)

	_cfg.set_option (
		option = 'client_branch',
		value = current_client_branch
	)

#==========================================================
def handle_sig_term(signum, frame):
	_log.critical('SIGTERM (SIG%s) received, shutting down ...' % signum)
	gmLog2.flush()
	print('GNUmed: SIGTERM (SIG%s) received, shutting down ...' % signum)
	if frame is not None:
		print('%s::%s@%s' % (frame.f_code.co_filename, frame.f_code.co_name, frame.f_lineno))

	# FIXME: need to do something useful here

	if _old_sig_term in [None, signal.SIG_IGN]:
		sys.exit(1)
	else:
		_old_sig_term(signum, frame)

#----------------------------------------------------------
def setup_signal_handlers():
	global _old_sig_term
	old_sig_term = signal.signal(signal.SIGTERM, handle_sig_term)

#==========================================================
def setup_locale():
	gmI18N.activate_locale()

	td = _cfg.get(option = '--text-domain', source_order = [('cli', 'return')])
	l =  _cfg.get(option = '--lang-gettext', source_order = [('cli', 'return')])
	gmI18N.install_domain(domain = td, language = l, prefer_local_catalog = _cfg.get(option = 'local-import'))

#	# make sure we re-get the default encoding
#	# in case it changed
#	gmLog2.set_string_encoding()

#==========================================================
def handle_help_request():
	src = [('cli', 'return')]

	help_requested = (
		_cfg.get(option = '--help', source_order = src) or
		_cfg.get(option = '-h', source_order = src) or
		_cfg.get(option = '-?', source_order = src)
	)

	if help_requested:
		input('\nHit <ENTER> to display commandline help\n')
		if platform.system() == 'Windows':
			for line in MANPAGE.split('\n'):
				print(regex.sub('^\.\w+\s*', '', line, count = 1))
			sys.exit(0)

		handle, man_page_fname = tempfile.mkstemp(text = True, suffix = '.1')
		man_page_file = open(man_page_fname, mode = 'wt', encoding = 'utf8')
		man_page_file.write(MANPAGE % datetime.date.today().strftime('%x'))
		man_page_file.close()
		os.system('man %s' % man_page_fname)
		sys.exit(0)

#==========================================================
def handle_version_request():
	gmTools._client_version = current_client_version

	src = [('cli', 'return')]

	version_requested = (
		_cfg.get(option = '--version', source_order = src) or
		_cfg.get(option = '-V', source_order = src)
	)

	if version_requested:

		from Gnumed.pycommon.gmPG2 import map_client_branch2required_db_version, known_schema_hashes

		print('GNUmed version information')
		print('--------------------------')
		print('client     : %s on branch [%s]' % (current_client_version, current_client_branch))
		print('database   : %s' % map_client_branch2required_db_version[current_client_branch])
		print('schema hash: %s' % known_schema_hashes[map_client_branch2required_db_version[current_client_branch]])
		sys.exit(0)

#==========================================================
def setup_paths_and_files():
	"""Create needed paths in user home directory."""

	gmd_dir = os.path.expanduser(os.path.join('~', 'gnumed'))
	dot_gmd_dir = os.path.expanduser(os.path.join('~', '.gnumed'))
	readme = """GNUmed Electronic Medical Record

	%s/

This directory should only ever contain files which the
user will come into direct contact with while using the
application (say, by selecting a file from the file system,
as when selecting document parts from files). You can create
subdirectories here as you see fit for the purpose.

This directory will also serve as the default directory when
GNUmed asks the user to select a directory for storing a
file.

Any files which are NOT intended for direct user interaction
but must be configured to live at a known location (say,
inter-application data exchange files) should be put under
the hidden directory:
	"%s/"
""" % (gmd_dir, dot_gmd_dir)
	gmTools.mkdir(gmd_dir)
	gmTools.create_directory_description_file(directory = gmd_dir, readme = readme)
	# remove old README
	gmTools.remove_file(os.path.join(gmd_dir, '00_README'))

	gmTools.mkdir(os.path.expanduser(os.path.join(dot_gmd_dir, 'spellcheck')))
	err_dir = os.path.expanduser(os.path.join(dot_gmd_dir, 'error_logs'))
	gmTools.mkdir(err_dir)
	readme = """This directory should be used for files not intended for user
interaction at the file system level (file selection dialogs,
file browsers) such as inter-application data exchange files
which need to live at a known location."""
	gmTools.create_directory_description_file(directory = dot_gmd_dir, readme = readme)
	gmTools.create_directory_description_file (
		directory = err_dir,
		readme = 'Whenever an unhandled exception is detected a copy of the log file is placed here.\n\nThis directory is subject to systemd-tmpfiles cleaning.'
	)

	# wxPython not available yet
	paths = gmTools.gmPaths(app_name = 'gnumed')
	print("Temp dir:", paths.tmp_dir)
	# ensure there's a user-level config file
	open(os.path.expanduser(os.path.join('~', '.gnumed', 'gnumed.conf')), mode = 'a+t').close()
	# symlink log file into temporary directory for easier debugging (everything in one place)
	logfile_link = os.path.join(paths.tmp_dir, 'zzz-gnumed.log')
	gmTools.mklink (gmLog2._logfile.name, logfile_link, overwrite = False)

#==========================================================
def setup_date_time():
	gmDateTime.init()

#==========================================================
def setup_cfg():
	"""Detect and setup access to GNUmed config file.

	Parts of this will have limited value due to
	wxPython not yet being available.
	"""

	enc = gmI18N.get_encoding()
	paths = gmTools.gmPaths(app_name = 'gnumed')

	candidates = [
		# the current working dir
		['workbase', os.path.join(paths.working_dir, 'gnumed.conf')],
		# /etc/gnumed/
		['system', os.path.join(paths.system_config_dir, 'gnumed-client.conf')],
		# ~/.gnumed/
		['user', os.path.join(paths.user_config_dir, 'gnumed.conf')],
		# CVS/tgz tree .../gnumed/client/ (IOW a local installation)
		['local', os.path.join(paths.local_base_dir, 'gnumed.conf')]
	]
	# --conf-file=
	explicit_fname = _cfg.get(option = '--conf-file', source_order = [('cli', 'return')])
	if explicit_fname is None:
		candidates.append(['explicit', None])
	else:
		candidates.append(['explicit', explicit_fname])

	for candidate in candidates:
		_cfg.add_file_source (
			source = candidate[0],
			file = candidate[1],
			encoding = enc
		)

	# --conf-file given but does not actually exist ?
	if explicit_fname is not None:
		if _cfg.source_files['explicit'] is None:
			_log.error('--conf-file argument does not exist')
			print(missing_cli_config_file % explicit_fname)
			sys.exit(1)

	# any config file found at all ?
	found_any_file = False
	for f in _cfg.source_files.values():
		if f is not None:
			found_any_file = True
			break
	if not found_any_file:
		_log.error('no config file found at all')
		print(no_config_files % '\n '.join(candidates))
		sys.exit(1)

	# mime type handling sources
	fname = 'mime_type2file_extension.conf'
	_cfg.add_file_source (
		source = 'user-mime',
		file = os.path.join(paths.user_config_dir, fname),
		encoding = enc
	)
	_cfg.add_file_source (
		source = 'system-mime',
		file = os.path.join(paths.system_config_dir, fname),
		encoding = enc
	)

#==========================================================
def setup_backend_environment():

	db_version = gmPG2.map_client_branch2required_db_version[current_client_branch]
	_log.info('client expects database version [%s]', db_version)
	_cfg.set_option (
		option = 'database_version',
		value = db_version
	)

	# set up database connection timezone
	timezone = _cfg.get (
		group = 'backend',
		option = 'client timezone',
		source_order = [
			('explicit', 'return'),
			('workbase', 'return'),
			('local', 'return'),
			('user', 'return'),
			('system', 'return')
		]
	)
#	if timezone is not None:
#		gmPG2.set_default_client_timezone(timezone)

#==========================================================
def run_gui():
	gmHooks.run_hook_script(hook = 'startup-before-GUI')

	_use_tui = _cfg.get(option = '--tui', source_order = [('cli', 'return')])
	if _use_tui:
		import curses as ncurs
		try:
			main_scr = ncurs.initscr()
			ncurs.cbreak()
			main_scr.keypad(True)		# arrow keys, Fn keys, etc
			main_scr.addstr('GNUmed text mode user interface')
			main_scr.refresh()
			main_scr.getch()
		finally:
			ncurs.endwin()
		return 0

	from Gnumed.wxpython import gmGuiMain
	profile_file = _cfg.get(option = '--profile', source_order = [('cli', 'return')])
	if profile_file is None:
		gmGuiMain.main()
	else:
		_log.info('writing profiling data into %s', profile_file)
		import profile
		profile.run('gmGuiMain.main()', profile_file)
	gmHooks.run_hook_script(hook = 'shutdown-post-GUI')
	return 0

#==========================================================
def run_tool():
	"""Run a console tool.

	Exit codes as per man page:
		   0: normal termination of the client
		 < 0: some error occurred while trying to run a console tool
			  -1: an unknown console tool was requested
			< -1: an error occurred while a console tool was run
		-999: hard abort of the client

	One of these needs to be returned from this function (and,
	by extension from the tool having been run, if any).
	"""
	tool = _cfg.get(option = '--tool', source_order = [('cli', 'return')])
	if tool is None:
		# not running a tool
		return None

	if tool not in _known_tools:
		_log.error('unknown tool requested: %s', tool)
		print('GNUmed startup: Unknown tool [%s] requested.' % tool)
		print('GNUmed startup: Known tools: %s' % _known_tools)
		return -1

	print('')
	print('==============================================')
	print('Running tool: %s' % tool)
	print('----------------------------------------------')
	print('')

	if tool == 'generate_man_page':
		man_page_fname = os.path.abspath(os.path.join('.', 'gnumed.1'))
		man_page_file = open(man_page_fname, mode = 'wt', encoding = 'utf8')
		man_page_file.write(MANPAGE % datetime.date.today().strftime('%x'))
		man_page_file.close()
		print('MAN page saved as:', man_page_fname)
		return 0

	login, creds = gmPG2.request_login_params()
	pool = gmConnectionPool.gmConnectionPool()
	pool.credentials = creds
	print('')

	if tool == 'read_all_rows_of_table':
		result = gmPG2.read_all_rows_of_table()
		if result in [None, True]:
			print('Success.')
			return 0
		print('Failed. Check the log for details.')
		return -2

	if tool == 'check_mimetypes_in_archive':
		from Gnumed.business import gmDocuments
		return gmDocuments.check_mimetypes_in_archive()

	if tool == 'check_enc_epi_xref':
		from Gnumed.business import gmEMRStructItems
		return gmEMRStructItems.check_fk_encounter_fk_episode_x_ref()

	if tool == 'export_pat_emr_structure':
		# setup praxis
		from Gnumed.business import gmPraxis
		praxis = gmPraxis.gmCurrentPraxisBranch(branch = gmPraxis.get_praxis_branches()[0])
		# get patient
		from Gnumed.business import gmPersonSearch
		pat = gmPersonSearch.ask_for_patient()
		# setup exporters
		from Gnumed.business import gmEMRStructItems
		from Gnumed.exporters import gmTimelineExporter
		from Gnumed.exporters import gmPatientExporter
		while pat is not None:
			print('patient:', pat['description_gender'])
			# as EMR structure
			fname = os.path.expanduser('~/gnumed/gm-emr_structure-%s.txt' % pat.subdir_name)
			print('EMR structure:', gmEMRStructItems.export_emr_structure(patient = pat, filename = fname))
			# as timeline
			fname = os.path.expanduser('~/gnumed/gm-emr-%s.timeline' % pat.subdir_name)
			try:
				print('EMR timeline:', gmTimelineExporter.create_timeline_file (
					patient = pat,
					filename = fname,
					include_documents = True,
					include_vaccinations = True,
					include_encounters = True
				))
			finally:
				pass
			# as journal by encounter
			exporter = gmPatientExporter.cEMRJournalExporter()
			fname = os.path.expanduser('~/gnumed/gm-emr-journal_by_encounter-%s.txt' % pat.subdir_name)
			print('EMR journal (by encounter):', exporter.save_to_file_by_encounter(patient = pat, filename = fname))
			# as journal by mod time
			fname = os.path.expanduser('~/gnumed/gm-emr-journal_by_mod_time-%s.txt' % pat.subdir_name)
			print('EMR journal (by mod time):', exporter.save_to_file_by_mod_time(patient = pat, filename = fname))
			# as statistical summary
			fname = os.path.expanduser('~/gnumed/gm-emr-statistics-%s.txt' % pat.subdir_name)
			output_file = open(fname, mode = 'wt', encoding = 'utf8', errors = 'replace')
			emr = pat.emr
			output_file.write(emr.format_statistics())
			output_file.close()
			print('EMR statistics:', fname)
			# as text file
			exporter = gmPatientExporter.cEmrExport(patient = pat)
			fname = os.path.expanduser('~/gnumed/gm-emr-text_export-%s.txt' % pat.subdir_name)
			output_file = open(fname, mode = 'wt', encoding = 'utf8', errors = 'replace')
			exporter.set_output_file(output_file)
			exporter.dump_constraints()
			exporter.dump_demographic_record(True)
			exporter.dump_clinical_record()
			exporter.dump_med_docs()
			output_file.close()
			print('EMR text file:', fname)
			# another patient ?
			pat = gmPersonSearch.ask_for_patient()

		return 0

	# tool export_patient_as (vcf, gdt, ...)
	#if tool == 'export_pat_demographics':

	# should not happen (because checked against _known_tools)
	return -1

#==========================================================
# shutdown helpers
#----------------------------------------------------------
def shutdown_backend():
	gmPG2.shutdown()

#==========================================================
def shutdown_logging():

#	if _cfg.get(option = u'debug'):
#		import types

#		def get_refcounts():
#			refcount = {}
#			# collect all classes
#			for module in sys.modules.values():
#				for sym in dir(module):
#					obj = getattr(module, sym)
#					if type(obj) is types.ClassType:
#						refcount[obj] = sys.getrefcount(obj)
#			# sort by refcount
#			pairs = map(lambda x: (x[1],x[0]), refcount.items())
#			pairs.sort()
#			pairs.reverse()
#			return pairs

#		rcfile = open('./gm-refcount.lst', 'wt', encoding = 'utf8')
#		for refcount, class_ in get_refcounts():
#			if not class_.__name__.startswith('wx'):
#				rcfile.write(u'%10d %s\n' % (refcount, class_.__name__))
#		rcfile.close()

	# do not choke on Windows
	logging.raiseExceptions = False

#==========================================================
def shutdown_tmp_dir():

	tmp_dir = gmTools.gmPaths().tmp_dir

	if _cfg.get(option = 'debug'):
		_log.debug('not removing tmp dir (--debug mode): %s', tmp_dir)
		return

	_log.warning('removing tmp dir: %s', tmp_dir)
	shutil.rmtree(tmp_dir, True)

#==========================================================
# main - launch the GNUmed wxPython GUI client
#----------------------------------------------------------

random.seed()

# setup
setup_fault_handler(target = None)
setup_console_encoding()
setup_python_path()
setup_logging()
log_startup_info()
setup_console_exception_handler()
setup_cli()
setup_signal_handlers()
setup_local_repo_path()

from Gnumed.pycommon import gmI18N
from Gnumed.pycommon import gmTools
from Gnumed.pycommon import gmDateTime

setup_locale()
handle_help_request()
handle_version_request()
setup_paths_and_files()
setup_date_time()
setup_cfg()

from Gnumed.pycommon import gmPG2
from Gnumed.pycommon import gmConnectionPool
setup_backend_environment()

# main
exit_code = run_tool()
if exit_code is None:
	from Gnumed.pycommon import gmHooks
	exit_code = run_gui()

# shutdown
shutdown_backend()
shutdown_tmp_dir()
_log.info('Normally shutting down as main module.')
shutdown_logging()

sys.exit(exit_code)

#==========================================================
