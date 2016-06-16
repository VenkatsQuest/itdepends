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

class VisualStudio:
	def __init__(self, dependencies, log):
		self.dependencies = dependencies
		self.log = log
		self.includes = {}
	
	def ReadProject(self, direc, project):
		name = project[0]
		proj = os.path.join(direc, project[1])
		projDir = os.path.split(proj)[0]
		self.log.write("%s %s\n" % (name, proj))
		incs = Includes(proj, projDir, direc)
		filename = ''
		filter = ''
		
		for line in open(proj + '.filters'):
			line = line.strip()
			if 0 == line.find('<ClCompile Include=') or 0 == line.find('<ClInclude Include='):
				filename = line.split('Include=')[1][1:-2]
				filter = ''
			if 0 == line.find('<Filter>'):
				filter = line.replace('Filter>', '')[1:-2].replace('\\', '/')
			if 1 == ['</ClCompile>', '</ClInclude>'].count(line):
				if 1 == ['Source Files', 'Header Files'].count(filter):
					continue
				filename = os.path.normpath(os.path.join(projDir, filename))
				if os.path.exists(filename):
					branch = self.dependencies.GetPath(filter)
					name = os.path.split(filename)[1]
					leaf = Leaf(name, branch)
					branch.Add(leaf)
					self.dependencies.tree[filter + "/" + name] = leaf
					self.includes[filename] = incs
					self.dependencies.leaves[filename] = leaf

def ReadSolution(filename):
	pairs = []
	for line in open(filename):
		if line[:10] == 'Project("{':
			bits = line.split(',')
			name = bits[0].split('=')[1].strip()[1:-1]
			filename = bits[1].strip()[1:-1]
			pairs.append([name, filename])
	return pairs
	
def GetVC():
	if "VCINSTALLDIR" in os.environ:
		return os.environ["VCINSTALLDIR"]
	return r"C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\\"
	
def Includes(proj, projDir, direc):
	incs = []
	id = 'AdditionalIncludeDirectories'
	vc = GetVC()
	for line in open(proj):
		line = line.strip()[1:]
		if id == line[:len(id)]:
			line = line.replace(id, '')[1:].replace(';%()', '').replace('</>', '')
			line = "$(VCInstallDir)include\;" + line
			line = line.replace('$(ProjectDir)', projDir + '\\')
			line = line.replace('$(SolutionDir)', direc + '\\')
			line = line.replace('\\\\', '\\')
			bits = line.split(';')
			for bit in bits:
				bit = bit.replace('$(VCInstallDir)', vc)
				bit = bit.replace('\\\\', '\\')
				if 0 == incs.count(bit):
					incs.append(bit)
	return incs

def Parse(state, args, log):
	"""Build the dependencies using a Visual Studio solution file
  Arguments:
    dependencies:
      name that the dependencies object is stored under
    input:
      sln file to parse"""
	slnFile = args["input"]
	direc = os.path.split(slnFile)[0]
	projects = ReadSolution(slnFile)
	dependencies = state[args["dependencies"]]
	visual = VisualStudio(dependencies, log)
	for project in projects:
		visual.ReadProject(direc, project)
	reader = Cpp(True, log)
	keys = dependencies.leaves.keys()
	for f in keys:
		leaf = dependencies.leaves[f]
		deps, missing = reader.ReadFile(f, visual.includes[f])
		leaf.missing.extend(missing)
		for dep in deps:
			dep = reader.AddFile(dep, dependencies.leaves)
			if dep == None:
				continue
			leaf.AddDependency(dep)

def Methods():
	return [Parse, ]