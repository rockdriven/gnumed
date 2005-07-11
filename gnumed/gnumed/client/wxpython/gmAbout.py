#====================================================================
# About GNUmed
#====================================================================
# $Source: /home/ncq/Projekte/cvs2git/vcs-mirror/gnumed/gnumed/client/wxpython/gmAbout.py,v $
# $Id: gmAbout.py,v 1.15 2005-07-11 16:16:21 ncq Exp $
__version__ = "$Revision: 1.15 $"
__author__ = "M.Bonert"
__license__ = "GPL"

from wxPython.wx import *
import zlib, cPickle

ID_MENU = wxNewId()
ID_EXIT = wxNewId()
#====================================================================
class ScrollTxtWin (wxWindow):
	"""
	Scrolling Text!
	"""

	# control parameters
	__scroll_speed=.3 	# pixels/milliseconds (?)
	__delay=500		# milliseconds
	name_list = [
		'Dr Gerardo Arnaez',
		'Dr Hilmar Berger',
		'Michael Bonert',
		'Dr Elizabeth Dodd',
		'Engelbert Gruber',
		'Dr David Guest',
		'Ian Haywood',
		'Dr Tony Lembke',
		'Thierry Michel',
		'Dr Richard Terry',
		'Syan J Tan',
		'Andreas Tille',
		'Dr Carlos Moro'
	]

	# initializations
	__scroll_ctr=+230
	__name_ctr=1
	__delay_ctr=1

	def __init__ (self, parent):
		wxWindow.__init__(self, parent, -1, size=(230,20), style=wxSUNKEN_BORDER)
		self.SetBackgroundColour(wxColour(255, 255, 255))
		self.__delay_ctr_reset=self.__delay*self.__scroll_speed

		self.moving_txt=wxStaticText(self, -1, "", size=(230,20), style=wxALIGN_CENTRE | wxST_NO_AUTORESIZE)
		self.moving_txt.SetFont(wxFont(10, wxSWISS, wxNORMAL, wxNORMAL))
		self.moving_txt.SetLabel(self.name_list[0])

		EVT_TIMER(self, -1, self.OnTimer)
		self.timer = wxTimer(self, -1)
		#self.timer.Start(self.__scroll_speed)
		self.timer.Start(1./self.__scroll_speed)

	def OnTimer(self, evt):
		if(self.__scroll_ctr<-2 and self.__delay_ctr<self.__delay_ctr_reset):
			# pause at centre
			self.__delay_ctr=self.__delay_ctr+1
		else:
			self.__scroll_ctr=self.__scroll_ctr-1
			self.moving_txt.MoveXY(self.__scroll_ctr, 0)
		if(self.__scroll_ctr<-230):
			# reset counters
			self.__scroll_ctr=+230
			self.__delay_ctr=1

			# get next name in dict.
			self.moving_txt.SetLabel(self.name_list[self.__name_ctr])
			self.__name_ctr=self.__name_ctr+1
			if(self.__name_ctr>len(self.name_list)-1):
				self.__name_ctr=0

class AboutFrame (wxFrame):
	"""
	About GNUmed
	"""

	icon_serpent='x\xdae\x8f\xb1\x0e\x83 \x10\x86w\x9f\xe2\x92\x1blb\xf2\x07\x96\xeaH:0\xd6\
\xc1\x85\xd5\x98N5\xa5\xef?\xf5N\xd0\x8a\xdcA\xc2\xf7qw\x84\xdb\xfa\xb5\xcd\
\xd4\xda;\xc9\x1a\xc8\xb6\xcd<\xb5\xa0\x85\x1e\xeb\xbc\xbc7b!\xf6\xdeHl\x1c\
\x94\x073\xec<*\xf7\xbe\xf7\x99\x9d\xb21~\xe7.\xf5\x1f\x1c\xd3\xbdVlL\xc2\
\xcf\xf8ye\xd0\x00\x90\x0etH \x84\x80B\xaa\x8a\x88\x85\xc4(U\x9d$\xfeR;\xc5J\
\xa6\x01\xbbt9\xceR\xc8\x81e_$\x98\xb9\x9c\xa9\x8d,y\xa9t\xc8\xcf\x152\xe0x\
\xe9$\xf5\x07\x95\x0cD\x95t:\xb1\x92\xae\x9cI\xa8~\x84\x1f\xe0\xa3ec'

	def __init__(self, parent, ID, title, pos=wxDefaultPosition, size=wxDefaultSize, style=wxDEFAULT_FRAME_STYLE):
		wxFrame.__init__(self, parent, ID, title, pos, size, style)

		icon = wxEmptyIcon()
		icon.CopyFromBitmap(wxBitmapFromXPMData(cPickle.loads(zlib.decompress(self.icon_serpent))))
		self.SetIcon(icon)

		box = wxBoxSizer(wxVERTICAL)
		if wxPlatform == '__WXMAC__':
			box.Add((0,0), 2)
		else:
			box.Add((0,0), 2)
		intro_txt=wxStaticText(self, -1, _("Monty the Serpent && the FSF Present"))
		intro_txt.SetFont(wxFont(10,wxSWISS,wxNORMAL,wxNORMAL,False,''))
		box.Add(intro_txt, 0, wxALIGN_CENTRE)
		if wxPlatform == '__WXMAC__':
			box.Add((0,0), 3)
		else:
			box.Add((0,0), 3)
		gm_txt=wxStaticText(self, -1, "GNUmed")
		gm_txt.SetFont(wxFont(30, wxSWISS, wxNORMAL, wxNORMAL))
		box.Add(gm_txt, 0, wxALIGN_CENTRE)

		motto_txt=wxStaticText(self, -1, _("Free eMedicine"))
		motto_txt.SetFont(wxFont(10,wxSWISS,wxNORMAL,wxNORMAL,False,''))
		box.Add(motto_txt, 0, wxALIGN_CENTRE)
		if wxPlatform == '__WXMAC__':
			box.Add((0,0), 4)
		else:
			box.Add((0,0), 4)
		ver_txt=wxStaticText(self, -1, _("Version 0.1 brought to you by"))
		ver_txt.SetFont(wxFont(10, wxSWISS, wxNORMAL, wxNORMAL))
		box.Add(ver_txt, 0, wxALIGN_CENTRE)

		admins_txt=wxStaticText(self, -1, _("Drs Horst Herb && Karsten Hilbert"))
		admins_txt.SetFont(wxFont(10, wxSWISS, wxNORMAL, wxNORMAL))
		box.Add(admins_txt, 0, wxALIGN_CENTRE)

		self.win=ScrollTxtWin(self)
		box.Add(self.win, 0, wxALIGN_CENTRE)
		if wxPlatform == '__WXMAC__':
			box.Add((0,0), 1)
		else:
			box.Add((0,0), 1)
		info_txt=wxStaticText(self, -1, _("Please visit http://www.gnumed.org/ for more info"))
		info_txt.SetFont(wxFont(10, wxSWISS, wxNORMAL, wxNORMAL))
		box.Add(info_txt, 0, wxALIGN_CENTRE)
		if wxPlatform == '__WXMAC__':
			box.Add((0,0), 1)
		else:
			box.Add((0,0), 1)
		btn = wxButton(self, ID_MENU , _("Close"))
		box.Add(btn,0, wxALIGN_CENTRE)
		if wxPlatform == '__WXMAC__':
			box.Add((0,0), 1)
		else:
			box.Add((0,0), 1)
		EVT_BUTTON(btn, ID_MENU, self.OnClose)

		self.SetAutoLayout(True)
 		self.SetSizer(box)
 		self.Layout()

	def OnClose (self, event):
		self.win.timer.Stop ()
		self.Destroy ()
#====================================================================
class cContributorsDlg(wx.wxDialog):
	# people who don't want to be listed here:
	# ...
	contributors = _(
'The following people kindly contributed to GNUmed.\n'
'Please write to <gnumed-devel@gnu.org> to have your\n'
'contribution duly recognized in this list or to have\n'
'your name removed from it for, say, privacy reasons.\n\n'
'Note that this list is sorted alphabetically by last\n'
'name, first name. If the only identifier is an email\n'
'address it is sorted under the first character of\n'
'the user name.\n'
'%s'
) % """
== F ===========================================

Joachim Fischer
 GP Fischer + Lintz
 Fach�rzte Allgemeinmedizin
 Wolfschlugen

 - Karteieintragsarten passend f�r Deutschland

== P ===========================================

Martin Preuss

 - Chipkartenansteuerung

== T ===========================================

Andreas Tille

 - Debian packages
 - encouragement, wisdom

"""
	#----------------------------------------------
	def __init__(self, *args, **kwargs):
		wx.wxDialog.__init__(self, *args, **kwargs)
		contributor_listing = wx.wxTextCtrl (
			self,
			-1,
			cContributorsDlg.contributors,
			style = wx.wxTE_MULTILINE | wx.wxTE_READONLY,
			size = wx.wxSize(400,300)
		)
#		contributor_listing.SetFont(wx.wxFont(12, wx.wxMODERN, wx.wxNORMAL, wx.wxNORMAL))
		# arrange widgets
		szr_outer = wx.wxBoxSizer(wx.wxVERTICAL)
		szr_outer.Add(contributor_listing, 1, wx.wxEXPAND, 0)
		# and do layout
		self.SetAutoLayout(1)
		self.SetSizerAndFit(szr_outer)
		szr_outer.SetSizeHints(self)
		self.Layout()
#====================================================================
# Main
#====================================================================
if __name__ == '__main__':
	# set up dummy app
	class TestApp (wxApp):
		def OnInit (self):
			frame = AboutFrame(None, -1, "About GNUmed", size=wxSize(300, 250))
			frame.Show(1)
			return 1
	#---------------------
	_ = lambda x:x
	app = TestApp ()
	app.MainLoop ()

#------------------------------------------------------------
# $Log: gmAbout.py,v $
# Revision 1.15  2005-07-11 16:16:21  ncq
# - display contributor dialog in a proper size
#
# Revision 1.14  2005/07/11 09:04:27  ncq
# - add contributors dialog
#
# Revision 1.13  2005/07/02 18:19:01  ncq
# - one more GnuMed -> GNUmed
#
# Revision 1.12  2005/06/30 10:05:47  cfmoro
# String corrections
#
# Revision 1.11  2005/06/21 04:57:12  rterry
# fix this to run under wxPython26
# -e.g incorrect sizer attributes
#
# Revision 1.10  2005/05/30 09:20:51  ncq
# - add Carlos Moro
#
# Revision 1.9  2004/07/18 20:30:53  ncq
# - wxPython.true/false -> Python.True/False as Python tells us to do
#
# Revision 1.8  2004/06/30 15:56:14  shilbert
# - more wxMAC fixes -they don't stop surfacing :-)
#
# Revision 1.7  2003/11/17 10:56:37  sjtan
#
# synced and commiting.
#
# Revision 1.1  2003/10/23 06:02:39  sjtan
#
# manual edit areas modelled after r.terry's specs.
#
# Revision 1.6  2003/05/17 18:18:19  michaelb
# added $Log statement
#
# 30/01/03: inital version
