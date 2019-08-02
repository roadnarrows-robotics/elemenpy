"""
Unit test the common module.

Package:
  RoadNarrows elemenpy python package.

File:
  utcommon.py

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

from elemenpy.testing.ut import *
import elemenpy.core.common as sut

# -----------------------------------------------------------------------------
# Unit Test Data
# -----------------------------------------------------------------------------

# test of isiterable()
class Counter:
  def __init__(self, low, high):
    self.low = low
    self.high = high
    self.current = self.low
  
  def __str__(self):
    return f"Counter({self.low!r}, {self.high!r})"

  def __iter__(self):
    return self
  
  def __next__(self):
    if self.current > self.high:
      self.current = self.low
      self.high = self.high
      raise StopIteration
    else:
      n = self.current
      self.current += 1
      return n

class Quadrilateral:
  def __init__(self, a, b, c, d):
    self.a = a
    self.b = b
    self.c = c
    self.d = d

  def __str__(self):
    return f"Quadrilateral({self.a!r}, {self.b!r}, {self.c!r}, {self.d!r})"

class Rectangle(Quadrilateral):
  def __init__(self, w, h):
    Quadrilateral.__init__(self, w, h, w, h)

  def __str__(self):
    return f"Rectangle({self.a!r}, {self.b!r})"

  def area(self):
    return self.a * self.b

class Square(Rectangle):
  def __init__(self, s):
    Rectangle.__init__(self, s, s)

  def __str__(self):
    return f"Square({self.a!r})"

class OneTwoThree(Enum):
  one = 1
  two = 2
  three = 3

class OhBeauty(Enum):
  BLUE_SKY = 0
  GRAY_OCEAN = 1
  PURPLE_MOUNTAINS = 2
  AMBER_GRAIN = 5

l = [1, 1, 2, 3, 5, 8, 11]
s = "I'm a string!"
d = {'a': 'aardvark', 'b': 'baboon'} #, 'c': 'coyote'}
b = False
i = -34
f = 3.14
t = ('LSD', 'bift')

# isderived test dataset
dsIsDerived = UTDataset('ds_isderived',
  data = [(d, 'dict', True),  (s, 'str', True),
          (f, 'float', True), (l, 'list', True),
          (f, float, True), (l, list, True),
          (t, 'tuple', True), (b, 'bool', True),
          (i, 'int', True),
          (Quadrilateral, 'Quadrilateral', True),
          (Quadrilateral(4, 5, 2, 3), 'Quadrilateral', True),
          (Rectangle, 'Rectangle', True),
          (Rectangle(9, 11), 'Rectangle', True),
          (Rectangle(30, 20), 'Square', False),
          (Square, 'Square', True),
          (Square(8), 'Square', True),
          (Square(88), 'Rectangle', True),
          (Square(888), 'Quadrilateral', True),
          (Square, Quadrilateral, True),
          (Square(888), 'list', False),
          ]

)

# isiterable test dataset
dsIsIterable = UTDataset('ds_isiterable',
  data = [(l, True), (s, True), (d, True), (b, False),
          (i, False), (f, False), (t, True),
          (Counter(-3, 12), True),
          (Square(8), False),
          ]
)

# enumfactory dataset
dsEnumFactory = UTDataset('ds_enumfactory', 
  data = [(OneTwoThree, 1, True), (OneTwoThree, 4, False),
          (OneTwoThree, 'three', True), (OneTwoThree, 'THREE', False),
          (OhBeauty, 2, True),
          (OhBeauty, 'gray ocean', True),
          (OhBeauty, OneTwoThree.three, False),
          (OhBeauty, OneTwoThree.one, True),
          (OhBeauty, 'GRAY_OCEAN', True),
          ]
)

# random whole numbers dataset
dsN = UTDataset('ds_n',
    data = [0, 1, 2] + [random.randint(3,100000) for i in range(30)])

# the database of datasets
db = UTDsDb('db', ds=[dsIsDerived, dsIsIterable, dsEnumFactory, dsN])

# -----------------------------------------------------------------------------
# Unit Tests
# -----------------------------------------------------------------------------

class utIsDerived(UT):
  """ Unit test isderived(). """
  def __init__(self, dskey):
    UT.__init__(self, "isderived()", dskey)

  def begin(self, sequencer, datum):
    self.obj  = datum[0]
    self.isa  = datum[1]
    self.tf   = datum[2]
    return (f"isderived({self.obj}, {self.isa!r})", UTState.PASS)

  def test(self, sequencer, datum):
    tf = sut.isderived(self.obj, self.isa)
    if tf == self.tf:
      res = UTState.PASS
      ans = f"{uRArrow} {tf}"
    else:
      res = UTState.FAIL
      ans = [f"{uRArrow} {tf}",
              f"determined to be {tf} but should be {self.tf}"]
    return (res, ans)

class utIsIterable(UT):
  """ Unit test isiterable(). """
  def __init__(self, dskey):
    UT.__init__(self, "isiterable()", dskey)

  def begin(self, sequencer, datum):
    self.obj  = datum[0]
    self.tf   = datum[1]
    return (f"isiterable({self.obj})", UTState.PASS)

  def test(self, sequencer, datum):
    tf = sut.isiterable(self.obj)
    if tf == self.tf:
      res = UTState.PASS
      ans = f"{uRArrow} {tf}"
    else:
      res = UTState.FAIL
      ans = [f"{uRArrow} {tf}",
              f"determined to be {tf} but should be {self.tf}"]
    return (res, ans)

class utEnumFactory(UT):
  """ Unit test enumfactory(). """
  def __init__(self, dskey):
    UT.__init__(self, "enumfactory()", dskey)

  def begin(self, sequencer, datum):
    self.klass  = datum[0]
    self.value  = datum[1]
    self.tf     = datum[2]
    if self.tf:
      expect = UTState.PASS
    else:
      expect = UTState.FAIL
    return (f"enumfactory({self.klass.__name__}, {self.value!r})", expect)

  def test(self, sequencer, datum):
    try:
      enu = enumfactory(self.klass, self.value)
      res = UTState.PASS
      ans = f"{uRArrow} {enu}"
    except (TypeError, ValueError) as e:
      res = UTState.FAIL
      ans = [f"{uRArrow} error", f"{e}"]
    return (res, ans)

class utPrimeFactorization(UT):
  """ Unit test prime_factorization(). """
  def __init__(self, dskey):
    UT.__init__(self, "prime_factorization()", dskey)

  def begin(self, sequencer, datum):
    return (f"prime_factorization({datum})", UTState.PASS)

  def test(self, sequencer, datum):
    primes = sut.prime_factorization(datum)
    m = self.validate(datum, primes)
    if m == datum:
      res = UTState.PASS
      ans = [ f"{uRArrow} factored into {len(primes)} primes", f"{primes}" ]
    else:
      res = UTState.FAIL
      ans = [ f"{uRArrow} {datum} {uNeq} {m}", f"{primes}" ]
    return res, ans

  def validate(self, n, primes):
    if len(primes) == 0:
      return n
    m = 1
    for p in primes:
      m *= p
    return m

# -----------------------------------------------------------------------------
# Unit Test Subsystem, Suite, Sequencer, and Main
# -----------------------------------------------------------------------------
suite = UTSuite('testsuite',
  subsystems=[
    UTSubsys('isa', "Test 'is a' functions.",
      unittests=[
        utIsDerived('ds_isderived'),
        utIsIterable('ds_isiterable'),
      ]
    ),
    UTSubsys('enum', "Test enumeration functions.",
      unittests=[
        utEnumFactory('ds_enumfactory'),
      ]
    ),
    UTSubsys('numbers', "Test numbers functions.",
      unittests=[
        utPrimeFactorization('ds_n'),
      ]
    ),
  ],
)

utseq = UTSequencer('common', suite, db)

utmain = lambda: UTMainTemplate(utseq, "Unit test common module.")
