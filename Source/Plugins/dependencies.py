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
import os, os.path, sys, json
from utilities import Default
from readtext import ReadKeyValue
from filtered import Filtered

class Dependency:
	def __init__(self, name, parent):
		self.name = name
		self.parent = parent
		self.dependencies = []
		self.interlinks = []
		self.links = []

	def Contains(self, dependency):
		return False

	def Assemble(self):
		return

	def AddDependency(self, dep):
		self.dependencies.append(dep)
		
	def Path(self):
		if self.parent == None:
			return ""
		path = self.parent.Path()
		if path == "":
			return self.name
		return "%s/%s" % (path, self.name)
		
	def IsDescendedFrom(self, parent):
		if self.parent == None:
			return False
		if self.parent == parent:
			return True
		return self.parent.IsDescendedFrom(parent)

	def FindChild(self, parent):
		if self.parent == None:
			return None
		if self.parent == parent:
			return self
		return self.parent.FindChild(parent)

	def CrossReference(self, dependencies):
		for dependency in self.dependencies:
			link = dependency.parent
			if link != None:
				if 0 == self.links.count(link):
					self.links.append(link)

	def EnclosedBy(self, ordered):
		count = 0
		for link in self.links:
			if ordered.count(link) == 1:
				count += 1
		if self.links.count(self) == 1 and ordered.count(self) == 0:
			count += 1
		return len(self.links) == count
		
class Leaf(Dependency):
	def __init__(self, name, parent):
		Dependency.__init__(self, name, parent)
		self.missing = []

	def Export(self, fp, indent, incr, end):
		fp.write('%s{\n'% (indent))
		fp.write('%s%s"name":"%s",\n'% (indent, incr, self.name))
		fp.write('%s%s"full":"%s",\n'% (indent, incr, self.Path()))
		
		if len(self.missing):
			missing = '", "'.join(self.missing)
			fp.write('%s%s"missing":["%s"],\n'% (indent, incr, missing))
		
		fp.write('%s%s"dependencies":[\n'% (indent, incr))
		
		dependencies = []
		for dep in self.dependencies:
			dependencies.append(dep.Path())
		dependencies = sorted(dependencies)
		
		dend = ','
		for i in range(len(dependencies)):
			if i == len(dependencies) - 1:
				dend = ''
			fp.write('%s%s%s"%s"%s\n'% (indent, incr, incr, dependencies[i], dend))
			
		fp.write('%s%s]\n'% (indent, incr))
		fp.write('%s}%s\n'% (indent, end))

class Branch(Dependency):
	def __init__(self, name, parent):
		Dependency.__init__(self, name, parent)
		self.children = []

	def Add(self, child):
		self.children.append(child)

	def Export(self, fp, indent, incr, end):
		fp.write('%s{\n'% (indent))
		fp.write('%s%s"name":"%s",\n'% (indent, incr, self.name))
		fp.write('%s%s"children":[\n'% (indent, incr))
		
		mapping = {}
		for child in self.children:
			mapping[child.name] = child
		children = sorted(mapping.keys())
		
		cend = ','
		for child in children:
			if child == children[-1]:
				cend = ''
			mapping[child].Export(fp, indent + incr + incr, incr, cend)
		
		fp.write('%s%s]\n'% (indent, incr))
		fp.write('%s}%s\n'% (indent, end))

	def Contains(self, dependency):
		return 1 == self.children.count(dependency)

	def Complexity(self):
		edges = 0
		for node in self.children:
			edges += len(node.interlinks)
		
		mapping = {}
		label = 0
		for node in self.children:
			parts = []
			if node in mapping:
				parts.append(mapping[node])
			for dep in node.interlinks:
				if dep in mapping and 0 == parts.count(mapping[dep]):
					parts.append(mapping[dep])
				mapping[dep] = label
			for dep in mapping.keys():
				if 1 == parts.count(mapping[dep]):
					mapping[dep] = label
			mapping[node] = label
			label += 1
		
		parts = []
		for dep in mapping.keys():
			if 0 == parts.count(mapping[dep]):
				parts.append(mapping[dep])
				
		self.complexity = [edges, len(self.children), len(parts)]

	def N(self):
		return self.complexity[1]

	def EPN(self):
		return self.complexity[0] - self.complexity[1] + self.complexity[2]

	def Assemble(self):
		for leaf in self.children:
			leaf.Assemble()
			for dependency in leaf.dependencies:
				if 0 == self.dependencies.count(dependency):
					self.dependencies.append(dependency)

class Dependencies:
	def __init__(self):
		self.tree = { "" : Branch("", None) }
		self.leaves = {}

	def Assemble(self):
		self.tree[""].Assemble()
		for node in self.tree.keys():
			self.tree[node].CrossReference(self)
		self.Interlinks()

	def OrderKeys(self):
		parents = []
		for key in self.leaves.keys():
			parent = self.leaves[key].parent
			if parents.count(parent) == 0:
				parents.append(parent)
		keys = []
		for parent in parents:
			keys.append(parent.Path())
		ordered = []
		while True:
			length = len(keys)
			if length == 0:
				break
			found = False
			for i in range(length):
				key = keys[i]
				node = self.tree[key]
				if node.EnclosedBy([self.tree[o] for o in ordered]):
					ordered.append(key)
					keys.remove(key)
					found = True
					break
			if not found:
				ordered.append(keys[0])
				keys = keys[1:]
		return ordered
		
	def SubSections(self):
		keys = []
		for key in self.tree.keys():
			o = self.tree[key]
			if isinstance(o, Branch):
				if o.parent != None:
					keys.append(o.Path())
		return sorted(keys)
		
	def GetLinks(self, s):
		deps = []
		for link in s.links:
			if link.IsDescendedFrom(s):
				continue
			if 0 == deps.count(link):
				deps.append(link)
		for child in s.children:
			for link in child.links:
				if link.IsDescendedFrom(s):
					continue
				if 0 == deps.count(link):
					deps.append(link)
		if deps.count(s):
			deps.remove(s)
			
		return deps

	def Interlinks(self):
		for key in self.tree.keys():
			branch = self.tree[key]
			if not isinstance(branch, Branch):
				continue
			for c in branch.children:
				for link in c.dependencies:
					dep = link.FindChild(branch)
					if dep == None or dep == c:
						continue
					if 1 == c.interlinks.count(dep):
						continue
					c.interlinks.append(dep)
				for dep in c.dependencies:
					if 1 == branch.children.count(dep):
						if 0 == c.interlinks.count(dep):
							c.interlinks.append(dep)
			branch.Complexity()

	def GetPath(self, path):
		if path in self.tree:
			return self.tree[path]
		i = path.rfind('/')
		if i == -1:
			parent = self.tree['']
			branch = Branch(path, parent)
		else:
			parent = self.GetPath(path[:i])
			branch = Branch(path[i+1:], parent)
		parent.Add(branch)
		self.tree[path] = branch
		return branch

	def PrintTable(self, keys, header):
		table = ""
		max = 0
		for g in keys:
			if max < len(g):
				max = len(g)
		format = "%%%ds " % max
		
		if header:
			for i in range(0, max):
				table += format % ""
				for key in keys:
					j = i + len(key) - max
					if j < 0:
						table += " "
					else:
						table += key[j]
				table += "\n"
			table += "\n"
		
		for g in keys:
			table += format % g
			node = self.tree[g]
			for h in keys:
				if g == h:
					table += '\\'
					continue
				c = [l.Path() for l in node.links].count(h)
				if c == 0:
					table += ' '
					continue
				table += "%d" % c
			table += "\n"
		return table

def Factory(state, args, log):
	"""Create an object to hold the dependencies
  Arguments:
    store:
      name to store the object in"""
	state[args["store"]] = Dependencies()

def Assemble(state, args, log):
	"""Cross-reference the dependencies
  Arguments:
    dependencies:
      name that the dependencies object is stored under"""
	state[args["dependencies"]].Assemble()

def Export(state, args, log):
	"""Exports the dependencies tree in JSON format
  Arguments:
    dependencies:
      name that the dependencies object is stored under
    output:
      filename to write the dependency tree in"""
	fp = open(args["output"], "w")
	state[args["dependencies"]].tree[""].Export(fp, "", "  ", "")
	fp.close()

def ImportHelper(mapping, leaves):
	if "children" in mapping:
		for child in mapping["children"]:
			ImportHelper(child, leaves)
	else:
		leaves[mapping["full"]] = mapping

def Import(state, args, log):
	"""Imports the dependencies tree in JSON format
  Arguments:
    dependencies:
      name that the dependencies object is stored under
    environment:
      file containing the environment variables used in filters and paths
      default is no environment file
    filters:
      file containing mappings from filter to file or directory
      default is no filters file
    input:
      filename to read the dependency tree from"""
	environment = {}
	if Default(args, "environment", "") != "":
		environment = ReadKeyValue(args["environment"], {})
		
	filters = {}
	if Default(args, "filters", "") != "":
		filters = ReadKeyValue(args["filters"], environment)
	filters = Filtered(filters)
		
	dependencies = state[args["dependencies"]]
	
	fp = open(args["input"], "r")
	mapping = json.load(fp)
	fp.close()
	
	leaves = {}
	ImportHelper(mapping, leaves)
	
	leaves2 = {}
	for path in leaves.keys():
		filter, name = os.path.split(path)
		filter = filters.Filter(path)
		branch = dependencies.GetPath(filter)
		leaf = Leaf(name, branch)
		leaves2[path] = leaf
		branch.Add(leaf)
	
	for path in leaves.keys():
		leaf = leaves2[path]
		for dep in leaves[path]["dependencies"]:
			if not dep in leaves2:
				log.write("Cannot find dependency %s\n" % dep)
				continue
			leaf.dependencies.append(leaves2[dep])

def Methods():
	return [Factory, Assemble, Export, Import]
