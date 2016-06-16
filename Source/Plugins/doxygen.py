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
from dependencies import Branch
from language import Language
from utilities import Default

class Node:
	def __init__(self, node, dependencies, lookup):
		self.title = "Top level"
		if node.name != "":
			self.title = node.Path().replace('/', '::')
		
		if isinstance(node, Branch):
			self.url = "%s.html" % lookup[node]
		else:
			self.url = "\\ref %s" % (node.name)

class NodeSet:
	def __init__(self, dependencies):
		self.subsections = dependencies.SubSections()
		self.lookup = {dependencies.tree[""] : "architecture0"}
		for index in range(len(self.subsections)):
			self.lookup[dependencies.tree[self.subsections[index]]] = "architecture%d" % (index + 1)
		
		self.nodes = {}
		for key in dependencies.tree.keys():
			self.nodes[dependencies.tree[key]] = Node(dependencies.tree[key], dependencies, self.lookup)

	def Graph(self, branch, direc, linkToLeaves):
		filename = "%s.dot" % self.lookup[branch]
		f2 = open(os.path.join(direc, filename), "w")
		f2.write("""
digraph solution {
	subgraph cluster_0 {
		label="%s";
"""[1:] % (self.nodes[branch].title))

		for c in branch.children:
			index = branch.children.index(c)
			if not c in self.nodes or (not linkToLeaves and self.nodes[c].url[:1] == '\\'):
				f2.write("""
		N%d [label="%s"];
"""[1:] % (index, c.name))
			else:
				f2.write("""
		N%d [label="%s", URL="%s"];
"""[1:] % (index, c.name, self.nodes[c].url))
			for dep in c.interlinks:
				f2.write("""
		N%d -> N%d;
"""[1:] % (index, branch.children.index(dep)))
		f2.write("""
	}
}
"""[1:])

	def Section(self, branch, dependencies, f, writer, direc):
		label = self.lookup[branch]
		
		writer.WriteToDoxygenFile(f, """

\page %s %s
"""[1:-1] % (label, self.nodes[branch].title))
	
		if branch.parent != None:
			parent = 'architecture0'
			if branch.parent.name != '':
				parent = self.lookup[branch.parent]
			writer.WriteToDoxygenFile(f, """

Subset of \\ref %s

"""[1:-1] % (parent))
	
		writer.WriteToDoxygenFile(f, """
N = %d, E + P - N = %d
\dotfile %s

"""[1:-1] % (branch.N(), branch.EPN(), "%s.dot" % label))

		line = ""
		deps = {}
		for dep in dependencies.GetLinks(branch):
			deps[dep.Path()] = dep
		for dep in sorted(deps.keys()):
			line += ", \\ref %s" % (self.lookup[deps[dep]])
		if line != "":
			writer.WriteToDoxygenFile(f, """
Dependencies are %s.

"""[1:-1] % (line[2:]))

def StructureMatrix(dependencies, f, writer):
	writer.WriteToDoxygenFile(f, """
\page StructureMatrix Structure Matrix
The structure matrix shows the dependency of one section on another, 
- a value of 1 indicates a dependency
- a blank indicates no dependency
- a slash indicates the diagonal

The rows and columns are in the same order and an attempt is made to sort the matrix into a lower triangular form, if this fails it should indicate the presence of a circular dependency.
\\verbatim
"""[1:-1])
	writer.WriteVerbatimToDoxygenFile(f, dependencies.PrintTable(dependencies.OrderKeys(), False))
	writer.WriteVerbatimToDoxygenFile(f, """
\endverbatim

"""[1:-1])

def Report(state, args, log):
	"""Create output to be processed by Doxygen/DoxyPress
  Arguments:
    dependencies:
      name that the dependencies object is stored under
    output:
      directory in which to write the output
    matrix:
      whether to output the structure matrix
      default is False
    linkToLeaves:
      whether to cross-reference to the code
      default is False
    language:
      name that the language object is stored under"""
	dependencies = state[args["dependencies"]]
	direc = args["output"]
	showStructure = Default(args, "matrix", False)
	linkToLeaves = Default(args, "linkToLeaves", False)
	
	writer = state[args["language"]]
	f = open(os.path.join(direc, "architecture") + writer.FileExtensions()[0], "w")
	writer.WriteToDoxygenFile(f, """
\page Architecture Architecture
"""[1:-1])

	writer.WriteToDoxygenFile(f, """
\section Introduction Introduction
By grouping files together it is possible to express the architecture in terms of a hierarchical set of directed graphs. Within a graph the edges represent a dependency of one node on another. By clicking on an ellipse in the diagram it is possible to descend to the next level. The top level diagram can be found in \\ref architecture0.

"""[1:-1])

	if showStructure:
		writer.WriteToDoxygenFile(f, """
The graphs can also be represented in matrix form as seen in \\ref StructureMatrix.

"""[1:-1])

	writer.WriteToDoxygenFile(f, """
Given that graphs have been derived then metrics can be calculated for each, these are presented in \\ref Summary.
"""[1:-1])

	if showStructure:
		StructureMatrix(dependencies, f, writer)
	
	nodeset = NodeSet(dependencies)
	factors = {}
	sum = 0.0
	sumN = 0.0
	for branch in nodeset.lookup.keys():
		name = branch.Path()
		node = nodeset.nodes[branch]
		
		nodeset.Graph(branch, direc, linkToLeaves)
		
		N = branch.N() * 1.0
		EPN = branch.EPN()
		if N > 0:
			factor = EPN / N
			sum += EPN
			sumN += factor
			if not factor in factors:
				factors[factor] = [name]
			else:
				factors[factor].append(name)
	
	writer.WriteToDoxygenFile(f, """
\page Summary Summary of graph complexity
The larger the value of (E + P) / N then the more complex the directed graph is, where
- E: Number of edges
- P: Number of parts
- N: Number of nodes

The value of (E + P - N) / N varies between 0 and N. A stricly layered architecture will have a value of 0.

The sum of (E + P - N) is %.0f, 
sum of (E + P - N) / N is %.2f.

Section | N | E + P - N | (E + P - N) / N
--------|---|-----------|----------------
"""[1:-1] % (sum, sumN))
	keys = sorted(factors.keys())
	keys.reverse()
	for key in keys:
		for name in sorted(factors[key]):
			branch = dependencies.tree[name]
			writer.WriteToDoxygenFile(f, """
\\ref %s | %d | %d | %.2f
"""[1:-1] % (nodeset.lookup[branch], branch.N(), branch.EPN(), key))
	
	nodeset.Section(dependencies.tree[""], dependencies, f, writer, direc)
	for index in range(len(nodeset.subsections)):
		name = nodeset.subsections[index]
		nodeset.Section(dependencies.tree[name], dependencies, f, writer, direc)
		
	f.close()

def Methods():
	return [Report, ]