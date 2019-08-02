"""
Unit test the standardmodel module.

Package:
  RoadNarrows elemenpy python package.

File:
  utstandardmodel.py

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

from elemenpy.core.format import (default_encoder,
                                  Format4Some,
                                  EncoderParseError)
from elemenpy.testing.ut import *

import elemenpy.sm.standardmodel as sut

# -----------------------------------------------------------------------------
# Unit Test Data
# -----------------------------------------------------------------------------
# null and singleton datasets
dsSmSymbols     = UTDataset('ds_sm_symbols', data=['sm'])
dsNullParticle  = UTDataset('ds_null_particle', data=[sut.NullParticle])
dsSubatomic     = UTDataset('ds_subatomic', data=[sut.SubatomicParticle])
dsSmPreSymbols  = UTDataset('ds_sm_pre_symbols',
    data=list(sut.StandardModel.SMMappingPre.values()))

# the database of datasets
db = UTDsDb('db', ds=[dsSmSymbols, dsNullParticle, dsSubatomic, dsSmPreSymbols])

# -----------------------------------------------------------------------------
# Unit Tests
# -----------------------------------------------------------------------------
class utPrintSymbols(UT):
  """ Unit test Standard Model symbols class. """
  def __init__(self, dskey, encoder=sut.default_encoder, in_ascii=False):
    self.encoder  = encoder
    self.in_ascii = in_ascii
    if self.in_ascii:
      UT.__init__(self, f"{encoder}.print_table(in_ascii)", dskey)
    else:
      UT.__init__(self, f"{encoder}.print_table()", dskey)

  def begin(self, sequencer, datum):
    self.tid = datum
    return f"{self.tid!r}", UTState.PASS

  def test(self, sequencer, datum):
    return UTState.PASS, f"{uRArrow} print"

  def end(self, sequencer):
    self.encoder.print_table(self.tid, in_ascii=self.in_ascii)

class utPrintParticle(UT):
  """ Unit test base particle print methods. """
  def __init__(self, dskey):
    UT.__init__(self, "properties", dskey)

  def begin(self, sequencer, datum):
    classobj  = datum
    classname = classobj.__name__
    self.func = None
    for funcname in [ 'print_properties',
                      'print_subatomic_properties',
                      'print_null_properties' ]:
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

class ut4Some(UT):
  """ Unit test Format4Some class. """
  def __init__(self, dskey):
    UT.__init__(self, f"Format4Some()", dskey)

  def begin(self, sequencer, datum):
    self.expr = datum
    return (f"{self.expr!r}", UTState.PASS)

  def test(self, sequencer, datum):
    try:
      fset = Format4Some(self.expr)
    except EncoderParseError as e:
      res = UTState.FAIL
      elines = str(e).split('\n')
      ans = [f"{uRArrow} error"] + elines
    else:
      with io.StringIO() as output:
        fset.print4(file=output)
        lines = output.getvalue().split('\n')
      if not lines[-1]:
        lines = lines[:-1]
      res = UTState.PASS
      ans = [f"{uRArrow}"] + lines
    return (res, ans)

# -----------------------------------------------------------------------------
# Unit Test Subsystem, Suite, Sequencer, and Main
# -----------------------------------------------------------------------------
suite = UTSuite('testsuite',
  subsystems=[
    UTSubsys('symbols',
      "Test SM symbol printing.",
      unittests=[
        utPrintSymbols('ds_sm_symbols'),
      ]
    ),
    UTSubsys('presymbols',
      "Test SM presymbol parsing on all 4 encodings.",
      unittests=[
        ut4Some('ds_sm_pre_symbols'),
      ]
    ),
    UTSubsys('particles',
      "Test SM base particle printing.",
      unittests=[
        utPrintParticle('ds_null_particle'),
        utPrintParticle('ds_subatomic'),
      ]
    ),
  ],
)

utseq = UTSequencer('standardmodel', suite, db)

utmain = lambda: UTMainTemplate(utseq, "Unit test standardmodel module.")
