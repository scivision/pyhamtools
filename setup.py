#!/usr/bin/env python
install_requires=["pytz","requests","pyephem","beautifulsoup4",]
tests_require=['nose','pytest']

import os
from setuptools import setup,find_packages

exec(open(os.path.join("pyhamtools","version.py")).read())


setup(name='pyhamtools',
      version=__release__,
      description='Collection of Tools for Amateur Radio developers',
      author='Tobias Wellnitz, DH1TW',
      author_email='Tobias@dh1tw.de',
      url='http://github.com/dh1tw/pyhamtools',
      package_data={'': ['countryfilemapping.json']},
      packages=find_packages(),
      install_requires=install_requires,
      tests_require=tests_require,
      extras_require={'tests':tests_require},
      python_requires='>=2.7',
     )
