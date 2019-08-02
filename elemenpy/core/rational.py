"""
Rational numbers.

Package:
  RoadNarrows elemenpy package.

File:
  rational.py

Link:
  https://github.com/roadnarrows-robotics/

Copyright:
  (c) 2019. RoadNarrows LLC
  https://www.roadnarrows.com
  All Rights Reserved

License:
  MIT
"""

import sys
import math

from elemenpy.core.common import (enumfactory, prime_factorization)
from elemenpy.core.format import (Format, Format4Some)

# -----------------------------------------------------------------------------
# Class Q
# -----------------------------------------------------------------------------
class Q:
  """
  Rational number Q class.

  A rational number Q is any number p/q where p and q are integers
  with q != 0.
  """
  def __init__(self, p, q=1):
    """
    Initializer.

    Parameters:
      p   Integer numerator.
      q   Integer denominator != 0.
    """
    self.p = p
    self.q = q

  @classmethod
  def from_value(klass, value):
    """
    Q class instance factory method.

    Create Q instance from value.

    Parameters:
      klass   (Derived) Q class.
      value   Value object used to initialize.

    Returns:
      (Derived) Q instance.
    """
    try:    # is (derived) Q instance
      return klass(value.p, value.q)
    except AttributeError:
      pass

    try:    # is iterable or indexed object
      return klass(value[0], value[1])
    except (IndexError, TypeError, KeyError):
      pass

    try:    # is dictionary like object
      return klass(value['p'], value.get('q', [])) 
    except (KeyError, AttributeError, TypeError):
      pass

    # float or scalar int
    if isinstance(value, float):
      return Q.float_to_rational(value)
    else:
      return klass(value, 1)  # try it as a scalar number

  @classmethod
  def float_to_rational(klass, f):
    """
    Convert float to rational.

    Note: This works accurately but may generate large integer numerators
          and denominators, as the following interactive example
          demonstrates:
            >>> f = 1/3
            >>> f
            >>> 0.3333333333333333
            >>> n, d = f.as_integer_ratio()
            >>> n, d
            >>> (6004799503160661, 18014398509481984)
            >>> n/d
            >>> 0.3333333333333333

    Parameters:
      klass   (Derived) Q class.
      f       Floating-point number.

    Returns:
      (Derived) Q instance.
    """
    return Q(*f.as_integer_ratio())

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"({self._p!r}, {self._q!r})"

  def __str__(self):
    return self.notation()

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Python built-in functions
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

  def __abs__(self):
    # Absolute value. Returns abs(self). """
    return Q(abs(self.p), abs(self.q))

  def __bool__(self):
    # Absolute value. Returns bool(self). """
    return self.p != 0

  def __complex__(self):
    # Float value. Returns complex(self). """
    return complex(self.fpn())

  def __float__(self):
    # Float value. Returns float(self). """
    return self.fpn()

  def __int__(self):
    # Float value. Returns int(self). """
    return int(self.fpn())

  def __round__(self):
    # Float value. Returns int(self). """
    return round(self.fpn())


  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Arithmetic binary operators
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

  def __add__(self, value):
    """ Addition. Returns self + value. """
    v = self.from_value(value)
    if self.q == v.q:
      return Q(self.p + v.p, self.q)
    else:
      return Q(self.p * v.q + self.q * v.p, self.q * v.q)

  def __sub__(self, value):
    """ Subtraction. Returns self - value. """
    v = self.from_value(value)
    if self.q == v.q:
      return Q(self.p - v.p, self.q)
    else:
      return Q(self.p * v.q - self.q * v.p, self.q * v.q)

  def __mul__(self, value):
    """ Multiplication. Returns self * value. """
    v = self.from_value(value)
    return Q(self.p * v.p, self.q * v.q)

  def __truediv__(self, value):
    """ Division. Returns self / value. """
    v = self.from_value(value)
    return self * v.reciprocal()

  def __floordiv__(self, value):
    """ Floor division. Returns self // value. """
    v = self.from_value(value)
    return Q(int(self.fpn() // v.fpn()))

  def __mod__(self, value):
    """ Remainder. Returns self % value. """
    v = self.from_value(value)
    n = self // v
    r = self - n * v
    return r
    # An alternative method
    #a = self * (v.q, v.q)     # self with common denominator with v
    #b = v * (self.q, self.q)  # v with common denominator with self
    #r = a.p % b.p             # numerator remainder
    #return Q(r, a.q)          # remainder rational

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # In-place arithmetic operators
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

  def __iadd__(self, value):
    """ In-place addition. self += value. """
    v = self.from_value(value)
    if self.q == v.q:
      self.p += v.p
    else:
      self.p = self.p * v.q + self.q * v.p
      self.q = self.q * v.q
    return self

  def __isub__(self, value):
    """ In-place subtraction. self -= value. """
    v = self.from_value(value)
    if self.q == v.q:
      self.p -= v.p
    else:
      self.p = self.p * v.q - self.q * v.p
      self.q = self.q * v.q
    return self

  def __imul__(self, value):
    """ In-place multiplication. self *= value. """
    v = self.from_value(value)
    self.p = self.p * v.p
    self.q = self.q * v.q
    return self

  def __itruediv__(self, value):
    """ In-place division. self /= value. """
    v = self.from_value(value)
    self *= v.reciprocal()
    return self

  def __ifloordiv__(self, value):
    """ In-place floor division. self //= value. """
    self = self // v
    return self

  def __imod__(self, value):
    """ In-place remainder. self %= value. """
    v = self % value
    self.p = v.p
    self.q = v.q
    return self

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Comparison binary operators
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

  def __lt__(self, value):
    """ Less than. Return self < value. """
    v = self.from_value(value)
    return self.p * v.q < self.q * v.p

  def __le__(self, value):
    """ Less than or equal to. Return self <= value. """
    v = self.from_value(value)
    return self.p * v.q <= self.q * v.p

  def __eq__(self, value):
    """ Equal to. Return self == value. """
    v = self.from_value(value)
    return self.p * v.q == self.q * v.p

  def __ne__(self, value):
    """ Not equal to. Return self != value. """
    v = self.from_value(value)
    return self.p * v.q != self.q * v.p

  def __gt__(self, value):
    """ Greater than. Return self > value."""
    v = self.from_value(value)
    return self.p * v.q > self.q * v.p

  def __ge__(self, value):
    """ Greater than or equal to. Return self >= value. """
    v = self.from_value(value)
    return self.p * v.q >= self.q * v.p

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Unary operators
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Access 
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

  def __call__(self):
    """ Return rational as an integer 2-tuple. """
    return (self.p, self.q)

  def numerator(self):
    """ Return rational numerator (on top). """
    return self.p

  def denominator(self):
    """ Return rational numerator (on bottom). """
    return self.q

  def fpn(self):
    """ Return rational as a floating-point number. """
    return float(self.p) / float(self.q)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Common methods on rationals
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  def inverse(self):
    """ Return additive inverse of self. """
    return Q(-self.p, self.q)

  def reciprocal(self):
    """ Return multiplicative inverse of self. """
    if self.p != 0:
      return Q(self.q, self.p)
    else:
      raise ZeroDivisionError(f"no multiplicative inverse for zero") 

  def primes(self):
    """
    Prime factorizations of the rational number numerator and denominator.

    Returns:
      A 2-tuple of list of primes for the absolute values of the
      numerator and denominator. Primes are in ascending order.
    """
    return (prime_factorization(self.p), prime_factorization(self.q))

  def gcd(self):
    """
    Find the greatest common divisor between the numerator p and
    denominator q.

    Returns:
      Returs GCD. If p and q are relatively prime, 1 is returned.
    """
    _gcd = math.gcd(self.p, self.q)
    # locally grown alternative
    #pfn, pfd = self.primes()
    #_gcd = 1
    #for p in pfn:
    #  try:
    #    pfd.remove(p)
    #    _gcd *= p
    #  except ValueError:
    #    pass
    return _gcd

  def lcm(self):
    """
    Find the least common multiple of the numerator p and
    denominator q.

    Returns:
      Returs LCM. If rational is 0, 0 is returned.
    """
    if self.p == 0:
      return 0

    pfn, pfd = self.primes()
    _lcm = 1

    while len(pfn) > 0:
      p   = pfn[0]
      cn  = pfn.count(p)
      pfn = pfn[cn:]

      cd = pfd.count(p)
      if cd > 0:
        i = pfd.index(p)
        pfd = pfd[:i] + pfd[i+cd:]

      _lcm *= p ** max(cn, cd)

    for p in pfd:
      _lcm *= p

    return _lcm

  def canonical(self):
    """
    Canonicalize this rational.

    A canonical form of a rational is the irreducible fraction p/q
    where p and q are relative prime.
    """
    _gcd = self.gcd()
    self.p /= _gcd
    self.q /= _gcd
    if (self.p < 0 and self.q < 0) or self.q < 0:
      self.p = -self.p
      self.q = -self.q

  def notation(self, fmt=Format.UNICODE):
    """
    Create electron orbital notation formatted string.

    Output format:
      n/d   (plain)

      n
       /    (unicode, html, latex)
        d 

      where:
        n   numerator
        d   denomenator

    Parameters:
      fmt           Output string format. See the enum Format.
                    The value may also be the Format integer or
                    string equivalenct (e.g. 1, 'plain', 'LATEX').

    Returns:
      Formatted string.
    """
    fmt = enumfactory(Format, fmt)
    n = self.p  # numerator
    d = self.q  # denominator (always > 0)
    if n < 0:
      sign = '-'
      n = -n
    else:
      sign = ''
    if d == 1:
      return sign + str(n)
    encode = Format4Some(f'$frac({n},{d})')
    return sign + encode[fmt]

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Get/set properties
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

  @property
  def p(self):
    return self._p

  @p.setter
  def p(self, value):
    self._p = int(value)

  @property
  def q(self):
    return self._q

  @q.setter
  def q(self, value):
    v = int(value)
    if v == 0:  # can't be zero
      raise ZeroDivisionError(f"denominator cannot be zero")
    elif v < 0: # keep denominator positive
      self._p = -self._p
      self._q = -v
    else:
      self._q = v

# -----------------------------------------------------------------------------
# Unit tests
# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import sys
  import tests.utrational as ut

  sys.exit(ut.utmain())
