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
from utilities import Default
from readtext import ReadKeyValue

class Language:
	def __init__(self, encoding, substitutions, verbose, log):
		self.encoding = encoding
		self.substitutions = substitutions
		self.verbose = verbose
		self.log = log
		
	def CanRead(self, filename):
		return False
		
	def AddFile(self, local, leaves):
		if local in leaves:
			return leaves[local]
		elif self.verbose:
			self.log.write("No leaf found for %s\n" % local)
		return None

	def Search(self, direc, paths, filename):
		allpaths = [direc]
		allpaths.extend(paths)
		for path in allpaths:
			fullpath = os.path.normpath(os.path.join(path, filename))
			if os.path.exists(fullpath):
				return fullpath
		return None

	def ReadFile(self, filename, paths):
		return [], []
		
def Factory(state, args, log):
	"""Create an object to hold the language
  Arguments:
    language:
      name of the language
    encoding:
      the encoding of any source files
      default is utf-8
    substitutions:
      a key-value pair file mapping from one source 
      default is no substitutions file
    verbose:
      whether to print warnings
    store:
      name to store the object in"""
	module = __import__(args["language"])
	method = getattr(module, "Factory")
	encoding = Default(args, "encoding", "utf-8")
	
	substitutions = {}
	if Default(args, "substitutions", "") != "":
		substitutions = ReadKeyValue(args["substitutions"], {})
	
	state[args["store"]] = method(encoding, substitutions, args["verbose"], log)

def Methods():
	return [Factory, ]