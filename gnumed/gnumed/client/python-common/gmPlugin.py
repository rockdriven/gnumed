#!/usr/bin/python
#############################################################################
#
# gmPlugin - base classes for GNUMed's plugin architecture
# ---------------------------------------------------------------------------
#
# @author: Dr. Horst Herb
# @copyright: author
# @license: GPL (details at http://www.gnu.org)
# @dependencies: nil
# @change log:
#	08.03.2002 hherb first draft, untested
#
# @TODO: Almost everything
############################################################################
# $Source: /home/ncq/Projekte/cvs2git/vcs-mirror/gnumed/gnumed/client/python-common/Attic/gmPlugin.py,v $
__version__ = "$Revision: 1.25 $"
__author__ = "H.Herb, I.Haywood, K.Hilbert"

import os, sys, re, traceback, cPickle, zlib

from wxPython.wx import *

import gmExceptions, gmGuiBroker, gmPG, gmConf, gmShadow, gmLog
log = gmLog.gmDefLog.Log
#------------------------------------------------------------------
class gmPlugin:
	"""base class for all gnumed plugins"""
	#-----------------------------------------------------
	def provides ():
		"""
		Returns a list of services that the plugin provides
		"""
		return []
	#-----------------------------------------------------
	def requires ():
		"""
		Requires a list of services that must be registered
		before this plugin is registered. The configuration
		tool must check these and make sure the load order
		satisfies the plugins' requirements
		"""
		return []
	#-----------------------------------------------------
	def description ():
		"""Returns a brief description of the plugin.
		"""
		pass
	#-----------------------------------------------------
	def name (self):
		return ''
	#-----------------------------------------------------
	def register(self):
		raise gmExceptions.PureVirtualFunction()
	#-----------------------------------------------------
	def unregister(self):
		raise gmExceptions.PureVirtualFunction()
#------------------------------------------------------------------
class wxBasePlugin (gmPlugin):
	
	"""
	base class for all plugins providing wxPython widgets.
	Plugins must have a class descending of this class in their file, which MUST HAVE THE SAME NAME AS THE FILE.
	The file must be in a directory which is loaded by LoadPluginSet (gui/ for the moment, others may be added for different plugin types)
	
	"""
	# NOTE: I anticipate that all plugins will in fact be derived
	# from this class. Without the brokers a plugin is useless (IH)
	def __init__(self, guibroker=None, callbackbroker=None, dbbroker=None, params=None):
		self.gb = guibroker
		self.cb = callbackbroker
		self.db = dbbroker
		if self.gb is None:
			self.gb = gmGuiBroker.GuiBroker ()
		if self.db is None:
			self.db = gmPG.ConnectionPool ()
	#-----------------------------------------------------
	def GetIcon (self):
		"""Return icon representing page on the toolbar.

		This is the default behaviour. GetIconData should return
		pickled, compressed and escaped string with the icon data.

		If you want to change the behaviour (because you want to load
		plugin icons from overseas via a satellite link or something
		you need to override this function in your plugin (class).

		Using this standard code also allows us to only import cPickle
		and zlib here and not in each and every plugin module which
		should speed up plugin load time :-)
		"""
		# FIXME: load from config which plugin we want
		# which_icon is a cookie stored on the backend by a config manager,
		# it tells the plugin which icon to return data for,
		which_icon = None
		icon_data = self.GetIconData(which_icon)
		if icon_data == None:
			return None
		else:
			return wxBitmapFromXPMData(cPickle.loads(zlib.decompress(icon_data)))
	#-----------------------------------------------------
	def GetIconData(self, anIconID = None):
		# FIXME: in overriding methods need to be very careful about the
		# type of the icon ID since if we read it back from the database we
		# may not know what type it was
		return None
	#-----------------------------------------------------
	def GetWidget (self, parent):
		"""
		Return the widget to display
		"""
		raise gmExceptions.PureVirtualFunction()
	#-----------------------------------------------------
	def MenuInfo (self):
		"""Return tuple of (menuname, menuitem).

		menuname can be "tools", "view", "help", "file"
		"""
		raise gmExceptions.PureVirtualFunction()
	#-----------------------------------------------------
	def Raise (self):
		"""Raises this plugin to the top level if not visible.
		"""
		raise gmExceptions.PureVirtualFunction ()
	#-----------------------------------------------------
	def Shown (self):
		"""Called whenever this module is shown onscreen.
		"""
		pass
#------------------------------------------------------------------
class wxNotebookPlugin (wxBasePlugin):
	"""
	Base plugin for plugins which provide a 'big page'
	Either whole screen, or notebook if it exists
	"""	
	def register (self):
		"""Register ourselves with the main notebook widget."""

		# add ourselves to the main notebook
		self.nb = self.gb['main.notebook']
		self.nb_no = self.nb.GetPageCount ()
		widget = self.GetWidget (self.nb)
		self.nb.AddPage (widget, self.name ())
		widget.Show (1)

		# place ourselves in the main toolbar
		# FIXME: this should be optional
		self.tbm = self.gb['main.toolbar']
		tb = self.tbm.AddBar (self.nb_no)
		self.gb['toolbar.%s' % self.name ()] = tb
		self.DoToolbar (tb, widget)
		tb.Realize ()

		# and put ourselves into the menu structure
		# FIXME: this should be optional, too
		if self.MenuInfo ():
			menuset, menuname = self.MenuInfo ()
			menu = self.gb['main.%smenu' % menuset]
			self.menu_id = wxNewId ()
			menu.Append (self.menu_id, menuname, self.name ())
			EVT_MENU (self.gb['main.frame'], self.menu_id, self.OnMenu)
		# so notebook can find this widget
		self.gb['main.notebook.numbers'][self.nb_no] = self
	#-----------------------------------------------------
	def unregister (self):
		"""Remove ourselves."""
		menu = self.gb['main.%smenu' % self.MenuInfo ()[0]]
		menu.Delete (self.menu_id)
		nb = gb['main.notebook']
		nb.DeletePage (self.nb_no)
		self.tbm.DeleteBar (self.nb_no)
		# FIXME: shouldn't we delete the menu item, too ?
	#-----------------------------------------------------	
	def Raise (self):
		self.nb.SetSelection (self.nb_no)
		self.tbm.ShowBar (self.nb_no)
	#-----------------------------------------------------
	def OnMenu (self, event):
		self.Raise ()
	#-----------------------------------------------------
	def GetNotebookNumber (self):
		return self.nb_no
	#----------------------------------------------------
	def DoToolbar (self, tb, widget):
		"""
		sets up the toolbar for this widget.
		tb is the toolbar
		widget is the widget returned by GetWidget () for connecting events
		"""
		pass
#------------------------------------------------------------------
class wxPatientPlugin (wxBasePlugin):
	"""
	A 'small page', sits inside the patient view, with the side visible
	"""
	def register (self):
		self.mwm = self.gb['patient.manager']
		if gmConf.config['main.shadow']:
			shadow = gmShadow.Shadow (self.mwm, -1)
			widget = self.GetWidget (shadow)
			shadow.SetContents (widget)
			self.mwm.RegisterLeftSide (self.name (), shadow)
		else:
			widget = self.GetWidget (self.mwm)
			self.mwm.RegisterLeftSide (self.name (), self.GetWidget (self.mwm))
		icon = self.GetIcon ()
		if icon is not None:
			tb2 = self.gb['toolbar.Patient']
			#tb2.AddSeparator()
			self.tool_id = wxNewId ()
			tool1 = tb2.AddTool(self.tool_id, icon,
					    shortHelpString=self.name ())
			EVT_TOOL (tb2, self.tool_id, self.OnTool)
		menuname = self.name ()
		menu = self.gb['patient.submenu']
		self.menu_id = wxNewId ()
		menu.Append (self.menu_id, menuname)
		EVT_MENU (self.gb['main.frame'], self.menu_id, self.OnTool)
	#-----------------------------------------------------        
	def OnTool (self, event):
		self.Shown ()
		self.mwm.Display (self.name ())
		self.gb['modules.gui']['Patient'].Raise ()
	#-----------------------------------------------------
	def Raise (self):
		self.gb['modules.gui']['Patient'].Raise ()
		self.mwm.Display (self.name ())
	#-----------------------------------------------------
	def unregister (self):
		self.mwm.Unregister (self.name ())
		menu = self.gb['main.submenu']
		menu.Delete (menu_id)
		if self.GetIcon () is not None:
			tb2 = self.gb['toolbar.Patient Window']
			tb2.DeleteTool (self.tool_id)
#------------------------------------------------------------------
def LoadPlugin (aPackage, plugin_name, guibroker = None, dbbroker = None):
	"""Loads a plugin from a package directory.

	- "set" specifies the subdirectory in which to find the plugin
	- this knows nothing of databases, all it does is load a named plugin

	There will be a general 'gui' directory for large GUI
	components: prescritions, etc., then several others for more
	specific types: export/import filters, crypto algorithms
	guibroker, dbbroker are broker objects provided
	defaults are the default set of plugins to be loaded

	FIXME: we should inform the user about failing plugins
	"""
	# we do need brokers, else we are useless
	if guibroker is None:
		guibroker = gmGuiBroker.GuiBroker ()
	if dbbroker is None:
		dbbroker = gmPG.ConnectionPool ()

	# bean counting ! -> loaded plugins
	if not ('modules.%s' % aPackage) in guibroker.keylist ():
		guibroker['modules.%s' % aPackage] = {}

	try:
		# use __import__() so we can dynamically calculate the module name
		mod_from_pkg = __import__ ("%s.%s" % (aPackage, plugin_name))
		# find name of class of plugin (must be the same as the plugin module filename)
		# 1) get module name
		plugin_module_name = mod_from_pkg.__dict__[plugin_name]
		# 2) get class name
		plugin_class = plugin_module_name.__dict__[plugin_name]
	except:
		exc = sys.exc_info()
		gmLog.gmDefLog.LogException ('Cannot import module "%s.%s".' % (aPackage, plugin_name), exc)
		return None

	if not issubclass (plugin_class, wxBasePlugin):
		log (gmLog.lErr, "class %s is not a subclass of wxBasePlugin" % plugin_name)
		return None

	log (gmLog.lInfo, "registering plugin %s" % plugin_name)
	try:
		plugin = plugin_class(guibroker = guibroker, dbbroker = dbbroker)
		plugin.register ()
	except:
		exc = sys.exc_info()
		gmLog.gmDefLog.LogException ('Cannot register module "%s.%s".' % (aPackage, plugin_name), exc)
		return None

	guibroker['modules.%s' % aPackage][plugin.name()] = plugin

	return 1
#------------------------------------------------------------------
# (FIXME: get plugin list from gmconfiguration for this user).
def GetAllPlugins (set):
	"""
	Searches the directory for all plugins
	"""
	gb = gmGuiBroker.GuiBroker ()
	dir = gb['gnumed_dir']
	# FIXME: in future versions we will ask the backend where plugins are
	dir = os.path.join (dir, 'wxpython', set)
	config_fname = os.path.join(dir, 'plugins.cfg')
	#see whether we shall only load specific plugins in a specific order
	try:
		f = open(config_fname)
		filesCR = f.readlines()
		files=[]
		for file in filesCR:
			files.append(file[:-1])
	except:
		files = os.listdir (dir)
	ret = []
	for f in files:
		if re.compile ('.+\.py$').match (f) and f != '__init__.py':
			ret.append (f[:-3])
	return ret
	
#------------------------------------------------------------------
def UnloadPlugin (set, name):
	"""
	Unloads the named plugin
	"""
	gb = gmGuiBroker.GuiBroker ()
	plugin = gb['modules.%s' % set][name]
	plugin.unregister ()
	del gb['modules.%s' % set][name]
	log (gmLog.lInfo, "unloaded plugin %s/%s" % (set, name))
#==================================================================
# Main
#------------------------------------------------------------------
log(gmLog.lData, __version__)
#==================================================================
# $Log: gmPlugin.py,v $
# Revision 1.25  2002-11-12 20:30:10  hherb
# Uses an optional config file in each plugin directory determining the order plugins are loaded as well as which plugins are loaded
#
# Revision 1.24  2002/09/26 13:10:43  ncq
# - silly ommitance
#
# Revision 1.23  2002/09/26 13:08:51  ncq
# - log version on import
# - TODO -> FIXME
#
# Revision 1.22  2002/09/09 00:50:28  ncq
# - return success or failure on LoadPlugin()
#
