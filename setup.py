from setuptools import setup
import setuptools

import hidman

setup(name='hidman',
      version=hidman.__version__,
      description=hidman.__description__,
      url='http://github.com/s4hri/hidman',
      author=hidman.__authors__,
      author_email=hidman.__emails__,
      license=hidman.__license__,
      packages=setuptools.find_packages(),
      install_requires=hidman.__requirements__,
      zip_safe=False)
