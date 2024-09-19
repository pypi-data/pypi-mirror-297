project('spheroidalwavefunctions',
        ['c', 'fortran'],
        version : '0.1',
        meson_version: '>= 1.1.0',
        default_options : [
                            'warning_level=1',
                            'buildtype=release'
                          ])
fc = meson.get_compiler('fortran')

# The intel compilers for windows give stack overflows, so allocate on the heap
if fc.get_id() == 'intel-llvm-cl' or fc.get_id() == 'intel-cl'
  extra_f_args = ['/heap-arrays']
else
  extra_f_args = []
endif

py = import('python').find_installation(pure: false)
py_dep = py.dependency()

incdir_numpy = run_command(py,
  ['-c', 'import os; os.chdir(".."); import numpy; print(numpy.get_include())'],
  check : true
).stdout().strip()

incdir_f2py = run_command(py,
    ['-c', 'import os; os.chdir(".."); import numpy.f2py; print(numpy.f2py.get_include())'],
    check : true
).stdout().strip()

inc_np = include_directories(incdir_numpy)
np_dep = declare_dependency(include_directories: inc_np)

incdir_f2py = incdir_numpy / '..' / '..' / 'f2py' / 'src'
inc_f2py = include_directories(incdir_f2py)
fortranobject_c = incdir_f2py / 'fortranobject.c'

inc_np = include_directories(incdir_numpy, incdir_f2py)
# gh-25000
quadmath_dep = fc.find_library('quadmath', required: false)

py.extension_module('spheroidalwavefunctions',
                     ['''prolate_swf.f90''', '''spheroidalwavefunctionsmodule.c''',
                     '''spheroidalwavefunctions-f2pywrappers2.f90''', fortranobject_c],
                     include_directories: [inc_np,],
                     dependencies : [py_dep, quadmath_dep,],
                     fortran_args : extra_f_args,
                     install : true)
