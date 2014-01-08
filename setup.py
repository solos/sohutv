
#!/usr/bin/python
#coding=utf-8

import sys
sys.path.append('./src')

from distutils.core import setup
from sohutv import __version__

setup(name='sohutv',
      version=__version__,
      description='A python empty project',
      long_description=open('README.md').read(),
      author='solos',
      author_email='solos@solos.so',
      packages=['sohutv'],
      package_dir={'sohutv': 'src/sohutv'},
      package_data={'sohutv': ['stuff']},
      license='MIT',
      platforms=['any'],
      url='https://github.com/solos/sohutv')
