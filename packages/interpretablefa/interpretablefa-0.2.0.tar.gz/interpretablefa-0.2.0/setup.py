from setuptools import setup, find_packages
from os import path
working_directory = path.abspath(path.dirname(__file__))

with open(path.join(working_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='interpretablefa',
    version='0.2.0',
    author='Justin Philip Tuazon, Gia Mizrane Abubo',
    description='A package for interpretable factor analysis',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    license='MIT',
    install_requires=[
        'numpy',
        'pandas',
        'factor_analyzer',
        'tensorflow_hub',
        'scipy',
        'nlopt',
        'seaborn',
        'matplotlib'
    ],
    python_requires=">=3.8",
    classifiers=[
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering"
    ]
)
