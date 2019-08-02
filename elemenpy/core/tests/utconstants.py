"""
Unit test the constants module.

Package:
  RoadNarrows elemenpy python package.

File:
  utconstants.py

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

from elemenpy.core.format import (default_encoder,
                                  Format4Some,
                                  EncoderParseError)
from elemenpy.testing.ut import *

import elemenpy.core.constants as sut

# -----------------------------------------------------------------------------
# Unit Test Data
# -----------------------------------------------------------------------------
dsPhySymbols     = UTDataset('ds_phy_symbols', data=['phy'])

dsPhyPreSymbols  = UTDataset('ds_phy_pre_symbols',
    data=list(sut.Constant.PhyMappingPre.values()))

dsConstants = UTDataset('ds_constants', data=sut.constants) # all defined k's

dsBuiltins  = UTDataset('ds_builtins',
    data = [abs, bool, complex, float, int, repr, round, str, type])

dsBuiltins2 = UTDataset('ds_builtins2', data = [format, pow, round])

dsFMethod   = UTDataset('ds_fmethod',
    data = ['as_integer_ratio', 'hex', 'is_integer'])

dsRand1 = UTDataset('ds_rand1',
    data=[random.uniform(10e-10, 10e+10) for i in range(0,10)])

dsExp = UTDataset('ds_tinyn', data=[-2, -1, -0.5, 0, 1, 1, 1, 0.5, 1, 2])

# the database of datasets
db = UTDsDb('db',
    ds=[dsPhySymbols, dsPhyPreSymbols, dsConstants, dsBuiltins,
        dsBuiltins2, dsFMethod, dsRand1, dsExp])

# -----------------------------------------------------------------------------
# Unit Tests
# -----------------------------------------------------------------------------
class utPrintInfo(UT):
  """ Unit test constants print_info(). """
  def __init__(self, dskey):
    UT.__init__(self, "print_info()", dskey)

  def begin(self, sequencer, datum):
    return (f"{datum}", UTState.PASS)

  def test(self, sequencer, datum):
    with io.StringIO() as output:
      datum.print_info(file=output)
      olines = output.getvalue().split('\n')
    if not olines[-1]:
      olines = olines[:-1]
    return UTState.PASS, [f"{uRArrow} output info"] + olines

class utBuiltins(UT):
  """ Unit test built-ins on one constant. """
  def __init__(self, dskey):
    UT.__init__(self, "call(k)", dskey)

  def prep(self, sequencer):
    UT.prep(self, sequencer)
    self.k = copy(random.choice(sut.constants))

  def begin(self, sequencer, datum):
    self.funcname = datum.__name__
    return (f"{self.funcname}({self.k.symbol})", UTState.PASS)

  def test(self, sequencer, datum):
    output = datum(self.k)
    return UTState.PASS, f"= {output!r}"

class utBuiltins2(UT):
  """ Unit test built-ins on one constant plus argument. """
  BuiltArg = {
    'format': lambda k: "1.35",
    'pow':    lambda k: 0.5,
    'round':  lambda k: 10,
  }
  def __init__(self, dskey):
    UT.__init__(self, "call(k, arg)", dskey)

  def prep(self, sequencer):
    UT.prep(self, sequencer)
    self.k = copy(random.choice(sut.constants))

  def begin(self, sequencer, datum):
    self.funcname = datum.__name__
    self.arg = utBuiltins2.BuiltArg[self.funcname](self.k)
    return (f"{self.funcname}({self.k.symbol},{self.arg!r})", UTState.PASS)

  def test(self, sequencer, datum):
    output = datum(self.k, self.arg)
    return UTState.PASS, f"= {output!r}"

class utZeroArgs(UT):
  """ Unit test float calls with no arguments on one constant. """
  def __init__(self, dskey):
    UT.__init__(self, "k.call()", dskey)

  def prep(self, sequencer):
    UT.prep(self, sequencer)
    self.k = copy(random.choice(sut.constants))

  def begin(self, sequencer, datum):
    self.funcname = datum
    return (f"{self.k.symbol}.{self.funcname}()", UTState.PASS)

  def test(self, sequencer, datum):
    scall = f'self.k.{datum}()'
    output = eval(scall)
    return UTState.PASS, f"{uRArrow} {output!r}"

class utAop(UT):
  Binop = {
    'add':      {'sym': default_encoder('$math(+)'),  'op': lambda a, b: a + b},
    'sub':      {'sym': default_encoder('$math(-)'),  'op': lambda a, b: a - b},
    'mul':      {'sym': default_encoder('$math(*)'),  'op': lambda a, b: a * b},
    'truediv':  {'sym': default_encoder('$math(/)'),  'op': lambda a, b: a / b},
    'floordiv': {'sym': default_encoder('$math(/)')*2, 'op':lambda a,b: a // b},
    'mod':      {'sym': '%',                      'op': lambda a, b: a % b},
    'pow':      {'sym': '**',                     'op': lambda a, b: a ** b},
  }

  """ Unit test k.__<op>__().  binary arithmetic operator """
  def __init__(self, dskey, **kwargs):
    UT.__init__(self, "k.__<op>__()", dskey, **kwargs)
    self.op   = self.kwargs['op']
    self.name = f"k.__{self.op}__()"

  def prep(self, sequencer):
    UT.prep(self, sequencer)
    self.k  = copy(random.choice(sut.constants))
    expon   = math.floor(math.log(abs(self.k), 10)) 
    sequencer.dsdb[self.dskey][4] = math.pow(10.0, expon-1)
    sequencer.dsdb[self.dskey][5] = self.k
    sequencer.dsdb[self.dskey][6] = math.pow(10.0, expon+1)

  def begin(self, sequencer, datum):
    self.rhs    = datum
    self.opSym  = utAop.Binop[self.op]['sym']
    self.opOp   = utAop.Binop[self.op]['op']
    return (f"{self.k.symbol}: {self.k} {self.opSym} {self.rhs}",
            self.expect())

  def test(self, sequencer, datum):
    try:
      lhs = self.opOp(self.k, self.rhs)
    except (TypeError, NameError) as e:
      return UTState.FAIL, [f"{uRArrow} error", f"{e}"]
    except (ZeroDivisionError) as e:
      return UTState.FAIL, [f"{uRArrow} error", f"{e}"]
    else:
      return UTState.PASS, f"= {lhs}"

  def expect(self):
    if self.op in ['truediv', 'floordiv', 'mod']:
      if self.rhs == 0:
        return UTState.FAIL
    return UTState.PASS

class utCop(UT):
  Binop = {
    'lt': {'sym': default_encoder('$math(<)'),    'op': lambda a, b: a < b},
    'le': {'sym': default_encoder('$math(<=)'),   'op': lambda a, b: a <= b},
    'eq': {'sym': default_encoder('$math(=)')*2,  'op': lambda a, b: a == b},
    'ge': {'sym': default_encoder('$math(>=)'),   'op': lambda a, b: a >= b},
    'gt': {'sym': default_encoder('$math(>)'),    'op': lambda a, b: a > b},
    'ne': {'sym': default_encoder('$math(!=)'),   'op': lambda a, b: a != b},
  }

  """ Unit test k.__<op>__().  binary comparison operator """
  def __init__(self, dskey, **kwargs):
    UT.__init__(self, "k.__<op>__()", dskey, **kwargs)
    self.op  = self.kwargs['op']
    self.name = f"k.__{self.op}__()"

  def prep(self, sequencer):
    UT.prep(self, sequencer)
    self.k  = copy(random.choice(sut.constants))
    expon   = math.floor(math.log(abs(self.k), 10)) 
    sequencer.dsdb[self.dskey][4] = math.pow(10.0, expon-1)
    sequencer.dsdb[self.dskey][5] = self.k
    sequencer.dsdb[self.dskey][6] = math.pow(10.0, expon+1)

  def begin(self, sequencer, datum):
    self.rhs = datum
    self.opSym = utCop.Binop[self.op]['sym']
    self.opOp  = utCop.Binop[self.op]['op']
    return (f"{self.k.symbol}: {self.k} {self.opSym} {self.rhs}",
            UTState.PASS)

  def test(self, sequencer, datum):
    try:
      tf = self.opOp(self.k, self.rhs)
    except (TypeError, NameError) as e:
      return UTState.FAIL, [f"{uRArrow} error", f"{e}"]
    else:
      return UTState.PASS, f"= {tf}"

class utPrintSymbols(UT):
  """ Unit test physics symbols class. """
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
      "Test physics symbol printing.",
      unittests=[
        utPrintSymbols('ds_phy_symbols'),
      ]
    ),
    UTSubsys('presymbols',
      "Test physics presymbol parsing in all 4 encodings.",
      unittests=[
        ut4Some('ds_phy_pre_symbols'),
      ]
    ),
    UTSubsys('k', "Test printing information for all physics constants k.",
      unittests=[
        utPrintInfo('ds_constants'),
      ]
    ),
    UTSubsys('builtins',
      "Test python built-ins call(k) for random physics constant k.",
      unittests=[
        utBuiltins('ds_builtins'),
      ]
    ),
    UTSubsys('builtins2',
      "Test python built-ins call(k,arg2) for random physics constant k.",
      unittests=[
        utBuiltins2('ds_builtins2'),
      ]
    ),
    UTSubsys('noargs',
      "Test float methods k.call() for random physics constant k.",
      unittests=[
        utZeroArgs('ds_fmethod'),
      ]
    ),
    UTSubsys('aop', "Test binary arithmetic operators k <op> value.",
      unittests=[
        utAop('ds_rand1', op="add"),
        utAop('ds_rand1', op="sub"),
        utAop('ds_tinyn', op="mul"),
        utAop('ds_tinyn', op="truediv"),
        utAop('ds_tinyn', op="floordiv"),
        utAop('ds_tinyn', op="mod"),
        utAop('ds_tinyn', op="pow"),
      ]
    ),
    UTSubsys('cop', "Test binary compare operators k <op> value.",
      unittests=[
        utCop('ds_rand1', op="lt"),
        utCop('ds_rand1', op="le"),
        utCop('ds_rand1', op="eq"),
        utCop('ds_rand1', op="ge"),
        utCop('ds_rand1', op="gt"),
        utCop('ds_rand1', op="ne"),
      ]
    ),
  ],
)

utseq = UTSequencer('constants', suite, db)

utmain = lambda: UTMainTemplate(utseq, "Unit test constants module.")
