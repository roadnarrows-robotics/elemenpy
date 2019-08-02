"""
ANSI colors.

This module specifies classes with ANSI color support.

Package:
  RoadNarrows elemenpy package.

File:
  color.py

Link:
  https://github.com/roadnarrows-robotics/

Copyright:
  (c) 2019. RoadNarrows LLC
  http://www.roadnarrows.com
  All Rights Reserved

License:
  MIT
"""

from __future__ import print_function

import os
import sys

class TermColors(dict):
  """
  Gives easy access to ANSI color codes. Attempts to fall back to no color
  for certain TERM values.
  """

  COLOR_TEMPLATES = (
        ("black"       , "0;30"),
        ("red"         , "0;31"),
        ("green"       , "0;32"),
        ("brown"       , "0;33"),
        ("blue"        , "0;34"),
        ("purple"      , "0;35"),
        ("cyan"        , "0;36"),
        ("lightgray"   , "0;37"),
        ("darkgray"    , "1;30"),
        ("lightred"    , "1;31"),
        ("lightgreen"  , "1;32"),
        ("yellow"      , "1;33"),
        ("lightblue"   , "1;34"),
        ("lightpurple" , "1;35"),
        ("lightcyan"   , "1;36"),
        ("white"       , "1;37"),
        ("normal"      , "0"),
  )

  NoColor = ''

  def __init__(self):
    """ Initializer. """
    self.m_usingColor = True
    self.enable()

  def enable(self):
    """ Enable color output. """
    if os.environ.get('TERM') in ('linux', 'screen', 'screen-256color',
                                  'screen-bce', 'screen.xterm-256color'):
      _base  = '\001\033[%sm\002'
      self.update(dict([(k, _base % v) for k,v in self.COLOR_TEMPLATES]))
      self.m_usingColor = True
         
    elif os.environ.get('TERM') in ('xterm', 'xterm-color', 'xterm-256color'):
      _base  = '\033[%sm'
      self.update(dict([(k, _base % v) for k,v in self.COLOR_TEMPLATES]))
      self.m_usingColor = True
         
    else:
      self.disable()

  def disable(self):
    """ Disable color output. """
    self.update(dict([(k, self.NoColor) for k,v in self.COLOR_TEMPLATES]))
    self.m_usingColor = False

  def usingColor(self):
    """ usingColor() --> True or False """
    return self.m_usingColor

  def colors(self):
    """ Return list of terminal supported colors. """
    return list(self.keys())

class TermColorWriter:
  """
  Terminal status writer with color.
  """
  def __init__(self, colors=None):
    """
    Initializer.
    
    Parameters:
      colors    TermColors object to bind with.
    """
    self.m_muted = False
    if colors is None:
      self.m_colors = TermColors()
    else:
      self.m_colors = colors

  def mute(self):
    """ Mute terminal writing. """
    self.m_muted = True

  def unmute(self):
    """ Unmute terminal writing. """
    self.m_muted = False

  def isMuted(self):
    """ isMuted() -> True or False """
    return self.m_muted

  def debug(self, msg, **kwargs):
    """
    Print debug message.

    Parameters:
      msg     Debug message.
      kwargs  Keyword arguments to Python3 print function.
    """
    if not self.m_muted:
      self.cprint('darkgray', "DBG: ", 'normal', msg, **kwargs)

  def info(self, msg, **kwargs):
    """
    Print information message.

    Parameters:
      msg     Information message.
      kwargs  Keyword arguments to Python3 print function.
    """
    if not self.m_muted:
      self.cprint('green', msg, **kwargs)

  def warn(self, msg, **kwargs):
    """
    Print warning message.

    Parameters:
      msg     Warning message.
      kwargs  Keyword arguments to Python3 print function.
    """
    if not self.m_muted:
      self.cprint('brown', "Warning: ", 'normal', msg, **kwargs)

  def error(self, msg, **kwargs):
    """
    Print error message.

    Parameters:
      msg     Error message.
      kwargs  Keyword arguments to Python3 print function.
    """
    if not self.m_muted:
      self.cprint('lightred', "Error: ", 'normal', msg, **kwargs)

  def critical(self, msg, **kwargs):
    """
    Print critical error message.

    Parameters:
      msg     Critical error message.
      kwargs  Keyword arguments to Python3 print function.
    """
    if not self.m_muted:
      self.cprint('lightpurple', "Critical: ", 'normal', msg, **kwargs)

  def cprint(self, *args, **kwargs):
    """
    Color print message sequence.

    Note: Not all print_function imports support the flush keyword, so
          this routine uses sys.stdout flush.

    Parameters:
      args    Iterable object of a sequence of color,message pairs.
      kwargs  Keyword arguments to Python3 print function.
    """
    if not self.m_muted:
      concat = ''
      for i in range(0,len(args),2):
        concat += "{}{}{}".format(self.m_colors[args[i]],
                                  args[i+1],
                                  self.m_colors['normal'])
      flush = kwargs.pop('flush', False)
      print("{}".format(concat), **kwargs)
      if flush:
        sys.stdout.flush()
      
  def ncprint(self, msg, **kwargs):
    """
    No color print message sequence.

    Note: Not all print_function imports support the flush keyword.
          this routine uses sys.stdout flush.

    Parameters:
      msg     Plain messge.
      kwargs  Keyword arguments to Python3 print function.
    """
    if not self.m_muted:
      flush = kwargs.pop('flush', False)
      print("{}".format(msg), **kwargs)
      if flush:
        sys.stdout.flush()

  def colors(self):
    """ Return ANSI colors instance TermColors. """
    return self.m_colors.colors()

# -----------------------------------------------------------------------------
# Unit tests
# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import sys
  import tests.utcolor as ut

  sys.exit(ut.utmain())
