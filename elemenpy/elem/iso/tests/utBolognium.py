"""
Unit test of the defined isotopes module.

Package:
  RoadNarrows elemenpy python package.

File:
  utBolognium.py

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

from elemenpy.elem.isotope import (Isotope)

from elemenpy.testing.ut import *

import elemenpy.elem.iso.H as sutH
import elemenpy.elem.iso.He as sutHe
import elemenpy.elem.iso.B as sutB

# -----------------------------------------------------------------------------
# Unit Test Data
# -----------------------------------------------------------------------------

# Hydrogen class
dsHClass = UTDataset('ds_h_class', data=[sutH.H1, sutH.H2, sutH.H3,])

# Hydrogen class instance
dsH = UTDataset('ds_h',
  data=[sutH.H1(label='auto'), sutH.H2(label='dude'), sutH.H3(label='auto'), ]
)

# Helium class
dsHeClass = UTDataset('ds_he_class', data=[sutHe.He4, sutHe.He3,])

# Helium class instance
dsHe = UTDataset('ds_he',
  data=[sutHe.He4(label='auto'), sutHe.He3(label='auto'),]
)

# Boron class
dsBClass = UTDataset('ds_b_class', data=[sutB.B11, sutB.B10,])

# Boron class instance
dsB = UTDataset('ds_b',
  data=[sutB.B11(label='auto'), sutB.B10(), ]
)

# the database of datasets
db = UTDsDb('db',
  ds=[
    dsHClass, dsH, dsHeClass, dsHe, dsBClass, dsB,
  ]
)

# -----------------------------------------------------------------------------
# Unit Tests
# -----------------------------------------------------------------------------
class utPrintProperties(UT):
  """ Unit test print properties. """
  def __init__(self, dskey):
    UT.__init__(self, "print_properties()", dskey)

  def begin(self, sequencer, datum):
    return (f"{datum}", UTState.PASS)

  def test(self, sequencer, datum):
    with io.StringIO() as output:
      datum.print_properties(indent=2, file=output)
      lines = output.getvalue().split('\n')
    if not lines[-1]:
      lines = lines[:-1]
    return UTState.PASS, [f"properties {uRArrow}"] + lines
    #return UTState.PASS, [f"{uRArrow} properties"] + lines

class utPrintState(UT):
  """ Unit test print state. """
  def __init__(self, dskey):
    UT.__init__(self, "print_state()", dskey)

  def begin(self, sequencer, datum):
    return (f"{datum}", UTState.PASS)

  def test(self, sequencer, datum):
    if isderivedinstance(datum, Isotope):
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

# keep alpha ordered for help
suite = UTSuite('testsuite',
  subsystems=[
    UTSubsys('b',
      "Test boron isotope classes.",
      unittests=[
        utPrintProperties('ds_b_class'),
        utPrintState('ds_b'),
      ]
    ),
    UTSubsys('h',
      "Test hydrogen isotope classes.",
      unittests=[
        utPrintProperties('ds_h_class'),
        utPrintState('ds_h'),
      ]
    ),
    UTSubsys('he',
      "Test helium isotope classes.",
      unittests=[
        utPrintProperties('ds_he_class'),
        utPrintState('ds_he'),
      ]
    ),
  ],
)

utseq = UTSequencer('Bolognium', suite, db)

utmain = lambda default_test=None: \
    UTMainTemplate(utseq, "Unit test defined isotope module(s).",
                          default_test=default_test)
