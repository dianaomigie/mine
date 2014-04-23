from setuptools import setup, Extension
from Cython.Distutils import build_ext

import os
import sys
import platform
if platform.system() == "Darwin":
    # openmp doesn't work with clang, the default OSX C compiler
    os.environ["CC"] = "gcc-4.2"
    os.environ["LDSHARED"] = "gcc-4.2"
    os.environ["OMP_NUM_THREADS"] = "4"
    os.environ["LDFLAGS"] = "-shared -lpython2.7 -I/usr/include/python2.7/"

script_args = ['build_ext', '--inplace']
script_args.extend(sys.argv[1:])

build_table_mem_efficient = Extension(
    'radiotool.algorithms.build_table_mem_efficient',
    ['radiotool/algorithms/build_table_mem_efficient.pyx'],
    extra_compile_args=['-O3'])
par_build_table = Extension(
    'radiotool.algorithms.par_build_table',
    ['radiotool/algorithms/par_build_table.pyx'],
    extra_compile_args=['-fopenmp', '-O3'], extra_link_args=['-fopenmp'])
build_table_full_backtrace = Extension(
    'radiotool.algorithms.build_table_full_backtrace',
    ['radiotool/algorithms/build_table_full_backtrace.pyx'],
    extra_compile_args=['-O3'])

setup(
    name='radiotool',
    version='0.4.0',
    description='Tools for constructing and retargeting audio',
    long_description=open('README.rst').read(),
    url='https://github.com/ucbvislab/radiotool',
    author='Steve Rubin',
    author_email='srubin@cs.berkeley.edu',
    packages=[
        'radiotool',
        'radiotool.composer',
        'radiotool.algorithms'
    ],
    ext_modules=[
        build_table_mem_efficient,
        par_build_table,
        build_table_full_backtrace
    ],
    cmdclass={'build_ext': build_ext},
    script_args=script_args,
    license='GPL v3',
    install_requires=[
        'numpy',
        'scipy',
        'scikits.audiolab',
        'librosa'
    ],
    #      extras_require=[
    #            'python-xmp-toolkit'
    #      ],
    # zip_safe=False,
    # test_suite='nose.collector',
    # tests_require=['nose']
)
