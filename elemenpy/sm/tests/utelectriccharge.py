"""
Unit test the electriccharge module.

Package:
  RoadNarrows elemenpy python package.

File:
  utelectriccharge.py

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

import elemenpy.sm.electriccharge as sut

# -----------------------------------------------------------------------------
# Unit Test Data
# -----------------------------------------------------------------------------
# null and singleton datasets
dsSpins = UTDataset('ds_charges',
    data =  [ sut.ElectricCharge(0),
              sut.ElectricCharge(1, 2),
              sut.ElectricCharge(-1, 2),
              sut.ElectricCharge(3, 2),
              sut.ElectricCharge(1),
              sut.ElectricCharge(-1),
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
      "Test python numeric built-ins on ElectricCharge dataset.",
      unittests=[
        utBoilBuiltins('ElectricCharge', 'ds_builtins_num', 'ds_charges'),
      ]
    ),
    UTSubsys('builtins',
      "Test python built-ins on ElectricCharge dataset.",
      unittests=[
        utBoilBuiltins('ElectricCharge', 'ds_builtins', 'ds_charges'),
      ]
    ),
  ],
)

utseq = UTSequencer('electriccharge', suite, db)

utmain = lambda: UTMainTemplate(utseq, "Unit test electriccharge module.")
