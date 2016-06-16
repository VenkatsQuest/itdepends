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
from dependencies import Leaf
from language import Language
from utilities import Default
from readtext import ReadText, ReadKeyValue
from filtered import Filtered

class Generic:
	def __init__(self, dependencies, filters, paths):
		self.dependencies = dependencies
		self.filters = filters
		self.paths = paths
	
	def ReadProject(self, direc, reader):
		for root, dirs, files in os.walk(direc):
			for  name in files:
				filename = os.path.join(root, name)
				if not reader.CanRead(filename):
					continue
				filter = self.filters.Filter(os.path.join(root[len(direc)+1:], name))
				
				branch = self.dependencies.GetPath(filter)
				leaf = Leaf(name, branch)
				branch.Add(leaf)
				self.dependencies.tree[os.path.join(filter, name)] = leaf
				self.dependencies.leaves[filename] = leaf

def Parse(state, args, log):
	"""Traverse a directory tree to build the dependencies
  Arguments:
    dependencies:
      name that the dependencies object is stored under
    input:
      directory to traverse
    environment:
      file containing the environment variables used in filters and paths
      default is no environment file
    filters:
      file containing mappings from filter to file or directory
      default is no filters file
    paths:
      file containing search directories for files to include
    language:
      name that the language object is stored under"""
	direc = args["input"]
	
	environment = {}
	if Default(args, "environment", "") != "":
		environment = ReadKeyValue(args["environment"], {})
		
	paths = ReadText(args["paths"], environment)
	
	filters = {}
	if Default(args, "filters", "") != "":
		filters = ReadKeyValue(args["filters"], environment)
	filters = Filtered(filters)
		
	dependencies = state[args["dependencies"]]
	generic = Generic(dependencies, filters, paths)
	reader = state[args["language"]]
	
	log.write("Reading project\n")
	generic.ReadProject(direc, reader)
	
	keys = dependencies.leaves.keys()
	log.write("About to read %d files\n" % len(keys))
	for f in keys:
		leaf = dependencies.leaves[f]
		deps, missing = reader.ReadFile(f, generic.paths)
		leaf.missing.extend(missing)
		for dep in deps:
			dep = reader.AddFile(dep, dependencies.leaves)
			if dep == None:
				continue
			leaf.AddDependency(dep)

def Methods():
	return [Parse, ]