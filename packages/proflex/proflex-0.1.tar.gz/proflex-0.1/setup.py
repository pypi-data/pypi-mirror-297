from setuptools import setup, find_packages

setup(
    name="proflex",
    version="0.1",
    description="A package for ProFlex creation adn manipulation",
    author="Damian Magill",
    author_email="damian.magill@iff.com",
    packages=find_packages(),
    install_requires=[
        "numpy",  
    ],
    extras_require={
        "pdb_analysis": ["prody"],         
        "biopython_tools": ["biopython"],   
        "visualization": ["pymol2"],       
    },
    entry_points={
        'console_scripts': [
            'proflex-query=proflex.proflex:ProFlexQuery',
        ],
    },
)

