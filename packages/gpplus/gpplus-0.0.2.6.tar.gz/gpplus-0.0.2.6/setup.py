from setuptools import setup, find_packages

setup(
    name='gpplus',
    version='0.0.2.6',
    author='Amin Yousefpour, Ramin Bostanabad',
    author_email='yousefpo@uci.edu',
    description='Python Library for Generalized Gaussian Process Modeling',
    # long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Bostanabad-Research-Group/GP-Plus',
    packages=find_packages(),
    install_requires=[
        'numpy==1.24.2',
        'scipy==1.11.1',
        'gpytorch==1.7.0',
        'matplotlib==3.7.1',
        'sobol_seq', 
        'tabulate==0.9.0',
        'pandas==1.5.2',
        'dill ==0.3.7',
        'pyro-ppl==1.8.0',
        'pyDOE',
        'botorch==0.6.4',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
