"""
An olio of useful data types and functions.

Package:
  RoadNarrows elemenpy package.

File:
  common.py

Link:
  https://github.com/roadnarrows-robotics/

Copyright:
  (c) 2019. RoadNarrows LLC
  http://www.roadnarrows.com
  All Rights Reserved

License:
  MIT
"""

import sys

# RDK needs work - only executes after module is imported which is too late
assert sys.version_info >= (3, 6)

import shutil
import inspect
from enum import Enum
import random
import string

##-
def isderivedclass(klass, parent):
  """
  Test if klass is derived from a parent class.

  Parameters:
    klass   A <class 'klass'> object.
    parent  Class type or string name of the parent class.

  Returns
    True or False.
  """
  try:
    name = parent.__name__
  except AttributeError:
    name = parent
  return name in [c.__name__ for c in inspect.getmro(klass)]

##-
def isderivedinstance(instance, parent):
  """
  Test if instance is derived from a parent class.

  Parameters:
    instance  Instance object.
    parent    Class type or string name of the parent class.

  Returns
    True or False.
  """
  try:
    name = parent.__name__
  except AttributeError:
    name = parent
  return name in [c.__name__ for c in inspect.getmro(instance.__class__)]

##-
def isderived(obj, parent):
  """
  Test if class or instance object is derived from a parent class.

  Parameters:
    obj     Some pythonic object.
    parent  Class type or string name of the parent class.

  Returns
    True or False.
  """
  try:
    return isderivedclass(obj, parent)
  except AttributeError:
    try:
      return isderivedinstance(obj, parent)
    except AttributeError:
      return False
  except:
    return False

##-
def isiterable(obj):
  """
  Test if object is iterable.

  Python str, list, dict, and tuple are all builtin iterable types.

  Parameters:
    obj   Some pythonic object.
    name  String name of a parent class to test.

  Returns
    True or False.
  """
  try:
    _ = (e for e in obj)
    return True
  except TypeError:
    return False

#
# Some simple lambdas to convert an upper case, undersore enum name
# to a more readable lower case, whitespace string and vice versa.
#
enum_to_str     = lambda e, sep=' ': e.name.lower().replace('_', sep)
enumname_to_str = lambda n, sep=' ': n.lower().replace('_', sep)
str_to_enumname = lambda s: s.upper().replace(' ', '_').replace('-', '_')

##-
def enumfactory(klass, nv):
  """
  Create enum class instance from value.

  Parameters:
    klass   Enum class.
    nv      Enum name or value. One of type: enum, int, or str. For str, 
            various spellings are tried.

  Returns:
    Return klass enum instance.
  """
  if isinstance(nv, Enum):
    return klass(nv.value)
  elif type(nv) == int:
    return klass(nv)
  elif type(nv) == str:
    try:
      return klass(nv)                        # stet try as value
    except ValueError:
      try:
        return klass[nv]                      # stet try as name (key)
      except KeyError:
        try:
          return klass[str_to_enumname(nv)]   # try as massaged name (key)
        except KeyError:
          raise TypeError(f"'{v}': no enum matches string")
  else:
    raise TypeError(f"{v}: cannot convert to enum")

##-
def indexget(obj, i, default=None):
  """
  Return obj[i] if possible, else default.

  Similar to dict.get() but for integer indexed objects.
  """
  try:
    return obj[i]
  except (IndexError, TypeError, KeyError):
    return default

##-
def termsize():
  """
  Get the attached terminal's current size.

  Returns:
    The size as a 2-tuple (lines, columns).
  """
  sz = shutil.get_terminal_size((80, 24)) # size with fallback default
  return (sz.lines, sz.columns)

##-
def static_vars(**kwargs):
  """
  Attach static variables to a function.

  Usage:
    @static_vars(k1=v1, k2=k2, ...)
    def myfunc(...):
      myfunc.k1...
  
  Parameters:
    **kwargs  Keyword=value pairs converted to static variables in decorated
              function.

  Returns:
    decorate
  """
  def decorate(func):
    for k, v in kwargs.items():
      setattr(func, k, v)
    return func
  return decorate

##-
@static_vars(sieve_size=2*3*5,                        # modular sieve size
          sieve=[1, 7, 11, 13, 17, 19, 23, 29],       # sieve
          base=[2, 3, 5, 7, 11, 13, 17, 19, 23, 29])  # all primes < sieve_size
def prime_factorization(n):
  """
  Prime factorization of a non-negative integer (whole number).

  The modular sieve algorithm is used to factor.

  See: https://stackoverflow.com/questions/28382444/prime-factorization-python

  Parameters:
    n   Number to factor.

  Returns:
    List of primes in ascending order. Empty list [] for n = 0,1.
  """
  # factors
  f = []

  # cannot be negative
  n = abs(n)

  # 0 and 1 have no primes
  if n in [0, 1]:
    return f

  # remove factors of primes < sieve_size
  for p in prime_factorization.base:
    while n % p == 0:
      n //= p
      f.append(p)
    if n < p*p:
      break

  # remnant fully factored?
  if n < p*p:
    if n > 1:
      f.append(n)
    return f

  # remove factors of values generated by modular sieve
  #   (We do not need to test for actual primality
  #   because candidate values are generated in ascending order,
  #   if the value is composite, all factors of it will have
  #   already been removed)
  z = prime_factorization.sieve_size
  while True:
    for s in prime_factorization.sieve:
      b = z + s      # 31, 37, 41, 43, ...
      while n % b == 0:
        n //= b
        f.append(b)
      if n < b*b:
        break

    if n < b*b:
      if n > 1:
        f.append(n)
      return f
    z += prime_factorization.sieve_size

##-
def randomstring(strlen=12, prefix=''):
  """
  Generate a random string from the set of ascii letters and
  decimal digits.

  Parameters:
    strlen    Length of generated string including prefix.
    prefix    Prefix string to random string.

  Returns:
    String.
  """
  n = strlen - len(prefix)
  if n <= 0:
    return prefix[:strlen]
  src = string.ascii_letters + string.digits
  return prefix + ''.join(random.choice(src) for i in range(n))


# -----------------------------------------------------------------------------
# Unit tests
# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import sys
  import tests.utcommon as ut

  sys.exit(ut.utmain())
