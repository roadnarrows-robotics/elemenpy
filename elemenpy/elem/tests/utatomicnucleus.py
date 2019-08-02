"""
Unit test the atomicnucleus module.

Package:
  RoadNarrows elemenpy python package.

File:
  utatomicnucleus.py

Link:
  https://github.com/roadnarrows-robotics/

Copyright:
  (c) 2019. RoadNarrows LLC
  http://www.roadnarrows.com
  All Rights Reserved

License:
  MIT
"""
import io
from copy import copy
import random
import math

from elemenpy.core.format import (default_encoder, Format4Some)
from elemenpy.testing.ut import *

import elemenpy.elem.atomicnucleus as sut

# -----------------------------------------------------------------------------
# Unit Test Data
# -----------------------------------------------------------------------------
dsNuclei = UTDataset('ds_nuclei',
    data=[sut.AtomicNucleus(1, 2),
          sut.AtomicNucleus(2, 4, name='alpha', symbol='$greek(alpha)'),
          sut.AtomicNucleus(90, 231, name='thorium'),
          sut.AtomicNucleus(54, 132),
    ]
)

# the database of datasets
db = UTDsDb('db', ds=[dsNuclei])

# -----------------------------------------------------------------------------
# Unit Tests
# -----------------------------------------------------------------------------
class utPrintProperties(UT):
  """ Unit test nucleus print_properties(). """
  def __init__(self, dskey):
    UT.__init__(self, "print_properties()", dskey)

  def begin(self, sequencer, datum):
    return (f"{datum}", UTState.PASS)

  def test(self, sequencer, datum):
    with io.StringIO() as output:
      datum.print_properties(file=output)
      lines = output.getvalue().split('\n')
    if not lines[-1]:
      lines = lines[:-1]
    return UTState.PASS, [f"{uRArrow} output info"] + lines

# -----------------------------------------------------------------------------
# Unit Test Subsystem, Suite, Sequencer, and Main
# -----------------------------------------------------------------------------
suite = UTSuite('testsuite',
  subsystems=[
    UTSubsys('AtomicNucleus',
      "Test AtomicNucleus class.",
      unittests=[
        utPrintProperties('ds_nuclei'),
      ]
    ),
  ],
)

utseq = UTSequencer('atomicnucleus', suite, db)

utmain = lambda: UTMainTemplate(utseq, "Unit test atomicnucleus module.")
