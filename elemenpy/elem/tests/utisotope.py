"""
Unit test the isotope module.

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

from elemenpy.core.common import (isderivedinstance)
from elemenpy.core.format import (default_encoder, Format4Some)

from elemenpy.testing.ut import *

import elemenpy.elem.isotope as sut

# -----------------------------------------------------------------------------
# Unit Test Data
# -----------------------------------------------------------------------------
dsIsotope = UTDataset('ds_isotope',
    data=[sut.Isotope,
          sut.Isotope(label='auto'),
    ]
)

# the database of datasets
db = UTDsDb('db', ds=[dsIsotope])

# -----------------------------------------------------------------------------
# Unit Tests
# -----------------------------------------------------------------------------
class utPrintProperties(UT):
  """ Unit test print properties. """
  def __init__(self, dskey):
    UT.__init__(self, "print_isotope_properties()", dskey)

  def begin(self, sequencer, datum):
    return (f"{datum}", UTState.PASS)

  def test(self, sequencer, datum):
    with io.StringIO() as output:
      datum.print_isotope_properties(indent=2, file=output)
      lines = output.getvalue().split('\n')
    if not lines[-1]:
      lines = lines[:-1]
    return UTState.PASS, [f"properties {uRArrow}"] + lines

class utPrintState(UT):
  """ Unit test print state. """
  def __init__(self, dskey):
    UT.__init__(self, "print_state()", dskey)

  def begin(self, sequencer, datum):
    return (f"{datum}", UTState.PASS)

  def test(self, sequencer, datum):
    if isderivedinstance(datum, sut.Isotope):
      with io.StringIO() as output:
        datum.print_state(indent=2, file=output)
        lines = output.getvalue().split('\n')
      if not lines[-1]:
        lines = lines[:-1]
      return UTState.PASS, [f"state {uRArrow}"] + lines
    else:
      return UTState.PASS, [f"{uRArrow} no state"]

# -----------------------------------------------------------------------------
# Unit Test Subsystem, Suite, Sequencer, and Main
# -----------------------------------------------------------------------------
suite = UTSuite('testsuite',
  subsystems=[
    UTSubsys('Isotope',
      "Test Isotope class.",
      unittests=[
        utPrintProperties('ds_isotope'),
        utPrintState('ds_isotope'),
      ]
    ),
  ],
)

utseq = UTSequencer('isotope', suite, db)

utmain = lambda: UTMainTemplate(utseq, "Unit test isotope module.")
