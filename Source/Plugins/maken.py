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
from cpp import Cpp
from utilities import Default
from readtext import ReadKeyValue
from filtered import Filtered

class MakeN:
	def __init__(self, dependencies, log, filters):
		self.dependencies = dependencies
		self.filters = filters
		self.log = log
		self.includes = {}
	
	def Read(self, direc, input, reader):
		for line in open(input):
			for bit in line.split(';'):
				command = bit.split()
				if command[0] != 'gcc':
					continue
				filepath = command[-1]
				incs = [[], []]
				for i in range(len(command)):
					option = command[i]
					if option == '-isystem':
						incs[1].append(command[i+1])
					elif option == '-include':
						incs[0].append(command[i+1])
					elif option[:2] == '-I':
						incs[0].append(option[2:])
				
				filename = os.path.join(direc, command[-1]).replace('\\', os.sep).replace('/', os.sep)
				if not os.path.exists(filename):
					self.log.write("Source directory hasn't got %s\n" % filename)
					continue
				if not reader.CanRead(filename):
					continue
				
				leaf = self.AddFile(filename, command[-1])
				
				includes = []
				for inc in incs[0]:
					inc = inc.replace('\\', os.sep).replace('/', os.sep)
					includes.append(os.path.join(direc, inc))
				self.includes[leaf] = includes
				
	def AddFile(self, filename, command):
		filter = self.filters.Filter(command)
		name = os.path.split(command)[1]
		
		branch = self.dependencies.GetPath(filter)
		leaf = Leaf(name, branch)
		branch.Add(leaf)
		self.dependencies.tree[os.path.join(filter, name)] = leaf
		self.dependencies.leaves[filename] = leaf
		
		return leaf

	def Recurse(self, reader, f, includes, direc):
		leaf = self.dependencies.leaves[f]
		filenames, missing = reader.ReadFile(f, includes)
		leaf.missing.extend(missing)
		for filename in filenames:
			if filename in self.dependencies.leaves:
				dep = self.dependencies.leaves[filename]
			else:
				dep = self.AddFile(filename, filename[len(direc)+1:])
				self.Recurse(reader, filename, includes, direc)
			leaf.AddDependency(dep)

def Parse(state, args, log):
	"""Build the dependencies using the output from make -n
  Arguments:
    dependencies:
      name that the dependencies object is stored under
    direc:
      directory containing the source code
    input:
      file containing output from make -n
    environment:
      file containing the environment variables used in filters and paths
      default is no environment file
    filters:
      file containing mappings from filter to file or directory
      default is no filters file
    language:
      name that the language object is stored under"""
	environment = {}
	if Default(args, "environment", "") != "":
		environment = ReadKeyValue(args["environment"], {})
		
	filters = {}
	if Default(args, "filters", "") != "":
		filters = ReadKeyValue(args["filters"], environment)
	filters = Filtered(filters)
		
	dependencies = state[args["dependencies"]]
	
	maken = MakeN(dependencies, log, filters)
	reader = state[args["language"]]
	direc = args["direc"]
	maken.Read(direc, args["input"], reader)
	
	keys = dependencies.leaves.keys()
	for f in list(keys):
		leaf = dependencies.leaves[f]
		includes = maken.includes[leaf]
		maken.Recurse(reader, f, includes, direc)

def Methods():
	return [Parse, ]