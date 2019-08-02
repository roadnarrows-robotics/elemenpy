"""
Unit test the colorcharge module.

Package:
  RoadNarrows elemenpy python package.

File:
  utcolorcharge.py

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

import elemenpy.sm.colorcharge as sut

# -----------------------------------------------------------------------------
# Unit Tests
# -----------------------------------------------------------------------------

class utNew(UT):
  """ Unit test ColorCharge(value) construction. """
  def __init__(self, dskey, dskey_out):
    UT.__init__(self, "ColorCharge(value)", dskey)
    self.dskeyOut = dskey_out
    self.dsTmp = UTDataset(self.dskeyOut, data=[])

  def begin(self, sequencer, datum):
    self.value  = datum
    return (f"ColorCharge({self.value!r})", UTState.PASS)

  def test(self, sequencer, datum):
    try:
      cc = sut.ColorCharge(self.value)
    except (TypeError, ValueError) as e:
      return UTState.FAIL, [f"{uRArrow} error", f"{e}"]
    else:
      self.dsTmp.append(cc)
      return UTState.PASS, f"{uRArrow} {cc.symbol} {cc.name}"

  def end(self, sequencer):
    pass

  def finalize(self, sequencer):
    if len(self.dsTmp) > 0:
      sequencer.dsdb[self.dskeyOut] = self.dsTmp.copy()
      print(f"      (dataset {self.dskeyOut!r} added to database.)")

# -----------------------------------------------------------------------------
# Unit Test Data
# -----------------------------------------------------------------------------
dsVals = UTDataset('ds_vals',
    data =  [
      'R', 'G', 'B', 'C', 'M', 'Y',
      'red', 'green', 'blue', 'antired', 'antigreen', 'antiblue',
      sut.ColorCharge.QCDColor.RED,
      sut.ColorCharge.QCDColor.GREEN,
      sut.ColorCharge.QCDColor.BLUE,
      'cyan', 'magenta', 'yellow',
    ])

dsBuiltins  = UTDataset('ds_builtins', data = [id, repr, str, type])

# the database of datasets
db = UTDsDb('db', ds=[dsVals, dsBuiltins])

# -----------------------------------------------------------------------------
# Unit Test Subsystem, Suite, Sequencer, and Main
# -----------------------------------------------------------------------------
suite = UTSuite('testsuite',
  subsystems=[
    UTSubsys('construct',
      "Test ColorCharge class construction.",
      unittests=[
        utNew('ds_vals', dskey_out='ds_cc')
      ]
    ),
    UTSubsys('builtins',
      "Test python built-ins on ColorCharge dataset.",
      unittests=[
        utBoilBuiltins('ColorCharge', 'ds_builtins', 'ds_cc'),
      ],
      prereqs=['construct']
    ),
  ],
)

utseq = UTSequencer('colorcharge', suite, db)

utmain = lambda: UTMainTemplate(utseq, "Unit test colorcharge module.")
