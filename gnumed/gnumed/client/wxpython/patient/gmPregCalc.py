#!/usr/bin/env python
#====================================================================
# GnuMed tool to calculate expected date of delivery & 18th week ultrasound scan
# licence: GPL - Copyright (c) 2003
# Changelog:
# 11/7/02: inital version
#====================================================================
# $Source: /home/ncq/Projekte/cvs2git/vcs-mirror/gnumed/gnumed/client/wxpython/patient/Attic/gmPregCalc.py,v $
# $Id: gmPregCalc.py,v 1.1 2003-07-07 02:59:57 michaelb Exp $
__version__ = "$Revision: 1.1 $"
__author__ = "M. Bonert, R. Terry, I. Haywood"

from wxPython.wx import *
from wxPython.calendar import *
from wxPython.lib.rcsizer import RowColSizer
import math, zlib, cPickle
import random
import string

ID_LNMP = wxNewId ()
ID_DUE = wxNewId ()
ID_DAY = wxNewId ()
ID_WEEK = wxNewId ()
ID_MENU = wxNewId ()

# Naegele's rule is easy for manual calculation, but a pain to code
# Enter Haywood's rule ;-), human gestation is defined as 24192000 seconds.
# 	ideally, tool should query backend for parity, race, etc. for exact measurement
GESTATION = 24192000
WEEK = 604800
DAY = 86400
US18_52 = 10886400	# 18 weeks in seconds (for 18/52 Ultrasound)
#====================================================================

_icons = {"""icon_Preg_calc""":
'x\xdaMP1\x0e\x830\x0c\xdcy\x85\xa5\x0et\xb2`h\x95\xb9H\xac\x0c,^\x11c\x91\
\xdc\xffO\xbd\xb3C\xc0\xb1\x02w\xf1]\xec<\x8f\xdf\xd8\xad\xfd\xf8\x16\xe4K\
\xc6\xbe\xdb\xd6\xded\x97\xcf\xb1\xed\xdf@\x0e\xf4\x98\x06\xae\xc0J\\\x06\
\xae\xc0B<\x97y\x9aK\xe0%\xf1\x80\xc8sU5\xb5H\x84T\x13A:"~\xb4\x92\x0e\x8aE\
\xa0],I%\'\xac\x03\xab\xad\x92%u\xabr\xa3\x15\x85Hx\xa6\xdc<]%X\xafr\xcf\xd0\
\xdcje\xa8\xa3\x94\xfaS\xeeI\xe4mv\xde\xae\xd9\xd2\x02\xcb[\xf3\x9ar\xf56Q\
\xb0\x11\xe4\xeec\xfa\xe9\x9c$\xa7`\x03No|\xda\xd3]\xe1|:\xfd\x03\xab\xf8h\
\xbf' }

class PregnancyFrame (wxFrame):
	"""
	The new pregnancy calculator.
	"""

	#TODO
	# IMPROVE removal of time from txtlnmp, txtedc, txtdue (?)
	#	see: def PurgeTime(self, date):
	#
	# general clean-up of code -- remove 'LNMP's -- make all 'LMP'
	#	remove dead code
	#
	# explore idea of 'status bar' across bottom -- something to make
	# 	clear how to use the calculator
	#
	# change the set-up of the RowColSizer(), shrink the size of the 'Weeks' & 'Days' fields
	#	make column on right side of preg. calc. more compact
	#
	# clean-up the names of the variables (some could be named more descriptively)
	#

	def __init__ (self, parent):
		myStyle = wxMINIMIZE_BOX | wxSYSTEM_MENU | wxCAPTION | wxALIGN_CENTER | \
			wxALIGN_CENTER_VERTICAL | wxTAB_TRAVERSAL | wxSTAY_ON_TOP
		wxFrame.__init__(self, parent, -1, _("Pregnancy Calculator"), style=myStyle)

		# initialization of variables used in the control & calculation
		self.lnp_or_usdate=0	# controls which variable (LNP or Ultrasound) a calendar event changes
					# (if == 0): {calendar selection modifies LNP}
					# (if == 1): {calendar selection modifies Ultrasound Date}

		self.ustxt=wxDateTime_Today()	# avoids problem - one would have if the user clicked on
						# ultrasound date
						# BONUS: makes the preg. calculator useful for EDC calcs given
						# 	a date and the gestation time

		icon = wxEmptyIcon()
		icon.CopyFromBitmap(wxBitmapFromXPMData(cPickle.loads(zlib.decompress( _icons[_("""icon_Preg_calc""")] ))) )
		self.SetIcon(icon)

		rcs = RowColSizer()

		#------------------------------
		# sizer holding the 'LNMP' stuff
		#------------------------------
		label = wxStaticText(self,-1,_("LMP"),size = (50,20))	#label Lmp
		label.SetFont(wxFont(12,wxSWISS,wxNORMAL,wxNORMAL,false,''))
		label.SetForegroundColour(wxColour(0,0,0))

		self.txtlnmp = wxTextCtrl(self,-1,"",size=(100,20))  	# text for lmp
		self.txtlnmp.SetFont(wxFont(12,wxSWISS,wxNORMAL,wxNORMAL,false,''))
		self.txtlnmp.SetToolTip(wxToolTip(_("Click on calendar to enter the last menstrual period date")))
		tiplmp=self.txtlnmp.GetToolTip()

		szr_row1 = wxBoxSizer(wxHORIZONTAL)
		szr_row1.Add(self.txtlnmp,1,wxEXPAND|wxALL,2)
		EVT_SET_FOCUS(self.txtlnmp, self.OnSetFocus_lnmp)

		szr_lnmp = wxBoxSizer(wxHORIZONTAL)
		szr_lnmp.Add(label, 1, 0, 0)
		szr_lnmp.Add(10,1,0,0)
		rcs.Add(szr_lnmp, flag=wxEXPAND, row=0, col=1)
		rcs.Add(szr_row1, flag=wxEXPAND, row=0, col=2, colspan=5)
		#------------------------------
		# sizer holding the 'Gest.' stuff
		#------------------------------
		label = wxStaticText(self,-1,_("Gest."),size = (50,20))
		label.SetFont(wxFont(12,wxSWISS,wxNORMAL,wxNORMAL,false,''))
		label.SetForegroundColour(wxColour(0,0,0))

		self.txtgest = wxTextCtrl(self,-1,"",size=(100,20))
		self.txtgest.Enable(false)
		self.txtgest.SetFont(wxFont(12,wxSWISS,wxNORMAL,wxNORMAL,false,''))
		self.txtgest_szr  = wxBoxSizer(wxHORIZONTAL)
		self.txtgest_szr.Add(self.txtgest,1,wxEXPAND|wxALL,2)

		szr_gest = wxBoxSizer(wxHORIZONTAL)
		szr_gest.Add(label, 1, 0, 0)
		szr_gest.Add(10,1,0,0)
		rcs.Add(szr_gest, flag=wxEXPAND, row=1, col=1)
		rcs.Add(self.txtgest_szr, flag=wxEXPAND, row=1, col=2, colspan=5)

		#------------------------------
		# sizer holding the 'EDC' stuff
		#------------------------------
		label = wxStaticText(self,-1,_("EDC"),size = (50,20))
		label.SetFont(wxFont(13,wxSWISS,wxNORMAL,wxNORMAL,false,''))
		label.SetForegroundColour(wxColour(0,0,0))

  		self.txtedc = wxTextCtrl(self,-1,"",size=(100,20))
		self.txtedc.Enable(false)
		self.txtedc.SetFont(wxFont(13,wxSWISS,wxNORMAL,wxNORMAL,false,''))
		szr_txtedc = wxBoxSizer(wxHORIZONTAL)
		szr_txtedc.Add(self.txtedc,1,wxEXPAND|wxALL,2)
		szr_edc = wxBoxSizer(wxHORIZONTAL)
		szr_edc.Add(label,1,0,0)
		szr_edc.Add(10,1,0,0)
		rcs.Add(szr_edc, flag=wxEXPAND, row=2, col=1)
		rcs.Add(szr_txtedc, flag=wxEXPAND, row=2, col=2, colspan=5)

		#------------------------------
		# "Ultrasound Scan" label
		#------------------------------
		us_label = wxStaticText(self,-1,_("18 Week Ultrasound Scan"),size = (20,20))
		us_label.SetFont(wxFont(12,wxSWISS,wxNORMAL,wxBOLD,false,''))
		us_label.SetForegroundColour(wxColour(50,50,204))
		szr_backgrnd_18WkScanDue = wxBoxSizer(wxVERTICAL)
		szr_backgrnd_18WkScanDue.Add(1,3, 0)
		szr_backgrnd_18WkScanDue.Add(us_label,1,wxEXPAND,1)
		rcs.Add(szr_backgrnd_18WkScanDue, flag=wxALIGN_CENTRE_HORIZONTAL, row=3, col=2, colspan=5)
		#------------------------------
		# sizer holding the 'Due' stuff
		#------------------------------
		label = wxStaticText(self,-1,_("Due"),size = (100,20))
		label.SetFont(wxFont(13,wxSWISS,wxNORMAL,wxNORMAL,false,''))
		label.SetForegroundColour(wxColour(0,0,0))

  		self.txtdue = wxTextCtrl(self,-1,"",size=(100,20))
		self.txtdue.Enable(false)
		self.txtdue.SetFont(wxFont(13,wxSWISS,wxNORMAL,wxNORMAL,false,''))
		self.szr_txtdue  = wxBoxSizer(wxHORIZONTAL)
		self.szr_txtdue.Add(self.txtdue,1,wxEXPAND|wxALL,2)
		szr_due = wxBoxSizer(wxHORIZONTAL)
		szr_due.Add(label,1,0,0)
		szr_due.Add(10,1,0,0)
		rcs.Add(szr_due, flag=wxEXPAND, row=4, col=1)
		rcs.Add(self.szr_txtdue, flag=wxEXPAND, row=4, col=2, colspan=5)

		#------------------------------
		# "Ultrasound Scan - Revised EDC" label
		#------------------------------
		rev_edc_label = wxStaticText(self,-1,_("Ultrasound Scan - Revised EDC"),size = (100,20))
		rev_edc_label.SetFont(wxFont(12,wxSWISS,wxNORMAL,wxBOLD,false,''))
		rev_edc_label.SetForegroundColour(wxColour(50,50,204))
		szr_backgrnd_RevEDCLabel = wxBoxSizer(wxVERTICAL)
		szr_backgrnd_RevEDCLabel.Add(1,3, 0)
		szr_backgrnd_RevEDCLabel.Add(rev_edc_label,1,wxEXPAND,1)
		rcs.Add(szr_backgrnd_RevEDCLabel, flag=wxALIGN_CENTRE_HORIZONTAL, row=5, col=2, colspan=5)

		#------------------------------
		# sizer holding the 'newedc' stuff
		#------------------------------
		label1 = wxStaticText(self,-1,_("Date"),size = (25,20))
		label1.SetFont(wxFont(13,wxSWISS,wxNORMAL,wxNORMAL,false,''))
		label1.SetForegroundColour(wxColour(0,0,0))
  		self.txtdate = wxTextCtrl(self,-1,"",size=(25,20))
		self.txtdate.SetFont(wxFont(13,wxSWISS,wxNORMAL,wxNORMAL,false,''))
		self.txtdate.SetToolTip(wxToolTip(_("Click on this field and then the ultrasound scan date on the calendar")))
		tipdue=self.txtdate.GetToolTip()
		wxToolTip_Enable(1)
		self.szr_txtdate  = wxBoxSizer(wxHORIZONTAL)
		self.szr_txtdate.Add(self.txtdate,1,wxEXPAND|wxALL,2)
		EVT_SET_FOCUS(self.txtdate, self.OnSetFocus_USDate)

		szr_label1 = wxBoxSizer(wxHORIZONTAL)
		szr_label1.Add(label1,1,0,0)
		szr_label1.Add(10,1,0,0)
		rcs.Add(szr_label1, flag=wxEXPAND, row=6, col=1)
		rcs.Add(self.szr_txtdate, flag=wxEXPAND, row=6, col=2, colspan=5)

		#------------------------------

		label2 = wxStaticText(self,-1,_("Weeks"),size = (25,20))
		label2.SetFont(wxFont(13,wxSWISS,wxNORMAL,wxNORMAL,false,''))
		label2.SetForegroundColour(wxColour(0,0,0))
		self.txtweeks = wxSpinCtrl (self, -1, value = "0", min = 0, max = 42)
		EVT_SPINCTRL (self.txtweeks ,self.txtweeks.GetId(), self.EvtText_calcnewedc)
		self.txtweeks.SetFont(wxFont(13,wxSWISS,wxNORMAL,wxNORMAL,false,''))
		self.szr_txtweeks  = wxBoxSizer(wxHORIZONTAL)
		self.szr_txtweeks.Add(self.txtweeks,1,wxEXPAND|wxALL,2)

		label3 = wxStaticText(self,-1,_("Days"),size = (25,20))
		label3.SetFont(wxFont(13,wxSWISS,wxNORMAL,wxNORMAL,false,''))
		label3.SetForegroundColour(wxColour(0,0,0))
		self.txtdays = wxSpinCtrl (self, -1, value = "0", min = 0, max = 6)
		EVT_SPINCTRL (self.txtdays ,self.txtdays.GetId(), self.EvtText_calcnewedc)
		self.txtdays.SetFont(wxFont(13,wxSWISS,wxNORMAL,wxNORMAL,false,''))
		self.szr_txtdays  = wxBoxSizer(wxHORIZONTAL)
		self.szr_txtdays.Add(self.txtdays,1,wxEXPAND|wxALL,2)

		szr_label2 = wxBoxSizer(wxHORIZONTAL)
		szr_label2.Add(label2,1,wxALIGN_CENTRE_VERTICAL,0)
		szr_label2.Add(10,1,0,0)
		szr_label3 = wxBoxSizer(wxHORIZONTAL)
		szr_label3.Add(10,1,0,0)
		szr_label3.Add(label3,1,wxALIGN_CENTRE_VERTICAL,0)
		szr_label3.Add(10,1,0,0)
		rcs.Add(szr_label2, flag=wxEXPAND, row=7, col=1)
		rcs.Add(self.szr_txtweeks, flag=wxEXPAND, row=7, col=2, colspan=2)
		rcs.Add(szr_label3, flag=wxEXPAND, row=7, col=4)
		rcs.Add(self.szr_txtdays, flag=wxEXPAND, row=7, col=5, colspan=2)

		#------------------------------
		# sizer holding the new (or revised) 'EDC' stuff
		#------------------------------
		label = wxStaticText(self,-1,_("EDC"),size = (100,20))
		label.SetFont(wxFont(13,wxSWISS,wxNORMAL,wxNORMAL,false,''))
		label.SetForegroundColour(wxColour(0,0,0))

  		self.txtnewedc = wxTextCtrl(self,-1,"",size=(100,20))
		self.txtnewedc.Enable(false)
		self.txtnewedc.SetFont(wxFont(13,wxSWISS,wxNORMAL,wxNORMAL,false,''))
		self.szr_txtnewedc  = wxBoxSizer(wxHORIZONTAL)
		self.szr_txtnewedc.Add(self.txtnewedc,1,wxEXPAND|wxALL,2)
		szr_label=wxBoxSizer(wxHORIZONTAL)
		szr_label.Add(label,1,0,0)
		szr_label.Add(10,1,0,0)
		rcs.Add(szr_label, flag=wxEXPAND, row=8, col=1)
		rcs.Add(self.szr_txtnewedc, flag=wxEXPAND, row=8, col=2, colspan=5)
		self.btnPrint = wxButton(self,1011,_('&Print'))
		self.btnSave = wxButton(self,1011,_('&Save'))
		szr_buttons = wxBoxSizer(wxHORIZONTAL)
		szr_buttons.Add(self.btnPrint,0,wxEXPAND)
		szr_buttons.Add(self.btnSave,0,wxEXPAND)
		rcs.Add(szr_buttons, flag=wxEXPAND,row=9, col=3, colspan=4)
		#------------------------------
		# Sizer holding stuff on the right
		#------------------------------
		szr_main_rt = wxBoxSizer(wxVERTICAL)
		szr_main_rt.Add(rcs)
		EVT_BUTTON(self,1010,self.EvtReset)
		EVT_BUTTON(self,1011,self.EvtPrint)
		EVT_BUTTON(self,1012,self.EvtSave)
		#------------------------------
		# Add calendar (stuff on the left)
		#------------------------------
		self.LNMPcal = wxCalendarCtrl (self, ID_LNMP,style = wxRAISED_BORDER)
		EVT_CALENDAR_SEL_CHANGED(self.LNMPcal, ID_LNMP, self.OnCalcByLNMP)

		szr_main_lf = wxBoxSizer(wxVERTICAL)
		szr_main_lf.Add(self.LNMPcal,0,wxALIGN_CENTRE_HORIZONTAL)
		btn_reset = wxButton(self, 1010, _('&Reset'))
		#szr_main_lf.Add(5,0,5)
		szr_main_lf.Add(btn_reset,0,wxEXPAND)

		#--------------------------------------
		# Super-sizer holds all the stuff above
		#--------------------------------------
		szr_main_top= wxBoxSizer(wxHORIZONTAL)
		szr_main_top.Add(szr_main_lf,0,0)
		szr_main_top.Add(15,0,0,0)
		szr_main_top.Add(szr_main_rt,0,0)
		#szr_main_top.Add(15,1,0,0)

		#------------------------------
		# Put everything together in one big sizer
		#------------------------------
		szr_main= wxBoxSizer(wxHORIZONTAL)
		szr_main.Add(szr_main_top,1,wxEXPAND|wxALL,10)
		self.SetSizer (szr_main)
		self.SetAutoLayout (1)
		szr_main.Fit (self)

		EVT_CLOSE (self, self.OnClose )
		self.Show(1)

	#-----------------------------------------
	def OnCalcByLNMP (self, event):

		if(self.lnp_or_usdate==0):
			# we do this the "UNIX Way" -- all dates are converted into seconds
			# since midnight 1 Jan, 1970.
			# .GetDate().GetTicks() returns time at 5AM.  The -18000 second
			#	correction adjusts LNMP to 12AM ??? NOT NEEDED
			#	is it possible there is a BUG in the wxPython
			#	Day Light Savings/Standard Time Calc?

			#LNMP = self.LNMPcal.GetDate ().GetTicks () - 18000 	# Standard Time Fix (?)
			self.LNMP = self.LNMPcal.GetDate ().GetTicks ()		# Correct for Day Light Saving Time
			today = wxDateTime_Today().GetTicks()
			due = self.LNMP + GESTATION
			gest = today - self.LNMP
			self.ultrasound18_52 = self.LNMP + US18_52

			# -----------------
			LNMPtxt = wxDateTime()			# FIXME? - change format of date (?)
			LNMPtxt.SetTimeT(self.LNMP)
			self.txtlnmp.SetValue(self.PurgeTime(LNMPtxt))

			# -----------------
			gest_week = gest / WEEK
			gest_day = (gest % WEEK) / DAY
			if(gest_day==1):
				days_label=_('day')
			else:
				days_label=_('days')
			if(gest_week==1):
				weeks_label=_('week')
			else:
				weeks_label=_('weeks')
			txtgest_str=str(gest_week)+" "+weeks_label+", "+str(gest_day)+" "+days_label
			self.txtgest.SetValue(txtgest_str)

			# -----------------
			edctxt = wxDateTime()
			edctxt.SetTimeT(due)
			self.txtedc.SetValue(self.PurgeTime(edctxt))

			# -----------------
			self.ustxt = wxDateTime()
			self.ustxt.SetTimeT(self.ultrasound18_52)
			self.txtdue.SetValue(self.PurgeTime(self.ustxt))

		else:
			# set Ultrasound Date
			self.usdate = self.LNMPcal.GetDate ().GetTicks ()
			usdatetxt = wxDateTime()	# FIXME? - change format of date
			usdatetxt.SetTimeT(self.usdate)
			self.txtdate.SetValue(self.PurgeTime(usdatetxt))

	#-----------------------------------------
	def EvtText_calcnewedc (self, event):
		try:
			weeks=self.txtweeks.GetValue()
			days=self.txtdays.GetValue()

			# get date of ultrasound
			newedc=self.usdate+GESTATION-WEEK*weeks-DAY*days

			wxD=wxDateTime()
			wxD.SetTimeT(newedc)
			self.txtnewedc.SetValue(self.PurgeTime(wxD))
		except:
			pass	# error handling - FIXME is 'try' statement necessary (?)

	#-----------------------------------------
	def EvtReset(self, event):
		# reset variables
		self.txtlnmp.SetValue("")
		self.txtgest.SetValue("")
		self.txtedc.SetValue("")
		self.txtdue.SetValue("")

		self.txtdate.SetValue("")
		self.ustxt=wxDateTime_Today()

		self.txtweeks.SetValue(0)			# FIXME - MAKE IT RESET TO BLANK?
		self.txtdays.SetValue(0)
		self.txtnewedc.SetValue("")

		self.lnp_or_usdate=0
		self.LNMPcal.SetDate(wxDateTime_Today())	# reset Calendar to current date

	#-----------------------------------------
	def EvtPrint(self, event):
		pass 					# TODO
	#-----------------------------------------
	def EvtSave(self, event):
		pass 					# TODO
	#-----------------------------------------
	#def EvtHandout(self, event):
	#	pass 					# TODO
	#-------------------------------------------
	def OnClose (self, event):
		self.Destroy ()

	#-------------------------------------------
	def PurgeTime(self, date):			# a not so elegant way of removing the time
		time_loc=string.find(str(date),":00:00")
		date_str=str(date)
		return date_str[:(time_loc-3)]

	#-------------------------------------------
	def OnSetFocus_lnmp (self, event):
		self.lnp_or_usdate=0
		event.Skip()				# required so wxTextCtrl box is selected

	#-------------------------------------------
	def OnSetFocus_USDate (self, event):
		self.LNMPcal.SetDate(self.ustxt)	# flip calendar to 18/52 date
		self.lnp_or_usdate=1
		event.Skip()



#====================================================================
# Main
#====================================================================
if __name__ == '__main__':
	# set up dummy app
	class TestApp (wxApp):
		def OnInit (self):
			frame = PregnancyFrame(None)
			frame.Show(1)
			return 1
	#---------------------
	import gettext
	_ = gettext.gettext
	gettext.textdomain ('gnumed')
	app = TestApp ()
	app.MainLoop ()
else:
	# plugin()ize
	import gmPlugin

	ID_PregCalc_BUTTON = wxNewId()

	class gmPregCalc (gmPlugin.wxBasePlugin):
		def name (self):
			return 'Pregnancy Calculator'
		#---------------------
		def register (self):
			menu = self.gb['main.toolsmenu']
			menu.Append (ID_MENU, _("Preg. Calc"), _("Pregnancy Calculator"))
			EVT_MENU (self.gb['main.frame'], ID_MENU, self.OnTool)
			self.tb = self.gb['main.toolbar']
			self.tool = wxToolBar (self.tb, -1, style=wxTB_HORIZONTAL|wxNO_BORDER|wxTB_FLAT)
			self.tool.AddTool(
				ID_PregCalc_BUTTON,
				wxBitmapFromXPMData(cPickle.loads(zlib.decompress( _icons[_("""icon_Preg_calc""")] ))),
				shortHelpString = _("Pregnancy Calculator")
			)
			self.tb.AddWidgetRightBottom (self.tool)
			EVT_TOOL (self.tool, ID_PregCalc_BUTTON, self.OnTool)
		#---------------------
		def unregister (self):
			menu = self.gb['main.toolsmenu']
			menu.Delete (ID_MENU)
		#---------------------
		def OnTool (self, event):
			frame = PregnancyFrame (self.gb['main.frame'])
			frame.Centre(wxBOTH)
			frame.Show (1)

#=====================================================================
# $Log: gmPregCalc.py,v $
# Revision 1.1  2003-07-07 02:59:57  michaelb
# a new preg calc (obsoletes "gmCalcPreg.py"), developed in test-area/michaelb/, spelling fix in LMP wxToolTip
#
# Revision 1.8  2003/07/06 23:14:35  rterry
# 18/52 changed to 18 Week as per list suggestion
#
# Revision 1.7  2003/07/06 21:36:30  michaelb
# fixed ultrasound scan date bug, added tooltips to 'LMP' and 'Date' fields
#
# Revision 1.5  2003/07/05 06:44:28  michaelb
# fixed "Revised EDC" calc, on reset LMP selected & calendar put on current date
#
# Revision 1.4  2003/07/05 06:14:41  michaelb
# calculation fully functional!
#
# Revision 1.2  2003/07/04 06:56:32  rterry
# richards latest gui improvement to pregcalc
#
# Revision 1.1  2003/07/01 06:35:09  michaelb
# a new pregnancy calc
#

