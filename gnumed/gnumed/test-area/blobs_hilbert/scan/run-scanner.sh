#!/bin/sh

# $Source: /home/ncq/Projekte/cvs2git/vcs-mirror/gnumed/gnumed/test-area/blobs_hilbert/scan/Attic/run-scanner.sh,v $
# $Revision: 1.1 $

# this is a wrapper for the indexer
# set your command line arguments etc. here

# if you want another language than the standard system one
#LANG = "de_DE@euro"

# if you need to set a special base directory for some reason
#SCAN-MED_DOCS_DIR = ""

python ./scan-med_docs.py --conf-file=/home/ncq/.gnumed/gnumed-archiv.conf --text-domain=gnumed-archiv
