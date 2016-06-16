#!/usr/bin/env python
#
# Copyright 2016 Zebedee Mason
#
#  The author's copyright is expressed through the following notice, thus
#  giving effective rights to copy and use this software to anyone, as shown
#  in the license text.
#
# NOTICE:
#  This software is released under the terms of the GNU Lesser General Public
#  license; a copy of the text has been released with this package (see file
#  LICENSE, where the license text also appears), and can be found on the
#  GNU web site, at the following address:
#
#           http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html
#
#  Please refer to the license text for any license information. This notice
#  has to be considered part of the license, and should be kept on every copy
#  integral or modified, of the source files. The removal of the reference to
#  the license will be considered an infringement of the license itself.
import sys, os, os.path, json

def Plugins(direc):
	print("""
usage: %s [-h|--help] filename
       where filename is the name of a json file containing a list of commands
       of the form {"plugin":plugin, "method":method, "args":{}}

Plugins
=======
"""[1:-1] % os.path.split(sys.argv[0])[1])
	for filename in os.listdir(direc):
		filename = os.path.splitext(filename)
		if filename[1] != '.py':
			continue
		try:
			module = __import__(filename[0])
			print("%s:" % filename[0])
			if hasattr(module, "Methods"):
				methods = getattr(module, "Methods")
				for method in methods():
					print("  %s:" % method.__name__)
					for line in method.__doc__.split('\n'):
						print("    %s" % line)
		except:
			continue

def Execute(direc):
	if len(sys.argv) == 1:
		sys.argv.append("-h")
		
	if 1 == ["-h", "--help"].count(sys.argv[1]):
		Plugins(direc)
		exit(0)

	state = {}
	for command in json.load(open(sys.argv[1])):
		module = __import__(command["plugin"])
		method = getattr(module, command["method"])
		method(state, command["args"], sys.stdout)
		
if __name__ == "__main__":
	direc = os.path.split(sys.argv[0])[0]
	sys.path.insert(0, os.path.join(direc, "Common"))
	direc = os.path.join(direc, "Plugins")
	sys.path.insert(0, direc)
	for sub in os.listdir(direc):
		d = os.path.join(direc, sub)
		if os.path.isdir(d):
			sys.path.insert(0, d)
	
	Execute(direc)