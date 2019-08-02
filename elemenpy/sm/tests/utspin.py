"""
Unit test the spin module.

Package:
  RoadNarrows elemenpy python package.

File:
  utspin.py

Link:
  https://github.com/roadnarrows-robotics/

Copyright:
  (c) 2019. RoadNarrows LLC
  http://www.roadnarrows.com
  All Rights Reserved

License:
  MIT
"""
from copy import copy
import random
import math

from elemenpy.testing.ut import *

import elemenpy.sm.spin as sut

# -----------------------------------------------------------------------------
# Unit Test Data
# -----------------------------------------------------------------------------
dsSpins = UTDataset('ds_spins',
    data =  [ sut.SpinQuantumNumber(0),
              sut.SpinQuantumNumber(1, 2),
              sut.SpinQuantumNumber(-1, 2),
              sut.SpinQuantumNumber(3, 2),
              sut.SpinQuantumNumber(1),
              sut.SpinQuantumNumber(-1)
            ])

dsBuiltinsNum  = UTDataset('ds_builtins_num',
    data = [abs, bool, complex, float, int, round])

dsBuiltins  = UTDataset('ds_builtins', data = [callable, id, repr, str, type])

# the database of datasets
db = UTDsDb('db', ds=[dsSpins, dsBuiltinsNum, dsBuiltins])

# -----------------------------------------------------------------------------
# Unit Tests
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Unit Test Subsystem, Suite, Sequencer, and Main
# -----------------------------------------------------------------------------
suite = UTSuite('testsuite',
  subsystems=[
    UTSubsys('numeric',
      "Test python numeric built-ins on SpinQuantumNumber dataset.",
      unittests=[
        utBoilBuiltins('SpinQuantumNumber', 'ds_builtins_num', 'ds_spins'),
      ]
    ),
    UTSubsys('builtins',
      "Test python built-ins on SpinQuantumNumber dataset.",
      unittests=[
        utBoilBuiltins('SpinQuantumNumber', 'ds_builtins', 'ds_spins'),
      ]
    ),
  ],
)

utseq = UTSequencer('spin', suite, db)

utmain = lambda: UTMainTemplate(utseq, "Unit test spin module.")
