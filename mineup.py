#!/usr/bin/env python
# encoding: utf-8
"""
mineup.py

Created by Marcus Schütte on 2012-10-26.
Copyright (c) 2012 __SL__. All rights reserved.
"""

import sys
import os
import uuid
import psycopg2
import psycopg2.extras
import datetime

import ConfigParser
from optparse import OptionParser


valid_date = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")

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




#
##############
#Funktionen
##############
#
#
#

def checkSeed(seed):
	pass

def initialize(config, dbcur):
	dbcur.execute("DROP TABLE IF EXISTS mineup_backups;")
	dbcur.execute("DROP TABLE IF EXISTS mineup_seed_name;")
	
	dbcur.execute("CREATE TABLE mineup_backups(id varchar(36), folder varchar(100), seed varchar(30), time varchar(30));")
	dbcur.execute("CREATE TABLE mineup_seed_name(id varchar(36), seed varchar(30), worldname varchar(50));")
	
	backup_list = os.listdir(config.backup_folder)
	
	for backup in backup_list:
		if(os.isdir(backup)):
			leveldat_path = os.path.join(config.backup_folder, backup, "world/level.dat")
			level = NBTFile(leveldat_path)
			
			id = uuid.uuid4();
			seed = level["Data"]["RandomSeed"]
			
			if(os.path.exists(os.path.join(config.backup_folder, backup, "backuptime"))):
				timestamp = open(os.path.join(config.backup_folder, backup, "backuptime"))
				time = timestamp.read()
			else:
				if(valid_date.match(backup)):
					time = backup
					timestamp = open(os.path.join(config.backup_folder, backup, "backuptime"))
					timestamp.write(backup)
					#timestamp erstellen
			dbcur.execute("INSERT INTO mineup_backups(id, folder, seed, time)")
	
def backup(config, dbcur):
	time = datetime.time()
	os.system("cp -r " + config.get("general", "world_folder") + " " + os.path.join(config.get("general", "backup_folder"), time.strftime("%Y-%m-%d %H-%M-%S"))
	
	


	
#
######################
#Parameter Parser
######################
#
#
opt = OptionParser("mineup.py [options]")
opt.add_option("-i", "--init", action="store_true", dest="initialize", default=False, help="initialize database")
opt.add_option("-c", "--configure", action="store_true", dest="configure", default=False, help="configure mineup")
opt.add_option("-b", "--backup", action="store_true", dest="backup", default=False, help="backup world folder")
opt.add_option("-r", "--cleanup", action="store_true", dest="cleanup", default=False, help="cleanup unneeded backups")
opt.add_option("-H", "--hardlinks", action="store_true", dest="hardlinks", default=False, help="set hardlinks for unchanged files")
opt.add_option("-n", "--name", action="store_true", dest="name", default=False, help="set seed alias")
opt.add_option("-d", "--delete", action="store_true", dest="delete", default=False, help="delete all backups of a seed")
opt.add_option("-m", "--rename", action="store_true", dest="rename", default=False, help="rename seed alias")
opt.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="start in verbose mode")

(param, args) = opt.parse_args()

#Config Parser
config = ConfigParser.RawConfigParser()
config.read('config.ini')



dbconn = psycopg2.connect("dbname="+config.get("database", "dbname")+" user=" + config.get("database", "user") + " host=" + config.get("database", "host") + " password=" + config.get("database", "password"))
dbcur = dbconn.cursor(cursor_factory=psycopg2.extras.DictCursor)


if param.configure:
	print "Configure!"
	
if param.initialize:
	initialize(config, dbcur)
if param.backup:
	print "Backup!"
if param.cleanup:
	print "Cleanup!"
if param.hardlinks:
	print "Hardlinks!"
if param.name:
	print "Name!"
if param.delete:
	print "Delete!"
if param.rename:
	print "Rename!"
if param.verbose:
	print "verbose!"

