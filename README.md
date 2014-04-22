# Simple library checking with SCONS

This collection of library checks is provided as a convenience helper. It 
offers the possibility to perform a platform independent check for the library
(including compilation and execution) and automatically adds command line
configuration options for it.

## Usage

Every library has an assigned library id string. Currently, checks are
implemented for:

- 'boost.numpy',
- 'boost.preprocessor',
- 'boost.python',
- 'boost.serialization',
- 'boost.test',
- 'boost.thread',
- 'python',
- 'numpy',
- 'opencv'.

You can either:

```
import SConsChecks
# call checks directly
SConsChecks.CheckNumPy()
```

or:

```
# import these convenience methods,
from SConsChecks import AddLibOptions, GetLibChecks
# define a list of required checks,
_libs = ['boost.numpy',
         'boost.preprocessor',
         'boost.python',
         'boost.serialization',
         'boost.test',
         'boost.thread',
         'python',
         'numpy',
         'opencv']
# and get a check (name, method) dict.
_checks = GetLibChecks(_libs)

# You can automatically add all command line options to configure the
# libraries as follows:
def setupOptions():
    if platform.system() == 'Windows':
        default_prefix = r'C:\Libraries'
    else:
        default_prefix = "/usr/local"
    AddOption("--prefix-dir", dest="prefix", type="string", nargs=1, action="store",
              metavar="DIR", default=default_prefix, help="installation prefix")
    # ...
    # Add library configuration options.
    AddLibOptions(AddOption, _libs)
```

See the attached sample project for details.


## License and credits

This project is heavily inspired by the build system of boost numpy 
(see https://github.com/ndarray/Boost.NumPy/blob/master/SConscript), which
hass been created by Jim Bosch.

The source code is distributed under the Boost Software License, Version 1.0
(see http://www.boost.org/LICENSE_1_0.txt).
