# -*- python -*-
#
# These SCons tests are based on the ones of boost numpy 
# (https://github.com/ndarray/Boost.NumPy/blob/master/SConscript),
# but have been altered and substantially extended.
#
# Copyright Christoph Lassner 2014.
# For the python, numpy and boost python checks, _setupPaths and _checkLibs:
# Copyright Jim Bosch 2010-2012.
#
# Distributed under the Boost Software License, Version 1.0.
#    (See http://www.boost.org/LICENSE_1_0.txt)


import platform
import os

from _tools import _checkLibs, _setupPaths
from SCons.SConf import CheckContext
CheckContext.checkLibs = _checkLibs

_check_dict = {}
_opencv_option_dict = {'--opencv-dir':
                        {'dest':"opencv_prefix",
                        'type':"string",
                        'nargs':1,
                        'action':"store",
                        'metavar':"DIR",
                        'default':os.environ.get("OPENCV_ROOT"),
                        'help':"prefix for OpenCV libraries; should have 'include' and 'lib' subdirectories"},
                        '--opencv-inc-dir':
                        {'dest':"opencv_include",
                        'type':"string",
                        'nargs':1,
                        'action':"store",
                        'metavar':"DIR",
                        'help':"location of OpenCV header files",
                        'default':os.environ.get("OPENCV_INCLUDE_DIR")},
                        '--boost-lib-dir':
                        {'dest':"opencv_lib",
                        'type':"string",
                        'nargs':1,
                        'action':"store",
                        'metavar':"DIR",
                        'help':"location of OpenCV libraries",
                        'default':os.environ.get("OPENCV_LIB_DIR")},
                        '--opencv-version':
                        {'dest':"opencv_version",
                        'type':"string",
                        'nargs':1,
                        'action':"store",
                        'metavar':"DIR",
                        'help':"opencv version, without dots, e.g. 248",
                        'default':os.environ.get("OPENCV_VERSION")}}

def CheckOpenCV(context):
    opencv_source_file = r"""
#include <opencv2/opencv.hpp>

int main()
{
  auto test = cv::Mat::eye(5, 5, CV_64F);
  return 0;
}
"""
    context.Message('Check building against OpenCV... ')
    _setupPaths(context.env,
        prefix = context.env.GetOption("opencv_prefix"),
        include = context.env.GetOption("opencv_include"),
        lib = context.env.GetOption("opencv_lib")
        )
    if context.env.GetOption("debug_checks"):
      libsuffix = 'd'
    else:
      libsuffix = ''
    if platform.system() == 'Windows':
        result = (context.checkLibs(['opencv_imgproc' + context.env.GetOption("opencv_version") + libsuffix,
                                     'opencv_highgui' + context.env.GetOption("opencv_version") + libsuffix,
                                     'opencv_core' + context.env.GetOption("opencv_version") + libsuffix], opencv_source_file))
    else:
        result = (context.checkLibs(['opencv_imgproc' + libsuffix,
                                     'opencv_highgui' + libsuffix,
                                     'opencv_core' + libsuffix], opencv_source_file))
    if not result:
        context.Result(0)
        print "Cannot build against OpenCV."
        return False
    result, output = context.TryRun(opencv_source_file, '.cpp')
    if not result:
        context.Result(0)
        print "Cannot run program built against OpenCV."
        return False
    context.Result(1)
    return True
_check_dict['opencv'] = {'options': _opencv_option_dict,
                         'checks': [CheckOpenCV]}