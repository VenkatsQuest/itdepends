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
import os.path, sys

class Filtered:
	def __init__(self, filters):
		self.filters = filters
	
	def Filter(self, fullpath):
		fullpath = fullpath.replace('\\', '/')
		if fullpath in self.filters:
			return self.filters[fullpath]
			
		path = ''
		i = fullpath.rfind('/')
		if i != -1:
			path = fullpath[:i+1]
		path += '*'
		if path in self.filters:
			return self.filters[path]
		return path[:-2]
	