from setuptools import setup

setup(name='tinyErrands',
      version='1.0',
      description='OpenShift App',
      author='Your Name',
      author_email='example@example.com',
      url='http://www.python.org/sigs/distutils-sig/',
#      install_requires=['Django>=1.3'],
     install_requires=['flask==0.10.1','sqlalchemy==0.8.2','flask-sqlalchemy==1.0'],
     )
