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

class Cs(Language):
	extensions = ['.cs']
	
	def __init__(self, encoding, substitutions, verbose, log):
		Language.__init__(self, encoding, substitutions, verbose, log)
		
	def FileExtensions(self):
		return Cs.extensions
		
	def WriteToDoxygenFile(self, fp, lines):
		for line in lines.split('\n'):
			fp.write("/// %s\n" % line)

	def WriteVerbatimToDoxygenFile(self, fp, lines):
		for line in lines.split('\n'):
			fp.write("%s\n" % line)

def Factory(encoding, substitutions, verbose, log):
	return Cs(encoding, substitutions, verbose, log)