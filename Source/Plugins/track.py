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
import os.path, time, datetime
import dependencies

def Report(state, args, log):
	"""Append metrics to a file
  Arguments:
    dependencies:
      name that the dependencies object is stored under
    output:
      file to create or append"""
	dependencies = state[args["dependencies"]]
	fullpath = args["output"]
	if not os.path.exists(fullpath):
		f = open(fullpath, "w")
		f.write("""
# The time is the number of seconds since some arbitrary start date.
# The quantity that we calculate the maximum and sum of is (E + P - N).
# This has a value of zero for strictly layered architectures
# otherwise it is positive.
# Also track the normalised value (E + P - N) / N.
# Time            Max        Sum        Max        Sum
"""[1:])
		f.close()
	
	f = open(fullpath, "a")
	
	sections = dependencies.SubSections()
	sections.append("")
	
	sum = 0
	max = 0
	sumN = 0.0
	maxN = 0.0
	for name in sections:
		branch = dependencies.tree[name]
		
		if branch.N() > 0:
			factor = branch.EPN()
			sum += factor
			if max < factor:
				max = factor
				
			factor /= branch.N() * 1.0
			sumN += factor
			if maxN < factor:
				maxN = factor
	
	dat = datetime.datetime.now()
	t = time.mktime(dat.timetuple())
	f.write("%.0f %10d %10d %10.2f %10.2f\n" % (t, max, sum, maxN, sumN))
	f.close()

def Methods():
	return [Report, ]
