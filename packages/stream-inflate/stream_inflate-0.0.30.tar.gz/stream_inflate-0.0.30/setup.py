from setuptools import setup, Extension
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("stream_inflate.py"),
    # Python 3.6 seems to need all of the below, even though they are in pyproject.toml
    name="stream-inflate",
    version="v0.0.30",
    extras_require={
        'dev': [
            "coverage>=6.2",
            "pytest>=6.2.5",
            "pytest-cov>=3.0.0",
            "Cython>=3.0.0",
            "setuptools",
            "build",
        ]
    },
    py_modules=[
        'stream_inflate',
    ],
)
