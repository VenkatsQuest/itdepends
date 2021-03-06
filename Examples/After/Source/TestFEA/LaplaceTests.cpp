#include "stdafx.h"
#include "CppUnitTest.h"
#include "Mesh.h"
#include "Solver.h"
#include "Equations/Laplace.h"
#include "Equations/LaplaceBoundary.h"
#include "Fields/FieldNodal.h"
#include "Fields/FieldHandler.h"
#include "FileIO/WriteVtk.h"
#include "TestClasses/DiffFiles.h"
#include "TestUtils/LogStream.h"
#include <fstream>
