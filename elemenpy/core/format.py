"""
Output formatting control data and classes.

Package:
  RoadNarrows elemenpy package.

File:
  format.py

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
import os
from enum import Enum
import math
import string

from elemenpy.core.common import (termsize, enumfactory)

# -----------------------------------------------------------------------------
# Format Enumeration
# -----------------------------------------------------------------------------
class Format(Enum):
  """ Format types enumeration. """
  PLAIN   = 0   # plain ascii format
  UNICODE = 1   # extended unicode format
  HTML    = 2   # HTML format
  LATEX   = 3   # LaTeX format

# -----------------------------------------------------------------------------
# Class EncodingTables
# -----------------------------------------------------------------------------
class EncodingTables:
  """
  Encoding tables class - collections of encoding look up tables.

  An encoding scheme contains a set of look up tables. Each table
  contains metadata and a mapping.

  Tree view:
    encoding_0
      table:tid_0
        desc, mapping
      table:tid_1
        desc, mapping
      ...
    encoding_1
      table:tid_0
        desc, mapping
      ...
    ...

  A mapping here is defined as a dictionary of key,code pairs, where:
    key     An ascii string.
    code    Any mapped encoded string (e.g. unicode, html, md, ...).
  """
  _instance = None

  def __new__(klass, *args, **kwargs):
    """
    Constructor.

    Parameters:
      args    Arguments passed to __init__()
      kwargs  Keyword arguments passed to __init__()

    Returns:
      EncodingTables instance.
    """
    print(f"DBG: EncodingTables.__new__()")
    if not klass._instance:
      print(f"DBG: EncodingTables.__new__(): construct")
      klass._instance = super(klass, klass).__new__(klass)
    return klass._instance

  def __init__(self):
    """
    Initializer.
    """
    print(f"DBG: EncodingTables.__init__()")
    self.installed  = {}      # installed encoding tables
    self.nsm        = {}      # associated nonspacing marks

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}()"

  def __str__(self):
    return f"{self.list_of_encodings()}"

  def __len__(self):
    """ Number of encodings installed. """
    return len(self.installed)

  def __contains__(self, encoding):
    """ True if encoding is installed, else False. """
    return encoding in self.installed

  def contains_table(self, encoding, tid):
    """ True if encoding contains table tid, else False. """
    if self.installed.haskey(encoding):
      return tid in self.installed[encoding][tid]
    else:
      return False

  def __iter__(self):
    """ Iterator over installed encoding keys. """
    return self.installed.__iter__()

  def encodings(self):
    """ Iterator over encoding,tables pairs. """
    return self.installed.items()

  def tables(self, encoding):
    """ Iterator over tables tid,data pairs in encoding. """
    return self.installed[encoding].items()

  def tid_list(self, encoding):
    """ Return list of installed tid's for encoding. """
    if encoding in self.installed:
      return list(self.installed[encoding].keys())
    else:
      return []

  def __getitem__(self, encoding):
    """ __getitem__(encoding)  <==> installed[encoding]. """
    return self.installed[encoding]

  def getdesc(self, encoding, tid):
    """ getdesc(encoding, tid)  <==> installed[encoding][tid]['desc']. """
    return self.installed[encoding][tid]['desc']

  def getmapping(self, encoding, tid):
    """ getmapping(encoding, tid)  <==> installed[encoding][tid]['mapping']. """
    return self.installed[encoding][tid]['mapping']

  def getmapped(self, encoding, tid, key):
    """
    getmapped(encoding, tid, key) <==> installed[encoding][tid]['mapping'][key]
    """
    return self.installed[encoding][tid]['mapping'][key]

  def __delitem__(self, encoding):
    """ Delete installed[encoding]. """
    del self.installed[encoding]

  def deltable(self, encoding, tid):
    """ Delete installed[encoding][tid]. """
    del self.installed[encoding][tid]

  def install_table(self, encoding, tid, desc, mapping):
    """
    Install new lookup table.

    Paramters:
      encoding  Encoding scheme.
      tid       Unique table identifier string within encoding.
      desc      Short description.
      mapping   The key, code mapping.
    """
    #print(f"DBG: install {tid} symbol table")
    if encoding not in self.installed:
      self.installed[encoding] = {}
      self.nsm[encoding] = []
    self.installed[encoding][tid] = {}
    self.installed[encoding][tid]['desc'] = desc
    self.installed[encoding][tid]['mapping'] = mapping
    if tid in ['phy', 'sm']:
      print(f"DBG: EncodingTables.install_table({encoding!r}, {tid!r},...): "\
              f"table installed, length={len(mapping)}")

  def uninstall_table(self, encoding, tid):
    """ Uninstall (delete) encoding table. """
    del self.installed[encoding][tid]

  def set_nsm(self, encoding, nsm):
    """
    Set nonspacing marks associated with encoding.

    Parameters:
      encoding    Encoding scheme.
      nsm         List of nonspacing marks.
    """
    if encoding not in self.installed:
      self.installed[encoding] = {}
      self.nsm[encoding] = []
    self.nsm[encoding] = nsm

  def get_nsm(self, encoding):
    """
    Get the nonspacing marks associated with an encoding.

    Parameters:
      encoding    Encoding scheme.

    Returns:
      List of nonspacing marks.
    """
    return self.nsm[encoding]

  def count_nsm(self, encoding, s):
    """
    Count the number of nonspacing marks.

    A nonspacing mark combines or modifies the current print position 
    character without advancing the position in the output stream.

    Parameters:
      encoding    Encoding scheme.
      s           String to search.

    Returns:
      Count >= 0.
    """
    cnt = 0
    for c in s:
      if c in self.nsm[encoding]:
        cnt += 1
    return cnt

  def has_leading_nsm(self, encoding, s):
    """ True if leading character is an nonspaciing mark, False otherwise. """
    return s[0] in self.nsm[encoding]

  def list_of_encodings(self):
    """
    Return list of installed encoding ids.
    
    Returns:
      [encoding, ...]
    """
    return list(self.installed.keys())

  def list_of_tables(self, encoding):
    """
    Return list of installed encoding table ids.
    
    Parameters:
      encoding  Encoding scheme.

    Returns:
      [tid, ...]
    """
    return list(self.installed[encoding].keys())

  def print_lookup_tbl(self, encoding, tid, in_ascii=False, **print_kwargs):
    """
    Print installed lookup table to an output stream.

    Parameters:
      encoding      Encoding scheme.
      tid           Table identifier.
      in_ascii      Do [not] print ASCII-only representation.
      print_kwargs  Keyword arguments to print().
    """
    if 'end' in print_kwargs:
      del print_kwargs['end']
    if 'file' not in print_kwargs:
      print_kwargs['file'] = sys.stdout

    desc = self.installed[encoding][tid]['desc']
    print(f"  Lookup Table: {encoding}:{tid}  {desc}", **print_kwargs)
    self.print_mapping(encoding, tid, in_ascii=in_ascii, **print_kwargs)

  def print_mapping(self, encoding, tid, in_ascii=False, **print_kwargs):
    """
    Print lookup table key,values helper method.

    Parameters:
      encoding      Encoding scheme.
      tid           Table identifier.
      in_ascii      Do [not] print ASCII-only representation.
      print_kwargs  Keyword arguments to print().
    """
    mapping = self.installed[encoding][tid]['mapping']

    # determine print control parameters
    ctl = self._printctl(encoding, tid, in_ascii, **print_kwargs) 

    # print column headers
    self._printhdr(**ctl, **print_kwargs)

    ncols   = ctl['ncols']
    indent  = ctl['indent']
    kwid    = ctl['kwid']
    cwid    = ctl['cwid']
    sep     = ctl['sep']

    # key,unicode table
    col = 0
    for key,code in mapping.items():
      if col == 0: 
        print(f"{'':<{indent}}", end='', **print_kwargs)

      if in_ascii:
        v   = ascii(code)[1:-1]  # strip quotes
        nsm = 0
      else:
        v   = code
        nsm = self.count_nsm(encoding, v)  # count nonspacing marks

      if self.has_leading_nsm(encoding, v):
        print(f"{key:<{kwid}} {'':<{nsm}}{v:<{cwid}}", end='', **print_kwargs)
      else:
        print(f"{key:<{kwid}} {v:<{cwid}}{'':<{nsm}}", end='', **print_kwargs)

      col += 1

      if col < ncols:
        print(f"{'':<{sep}}", end='', **print_kwargs)
      else:
        print('', **print_kwargs)
        col = 0

    if col != 0:
      print('', **print_kwargs)

  def _printctl(self, encoding, tid, in_ascii, **print_kwargs):
    """
    Calculate printing control parameters such as number of columns,
    column widths, and spacing between.

    Parameters:
      encoding      Encoding scheme.
      tid           Table identifier.
      in_ascii      Do [not] print ASCII-only representation.
      print_kwargs  Keyword arguments to print().

    Returns:
      Dictionary of output printing control parameters.
    """
    mapping = self.installed[encoding][tid]['mapping']

    ncols = 1   # number of column pairs
    kwid  = 1   # key header width
    cwid  = 1   # code header width
    sep   = 2   # separtion between column pairs

    # table key and code max widths
    for key,code in mapping.items():
      if len(key) > kwid:
        kwid = len(key)
      if in_ascii:
        a = ascii(code)
        w = len(a) - a.count('\\')            # double back slashes print as one
      else:
        w = len(code) - self.count_nsm(encoding, code)  # less nonspacing marks
      if w > cwid:
        cwid = w

    # output max columns
    if os.isatty(print_kwargs['file'].fileno()):
      maxcols = termsize()[1]
    else:
      maxcols = 80

    # column pair width include space between
    w = kwid + 1 + cwid

    # crude cut on number a column pairs
    ncols = int(maxcols / (w + sep))

    # always have one pair 
    if ncols == 0:
      ncols = 1
      sep   = 1
    # but never larger than the table
    elif ncols > len(mapping):
      ncols = len(mapping)

    # number of columns pairs are 1, 2, 4, 8, 12, 16
    if ncols > 1:
      k = int(ncols / 4)
      if k > 0:
        ncols = k * 4
      if ncols > 16:
        ncols = 16
      sep = maxcols - (ncols * w)
      sep = int(sep/(ncols-1))
      if sep > 6:
        sep = 6
    return {'ncols':ncols, 'indent':0, 'kwid':kwid, 'cwid':cwid, 'sep':sep}

  def _printhdr(self, ncols=1, indent=0, kwid=16, cwid=1, sep=6,
                      **print_kwargs):
    """
    Print lookup table header helper method.

    Parameters:
      ncols         Number of key,unicode column pairs per output row.
      indent        Left row indent.
      kwid          Width of key columns.
      cwid          Width of code columns.
      sep           White space separtion between key,unicode column pairs.
      print_kwargs  Keyword arguments to print().
    """
    # column header names
    kcol = 'key'[:kwid]
    ccol = 'code'[:cwid]

    # print header name pairs
    print(f"{'':<{indent}}", end='', **print_kwargs)
    for col in range(ncols-1):
      print(f"{kcol:<{kwid}} {ccol:<{cwid}}{'':<{sep}}", end='', **print_kwargs)
    print(f"{kcol:<{kwid}} {ccol:<{cwid}}", **print_kwargs) 

    # print header underline pairs
    dash = '\u2014'   # em dash
    kbar = dash * kwid
    cbar = dash * cwid
    print(f"{'':<{indent}}", end='', **print_kwargs)
    for col in range(ncols-1):
      print(f"{kbar:<{kwid}} {cbar:<{cwid}}{'':<{sep}}", end='', **print_kwargs)
    print(f"{kbar:<{kwid}} {cbar:<{cwid}}", **print_kwargs)

# -----------------------------------------------------------------------------
# Class BaseEncoder
# -----------------------------------------------------------------------------
class BaseEncoder:
  """ Base encoder class. """
  EncTbls = EncodingTables()  # only one instance to encode them all

  _loaded_builtins = True     # redefine in derived class

  def __init__(self, encoding):
    """
    Initializer.

    Parameters:
      encoding    Encoding scheme string.
    """
    self._encoding = encoding
    self.encoders  = {}
    self._parser   = EncoderParser(self, strict=False)
    if not self._loaded_builtins:
      print(f"DBG: BaseEncoder.__init__({self.encoding}).load_builtins()")
      self.load_builtins()

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"({self.encoding!r})"

  def __str__(self):
    return self.encoding

  def __call__(self, expr):
    """
    Parse expression.

    Parameters:
      expr    Parsable string expression.

    Returns:
      Encoded string.
    """
    if self._parser is not None:
      return self._parser.parse(expr)
    else:
      return 'NOBASECLASSPARSER.'

  @property
  def encoding(self):
    return self._encoding

  @property
  def parser(self):
    return self._parser

  def load_builtins(self):
    """ Load built-in encoders.  """
    pass

  def parse(self, expr):
    """
    Parse expression to generate an ascii-unicode mixed string.

    See:
      UnicoderParser for grammar.

    Parameters:
      klass   Unicoder (derived) class.
      expr    String expression to parse.

    Returns:
      Mixed ascii-unicode string.
    """
    if self._parser is not None:
      return self._parser.parse(expr)
    else:
      return 'NOBASECLASSPARSER.'

  def tr(self, s):
    """
    Translate s to encoding scheme code.

    Base class has no encoding translation.

    Parameters:
      s   String to translate.

    Return:
      s.
    """
    return s

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Encoders
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

  def encoder_dft(self, gid, key):
    """
    Default lookup method.

    It uses the key to find a single encoded value.

    Parameters:
      gid     Unique encoding group (and table) identifier.
      key     Lookup table key.

    Returns:
      Encoded value.
    """
    try:
      mapping = BaseEncoder.EncTbls.getmapping(self.encoding, gid)
    except KeyError:
      raise KeyError(f"no {self.encoding} table {gid!r}")
    try:
      return BaseEncoder.EncTbls.getmapped(self.encoding, gid, str(key))
    except KeyError:
      raise KeyError(
          f"{self.encoding} encoding table {gid!r} has no key {key!r}")
    except TypeError:
      raise TypeError(
          f"{self.encoding} encoding table {gid!r} key {key!r} invalid type")

  def encoder_cat(self, gid, keys):
    """
    Concatenated lookup method.

    Each ascii character in keys is considered a key into the lookup
    table.

    Parameters:
      gid     Unique encoding group (and table) identifier.
      keys    String of single character keys.

    Returns:
      Concatenated encoded value.
    """
    s       = str(keys)
    code    = ''
    try:
      mapping = BaseEncoder.EncTbls.getmapping(self.encoding, gid)
    except KeyError:
      raise KeyError(f"no {self.encoding} table {gid!r}")
    for k in s:
      try:
        c = mapping[k]
      except KeyError:
        raise KeyError(
            f"{self.encoding} encoding table {gid!r} has no key {k!r}")
      except TypeError:
        raise TypeError(
            f"{self.encoding} encoding table {gid!r} key {k!r} invalid type")
      else:
        code += c
    return code

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Install Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

  def install_encoding_table(self, tid, desc, mapping):
    """
    Install new encoding table.

    Paramters:
      tid       Unique table identifier string.
      desc      Short description.
      mapping   The key, code mapping.
    """
    BaseEncoder.EncTbls.install_table(self.encoding, tid, desc, mapping)

  def install_encoder(self, gid, desc, encoder=None, mapping=None):
    """
    Install new encoder associtated with encoding group.

    Paramters:
      gid       Unique encoding group identifier string.
      desc      Short description.
      encoder   Encoded encoder function. The call signature:
                  encoder(gid, key, *args, **kwargs).
                Available built-ins:
                  self.encoder_dft(), self.encoder_cat()
                If None, then self.encoder.dft() is used.
      mapping   The key,code mapping. Not required.
    """
    if mapping is not None:
      BaseEncoder.EncTbls.install_table(self.encoding, gid, desc, mapping)
    if encoder is None:
      encoder = self.encoder_dft
    self.encoders[gid] = {'encoder': encoder, 'desc': desc}

  def nsm(self, nsm=None):
    """
    Get or set nonspacing marks list.

    Parameters:
      nsm   List of nonspacing marks. None to simple retrieve.

    Returns:
      (New) current nsm list.
    """
    if nsm is not None:
      BaseEncoder.EncTbls.set_nsm(self.encoding, nsm)
    return BaseEncoder.EncTbls.get_nsm(self.encoding)

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Access Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  
  def lookup(self, tid, key):
    """
    Lookup up an encoded string.

    Parameters:
      tid     Unique table identifier string.
      key     An ascii string.

    Returns:
      Unicode string.
    """
    return BaseEncoder.EncTbls.getmapped(self.encoding, tid, key)

  def has_table(self, tid):
    """ Returns True/False if table tid is installed under encoding. """
    return tid in BaseEncoder.EncTbls[self.encoding]

  def tid_list(self):
    """
    Return list of installed table identifier strings for this encoding.
    
    Returns:
      [tid, ...]
    """
    return BaseEncoder.EncTbls.tid_list(self.encoding)

  def gid_list(self):
    """
    Return list of installed group identifier strings.
    
    Returns:
      [gid, ...]
    """
    return list(self.encoders.keys())

  def call_dict(self):
    """
    Return dictionary of installed lookup table access methods.
    
    Returns:
      {group: call, ...}
    """
    d = {}
    for k,v in self.encoders.items():
      d[k] = v['encoder']
    return d

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Print Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

  def print_table(self, tid, in_ascii=False, **print_kwargs):
    """
    Print group encoding table.

    Parameters:
      tid           Unique table identifier within encoding.
      in_ascii      Do [not] print unicode in ASCII-only representation.
      print_kwargs  Keyword arguments to print().
    """
    BaseEncoder.EncTbls.print_lookup_tbl(self.encoding, tid,
                              in_ascii=in_ascii, **print_kwargs)

# -----------------------------------------------------------------------------
# Class UnicodeEncoder
# -----------------------------------------------------------------------------
class UnicodeEncoder(BaseEncoder):
  """ Unicode encoder class. """

  # Arabic digits unicode mappings
  ArabicDigitsMapping = {
    '0': '\u0660', '1': '\u0661', '2': '\u0662', '3': '\u0663', '4': '\u0664',
    '5': '\u0665', '6': '\u0666', '7': '\u0667', '8': '\u0668', '9': '\u0669',
  }
  
  
  # superscript unicode mappings
  SupMapping = {
    '0': '\u2070', '1': '\u00b9', '2': '\u00b2', '3': '\u00b3', '4': '\u2074',
    '5': '\u2075', '6': '\u2076', '7': '\u2077', '8': '\u2078', '9': '\u2079',
    '+': '\u207a', '-': '\u207b', '=': '\u207c', '(': '\u207d', ')': '\u207e',
    'i': '\u2071', 'n': '\u207f',
  
    'o': '\u00b0',    # degrees (little o)
  
    # quotation marks
    '"': '\u0022', "'": '\u0027', 'ldquo': '\u201c', 'rdquo': '\u201d',
  }
  
  # subscript unicode mappings
  SubMapping = {
    '0': '\u2080', '1': '\u2081', '2': '\u2082', '3': '\u2083', '4': '\u2084',
    '5': '\u2085', '6': '\u2086', '7': '\u2087', '8': '\u2088', '9': '\u2089',
    '+': '\u208a', '-': '\u208b', '=': '\u208c', '(': '\u208d', ')': '\u208e',
    'a': '\u2090', 'e': '\u2091', 'o': '\u2092', 'x': '\u2093', '@': '\u2094',
    'h': '\u2095', 'k': '\u2096', 'l': '\u2097', 'm': '\u2098', 'n': '\u2099',
    'p': '\u209a', 's': '\u209b', 't': '\u209c',
  }
  
  # vulgar (common) fraction unicode mappings
  FracMapping = {
    '1/2': '\u00bd',
    '0/3': '\u2189', '1/3': '\u2153', '2/3': '\u2154',
    '1/4': '\u00bc', '3/4': '\u00be', '1/5': '\u2155',
    '2/5': '\u2156', '3/5': '\u2157', '4/5': '\u2158',
    '1/6': '\u2159', '5/6': '\u215a',
    '1/7': '\u2150',
    '1/8': '\u215b', '3/8': '\u215c', '5/8': '\u215d', '7/8': '\u215e',
    '1/9': '\u2151',
    '1/10': '\u2152',
  }
  
  # greek letter unicode mappings
  GreekLetterMapping = {
    # lower case
    'alpha':    '\u03b1', 'beta':     '\u03b2',
    'gamma':    '\u03b3', 'delta':    '\u03b4',
    'epsilon':  '\u03b5', 'zeta':     '\u03b6',
    'eta':      '\u03b7', 'theta':    '\u03b8',
    'iota':     '\u03b9', 'kappa':    '\u03ba',
    'lambda':   '\u03bb', 'mu':       '\u03bc',
    'nu':       '\u03bd', 'xi':       '\u03be',
    'omicron':  '\u03bf', 'pi':       '\u03c0',
    'rho':      '\u03c1', 'sigma':    '\u03c3',
    'tau':      '\u03c4', 'upsilon':  '\u03c5',
    'phi':      '\u03c6', 'chi':      '\u03c7',
    'psi':      '\u03c8', 'omega':    '\u03c9',
  
    # upper case
    'Alpha':    '\u0391', 'Beta':     '\u0392',
    'Gamma':    '\u0393', 'Delta':    '\u0394',
    'Epsilon':  '\u0395', 'Zeta':     '\u0396',
    'Eta':      '\u0397', 'Theta':    '\u0398',
    'Iota':     '\u0399', 'Kappa':    '\u039a',
    'Lambda':   '\u039b', 'Mu':       '\u039c',
    'Nu':       '\u039d', 'Xi':       '\u039e',
    'Omicron':  '\u039f', 'Pi':       '\u03a0',
    'Rho':      '\u03a1', 'Sigma':    '\u03a3',
    'Tau':      '\u03a4', 'Upsilon':  '\u03a5',
    'Phi':      '\u03a6', 'Chi':      '\u03a7',
    'Psi':      '\u03a8', 'Omega':    '\u03a9',
  }
  
  # Upper case script letter unicode mapping
  ScriptLetterMapping = {
    'A':'\U0001d49c', 'B':'\u212c',     'C':'\U0001d49e', 'D':'\U0001d49f',
    'E':'\u2130',     'F':'\u2131',     'G':'\U0001d4a2', 'H':'\u210b',
    'I':'\u2110',     'J':'\U0001d4a5', 'K':'\U0001d4a6', 'L':'\u2112',
    'M':'\u2133',     'N':'\U0001d4a9', 'O':'\U0001d4aa', 'P':'\U0001d4ab',
    'Q':'\U0001d4ac', 'R':'\u211b',     'S':'\U0001d4ae', 'T':'\U0001d4af',
    'U':'\U0001d4b0', 'V':'\U0001d4b1', 'W':'\U0001d4b2', 'X':'\U0001d4b3',
    'Y':'\U0001d4b4', 'Z':'\U0001d4b5',
  }

  # math symbol unicode mappings
  MathMapping = {
    # binary comparators
    '<':  '\u003c',     # less than 
    '<=': '\u2264',     # less than or equal to
    '=':  '\u003d',     # equal to
    '>=': '\u2265',     # greater than or equal to
    '>':  '\u003e',     # greater than
    '!=': '\u2260',     # not equal to
  
    # range
    '+-': '\u00b1',     # plus or minus
    '-+': '\u2213',     # minus or plus
  
    # binary arithmetic operators
    '+':      '\u208a', # addition sign
    '-':      '\u208b', # subtraction sign
    '*':      '\u00d7', # multiplication sign
    '/':      '\u2215', # division sign
    'frac':   '\u2044', # fraction slash
    'obelus': '\u00f7', # division symbol (horizontal line with over/under dots)
  
    # common use symbols
    'inf':  '\u221e',   # positive infinity 
    'deg':  '\u00b0',   # degree symbol
    'sum':  '\u2140',   # summation (sigma)
    'int':  '\u222b',   # indefinite integral
    'null': '\u00d8',   # null set
  
    # primes
    "'":    '\u2032',   # prime
    "''":   '\u2033',   # double prime
    "'''":  '\u2034',   # triple prime
    "''''": '\u2057',   # quadruple prime
  
    # combining by overlaying with previous letter
    'hat':      '\u0302', # circumflex ^
    'twiddle':  '\u0303', # tilde
    'dot':      '\u0307', # single dot
    'dotdot':   '\u0308', # double dot
    'bar':      '\u0304', # bar
    'bbar':     '\u0305', # big bar
  }

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Built-in Set of Lookup Tables
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

  # marks that combine with previous character
  CombiningMarks = [
    '\u0302', # circumflex ^
    '\u0303', # tilde
    '\u0307', # single dot
    '\u0308', # double dot
    '\u0304', # bar
    '\u0305', # big bar
  ]

  _loaded_builtins = False

  def __init__(self):
    """ Initializer. """
    BaseEncoder.__init__(self, 'unicode')
    UnicodeEncoder._loaded_builtins = True

  def load_builtins(self):
    """ Load built-in encoders.  """
    self.install_encoder('arabic', 'Arabic digits 0-9',
      encoder=self.encoder_cat, mapping=UnicodeEncoder.ArabicDigitsMapping)

    self.install_encoder('frac', 'fractions',
      encoder=self.encoder_fraction, mapping=UnicodeEncoder.FracMapping)

    self.install_encoder('greek', 'Greek letters',
        mapping=UnicodeEncoder.GreekLetterMapping)

    self.install_encoder('math', 'math symbols',
        mapping=UnicodeEncoder.MathMapping)

    self.install_encoder('script', 'script capital letters',
      encoder=self.encoder_cat, mapping=UnicodeEncoder.ScriptLetterMapping)

    self.install_encoder('sub', 'subscripts',
      encoder=self.encoder_cat, mapping=UnicodeEncoder.SubMapping)

    self.install_encoder('sup', 'superscripts',
      encoder=self.encoder_cat, mapping=UnicodeEncoder.SupMapping)

    self.nsm(UnicodeEncoder.CombiningMarks)

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}()"

  def __str__(self):
    return self.encoding

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Encoders
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

  def encoder_fraction(self, gid, numerator, denominator):
    """
    Unicode vulgar fraction encoder.

    If the numerator/denominator exists as a unicode fraction, then
    that code is used. Otherwise fraction is built up by:
      superscript '/' subscript.

    Parameters:
      gid           Unique encoding group identifier.
      numerator     Fraction integer or string numerator.
      denominator   Fraction integer or string denominator.

    Returns:
      Unicode string.
    """
    n = str(numerator).strip()
    d = str(denominator).strip()
    if d == '1':
      return n
    elif d == '0':
      return 'inf'
    mapping = BaseEncoder.EncTbls.getmapping(self.encoding, gid)
    key     = n + '/' + d                     # make a key
    try:
      q = mapping[key]
    except (KeyError, TypeError):
      try:
        q = self.encoder_cat('sup', n) + \
            self.encoder_dft('math', 'frac') + \
            self.encoder_cat('sub', d)
      except (KeyError, TypeError):
        q = key
    return q
 
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Lookup Unicode Built-In Symbol Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

  def arabic(self, key):
    """
    Look up unicode Arabic digit string.

    Parameters:
      key   Single digit '0' - '9'.

    Returns:
      Unicode string.
    """
    return BaseEncoder.EncTbls.getmapped(self.encoding, 'arabic', str(key))

  def fraction(self, numerator, denominator):
    """
    Look up unicode vulgar fraction string.

    Parameters:
      numerator     Fraction integer or string numerator.
      denominator   Fraction integer or string denominator.

    Returns:
      Unicode string.
    """
    key = f"{numerator}/{denominator}"
    return BaseEncoder.EncTbls.getmapped(self.encoding, 'frac', str(key))

  def greek(self, key):
    """
    Look up unicode Greek letter.

    Parameters:
      key     Greek English key for letter (e.g. 'alpha', 'Alpha', etc).

    Returns:
      Unicode string.
    """
    return BaseEncoder.EncTbls.getmapped(self.encoding, 'greek', str(key))

  def mathsym(self, key):
    """
    Look up unicode math symbol.

    Parameters:
      key     Math key for symbol (e.g. '>=', 'inf', etc).

    Returns:
      Unicode string.
    """
    return BaseEncoder.EncTbls.getmapped(self.encoding, 'math', str(key))

  def subscript(self, key):
    """
    Look up unicode subscript string.

    Note: The character '@' is mapped to the schwa subscript
          (upside down lower case 'e').

    Parameters:
      key   Subscript key.

    Returns:
      Unicode string.
    """
    return BaseEncoder.EncTbls.getmapped(self.encoding, 'sub', str(key))

  def superscript(self, key):
    """
    Look up unicode superscript string.

    Parameters:
      key   Subscript key.

    Returns:
      Unicode string.
    """
    return BaseEncoder.EncTbls.getmapped(self.encoding, 'sup', str(key))

# -----------------------------------------------------------------------------
# Class HtmlEncoder
# -----------------------------------------------------------------------------
class HtmlEncoder(BaseEncoder):
  """ HTML encoder class. """

  # convert unicode character to html hex equivalent.
  unicode2html = lambda u: "&#" + hex(ord(u))[1:] + ";"

  _loaded_builtins = False

  def __init__(self):
    """ Initializer. """
    BaseEncoder.__init__(self, 'html')
    HtmlEncoder._loaded_builtins = True

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}()"

  def __str__(self):
    return self.encoding

  def load_builtins(self):
    """ Load built-in encoders. """
    self.install_encoder('arabic', 'Arabic digits 0-9',
      encoder=self.encoder_arabic_digits)

    self.install_encoder('frac', 'fractions', encoder=self.encoder_fraction)

    self.install_encoder('greek', 'Greek letters', encoder=self.encoder_greek)

    self.install_encoder('math', 'math symbols',
        encoder=self.encoder_math_symbol)

    self.install_encoder('script', 'script capital letters',
        encoder=self.encoder_script)

    self.install_encoder('sub', 'subscripts', encoder=self.encoder_subscript)

    self.install_encoder('sup', 'superscripts',
      encoder=self.encoder_superscript)

  def tr(self, s):
    """
    Translate string into a valid HTML quasi-equivalent.

    tr: ' '         ->  ' '       ; space
        '\\n'        ->  '<br>'    ; newline
        '&'         ->  '&amp;'   ; lone ampersand (needs work)
        '<'         ->  '&lt;'    ; lone less than (needs work)
        '>'         ->  '&gt;'    ; greater than (needs work)
        'c'         ->  'c'       ; for ord('c') < 128
        '\\uxxxx'    ->  '&#xxxx;' ; for ord('c') >= 128

    Note: Is there a cleaner way of doing this in python3?

    Parameters:
      s     String to translate.

    Returns:
      HTML safe translated string.
    """
    t = ''
    for c in s:
      if c == '\n':
        t += '<br>'
      elif c == ' ':
        t += ' '
      #elif c == '&':
      #  t += '&amp;'
      #elif c == '<':
      #  t += '&lt;'
      #elif c == '>':
      #  t += '&gt;'
      elif ord(c) < 128:
        t += c
      else:
        t += HtmlEncoder.unicode2html(c)
    return t

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Encoders
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

  def encoder_arabic_digits(self, gid, number):
    """
    Arabic digits html encoder.

    Parameters:
      gid     Unique encoding group identifier.
      number  Decimal digits string.

    Returns:
      HTML encoded string.
    """
    digs = str(number).strip()
    html = ''
    for d in digs:
      ucode = BaseEncoder.EncTbls.getmapped('unicode', gid, d)
      html += HtmlEncoder.unicode2html(ucode)
    return self.tr(html)

  def encoder_fraction(self, gid, numerator, denominator):
    """
    Fraction html encoder.

    Parameters:
      gid         Unique encoding group identifier.
      numerator   Fraction integer or string numerator.
      denominator Fraction integer or string denominator.

    Returns:
      HTML encoded string.
    """
    n = self.tr(str(numerator).strip())
    d = self.tr(str(denominator).strip())
    return f"<sup>{n}</sup>/<sub>{d}</sub>"

  def encoder_greek(self, gid, englishword):
    """
    Greek letter html encoder.

    Parameters:
      gid           Unique encoding group identifier.
      englishword   English word for Greek letter (e.g. alpha, Omega).

    Returns:
      HTML encoded string.
    """
    e = self.tr(str(englishword).strip())
    return f"&{e};"

  def encoder_math_symbol(self, gid, symbol):
    """
    Math symbol html encoder.

    Parameters:
      gid       Unique encoding group identifier.
      symbol    Math symbol in ascii (e.g. inf, >=).

    Returns:
      HTML encoded string.
    """
    ucode = BaseEncoder.EncTbls.getmapped('unicode', gid, str(symbol))
    return HtmlEncoder.unicode2html(ucode)

  def encoder_script(self, gid, letters):
    """
    Arabic digits html encoder.

    Parameters:
      gid     Unique encoding group identifier.
      number  Decimal digits string.

    Returns:
      HTML encoded string.
    """
    abc = str(letters).strip()
    html = ''
    for c in abc:
      ucode = BaseEncoder.EncTbls.getmapped('unicode', gid, c)
      html += HtmlEncoder.unicode2html(ucode)
    return self.tr(html)

  def encoder_subscript(self, gid, sub):
    """
    Subscript html encoder.

    Parameters:
      gid     Unique encoding group identifier.
      sub     String of subscriptable characters.

    Returns:
      HTML encoded string.
    """
    s = self.tr(str(sub))
    return f"<sub>{s}</sub>"

  def encoder_superscript(self, gid, sup):
    """
    Superscript html encoder.

    Parameters:
      gid     Unique encoding group identifier.
      sup     String of superscriptable characters.

    Returns:
      HTML encoded string.
    """
    s = self.tr(str(sup))
    return f"<sup>{s}</sup>"

# -----------------------------------------------------------------------------
# Class LatexEncoder
# -----------------------------------------------------------------------------
class LatexEncoder(BaseEncoder):
  """ LaTeX encoder class. """

  # greek letter latex mappings
  GreekLetterMapping = {
    # lower case
    'alpha':    '\\alpha',    'beta':     '\\beta',
    'gamma':    '\\gamma',    'delta':    '\\delta',
    'epsilon':  '\\epsilon',  'zeta':     '\\zeta',
    'eta':      '\\eta',      'theta':    '\\theta',
    'iota':     '\\iota',     'kappa':    '\\kappa',
    'lambda':   '\\lambda',   'mu':       '\\mu',
    'nu':       '\\nu',       'xi':       '\\xi',
    'omicron':  'o',          'pi':       '\\pi',
    'rho':      '\\rho',      'sigma':    '\\sigma',
    'tau':      '\\tau',      'upsilon':  '\\upsilon',
    'phi':      '\\phi',      'chi':      '\\chi',
    'psi':      '\\psi',      'omega':    '\\omega',
  
    # upper case
    'Alpha':    'A',          'Beta':     'B',
    'Gamma':    '\\Gamma',    'Delta':    '\\Delta',
    'Epsilon':  'E',          'Zeta':     'Z',
    'Eta':      'H',          'Theta':    '\\Theta',
    'Iota':     'I',          'Kappa':    'K',
    'Lambda':   '\\Lambda',   'Mu':       'M',
    'Nu':       'N',          'Xi':       '\\Xi',
    'Omicron':  'O',          'Pi':       '\\Pi',
    'Rho':      'P',          'Sigma':    '\\Sigma',
    'Tau':      'T',          'Upsilon':  '\\Upsilon',
    'Phi':      '\\Phi',      'Chi':      'X',
    'Psi':      '\\Psi',      'Omega':    '\\Omega',
  }
  
  # math symbol latex mappings
  MathMapping = {
    # binary comparators
    '<':  '<',                # less than 
    '<=': '\\leq',            # less than or equal to
    '=':  '=',                # equal to
    '>=': '\\geq',            # greater than or equal to
    '>':  '>',                # greater than
    '!=': '\\neq',            # not equal to
  
    # range
    '+-': '\\pm',             # plus or minus
    '-+': '\\mp',             # minus or plus
  
    # binary arithmetic operators
    '+':      '+',            # addition sign
    '-':      '-',            # subtraction sign
    '*':      '\\times',      # multiplication sign
    '/':      '/',            # division sign
    'frac':   '/',            # fraction slash
    'obelus': '\\div',        # division (horizontal line with over/under dots)
  
    # common use symbols
    'inf':  '\\infty',        # positive infinity 
    'deg':  '^\\circ',        # degree symbol
    'sum':  '\\sum',          # summation (sigma)
    'int':  '\\int',          # indefinite integral
    'null': '\\emptyset',     # null set
  
    # primes
    "'":    "'",              # prime
    "''":   "''",             # double prime
    "'''":  "'''",            # triple prime
    "''''": "''''",           # quadruple prime
  
    # combining by overlaying with previous letter
    'hat':      '\\^',        # circumflex ^
    'twiddle':  '\\~',        # tilde
    'dot':      '\\.',        # single dot
    'dotdot':   '\\"',        # double dot
    'bar':      '\\bar',      # bar
    'bbar':     '\\overline', # big bar
  }

  # convert unicode character to latex equivalent.
  unicode2latex = lambda u: "\\unicode{" + hex(ord(u))[2:] + "}"

  _loaded_builtins = False

  def __init__(self):
    """ Initializer. """
    BaseEncoder.__init__(self, 'latex')
    LatexEncoder._loaded_builtins = True
    self.nsm = [LatexEncoder.MathMapping[key] for key in ['hat', 'twiddle',
                  'dot', 'dotdot', 'bar', 'bbar']]

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}()"

  def __str__(self):
    return self.encoding

  def load_builtins(self):
    """ Load built-in encoders. """
    self.install_encoder('arabic', 'Arabic digits 0-9',
      encoder=self.encoder_arabic_digits)

    self.install_encoder('frac', 'fractions', encoder=self.encoder_fraction)

    self.install_encoder('greek', 'Greek letters',
        encoder=self.encoder_greek, mapping=LatexEncoder.GreekLetterMapping)

    self.install_encoder('math', 'math symbols',
        encoder=self.encoder_math_symbol, mapping=LatexEncoder.MathMapping)

    self.install_encoder('script', 'script capital letters',
        encoder=self.encoder_script)

    self.install_encoder('sub', 'subscripts', encoder=self.encoder_subscript)

    self.install_encoder('sup', 'superscripts',
      encoder=self.encoder_superscript)

  def tr(self, s):
    """
    Translate string into a valid LaTeX quasi-equivalent.

    tr: ' '       -> '\\ '               ; space
        '\\n'      -> '\\\\'               ; newline
        'c'       -> 'c'                ; for ord(c) < 128
        '\\uxxxx'  -> '\\unicode{xxxx)'   ; for ord(c) >= 128
        nsm       -> reorder            ; for nonspacing marks, reorder

    Note: The '\\unicode' markup is invented. The user must define its
          render by a LaTeX macro or by hook or crook.

    Parameters:
      s     String to translate (ignored).

    Returns:
      LaTeX safe translated string.
    """
    elist = self.parser.encoded_list

    # for latex, nsm's must preceed the target character(s) to mark
    for mark in self.nsm:
      if len(elist) == 0: # nothing in list
        break
      flist = [elist[0]]  # first encoded (front marks always preceeds all)
      i = 0; j = 1        # initialize indices
      while j < len(elist):
        if elist[j] == mark:      # nsm
          pre = flist.pop()       # pop off preceeding encoded
          flist.append(mark)      # push mark
          if len(pre) == 0:       # empty pre - hope this doesn't occur
            flist.append(pre)
          elif pre[0] in ['{', '\\']: # push as is
            flist.append(pre)
          else:                   # delineate first char in encode for mark
            flist.append('{' + pre[0] + '}' + pre[1:])
        else:
          flist.append(elist[j])  # not an nsm
        i += 1; j += 1            # increment indices
      elist = flist               # copy back to encoded list
    s = ''.join(elist)            # build string
    
    # replace single characters
    t = ''
    for c in s:
      if c == '\n':
        t += '\\\\'
      elif c == ' ':
        t += '\\ '
      elif ord(c) < 128:
        t += c
      else:
        t += LatexEncoder.unicode2latex(c)

    return t

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Encoders
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

  def encoder_arabic_digits(self, gid, number):
    """
    Arabic digits latex encoder.

    Parameters:
      gid     Unique encoding group identifier.
      number  Decimal digits string.

    Returns:
      Latex encoded string.
    """
    return f"{number}"

  def encoder_fraction(self, gid, numerator, denominator):
    """
    Fraction latex encoder.

    Parameters:
      gid         Unique encoding group identifier.
      numerator   Fraction integer or string numerator.
      denominator Fraction integer or string denominator.

    Returns:
      LaTeX encoded string.
    """
    return f"\\frac{{{numerator}}}{{{denominator}}}"

  def encoder_greek(self, gid, englishword):
    """
    Greek letter latex encoder.

    Parameters:
      gid           Unique encoding group identifier.
      englishword   English word for Greek letter (e.g. alpha, Omega).

    Returns:
      LaTeX encoded string.
    """
    return "{" + self.encoder_dft(gid, englishword) + "}"

  def encoder_math_symbol(self, gid, symbol):
    """
    Math symbol latex encoder.

    Parameters:
      gid       Unique encoding group identifier.
      symbol    Math symbol in ascii (e.g. inf, >=).

    Returns:
      LaTeX encoded string.
    """
    return BaseEncoder.EncTbls.getmapped(self.encoding, gid, str(symbol))

  def encoder_script(self, gid, letters):
    """
    Sciprt letters latex encoder.

    Parameters:
      gid       Unique encoding group identifier.
      letters   String of capital letters.

    Returns:
      LaTeX encoded string.
    """
    s = str(letters).strip()
    return f"\\mathcal{{{s}}}"

  def encoder_subscript(self, gid, sub):
    """
    Subscript latex encoder.

    Parameters:
      gid     Unique encoding group identifier.
      sub     String of subscriptable characters.

    Returns:
      LaTeX encoded string.
    """
    return f"_{{{sub}}}"

  def encoder_superscript(self, gid, sup):
    """
    Superscript latex encoder.

    Parameters:
      gid     Unique encoding group identifier.
      sup     String of superscriptable characters.

    Returns:
      LaTeX encoded string.
    """
    return f"^{{{sup}}}"

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Built-In Lookup Unicode Symbol Methods
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

  def mathsym(self, key):
    """
    Look up Latex math symbol.

    Parameters:
      key     Math key for symbol (e.g. '>=', 'inf', etc).

    Returns:
      Latex string.
    """
    return BaseEncoder.EncTbls.getmapped(self.encoding, 'math', str(key))


# -----------------------------------------------------------------------------
# Class PlainEncoder
# -----------------------------------------------------------------------------
class PlainEncoder(BaseEncoder):
  """ Plain text encoder class. """

  # math symbol unicode mappings
  MathMapping = {
    'frac':   '/', # fraction slash
    'obelus': '/', # division symbol (horizontal line with over/under dots)

    # common use symbols
    'inf':  'inf',            # positive infinity 
    'deg':  'degrees',        # degree symbol
    'sum':  'sum',            # summation (sigma)
    'int':  'integral',       # indefinite integral
    'null': 'null',           # null set

    # hypothetical overlays with previous letter
    'hat':      '-hat',       # circumflex ^
    'twiddle':  '-twiddle',   # tilde
    'dot':      '-dot',       # single dot
    'dotdot':   '-dotdot',    # double dot
    'bar':      '-bar',       # bar
    'bbar':     '-bar',       # big bar
  }

  # convert unicode character to plain text equivalent.
  unicode2plain = lambda u: "?"

  _loaded_builtins = False

  def __init__(self):
    """ Initializer. """
    BaseEncoder.__init__(self, 'plain')
    PlainEncoder._loaded_builtins = True

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}()"

  def __str__(self):
    return self.encoding

  def load_builtins(self):
    """ Load built-in encoders. """
    self.install_encoder('arabic', 'Arabic digits 0-9',
      encoder=self.encoder_arabic_digits)

    self.install_encoder('frac', 'fractions', encoder=self.encoder_fraction)

    self.install_encoder('greek', 'Greek letters', encoder=self.encoder_greek)

    self.install_encoder('math', 'math symbols',
        encoder=self.encoder_math_symbol, mapping=PlainEncoder.MathMapping)

    self.install_encoder('sub', 'subscripts', encoder=self.encoder_subscript)

    self.install_encoder('sup', 'superscripts',
      encoder=self.encoder_superscript)

  def tr(self, s):
    """
    Translate string into a valid plain text quasi-equivalent.

    tr: 'c'       -> 'c'  ; for ord(c) < 128
        '\\uxxxx'  -> '?'  ; for ord(c) >= 128

    Parameters:
      s     String to translate.

    Returns:
      Plain text safe translated string.
    """
    t = ''
    for c in s:
      if ord(c) < 128:
        t += c
      else:
        t += PlainEncoder.unicode2plain(c)
    return t

  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
  # Encoders
  # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

  def encoder_arabic_digits(self, gid, number):
    """
    Arabic digits plain text encoder.

    Parameters:
      gid     Unique encoding group identifier.
      number  Decimal digits string.

    Returns:
      Plain text encoded string.
    """
    return str(number).strip()

  def encoder_fraction(self, gid, numerator, denominator):
    """
    Fraction plain text encoder.

    Parameters:
      gid         Unique encoding group identifier.
      numerator   Fraction integer or string numerator.
      denominator Fraction integer or string denominator.

    Returns:
      Plain text encoded string.
    """
    return str(numerator).strip()  + '/' + str(denominator).strip()

  def encoder_greek(self, gid, englishword):
    """
    Greek letter plain text encoder.

    Parameters:
      gid           Unique encoding group identifier.
      englishword   English word for Greek letter (e.g. alpha, Omega).

    Returns:
      Plain text encoded string.
    """
    return str(englishword).strip()

  def encoder_math_symbol(self, gid, symbol):
    """
    Math symbol plain text encoder.

    Parameters:
      gid       Unique encoding group identifier.
      symbol    Math symbol in ascii (e.g. inf, >=).

    Returns:
      Plain text encoded string.
    """
    symbol = str(symbol).strip()
    try:
      return BaseEncoder.EncTbls.getmapped(self.encoding, gid, symbol)
    except:
      return symbol

  def encoder_subscript(self, gid, sub):
    """
    Subscript plain text encoder.

    Parameters:
      gid     Unique encoding group identifier.
      sub     String of subscriptable characters.

    Returns:
      Plain text encoded string.
    """
    return f"_{sub}"

  def encoder_superscript(self, gid, sup):
    """
    Superscript plain text encoder.

    Parameters:
      gid     Unique encoding group identifier.
      sup     String of superscriptable characters.

    Returns:
      Plain text encoded string.
    """
    return f"{sup}"

# -----------------------------------------------------------------------------
# Format4Some Class
# -----------------------------------------------------------------------------
class Format4Some:
  """ An associated 4 ways formatted encoded class. """

  """
  TODO
  __call__(expr=None)
    parse(expr)
    return default
  """

  def __init__(self, expr, default='unicode'):
    """
    Initializer.

    Parameters:
      expr      Parsable expression.
      default   Default format.
    """
    self.codes = {}
    self.parse4(expr)
    self._default = enumfactory(Format, default)

  def __getitem__(self, fmt):
    """ __getitem__(fmt)  <==> codes[fmt]. """
    return self.codes[enumfactory(Format, fmt)]

  def __setitem__(self, fmt, code):
    """ __setitem__(fmt, code)  <==> codes[fmt] = code """
    self.codes[enumfactory(Format, fmt)] = code

  def __call__(self, expr):
    self.parse4(expr)
    return self.default

  def parse4(self, expr):
    self.codes[Format.PLAIN]    = plain_encoder(expr)
    self.codes[Format.HTML]     = html_encoder(expr)
    self.codes[Format.LATEX]    = latex_encoder(expr)
    self.codes[Format.UNICODE]  = unicode_encoder(expr)

  @property
  def html(self):
    return self.codes[Format.HTML]

  @property
  def latex(self):
    return self.codes[Format.LATEX]

  @property
  def plain(self):
    return self.codes[Format.PLAIN]

  @property
  def unicode(self):
    return self.codes[Format.UNICODE]

  @property
  def default(self):
    return self.codes[self._default]

  @default.setter
  def default(self, fmt):
    self._default = enumfactory(Format, fmt)

  def print4(self, **print_kwargs):
    print(f"""\
html:    {self.html}
latex:   {self.latex}
plain:   {self.plain}
unicode: {self.unicode}""", **print_kwargs)

# -----------------------------------------------------------------------------
# Class EncoderParser
# -----------------------------------------------------------------------------
class EncoderParser:
  """
  Simple parser to generate an encoding from an ascii string expression.

  The encoding is extracted from an Encoder derived class.

  Encodings:
    plain, unicode, html, latex

  BNF:
    grammar ::= { expr }  (* grammar is composed of within expression *)

    expr ::=  '\\' '$'            (* dollar escape sequence *)
            | '$' call            (* dollar call sequence *)
            | { char_no_dollar }  (* any ascii sequence sans dollar sign*)

    call ::= call_name '(' [args] ') (* encoder call *) 

    call_name ::= INSTALLED       (* installed encoder list *)

    args ::=  arg                 (* one argument *)
            | arg ',' { args }    (* comma separated arguments *)

    arg ::=  esc_seq { arg }      (* escape seqence argument *)
            | '$' call            (* nested call argument *)
            | char_arg { arg }    (* normal characgter argument *)

    char_no_dollar ::= ASCII - '$'    (* ascii character except '$' *)

    char_arg ::= ASCII - (')' | ',')  (* ascii character except '),' *)

    esc_seq ::= '\\' special_char     (* escape sequence *)

    identifier ::= id0 [{idn}]        (* standard identifier *)

    (* grammar special characters *)
    special_char ::= '$' | '(' | ')' | ',' | '\\'

    (* lower case alpha character *)
    alpha_lower ::= 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i'
                  | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r'
                  | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z'

    (* upper case alpha character *)
    alpha_upper ::=  'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'G' | 'H' | 'I'
                   | 'J' | 'K' | 'L' | 'M' | 'N' | 'O' | 'P' | 'Q' | 'R'
                   | 'S' | 'T' | 'U' | 'V' | 'W' | 'X' | 'Y' | 'Z'

    (* decimal digits *)
    digits ::= '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'

    (* identifier legal start character and legal subsequent characters *)
    id0 ::= '_' | alpha_lower | alpha_upper
    idn ::= id0 | digits

    ASCII ::= 7-bit US ASCII

  Examples:
    "My plain world."
    "$greek(Omega) man and his dog Tri$greek(alpha)."
    "\$50$math(*)10$sup(9) dollars, ooh baby."
    "To $math(inf) and beyond."
    "Spodumene cation: LiAlSi$sub(2)O$sub(6)$sup(+)"
    "$frac(3,5) is 60%"
    "reduced Planck constant: $phy{h-bar}"
  """
  SpecChar  = '%(),\\'              # grammar special characters
  Digits    = string.digits         # decimal digits
  Alpha     = string.ascii_letters  # lower and upper case abc's
  Id0       = '_' + Alpha           # identifier allowed starting char
  IdN       = Id0 + Digits          # identifier subsequent c's

  def __init__(self, encoder, strict=True):
    """
    Initializer.

    Parameters:
      encoder BaseEncoder derived class instance.
      strict  If True then abort on parse errors. Otherwise try to
              recover with a reasonable encoding. Syntax errors
              are never forgiven.
    """
    self._encoder = encoder   # bind encoder
    self._strict  = strict    # parse level
    self.encoder_callbacks()  # encoder callbacks
    self.reset()

  def __repr__(self):
    return  f"{self.__module__}.{self.__class__.__name__}"\
            f"({self._encoder!r}, {self._strict!r})"

  @property
  def encoder(self):
    """ Return bound encoder to parser. """
    return self._encoder

  @property
  def strict(self):
    """ Return parse strictness level. """
    return self._strict

  @property
  def encoded_string(self):
    """ Return encoded string from last expression parse. """
    return self.sout

  @property
  def encoded_list(self):
    """ Return list of encode values, left to right, from last parse. """
    return self.encoded

  def encoder_callbacks(self):
    """ Load supported callbacks to encoder. """
    self.calls = self._encoder.call_dict()

  def reset(self, expr=''):
    """
    Reset parser accounting.

    Parameters:
      expr    (New) string expression to parse.
    """
    self.cursor   = 0     # cursor in input string
    self.sin      = expr  # input string
    self.sout     = ''    # output string
    self.eos      = len(self.sin) == 0   # is [not] at end of string
    self.encoded  = []    # encoded subexpression list

  def parse(self, expr):
    """
    Parse string.

    Parameters:
      expr    String expression to parse.

    Returns:
      Mixed ascii-unicode string.
    """
    self.encoder_callbacks()  # encoder can change callback profile, so collect
    self.reset(expr)          # reset parser accounting

    # parse
    while not self.eos:
      enc = self.parse_substr()
      self.encoded.append(enc)
      self.sout += enc

    # return string with any final translations
    return self._encoder.tr(self.sout)

  def parse_substr(self):
    """
    Parse grammar substring component.

    parser_substr := '$' parse_call | parse_seq_no_dollar

    Returns:
      Mixed ascii-unicode string.
    """
    while not self.eos:
      c = self.peekc()
      if c == '$':
        self.getc() # eat
        return self.parse_call()
      else:
        return self.parse_seq_no_dollar()

  def parse_call(self):
    """
    Parse grammar encoder call component.

    parse_call := parse_identity '(' [parse_args] ')'

    Returns:
      Encoded string.
    """
    noexec = False

    # parse function name
    fnname = self.parse_identifier()
    if not fnname:
      raise EncoderParseError(f"encoder call missing",
          self.sin, self.cursor)
    elif not fnname in self.calls:
      if self.strict:
        raise EncoderParseError(f"encoder call '{fnname}' not found",
          self.sin, self.cursor)
      else:
        noexec = True 

    # parse open parenthesis
    if self.getc() != '(':
      raise EncoderParseError(f"missing left parenthesis '('",
          self.sin, self.cursor)

    # parse function argument(s)
    argv = self.parse_args()

    # parse close parenthesis
    if self.getc() != ')':
      raise EncoderParseError(f"missing right parenthesis ')'",
          self.sin, self.cursor)

    # encountered loose error - fallback to parsed arguments
    if noexec:
      return ' '.join(argv)

    # call encoder
    try:
      return self.calls[fnname](fnname, *argv)  # encode
    except KeyError as e:
      if self.strict:
        raise EncoderParseError(
          f"encoder {fnname}({' '.join(argv)}) argument error {e}",
          self.sin, self.cursor)
      else:
        return ' '.join(argv)
    except TypeError as e:
      raise EncoderParseError(f"encoder {e}", self.sin, self.cursor)

  def parse_args(self):
    """
    Parse grammar encoder call arguments.

    parse_args := parse_arg [, parse_arg...]

    Returns:
      List of mixed ascii-unicode strings.
    """
    argv = []
    while not self.eos:
      arg = self.parse_arg()
      if len(arg) > 0:
        argv += [arg]
      if self.peekc() == ',':
        self.getc()  # eat
      else:
        break
    return argv

  def parse_arg(self):
    """
    Parse grammar encoder call argument.

    parse_arg := seq_no_comma_rparen

    Returns:
      Mixed ascii-unicode string.
    """
    s = ''
    while not self.eos:
      c = self.getc()
      if c == '\\':
        s += self.getc()
      elif c == '$':
        rarg = self.parse_call()
        s += rarg
      elif c in [',', ')']:
        self.ungetc()
        break
      else:
        s += c
    return s

  def parse_seq_no_dollar(self):
    """
    Parse grammar characters sequence with no unescaped '$'.

    Returns:
      Mixed ascii-unicode string.
    """
    s = ''
    while not self.eos:
      c = self.getc()
      if c == '$':
        self.ungetc()
        break
      elif c == '\\':
        c = self.getc()
      s += c
    return s

  def parse_identifier(self):
    """
    Parse C identifier.

    Returns:
      Mixed ascii-unicode string.
    """
    s = ''
    legal = self.Id0
    while not self.eos:
      c = self.getc()
      if c in legal:
        s += c
        legal = self.IdN
      else:
        self.ungetc()
        break
    return s

  def isspecial(self, c):
    """
    Test if c is a grammar special character.

    Returns:
      True or False.
    """
    return c in self.SpecChar
        
  def getc(self):
    """
    Get next character in the input string.

    The parser cursor is advanced. An end-of-string condition
    is set when input string is exhausted.

    Returns:
      Character or '' on EOS.
    """
    if self.eos:
      return ''
    c = self.sin[self.cursor]
    self.cursor += 1
    if self.cursor >= len(self.sin):
      self.eos = True
    return c

  def peekc(self):
    """
    Peek next character in the input string.

    The parser cursor is NOT advanced.

    Returns:
      Character or '' on EOS.
    """
    if self.eos:
      return ''
    return self.sin[self.cursor]

  def ungetc(self):
    """
    Unget last character 'read' in the input string.

    The parser cursor is decrement by one iff not at begining.
    An end-of-string condition is unset.
    """
    if self.cursor > 0:
      self.cursor -= 1
      self.eos = False

# -----------------------------------------------------------------------------
# Class EncoderParseError
# -----------------------------------------------------------------------------
class EncoderParseError(SyntaxError):
  """ Encoder parse error exception class. """

  def __init__(self, emsg, sin, cursor):
    """
    Initialize exception instance.

    Parameters:
      emsg    Error message.
      sin     Input string being parsed.
      cursor  Current parser cursor position.
    """
    SyntaxError.__init__(self)
    # n/a
    self.filename   = ''
    self.lineno     = 0
    self.print_file_and_line = False

    # relevant
    self.msg    = emsg
    self.offset = cursor
    self.text   = sin

  def __repr__(self):
    return  f"{self.__class__.__name__}"\
            f"({self.msg!r}, {self.text!r}, {self.offset!r})"

  def __str__(self):
    return  f"{self.text}\n"\
            f"{'^':>{self.offset}}\n"\
            f"{self.msg}"


# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------

# Pretty format number that may be += infinite
#
# Parameters:
#  n   Number to format.
#  fmt Optional format string if non-infinite.
#
# Returns:
#  Formatted string.
fInfNum = lambda n, fmt='': \
    f"{n:{fmt}}" if not math.isinf(n) else \
    default_encoder('$math(inf)') if n > 0 else \
    default_encoder('$math(-)$math(inf)')

# -----------------------------------------------------------------------------
# Data
# -----------------------------------------------------------------------------
unicode_encoder = UnicodeEncoder()
html_encoder    = HtmlEncoder()
latex_encoder   = LatexEncoder()
plain_encoder   = PlainEncoder()
default_encoder = unicode_encoder   # default (from TBD yaml cfg)

# -----------------------------------------------------------------------------
# Unit tests
# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import sys
  import tests.utformat as ut

  sys.exit(ut.utmain())
