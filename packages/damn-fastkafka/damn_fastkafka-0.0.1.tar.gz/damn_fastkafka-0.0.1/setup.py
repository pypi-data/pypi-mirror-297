from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='damn_fastkafka',
  version='0.0.1',
  author='mniyazkhanov@gmail.com',
  author_email='mniyazkhanov@gmail.com',
  description='This is the simplest module for quick work with kafka.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://gitlab.com/nmModi/damn_fastkafka',
  packages=find_packages(),
  install_requires=[],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='kafka fastapi',
  project_urls={},
  python_requires='>=3.11'
)