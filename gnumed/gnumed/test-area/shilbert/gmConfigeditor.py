#!/usr/bin/env python

__version__ = ""
__author__ = "S.Hilbert, K.Hilbert"

import sys, os, string
# location of our modules
if __name__ == "__main__":
	#sys.path.append(os.path.join('..', '..', 'python-common'))
	#sys.path.append(os.path.join('..', '..', 'business'))
	sys.path.append(os.path.join('.','modules'))

import gmLog
_log = gmLog.gmDefLog
if __name__ == '__main__':
	_log.SetAllLogLevels(gmLog.lData)

_log.Log(gmLog.lData, __version__)

if __name__ == "__main__":
	import gmI18N

import gmCfg
_cfg = gmCfg.gmDefCfgFile

from wxPython.wx import *

[wxID_WXFRAME1, 
wxID_WXFRAME1NOTEBOOK1, 
wxID_WXFRAME1MAINPANEL, 
wxID_WXFRAME1STARTPANEL, 
wxID_WXFRAME1METADATAPANEL, 
wxID_WXFRAME1SCANPANEL, 
wxID_WXFRAME1INDEXPANEL, 
wxID_WXFRAME1IMPORTPANEL, 
wxID_WXFRAME1VIEWERPANEL,
wxID_WXFRAME1DATABASEPANEL,
wxID_WXFRAME1DUMPTOCFGFILEPANEL,
wxID_old_to_new_BTN,
wxID_new_to_old_BTN,
wxID_new_BTN,
wxID_old_to_new_rep_BTN,
wxID_new_to_old_rep_BTN,
wxID_check_metadata_BTN,
wxID_check_scan_BTN,
wxID_check_index_BTN,
wxID_check_import_BTN,
wxID_check_viewer_BTN,
wxID_check_database_BTN,
wxID_write_cfgfile_BTN,
wxID_new_rep_BTN,
wxID_tmp_dir_BTN,
wxID_export_dirBTN,
wxID_sel_idfile_BTN,
wxID_patient_fileBTN,
wxID_viewer_patient_fileBTN,
wxID_repository_dirBTN,
wxID_SelBOX_id_mode,
wxID_SelBOX_show_id,
wxID_SelBOX_do_barcodes,
wxID_SelBOX_JPEG_conv,
wxID_SelBOX_progressive_JPEG,
wxID_patient_format_view_LBOX,
wxID_patient_format_idx_LBOX,
wxID_patient_format_import_LBOX ] = map(lambda _init_ctrls: wxNewId(), range(38))

class gmConfigEditorPanel(wxPanel):
	def __init__(self, parent):
		wxPanel.__init__(self, parent, -1)
		self.parent_notebook = wxNotebook(self, -1, style=wxNB_RIGHT)
		self.CtrlsContainer = []
		self.groupCtrlsList = {}
		self.optionCtrlsList = {}
		#create notebook tab for checking and saving
		self.saveCfgFilePanel = wxPanel(id = wxID_WXFRAME1DUMPTOCFGFILEPANEL, name = 'dumptoCfgFilePanel', parent = self.parent_notebook, pos = wxPoint(0,0), size = wxSize(768, 513), style = wxTAB_TRAVERSAL)
		self.parent_notebook.AddPage(self.saveCfgFilePanel,'check n save')
		y = 20
		# get the name of all the groups in a config-file and
		# add a notebook tab for each 
		groups  = _cfg.getGroups()
		for group in groups:		
		# create a check-button for each group on the "check n save" panel
			BTNcheck_n_save  = wxButton (self.saveCfgFilePanel,-1,group,(20,y))
			y = y + 30
			# dynamically draw the rest
			panel_nb_page = wxPanel(
				id = -1,
				 name = group,
				 parent = self.parent_notebook,
				 pos = wxPoint(0, 0), 
				 size = wxSize(640, 480),
				 style = wxTAB_TRAVERSAL
			)
			self.parent_notebook.AddPage(panel_nb_page, group)    	
			panelsizer = wxBoxSizer(wxVERTICAL)
			
			notebooksizer = wxBoxSizer(wxVERTICAL)
			grid_sizer_1 = wxGridSizer(14, 2, 0, 0)
			# now get all available options in a group plus their descriptions
			# add descritiption and options as statictext
			options  = _cfg.getOptions(group)	
			# now get all available options in a group plus their descriptions
			# add description and options as statictext
			for option in options:	
				tempcomment = wxStaticText(panel_nb_page,-1,str(option))
				#tempcomment = wxStaticText(self.panel,-1,str(string.join(_cfg.getComment(group,option),"\n")))
				tempctrl = wxTextCtrl(panel_nb_page,-1,str(_cfg.get(group,option)))
				self.optionCtrlsList[option]=tempctrl
				grid_sizer_1.Add(tempcomment, 0, wxLEFT, 10)
				grid_sizer_1.Add(tempctrl, 0, wxLEFT, 10)
			
			self.groupCtrlsList[group]=self.optionCtrlsList
			#now clean the list of ctrls
			self.optionCtrlsList = {}
			#print self.groupCtrlsList
			notebooksizer.Add(grid_sizer_1, 1, wxEXPAND, 0)
			panel_nb_page.SetAutoLayout(1)
			panel_nb_page.SetSizer(notebooksizer)
			notebooksizer.Fit(panel_nb_page)
			notebooksizer.SetSizeHints(panel_nb_page)
			panelsizer.Add(wxNotebookSizer(self.parent_notebook), 1, wxEXPAND, 0)
			self.SetAutoLayout(1)
			self.SetSizer(panelsizer)
			panelsizer.Fit(self)
			panelsizer.SetSizeHints(self)
			self.Layout()
			#append dictionary to a list
			self.CtrlsContainer.append(self.groupCtrlsList)
			# clean dictionary
			self.groupCtrlsList = {}
		#self.check_metadata_BTN  = wxButton (self.dumptoCfgFilePanel,wxID_check_metadata_BTN,_('check metadata'),(1,20))
		#self.check_scan_BTN      = wxButton (self.dumptoCfgFilePanel,wxID_check_scan_BTN,_('check scan'),(1,60))
		#self.check_index_BTN     = wxButton (self.dumptoCfgFilePanel,wxID_check_index_BTN,_('check index'),(1,100))
		#self.check_import_BTN    = wxButton (self.dumptoCfgFilePanel,wxID_check_import_BTN,_('check import'),(1,140))
		#self.check_viewer_BTN    = wxButton (self.dumptoCfgFilePanel,wxID_check_viewer_BTN,_('check viewer'),(1,180))
		#self.check_database_BTN  = wxButton (self.dumptoCfgFilePanel,wxID_check_database_BTN,_('check database'),(1,220))
		self.write_cfgfile_BTN  = wxButton (self.saveCfgFilePanel,wxID_write_cfgfile_BTN,_('write configfile'),(1,260))
		#EVT_BUTTON(self.check_metadata_BTN, wxID_check_metadata_BTN, self.on_check_metadata_BTN)
		#EVT_BUTTON(self.check_scan_BTN, wxID_check_scan_BTN, self.on_check_scan_BTN)
		#EVT_BUTTON(self.check_index_BTN, wxID_check_index_BTN, self.on_check_index_BTN)
		#EVT_BUTTON(self.check_import_BTN, wxID_check_import_BTN, self.on_check_import_BTN)
		#EVT_BUTTON(self.check_viewer_BTN, wxID_check_viewer_BTN, self.on_check_viewer_BTN)
		#EVT_BUTTON(self.check_database_BTN, wxID_check_database_BTN, self.on_check_database_BTN)
		EVT_BUTTON(self.write_cfgfile_BTN, wxID_write_cfgfile_BTN, self.__dump_to_cfgfile)

	def __dump_to_cfgfile(self, aDir):
		# retrieve individual dicts from list of groupdicts 
		for elementsdict in self.CtrlsContainer:
			#retrieve list of groupsnames ( key in each dict)  
			temp = elementsdict.keys()
			for groups in temp:
				#print groups
				# retrieve dict of options for this group 
				optionsdict = elementsdict[groups]
				temp = optionsdict.keys()
				for option in temp:
					data = optionsdict[option].GetValue()
					_cfg.set(groups,option,data)
	    	_cfg.store()
		#else:
		#    dlg = wxMessageDialog(
		#	self,
		#	_('[dump] error : not all sections were ok'),
		#	_('checking [dump] sections'),
		#	wxOK | wxICON_ERROR
		#    )
		#    dlg.ShowModal()
		#    dlg.Destroy()
		#    return 1
	
	
	
#================================================================
# MAIN
#----------------------------------------------------------------
if __name__ == '__main__':
	_log.Log (gmLog.lInfo, "starting config editor")

	if _cfg == None:
		_log.Log(gmLog.lErr, "Cannot run without config file.")
		sys.exit("Cannot run without config file.")

	# catch all remaining exceptions
	try:
		application = wxPyWidgetTester(size=(800,1000))
		application.SetWidget(gmConfigEditorPanel)
		application.MainLoop()
	except:
		_log.LogException("unhandled exception caught !", sys.exc_info(), fatal=1)
		# but re-raise them
		raise

	_log.Log (gmLog.lInfo, "closing config editor")

else:
	import gmPlugin

	class gmConfigEditor(gmPlugin.wxNotebookPlugin):
		def name (self):
			return _("config")

		def GetWidget (self, parent):
			self.configeditor = gmConfigEditorPanel(parent)
			return self.viewer

		def MenuInfo (self):
			return ('tools', _('&config file edit'))

		def ReceiveFocus(self):
			# get file name
			# - via file select dialog
			aWildcard = "%s (*.conf)|*.conf|%s (*.*)|*.*" % (_("config file"), _("all files"))
			aDefDir = os.path.abspath(os.path.expanduser(os.path.join('~', "gnumed")))
			dlg = wxFileDialog(
				parent = NULL,
				message = _("Choose a config file"),
				defaultDir = aDefDir,
				defaultFile = "",
				wildcard = aWildcard,
				style = wxOPEN | wxFILE_MUST_EXIST
			)
			if dlg.ShowModal() == wxID_OK:
				fname = dlg.GetPath()
			dlg.Destroy()
			_log.Log(gmLog.lData, 'selected [%s]' % fname)

			# - via currently selected patient -> XDT files
			# ...

			self.viewer.filename = fname
			self.viewer.Populate()
			return 1

# $Log: gmConfigeditor.py,v $
# Revision 1.7  2003-04-13 17:42:00  shilbert
# - typos in panel names fixed
#
# Revision 1.6  2003/04/13 17:37:47  shilbert
#  - now save changes
#
# Revision 1.5  2003/04/13 15:08:17  ncq
# - some cleanup, added comments
#
# Revision 1.4  2003/04/12 17:07:17  shilbert
# complete rewrite
# converted from static to dynamic
#
# Revision 1.3  2003/04/05 00:22:05  shilbert
# clean up
#