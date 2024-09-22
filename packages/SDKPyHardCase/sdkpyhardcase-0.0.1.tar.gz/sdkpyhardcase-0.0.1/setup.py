from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='SDKPyHardCase',
  version='0.0.1',
  author='HardCase',
  description='This is the simplest module for work with our SDK',
  long_description=readme(),
  long_description_content_type='text/markdown',
  packages=find_packages(),
  install_requires=[],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='SDK HardCase',
  project_urls={

  },
  python_requires='>=3.11'
)