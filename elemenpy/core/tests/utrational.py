"""
Unit test the rational module.

Package:
  RoadNarrows elemenpy python package.

File:
  utrational.py

Link:
  https://github.com/roadnarrows-robotics/

Copyright:
  (c) 2019. RoadNarrows LLC
  http://www.roadnarrows.com
  All Rights Reserved

License:
  MIT
"""
import random
from enum import Enum
import io
from copy import copy


from elemenpy.testing.ut import *
from elemenpy.core.format import default_encoder

import elemenpy.core.rational as sut

# -----------------------------------------------------------------------------
# Unit Test Data
# -----------------------------------------------------------------------------

# Notes:
#   If dataset name contains '.raw' than must convert with factory.
#   If dataset name contains '.error' than all failures.

# unit test dataset 1: (what, Q instance)
ds1 = UTDataset('ds1',
        data = [
          ("Q(0)",                sut.Q(0)),
          ("Q(1)",                sut.Q(1)),
          ("Q(1,2)",              sut.Q(1, 2)),
          ("Q(23,3)",             sut.Q(23, 3)),
          ("Q(3,8)",              sut.Q(3, 8)),
          ("Q(2x2x5x53,2x5x37)",  sut.Q(2*2*5*53, 2*5*37)),
          ("Q(9,-16)",            sut.Q(9, -16)),
        ])

# unit test dataset 2: (what, Q instance)
ds2Raw = UTDataset('ds2.raw',
        data = [
          ("Q(1/2)",            sut.Q(1, 2)),
          ("(4,-3)",            (4, -3)),
          ("{'p':44, 'q':45}",  {'p': 44, 'q': 45}), 
          ("-99",               -99),
          ("1/3",               1/3),
          ("1/4",               1/4),
        ])


# unit test dataset of non-convertible Q's
ds3Raw = UTDataset('ds3.raw.error',
        data = [
          ('"hello"', "hello"),
          ("(None)",  (None)),
          ("[12]",    [12]),
          ("dict",    {'monkey': 'sees', 'man': 'apes'}),
        ])

# dataset 3 is datasets 1 and 2
ds4Raw      = ds1 + ds2Raw
ds4Raw.name = 'ds4.raw'

# unit test dataset 4: (what, Q instance)
ds5Raw = UTDataset('ds5.raw',
        data = [
          ("Q(2)",        sut.Q(2)),
          ("(7, 11)",     (7, 11)),
          ("-5",          -5),
          ("Q(46, 6)",    sut.Q(46,6)),
          ("Q(9,10)",     sut.Q(9, 10)),
          ("[-89, -20]",  [-89, -20]),
          ("0",           0),           # will raise exceptions in some cases
          ("Q(3,2)",      sut.Q(3, 2)),
        ])

# the database of datasets
db = UTDsDb('db', ds=[ds1, ds2Raw, ds3Raw, ds4Raw, ds5Raw])

# -----------------------------------------------------------------------------
# Unit Tests
# -----------------------------------------------------------------------------
class utQstr(UT):
  """ Unit test Q.str(). """
  def __init__(self, dskey):
    UT.__init__(self, "Q.__str__()", dskey)

  def begin(self, sequencer, datum):
    self.what   = datum[0]
    self.value  = datum[1]
    return (f"str({self.what})", UTState.PASS)

  def test(self, sequencer, datum):
    try:
      s = str(self.value)
    except (NameError) as e:
      return UTState.FAIL, [f"{uRArrow} error", f"{e}"]
    else:
      return UTState.PASS, f"{uRArrow} {s}"

class utQcall(UT):
  """ Unit test Q(). """
  def __init__(self, dskey):
    UT.__init__(self, "Q__call__()", dskey)

  def begin(self, sequencer, datum):
    self.what   = datum[0]
    self.value  = datum[1]
    return (f"str({self.what})", UTState.PASS)

  def test(self, sequencer, datum):
    try:
      s = self.value()
    except (TypeError) as e:
      return UTState.FAIL, [f"{uRArrow} error", f"{e}"]
    else:
      return UTState.PASS, f"{uRArrow} {s}"

class utQfactory(UT):
  """ Unit test Q.from_value(). """
  def __init__(self, dskey):
    UT.__init__(self, "Q.from_value()", dskey)

    # if dataset name has .error it all bad
    i = dskey.find('.error')
    if i < 0:
      self.pf = UTState.PASS
    else:
      self.pf = UTState.FAIL

    # if dataset name has .raw then update converted to db
    i = dskey.find('.raw')
    if i < 0:
      self.bAdd = False
    else:
      self.bAdd     = True
      self.dskeyAdd = dskey[:i]

    self.dsAdd = UTDataset('temp', data=[])

  def begin(self, sequencer, datum):
    self.what   = datum[0]
    self.value  = datum[1]
    return (f"Q.from_value({self.what})", self.pf)

  def test(self, sequencer, datum):
    try:
      q = sut.Q.from_value(self.value)
    except (TypeError, ValueError) as e:
      return UTState.FAIL, [f"{uRArrow} error", f"{e}"]
    else:
      self.dsAdd.append((f"Q{q()}", q))
      return UTState.PASS, f"{uRArrow} {q}"

  def end(self, sequencer):
    pass

  def finalize(self, sequencer):
    if self.bAdd and self.stats.failed == 0:
      self.dsAdd.name = self.dskeyAdd
      sequencer.dsdb[self.dskeyAdd] = self.dsAdd.copy()
      print(f"(dataset {self.dskeyAdd!r} added to database.)")

class utQrepr(UT):
  """ Unit test Q.repr(). """
  def __init__(self, dskey):
    UT.__init__(self, "Q.__repr__()", dskey)

  def begin(self, sequencer, datum):
    self.what   = datum[0]
    self.value  = datum[1]
    return (f"repr({self.what})", UTState.PASS)

  def test(self, sequencer, datum):
    try:
      s = repr(self.value)
    except (NameError) as e:
      return UTState.FAIL, [f"{uRArrow} error", f"{e}"]
    else:
      return UTState.PASS, f"{uRArrow} {s}"

class utQadd(UT):
  """ Unit test Q.__add__(). """
  def __init__(self, dskey, dskey2):
    UT.__init__(self, "Q.__add__()", dskey, dskey2)
    self.rhs = UTDsAux(self.args[0])

  def reset(self):
    UT.reset(self)
    self.rhs.reset()

  def prep(self, sequencer):
    UT.prep(self, sequencer)
    self.rhs.prep(sequencer)

  def begin(self, sequencer, datum):
    self.a = datum[1]
    self.b = self.rhs.datum()[1]
    return  (f"{self.a} + {self.b}", UTState.PASS)

  def test(self, sequencer, datum):
    try:
      c = self.a + self.b
    except (TypeError, NameError) as e:
      return UTState.FAIL, [f"{uRArrow} error", f"{e}"]
    else:
      return UTState.PASS, f"= {c}"

  def end(self, sequencer):
    self.rhs += 1

class utQsub(UT):
  """ Unit test Q.__sub__(). """
  def __init__(self, dskey, dskey2):
    UT.__init__(self, "Q.__sub__()", dskey, dskey2)
    self.rhs = UTDsAux(self.args[0])

  def reset(self):
    UT.reset(self)
    self.rhs.reset()

  def prep(self, sequencer):
    UT.prep(self, sequencer)
    self.rhs.prep(sequencer)

  def begin(self, sequencer, datum):
    self.a = datum[1]
    self.b = self.rhs.datum()[1]
    return  (f"{self.a} - {self.b}", UTState.PASS)

  def test(self, sequencer, datum):
    try:
      c = self.a - self.b
    except (TypeError, NameError) as e:
      return UTState.FAIL, [f"{uRArrow} error", f"{e}"]
    else:
      return UTState.PASS, f"= {c}"

  def end(self, sequencer):
    self.rhs += 1

class utQmul(UT):
  """ Unit test Q.__mul__(). """
  def __init__(self, dskey, dskey2):
    UT.__init__(self, "Q.__mul__()", dskey, dskey2)
    self.rhs = UTDsAux(self.args[0])

  def reset(self):
    UT.reset(self)
    self.rhs.reset()

  def prep(self, sequencer):
    UT.prep(self, sequencer)
    self.rhs.prep(sequencer)

  def begin(self, sequencer, datum):
    self.a = datum[1]
    self.b = self.rhs.datum()[1]
    return  (f"{self.a} * {self.b}", UTState.PASS)

  def test(self, sequencer, datum):
    try:
      c = self.a * self.b
    except (TypeError, NameError) as e:
      return UTState.FAIL, [f"{uRArrow} error", f"{e}"]
    else:
      return UTState.PASS, f"= {c}"

  def end(self, sequencer):
    self.rhs += 1

class utQdiv(UT):
  """ Unit test Q.__div__(). """
  def __init__(self, dskey, dskey2):
    UT.__init__(self, "Q.__truediv__()", dskey, dskey2)
    self.rhs = UTDsAux(self.args[0])

  def reset(self):
    UT.reset(self)
    self.rhs.reset()

  def prep(self, sequencer):
    UT.prep(self, sequencer)
    self.rhs.prep(sequencer)

  def begin(self, sequencer, datum):
    self.a = datum[1]
    self.b = self.rhs.datum()[1]
    return  (f"{self.a} / {self.b}", self.expect(self.b))

  def test(self, sequencer, datum):
    try:
      c = self.a / self.b
    except (TypeError, NameError) as e:
      return UTState.FAIL, [f"{uRArrow} error", f"{e}"]
    except (ZeroDivisionError) as e:
      return UTState.FAIL, [f"{uRArrow} error", f"{e}"]
    else:
      return UTState.PASS, f"= {c}"

  def end(self, sequencer):
    self.rhs += 1

  def expect(self, b):
    q = sut.Q.from_value(b)
    if q == 0:
      return UTState.FAIL
    else:
      return UTState.PASS

class utQfloor(UT):
  """ Unit test Q.__div__(). """
  def __init__(self, dskey, dskey2):
    UT.__init__(self, "Q.__floordiv__()", dskey, dskey2)
    self.rhs = UTDsAux(self.args[0])

  def reset(self):
    UT.reset(self)
    self.rhs.reset()

  def prep(self, sequencer):
    UT.prep(self, sequencer)
    self.rhs.prep(sequencer)

  def begin(self, sequencer, datum):
    self.a = datum[1]
    self.b = self.rhs.datum()[1]
    return  (f"{self.a} // {self.b}", self.expect(self.b))

  def test(self, sequencer, datum):
    try:
      c = self.a // self.b
    except (TypeError, NameError) as e:
      return UTState.FAIL, [f"{uRArrow} error", f"{e}"]
    except (ZeroDivisionError) as e:
      return UTState.FAIL, [f"{uRArrow} error", f"{e}"]
    else:
      return UTState.PASS, f"= {c}"

  def end(self, sequencer):
    self.rhs += 1

  def expect(self, b):
    q = sut.Q.from_value(b)
    if q == 0:
      return UTState.FAIL
    else:
      return UTState.PASS

class utQmod(UT):
  """ Unit test Q.__mod__(). """
  def __init__(self, dskey, dskey2):
    UT.__init__(self, "Q.__mod__()", dskey, dskey2)
    self.rhs = UTDsAux(self.args[0])

  def reset(self):
    UT.reset(self)
    self.rhs.reset()

  def prep(self, sequencer):
    UT.prep(self, sequencer)
    self.rhs.prep(sequencer)

  def begin(self, sequencer, datum):
    self.a = datum[1]
    self.b = self.rhs.datum()[1]
    return  (f"{self.a} % {self.b}", self.expect(self.b))

  def test(self, sequencer, datum):
    try:
      c = self.a % self.b
    except (TypeError, NameError) as e:
      return UTState.FAIL, [f"{uRArrow} error", f"{e}"]
    except (ZeroDivisionError) as e:
      return UTState.FAIL, [f"{uRArrow} error", f"{e}"]
    else:
      return UTState.PASS, f"= {c}"

  def end(self, sequencer):
    self.rhs += 1

  def expect(self, b):
    q = sut.Q.from_value(b)
    if q == 0:
      return UTState.FAIL
    else:
      return UTState.PASS

class utQcop(UT):
  # bad boy, ...
  BinCop = {
    'lt': {'sym': default_encoder('$math(<)'),    'op': lambda a, b: a < b},
    'le': {'sym': default_encoder('$math(<=)'),   'op': lambda a, b: a <= b},
    'eq': {'sym': default_encoder('$math(=)')*2,  'op': lambda a, b: a == b},
    'ge': {'sym': default_encoder('$math(>=)'),   'op': lambda a, b: a >= b},
    'gt': {'sym': default_encoder('$math(>)'),    'op': lambda a, b: a > b},
    'ne': {'sym': default_encoder('$math(!=)'),   'op': lambda a, b: a != b},
  }

  """ Unit test Q.__<cop>__().  binary comparison operator """
  def __init__(self, dskey, dskey2, **kwargs):
    UT.__init__(self, "Q.__<cop>__()", dskey, dskey2, **kwargs)
    self.rhs  = UTDsAux(self.args[0])
    self.cop  = self.kwargs['cop']
    self.name = f"Q.__{self.cop}__()"

  def reset(self):
    UT.reset(self)
    self.rhs.reset()

  def prep(self, sequencer):
    UT.prep(self, sequencer)
    self.rhs.prep(sequencer)

  def begin(self, sequencer, datum):
    self.a = datum[1]
    self.b = self.rhs.datum()[1]
    self.copSym = utQcop.BinCop[self.cop]['sym']
    self.copOp  = utQcop.BinCop[self.cop]['op']
    return  (f"{self.a} {self.copSym} {self.b}", UTState.PASS)

  def test(self, sequencer, datum):
    try:
      tf = self.copOp(self.a, self.b)
    except (TypeError, NameError) as e:
      return UTState.FAIL, [f"{uRArrow} error", f"{e}"]
    else:
      res, details = self.verify(tf, 0.00001)
      return res, f"{uRArrow} {tf} " + details

  def end(self, sequencer):
    self.rhs += 1

  def verify(self, tf, epsilon):
    """
    Verify comparative operator result.

    Parameters:
      tf      Result of applying the operator to two rationals.
      epsilon Epsilon accuracy. Used for floating-point rounding (TBD).
    """
    a = self.a.fpn()
    b = sut.Q.from_value(self.b).fpn()
    diff  = a - b   # a cop b => a - b cop 0
    truth = self.copOp(a, b)
    delta = default_encoder('$greek(Delta)')
    if tf == truth:
      res = UTState.PASS
    else:
      res = UTState.FAIL
    details = f"({a:.3} {self.copSym} {b:.3}? {delta}{diff:.3})"
    return res, details

class utQprimes(UT):
  """ Unit test Q.primes(). """
  def __init__(self, dskey):
    UT.__init__(self, "Q.primes()", dskey)

  def begin(self, sequencer, datum):
    return (f"{str(datum[1])}", UTState.PASS)

  def test(self, sequencer, datum):
    q = datum[1]
    try:
      pfn, pfd = q.primes()
    except (NameError, ValueError, TypeError) as e:
      return UTState.FAIL, [f"{uRArrow} error", f"{e}"]
    else:
      return UTState.PASS, f"{uRArrow} {pfn}/{pfd}"

class utQgcd(UT):
  """ Unit test Q.gcd(). """
  def __init__(self, dskey):
    UT.__init__(self, "Q.gcd()", dskey)

  def begin(self, sequencer, datum):
    return (f"{str(datum[1])}", UTState.PASS)

  def test(self, sequencer, datum):
    q = datum[1]
    try:
      gcd = q.gcd()
    except (NameError, ValueError, TypeError) as e:
      return UTState.FAIL, [f"{uRArrow} error", f"{e}"]
    else:
      return UTState.PASS, f"{uRArrow} {gcd}"

class utQlcm(UT):
  """ Unit test Q.lcm(). """
  def __init__(self, dskey):
    UT.__init__(self, "Q.lcm()", dskey)

  def begin(self, sequencer, datum):
    return (f"{str(datum[1])}", UTState.PASS)

  def test(self, sequencer, datum):
    q = datum[1]
    try:
      lcm = q.lcm()
    except (NameError, ValueError, TypeError) as e:
      return UTState.FAIL, [f"{uRArrow} error", f"{e}"]
    else:
      return UTState.PASS, f"{uRArrow} {lcm}"

class utQcanonical(UT):
  """ Unit test Q.canonical(). """
  def __init__(self, dskey):
    UT.__init__(self, "Q.canonical()", dskey)

  def begin(self, sequencer, datum):
    return (f"{str(datum[1])}", UTState.PASS)

  def test(self, sequencer, datum):
    q = copy(datum[1])
    try:
      q.canonical()
    except (NameError, ValueError, TypeError) as e:
      return UTState.FAIL, [f"{uRArrow} error", f"{e}"]
    else:
      return UTState.PASS, f"{uRArrow} {q}"

# -----------------------------------------------------------------------------
# Unit Test Subsystem, Suite, Sequencer, and Main
# -----------------------------------------------------------------------------
suite = UTSuite('testsuite',
  subsystems=[
    UTSubsys('str', "Test str(Q).",
      unittests=[
        utQstr('ds1'),
      ]
    ),
    UTSubsys('call', "Test Q().",
      unittests=[
        utQcall('ds1'),
      ]
    ),
    UTSubsys('factory', "Test Q = Q.factory_value() factory class method.",
      unittests=[
        utQfactory('ds1'),
        utQfactory('ds2.raw'),
        utQfactory('ds3.raw.error'),
        utQfactory('ds4.raw'),
        utQfactory('ds5.raw'),
      ]
    ),
    UTSubsys('repr', "Test Q.repr().",
      unittests=[
        utQrepr('ds1'),
        utQrepr('ds2'),
        utQrepr('ds4'),
        utQrepr('ds5'),
      ],
      prereqs=['factory']
    ),
    UTSubsys('add', "Test addition Q + value.",
      unittests=[
        utQadd('ds4', 'ds5.raw'),
      ],
      prereqs=['factory']
    ),
    UTSubsys('sub', "Test subtraction Q - value.",
      unittests=[
        utQsub('ds4', 'ds5.raw'),
      ],
      prereqs=['factory']
    ),
    UTSubsys('mul', "Test multiplication Q * value.",
      unittests=[
        utQmul('ds4', 'ds5.raw'),
      ],
      prereqs=['factory']
    ),
    UTSubsys('div', "Test true division Q / value.",
      unittests=[
        utQdiv('ds4', 'ds5.raw'),
      ],
      prereqs=['factory']
    ),
    UTSubsys('floor', "Test floor division Q // value.",
      unittests=[
        utQfloor('ds4', 'ds5.raw'),
      ],
      prereqs=['factory']
    ),
    UTSubsys('mod', "Test modulo Q % value.",
      unittests=[
        utQmod('ds4', 'ds5.raw'),
      ],
      prereqs=['factory']
    ),
    UTSubsys('cop', "Test binary compare operators Q <cop> value.",
      unittests=[
        utQcop('ds4', 'ds5.raw', cop="lt"),
        utQcop('ds4', 'ds5.raw', cop="le"),
        utQcop('ds4', 'ds5.raw', cop="eq"),
        utQcop('ds4', 'ds5.raw', cop="ge"),
        utQcop('ds4', 'ds5.raw', cop="gt"),
        utQcop('ds4', 'ds5.raw', cop="ne"),
      ],
      prereqs=['factory']
    ),
    UTSubsys('primes', "Test prime factorization Q.primes().",
      unittests=[
        utQprimes('ds4'),
        utQprimes('ds5'),
      ],
      prereqs=['factory']
    ),
    UTSubsys('gcd', "Test Greatest Common Divisor Q.gcd().",
      unittests=[
        utQgcd('ds4'),
        utQgcd('ds5'),
      ],
      prereqs=['factory']
    ),
    UTSubsys('lcm', "Test Least Common Multiple Q.lcm().",
      unittests=[
        utQlcm('ds4'),
        utQlcm('ds5'),
      ],
      prereqs=['factory']
    ),
    UTSubsys('canonical', "Test canonicalization Q.canonical().",
      unittests=[
        utQcanonical('ds4'),
        utQcanonical('ds5'),
      ],
      prereqs=['factory']
    ),
  ],
)

utseq = UTSequencer('rational', suite, db)

utmain = lambda: UTMainTemplate(utseq, "Unit test rational module.")
