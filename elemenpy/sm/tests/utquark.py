"""
Unit test the quark module.

Package:
  RoadNarrows elemenpy python package.

File:
  utquark.py

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
from elemenpy.core.prettyprint import (print2cols)

from elemenpy.sm.colorcharge import ColorCharge as cc
import elemenpy.sm.quark as sut

# -----------------------------------------------------------------------------
# Unit Tests
# -----------------------------------------------------------------------------

##-
class utPrintProperties(UT):
  """ Unit test print properties methods. """
  def __init__(self, dskey, classobj):
    UT.__init__(self, "print_properties", dskey)
    self.classobj = classobj

  def begin(self, sequencer, datum):
    #classobj  = datum
    classname = self.classobj.__name__
    self.func = None
    for funcname in ['print_properties', 'print_quark_properties']:
      try:
        self.func = getattr(self.classobj, funcname)
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
    return UTState.PASS, [f"{uRArrow}"] + lines

##-
class utPrintRegistered(UT):
  """ Unit test print registered quark family. """
  def __init__(self, dskey):
    UT.__init__(self, "family", dskey)

  def begin(self, sequencer, datum):
    return (f"registered.family", UTState.PASS)

  def test(self, sequencer, datum):
    family = [(name,cls) for name,cls in sut.Quark.quark_family().items()]
    with io.StringIO() as output:
      print2cols(family, indent=2, file=output)
      lines = output.getvalue().split('\n')
    if not lines[-1]:
      lines = lines[:-1]
    return UTState.PASS, [f"{uRArrow}"] + lines

##-
class utNew(UT):
  """ Unit test quark instantiation. """
  def __init__(self, dskey, classobj, dskey_out):
    UT.__init__(self, "new", dskey)
    self.classobj = classobj
    self.dskeyOut = dskey_out
    self.dsTmp = UTDataset(self.dskeyOut, data=[])

  def begin(self, sequencer, datum):
    self.color  = datum
    self.pf     = UTState.PASS
    return (f"{self.classobj.__name__}({self.color})", self.pf)

  def test(self, sequencer, datum):
    try:
      q = self.classobj(self.color)
    except (TypeError, ValueError) as e:
      return (UTState.FAIL, [f"{uRArrow}", f"Error: {e}"])
    else:
      self.dsTmp.append(q)
      return (UTState.PASS, f"{uRArrow} {q}({q.color_charge})")

  def finalize(self, sequencer):
    if len(self.dsTmp) > 0:
      sequencer.dsdb[self.dskeyOut] = self.dsTmp.copy()
      print(f"       (dataset {self.dskeyOut!r} added to database)")

##-
class utPrintState(UT):
  """ Unit test print state methods. """
  def __init__(self, dskey):
    UT.__init__(self, "print_state", dskey)

  def begin(self, sequencer, datum):
    return (f"{datum}.print_state()", UTState.PASS)

  def test(self, sequencer, datum):
    with io.StringIO() as output:
      datum.print_state(indent=2, file=output)
      lines = output.getvalue().split('\n')
    if not lines[-1]:
      lines = lines[:-1]
    return UTState.PASS, [f"{uRArrow}"] + lines

# -----------------------------------------------------------------------------
# Unit Test Data
# -----------------------------------------------------------------------------

# datasets
dsBase    = UTDataset('ds_base', data=[sut.Quark])
dsFamily  = UTDataset('ds_family',
    data=[cls for name,cls in sut.Quark.quark_family().items()])
dsColor     = UTDataset('ds_color', data=list(cc.PrimaryColors))
dsAntiColor = UTDataset('ds_anticolor', data=list(cc.AntiColors))

# the database of datasets
db = UTDsDb('db', ds=[dsBoilOne, dsBase, dsFamily, dsColor, dsAntiColor,])

# -----------------------------------------------------------------------------
# Unit Test Subsystem, Suite, Sequencer, and Main
# -----------------------------------------------------------------------------
suite = UTSuite('testsuite',
  subsystems=[
    UTSubsys('base',
      "Test Quark base class.",
      unittests=[
        utPrintProperties('ds_boil_one', classobj=sut.Quark),
        utPrintRegistered('ds_boil_one'),
      ]
    ),
    UTSubsys('up',
      "Test Quark derived Up class.",
      unittests=[
        utPrintProperties('ds_boil_one', classobj=sut.Up),
        utNew('ds_color', classobj=sut.Up, dskey_out='ds_up'),
        utPrintState('ds_up'),
      ]
    ),
    UTSubsys('antiup',
      "Test Quark derived AntiUp class.",
      unittests=[
        utPrintProperties('ds_boil_one', classobj=sut.AntiUp),
        utNew('ds_anticolor', classobj=sut.AntiUp, dskey_out='ds_antiup'),
        utPrintState('ds_antiup'),
      ]
    ),
    UTSubsys('down',
      "Test Quark derived Down class.",
      unittests=[
        utPrintProperties('ds_boil_one', classobj=sut.Down),
        utNew('ds_color', classobj=sut.Down, dskey_out='ds_down'),
        utPrintState('ds_down'),
      ]
    ),
    UTSubsys('antidown',
      "Test Quark derived AntiDown class.",
      unittests=[
        utPrintProperties('ds_boil_one', classobj=sut.AntiDown),
        utNew('ds_anticolor', classobj=sut.AntiDown, dskey_out='ds_antidown'),
        utPrintState('ds_antidown'),
      ]
    ),
    UTSubsys('charm',
      "Test Quark derived Charm class.",
      unittests=[
        utPrintProperties('ds_boil_one', classobj=sut.Charm),
        utNew('ds_color', classobj=sut.Charm, dskey_out='ds_charm'),
        utPrintState('ds_charm'),
      ]
    ),
    UTSubsys('anticharm',
      "Test Quark derived AntiCharm class.",
      unittests=[
        utPrintProperties('ds_boil_one', classobj=sut.AntiCharm),
        utNew('ds_anticolor', classobj=sut.AntiCharm, dskey_out='ds_anticharm'),
        utPrintState('ds_anticharm'),
      ]
    ),
    UTSubsys('strange',
      "Test Quark derived Strange class.",
      unittests=[
        utPrintProperties('ds_boil_one', classobj=sut.Strange),
        utNew('ds_color', classobj=sut.Strange, dskey_out='ds_strange'),
        utPrintState('ds_strange'),
      ]
    ),
    UTSubsys('antistrange',
      "Test Quark derived AntiStrange class.",
      unittests=[
        utPrintProperties('ds_boil_one', classobj=sut.AntiStrange),
        utNew('ds_anticolor', classobj=sut.AntiStrange,
                              dskey_out='ds_antistrange'),
        utPrintState('ds_antistrange'),
      ]
    ),
    UTSubsys('top',
      "Test Quark derived Top class.",
      unittests=[
        utPrintProperties('ds_boil_one', classobj=sut.Top),
        utNew('ds_color', classobj=sut.Top, dskey_out='ds_top'),
        utPrintState('ds_top'),
      ]
    ),
    UTSubsys('antitop',
      "Test Quark derived AntiTop class.",
      unittests=[
        utPrintProperties('ds_boil_one', classobj=sut.AntiTop),
        utNew('ds_anticolor', classobj=sut.AntiTop, dskey_out='ds_antitop'),
        utPrintState('ds_antitop'),
      ]
    ),
    UTSubsys('bottom',
      "Test Quark derived Bottom class.",
      unittests=[
        utPrintProperties('ds_boil_one', classobj=sut.Bottom),
        utNew('ds_color', classobj=sut.Bottom, dskey_out='ds_bottom'),
        utPrintState('ds_bottom'),
      ]
    ),
    UTSubsys('antibottom',
      "Test Quark derived AntiBottom class.",
      unittests=[
        utPrintProperties('ds_boil_one', classobj=sut.AntiBottom),
        utNew('ds_anticolor', classobj=sut.AntiBottom,
                              dskey_out='ds_antibottom'),
        utPrintState('ds_antibottom'),
      ]
    ),
  ],
)

utseq = UTSequencer('quark', suite, db)

utmain = lambda: UTMainTemplate(utseq, "Unit test quark module.")
