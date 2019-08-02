"""
Unit test the lepton module.

Package:
  RoadNarrows elemenpy python package.

File:
  utlepton.py

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
import io

from elemenpy.testing.ut import *

import elemenpy.sm.lepton as sut

# -----------------------------------------------------------------------------
# Unit Test Data
# -----------------------------------------------------------------------------
# null and singleton datasets
dsBase      = UTDataset('ds_base', data=[sut.Lepton])
dsDerived   = UTDataset('ds_derived',
    data=[cls for name,cls in sut.Lepton.lepton_family().items()])

# the database of datasets
db = UTDsDb('db', ds=[dsBase, dsDerived])

# -----------------------------------------------------------------------------
# Unit Tests
# -----------------------------------------------------------------------------
class utPrint(UT):
  """ Unit test print methods. """
  def __init__(self, dskey):
    UT.__init__(self, "properties", dskey)

  def begin(self, sequencer, datum):
    classobj  = datum
    classname = classobj.__name__
    self.func = None
    for funcname in ['print_properties', 'print_lepton_properties']:
      try:
        self.func = getattr(classobj, funcname)
        break
      except AttributeError:
        self.func = None
    if self.func is not None:
      return (f"{classname}.{funcname}()", UTState.PASS)
    else:
      return (f"{classname}.NO_PRINT_METHOD()", UTState.FAIL)

  def test(self, sequencer, datum):
    if self.func is None:
      return UTState.FAIL, f"{uRArrow} cannot print"
    with io.StringIO() as output:
      self.func(indent=2, file=output)
      lines = output.getvalue().split('\n')
    if not lines[-1]:
      lines = lines[:-1]
    return UTState.PASS, [f"{uRArrow} print output"] + lines

# -----------------------------------------------------------------------------
# Unit Test Subsystem, Suite, Sequencer, and Main
# -----------------------------------------------------------------------------
suite = UTSuite('testsuite',
  subsystems=[
    UTSubsys('print',
      "Test printing.",
      unittests=[
        utPrint('ds_base'),
        utPrint('ds_derived'),
      ]
    ),
  ],
)

utseq = UTSequencer('lepton', suite, db)

utmain = lambda: UTMainTemplate(utseq, "Unit test lepton module.")
