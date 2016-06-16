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
import os.path
from language import Language

class Python(Language):
	extensions = ['.py', '.pyw']
	
	def __init__(self, verbose, log):
		Language.__init__(self, verbose, log)
		
	def CanRead(self, filename):
		readable = (1 == Python.extensions.count(os.path.splitext(filename)[1]))
		if self.verbose and not readable:
			self.log.write("Cannot read %s\n" % filename)
		return readable
		
	def ReadFile(self, filename, paths):
		items = []
		for line in open(filename):
			bits = line.split()
			if len(bits) == 0:
				continue
			if 'from' == bits[0]:
				items.append(bits[1])
			elif 'import' == bits[0]:
				items.extend(line[6:].split(','))
			else:
				continue
		files = []
		missing = []
		for item in items:
			item = item.split('as')[0].strip()
			found = None
			for ext in Python.extensions:
				line = item + ext
				found = self.Search(os.path.split(filename)[0], paths, line)
				if found != None:
					break
			if found != None:
				files.append(found)
			elif self.verbose:
				self.log.write("Cannot find %s from %s\n" % (item, filename))
				missing.append(line)
		return files, missing
		
	def FileExtensions(self):
		return Python.extensions
		
	def WriteToDoxygenFile(self, fp, lines):
		for line in lines.split('\n'):
			fp.write("## %s\n" % line)

	def WriteVerbatimToDoxygenFile(self, fp, lines):
		for line in lines.split('\n'):
			fp.write("## %s\n" % line)

def Factory(verbose, log):
	return Python(verbose, log)