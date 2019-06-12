from os.path import abspath, dirname, join
from setuptools import setup


CURDIR = dirname(abspath(__file__))

DESCRIPTION = """
Screen comparation library for robot framework
"""[1:-1]

with open(join(CURDIR, 'requirements.txt')) as f:
    REQUIREMENTS = f.read().splitlines()

setup(name='robotframework-ScreenCompareLibrary',
      version='0.0.1',
      description='Screen compare library',
      long_description=DESCRIPTION,
      author='Tomas Pekarovic',
      author_email='<tomas.pekarovic@gmail.com>',
      url='',
      license='Apache License 2.0',
      keywords='robot framework test automation screen comparision',
      platforms='any',
      classifiers=[
                       "Development Status :: 3 - Alpha",
                       "License :: OSI Approved :: Apache Software License",
                       "Operating System :: OS Independent",
                       "Programming Language :: Python",
                       "Topic :: Software Development :: Testing"
                  ],
      install_requires=REQUIREMENTS,
      package_dir={'': 'src'},
      packages=['ScreenCompareLibrary', 'ScreenCompareLibrary.keywords',
                'ScreenCompareLibrary.utils'],
      include_package_data=True
      )
