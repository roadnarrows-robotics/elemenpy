"""
Light-weight listing of all 94 natural elements.

So light-weight you can invite elements to any party for fun and
hilarity.

Package:
  RoadNarrows elements package.

File:
  elements.py

Link:
  https://github.com/roadnarrows-robotics/

Copyright:
  (c) 2019. RoadNarrows LLC
  http://www.roadnarrows.com
  All Rights Reserved

License:
  MIT
"""

from enum import (Enum, unique)

from elemenpy.core.common import (enumfactory, enum_to_str)

# -----------------------------------------------------------------------------
# ElementZ Enumeration
# -----------------------------------------------------------------------------
@unique
class ElementZ(Enum):
  """ All naturally ocurring elements, uniquely ordered by Z number. """
  UNKNOWN = 0

  HYDROGEN      =  1
  HELIUM        =  2
  LITHIUM       =  3
  BERYLLIUM     =  4
  BORON         =  5
  CARBON        =  6
  NITROGEN      =  7
  OXYGEN        =  8
  FLUORINE      =  9
  NEON          = 10
  SODIUM        = 11
  MAGNESIUM     = 12
  ALUMINUM      = 13
  SILICON       = 14
  PHOSPHORUS    = 15
  SULFUR        = 16
  CHLORINE      = 17
  ARGON         = 18
  POTASSIUM     = 19
  CALCIUM       = 20
  SCANDIUM      = 21
  TITANIUM      = 22
  VANADIUM      = 23
  CHROMIUM      = 24
  MANGANESE     = 25
  IRON          = 26
  COBALT        = 27
  NICKEL        = 28
  COPPER        = 29
  ZINC          = 30
  GALLIUM       = 31
  GERMANIUM     = 32
  ARSENIC       = 33
  SELENIUM      = 34
  BROMINE       = 35
  KRYPTON       = 36
  RUBIDIUM      = 37
  STRONTIUM     = 38
  YTTRIUM       = 39
  ZIRCONIUM     = 40
  NIOBIUM       = 41
  MOLYBDENUM    = 42
  TECHNETIUM    = 43
  RUTHENIUM     = 44
  RHODIUM       = 45
  PALLADIUM     = 46
  SILVER        = 47
  CADMIUM       = 48
  INDIUM        = 49
  TIN           = 50
  ANTIMONY      = 51
  TELLURIUM     = 52
  IODINE        = 53
  XENON         = 54
  CESIUM        = 55
  BARIUM        = 56
  LANTHANUM     = 57
  CERIUM        = 58
  PRASEODYMIUM  = 59
  NEODYMIUM     = 60
  PROMETHIUM    = 61
  SAMARIUM      = 62
  EUROPIUM      = 63
  GADOLINIUM    = 64
  TERBIUM       = 65
  DYSPROSIUM    = 66
  HOLMIUM       = 67
  ERBIUM        = 68
  THULIUM       = 69
  YTTERBIUM     = 70
  LUTETIUM      = 71
  HAFNIUM       = 72
  TANTALUM      = 73
  TUNGSTEN      = 74
  RHENIUM       = 75
  OSMIUM        = 76
  IRIDIUM       = 77
  PLATINUM      = 78
  GOLD          = 79
  MERCURY       = 80
  THALLIUM      = 81
  LEAD          = 82
  BISMUTH       = 83
  POLONIUM      = 84
  ASTATINE      = 85
  RADON         = 86
  FRANCIUM      = 87
  RADIUM        = 88
  ACTINIUM      = 89
  THORIUM       = 90
  PROTACTINIUM  = 91
  URANIUM       = 92
  NEPTUNIUM     = 93
  PLUTONIUM     = 94

# -----------------------------------------------------------------------------
# Element Z, symbol dictionary.
# -----------------------------------------------------------------------------
ElementSymbol = {
  ElementZ.UNKNOWN:       '??',

  ElementZ.HYDROGEN:      'H',
  ElementZ.HELIUM:        'He',
  ElementZ.LITHIUM:       'Li',
  ElementZ.BERYLLIUM:     'Be',
  ElementZ.BORON:         'B',
  ElementZ.CARBON:        'C',
  ElementZ.NITROGEN:      'N',
  ElementZ.OXYGEN:        'O',
  ElementZ.FLUORINE:      'F',
  ElementZ.NEON:          'Ne',
  ElementZ.SODIUM:        'Na',
  ElementZ.MAGNESIUM:     'Mg',
  ElementZ.ALUMINUM:      'Al',
  ElementZ.SILICON:       'Si',
  ElementZ.PHOSPHORUS:    'P',
  ElementZ.SULFUR:        'S',
  ElementZ.CHLORINE:      'Cl',
  ElementZ.ARGON:         'Ar',
  ElementZ.POTASSIUM:     'K',
  ElementZ.CALCIUM:       'Ca',
  ElementZ.SCANDIUM:      'Sc',
  ElementZ.TITANIUM:      'Ti',
  ElementZ.VANADIUM:      'V',
  ElementZ.CHROMIUM:      'Cr',
  ElementZ.MANGANESE:     'Mn',
  ElementZ.IRON:          'Fe',
  ElementZ.COBALT:        'Co',
  ElementZ.NICKEL:        'Ni',
  ElementZ.COPPER:        'Cu',
  ElementZ.ZINC:          'Zn',
  ElementZ.GALLIUM:       'Ga',
  ElementZ.GERMANIUM:     'Ge',
  ElementZ.ARSENIC:       'As',
  ElementZ.SELENIUM:      'Se',
  ElementZ.BROMINE:       'Br',
  ElementZ.KRYPTON:       'Kr',
  ElementZ.RUBIDIUM:      'Rb',
  ElementZ.STRONTIUM:     'Sr',
  ElementZ.YTTRIUM:       'Y',
  ElementZ.ZIRCONIUM:     'Zr',
  ElementZ.NIOBIUM:       'Nb',
  ElementZ.MOLYBDENUM:    'Mo',
  ElementZ.TECHNETIUM:    'Tc',
  ElementZ.RUTHENIUM:     'Ru',
  ElementZ.RHODIUM:       'Rh',
  ElementZ.PALLADIUM:     'Pd',
  ElementZ.SILVER:        'Ag',
  ElementZ.CADMIUM:       'Cd',
  ElementZ.INDIUM:        'In',
  ElementZ.TIN:           'Sn',
  ElementZ.ANTIMONY:      'Sb',
  ElementZ.TELLURIUM:     'Te',
  ElementZ.IODINE:        'I',
  ElementZ.XENON:         'Xe',
  ElementZ.CESIUM:        'Cs',
  ElementZ.BARIUM:        'Ba',
  ElementZ.LANTHANUM:     'La',
  ElementZ.CERIUM:        'Ce',
  ElementZ.PRASEODYMIUM:  'Pr',
  ElementZ.NEODYMIUM:     'Nd',
  ElementZ.PROMETHIUM:    'Pm',
  ElementZ.SAMARIUM:      'Sm',
  ElementZ.EUROPIUM:      'Eu',
  ElementZ.GADOLINIUM:    'Gd',
  ElementZ.TERBIUM:       'Tb',
  ElementZ.DYSPROSIUM:    'Dy',
  ElementZ.HOLMIUM:       'Ho',
  ElementZ.ERBIUM:        'Er',
  ElementZ.THULIUM:       'Tm',
  ElementZ.YTTERBIUM:     'Yb',
  ElementZ.LUTETIUM:      'Lu',
  ElementZ.HAFNIUM:       'Hf',
  ElementZ.TANTALUM:      'Ta',
  ElementZ.TUNGSTEN:      'W',
  ElementZ.RHENIUM:       'Re',
  ElementZ.OSMIUM:        'Os',
  ElementZ.IRIDIUM:       'Ir',
  ElementZ.PLATINUM:      'Pt',
  ElementZ.GOLD:          'Au',
  ElementZ.MERCURY:       'Hg',
  ElementZ.THALLIUM:      'Tl',
  ElementZ.LEAD:          'Pb',
  ElementZ.BISMUTH:       'Bi',
  ElementZ.POLONIUM:      'Po',
  ElementZ.ASTATINE:      'At',
  ElementZ.RADON:         'Rn',
  ElementZ.FRANCIUM:      'Fr',
  ElementZ.RADIUM:        'Ra',
  ElementZ.ACTINIUM:      'Ac',
  ElementZ.THORIUM:       'Th',
  ElementZ.PROTACTINIUM:  'Pa',
  ElementZ.URANIUM:       'U',
  ElementZ.NEPTUNIUM:     'Np',
  ElementZ.PLUTONIUM:     'Pu',
}

# -----------------------------------------------------------------------------
# ElementGroup Enumeration
# -----------------------------------------------------------------------------
@unique
class ElementGroup(Enum):
  """
  Periodic table element groups (vertical columns).

  Systematic group names are typically given by the first element
  in that group.
  """
  UNKNOWN   = 0

  LITHIUM_GROUP   =  1
  BERYLLIUM_GROUP =  2
  SCANDIUM_GROUP  =  3
  TITANIUM_GROUP  =  4
  VANADIUM_GROUP  =  5
  CHROMIUM_GROUP  =  6
  MANGANESE_GROUP =  7
  IRON_GROUP      =  8
  COBALT_GROUP    =  9
  NICKEL_GROUP    = 10
  COPPER_GROUP    = 11
  ZINC_GROUP      = 12
  BORON_GROUP     = 13
  CARBON_GROUP    = 14
  NITROGEN_GROUP  = 15
  OXYGEN_GROUP    = 16
  FLUORINE_GROUP  = 17
  HELIUM_GROUP    = 18

# -----------------------------------------------------------------------------
# ElementPeriod Enumeration
# -----------------------------------------------------------------------------
@unique
class ElementPeriod(Enum):
  """ Periodic table element periods (horizontal rows). """
  UNKNOWN = 0

  PERIOD_1 = 1
  PERIOD_2 = 2
  PERIOD_3 = 3
  PERIOD_4 = 4
  PERIOD_5 = 5
  PERIOD_6 = 6
  PERIOD_7 = 7

  @classmethod
  def min(klass):
    """ Return minimum period value. """
    return klass.P1.value

  @classmethod
  def max(klass):
    """ Return maximum period value. """
    return klass.P7.value

# -----------------------------------------------------------------------------
# ElementBlock Enumeration
# -----------------------------------------------------------------------------
@unique
class ElementBlock(Enum):
  """ Periodic table element blocks (regions). """
  UNKNOWN = '?'

  S = 's'
  D = 'd'
  F = 'f'
  P = 'p'

# -----------------------------------------------------------------------------
# ElementCategory Enumeration
# -----------------------------------------------------------------------------
@unique
class ElementCategory(Enum):
  """ Element categories. """
  UNKNOWN   = 0

  METAL     = 1
  METALLOID = 2
  NONMETAL  = 3

  @classmethod
  def min(klass):
    """ Return minimum category value. """
    return klass.METAL.value

  @classmethod
  def max(klass):
    """ Return maximum category value. """
    return klass.NONMETAL.value

# -----------------------------------------------------------------------------
# ElementSubcategory Enumeration
# -----------------------------------------------------------------------------
@unique
class ElementSubcategory(Enum):
  """ Element subcategories. """
  UNKNOWN               = 0

  ALKALI_METAL          = 1
  ALKALINE_EARTH_METAL  = 2
  LANTHANIDE            = 3
  ACTINIDE              = 4
  TRANSITION_METAL      = 5
  POST_TRANSITION_METAL = 6
  METALLOID             = 7
  REACTIVE_NONMETAL     = 8
  NOBLE_GAS             = 9

  @classmethod
  def min(klass):
    """ Return minimum subcategory value. """
    return klass.ALKALI_METAL.value

  @classmethod
  def max(klass):
    """ Return maximum subcategory value. """
    return klass.NOBLE_GAS.value

# -----------------------------------------------------------------------------
# Functions - Some little lambda's that Mary had.
# -----------------------------------------------------------------------------

# Convert ElementZ enum to associated element atomic number Z.
z_to_z = lambda ez: enumfactory(ElementZ, ez).value

# Create ElementZ enum associated element name string.
z_to_name = lambda ez: enumfactory(ElementZ, ez).name.lower()

# Look up ElementZ enum associated element 1-2 letter symbol string.
z_to_symbol = lambda ez: ElementSymbol[enumfactory(ElementZ, ez)]

# -----------------------------------------------------------------------------
# Unit tests
# -----------------------------------------------------------------------------
if __name__ == "__main__":
  import sys
  import tests.utelements as ut

  sys.exit(ut.utmain())
