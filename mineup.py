#!/usr/bin/env python
# encoding: utf-8
"""
mineup.py

Created by Marcus Schütte on 2012-10-26.
Copyright (c) 2012 __SL__. All rights reserved.
"""

import sys
import os
from optparse import OptionParser

# local module
try:
	import nbt
except ImportError:
	# nbt not in search path. Let's see if it can be found in the parent folder
	extrasearchpath = os.path.realpath(os.path.join(__file__,os.pardir,os.pardir))
	if not os.path.exists(os.path.join(extrasearchpath,'nbt')):
		raise
	sys.path.append(extrasearchpath)
from nbt.nbt import NBTFile

def checkSeed(seed):
	pass


opt = OptionParser("mineup.py [options]")
opt.add_option("-i", "--init", action="store_true", dest="initialize", default=False, help="initialize backup folder")
opt.add_option("-c", "--configure", action="store_true", dest="configure", default=False, help="configure mineup")
opt.add_option("-b", "--backup", action="store_true", dest="backup", default=False, help="backup world folder")
opt.add_option("-r", "--cleanup", action="store_true", dest="cleanup", default=False, help="cleanup unneeded backups")
opt.add_option("-n", "--name", action="store_true", dest="name", default=False, help="set seed alias")
opt.add_option("-d", "--delete", action="store_true", dest="delete", default=False, help="delete all backups of a seed")
opt.add_option("-m", "--rename", action="store_true", dest="rename", default=False, help="rename seed alias")
opt.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="start in verbose mode")

(param, args) = opt.parse_args()

if param.configure:
	print "Configure!"
	
if param.initialize:
	print "Initialize!"
if param.backup:
	print "Backup!"
if param.cleanup:
	print "Cleanup!"
if param.name:
	print "Name!"
if param.delete:
	print "Delete!"
if param.rename:
	print "Rename!"
if param.verbose:
	print "verbose!"

