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

class Cpp(Language):
	extensions = ['.c', '.cpp', '.cxx', '.h', '.hpp', '.hxx', '.S', '.ipp']
	
	def __init__(self, encoding, substitutions, verbose, log):
		Language.__init__(self, encoding, substitutions, verbose, log)
		
	def CanRead(self, filename):
		readable = (1 == Cpp.extensions.count(os.path.splitext(filename)[1]))
		if self.verbose and not readable:
			self.log.write("Cannot read %s\n" % filename)
		return readable
		
	def ReadFile(self, filename, paths):
		files = []
		missing = []
		for line in open(filename, encoding=self.encoding):
			line = line.strip()
			for key in self.substitutions:
				line = line.replace(key, self.substitutions[key])
			if line[:8] != '#include':
				continue
			line = line[8:].strip()
			if line[0] == '"':
				line = line[1:]
				line = line[:line.find('"')]
			elif line[0] == '<':
				line = line[1:]
				line = line[:line.find('>')]
			
			found = self.Search(os.path.split(filename)[0], paths, line)
			if found != None:
				files.append(found)
			else:
				missing.append(line)
				if self.verbose:
					self.log.write("Cannot find %s from %s\n" % (item, filename))
		return files, missing
		
	def FileExtensions(self):
		return Cpp.extensions
		
	def WriteToDoxygenFile(self, fp, lines):
		for line in lines.split('\n'):
			fp.write("/// %s\n" % line)

	def WriteVerbatimToDoxygenFile(self, fp, lines):
		for line in lines.split('\n'):
			fp.write("%s\n" % line)

def Factory(encoding, substitutions, verbose, log):
	return Cpp(encoding, substitutions, verbose, log)