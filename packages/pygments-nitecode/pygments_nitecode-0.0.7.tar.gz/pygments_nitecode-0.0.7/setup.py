#!/usr/bin/env python
from setuptools import setup, find_packages

entry_points = '''
[pygments.lexers]
nitecode=pygments_nitecode:NiteCodeLexer
'''

setup(
    name='pygments-nitecode',
    version='0.0.7',
    description='Pygments lexer package for NiteCode language.',
	# long_description=open('README.rst').read(),
    author='NiTiSon',
    url='https://github.com/NiTiSon/pygment_nitecode',
    packages=find_packages(),
    entry_points=entry_points,
    install_requires=[
        'Pygments>=2.0.1'
    ],
    zip_safe=True,
    license='MIT License',
    classifiers=[
        'Environment :: Plugins',
        'License :: OSI Approved :: MIT License'
    ],
)