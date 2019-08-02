"""
Unit test the orbital module.

Package:
  RoadNarrows elemenpy python package.

File:
  utorbital.py

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

import elemenpy.elem.orbital as sut

# -----------------------------------------------------------------------------
# Unit Test Data
# -----------------------------------------------------------------------------
# null and singleton datasets
dsOrbitals = UTDataset('ds_orbitals',
    data =  [ sut.ElectronOrbital(1, 's', 2),
              sut.ElectronOrbital(2, sut.Subshell.p, 1),
              sut.ElectronOrbital(3, 2, 2),
            ])

dsBuiltins  = UTDataset('ds_builtins', data = [repr, str, type])

# the database of datasets
db = UTDsDb('db', ds=[ dsOrbitals, dsBuiltins, ])

# -----------------------------------------------------------------------------
# Unit Tests
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Unit Test Subsystem, Suite, Sequencer, and Main
# -----------------------------------------------------------------------------
suite = UTSuite('testsuite',
  subsystems=[
    UTSubsys('builtins',
      "Test python built-ins call(spin) on orbital dataset.",
      unittests=[
        utBoilBuiltins('ElectronOrbital', 'ds_builtins', 'ds_orbitals'),
      ]
    ),
  ],
)

utseq = UTSequencer('orbital', suite, db)

utmain = lambda: UTMainTemplate(utseq, "Unit test orbital module.")
