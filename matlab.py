# -*- python -*-
#
# Copyright Christoph Lassner 2014.
#
# Distributed under the Boost Software License, Version 1.0.
#    (See http://www.boost.org/LICENSE_1_0.txt)
from __future__ import print_function
from ._tools import _checkLibs, _setupPaths
from SCons.SConf import CheckContext
CheckContext.checkLibs = _checkLibs
import os

_check_dict = {}
_matlab_option_dict = {'--matlab-dir':
                       {'dest':"matlab_prefix",
                       'type':"string",
                       'nargs':1,
                       'action':"store",
                       'metavar':"DIR",
                       'default':os.environ.get("MATLAB_ROOT"),
                       'help':"prefix for Matlab; should contain the 'extern' folder."},
                       '--matlab-inc-dir':
                       {'dest':"matlab_include",
                       'type':"string",
                       'nargs':1,
                       'action':"store",
                       'metavar':"DIR",
                       'help':"this folder should contain 'mex.h'.",
                       'default':os.environ.get("MATLAB_INCLUDE_DIR")},
                       '--matlab-lib-dir':
                       {'dest':"matlab_lib",
                       'type':"string",
                       'nargs':1,
                       'action':"store",
                       'metavar':"DIR",
                       'help':"this folder should contain 'libmex.lib'.",
                       'default':os.environ.get("MATLAB_LIB_DIR")}}

def CheckMatlab(context):
    matlab_source_file = r"""
#include <mex.h>
void mexFunction(int nlhs, mxArray* plhs[], int nrhs, const mxArray* prhs[]) {
    if (nrhs != 1)  {
        mexErrMsgTxt("One input required.");
    } 
    else if (nlhs > 1) {
        mexErrMsgTxt("Too many output arguments");
    }    
    /* The input must be a noncomplex scalar integer.*/
    int mrows, ncols;
    mrows = mxGetM(prhs[0]);
    ncols = mxGetN(prhs[0]);
    if (!mxIsDouble(prhs[0]) || mxIsComplex(prhs[0]) || 
        !(mrows == 1 && ncols == 1)) {
        mexErrMsgTxt("Input must be a noncomplex scalar integer.");
    }
    double x, *y;
    x = mxGetScalar(prhs[0]);
    /* Create matrix for the return argument. */
    plhs[0] = mxCreateDoubleMatrix(mrows /* 1 */, ncols, mxREAL);
}
int main() {
    return 0;
}
"""
    context.Message('Check building with MATLAB... ')
    matlab_root = context.env.GetOption("matlab_prefix")
    matlab_ex_inc = context.env.GetOption("matlab_include")
    matlab_ex_lib = context.env.GetOption("matlab_lib")
    if os.name == 'nt':
        lib_add_dir = r'extern\lib\win64\microsoft'
    else:
        lib_add_dir = 'extern/lib'
    _setupPaths(context.env,
        prefix = matlab_root,
        include = matlab_ex_inc,
        lib = matlab_ex_lib,
        include_add_dir = os.path.join('extern', 'include'),
        lib_add_dir = lib_add_dir
        )
    result = context.checkLibs(['libmx.lib',
                                'libmat.lib',
                                'libmex.lib'], matlab_source_file)
    if not result:
        context.Result(0)
        print("Cannot build with MATLAB.")
        return False
    result, output = context.TryRun(matlab_source_file, '.cpp')
    if not result:
        context.Result(0)
        print("Cannot run program built with MATLAB.")
        return False
    context.Result(1)
    return True
_check_dict['matlab'] = {'options': _matlab_option_dict,
                         'checks': [CheckMatlab]}
