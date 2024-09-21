from setuptools import setup, find_packages
from setuptools.command.build_ext import build_ext
import os
import cffi
from setuptools import setup, find_packages
from setuptools.command.build_ext import build_ext
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INCLUDE_DIRS = [os.path.join(BASE_DIR, 'src/package_FUNNY/c_code')]
SOURCES = [os.path.join(BASE_DIR, 'src/package_FUNNY/c_code/matrix_library.c')]


def build_cffi_module():
    ffi = cffi.FFI()

    ffi.cdef("""
        double* matrix_multiply(double *A, double *B, double *C, int m, int n, int p);
        double* matrix_transpose(double *A, double *B, int m, int n);
        double* matrix_add(double *A, double *B, double *C, int m, int n);
    """)

    ffi.set_source(
        'matrix_library_calculation',
        '#include "matrix_library.h"',
        include_dirs=INCLUDE_DIRS,
        sources=SOURCES,
        libraries=[],  # 'stdlib'
    )

    ffi.compile(target=os.path.join(BASE_DIR, 'src/package_FUNNY/PYPILibrary/matrix_library_calculation'))


# C:\Program Files\JetBrains\PyCharm Community Edition 2021.3.2\plugins\python-ce\helpers\typeshed\stubs\setuptools\setuptools\command\build_ext.pyi
class CFFIBuildExt(build_ext):
    def run(self):
        build_cffi_module()
        super().run()


print(isinstance(CFFIBuildExt, build_ext))
build_cffi_module()

setup(
    name="package_FUNNY",
    version="0.1.0",
    description="A Python package for advanced matrix calculations",
    long_description="README.md",
    long_description_content_type="text/markdown",
    author="Il tuo Nome",
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={"package_FUNNY": ["c_code/*"]},
    python_requires='>=3.11',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: C",
        "Programming Language :: Python :: Implementation :: CPython",
        "Operating System :: OS Independent",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    cmdclass={
        'build_ext': build_ext,
        # il dizionario deve mappare stringhe (nomi dei comandi) a classi che estendono setuptools.Command
    },
    install_requires=[  # Durante l'installazione del pacchetto.
        'setuptools>=61.0',
        'wheel',
        'cffi>=1.0.0'
    ],
    setup_requires=[  # Durante il processo di setup, prima che il pacchetto venga installato.: toml
        'cffi>=1.0.0',
    ],
    zip_safe=False,
    #project_urls={ "Source Code": "https://github.com/enricozanardo/matrix"}
)
