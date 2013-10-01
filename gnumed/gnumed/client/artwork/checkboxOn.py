# -*- coding: utf-8 -*-
#----------------------------------------------------------------------
# This file was generated by /usr/local/bin/img2py
#
try:
	import wxversion
	import wx
except ImportError:
	from wxPython import wx
	#from wxPython.wx import wxImageFromStream, wxBitmapFromImage

import cStringIO, zlib


def getCheckboxOn():
    return zlib.decompress(
"x\xda\x01D\x01\xbb\xfe\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\r\x00\
\x00\x00\r\x08\x06\x00\x00\x00r\xeb\xe4|\x00\x00\x00\x04sBIT\x08\x08\x08\x08\
|\x08d\x88\x00\x00\x00\xfbIDATx\x9c\x9d\x921\x8a\x83P\x10\x86\xbf,\xe9\xec$`\
'Xx\x02\xc1\x03$bc\xf3\x0e`oi!D\xbbW[\xbc&\xa4\x14/`\xe7\x01l<\x80\x8d\xfd+\
\x03\xe2\tl\xb2\xc5\xb2\x82$\x1bd\xa7\x9b\x9f\xf9f\xfe\x19\xe6\xd0u\xddSk\
\xcd\xdep\x1c\x87\xa3\xd6\x9a\xcb\xe5\xb2\x0bX\x96\x85\xbe\xef9\xfe\n\xa7\
\xd3\xe9#\xf0x<p]\x97\xbe\xef\xf9\xda3A)E\x92$k~\xfcP\x0b\x80\x94\x92a\x18\
\x90R\xee\x83\xa4\x94(\xa5h\xdb\x16\xcf\xf3V}c\xaf(\n\xaa\xaa\x02`\x1cG\x94R\
dY\xc6\xf9|\xde4['\x95e\xc9\xfd~\x07~\x8eR\xd75\xb6m\x13E\xd1\x8b\x83\x15\
\xca\xf3\x9ci\x9ah\x9a\x868\x8e\x01\x08\x82\x00\xdf\xf7_\xa0\x8d\xbd\xeb\xf5\
\xca\xedv\xc34M\x00\xc20|\xbb\xeb\xe6\x10\x96e!\x84`\x9eg\xda\xb6E\x08\xf17\
\xb4,\x0b\x86a\xacb\x9a\xa6\xa4i\xfa\x16\x008\xfc\xe7\xf7\xbe\x01\x92\xe9R\
\x8b&]\x902\x00\x00\x00\x00IEND\xaeB`\x82\xd6/\x8b\x02" )

def getCheckboxOnBitmap():
    return wxBitmapFromImage(getImage())

def getImage():
    stream = cStringIO.StringIO(getCheckboxOn())
    return wxImageFromStream(stream)

