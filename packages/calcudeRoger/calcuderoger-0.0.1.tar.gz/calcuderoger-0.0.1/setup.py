from setuptools import setup, find_packages


setup( 
    name='calcudeRoger', 
    version='0.0.1',
    packages=['calcudeRoger'],
    author='Roger', 
    description= 'Simple test package', 
    long_description=open("README.md","r", encoding="utf-8").read(),
    install_requires=['CoolProp'],
)
