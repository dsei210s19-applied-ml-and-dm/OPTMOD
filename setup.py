# ****************************************************#
# This file is part of OPTMOD                        #
#                                                    #
# Copyright (c) 2019, Tomas Tinoco De Rubira.        #
#                                                    #
# OPTMOD is released under the BSD 2-clause license. #
# ****************************************************#

import os
import sys
import numpy as np
from subprocess import call
from Cython.Build import cythonize
from setuptools import setup, Extension
import py_compile
from distutils import log
from setuptools.command.build_py import build_py
from setuptools.command.bdist_egg import bdist_egg
from wheel.bdist_wheel import bdist_wheel


# Custom distribution build commands
class bdist_wheel_compiled(bdist_wheel):
    """Small customizations to build compiled only wheel."""
    description = 'build compiled wheel distribution'


class bdist_egg_compiled(bdist_egg):
    """Small customizations to build compiled only egg."""
    description = 'build compiled egg distribution'


if len(sys.argv) > 1 and 'compiled' in sys.argv[1]:

    class build_py(build_py):
        """
        A custom build_py command to exclude source files from packaging and
        include compiled pyc files instead.
        """
        def byte_compile(self, files):
            for file in files:
                full_path = os.path.abspath(file)
                if file.endswith('.py'):
                    log.info("{}  compiling and unlinking".format(file))
                    py_compile.compile(file, cfile=file+'c')
                    os.unlink(file)
                elif file.endswith('pyx') or file.endswith('pxd'):
                    log.info("{}  unlinking".format(file))
                    os.unlink(file)

    extra_cmd_classes = {'bdist_wheel_compiled': bdist_wheel_compiled,
                         'bdist_egg_compiled': bdist_egg_compiled,
                         'build_py': build_py}

else:
    extra_cmd_classes = {'bdist_wheel_compiled': bdist_wheel_compiled,
                         'bdist_egg_compiled': bdist_egg_compiled}

ext_modules = cythonize([Extension(name='optmod.coptmod.coptmod',
                                   sources=['./optmod/coptmod/coptmod.pyx',
                                            './optmod/coptmod/evaluator.c',
                                            './optmod/coptmod/node.c'],
                                   libraries=[],
                                   include_dirs=[np.get_include(), './optmod/coptmod'],
                                   library_dirs=[],
                                   extra_link_args=[])])

setup(name='OPTMOD',
      zip_safe=False,
      version='0.0.1',
      description='Optimization Modeling Library',
      url='',
      author='Tomas Tinoco De Rubira',
      author_email='ttinoco5687@gmail.com',
      include_package_data=True,
      cmdclass=extra_cmd_classes,
      license='BSD 2-Clause License',
      packages=['optmod',
                'optmod.coptmod'],
      install_requires=['cython>=0.20.1',
                        'numpy>=1.11.2',
                        'scipy>=0.18.1',
                        'optalg==1.1.7rc1',
                        'nose'],
      package_data={'optmod': []},
      classifiers=['Development Status :: 5 - Production/Stable',
                   'License :: OSI Approved :: BSD License',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.5'],
      ext_modules=ext_modules)
