from setuptools import setup, find_packages

setup(
    name='Taelcore',  
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
    ],
    author='Ian MORILLA, Kelly Larissa VOMO DONFACK',  
    author_email='ian.morilla@math.univ-paris13.fr',
    description='A library for dimention reduction using autoencoder',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # License type
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',

)