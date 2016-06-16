# itdepends

## Introduction

itdepends seeks to bridge the code-model gap as described by [George Fairbanks](http://georgefairbanks.com/book/), and thus may be considered an Architecture Development Environment. The software accompanies an article on [CodeProject](http://www.codeproject.com/Articles/1098935/As-Is-Software-Architecture) and is written in Python 3.

The basis of the software is the manipulation of dependencies between units of code. The directly supported units are

* C/C++ source files
* Python source files

where the dependencies may be acquired from

* a Microsoft Visual C++ sln file
* scanning a directory
* GCC calls from "make -n" or "make V=1"
* reading a JSON file (that may have been generated using one of the above)

The units are associated with a filter that may be related to the location within the file system. In the specific case of Visual C++ the the Visual C++ filters file associated with the relevant vcxproj file is used. In the other cases there is the option of using a file which specifies a mapping.

For output options are

* save the dependency information to a JSON file
* create input for [Doxygen](http://www.doxygen.org)
* append metrics information to a file

## Project structure

The Source directory contains

* itdepends.py - the main script (invoke with -h for help)
* Plugins - the plugins used by the main script
* Common - a set of libraries used by the plugins
* plot.py - a script to plot the metrics (invoke with -h for help)

The Examples directory contains

* Before - the main Doxygen example from [CodeProject](http://www.codeproject.com/Articles/1098935/As-Is-Software-Architecture) before refactoring
* After - the main Doxygen example from [CodeProject](http://www.codeproject.com/Articles/1098935/As-Is-Software-Architecture) after refactoring
* Plotting - the metrics example from [CodeProject](http://www.codeproject.com/Articles/1098935/As-Is-Software-Architecture)
* Python - generation of Doxygen docs from this projects source
* Linux - generation of Doxygen docs from the Linux kernel 4.6 source