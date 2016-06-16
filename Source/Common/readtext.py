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
def ReadText(filename, environment):
	lines = []
	for line in open(filename):
		for key in environment.keys():
			line = line.replace(key, environment[key])
		lines.append(line.strip())
	return lines
	
def ReadKeyValue(filename, environment):
	mapping = {}
	for line in ReadText(filename, environment):
		bits = line.split()
		if len(bits) != 2:
			continue
		mapping[bits[0]] = bits[1]
	return mapping
