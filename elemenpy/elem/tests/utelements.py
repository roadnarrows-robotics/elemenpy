"""
Unit test the elements module.

Package:
  RoadNarrows elemenpy python package.

File:
  utelements.py

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

from elemenpy.core.common import (enum_to_str)

from elemenpy.testing.ut import *

import elemenpy.elem.elements as sut

# -----------------------------------------------------------------------------
# Unit Test Data
# -----------------------------------------------------------------------------

# the database of datasets
db = UTDsDb('db', ds=[dsBoilOne])

# -----------------------------------------------------------------------------
# Unit Tests
# -----------------------------------------------------------------------------
class utPrintZ(UT):
  """ Unit test ElementZ data. """
  def __init__(self, dskey):
    UT.__init__(self, f"{sut.ElementZ.__name__}.print", dskey)

  def begin(self, sequencer, datum):
    return (f"data", UTState.PASS)

  def test(self, sequencer, datum):
    with io.StringIO() as output:
      print(f"{'Enum':<24}{'Z':<4}{'Name':<14}Symbol", file=output)
      print(f"{'----':<24}{'-':<4}{'----':<14}------", file=output)
      for ez in sut.ElementZ:
        z     = sut.z_to_z(ez)
        name  = sut.z_to_name(ez)
        sym   = sut.z_to_symbol(ez)
        print(f"{ez:<24}{z:<4}{name:<14}{sym}", file=output)
      lines = output.getvalue().split('\n')
    if not lines[-1]:
      lines = lines[:-1]
    return UTState.PASS, [f"{uRArrow} the elements"] + lines

class utPrintEnum(UT):
  """ Unit test enum data. """
  def __init__(self, dskey, enum):
    UT.__init__(self, f"{enum.__name__}.print", dskey, enum)

  def prep(self, sequencer):
    UT.prep(self, sequencer)
    self.enum = self.args[0]
    
  def begin(self, sequencer, datum):
    return ("data", UTState.PASS)

  def test(self, sequencer, datum):
    with io.StringIO() as output:
      print(f"{'Enum':<42}{'Value':<7}Name", file=output)
      print(f"{'----':<42}{'-----':<7}----", file=output)
      for e in self.enum:
        val   = e.value
        name  = enum_to_str(e, sep='-')
        print(f"{e:<42}{val:<7}{name}", file=output)
      lines = output.getvalue().split('\n')
    if not lines[-1]:
      lines = lines[:-1]
    return UTState.PASS, [f"{uRArrow} the data"] + lines

# -----------------------------------------------------------------------------
# Unit Test Subsystem, Suite, Sequencer, and Main
# -----------------------------------------------------------------------------
suite = UTSuite('testsuite',
  subsystems=[
    UTSubsys('z',
      "Test ElementZ data.",
      unittests=[
        utPrintZ('ds_boil_one'),
      ]
    ),
    UTSubsys('group',
      "Test ElementGroup enum.",
      unittests=[
        utPrintEnum('ds_boil_one', sut.ElementGroup),
      ]
    ),
    UTSubsys('period',
      "Test ElementPeriod enum.",
      unittests=[
        utPrintEnum('ds_boil_one', sut.ElementPeriod),
      ]
    ),
    UTSubsys('block',
      "Test ElementBlock enum.",
      unittests=[
        utPrintEnum('ds_boil_one', sut.ElementBlock),
      ]
    ),
    UTSubsys('category',
      "Test ElementCategory enum.",
      unittests=[
        utPrintEnum('ds_boil_one', sut.ElementCategory),
      ]
    ),
    UTSubsys('subcategory',
      "Test ElementSubcategory enum.",
      unittests=[
        utPrintEnum('ds_boil_one', sut.ElementSubcategory),
      ]
    ),
  ],
)

utseq = UTSequencer('elements', suite, db)

utmain = lambda: UTMainTemplate(utseq, "Unit test elements module.")
