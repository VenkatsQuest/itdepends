#!/usr/bin/env python
#
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
import sys, os.path
import matplotlib.pyplot as plt

def Plot(filename):
	header = []
	times = []
	sum = []
	max = []
	sumN = []
	maxN = []
	comments = []
	for line in open(filename):
		if line[:1] == '#':
			header = line[1:].split()
			continue
		bits = line.split()
		times.append(float(bits[0]))
		sum.append(int(bits[1]))
		max.append(int(bits[2]))
		sumN.append(float(bits[3]))
		maxN.append(float(bits[4]))
	for i in range(1, len(times)):
		times[i] = (times[i] - times[0]) / 86400.0
	times[0] = 0.0
	
	plt.plot(times, sum, label=header[1])
	plt.plot(times, max, label=header[2])
	plt.xlabel(header[0])
	plt.ylabel('E + P - N')
	plt.xlim(xmin=0)
	plt.ylim(ymin=0)
	plt.legend()
	plt.show()
	
	plt.plot(times, sumN, label=header[3])
	plt.plot(times, maxN, label=header[4])
	plt.xlabel(header[0])
	plt.ylabel('(E + P - N) / N')
	plt.xlim(xmin=0)
	plt.ylim(ymin=0)
	plt.legend()
	plt.show()

if __name__ == "__main__":
	if len(sys.argv) == 1:
		sys.argv.append("-h")
		
	if 1 == ["-h", "--help"].count(sys.argv[1]):
		print("""
usage: %s [-h|--help] filename
       where filename is the name of a file containing the output from the track plugin
"""[1:] % os.path.split(sys.argv[0])[1])
		exit(0)
	Plot(sys.argv[1])
