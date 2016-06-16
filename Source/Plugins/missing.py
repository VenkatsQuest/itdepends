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
from dependencies import Leaf
from utilities import Default
from readtext import ReadText, ReadKeyValue

def Remove(state, args, log):
	"""Remove the missing dependencies that match those read from a file
  Arguments:
    dependencies:
      name that the dependencies object is stored under
    environment:
      file containing the environment variables used in filters and paths
      default is no environment file
    input:
      filename to read the list of dependencies to eliminate"""
	
	environment = {}
	if Default(args, "environment", "") != "":
		environment = ReadKeyValue(args["environment"], {})
		
	paths = ReadText(args["input"], environment)
	  
	dependencies = state[args["dependencies"]]
	
	for key in dependencies.leaves.keys():
		leaf = dependencies.leaves[key]
		for i in range(len(leaf.missing)-1, -1, -1):
			miss = leaf.missing[i]
			if 1 == paths.count(miss):
				leaf.missing.remove(miss)

def Methods():
	return [Remove]