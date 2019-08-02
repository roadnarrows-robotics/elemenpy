"""
Unit test the meson module.

Package:
  RoadNarrows elemenpy python package.

File:
  utmeson.py

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

from elemenpy.core.prettyprint import (print2cols)

from elemenpy.testing.ut import *

from elemenpy.sm.colorcharge import ColorCharge as cc
import elemenpy.sm.meson as sut

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
    for funcname in ['print_properties', 'print_meson_properties']:
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
  """ Unit test print registered meson family. """
  def __init__(self, dskey):
    UT.__init__(self, "family", dskey)

  def begin(self, sequencer, datum):
    return (f"registered.family", UTState.PASS)

  def test(self, sequencer, datum):
    family = [(name,cls) for name,cls in sut.Meson.meson_family().items()]
    with io.StringIO() as output:
      print2cols(family, indent=2, file=output)
      lines = output.getvalue().split('\n')
    if not lines[-1]:
      lines = lines[:-1]
    return UTState.PASS, [f"{uRArrow}"] + lines

##-
class utNew(UT):
  """ Unit test meson instantiation. """
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
      m = self.classobj(self.color)
    except (TypeError, ValueError) as e:
      return (UTState.FAIL, [f"{uRArrow}", f"Error: {e}"])
    else:
      self.dsTmp.append(m)
      return (UTState.PASS, f"{uRArrow} {m}(...)")

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
# null and singleton datasets
dsBase    = UTDataset('ds_base', data=[sut.Meson])
dsFamily  = UTDataset('ds_family',
    data=[cls for name,cls in sut.Meson.meson_family().items()])
dsColor   = UTDataset('ds_color', data=list(cc.PrimaryColors))

# the database of datasets
db = UTDsDb('db', ds=[dsBoilOne, dsBase, dsFamily, dsColor])

# -----------------------------------------------------------------------------
# Unit Test Subsystem, Suite, Sequencer, and Main
# -----------------------------------------------------------------------------
suite = UTSuite('testsuite',
  subsystems=[
    UTSubsys('base',
      "Test Meson bass class.",
      unittests=[
        utPrintProperties('ds_boil_one', classobj=sut.Meson),
        utPrintRegistered('ds_boil_one'),
      ]
    ),
    UTSubsys('pion+',
      "Test Meson derived PionP class.",
      unittests=[
        utPrintProperties('ds_boil_one', classobj=sut.PionP),
        utNew('ds_color', classobj=sut.PionP, dskey_out='ds_pion+'),
        utPrintState('ds_pion+'),
      ]
    ),
    UTSubsys('pion-',
      "Test Meson derived PionN class.",
      unittests=[
        utPrintProperties('ds_boil_one', classobj=sut.PionN),
        utNew('ds_color', classobj=sut.PionN, dskey_out='ds_pion-'),
        utPrintState('ds_pion-'),
      ]
    ),
    UTSubsys('pion0',
      "Test Meson derived Pion0 class.",
      unittests=[
        utPrintProperties('ds_boil_one', classobj=sut.Pion0),
        utNew('ds_color', classobj=sut.Pion0, dskey_out='ds_pion0'),
        utPrintState('ds_pion0'),
      ]
    ),
    UTSubsys('kaon+',
      "Test Meson derived KaonP class.",
      unittests=[
        utPrintProperties('ds_boil_one', classobj=sut.KaonP),
        utNew('ds_color', classobj=sut.KaonP, dskey_out='ds_kaon+'),
        utPrintState('ds_kaon+'),
      ]
    ),
    UTSubsys('kaon-',
      "Test Meson derived KaonN class.",
      unittests=[
        utPrintProperties('ds_boil_one', classobj=sut.KaonN),
        utNew('ds_color', classobj=sut.KaonN, dskey_out='ds_kaon-'),
        utPrintState('ds_kaon-'),
      ]
    ),
  ],
)

utseq = UTSequencer('meson', suite, db)

utmain = lambda: UTMainTemplate(utseq, "Unit test meson module.")
