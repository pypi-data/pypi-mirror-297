from setuptools import setup, find_packages



setup(
  name='open_observe_tracking_django',
  version='0.1',
  packages= find_packages(),
  install_requires=[
    'requests',
    'Django>=4.1.6',
    'celery',

  ]
  

)